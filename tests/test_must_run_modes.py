from __future__ import annotations

import pandas as pd

from src.modules.q1_transition import run_q1
from src.processing import build_hourly_table


def test_must_run_observed_sum_components(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    cfg = countries_cfg["countries"]["FR"].copy()
    cfg["must_run"]["mode"] = "observed"
    df = build_hourly_table(raw, "FR", 2024, cfg, thresholds_cfg, "FR")
    expected = raw["gen_nuclear_mw"] + raw["gen_hydro_ror_mw"] + raw["gen_biomass_mw"]
    assert float((df["gen_must_run_mw"] - expected).abs().max()) < 1e-9


def test_floor_mode_capped_by_observed(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    cfg = countries_cfg["countries"]["FR"].copy()
    cfg["must_run"]["mode"] = "floor"
    df = build_hourly_table(raw, "FR", 2024, cfg, thresholds_cfg, "FR")
    assert (df["gen_must_run_mw"] <= df["gen_must_run_observed_mw"]).all()


def test_floor_mode_respects_floor(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    cfg = countries_cfg["countries"]["FR"].copy()
    cfg["must_run"]["mode"] = "floor"
    cfg["must_run"]["floor_gw"] = 1.0
    cfg["must_run"]["modulation_pct"] = 1.0
    df = build_hourly_table(raw, "FR", 2024, cfg, thresholds_cfg, "FR")
    assert (df["gen_must_run_mw"] >= 1000).all()


def test_scope_coverage_ratio_uses_configured_components(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=168, year=2024)
    hourly = build_hourly_table(raw, "DE", 2024, countries_cfg["countries"]["DE"], thresholds_cfg, "DE")
    annual = pd.DataFrame(
        [
            {
                "country": "DE",
                "year": 2024,
                "quality_flag": "OK",
                "completeness": 1.0,
                "regime_coherence": 1.0,
                "h_negative_obs": 150.0,
                "h_below_5_obs": 250.0,
                "days_spread_gt50": 180.0,
                "capture_ratio_pv_vs_ttl": 0.7,
                "sr_energy": 0.002,
                "far_energy": 0.99,
                "ir_p10": 0.8,
                "ttl_eur_mwh": 150.0,
            }
        ]
    )
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q1(
        annual,
        assumptions,
        {"countries": ["DE"], "years": [2024]},
        "TEST_SCOPE",
        hourly_by_country_year={("DE", 2024): hourly},
    )
    scope = res.tables["Q1_scope_audit"]
    assert not scope.empty
    assert float(scope.iloc[0]["scope_coverage_ratio"]) < 0.70
