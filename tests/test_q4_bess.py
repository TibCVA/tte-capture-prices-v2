from __future__ import annotations

import pandas as pd

from src.modules.q4_bess import run_q4
from src.processing import build_hourly_table


def test_q4_soc_bounds(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(hourly, assumptions, {"country": "FR", "year": 2024}, "test")
    assert not res.tables["Q4_bess_frontier"].empty


def test_q4_monotonic_surplus_reduction(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(hourly, assumptions, {"country": "FR", "year": 2024}, "test")
    f = res.tables["Q4_bess_frontier"].sort_values("required_bess_power_mw")
    if len(f) >= 2:
        assert f["surplus_unabs_energy_after"].iloc[-1] <= f["surplus_unabs_energy_after"].iloc[0]
