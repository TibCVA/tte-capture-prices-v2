"""Historical calibration helpers for phase2 scenario engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def _safe_series(df: pd.DataFrame, col: str, default: float = 0.0) -> pd.Series:
    if col not in df.columns:
        return pd.Series(default, index=df.index, dtype=float)
    return pd.to_numeric(df[col], errors="coerce")


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
        if np.isfinite(out):
            return out
        return float(default)
    except Exception:
        return float(default)


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def _country_latest_annual(annual_hist: pd.DataFrame, country: str) -> pd.Series | None:
    if annual_hist is None or annual_hist.empty:
        return None
    scope = annual_hist[annual_hist["country"].astype(str) == str(country)].copy()
    if scope.empty:
        return None
    scope["year"] = pd.to_numeric(scope["year"], errors="coerce")
    scope = scope.sort_values("year")
    if scope.empty:
        return None
    return scope.iloc[-1]


def _fit_regime_b(ref_hourly: pd.DataFrame) -> dict[str, float]:
    regime = ref_hourly.get("regime")
    if regime is None:
        return {
            "price_b_floor": -10.0,
            "price_b_cap": 120.0,
            "price_b_intercept": 30.0,
            "price_b_slope_surplus_norm": -12.0,
            "price_b_tca_pass": 0.35,
            "price_anchor_ref": 80.0,
        }

    price = pd.to_numeric(ref_hourly.get("price_da_eur_mwh"), errors="coerce")
    surplus = pd.to_numeric(ref_hourly.get("surplus_mw"), errors="coerce").fillna(0.0)
    reg = regime.astype(str)

    b_price = price[reg == "B"].dropna()
    b_surplus = surplus[reg == "B"].reindex(b_price.index).fillna(0.0)

    cd_price = price[reg.isin(["C", "D"])].dropna()
    anchor_ref = float(cd_price.median()) if not cd_price.empty else float(price.dropna().median() if not price.dropna().empty else 80.0)

    if len(b_price) < 120:
        return {
            "price_b_floor": -10.0,
            "price_b_cap": max(20.0, anchor_ref * 0.8),
            "price_b_intercept": max(5.0, anchor_ref * 0.35),
            "price_b_slope_surplus_norm": -10.0,
            "price_b_tca_pass": 0.35,
            "price_anchor_ref": anchor_ref,
        }

    q95_surplus = float(np.nanquantile(pd.to_numeric(ref_hourly.get("surplus_mw"), errors="coerce").fillna(0.0), 0.95))
    q95_surplus = max(q95_surplus, 1.0)
    x = (b_surplus / q95_surplus).to_numpy(dtype=float)
    y = b_price.to_numpy(dtype=float)

    slope = np.nan
    if len(x) >= 2 and np.nanstd(x) > 1e-9:
        try:
            slope = float(np.polyfit(x, y, 1)[0])
        except Exception:
            slope = np.nan
    if not np.isfinite(slope) or slope >= -0.25:
        slope = -6.0
    slope = float(np.clip(slope, -150.0, -0.25))

    intercept = float(np.nanmedian(y))
    floor = float(np.nanquantile(y, 0.05))
    cap = float(np.nanquantile(y, 0.90))
    if not np.isfinite(floor):
        floor = -10.0
    if not np.isfinite(cap):
        cap = max(30.0, intercept * 1.5)
    if cap <= floor:
        cap = floor + 10.0

    pass_through = 0.35
    if np.isfinite(anchor_ref) and abs(anchor_ref) > 1e-9:
        pass_through = float(np.clip(intercept / anchor_ref, 0.10, 0.80))

    return {
        "price_b_floor": floor,
        "price_b_cap": cap,
        "price_b_intercept": intercept,
        "price_b_slope_surplus_norm": slope,
        "price_b_tca_pass": pass_through,
        "price_anchor_ref": anchor_ref,
    }


def _price_cd_levels(ref_hourly: pd.DataFrame) -> dict[str, float]:
    reg = ref_hourly.get("regime")
    if reg is None:
        return {
            "price_c_level": 70.0,
            "price_d_level": 130.0,
            "nrl_p90": 1000.0,
            "nrl_p99": 3000.0,
            "surplus_p95": 500.0,
        }

    reg = reg.astype(str)
    price = pd.to_numeric(ref_hourly.get("price_da_eur_mwh"), errors="coerce")
    nrl = pd.to_numeric(ref_hourly.get("nrl_mw"), errors="coerce").fillna(0.0)
    surplus = pd.to_numeric(ref_hourly.get("surplus_mw"), errors="coerce").fillna(0.0)

    c_price = price[reg == "C"].dropna()
    d_price = price[reg == "D"].dropna()
    c_level = float(c_price.median()) if not c_price.empty else float(price.dropna().median() if not price.dropna().empty else 70.0)
    d_level = float(d_price.median()) if not d_price.empty else c_level * 1.35
    if d_level <= c_level:
        d_level = c_level + 20.0

    nrl_pos = nrl[nrl > 0]
    nrl_p90 = float(np.nanquantile(nrl_pos, 0.90)) if len(nrl_pos) else 1000.0
    nrl_p99 = float(np.nanquantile(nrl_pos, 0.99)) if len(nrl_pos) else max(1.0, nrl_p90 * 1.8)
    if not np.isfinite(nrl_p90) or nrl_p90 <= 0:
        nrl_p90 = 1000.0
    if not np.isfinite(nrl_p99) or nrl_p99 <= nrl_p90:
        nrl_p99 = nrl_p90 * 1.8

    surplus_p95 = float(np.nanquantile(surplus, 0.95))
    if not np.isfinite(surplus_p95) or surplus_p95 <= 0:
        surplus_p95 = 500.0

    return {
        "price_c_level": c_level,
        "price_d_level": d_level,
        "nrl_p90": nrl_p90,
        "nrl_p99": nrl_p99,
        "surplus_p95": surplus_p95,
    }


def calibrate_country_bundle(
    country: str,
    ref_hourly: pd.DataFrame,
    annual_hist: pd.DataFrame,
    scenario_row: pd.Series,
    interconnection_proxy_path: Path = Path("data/external/normalized/interconnection_proxy_phase1.csv"),
    coincidence_matrix_path: Path = Path("data/external/normalized/surplus_coincidence_matrix_phase1.csv"),
) -> dict[str, float]:
    ref = ref_hourly.copy()

    mr = _safe_series(ref, "gen_must_run_mw").fillna(0.0)
    mr_p10 = float(mr.quantile(0.10)) if not mr.empty else 0.0
    mr_mean = float(mr.mean()) if not mr.empty else 0.0
    if not np.isfinite(mr_p10):
        mr_p10 = 0.0
    if not np.isfinite(mr_mean):
        mr_mean = 0.0

    annual_row = _country_latest_annual(annual_hist, country)
    far_hist = _safe_float(annual_row.get("far_energy") if annual_row is not None else np.nan, np.nan)
    if not np.isfinite(far_hist):
        far_hist = 0.85
    flex_realization = float(np.clip(far_hist * 0.90, 0.60, 0.95))

    inter_proxy = _read_csv(interconnection_proxy_path)
    cap_proxy_gw = np.nan
    if not inter_proxy.empty:
        scoped = inter_proxy[inter_proxy["country"].astype(str) == str(country)]
        if not scoped.empty and "interconnection_export_gw_proxy" in scoped.columns:
            cap_proxy_gw = _safe_float(scoped.iloc[0]["interconnection_export_gw_proxy"], np.nan)

    coincidence = _read_csv(coincidence_matrix_path)
    coincidence_emp = np.nan
    if not coincidence.empty and {"country", "neighbor_country", "export_coincidence_factor"}.issubset(coincidence.columns):
        scoped = coincidence[
            (coincidence["country"].astype(str) == str(country))
            & (coincidence["neighbor_country"].astype(str) != str(country))
        ]
        vals = pd.to_numeric(scoped["export_coincidence_factor"], errors="coerce").dropna()
        if not vals.empty:
            coincidence_emp = float(vals.mean())

    coincidence_scen = _safe_float(scenario_row.get("export_coincidence_factor"), np.nan)
    coincidence_used = coincidence_scen if np.isfinite(coincidence_scen) else coincidence_emp
    if np.isfinite(coincidence_emp) and np.isfinite(coincidence_used):
        coincidence_used = max(coincidence_emp, coincidence_used)
    if not np.isfinite(coincidence_used):
        coincidence_used = 0.35
    coincidence_used = float(np.clip(coincidence_used, 0.0, 0.95))

    cap_assumption = _safe_float(scenario_row.get("interconnection_export_gw"), np.nan)
    if np.isfinite(cap_assumption) and cap_assumption > 0:
        cap_input_gw = cap_assumption
    else:
        cap_input_gw = cap_proxy_gw if np.isfinite(cap_proxy_gw) else 0.0
    cap_eff_gw = float(max(0.0, cap_input_gw * (1.0 - coincidence_used)))

    scenario_id = str(scenario_row.get("scenario_id", "")).upper()
    vre_floor_map = {
        "BASE": 1.00,
        "DEMAND_UP": 1.00,
        "LOW_RIGIDITY": 1.00,
        "HIGH_CO2": 1.00,
        "HIGH_GAS": 1.00,
    }
    vre_floor = float(vre_floor_map.get(scenario_id, 1.00))

    regime_b = _fit_regime_b(ref)
    cd = _price_cd_levels(ref)

    return {
        "mr_p10_mw": mr_p10,
        "mr_mean_mw": mr_mean,
        "flex_realization_factor": flex_realization,
        "export_realization_factor": float(np.clip(0.90 - 0.25 * coincidence_used, 0.45, 0.95)),
        "psh_realization_factor": float(np.clip(0.92 - 0.20 * coincidence_used, 0.55, 0.95)),
        "stress_penalty": float(np.clip(0.15 + 0.35 * coincidence_used, 0.15, 0.55)),
        "export_cap_proxy_gw": float(cap_proxy_gw) if np.isfinite(cap_proxy_gw) else np.nan,
        "export_cap_eff_gw": cap_eff_gw,
        "export_coincidence_emp": float(coincidence_emp) if np.isfinite(coincidence_emp) else np.nan,
        "export_coincidence_used": coincidence_used,
        "vre_floor_factor": vre_floor,
        "calib_scenario_id": scenario_id,
        **regime_b,
        **cd,
    }
