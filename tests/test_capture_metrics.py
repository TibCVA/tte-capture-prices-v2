from __future__ import annotations

import numpy as np

from src.conventions import PENETRATION_UNIT_CANONICAL
from src.metrics import compute_annual_metrics
from src.processing import build_hourly_table


def test_capture_rate_weighted_average(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    raw["price_da_eur_mwh"] = 100
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    m = compute_annual_metrics(df, countries_cfg["countries"]["FR"], data_version_hash="x")
    assert abs(m["capture_rate_pv_eur_mwh"] - 100) < 1e-9


def test_capture_ratio_division_by_baseload(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    raw["price_da_eur_mwh"] = 50
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    m = compute_annual_metrics(df, countries_cfg["countries"]["FR"], data_version_hash="x")
    assert abs(m["capture_ratio_pv"] - 1.0) < 1e-9


def test_far_one_when_no_surplus(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    raw["load_total_mw"] = 120000.0
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    m = compute_annual_metrics(df, countries_cfg["countries"]["FR"], data_version_hash="x")
    assert float(m["far_energy"]) == 1.0


def test_units_and_bounds(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    m = compute_annual_metrics(df, countries_cfg["countries"]["FR"], data_version_hash="x")

    assert PENETRATION_UNIT_CANONICAL == "pct"
    for col in ["vre_penetration_pct_gen", "pv_penetration_pct_gen", "wind_penetration_pct_gen"]:
        assert 0.0 <= float(m[col]) <= 100.0
    for col in ["vre_penetration_share_gen", "pv_penetration_share_gen", "wind_penetration_share_gen"]:
        assert 0.0 <= float(m[col]) <= 1.0
    for col in ["sr_energy_share_load", "sr_energy_share_gen", "sr_hours_share"]:
        assert 0.0 <= float(m[col]) <= 1.0

    far = float(m["far_energy"]) if np.isfinite(m["far_energy"]) else np.nan
    if np.isfinite(far):
        assert 0.0 <= far <= 1.0
    assert float(m["ir_p10"]) >= 0.0
