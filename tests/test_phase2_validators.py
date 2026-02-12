from __future__ import annotations

import pandas as pd

from src.scenario.trajectory import expand_phase2_trajectory
from src.scenario.validators import validate_phase2_assumptions


def test_phase2_validators_pass_on_reference_table() -> None:
    df = pd.read_csv("data/assumptions/phase2/phase2_scenario_country_year.csv")
    findings = validate_phase2_assumptions(df)
    severities = {f["severity"] for f in findings}
    assert "ERROR" not in severities


def test_phase2_validators_detect_duplicate_keys() -> None:
    df = pd.read_csv("data/assumptions/phase2/phase2_scenario_country_year.csv").head(1)
    dup = pd.concat([df, df], ignore_index=True)
    findings = validate_phase2_assumptions(dup)
    codes = {f["code"] for f in findings}
    assert "P2_DUP_KEY" in codes


def test_phase2_validators_detect_out_of_range() -> None:
    df = pd.read_csv("data/assumptions/phase2/phase2_scenario_country_year.csv").head(1).copy()
    df.loc[:, "export_coincidence_factor"] = 2.0
    findings = validate_phase2_assumptions(df)
    assert any(f["code"] == "P2_RANGE_01" for f in findings)


def test_phase2_validators_warn_on_sparse_trajectory() -> None:
    df = pd.read_csv("data/assumptions/phase2/phase2_scenario_country_year.csv").head(2).copy()
    findings = validate_phase2_assumptions(df)
    codes = {f["code"] for f in findings}
    assert "P2_TRAJECTORY_SPARSE" in codes


def test_phase2_validators_no_gaps_after_trajectory_expansion() -> None:
    df = pd.read_csv("data/assumptions/phase2/phase2_scenario_country_year.csv")
    expanded = expand_phase2_trajectory(df)
    findings = validate_phase2_assumptions(expanded)
    codes = {f["code"] for f in findings}
    assert "P2_TRAJECTORY_GAPS" not in codes


def test_phase2_validators_include_non_confounding_check() -> None:
    df = pd.read_csv("data/assumptions/phase2/phase2_scenario_country_year.csv")
    findings = validate_phase2_assumptions(df)
    assert any(f["code"] == "TEST_SCEN_001" for f in findings)
    assert not any(f["code"] == "TEST_SCEN_001" and f["severity"] == "ERROR" for f in findings)


def test_phase2_validators_non_confounding_fails_for_unitary_scenario() -> None:
    df = pd.read_csv("data/assumptions/phase2/phase2_scenario_country_year.csv")
    base = df[df["scenario_id"] == "BASE"].head(1).copy()
    demand = base.copy()
    demand.loc[:, "scenario_id"] = "DEMAND_UP"
    demand.loc[:, "demand_total_twh"] = demand["demand_total_twh"] * 1.1
    demand.loc[:, "demand_peak_gw"] = demand["demand_peak_gw"] * 1.1
    demand.loc[:, "cap_pv_gw"] = demand["cap_pv_gw"] * 1.2
    demand.loc[:, "cap_wind_on_gw"] = demand["cap_wind_on_gw"] * 1.2
    demand.loc[:, "interconnection_export_gw"] = demand["interconnection_export_gw"] * 1.1
    stress = pd.concat([base, demand], ignore_index=True)
    findings = validate_phase2_assumptions(stress)
    assert any(f["code"] == "TEST_SCEN_001" and f["severity"] == "ERROR" for f in findings)
