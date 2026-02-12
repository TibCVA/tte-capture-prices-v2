"""Canonical hourly/annual metrics used across Q1..Q5."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.constants import (
    COL_EXPORTS,
    COL_FLEX_OTHER,
    COL_FLEX_OBS,
    COL_GEN_MUST_RUN,
    COL_GEN_PRIMARY,
    COL_GEN_PV_ALIAS,
    COL_GEN_SOLAR,
    COL_GEN_TOTAL,
    COL_GEN_VRE,
    COL_GEN_WIND_OFF,
    COL_GEN_WIND_ON,
    COL_LOAD_NET,
    COL_LOAD_TOTAL,
    COL_NET_POSITION,
    COL_NRL,
    COL_PRICE_DA,
    COL_PSH_PUMP,
    COL_PSH_PUMP_ALIAS,
    COL_SURPLUS,
    COL_SURPLUS_ABSORBED,
)

EPS = 1e-12


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


def _safe_ratio(num: float, den: float) -> float:
    if not (np.isfinite(num) and np.isfinite(den)) or abs(den) <= EPS:
        return float("nan")
    return float(num / den)


def _coalesce_numeric(df: pd.DataFrame, candidates: list[str], index: pd.Index, default: float = np.nan) -> pd.Series:
    for col in candidates:
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
    return pd.Series(default, index=index, dtype=float)


def _weighted_price(price: pd.Series, volume: pd.Series) -> float:
    p = pd.to_numeric(price, errors="coerce")
    v = pd.to_numeric(volume, errors="coerce").fillna(0.0).clip(lower=0.0)
    den = float(v.sum())
    if den <= 0.0:
        return float("nan")
    num = float((p * v).sum())
    return num / den


def build_canonical_hourly_panel(hourly_df: pd.DataFrame) -> pd.DataFrame:
    """Return the canonical hourly panel used by all modules."""

    df = hourly_df.copy()
    index = df.index

    price = _coalesce_numeric(df, [COL_PRICE_DA, "price_eur_mwh"], index=index, default=np.nan)
    load_total = _coalesce_numeric(df, [COL_LOAD_TOTAL, "load_total_mw"], index=index, default=np.nan)
    psh_raw = _coalesce_numeric(df, [COL_PSH_PUMP, COL_PSH_PUMP_ALIAS, "psh_pumping_mw"], index=index, default=np.nan)
    psh = psh_raw.clip(lower=0.0).fillna(0.0)
    load = (load_total - psh).clip(lower=0.0)

    pv = _coalesce_numeric(df, [COL_GEN_SOLAR, COL_GEN_PV_ALIAS, "gen_pv_mw"], index=index, default=0.0).fillna(0.0).clip(lower=0.0)
    wind_on = _coalesce_numeric(df, [COL_GEN_WIND_ON], index=index, default=0.0).fillna(0.0).clip(lower=0.0)
    wind_off = _coalesce_numeric(df, [COL_GEN_WIND_OFF], index=index, default=0.0).fillna(0.0).clip(lower=0.0)
    wind = (wind_on + wind_off).clip(lower=0.0)
    vre = _coalesce_numeric(df, [COL_GEN_VRE, "gen_vre_mw"], index=index, default=np.nan)
    if vre.notna().sum() == 0:
        vre = pv + wind
    else:
        vre = vre.fillna(0.0).clip(lower=0.0)
    must_run = _coalesce_numeric(df, [COL_GEN_MUST_RUN, "must_run_mw"], index=index, default=0.0).fillna(0.0).clip(lower=0.0)

    exports_direct = _coalesce_numeric(df, [COL_EXPORTS, "exports_net_mw", "exports_mw"], index=index, default=np.nan)
    net_position = _coalesce_numeric(df, [COL_NET_POSITION, "net_position_mw"], index=index, default=np.nan)
    exports_net = exports_direct.copy()
    if exports_net.notna().sum() == 0:
        exports_net = net_position.clip(lower=0.0)
    exports_net = exports_net.fillna(0.0).clip(lower=0.0)

    imports_net = pd.Series(0.0, index=index, dtype=float)
    if net_position.notna().sum() > 0:
        imports_net = (-net_position).clip(lower=0.0).fillna(0.0)

    flex_obs = _coalesce_numeric(df, [COL_FLEX_OBS, "flex_sink_observed_mw"], index=index, default=np.nan)
    other_flex = _coalesce_numeric(df, [COL_FLEX_OTHER, "flex_sink_other_mw", "other_flex_sinks_mw"], index=index, default=np.nan)
    if other_flex.notna().sum() == 0:
        other_flex = pd.Series(0.0, index=index, dtype=float)
        if flex_obs.notna().sum() > 0:
            other_flex = (flex_obs.fillna(0.0) - exports_net - psh).clip(lower=0.0)
    else:
        other_flex = other_flex.fillna(0.0).clip(lower=0.0)

    nrl = _coalesce_numeric(df, [COL_NRL, "nrl_mw"], index=index, default=np.nan)
    if nrl.notna().sum() == 0:
        nrl = load - vre - must_run
    nrl = nrl.fillna(0.0)
    surplus = _coalesce_numeric(df, [COL_SURPLUS, "surplus_mw"], index=index, default=np.nan)
    if surplus.notna().sum() == 0:
        surplus = (-nrl).clip(lower=0.0)
    else:
        surplus = surplus.fillna(0.0).clip(lower=0.0)
    shortage = nrl.clip(lower=0.0)

    absorbed_hourly = _coalesce_numeric(df, [COL_SURPLUS_ABSORBED, "surplus_absorbed_mw"], index=index, default=np.nan)
    if absorbed_hourly.notna().sum() == 0:
        if flex_obs.notna().sum() > 0:
            absorbed_hourly = flex_obs.fillna(0.0).clip(lower=0.0)
        else:
            absorbed_hourly = np.minimum(surplus, exports_net + psh + other_flex)
    absorbed_hourly = absorbed_hourly.fillna(0.0).clip(lower=0.0)
    absorbed_hourly = np.minimum(absorbed_hourly, surplus)

    total_gen = _coalesce_numeric(df, [COL_GEN_PRIMARY, COL_GEN_TOTAL, "total_gen_mw"], index=index, default=np.nan)
    if total_gen.notna().sum() == 0:
        total_gen = (load + exports_net + psh).fillna(0.0).clip(lower=0.0)
    else:
        total_gen = total_gen.fillna(0.0).clip(lower=0.0)

    out = pd.DataFrame(
        {
            "price_eur_mwh": price,
            "load_total_mw": load_total,
            "psh_pumping_mw": psh,
            "load_mw": load,
            "gen_pv_mw": pv,
            "gen_wind_mw": wind,
            "gen_vre_mw": vre,
            "must_run_mw": must_run,
            "exports_net_mw": exports_net,
            "imports_net_mw": imports_net,
            "other_flex_sinks_mw": other_flex,
            "nrl_mw": nrl,
            "surplus_mw": surplus,
            "shortage_mw": shortage,
            "surplus_absorbed_mw": absorbed_hourly,
            "total_gen_mw": total_gen,
        },
        index=index,
    )
    return out


def compute_canonical_year_metrics(
    hourly_df: pd.DataFrame,
    *,
    country: str | None = None,
    year: int | None = None,
    scenario_id: str | None = None,
) -> dict[str, Any]:
    """Compute canonical annual metrics and return explicit denominators."""

    h = build_canonical_hourly_panel(hourly_df)
    n_hours = int(len(h))
    price = pd.to_numeric(h["price_eur_mwh"], errors="coerce")
    load = pd.to_numeric(h["load_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    load_total = pd.to_numeric(h["load_total_mw"], errors="coerce")
    psh = pd.to_numeric(h["psh_pumping_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    pv = pd.to_numeric(h["gen_pv_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    wind = pd.to_numeric(h["gen_wind_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    must_run = pd.to_numeric(h["must_run_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    exports = pd.to_numeric(h["exports_net_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    surplus = pd.to_numeric(h["surplus_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    absorbed = pd.to_numeric(h["surplus_absorbed_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    total_gen = pd.to_numeric(h["total_gen_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)

    h_negative = int((price < 0.0).sum())
    h_zero_or_negative = int((price <= 0.0).sum())
    h_below_5 = int((price < 5.0).sum())
    low_price_hours_share = _safe_ratio(float(h_below_5), float(n_hours))

    baseload = float(price.mean()) if price.notna().any() else float("nan")
    capture_price_pv = _weighted_price(price, pv)
    capture_price_wind = _weighted_price(price, wind)
    capture_ratio_pv = _safe_ratio(capture_price_pv, baseload) if np.isfinite(baseload) and baseload > 0.0 else float("nan")
    capture_ratio_wind = _safe_ratio(capture_price_wind, baseload) if np.isfinite(baseload) and baseload > 0.0 else float("nan")

    surplus_energy_mwh = float(surplus.sum())
    absorbed_energy_mwh = float(absorbed.sum())
    if surplus_energy_mwh <= 0.0:
        far_energy = 1.0
    else:
        far_energy = float(np.clip(absorbed_energy_mwh / surplus_energy_mwh, 0.0, 1.0))

    sr_hours_share = _safe_ratio(float((surplus > 0.0).sum()), float(n_hours))

    total_gen_energy_mwh = float(total_gen.sum())
    proxy_den_mwh = float(load.sum() + exports.sum() + psh.sum())
    if total_gen_energy_mwh > 0.0:
        sr_denominator_mwh = total_gen_energy_mwh
        sr_denominator_kind = "total_gen_mw"
    else:
        sr_denominator_mwh = proxy_den_mwh
        sr_denominator_kind = "load_plus_exports_plus_psh_proxy"
    sr_energy_share_gen = _safe_ratio(surplus_energy_mwh, sr_denominator_mwh)
    if np.isfinite(sr_energy_share_gen):
        sr_energy_share_gen = float(np.clip(sr_energy_share_gen, 0.0, 1.0))

    load_p10 = _safe_float(load.quantile(0.10), np.nan) if load.notna().any() else np.nan
    must_run_p10 = _safe_float(must_run.quantile(0.10), np.nan) if must_run.notna().any() else np.nan
    ir_quality_flag = "OK"
    if not np.isfinite(load_p10) or load_p10 <= 0.0:
        ir_p10 = float("nan")
        ir_quality_flag = "IR_P10_LOAD_NON_POSITIVE"
    else:
        ir_p10 = _safe_ratio(must_run_p10, load_p10)
        if np.isfinite(ir_p10):
            ir_p10 = max(0.0, float(ir_p10))

    load_energy_mwh = float(load.sum())
    exports_energy_mwh = float(exports.sum())
    psh_energy_mwh = float(psh.sum())
    must_run_energy_mwh = float(must_run.sum())
    net_demand_proxy_mwh = load_energy_mwh + exports_energy_mwh + psh_energy_mwh
    must_run_share_load = _safe_ratio(must_run_energy_mwh, load_energy_mwh)
    must_run_share_netdemand = _safe_ratio(must_run_energy_mwh, net_demand_proxy_mwh)

    quality_flags: list[str] = []
    if (psh < -EPS).any():
        quality_flags.append("INV_PSH_001")
    if load_total.notna().any():
        residual = (load_total - (load + psh)).abs()
        mask = load_total.notna()
        if bool((residual[mask] > 1e-6).any()):
            quality_flags.append("INV_LOAD_001")
    if not (0.0 - 1e-9 <= far_energy <= 1.0 + 1e-9):
        quality_flags.append("INV_FAR_RANGE")
    if np.isfinite(sr_hours_share) and not (0.0 - 1e-9 <= sr_hours_share <= 1.0 + 1e-9):
        quality_flags.append("INV_SR_HOURS_RANGE")
    if np.isfinite(sr_energy_share_gen) and not (0.0 - 1e-9 <= sr_energy_share_gen <= 1.0 + 1e-9):
        quality_flags.append("INV_SR_ENERGY_RANGE")
    if surplus_energy_mwh <= EPS and abs(far_energy - 1.0) > 1e-9:
        quality_flags.append("INV_FAR_ZERO_SURPLUS")

    out: dict[str, Any] = {
        "country": "" if country is None else str(country),
        "year": np.nan if year is None else int(year),
        "scenario_id": "" if scenario_id is None else str(scenario_id),
        "n_hours": n_hours,
        "h_negative": h_negative,
        "h_zero_or_negative": h_zero_or_negative,
        "h_below_5": h_below_5,
        "low_price_hours_share": low_price_hours_share,
        "baseload_price_eur_mwh": baseload,
        "capture_price_pv_eur_mwh": capture_price_pv,
        "capture_price_wind_eur_mwh": capture_price_wind,
        "capture_ratio_pv": capture_ratio_pv,
        "capture_ratio_wind": capture_ratio_wind,
        "sr_energy_share_gen": sr_energy_share_gen,
        "sr_hours_share": sr_hours_share,
        "far_energy": far_energy,
        "ir_p10": ir_p10,
        "must_run_share_load": must_run_share_load,
        "must_run_share_netdemand": must_run_share_netdemand,
        "load_energy_mwh": load_energy_mwh,
        "exports_energy_mwh": exports_energy_mwh,
        "psh_pumping_energy_mwh": psh_energy_mwh,
        "must_run_energy_mwh": must_run_energy_mwh,
        "net_demand_proxy_energy_mwh": net_demand_proxy_mwh,
        "surplus_energy_mwh": surplus_energy_mwh,
        "absorbed_surplus_energy_mwh": absorbed_energy_mwh,
        "sr_energy_denominator_mwh": sr_denominator_mwh,
        "sr_energy_denominator_kind": sr_denominator_kind,
        "capture_price_pv_denominator_mwh": float(pv.sum()),
        "capture_price_wind_denominator_mwh": float(wind.sum()),
        "ir_p10_load_mw": load_p10,
        "ir_p10_must_run_mw": must_run_p10,
        "ir_p10_quality_flag": ir_quality_flag,
        "canonical_quality_flags": ";".join(quality_flags),
    }
    return out


def canonical_metrics_dictionary(
    *,
    country: str,
    year: int,
    scenario_id: str,
    hourly_df: pd.DataFrame,
) -> dict[str, Any]:
    """Public helper used by Q modules for auditable per-year dictionaries."""

    return compute_canonical_year_metrics(
        hourly_df=hourly_df,
        country=country,
        year=year,
        scenario_id=scenario_id,
    )
