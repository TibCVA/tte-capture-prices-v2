"""Q1 - Phase 1 to Phase 2 transition analysis."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.constants import COL_GEN_TOTAL, COL_LOAD_NET, COL_MUST_RUN_MODE
from src.core.definitions import compute_scope_coverage_lowload
from src.modules.common import assumptions_subset
from src.modules.reality_checks import build_common_checks
from src.modules.result import ModuleResult

Q1_RULE_VERSION = "q1_rule_v3_2026_02_11"

Q1_PARAMS = [
    "h_negative_stage2_min",
    "h_negative_stage2_strong",
    "h_below_5_stage2_min",
    "capture_ratio_pv_stage2_max",
    "capture_ratio_wind_stage2_max",
    "capture_ratio_pv_vs_ttl_stage2_max",
    "capture_ratio_pv_vs_ttl_crisis_max",
    "days_spread_gt50_stage2_min",
    "sr_energy_material_min",
    "sr_hours_material_min",
    "far_energy_tension_max",
    "ir_p10_high_min",
    "regime_coherence_min_for_causality",
    "stage1_h_negative_max",
    "stage1_h_below_5_max",
    "stage1_capture_ratio_pv_vs_ttl_min",
    "stage1_days_spread_gt50_max",
    "stage2_score_threshold",
    "q1_persistence_window_years",
    "q1_lever_max_uplift",
]


def _safe_param(params: dict[str, float], key: str, default: float) -> float:
    v = params.get(key, default)
    try:
        return float(v)
    except Exception:
        return float(default)


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


def _safe_ratio(a: Any, b: Any) -> float:
    aa = _safe_float(a, np.nan)
    bb = _safe_float(b, np.nan)
    if not (np.isfinite(aa) and np.isfinite(bb)) or bb == 0:
        return float("nan")
    return float(aa / bb)


def _quantile(series: pd.Series, q: float) -> float:
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return float("nan")
    return float(s.quantile(q))


def _is_stage1(row: pd.Series, p: dict[str, float]) -> bool:
    return bool(
        float(row.get("h_negative_obs", np.nan)) <= _safe_param(p, "stage1_h_negative_max", 100.0)
        and float(row.get("h_below_5_obs", np.nan)) <= _safe_param(p, "stage1_h_below_5_max", 300.0)
        and float(row.get("capture_ratio_pv_vs_ttl", np.nan)) >= _safe_param(p, "stage1_capture_ratio_pv_vs_ttl_min", 0.9)
        and float(row.get("days_spread_gt50", np.nan)) <= _safe_param(p, "stage1_days_spread_gt50_max", 120.0)
    )


def _build_rule_definition(params: dict[str, float]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "q1_rule_version": Q1_RULE_VERSION,
                "score_min_phase2_market": _safe_param(params, "stage2_score_threshold", 3.0),
                "h_negative_stage2_min": _safe_param(params, "h_negative_stage2_min", 200.0),
                "h_negative_stage2_strong": _safe_param(params, "h_negative_stage2_strong", 300.0),
                "h_below_5_stage2_min": _safe_param(params, "h_below_5_stage2_min", 500.0),
                "capture_ratio_pv_stage2_max": _safe_param(params, "capture_ratio_pv_stage2_max", 0.90),
                "capture_ratio_wind_stage2_max": _safe_param(params, "capture_ratio_wind_stage2_max", 0.90),
                "capture_ratio_pv_vs_ttl_stage2_max": _safe_param(params, "capture_ratio_pv_vs_ttl_stage2_max", 0.8),
                "days_spread_gt50_stage2_min": _safe_param(params, "days_spread_gt50_stage2_min", 150.0),
                "sr_energy_material_min": _safe_param(params, "sr_energy_material_min", 0.01),
                "far_energy_tension_max": _safe_param(params, "far_energy_tension_max", 0.95),
                "ir_p10_high_min": _safe_param(params, "ir_p10_high_min", 0.70),
                "persistence_window_years": _safe_param(params, "q1_persistence_window_years", 3.0),
                "rule_logic": (
                    "phase2_candidate=(>=1 LOW_PRICE flag OR >=1 PHYSICAL flag); "
                    "CAPTURE-only forbidden; stage2 score must be >= threshold."
                ),
            }
        ]
    )


def _flag_list(row: pd.Series) -> str:
    names: list[str] = []
    for col in [
        "flag_h_negative_stage2",
        "flag_h_below_5_stage2",
        "flag_p10_price_below_0",
        "flag_capture_pv_low",
        "flag_capture_wind_low",
        "flag_sr_high",
        "flag_far_low",
        "flag_ir_high",
        "flag_spread_high",
    ]:
        if bool(row.get(col, False)):
            names.append(col)
    return ",".join(names)


def _apply_phase2_logic(panel: pd.DataFrame, p: dict[str, float]) -> pd.DataFrame:
    out = panel.copy()
    if "capture_ratio_pv" not in out.columns:
        out["capture_ratio_pv"] = out.get("capture_ratio_pv_vs_baseload", np.nan)
    if "capture_ratio_wind" not in out.columns:
        out["capture_ratio_wind"] = out.get("capture_ratio_wind_vs_baseload", np.nan)
    if "sr_energy_share_load" not in out.columns:
        out["sr_energy_share_load"] = out.get("sr_energy", np.nan)
    if "sr_hours_share" not in out.columns:
        out["sr_hours_share"] = out.get("sr_hours", np.nan)

    out["flag_h_negative_stage2"] = pd.to_numeric(out.get("h_negative_obs"), errors="coerce") >= _safe_param(p, "h_negative_stage2_min", 200.0)
    out["flag_h_negative_strong_stage2"] = pd.to_numeric(out.get("h_negative_obs"), errors="coerce") >= _safe_param(p, "h_negative_stage2_strong", 300.0)
    out["flag_h_below_5_stage2"] = pd.to_numeric(out.get("h_below_5_obs"), errors="coerce") >= _safe_param(p, "h_below_5_stage2_min", 500.0)
    out["flag_p10_price_below_0"] = pd.to_numeric(out.get("p10_price_da_eur_mwh"), errors="coerce") < 0.0
    out["flag_capture_pv_low"] = (
        (pd.to_numeric(out.get("capture_ratio_pv"), errors="coerce") <= _safe_param(p, "capture_ratio_pv_stage2_max", 0.90))
        | (pd.to_numeric(out.get("capture_ratio_pv_vs_ttl"), errors="coerce") <= _safe_param(p, "capture_ratio_pv_vs_ttl_stage2_max", 0.8))
    )
    out["flag_capture_wind_low"] = pd.to_numeric(out.get("capture_ratio_wind"), errors="coerce") <= _safe_param(p, "capture_ratio_wind_stage2_max", 0.90)
    out["flag_sr_high"] = pd.to_numeric(out.get("sr_energy_share_load"), errors="coerce") >= _safe_param(p, "sr_energy_material_min", 0.01)
    out["flag_far_low"] = pd.to_numeric(out.get("far_energy"), errors="coerce") <= _safe_param(p, "far_energy_tension_max", 0.95)
    out["flag_ir_high"] = pd.to_numeric(out.get("ir_p10"), errors="coerce") >= _safe_param(p, "ir_p10_high_min", 0.70)
    out["flag_spread_high"] = pd.to_numeric(out.get("days_spread_gt50"), errors="coerce") >= _safe_param(p, "days_spread_gt50_stage2_min", 150.0)

    out["low_price_flags_count"] = (
        out[["flag_h_negative_stage2", "flag_h_below_5_stage2", "flag_p10_price_below_0"]]
        .fillna(False)
        .astype(int)
        .sum(axis=1)
    )
    out["capture_flags_count"] = out[["flag_capture_pv_low", "flag_capture_wind_low"]].fillna(False).astype(int).sum(axis=1)
    out["physical_flags_count"] = out[["flag_sr_high", "flag_far_low", "flag_ir_high"]].fillna(False).astype(int).sum(axis=1)

    out["stage2_points_low_price"] = out["low_price_flags_count"] * 2 + out["flag_h_negative_strong_stage2"].fillna(False).astype(int)
    out["stage2_points_capture"] = out["capture_flags_count"] * 1
    out["stage2_points_physical"] = out["physical_flags_count"] * 2
    out["stage2_points_vol"] = out["flag_spread_high"].fillna(False).astype(int)
    out["stage2_market_score"] = (
        out["stage2_points_low_price"] + out["stage2_points_capture"] + out["stage2_points_physical"] + out["stage2_points_vol"]
    )
    out["score_breakdown"] = out.apply(
        lambda r: f"low={int(r['stage2_points_low_price'])};cap={int(r['stage2_points_capture'])};phys={int(r['stage2_points_physical'])};vol={int(r['stage2_points_vol'])}",
        axis=1,
    )

    out["phase2_candidate_year"] = (out["low_price_flags_count"] >= 1) | (out["physical_flags_count"] >= 1)
    out["flag_capture_only_stage2"] = (out["capture_flags_count"] > 0) & (out["low_price_flags_count"] == 0) & (out["physical_flags_count"] == 0)
    out["is_phase2_market"] = (
        out["phase2_candidate_year"]
        & (out["stage2_market_score"] >= _safe_param(p, "stage2_score_threshold", 3.0))
        & (~out["flag_capture_only_stage2"])
    )
    out["is_phase2_physical"] = out["physical_flags_count"] >= 1
    out["signal_low_price"] = out["low_price_flags_count"] >= 1
    out["signal_value"] = out["capture_flags_count"] >= 1
    out["signal_physical"] = out["physical_flags_count"] >= 1
    out["flag_non_capture_stage2"] = (out["low_price_flags_count"] > 0).astype(int) + (out["physical_flags_count"] > 0).astype(int)
    out["active_flags"] = out.apply(_flag_list, axis=1)

    out["is_stage1_criteria"] = out.apply(lambda row: _is_stage1(row, p), axis=1)
    out["phase_market"] = np.select(
        [out["is_phase2_market"], out["is_stage1_criteria"]],
        ["phase2", "phase1"],
        default="uncertain",
    )
    out["stress_phys_state"] = np.select(
        [
            pd.to_numeric(out["sr_energy_share_load"], errors="coerce") < _safe_param(p, "sr_energy_material_min", 0.01),
            (pd.to_numeric(out["sr_energy_share_load"], errors="coerce") >= _safe_param(p, "sr_energy_material_min", 0.01))
            & (pd.to_numeric(out["far_energy"], errors="coerce") > _safe_param(p, "far_energy_tension_max", 0.95)),
            (pd.to_numeric(out["sr_energy_share_load"], errors="coerce") >= _safe_param(p, "sr_energy_material_min", 0.01))
            & (pd.to_numeric(out["far_energy"], errors="coerce") <= _safe_param(p, "far_energy_tension_max", 0.95)),
        ],
        ["pas_de_surplus_structurel", "surplus_present_mais_absorbe", "surplus_non_absorbe"],
        default="unknown",
    )
    return out


def _first_persistent_year(group: pd.DataFrame, col: str, window_years: int) -> float:
    if group.empty or col not in group.columns:
        return float("nan")
    years = pd.to_numeric(group["year"], errors="coerce").to_numpy(dtype=float)
    flags = group[col].fillna(False).astype(bool).to_numpy()
    w = max(3, int(window_years))
    for i in range(len(group)):
        if not flags[i]:
            continue
        # 2 of 3 condition.
        j0 = max(0, i - (w - 1))
        if int(flags[j0 : i + 1].sum()) >= 2:
            if i > 0 and flags[i - 1]:
                # Consecutive years robustness.
                y_prev = years[i - 1]
                if np.isfinite(y_prev):
                    return float(int(y_prev))
            y = years[i]
            if np.isfinite(y):
                return float(int(y))
    return float("nan")


def _is_market_persistent(group: pd.DataFrame, bascule_year: float) -> bool:
    if not np.isfinite(bascule_year):
        return False
    y0 = int(bascule_year)
    subset = group[(group["year"] >= y0) & (group["year"] <= y0 + 2)]
    if subset.empty:
        return False
    return int(subset["is_phase2_market"].fillna(False).astype(bool).sum()) >= 2


def _adjust_for_lever(group: pd.DataFrame, demand_uplift: float = 0.0, flex_uplift: float = 0.0) -> pd.DataFrame:
    g = group.copy()
    demand_factor = max(1.0, 1.0 + float(demand_uplift))
    flex_factor = max(1.0, 1.0 + float(flex_uplift))
    h_factor = demand_factor * (1.0 + 0.8 * float(flex_uplift))

    g["h_negative_obs"] = pd.to_numeric(g.get("h_negative_obs"), errors="coerce") / h_factor
    g["h_below_5_obs"] = pd.to_numeric(g.get("h_below_5_obs"), errors="coerce") / h_factor
    g["days_spread_gt50"] = pd.to_numeric(g.get("days_spread_gt50"), errors="coerce") / demand_factor
    g["sr_energy"] = pd.to_numeric(g.get("sr_energy"), errors="coerce") / demand_factor
    g["sr_hours"] = pd.to_numeric(g.get("sr_hours"), errors="coerce") / demand_factor
    g["ir_p10"] = pd.to_numeric(g.get("ir_p10"), errors="coerce") / demand_factor
    far = pd.to_numeric(g.get("far_energy"), errors="coerce")
    g["far_energy"] = 1.0 - (1.0 - far) / flex_factor
    cap_pv = pd.to_numeric(g.get("capture_ratio_pv"), errors="coerce")
    cap_pv_ttl = pd.to_numeric(g.get("capture_ratio_pv_vs_ttl"), errors="coerce")
    cap_w = pd.to_numeric(g.get("capture_ratio_wind"), errors="coerce")
    cap_boost = 0.10 * float(demand_uplift) + 0.08 * float(flex_uplift)
    g["capture_ratio_pv"] = (cap_pv + cap_boost).clip(lower=0.0, upper=2.0)
    g["capture_ratio_pv_vs_ttl"] = (cap_pv_ttl + cap_boost).clip(lower=0.0, upper=2.0)
    g["capture_ratio_wind"] = (cap_w + cap_boost).clip(lower=0.0, upper=2.0)
    return g


def _required_lever_to_avoid_phase2(group: pd.DataFrame, p: dict[str, float], lever: str, max_uplift: float) -> tuple[float | None, str]:
    scoped = group.sort_values("year").copy()
    if scoped.empty:
        return None, "insufficient_data"
    baseline = _apply_phase2_logic(scoped, p)
    y0 = _first_persistent_year(baseline, "is_phase2_market", _safe_param(p, "q1_persistence_window_years", 3.0))
    if not np.isfinite(y0):
        return 0.0, "already_not_phase2"

    hi = float(max(0.0, max_uplift))
    lo = 0.0

    def _cond(x: float) -> bool:
        if lever == "demand":
            adj = _adjust_for_lever(scoped, demand_uplift=x, flex_uplift=0.0)
        else:
            adj = _adjust_for_lever(scoped, demand_uplift=0.0, flex_uplift=x)
        panel_x = _apply_phase2_logic(adj, p)
        return not np.isfinite(_first_persistent_year(panel_x, "is_phase2_market", _safe_param(p, "q1_persistence_window_years", 3.0)))

    if _cond(lo):
        return 0.0, "already_not_phase2"
    if not _cond(hi):
        return None, "beyond_plausible_bounds"

    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if _cond(mid):
            hi = mid
        else:
            lo = mid
        if abs(hi - lo) <= 1e-4:
            break
    return float(hi), "ok"


def _ir_case_class(row: pd.Series) -> str:
    load_ratio = _safe_ratio(row.get("p10_load_mw"), row.get("p50_load_mw"))
    mr_ratio = _safe_ratio(row.get("p10_must_run_mw"), row.get("p50_must_run_mw"))
    if np.isfinite(load_ratio) and load_ratio < 0.60:
        return "load_valley_effect"
    if np.isfinite(mr_ratio) and mr_ratio > 0.90:
        return "must_run_floor_effect"
    return "mixed"


def _build_before_after_bascule(panel: pd.DataFrame, summary: pd.DataFrame) -> pd.DataFrame:
    metrics = ["capture_ratio_pv_vs_ttl", "h_negative_obs", "sr_energy", "far_energy", "ir_p10"]
    rows: list[dict[str, Any]] = []
    if panel.empty or summary.empty:
        return pd.DataFrame()

    for _, srow in summary.iterrows():
        country = str(srow.get("country", ""))
        bascule = _safe_float(srow.get("bascule_year_market"), np.nan)
        group = panel[panel["country"].astype(str) == country].sort_values("year")
        if group.empty:
            continue

        if np.isfinite(bascule):
            b_year = int(bascule)
            pre = group[(group["year"] >= b_year - 3) & (group["year"] <= b_year - 1)]
            post = group[(group["year"] >= b_year) & (group["year"] <= b_year + 2)]
            pre_start = int(b_year - 3)
            pre_end = int(b_year - 1)
            post_start = int(b_year)
            post_end = int(b_year + 2)
        else:
            b_year = np.nan
            pre = group.iloc[0:0]
            post = group.iloc[0:0]
            pre_start = np.nan
            pre_end = np.nan
            post_start = np.nan
            post_end = np.nan

        out: dict[str, Any] = {
            "country": country,
            "bascule_year_market": b_year,
            "pre_window_start_year": pre_start,
            "pre_window_end_year": pre_end,
            "post_window_start_year": post_start,
            "post_window_end_year": post_end,
            "n_pre_years": int(len(pre)),
            "n_post_years": int(len(post)),
        }
        for metric in metrics:
            pre_mean = _safe_float(pd.to_numeric(pre.get(metric), errors="coerce").mean(), np.nan)
            post_mean = _safe_float(pd.to_numeric(post.get(metric), errors="coerce").mean(), np.nan)
            out[f"pre_mean_{metric}"] = pre_mean
            out[f"post_mean_{metric}"] = post_mean
            out[f"delta_post_minus_pre_{metric}"] = (
                post_mean - pre_mean if np.isfinite(pre_mean) and np.isfinite(post_mean) else np.nan
            )
        rows.append(out)
    return pd.DataFrame(rows)


def _build_scope_audit(
    panel: pd.DataFrame,
    hourly_by_country_year: dict[tuple[str, int], pd.DataFrame] | None,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if panel.empty:
        return pd.DataFrame()

    for _, prow in panel.iterrows():
        country = str(prow.get("country", ""))
        year = int(prow.get("year"))
        key = (country, year)
        status = "NON_TESTABLE"
        reason = "hourly_missing"
        coverage = np.nan
        lowload_p20 = np.nan
        load_mode = ""
        must_run_mode = ""

        if hourly_by_country_year is not None and key in hourly_by_country_year:
            hourly = hourly_by_country_year[key]
            if hourly is not None and not hourly.empty:
                load = pd.to_numeric(hourly.get(COL_LOAD_NET), errors="coerce")
                mr = pd.to_numeric(hourly.get("gen_must_run_mw"), errors="coerce")
                gen_total = pd.to_numeric(hourly.get(COL_GEN_TOTAL), errors="coerce")
                coverage = compute_scope_coverage_lowload(load, mr, gen_total, lowload_quantile=0.20)
                lowload_p20 = _quantile(load, 0.20)
                load_mode = str(hourly.get("load_net_mode", pd.Series(dtype=object)).dropna().iloc[0]) if "load_net_mode" in hourly.columns and hourly["load_net_mode"].notna().any() else ""
                must_run_mode = str(hourly.get(COL_MUST_RUN_MODE, pd.Series(dtype=object)).dropna().iloc[0]) if COL_MUST_RUN_MODE in hourly.columns and hourly[COL_MUST_RUN_MODE].notna().any() else ""
                ir = _safe_float(prow.get("ir_p10"), np.nan)
                if not np.isfinite(coverage):
                    status = "NON_TESTABLE"
                    reason = "no_lowload_generation"
                elif coverage < 0.05 and np.isfinite(ir) and ir > 0.30:
                    status = "WARN"
                    reason = "low_coverage_high_ir_contradiction"
                elif coverage > 0.60:
                    status = "WARN"
                    reason = "high_coverage_possible_overestimate"
                else:
                    status = "INFO"
                    reason = "coverage_coherent"

        rows.append(
            {
                "country": country,
                "year": year,
                "must_run_scope_coverage": coverage,
                "lowload_p20_mw": lowload_p20,
                "ir_p10": _safe_float(prow.get("ir_p10"), np.nan),
                "scope_status": status,
                "scope_reason": reason,
                "load_net_mode": load_mode,
                "must_run_mode_hourly": must_run_mode,
            }
        )

    return pd.DataFrame(rows).sort_values(["country", "year"]).reset_index(drop=True)


def run_q1(
    annual_df: pd.DataFrame,
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
    hourly_by_country_year: dict[tuple[str, int], pd.DataFrame] | None = None,
) -> ModuleResult:
    countries = selection.get("countries", sorted(annual_df["country"].dropna().unique().tolist()))
    years = selection.get("years", sorted(annual_df["year"].dropna().unique().tolist()))

    panel = annual_df[annual_df["country"].isin(countries) & annual_df["year"].isin(years)].copy()
    panel = panel.sort_values(["country", "year"]).reset_index(drop=True)
    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q1_PARAMS)].iterrows()
    }

    panel = _apply_phase2_logic(panel, params)
    panel["quality_ok"] = panel.get("quality_flag", pd.Series("WARN", index=panel.index)).fillna("WARN").astype(str) != "FAIL"

    checks: list[dict[str, str]] = []
    warnings: list[str] = []
    summary_rows: list[dict[str, Any]] = []
    persist_window = int(_safe_param(params, "q1_persistence_window_years", 3.0))
    max_lever = float(_safe_param(params, "q1_lever_max_uplift", 1.0))

    for country, group in panel.groupby("country"):
        group = group.sort_values("year").copy()
        gq = group[group["quality_ok"]]
        bascule_year = _first_persistent_year(gq, "is_phase2_market", persist_window)
        physical_year = _first_persistent_year(gq, "is_phase2_physical", persist_window)
        at = group[group["year"] == int(bascule_year)].iloc[0] if np.isfinite(bascule_year) else group.iloc[-1]

        confidence = 1.0 if np.isfinite(bascule_year) else 0.0
        if np.isfinite(bascule_year):
            y0 = int(bascule_year)
            around = group[(group["year"] >= y0 - 1) & (group["year"] <= y0 + 1)].copy()
            if not around.empty:
                low_coherence = pd.to_numeric(around.get("regime_coherence"), errors="coerce") < 0.20
                if bool(low_coherence.fillna(False).any()):
                    confidence -= 0.25
                if bool(around.get("flag_capture_only_stage2", pd.Series(False)).fillna(False).any()):
                    confidence -= 0.20
                bad_quality = around.get("quality_flag", pd.Series(dtype=object)).astype(str).str.upper() != "OK"
                if bool(bad_quality.fillna(False).any()):
                    confidence -= 0.10
            if not _is_market_persistent(group, bascule_year):
                confidence -= 0.20
        confidence = float(np.clip(confidence, 0.0, 1.0))

        req_demand, req_demand_status = _required_lever_to_avoid_phase2(group, params, "demand", max_uplift=max_lever)
        req_flex, req_flex_status = _required_lever_to_avoid_phase2(group, params, "flex", max_uplift=max_lever)

        rationale = (
            "Bascule validee: condition candidate (low-price/physical) + score + persistance."
            if np.isfinite(bascule_year)
            else "Pas de bascule persistante sur la fenetre."
        )

        summary_rows.append(
            {
                "country": country,
                "bascule_year_market": bascule_year,
                "bascule_year_physical": physical_year,
                "bascule_confidence": confidence,
                "drivers_at_bascule": at.get("active_flags", ""),
                "low_price_flags_count_at_bascule": int(_safe_float(at.get("low_price_flags_count"), 0.0)),
                "physical_flags_count_at_bascule": int(_safe_float(at.get("physical_flags_count"), 0.0)),
                "capture_flags_count_at_bascule": int(_safe_float(at.get("capture_flags_count"), 0.0)),
                "stage2_market_score_at_bascule": _safe_float(at.get("stage2_market_score"), np.nan),
                "score_breakdown_at_bascule": str(at.get("score_breakdown", "")),
                "required_demand_uplift_to_avoid_phase2": req_demand,
                "required_demand_uplift_status": req_demand_status,
                "required_flex_uplift_to_avoid_phase2": req_flex,
                "required_flex_uplift_status": req_flex_status,
                "bascule_rationale": rationale,
                "sr_energy_at_bascule": at.get("sr_energy", np.nan),
                "far_energy_at_bascule": at.get("far_energy", np.nan),
                "ir_p10_at_bascule": at.get("ir_p10", np.nan),
                "ttl_at_bascule": at.get("ttl_eur_mwh", np.nan),
                "capture_ratio_pv_vs_ttl_at_bascule": at.get("capture_ratio_pv_vs_ttl", np.nan),
                "h_negative_at_bascule": at.get("h_negative_obs", np.nan),
                "notes_quality": "coherence_low"
                if float(at.get("regime_coherence", 1.0)) < _safe_param(params, "regime_coherence_min_for_causality", 0.55)
                else "ok",
            }
        )

    for _, row in panel.iterrows():
        if bool(row.get("flag_capture_only_stage2", False)):
            checks.append(
                {
                    "status": "INFO",
                    "code": "Q1_CAPTURE_ONLY_SIGNAL",
                    "message": f"{row['country']} {int(row['year'])}: capture-only sans low-price ni stress physique.",
                }
            )
        if bool(row.get("is_phase2_market", False)) and int(_safe_float(row.get("low_price_flags_count"), 0.0)) == 0 and int(_safe_float(row.get("physical_flags_count"), 0.0)) == 0:
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q1_NO_FALSE_PHASE2_WITHOUT_LOW_PRICE",
                    "message": f"{row['country']} {int(row['year'])}: Phase2 detectee sans LOW-PRICE ni PHYSICAL flags.",
                }
            )

    summary = pd.DataFrame(summary_rows)
    q1_rule_definition = _build_rule_definition(params)
    q1_rule_application_cols = [
        "country",
        "year",
        "stage2_market_score",
        "score_breakdown",
        "phase2_candidate_year",
        "low_price_flags_count",
        "physical_flags_count",
        "capture_flags_count",
        "active_flags",
        "flag_h_negative_stage2",
        "flag_h_below_5_stage2",
        "flag_p10_price_below_0",
        "flag_capture_pv_low",
        "flag_capture_wind_low",
        "flag_sr_high",
        "flag_far_low",
        "flag_ir_high",
        "flag_spread_high",
        "flag_capture_only_stage2",
        "is_stage1_criteria",
        "is_phase2_market",
        "is_phase2_physical",
        "phase_market",
        "stress_phys_state",
    ]
    q1_rule_application = panel[[c for c in q1_rule_application_cols if c in panel.columns]].copy()
    q1_before_after_bascule = _build_before_after_bascule(panel, summary)

    for col in ["p10_load_mw", "p10_must_run_mw", "p50_load_mw", "p50_must_run_mw"]:
        if col not in panel.columns:
            panel[col] = np.nan
    q1_ir_diagnostics = panel[["country", "year", "ir_p10", "p10_must_run_mw", "p10_load_mw", "p50_must_run_mw", "p50_load_mw"]].copy()
    q1_ir_diagnostics["ir_case_class"] = q1_ir_diagnostics.apply(_ir_case_class, axis=1)

    q1_scope_audit = _build_scope_audit(panel, hourly_by_country_year)
    if not q1_scope_audit.empty:
        low_cov = q1_scope_audit[q1_scope_audit["scope_reason"].astype(str) == "low_coverage_high_ir_contradiction"].copy()
        high_cov = q1_scope_audit[q1_scope_audit["scope_reason"].astype(str) == "high_coverage_possible_overestimate"].copy()
        if not low_cov.empty:
            for country, grp in low_cov.groupby("country"):
                grp = grp.copy()
                cov = pd.to_numeric(grp["must_run_scope_coverage"], errors="coerce")
                idx = cov.idxmin() if cov.notna().any() else grp.index[0]
                row = grp.loc[idx]
                cov_v = _safe_float(row.get("must_run_scope_coverage"), np.nan)
                checks.append(
                    {
                        "status": "WARN",
                        "code": "Q1_MUSTRUN_SCOPE_LOW_COVERAGE",
                        "message": f"{country}: coverage min={cov_v:.2%} avec IR eleve (contradiction).",
                    }
                )
        if not high_cov.empty:
            for country, grp in high_cov.groupby("country"):
                grp = grp.copy()
                cov = pd.to_numeric(grp["must_run_scope_coverage"], errors="coerce")
                idx = cov.idxmax() if cov.notna().any() else grp.index[0]
                row = grp.loc[idx]
                cov_v = _safe_float(row.get("must_run_scope_coverage"), np.nan)
                checks.append(
                    {
                        "status": "WARN",
                        "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
                        "message": f"{country}: coverage max={cov_v:.2%} (>60%), possible surestimation must-run.",
                    }
                )

    checks.extend(build_common_checks(panel, hourly_by_key=hourly_by_country_year))
    if not checks:
        checks.append({"status": "PASS", "code": "Q1_PASS", "message": "Q1 checks pass."})

    kpis = {
        "n_countries": int(summary["country"].nunique()) if not summary.empty else 0,
        "n_bascule_market": int(summary["bascule_year_market"].notna().sum()) if not summary.empty else 0,
        "n_bascule_physical": int(summary["bascule_year_physical"].notna().sum()) if not summary.empty else 0,
        "n_scope_rows": int(len(q1_scope_audit)),
    }

    narrative = (
        "Q1 identifie la bascule Phase 1 -> Phase 2 avec un gating strict: "
        "LOW-PRICE ou PHYSICAL obligatoire, CAPTURE-only interdit, score + persistance requis. "
        "Les sorties incluent la decomposition des flags, le score, la rationale et des solveurs required-lever."
    )

    return ModuleResult(
        module_id="Q1",
        run_id=run_id,
        selection=selection,
        assumptions_used=assumptions_subset(assumptions_df, Q1_PARAMS),
        kpis=kpis,
        tables={
            "Q1_country_summary": summary,
            "Q1_year_panel": panel,
            "Q1_rule_definition": q1_rule_definition,
            "Q1_rule_application": q1_rule_application,
            "Q1_before_after_bascule": q1_before_after_bascule,
            "Q1_scope_audit": q1_scope_audit,
            "Q1_ir_diagnostics": q1_ir_diagnostics,
        },
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
        mode=str(selection.get("mode", "HIST")).upper(),
        scenario_id=selection.get("scenario_id"),
        horizon_year=selection.get("horizon_year"),
    )
