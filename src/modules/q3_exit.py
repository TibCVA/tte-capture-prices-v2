"""Q3 - Exit from Phase 2 and inversion stop-conditions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.modules.common import assumptions_subset
from src.modules.q1_transition import run_q1
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
    share_thr = float(params.get("low_price_hours_share_stage2_min", h_low_thr / 8760.0))
    return bool(
        (np.isfinite(h_negative) and h_negative >= h_neg_thr)
        or (np.isfinite(h_below_5) and h_below_5 >= h_low_thr)
        or (np.isfinite(low_price_share) and low_price_share >= share_thr)
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


def _compute_hourly_proxy_metrics(
    hourly: pd.DataFrame,
    *,
    demand_uplift: float = 0.0,
    export_uplift: float = 0.0,
    flex_mw_additional: float = 0.0,
    export_coincidence_factor: float = 1.0,
) -> dict[str, float]:
    h = hourly.copy()
    if h.empty:
        return {"status": "NOT_CALCULABLE"}

    load = _safe_series(h, "load_mw", np.nan)
    if load.notna().sum() == 0:
        load = _safe_series(h, "load_total_mw", np.nan) - _safe_series(h, "psh_pump_mw", 0.0).fillna(0.0)
    vre = _safe_series(h, "gen_vre_mw", np.nan)
    if vre.notna().sum() == 0:
        vre = _safe_series(h, "gen_solar_mw", 0.0).fillna(0.0) + _safe_series(h, "gen_wind_on_mw", 0.0).fillna(0.0) + _safe_series(h, "gen_wind_off_mw", 0.0).fillna(0.0)
    must_run = _safe_series(h, "gen_must_run_mw", 0.0).fillna(0.0)
    net_position = _safe_series(h, "net_position_mw", 0.0).fillna(0.0)
    psh = _safe_series(h, "psh_pump_mw", 0.0).fillna(0.0).clip(lower=0.0)
    flex_obs = _safe_series(h, "flex_sink_observed_mw", np.nan)
    export_base = net_position.clip(lower=0.0)
    if flex_obs.notna().sum() == 0:
        flex_obs = export_base + psh
    else:
        flex_obs = flex_obs.fillna(0.0).clip(lower=0.0)

    load_after = load * (1.0 + max(0.0, float(demand_uplift)))
    nrl_after = load_after - vre - must_run
    surplus_after = (-nrl_after).clip(lower=0.0)

    export_after = export_base * (1.0 + max(0.0, float(export_uplift))) * max(0.0, float(export_coincidence_factor))
    other_sink = (flex_obs - export_base - psh).clip(lower=0.0)
    base_sink_after = export_after + psh + other_sink
    extra_flex_sink = pd.Series(0.0, index=h.index, dtype=float)
    if float(flex_mw_additional) > 0.0:
        extra_flex_sink = np.minimum(float(flex_mw_additional), surplus_after)
    sink_after = base_sink_after + extra_flex_sink
    absorbed_after = np.minimum(surplus_after, sink_after)
    unabsorbed_after = (surplus_after - absorbed_after).clip(lower=0.0)

    sr_hours_after = float((unabsorbed_after > 0.0).mean())
    nrl_q10 = _safe_float(pd.to_numeric(nrl_after, errors="coerce").quantile(0.10), np.nan)
    proxy_mask = (unabsorbed_after > 0.0)
    if np.isfinite(nrl_q10):
        proxy_mask = proxy_mask | (nrl_after <= nrl_q10)
    h_negative_proxy_after = float(proxy_mask.sum())

    return {
        "status": "OK",
        "sr_hours_after": sr_hours_after,
        "h_negative_proxy_after": h_negative_proxy_after,
        "surplus_unabsorbed_twh_after": float(unabsorbed_after.sum()) / 1e6,
    }


def _solve_lever_binary_search(
    eval_fn: Any,
    *,
    min_value: float,
    max_value: float,
    target_sr_hours: float,
    target_h_negative_proxy: float,
) -> dict[str, Any]:
    base = eval_fn(min_value)
    if str(base.get("status", "")) != "OK":
        return {"status": "NOT_CALCULABLE", "required_uplift": np.nan, **base}

    def _objective_ok(metrics: dict[str, Any]) -> bool:
        sr_ok = _safe_float(metrics.get("sr_hours_after"), np.nan) <= float(target_sr_hours)
        h_ok = _safe_float(metrics.get("h_negative_proxy_after"), np.nan) <= float(target_h_negative_proxy)
        return bool(sr_ok and h_ok)

    if _objective_ok(base):
        return {
            "status": "OK",
            "within_bounds": True,
            "required_uplift": float(min_value),
            **base,
        }

    hi_metrics = eval_fn(max_value)
    if str(hi_metrics.get("status", "")) != "OK":
        return {"status": "NOT_CALCULABLE", "required_uplift": np.nan, **hi_metrics}
    if not _objective_ok(hi_metrics):
        return {
            "status": "UNREACHABLE",
            "within_bounds": False,
            "required_uplift": np.nan,
            **hi_metrics,
        }

    lo = float(min_value)
    hi = float(max_value)
    best_metrics = hi_metrics
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        m = eval_fn(mid)
        if str(m.get("status", "")) != "OK":
            return {"status": "NOT_CALCULABLE", "required_uplift": np.nan, **m}
        if _objective_ok(m):
            hi = mid
            best_metrics = m
        else:
            lo = mid
        if abs(hi - lo) <= 1e-4:
            break
    return {
        "status": "OK",
        "within_bounds": True,
        "required_uplift": float(hi),
        **best_metrics,
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
    target_sr_hours = float(selection.get("target_sr_hours", all_params.get("stage1_sr_hours_max", 0.05)))
    target_h_negative_proxy = float(selection.get("target_h_negative", all_params.get("stage1_h_negative_max", 200.0)))
    max_export_uplift = max(0.0, float(selection.get("export_uplift_max", all_params.get("q1_lever_max_uplift", 1.0))))
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
            bascule_ref = np.nan
            bascule_source = "missing"
            c_sum_ref = None

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
                    "inversion_k_demand_status": "insufficient_scope",
                    "inversion_r_mustrun": np.nan,
                    "inversion_r_mustrun_status": "proxy_not_computed",
                    "inversion_f_flex": np.nan,
                    "inversion_f_flex_status": "proxy_not_computed",
                    "additional_absorbed_needed_TWh_year": np.nan,
                    "additional_sink_power_p95_mw": np.nan,
                    "additional_sink_profile_status": "hourly_profile_unavailable",
                    "warnings_quality": "missing_panel",
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
                        "within_bounds": False,
                        "target_sr": target_sr_hours,
                        "target_h_negative": target_h_negative_proxy,
                        "predicted_sr_after": np.nan,
                        "predicted_h_negative_after": np.nan,
                        "predicted_h_negative_metric": "PROXY_SURPLUS_OR_LOW_NRL",
                        "applicability_flag": "HORS_SCOPE_PHASE2",
                        "status": "NOT_CALCULABLE",
                        "reason": "missing_panel",
                    }
                )
            continue

        if not np.isfinite(bascule_ref):
            last_any = c_panel.iloc[-1]
            rows.append(
                {
                    "country": country,
                    **audit_common,
                    "reference_year": int(_safe_float(last_any.get("year"), np.nan)) if np.isfinite(_safe_float(last_any.get("year"), np.nan)) else np.nan,
                    "in_phase2": False,
                    "status": "HORS_SCOPE_PHASE2",
                    "reason_code": "q1_no_bascule",
                    "status_explanation": "Absence de bascule de reference.",
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
                    "inversion_k_demand_status": "insufficient_scope",
                    "inversion_r_mustrun": np.nan,
                    "inversion_r_mustrun_status": "proxy_not_computed",
                    "inversion_f_flex": np.nan,
                    "inversion_f_flex_status": "proxy_not_computed",
                    "additional_absorbed_needed_TWh_year": np.nan,
                    "additional_sink_power_p95_mw": np.nan,
                    "additional_sink_profile_status": "hourly_profile_unavailable",
                    "warnings_quality": "q1_no_bascule",
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
                        "within_bounds": False,
                        "target_sr": target_sr_hours,
                        "target_h_negative": target_h_negative_proxy,
                        "predicted_sr_after": np.nan,
                        "predicted_h_negative_after": np.nan,
                        "predicted_h_negative_metric": "PROXY_SURPLUS_OR_LOW_NRL",
                        "applicability_flag": "HORS_SCOPE_PHASE2",
                        "status": "HORS_SCOPE_PHASE2",
                        "reason": "q1_no_bascule",
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

        trend_capture = _trend_slope(recent.get("year"), recent.get("capture_ratio_pv"))
        trend_hneg = _trend_slope(recent.get("year"), recent.get("h_negative_obs"))
        trend_h_zero_or_negative = (
            _trend_slope(recent.get("year"), recent.get("h_zero_or_negative"))
            if "h_zero_or_negative" in recent.columns
            else np.nan
        )

        in_phase2_current = bool(last.get("is_phase2_market", False))
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

        if hourly_ref is None or hourly_ref.empty:
            demand_solver = {"status": "NOT_CALCULABLE", "required_uplift": np.nan, "reason": "hourly_profile_unavailable"}
            export_solver = {"status": "NOT_CALCULABLE", "required_uplift": np.nan, "reason": "hourly_profile_unavailable"}
            flex_solver = {"status": "NOT_CALCULABLE", "required_uplift": np.nan, "reason": "hourly_profile_unavailable"}
        else:
            demand_solver = _solve_lever_binary_search(
                lambda x: _compute_hourly_proxy_metrics(
                    hourly_ref,
                    demand_uplift=x,
                    export_uplift=0.0,
                    flex_mw_additional=0.0,
                    export_coincidence_factor=export_coincidence_factor,
                ),
                min_value=0.0,
                max_value=max(0.0, float(params.get("demand_k_max", 0.30))),
                target_sr_hours=target_sr_hours,
                target_h_negative_proxy=target_h_negative_proxy,
            )
            export_solver = _solve_lever_binary_search(
                lambda x: _compute_hourly_proxy_metrics(
                    hourly_ref,
                    demand_uplift=0.0,
                    export_uplift=x,
                    flex_mw_additional=0.0,
                    export_coincidence_factor=export_coincidence_factor,
                ),
                min_value=0.0,
                max_value=max_export_uplift,
                target_sr_hours=target_sr_hours,
                target_h_negative_proxy=target_h_negative_proxy,
            )
            flex_cap = _safe_float(selection.get("flex_mw_max"), np.nan)
            if not np.isfinite(flex_cap) or flex_cap <= 0.0:
                nrl_proxy = _safe_series(hourly_ref, "nrl_mw", np.nan)
                if nrl_proxy.notna().sum() > 0:
                    flex_cap = max(1.0, float((-nrl_proxy).clip(lower=0.0).quantile(0.95)) * 1.5)
                else:
                    load_proxy = _safe_series(hourly_ref, "load_mw", np.nan)
                    flex_cap = max(1.0, _safe_float(load_proxy.quantile(0.5), 1000.0) * 0.05)
            flex_solver = _solve_lever_binary_search(
                lambda x: _compute_hourly_proxy_metrics(
                    hourly_ref,
                    demand_uplift=0.0,
                    export_uplift=0.0,
                    flex_mw_additional=x,
                    export_coincidence_factor=export_coincidence_factor,
                ),
                min_value=0.0,
                max_value=float(flex_cap),
                target_sr_hours=target_sr_hours,
                target_h_negative_proxy=target_h_negative_proxy,
            )

        for lever, solver in [
            ("demand_uplift", demand_solver),
            ("export_uplift", export_solver),
            ("flex_uplift", flex_solver),
        ]:
            raw_status = str(solver.get("status", "NOT_CALCULABLE")).upper()
            if raw_status not in {"OK", "UNREACHABLE", "NOT_CALCULABLE"}:
                raw_status = "NOT_CALCULABLE"
            req_uplift = _safe_float(solver.get("required_uplift"), np.nan)
            pred_sr_after = _safe_float(solver.get("sr_hours_after"), np.nan)
            pred_hneg_after = _safe_float(solver.get("h_negative_proxy_after"), np.nan)
            if raw_status == "OK" and not np.isfinite(req_uplift):
                raw_status = "NOT_CALCULABLE"
            requirement_rows.append(
                {
                    "country": country,
                    "scenario_id": scenario_id,
                    "year": hourly_ref_year if hourly_ref_year is not None else (ref_year_int if ref_year_int is not None else np.nan),
                    "lever": lever,
                    "required_uplift": req_uplift,
                    "within_bounds": bool(solver.get("within_bounds", False)) if in_phase2_current else False,
                    "target_sr": target_sr_hours,
                    "target_h_negative": target_h_negative_proxy,
                    "predicted_sr_after": pred_sr_after,
                    "predicted_h_negative_after": pred_hneg_after,
                    "predicted_h_negative_metric": "PROXY_SURPLUS_OR_LOW_NRL",
                    "applicability_flag": "APPLICABLE" if in_phase2_current else "HORS_SCOPE_PHASE2",
                    "status": raw_status if in_phase2_current else "HORS_SCOPE_PHASE2",
                    "reason": str(solver.get("reason", raw_status.lower())),
                    "export_coincidence_factor": export_coincidence_factor,
                }
            )

        demand_status = str(demand_solver.get("status", "NOT_CALCULABLE")).upper()
        if in_phase2_current:
            if demand_status == "OK" and _safe_float(demand_solver.get("required_uplift"), np.nan) <= 1e-6:
                status = "STOP_CONFIRMED"
                reason_code = "already_meets_targets"
                status_explanation = "Les cibles proxy sont deja respectees."
            elif demand_status == "UNREACHABLE":
                status = "CONTINUES"
                reason_code = "targets_unreachable_within_bounds"
                status_explanation = "Les cibles proxy ne sont pas atteignables dans les bornes du levier."
            elif demand_status == "NOT_CALCULABLE":
                status = "CONTINUES"
                reason_code = "not_calculable"
                status_explanation = "Le calcul du levier demande est indisponible."
            else:
                status = "CONTINUES"
                reason_code = "no_family_turned_off"
                status_explanation = "Une hausse de demande est necessaire pour respecter les cibles proxy."
        else:
            status = "HORS_SCOPE_PHASE2"
            reason_code = "not_in_phase2"
            status_explanation = "Le pays n'est pas en phase2 sur l'annee de reference."

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

        rows.append(
            {
                "country": country,
                **audit_common,
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
                "inversion_k_demand": _safe_float(demand_solver.get("required_uplift"), np.nan),
                "inversion_k_demand_status": demand_status.lower(),
                "inversion_r_mustrun": mustrun_reduction_needed,
                "inversion_r_mustrun_status": mustrun_status,
                "inversion_f_flex": _safe_float(flex_solver.get("required_uplift"), np.nan),
                "inversion_f_flex_status": str(flex_solver.get("status", "NOT_CALCULABLE")).upper().lower(),
                "additional_absorbed_needed_TWh_year": demand_uplift_twh,
                "additional_sink_power_p95_mw": sink_p95,
                "additional_sink_profile_status": sink_profile_status,
                "warnings_quality": "" if sink_profile_status in {"profile_weighted_surplus", "no_additional_energy_required"} else sink_profile_status,
                "bascule_reference_year": float(int(bascule_ref)),
                "bascule_reference_source": bascule_source,
                "families_active_at_bascule": ",".join(sorted(active_bascule)),
                "turned_off_low_price": bool(turned_off_map["LOW_PRICE"]),
                "turned_off_physical": bool(turned_off_map["PHYSICAL"]),
                "turned_off_value_pv": bool(turned_off_map["VALUE_PV"]),
                "turned_off_value_wind": bool(turned_off_map["VALUE_WIND"]),
                "turned_off_family_any": bool(turned_off_any),
                "turned_off_family_persistent_2y": bool(persistent_off),
                "within_bounds": bool(demand_solver.get("within_bounds", False)) if in_phase2_current else False,
                "target_sr": target_sr_hours,
                "target_h_negative": target_h_negative_proxy,
                "predicted_sr_after": _safe_float(demand_solver.get("sr_hours_after"), np.nan),
                "predicted_h_negative_after": _safe_float(demand_solver.get("h_negative_proxy_after"), np.nan),
                "predicted_h_negative_metric": "PROXY_SURPLUS_OR_LOW_NRL",
                "q2_slope_above_target": bool(np.isfinite(q2_slope) and q2_slope >= slope_capture_target),
            }
        )

    out = pd.DataFrame(rows)
    q3_inversion_requirements = pd.DataFrame(requirement_rows)
    if out.empty:
        checks.append({"status": "FAIL", "code": "Q3_EMPTY", "message": "Aucune sortie Q3."})
    else:
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
        }
        if required_cols.issubset(set(out.columns)):
            tol = _safe_float(selection.get("q3_target_tolerance", 1e-6), 1e-6)
            wb = out["within_bounds"].fillna(False).astype(bool)
            pred_sr = pd.to_numeric(out["predicted_sr_after"], errors="coerce")
            tgt_sr = pd.to_numeric(out["target_sr"], errors="coerce")
            pred_hn = pd.to_numeric(out["predicted_h_negative_after"], errors="coerce")
            tgt_hn = pd.to_numeric(out["target_h_negative"], errors="coerce")
            bad = wb & ((pred_sr > (tgt_sr + tol)) | (pred_hn > (tgt_hn + tol)))
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
                        "message": "Toutes les lignes within_bounds=true respectent target_sr et target_h_negative.",
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

    if not q3_inversion_requirements.empty:
        ok_mask = q3_inversion_requirements["status"].astype(str).str.upper() == "OK"
        pred_sr_nan = pd.to_numeric(q3_inversion_requirements["predicted_sr_after"], errors="coerce").isna()
        pred_h_nan = pd.to_numeric(q3_inversion_requirements["predicted_h_negative_after"], errors="coerce").isna()
        if bool((ok_mask & (pred_sr_nan | pred_h_nan)).any()):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q3_PREDICTED_NAN_WITH_STATUS_OK",
                    "message": "status=OK doit fournir predicted_sr_after et predicted_h_negative_after.",
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
        tables={"Q3_status": out, "q3_inversion_requirements": q3_inversion_requirements},
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
        mode=str(selection.get("mode", "HIST")).upper(),
        scenario_id=scenario_id,
        horizon_year=selection.get("horizon_year"),
    )
