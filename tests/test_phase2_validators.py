from __future__ import annotations

import pandas as pd

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
