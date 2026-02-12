"""Annual and daily metrics computation (SPEC V1)."""

from __future__ import annotations

import json
import math
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

from src.conventions import clip01, to_pct
from src.constants import (
    COL_COMPLETENESS,
    COL_COUNTRY,
    COL_DATA_VERSION_HASH,
    COL_ENTSOE_CODE_USED,
    COL_EXPORTS,
    COL_FLEX_EXPORTS,
    COL_FLEX_OTHER,
    COL_FLEX_OBS,
    COL_FLEX_PSH,
    COL_GEN_BIOMASS,
    COL_GEN_HYDRO_ROR,
    COL_GEN_MUST_RUN,
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
    COL_LOW_RESIDUAL_HOUR,
    COL_LOW_RESIDUAL_THRESHOLD,
    COL_MUST_RUN_MODE,
    COL_NET_POSITION,
    COL_NET_POSITION_SCORE_NEG,
    COL_NET_POSITION_SCORE_POS,
    COL_NET_POSITION_SIGN_CHOICE,
    COL_NRL,
    COL_NRL_PRICE_CORR,
    COL_PRICE_DA,
    COL_PSH_PUMP,
    COL_PSH_PUMP_COVERAGE,
    COL_PSH_PUMP_STATUS,
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
from src.core.canonical_metrics import build_canonical_hourly_panel, compute_canonical_year_metrics
from src.core.definitions import compute_balance_metrics, compute_scope_coverage_lowload, sanity_check_core_definitions
from src.time_utils import expected_hours, local_peak_mask


def _safe_div(a: float, b: float) -> float:
    if b is None or b == 0 or not np.isfinite(b):
        return float("nan")
    return float(a / b)


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


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
    scenario_id = (
        str(df.get("scenario_id", pd.Series(["HIST"])).iloc[0]).strip()
        if "scenario_id" in df.columns
        else "HIST"
    )
    if scenario_id == "":
        scenario_id = "HIST"
    expected = expected_hours(year)

    canonical_hourly = build_canonical_hourly_panel(df)
    canonical_metrics = compute_canonical_year_metrics(
        hourly_df=df,
        country=str(df[COL_COUNTRY].iloc[0]),
        year=year,
        scenario_id=scenario_id,
    )

    price = pd.to_numeric(canonical_hourly["price_eur_mwh"], errors="coerce")
    load = pd.to_numeric(canonical_hourly["load_mw"], errors="coerce")

    baseload = _safe_float(canonical_metrics.get("baseload_price_eur_mwh"), np.nan)
    peak_mask = local_peak_mask(df.index, timezone)
    peak_price = float(price[peak_mask].mean()) if price[peak_mask].notna().any() else float("nan")
    offpeak_price = float(price[~peak_mask].mean()) if price[~peak_mask].notna().any() else float("nan")

    wind_total = pd.to_numeric(canonical_hourly["gen_wind_mw"], errors="coerce").fillna(0)

    capture_pv = _safe_float(canonical_metrics.get("capture_price_pv_eur_mwh"), np.nan)
    capture_wind = _safe_float(canonical_metrics.get("capture_price_wind_eur_mwh"), np.nan)

    mask_cd = df[COL_REGIME].isin(["C", "D"]) & price.notna()
    ttl = float(price[mask_cd].quantile(0.95)) if int(mask_cd.sum()) >= 1 else float("nan")

    h_negative = int(_safe_float(canonical_metrics.get("h_negative"), 0.0))
    h_below_5 = int(_safe_float(canonical_metrics.get("h_below_5"), 0.0))
    h_zero_or_negative = int(_safe_float(canonical_metrics.get("h_zero_or_negative"), 0.0))
    low_price_hours_share = _safe_float(canonical_metrics.get("low_price_hours_share"), np.nan)
    days_spread_gt50, avg_daily_spread, max_daily_spread = _days_spread(price, timezone)

    regime = df[COL_REGIME].astype(str) if COL_REGIME in df.columns else pd.Series(index=df.index, dtype=object)
    neg_mask = price < 0
    neg_count = int(neg_mask.sum())
    neg_ab_count = int((neg_mask & regime.isin(["A", "B"])).sum()) if neg_count > 0 else 0
    low_residual_flag = (
        pd.to_numeric(df[COL_LOW_RESIDUAL_HOUR], errors="coerce").fillna(0.0) > 0
        if COL_LOW_RESIDUAL_HOUR in df.columns
        else pd.Series(False, index=df.index)
    )
    neg_low_residual_count = int((neg_mask & low_residual_flag).sum()) if neg_count > 0 else 0
    neg_ab_or_low_residual_count = int((neg_mask & (regime.isin(["A", "B"]) | low_residual_flag)).sum()) if neg_count > 0 else 0
    share_neg_price_hours_in_ab = _safe_div(float(neg_ab_count), float(neg_count)) if neg_count > 0 else float("nan")
    share_neg_price_hours_in_low_residual = _safe_div(float(neg_low_residual_count), float(neg_count)) if neg_count > 0 else float("nan")
    share_neg_price_hours_in_ab_or_low_residual = (
        _safe_div(float(neg_ab_or_low_residual_count), float(neg_count)) if neg_count > 0 else float("nan")
    )

    nrl_series = pd.to_numeric(df[COL_NRL], errors="coerce")
    residual_p10 = _percentile(nrl_series, 0.10)
    residual_p50 = _percentile(nrl_series, 0.50)
    residual_p90 = _percentile(nrl_series, 0.90)
    low_residual_share = float(low_residual_flag.mean()) if len(low_residual_flag) else float("nan")
    low_residual_threshold_mw = _safe_float(
        pd.to_numeric(df[COL_LOW_RESIDUAL_THRESHOLD], errors="coerce").dropna().iloc[0],
        np.nan,
    ) if COL_LOW_RESIDUAL_THRESHOLD in df.columns and pd.to_numeric(df[COL_LOW_RESIDUAL_THRESHOLD], errors="coerce").notna().any() else np.nan
    price_low_residual_median = _safe_float(price[low_residual_flag].median(), np.nan) if bool(low_residual_flag.any()) else np.nan
    price_negative_median = _safe_float(price[neg_mask].median(), np.nan) if neg_count > 0 else np.nan
    residual_negative_p50 = _safe_float(nrl_series[neg_mask].median(), np.nan) if neg_count > 0 else np.nan

    surplus_energy = _safe_float(canonical_metrics.get("surplus_energy_mwh"), 0.0)
    surplus_absorbed = float(pd.to_numeric(df.get(COL_SURPLUS_ABSORBED), errors="coerce").fillna(0.0).clip(lower=0.0).sum())
    surplus_unabs = float(pd.to_numeric(df[COL_SURPLUS_UNABS], errors="coerce").fillna(0).clip(lower=0.0).sum())
    psh_pumping_mwh = _safe_float(canonical_metrics.get("psh_pumping_energy_mwh"), 0.0)
    flex_sink_exports_mwh = float(
        pd.to_numeric(df.get(COL_FLEX_EXPORTS, df.get(COL_EXPORTS)), errors="coerce").fillna(0.0).clip(lower=0.0).sum()
    )
    flex_sink_psh_mwh = float(
        pd.to_numeric(df.get(COL_FLEX_PSH, df.get(COL_PSH_PUMP)), errors="coerce").fillna(0.0).clip(lower=0.0).sum()
    )
    flex_sink_other_mwh = float(
        pd.to_numeric(df.get(COL_FLEX_OTHER), errors="coerce").fillna(0.0).clip(lower=0.0).sum()
    )
    flex_sink_total_mwh = float(pd.to_numeric(df.get(COL_FLEX_OBS), errors="coerce").fillna(0.0).clip(lower=0.0).sum())
    psh_pumping_coverage_share = _safe_float(
        pd.to_numeric(df.get(COL_PSH_PUMP_COVERAGE), errors="coerce").dropna().iloc[0],
        np.nan,
    ) if COL_PSH_PUMP_COVERAGE in df.columns and pd.to_numeric(df.get(COL_PSH_PUMP_COVERAGE), errors="coerce").notna().any() else np.nan
    psh_pumping_data_status = (
        str(df[COL_PSH_PUMP_STATUS].dropna().iloc[0])
        if COL_PSH_PUMP_STATUS in df.columns and df[COL_PSH_PUMP_STATUS].notna().any()
        else "missing"
    )
    net_position_sign_choice = (
        str(df[COL_NET_POSITION_SIGN_CHOICE].dropna().iloc[0])
        if COL_NET_POSITION_SIGN_CHOICE in df.columns and df[COL_NET_POSITION_SIGN_CHOICE].notna().any()
        else "unknown"
    )
    net_position_score_pos = _safe_float(
        pd.to_numeric(df.get(COL_NET_POSITION_SCORE_POS), errors="coerce").dropna().iloc[0],
        np.nan,
    ) if COL_NET_POSITION_SCORE_POS in df.columns and pd.to_numeric(df.get(COL_NET_POSITION_SCORE_POS), errors="coerce").notna().any() else np.nan
    net_position_score_neg = _safe_float(
        pd.to_numeric(df.get(COL_NET_POSITION_SCORE_NEG), errors="coerce").dropna().iloc[0],
        np.nan,
    ) if COL_NET_POSITION_SCORE_NEG in df.columns and pd.to_numeric(df.get(COL_NET_POSITION_SCORE_NEG), errors="coerce").notna().any() else np.nan
    load_total_series = pd.to_numeric(df[COL_LOAD_TOTAL], errors="coerce")
    load_net_series = pd.to_numeric(df[COL_LOAD_NET], errors="coerce")
    psh_series = pd.to_numeric(df.get(COL_PSH_PUMP), errors="coerce")
    load_identity_residual = load_total_series - (load_net_series + psh_series)
    identity_mask = load_total_series.notna() & load_net_series.notna() & psh_series.notna()
    if bool(identity_mask.any()):
        load_identity_abs_max_mw = float(load_identity_residual[identity_mask].abs().max())
        denom = load_total_series[identity_mask].abs().replace(0.0, np.nan)
        load_identity_rel_err = float((load_identity_residual[identity_mask].abs() / denom).max())
    else:
        load_identity_abs_max_mw = float("nan")
        load_identity_rel_err = float("nan")
    load_identity_ok = bool(np.isfinite(load_identity_rel_err) and load_identity_rel_err <= 1e-3)

    load_energy = _safe_float(canonical_metrics.get("load_energy_mwh"), 0.0)
    gen_primary_series = pd.to_numeric(df[COL_GEN_PRIMARY], errors="coerce") if COL_GEN_PRIMARY in df.columns else pd.Series(0.0, index=df.index, dtype=float)
    if gen_primary_series.notna().sum() == 0:
        gen_primary_series = pd.to_numeric(df[COL_GEN_TOTAL], errors="coerce")
    gen_primary = float(gen_primary_series.fillna(0.0).clip(lower=0.0).sum())
    gen_total = float(pd.to_numeric(df[COL_GEN_TOTAL], errors="coerce").fillna(0).clip(lower=0.0).sum())

    sr_load = _safe_div(surplus_energy, load_energy)
    sr_gen = _safe_float(canonical_metrics.get("sr_energy_share_gen"), np.nan)
    far = _safe_float(canonical_metrics.get("far_energy"), np.nan)

    balance = compute_balance_metrics(
        load_mw=df[COL_LOAD_NET],
        must_run_mw=df[COL_GEN_MUST_RUN],
        surplus_mw=df[COL_SURPLUS],
        absorbed_mw=df[COL_SURPLUS_ABSORBED],
        gen_primary_mw=gen_primary_series,
    )

    p10_mr = _safe_float(canonical_metrics.get("ir_p10_must_run_mw"), balance.p10_must_run_mw)
    p10_load = _safe_float(canonical_metrics.get("ir_p10_load_mw"), balance.p10_load_mw)
    p50_mr = _percentile(df[COL_GEN_MUST_RUN], 0.50)
    p50_load = _percentile(df[COL_LOAD_NET], 0.50)
    ir_p10 = _safe_float(canonical_metrics.get("ir_p10"), balance.ir)
    ir_p10_excess = float(ir_p10 - 1.0) if np.isfinite(ir_p10) else float("nan")
    ir_mean = _safe_div(float(pd.to_numeric(df[COL_GEN_MUST_RUN], errors="coerce").mean()), float(load.mean()))
    must_run_share_load = _safe_float(canonical_metrics.get("must_run_share_load"), np.nan)
    must_run_share_netdemand = _safe_float(canonical_metrics.get("must_run_share_netdemand"), np.nan)

    capture_ratio_pv_vs_baseload = _safe_float(canonical_metrics.get("capture_ratio_pv"), np.nan)
    capture_ratio_wind_vs_baseload = _safe_float(canonical_metrics.get("capture_ratio_wind"), np.nan)
    capture_ratio_pv_vs_ttl = _safe_div(capture_pv, ttl)
    capture_ratio_wind_vs_ttl = _safe_div(capture_wind, ttl)

    gen_vre_twh = float(pd.to_numeric(df[COL_GEN_VRE], errors="coerce").fillna(0).sum()) / 1e6
    gen_primary_twh = gen_primary / 1e6
    pv_twh = float(pd.to_numeric(df[COL_GEN_SOLAR], errors="coerce").fillna(0).sum()) / 1e6
    wind_twh = float(wind_total.sum()) / 1e6
    vre_pen_share = _safe_div(gen_vre_twh, gen_primary_twh)
    pv_pen_share = _safe_div(pv_twh, gen_primary_twh)
    wind_pen_share = _safe_div(wind_twh, gen_primary_twh)
    vre_pen_proxy = _safe_div(gen_vre_twh, load_energy / 1e6)

    if df[[COL_NRL, COL_PRICE_DA]].dropna().shape[0] >= 3:
        nrl_price_corr = float(pearsonr(df[[COL_NRL, COL_PRICE_DA]].dropna()[COL_NRL], df[[COL_NRL, COL_PRICE_DA]].dropna()[COL_PRICE_DA]).statistic)
    else:
        nrl_price_corr = float("nan")

    n_hours_with_price = int(df[COL_PRICE_DA].notna().sum())
    n_hours_with_load = int(df[COL_LOAD_TOTAL].notna().sum())
    n_hours_with_vre = int(df[COL_GEN_VRE].notna().sum())
    n_hours_with_must_run = int(df[COL_GEN_MUST_RUN].notna().sum())
    n_hours_with_pv = int(pd.to_numeric(df.get(COL_GEN_SOLAR), errors="coerce").notna().sum())
    wind_on_cov = pd.to_numeric(df.get(COL_GEN_WIND_ON), errors="coerce")
    wind_off_cov = pd.to_numeric(df.get(COL_GEN_WIND_OFF), errors="coerce")
    n_hours_with_wind = int((wind_on_cov.notna() | wind_off_cov.notna()).sum())
    n_hours_with_nuclear = int(pd.to_numeric(df.get(COL_GEN_NUCLEAR), errors="coerce").notna().sum())
    n_hours_with_biomass = int(pd.to_numeric(df.get(COL_GEN_BIOMASS), errors="coerce").notna().sum())
    n_hours_with_ror = int(pd.to_numeric(df.get(COL_GEN_HYDRO_ROR), errors="coerce").notna().sum())

    coverage_price = _safe_div(float(n_hours_with_price), float(expected))
    coverage_load_total = _safe_div(float(n_hours_with_load), float(expected))
    coverage_vre = _safe_div(float(n_hours_with_vre), float(expected))
    coverage_must_run = _safe_div(float(n_hours_with_must_run), float(expected))
    coverage_pv = _safe_div(float(n_hours_with_pv), float(expected))
    coverage_wind = _safe_div(float(n_hours_with_wind), float(expected))
    coverage_nuclear = _safe_div(float(n_hours_with_nuclear), float(expected))
    coverage_biomass = _safe_div(float(n_hours_with_biomass), float(expected))
    coverage_ror = _safe_div(float(n_hours_with_ror), float(expected))
    coverage_net_position = 1.0 - float(df[COL_Q_MISSING_NET_POSITION].mean())

    load_total_mw_avg = _safe_float(load_total_series.mean(), np.nan)
    psh_pumping_mw_avg = _safe_float(psh_series.mean(), np.nan)
    load_mw_avg = _safe_float(load.mean(), np.nan)
    gen_vre_mw_avg = _safe_float(pd.to_numeric(df[COL_GEN_VRE], errors="coerce").mean(), np.nan)
    pv_mw_avg = _safe_float(pd.to_numeric(df[COL_GEN_SOLAR], errors="coerce").mean(), np.nan)
    wind_on_mw_avg = _safe_float(pd.to_numeric(df[COL_GEN_WIND_ON], errors="coerce").mean(), np.nan)
    wind_off_mw_avg = _safe_float(pd.to_numeric(df[COL_GEN_WIND_OFF], errors="coerce").mean(), np.nan)
    must_run_mw_avg = _safe_float(pd.to_numeric(df[COL_GEN_MUST_RUN], errors="coerce").mean(), np.nan)
    must_run_nuclear_mw_avg = _safe_float(pd.to_numeric(df.get(COL_GEN_NUCLEAR), errors="coerce").mean(), np.nan)
    must_run_biomass_mw_avg = _safe_float(pd.to_numeric(df.get(COL_GEN_BIOMASS), errors="coerce").mean(), np.nan)
    must_run_ror_mw_avg = _safe_float(pd.to_numeric(df.get(COL_GEN_HYDRO_ROR), errors="coerce").mean(), np.nan)
    nrl_mw_avg = _safe_float(pd.to_numeric(df.get(COL_NRL), errors="coerce").mean(), np.nan)
    nrl_p10 = _percentile(pd.to_numeric(df.get(COL_NRL), errors="coerce"), 0.10)
    nrl_p50 = _percentile(pd.to_numeric(df.get(COL_NRL), errors="coerce"), 0.50)
    nrl_p90 = _percentile(pd.to_numeric(df.get(COL_NRL), errors="coerce"), 0.90)

    surplus_hours_count = int((pd.to_numeric(df[COL_SURPLUS], errors="coerce") > 0).sum())
    absorbed_hours_count = int((pd.to_numeric(df[COL_SURPLUS_ABSORBED], errors="coerce") > 0).sum())
    far_hours = _safe_div(float(absorbed_hours_count), float(surplus_hours_count)) if surplus_hours_count > 0 else 1.0
    sink_breakdown_json = json.dumps(
        {
            "exports_absorption_mwh": _safe_float(flex_sink_exports_mwh, 0.0),
            "psh_absorption_mwh": _safe_float(flex_sink_psh_mwh, 0.0),
            "other_flex_absorption_mwh": _safe_float(flex_sink_other_mwh, 0.0),
        },
        ensure_ascii=False,
    )

    core_sanity_issues = sanity_check_core_definitions(df, far_energy=far, sr_energy=sr_gen, ir=ir_p10)

    flex_identity_tol = max(1e-6, 1e-4 * max(surplus_energy, 0.0))
    flex_identity_abs_err = abs(float(flex_sink_total_mwh) - float(surplus_absorbed))
    flex_identity_ok = bool(flex_identity_abs_err <= flex_identity_tol)
    flex_components_sum = float(flex_sink_exports_mwh + flex_sink_psh_mwh + flex_sink_other_mwh)
    flex_components_abs_err = abs(flex_sink_total_mwh - flex_components_sum)
    flex_components_ok = bool(flex_components_abs_err <= flex_identity_tol)
    use_psh_pumping = bool(country_cfg.get("flex", {}).get("use_psh_pump", True)) if isinstance(country_cfg, dict) else True

    data_quality_flags: list[str] = []
    for cov_name, cov_value in [
        ("coverage_price", coverage_price),
        ("coverage_load_total", coverage_load_total),
        ("coverage_net_position", coverage_net_position),
        ("coverage_pv", coverage_pv),
        ("coverage_wind", coverage_wind),
        ("coverage_nuclear", coverage_nuclear),
        ("coverage_biomass", coverage_biomass),
        ("coverage_ror", coverage_ror),
    ]:
        if not np.isfinite(cov_value):
            data_quality_flags.append(f"{cov_name.upper()}_MISSING")
        elif cov_value < 0.95:
            data_quality_flags.append(f"{cov_name.upper()}_LOW")
    if not np.isfinite(psh_pumping_coverage_share):
        data_quality_flags.append("COVERAGE_PSH_PUMPING_MISSING")
    elif psh_pumping_coverage_share < 0.95:
        data_quality_flags.append("COVERAGE_PSH_PUMPING_LOW")
    if not load_identity_ok and np.isfinite(load_identity_rel_err):
        data_quality_flags.append("LOAD_IDENTITY_FAIL")
    if not flex_identity_ok:
        data_quality_flags.append("FLEX_IDENTITY_FAIL")
    if not flex_components_ok:
        data_quality_flags.append("FLEX_COMPONENTS_SUM_FAIL")
    if core_sanity_issues:
        data_quality_flags.append("CORE_SANITY_WARN")
    if use_psh_pumping and str(psh_pumping_data_status).lower() in {"missing", "partial"}:
        data_quality_flags.append("PSH_PUMPING_DATA_INCOMPLETE")
    if use_psh_pumping and str(psh_pumping_data_status).lower() == "missing":
        data_quality_flags.append("PSH_PUMPING_REQUIRED_BUT_MISSING")
    if (
        surplus_energy > 1e-6
        and float(pd.to_numeric(df.get(COL_EXPORTS), errors="coerce").fillna(0.0).clip(lower=0.0).sum()) > 1e-6
        and flex_sink_exports_mwh <= 1e-9
    ):
        data_quality_flags.append("EXPORT_SINK_SIGN_SUSPECT")

    completeness = float((~df[[COL_Q_MISSING_PRICE, COL_Q_MISSING_LOAD, COL_Q_MISSING_GENERATION]].any(axis=1)).mean())
    must_run_scope_coverage = compute_scope_coverage_lowload(
        load_mw=df[COL_LOAD_NET],
        must_run_mw=df[COL_GEN_MUST_RUN],
        total_generation_mw=df[COL_GEN_TOTAL],
    )
    row = {
        COL_COUNTRY: str(df[COL_COUNTRY].iloc[0]),
        COL_YEAR: year,
        "scenario_id": scenario_id,
        "n_hours_expected": expected,
        "n_hours_with_price": n_hours_with_price,
        "n_hours_with_load": n_hours_with_load,
        "n_hours_with_vre": n_hours_with_vre,
        "n_hours_with_must_run": n_hours_with_must_run,
        "n_hours_with_pv": n_hours_with_pv,
        "n_hours_with_wind": n_hours_with_wind,
        "n_hours_with_nuclear": n_hours_with_nuclear,
        "n_hours_with_biomass": n_hours_with_biomass,
        "n_hours_with_ror": n_hours_with_ror,
        "missing_share_price": float(df[COL_Q_MISSING_PRICE].mean()),
        "missing_share_load": float(df[COL_Q_MISSING_LOAD].mean()),
        "missing_share_generation": float(df[COL_Q_MISSING_GENERATION].mean()),
        "missing_share_net_position": float(df[COL_Q_MISSING_NET_POSITION].mean()),
        "coverage_price": coverage_price,
        "coverage_load_total": coverage_load_total,
        "coverage_net_position": coverage_net_position,
        "coverage_vre": coverage_vre,
        "coverage_must_run": coverage_must_run,
        "coverage_psh_pumping": psh_pumping_coverage_share,
        "coverage_pv": coverage_pv,
        "coverage_wind": coverage_wind,
        "coverage_nuclear": coverage_nuclear,
        "coverage_biomass": coverage_biomass,
        "coverage_ror": coverage_ror,
        COL_LOAD_NET_MODE: str(df[COL_LOAD_NET_MODE].iloc[0]),
        COL_MUST_RUN_MODE: str(df[COL_MUST_RUN_MODE].iloc[0]),
        "use_psh_pumping_config": use_psh_pumping,
        COL_ENTSOE_CODE_USED: str(df[COL_ENTSOE_CODE_USED].iloc[0]),
        COL_DATA_VERSION_HASH: data_version_hash,
        "load_total_twh": float(pd.to_numeric(df[COL_LOAD_TOTAL], errors="coerce").fillna(0).sum()) / 1e6,
        "load_net_twh": load_energy / 1e6,
        "load_total_mw_avg": load_total_mw_avg,
        "psh_pumping_mw_avg": psh_pumping_mw_avg,
        "load_mw_avg": load_mw_avg,
        "gen_vre_mw_avg": gen_vre_mw_avg,
        "pv_mw_avg": pv_mw_avg,
        "wind_on_mw_avg": wind_on_mw_avg,
        "wind_off_mw_avg": wind_off_mw_avg,
        "must_run_mw_avg": must_run_mw_avg,
        "must_run_nuclear_mw_avg": must_run_nuclear_mw_avg,
        "must_run_biomass_mw_avg": must_run_biomass_mw_avg,
        "must_run_ror_mw_avg": must_run_ror_mw_avg,
        "nrl_mw_avg": nrl_mw_avg,
        "nrl_p10_mw": nrl_p10,
        "nrl_p50_mw": nrl_p50,
        "nrl_p90_mw": nrl_p90,
        "psh_pumping_twh": psh_pumping_mwh / 1e6,
        "psh_pumping_coverage_share": psh_pumping_coverage_share,
        "psh_pumping_data_status": psh_pumping_data_status,
        "sink_breakdown_json": sink_breakdown_json,
        "gen_solar_twh": pv_twh,
        "gen_wind_on_twh": float(pd.to_numeric(df[COL_GEN_WIND_ON], errors="coerce").fillna(0).sum()) / 1e6,
        "gen_wind_off_twh": float(pd.to_numeric(df[COL_GEN_WIND_OFF], errors="coerce").fillna(0).sum()) / 1e6,
        "gen_vre_twh": gen_vre_twh,
        "gen_primary_twh": gen_primary_twh,
        "gen_must_run_twh": float(pd.to_numeric(df[COL_GEN_MUST_RUN], errors="coerce").fillna(0).sum()) / 1e6,
        "exports_twh": float(pd.to_numeric(df[COL_EXPORTS], errors="coerce").fillna(0).sum()) / 1e6,
        "net_position_sign_choice": net_position_sign_choice,
        "net_position_score_pos": net_position_score_pos,
        "net_position_score_neg": net_position_score_neg,
        "flex_sink_exports_twh": flex_sink_exports_mwh / 1e6,
        "flex_sink_psh_twh": flex_sink_psh_mwh / 1e6,
        "flex_sink_other_twh": flex_sink_other_mwh / 1e6,
        "flex_sink_total_twh": flex_sink_total_mwh / 1e6,
        "vre_penetration_share_gen": vre_pen_share,
        "pv_penetration_share_gen": pv_pen_share,
        "wind_penetration_share_gen": wind_pen_share,
        "vre_penetration_pct_gen": to_pct(vre_pen_share),
        "pv_penetration_pct_gen": to_pct(pv_pen_share),
        "wind_penetration_pct_gen": to_pct(wind_pen_share),
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
        "h_zero_or_negative": h_zero_or_negative,
        "h_below_5": h_below_5,
        "h_below_5_obs": h_below_5,
        "low_price_hours_share": low_price_hours_share,
        "share_neg_price_hours_in_AB": share_neg_price_hours_in_ab,
        "share_neg_price_hours_in_low_residual": share_neg_price_hours_in_low_residual,
        "share_neg_price_hours_in_AB_OR_LOW_RESIDUAL": share_neg_price_hours_in_ab_or_low_residual,
        "days_spread_50_obs": days_spread_gt50,
        "days_spread_gt50": days_spread_gt50,
        "avg_daily_spread_obs": avg_daily_spread,
        "max_daily_spread_obs": max_daily_spread,
        "surplus_twh": surplus_energy / 1e6,
        "surplus_energy_twh": surplus_energy / 1e6,
        "surplus_mwh_total": surplus_energy,
        "absorbed_surplus_twh": surplus_absorbed / 1e6,
        "unabsorbed_surplus_twh": surplus_unabs / 1e6,
        "surplus_unabsorbed_twh": surplus_unabs / 1e6,
        "sr_energy_share_load": sr_load,
        "sr_energy_share_gen": sr_gen,
        "sr_energy": sr_gen,
        "sr_hours_share": float((pd.to_numeric(df[COL_SURPLUS], errors="coerce") > 0).mean()),
        "sr_hours": float((pd.to_numeric(df[COL_SURPLUS], errors="coerce") > 0).mean()),
        "far_observed": far,
        "far_energy": far,
        "far_hours": far_hours,
        "ir_p10": ir_p10,
        "p10_load_mw": p10_load,
        "p10_must_run_mw": p10_mr,
        "p50_load_mw": p50_load,
        "p50_must_run_mw": p50_mr,
        "ir_p10_excess": ir_p10_excess,
        "ir_mean": ir_mean,
        "must_run_share_load": must_run_share_load,
        "must_run_share_netdemand": must_run_share_netdemand,
        "must_run_scope_coverage": must_run_scope_coverage,
        "sr_energy_denominator_kind": canonical_metrics.get("sr_energy_denominator_kind", ""),
        "sr_energy_denominator_mwh": _safe_float(canonical_metrics.get("sr_energy_denominator_mwh"), np.nan),
        "capture_price_pv_denominator_mwh": _safe_float(canonical_metrics.get("capture_price_pv_denominator_mwh"), np.nan),
        "capture_price_wind_denominator_mwh": _safe_float(canonical_metrics.get("capture_price_wind_denominator_mwh"), np.nan),
        "ir_p10_quality_flag": canonical_metrics.get("ir_p10_quality_flag", ""),
        "canonical_quality_flags": canonical_metrics.get("canonical_quality_flags", ""),
        "core_sanity_issue_count": int(len(core_sanity_issues)),
        "core_sanity_issues": "; ".join(core_sanity_issues),
        "ttl_price_based_eur_mwh": ttl,
        "ttl_eur_mwh": ttl,
        "ttl_observed_eur_mwh": ttl,
        "tca_ccgt_median_eur_mwh": float("nan"),
        "tca_method": "none",
        "h_regime_a": int((df[COL_REGIME] == "A").sum()),
        "h_regime_b": int((df[COL_REGIME] == "B").sum()),
        "h_regime_c": int((df[COL_REGIME] == "C").sum()),
        "h_regime_d": int((df[COL_REGIME] == "D").sum()),
        "low_residual_hours_share": low_residual_share,
        "low_residual_threshold_mw": low_residual_threshold_mw,
        "residual_load_p10_mw": residual_p10,
        "residual_load_p50_mw": residual_p50,
        "residual_load_p90_mw": residual_p90,
        "price_low_residual_median_eur_mwh": price_low_residual_median,
        "price_negative_hours_median_eur_mwh": price_negative_median,
        "residual_load_p50_on_negative_price_mw": residual_negative_p50,
        "capture_ratio_pv_vs_ttl_observed": capture_ratio_pv_vs_ttl,
        "capture_ratio_wind_vs_ttl_observed": capture_ratio_wind_vs_ttl,
        "load_identity_abs_max_mw": load_identity_abs_max_mw,
        "load_identity_rel_err": load_identity_rel_err,
        "load_identity_ok": load_identity_ok,
        "flex_identity_abs_err_mwh": flex_identity_abs_err,
        "flex_identity_tol_mwh": flex_identity_tol,
        "flex_identity_ok": flex_identity_ok,
        "flex_components_abs_err_mwh": flex_components_abs_err,
        "flex_components_ok": flex_components_ok,
        "data_quality_flags": ";".join(sorted(set(data_quality_flags))),
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
    out["daily_has_below_5"] = out["daily_min_price"] < 5
    out["daily_vre_share_of_gen"] = out["daily_vre_mwh"] / out["daily_primary_mwh"]
    out = out.drop(columns=["daily_vre_mwh", "daily_primary_mwh"])
    return out

