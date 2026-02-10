"""Validators for phase2 scenario assumptions."""

from __future__ import annotations

from typing import Any

import pandas as pd


PHASE2_REQUIRED_COLUMNS = [
    "scenario_id",
    "country",
    "year",
    "demand_total_twh",
    "demand_peak_gw",
    "demand_shape_reference",
    "cap_pv_gw",
    "cap_wind_on_gw",
    "cap_wind_off_gw",
    "cap_must_run_nuclear_gw",
    "cap_must_run_chp_gw",
    "cap_must_run_biomass_gw",
    "cap_must_run_hydro_ror_gw",
    "must_run_min_output_factor",
    "interconnection_export_gw",
    "export_coincidence_factor",
    "psh_pump_gw",
    "bess_power_gw",
    "bess_energy_gwh",
    "bess_eta_roundtrip",
    "co2_eur_per_t",
    "gas_eur_per_mwh_th",
    "marginal_tech",
    "marginal_efficiency",
    "marginal_emission_factor_t_per_mwh",
    "supported_vre_share",
    "negative_price_rule",
    "negative_price_rule_threshold_hours",
    "price_exposure_share",
    "source_label",
    "notes",
]


def _to_num(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_numeric(df[col], errors="coerce")


def validate_phase2_assumptions(df: pd.DataFrame) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    missing = [c for c in PHASE2_REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        findings.append(
            {
                "severity": "ERROR",
                "code": "P2_MISSING_COLUMNS",
                "message": f"Missing columns: {missing}",
            }
        )
        return findings

    if df.empty:
        findings.append({"severity": "ERROR", "code": "P2_EMPTY", "message": "Phase2 assumptions table is empty"})
        return findings

    dup = df.duplicated(subset=["scenario_id", "country", "year"]).sum()
    if int(dup) > 0:
        findings.append({"severity": "ERROR", "code": "P2_DUP_KEY", "message": f"Duplicate keys: {int(dup)}"})

    bounded_01 = [
        "must_run_min_output_factor",
        "export_coincidence_factor",
        "bess_eta_roundtrip",
        "supported_vre_share",
        "price_exposure_share",
    ]
    for col in bounded_01:
        s = _to_num(df, col)
        bad = int((s.notna() & ((s < 0) | (s > 1))).sum())
        if bad > 0:
            findings.append({"severity": "ERROR", "code": "P2_RANGE_01", "message": f"{col} out of [0,1]: {bad}"})

    positive_cols = [
        "demand_total_twh",
        "cap_pv_gw",
        "cap_wind_on_gw",
        "interconnection_export_gw",
        "bess_power_gw",
        "bess_energy_gwh",
        "co2_eur_per_t",
        "gas_eur_per_mwh_th",
    ]
    for col in positive_cols:
        s = _to_num(df, col)
        bad = int((s.notna() & (s < 0)).sum())
        if bad > 0:
            findings.append({"severity": "ERROR", "code": "P2_NEG_VALUE", "message": f"{col} negative values: {bad}"})

    tech_allowed = {"gas_ccgt", "coal", "mixed"}
    bad_tech = int((~df["marginal_tech"].astype(str).str.lower().isin(tech_allowed)).sum())
    if bad_tech > 0:
        findings.append({"severity": "WARN", "code": "P2_UNKNOWN_TECH", "message": f"Unknown marginal_tech rows: {bad_tech}"})

    rules_allowed = {"none", "support_suspension", "curtailment_trigger"}
    bad_rules = int((~df["negative_price_rule"].astype(str).str.lower().isin(rules_allowed)).sum())
    if bad_rules > 0:
        findings.append({"severity": "WARN", "code": "P2_UNKNOWN_RULE", "message": f"Unknown negative_price_rule rows: {bad_rules}"})

    if not findings:
        findings.append({"severity": "PASS", "code": "P2_OK", "message": "Phase2 assumptions validation passed"})
    return findings

