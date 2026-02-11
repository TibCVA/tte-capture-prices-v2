"""Phase2 scenario engine (pragmatic stress-tests)."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.config_loader import load_countries, load_thresholds
from src.constants import (
    COL_BESS_CHARGE,
    COL_BESS_DISCHARGE,
    COL_BESS_SOC,
    COL_EXPORTS,
    COL_FLEX_EFFECTIVE,
    COL_FLEX_OBS,
    COL_FLEX_PSH,
    COL_GEN_BIOMASS,
    COL_GEN_COAL,
    COL_GEN_GAS,
    COL_GEN_HYDRO_PSH_GEN,
    COL_GEN_HYDRO_RES,
    COL_GEN_HYDRO_ROR,
    COL_GEN_LIGNITE,
    COL_GEN_NUCLEAR,
    COL_GEN_OIL,
    COL_GEN_OTHER,
    COL_GEN_SOLAR,
    COL_GEN_WIND_OFF,
    COL_GEN_WIND_ON,
    COL_LOAD_TOTAL,
    COL_NET_POSITION,
    COL_NRL,
    COL_NRL_THRESHOLD,
    COL_PRICE_DA,
    COL_PSH_PUMP,
    COL_REGIME,
    COL_SURPLUS,
    COL_SURPLUS_ABSORBED,
    COL_SURPLUS_UNABS,
)
from src.hash_utils import hash_object
from src.metrics import compute_annual_metrics
from src.processing import build_hourly_table
from src.scenario.calibration import calibrate_country_bundle
from src.scenario.validators import validate_phase2_assumptions
from src.storage import (
    load_hourly,
    save_scenario_annual_metrics_row,
    save_scenario_hourly,
    save_scenario_validation_findings,
)
from src.time_utils import annual_utc_index
from src.validation_report import build_validation_report


def _repeat_to_length(arr: np.ndarray, n: int) -> np.ndarray:
    if len(arr) == 0:
        return np.zeros(n, dtype=float)
    return np.resize(arr, n).astype(float)


def _safe_float(obj: Any, key: str | None = None, default: float = 0.0) -> float:
    try:
        if key is None:
            v = float(obj)
        else:
            v = float(obj.get(key, default))
        if np.isfinite(v):
            return v
        return float(default)
    except Exception:
        return float(default)


def _scaled_profile_to_energy(ref: np.ndarray, n: int, target_energy_mwh: float) -> np.ndarray:
    base = _repeat_to_length(ref, n)
    base = np.maximum(base, 0.0)
    total = float(np.sum(base))
    if total <= 0 or target_energy_mwh <= 0:
        return np.zeros(n, dtype=float)
    return base / total * float(target_energy_mwh)


def _scaled_component_profile(
    ref: np.ndarray,
    n: int,
    target_mean_mw: float,
    floor_mean_mw: float = 0.0,
    cap_mean_mw: float | None = None,
) -> np.ndarray:
    base = _repeat_to_length(ref, n)
    base = np.maximum(base, 0.0)
    mean = float(np.nanmean(base)) if len(base) else 0.0
    if not np.isfinite(mean) or mean <= 0:
        out = np.full(n, max(0.0, target_mean_mw), dtype=float)
    else:
        shape = base / mean
        out = np.maximum(0.0, shape * max(0.0, target_mean_mw))
    if floor_mean_mw > 0 and np.nanmean(out) < floor_mean_mw:
        ratio = floor_mean_mw / max(np.nanmean(out), 1e-9)
        out = out * ratio
    if cap_mean_mw is not None and cap_mean_mw > 0 and np.nanmean(out) > cap_mean_mw:
        ratio = cap_mean_mw / max(np.nanmean(out), 1e-9)
        out = out * ratio
    return np.maximum(out, 0.0)


def _select_reference_year(country: str, demand_shape_reference: str, annual_hist: pd.DataFrame) -> int:
    ref = str(demand_shape_reference or "").lower()
    if ref.startswith("year_"):
        try:
            return int(ref.split("_")[1])
        except Exception:
            pass
    country_years = annual_hist[annual_hist["country"] == country]["year"].dropna().astype(int).tolist()
    if not country_years:
        raise ValueError(f"No historical annual data available for country={country}")
    return int(max(country_years))


def _regime_from_nrl(nrl: np.ndarray, min_pos_hours: int = 200, q: float = 0.9) -> tuple[np.ndarray, float]:
    surplus = np.maximum(0.0, -nrl)
    regime = np.array(["C"] * len(nrl), dtype=object)
    regime[surplus > 0] = "B"
    pos = nrl[nrl > 0]
    if len(pos) < min_pos_hours:
        threshold = float("nan")
    else:
        threshold = float(np.nanquantile(pos, q))
        regime[(surplus == 0) & (nrl >= threshold)] = "D"
    return regime, threshold


def _apply_bess(hourly: pd.DataFrame, power_mw: float, energy_mwh: float, eta_rt: float) -> pd.DataFrame:
    if power_mw <= 0 or energy_mwh <= 0:
        hourly[COL_BESS_CHARGE] = 0.0
        hourly[COL_BESS_DISCHARGE] = 0.0
        hourly[COL_BESS_SOC] = 0.0
        return hourly

    eta_c = float(np.sqrt(max(0.01, eta_rt)))
    eta_d = float(np.sqrt(max(0.01, eta_rt)))
    soc = 0.5 * energy_mwh

    charge = np.zeros(len(hourly), dtype=float)
    discharge = np.zeros(len(hourly), dtype=float)
    soc_series = np.zeros(len(hourly), dtype=float)

    nrl = pd.to_numeric(hourly[COL_NRL], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    surplus_unabs = pd.to_numeric(hourly[COL_SURPLUS_UNABS], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    nrl_pos = np.maximum(0.0, nrl)
    discharge_trigger = float(np.nanquantile(nrl_pos[nrl_pos > 0], 0.8)) if (nrl_pos > 0).any() else float("inf")

    for i in range(len(hourly)):
        ch = 0.0
        dis = 0.0
        if surplus_unabs[i] > 0:
            ch = min(power_mw, surplus_unabs[i], max(0.0, (energy_mwh - soc) / eta_c))
            soc += ch * eta_c
        elif nrl[i] > discharge_trigger:
            dis = min(power_mw, max(0.0, soc * eta_d))
            soc -= dis / eta_d

        soc = max(0.0, min(energy_mwh, soc))
        charge[i] = ch
        discharge[i] = dis
        soc_series[i] = soc

    hourly[COL_BESS_CHARGE] = charge
    hourly[COL_BESS_DISCHARGE] = discharge
    hourly[COL_BESS_SOC] = soc_series
    return hourly


def _inject_synthetic_price(hourly: pd.DataFrame, row: pd.Series, calib: dict[str, float]) -> pd.DataFrame:
    tech = str(row.get("marginal_tech", "gas_ccgt")).lower()
    eff = _safe_float(row, "marginal_efficiency", 0.55)
    ef = _safe_float(row, "marginal_emission_factor_t_per_mwh", 0.202)
    gas = _safe_float(row, "gas_eur_per_mwh_th", 45.0)
    co2 = _safe_float(row, "co2_eur_per_t", 90.0)

    vom = 3.0 if tech in {"gas_ccgt", "mixed"} else 4.0
    tca = gas / max(0.2, eff) + co2 * (ef / max(0.2, eff)) + vom

    nrl = pd.to_numeric(hourly[COL_NRL], errors="coerce").fillna(0.0)
    nrl_pos = nrl.clip(lower=0.0)
    surplus = pd.to_numeric(hourly[COL_SURPLUS], errors="coerce").fillna(0.0)
    surplus_unabs = pd.to_numeric(hourly[COL_SURPLUS_UNABS], errors="coerce").fillna(0.0)
    regime = hourly[COL_REGIME].astype(str)

    price_anchor_ref = float(calib.get("price_anchor_ref", 80.0))
    price_b_floor = float(calib.get("price_b_floor", -10.0))
    price_b_cap = float(calib.get("price_b_cap", 120.0))
    price_b_intercept = float(calib.get("price_b_intercept", 30.0))
    price_b_slope = float(calib.get("price_b_slope_surplus_norm", -12.0))
    price_b_tca_pass = float(calib.get("price_b_tca_pass", 0.35))
    surplus_p95 = max(float(calib.get("surplus_p95", 500.0)), 1.0)
    nrl_p90 = max(float(calib.get("nrl_p90", 1000.0)), 1.0)
    nrl_p99 = max(float(calib.get("nrl_p99", 3000.0)), nrl_p90 + 1.0)
    c_level = float(calib.get("price_c_level", max(5.0, price_anchor_ref * 0.8)))
    d_level = float(calib.get("price_d_level", max(c_level + 15.0, price_anchor_ref * 1.2)))

    tca_delta = tca - price_anchor_ref
    surplus_norm = surplus / surplus_p95
    nrl_norm_c = nrl_pos / nrl_p90
    nrl_norm_d = nrl_pos / nrl_p99

    # Piecewise-affine synthetic price with historical calibration for regime B.
    p = pd.Series(index=hourly.index, dtype=float)
    # Regime A: stronger downside with unabsorbed surplus.
    p.loc[regime == "A"] = -20.0 - 0.04 * surplus_unabs.loc[regime == "A"]
    # Regime B: calibrated floor/intercept/slope against historical B behavior.
    p_b_raw = price_b_intercept + price_b_slope * surplus_norm + price_b_tca_pass * tca_delta
    p.loc[regime == "B"] = p_b_raw.loc[regime == "B"].clip(lower=price_b_floor, upper=price_b_cap)
    # Regime C/D: anchored on historical C/D levels with moderate TCA and NRL pass-through.
    p.loc[regime == "C"] = c_level + 0.25 * tca_delta + 8.0 * nrl_norm_c.loc[regime == "C"]
    p.loc[regime == "D"] = d_level + 0.35 * tca_delta + 20.0 * nrl_norm_d.loc[regime == "D"]
    p = p.fillna(c_level + 0.25 * tca_delta).clip(lower=-500.0, upper=5000.0)
    hourly[COL_PRICE_DA] = p
    return hourly


def _project_raw_panel(
    ref_hourly: pd.DataFrame,
    row: pd.Series,
    target_year: int,
    calib: dict[str, float],
) -> pd.DataFrame:
    idx = annual_utc_index(target_year)
    n = len(idx)

    out = pd.DataFrame(index=idx)
    out.index.name = "timestamp_utc"

    # Demand
    ref_load = (
        pd.to_numeric(ref_hourly[COL_LOAD_TOTAL], errors="coerce")
        .ffill()
        .bfill()
        .fillna(0.0)
        .to_numpy(dtype=float)
    )
    load_shape = _repeat_to_length(ref_load, n)
    load_shape = np.maximum(load_shape, 0.0)
    load_shape_sum = float(load_shape.sum())
    target_load_mwh = _safe_float(row, "demand_total_twh", 0.0) * 1e6
    if load_shape_sum <= 0:
        out[COL_LOAD_TOTAL] = target_load_mwh / n
    else:
        out[COL_LOAD_TOTAL] = load_shape / load_shape_sum * target_load_mwh

    # Net position / exports proxy
    ref_net = pd.to_numeric(ref_hourly[COL_NET_POSITION], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    net_shape = _repeat_to_length(ref_net, n)
    cap_scen_gw = _safe_float(row, "interconnection_export_gw", np.nan)
    cap_eff_gw = _safe_float(calib.get("export_cap_eff_gw"), default=np.nan)
    if np.isfinite(cap_eff_gw) and cap_eff_gw > 0:
        cap_eff_mw = cap_eff_gw * 1000.0
    elif np.isfinite(cap_scen_gw) and cap_scen_gw > 0:
        coincidence = float(np.clip(_safe_float(row, "export_coincidence_factor", 0.35), 0.0, 0.95))
        cap_eff_mw = cap_scen_gw * 1000.0 * (1.0 - coincidence)
    else:
        cap_eff_mw = 0.0
    net_pos = np.clip(net_shape, -cap_eff_mw, cap_eff_mw)
    out[COL_NET_POSITION] = net_pos

    # PSH pump proxy
    ref_psh = pd.to_numeric(ref_hourly.get(COL_PSH_PUMP, 0.0), errors="coerce").fillna(0.0).to_numpy(dtype=float)
    psh_shape = _repeat_to_length(ref_psh, n)
    psh_cap = _safe_float(row, "psh_pump_gw", 0.0) * 1000.0
    psh_realization = float(np.clip(_safe_float(calib.get("psh_realization_factor"), 0.85), 0.30, 1.0))
    out[COL_PSH_PUMP] = np.minimum(np.maximum(psh_shape, 0.0), psh_cap) * psh_realization

    # VRE generation scaling from capacities with historical energy floor.
    vre_floor_factor = float(np.clip(_safe_float(calib.get("vre_floor_factor"), 1.0), 0.5, 2.5))
    for cap_col, gen_col, ref_col in [
        ("cap_pv_gw", COL_GEN_SOLAR, COL_GEN_SOLAR),
        ("cap_wind_on_gw", COL_GEN_WIND_ON, COL_GEN_WIND_ON),
        ("cap_wind_off_gw", COL_GEN_WIND_OFF, COL_GEN_WIND_OFF),
    ]:
        cap_mw = _safe_float(row, cap_col, 0.0) * 1000.0
        ref_gen = pd.to_numeric(ref_hourly.get(ref_col, 0.0), errors="coerce").fillna(0.0).to_numpy(dtype=float)
        ref_gen = _repeat_to_length(ref_gen, n)
        hist_energy = float(np.sum(np.maximum(ref_gen, 0.0)))
        peak = float(np.nanquantile(ref_gen, 0.995)) if len(ref_gen) else 0.0
        if peak > 0 and cap_mw > 0:
            cf_ref = float(np.clip(hist_energy / (peak * n), 0.01, 0.80))
            target_energy_cap = cap_mw * cf_ref * n
        else:
            target_energy_cap = 0.0
        target_energy = max(target_energy_cap, hist_energy * vre_floor_factor)
        out[gen_col] = _scaled_profile_to_energy(ref_gen, n, target_energy)

    # Must-run components from capacities, anchored on historical must-run floor.
    must_run_factor = _safe_float(row, "must_run_min_output_factor", 0.5)
    mr_floor = float(max(0.0, _safe_float(calib.get("mr_p10_mw"), 0.0) * 0.90))
    mr_cap = _safe_float(calib.get("mr_mean_mw"), np.nan)
    mr_cap = float(mr_cap * 1.15) if np.isfinite(mr_cap) else None

    nuc_ref = pd.to_numeric(ref_hourly.get(COL_GEN_NUCLEAR, 0.0), errors="coerce").fillna(0.0).to_numpy(dtype=float)
    bio_ref = pd.to_numeric(ref_hourly.get(COL_GEN_BIOMASS, 0.0), errors="coerce").fillna(0.0).to_numpy(dtype=float)
    ror_ref = pd.to_numeric(ref_hourly.get(COL_GEN_HYDRO_ROR, 0.0), errors="coerce").fillna(0.0).to_numpy(dtype=float)

    target_nuc = _safe_float(row, "cap_must_run_nuclear_gw", 0.0) * 1000.0 * must_run_factor
    target_bio = _safe_float(row, "cap_must_run_biomass_gw", 0.0) * 1000.0 * must_run_factor
    target_ror = _safe_float(row, "cap_must_run_hydro_ror_gw", 0.0) * 1000.0 * must_run_factor
    target_chp = _safe_float(row, "cap_must_run_chp_gw", 0.0) * 1000.0 * must_run_factor
    target_raw_total = target_nuc + target_bio + target_ror + target_chp
    target_total = max(target_raw_total, mr_floor)
    if mr_cap is not None and mr_cap > 0:
        target_total = min(target_total, mr_cap)
    must_run_scale = float(max(0.0, _safe_float(row, "must_run_scale_scenario", 1.0)))

    means = np.array(
        [
            float(np.nanmean(np.maximum(_repeat_to_length(nuc_ref, n), 0.0))),
            float(np.nanmean(np.maximum(_repeat_to_length(bio_ref, n), 0.0))),
            float(np.nanmean(np.maximum(_repeat_to_length(ror_ref, n), 0.0))),
        ],
        dtype=float,
    )
    if np.sum(means) <= 0:
        if target_total > 0:
            means = np.array([1.0, 1.0, 1.0], dtype=float)
        else:
            means = np.array([target_nuc, target_bio, target_ror], dtype=float)
    shares = means / max(np.sum(means), 1e-9)

    out[COL_GEN_NUCLEAR] = _scaled_component_profile(nuc_ref, n, target_total * shares[0], floor_mean_mw=0.0)
    out[COL_GEN_BIOMASS] = _scaled_component_profile(bio_ref, n, target_total * shares[1], floor_mean_mw=0.0)
    out[COL_GEN_HYDRO_ROR] = _scaled_component_profile(ror_ref, n, target_total * shares[2], floor_mean_mw=0.0)
    out["must_run_profile_override_mw"] = np.nan
    out["must_run_scale_scenario"] = must_run_scale
    if target_total <= 1e-9:
        ref_profile = pd.to_numeric(ref_hourly.get("gen_must_run_mw"), errors="coerce").fillna(0.0).to_numpy(dtype=float)
        out["must_run_profile_override_mw"] = _repeat_to_length(ref_profile, n)

    ref_hydro_res = pd.to_numeric(ref_hourly.get(COL_GEN_HYDRO_RES, 0.0), errors="coerce").fillna(0.0).to_numpy(dtype=float)
    out[COL_GEN_HYDRO_RES] = _repeat_to_length(ref_hydro_res, n) * 0.9
    ref_psh_gen = pd.to_numeric(ref_hourly.get(COL_GEN_HYDRO_PSH_GEN, 0.0), errors="coerce").fillna(0.0).to_numpy(dtype=float)
    out[COL_GEN_HYDRO_PSH_GEN] = _repeat_to_length(ref_psh_gen, n) * 0.8

    # Thermal placeholders
    out[COL_GEN_GAS] = 0.0
    out[COL_GEN_COAL] = 0.0
    out[COL_GEN_LIGNITE] = 0.0
    out[COL_GEN_OIL] = 0.0
    out[COL_GEN_OTHER] = 0.0

    # Price placeholder (replaced later)
    out[COL_PRICE_DA] = 0.0
    return out


def run_phase2_scenario(
    scenario_id: str,
    countries: list[str],
    years: list[int],
    assumptions_phase2: pd.DataFrame,
    annual_hist: pd.DataFrame,
    hourly_hist_map: dict[tuple[str, int], pd.DataFrame] | None = None,
) -> dict[str, Any]:
    findings = validate_phase2_assumptions(assumptions_phase2)
    hard = [f for f in findings if f["severity"] == "ERROR"]
    if hard:
        raise ValueError(f"Phase2 assumptions invalid: {hard}")

    countries_cfg = load_countries()["countries"]
    thresholds_cfg = load_thresholds()

    selected = assumptions_phase2[
        (assumptions_phase2["scenario_id"].astype(str) == str(scenario_id))
        & (assumptions_phase2["country"].astype(str).isin(countries))
        & (pd.to_numeric(assumptions_phase2["year"], errors="coerce").isin(years))
    ].copy()
    if selected.empty:
        raise ValueError(f"No scenario rows found for scenario_id={scenario_id}, countries={countries}, years={years}")

    if hourly_hist_map is None:
        hourly_hist_map = {}

    annual_rows: list[dict[str, Any]] = []
    all_findings: list[dict[str, Any]] = []
    hourly_paths: list[str] = []

    for _, row in selected.iterrows():
        country = str(row["country"])
        year = int(row["year"])
        ref_year = _select_reference_year(country, str(row.get("demand_shape_reference", "")), annual_hist)
        ref_key = (country, ref_year)
        if ref_key in hourly_hist_map:
            ref_hourly = hourly_hist_map[ref_key]
        else:
            ref_hourly = load_hourly(country, ref_year)

        calib = calibrate_country_bundle(country=country, ref_hourly=ref_hourly, annual_hist=annual_hist, scenario_row=row)

        raw_panel = _project_raw_panel(ref_hourly, row, year, calib)
        built = build_hourly_table(
            raw_panel=raw_panel,
            country=country,
            year=year,
            country_cfg=countries_cfg[country],
            thresholds_cfg=thresholds_cfg,
            entsoe_code_used=f"SCEN:{scenario_id}",
        )

        # Recompute effective absorption with conservative realization factors.
        surplus = pd.to_numeric(built[COL_SURPLUS], errors="coerce").fillna(0.0)
        exports_raw = pd.to_numeric(built[COL_EXPORTS], errors="coerce").fillna(0.0)
        psh_raw = pd.to_numeric(built[COL_FLEX_PSH], errors="coerce").fillna(0.0)
        coincidence_used = float(np.clip(_safe_float(calib.get("export_coincidence_used"), default=0.35), 0.0, 0.95))
        export_real = float(np.clip(_safe_float(calib.get("export_realization_factor"), default=0.75), 0.30, 1.0))
        psh_real = float(np.clip(_safe_float(calib.get("psh_realization_factor"), default=0.80), 0.30, 1.0))
        flex_real = float(np.clip(_safe_float(calib.get("flex_realization_factor"), default=0.85), 0.30, 1.0))
        stress_penalty = float(np.clip(_safe_float(calib.get("stress_penalty"), default=0.25), 0.0, 0.80))

        surplus_p90 = float(surplus.quantile(0.90)) if len(surplus) else 0.0
        stress_mask = surplus > max(surplus_p90, 0.0)
        exports_eff = exports_raw * export_real * flex_real
        exports_eff.loc[stress_mask] = exports_eff.loc[stress_mask] * max(0.0, 1.0 - stress_penalty * coincidence_used)

        remaining = surplus.copy()
        exports_sink = np.minimum(exports_eff, remaining)
        remaining = (remaining - exports_sink).clip(lower=0.0)
        psh_eff = psh_raw * psh_real * flex_real
        psh_sink = np.minimum(psh_eff, remaining)
        remaining = (remaining - psh_sink).clip(lower=0.0)

        built[COL_FLEX_PSH] = psh_sink
        built[COL_FLEX_OBS] = exports_sink + psh_sink
        built[COL_SURPLUS_UNABS] = remaining

        built = _apply_bess(
            built,
            power_mw=_safe_float(row, "bess_power_gw", 0.0) * 1000.0,
            energy_mwh=_safe_float(row, "bess_energy_gwh", 0.0) * 1000.0,
            eta_rt=_safe_float(row, "bess_eta_roundtrip", 0.88),
        )

        # Final effective absorption after BESS charge on remaining surplus.
        bess_charge = pd.to_numeric(built[COL_BESS_CHARGE], errors="coerce").fillna(0.0)
        bess_sink = np.minimum(bess_charge, remaining)
        built[COL_FLEX_EFFECTIVE] = built[COL_FLEX_OBS] + bess_sink
        built[COL_SURPLUS_ABSORBED] = (exports_sink + psh_sink + bess_sink).clip(lower=0.0)
        built[COL_SURPLUS_UNABS] = (surplus - built[COL_SURPLUS_ABSORBED]).clip(lower=0.0)

        # Regimes after BESS update
        nrl = pd.to_numeric(built[COL_NRL], errors="coerce").fillna(0.0).to_numpy(dtype=float)
        regime, threshold = _regime_from_nrl(nrl)
        regime = pd.Series(regime, index=built.index, dtype=object)
        regime[pd.to_numeric(built[COL_SURPLUS_UNABS], errors="coerce").fillna(0.0) > 0] = "A"
        regime[(pd.to_numeric(built[COL_SURPLUS], errors="coerce").fillna(0.0) > 0) & (pd.to_numeric(built[COL_SURPLUS_UNABS], errors="coerce").fillna(0.0) <= 0)] = "B"
        built[COL_REGIME] = regime
        built[COL_NRL_THRESHOLD] = threshold

        built = _inject_synthetic_price(built, row, calib)

        data_version_hash = hash_object(
            {
                "scenario_id": scenario_id,
                "country": country,
                "year": year,
                "assumptions_row": row.to_dict(),
                "calibration": calib,
            }
        )
        annual_row = compute_annual_metrics(built, countries_cfg[country], data_version_hash=data_version_hash)
        annual_row["scenario_id"] = scenario_id
        annual_row["mode"] = "SCEN"
        annual_row["horizon_year"] = year
        annual_row["calib_mustrun_scale"] = _safe_float(calib.get("mr_p10_mw"), default=np.nan)
        annual_row["calib_vre_scale_pv"] = _safe_float(row, "cap_pv_gw", np.nan)
        annual_row["calib_vre_scale_wind_on"] = _safe_float(row, "cap_wind_on_gw", np.nan)
        annual_row["calib_vre_scale_wind_off"] = _safe_float(row, "cap_wind_off_gw", np.nan)
        annual_row["calib_export_cap_eff_gw"] = _safe_float(calib.get("export_cap_eff_gw"), default=np.nan)
        annual_row["calib_export_coincidence_used"] = _safe_float(calib.get("export_coincidence_used"), default=np.nan)
        annual_row["calib_flex_realization_factor"] = _safe_float(calib.get("flex_realization_factor"), default=np.nan)
        annual_row["calib_price_b_floor"] = _safe_float(calib.get("price_b_floor"), default=np.nan)
        annual_row["calib_price_b_intercept"] = _safe_float(calib.get("price_b_intercept"), default=np.nan)
        annual_row["calib_price_b_slope_surplus_norm"] = _safe_float(calib.get("price_b_slope_surplus_norm"), default=np.nan)
        annual_rows.append(annual_row)

        val = build_validation_report(built, annual_row)
        for f in val:
            f["country"] = country
            f["year"] = year
            f["scenario_id"] = scenario_id
        all_findings.extend(val)

        p = save_scenario_hourly(built, scenario_id, country, year)
        hourly_paths.append(str(p))
        save_scenario_annual_metrics_row(annual_row, scenario_id)

    findings_df = pd.DataFrame(all_findings)
    if not findings_df.empty:
        save_scenario_validation_findings(findings_df, scenario_id)

    annual_df = pd.DataFrame(annual_rows).sort_values(["country", "year"]).reset_index(drop=True)
    return {
        "scenario_id": scenario_id,
        "countries": sorted(set(annual_df["country"].astype(str).tolist())) if not annual_df.empty else [],
        "years": sorted(set(annual_df["year"].astype(int).tolist())) if not annual_df.empty else [],
        "annual_metrics": annual_df,
        "validation_findings": findings_df,
        "hourly_paths": hourly_paths,
        "assumptions_validation": findings,
    }
