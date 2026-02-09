from __future__ import annotations

import numpy as np

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


def test_far_nan_when_no_surplus(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    raw["load_total_mw"] = 120000.0
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    m = compute_annual_metrics(df, countries_cfg["countries"]["FR"], data_version_hash="x")
    assert np.isnan(m["far_energy"])
