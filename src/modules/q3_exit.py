"""Q3 - Exit from Phase 2 and inversion stop-conditions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.core.canonical_metrics import build_canonical_hourly_panel
from src.core.market_proxy import MarketProxyBucketModel
from src.modules.common import assumptions_subset
from src.modules.q1_transition import run_q1, stage2_active_from_metrics
from src.modules.q2_slope import run_q2
from src.modules.reality_checks import build_common_checks
from src.modules.result import ModuleResult

Q3_PARAMS = [
    "trend_window_years",
    "require_recent_stage2",
    "stage2_recent_h_negative_min",
    "stage2_recent_h_negative_min_scen",
    "stage2_recent_sr_energy_min_scen",
    "trend_h_negative_max",
    "trend_capture_ratio_min",
    "h_negative_target",
    "h_below_5_target",
    "sr_energy_target",
    "far_target",
    "demand_k_max",
    "slope_capture_target",
]

Q3_OUTPUT_SCHEMA_VERSION = "2.0.0"


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


def _trend_slope(year: pd.Series, value: pd.Series) -> float:
    x = pd.to_numeric(year, errors="coerce")
    y = pd.to_numeric(value, errors="coerce")
    tmp = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(tmp) < 2:
        return np.nan
    x0 = float(tmp["x"].iloc[0])
    x1 = float(tmp["x"].iloc[-1])
    y0 = float(tmp["y"].iloc[0])
    y1 = float(tmp["y"].iloc[-1])
    dx = x1 - x0
    if abs(dx) < 1e-12:
        return np.nan
    return float((y1 - y0) / dx)


def _parse_family_set(raw: Any) -> set[str]:
    txt = str(raw or "").strip()
    if not txt:
        return set()
    return {part.strip().upper() for part in txt.split(",") if part.strip()}


def _row_family_state(row: pd.Series) -> dict[str, bool]:
    return {
        "LOW_PRICE": bool(row.get("low_price_family", False)),
        "PHYSICAL": bool(row.get("physical_family", False)),
        "VALUE_PV": bool(row.get("value_family_pv", row.get("flag_capture_pv_low", False))),
        "VALUE_WIND": bool(row.get("value_family_wind", row.get("flag_capture_wind_low", False))),
    }


def _families_active_at_bascule(country_summary_row: pd.Series | None, fallback_row: pd.Series | None) -> set[str]:
    if country_summary_row is not None:
        for col in ["families_active_at_bascule_country", "families_active_at_bascule_pv", "families_active_at_bascule_wind"]:
            fam = _parse_family_set(country_summary_row.get(col, ""))
            if fam:
                return fam
    if fallback_row is None:
        return set()
    state = _row_family_state(fallback_row)
    return {k for k, v in state.items() if v}


def _two_year_persistence_off(non_crisis_rows: pd.DataFrame, active_at_bascule: set[str]) -> bool:
    if non_crisis_rows.empty or not active_at_bascule:
        return False
    seq: list[bool] = []
    for _, row in non_crisis_rows.sort_values("year").iterrows():
        state = _row_family_state(row)
        turned_off = [(fam in state) and (not state[fam]) for fam in active_at_bascule]
        seq.append(bool(any(turned_off)))
    if len(seq) < 2:
        return False
    return bool(seq[-1] and seq[-2])


def _low_price_flag_from_metrics(h_negative: float, h_below_5: float, low_price_share: float, params: dict[str, float]) -> bool:
    h_neg_thr = float(params.get("h_negative_stage2_min", 200.0))
    h_low_thr = float(params.get("h_below_5_stage2_min", 500.0))
    return bool(
        (np.isfinite(h_negative) and h_negative >= h_neg_thr)
        or (np.isfinite(h_below_5) and h_below_5 >= h_low_thr)
    )


def _physical_flag_from_metrics(sr_energy: float, sr_hours: float, ir_p10: float, params: dict[str, float]) -> bool:
    sr_e_thr = float(params.get("sr_energy_stage2_min", params.get("sr_energy_material_min", 0.01)))
    sr_h_thr = float(params.get("sr_hours_stage2_min", 0.10))
    ir_thr = float(params.get("ir_p10_stage2_min", 1.5))
    return bool(
        (np.isfinite(sr_energy) and sr_energy >= sr_e_thr)
        or (np.isfinite(sr_hours) and sr_hours >= sr_h_thr)
        or (np.isfinite(ir_p10) and ir_p10 >= ir_thr)
    )


def _required_mustrun_reduction(last_row: pd.Series, params: dict[str, float], max_reduction: float = 1.0) -> tuple[float, str]:
    h_neg_0 = _safe_float(last_row.get("h_negative_obs"), np.nan)
    h_low_0 = _safe_float(last_row.get("h_below_5_obs"), np.nan)
    low_share_0 = _safe_float(last_row.get("low_price_hours_share"), np.nan)
    if not np.isfinite(low_share_0):
        n_hours = _safe_float(last_row.get("n_hours_expected"), np.nan)
        if np.isfinite(n_hours) and n_hours > 0 and np.isfinite(h_low_0):
            low_share_0 = h_low_0 / n_hours
    sr_energy_0 = _safe_float(last_row.get("sr_energy_share_gen", last_row.get("sr_energy")), np.nan)
    sr_hours_0 = _safe_float(last_row.get("sr_hours_share", last_row.get("sr_hours")), np.nan)
    ir_0 = _safe_float(last_row.get("ir_p10"), np.nan)

    low_0 = _low_price_flag_from_metrics(h_neg_0, h_low_0, low_share_0, params)
    phys_0 = _physical_flag_from_metrics(sr_energy_0, sr_hours_0, ir_0, params)
    if (not low_0) or (not phys_0):
        return 0.0, "already_not_phase2_stress"

    r_max = float(np.clip(max_reduction, 0.0, 1.0))
    if r_max <= 0.0:
        return np.nan, "beyond_plausible_bounds"

    def _condition(r: float) -> bool:
        rr = float(np.clip(r, 0.0, 1.0))
        h_neg = h_neg_0 * (1.0 - 0.80 * rr) if np.isfinite(h_neg_0) else np.nan
        h_low = h_low_0 * (1.0 - 0.70 * rr) if np.isfinite(h_low_0) else np.nan
        low_share = low_share_0 * (1.0 - 0.70 * rr) if np.isfinite(low_share_0) else np.nan
        sr_energy = sr_energy_0 * (1.0 - 0.60 * rr) if np.isfinite(sr_energy_0) else np.nan
        sr_hours = sr_hours_0 * (1.0 - 0.55 * rr) if np.isfinite(sr_hours_0) else np.nan
        ir = ir_0 * (1.0 - rr) if np.isfinite(ir_0) else np.nan
        low_flag = _low_price_flag_from_metrics(h_neg, h_low, low_share, params)
        phys_flag = _physical_flag_from_metrics(sr_energy, sr_hours, ir, params)
        return (not low_flag) or (not phys_flag)

    if not _condition(r_max):
        return np.nan, "beyond_plausible_bounds"

    lo = 0.0
    hi = r_max
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if _condition(mid):
            hi = mid
        else:
            lo = mid
        if abs(hi - lo) <= 1e-4:
            break
    return float(hi), "ok"


def _infer_historical_bascule_summary(
    annual_df: pd.DataFrame,
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
) -> pd.DataFrame:
    mode = str(selection.get("mode", "HIST")).upper()
    if mode != "SCEN":
        return pd.DataFrame()

    hist_candidates = [
        Path("data/metrics/annual_metrics.parquet"),
        Path("data/metrics/annual_metrics.csv"),
    ]
    hist_df = pd.DataFrame()
    for p in hist_candidates:
        if p.exists() and p.suffix.lower() == ".parquet":
            hist_df = pd.read_parquet(p)
            break
        if p.exists() and p.suffix.lower() == ".csv":
            hist_df = pd.read_csv(p)
            break
    if hist_df.empty:
        return hist_df

    countries = selection.get("countries", sorted(annual_df["country"].dropna().astype(str).unique().tolist()))
    hist_df = hist_df[hist_df["country"].astype(str).isin([str(c) for c in countries])].copy()
    if hist_df.empty:
        return hist_df

    hist_q1 = run_q1(
        hist_df,
        assumptions_df,
        {"countries": countries, "mode": "HIST"},
        run_id=f"{run_id}_Q1_HIST_REF",
    )
    return hist_q1.tables.get("Q1_country_summary", pd.DataFrame()).copy()


def _additional_sink_power_p95(
    hourly_by_country_year: dict[tuple[str, int], pd.DataFrame],
    country: str,
    year: float,
    additional_absorbed_needed_twh_year: float,
) -> tuple[float, str]:
    add_twh = _safe_float(additional_absorbed_needed_twh_year, np.nan)
    if not np.isfinite(add_twh):
        return np.nan, "insufficient_additional_energy"
    if add_twh <= 0.0:
        return 0.0, "no_additional_energy_required"
    y = int(_safe_float(year, np.nan)) if np.isfinite(_safe_float(year, np.nan)) else None
    if y is None:
        return np.nan, "invalid_reference_year"
    h = hourly_by_country_year.get((str(country), y))
    if h is None or h.empty:
        return np.nan, "hourly_profile_unavailable"

    surplus = pd.to_numeric(h.get("surplus_mw", h.get("surplus_unabsorbed_mw")), errors="coerce").fillna(0.0).clip(lower=0.0)
    weights = surplus.copy()
    if float(weights.sum()) <= 0.0:
        price = pd.to_numeric(h.get("price_da_eur_mwh"), errors="coerce")
        weights = (price < 0.0).astype(float)
    w_sum = float(weights.sum())
    if w_sum <= 0.0:
        return np.nan, "hourly_profile_unavailable"

    add_mwh = add_twh * 1e6
    profile = weights / w_sum * add_mwh
    p95 = _safe_float(pd.to_numeric(profile, errors="coerce").quantile(0.95), np.nan)
    if not np.isfinite(p95):
        return np.nan, "hourly_profile_unavailable"
    return max(0.0, p95), "profile_weighted_surplus"


def _safe_series(df: pd.DataFrame, col: str, default: float = 0.0) -> pd.Series:
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    return pd.Series(default, index=df.index, dtype=float)


def _top_risk_bucket_ids(model: MarketProxyBucketModel, top_n: int = 4) -> set[int]:
    stats = model.bucket_stats.copy()
    if stats.empty:
        return set()
    stats["risk_score"] = (
        0.7 * pd.to_numeric(stats.get("p_neg"), errors="coerce").fillna(0.0)
        + 0.3 * pd.to_numeric(stats.get("p_low"), errors="coerce").fillna(0.0)
    )
    ranked = stats.sort_values(["risk_score", "p_neg", "p_low"], ascending=[False, False, False]).head(max(1, int(top_n)))
    return set(pd.to_numeric(ranked.get("bucket_id"), errors="coerce").dropna().astype(int).tolist())


def _compute_hourly_proxy_metrics(
    hourly: pd.DataFrame,
    *,
    market_proxy_model: MarketProxyBucketModel | None = None,
    risk_bucket_ids: set[int] | None = None,
    demand_uplift: float = 0.0,
    demand_uplift_mw: float | None = None,
    export_uplift: float = 0.0,
    export_uplift_mw: float | None = None,
    flex_mw_additional: float = 0.0,
    export_coincidence_factor: float = 1.0,
) -> dict[str, float]:
    if hourly is None or hourly.empty:
        return {"status": "missing_data"}

    canonical = build_canonical_hourly_panel(hourly)
    if canonical.empty:
        return {"status": "missing_data"}

    if market_proxy_model is None:
        try:
            market_proxy_model = MarketProxyBucketModel.fit_baseline(hourly, eps=1e-6)
        except Exception:
            return {"status": "missing_data", "reason": "market_proxy_invalid"}

    features_before = market_proxy_model._extract_features(hourly, eps=1e-6)
    load = pd.to_numeric(canonical.get("load_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
    vre = pd.to_numeric(canonical.get("gen_vre_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
    must_run = pd.to_numeric(canonical.get("must_run_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
    residual_base = pd.to_numeric(features_before.get("residual_load_mw"), errors="coerce").fillna(0.0)
    export_base = pd.to_numeric(canonical.get("exports_net_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
    assigned_before = market_proxy_model.assign_buckets(features_before)
    if risk_bucket_ids is None:
        risk_bucket_ids = _top_risk_bucket_ids(market_proxy_model, top_n=4)
    stress_mask = assigned_before["bucket_id"].isin(risk_bucket_ids).fillna(False).astype(float)
    surplus_base = (-residual_base).clip(lower=0.0)

    avg_load = _safe_float(load.mean(), 0.0)
    export_ref = _safe_float(export_base.quantile(0.95), np.nan)
    if not np.isfinite(export_ref) or export_ref <= 0.0:
        export_ref = max(1.0, _safe_float(export_base.mean(), 1.0))

    demand_mw = _safe_float(demand_uplift_mw, np.nan)
    if not np.isfinite(demand_mw):
        raw = max(0.0, _safe_float(demand_uplift, 0.0))
        demand_mw = raw * avg_load if raw <= 3.0 else raw
    demand_mw = max(0.0, float(demand_mw))

    export_mw = _safe_float(export_uplift_mw, np.nan)
    if not np.isfinite(export_mw):
        raw = max(0.0, _safe_float(export_uplift, 0.0))
        export_mw = raw * export_ref if raw <= 3.0 else raw
    export_mw = max(0.0, float(export_mw))

    flex_mw = max(0.0, _safe_float(flex_mw_additional, 0.0))
    coincidence = max(0.0, _safe_float(export_coincidence_factor, 1.0))

    demand_series = pd.Series(demand_mw, index=load.index, dtype=float)
    export_series = ((surplus_base > 0.0).astype(float) * export_mw * coincidence).astype(float)
    if export_base.notna().any():
        export_series = export_series.where((export_base > 0.0) | (surplus_base > 0.0), 0.0)
    flex_series = (stress_mask * flex_mw).astype(float)

    load_after = (load + demand_series + export_series + flex_series).clip(lower=0.0)
    residual_after = load_after - vre - must_run
    ir_after = must_run / np.maximum(load_after, 1e-6)
    surplus_after = (-residual_after).clip(lower=0.0)

    unabsorbed_energy = float(pd.to_numeric(surplus_after, errors="coerce").fillna(0.0).clip(lower=0.0).sum())
    surplus_energy_before = float(pd.to_numeric(surplus_base, errors="coerce").fillna(0.0).clip(lower=0.0).sum())
    load_energy = float(pd.to_numeric(load_after, errors="coerce").fillna(0.0).clip(lower=0.0).sum())
    sr_energy_after = (unabsorbed_energy / load_energy) if load_energy > 0.0 else np.nan
    sr_energy_after = float(np.clip(sr_energy_after, 0.0, 1.0)) if np.isfinite(sr_energy_after) else np.nan
    sr_hours_after = float((pd.to_numeric(surplus_after, errors="coerce").fillna(0.0) > 0.0).mean())
    far_after = 1.0 if surplus_energy_before <= 0.0 else float(np.clip(1.0 - (unabsorbed_energy / max(surplus_energy_before, 1e-12)), 0.0, 1.0))

    features_after = pd.DataFrame(
        {
            "spot_price_eur_mwh": pd.to_numeric(features_before.get("spot_price_eur_mwh"), errors="coerce"),
            "load_mw": load_after,
            "vre_gen_mw": vre,
            "must_run_mw": must_run,
            "residual_load_mw": residual_after,
            "ir_hour": ir_after,
            "pv_gen_mw": pd.to_numeric(features_before.get("pv_gen_mw"), errors="coerce").fillna(0.0).clip(lower=0.0),
            "wind_gen_mw": pd.to_numeric(features_before.get("wind_gen_mw"), errors="coerce").fillna(0.0).clip(lower=0.0),
        },
        index=features_before.index,
    )
    est_after = market_proxy_model.estimate_from_features(features_after)
    h_negative_est_after = _safe_float(est_after.get("h_negative_est"), np.nan)
    h_below5_est_after = _safe_float(est_after.get("h_below_5_est"), np.nan)
    if np.isfinite(h_negative_est_after) and np.isfinite(h_below5_est_after) and h_below5_est_after < h_negative_est_after:
        h_below5_est_after = h_negative_est_after

    return {
        "status": "ok",
        "demand_uplift_mw": demand_mw,
        "export_uplift_mw": export_mw,
        "flex_uplift_mw": flex_mw,
        "sr_energy_after": sr_energy_after,
        "sr_hours_after": sr_hours_after,
        "far_after": far_after,
        "h_negative_est_after": h_negative_est_after,
        "h_below_5_est_after": h_below5_est_after,
        "baseload_price_est_after": _safe_float(est_after.get("baseload_price_est"), np.nan),
        "pv_capture_price_est_after": _safe_float(est_after.get("pv_capture_price_est"), np.nan),
        "wind_capture_price_est_after": _safe_float(est_after.get("wind_capture_price_est"), np.nan),
        "capture_ratio_pv_est_after": _safe_float(est_after.get("capture_ratio_pv_est"), np.nan),
        "capture_ratio_wind_est_after": _safe_float(est_after.get("capture_ratio_wind_est"), np.nan),
        # Legacy aliases.
        "h_negative_proxy_after": h_negative_est_after,
        "h_below_5_proxy_after": h_below5_est_after,
        "surplus_unabsorbed_twh_after": unabsorbed_energy / 1e6,
    }


def _solve_lever_binary_search(
    eval_fn: Any,
    *,
    min_value: float,
    max_value: float,
    target_sr_energy: float,
    target_h_negative_est: float,
    target_h_below_5: float,
    require_sr_target: bool = True,
) -> dict[str, Any]:
    base = eval_fn(min_value)
    if str(base.get("status", "")).lower() != "ok":
        return {**base, "status": "missing_data", "required_uplift": np.nan}

    def _objective_ok(metrics: dict[str, Any]) -> bool:
        sr_ok = True
        if require_sr_target:
            sr_ok = _safe_float(metrics.get("sr_energy_after"), np.nan) <= float(target_sr_energy)
        h_ok = _safe_float(metrics.get("h_negative_est_after", metrics.get("h_negative_proxy_after")), np.nan) <= float(target_h_negative_est)
        h5_ok = _safe_float(metrics.get("h_below_5_est_after", metrics.get("h_below_5_proxy_after")), np.nan) <= float(target_h_below_5)
        return bool(sr_ok and h_ok and h5_ok)

    if _objective_ok(base):
        return {
            **base,
            "status": "already_ok",
            "within_bounds": True,
            "required_uplift": float(min_value),
        }

    hi_metrics = eval_fn(max_value)
    if str(hi_metrics.get("status", "")).lower() != "ok":
        return {**hi_metrics, "status": "missing_data", "required_uplift": np.nan}
    if not _objective_ok(hi_metrics):
        return {
            **hi_metrics,
            "status": "not_achievable",
            "within_bounds": False,
            "required_uplift": float(max_value),
        }

    lo = float(min_value)
    hi = float(max_value)
    best_metrics = hi_metrics
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        m = eval_fn(mid)
        if str(m.get("status", "")).lower() != "ok":
            return {**m, "status": "missing_data", "required_uplift": np.nan}
        if _objective_ok(m):
            hi = mid
            best_metrics = m
        else:
            lo = mid
        if abs(hi - lo) <= 1e-4:
            break
    return {
        **best_metrics,
        "status": "ok",
        "within_bounds": True,
        "required_uplift": float(hi),
    }


def run_q3(
    annual_df: pd.DataFrame,
    hourly_by_country_year: dict[tuple[str, int], pd.DataFrame],
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
    validation_findings_df: pd.DataFrame | None = None,
) -> ModuleResult:
    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q3_PARAMS)].iterrows()
    }
    all_params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df.iterrows()
        if str(r.get("param_name", "")).strip() != ""
    }
    trend_window = max(2, int(params.get("trend_window_years", 3)))
    sr_energy_target = float(params.get("sr_energy_target", 0.01))
    target_sr_energy = float(selection.get("target_sr_energy", selection.get("target_sr", all_params.get("stage1_sr_energy_max", sr_energy_target))))
    target_h_negative_est = float(selection.get("target_h_negative", all_params.get("stage1_h_negative_max", 200.0)))
    target_h_negative_proxy = target_h_negative_est  # Legacy alias
    target_h_below_5 = float(selection.get("target_h_below_5", all_params.get("stage1_h_below_5_max", 500.0)))
    slope_capture_target = float(params.get("slope_capture_target", params.get("trend_capture_ratio_min", 0.0)))
    mode = str(selection.get("mode", "HIST")).upper()
    scenario_id = str(selection.get("scenario_id") or ("HIST" if mode == "HIST" else "SCEN"))
    assumed_demand_multiplier = _safe_float(selection.get("demand_multiplier", 1.0), 1.0)
    assumed_must_run_reduction_factor = _safe_float(selection.get("must_run_reduction_factor", 0.0), 0.0)
    assumed_flex_multiplier = _safe_float(selection.get("flex_multiplier", 1.0), 1.0)

    q1 = run_q1(
        annual_df,
        assumptions_df,
        selection,
        run_id=f"{run_id}_Q1",
        hourly_by_country_year=hourly_by_country_year,
        validation_findings_df=validation_findings_df,
    )
    q2 = run_q2(
        annual_df,
        assumptions_df,
        selection,
        run_id=f"{run_id}_Q2",
        hourly_by_country_year=hourly_by_country_year,
        validation_findings_df=validation_findings_df,
    )

    q1_panel = q1.tables.get("Q1_year_panel", pd.DataFrame()).copy()
    q1_summary = q1.tables.get("Q1_country_summary", pd.DataFrame()).copy()
    q2_slopes = q2.tables.get("Q2_country_slopes", pd.DataFrame()).copy()
    q1_summary_hist_ref = _infer_historical_bascule_summary(
        annual_df=annual_df,
        assumptions_df=assumptions_df,
        selection=selection,
        run_id=run_id,
    )

    countries = selection.get("countries", sorted(annual_df["country"].dropna().astype(str).unique().tolist()))
    rows: list[dict[str, Any]] = []
    requirement_rows: list[dict[str, Any]] = []
    checks: list[dict[str, str]] = []
    warnings: list[str] = []

    for country in countries:
        if "country" in q1_panel.columns:
            c_panel = q1_panel[q1_panel["country"].astype(str) == str(country)].sort_values("year").copy()
        else:
            c_panel = pd.DataFrame()
        if "country" in q1_summary.columns:
            c_sum = q1_summary[q1_summary["country"].astype(str) == str(country)].copy()
        else:
            c_sum = pd.DataFrame()
        if "country" in q1_summary_hist_ref.columns:
            c_hist_sum = q1_summary_hist_ref[
                q1_summary_hist_ref["country"].astype(str) == str(country)
            ].copy()
        else:
            c_hist_sum = pd.DataFrame()
        c_sum_row = c_sum.iloc[0] if not c_sum.empty else None
        stage2_active_end_year = stage2_active_from_metrics(
            c_sum_row,
            all_params,
            suffix="_at_end_year",
        )
        end_year_q1 = _safe_float(c_sum_row.get("end_year"), np.nan) if c_sum_row is not None else np.nan
        if (not np.isfinite(end_year_q1)) and (not c_panel.empty):
            end_year_q1 = _safe_float(c_panel["year"].max(), np.nan)

        bascule_hist = _safe_float(c_hist_sum.get("bascule_year_market_country", c_hist_sum.get("bascule_year_market", pd.Series([np.nan]))).iloc[0], np.nan) if not c_hist_sum.empty else np.nan
        bascule_curr = _safe_float(c_sum.get("bascule_year_market_country", c_sum.get("bascule_year_market", pd.Series([np.nan]))).iloc[0], np.nan) if not c_sum.empty else np.nan

        if np.isfinite(bascule_hist):
            bascule_ref = float(int(bascule_hist))
            bascule_source = "historical"
            c_sum_ref = c_hist_sum.iloc[0] if not c_hist_sum.empty else (c_sum.iloc[0] if not c_sum.empty else None)
        elif np.isfinite(bascule_curr):
            bascule_ref = float(int(bascule_curr))
            bascule_source = "current_mode"
            c_sum_ref = c_sum.iloc[0] if not c_sum.empty else None
        else:
            if stage2_active_end_year and np.isfinite(end_year_q1):
                bascule_ref = float(int(end_year_q1))
                bascule_source = "end_year_stage2_active"
                c_sum_ref = c_sum.iloc[0] if not c_sum.empty else None
            else:
                bascule_ref = np.nan
                bascule_source = "missing"
                c_sum_ref = None
        stage2_hneg_min = float(all_params.get("h_negative_stage2_min", 200.0))
        stage2_hb5_min = float(all_params.get("h_below_5_stage2_min", 500.0))
        low_price_evidence_at_bascule = False
        if np.isfinite(bascule_ref):
            hneg_b = _safe_float(c_sum_ref.get("h_negative_at_bascule"), np.nan) if c_sum_ref is not None else np.nan
            hb5_b = _safe_float(c_sum_ref.get("h_below_5_at_bascule"), np.nan) if c_sum_ref is not None else np.nan
            if (not np.isfinite(hneg_b)) and (not np.isfinite(hb5_b)):
                b_rows = c_panel[c_panel["year"] == int(bascule_ref)] if "year" in c_panel.columns else pd.DataFrame()
                if not b_rows.empty:
                    hneg_b = _safe_float(b_rows.iloc[0].get("h_negative_obs"), np.nan)
                    hb5_b = _safe_float(b_rows.iloc[0].get("h_below_5_obs"), np.nan)
            low_price_evidence_at_bascule = bool(
                (np.isfinite(hneg_b) and hneg_b >= stage2_hneg_min)
                or (np.isfinite(hb5_b) and hb5_b >= stage2_hb5_min)
            )
            if not low_price_evidence_at_bascule:
                if stage2_active_end_year and np.isfinite(end_year_q1):
                    bascule_ref = float(int(end_year_q1))
                    bascule_source = "end_year_stage2_active"
                else:
                    bascule_ref = np.nan
                    bascule_source = f"{bascule_source}_insufficient_low_price_evidence"

        audit_common = {
            "scenario_id": scenario_id,
            "assumed_demand_multiplier": assumed_demand_multiplier,
            "assumed_must_run_reduction_factor": assumed_must_run_reduction_factor,
            "assumed_flex_multiplier": assumed_flex_multiplier,
        }

        if c_panel.empty:
            rows.append(
                {
                    "country": country,
                    **audit_common,
                    "applicability_flag": "HORS_SCOPE_PHASE2",
                    "reference_year": np.nan,
                    "in_phase2": False,
                    "status": "HORS_SCOPE_PHASE2",
                    "reason_code": "missing_panel",
                    "status_explanation": "Panel Q1 vide.",
                    "stage3_ready_year": False,
                    "phase2_slope_capture_ratio_pv": np.nan,
                    "phase2_slope_method": "none",
                    "trend_capture_ratio_pv": np.nan,
                    "trend_h_negative": np.nan,
                    "stop_possible_if": np.nan,
                    "stop_condition_detail": "non_applicable",
                    "surplus_energy_twh_recent": np.nan,
                    "target_absorption_twh": np.nan,
                    "demand_uplift_twh": np.nan,
                    "inversion_k_demand": np.nan,
                    "required_demand_uplift_mw": np.nan,
                    "inversion_k_demand_status": "insufficient_scope",
                    "inversion_r_mustrun": np.nan,
                    "required_mustrun_reduction_ratio": np.nan,
                    "inversion_r_mustrun_status": "proxy_not_computed",
                    "inversion_f_flex": np.nan,
                    "inversion_f_flex_status": "proxy_not_computed",
                    "already_phase3": False,
                    "additional_absorbed_needed_TWh_year": np.nan,
                    "additional_sink_power_p95_mw": np.nan,
                    "additional_sink_profile_status": "hourly_profile_unavailable",
                    "warnings_quality": "missing_panel",
                    "trend_quality_flag": "NOT_APPLICABLE",
                    "bascule_reference_year": bascule_ref,
                    "bascule_reference_source": bascule_source,
                }
            )
            for lever in ["demand_uplift", "export_uplift", "flex_uplift"]:
                requirement_rows.append(
                    {
                        "country": country,
                        "scenario_id": scenario_id,
                        "year": np.nan,
                        "lever": lever,
                        "required_uplift": np.nan,
                        "required_uplift_mw": np.nan,
                        "required_uplift_pct_avg_load": np.nan,
                        "required_uplift_twh_per_year": np.nan,
                        "within_bounds": False,
                        "target_sr": target_sr_energy,
                        "target_h_negative": target_h_negative_est,
                        "target_h_below_5": target_h_below_5,
                        "predicted_sr_after": np.nan,
                        "predicted_far_after": np.nan,
                        "predicted_h_negative_after": np.nan,
                        "predicted_h_below_5_after": np.nan,
                        "predicted_h_negative_metric": "MARKET_PROXY_BUCKET_MODEL_EST",
                        "applicability_flag": "HORS_SCOPE_PHASE2",
                        "status": "hors_scope_phase2",
                        "reason": "no_stage2_detected",
                    }
                )
            continue

        if not bool(stage2_active_end_year):
            last_any = c_panel.iloc[-1]
            ref_year_val = int(_safe_float(last_any.get("year"), np.nan)) if np.isfinite(_safe_float(last_any.get("year"), np.nan)) else np.nan
            rows.append(
                {
                    "country": country,
                    **audit_common,
                    "applicability_flag": "HORS_SCOPE_PHASE2",
                    "reference_year": ref_year_val,
                    "in_phase2": False,
                    "status": "HORS_SCOPE_PHASE2",
                    "reason_code": "no_stage2_detected",
                    "status_explanation": "Stage2 non active a l'end_year selon les criteres Q1 partages.",
                    "stage3_ready_year": False,
                    "phase2_slope_capture_ratio_pv": np.nan,
                    "phase2_slope_method": "none",
                    "trend_capture_ratio_pv": np.nan,
                    "trend_h_negative": np.nan,
                    "stop_possible_if": np.nan,
                    "stop_condition_detail": "non_applicable",
                    "surplus_energy_twh_recent": np.nan,
                    "target_absorption_twh": np.nan,
                    "demand_uplift_twh": np.nan,
                    "inversion_k_demand": np.nan,
                    "required_demand_uplift_mw": np.nan,
                    "inversion_k_demand_status": "insufficient_scope",
                    "inversion_r_mustrun": np.nan,
                    "required_mustrun_reduction_ratio": np.nan,
                    "inversion_r_mustrun_status": "proxy_not_computed",
                    "inversion_f_flex": np.nan,
                    "inversion_f_flex_status": "proxy_not_computed",
                    "already_phase3": False,
                    "additional_absorbed_needed_TWh_year": np.nan,
                    "additional_sink_power_p95_mw": np.nan,
                    "additional_sink_profile_status": "hourly_profile_unavailable",
                    "warnings_quality": "no_stage2_detected",
                    "trend_quality_flag": "NOT_APPLICABLE",
                    "bascule_reference_year": np.nan,
                    "bascule_reference_source": bascule_source,
                }
            )
            for lever in ["demand_uplift", "export_uplift", "flex_uplift"]:
                requirement_rows.append(
                    {
                        "country": country,
                        "scenario_id": scenario_id,
                        "year": ref_year_val,
                        "lever": lever,
                        "required_uplift": np.nan,
                        "required_uplift_mw": np.nan,
                        "required_uplift_pct_avg_load": np.nan,
                        "required_uplift_twh_per_year": np.nan,
                        "within_bounds": False,
                        "target_sr": target_sr_energy,
                        "target_h_negative": target_h_negative_est,
                        "target_h_below_5": target_h_below_5,
                        "predicted_sr_after": np.nan,
                        "predicted_far_after": np.nan,
                        "predicted_h_negative_after": np.nan,
                        "predicted_h_below_5_after": np.nan,
                        "predicted_h_negative_metric": "MARKET_PROXY_BUCKET_MODEL_EST",
                        "applicability_flag": "HORS_SCOPE_PHASE2",
                        "status": "hors_scope_phase2",
                        "reason": "no_stage2_detected",
                    }
                )
            continue

        if not np.isfinite(bascule_ref):
            last_any = c_panel.iloc[-1]
            rows.append(
                {
                    "country": country,
                    **audit_common,
                    "applicability_flag": "HORS_SCOPE_PHASE2",
                    "reference_year": int(_safe_float(last_any.get("year"), np.nan)) if np.isfinite(_safe_float(last_any.get("year"), np.nan)) else np.nan,
                    "in_phase2": False,
                    "status": "HORS_SCOPE_PHASE2",
                    "reason_code": "no_stage2_detected",
                    "status_explanation": "Aucune phase2 valide detectee (bascule absente ou evidence low-price insuffisante).",
                    "stage3_ready_year": False,
                    "phase2_slope_capture_ratio_pv": np.nan,
                    "phase2_slope_method": "none",
                    "trend_capture_ratio_pv": np.nan,
                    "trend_h_negative": np.nan,
                    "stop_possible_if": np.nan,
                    "stop_condition_detail": "non_applicable",
                    "surplus_energy_twh_recent": np.nan,
                    "target_absorption_twh": np.nan,
                    "demand_uplift_twh": np.nan,
                    "inversion_k_demand": np.nan,
                    "required_demand_uplift_mw": np.nan,
                    "inversion_k_demand_status": "insufficient_scope",
                    "inversion_r_mustrun": np.nan,
                    "required_mustrun_reduction_ratio": np.nan,
                    "inversion_r_mustrun_status": "proxy_not_computed",
                    "inversion_f_flex": np.nan,
                    "inversion_f_flex_status": "proxy_not_computed",
                    "already_phase3": False,
                    "additional_absorbed_needed_TWh_year": np.nan,
                    "additional_sink_power_p95_mw": np.nan,
                    "additional_sink_profile_status": "hourly_profile_unavailable",
                    "warnings_quality": "no_stage2_detected",
                    "trend_quality_flag": "NOT_APPLICABLE",
                    "bascule_reference_year": np.nan,
                    "bascule_reference_source": bascule_source,
                }
            )
            for lever in ["demand_uplift", "export_uplift", "flex_uplift"]:
                requirement_rows.append(
                    {
                        "country": country,
                        "scenario_id": scenario_id,
                        "year": int(_safe_float(last_any.get("year"), np.nan)) if np.isfinite(_safe_float(last_any.get("year"), np.nan)) else np.nan,
                        "lever": lever,
                        "required_uplift": np.nan,
                        "required_uplift_mw": np.nan,
                        "required_uplift_pct_avg_load": np.nan,
                        "required_uplift_twh_per_year": np.nan,
                        "within_bounds": False,
                        "target_sr": target_sr_energy,
                        "target_h_negative": target_h_negative_est,
                        "target_h_below_5": target_h_below_5,
                        "predicted_sr_after": np.nan,
                        "predicted_far_after": np.nan,
                        "predicted_h_negative_after": np.nan,
                        "predicted_h_below_5_after": np.nan,
                        "predicted_h_negative_metric": "MARKET_PROXY_BUCKET_MODEL_EST",
                        "applicability_flag": "HORS_SCOPE_PHASE2",
                        "status": "hors_scope_phase2",
                        "reason": "no_stage2_detected",
                    }
                )
            continue

        c_phase = c_panel[c_panel["year"] >= int(bascule_ref)].copy()
        if c_phase.empty:
            c_phase = c_panel.copy()
        c_phase["quality_ok"] = c_phase.get("quality_ok", True).fillna(False).astype(bool)
        c_phase["crisis_year"] = c_phase.get("crisis_year", False).fillna(False).astype(bool)
        c_phase_non_crisis = c_phase[c_phase["quality_ok"] & (~c_phase["crisis_year"])].sort_values("year")
        if c_phase_non_crisis.empty:
            c_phase_non_crisis = c_phase.sort_values("year").copy()

        recent = c_phase_non_crisis.tail(trend_window).copy()
        last = recent.iloc[-1]
        ref_year = _safe_float(last.get("year"), np.nan)
        insufficient_history_for_trend = int(len(recent)) < 2

        if np.isfinite(bascule_ref):
            b_rows = c_panel[c_panel["year"] == int(bascule_ref)]
            b_row = b_rows.iloc[0] if not b_rows.empty else None
        else:
            b_row = None
        active_bascule = _families_active_at_bascule(c_sum_ref, b_row)
        state_now = _row_family_state(last)
        turned_off_map = {
            fam: (fam in active_bascule and fam in state_now and (not state_now[fam]))
            for fam in ["LOW_PRICE", "PHYSICAL", "VALUE_PV", "VALUE_WIND"]
        }
        turned_off_any = bool(any(turned_off_map.values()))
        all_off = bool(active_bascule) and all(
            (fam in state_now and not state_now[fam]) for fam in active_bascule if fam in state_now
        )
        low_price_off = bool(turned_off_map.get("LOW_PRICE", False))
        persistent_off = _two_year_persistence_off(c_phase_non_crisis, active_bascule)

        if all_off:
            status = "BACK_TO_STAGE1"
            reason_code = "all_families_turned_off"
            status_explanation = "Toutes les familles actives a la bascule sont eteintes."
        elif turned_off_any:
            if low_price_off or persistent_off:
                status = "STOP_CONFIRMED"
                reason_code = "family_turned_off_confirmed"
                status_explanation = "Au moins une famille basculee est eteinte de facon persistante."
            else:
                status = "STOP_POSSIBLE"
                reason_code = "family_turned_off_recent"
                status_explanation = "Au moins une famille basculee est eteinte mais sans confirmation temporelle."
        else:
            status = "CONTINUES"
            reason_code = "no_family_turned_off"
            status_explanation = "Aucune famille active a la bascule n'est eteinte."

        q2_row = q2_slopes[
            (q2_slopes.get("country", pd.Series(dtype=object)).astype(str) == str(country))
            & (q2_slopes.get("tech", pd.Series(dtype=object)).astype(str) == "PV")
        ]
        q2_slope = np.nan
        q2_method = "none"
        if not q2_row.empty:
            q2_slope = _safe_float(q2_row.iloc[0].get("slope"), np.nan)
            q2_method = str(q2_row.iloc[0].get("slope_method", "none"))

        if insufficient_history_for_trend:
            trend_capture = np.nan
            trend_hneg = np.nan
            trend_h_zero_or_negative = np.nan
        else:
            trend_capture = _trend_slope(recent.get("year"), recent.get("capture_ratio_pv"))
            trend_hneg = _trend_slope(recent.get("year"), recent.get("h_negative_obs"))
            trend_h_zero_or_negative = (
                _trend_slope(recent.get("year"), recent.get("h_zero_or_negative"))
                if "h_zero_or_negative" in recent.columns
                else np.nan
            )

        in_phase2_current = bool(last.get("is_phase2_market", False)) or bool(stage2_active_end_year)
        applicability_flag = "APPLICABLE" if bool(stage2_active_end_year) else "HORS_SCOPE_PHASE2"
        available_ref_years = sorted([int(y) for (c, y) in hourly_by_country_year.keys() if str(c) == str(country)])
        ref_year_int = int(ref_year) if np.isfinite(ref_year) else None
        if ref_year_int is not None and ref_year_int in available_ref_years:
            hourly_ref_year = ref_year_int
        elif available_ref_years:
            hourly_ref_year = int(available_ref_years[-1])
        else:
            hourly_ref_year = None
        hourly_ref = hourly_by_country_year.get((str(country), int(hourly_ref_year))) if hourly_ref_year is not None else None
        export_coincidence_factor = _safe_float(last.get("export_coincidence_factor"), _safe_float(selection.get("export_coincidence_factor"), 1.0))
        if not np.isfinite(export_coincidence_factor):
            export_coincidence_factor = 1.0

        avg_load_ref = np.nan
        n_hours_ref = np.nan
        baseline_est: dict[str, Any] = {}
        proxy_quality_status = "NOT_RUN"
        proxy_quality_reasons = "not_run"
        market_proxy_model: MarketProxyBucketModel | None = None
        risk_bucket_ids: set[int] = set()
        if hourly_ref is None or hourly_ref.empty:
            demand_solver = {"status": "missing_data", "required_uplift": np.nan, "reason": "hourly_profile_unavailable"}
            export_solver = {"status": "missing_data", "required_uplift": np.nan, "reason": "hourly_profile_unavailable"}
            flex_solver = {"status": "missing_data", "required_uplift": np.nan, "reason": "hourly_profile_unavailable"}
        else:
            canonical_ref = build_canonical_hourly_panel(hourly_ref)
            avg_load_ref = _safe_float(pd.to_numeric(canonical_ref.get("load_mw"), errors="coerce").mean(), np.nan)
            n_hours_ref = _safe_float(len(canonical_ref), np.nan)
            exports_ref = pd.to_numeric(canonical_ref.get("exports_net_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
            try:
                market_proxy_model = MarketProxyBucketModel.fit_baseline(hourly_ref, eps=1e-6)
                baseline_est = market_proxy_model.estimate_from_hourly(hourly_ref)
                proxy_quality_status = str(market_proxy_model.quality_summary.get("quality_status", "FAIL")).upper()
                proxy_quality_reasons = str(market_proxy_model.quality_summary.get("quality_reasons", "")).strip()
                risk_bucket_ids = _top_risk_bucket_ids(market_proxy_model, top_n=int(max(1, _safe_float(selection.get("q3_flex_risk_bucket_count"), 4.0))))
            except Exception as exc:
                market_proxy_model = None
                proxy_quality_status = "FAIL"
                proxy_quality_reasons = f"market_proxy_fit_error:{exc}"

            demand_cap_mw = _safe_float(selection.get("demand_uplift_max_mw"), np.nan)
            if not np.isfinite(demand_cap_mw) or demand_cap_mw <= 0.0:
                demand_cap_mw = max(1.0, max(0.0, _safe_float(avg_load_ref, 0.0)) * max(0.0, float(params.get("demand_k_max", 0.30))))
            export_cap_mw = _safe_float(selection.get("export_uplift_max_mw"), np.nan)
            if not np.isfinite(export_cap_mw) or export_cap_mw <= 0.0:
                export_cap_mw = max(1.0, _safe_float(exports_ref.quantile(0.95), 0.0) * max(0.5, _safe_float(all_params.get("q1_lever_max_uplift"), 1.0)))
            flex_cap = _safe_float(selection.get("flex_uplift_max_mw", selection.get("flex_mw_max")), np.nan)
            if not np.isfinite(flex_cap) or flex_cap <= 0.0:
                nrl_proxy = pd.to_numeric(canonical_ref.get("nrl_mw"), errors="coerce")
                if nrl_proxy.notna().sum() > 0:
                    flex_cap = max(1.0, float((-nrl_proxy).clip(lower=0.0).quantile(0.95)) * 1.5)
                else:
                    flex_cap = max(1.0, _safe_float(avg_load_ref, 1000.0) * 0.05)

            if market_proxy_model is None or proxy_quality_status == "FAIL":
                demand_solver = {
                    "status": "missing_data",
                    "required_uplift": np.nan,
                    "reason": "market_proxy_invalid",
                }
                export_solver = {
                    "status": "missing_data",
                    "required_uplift": np.nan,
                    "reason": "market_proxy_invalid",
                }
                flex_solver = {
                    "status": "missing_data",
                    "required_uplift": np.nan,
                    "reason": "market_proxy_invalid",
                }
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "Q3_MARKET_PROXY_INVALID",
                        "message": f"{country}: quality FAIL sur proxy marche ({proxy_quality_reasons or 'invalid'}).",
                    }
                )
            else:
                demand_solver = _solve_lever_binary_search(
                    lambda x: _compute_hourly_proxy_metrics(
                        hourly_ref,
                        market_proxy_model=market_proxy_model,
                        risk_bucket_ids=risk_bucket_ids,
                        demand_uplift_mw=x,
                        export_uplift_mw=0.0,
                        flex_mw_additional=0.0,
                        export_coincidence_factor=export_coincidence_factor,
                    ),
                    min_value=0.0,
                    max_value=float(demand_cap_mw),
                    target_sr_energy=target_sr_energy,
                    target_h_negative_est=target_h_negative_est,
                    target_h_below_5=target_h_below_5,
                )
                export_solver = _solve_lever_binary_search(
                    lambda x: _compute_hourly_proxy_metrics(
                        hourly_ref,
                        market_proxy_model=market_proxy_model,
                        risk_bucket_ids=risk_bucket_ids,
                        demand_uplift_mw=0.0,
                        export_uplift_mw=x,
                        flex_mw_additional=0.0,
                        export_coincidence_factor=export_coincidence_factor,
                    ),
                    min_value=0.0,
                    max_value=float(export_cap_mw),
                    target_sr_energy=target_sr_energy,
                    target_h_negative_est=target_h_negative_est,
                    target_h_below_5=target_h_below_5,
                )
                flex_solver = _solve_lever_binary_search(
                    lambda x: _compute_hourly_proxy_metrics(
                        hourly_ref,
                        market_proxy_model=market_proxy_model,
                        risk_bucket_ids=risk_bucket_ids,
                        demand_uplift_mw=0.0,
                        export_uplift_mw=0.0,
                        flex_mw_additional=x,
                        export_coincidence_factor=export_coincidence_factor,
                    ),
                    min_value=0.0,
                    max_value=float(flex_cap),
                    target_sr_energy=target_sr_energy,
                    target_h_negative_est=target_h_negative_est,
                    target_h_below_5=target_h_below_5,
                )

        lever_to_solver = [
            ("demand_uplift", demand_solver),
            ("export_uplift", export_solver),
            ("flex_uplift", flex_solver),
        ]
        for lever, solver in lever_to_solver:
            raw_status = str(solver.get("status", "missing_data")).lower()
            req_uplift_mw = _safe_float(solver.get("required_uplift"), np.nan)
            if raw_status == "already_ok":
                req_uplift_mw = 0.0
            if np.isfinite(req_uplift_mw):
                req_uplift_mw = max(0.0, req_uplift_mw)
            pred_sr_after = _safe_float(solver.get("sr_energy_after"), np.nan)
            pred_far_after = _safe_float(solver.get("far_after"), np.nan)
            pred_hneg_after = _safe_float(solver.get("h_negative_est_after", solver.get("h_negative_proxy_after")), np.nan)
            pred_hb5_after = _safe_float(solver.get("h_below_5_est_after", solver.get("h_below_5_proxy_after")), np.nan)
            req_uplift_pct = (
                req_uplift_mw / avg_load_ref
                if np.isfinite(req_uplift_mw) and np.isfinite(avg_load_ref) and avg_load_ref > 0.0
                else np.nan
            )
            req_uplift_twh = (
                req_uplift_mw * n_hours_ref / 1e6
                if np.isfinite(req_uplift_mw) and np.isfinite(n_hours_ref)
                else np.nan
            )
            if in_phase2_current:
                out_status = raw_status
                out_required = req_uplift_mw
            else:
                out_status = "already_ok"
                out_required = 0.0
            if out_status not in {"ok", "already_ok", "not_achievable", "missing_data", "hors_scope_phase2"}:
                out_status = "missing_data"
            requirement_rows.append(
                {
                    "country": country,
                    "scenario_id": scenario_id,
                    "year": hourly_ref_year if hourly_ref_year is not None else (ref_year_int if ref_year_int is not None else np.nan),
                    "lever": lever,
                    "required_uplift": out_required,
                    "required_uplift_mw": out_required,
                    "required_uplift_pct_avg_load": req_uplift_pct if in_phase2_current else np.nan,
                    "required_uplift_twh_per_year": req_uplift_twh if in_phase2_current else np.nan,
                    "within_bounds": bool(solver.get("within_bounds", False)) if in_phase2_current else False,
                    "target_sr": target_sr_energy,
                    "target_h_negative": target_h_negative_est,
                    "target_h_below_5": target_h_below_5,
                    "predicted_sr_after": pred_sr_after,
                    "predicted_far_after": pred_far_after,
                    "predicted_h_negative_after": pred_hneg_after,
                    "predicted_h_below_5_after": pred_hb5_after,
                    "predicted_h_negative_metric": "MARKET_PROXY_BUCKET_MODEL_EST",
                    "h_negative_obs_before": _safe_float(baseline_est.get("h_negative_obs"), np.nan),
                    "h_below_5_obs_before": _safe_float(baseline_est.get("h_below_5_obs"), np.nan),
                    "h_negative_est_before": _safe_float(baseline_est.get("h_negative_est"), np.nan),
                    "h_below_5_est_before": _safe_float(baseline_est.get("h_below_5_est"), np.nan),
                    "applicability_flag": applicability_flag,
                    "status": out_status,
                    "reason": str(solver.get("reason", "already_phase3" if (not in_phase2_current) else out_status)),
                    "export_coincidence_factor": export_coincidence_factor,
                    "proxy_quality_status": proxy_quality_status,
                    "proxy_quality_reasons": proxy_quality_reasons,
                    "output_schema_version": Q3_OUTPUT_SCHEMA_VERSION,
                }
            )

        demand_status = str(demand_solver.get("status", "missing_data")).lower()
        demand_required = _safe_float(demand_solver.get("required_uplift"), np.nan)
        if demand_status == "already_ok":
            demand_required = 0.0
        if np.isfinite(demand_required):
            demand_required = max(0.0, demand_required)
        if in_phase2_current:
            if proxy_quality_status == "FAIL":
                status = "FAIL"
                reason_code = "market_proxy_invalid"
                status_explanation = "Le proxy marche est invalide (quality FAIL), simulation non defensable."
            elif demand_status == "already_ok":
                status = "STOP_CONFIRMED"
                reason_code = "already_meets_targets"
                status_explanation = "Les cibles proxy marche EST sont deja respectees a uplift=0."
            elif demand_status == "not_achievable":
                status = "CONTINUES"
                reason_code = "targets_unreachable_within_bounds"
                status_explanation = "Les cibles proxy EST ne sont pas atteignables dans les bornes de levier."
            elif demand_status == "missing_data":
                status = "CONTINUES"
                reason_code = "missing_data"
                status_explanation = "Donnees insuffisantes pour calibrer le proxy marche."
            else:
                status = "CONTINUES"
                reason_code = "no_family_turned_off"
                status_explanation = "Un uplift est requis pour atteindre les cibles proxy."
        else:
            status = "STOP_CONFIRMED"
            reason_code = "already_phase3"
            status_explanation = "Conditions de sortie deja satisfaites dans le baseline (deja inverse)."
            demand_status = "already_ok"
            demand_required = 0.0

        surplus_twh = _safe_float(last.get("surplus_energy_twh", last.get("surplus_twh")), np.nan)
        load_twh = _safe_float(last.get("load_net_twh"), np.nan)
        target_abs_twh = load_twh * sr_energy_target if np.isfinite(load_twh) else np.nan
        demand_uplift_twh = (
            max(0.0, surplus_twh - target_abs_twh)
            if np.isfinite(surplus_twh) and np.isfinite(target_abs_twh)
            else np.nan
        )
        sink_p95, sink_profile_status = _additional_sink_power_p95(
            hourly_by_country_year,
            str(country),
            float(hourly_ref_year) if hourly_ref_year is not None else ref_year,
            demand_uplift_twh,
        )
        mustrun_reduction_needed, mustrun_status = _required_mustrun_reduction(last, all_params, max_reduction=1.0)
        if np.isfinite(mustrun_reduction_needed):
            mustrun_reduction_needed = float(np.clip(mustrun_reduction_needed, 0.0, 1.0))
        already_phase3 = bool((not in_phase2_current) or demand_status == "already_ok")
        if already_phase3:
            mustrun_reduction_needed = 0.0
            mustrun_status = "already_ok"
        if proxy_quality_status == "FAIL":
            status = "FAIL"
            reason_code = "market_proxy_invalid"
            status_explanation = "Le proxy marche est invalide (quality FAIL)."
            already_phase3 = False

        warning_quality_codes: list[str] = []
        if sink_profile_status not in {"profile_weighted_surplus", "no_additional_energy_required"}:
            warning_quality_codes.append(str(sink_profile_status))
        if insufficient_history_for_trend:
            warning_quality_codes.append("INSUFFICIENT_HISTORY_FOR_TREND")

        rows.append(
            {
                "country": country,
                **audit_common,
                "applicability_flag": applicability_flag,
                "reference_year": hourly_ref_year if hourly_ref_year is not None else (int(ref_year) if np.isfinite(ref_year) else np.nan),
                "in_phase2": in_phase2_current,
                "status": status,
                "reason_code": reason_code,
                "status_explanation": status_explanation,
                "stage3_ready_year": bool(status in {"STOP_POSSIBLE", "STOP_CONFIRMED", "BACK_TO_STAGE1"}),
                "phase2_slope_capture_ratio_pv": q2_slope,
                "phase2_slope_method": q2_method,
                "trend_capture_ratio_pv": trend_capture,
                "trend_h_negative": trend_hneg,
                "trend_h_zero_or_negative": trend_h_zero_or_negative,
                "stop_possible_if": turned_off_any,
                "stop_condition_detail": ";".join([k for k, v in turned_off_map.items() if v]) if turned_off_any else "none",
                "surplus_energy_twh_recent": surplus_twh,
                "target_absorption_twh": target_abs_twh,
                "demand_uplift_twh": demand_uplift_twh,
                "inversion_k_demand": demand_required if np.isfinite(demand_required) else np.nan,
                "required_demand_uplift_mw": demand_required if np.isfinite(demand_required) else np.nan,
                "inversion_k_demand_status": demand_status,
                "inversion_r_mustrun": mustrun_reduction_needed if np.isfinite(mustrun_reduction_needed) else np.nan,
                "required_mustrun_reduction_ratio": mustrun_reduction_needed if np.isfinite(mustrun_reduction_needed) else np.nan,
                "inversion_r_mustrun_status": mustrun_status,
                "inversion_f_flex": _safe_float(flex_solver.get("required_uplift"), np.nan),
                "inversion_f_flex_status": str(flex_solver.get("status", "missing_data")).lower(),
                "already_phase3": already_phase3,
                "additional_absorbed_needed_TWh_year": demand_uplift_twh,
                "additional_sink_power_p95_mw": sink_p95,
                "additional_sink_profile_status": sink_profile_status,
                "warnings_quality": ";".join([w for w in warning_quality_codes if str(w).strip()]),
                "trend_quality_flag": "INSUFFICIENT_HISTORY_FOR_TREND" if insufficient_history_for_trend else "OK",
                "bascule_reference_year": float(int(bascule_ref)) if np.isfinite(bascule_ref) else np.nan,
                "bascule_reference_source": bascule_source,
                "families_active_at_bascule": ",".join(sorted(active_bascule)),
                "turned_off_low_price": bool(turned_off_map["LOW_PRICE"]),
                "turned_off_physical": bool(turned_off_map["PHYSICAL"]),
                "turned_off_value_pv": bool(turned_off_map["VALUE_PV"]),
                "turned_off_value_wind": bool(turned_off_map["VALUE_WIND"]),
                "turned_off_family_any": bool(turned_off_any),
                "turned_off_family_persistent_2y": bool(persistent_off),
                "within_bounds": bool(demand_solver.get("within_bounds", False)) if in_phase2_current else False,
                "target_sr": target_sr_energy,
                "target_h_negative": target_h_negative_est,
                "target_h_below_5": target_h_below_5,
                "predicted_sr_after": _safe_float(demand_solver.get("sr_energy_after"), np.nan),
                "predicted_far_after": _safe_float(demand_solver.get("far_after"), np.nan),
                "predicted_h_negative_after": _safe_float(demand_solver.get("h_negative_est_after", demand_solver.get("h_negative_proxy_after")), np.nan),
                "predicted_h_below_5_after": _safe_float(demand_solver.get("h_below_5_est_after", demand_solver.get("h_below_5_proxy_after")), np.nan),
                "predicted_h_negative_metric": "MARKET_PROXY_BUCKET_MODEL_EST",
                "required_uplift_mw": demand_required if np.isfinite(demand_required) else np.nan,
                "required_uplift_pct_avg_load": (
                    (demand_required / avg_load_ref)
                    if np.isfinite(demand_required) and np.isfinite(avg_load_ref) and avg_load_ref > 0.0
                    else np.nan
                ),
                "required_uplift_twh_per_year": (
                    (demand_required * n_hours_ref / 1e6)
                    if np.isfinite(demand_required) and np.isfinite(n_hours_ref)
                    else np.nan
                ),
                "h_negative_obs_before": _safe_float(baseline_est.get("h_negative_obs"), np.nan),
                "h_below_5_obs_before": _safe_float(baseline_est.get("h_below_5_obs"), np.nan),
                "h_negative_est_before": _safe_float(baseline_est.get("h_negative_est"), np.nan),
                "h_below_5_est_before": _safe_float(baseline_est.get("h_below_5_est"), np.nan),
                "h_negative_est_after": _safe_float(demand_solver.get("h_negative_est_after", demand_solver.get("h_negative_proxy_after")), np.nan),
                "h_below_5_est_after": _safe_float(demand_solver.get("h_below_5_est_after", demand_solver.get("h_below_5_proxy_after")), np.nan),
                "delta_h_negative_est": (
                    _safe_float(demand_solver.get("h_negative_est_after", demand_solver.get("h_negative_proxy_after")), np.nan)
                    - _safe_float(baseline_est.get("h_negative_est"), np.nan)
                ),
                "delta_h_below_5_est": (
                    _safe_float(demand_solver.get("h_below_5_est_after", demand_solver.get("h_below_5_proxy_after")), np.nan)
                    - _safe_float(baseline_est.get("h_below_5_est"), np.nan)
                ),
                "baseload_price_obs_before": _safe_float(baseline_est.get("baseload_price_obs"), np.nan),
                "baseload_price_est_before": _safe_float(baseline_est.get("baseload_price_est"), np.nan),
                "baseload_price_est_after": _safe_float(demand_solver.get("baseload_price_est_after"), np.nan),
                "pv_capture_price_obs_before": _safe_float(baseline_est.get("pv_capture_price_obs"), np.nan),
                "pv_capture_price_est_before": _safe_float(baseline_est.get("pv_capture_price_est"), np.nan),
                "pv_capture_price_est_after": _safe_float(demand_solver.get("pv_capture_price_est_after"), np.nan),
                "wind_capture_price_obs_before": _safe_float(baseline_est.get("wind_capture_price_obs"), np.nan),
                "wind_capture_price_est_before": _safe_float(baseline_est.get("wind_capture_price_est"), np.nan),
                "wind_capture_price_est_after": _safe_float(demand_solver.get("wind_capture_price_est_after"), np.nan),
                "capture_ratio_pv_obs_before": _safe_float(baseline_est.get("capture_ratio_pv_obs"), np.nan),
                "capture_ratio_pv_est_before": _safe_float(baseline_est.get("capture_ratio_pv_est"), np.nan),
                "capture_ratio_pv_est_after": _safe_float(demand_solver.get("capture_ratio_pv_est_after"), np.nan),
                "capture_ratio_wind_obs_before": _safe_float(baseline_est.get("capture_ratio_wind_obs"), np.nan),
                "capture_ratio_wind_est_before": _safe_float(baseline_est.get("capture_ratio_wind_est"), np.nan),
                "capture_ratio_wind_est_after": _safe_float(demand_solver.get("capture_ratio_wind_est_after"), np.nan),
                "proxy_quality_status": proxy_quality_status,
                "proxy_quality_reasons": proxy_quality_reasons,
                "h_negative_before": _safe_float(baseline_est.get("h_negative_obs"), np.nan),
                "h_negative_after": _safe_float(demand_solver.get("h_negative_est_after", demand_solver.get("h_negative_proxy_after")), np.nan),
                "h_negative_after_source": "est_proxy",
                "h_below_5_before": _safe_float(baseline_est.get("h_below_5_obs"), np.nan),
                "h_below_5_after": _safe_float(demand_solver.get("h_below_5_est_after", demand_solver.get("h_below_5_proxy_after")), np.nan),
                "h_below_5_after_source": "est_proxy",
                "output_schema_version": Q3_OUTPUT_SCHEMA_VERSION,
                "q2_slope_above_target": bool(np.isfinite(q2_slope) and q2_slope >= slope_capture_target),
            }
        )

    out = pd.DataFrame(rows)
    q3_inversion_requirements = pd.DataFrame(requirement_rows)
    q3_quality_summary = pd.DataFrame()
    if not out.empty:
        defaults: dict[str, Any] = {
            "proxy_quality_status": "NOT_RUN",
            "proxy_quality_reasons": "not_run",
            "output_schema_version": Q3_OUTPUT_SCHEMA_VERSION,
            "h_negative_after_source": "est_proxy",
            "h_below_5_after_source": "est_proxy",
        }
        for col, default in defaults.items():
            if col not in out.columns:
                out[col] = default
            else:
                out[col] = out[col].fillna(default)
        q3_quality_summary = (
            out[
                [
                    "country",
                    "scenario_id",
                    "reference_year",
                    "proxy_quality_status",
                    "proxy_quality_reasons",
                    "output_schema_version",
                ]
            ]
            .rename(columns={"reference_year": "year"})
            .copy()
        )
        q3_quality_summary["module_id"] = "Q3"
        q3_quality_summary["quality_status"] = q3_quality_summary["proxy_quality_status"]

    if out.empty:
        checks.append({"status": "FAIL", "code": "Q3_EMPTY", "message": "Aucune sortie Q3."})
    else:
        if "country" in q1_summary.columns:
            q1_stage2_map: dict[str, bool] = {}
            for _, q1_row in q1_summary.iterrows():
                q1_stage2_map[str(q1_row.get("country", ""))] = stage2_active_from_metrics(
                    q1_row,
                    all_params,
                    suffix="_at_end_year",
                ) or (_safe_float(q1_row.get("stage2_market_score_at_end_year"), np.nan) >= 1.0)
            for _, q3_row in out.iterrows():
                c = str(q3_row.get("country", ""))
                must_apply = bool(q1_stage2_map.get(c, False))
                applicability = str(q3_row.get("applicability_flag", "")).upper().strip()
                if must_apply and applicability != "APPLICABLE":
                    checks.append(
                        {
                            "status": "FAIL",
                            "code": "Q3_Q1_PHASE2_ENDYEAR_COHERENCE",
                            "message": f"{c}: Q1 indique stage2 active a l'end_year mais Q3 n'est pas APPLICABLE.",
                        }
                    )
        proxy_fail = out["proxy_quality_status"].astype(str).str.upper().eq("FAIL")
        if bool(proxy_fail.any()):
            non_failed = ~out.loc[proxy_fail, "status"].astype(str).str.upper().eq("FAIL")
            if bool(non_failed.any()):
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "Q3_PROXY_FAIL_NOT_PROPAGATED",
                        "message": "proxy_quality_status=FAIL doit imposer status=FAIL sur Q3.",
                    }
                )
        add_needed = pd.to_numeric(out.get("additional_absorbed_needed_TWh_year"), errors="coerce")
        sink_p95 = pd.to_numeric(out.get("additional_sink_power_p95_mw"), errors="coerce")
        profile_status = out.get("additional_sink_profile_status", pd.Series("", index=out.index)).astype(str)
        bad_sink = (
            (add_needed > 0.0)
            & (
                sink_p95.isna()
                | (sink_p95 <= 0.0)
            )
            & (~profile_status.isin(["hourly_profile_unavailable", "invalid_reference_year", "insufficient_additional_energy"]))
        )
        if bool(bad_sink.any()):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q3_ADDITIONAL_SINK_POWER_INCONSISTENT",
                    "message": "additional_absorbed_needed_TWh_year>0 doit impliquer additional_sink_power_p95_mw>0 sauf profil indisponible.",
                }
            )
        if "scenario_id" not in out.columns or out["scenario_id"].astype(str).str.strip().eq("").any():
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q3_SCENARIO_ID_MISSING",
                    "message": "Chaque ligne Q3 doit inclure scenario_id.",
                }
            )
        required_cols = {
            "within_bounds",
            "predicted_sr_after",
            "target_sr",
            "predicted_h_negative_after",
            "target_h_negative",
            "predicted_h_below_5_after",
            "target_h_below_5",
        }
        if required_cols.issubset(set(out.columns)):
            tol = _safe_float(selection.get("q3_target_tolerance", 1e-6), 1e-6)
            wb = out["within_bounds"].fillna(False).astype(bool)
            pred_sr = pd.to_numeric(out["predicted_sr_after"], errors="coerce")
            tgt_sr = pd.to_numeric(out["target_sr"], errors="coerce")
            pred_hn = pd.to_numeric(out["predicted_h_negative_after"], errors="coerce")
            tgt_hn = pd.to_numeric(out["target_h_negative"], errors="coerce")
            pred_h5 = pd.to_numeric(out["predicted_h_below_5_after"], errors="coerce")
            tgt_h5 = pd.to_numeric(out["target_h_below_5"], errors="coerce")
            bad = wb & ((pred_sr > (tgt_sr + tol)) | (pred_hn > (tgt_hn + tol)) | (pred_h5 > (tgt_h5 + tol)))
            if bool(bad.any()):
                for _, bad_row in out.loc[bad, ["country", "scenario_id"]].iterrows():
                    checks.append(
                        {
                            "status": "FAIL",
                            "code": "TEST_Q3_001",
                            "message": f"{bad_row['country']}-{bad_row['scenario_id']}: within_bounds=true mais cible non tenue.",
                        }
                    )
            else:
                checks.append(
                    {
                        "status": "PASS",
                        "code": "TEST_Q3_001",
                        "message": "Toutes les lignes within_bounds=true respectent target_sr/target_h_negative/target_h_below_5.",
                    }
                )
        else:
            checks.append(
                {
                    "status": "WARN",
                    "code": "TEST_Q3_001",
                    "message": "Colonnes predicted/target non disponibles dans Q3_status; test non applicable.",
                }
            )
        k_required = pd.to_numeric(
            out.get("required_demand_uplift_mw", out.get("inversion_k_demand")),
            errors="coerce",
        )
        if bool((k_required < -1e-9).fillna(False).any()):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q3_REQUIRED_DEMAND_NEGATIVE",
                    "message": "required_demand_uplift_mw (alias inversion_k_demand) doit etre >= 0.",
                }
            )
        r_required = pd.to_numeric(
            out.get("required_mustrun_reduction_ratio", out.get("inversion_r_mustrun")),
            errors="coerce",
        )
        if bool((r_required < -1e-9).fillna(False).any()):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q3_REQUIRED_MUSTRUN_NEGATIVE",
                    "message": "required_mustrun_reduction_ratio (alias inversion_r_mustrun) doit etre >= 0.",
                }
            )
        if bool((r_required > 1.0 + 1e-9).fillna(False).any()):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q3_REQUIRED_MUSTRUN_GT_ONE",
                    "message": "required_mustrun_reduction_ratio doit rester dans [0,1].",
                }
            )

    if not q3_inversion_requirements.empty:
        ok_mask = q3_inversion_requirements["status"].astype(str).str.lower().isin(["ok", "already_ok"])
        pred_sr_nan = pd.to_numeric(q3_inversion_requirements["predicted_sr_after"], errors="coerce").isna()
        pred_h_nan = pd.to_numeric(q3_inversion_requirements["predicted_h_negative_after"], errors="coerce").isna()
        if bool((ok_mask & (pred_sr_nan | pred_h_nan)).any()):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q3_PREDICTED_NAN_WITH_STATUS_OK",
                    "message": "status in {ok,already_ok} doit fournir predicted_sr_after et predicted_h_negative_after.",
                }
            )

    checks.extend(build_common_checks(q1_panel))
    if not checks:
        checks.append({"status": "PASS", "code": "Q3_PASS", "message": "Q3 checks pass."})

    kpis = {
        "n_countries": int(out["country"].nunique()) if not out.empty else 0,
        "n_in_phase2": int((out.get("in_phase2") == True).sum()) if not out.empty else 0,
        "n_stop_possible": int((out.get("status") == "STOP_POSSIBLE").sum()) if not out.empty else 0,
        "n_stop_confirmed": int((out.get("status") == "STOP_CONFIRMED").sum()) if not out.empty else 0,
        "n_requirements_rows": int(len(q3_inversion_requirements)),
    }

    narrative = (
        "Q3 compare les familles actives a la bascule avec l'etat courant et classe "
        "CONTINUES / STOP_POSSIBLE / STOP_CONFIRMED / BACK_TO_STAGE1. "
        "En mode SCEN, la bascule historique est prioritaire comme reference. "
        "Les ordres de grandeur d'inversion couvrent demande et reduction must-run, "
        "et le besoin de puissance de sink est distribue sur profil horaire."
    )

    return ModuleResult(
        module_id="Q3",
        run_id=run_id,
        selection=selection,
        assumptions_used=assumptions_subset(assumptions_df, Q3_PARAMS),
        kpis=kpis,
        tables={
            "Q3_status": out,
            "q3_inversion_requirements": q3_inversion_requirements,
            "q3_quality_summary": q3_quality_summary,
        },
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
        mode=str(selection.get("mode", "HIST")).upper(),
        scenario_id=scenario_id,
        horizon_year=selection.get("horizon_year"),
    )
