from __future__ import annotations

import numpy as np
import pandas as pd

from src.metrics import compute_annual_metrics
from src.modules.q1_transition import Q1_REASON_CODE_REQUIRED_METRICS, run_q1
from src.modules.q2_slope import run_q2
from src.modules.q3_exit import _compute_hourly_proxy_metrics, run_q3
from src.modules.q4_bess import run_q4
from src.modules.q5_thermal_anchor import run_q5
from src.processing import build_hourly_table


def _phase1_assumptions() -> pd.DataFrame:
    return pd.read_csv("data/assumptions/phase1_assumptions.csv")


def _annual_panel_for_modules(annual_panel_fixture: pd.DataFrame) -> pd.DataFrame:
    panel = annual_panel_fixture.copy()
    panel["scenario_id"] = "HIST"
    panel["capture_ratio_pv"] = pd.to_numeric(panel.get("capture_ratio_pv"), errors="coerce")
    panel["capture_ratio_pv"] = panel["capture_ratio_pv"].where(
        panel["capture_ratio_pv"].notna(),
        pd.to_numeric(panel.get("capture_ratio_pv_vs_ttl"), errors="coerce"),
    )
    panel["capture_ratio_wind"] = pd.to_numeric(panel.get("capture_ratio_wind"), errors="coerce")
    panel["capture_ratio_wind"] = panel["capture_ratio_wind"].where(
        panel["capture_ratio_wind"].notna(),
        pd.to_numeric(panel.get("capture_ratio_wind_vs_ttl"), errors="coerce"),
    )
    panel["far_observed"] = pd.to_numeric(panel.get("far_observed"), errors="coerce")
    panel["far_observed"] = panel["far_observed"].where(
        panel["far_observed"].notna(),
        pd.to_numeric(panel.get("far_energy"), errors="coerce"),
    )
    panel["sr_hours_share"] = pd.to_numeric(panel.get("sr_hours_share"), errors="coerce")
    panel["sr_hours_share"] = panel["sr_hours_share"].where(
        panel["sr_hours_share"].notna(),
        pd.to_numeric(panel.get("sr_hours"), errors="coerce"),
    )
    panel["low_price_hours_share"] = pd.to_numeric(panel.get("low_price_hours_share"), errors="coerce")
    panel["low_price_hours_share"] = panel["low_price_hours_share"].where(
        panel["low_price_hours_share"].notna(),
        pd.to_numeric(panel.get("h_below_5_obs"), errors="coerce") / 8760.0,
    )
    panel["coverage_price"] = 1.0
    panel["coverage_load_total"] = 1.0
    panel["coverage_net_position"] = 1.0
    panel["coverage_pv"] = 1.0
    panel["coverage_wind"] = 1.0
    panel["coverage_nuclear"] = 1.0
    panel["coverage_biomass"] = 1.0
    panel["coverage_ror"] = 1.0
    return panel


def _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg) -> pd.DataFrame:
    raw = make_raw_panel(n=240, year=2024)
    return build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")


def test_no_blank_strings_in_numeric_columns(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    annual = compute_annual_metrics(hourly, countries_cfg["countries"]["FR"], "test_hash")
    out = pd.DataFrame([annual])
    numeric_cols = out.select_dtypes(include=[np.number]).columns.tolist()
    assert numeric_cols
    assert not (out[numeric_cols].astype(object) == "").any().any()


def test_unique_key_annual_metrics(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly_2023 = build_hourly_table(
        make_raw_panel(n=240, year=2023),
        "FR",
        2023,
        countries_cfg["countries"]["FR"],
        thresholds_cfg,
        "FR",
    )
    hourly_2024 = build_hourly_table(
        make_raw_panel(n=240, year=2024),
        "FR",
        2024,
        countries_cfg["countries"]["FR"],
        thresholds_cfg,
        "FR",
    )
    rows = [
        compute_annual_metrics(hourly_2023, countries_cfg["countries"]["FR"], "h1"),
        compute_annual_metrics(hourly_2024, countries_cfg["countries"]["FR"], "h2"),
    ]
    out = pd.DataFrame(rows)
    assert not out.duplicated(subset=["country", "year", "scenario_id"]).any()


def test_load_identity_if_pumping_available(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    annual = compute_annual_metrics(hourly, countries_cfg["countries"]["FR"], "test_hash")
    if float(annual.get("coverage_psh_pumping", 0.0)) > 0.95:
        lhs = float(annual["load_total_mw_avg"])
        rhs = float(annual["load_mw_avg"]) + float(annual["psh_pumping_mw_avg"])
        assert abs(lhs - rhs) <= 1e-6


def test_presence_of_all_required_columns(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    annual = compute_annual_metrics(hourly, countries_cfg["countries"]["FR"], "test_hash")
    required = {
        "country",
        "year",
        "scenario_id",
        "coverage_load_total",
        "coverage_psh_pumping",
        "coverage_price",
        "coverage_pv",
        "coverage_wind",
        "coverage_net_position",
        "coverage_nuclear",
        "coverage_biomass",
        "coverage_ror",
        "load_total_mw_avg",
        "psh_pumping_mw_avg",
        "load_mw_avg",
        "must_run_mw_avg",
        "must_run_nuclear_mw_avg",
        "must_run_biomass_mw_avg",
        "must_run_ror_mw_avg",
        "nrl_mw_avg",
        "nrl_mw_avg",
        "surplus_mwh_total",
        "sr_energy",
        "sr_hours",
        "far_energy",
        "ir_p10",
        "baseload_price_eur_mwh",
        "ttl_observed_eur_mwh",
        "capture_price_pv_eur_mwh",
        "capture_ratio_pv",
        "capture_ratio_pv_vs_ttl_observed",
        "capture_price_wind_eur_mwh",
        "capture_ratio_wind",
        "capture_ratio_wind_vs_ttl_observed",
        "h_negative_obs",
        "h_below_5_obs",
        "days_spread_gt50",
        "sink_breakdown_json",
        "data_quality_flags",
    }
    assert required.issubset(set(annual.keys()))
    assert {"nrl_p10_mw", "nrl_p50_mw", "nrl_p90_mw"}.issubset(set(annual.keys()))


def test_q1_reason_codes_metrics_exist_in_annual_metrics(annual_panel_fixture):
    panel = _annual_panel_for_modules(annual_panel_fixture)
    assert Q1_REASON_CODE_REQUIRED_METRICS.issubset(set(panel.columns))
    res = run_q1(panel, _phase1_assumptions(), {"countries": ["FR", "DE"], "years": [2021, 2022, 2023, 2024]}, "q1_reason_codes")
    fail_codes = {str(c.get("code")) for c in res.checks if str(c.get("status")).upper() == "FAIL"}
    assert "Q1_REASON_CODES_UNKNOWN_METRICS" not in fail_codes


def test_q1_transition_requires_multiple_families(annual_panel_fixture):
    panel = _annual_panel_for_modules(annual_panel_fixture)
    res = run_q1(panel, _phase1_assumptions(), {"countries": ["FR", "DE"], "years": [2021, 2022, 2023, 2024]}, "q1_families")
    diag = res.tables["q1_yearly_diagnostics"]
    phase2 = diag[diag["stage_label"] == "Phase2"]
    if not phase2.empty:
        assert (pd.to_numeric(phase2["family_count_overall"], errors="coerce") >= 2).all()


def test_q1_explainability_shares_sum_to_1_or_less(make_raw_panel, countries_cfg, thresholds_cfg, annual_panel_fixture):
    panel = _annual_panel_for_modules(annual_panel_fixture)
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    hourly.loc[hourly.index[:48], "price_da_eur_mwh"] = -10.0
    res = run_q1(
        panel[panel["country"] == "FR"],
        _phase1_assumptions(),
        {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]},
        "q1_explainability",
        hourly_by_country_year={("FR", 2024): hourly},
    )
    explain = res.tables["q1_negative_price_explainability"]
    if not explain.empty:
        union = pd.to_numeric(explain["share_neg_hours_explained_union"], errors="coerce").dropna()
        if not union.empty:
            assert (union <= 1.000001).all()
        unexplained = pd.to_numeric(explain["share_neg_hours_unexplained"], errors="coerce").dropna()
        if not unexplained.empty:
            assert (unexplained >= -1e-9).all()


def test_q1_outputs_have_no_nan_on_required_fields(annual_panel_fixture):
    panel = _annual_panel_for_modules(annual_panel_fixture)
    res = run_q1(panel, _phase1_assumptions(), {"countries": ["FR", "DE"], "years": [2021, 2022, 2023, 2024]}, "q1_required_fields")
    summary = res.tables["Q1_country_summary"]
    for col in ["country", "bascule_status_market", "bascule_status_physical"]:
        assert col in summary.columns
        assert summary[col].notna().all()


def test_q2_flagging_rules(annual_panel_fixture):
    panel = _annual_panel_for_modules(annual_panel_fixture)
    q1 = run_q1(panel, _phase1_assumptions(), {"countries": ["FR", "DE"], "years": [2021, 2022, 2023, 2024]}, "q2_from_q1")
    q2 = run_q2(q1.tables["Q1_year_panel"], _phase1_assumptions(), {"countries": ["FR", "DE"]}, "q2_flags")
    slopes = q2.tables["Q2_country_slopes"]
    passed = slopes[slopes["slope_quality_flag"] == "PASS"]
    if not passed.empty:
        assert (pd.to_numeric(passed["n_points"], errors="coerce") >= 6).all()
        assert (pd.to_numeric(passed["p_value"], errors="coerce") <= 0.05).all()
        assert (pd.to_numeric(passed["loo_rel_var_max"], errors="coerce") <= 0.20).all()


def test_q2_slope_unit_present(annual_panel_fixture):
    panel = _annual_panel_for_modules(annual_panel_fixture)
    q2 = run_q2(panel, _phase1_assumptions(), {"countries": ["FR", "DE"]}, "q2_units")
    slopes = q2.tables["Q2_country_slopes"]
    assert "slope_unit" in slopes.columns
    assert slopes["slope_unit"].astype(str).str.strip().ne("").all()


def test_q2_no_pass_if_pvalue_gt_0_05(annual_panel_fixture):
    panel = _annual_panel_for_modules(annual_panel_fixture)
    q2 = run_q2(panel, _phase1_assumptions(), {"countries": ["FR", "DE"]}, "q2_pvalue")
    slopes = q2.tables["Q2_country_slopes"]
    mask = (slopes["slope_quality_flag"] == "PASS") & (pd.to_numeric(slopes["p_value"], errors="coerce") > 0.05)
    assert not mask.any()


def test_q2_years_used_subset_of_phase2_years(annual_panel_fixture):
    panel = _annual_panel_for_modules(annual_panel_fixture)
    q1 = run_q1(panel, _phase1_assumptions(), {"countries": ["FR", "DE"], "years": [2021, 2022, 2023, 2024]}, "q2_phase2_subset")
    q1_panel = q1.tables["Q1_year_panel"]
    q2 = run_q2(q1_panel, _phase1_assumptions(), {"countries": ["FR", "DE"]}, "q2_phase2_subset")
    slopes = q2.tables["Q2_country_slopes"]
    for _, row in slopes.iterrows():
        country = str(row["country"])
        years_used = {
            int(float(y.strip()))
            for y in str(row.get("years_used", "")).split(",")
            if y.strip()
        }
        phase2_years = set(
            pd.to_numeric(
                q1_panel.loc[
                    (q1_panel["country"] == country)
                    & (pd.to_numeric(q1_panel.get("is_phase2_market"), errors="coerce").fillna(0.0) > 0.0),
                    "year",
                ],
                errors="coerce",
            )
            .dropna()
            .astype(int)
            .tolist()
        )
        assert years_used.issubset(phase2_years)


def test_q3_no_nan_for_predicted_fields_when_status_ok(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    panel = _annual_panel_for_modules(annual_panel_fixture)
    panel["is_phase2_market"] = True
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    res = run_q3(
        panel[panel["country"] == "FR"],
        {("FR", 2024): hourly},
        _phase1_assumptions(),
        {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]},
        "q3_ok_non_nan",
    )
    req = res.tables["q3_inversion_requirements"]
    ok_rows = req[req["status"].astype(str).str.upper() == "OK"]
    if not ok_rows.empty:
        assert pd.to_numeric(ok_rows["predicted_sr_after"], errors="coerce").notna().all()
        assert pd.to_numeric(ok_rows["predicted_h_negative_after"], errors="coerce").notna().all()


def test_q3_demand_uplift_positive_when_baseline_violates_objective(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    panel = _annual_panel_for_modules(annual_panel_fixture)
    panel = panel[panel["country"] == "FR"].copy()
    panel.loc[:, "is_phase2_market"] = True
    panel.loc[:, "h_negative_obs"] = 600.0
    panel.loc[:, "sr_hours_share"] = 0.2
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    res = run_q3(
        panel,
        {("FR", 2024): hourly},
        _phase1_assumptions(),
        {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]},
        "q3_positive_uplift",
    )
    req = res.tables["q3_inversion_requirements"]
    dem = req[req["lever"] == "demand_uplift"]
    if not dem.empty and str(dem.iloc[0]["status"]).upper() == "OK":
        assert float(dem.iloc[0]["required_uplift"]) >= 0.0


def test_q3_export_lever_uses_net_position_positive_only(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg).copy()
    hourly["net_position_mw"] = -500.0
    base = _compute_hourly_proxy_metrics(hourly, demand_uplift=0.0, export_uplift=0.0, flex_mw_additional=0.0, export_coincidence_factor=0.45)
    uplift = _compute_hourly_proxy_metrics(hourly, demand_uplift=0.0, export_uplift=0.5, flex_mw_additional=0.0, export_coincidence_factor=0.45)
    assert abs(float(uplift["sr_hours_after"]) - float(base["sr_hours_after"])) <= 1e-12
    assert abs(float(uplift["h_negative_proxy_after"]) - float(base["h_negative_proxy_after"])) <= 1e-12


def test_q3_binary_search_monotonicity(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    m0 = _compute_hourly_proxy_metrics(hourly, demand_uplift=0.0, export_uplift=0.0, flex_mw_additional=0.0, export_coincidence_factor=0.45)
    m1 = _compute_hourly_proxy_metrics(hourly, demand_uplift=0.2, export_uplift=0.0, flex_mw_additional=0.0, export_coincidence_factor=0.45)
    assert float(m1["sr_hours_after"]) <= float(m0["sr_hours_after"]) + 1e-12
    assert float(m1["h_negative_proxy_after"]) <= float(m0["h_negative_proxy_after"]) + 1e-12


def test_q4_no_duplicates(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    import src.modules.q4_bess as q4_module

    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    res = run_q4(
        hourly,
        _phase1_assumptions(),
        {
            "country": "FR",
            "year": 2024,
            "objective": "LOW_PRICE_TARGET",
            "power_grid": [0.0, 0.0, 250.0, 250.0],
            "duration_grid": [0.0, 2.0, 2.0],
            "force_recompute": True,
        },
        "q4_no_dup",
        dispatch_mode="SURPLUS_FIRST",
    )
    curve = res.tables["q4_bess_sizing_curve"]
    keys = ["country", "scenario_id", "year", "bess_power_gw", "bess_energy_gwh", "eta_roundtrip"]
    assert not curve.duplicated(subset=keys).any()


def test_q4_cycles_not_nan(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    import src.modules.q4_bess as q4_module

    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    res = run_q4(hourly, _phase1_assumptions(), {"country": "FR", "year": 2024, "force_recompute": True}, "q4_cycles", dispatch_mode="SURPLUS_FIRST")
    curve = res.tables["q4_bess_sizing_curve"]
    assert "cycles_realized_per_day" in curve.columns
    nonzero_energy = pd.to_numeric(curve["bess_energy_gwh"], errors="coerce").fillna(0.0) > 0.0
    assert pd.to_numeric(curve.loc[nonzero_energy, "cycles_realized_per_day"], errors="coerce").notna().all()


def test_q4_monotonicity_by_duration(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    import src.modules.q4_bess as q4_module

    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    res = run_q4(
        hourly,
        _phase1_assumptions(),
        {"country": "FR", "year": 2024, "power_grid": [0.0, 100.0, 300.0], "duration_grid": [1.0, 2.0, 4.0], "force_recompute": True},
        "q4_monotonicity",
        dispatch_mode="SURPLUS_FIRST",
    )
    curve = res.tables["q4_bess_sizing_curve"]
    for d in sorted(pd.to_numeric(curve["bess_energy_gwh"] / curve["bess_power_gw"].replace(0, np.nan), errors="coerce").dropna().unique().tolist()):
        g = curve[np.isclose((curve["bess_energy_gwh"] / curve["bess_power_gw"].replace(0, np.nan)).astype(float), float(d), equal_nan=False)]
        g = g.sort_values("bess_power_gw")
        if len(g) >= 2:
            diff = pd.to_numeric(g["surplus_unabsorbed_twh_after"], errors="coerce").diff().dropna()
            assert (diff <= 1e-9).all()


def test_q4_upper_bound_non_increasing_with_more_bess(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    import src.modules.q4_bess as q4_module

    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg).copy()
    hourly.loc[hourly.index[:120], "price_da_eur_mwh"] = -15.0
    res = run_q4(
        hourly,
        _phase1_assumptions(),
        {"country": "FR", "year": 2024, "power_grid": [0.0, 100.0, 300.0], "duration_grid": [2.0], "force_recompute": True},
        "q4_upper_bound",
        dispatch_mode="SURPLUS_FIRST",
    )
    curve = res.tables["q4_bess_sizing_curve"].sort_values("bess_power_gw")
    ub = pd.to_numeric(curve["h_negative_upper_bound_after"], errors="coerce").diff().dropna()
    assert (ub <= 1e-9).all()


def test_q4_reality_check_small_bess_cannot_remove_large_fraction_without_condition(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    import src.modules.q4_bess as q4_module

    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg).copy()
    hourly.loc[hourly.index[:120], "price_da_eur_mwh"] = -20.0
    res = run_q4(
        hourly,
        _phase1_assumptions(),
        {
            "country": "FR",
            "year": 2024,
            "objective": "LOW_PRICE_TARGET",
            "power_grid": [0.0, 50.0, 100.0],
            "duration_grid": [2.0],
            "force_recompute": True,
        },
        "q4_reality",
        dispatch_mode="SURPLUS_FIRST",
    )
    frontier = res.tables["Q4_bess_frontier"].copy()
    small = frontier[pd.to_numeric(frontier["bess_power_mw_test"], errors="coerce") <= 100.0]
    if not small.empty:
        before = pd.to_numeric(small["h_negative_before"], errors="coerce")
        after = pd.to_numeric(small["h_negative_after"], errors="coerce")
        reduc_frac = ((before - after) / before.replace(0, np.nan)).fillna(0.0)
        assert (reduc_frac <= 0.9).all()


def test_q5_no_nan_deltas_when_base_exists(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    assumptions = _phase1_assumptions()
    commodity_base = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=20, freq="D"), "gas_price_eur_mwh_th": 35.0, "co2_price_eur_t": 80.0})
    commodity_scen = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=20, freq="D"), "gas_price_eur_mwh_th": 45.0, "co2_price_eur_t": 100.0})
    base = run_q5(hourly, assumptions, {"country": "FR", "year": 2024, "scenario_id": "BASE", "mode": "SCEN"}, "q5_base", commodity_daily=commodity_base).tables["Q5_summary"].iloc[0]
    scen = run_q5(
        hourly,
        assumptions,
        {
            "country": "FR",
            "year": 2024,
            "scenario_id": "HIGH_BOTH",
            "mode": "SCEN",
            "base_tca_eur_mwh": float(base["tca_current_eur_mwh"]),
            "base_ttl_observed_eur_mwh": float(base["ttl_observed_eur_mwh"]),
        },
        "q5_scen",
        commodity_daily=commodity_scen,
    ).tables["Q5_summary"].iloc[0]
    assert pd.notna(scen["delta_tca_vs_base"])
    assert pd.notna(scen["delta_ttl_model_vs_base"])


def test_q5_tca_increases_with_gas_or_co2(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    assumptions = _phase1_assumptions()
    commodity_low = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=20, freq="D"), "gas_price_eur_mwh_th": 35.0, "co2_price_eur_t": 80.0})
    commodity_high = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=20, freq="D"), "gas_price_eur_mwh_th": 45.0, "co2_price_eur_t": 100.0})
    low = run_q5(hourly, assumptions, {"country": "FR", "year": 2024}, "q5_low", commodity_daily=commodity_low).tables["Q5_summary"].iloc[0]
    high = run_q5(hourly, assumptions, {"country": "FR", "year": 2024}, "q5_high", commodity_daily=commodity_high).tables["Q5_summary"].iloc[0]
    assert float(high["tca_ccgt_eur_mwh"]) >= float(low["tca_ccgt_eur_mwh"])


def test_q5_ttl_observed_equals_socle_for_hist(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    annual = compute_annual_metrics(hourly, countries_cfg["countries"]["FR"], "socle_hash")
    assumptions = _phase1_assumptions()
    commodity = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=20, freq="D"), "gas_price_eur_mwh_th": 35.0, "co2_price_eur_t": 80.0})
    q5 = run_q5(hourly, assumptions, {"country": "FR", "year": 2024, "mode": "HIST", "scenario_id": "HIST"}, "q5_hist", commodity_daily=commodity).tables["Q5_summary"].iloc[0]
    ttl_socle = float(annual["ttl_observed_eur_mwh"])
    ttl_q5 = float(q5["ttl_observed_eur_mwh"])
    if abs(ttl_socle) > 1e-12:
        assert abs(ttl_q5 - ttl_socle) / abs(ttl_socle) <= 0.10


def test_q5_output_columns_present(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly_fr_2024(make_raw_panel, countries_cfg, thresholds_cfg)
    assumptions = _phase1_assumptions()
    commodity = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=20, freq="D"), "gas_price_eur_mwh_th": 35.0, "co2_price_eur_t": 80.0})
    res = run_q5(hourly, assumptions, {"country": "FR", "year": 2024}, "q5_cols", commodity_daily=commodity)
    summary = res.tables["Q5_summary"]
    curve = res.tables["q5_anchor_sensitivity"]
    for col in ["ttl_observed_eur_mwh", "ttl_model_eur_mwh", "delta_tca_vs_base", "delta_ttl_model_vs_base", "coherence_flag"]:
        assert col in summary.columns
    for col in ["country", "scenario_id", "year", "tca_ccgt_eur_mwh", "ttl_observed_eur_mwh", "ttl_model_eur_mwh"]:
        assert col in curve.columns
