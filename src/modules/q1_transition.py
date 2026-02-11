"""Q1 - Phase 1 to Phase 2 transition analysis."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.config_loader import load_countries
from src.constants import (
    COL_GEN_BIOMASS,
    COL_GEN_COAL,
    COL_GEN_GAS,
    COL_GEN_HYDRO_RES,
    COL_GEN_HYDRO_ROR,
    COL_GEN_LIGNITE,
    COL_GEN_NUCLEAR,
    COL_LOAD_NET,
    COL_PRICE_DA,
    COL_REGIME,
)
from src.modules.common import assumptions_subset
from src.modules.reality_checks import build_common_checks
from src.modules.result import ModuleResult

Q1_RULE_VERSION = "q1_rule_v2_2026_02_10"

Q1_PARAMS = [
    "h_negative_stage2_min",
    "h_negative_stage2_strong",
    "h_below_5_stage2_min",
    "capture_ratio_pv_stage2_max",
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
    "q1_require_non_capture_signal",
    "q1_min_non_capture_flags",
]

_SCOPE_CANDIDATE_COMPONENTS = ["nuclear", "lignite", "coal", "gas", "biomass", "hydro_ror", "hydro_res"]
_SCOPE_COMPONENT_TO_COL = {
    "nuclear": COL_GEN_NUCLEAR,
    "lignite": COL_GEN_LIGNITE,
    "coal": COL_GEN_COAL,
    "gas": COL_GEN_GAS,
    "biomass": COL_GEN_BIOMASS,
    "hydro_ror": COL_GEN_HYDRO_ROR,
    "hydro_res": COL_GEN_HYDRO_RES,
}
_SCOPE_PRIORITY_ROWS = {("NL", 2024), ("DE", 2018)}


def _safe_param(params: dict[str, float], key: str, default: float) -> float:
    v = params.get(key, default)
    try:
        return float(v)
    except Exception:
        return float(default)


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
        if np.isfinite(out):
            return out
    except Exception:
        pass
    return float(default)


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


def _market_score(row: pd.Series, p: dict[str, float]) -> int:
    score = 0
    if float(row.get("h_negative_obs", 0.0)) >= _safe_param(p, "h_negative_stage2_min", 200.0):
        score += 1
    if float(row.get("h_negative_obs", 0.0)) >= _safe_param(p, "h_negative_stage2_strong", 300.0):
        score += 2
    if float(row.get("h_below_5_obs", 0.0)) >= _safe_param(p, "h_below_5_stage2_min", 500.0):
        score += 1
    if float(row.get("capture_ratio_pv_vs_ttl", np.nan)) <= _safe_param(p, "capture_ratio_pv_vs_ttl_stage2_max", 0.8):
        score += 1
    if float(row.get("capture_ratio_pv_vs_ttl", np.nan)) <= _safe_param(p, "capture_ratio_pv_vs_ttl_crisis_max", 0.7):
        score += 2
    if float(row.get("days_spread_gt50", 0.0)) >= _safe_param(p, "days_spread_gt50_stage2_min", 150.0):
        score += 1
    return score


def _phase2_market_condition(row: pd.Series, p: dict[str, float]) -> bool:
    signal_low_price = bool(row.get("signal_low_price", False))
    signal_value = bool(row.get("signal_value", False))
    signal_physical = bool(row.get("signal_physical", False))
    signal_capture_only = bool(row.get("flag_capture_only_stage2", False))
    if signal_capture_only:
        return False
    return bool((signal_low_price and (signal_value or signal_physical)) or (signal_value and signal_physical))


def _phase2_physical_condition(row: pd.Series, p: dict[str, float]) -> bool:
    sr_energy_share_load = _safe_float(row.get("sr_energy_share_load"), np.nan)
    if not np.isfinite(sr_energy_share_load):
        sr_energy_share_load = _safe_float(row.get("sr_energy"), np.nan)
    sr_hours_share = _safe_float(row.get("sr_hours_share"), np.nan)
    if not np.isfinite(sr_hours_share):
        sr_hours_share = _safe_float(row.get("sr_hours"), np.nan)
    ir_p10 = _safe_float(row.get("ir_p10"), np.nan)
    far_energy = _safe_float(row.get("far_energy"), np.nan)
    signal_surplus = (
        (np.isfinite(sr_energy_share_load) and sr_energy_share_load >= _safe_param(p, "sr_energy_material_min", 0.01))
        or (np.isfinite(sr_hours_share) and sr_hours_share >= _safe_param(p, "sr_hours_material_min", 0.05))
    )
    signal_rigidity = (
        (np.isfinite(ir_p10) and ir_p10 >= _safe_param(p, "ir_p10_high_min", 0.70))
        or (np.isfinite(far_energy) and far_energy <= _safe_param(p, "far_energy_tension_max", 0.95))
    )
    return bool(signal_surplus and signal_rigidity)


def _first_year_two_of_three(group: pd.DataFrame, col: str) -> float:
    if group.empty or col not in group.columns:
        return float("nan")
    years = pd.to_numeric(group["year"], errors="coerce")
    flags = group[col].fillna(False).astype(bool).to_numpy()
    for i in range(len(group)):
        j0 = max(0, i - 2)
        if flags[i] and int(flags[j0 : i + 1].sum()) >= 2:
            y = _safe_float(years.iloc[i], np.nan)
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
                "score_min_phase2_market": 2.0,
                "h_negative_stage2_min": _safe_param(params, "h_negative_stage2_min", 200.0),
                "h_negative_stage2_strong": _safe_param(params, "h_negative_stage2_strong", 300.0),
                "h_below_5_stage2_min": _safe_param(params, "h_below_5_stage2_min", 500.0),
                "capture_ratio_pv_stage2_max": _safe_param(params, "capture_ratio_pv_stage2_max", 0.90),
                "capture_ratio_pv_vs_ttl_stage2_max": _safe_param(params, "capture_ratio_pv_vs_ttl_stage2_max", 0.8),
                "capture_ratio_pv_vs_ttl_crisis_max": _safe_param(params, "capture_ratio_pv_vs_ttl_crisis_max", 0.7),
                "days_spread_gt50_stage2_min": _safe_param(params, "days_spread_gt50_stage2_min", 150.0),
                "q1_require_non_capture_signal": _safe_param(params, "q1_require_non_capture_signal", 1.0),
                "q1_min_non_capture_flags": _safe_param(params, "q1_min_non_capture_flags", 1.0),
                "sr_energy_material_min": _safe_param(params, "sr_energy_material_min", 0.01),
                "sr_hours_material_min": _safe_param(params, "sr_hours_material_min", 0.05),
                "far_energy_tension_max": _safe_param(params, "far_energy_tension_max", 0.95),
                "ir_p10_high_min": _safe_param(params, "ir_p10_high_min", 0.70),
                "rule_logic": (
                    "is_phase2_market=((signal_low_price AND (signal_value OR signal_physical)) "
                    "OR (signal_value AND signal_physical)); capture_only interdit."
                ),
            }
        ]
    )


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


def _scope_components_for_country(country: str) -> list[str]:
    try:
        countries_cfg = load_countries().get("countries", {})
    except Exception:
        return []
    cfg = countries_cfg.get(str(country), {})
    return [str(x) for x in cfg.get("must_run", {}).get("observed_components", [])]


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
        configured_components = _scope_components_for_country(country)

        coverage_ratio = np.nan
        neg_in_ab_share = np.nan
        neg_in_cd_share = np.nan
        scope_status = "NON_TESTABLE"
        scope_reason = "hourly_missing"
        candidate_components: list[str] = []

        if hourly_by_country_year is not None and key in hourly_by_country_year:
            hourly = hourly_by_country_year[key]
            if hourly is not None and not hourly.empty:
                load_p10 = _quantile(hourly.get(COL_LOAD_NET, pd.Series(dtype=float)), 0.10)
                comp_weights: dict[str, float] = {}
                for comp in _SCOPE_CANDIDATE_COMPONENTS:
                    col = _SCOPE_COMPONENT_TO_COL[comp]
                    if col not in hourly.columns:
                        continue
                    p10_comp = _quantile(hourly[col], 0.10)
                    ratio = _safe_ratio(p10_comp, load_p10)
                    if np.isfinite(ratio) and ratio >= 0.05:
                        comp_weights[comp] = ratio
                candidate_components = sorted(comp_weights.keys())

                total_weight = float(sum(comp_weights.values()))
                covered_weight = float(sum(comp_weights[c] for c in candidate_components if c in configured_components))
                coverage_ratio = _safe_ratio(covered_weight, total_weight)

                price = pd.to_numeric(hourly.get(COL_PRICE_DA, pd.Series(dtype=float)), errors="coerce")
                regime = hourly.get(COL_REGIME, pd.Series(index=hourly.index, dtype=object)).astype(str)
                neg_mask = price < 0
                neg_total = int(neg_mask.sum())
                if neg_total > 0:
                    neg_in_ab_share = float(((neg_mask) & regime.isin(["A", "B"])).sum()) / float(neg_total)
                    neg_in_cd_share = float(((neg_mask) & regime.isin(["C", "D"])).sum()) / float(neg_total)

                if not np.isfinite(coverage_ratio):
                    scope_status = "NON_TESTABLE"
                    scope_reason = "no_inflexible_candidates"
                elif coverage_ratio < 0.70:
                    scope_status = "REVIEW"
                    scope_reason = "scope_coverage_below_0.70"
                else:
                    scope_status = "OK"
                    scope_reason = "scope_coverage_sufficient"

        rows.append(
            {
                "country": country,
                "year": year,
                "configured_components": ",".join(configured_components),
                "candidate_components": ",".join(candidate_components),
                "scope_coverage_ratio": coverage_ratio,
                "h_negative_obs": _safe_float(prow.get("h_negative_obs"), np.nan),
                "neg_in_ab_share": neg_in_ab_share,
                "neg_in_cd_share": neg_in_cd_share,
                "sr_energy": _safe_float(prow.get("sr_energy"), np.nan),
                "far_energy": _safe_float(prow.get("far_energy"), np.nan),
                "scope_status": scope_status,
                "scope_reason": scope_reason,
                "priority_case": bool((country, year) in _SCOPE_PRIORITY_ROWS),
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

    if "sr_energy_share_load" not in panel.columns:
        panel["sr_energy_share_load"] = panel.get("sr_energy", np.nan)
    if "sr_hours_share" not in panel.columns:
        panel["sr_hours_share"] = panel.get("sr_hours", np.nan)
    if "capture_ratio_pv" not in panel.columns:
        panel["capture_ratio_pv"] = panel.get("capture_ratio_pv_vs_baseload", np.nan)

    panel["stage2_market_score"] = panel.apply(lambda row: _market_score(row, params), axis=1)
    panel["flag_h_negative_stage2"] = panel["h_negative_obs"] >= _safe_param(params, "h_negative_stage2_min", 200.0)
    panel["flag_h_below_5_stage2"] = panel["h_below_5_obs"] >= _safe_param(params, "h_below_5_stage2_min", 500.0)
    panel["flag_capture_stage2"] = (
        (panel["capture_ratio_pv"] <= _safe_param(params, "capture_ratio_pv_stage2_max", 0.90))
        | (panel["capture_ratio_pv_vs_ttl"] <= _safe_param(params, "capture_ratio_pv_vs_ttl_stage2_max", 0.8))
    )
    panel["flag_days_spread_stage2"] = panel["days_spread_gt50"] >= _safe_param(params, "days_spread_gt50_stage2_min", 150.0)
    panel["signal_low_price"] = panel["flag_h_negative_stage2"] | panel["flag_h_below_5_stage2"]
    panel["signal_value"] = panel["flag_capture_stage2"]
    panel["signal_physical"] = (
        (panel["sr_energy_share_load"] >= _safe_param(params, "sr_energy_material_min", 0.01))
        | (panel["sr_hours_share"] >= _safe_param(params, "sr_hours_material_min", 0.05))
        | (panel["ir_p10"] >= _safe_param(params, "ir_p10_high_min", 0.70))
    )
    panel["flag_non_capture_stage2"] = panel["signal_low_price"].astype(int) + panel["signal_physical"].astype(int)
    panel["flag_capture_only_stage2"] = panel["signal_value"] & (~panel["signal_low_price"]) & (~panel["signal_physical"])

    panel["is_stage1_criteria"] = panel.apply(lambda row: _is_stage1(row, params), axis=1)
    panel["is_phase2_market"] = panel.apply(lambda row: _phase2_market_condition(row, params), axis=1)
    panel["is_phase2_physical"] = panel.apply(lambda row: _phase2_physical_condition(row, params), axis=1)
    panel["phase_market"] = np.select(
        [
            panel["is_phase2_market"],
            panel["is_stage1_criteria"],
        ],
        [
            "phase2",
            "phase1",
        ],
        default="uncertain",
    )

    panel["stress_phys_state"] = np.select(
        [
            panel["sr_energy_share_load"] < _safe_param(params, "sr_energy_material_min", 0.01),
            (panel["sr_energy_share_load"] >= _safe_param(params, "sr_energy_material_min", 0.01))
            & (panel["far_energy"] > _safe_param(params, "far_energy_tension_max", 0.95)),
            (panel["sr_energy_share_load"] >= _safe_param(params, "sr_energy_material_min", 0.01))
            & (panel["far_energy"] <= _safe_param(params, "far_energy_tension_max", 0.95)),
        ],
        [
            "pas_de_surplus_structurel",
            "surplus_present_mais_absorbe",
            "surplus_non_absorbe",
        ],
        default="unknown",
    )

    panel["quality_ok"] = panel["quality_flag"].fillna("WARN") != "FAIL"
    panel["flag_sr_stress"] = panel["sr_energy_share_load"] >= _safe_param(params, "sr_energy_material_min", 0.01)
    panel["flag_far_tension"] = panel["far_energy"] <= _safe_param(params, "far_energy_tension_max", 0.95)
    panel["flag_ir_high"] = panel["ir_p10"] >= _safe_param(params, "ir_p10_high_min", 0.70)

    checks: list[dict[str, str]] = []
    warnings: list[str] = []

    summary_rows: list[dict[str, Any]] = []
    for country, group in panel.groupby("country"):
        group = group.sort_values("year")
        market_candidates = group[
            (group["phase_market"] == "phase2")
            & (group["quality_ok"])
            & (group["capture_ratio_pv_vs_ttl"].notna())
        ]
        market_year = int(market_candidates["year"].min()) if not market_candidates.empty else np.nan
        physical_year = _first_year_two_of_three(group[group["quality_ok"]], "is_phase2_physical")

        at = group[group["year"] == market_year].iloc[0] if np.isfinite(market_year) else group.iloc[-1]
        drivers: list[str] = []
        if at.get("flag_sr_stress", False):
            drivers.append("SR")
        if at.get("flag_far_tension", False):
            drivers.append("FAR")
        if at.get("flag_ir_high", False):
            drivers.append("IR")
        if at.get("flag_h_negative_stage2", False):
            drivers.append("h_negative")
        if at.get("flag_capture_stage2", False):
            drivers.append("capture_ratio")
        if at.get("signal_low_price", False):
            drivers.append("low_price")

        confidence = 1.0 if np.isfinite(market_year) else 0.0
        if np.isfinite(market_year):
            y0 = int(market_year)
            around = group[(group["year"] >= y0 - 1) & (group["year"] <= y0 + 1)].copy()
            if not around.empty:
                low_coherence = pd.to_numeric(around.get("regime_coherence"), errors="coerce") < 0.20
                if bool(low_coherence.fillna(False).any()):
                    confidence -= 0.25
                    warnings.append(f"{country}: regime_coherence < 0.20 autour de la bascule.")
                if bool(around.get("flag_capture_only_stage2", pd.Series(False)).fillna(False).any()):
                    confidence -= 0.20
                    warnings.append(f"{country}: capture-only detecte autour de la bascule.")
                bad_quality = around.get("quality_flag", pd.Series(dtype=object)).astype(str).str.upper() != "OK"
                if bool(bad_quality.fillna(False).any()):
                    confidence -= 0.15
                    warnings.append(f"{country}: quality_flag != OK autour de la bascule.")
            if not _is_market_persistent(group, market_year):
                confidence -= 0.20
                warnings.append(f"{country}: bascule marche non persistante (fenetre +2 ans).")
        confidence = max(0.0, min(1.0, confidence))

        if np.isfinite(market_year) and pd.isna(at.get("capture_ratio_pv_vs_ttl", np.nan)):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q1_CAPTURE_NAN_BASCULE",
                    "message": f"{country}: bascule detectee avec capture_ratio_pv_vs_ttl NaN.",
                }
            )

        summary_rows.append(
            {
                "country": country,
                "bascule_year_market": market_year,
                "bascule_year_physical": physical_year,
                "bascule_confidence": confidence,
                "drivers_at_bascule": ", ".join(drivers[:3]),
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
        if row.get("flag_capture_only_stage2", False):
            checks.append(
                {
                    "status": "WARN",
                    "code": "Q1_CAPTURE_ONLY_SIGNAL",
                    "message": f"{row['country']} {int(row['year'])}: signal stage2 majoritairement capture-only.",
                }
            )
        if (
            bool(row.get("is_phase2_market", False))
            and float(row.get("h_negative_obs", np.nan)) == 0.0
            and float(row.get("h_below_5_obs", np.nan)) < _safe_param(params, "h_below_5_stage2_min", 500.0)
            and float(row.get("sr_energy_share_load", np.nan)) < _safe_param(params, "sr_energy_material_min", 0.01)
        ):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q1_NO_FALSE_PHASE2_WITHOUT_LOW_PRICE",
                    "message": (
                        f"{row['country']} {int(row['year'])}: Phase2 marche detectee sans prix bas ni stress physique."
                    ),
                }
            )
        if row["phase_market"] == "phase2" and float(row.get("h_negative_obs", 0.0)) < 100 and float(row.get("capture_ratio_pv_vs_ttl", 1.0)) > 0.9:
            checks.append(
                {
                    "status": "WARN",
                    "code": "Q1_INCOHERENT_BASCULE",
                    "message": f"{row['country']} {int(row['year'])}: bascule incoherente avec symptomes marche.",
                }
            )

    summary = pd.DataFrame(summary_rows)

    for col in ["p10_load_mw", "p10_must_run_mw", "p50_load_mw", "p50_must_run_mw"]:
        if col not in panel.columns:
            panel[col] = np.nan

    q1_rule_definition = _build_rule_definition(params)
    q1_rule_application_cols = [
        "country",
        "year",
        "stage2_market_score",
        "flag_h_negative_stage2",
        "flag_h_below_5_stage2",
        "flag_capture_stage2",
        "flag_days_spread_stage2",
        "flag_non_capture_stage2",
        "flag_capture_only_stage2",
        "signal_low_price",
        "signal_value",
        "signal_physical",
        "is_stage1_criteria",
        "is_phase2_market",
        "is_phase2_physical",
        "phase_market",
        "stress_phys_state",
        "quality_ok",
        "flag_sr_stress",
        "flag_far_tension",
        "flag_ir_high",
    ]
    q1_rule_application = panel[[c for c in q1_rule_application_cols if c in panel.columns]].copy()
    q1_before_after_bascule = _build_before_after_bascule(panel, summary)

    q1_ir_diagnostics = panel[
        [
            "country",
            "year",
            "ir_p10",
            "p10_must_run_mw",
            "p10_load_mw",
            "p50_must_run_mw",
            "p50_load_mw",
        ]
    ].copy()
    q1_ir_diagnostics["ir_case_class"] = q1_ir_diagnostics.apply(_ir_case_class, axis=1)

    q1_scope_audit = _build_scope_audit(panel, hourly_by_country_year)
    if not q1_scope_audit.empty:
        for _, row in q1_scope_audit.iterrows():
            coverage = _safe_float(row.get("scope_coverage_ratio"), np.nan)
            h_negative_obs = _safe_float(row.get("h_negative_obs"), np.nan)
            sr_energy = _safe_float(row.get("sr_energy"), np.nan)
            neg_in_ab = _safe_float(row.get("neg_in_ab_share"), np.nan)
            if np.isfinite(coverage) and coverage < 0.70:
                checks.append(
                    {
                        "status": "WARN",
                        "code": "Q1_MR_SCOPE_REVIEW",
                        "message": (
                            f"{row['country']} {int(row['year'])}: must-run scope coverage faible "
                            f"({coverage:.2f} < 0.70)."
                        ),
                    }
                )
            if (
                np.isfinite(h_negative_obs)
                and h_negative_obs >= 100.0
                and np.isfinite(sr_energy)
                and sr_energy <= 0.003
                and np.isfinite(neg_in_ab)
                and neg_in_ab < 0.50
            ):
                checks.append(
                    {
                        "status": "WARN",
                        "code": "Q1_NRL_SCOPE_DIVERGENCE",
                        "message": (
                            f"{row['country']} {int(row['year'])}: divergence NRL/scope "
                            f"(h_negative={h_negative_obs:.0f}, sr_energy={sr_energy:.4f}, neg_in_ab_share={neg_in_ab:.2f})."
                        ),
                    }
                )

        priority_rows = q1_scope_audit[
            q1_scope_audit.apply(lambda r: (str(r["country"]), int(r["year"])) in _SCOPE_PRIORITY_ROWS, axis=1)
        ]
        if not priority_rows.empty:
            labels = [f"{str(r['country'])}-{int(r['year'])}" for _, r in priority_rows.iterrows()]
            warnings.append(f"Q1 priority scope rows: {', '.join(labels)}.")

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
        "Q1 identifie la bascule Phase 1 -> Phase 2 via deux diagnostics independants: "
        "symptomes de marche (score) et stress physique (SR/FAR/IR). "
        "Les tables Q1_rule_definition, Q1_rule_application, Q1_before_after_bascule, "
        "Q1_scope_audit et Q1_ir_diagnostics explicitent la regle, son application et les zones de fragilite."
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
