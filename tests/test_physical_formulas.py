from __future__ import annotations

from src.processing import build_hourly_table


def test_nrl_identity(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    expected = df["load_mw"] - df["gen_vre_mw"] - df["gen_must_run_mw"]
    assert float((df["nrl_mw"] - expected).abs().max()) < 1e-9


def test_surplus_definition(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    expected = (-df["nrl_mw"]).clip(lower=0.0)
    assert float((df["surplus_mw"] - expected).abs().max()) < 1e-9


def test_surplus_unabsorbed_non_negative(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assert (df["surplus_unabsorbed_mw"] >= 0).all()


def test_exports_definition(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(net=-100)
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assert (df["exports_mw"] == 0).all()
