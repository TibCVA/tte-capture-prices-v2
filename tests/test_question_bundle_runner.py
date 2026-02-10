from __future__ import annotations

import pandas as pd

from src.config_loader import load_phase2_assumptions
from src.modules.question_bundle_runner import _annotate_comparison_interpretability, run_question_bundle
from src.processing import build_hourly_table


def _build_hourly_map_for_fixture(
    countries_cfg: dict,
    thresholds_cfg: dict,
    make_raw_panel,
    countries: list[str],
    years: list[int],
) -> dict[tuple[str, int], pd.DataFrame]:
    out: dict[tuple[str, int], pd.DataFrame] = {}
    for country in countries:
        cfg = countries_cfg["countries"][country]
        for year in years:
            raw = make_raw_panel(n=168, year=year)
            out[(country, year)] = build_hourly_table(raw, country, year, cfg, thresholds_cfg, country)
    return out


def test_run_question_bundle_q1_hist_and_scen(
    annual_panel_fixture,
    countries_cfg,
    thresholds_cfg,
    make_raw_panel,
):
    assumptions_phase1 = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions_phase2 = load_phase2_assumptions()
    hourly_hist_map = _build_hourly_map_for_fixture(
        countries_cfg=countries_cfg,
        thresholds_cfg=thresholds_cfg,
        make_raw_panel=make_raw_panel,
        countries=["FR", "DE"],
        years=[2021, 2022, 2023, 2024],
    )

    bundle = run_question_bundle(
        question_id="Q1",
        annual_hist=annual_panel_fixture,
        hourly_hist_map=hourly_hist_map,
        assumptions_phase1=assumptions_phase1,
        assumptions_phase2=assumptions_phase2,
        selection={
            "countries": ["FR", "DE"],
            "years": [2021, 2022, 2023, 2024],
            "scenario_ids": ["BASE"],
            "scenario_years": [2030, 2040],
        },
        run_id="TEST_BUNDLE_Q1",
    )

    assert bundle.question_id == "Q1"
    assert bundle.hist_result.module_id == "Q1"
    assert "BASE" in bundle.scen_results
    assert not bundle.test_ledger.empty
    assert {"test_id", "mode", "status"}.issubset(bundle.test_ledger.columns)


def test_run_question_bundle_q4_executes_hist_modes(
    annual_panel_fixture,
    countries_cfg,
    thresholds_cfg,
    make_raw_panel,
):
    assumptions_phase1 = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions_phase2 = load_phase2_assumptions()
    hourly_hist_map = _build_hourly_map_for_fixture(
        countries_cfg=countries_cfg,
        thresholds_cfg=thresholds_cfg,
        make_raw_panel=make_raw_panel,
        countries=["FR"],
        years=[2024],
    )

    bundle = run_question_bundle(
        question_id="Q4",
        annual_hist=annual_panel_fixture,
        hourly_hist_map=hourly_hist_map,
        assumptions_phase1=assumptions_phase1,
        assumptions_phase2=assumptions_phase2,
        selection={
            "country": "FR",
            "countries": ["FR"],
            "year": 2024,
            "years": [2024],
            "objective": "FAR_TARGET",
            "power_grid": [0.0, 200.0, 500.0],
            "duration_grid": [2.0, 4.0],
            "scenario_ids": [],
            "scenario_years": [2040],
            "horizon_year": 2040,
        },
        run_id="TEST_BUNDLE_Q4",
    )

    assert bundle.question_id == "Q4"
    assert bundle.hist_result.module_id == "Q4"
    assert not bundle.test_ledger.empty
    assert "Q4-H-01" in bundle.test_ledger["test_id"].tolist()


def test_q3_comparison_annotation_flags_non_testable_and_fragile() -> None:
    raw = pd.DataFrame(
        [
            {
                "country": "FR",
                "scenario_id": "BASE",
                "metric": "inversion_k_demand",
                "hist_value": 0.10,
                "scen_value": 0.15,
                "delta": 0.05,
                "scen_status": "hors_scope_stage2",
            },
            {
                "country": "DE",
                "scenario_id": "BASE",
                "metric": "inversion_k_demand",
                "hist_value": 0.20,
                "scen_value": 0.20,
                "delta": 0.0,
                "scen_status": "stabilisation",
            },
            {
                "country": "ES",
                "scenario_id": "BASE",
                "metric": "inversion_k_demand",
                "hist_value": 0.10,
                "scen_value": 0.25,
                "delta": 0.15,
                "scen_status": "amelioration",
            },
        ]
    )
    out = _annotate_comparison_interpretability("Q3", raw)
    assert {"interpretability_status", "interpretability_reason"}.issubset(out.columns)
    assert out.loc[out["country"] == "FR", "interpretability_status"].iloc[0] == "NON_TESTABLE"
    assert out.loc[out["country"] == "DE", "interpretability_status"].iloc[0] == "FRAGILE"
    assert out.loc[out["country"] == "ES", "interpretability_status"].iloc[0] == "INFORMATIVE"
