from __future__ import annotations

import numpy as np
import pandas as pd

from src.core.definitions import compute_core_hourly_definitions, sanity_check_core_definitions
from src.modules.q1_transition import _drivers_at_bascule, _quality_flags_from_row, run_q1
from src.modules.q3_exit import run_q3
from src.modules.q4_bess import run_q4
from src.modules.q5_thermal_anchor import run_q5
from src.processing import build_hourly_table


def _assumptions() -> pd.DataFrame:
    return pd.read_csv("data/assumptions/phase1_assumptions.csv")


def test_core_export_sign_convention_from_net_position():
    idx = pd.date_range("2024-01-01", periods=2, freq="h", tz="UTC")
    df = pd.DataFrame(
        {
            "load_total_mw": [1000.0, 1000.0],
            "psh_pump_mw": [100.0, 100.0],
            "gen_solar_mw": [0.0, 0.0],
            "gen_wind_on_mw": [0.0, 0.0],
            "gen_wind_off_mw": [0.0, 0.0],
            "net_position_mw": [200.0, -150.0],
        },
        index=idx,
    )
    out_pos = compute_core_hourly_definitions(df, net_position_positive_is_export=True)
    out_neg = compute_core_hourly_definitions(df, net_position_positive_is_export=False)

    exp_pos = pd.to_numeric(out_pos["export_sink_mw"], errors="coerce")
    exp_neg = pd.to_numeric(out_neg["export_sink_mw"], errors="coerce")
    assert float(exp_pos.iloc[0]) == 200.0
    assert float(exp_pos.iloc[1]) == 0.0
    assert float(exp_neg.iloc[0]) == 0.0
    assert float(exp_neg.iloc[1]) == 150.0


def test_core_far_near_one_requires_near_zero_unabsorbed():
    df = pd.DataFrame(
        {
            "surplus_mw": [10.0, 10.0],
            "surplus_absorbed_mw": [10.0, 10.0],
            "surplus_unabsorbed_mw": [1.0, 0.5],
            "gen_must_run_mw": [0.0, 0.0],
            "gen_total_mw": [100.0, 100.0],
            "load_total_mw": [1000.0, 1000.0],
            "load_mw": [900.0, 900.0],
            "exports_mw": [0.0, 0.0],
            "psh_pump_mw": [0.0, 0.0],
        }
    )
    issues = sanity_check_core_definitions(df, far_energy=1.0, sr_energy=0.0, ir=0.0)
    assert any("FAR~1" in issue for issue in issues)


def test_q1_low_residual_bucket_not_systematically_zero(annual_panel_fixture):
    panel = annual_panel_fixture[annual_panel_fixture["country"] == "FR"].copy()
    panel = panel[panel["year"] == 2024].copy()
    idx = pd.date_range("2024-01-01", periods=12, freq="h", tz="UTC")
    hourly = pd.DataFrame(
        {
            "price_da_eur_mwh": [-20.0, -10.0, 10.0, 30.0, 40.0, 50.0, -5.0, 15.0, 60.0, 55.0, 45.0, 35.0],
            "regime": ["C", "C", "A", "B", "B", "C", "C", "A", "B", "C", "C", "C"],
            "low_residual_hour": [True, True, False, False, False, False, True, False, False, False, False, False],
        },
        index=idx,
    )
    res = run_q1(
        panel,
        _assumptions(),
        {"countries": ["FR"], "years": [2024]},
        "q1_low_residual_test",
        hourly_by_country_year={("FR", 2024): hourly},
    )
    explain = res.tables["q1_negative_price_explainability"]
    assert not explain.empty
    row = explain.iloc[0]
    assert float(row["share_neg_hours_in_low_residual_bucket"]) > 0.0
    assert float(row["share_neg_hours_explained_union"]) <= 1.000001
    assert float(row["share_neg_hours_unexplained"]) >= -1e-9


def test_q1_unexplained_negative_is_quality_flag_not_driver():
    row = pd.Series(
        {
            "low_price_family": False,
            "value_family_pv": False,
            "value_family_wind": False,
            "physical_family": False,
            "flag_unexplained_negative_prices": True,
            "share_neg_hours_unexplained": 0.7,
        }
    )
    drivers = _drivers_at_bascule(row, {})
    flags = _quality_flags_from_row(row)
    assert "UNEXPLAINED_NEGATIVE_PRICES" not in str(drivers)
    assert "UNEXPLAINED_NEGATIVE_PRICES" in str(flags)


def test_q3_required_uplift_nan_only_for_allowed_statuses(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    panel = annual_panel_fixture[annual_panel_fixture["country"] == "FR"].copy()
    panel["is_phase2_market"] = True
    raw = make_raw_panel(n=240, year=2024)
    raw.loc[raw.index[:120], "price_da_eur_mwh"] = -15.0
    raw.loc[raw.index[120:], "price_da_eur_mwh"] = 80.0
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    res = run_q3(
        panel,
        {("FR", 2024): hourly},
        _assumptions(),
        {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]},
        "q3_required_uplift_statuses",
    )
    req = res.tables["q3_inversion_requirements"].copy()
    status = req["status"].astype(str).str.lower()
    upl = pd.to_numeric(req["required_uplift"], errors="coerce")
    bad = req[upl.isna() & ~status.isin(["not_achievable", "missing_data"])]
    assert bad.empty


def test_q3_predicted_h_negative_country_specific(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    base = annual_panel_fixture[annual_panel_fixture["country"] == "FR"].copy()
    de = base.copy()
    de["country"] = "DE"
    es = base.copy()
    es["country"] = "ES"
    panel = pd.concat([de, es], ignore_index=True)
    panel["is_phase2_market"] = True

    idx = pd.date_range("2024-01-01", periods=240, freq="h", tz="UTC")
    hourly_de = pd.DataFrame(
        {
            "load_total_mw": 3000.0,
            "psh_pump_mw": 0.0,
            "gen_solar_mw": 1200.0,
            "gen_wind_on_mw": 800.0,
            "gen_wind_off_mw": 200.0,
            "gen_must_run_mw": 2500.0,
            "net_position_mw": 0.0,
            "nrl_mw": np.r_[np.full(180, -1700.0), np.full(60, -200.0)],
            "price_da_eur_mwh": np.r_[np.full(180, -25.0), np.full(60, 15.0)],
        },
        index=idx,
    )
    hourly_es = pd.DataFrame(
        {
            "load_total_mw": 9000.0,
            "psh_pump_mw": 0.0,
            "gen_solar_mw": 1200.0,
            "gen_wind_on_mw": 800.0,
            "gen_wind_off_mw": 200.0,
            "gen_must_run_mw": 1500.0,
            "net_position_mw": 0.0,
            "nrl_mw": np.r_[np.full(40, -100.0), np.full(100, 200.0), np.full(100, 500.0)],
            "price_da_eur_mwh": np.r_[np.full(40, -2.0), np.full(100, 2.0), np.full(100, 70.0)],
        },
        index=idx,
    )

    res = run_q3(
        panel,
        {("DE", 2024): hourly_de, ("ES", 2024): hourly_es},
        _assumptions(),
        {"countries": ["DE", "ES"], "years": [2021, 2022, 2023, 2024]},
        "q3_country_specific",
    )
    req = res.tables["q3_inversion_requirements"].copy()
    dem = req[req["lever"].astype(str) == "demand_uplift"].copy()
    dem = dem[dem["country"].astype(str).isin(["DE", "ES"])]
    if len(dem) >= 2:
        metric_cols = ["predicted_h_negative_after", "predicted_h_below_5_after", "predicted_sr_after"]
        vectors: list[tuple[float, ...]] = []
        for _, row in dem.iterrows():
            vec = tuple(float(pd.to_numeric(pd.Series([row.get(c)]), errors="coerce").iloc[0]) for c in metric_cols)
            vectors.append(vec)
        if len(vectors) >= 2:
            assert len(set(vectors)) > 1


def test_q4_h_below_5_proxy_after_ge_h_negative_after(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    import src.modules.q4_bess as q4_module

    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240, year=2024)
    raw.loc[raw.index[:80], "price_da_eur_mwh"] = -5.0
    raw.loc[raw.index[80:180], "price_da_eur_mwh"] = 2.0
    raw.loc[raw.index[180:], "price_da_eur_mwh"] = 70.0
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    res = run_q4(
        hourly,
        _assumptions(),
        {"country": "FR", "year": 2024, "objective": "LOW_PRICE_TARGET", "force_recompute": True},
        "q4_hbelow_ge_hneg",
        dispatch_mode="SURPLUS_FIRST",
    )
    frontier = res.tables["Q4_bess_frontier"].copy()
    hneg = pd.to_numeric(frontier["h_negative_after"], errors="coerce")
    h5 = pd.to_numeric(frontier["h_below_5_after"], errors="coerce")
    assert (h5 >= hneg).fillna(True).all()


def test_q4_no_default_250mw_when_frontier_only_zero(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    import src.modules.q4_bess as q4_module

    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240, year=2024)
    raw.loc[raw.index[:120], "price_da_eur_mwh"] = -10.0
    raw.loc[raw.index[120:], "price_da_eur_mwh"] = 60.0
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    res = run_q4(
        hourly,
        _assumptions(),
        {
            "country": "FR",
            "year": 2024,
            "objective": "LOW_PRICE_TARGET",
            "power_grid": [0.0],
            "duration_grid": [0.0],
            "force_recompute": True,
        },
        "q4_no_default_250",
        dispatch_mode="SURPLUS_FIRST",
    )
    frontier = res.tables["Q4_bess_frontier"].copy()
    summary = res.tables["Q4_sizing_summary"].iloc[0]
    required_power = pd.to_numeric(pd.Series([summary.get("required_bess_power_mw")]), errors="coerce").iloc[0]
    frontier_power = pd.to_numeric(frontier.get("bess_power_mw_test", frontier.get("bess_power_mw")), errors="coerce").fillna(0.0)
    only_zero_frontier = (frontier_power.abs() <= 1e-9).all()
    assert not (pd.notna(required_power) and abs(float(required_power) - 250.0) <= 1e-9)
    if only_zero_frontier:
        assert (pd.isna(required_power)) or (abs(float(required_power)) <= 1e-9) or (str(summary.get("status", "")).lower() in {"not_sensitive", "not_applicable"})


def test_q5_missing_base_explicit_status_and_nan_deltas(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240, year=2024)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    commodity = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 45.0,
            "co2_price_eur_t": 120.0,
        }
    )
    row = run_q5(
        hourly,
        _assumptions(),
        {"country": "FR", "year": 2024, "mode": "SCEN", "scenario_id": "HIGH_CO2"},
        "q5_missing_base",
        commodity_daily=commodity,
    ).tables["Q5_summary"].iloc[0]
    assert str(row["status"]).lower() == "missing_base"
    assert pd.isna(row["delta_tca_vs_base"])
    assert pd.isna(row["delta_ttl_model_vs_base"])


def test_q5_base_provided_produces_finite_deltas_and_method(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240, year=2024)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = _assumptions()
    commodity_base = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 35.0,
            "co2_price_eur_t": 80.0,
        }
    )
    commodity_scen = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 45.0,
            "co2_price_eur_t": 120.0,
        }
    )
    base = run_q5(
        hourly,
        assumptions,
        {"country": "FR", "year": 2024, "mode": "SCEN", "scenario_id": "BASE"},
        "q5_base_for_delta",
        commodity_daily=commodity_base,
    ).tables["Q5_summary"].iloc[0]
    scen = run_q5(
        hourly,
        assumptions,
        {
            "country": "FR",
            "year": 2024,
            "mode": "SCEN",
            "scenario_id": "HIGH_BOTH",
            "base_tca_eur_mwh": float(base["tca_current_eur_mwh"]),
            "base_tca_ccgt_eur_mwh": float(base["tca_ccgt_eur_mwh"]),
            "base_tca_coal_eur_mwh": float(base["tca_coal_eur_mwh"]),
            "base_ttl_model_eur_mwh": float(base["ttl_model_eur_mwh"]),
            "base_gas_eur_per_mwh_th": float(base["assumed_gas_price_eur_mwh_th"]),
            "base_co2_eur_per_t": float(base["assumed_co2_price_eur_t"]),
        },
        "q5_scen_for_delta",
        commodity_daily=commodity_scen,
    ).tables["Q5_summary"].iloc[0]
    assert str(scen["status"]).lower() == "ok"
    assert pd.notna(scen["delta_tca_vs_base"])
    assert pd.notna(scen["delta_ttl_model_vs_base"])
    assert str(scen["ttl_proxy_method"]).strip() != ""
    assert float(scen["ttl_model_eur_mwh"]) >= 0.0
