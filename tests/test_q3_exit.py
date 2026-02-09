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
    panel.loc[panel["year"] < 2024, "country"] = "FR"

    res = run_q3(panel, hourly_map, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    out = res.tables["Q3_status"]
    assert not out.empty
    assert "inversion_k_demand" in out.columns
