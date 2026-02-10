"""Annual and daily metrics computation (SPEC V1)."""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

from src.constants import (
    COL_COMPLETENESS,
    COL_COUNTRY,
    COL_DATA_VERSION_HASH,
    COL_ENTSOE_CODE_USED,
    COL_EXPORTS,
    COL_FLEX_OBS,
    COL_GEN_MUST_RUN,
    COL_GEN_PRIMARY,
    COL_GEN_SOLAR,
    COL_GEN_TOTAL,
    COL_GEN_VRE,
    COL_GEN_WIND_OFF,
    COL_GEN_WIND_ON,
    COL_LOAD_NET,
    COL_LOAD_NET_MODE,
    COL_LOAD_TOTAL,
    COL_MUST_RUN_MODE,
    COL_NET_POSITION,
    COL_NRL,
    COL_NRL_PRICE_CORR,
    COL_PRICE_DA,
    COL_Q_ANY_CRITICAL_MISSING,
    COL_Q_MISSING_GENERATION,
    COL_Q_MISSING_LOAD,
    COL_Q_MISSING_NET_POSITION,
    COL_Q_MISSING_PRICE,
    COL_REGIME,
    COL_REGIME_COHERENCE,
    COL_QUALITY_FLAG,
    COL_SURPLUS,
    COL_SURPLUS_ABSORBED,
    COL_SURPLUS_UNABS,
    COL_YEAR,
    PRICE_LOW_THRESHOLD_DEFAULT,
)
from src.time_utils import expected_hours, local_peak_mask


def _safe_div(a: float, b: float) -> float:
    if b is None or b == 0 or not np.isfinite(b):
        return float("nan")
    return float(a / b)


def _weighted_capture(price: pd.Series, gen: pd.Series) -> float:
    g = pd.to_numeric(gen, errors="coerce").fillna(0.0)
    p = pd.to_numeric(price, errors="coerce")
    den = float(g.sum())
    if den <= 0:
        return float("nan")
    num = float((p * g).sum())
    return num / den


def _percentile(series: pd.Series, q: float) -> float:
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return float("nan")
    return float(s.quantile(q))


def _days_spread(price: pd.Series, timezone: str) -> tuple[int, float, float]:
    p = pd.to_numeric(price, errors="coerce")
    if p.dropna().empty:
        return 0, float("nan"), float("nan")
    idx_local = p.index.tz_convert(timezone)
    daily = pd.DataFrame({"price": p.values, "date_local": idx_local.date}).groupby("date_local")["price"].agg(
        lambda x: float(np.nanmax(x) - np.nanmin(x))
    )
    count = int((daily >= 50.0).sum())
    return count, float(daily.mean()), float(daily.max())


def _regime_coherence(df: pd.DataFrame) -> float:
    price = pd.to_numeric(df[COL_PRICE_DA], errors="coerce")
    regime = df[COL_REGIME].astype(str)
    valid = df[[COL_PRICE_DA, COL_REGIME]].dropna()
    if valid.empty:
        return float("nan")

    cond_a = (regime == "A") & (price <= PRICE_LOW_THRESHOLD_DEFAULT)
    cond_b = (regime == "B") & (price <= 30.0)
    cond_c = (regime == "C") & (price >= -50.0)
    cond_d = (regime == "D") & (price >= np.nanmedian(price))

    ok = (cond_a | cond_b | cond_c | cond_d)
    ok = ok[df[COL_PRICE_DA].notna()]
    if ok.empty:
        return float("nan")
    return float(ok.mean())


def _quality_flag(completeness: float) -> str:
    if not np.isfinite(completeness):
        return "FAIL"
    if completeness >= 0.98:
        return "OK"
    if completeness >= 0.90:
        return "WARN"
    return "FAIL"


def compute_annual_metrics(df: pd.DataFrame, country_cfg: dict[str, Any], data_version_hash: str) -> dict[str, Any]:
    timezone = country_cfg["timezone"]
    year = int(df[COL_YEAR].iloc[0])
    expected = expected_hours(year)

    price = pd.to_numeric(df[COL_PRICE_DA], errors="coerce")
    load = pd.to_numeric(df[COL_LOAD_NET], errors="coerce")

    baseload = float(price.mean()) if price.notna().any() else float("nan")
    peak_mask = local_peak_mask(df.index, timezone)
    peak_price = float(price[peak_mask].mean()) if price[peak_mask].notna().any() else float("nan")
    offpeak_price = float(price[~peak_mask].mean()) if price[~peak_mask].notna().any() else float("nan")

    wind_total = pd.to_numeric(df[COL_GEN_WIND_ON], errors="coerce").fillna(0) + pd.to_numeric(df[COL_GEN_WIND_OFF], errors="coerce").fillna(0)

    capture_pv = _weighted_capture(price, df[COL_GEN_SOLAR])
    capture_wind = _weighted_capture(price, wind_total)

    mask_cd = df[COL_REGIME].isin(["C", "D"]) & price.notna()
    ttl = float(price[mask_cd].quantile(0.95)) if int(mask_cd.sum()) >= 1 else float("nan")

    h_negative = int((price < 0).sum())
    h_below_5 = int((price <= 5).sum())
    days_spread_gt50, avg_daily_spread, max_daily_spread = _days_spread(price, timezone)

    surplus_energy = float(pd.to_numeric(df[COL_SURPLUS], errors="coerce").fillna(0).sum())
    surplus_absorbed = float(pd.to_numeric(df[COL_SURPLUS_ABSORBED], errors="coerce").fillna(0).sum())
    surplus_unabs = float(pd.to_numeric(df[COL_SURPLUS_UNABS], errors="coerce").fillna(0).sum())

    load_energy = float(pd.to_numeric(df[COL_LOAD_NET], errors="coerce").fillna(0).sum())
    gen_primary = float(pd.to_numeric(df[COL_GEN_PRIMARY], errors="coerce").fillna(0).sum())
    gen_total = float(pd.to_numeric(df[COL_GEN_TOTAL], errors="coerce").fillna(0).sum())

    sr_load = _safe_div(surplus_energy, load_energy)
    sr_gen = _safe_div(surplus_energy, gen_primary)

    far = float("nan") if surplus_energy <= 0 else _safe_div(surplus_absorbed, surplus_energy)

    p10_mr = _percentile(df[COL_GEN_MUST_RUN], 0.10)
    p10_load = _percentile(df[COL_LOAD_NET], 0.10)
    ir_p10 = _safe_div(p10_mr, p10_load)
    ir_mean = _safe_div(float(pd.to_numeric(df[COL_GEN_MUST_RUN], errors="coerce").mean()), float(load.mean()))

    capture_ratio_pv_vs_baseload = _safe_div(capture_pv, baseload)
    capture_ratio_wind_vs_baseload = _safe_div(capture_wind, baseload)
    capture_ratio_pv_vs_ttl = _safe_div(capture_pv, ttl)
    capture_ratio_wind_vs_ttl = _safe_div(capture_wind, ttl)

    gen_vre_twh = float(pd.to_numeric(df[COL_GEN_VRE], errors="coerce").fillna(0).sum()) / 1e6
    gen_primary_twh = gen_primary / 1e6
    vre_pen_gen = _safe_div(gen_vre_twh, gen_primary_twh)
    vre_pen_proxy = _safe_div(gen_vre_twh, load_energy / 1e6)

    if df[[COL_NRL, COL_PRICE_DA]].dropna().shape[0] >= 3:
        nrl_price_corr = float(pearsonr(df[[COL_NRL, COL_PRICE_DA]].dropna()[COL_NRL], df[[COL_NRL, COL_PRICE_DA]].dropna()[COL_PRICE_DA]).statistic)
    else:
        nrl_price_corr = float("nan")

    completeness = float((~df[[COL_Q_MISSING_PRICE, COL_Q_MISSING_LOAD, COL_Q_MISSING_GENERATION]].any(axis=1)).mean())

    row = {
        COL_COUNTRY: str(df[COL_COUNTRY].iloc[0]),
        COL_YEAR: year,
        "n_hours_expected": expected,
        "n_hours_with_price": int(df[COL_PRICE_DA].notna().sum()),
        "n_hours_with_load": int(df[COL_LOAD_TOTAL].notna().sum()),
        "n_hours_with_vre": int(df[COL_GEN_VRE].notna().sum()),
        "n_hours_with_must_run": int(df[COL_GEN_MUST_RUN].notna().sum()),
        "missing_share_price": float(df[COL_Q_MISSING_PRICE].mean()),
        "missing_share_load": float(df[COL_Q_MISSING_LOAD].mean()),
        "missing_share_generation": float(df[COL_Q_MISSING_GENERATION].mean()),
        "missing_share_net_position": float(df[COL_Q_MISSING_NET_POSITION].mean()),
        COL_LOAD_NET_MODE: str(df[COL_LOAD_NET_MODE].iloc[0]),
        COL_MUST_RUN_MODE: str(df[COL_MUST_RUN_MODE].iloc[0]),
        COL_ENTSOE_CODE_USED: str(df[COL_ENTSOE_CODE_USED].iloc[0]),
        COL_DATA_VERSION_HASH: data_version_hash,
        "load_total_twh": float(pd.to_numeric(df[COL_LOAD_TOTAL], errors="coerce").fillna(0).sum()) / 1e6,
        "load_net_twh": load_energy / 1e6,
        "gen_solar_twh": float(pd.to_numeric(df[COL_GEN_SOLAR], errors="coerce").fillna(0).sum()) / 1e6,
        "gen_wind_on_twh": float(pd.to_numeric(df[COL_GEN_WIND_ON], errors="coerce").fillna(0).sum()) / 1e6,
        "gen_wind_off_twh": float(pd.to_numeric(df[COL_GEN_WIND_OFF], errors="coerce").fillna(0).sum()) / 1e6,
        "gen_vre_twh": gen_vre_twh,
        "gen_primary_twh": gen_primary_twh,
        "gen_must_run_twh": float(pd.to_numeric(df[COL_GEN_MUST_RUN], errors="coerce").fillna(0).sum()) / 1e6,
        "exports_twh": float(pd.to_numeric(df[COL_EXPORTS], errors="coerce").fillna(0).sum()) / 1e6,
        "vre_penetration_pct_gen": vre_pen_gen,
        "pv_penetration_pct_gen": _safe_div(float(pd.to_numeric(df[COL_GEN_SOLAR], errors="coerce").fillna(0).sum()) / 1e6, gen_primary_twh),
        "wind_penetration_pct_gen": _safe_div((float(wind_total.sum()) / 1e6), gen_primary_twh),
        "vre_penetration_proxy": vre_pen_proxy,
        "baseload_price_eur_mwh": baseload,
        "peakload_price_eur_mwh": peak_price,
        "offpeak_price_eur_mwh": offpeak_price,
        "capture_rate_pv_eur_mwh": capture_pv,
        "capture_rate_wind_eur_mwh": capture_wind,
        "capture_ratio_pv": capture_ratio_pv_vs_baseload,
        "capture_ratio_wind": capture_ratio_wind_vs_baseload,
        "capture_price_pv_eur_mwh": capture_pv,
        "capture_price_wind_eur_mwh": capture_wind,
        "capture_ratio_pv_vs_baseload": capture_ratio_pv_vs_baseload,
        "capture_ratio_wind_vs_baseload": capture_ratio_wind_vs_baseload,
        "capture_ratio_pv_vs_ttl": capture_ratio_pv_vs_ttl,
        "capture_ratio_wind_vs_ttl": capture_ratio_wind_vs_ttl,
        "h_negative": h_negative,
        "h_negative_obs": h_negative,
        "h_below_5": h_below_5,
        "h_below_5_obs": h_below_5,
        "days_spread_50_obs": days_spread_gt50,
        "days_spread_gt50": days_spread_gt50,
        "avg_daily_spread_obs": avg_daily_spread,
        "max_daily_spread_obs": max_daily_spread,
        "surplus_twh": surplus_energy / 1e6,
        "surplus_unabsorbed_twh": surplus_unabs / 1e6,
        "sr_energy_share_load": sr_load,
        "sr_energy_share_gen": sr_gen,
        "sr_energy": sr_gen,
        "sr_hours": float((pd.to_numeric(df[COL_SURPLUS], errors="coerce") > 0).mean()),
        "far_observed": far,
        "far_energy": far,
        "ir_p10": ir_p10,
        "ir_mean": ir_mean,
        "ttl_price_based_eur_mwh": ttl,
        "ttl_eur_mwh": ttl,
        "tca_ccgt_median_eur_mwh": float("nan"),
        "tca_method": "none",
        "h_regime_a": int((df[COL_REGIME] == "A").sum()),
        "h_regime_b": int((df[COL_REGIME] == "B").sum()),
        "h_regime_c": int((df[COL_REGIME] == "C").sum()),
        "h_regime_d": int((df[COL_REGIME] == "D").sum()),
        COL_REGIME_COHERENCE: _regime_coherence(df),
        COL_NRL_PRICE_CORR: nrl_price_corr,
        COL_COMPLETENESS: completeness,
        COL_QUALITY_FLAG: _quality_flag(completeness),
    }

    return row


def compute_daily_metrics(df: pd.DataFrame, timezone: str) -> pd.DataFrame:
    p = pd.to_numeric(df[COL_PRICE_DA], errors="coerce")
    idx_local = df.index.tz_convert(timezone)

    base = pd.DataFrame(index=df.index)
    base["country"] = df[COL_COUNTRY].astype(str)
    base["date_local"] = idx_local.date
    base["price"] = p
    base["regime"] = df[COL_REGIME].astype(str)
    base["gen_vre"] = pd.to_numeric(df[COL_GEN_VRE], errors="coerce")
    base["gen_primary"] = pd.to_numeric(df[COL_GEN_PRIMARY], errors="coerce")

    grp = base.groupby(["country", "date_local"], dropna=False)
    out = grp.agg(
        daily_min_price=("price", "min"),
        daily_max_price=("price", "max"),
        daily_regime_a_hours=("regime", lambda s: int((s == "A").sum())),
        daily_regime_b_hours=("regime", lambda s: int((s == "B").sum())),
        daily_vre_mwh=("gen_vre", "sum"),
        daily_primary_mwh=("gen_primary", "sum"),
    ).reset_index()

    out["daily_spread"] = out["daily_max_price"] - out["daily_min_price"]
    out["daily_has_negative"] = out["daily_min_price"] < 0
    out["daily_has_below_5"] = out["daily_min_price"] <= 5
    out["daily_vre_share_of_gen"] = out["daily_vre_mwh"] / out["daily_primary_mwh"]
    out = out.drop(columns=["daily_vre_mwh", "daily_primary_mwh"])
    return out

