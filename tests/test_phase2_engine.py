from __future__ import annotations

import pandas as pd

import src.storage as storage_module
from src.processing import build_hourly_table
from src.scenario.phase2_engine import run_phase2_scenario


def test_phase2_engine_runs_and_persists_outputs(
    annual_panel_fixture,
    make_raw_panel,
    countries_cfg,
    thresholds_cfg,
    tmp_path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(storage_module, "SCENARIO_BASE", tmp_path / "scenario")

    raw = make_raw_panel(n=240, year=2024)
    ref_hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    hourly_hist_map = {("FR", 2024): ref_hourly}

    p2 = pd.read_csv("data/assumptions/phase2/phase2_scenario_country_year.csv")
    row = p2[(p2["scenario_id"] == "BASE") & (p2["country"] == "FR") & (p2["year"] == 2030)].head(1).copy()
    row.loc[:, "scenario_id"] = "TEST_SCEN"
    assumptions = row.copy()

    out = run_phase2_scenario(
        scenario_id="TEST_SCEN",
        countries=["FR"],
        years=[2030],
        assumptions_phase2=assumptions,
        annual_hist=annual_panel_fixture,
        hourly_hist_map=hourly_hist_map,
    )

    assert "annual_metrics" in out
    annual = out["annual_metrics"]
    assert not annual.empty
    assert str(annual.iloc[0]["scenario_id"]) == "TEST_SCEN"
    assert str(annual.iloc[0]["mode"]) == "SCEN"

    hourly_path = storage_module.SCENARIO_BASE / "TEST_SCEN" / "hourly" / "FR" / "2030.parquet"
    annual_path = storage_module.SCENARIO_BASE / "TEST_SCEN" / "annual_metrics.parquet"
    findings_path = storage_module.SCENARIO_BASE / "TEST_SCEN" / "validation_findings.parquet"
    assert hourly_path.exists()
    assert annual_path.exists()
    assert findings_path.exists()


def test_phase2_engine_far_is_finite_when_surplus_exists(
    annual_panel_fixture,
    make_raw_panel,
    countries_cfg,
    thresholds_cfg,
    tmp_path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(storage_module, "SCENARIO_BASE", tmp_path / "scenario")

    raw = make_raw_panel(n=240, year=2024)
    ref_hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    hourly_hist_map = {("FR", 2024): ref_hourly}

    p2 = pd.read_csv("data/assumptions/phase2/phase2_scenario_country_year.csv")
    assumptions = p2[(p2["scenario_id"] == "BASE") & (p2["country"] == "FR") & (p2["year"] == 2030)].head(1).copy()
    assumptions.loc[:, "scenario_id"] = "TEST_SCEN_FAR"

    out = run_phase2_scenario(
        scenario_id="TEST_SCEN_FAR",
        countries=["FR"],
        years=[2030],
        assumptions_phase2=assumptions,
        annual_hist=annual_panel_fixture,
        hourly_hist_map=hourly_hist_map,
    )
    annual = out["annual_metrics"]
    assert not annual.empty
    row = annual.iloc[0]
    if float(row["sr_energy"]) > 0:
        assert pd.notna(row["far_observed"])
        assert 0.0 <= float(row["far_observed"]) <= 1.0
