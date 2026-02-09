from __future__ import annotations

import pandas as pd

from src.modules.q5_thermal_anchor import run_q5
from src.processing import build_hourly_table


def test_q5_sensitivities_positive(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    commodity = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=20, freq="D"), "gas_price_eur_mwh_th": 35.0, "co2_price_eur_t": 80.0})
    res = run_q5(hourly, assumptions, {"country": "FR", "year": 2024, "marginal_tech": "CCGT"}, "test", commodity_daily=commodity, ttl_target_eur_mwh=120)
    row = res.tables["Q5_summary"].iloc[0]
    assert row["dTCA_dCO2"] > 0
    assert row["dTCA_dGas"] > 0


def test_q5_co2_required_increases_with_target(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    commodity = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=20, freq="D"), "gas_price_eur_mwh_th": 35.0, "co2_price_eur_t": 80.0})
    a = run_q5(hourly, assumptions, {"country": "FR", "year": 2024, "marginal_tech": "CCGT"}, "test", commodity_daily=commodity, ttl_target_eur_mwh=100)
    b = run_q5(hourly, assumptions, {"country": "FR", "year": 2024, "marginal_tech": "CCGT"}, "test", commodity_daily=commodity, ttl_target_eur_mwh=130)
    assert b.tables["Q5_summary"].iloc[0]["co2_required_base"] >= a.tables["Q5_summary"].iloc[0]["co2_required_base"]
