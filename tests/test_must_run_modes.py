from __future__ import annotations

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
