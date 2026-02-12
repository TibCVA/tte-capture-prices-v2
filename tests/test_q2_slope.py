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
    assert set(out["x_axis_used"].astype(str).unique()).issubset(
        {"pv_penetration_share_load", "wind_penetration_share_load", "none"}
    )


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
    low_n = out[pd.to_numeric(out["n"], errors="coerce") < 4]
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
    endpoint = out[out["slope_method"].astype(str) == "endpoint_delta"]
    if endpoint.empty:
        return
    assert pd.to_numeric(endpoint["slope"], errors="coerce").notna().all()


def test_q2_fragile_rows_have_cross_country_benchmark(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q2(annual_panel_fixture, assumptions, {"countries": ["FR", "DE"]}, "test")
    out = res.tables["Q2_country_slopes"]
    if out.empty:
        return
    fragile = out[out["robust_flag"].astype(str) == "FRAGILE"]
    if fragile.empty:
        return
    assert fragile["cross_country_benchmark_slope"].notna().any()


def test_q2_default_excludes_2022_and_emits_check(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q2(annual_panel_fixture, assumptions, {"countries": ["FR"]}, "test")
    checks = [c for c in res.checks if str(c.get("code")) == "TEST_Q2_2022_001"]
    assert checks
    assert any(str(c.get("status")) == "PASS" for c in checks)
    out = res.tables["Q2_country_slopes"]
    if not out.empty:
        years_used = out["years_used"].astype(str).str.cat(sep=",")
        assert "2022" not in years_used


def test_q2_include_2022_sets_outlier_warning(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q2(
        annual_panel_fixture,
        assumptions,
        {"countries": ["FR"], "include_2022": True},
        "test",
    )
    assert "includes_2022_outlier" in [str(w) for w in res.warnings]
    warn_checks = [c for c in res.checks if str(c.get("code")) == "includes_2022_outlier"]
    assert warn_checks
    assert any(str(c.get("status")) == "WARN" for c in warn_checks)


def test_q2_warns_on_positive_slope_with_strong_negative_vre_load_corr():
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    rows = []
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    loads = [600.0, 550.0, 500.0, 450.0, 400.0, 350.0]
    for i, (year, load_twh) in enumerate(zip(years, loads)):
        rows.append(
            {
                "country": "FR",
                "year": year,
                "quality_flag": "OK",
                "completeness": 1.0,
                "sr_energy": 0.02,
                "sr_hours": 0.15,
                "far_energy": 0.90,
                "ir_p10": 0.8,
                "ttl_eur_mwh": 100.0,
                "capture_ratio_pv_vs_ttl": 0.70 + 0.05 * i,
                "capture_ratio_wind_vs_ttl": 0.80,
                "capture_ratio_pv": 0.70 + 0.05 * i,
                "capture_ratio_wind": 0.80,
                "h_negative_obs": 300.0,
                "h_below_5_obs": 700.0,
                "days_spread_gt50": 200.0,
                "pv_penetration_pct_gen": 0.10 + 0.02 * i,
                "wind_penetration_pct_gen": 0.20,
                "vre_penetration_proxy": 0.40,
                "nrl_price_corr": -0.30,
                "regime_coherence": 0.80,
                "load_net_twh": load_twh,
                "gen_vre_twh": 100.0 + 20.0 * i,
                "gen_solar_twh": (0.10 + 0.02 * i) * load_twh,
                "gen_wind_on_twh": 0.10 * load_twh,
                "gen_wind_off_twh": 0.05 * load_twh,
            }
        )
    annual = pd.DataFrame(rows)
    res = run_q2(annual, assumptions, {"countries": ["FR"]}, "test")
    warn_checks = [c for c in res.checks if str(c.get("code")) == "TEST_Q2_002"]
    assert warn_checks
    assert any(str(c.get("status")) == "WARN" for c in warn_checks)
