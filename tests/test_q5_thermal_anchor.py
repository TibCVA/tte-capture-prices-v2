from __future__ import annotations

import pandas as pd

from src.modules.q5_thermal_anchor import run_q5
from src.processing import build_hourly_table


def test_q5_sensitivities_positive(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    commodity = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 35.0,
            "co2_price_eur_t": 80.0,
        }
    )
    res = run_q5(
        hourly,
        assumptions,
        {"country": "FR", "year": 2024, "marginal_tech": "CCGT"},
        "test",
        commodity_daily=commodity,
        ttl_target_eur_mwh=120,
    )
    row = res.tables["Q5_summary"].iloc[0]
    assert row["dTCA_dCO2"] > 0
    assert row["dTCA_dFuel"] > 0
    assert row["dTCA_dGas"] > 0


def test_q5_co2_required_increases_with_target(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    commodity = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 35.0,
            "co2_price_eur_t": 80.0,
        }
    )
    a = run_q5(hourly, assumptions, {"country": "FR", "year": 2024, "marginal_tech": "CCGT"}, "test", commodity_daily=commodity, ttl_target_eur_mwh=100)
    b = run_q5(hourly, assumptions, {"country": "FR", "year": 2024, "marginal_tech": "CCGT"}, "test", commodity_daily=commodity, ttl_target_eur_mwh=130)
    assert b.tables["Q5_summary"].iloc[0]["co2_required_base"] >= a.tables["Q5_summary"].iloc[0]["co2_required_base"]


def test_q5_override_outputs(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    commodity = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 35.0,
            "co2_price_eur_t": 80.0,
        }
    )
    out = run_q5(
        hourly,
        assumptions,
        {"country": "FR", "year": 2024, "marginal_tech": "CCGT"},
        "test",
        commodity_daily=commodity,
        ttl_target_eur_mwh=120,
        gas_override_eur_mwh_th=45.0,
    ).tables["Q5_summary"].iloc[0]
    assert pd.notna(out["co2_required_gas_override"])


def test_q5_required_values_non_negative(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    commodity = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 35.0,
            "co2_price_eur_t": 80.0,
        }
    )
    out = run_q5(
        hourly,
        assumptions,
        {"country": "FR", "year": 2024, "marginal_tech": "CCGT"},
        "test",
        commodity_daily=commodity,
        ttl_target_eur_mwh=160.0,
    ).tables["Q5_summary"].iloc[0]
    assert float(out["required_co2_eur_t"]) >= 0.0
    assert float(out["required_gas_eur_mwh_th"]) >= 0.0
    assert "required_co2_abs_eur_t" in out.index
    assert "required_gas_abs_eur_mwh_th" in out.index


def test_q5_already_above_target_sets_required_zero(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    commodity = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 35.0,
            "co2_price_eur_t": 80.0,
        }
    )
    out = run_q5(
        hourly,
        assumptions,
        {"country": "FR", "year": 2024, "marginal_tech": "CCGT"},
        "test",
        commodity_daily=commodity,
        ttl_target_eur_mwh=60.0,
    ).tables["Q5_summary"].iloc[0]
    assert out["anchor_status"] == "already_above_target"
    assert float(out["delta_co2_vs_scenario"]) == 0.0
    assert float(out["delta_gas_vs_scenario"]) == 0.0


def test_q5_ttl_year_specific_consistent_with_annual_ttl(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    commodity = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 35.0,
            "co2_price_eur_t": 80.0,
        }
    )
    out = run_q5(
        hourly,
        assumptions,
        {
            "country": "FR",
            "year": 2024,
            "horizon_year": 2024,
            "marginal_tech": "CCGT",
            "ttl_reference_mode": "year_specific",
        },
        "test",
        commodity_daily=commodity,
        ttl_target_eur_mwh=140.0,
    ).tables["Q5_summary"].iloc[0]
    ttl_obs = float(out["ttl_obs"])
    ttl_annual = float(out["ttl_annual_metrics_same_year"])
    if abs(ttl_annual) > 1e-12:
        assert abs(ttl_obs - ttl_annual) / abs(ttl_annual) < 0.05


def test_q5_warns_on_implausible_implicit_efficiency(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions.loc[assumptions["param_name"] == "ccgt_efficiency", "param_value"] = 0.9
    commodity = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 35.0,
            "co2_price_eur_t": 80.0,
        }
    )
    res = run_q5(
        hourly,
        assumptions,
        {"country": "FR", "year": 2024, "marginal_tech": "CCGT"},
        "test",
        commodity_daily=commodity,
        ttl_target_eur_mwh=140.0,
    )
    codes = {str(c.get("code")) for c in res.checks}
    assert "Q5_IMPL_EFF_OUT_OF_RANGE" in codes


def test_q5_required_deltas_positive_when_target_above_anchor(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    commodity = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 35.0,
            "co2_price_eur_t": 80.0,
        }
    )
    out = run_q5(
        hourly,
        assumptions,
        {"country": "FR", "year": 2024, "marginal_tech": "CCGT", "scenario_id": "BASE", "mode": "SCEN"},
        "test",
        commodity_daily=commodity,
        ttl_target_eur_mwh=220.0,
    ).tables["Q5_summary"].iloc[0]
    assert float(out["ttl_target"]) > float(out["ttl_anchor_formula"])
    assert float(out["delta_co2_vs_scenario"]) > 0.0
    assert float(out["delta_gas_vs_scenario"]) > 0.0


def test_q5_summary_contains_scenario_audit_fields(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    commodity = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 35.0,
            "co2_price_eur_t": 80.0,
        }
    )
    out = run_q5(
        hourly,
        assumptions,
        {"country": "FR", "year": 2024, "marginal_tech": "CCGT", "scenario_id": "HIGH_CO2", "mode": "SCEN"},
        "test",
        commodity_daily=commodity,
        ttl_target_eur_mwh=140.0,
    ).tables["Q5_summary"].iloc[0]
    for col in [
        "scenario_id",
        "assumed_co2_price_eur_t",
        "assumed_gas_price_eur_mwh_th",
        "assumed_efficiency",
        "assumed_emission_factor_t_per_mwh_th",
        "chosen_anchor_tech",
    ]:
        assert col in out.index
    assert str(out["scenario_id"]) == "HIGH_CO2"
