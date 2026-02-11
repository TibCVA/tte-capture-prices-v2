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


def test_q4_monotonic_surplus_reduction(make_raw_panel, countries_cfg, thresholds_cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(q4_module, "Q4_CACHE_BASE", tmp_path / "q4cache")

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q4(hourly, assumptions, _selection(force_recompute=True), "test", dispatch_mode="SURPLUS_FIRST")

    f = res.tables["Q4_bess_frontier"].sort_values("required_bess_power_mw")
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
