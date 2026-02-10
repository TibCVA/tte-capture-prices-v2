from __future__ import annotations

from time import perf_counter

import pandas as pd

from src.config_loader import load_phase2_assumptions
from src.modules.question_bundle_runner import run_question_bundle
from src.processing import build_hourly_table


def test_q4_bundle_warm_run_is_faster(countries_cfg, thresholds_cfg, make_raw_panel, annual_panel_fixture):
    assumptions_phase1 = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions_phase2 = load_phase2_assumptions()

    raw = make_raw_panel(n=24 * 14, year=2024)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    hourly_hist_map = {("FR", 2024): hourly}

    selection = {
        "country": "FR",
        "countries": ["FR"],
        "year": 2024,
        "years": [2024],
        "objective": "FAR_TARGET",
        "power_grid": [0.0, 500.0, 1000.0, 2000.0],
        "duration_grid": [2.0, 4.0],
        "scenario_ids": [],
        "scenario_years": [2040],
        "horizon_year": 2040,
    }

    t0 = perf_counter()
    b1 = run_question_bundle(
        question_id="Q4",
        annual_hist=annual_panel_fixture,
        hourly_hist_map=hourly_hist_map,
        assumptions_phase1=assumptions_phase1,
        assumptions_phase2=assumptions_phase2,
        selection=selection,
        run_id="Q4_PERF_TEST_1",
    )
    dt1 = perf_counter() - t0

    t1 = perf_counter()
    b2 = run_question_bundle(
        question_id="Q4",
        annual_hist=annual_panel_fixture,
        hourly_hist_map=hourly_hist_map,
        assumptions_phase1=assumptions_phase1,
        assumptions_phase2=assumptions_phase2,
        selection=selection,
        run_id="Q4_PERF_TEST_2",
    )
    dt2 = perf_counter() - t1

    assert b1.hist_result.module_id == "Q4"
    assert b2.hist_result.module_id == "Q4"
    assert dt2 <= (dt1 + 0.5)
