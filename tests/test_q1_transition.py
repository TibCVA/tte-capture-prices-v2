from __future__ import annotations

from src.modules.q1_transition import run_q1


def test_q1_transition_classification(annual_panel_fixture):
    assumptions = __import__("pandas").read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q1(annual_panel_fixture, assumptions, {"countries": ["FR", "DE"], "years": [2021, 2022, 2023, 2024]}, "test")
    panel = res.tables["Q1_year_panel"]
    assert (panel["phase_market"] == "phase2").any()


def test_q1_bascule_year_first_year_condition(annual_panel_fixture):
    assumptions = __import__("pandas").read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q1(annual_panel_fixture, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    summary = res.tables["Q1_country_summary"]
    assert summary["bascule_year_market"].notna().all()
