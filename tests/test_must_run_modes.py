from __future__ import annotations

import pandas as pd

from src.core.definitions import compute_must_run_floor
from src.modules.q1_transition import run_q1
from src.processing import build_hourly_table


def test_must_run_floor_is_bounded_by_candidates(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    candidates_sum = (
        pd.to_numeric(df["gen_nuclear_mw"], errors="coerce").fillna(0.0)
        + pd.to_numeric(df["gen_lignite_mw"], errors="coerce").fillna(0.0)
        + pd.to_numeric(df["gen_coal_mw"], errors="coerce").fillna(0.0)
        + pd.to_numeric(df["gen_gas_mw"], errors="coerce").fillna(0.0)
        + pd.to_numeric(df["gen_biomass_mw"], errors="coerce").fillna(0.0)
        + pd.to_numeric(df["gen_hydro_ror_mw"], errors="coerce").fillna(0.0)
    )
    assert (df["gen_must_run_mw"] <= candidates_sum + 1e-9).all()


def test_floor_component_non_negative_and_zero_if_series_zero(make_raw_panel):
    raw = make_raw_panel()
    raw["gen_nuclear_mw"] = 0.0
    res = compute_must_run_floor(raw, candidate_components=["nuclear"], floor_quantile=0.10)
    assert res.floor_by_component_mw["nuclear"] >= 0.0
    assert res.floor_by_component_mw["nuclear"] == 0.0
    assert float(res.must_run_mw.sum()) == 0.0


def test_q1_scope_coverage_in_01(make_raw_panel, countries_cfg, thresholds_cfg):
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
                "capture_ratio_wind_vs_ttl": 0.8,
                "capture_ratio_pv": 0.7,
                "capture_ratio_wind": 0.8,
                "sr_energy": 0.01,
                "far_energy": 0.95,
                "ir_p10": 0.3,
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
    val = float(scope.iloc[0]["must_run_scope_coverage"])
    assert 0.0 <= val <= 1.0
