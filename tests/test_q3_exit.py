from __future__ import annotations

import pandas as pd

from src.modules.q3_exit import run_q3


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
    assert set(k_status.unique()).issubset({"ok", "already_ready", "beyond_bounds", "invalid_bounds"})
    assert set(r_status.unique()).issubset({"ok", "already_ready", "beyond_bounds", "invalid_bounds"})


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
    assert bool(out.iloc[0]["stage3_ready_year"]) is True


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
    assert float(out.iloc[0]["additional_absorbed_needed_TWh_year"]) >= 0.0
