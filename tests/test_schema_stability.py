from __future__ import annotations

from src.constants import REQUIRED_HOURLY_COLUMNS
from src.metrics import compute_annual_metrics
from src.processing import build_hourly_table


def test_processed_hourly_has_all_required_columns(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    missing = [c for c in REQUIRED_HOURLY_COLUMNS if c not in df.columns]
    assert missing == []


def test_annual_metrics_has_required_columns(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    m = compute_annual_metrics(df, countries_cfg["countries"]["FR"], data_version_hash="x")
    required = ["country", "year", "sr_energy", "far_energy", "ir_p10", "ttl_eur_mwh", "capture_ratio_pv_vs_ttl", "h_negative_obs"]
    for k in required:
        assert k in m
