from __future__ import annotations

import pandas as pd

from src.modules.q2_slope import run_q2


def test_q2_slope_basic(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q2(annual_panel_fixture, assumptions, {"countries": ["FR", "DE"]}, "test")
    out = res.tables["Q2_country_slopes"]
    assert not out.empty
    assert "slope" in out.columns
    assert "phase2_start_year_for_slope" in out.columns
    assert "years_used" in out.columns
    assert "surplus_load_trough_share_phase2" in out.columns


def test_q2_fragile_when_low_n(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    df = annual_panel_fixture[annual_panel_fixture["year"] >= 2024].copy()
    res = run_q2(df, assumptions, {"countries": ["FR"]}, "test")
    if not res.tables["Q2_country_slopes"].empty:
        allowed = {"FRAGILE", "NON_TESTABLE"}
        assert set(res.tables["Q2_country_slopes"]["robust_flag"].astype(str).unique()).issubset(allowed)


def test_q2_fallback_axis_sr_energy(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    df = annual_panel_fixture.copy()
    df["pv_penetration_pct_gen"] = pd.NA
    df["wind_penetration_pct_gen"] = pd.NA
    res = run_q2(df, assumptions, {"countries": ["FR"]}, "test")
    out = res.tables["Q2_country_slopes"]
    assert not out.empty
    assert (out["x_axis_used"] == "sr_energy").all()


def test_q2_outlier_columns_present(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q2(annual_panel_fixture, assumptions, {"countries": ["FR"]}, "test")
    out = res.tables["Q2_country_slopes"]
    assert not out.empty
    assert {"slope_all_years", "slope_excluding_outliers", "outlier_years_count"}.issubset(out.columns)


def test_q2_n_lt_3_has_nan_pvalue_and_no_ols(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    df = annual_panel_fixture[annual_panel_fixture["year"] >= 2023].copy()
    res = run_q2(df, assumptions, {"countries": ["FR"]}, "test")
    out = res.tables["Q2_country_slopes"]
    if out.empty:
        return
    low_n = out[pd.to_numeric(out["n"], errors="coerce") < 3]
    if low_n.empty:
        return
    assert (~low_n["slope_method"].astype(str).eq("ols")).all()
    assert pd.to_numeric(low_n["p_value"], errors="coerce").isna().all()


def test_q2_two_point_slope_is_finite_when_x_varies(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    df = annual_panel_fixture.copy()
    df = df[df["year"].isin([2023, 2024])].copy()
    res = run_q2(df, assumptions, {"countries": ["FR"]}, "test")
    out = res.tables["Q2_country_slopes"]
    if out.empty:
        return
    two_pt = out[out["slope_method"].astype(str) == "two_point_delta"]
    if two_pt.empty:
        return
    assert pd.to_numeric(two_pt["slope"], errors="coerce").notna().all()
