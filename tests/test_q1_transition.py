from __future__ import annotations

import pandas as pd

from src.modules.q1_transition import run_q1


def test_q1_transition_classification(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q1(annual_panel_fixture, assumptions, {"countries": ["FR", "DE"], "years": [2021, 2022, 2023, 2024]}, "test")
    panel = res.tables["Q1_year_panel"]
    assert (panel["phase_market"] == "phase2").any()


def test_q1_bascule_year_first_year_condition(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q1(annual_panel_fixture, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    summary = res.tables["Q1_country_summary"]
    assert summary["bascule_year_market"].notna().all()


def test_q1_no_bascule_on_quality_fail(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    df = annual_panel_fixture.copy()
    df.loc[(df["country"] == "FR") & (df["year"] == 2024), "quality_flag"] = "FAIL"
    res = run_q1(df, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    # Baseline from fixture is 2022+; quality fail on 2024 should not create illegal NaN-based bascule
    assert "Q1_CAPTURE_NAN_BASCULE" not in [c.get("code") for c in res.checks]
