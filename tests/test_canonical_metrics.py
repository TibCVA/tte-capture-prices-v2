from __future__ import annotations

import math

import pandas as pd

from src.core.canonical_metrics import (
    build_canonical_hourly_panel,
    canonical_metrics_dictionary,
    compute_canonical_year_metrics,
)
from src.processing import build_hourly_table


def _hourly(make_raw_panel, countries_cfg, thresholds_cfg, *, n: int = 240, load_total: float | None = None) -> pd.DataFrame:
    raw = make_raw_panel(n=n)
    if load_total is not None:
        raw["load_total_mw"] = float(load_total)
    return build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")


def test_canonical_load_identity_and_psh_non_negative(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly(make_raw_panel, countries_cfg, thresholds_cfg)
    c = build_canonical_hourly_panel(hourly)
    residual = (c["load_total_mw"] - (c["load_mw"] + c["psh_pumping_mw"])).abs()
    mask = c["load_total_mw"].notna()
    assert float(residual[mask].max()) <= 1e-9
    assert bool((c["psh_pumping_mw"] >= -1e-12).all())


def test_canonical_capture_nan_when_no_pv(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    raw["gen_solar_mw"] = 0.0
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    m = compute_canonical_year_metrics(hourly, country="FR", year=2024, scenario_id="HIST")
    assert math.isnan(float(m["capture_price_pv_eur_mwh"]))
    assert math.isnan(float(m["capture_ratio_pv"]))


def test_canonical_far_bounds_and_zero_surplus_case(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly(make_raw_panel, countries_cfg, thresholds_cfg, load_total=180000.0)
    m = compute_canonical_year_metrics(hourly, country="FR", year=2024, scenario_id="HIST")
    assert float(m["far_energy"]) == 1.0
    assert 0.0 <= float(m["far_energy"]) <= 1.0


def test_canonical_sr_bounds_and_negative_hours_range(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly(make_raw_panel, countries_cfg, thresholds_cfg)
    m = compute_canonical_year_metrics(hourly, country="FR", year=2024, scenario_id="HIST")
    assert 0 <= int(m["h_negative"]) <= 8784
    assert 0.0 <= float(m["sr_hours_share"]) <= 1.0
    if pd.notna(m["sr_energy_share_gen"]):
        assert 0.0 <= float(m["sr_energy_share_gen"]) <= 1.0


def test_canonical_metrics_are_reproducible(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly(make_raw_panel, countries_cfg, thresholds_cfg)
    m1 = compute_canonical_year_metrics(hourly, country="FR", year=2024, scenario_id="BASE")
    m2 = compute_canonical_year_metrics(hourly, country="FR", year=2024, scenario_id="BASE")
    keys = [
        "h_negative",
        "h_below_5",
        "baseload_price_eur_mwh",
        "capture_ratio_pv",
        "capture_ratio_wind",
        "far_energy",
        "sr_energy_share_gen",
        "ir_p10",
        "sr_energy_denominator_kind",
        "scenario_id",
    ]
    for key in keys:
        v1 = m1[key]
        v2 = m2[key]
        if isinstance(v1, str):
            assert v1 == v2
        else:
            if pd.isna(v1) and pd.isna(v2):
                continue
            assert abs(float(v1) - float(v2)) <= 1e-12


def test_canonical_metrics_dictionary_includes_audit_denominators(make_raw_panel, countries_cfg, thresholds_cfg):
    hourly = _hourly(make_raw_panel, countries_cfg, thresholds_cfg)
    out = canonical_metrics_dictionary(country="FR", year=2024, scenario_id="BASE", hourly_df=hourly)
    assert out["country"] == "FR"
    assert int(out["year"]) == 2024
    assert out["scenario_id"] == "BASE"
    for col in [
        "sr_energy_denominator_mwh",
        "capture_price_pv_denominator_mwh",
        "capture_price_wind_denominator_mwh",
        "ir_p10_load_mw",
        "ir_p10_must_run_mw",
    ]:
        assert col in out

