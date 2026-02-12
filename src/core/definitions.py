"""Canonical physical definitions for hourly/annual computations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from src.constants import (
    COL_BESS_CHARGE,
    COL_EXPORTS,
    COL_FLEX_EFFECTIVE,
    COL_FLEX_EXPORTS,
    COL_FLEX_OBS,
    COL_FLEX_OTHER,
    COL_FLEX_PSH,
    COL_GEN_BIOMASS,
    COL_GEN_COAL,
    COL_GEN_GAS,
    COL_GEN_LIGNITE,
    COL_GEN_NUCLEAR,
    COL_GEN_PRIMARY,
    COL_GEN_SOLAR,
    COL_GEN_TOTAL,
    COL_GEN_VRE,
    COL_GEN_WIND_OFF,
    COL_GEN_WIND_ON,
    COL_LOAD_NET,
    COL_LOAD_NET_MODE,
    COL_LOAD_TOTAL,
    COL_NET_POSITION,
    COL_NET_POSITION_SCORE_NEG,
    COL_NET_POSITION_SCORE_POS,
    COL_NET_POSITION_SIGN_CHOICE,
    COL_NRL,
    COL_PSH_PUMP,
    COL_PSH_PUMP_ALIAS,
    COL_PSH_PUMP_COVERAGE,
    COL_PSH_PUMP_STATUS,
    COL_SURPLUS,
    COL_SURPLUS_ABSORBED,
    COL_SURPLUS_UNABS,
)

DEFAULT_MUST_RUN_CANDIDATES = (
    "nuclear",
    "fossil_lignite",
    "fossil_hard_coal",
    "fossil_gas",
    "biomass",
    "waste",
    "geothermal",
    "hydro_ror",
)

MUST_RUN_COMPONENT_TO_COL = {
    "nuclear": COL_GEN_NUCLEAR,
    "fossil_lignite": COL_GEN_LIGNITE,
    "fossil_hard_coal": COL_GEN_COAL,
    "fossil_gas": COL_GEN_GAS,
    "biomass": COL_GEN_BIOMASS,
    "waste": "gen_waste_mw",
    "geothermal": "gen_geothermal_mw",
    "hydro_ror": "gen_hydro_ror_mw",
    # Backward-compatible aliases.
    "lignite": COL_GEN_LIGNITE,
    "coal": COL_GEN_COAL,
    "gas": COL_GEN_GAS,
}


@dataclass(frozen=True)
class MustRunFloorResult:
    observed_mw: pd.Series
    must_run_mw: pd.Series
    floor_by_component_mw: dict[str, float]
    mode: str


@dataclass(frozen=True)
class CoreBalanceResult:
    sr_energy: float
    far_energy: float
    ir: float
    p10_load_mw: float
    p10_must_run_mw: float


def _numeric_series(df: pd.DataFrame, col: str, default: float = 0.0) -> pd.Series:
    if col not in df.columns:
        return pd.Series(default, index=df.index, dtype=float)
    return pd.to_numeric(df[col], errors="coerce")


def _finite_quantile(series: pd.Series, q: float) -> float:
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return float("nan")
    return float(s.quantile(q))


def _safe_ratio(num: float, den: float) -> float:
    if not (np.isfinite(num) and np.isfinite(den)) or den == 0.0:
        return float("nan")
    return float(num / den)


def resolve_load_and_pump(
    load_total_mw: pd.Series,
    psh_pump_mw: pd.Series,
    prefer_net_of_psh_pump: bool = True,
    psh_missing_share_threshold: float = 0.05,
) -> tuple[pd.Series, pd.Series, str, dict[str, Any]]:
    """Resolve canonical load and PSH sink with explicit load-net mode."""

    load_total = pd.to_numeric(load_total_mw, errors="coerce")
    psh_raw = pd.to_numeric(psh_pump_mw, errors="coerce")
    psh_negative_input_mask = psh_raw < 0.0
    psh = psh_raw.clip(lower=0.0)
    psh_effective = psh.fillna(0.0)
    psh_coverage_share = float(psh_raw.notna().mean()) if len(psh_raw) else 0.0
    if psh_coverage_share <= 0.0:
        psh_status = "missing"
    elif psh_coverage_share >= 1.0:
        psh_status = "ok"
    else:
        psh_status = "partial"

    # Mandatory identity when PSH data exists (ok/partial):
    # load_mw = load_total_mw - psh_pumping_mw
    if prefer_net_of_psh_pump and psh_status in {"ok", "partial"}:
        load_net_raw = load_total - psh_effective
        load_net_mode = "entsoe_total_load_minus_psh_pumping"
    else:
        load_net_raw = load_total
        load_net_mode = "entsoe_total_load_no_pumping_adjust"

    load_net_clamped_mask = load_net_raw < 0.0
    load_net = load_net_raw.mask(load_net_clamped_mask, 0.0)
    diagnostics = {
        "load_net_clamped_mask": load_net_clamped_mask.fillna(False).astype(bool),
        "load_net_clamped_count": int(load_net_clamped_mask.fillna(False).sum()),
        "psh_negative_input_count": int(psh_negative_input_mask.fillna(False).sum()),
        "psh_pumping_coverage_share": psh_coverage_share,
        "psh_pumping_data_status": psh_status,
        "psh_missing_above_threshold": bool(psh_coverage_share < (1.0 - float(max(0.0, psh_missing_share_threshold)))),
    }
    return load_net, psh_effective, load_net_mode, diagnostics


def build_vre_mw(df: pd.DataFrame) -> pd.Series:
    return (
        _numeric_series(df, COL_GEN_SOLAR, 0.0).fillna(0.0)
        + _numeric_series(df, COL_GEN_WIND_ON, 0.0).fillna(0.0)
        + _numeric_series(df, COL_GEN_WIND_OFF, 0.0).fillna(0.0)
    )


def compute_must_run_floor(
    df: pd.DataFrame,
    floor_quantile: float = 0.10,
    candidate_components: list[str] | tuple[str, ...] | None = None,
    fallback_profile_mw: pd.Series | None = None,
    fallback_scale: float = 1.0,
) -> MustRunFloorResult:
    """Compute must-run from component floors, with optional historical fallback profile."""

    components = list(candidate_components or DEFAULT_MUST_RUN_CANDIDATES)
    observed = pd.Series(0.0, index=df.index, dtype=float)
    must_run = pd.Series(0.0, index=df.index, dtype=float)
    floors: dict[str, float] = {}
    used_cols: set[str] = set()

    for component in components:
        col = MUST_RUN_COMPONENT_TO_COL.get(str(component))
        if not col:
            floors[str(component)] = 0.0
            continue
        if col in used_cols:
            floors[str(component)] = 0.0
            continue
        used_cols.add(col)
        s = _numeric_series(df, col, 0.0).fillna(0.0).clip(lower=0.0)
        floor = _finite_quantile(s, floor_quantile)
        if not np.isfinite(floor):
            floor = 0.0
        floors[str(component)] = float(max(0.0, floor))
        observed = observed.add(s, fill_value=0.0)
        must_run = must_run.add(np.minimum(s, floor), fill_value=0.0)

    mode = "floor_quantile"
    if float(observed.sum()) <= 1e-9 and fallback_profile_mw is not None:
        fb = pd.to_numeric(fallback_profile_mw, errors="coerce").reindex(df.index).fillna(0.0).clip(lower=0.0)
        scale = float(max(0.0, fallback_scale))
        must_run = fb * scale
        observed = fb
        mode = "profile_from_hist_scaled"

    return MustRunFloorResult(
        observed_mw=observed.clip(lower=0.0),
        must_run_mw=must_run.clip(lower=0.0),
        floor_by_component_mw=floors,
        mode=mode,
    )


def compute_balance_metrics(
    load_mw: pd.Series,
    must_run_mw: pd.Series,
    surplus_mw: pd.Series,
    absorbed_mw: pd.Series,
    gen_primary_mw: pd.Series,
) -> CoreBalanceResult:
    load = pd.to_numeric(load_mw, errors="coerce")
    must_run = pd.to_numeric(must_run_mw, errors="coerce")
    surplus = pd.to_numeric(surplus_mw, errors="coerce").fillna(0.0).clip(lower=0.0)
    absorbed = pd.to_numeric(absorbed_mw, errors="coerce").fillna(0.0).clip(lower=0.0)
    gen_primary = pd.to_numeric(gen_primary_mw, errors="coerce").fillna(0.0)

    surplus_sum = float(surplus.sum())
    absorbed_sum = float(absorbed.sum())
    gen_primary_sum = float(gen_primary.sum())

    sr = _safe_ratio(surplus_sum, gen_primary_sum)
    if np.isfinite(sr):
        sr = float(np.clip(sr, 0.0, 1.0))

    if surplus_sum <= 0.0:
        far = 1.0
    else:
        far = float(np.clip(_safe_ratio(absorbed_sum, surplus_sum), 0.0, 1.0))

    p10_load = _finite_quantile(load, 0.10)
    p10_mr = _finite_quantile(must_run, 0.10)
    ir = _safe_ratio(p10_mr, p10_load)
    if np.isfinite(ir):
        ir = max(0.0, float(ir))

    return CoreBalanceResult(
        sr_energy=sr,
        far_energy=far,
        ir=ir,
        p10_load_mw=p10_load,
        p10_must_run_mw=p10_mr,
    )


def compute_scope_coverage_lowload(
    load_mw: pd.Series,
    must_run_mw: pd.Series,
    total_generation_mw: pd.Series,
    lowload_quantile: float = 0.20,
) -> float:
    load = pd.to_numeric(load_mw, errors="coerce")
    if not isinstance(load, pd.Series):
        load = pd.Series([load], dtype=float)
    mr = pd.to_numeric(must_run_mw, errors="coerce")
    if isinstance(mr, pd.Series):
        mr = mr.reindex(load.index)
    else:
        mr = pd.Series(float(mr), index=load.index, dtype=float)
    total = pd.to_numeric(total_generation_mw, errors="coerce")
    if isinstance(total, pd.Series):
        total = total.reindex(load.index)
    else:
        total = pd.Series(float(total), index=load.index, dtype=float)
    mr = mr.fillna(0.0).clip(lower=0.0)
    total = total.fillna(0.0).clip(lower=0.0)
    if load.dropna().empty:
        return float("nan")
    q = _finite_quantile(load, lowload_quantile)
    if not np.isfinite(q):
        return float("nan")
    mask = load <= q
    denom = float(total[mask].sum())
    if denom <= 0.0:
        return float("nan")
    cov = float(mr[mask].sum()) / denom
    return float(np.clip(cov, 0.0, 1.0))


def _resolve_export_sink(
    df: pd.DataFrame,
    surplus_raw_mw: pd.Series,
    *,
    net_position_sign_mode: str | None = None,
    net_position_positive_is_export: bool | None = None,
) -> tuple[pd.Series, str, float, float]:
    exports_raw = _numeric_series(df, COL_EXPORTS, np.nan)
    if exports_raw.notna().any():
        exports_pos = exports_raw.fillna(0.0).clip(lower=0.0)
        return exports_pos, "exports_mw_direct", float("nan"), float("nan")

    net_position = _numeric_series(df, COL_NET_POSITION, 0.0).fillna(0.0)
    candidate_export_pos = net_position.clip(lower=0.0)
    candidate_export_neg = (-net_position).clip(lower=0.0)
    score_pos = float(np.minimum(candidate_export_pos, surplus_raw_mw).sum())
    score_neg = float(np.minimum(candidate_export_neg, surplus_raw_mw).sum())

    mode = (str(net_position_sign_mode or "auto").strip().lower() if net_position_sign_mode is not None else "auto")
    if net_position_positive_is_export is not None:
        mode = "positive_is_export" if bool(net_position_positive_is_export) else "negative_is_export"

    if mode in {"positive", "positive_is_export", "pos"}:
        return candidate_export_pos, "positive_is_export", score_pos, score_neg
    if mode in {"negative", "negative_is_export", "neg"}:
        return candidate_export_neg, "negative_is_export", score_pos, score_neg
    if score_pos >= score_neg:
        return candidate_export_pos, "positive_is_export", score_pos, score_neg
    return candidate_export_neg, "negative_is_export", score_pos, score_neg


def compute_core_hourly_definitions(
    df: pd.DataFrame,
    *,
    prefer_net_of_psh_pump: bool = True,
    psh_missing_share_threshold: float = 0.05,
    net_position_sign_mode: str | None = "auto",
    net_position_positive_is_export: bool | None = None,
    use_psh_pumping: bool = True,
    must_run_floor_quantile: float = 0.10,
    must_run_candidates: list[str] | tuple[str, ...] | None = None,
    fallback_must_run_profile_mw: pd.Series | None = None,
    fallback_must_run_scale: float = 1.0,
) -> dict[str, Any]:
    """Compute canonical load/VRE/must-run/NRL/surplus/flex definitions on an hourly panel."""

    load_total = _numeric_series(df, COL_LOAD_TOTAL, np.nan)
    if bool(use_psh_pumping) and COL_PSH_PUMP in df.columns:
        psh_pump_raw = _numeric_series(df, COL_PSH_PUMP, np.nan)
    elif bool(use_psh_pumping) and COL_PSH_PUMP_ALIAS in df.columns:
        psh_pump_raw = _numeric_series(df, COL_PSH_PUMP_ALIAS, np.nan)
    else:
        psh_pump_raw = pd.Series(np.nan, index=df.index, dtype=float)

    load_mw, psh_pump_effective, load_mode, load_psh_diag = resolve_load_and_pump(
        load_total_mw=load_total,
        psh_pump_mw=psh_pump_raw,
        prefer_net_of_psh_pump=prefer_net_of_psh_pump,
        psh_missing_share_threshold=psh_missing_share_threshold,
    )
    psh_coverage_share = float(_safe_ratio(float(psh_pump_raw.notna().sum()), float(len(psh_pump_raw)))) if len(psh_pump_raw) else 0.0
    psh_status = str(load_psh_diag.get("psh_pumping_data_status", "missing"))

    vre_mw = build_vre_mw(df).clip(lower=0.0)
    must_run = compute_must_run_floor(
        df=df,
        floor_quantile=must_run_floor_quantile,
        candidate_components=must_run_candidates,
        fallback_profile_mw=fallback_must_run_profile_mw,
        fallback_scale=fallback_must_run_scale,
    )

    nrl_mw = load_mw - vre_mw - must_run.must_run_mw
    surplus_raw_mw = (-nrl_mw).clip(lower=0.0).fillna(0.0)
    export_sink_mw, net_position_sign_choice, score_pos, score_neg = _resolve_export_sink(
        df=df,
        surplus_raw_mw=surplus_raw_mw,
        net_position_sign_mode=net_position_sign_mode,
        net_position_positive_is_export=net_position_positive_is_export,
    )
    psh_pumping_mw = psh_pump_effective.fillna(0.0).clip(lower=0.0)

    flex_obs_raw = _numeric_series(df, COL_FLEX_OBS, np.nan)
    if flex_obs_raw.notna().any():
        other_flex_sink_mw = (
            flex_obs_raw.fillna(0.0).clip(lower=0.0) - export_sink_mw - psh_pumping_mw
        ).clip(lower=0.0)
    else:
        other_flex_sink_mw = pd.Series(0.0, index=df.index, dtype=float)

    sink_non_bess_mw = (export_sink_mw + psh_pumping_mw + other_flex_sink_mw).clip(lower=0.0)
    absorbed_non_bess_mw = np.minimum(surplus_raw_mw, sink_non_bess_mw)
    unabsorbed_surplus_mw = (surplus_raw_mw - absorbed_non_bess_mw).clip(lower=0.0)

    ratio_denom = sink_non_bess_mw.replace(0.0, np.nan)
    export_absorb_mw = (absorbed_non_bess_mw * (export_sink_mw / ratio_denom)).fillna(0.0).clip(lower=0.0)
    psh_absorb_mw = (absorbed_non_bess_mw * (psh_pumping_mw / ratio_denom)).fillna(0.0).clip(lower=0.0)
    other_absorb_mw = (absorbed_non_bess_mw * (other_flex_sink_mw / ratio_denom)).fillna(0.0).clip(lower=0.0)

    # Keep explicit non-BESS sinks in observed flex; BESS dispatch is handled by Q4/phase2 layers.
    flex_obs = absorbed_non_bess_mw.clip(lower=0.0)
    flex_sinks = sink_non_bess_mw

    if COL_GEN_PRIMARY in df.columns:
        gen_primary_mw = _numeric_series(df, COL_GEN_PRIMARY, 0.0).fillna(0.0).clip(lower=0.0)
    else:
        gen_primary_mw = _numeric_series(df, COL_GEN_TOTAL, 0.0).fillna(0.0).clip(lower=0.0)

    balances = compute_balance_metrics(
        load_mw=load_mw,
        must_run_mw=must_run.must_run_mw,
        surplus_mw=surplus_raw_mw,
        absorbed_mw=absorbed_non_bess_mw,
        gen_primary_mw=gen_primary_mw,
    )
    scope_cov = compute_scope_coverage_lowload(
        load_mw=load_mw,
        must_run_mw=must_run.must_run_mw,
        total_generation_mw=_numeric_series(df, COL_GEN_TOTAL, 0.0).fillna(0.0).clip(lower=0.0),
    )

    load_energy = float(pd.to_numeric(load_mw, errors="coerce").fillna(0.0).clip(lower=0.0).sum())
    surplus_energy = float(pd.to_numeric(surplus_raw_mw, errors="coerce").fillna(0.0).clip(lower=0.0).sum())
    unabsorbed_energy = float(pd.to_numeric(unabsorbed_surplus_mw, errors="coerce").fillna(0.0).clip(lower=0.0).sum())
    sr_energy_share_load = float(np.clip(_safe_ratio(unabsorbed_energy, load_energy), 0.0, 1.0)) if load_energy > 0.0 else np.nan
    sr_hours_share_unabsorbed = float(np.clip((pd.to_numeric(unabsorbed_surplus_mw, errors="coerce").fillna(0.0) > 0.0).mean(), 0.0, 1.0))
    far_energy_from_unabsorbed = (
        1.0
        if surplus_energy <= 0.0
        else float(np.clip(1.0 - (unabsorbed_energy / max(surplus_energy, 1e-12)), 0.0, 1.0))
    )

    return {
        COL_LOAD_NET: load_mw,
        COL_LOAD_NET_MODE: load_mode,
        COL_PSH_PUMP: psh_pump_effective,
        COL_PSH_PUMP_COVERAGE: psh_coverage_share,
        COL_PSH_PUMP_STATUS: psh_status,
        COL_GEN_VRE: vre_mw,
        "must_run_observed_mw": must_run.observed_mw,
        "must_run_floor_by_component_mw": must_run.floor_by_component_mw,
        "must_run_mode": must_run.mode,
        "must_run_mw": must_run.must_run_mw,
        COL_NRL: nrl_mw,
        COL_SURPLUS: surplus_raw_mw,
        COL_EXPORTS: export_sink_mw,
        COL_FLEX_EXPORTS: export_absorb_mw,
        COL_FLEX_PSH: psh_absorb_mw,
        COL_FLEX_OTHER: other_absorb_mw,
        COL_FLEX_OBS: flex_obs,
        COL_FLEX_EFFECTIVE: flex_sinks,
        "surplus_raw_mw": surplus_raw_mw,
        "export_sink_mw": export_sink_mw,
        "psh_pumping_mw": psh_pumping_mw,
        "sink_non_bess_mw": sink_non_bess_mw,
        "export_absorption_mw": export_absorb_mw,
        "psh_absorption_mw": psh_absorb_mw,
        "other_flex_absorption_mw": other_absorb_mw,
        "flex_sinks_mw": flex_sinks,
        COL_SURPLUS_ABSORBED: pd.Series(absorbed_non_bess_mw, index=df.index, dtype=float),
        COL_SURPLUS_UNABS: pd.Series(unabsorbed_surplus_mw, index=df.index, dtype=float),
        "sr_energy": balances.sr_energy,
        "far_energy": balances.far_energy,
        "sr_energy_share_load": sr_energy_share_load,
        "sr_hours_share_unabsorbed": sr_hours_share_unabsorbed,
        "far_energy_from_unabsorbed": far_energy_from_unabsorbed,
        "ir_p10": balances.ir,
        "p10_load_mw": balances.p10_load_mw,
        "p10_must_run_mw": balances.p10_must_run_mw,
        "must_run_scope_coverage": scope_cov,
        "export_sign_convention": f"net_position_mw_{net_position_sign_choice}",
        COL_NET_POSITION_SIGN_CHOICE: net_position_sign_choice,
        COL_NET_POSITION_SCORE_POS: score_pos,
        COL_NET_POSITION_SCORE_NEG: score_neg,
        "load_net_clamped_mask": load_psh_diag["load_net_clamped_mask"],
        "load_net_clamped_count": load_psh_diag["load_net_clamped_count"],
        "psh_negative_input_count": load_psh_diag["psh_negative_input_count"],
    }


def sanity_check_core_definitions(df: pd.DataFrame, far_energy: float, sr_energy: float, ir: float) -> list[str]:
    """Runtime sanity checks for canonical definitions."""

    issues: list[str] = []
    tol = 1e-8

    def _series(name: str) -> pd.Series:
        if name in df.columns:
            raw = df[name]
        else:
            raw = pd.Series(np.nan, index=df.index, dtype=float)
        return pd.to_numeric(raw, errors="coerce")

    if np.isfinite(far_energy) and not (-tol <= float(far_energy) <= 1.0 + tol):
        issues.append("FAR outside [0,1]")
    if np.isfinite(sr_energy) and not (-tol <= float(sr_energy) <= 1.0 + tol):
        issues.append("SR outside [0,1]")
    if np.isfinite(ir) and float(ir) < -tol:
        issues.append("IR negative")

    surplus = _series(COL_SURPLUS).fillna(0.0)
    absorbed = _series(COL_SURPLUS_ABSORBED).fillna(0.0)
    unabs = _series(COL_SURPLUS_UNABS).fillna(0.0)
    flex_exports_raw = _series(COL_FLEX_EXPORTS)
    flex_psh_raw = _series(COL_FLEX_PSH)
    flex_other_raw = _series(COL_FLEX_OTHER)
    flex_total_raw = _series(COL_FLEX_OBS)
    flex_exports = flex_exports_raw.fillna(0.0).clip(lower=0.0)
    flex_psh = flex_psh_raw.fillna(0.0).clip(lower=0.0)
    flex_other = flex_other_raw.fillna(0.0).clip(lower=0.0)
    flex_total = flex_total_raw.fillna(0.0).clip(lower=0.0)
    mr = _series("gen_must_run_mw")
    load = _series(COL_LOAD_NET)
    load_total = _series(COL_LOAD_TOTAL)
    exports = _series(COL_EXPORTS).fillna(0.0).clip(lower=0.0)
    psh_raw = _series(COL_PSH_PUMP)
    psh = psh_raw.fillna(0.0).clip(lower=0.0)
    curtailment_proxy = _series(COL_SURPLUS_UNABS).fillna(0.0).clip(lower=0.0)
    total_gen = _series(COL_GEN_TOTAL)

    if ((absorbed - surplus) > tol).any():
        issues.append("absorbed_mw > surplus_mw")
    if (unabs < -tol).any():
        issues.append("unabsorbed_mw < 0")
    if ((absorbed + unabs - surplus).abs() > 1e-6).any():
        issues.append("INV_SURPLUS_001: surplus_mw != absorbed_mw + unabsorbed_mw")
    if ((flex_total - absorbed).abs() > 1e-6).any():
        issues.append("INV_FLEX_001: flex_sink_observed_mw != surplus_absorbed_mw")
    if ((flex_exports + flex_psh + flex_other - flex_total).abs() > 1e-6).any():
        issues.append("INV_FLEX_002: flex components do not sum to flex total")
    if flex_exports_raw.notna().any() and (flex_exports_raw < -tol).any():
        issues.append("INV_FLEX_003: flex_sink_exports_mw < 0")
    if flex_psh_raw.notna().any() and (flex_psh_raw < -tol).any():
        issues.append("INV_FLEX_004: flex_sink_psh_pump_mw < 0")
    if flex_total_raw.notna().any() and (flex_total_raw < -tol).any():
        issues.append("INV_FLEX_005: flex_sink_observed_mw < 0")

    if total_gen.notna().any() and mr.notna().any() and ((mr - total_gen) > tol).any():
        issues.append("must_run_mw > total_generation_mw")

    rhs = load.fillna(0.0) + exports + psh + curtailment_proxy
    if mr.notna().any() and ((mr.fillna(0.0) - rhs) > tol).any():
        issues.append("must_run_mw exceeds load+exports+psh+curtailment_proxy")

    if load.notna().any() and (load < -tol).any():
        issues.append("INV_LOAD_002: load_mw < 0")

    if psh_raw.notna().any() and (psh_raw < -tol).any():
        issues.append("INV_PSH_001: psh_pump_mw < 0")

    inv_load_mask = load_total.notna() & load.notna() & psh.notna() & (psh > tol)
    if bool(inv_load_mask.any()):
        inv_load_residual = (load_total - (load + psh)).abs()
        if (inv_load_residual[inv_load_mask] > 1e-6).any():
            issues.append("INV_LOAD_001: load_total_mw != load_mw + psh_pump_mw (hourly)")

    if load_total.notna().any():
        # Annual energy identity check against PSH de-netting.
        lhs = float(load_total.fillna(0.0).sum())
        rhs_energy = float(load.fillna(0.0).sum() + psh.fillna(0.0).sum())
        tol_energy = max(1e-6, 0.001 * abs(lhs))
        if abs(lhs - rhs_energy) > tol_energy:
            issues.append("load_total_mw != load_mw + psh_pump_mw (energy)")

    surplus_sum = float(surplus.sum())
    unabs_sum = float(unabs.sum())
    if surplus_sum <= tol:
        if np.isfinite(far_energy) and abs(float(far_energy) - 1.0) > 1e-6:
            issues.append("FAR must equal 1 when surplus is zero")
        if unabs_sum > tol:
            issues.append("unabsorbed energy must be zero when surplus is zero")
    elif np.isfinite(far_energy) and abs(float(far_energy) - 1.0) <= 1e-6:
        load_sum = float(load.fillna(0.0).clip(lower=0.0).sum())
        tol_unabs = max(1e-9, 1e-6 * max(load_sum, 1.0))
        if unabs_sum > tol_unabs:
            issues.append("FAR~1 but unabsorbed energy is not near zero")

    return issues
