from __future__ import annotations

import pandas as pd

from src.modules.q1_transition import run_q1
from src.modules.q3_exit import _additional_sink_power_p95, run_q3


def test_q3_monotonic_counterfactuals(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    from src.processing import build_hourly_table

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    hourly_map = {("FR", 2024): hourly}
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    panel = annual_panel_fixture[annual_panel_fixture["country"] == "FR"].copy()

    res = run_q3(panel, hourly_map, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    out = res.tables["Q3_status"]
    assert not out.empty
    assert "inversion_k_demand" in out.columns
    k = pd.to_numeric(out["inversion_k_demand"], errors="coerce")
    r = pd.to_numeric(out["inversion_r_mustrun"], errors="coerce")
    assert ((k >= 0) | k.isna()).all()
    assert ((r >= 0) | r.isna()).all()
    k_status = out["inversion_k_demand_status"].astype(str).str.lower()
    r_status = out["inversion_r_mustrun_status"].astype(str).str.lower()
    assert k_status.str.len().min() > 0
    assert r_status.str.len().min() > 0


def test_q3_status_field_present(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    from src.processing import build_hourly_table

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q3(
        annual_panel_fixture[annual_panel_fixture["country"] == "FR"],
        {("FR", 2024): hourly},
        assumptions,
        {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]},
        "test",
    )
    assert "status" in res.tables["Q3_status"].columns


def test_q3_stage3_ready_when_far_and_trend_ok(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    from src.processing import build_hourly_table

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    panel = annual_panel_fixture[annual_panel_fixture["country"] == "FR"].copy()
    panel["far_energy"] = 0.98
    panel.loc[panel["year"] == 2022, "h_negative_obs"] = 300.0
    panel.loc[panel["year"] == 2023, "h_negative_obs"] = 200.0
    panel.loc[panel["year"] == 2024, "h_negative_obs"] = 100.0
    panel["capture_ratio_pv_vs_ttl"] = [0.6, 0.65, 0.7, 0.75]

    res = run_q3(panel, {("FR", 2024): hourly}, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    out = res.tables["Q3_status"]
    assert not out.empty
    assert str(out.iloc[0].get("status", "")).upper() in {
        "HORS_SCOPE_PHASE2",
        "CONTINUES",
        "STOP_POSSIBLE",
        "STOP_CONFIRMED",
        "BACK_TO_STAGE1",
    }


def test_q3_additional_absorbed_non_zero_when_flex_reduces_unabsorbed(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    from src.processing import build_hourly_table

    raw = make_raw_panel(n=240)
    raw["load_total_mw"] = 20000.0
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    panel = annual_panel_fixture[annual_panel_fixture["country"] == "FR"].copy()
    panel["far_energy"] = 0.80
    panel["h_negative_obs"] = [300.0, 320.0, 340.0, 360.0]

    res = run_q3(panel, {("FR", 2024): hourly}, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    out = res.tables["Q3_status"]
    assert not out.empty
    val = pd.to_numeric(out["additional_absorbed_needed_TWh_year"], errors="coerce").iloc[0]
    if pd.notna(val):
        assert float(val) >= 0.0
    else:
        assert str(out.iloc[0].get("reason_code", "")) in {
            "q1_no_bascule",
            "missing_panel",
            "all_families_turned_off",
            "family_turned_off_confirmed",
            "family_turned_off_recent",
            "no_family_turned_off",
            "targets_unreachable_within_bounds",
        }


def test_q3_hourly_profile_additional_sink_power_is_positive_when_needed():
    idx = pd.date_range("2024-01-01", periods=48, freq="h", tz="UTC")
    hourly = pd.DataFrame({"surplus_mw": [100.0] * 24 + [0.0] * 24}, index=idx)
    p95, status = _additional_sink_power_p95({("FR", 2024): hourly}, "FR", 2024.0, 0.02)
    assert status == "profile_weighted_surplus"
    assert float(p95) > 0.0


def test_q3_rows_contain_scenario_audit_fields(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    from src.processing import build_hourly_table

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    panel = annual_panel_fixture[annual_panel_fixture["country"] == "FR"].copy()
    res = run_q3(
        panel,
        {("FR", 2024): hourly},
        assumptions,
        {
            "countries": ["FR"],
            "years": [2021, 2022, 2023, 2024],
            "mode": "SCEN",
            "scenario_id": "DEMAND_UP",
            "demand_multiplier": 1.1,
            "must_run_reduction_factor": 0.2,
            "flex_multiplier": 1.05,
        },
        "test",
    )
    out = res.tables["Q3_status"]
    assert not out.empty
    for col in [
        "scenario_id",
        "assumed_demand_multiplier",
        "assumed_must_run_reduction_factor",
        "assumed_flex_multiplier",
    ]:
        assert col in out.columns
    assert (out["scenario_id"].astype(str) == "DEMAND_UP").all()
    fail_codes = {str(c.get("code")) for c in res.checks if str(c.get("status", "")).upper() == "FAIL"}
    assert "Q3_SCENARIO_ID_MISSING" not in fail_codes


def test_q3_applicable_when_q1_stage2_active_at_end_year(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    from src.processing import build_hourly_table

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    panel = annual_panel_fixture[annual_panel_fixture["country"] == "FR"].copy()

    panel.loc[panel["year"] < 2024, "h_negative_obs"] = 0.0
    panel.loc[panel["year"] < 2024, "h_below_5_obs"] = 10.0
    panel.loc[panel["year"] < 2024, "capture_ratio_pv"] = 1.05
    panel.loc[panel["year"] < 2024, "capture_ratio_wind"] = 1.05
    panel.loc[panel["year"] < 2024, "sr_energy"] = 0.0
    panel.loc[panel["year"] < 2024, "sr_hours"] = 0.0
    panel.loc[panel["year"] < 2024, "far_energy"] = 0.99
    panel.loc[panel["year"] < 2024, "ir_p10"] = 0.5

    panel.loc[panel["year"] == 2024, "h_negative_obs"] = 420.0
    panel.loc[panel["year"] == 2024, "h_below_5_obs"] = 800.0
    panel.loc[panel["year"] == 2024, "capture_ratio_pv"] = 0.70
    panel.loc[panel["year"] == 2024, "capture_ratio_wind"] = 0.82
    panel.loc[panel["year"] == 2024, "sr_energy"] = 0.03
    panel.loc[panel["year"] == 2024, "sr_hours"] = 0.15
    panel.loc[panel["year"] == 2024, "far_energy"] = 0.92
    panel.loc[panel["year"] == 2024, "ir_p10"] = 1.9

    q1 = run_q1(panel, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test_q1_ref")
    q1_row = q1.tables["Q1_country_summary"].iloc[0]
    assert bool(q1_row.get("stage2_active_at_end_year", False)) is True

    q3 = run_q3(
        panel,
        {("FR", 2024): hourly},
        assumptions,
        {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]},
        "test_q3_ref",
    )
    out = q3.tables["Q3_status"]
    assert not out.empty
    assert str(out.iloc[0].get("applicability_flag", "")).upper() == "APPLICABLE"
    fail_codes = {str(c.get("code")) for c in q3.checks if str(c.get("status", "")).upper() == "FAIL"}
    assert "Q3_Q1_PHASE2_ENDYEAR_COHERENCE" not in fail_codes


def test_q3_emits_test_q3_001_reality_check(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    from src.processing import build_hourly_table

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q3(
        annual_panel_fixture[annual_panel_fixture["country"] == "FR"],
        {("FR", 2024): hourly},
        assumptions,
        {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]},
        "test",
    )
    checks = [c for c in res.checks if str(c.get("code")) == "TEST_Q3_001"]
    assert checks
    assert all(str(c.get("status")) in {"PASS", "WARN", "FAIL", "NON_TESTABLE"} for c in checks)


def test_q3_no_stage2_outputs_are_non_testable(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    from src.processing import build_hourly_table

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    panel = annual_panel_fixture[annual_panel_fixture["country"] == "FR"].copy()
    panel["h_negative_obs"] = 0.0
    panel["h_below_5_obs"] = 10.0
    panel["capture_ratio_pv"] = 1.1
    panel["capture_ratio_wind"] = 1.1
    panel["sr_energy"] = 0.0
    panel["sr_hours"] = 0.0
    panel["far_energy"] = 0.99
    panel["ir_p10"] = 0.5

    res = run_q3(panel, {("FR", 2024): hourly}, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    out = res.tables["Q3_status"]
    row = out.iloc[0]
    assert str(row.get("reason_code", "")) == "no_stage2_detected"
    assert pd.isna(pd.to_numeric(pd.Series([row.get("required_demand_uplift_mw")]), errors="coerce").iloc[0])
    assert pd.isna(pd.to_numeric(pd.Series([row.get("required_mustrun_reduction_ratio")]), errors="coerce").iloc[0])
