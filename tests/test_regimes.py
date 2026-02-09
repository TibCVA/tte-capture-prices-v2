from __future__ import annotations

from src.processing import build_hourly_table


def test_regime_a_when_surplus_unabsorbed_positive(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    raw["load_total_mw"] = 10000.0
    raw["net_position_mw"] = 0.0
    raw["psh_pump_mw"] = 0.0
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assert (df["regime"] == "A").any()


def test_regime_b_when_surplus_absorbed_only(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel()
    raw["load_total_mw"] = 10000.0
    raw["net_position_mw"] = 50000.0
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assert ((df["surplus_mw"] > 0) & (df["surplus_unabsorbed_mw"] == 0) & (df["regime"] == "B")).any()


def test_regime_d_threshold_quantile_logic(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=500)
    raw.loc[raw.index[:250], "load_total_mw"] = 90000
    raw.loc[raw.index[250:], "load_total_mw"] = 40000
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assert "nrl_positive_quantile_threshold" in df.columns
    assert (df["regime"] == "D").any()
