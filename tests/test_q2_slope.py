from __future__ import annotations

from src.modules.q2_slope import run_q2


def test_q2_slope_basic(annual_panel_fixture):
    assumptions = __import__("pandas").read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q2(annual_panel_fixture, assumptions, {"countries": ["FR", "DE"]}, "test")
    out = res.tables["Q2_country_slopes"]
    assert not out.empty
    assert "slope" in out.columns


def test_q2_fragile_when_low_n(annual_panel_fixture):
    assumptions = __import__("pandas").read_csv("data/assumptions/phase1_assumptions.csv")
    df = annual_panel_fixture[annual_panel_fixture["year"] >= 2024].copy()
    res = run_q2(df, assumptions, {"countries": ["FR"]}, "test")
    if not res.tables["Q2_country_slopes"].empty:
        assert (res.tables["Q2_country_slopes"]["robust_flag"] == "FRAGILE").all()
