"""Q1 - Phase 1 to Phase 2 transition analysis."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import numpy as np
import pandas as pd

from src.constants import COL_GEN_TOTAL, COL_LOAD_NET, COL_LOW_RESIDUAL_HOUR, COL_MUST_RUN_MODE, COL_PRICE_DA, COL_REGIME
from src.config_loader import load_thresholds
from src.core.definitions import compute_scope_coverage_lowload
from src.modules.common import assumptions_subset
from src.modules.reality_checks import build_common_checks
from src.modules.result import ModuleResult

Q1_RULE_VERSION = "q1_rule_v5_2026_02_12"
DEFAULT_CRISIS_YEARS = {2022}
Q1_UNEXPLAINED_NEGATIVE_PRICES_MAX = 0.35
Q1_REASON_CODE_REQUIRED_METRICS = {
    "h_negative_obs",
    "h_below_5_obs",
    "low_price_hours_share",
    "capture_ratio_pv",
    "capture_ratio_wind",
    "sr_energy",
    "sr_hours_share",
    "far_observed",
    "ir_p10",
}
DATA_QUALITY_BLOCKING_FLAGS = {
    "FAIL",
    "DATA_GAP",
    "OUT_OF_RANGE",
    "OUT_OF_BOUNDS",
    "INVALID_BOUNDS",
    "INVALID_UNIT",
    "MISSING",
    "ERROR",
}

Q1_PARAMS = [
    "h_negative_stage2_min",
    "h_below_5_stage2_min",
    "low_price_hours_share_stage2_min",
    "capture_ratio_pv_stage2_max",
    "capture_ratio_wind_stage2_max",
    "sr_energy_stage2_min",
    "sr_hours_stage2_min",
    "low_residual_hours_stage2_min",
    "far_stage2_min",
    "ir_p10_stage2_min",
    "days_spread_gt50_stage2_min",
    "avg_daily_spread_crisis_min",
    "stage1_capture_ratio_pv_min",
    "stage1_capture_ratio_wind_min",
    "stage1_sr_energy_max",
    "stage1_sr_hours_max",
    "stage1_far_min",
    "stage1_ir_p10_max",
    "stage1_h_negative_max",
    "stage1_h_below_5_max",
    "regime_coherence_min_for_causality",
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
    s = pd.to_numeric(series, errors="coerce")
    if isinstance(s, pd.Series):
        s = s.dropna()
    else:
        s = pd.Series([s], dtype=float).dropna()
    if s.empty:
        return float("nan")
    return float(s.quantile(q))


def _parse_year_set(value: Any) -> set[int]:
    if value is None:
        return set()
    if isinstance(value, (list, tuple, set)):
        out: set[int] = set()
        for v in value:
            fv = _safe_float(v, np.nan)
            if np.isfinite(fv):
                out.add(int(fv))
        return out
    txt = str(value).strip()
    if not txt:
        return set()
    out: set[int] = set()
    for tok in txt.split(","):
        fv = _safe_float(tok.strip(), np.nan)
        if np.isfinite(fv):
            out.add(int(fv))
    return out


@lru_cache(maxsize=1)
def _load_crisis_years_from_config() -> tuple[set[int], dict[str, set[int]]]:
    years = set(DEFAULT_CRISIS_YEARS)
    per_country: dict[str, set[int]] = {}
    try:
        cfg = load_thresholds()
    except Exception:
        return years, per_country

    analysis = cfg.get("analysis", {}) if isinstance(cfg, dict) else {}
    cycle = analysis.get("cycle", {}) if isinstance(analysis, dict) else {}

    years_cfg = _parse_year_set(cycle.get("crisis_years"))
    if years_cfg:
        years = years_cfg

    overrides = cycle.get("crisis_years_by_country", {})
    if isinstance(overrides, dict):
        for country, v in overrides.items():
            parsed = _parse_year_set(v)
            if parsed:
                per_country[str(country)] = parsed
    return years, per_country


def _resolve_crisis_years(selection: dict[str, Any]) -> tuple[set[int], dict[str, set[int]]]:
    global_years, per_country = _load_crisis_years_from_config()
    out_global = set(global_years)
    out_country = {str(k): set(v) for k, v in per_country.items()}

    sel_years = _parse_year_set(selection.get("crisis_years"))
    if sel_years:
        out_global = sel_years

    sel_per_country = selection.get("crisis_years_by_country", {})
    if isinstance(sel_per_country, dict):
        for country, v in sel_per_country.items():
            parsed = _parse_year_set(v)
            if parsed:
                out_country[str(country)] = parsed

    if not out_global:
        out_global = set(DEFAULT_CRISIS_YEARS)
    return out_global, out_country


def _stage1_score_components(row: pd.Series, p: dict[str, float]) -> tuple[int, bool, bool, bool, bool, bool]:
    h_neg_ok = bool(
        _safe_float(row.get("h_negative_obs"), np.nan)
        <= _safe_param(p, "stage1_h_negative_max", _safe_param(p, "h_negative_stage2_min", 200.0))
    )
    h_below_ok = bool(
        _safe_float(row.get("h_below_5_obs"), np.nan)
        <= _safe_param(p, "stage1_h_below_5_max", _safe_param(p, "h_below_5_stage2_min", 500.0))
    )
    pv_ratio = _safe_float(row.get("capture_ratio_pv"), np.nan)
    wind_ratio = _safe_float(row.get("capture_ratio_wind"), np.nan)
    capture_ok = False
    if np.isfinite(pv_ratio):
        capture_ok = bool(pv_ratio >= _safe_param(p, "stage1_capture_ratio_pv_min", 0.85))
    elif np.isfinite(wind_ratio):
        capture_ok = bool(wind_ratio >= _safe_param(p, "stage1_capture_ratio_wind_min", 0.90))
    sr_energy_val = _safe_float(row.get("sr_energy_share_gen", row.get("sr_energy", np.nan)), np.nan)
    sr_ok = bool(sr_energy_val <= _safe_param(p, "stage1_sr_energy_max", _safe_param(p, "sr_energy_stage2_min", 0.01)))
    stage1_score = int(h_neg_ok) + int(h_below_ok) + int(capture_ok) + int(sr_ok)
    return stage1_score, h_neg_ok, h_below_ok, capture_ok, sr_ok, bool(stage1_score >= 3)


def _is_stage1(row: pd.Series, p: dict[str, float]) -> bool:
    stage1_score, _, _, _, _, score_ok = _stage1_score_components(row, p)
    capture_degradation = bool(
        row.get(
            "CAPTURE_DEGRADATION_FLAG",
            (_safe_float(row.get("capture_ratio_pv"), np.nan) <= _safe_param(p, "capture_ratio_pv_stage2_max", 0.80))
            or (_safe_float(row.get("capture_ratio_wind"), np.nan) <= _safe_param(p, "capture_ratio_wind_stage2_max", 0.90)),
        )
    )
    return bool(score_ok and stage1_score >= 3 and (not capture_degradation))


def _build_rule_definition(params: dict[str, float], crisis_years: set[int]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "q1_rule_version": Q1_RULE_VERSION,
                "h_negative_stage2_min": _safe_param(params, "h_negative_stage2_min", 200.0),
                "h_below_5_stage2_min": _safe_param(params, "h_below_5_stage2_min", 500.0),
                "low_price_hours_share_stage2_min": _safe_param(
                    params,
                    "low_price_hours_share_stage2_min",
                    _safe_param(params, "h_below_5_stage2_min", 500.0) / 8760.0,
                ),
                "capture_ratio_pv_stage2_max": _safe_param(params, "capture_ratio_pv_stage2_max", 0.80),
                "capture_ratio_wind_stage2_max": _safe_param(params, "capture_ratio_wind_stage2_max", 0.90),
                "sr_energy_stage2_min": _safe_param(params, "sr_energy_stage2_min", _safe_param(params, "sr_energy_material_min", 0.01)),
                "sr_hours_stage2_min": _safe_param(params, "sr_hours_stage2_min", 0.10),
                "low_residual_hours_stage2_min": _safe_param(
                    params,
                    "low_residual_hours_stage2_min",
                    _safe_param(params, "sr_hours_stage2_min", 0.10),
                ),
                "far_stage2_min": _safe_param(params, "far_stage2_min", 0.95),
                "ir_p10_stage2_min": _safe_param(params, "ir_p10_stage2_min", 1.5),
                "days_spread_gt50_stage2_min": _safe_param(params, "days_spread_gt50_stage2_min", 150.0),
                "avg_daily_spread_crisis_min": _safe_param(params, "avg_daily_spread_crisis_min", 50.0),
                "stage1_capture_ratio_pv_min": _safe_param(params, "stage1_capture_ratio_pv_min", 0.85),
                "stage1_capture_ratio_wind_min": _safe_param(params, "stage1_capture_ratio_wind_min", 0.90),
                "stage1_sr_energy_max": _safe_param(
                    params,
                    "stage1_sr_energy_max",
                    _safe_param(params, "sr_energy_stage2_min", _safe_param(params, "sr_energy_material_min", 0.01)),
                ),
                "stage1_sr_hours_max": _safe_param(params, "stage1_sr_hours_max", 0.05),
                "stage1_far_min": _safe_param(params, "stage1_far_min", 0.95),
                "stage1_ir_p10_max": _safe_param(params, "stage1_ir_p10_max", 1.5),
                "persistence_window_years": _safe_param(params, "q1_persistence_window_years", 2.0),
                "crisis_years_explicit": ",".join([str(int(y)) for y in sorted(crisis_years)]),
                "rule_logic": (
                    "is_phase2_market := family_count(LOW_PRICE,VALUE,PHYSICAL) >= 2; "
                    "is_phase2_physical := PHYSICAL_STRESS_FLAG. "
                    "LOW_PRICE_FLAG uses h_negative OR h_below_5 OR low_price_hours_share. "
                    "PHYSICAL_STRESS_FLAG uses sr_energy OR sr_hours OR ir_p10. "
                    "is_stage1 := stage1_score>=3 AND NOT CAPTURE_DEGRADATION_FLAG (hors crise/qualite OK)."
                ),
            }
        ]
    )


def _flag_list(row: pd.Series) -> str:
    names: list[str] = []
    for col in [
        "low_price_family",
        "value_family",
        "physical_family",
        "flag_h_negative_stage2",
        "flag_h_below_5_stage2",
        "flag_low_price_share_high",
        "flag_capture_pv_low",
        "flag_capture_wind_low",
        "flag_sr_energy_high",
        "flag_sr_hours_high",
        "flag_low_residual_high",
        "flag_far_low",
        "flag_ir_high",
        "flag_spread_high",
    ]:
        if bool(row.get(col, False)):
            names.append(col)
    return ",".join(names)


def _apply_phase2_logic(
    panel: pd.DataFrame,
    p: dict[str, float],
    crisis_years_global: set[int],
    crisis_years_by_country: dict[str, set[int]] | None = None,
    quality_overrides: dict[tuple[str, int], str] | None = None,
    market_physical_gap_ratios: dict[tuple[str, int], float] | None = None,
) -> pd.DataFrame:
    out = panel.copy()
    crisis_years_by_country = crisis_years_by_country or {}
    if "capture_ratio_pv" not in out.columns:
        out["capture_ratio_pv"] = out.get("capture_ratio_pv_vs_baseload", out.get("capture_ratio_pv_vs_ttl", np.nan))
    if "capture_ratio_wind" not in out.columns:
        out["capture_ratio_wind"] = out.get("capture_ratio_wind_vs_baseload", out.get("capture_ratio_wind_vs_ttl", np.nan))
    if "sr_energy_share_load" not in out.columns:
        out["sr_energy_share_load"] = out.get("sr_energy", np.nan)
    if "sr_hours_share" not in out.columns:
        out["sr_hours_share"] = out.get("sr_hours", np.nan)
    if "far_observed" not in out.columns:
        out["far_observed"] = out.get("far_energy", np.nan)
    if "h_negative_obs" not in out.columns:
        out["h_negative_obs"] = out.get("h_negative", np.nan)
    if "h_below_5_obs" not in out.columns:
        out["h_below_5_obs"] = out.get("h_below_5", np.nan)
    if "days_spread_gt50" not in out.columns:
        out["days_spread_gt50"] = out.get("days_spread_50_obs", np.nan)
    if "avg_daily_spread_obs" not in out.columns:
        out["avg_daily_spread_obs"] = np.nan
    if "low_residual_hours_share" not in out.columns:
        out["low_residual_hours_share"] = np.nan
    if "share_neg_price_hours_in_AB" not in out.columns:
        out["share_neg_price_hours_in_AB"] = np.nan
    if "share_neg_price_hours_in_low_residual" not in out.columns:
        out["share_neg_price_hours_in_low_residual"] = np.nan
    if "share_neg_price_hours_in_AB_OR_LOW_RESIDUAL" not in out.columns:
        out["share_neg_price_hours_in_AB_OR_LOW_RESIDUAL"] = np.nan
    out["share_neg_hours_unexplained"] = (
        1.0
        - pd.to_numeric(out.get("share_neg_price_hours_in_AB_OR_LOW_RESIDUAL"), errors="coerce")
    ).clip(lower=0.0, upper=1.0)
    out["flag_unexplained_negative_prices"] = pd.to_numeric(
        out.get("share_neg_hours_unexplained"),
        errors="coerce",
    ) > Q1_UNEXPLAINED_NEGATIVE_PRICES_MAX
    for col, default in {
        "psh_pumping_twh": 0.0,
        "psh_pumping_coverage_share": np.nan,
        "psh_pumping_data_status": "missing",
        "flex_sink_exports_twh": 0.0,
        "flex_sink_psh_twh": 0.0,
        "flex_sink_total_twh": 0.0,
        "surplus_energy_twh": out.get("surplus_twh", np.nan),
        "absorbed_surplus_twh": np.nan,
        "unabsorbed_surplus_twh": out.get("surplus_unabsorbed_twh", np.nan),
    }.items():
        if col not in out.columns:
            out[col] = default

    h_neg = pd.to_numeric(out.get("h_negative_obs"), errors="coerce")
    h_low = pd.to_numeric(out.get("h_below_5_obs"), errors="coerce")
    low_price_raw = out.get("low_price_hours_share", pd.Series(np.nan, index=out.index))
    if isinstance(low_price_raw, pd.Series):
        low_price_share = pd.to_numeric(low_price_raw, errors="coerce")
    else:
        low_price_share = pd.Series(low_price_raw, index=out.index, dtype=float)
    if low_price_share.notna().sum() == 0:
        hours_raw = out.get("n_hours_expected", pd.Series(np.nan, index=out.index))
        if isinstance(hours_raw, pd.Series):
            hours = pd.to_numeric(hours_raw, errors="coerce")
        else:
            hours = pd.Series(hours_raw, index=out.index, dtype=float)
        hours = hours.replace(0.0, np.nan)
        if hours.notna().sum() == 0:
            hours = pd.Series(8760.0, index=out.index, dtype=float)
        low_price_share = h_low / hours
    out["low_price_hours_share"] = low_price_share
    cr_pv = pd.to_numeric(out.get("capture_ratio_pv"), errors="coerce")
    cr_wind = pd.to_numeric(out.get("capture_ratio_wind"), errors="coerce")
    sr_energy = pd.to_numeric(out.get("sr_energy_share_gen", out.get("sr_energy")), errors="coerce")
    sr_h = pd.to_numeric(out.get("sr_hours_share"), errors="coerce")
    far = pd.to_numeric(out.get("far_observed"), errors="coerce")
    ir = pd.to_numeric(out.get("ir_p10"), errors="coerce")
    low_residual_share = pd.to_numeric(out.get("low_residual_hours_share"), errors="coerce")

    out["flag_h_negative_stage2"] = h_neg >= _safe_param(p, "h_negative_stage2_min", 200.0)
    out["flag_h_below_5_stage2"] = h_low >= _safe_param(p, "h_below_5_stage2_min", 500.0)
    out["flag_low_price_share_high"] = low_price_share >= _safe_param(
        p,
        "low_price_hours_share_stage2_min",
        _safe_param(p, "h_below_5_stage2_min", 500.0) / 8760.0,
    )
    out["flag_capture_pv_low"] = cr_pv <= _safe_param(p, "capture_ratio_pv_stage2_max", 0.80)
    out["flag_capture_wind_low"] = cr_wind <= _safe_param(p, "capture_ratio_wind_stage2_max", 0.90)
    out["flag_sr_energy_high"] = sr_energy >= _safe_param(
        p,
        "sr_energy_stage2_min",
        _safe_param(p, "sr_energy_material_min", 0.01),
    )
    out["flag_sr_hours_high"] = sr_h >= _safe_param(p, "sr_hours_stage2_min", 0.10)
    out["flag_sr_high"] = out["flag_sr_hours_high"]
    out["flag_low_residual_high"] = low_residual_share >= _safe_param(
        p,
        "low_residual_hours_stage2_min",
        _safe_param(p, "sr_hours_stage2_min", 0.10),
    )
    out["flag_far_low"] = far < _safe_param(p, "far_stage2_min", 0.95)
    out["flag_ir_high"] = ir >= _safe_param(p, "ir_p10_stage2_min", 1.5)
    out["flag_spread_high"] = pd.to_numeric(out.get("days_spread_gt50"), errors="coerce") >= _safe_param(
        p,
        "days_spread_gt50_stage2_min",
        150.0,
    )
    crisis = pd.Series(False, index=out.index, dtype=bool)
    for i, row in out[["country", "year"]].iterrows():
        country = str(row.get("country", ""))
        year = _safe_float(row.get("year"), np.nan)
        if not np.isfinite(year):
            continue
        y = int(year)
        years_set = crisis_years_by_country.get(country, crisis_years_global)
        crisis.at[i] = y in years_set
    out["crisis_year"] = crisis

    out["LOW_PRICE_FLAG"] = (
        out["flag_h_negative_stage2"]
        | out["flag_h_below_5_stage2"]
        | out["flag_low_price_share_high"]
    )
    out["CAPTURE_DEGRADATION_FLAG"] = out["flag_capture_pv_low"] | out["flag_capture_wind_low"]
    out["PHYSICAL_STRESS_FLAG"] = out["flag_sr_energy_high"] | out["flag_sr_hours_high"] | out["flag_ir_high"]

    out["low_price_family"] = out["LOW_PRICE_FLAG"]
    out["value_family_pv"] = out["flag_capture_pv_low"]
    out["value_family_wind"] = out["flag_capture_wind_low"]
    out["value_family"] = out["CAPTURE_DEGRADATION_FLAG"]
    out["physical_family"] = out["PHYSICAL_STRESS_FLAG"]

    out["low_price_flags_count"] = (
        out[["flag_h_negative_stage2", "flag_h_below_5_stage2", "flag_low_price_share_high"]].fillna(False).astype(int).sum(axis=1)
    )
    out["capture_flags_count"] = out[["flag_capture_pv_low", "flag_capture_wind_low"]].fillna(False).astype(int).sum(axis=1)
    out["physical_flags_count"] = out[["flag_sr_energy_high", "flag_sr_hours_high", "flag_ir_high"]].fillna(False).astype(int).sum(axis=1)

    out["family_count"] = out[["low_price_family", "value_family", "physical_family"]].fillna(False).astype(int).sum(axis=1)
    out["family_count_pv"] = out[["low_price_family", "physical_family", "value_family_pv"]].fillna(False).astype(int).sum(axis=1)
    out["family_count_wind"] = out[["low_price_family", "physical_family", "value_family_wind"]].fillna(False).astype(int).sum(axis=1)
    out["stage2_points_low_price"] = out["LOW_PRICE_FLAG"].fillna(False).astype(int)
    out["stage2_points_capture"] = out["CAPTURE_DEGRADATION_FLAG"].fillna(False).astype(int)
    out["stage2_points_physical"] = out["PHYSICAL_STRESS_FLAG"].fillna(False).astype(int)
    out["stage2_points_vol"] = out["crisis_year"].fillna(False).astype(int)
    out["stage2_market_score"] = (
        out["stage2_points_low_price"] + out["stage2_points_capture"] + out["stage2_points_physical"] + out["stage2_points_vol"]
    )
    out["score_breakdown"] = out.apply(
        lambda r: f"low={int(r['stage2_points_low_price'])};value={int(r['stage2_points_capture'])};physical={int(r['stage2_points_physical'])};crisis={int(r['stage2_points_vol'])}",
        axis=1,
    )

    # Data-quality gate (coverage/units/bounds only).
    out["quality_flag"] = out.get("quality_flag", pd.Series("OK", index=out.index)).astype(str).str.upper()
    if quality_overrides:
        for i, row in out[["country", "year"]].iterrows():
            y = _safe_float(row.get("year"), np.nan)
            if not np.isfinite(y):
                continue
            key = (str(row["country"]), int(y))
            override = quality_overrides.get(key)
            if override:
                out.at[i, "quality_flag"] = str(override).upper()
    out["quality_ok"] = ~out["quality_flag"].isin(DATA_QUALITY_BLOCKING_FLAGS)

    out["neg_price_explained_by_surplus_ratio"] = pd.to_numeric(
        out.get("neg_price_explained_by_surplus_ratio", np.nan),
        errors="coerce",
    )
    if "market_physical_gap_flag" in out.columns:
        out["market_physical_gap_flag"] = out["market_physical_gap_flag"].fillna(False).astype(bool)
    else:
        out["market_physical_gap_flag"] = False
    if market_physical_gap_ratios:
        for i, row in out[["country", "year"]].iterrows():
            y = _safe_float(row.get("year"), np.nan)
            if not np.isfinite(y):
                continue
            key = (str(row["country"]), int(y))
            ratio = market_physical_gap_ratios.get(key)
            if ratio is None:
                continue
            out.at[i, "neg_price_explained_by_surplus_ratio"] = float(ratio)
            out.at[i, "market_physical_gap_flag"] = bool(ratio < 0.5)
    out["market_physical_gap_flag"] = out["market_physical_gap_flag"] | (
        pd.to_numeric(out["neg_price_explained_by_surplus_ratio"], errors="coerce") < 0.5
    )
    out["market_physical_gap_flag"] = out["market_physical_gap_flag"].fillna(False).astype(bool)

    phase2_market_core_country = out["family_count"] >= 2
    phase2_market_core_pv = out["family_count_pv"] >= 2
    phase2_market_core_wind = out["family_count_wind"] >= 2
    out["is_phase2_market"] = phase2_market_core_country & out["quality_ok"].fillna(False) & (~out["crisis_year"].fillna(False))
    out["is_phase2_physical"] = out["PHYSICAL_STRESS_FLAG"] & out["quality_ok"].fillna(False) & (~out["crisis_year"].fillna(False))
    out["stage2_candidate_year"] = out["is_phase2_market"]
    out["stage2_candidate_year_pv"] = phase2_market_core_pv & out["quality_ok"].fillna(False) & (~out["crisis_year"].fillna(False))
    out["stage2_candidate_year_wind"] = phase2_market_core_wind & out["quality_ok"].fillna(False) & (~out["crisis_year"].fillna(False))
    out["stage2_candidate_year_country"] = out["is_phase2_market"]
    out["phase2_candidate_year"] = out["stage2_candidate_year"]
    out["flag_capture_only_stage2"] = out["CAPTURE_DEGRADATION_FLAG"] & (~out["LOW_PRICE_FLAG"]) & (~out["PHYSICAL_STRESS_FLAG"])
    out["physical_candidate_year"] = out["is_phase2_physical"]
    out["signal_low_price"] = out["low_price_family"]
    out["signal_value"] = out["value_family"]
    out["signal_physical"] = out["physical_family"]
    out["flag_non_capture_stage2"] = out["low_price_family"].astype(int) + out["physical_family"].astype(int)
    out["active_flags"] = out.apply(_flag_list, axis=1)

    stage_components = out.apply(lambda row: _stage1_score_components(row, p), axis=1)
    out["stage1_score"] = stage_components.apply(lambda x: int(x[0]))
    out["stage1_h_negative_ok"] = stage_components.apply(lambda x: bool(x[1]))
    out["stage1_h_below_5_ok"] = stage_components.apply(lambda x: bool(x[2]))
    out["stage1_capture_ok"] = stage_components.apply(lambda x: bool(x[3]))
    out["stage1_sr_ok"] = stage_components.apply(lambda x: bool(x[4]))
    out["is_stage1_criteria"] = (
        out.apply(lambda row: _is_stage1(row, p), axis=1)
        & out["quality_ok"].fillna(False)
        & (~out["crisis_year"].fillna(False))
    )
    out["is_stage1"] = out["is_stage1_criteria"]
    out["stage1_candidate_year"] = out["is_stage1_criteria"]
    out["phase_market"] = np.select(
        [out["is_stage1_criteria"], out["is_phase2_market"]],
        ["phase1", "phase2"],
        default="uncertain",
    )
    out["stress_phys_state"] = np.select(
        [
            ~out["PHYSICAL_STRESS_FLAG"],
            out["PHYSICAL_STRESS_FLAG"] & out["LOW_PRICE_FLAG"],
            out["PHYSICAL_STRESS_FLAG"] & (~out["LOW_PRICE_FLAG"]),
        ],
        ["pas_de_stress_physique", "stress_physique_avec_signal_prix", "stress_physique_sans_signal_prix"],
        default="unknown",
    )
    return out


def _first_persistent_year(group: pd.DataFrame, col: str, window_years: int) -> float:
    start, _ = _persistent_run_start_and_status(group, col, window_years)
    return start


def _persistent_run_start_and_status(group: pd.DataFrame, col: str, window_years: int) -> tuple[float, str]:
    if group.empty or col not in group.columns:
        return float("nan"), "not_reached_in_window"

    w = max(1, int(window_years))
    g = group.sort_values("year").copy()
    # Persistence is evaluated on the non-crisis sequence only.
    if "crisis_year" in g.columns:
        g = g[~g["crisis_year"].fillna(False).astype(bool)].copy()
    if g.empty:
        return float("nan"), "not_reached_in_window"
    years = pd.to_numeric(g["year"], errors="coerce")
    flags = g[col].fillna(False).astype(bool)
    if years.notna().sum() == 0:
        return float("nan"), "not_reached_in_window"

    first_year = int(years.dropna().iloc[0])
    n = len(g)
    i = 0
    while i < n:
        y0 = _safe_float(years.iloc[i], np.nan)
        if not (np.isfinite(y0) and bool(flags.iloc[i])):
            i += 1
            continue
        run_start = int(y0)
        run_len = 1
        j = i + 1
        while j < n:
            yj = _safe_float(years.iloc[j], np.nan)
            if not (np.isfinite(yj) and bool(flags.iloc[j])):
                break
            run_len += 1
            j += 1
        if run_len >= w:
            status = "already_phase2_at_window_start" if run_start == first_year else "transition_observed"
            return float(run_start), status
        i = max(j, i + 1)

    return float("nan"), "not_reached_in_window"


def _is_market_persistent(group: pd.DataFrame, bascule_year: float, window_years: int = 2) -> bool:
    if not np.isfinite(bascule_year):
        return False
    y0 = int(bascule_year)
    subset = group[group["year"] >= y0].sort_values("year").copy()
    if subset.empty:
        return False
    start, _ = _persistent_run_start_and_status(subset, "stage2_candidate_year", window_years)
    return bool(np.isfinite(start) and int(start) == y0)


def _parse_evidence_ratio(evidence: Any) -> float:
    txt = str(evidence or "")
    if not txt:
        return float("nan")
    try:
        import re

        m = re.search(r"ratio(?:_ab_or_low_residual|_ab|)\s*=\s*([0-9]*\.?[0-9]+)", txt)
        if m:
            return float(m.group(1))
        return float(txt)
    except Exception:
        return float("nan")


def _market_physical_gap_from_findings(validation_findings_df: pd.DataFrame | None) -> dict[tuple[str, int], float]:
    overrides: dict[tuple[str, int], float] = {}
    if validation_findings_df is None or validation_findings_df.empty:
        return overrides
    req = {"country", "year", "code"}
    if not req.issubset(set(validation_findings_df.columns)):
        return overrides
    vf = validation_findings_df.copy()
    vf["country"] = vf["country"].astype(str)
    vf["year"] = pd.to_numeric(vf["year"], errors="coerce")
    vf["code"] = vf["code"].astype(str)
    vf = vf[
        vf["code"].isin(
            [
                "RC_NEG_NOT_IN_SURPLUS",
                "RC_NEG_NOT_IN_AB",
                "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
            ]
        )
        & vf["year"].notna()
    ]
    if vf.empty:
        return overrides
    for _, row in vf.iterrows():
        ratio = _parse_evidence_ratio(row.get("evidence", ""))
        if np.isfinite(ratio):
            overrides[(str(row["country"]), int(row["year"]))] = float(ratio)
    return overrides


def _drivers_at_bascule(row: pd.Series, p: dict[str, float]) -> str:
    drivers: list[str] = []
    if bool(row.get("low_price_family", False)):
        if bool(row.get("flag_h_negative_stage2", False)):
            drivers.append(
                f"LOW_PRICE:h_negative_obs>={_safe_param(p, 'h_negative_stage2_min', 200.0)} ({_safe_float(row.get('h_negative_obs'), np.nan):.1f})"
            )
        if bool(row.get("flag_h_below_5_stage2", False)):
            drivers.append(
                f"LOW_PRICE:h_below_5_obs>={_safe_param(p, 'h_below_5_stage2_min', 500.0)} ({_safe_float(row.get('h_below_5_obs'), np.nan):.1f})"
            )
        if bool(row.get("flag_low_price_share_high", False)):
            drivers.append(
                f"LOW_PRICE:low_price_hours_share>={_safe_param(p, 'low_price_hours_share_stage2_min', _safe_param(p, 'h_below_5_stage2_min', 500.0)/8760.0):.3f} ({_safe_float(row.get('low_price_hours_share'), np.nan):.3f})"
            )
    if bool(row.get("value_family", False)):
        if bool(row.get("flag_capture_pv_low", False)):
            drivers.append(
                f"VALUE:capture_ratio_pv<={_safe_param(p, 'capture_ratio_pv_stage2_max', 0.80):.2f} ({_safe_float(row.get('capture_ratio_pv'), np.nan):.3f})"
            )
        if bool(row.get("flag_capture_wind_low", False)):
            drivers.append(
                f"VALUE:capture_ratio_wind<={_safe_param(p, 'capture_ratio_wind_stage2_max', 0.90):.2f} ({_safe_float(row.get('capture_ratio_wind'), np.nan):.3f})"
            )
    if bool(row.get("physical_family", False)):
        if bool(row.get("flag_sr_energy_high", False)):
            drivers.append(
                f"PHYSICAL:sr_energy>={_safe_param(p, 'sr_energy_stage2_min', _safe_param(p, 'sr_energy_material_min', 0.01)):.3f} ({_safe_float(row.get('sr_energy_share_gen', row.get('sr_energy')), np.nan):.3f})"
            )
        if bool(row.get("flag_sr_hours_high", False)):
            drivers.append(
                f"PHYSICAL:sr_hours>={_safe_param(p, 'sr_hours_stage2_min', 0.10):.2f} ({_safe_float(row.get('sr_hours_share'), np.nan):.3f})"
            )
        if bool(row.get("flag_far_low", False)):
            drivers.append(
                f"PHYSICAL:far_observed<{_safe_param(p, 'far_stage2_min', 0.95):.2f} ({_safe_float(row.get('far_observed'), np.nan):.3f})"
            )
        if bool(row.get("flag_ir_high", False)):
            drivers.append(
                f"PHYSICAL:ir_p10>={_safe_param(p, 'ir_p10_stage2_min', 1.5):.2f} ({_safe_float(row.get('ir_p10'), np.nan):.3f})"
            )
    return "; ".join(drivers)


def _quality_flags_from_row(row: pd.Series) -> str:
    flags: list[str] = []
    if bool(row.get("flag_unexplained_negative_prices", False)):
        flags.append("UNEXPLAINED_NEGATIVE_PRICES")
    return "; ".join(flags)


def _families_active_at_row(row: pd.Series, tech: str | None = None) -> str:
    families: list[str] = []
    if bool(row.get("low_price_family", False)):
        families.append("LOW_PRICE")
    if bool(row.get("physical_family", False)):
        families.append("PHYSICAL")
    t = str(tech or "").upper().strip()
    if t == "PV":
        if bool(row.get("value_family_pv", False)):
            families.append("VALUE_PV")
    elif t == "WIND":
        if bool(row.get("value_family_wind", False)):
            families.append("VALUE_WIND")
    else:
        if bool(row.get("value_family_pv", False)):
            families.append("VALUE_PV")
        if bool(row.get("value_family_wind", False)):
            families.append("VALUE_WIND")
    return ",".join(families)


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
    g["sr_hours_share"] = pd.to_numeric(g.get("sr_hours_share", g.get("sr_hours")), errors="coerce") / demand_factor
    g["ir_p10"] = pd.to_numeric(g.get("ir_p10"), errors="coerce") / demand_factor
    far = pd.to_numeric(g.get("far_observed", g.get("far_energy")), errors="coerce")
    g["far_observed"] = 1.0 - (1.0 - far) / flex_factor
    g["far_energy"] = g["far_observed"]
    cap_pv = pd.to_numeric(g.get("capture_ratio_pv"), errors="coerce")
    cap_w = pd.to_numeric(g.get("capture_ratio_wind"), errors="coerce")
    cap_boost = 0.10 * float(demand_uplift) + 0.08 * float(flex_uplift)
    g["capture_ratio_pv"] = (cap_pv + cap_boost).clip(lower=0.0, upper=2.0)
    g["capture_ratio_wind"] = (cap_w + cap_boost).clip(lower=0.0, upper=2.0)
    return g


def _required_lever_to_avoid_phase2(
    group: pd.DataFrame,
    p: dict[str, float],
    lever: str,
    max_uplift: float,
    crisis_years_global: set[int] | None = None,
    crisis_years_by_country: dict[str, set[int]] | None = None,
) -> tuple[float | None, str]:
    scoped = group.sort_values("year").copy()
    if scoped.empty:
        return None, "insufficient_data"
    if crisis_years_global is None:
        crisis_years_global, cfg_by_country = _load_crisis_years_from_config()
        crisis_years_by_country = cfg_by_country
    crisis_years_by_country = crisis_years_by_country or {}
    baseline = _apply_phase2_logic(
        scoped,
        p,
        crisis_years_global=crisis_years_global,
        crisis_years_by_country=crisis_years_by_country,
    )
    y0 = _first_persistent_year(baseline, "stage2_candidate_year", _safe_param(p, "q1_persistence_window_years", 3.0))
    if not np.isfinite(y0):
        return 0.0, "already_not_phase2"

    hi = float(max(0.0, max_uplift))
    lo = 0.0

    def _cond(x: float) -> bool:
        if lever == "demand":
            adj = _adjust_for_lever(scoped, demand_uplift=x, flex_uplift=0.0)
        else:
            adj = _adjust_for_lever(scoped, demand_uplift=0.0, flex_uplift=x)
        panel_x = _apply_phase2_logic(
            adj,
            p,
            crisis_years_global=crisis_years_global,
            crisis_years_by_country=crisis_years_by_country,
        )
        return not np.isfinite(_first_persistent_year(panel_x, "stage2_candidate_year", _safe_param(p, "q1_persistence_window_years", 3.0)))

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
    metrics = ["capture_ratio_pv", "capture_ratio_wind", "h_negative_obs", "sr_hours_share", "far_observed", "ir_p10"]
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


def _build_residual_diagnostics(
    panel: pd.DataFrame,
    hourly_by_country_year: dict[tuple[str, int], pd.DataFrame] | None,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if panel.empty:
        return pd.DataFrame()
    hourly_by_country_year = hourly_by_country_year or {}

    for _, prow in panel.iterrows():
        country = str(prow.get("country", ""))
        year = int(prow.get("year"))
        key = (country, year)
        row: dict[str, Any] = {"country": country, "year": year}
        if key in hourly_by_country_year and hourly_by_country_year[key] is not None and not hourly_by_country_year[key].empty:
            h = hourly_by_country_year[key]
            nrl_raw = h.get("nrl_mw")
            nrl = (
                pd.to_numeric(nrl_raw, errors="coerce")
                if isinstance(nrl_raw, pd.Series)
                else pd.Series(np.nan, index=h.index, dtype=float)
            )
            price_raw = h.get("price_da_eur_mwh")
            price = (
                pd.to_numeric(price_raw, errors="coerce")
                if isinstance(price_raw, pd.Series)
                else pd.Series(np.nan, index=h.index, dtype=float)
            )
            low_residual = (
                pd.to_numeric(h.get("low_residual_hour"), errors="coerce").fillna(0.0) > 0
                if "low_residual_hour" in h.columns
                else pd.Series(False, index=h.index)
            )
            neg = price < 0
            row.update(
                {
                    "residual_load_p10_mw": _safe_float(nrl.quantile(0.10), np.nan) if nrl.notna().any() else np.nan,
                    "residual_load_p50_mw": _safe_float(nrl.quantile(0.50), np.nan) if nrl.notna().any() else np.nan,
                    "residual_load_p90_mw": _safe_float(nrl.quantile(0.90), np.nan) if nrl.notna().any() else np.nan,
                    "price_low_residual_median_eur_mwh": _safe_float(price[low_residual].median(), np.nan) if bool(low_residual.any()) else np.nan,
                    "price_negative_median_eur_mwh": _safe_float(price[neg].median(), np.nan) if bool(neg.any()) else np.nan,
                    "residual_negative_p10_mw": _safe_float(nrl[neg].quantile(0.10), np.nan) if bool(neg.any()) else np.nan,
                    "residual_negative_p50_mw": _safe_float(nrl[neg].quantile(0.50), np.nan) if bool(neg.any()) else np.nan,
                    "residual_negative_p90_mw": _safe_float(nrl[neg].quantile(0.90), np.nan) if bool(neg.any()) else np.nan,
                }
            )
        else:
            row.update(
                {
                    "residual_load_p10_mw": _safe_float(prow.get("residual_load_p10_mw"), np.nan),
                    "residual_load_p50_mw": _safe_float(prow.get("residual_load_p50_mw"), np.nan),
                    "residual_load_p90_mw": _safe_float(prow.get("residual_load_p90_mw"), np.nan),
                    "price_low_residual_median_eur_mwh": _safe_float(prow.get("price_low_residual_median_eur_mwh"), np.nan),
                    "price_negative_median_eur_mwh": _safe_float(prow.get("price_negative_hours_median_eur_mwh"), np.nan),
                    "residual_negative_p10_mw": np.nan,
                    "residual_negative_p50_mw": _safe_float(prow.get("residual_load_p50_on_negative_price_mw"), np.nan),
                    "residual_negative_p90_mw": np.nan,
                }
            )
        rows.append(row)

    return pd.DataFrame(rows).sort_values(["country", "year"]).reset_index(drop=True)


def _ensure_reason_code_metrics_available(panel: pd.DataFrame) -> None:
    missing = sorted([c for c in Q1_REASON_CODE_REQUIRED_METRICS if c not in panel.columns])
    if missing:
        raise ValueError(
            "Q1 reason_codes reference metrics missing from annual_metrics_phase1: "
            + ", ".join(missing)
        )


def _build_q1_yearly_diagnostics(
    panel: pd.DataFrame,
    summary: pd.DataFrame,
    params: dict[str, float],
) -> pd.DataFrame:
    if panel.empty:
        return pd.DataFrame()
    persist_window = int(_safe_param(params, "q1_persistence_window_years", 2.0))
    out = panel.copy()
    out["score_price"] = out[["flag_h_negative_stage2", "flag_h_below_5_stage2", "flag_low_price_share_high"]].fillna(False).astype(int).sum(axis=1)
    out["score_value"] = out[["flag_capture_pv_low", "flag_capture_wind_low"]].fillna(False).astype(int).sum(axis=1)
    out["score_physical"] = out[["flag_sr_energy_high", "flag_sr_hours_high", "flag_ir_high"]].fillna(False).astype(int).sum(axis=1)
    out["family_count_overall"] = out[["low_price_family", "value_family", "physical_family"]].fillna(False).astype(int).sum(axis=1)
    out["stage_label"] = np.select(
        [
            out["is_phase2_market"].fillna(False),
            out["is_stage1_criteria"].fillna(False),
        ],
        ["Phase2", "Phase1"],
        default="ambiguous",
    )
    out["reason_codes"] = out.apply(lambda r: _drivers_at_bascule(r, params), axis=1)
    keep_cols = [
        "country",
        "year",
        "stage_label",
        "family_count_overall",
        "score_price",
        "score_value",
        "score_physical",
        "low_price_family",
        "value_family",
        "physical_family",
        "value_family_pv",
        "value_family_wind",
        "is_phase2_market",
        "is_stage1_criteria",
        "reason_codes",
    ]
    diag = out[[c for c in keep_cols if c in out.columns]].copy()
    if not summary.empty:
        enrich_cols = [
            "country",
            "bascule_year_market",
            "bascule_year_market_pv",
            "bascule_year_market_wind",
            "bascule_confidence",
        ]
        diag = diag.merge(summary[[c for c in enrich_cols if c in summary.columns]], on="country", how="left")
    diag["persistence_window_years"] = persist_window
    return diag.sort_values(["country", "year"]).reset_index(drop=True)


def _build_negative_price_explainability(
    panel: pd.DataFrame,
    hourly_by_country_year: dict[tuple[str, int], pd.DataFrame] | None,
) -> pd.DataFrame:
    if panel.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    hourly_by_country_year = hourly_by_country_year or {}
    for _, row in panel[["country", "year"]].iterrows():
        country = str(row["country"])
        year = int(_safe_float(row["year"], np.nan))
        key = (country, year)
        share_a = np.nan
        share_b = np.nan
        share_low = np.nan
        share_union = np.nan
        neg_hours = np.nan

        hourly = hourly_by_country_year.get(key)
        if hourly is not None and not hourly.empty and COL_PRICE_DA in hourly.columns:
            price = pd.to_numeric(hourly.get(COL_PRICE_DA), errors="coerce")
            reg = hourly.get(COL_REGIME, pd.Series(index=hourly.index, dtype=object)).astype(str)
            if COL_LOW_RESIDUAL_HOUR in hourly.columns:
                low_residual = pd.to_numeric(hourly.get(COL_LOW_RESIDUAL_HOUR), errors="coerce").fillna(0.0) > 0.0
            else:
                nrl_raw = hourly.get("nrl_mw")
                nrl = (
                    pd.to_numeric(nrl_raw, errors="coerce")
                    if isinstance(nrl_raw, pd.Series)
                    else pd.Series(np.nan, index=hourly.index, dtype=float)
                )
                nrl_pos = nrl[nrl > 0.0]
                if nrl_pos.notna().any():
                    low_residual_threshold = float(nrl_pos.quantile(0.10))
                    low_residual = (nrl > 0.0) & (nrl <= low_residual_threshold)
                else:
                    low_residual = pd.Series(False, index=hourly.index, dtype=bool)
            neg = price < 0.0
            neg_count = int(neg.sum())
            neg_hours = float(neg_count)
            if neg_count > 0:
                share_a = float((neg & reg.eq("A")).sum()) / float(neg_count)
                share_b = float((neg & reg.eq("B")).sum()) / float(neg_count)
                share_low = float((neg & low_residual).sum()) / float(neg_count)
                share_union = float((neg & (reg.isin(["A", "B"]) | low_residual)).sum()) / float(neg_count)

        if not np.isfinite(share_union):
            p_row = panel[(panel["country"].astype(str) == country) & (pd.to_numeric(panel["year"], errors="coerce") == year)]
            if not p_row.empty:
                r0 = p_row.iloc[0]
                share_union = _safe_float(r0.get("share_neg_price_hours_in_AB_OR_LOW_RESIDUAL"), np.nan)
                share_low = _safe_float(r0.get("share_neg_price_hours_in_low_residual"), np.nan)
                if np.isfinite(_safe_float(r0.get("share_neg_price_hours_in_AB"), np.nan)):
                    share_ab = _safe_float(r0.get("share_neg_price_hours_in_AB"), np.nan)
                    share_a = share_ab
                    share_b = 0.0

        share_unexplained = (1.0 - share_union) if np.isfinite(share_union) else np.nan
        if np.isfinite(share_unexplained):
            share_unexplained = float(np.clip(share_unexplained, 0.0, 1.0))
        rows.append(
            {
                "country": country,
                "year": year,
                "negative_hours": neg_hours,
                "share_neg_hours_in_regime_A": share_a,
                "share_neg_hours_in_regime_B": share_b,
                "share_neg_hours_in_low_residual_bucket": share_low,
                "share_neg_hours_explained_union": share_union,
                "share_neg_hours_unexplained": share_unexplained,
                "flag_unexplained_negative_prices": bool(
                    np.isfinite(share_unexplained) and share_unexplained > Q1_UNEXPLAINED_NEGATIVE_PRICES_MAX
                ),
            }
        )
    return pd.DataFrame(rows).sort_values(["country", "year"]).reset_index(drop=True)


def run_q1(
    annual_df: pd.DataFrame,
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
    hourly_by_country_year: dict[tuple[str, int], pd.DataFrame] | None = None,
    validation_findings_df: pd.DataFrame | None = None,
) -> ModuleResult:
    countries = selection.get("countries", sorted(annual_df["country"].dropna().unique().tolist()))
    years = selection.get("years", sorted(annual_df["year"].dropna().unique().tolist()))

    panel = annual_df[annual_df["country"].isin(countries) & annual_df["year"].isin(years)].copy()
    panel = panel.sort_values(["country", "year"]).reset_index(drop=True)
    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q1_PARAMS)].iterrows()
    }

    crisis_years_global, crisis_years_by_country = _resolve_crisis_years(selection)
    market_physical_gap_overrides = _market_physical_gap_from_findings(validation_findings_df)
    panel = _apply_phase2_logic(
        panel,
        params,
        crisis_years_global=crisis_years_global,
        crisis_years_by_country=crisis_years_by_country,
        quality_overrides=None,
        market_physical_gap_ratios=market_physical_gap_overrides,
    )
    _ensure_reason_code_metrics_available(panel)
    q1_negative_price_explainability = _build_negative_price_explainability(panel, hourly_by_country_year)
    if not q1_negative_price_explainability.empty:
        panel = panel.merge(
            q1_negative_price_explainability[
                ["country", "year", "share_neg_hours_unexplained", "flag_unexplained_negative_prices"]
            ],
            on=["country", "year"],
            how="left",
            suffixes=("", "_expl"),
        )
        if "flag_unexplained_negative_prices_expl" in panel.columns:
            panel["flag_unexplained_negative_prices"] = (
                panel["flag_unexplained_negative_prices"].fillna(False)
                | panel["flag_unexplained_negative_prices_expl"].fillna(False)
            )
            panel = panel.drop(columns=["flag_unexplained_negative_prices_expl"])
        if "share_neg_hours_unexplained_expl" in panel.columns:
            panel["share_neg_hours_unexplained"] = panel["share_neg_hours_unexplained_expl"].combine_first(
                panel["share_neg_hours_unexplained"]
            )
            panel = panel.drop(columns=["share_neg_hours_unexplained_expl"])
    panel["quality_flag_unexplained_neg_prices"] = panel.get("flag_unexplained_negative_prices", False).fillna(False).astype(bool)
    panel["quality_flags"] = panel.apply(_quality_flags_from_row, axis=1)

    checks: list[dict[str, str]] = []
    warnings: list[str] = []
    summary_rows: list[dict[str, Any]] = []
    persist_window = int(_safe_param(params, "q1_persistence_window_years", 3.0))
    max_lever = float(_safe_param(params, "q1_lever_max_uplift", 1.0))

    for country, group in panel.groupby("country"):
        group = group.sort_values("year").copy()
        bascule_year_pv, bascule_status_market_pv = _persistent_run_start_and_status(
            group,
            "stage2_candidate_year_pv",
            persist_window,
        )
        bascule_year_wind, bascule_status_market_wind = _persistent_run_start_and_status(
            group,
            "stage2_candidate_year_wind",
            persist_window,
        )
        if np.isfinite(bascule_year_pv) and np.isfinite(bascule_year_wind):
            bascule_year = float(min(int(bascule_year_pv), int(bascule_year_wind)))
        elif np.isfinite(bascule_year_pv):
            bascule_year = float(int(bascule_year_pv))
        elif np.isfinite(bascule_year_wind):
            bascule_year = float(int(bascule_year_wind))
        else:
            bascule_year = float("nan")
        bascule_status_market = (
            "transition_observed"
            if np.isfinite(bascule_year)
            else (
                "already_phase2_at_window_start"
                if ("already_phase2_at_window_start" in {bascule_status_market_pv, bascule_status_market_wind})
                else "not_reached_in_window"
            )
        )
        physical_year, bascule_status_physical = _persistent_run_start_and_status(group, "physical_candidate_year", persist_window)
        stage1_year, _ = _persistent_run_start_and_status(group, "stage1_candidate_year", persist_window)
        if np.isfinite(bascule_year):
            at_rows = group[group["year"] == int(bascule_year)]
            at = at_rows.iloc[0] if not at_rows.empty else group.iloc[-1]
        else:
            at = group.iloc[-1]
        at_pv = (
            group[group["year"] == int(bascule_year_pv)].iloc[0]
            if np.isfinite(bascule_year_pv) and not group[group["year"] == int(bascule_year_pv)].empty
            else at
        )
        at_wind = (
            group[group["year"] == int(bascule_year_wind)].iloc[0]
            if np.isfinite(bascule_year_wind) and not group[group["year"] == int(bascule_year_wind)].empty
            else at
        )

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
                bad_quality = ~around.get("quality_ok", pd.Series(False, index=around.index)).fillna(False).astype(bool)
                if bool(bad_quality.fillna(False).any()):
                    confidence -= 0.10
                if bool(around.get("flag_unexplained_negative_prices", pd.Series(False, index=around.index)).fillna(False).any()):
                    confidence -= 0.20
            if not _is_market_persistent(group, bascule_year, persist_window):
                confidence -= 0.20
        confidence = float(np.clip(confidence, 0.0, 1.0))

        req_demand, req_demand_status = _required_lever_to_avoid_phase2(
            group,
            params,
            "demand",
            max_uplift=max_lever,
            crisis_years_global=crisis_years_global,
            crisis_years_by_country=crisis_years_by_country,
        )
        req_flex, req_flex_status = _required_lever_to_avoid_phase2(
            group,
            params,
            "flex",
            max_uplift=max_lever,
            crisis_years_global=crisis_years_global,
            crisis_years_by_country=crisis_years_by_country,
        )

        if bascule_status_market == "transition_observed":
            rationale = "Bascule validee: >=2 familles actives (LOW_PRICE/VALUE/PHYSICAL) sur 2 annees consecutives hors crise."
        elif bascule_status_market == "already_phase2_at_window_start":
            rationale = "Phase2 deja active au debut de fenetre: transition anterieure au scope observe."
        else:
            rationale = "Pas de bascule persistante sur la fenetre."

        summary_rows.append(
            {
                "country": country,
                "bascule_year_market": bascule_year,
                "bascule_year_market_country": bascule_year,
                "bascule_year_market_pv": bascule_year_pv,
                "bascule_year_market_wind": bascule_year_wind,
                "bascule_year_physical": physical_year,
                "bascule_year_market_observed": bascule_year if bascule_status_market == "transition_observed" else np.nan,
                "bascule_year_physical_observed": physical_year if bascule_status_physical == "transition_observed" else np.nan,
                "bascule_status_market": bascule_status_market,
                "bascule_status_market_pv": bascule_status_market_pv,
                "bascule_status_market_wind": bascule_status_market_wind,
                "bascule_status_physical": bascule_status_physical,
                "stage1_bascule_year": stage1_year,
                "stage1_detected": bool(np.isfinite(stage1_year)),
                "bascule_confidence": confidence,
                "families_active_at_bascule_pv": _families_active_at_row(at_pv, tech="PV"),
                "families_active_at_bascule_wind": _families_active_at_row(at_wind, tech="WIND"),
                "families_active_at_bascule_country": _families_active_at_row(at, tech=None),
                "drivers_at_bascule": _drivers_at_bascule(at, params),
                "quality_flag_unexplained_neg_prices": bool(at.get("flag_unexplained_negative_prices", False)),
                "quality_flags": _quality_flags_from_row(at),
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
                "far_energy_at_bascule": at.get("far_observed", at.get("far_energy", np.nan)),
                "ir_p10_at_bascule": at.get("ir_p10", np.nan),
                "ttl_at_bascule": at.get("ttl_eur_mwh", np.nan),
                "capture_ratio_pv_vs_ttl_at_bascule": at.get("capture_ratio_pv_vs_ttl", np.nan),
                "capture_ratio_pv_at_bascule": at.get("capture_ratio_pv", np.nan),
                "capture_ratio_wind_at_bascule": at.get("capture_ratio_wind", np.nan),
                "market_physical_gap_at_bascule": bool(at.get("market_physical_gap_flag", False)),
                "neg_price_explained_by_surplus_ratio_at_bascule": _safe_float(at.get("neg_price_explained_by_surplus_ratio"), np.nan),
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
        if bool(row.get("is_phase2_market", False)) and int(_safe_float(row.get("family_count"), 0.0)) < 2:
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q1_NO_FALSE_PHASE2_WITHOUT_TWO_FAMILIES",
                    "message": (
                        f"{row['country']} {int(row['year'])}: is_phase2_market exige >=2 familles "
                        "actives parmi LOW_PRICE/VALUE/PHYSICAL."
                    ),
                }
            )
        if bool(row.get("is_phase2_market", False)) and (
            (not bool(row.get("LOW_PRICE_FLAG", False)))
            and (not bool(row.get("PHYSICAL_STRESS_FLAG", False)))
            and (not bool(row.get("CAPTURE_DEGRADATION_FLAG", False)))
        ):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q1_NO_FALSE_PHASE2_WITHOUT_ANY_FAMILY",
                    "message": f"{row['country']} {int(row['year'])}: impossible d'avoir phase2 sans aucune famille active.",
                }
            )
        capture_ratio_pv = _safe_float(row.get("capture_ratio_pv"), np.nan)
        if np.isfinite(capture_ratio_pv) and capture_ratio_pv >= 1.0 and bool(row.get("flag_capture_pv_low", False)):
            checks.append(
                {
                    "status": "WARN",
                    "code": "Q1_CAPTURE_LOW_CONTRADICTION",
                    "message": f"{row['country']} {int(row['year'])}: flag_capture_pv_low=True alors que capture_ratio_pv={capture_ratio_pv:.3f}>=1.0.",
                }
            )
        healthy = bool(
            int(_safe_float(row.get("stage1_score"), 0.0)) >= 3
            and (not bool(row.get("CAPTURE_DEGRADATION_FLAG", False)))
        )
        if healthy and bool(row.get("quality_ok", False)) and (not bool(row.get("crisis_year", False))) and not bool(row.get("is_stage1_criteria", False)):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
                    "message": f"{row['country']} {int(row['year'])}: annee saine non marquee stage1.",
                }
            )
        if bool(row.get("phase_market") == "phase1") and bool(row.get("CAPTURE_DEGRADATION_FLAG", False)) and bool(row.get("LOW_PRICE_FLAG", False)):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q1_PHASE1_CONTRADICTION",
                    "message": f"{row['country']} {int(row['year'])}: phase1 incompatible avec LOW_PRICE_FLAG et CAPTURE_DEGRADATION_FLAG.",
                }
            )
        if str(selection.get("mode", "HIST")).upper() == "SCEN":
            far_val = _safe_float(row.get("far_observed"), np.nan)
            if not np.isfinite(far_val):
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "Q1_SCEN_FAR_NAN",
                        "message": f"{row['country']} {int(row['year'])}: far_observed manquant en scenario.",
                    }
                )
        for share_col in ["must_run_share_load", "must_run_share_netdemand"]:
            share_val = _safe_float(row.get(share_col), np.nan)
            if np.isfinite(share_val) and not (0.0 <= share_val <= 1.0):
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "Q1_MUSTRUN_SHARE_OUT_OF_RANGE",
                        "message": f"{row['country']} {int(row['year'])}: {share_col} hors [0,1].",
                    }
                )

    stage2_mask = panel.get("is_phase2_market", pd.Series(False, index=panel.index)).fillna(False).astype(bool)
    if bool(stage2_mask.any()):
        h_neg_thr = _safe_param(params, "h_negative_stage2_min", 200.0)
        h_low_thr = _safe_param(params, "h_below_5_stage2_min", 500.0)
        spread_thr = _safe_param(params, "days_spread_gt50_stage2_min", 150.0)
        h_neg = pd.to_numeric(panel.get("h_negative_obs"), errors="coerce")
        h_low = pd.to_numeric(panel.get("h_below_5_obs"), errors="coerce")
        spread = pd.to_numeric(panel.get("days_spread_gt50"), errors="coerce")
        if spread.notna().sum() == 0:
            spread = pd.to_numeric(panel.get("days_spread_50_obs"), errors="coerce")
        low_price_evidence = (h_neg >= h_neg_thr) | (h_low >= h_low_thr) | (spread >= spread_thr)
        invalid = stage2_mask & (~low_price_evidence.fillna(False))
        if bool(invalid.any()):
            for _, bad_row in panel.loc[invalid, ["country", "year", "h_negative_obs", "h_below_5_obs"]].iterrows():
                bad_year = _safe_float(bad_row.get("year"), np.nan)
                bad_year_txt = str(int(bad_year)) if np.isfinite(bad_year) else "NA"
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "TEST_Q1_001",
                        "message": (
                            f"{bad_row['country']}-{bad_year_txt}: stage2 sans evidence low-price "
                            f"(h_negative={_safe_float(bad_row.get('h_negative_obs'), np.nan):.1f}, "
                            f"h_below_5={_safe_float(bad_row.get('h_below_5_obs'), np.nan):.1f})."
                        ),
                    }
                )
        else:
            checks.append(
                {
                    "status": "PASS",
                    "code": "TEST_Q1_001",
                    "message": "Toutes les lignes stage2 ont au moins un signal low-price (h_negative/h_below_5/days_spread_gt50).",
                }
            )
    else:
        checks.append({"status": "WARN", "code": "TEST_Q1_001", "message": "Aucune ligne stage2 observee; test non applicable."})

    summary = pd.DataFrame(summary_rows)
    for col, default in {
        "bascule_status_market": "not_reached_in_window",
        "bascule_status_physical": "not_reached_in_window",
        "bascule_year_market": np.nan,
        "bascule_year_physical": np.nan,
    }.items():
        if col not in summary.columns:
            summary[col] = default
    q1_rule_definition = _build_rule_definition(params, crisis_years=crisis_years_global)
    q1_rule_application_cols = [
        "country",
        "year",
        "capture_ratio_pv",
        "capture_ratio_wind",
        "stage2_market_score",
        "score_breakdown",
        "crisis_year",
        "quality_flag",
        "quality_ok",
        "quality_flag_unexplained_neg_prices",
        "quality_flags",
        "stage2_candidate_year",
        "stage1_candidate_year",
        "phase2_candidate_year",
        "low_price_flags_count",
        "physical_flags_count",
        "capture_flags_count",
        "active_flags",
        "flag_h_negative_stage2",
        "flag_h_below_5_stage2",
        "flag_low_price_share_high",
        "flag_capture_pv_low",
        "flag_capture_wind_low",
        "flag_sr_energy_high",
        "flag_sr_hours_high",
        "flag_low_residual_high",
        "flag_sr_high",
        "flag_far_low",
        "flag_ir_high",
        "flag_spread_high",
        "LOW_PRICE_FLAG",
        "CAPTURE_DEGRADATION_FLAG",
        "PHYSICAL_STRESS_FLAG",
        "stage1_score",
        "stage1_h_negative_ok",
        "stage1_h_below_5_ok",
        "stage1_capture_ok",
        "stage1_sr_ok",
        "is_stage1",
        "market_physical_gap_flag",
        "neg_price_explained_by_surplus_ratio",
        "low_price_family",
        "value_family",
        "value_family_pv",
        "value_family_wind",
        "physical_family",
        "family_count_pv",
        "family_count_wind",
        "stage2_candidate_year_pv",
        "stage2_candidate_year_wind",
        "stage2_candidate_year_country",
        "physical_candidate_year",
        "flag_capture_only_stage2",
        "is_stage1_criteria",
        "is_phase2_market",
        "is_phase2_physical",
        "phase_market",
        "stress_phys_state",
    ]
    q1_rule_application = panel[[c for c in q1_rule_application_cols if c in panel.columns]].copy()
    q1_before_after_bascule = _build_before_after_bascule(panel, summary)
    if not q1_negative_price_explainability.empty:
        invalid_share = q1_negative_price_explainability[
            pd.to_numeric(q1_negative_price_explainability["share_neg_hours_explained_union"], errors="coerce")
            > 1.000001
        ]
        for _, irow in invalid_share.iterrows():
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q1_NEG_EXPLAINABILITY_SUM_INVALID",
                    "message": (
                        f"{irow['country']}-{int(irow['year'])}: share_neg_hours_explained_union>1 "
                        f"({ _safe_float(irow.get('share_neg_hours_explained_union'), np.nan):.3f})."
                    ),
                }
            )
        bad_explain = q1_negative_price_explainability[
            pd.to_numeric(q1_negative_price_explainability["share_neg_hours_unexplained"], errors="coerce")
            > Q1_UNEXPLAINED_NEGATIVE_PRICES_MAX
        ]
        for _, erow in bad_explain.iterrows():
            checks.append(
                {
                    "status": "WARN",
                    "code": "UNEXPLAINED_NEGATIVE_PRICES",
                    "message": (
                        f"{erow['country']}-{int(erow['year'])}: share_neg_hours_unexplained="
                        f"{_safe_float(erow.get('share_neg_hours_unexplained'), np.nan):.1%} > "
                        f"{Q1_UNEXPLAINED_NEGATIVE_PRICES_MAX:.0%}."
                    ),
                }
            )
    q1_yearly_diagnostics = _build_q1_yearly_diagnostics(panel, summary, params)

    for col in ["p10_load_mw", "p10_must_run_mw", "p50_load_mw", "p50_must_run_mw"]:
        if col not in panel.columns:
            panel[col] = np.nan
    q1_ir_diagnostics = panel[["country", "year", "ir_p10", "p10_must_run_mw", "p10_load_mw", "p50_must_run_mw", "p50_load_mw"]].copy()
    q1_ir_diagnostics["ir_case_class"] = q1_ir_diagnostics.apply(_ir_case_class, axis=1)

    q1_scope_audit = _build_scope_audit(panel, hourly_by_country_year)
    q1_residual_diagnostics = _build_residual_diagnostics(panel, hourly_by_country_year)
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
        "Q1 identifie la bascule Phase 1 -> Phase 2 avec gating explicite: "
        ">=2 familles LOW_PRICE/VALUE/PHYSICAL, hors annees de crise configurees, et qualite data uniquement. "
        "Les diagnostics NEG_NOT_IN_SURPLUS restent visibles via market_physical_gap_flag mais ne bloquent pas la classification."
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
            "q1_yearly_diagnostics": q1_yearly_diagnostics,
            "q1_negative_price_explainability": q1_negative_price_explainability,
            "Q1_rule_definition": q1_rule_definition,
            "Q1_rule_application": q1_rule_application,
            "Q1_before_after_bascule": q1_before_after_bascule,
            "Q1_scope_audit": q1_scope_audit,
            "Q1_residual_diagnostics": q1_residual_diagnostics,
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
