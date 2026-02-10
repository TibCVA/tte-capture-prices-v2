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


def _safe_float(row: pd.Series, key: str, default: float = 0.0) -> float:
    try:
        v = float(row.get(key, default))
        if np.isfinite(v):
            return v
        return float(default)
    except Exception:
        return float(default)


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


def _inject_synthetic_price(hourly: pd.DataFrame, row: pd.Series) -> pd.DataFrame:
    tech = str(row.get("marginal_tech", "gas_ccgt")).lower()
    eff = _safe_float(row, "marginal_efficiency", 0.55)
    ef = _safe_float(row, "marginal_emission_factor_t_per_mwh", 0.202)
    gas = _safe_float(row, "gas_eur_per_mwh_th", 45.0)
    co2 = _safe_float(row, "co2_eur_per_t", 90.0)

    vom = 3.0 if tech in {"gas_ccgt", "mixed"} else 4.0
    tca = gas / max(0.2, eff) + co2 * (ef / max(0.2, eff)) + vom

    nrl = pd.to_numeric(hourly[COL_NRL], errors="coerce").fillna(0.0)
    nrl_pos = nrl.clip(lower=0.0)
    regime = hourly[COL_REGIME].astype(str)

    # Piecewise-affine synthetic price anchored on TCA/TTL logic
    p = pd.Series(index=hourly.index, dtype=float)
    p.loc[regime == "A"] = -10.0 - 0.02 * pd.to_numeric(hourly.loc[regime == "A", COL_SURPLUS_UNABS], errors="coerce").fillna(0.0)
    p.loc[regime == "B"] = 0.35 * tca
    p.loc[regime == "C"] = 0.85 * tca + 0.02 * nrl_pos.loc[regime == "C"]
    p.loc[regime == "D"] = 1.20 * tca + 0.05 * nrl_pos.loc[regime == "D"]
    p = p.fillna(0.85 * tca).clip(lower=-500.0, upper=5000.0)
    hourly[COL_PRICE_DA] = p
    return hourly


def _project_raw_panel(ref_hourly: pd.DataFrame, row: pd.Series, target_year: int) -> pd.DataFrame:
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
    cap_eff_mw = _safe_float(row, "interconnection_export_gw", 0.0) * 1000.0 * (1.0 - _safe_float(row, "export_coincidence_factor", 0.0))
    net_pos = np.clip(net_shape, -cap_eff_mw, cap_eff_mw)
    out[COL_NET_POSITION] = net_pos

    # PSH pump proxy
    ref_psh = pd.to_numeric(ref_hourly.get(COL_PSH_PUMP, 0.0), errors="coerce").fillna(0.0).to_numpy(dtype=float)
    psh_shape = _repeat_to_length(ref_psh, n)
    psh_cap = _safe_float(row, "psh_pump_gw", 0.0) * 1000.0
    out[COL_PSH_PUMP] = np.minimum(np.maximum(psh_shape, 0.0), psh_cap)

    # VRE generation scaling from capacities
    for cap_col, gen_col, ref_col in [
        ("cap_pv_gw", COL_GEN_SOLAR, COL_GEN_SOLAR),
        ("cap_wind_on_gw", COL_GEN_WIND_ON, COL_GEN_WIND_ON),
        ("cap_wind_off_gw", COL_GEN_WIND_OFF, COL_GEN_WIND_OFF),
    ]:
        cap_mw = _safe_float(row, cap_col, 0.0) * 1000.0
        ref_gen = pd.to_numeric(ref_hourly.get(ref_col, 0.0), errors="coerce").fillna(0.0).to_numpy(dtype=float)
        ref_gen = _repeat_to_length(ref_gen, n)
        peak = float(np.nanquantile(ref_gen, 0.995)) if len(ref_gen) else 0.0
        ratio = 0.0 if peak <= 0 else cap_mw / peak
        out[gen_col] = np.maximum(ref_gen * ratio, 0.0)

    # Must-run components from capacities (simple floor around profiles)
    must_run_factor = _safe_float(row, "must_run_min_output_factor", 0.5)
    out[COL_GEN_NUCLEAR] = _safe_float(row, "cap_must_run_nuclear_gw", 0.0) * 1000.0 * must_run_factor
    out[COL_GEN_BIOMASS] = _safe_float(row, "cap_must_run_biomass_gw", 0.0) * 1000.0 * must_run_factor
    out[COL_GEN_HYDRO_ROR] = _safe_float(row, "cap_must_run_hydro_ror_gw", 0.0) * 1000.0 * must_run_factor
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

        raw_panel = _project_raw_panel(ref_hourly, row, year)
        built = build_hourly_table(
            raw_panel=raw_panel,
            country=country,
            year=year,
            country_cfg=countries_cfg[country],
            thresholds_cfg=thresholds_cfg,
            entsoe_code_used=f"SCEN:{scenario_id}",
        )

        built = _apply_bess(
            built,
            power_mw=_safe_float(row, "bess_power_gw", 0.0) * 1000.0,
            energy_mwh=_safe_float(row, "bess_energy_gwh", 0.0) * 1000.0,
            eta_rt=_safe_float(row, "bess_eta_roundtrip", 0.88),
        )

        # Recompute flex and surplus with BESS charge
        built[COL_FLEX_EFFECTIVE] = pd.to_numeric(built[COL_FLEX_OBS], errors="coerce").fillna(0.0) + pd.to_numeric(
            built[COL_BESS_CHARGE], errors="coerce"
        ).fillna(0.0)
        built[COL_SURPLUS_ABSORBED] = np.minimum(
            pd.to_numeric(built[COL_SURPLUS], errors="coerce").fillna(0.0),
            pd.to_numeric(built[COL_FLEX_EFFECTIVE], errors="coerce").fillna(0.0),
        )
        built[COL_SURPLUS_UNABS] = (
            pd.to_numeric(built[COL_SURPLUS], errors="coerce").fillna(0.0) - pd.to_numeric(built[COL_SURPLUS_ABSORBED], errors="coerce").fillna(0.0)
        ).clip(lower=0.0)

        # Regimes after BESS update
        nrl = pd.to_numeric(built[COL_NRL], errors="coerce").fillna(0.0).to_numpy(dtype=float)
        regime, threshold = _regime_from_nrl(nrl)
        regime = pd.Series(regime, index=built.index, dtype=object)
        regime[pd.to_numeric(built[COL_SURPLUS_UNABS], errors="coerce").fillna(0.0) > 0] = "A"
        regime[(pd.to_numeric(built[COL_SURPLUS], errors="coerce").fillna(0.0) > 0) & (pd.to_numeric(built[COL_SURPLUS_UNABS], errors="coerce").fillna(0.0) <= 0)] = "B"
        built[COL_REGIME] = regime
        built[COL_NRL_THRESHOLD] = threshold

        built = _inject_synthetic_price(built, row)

        data_version_hash = hash_object(
            {
                "scenario_id": scenario_id,
                "country": country,
                "year": year,
                "assumptions_row": row.to_dict(),
            }
        )
        annual_row = compute_annual_metrics(built, countries_cfg[country], data_version_hash=data_version_hash)
        annual_row["scenario_id"] = scenario_id
        annual_row["mode"] = "SCEN"
        annual_row["horizon_year"] = year
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
