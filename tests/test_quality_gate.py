from __future__ import annotations

import numpy as np
import pandas as pd

import src.modules.q3_exit as q3_module
import src.modules.q4_bess as q4_module
from src.config_loader import load_phase2_assumptions
from src.modules.q2_slope import run_q2
from src.modules.q3_exit import run_q3
from src.modules.q4_bess import run_q4
from src.modules.question_bundle_runner import run_question_bundle
from src.processing import build_hourly_table


def _assumptions() -> pd.DataFrame:
    return pd.read_csv("data/assumptions/phase1_assumptions.csv")


def _hourly_map_for_fixture(
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


def test_q4_objective_met_matches_directional_rule(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    res = run_q4(
        hourly,
        _assumptions(),
        {"country": "FR", "year": 2024, "objective": "LOW_PRICE_TARGET", "force_recompute": True},
        "quality_gate_q4_obj",
        dispatch_mode="SURPLUS_FIRST",
    )
    s = res.tables["Q4_sizing_summary"].iloc[0]
    direction = str(s.get("objective_direction", ""))
    value = float(pd.to_numeric(pd.Series([s.get("objective_value_after")]), errors="coerce").iloc[0])
    target = float(pd.to_numeric(pd.Series([s.get("objective_target_value")]), errors="coerce").iloc[0])
    if np.isfinite(value) and np.isfinite(target):
        if direction == "lower_is_better":
            assert bool(s["objective_met"]) is (value <= target + 1e-9)
        elif direction == "higher_is_better":
            assert bool(s["objective_met"]) is (value >= target - 1e-9)


def test_q2_default_axis_is_generation_share(annual_panel_fixture):
    out = run_q2(annual_panel_fixture, _assumptions(), {"countries": ["FR", "DE"]}, "quality_gate_q2_axis").tables[
        "Q2_country_slopes"
    ]
    assert not out.empty
    used = out[out["x_axis_used"].astype(str) != "none"]["x_axis_used"].astype(str)
    if not used.empty:
        assert used.str.endswith("_generation").all()


def test_q2_high_scenarios_do_not_drop_to_zero_points_when_hist_has_points(annual_panel_fixture):
    hist = run_q2(annual_panel_fixture, _assumptions(), {"countries": ["FR"]}, "quality_gate_q2_hist").tables["Q2_country_slopes"]
    assert not hist.empty
    refs_years: dict[str, list[int]] = {}
    refs_start: dict[str, int] = {}
    for _, r in hist.iterrows():
        key = f"{r['country']}|{str(r['tech']).upper()}"
        years = [int(float(tok.strip())) for tok in str(r.get("years_used", "")).split(",") if tok.strip()]
        if years:
            refs_years[key] = years
            refs_start[key] = int(min(years))
    scen = run_q2(
        annual_panel_fixture,
        _assumptions(),
        {
            "countries": ["FR"],
            "mode": "SCEN",
            "scenario_id": "HIGH_CO2",
            "phase2_years_by_country_tech": refs_years,
            "phase2_start_year_by_country_tech": refs_start,
        },
        "quality_gate_q2_high",
    ).tables["Q2_country_slopes"]
    merged = hist[["country", "tech", "n_points"]].merge(
        scen[["country", "tech", "n_points"]],
        on=["country", "tech"],
        suffixes=("_hist", "_scen"),
        how="inner",
    )
    assert not merged.empty
    bad = (
        (pd.to_numeric(merged["n_points_hist"], errors="coerce") >= 2)
        & (pd.to_numeric(merged["n_points_scen"], errors="coerce") <= 0)
    )
    assert not bool(bad.any())


def test_q3_proxy_fail_forces_module_fail(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg, monkeypatch):
    def _fail_fit(*args, **kwargs):
        raise RuntimeError("forced_proxy_failure")

    monkeypatch.setattr(q3_module.MarketProxyBucketModel, "fit_baseline", _fail_fit)
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    panel = annual_panel_fixture[annual_panel_fixture["country"] == "FR"].copy()
    panel["is_phase2_market"] = True
    res = run_q3(
        panel,
        {("FR", 2024): hourly},
        _assumptions(),
        {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]},
        "quality_gate_q3_proxy_fail",
    )
    out = res.tables["Q3_status"]
    assert not out.empty
    assert (out["status"].astype(str).str.upper() == "FAIL").any()
    fail_codes = {str(c.get("code")) for c in res.checks if str(c.get("status", "")).upper() == "FAIL"}
    assert "Q3_MARKET_PROXY_INVALID" in fail_codes


def test_q4_proxy_fail_forces_module_fail(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")

    def _fail_fit(*args, **kwargs):
        raise RuntimeError("forced_proxy_failure")

    monkeypatch.setattr(q4_module.MarketProxyBucketModel, "fit_baseline", _fail_fit)
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    res = run_q4(
        hourly,
        _assumptions(),
        {"country": "FR", "year": 2024, "objective": "FAR_TARGET", "force_recompute": True},
        "quality_gate_q4_proxy_fail",
        dispatch_mode="SURPLUS_FIRST",
    )
    fail_codes = {str(c.get("code")) for c in res.checks if str(c.get("status", "")).upper() == "FAIL"}
    assert "Q4_MARKET_PROXY_INVALID" in fail_codes
    s = res.tables["Q4_sizing_summary"].iloc[0]
    assert str(s.get("status", "")).upper() == "FAIL"


def test_q4_delta_reduction_bound_by_charge_hours(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    raw.loc[raw.index[:120], "price_da_eur_mwh"] = -10.0
    raw.loc[raw.index[120:], "price_da_eur_mwh"] = 60.0
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    res = run_q4(
        hourly,
        _assumptions(),
        {"country": "FR", "year": 2024, "objective": "LOW_PRICE_TARGET", "force_recompute": True},
        "quality_gate_q4_charge_bound",
        dispatch_mode="SURPLUS_FIRST",
    )
    f = res.tables["Q4_bess_frontier"].copy()
    delta_hneg = pd.to_numeric(f.get("delta_h_negative_est", f.get("delta_h_negative")), errors="coerce")
    delta_h5 = pd.to_numeric(f.get("delta_h_below_5_est", f.get("delta_h_below_5")), errors="coerce")
    charge_hours = pd.to_numeric(f.get("charge_hours"), errors="coerce").fillna(0.0)
    assert ((-delta_hneg) <= (charge_hours + 5.0)).fillna(True).all()
    assert ((-delta_h5) <= (charge_hours + 5.0)).fillna(True).all()


def test_q5_runner_uses_hist_fallback_when_base_missing(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    assumptions_phase1 = _assumptions()
    assumptions_phase2 = load_phase2_assumptions()
    hourly_hist_map = _hourly_map_for_fixture(
        countries_cfg=countries_cfg,
        thresholds_cfg=thresholds_cfg,
        make_raw_panel=make_raw_panel,
        countries=["FR"],
        years=[2024],
    )
    bundle = run_question_bundle(
        question_id="Q5",
        annual_hist=annual_panel_fixture,
        hourly_hist_map=hourly_hist_map,
        assumptions_phase1=assumptions_phase1,
        assumptions_phase2=assumptions_phase2,
        selection={
            "countries": ["FR"],
            "years": [2024],
            "scenario_ids": ["HIGH_CO2"],
            "scenario_years": [2030],
        },
        run_id="quality_gate_q5_missing_base",
    )
    fail_codes = {str(c.get("code")) for c in bundle.checks if str(c.get("status", "")).upper() == "FAIL"}
    assert "Q5_BASE_SCENARIO_MISSING" not in fail_codes
    q5_quality = bundle.scen_results.get("HIGH_CO2").tables.get("q5_quality_summary", pd.DataFrame())
    q5_anchor = bundle.scen_results.get("HIGH_CO2").tables.get("q5_anchor_sensitivity", pd.DataFrame())
    assert not q5_quality.empty
    assert (q5_quality["quality_status"].astype(str).isin(["PASS", "WARN"])).all()
    assert not q5_anchor.empty
    statuses = set(q5_anchor["base_ref_status"].astype(str).str.lower().unique().tolist())
    assert statuses.issubset({"ok", "warn_fallback_from_hist"})
