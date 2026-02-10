from __future__ import annotations

import pandas as pd

from src.modules.q1_transition import run_q1
from src.processing import build_hourly_table


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


def test_q1_new_tables_present_and_before_after_windows(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q1(annual_panel_fixture, assumptions, {"countries": ["FR", "DE"], "years": [2021, 2022, 2023, 2024]}, "test")

    expected_tables = {
        "Q1_rule_definition",
        "Q1_rule_application",
        "Q1_before_after_bascule",
        "Q1_scope_audit",
        "Q1_ir_diagnostics",
    }
    assert expected_tables.issubset(set(res.tables.keys()))

    before_after = res.tables["Q1_before_after_bascule"]
    assert not before_after.empty
    fr = before_after[before_after["country"] == "FR"].iloc[0]
    assert int(fr["pre_window_start_year"]) == int(fr["bascule_year_market"] - 3)
    assert int(fr["pre_window_end_year"]) == int(fr["bascule_year_market"] - 1)
    assert int(fr["post_window_start_year"]) == int(fr["bascule_year_market"])
    assert int(fr["post_window_end_year"]) == int(fr["bascule_year_market"] + 2)


def test_q1_scope_review_check_triggers(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    raw = make_raw_panel(n=168, year=2024)
    hourly = build_hourly_table(raw, "DE", 2024, countries_cfg["countries"]["DE"], thresholds_cfg, "DE")
    hourly_map = {("DE", 2024): hourly}

    res = run_q1(
        annual_panel_fixture,
        assumptions,
        {"countries": ["DE"], "years": [2024]},
        "test",
        hourly_by_country_year=hourly_map,
    )

    codes = [str(c.get("code")) for c in res.checks]
    assert "Q1_MR_SCOPE_REVIEW" in codes
    scope = res.tables["Q1_scope_audit"]
    assert not scope.empty
    assert float(scope.iloc[0]["scope_coverage_ratio"]) < 0.70
