from __future__ import annotations

from time import perf_counter

import pandas as pd
import pytest

import src.modules.q4_bess as q4_module
from src.modules.q4_bess import run_q4
from src.processing import build_hourly_table


def _selection(force_recompute: bool) -> dict:
    return {
        "country": "FR",
        "year": 2024,
        "objective": "FAR_TARGET",
        "force_recompute": force_recompute,
    }


def test_q4_soc_bounds(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test")

    frontier = res.tables["Q4_bess_frontier"]
    assert not frontier.empty
    assert (frontier["soc_min"] >= -1e-6).all()


def test_q4_reduces_negative_hours_when_present(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")

    raw = make_raw_panel(n=240)
    raw.loc[raw.index[:120], "price_da_eur_mwh"] = -10.0
    raw.loc[raw.index[120:], "price_da_eur_mwh"] = 90.0
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(
        hourly,
        assumptions,
        {
            "country": "FR",
            "year": 2024,
            "objective": "LOW_PRICE_TARGET",
            "power_grid": [0.0, 250.0, 500.0, 1000.0],
            "duration_grid": [2.0, 4.0],
            "force_recompute": True,
        },
        "test",
        dispatch_mode="SURPLUS_FIRST",
    )
    f = res.tables["Q4_bess_frontier"].copy()
    h_before = pd.to_numeric(f["h_negative_before"], errors="coerce")
    if pd.notna(h_before).any() and float(h_before.max()) > 0:
        assert (pd.to_numeric(f["delta_h_negative"], errors="coerce") <= 0).all()
    fail_codes = {str(c.get("code", "")) for c in res.checks if str(c.get("status", "")).upper() == "FAIL"}
    assert "Q4_BESS_INEFFECTIVE" not in fail_codes


def test_q4_monotonic_surplus_reduction(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test", dispatch_mode="SURPLUS_FIRST")

    f = res.tables["Q4_bess_frontier"].sort_values("bess_power_mw_test")
    if len(f) >= 2:
        assert f["surplus_unabs_energy_after"].iloc[-1] <= f["surplus_unabs_energy_after"].iloc[0]


def test_q4_no_fail_check_on_fixture(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test", dispatch_mode="SURPLUS_FIRST")
    assert "FAIL" not in [c.get("status") for c in res.checks]


def test_q4_required_bess_positive_if_target_reachable(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(
        hourly,
        assumptions,
        {
            "country": "FR",
            "year": 2024,
            "objective": "FAR_TARGET",
            "power_grid": [0.0, 500.0, 1000.0, 2000.0],
            "duration_grid": [0.0, 2.0, 4.0],
            "force_recompute": True,
        },
        "test",
        dispatch_mode="SURPLUS_FIRST",
    )
    summary = res.tables["Q4_sizing_summary"].iloc[0]
    if float(summary["far_before"]) < 0.95 and not bool(summary["objective_not_reached"]):
        assert float(summary["required_bess_power_mw"]) > 0.0


def test_q4_objective_not_reached_flag(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions.loc[assumptions["param_name"] == "target_far", "param_value"] = 1.01
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test", dispatch_mode="SURPLUS_FIRST")
    summary = res.tables["Q4_sizing_summary"].iloc[0]
    assert bool(summary["objective_not_reached"]) is True


def test_q4_cache_hit_and_diagnostics(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")

    cold = run_q4(hourly, assumptions, _selection(force_recompute=True), "cold", dispatch_mode="SURPLUS_FIRST")
    warm = run_q4(hourly, assumptions, _selection(force_recompute=False), "warm", dispatch_mode="SURPLUS_FIRST")

    assert cold.kpis.get("cache_hit") is False
    assert warm.kpis.get("cache_hit") is True

    frontier = warm.tables["Q4_bess_frontier"]
    for col in ["compute_time_sec", "cache_hit", "engine_version"]:
        assert col in frontier.columns


def test_q4_summary_has_finite_far_and_nonzero_rec_when_objective_not_reached(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions.loc[assumptions["param_name"] == "target_far", "param_value"] = 1.01
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test", dispatch_mode="SURPLUS_FIRST")
    s = res.tables["Q4_sizing_summary"].iloc[0]
    assert pd.notna(s["far_before"]) and pd.notna(s["far_after"])
    assert 0.0 <= float(s["far_before"]) <= 1.0
    assert 0.0 <= float(s["far_after"]) <= 1.0
    if bool(s["objective_not_reached"]):
        assert str(s["objective_reason"]) == "not_met_grid_too_small"


def test_q4_frontier_has_join_keys(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(
        hourly,
        assumptions,
        {
            "country": "FR",
            "year": 2024,
            "scenario_id": "BASE",
            "objective": "FAR_TARGET",
            "force_recompute": True,
        },
        "test",
    )
    f = res.tables["Q4_bess_frontier"]
    for col in ["scenario_id", "country", "year"]:
        assert col in f.columns
        assert f[col].notna().all()


def test_q4_no_free_energy_when_no_charge(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test", dispatch_mode="SURPLUS_FIRST")
    frontier = res.tables["Q4_bess_frontier"].copy()
    mask = pd.to_numeric(frontier["charge_sum_mwh"], errors="coerce").fillna(0.0).abs() <= 1e-6
    assert (pd.to_numeric(frontier.loc[mask, "discharge_sum_mwh"], errors="coerce").fillna(0.0).abs() <= 1e-6).all()


def test_q4_energy_conservation_annual(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test", dispatch_mode="SURPLUS_FIRST")
    f = res.tables["Q4_bess_frontier"].copy()
    lhs = pd.to_numeric(f["discharge_sum_mwh"], errors="coerce").fillna(0.0)
    rhs = (
        pd.to_numeric(f["charge_sum_mwh"], errors="coerce").fillna(0.0)
        * pd.to_numeric(f["eta_roundtrip"], errors="coerce").fillna(0.0)
        + pd.to_numeric(f["soc_start_mwh"], errors="coerce").fillna(0.0)
        - pd.to_numeric(f["soc_end_mwh"], errors="coerce").fillna(0.0)
        + 1e-6
    )
    assert (lhs <= rhs + 1e-9).all()


def test_q4_soc_end_zero_in_default_mode(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test", dispatch_mode="SURPLUS_FIRST")
    f = res.tables["Q4_bess_frontier"].copy()
    end = pd.to_numeric(f["soc_end_mwh"], errors="coerce").fillna(0.0).abs()
    e = pd.to_numeric(f["bess_energy_mwh_test"], errors="coerce").fillna(0.0)
    tol = (e.clip(lower=1.0) * 1e-6) + 1e-9
    assert (end <= tol).all()


def test_q4_already_met_has_no_objective_not_reached_warning(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions.loc[assumptions["param_name"] == "target_far", "param_value"] = 0.0
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test", dispatch_mode="SURPLUS_FIRST")
    s = res.tables["Q4_sizing_summary"].iloc[0]
    assert bool(s["objective_met"]) is True
    assert bool(s["objective_not_reached"]) is False
    assert str(s["objective_reason"]) == "met_in_base_grid"
    objective_warn_codes = {
        str(c.get("code"))
        for c in res.checks
        if str(c.get("status", "")).upper() == "WARN"
    }
    assert "Q4_OBJECTIVE_NOT_REACHED_GRID" not in objective_warn_codes
    assert "Q4_OBJECTIVE_UNREACHABLE" not in objective_warn_codes


def test_q4_objective_reason_normalized_and_flags_consistent(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions.loc[assumptions["param_name"] == "target_far", "param_value"] = 1.01
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test", dispatch_mode="SURPLUS_FIRST")
    s = res.tables["Q4_sizing_summary"].iloc[0]
    allowed = {"met_in_base_grid", "met_after_grid_expansion", "not_met_grid_too_small", "not_applicable"}
    assert str(s["objective_reason"]) in allowed
    if bool(s["objective_met"]):
        assert bool(s["objective_not_reached"]) is False
    if bool(s["objective_not_reached"]):
        assert str(s["objective_reason"]) == "not_met_grid_too_small"
    fail_codes = {str(c.get("code")) for c in res.checks if str(c.get("status", "")).upper() == "FAIL"}
    assert "Q4_OBJECTIVE_REASON_INVALID" not in fail_codes
    assert "Q4_OBJECTIVE_FLAG_CONTRADICTION" not in fail_codes


def test_q4_boundary_solution_warning_when_met_on_grid_max(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions.loc[assumptions["param_name"] == "target_far", "param_value"] = 0.0
    res = run_q4(
        hourly,
        assumptions,
        {
            "country": "FR",
            "year": 2024,
            "objective": "FAR_TARGET",
            "power_grid": [0.0],
            "duration_grid": [0.0],
            "force_recompute": True,
        },
        "test_boundary",
        dispatch_mode="SURPLUS_FIRST",
    )
    s = res.tables["Q4_sizing_summary"].iloc[0]
    assert bool(s["objective_met"]) is True
    assert bool(s["objective_not_reached"]) is False
    warn_codes = {str(c.get("code")) for c in res.checks if str(c.get("status", "")).upper() == "WARN"}
    assert "GRID_BOUNDARY_SOLUTION" in warn_codes
    assert "Q4_OBJECTIVE_NOT_REACHED_GRID" not in warn_codes


def test_q4_emits_test_q4_reality_checks(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test", dispatch_mode="SURPLUS_FIRST")

    q4_001 = [c for c in res.checks if str(c.get("code")) == "TEST_Q4_001"]
    q4_002 = [c for c in res.checks if str(c.get("code")) == "TEST_Q4_002"]
    assert q4_001 and any(str(c.get("status")) == "PASS" for c in q4_001)
    assert q4_002 and any(str(c.get("status")) == "PASS" for c in q4_002)


def test_q4_zero_size_after_equals_before(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    raw.loc[raw.index[:120], "price_da_eur_mwh"] = -20.0
    raw.loc[raw.index[120:], "price_da_eur_mwh"] = 70.0
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(
        hourly,
        assumptions,
        {
            "country": "FR",
            "year": 2024,
            "objective": "LOW_PRICE_TARGET",
            "power_grid": [0.0, 200.0],
            "duration_grid": [0.0, 2.0],
            "force_recompute": True,
        },
        "test",
        dispatch_mode="SURPLUS_FIRST",
    )
    f = res.tables["Q4_bess_frontier"].copy()
    zero = (
        pd.to_numeric(f["bess_power_mw_test"], errors="coerce").fillna(0.0).abs() <= 1e-9
    ) | (
        pd.to_numeric(f["bess_energy_mwh_test"], errors="coerce").fillna(0.0).abs() <= 1e-9
    )
    z = f[zero]
    assert not z.empty
    for after_col, before_col in [
        ("h_negative_after", "h_negative_before"),
        ("h_below_5_after", "h_below_5_before"),
        ("capture_ratio_pv_after", "capture_ratio_pv_before"),
        ("capture_ratio_wind_after", "capture_ratio_wind_before"),
    ]:
        a = pd.to_numeric(z[after_col], errors="coerce")
        b = pd.to_numeric(z[before_col], errors="coerce")
        assert ((a - b).abs() <= 1e-9).all()


def test_q4_monotonic_hneg_and_unabs_on_grid(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    raw.loc[raw.index[:120], "price_da_eur_mwh"] = -10.0
    raw.loc[raw.index[120:], "price_da_eur_mwh"] = 80.0
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(
        hourly,
        assumptions,
        {
            "country": "FR",
            "year": 2024,
            "objective": "LOW_PRICE_TARGET",
            "power_grid": [0.0, 100.0, 300.0],
            "duration_grid": [1.0, 2.0, 4.0],
            "force_recompute": True,
        },
        "test",
        dispatch_mode="SURPLUS_FIRST",
    )
    f = res.tables["Q4_bess_frontier"].copy()

    for d in sorted(pd.to_numeric(f["bess_duration_h_test"], errors="coerce").dropna().unique().tolist()):
        g = f[pd.to_numeric(f["bess_duration_h_test"], errors="coerce") == float(d)].sort_values("bess_power_mw_test")
        if len(g) >= 2:
            assert (pd.to_numeric(g["surplus_unabs_energy_after"], errors="coerce").diff().dropna() <= 1e-9).all()
            assert (pd.to_numeric(g["h_negative_after"], errors="coerce").diff().dropna() <= 1e-9).all()

    for p in sorted(pd.to_numeric(f["bess_power_mw_test"], errors="coerce").dropna().unique().tolist()):
        g = f[pd.to_numeric(f["bess_power_mw_test"], errors="coerce") == float(p)].sort_values("bess_energy_mwh_test")
        if len(g) >= 2:
            assert (pd.to_numeric(g["surplus_unabs_energy_after"], errors="coerce").diff().dropna() <= 1e-9).all()
            assert (pd.to_numeric(g["h_negative_after"], errors="coerce").diff().dropna() <= 1e-9).all()


def test_q4_no_charge_above_surplus_in_surplus_first(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test", dispatch_mode="SURPLUS_FIRST")
    f = res.tables["Q4_bess_frontier"]
    assert (pd.to_numeric(f["charge_vs_surplus_violation_hours"], errors="coerce").fillna(0.0) <= 0.0).all()


def test_q4_no_impact_without_dispatch(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    raw["load_total_mw"] = 90000.0
    raw["price_da_eur_mwh"] = 50.0
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(
        hourly,
        assumptions,
        {
            "country": "FR",
            "year": 2024,
            "objective": "LOW_PRICE_TARGET",
            "power_grid": [0.0, 250.0, 500.0],
            "duration_grid": [2.0, 4.0],
            "force_recompute": True,
        },
        "test_no_dispatch",
        dispatch_mode="SURPLUS_FIRST",
    )
    f = res.tables["Q4_bess_frontier"].copy()
    mask = (
        pd.to_numeric(f["charge_sum_mwh"], errors="coerce").fillna(0.0).abs() <= 1e-9
    ) & (
        pd.to_numeric(f["discharge_sum_mwh"], errors="coerce").fillna(0.0).abs() <= 1e-9
    )
    nd = f[mask]
    assert not nd.empty
    assert (
        pd.to_numeric(nd["h_negative_after"], errors="coerce")
        - pd.to_numeric(nd["h_negative_before"], errors="coerce")
    ).abs().le(1e-9).all()
    assert (
        pd.to_numeric(nd["pv_capture_price_after"], errors="coerce")
        - pd.to_numeric(nd["pv_capture_price_before"], errors="coerce")
    ).abs().le(1e-9).all()


@pytest.mark.parametrize("dispatch_mode", ["SURPLUS_FIRST", "PRICE_ARBITRAGE_SIMPLE", "PV_COLOCATED"])
def test_q4_physics_invariants_hold_across_dispatch_modes(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch, dispatch_mode):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")
    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(
        hourly,
        assumptions,
        {
            "country": "FR",
            "year": 2024,
            "objective": "LOW_PRICE_TARGET",
            "power_grid": [0.0, 200.0, 500.0],
            "duration_grid": [2.0, 4.0],
            "force_recompute": True,
        },
        f"test_{dispatch_mode}",
        dispatch_mode=dispatch_mode,
    )
    fail_codes = {str(c.get("code", "")).upper() for c in res.checks if str(c.get("status", "")).upper() == "FAIL"}
    assert "Q4_ENERGY_BALANCE" not in fail_codes
    assert "Q4_SOC_END_BOUNDARY" not in fail_codes
    assert "TEST_Q4_001" not in fail_codes
    f = res.tables["Q4_bess_frontier"].copy()
    end = pd.to_numeric(f["soc_end_mwh"], errors="coerce").fillna(0.0).abs()
    e = pd.to_numeric(f["bess_energy_mwh_test"], errors="coerce").fillna(0.0)
    tol = (e.clip(lower=1.0) * 1e-6) + 1e-9
    assert (end <= tol).all()


@pytest.mark.performance
def test_q4_performance_smoke(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")

    t0 = perf_counter()
    run_q4(
        hourly,
        assumptions,
        {
            "country": "FR",
            "year": 2024,
            "objective": "FAR_TARGET",
            "power_grid": [0.0, 500.0, 2000.0],
            "duration_grid": [1.0, 2.0, 4.0],
            "force_recompute": True,
        },
        "perf",
        dispatch_mode="SURPLUS_FIRST",
    )
    elapsed = perf_counter() - t0
    assert elapsed < 3.0
