from __future__ import annotations

import pandas as pd

from src.core.definitions import compute_balance_metrics, sanity_check_core_definitions
from src.processing import build_hourly_table


def test_core_balance_ranges(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    bal = compute_balance_metrics(
        load_mw=df["load_mw"],
        must_run_mw=df["gen_must_run_mw"],
        surplus_mw=df["surplus_mw"],
        absorbed_mw=df["surplus_absorbed_mw"],
        gen_primary_mw=df["gen_primary_mw"],
    )
    assert 0.0 <= float(bal.sr_energy) <= 1.0
    assert 0.0 <= float(bal.far_energy) <= 1.0
    assert float(bal.ir) >= 0.0


def test_core_absorption_identities(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assert (df["surplus_absorbed_mw"] <= df["surplus_mw"] + 1e-9).all()
    assert (df["surplus_unabsorbed_mw"] >= -1e-9).all()


def test_far_equals_one_when_surplus_zero(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=120)
    raw["load_total_mw"] = 120000.0
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    issues = sanity_check_core_definitions(df, far_energy=1.0, sr_energy=0.0, ir=0.0)
    assert "FAR must equal 1 when surplus is zero" not in issues
    assert float(pd.to_numeric(df["surplus_unabsorbed_mw"], errors="coerce").sum()) == 0.0


def test_load_psh_energy_identity(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=240)
    raw["psh_pump_mw"] = 400.0
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    lhs = float(pd.to_numeric(df["load_total_mw"], errors="coerce").fillna(0.0).sum())
    rhs = float(pd.to_numeric(df["load_mw"], errors="coerce").fillna(0.0).sum() + pd.to_numeric(df["psh_pump_mw"], errors="coerce").fillna(0.0).sum())
    tol = max(1e-6, 0.001 * abs(lhs))
    assert abs(lhs - rhs) <= tol


def test_psh_status_and_coverage_when_partial_or_missing(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=48)
    raw.loc[raw.index[:12], "psh_pump_mw"] = pd.NA
    df_partial = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assert "psh_pumping_data_status" in df_partial.columns
    assert "psh_pumping_coverage_share" in df_partial.columns
    assert set(df_partial["psh_pumping_data_status"].astype(str).str.lower().unique()) == {"partial"}
    assert 0.0 < float(pd.to_numeric(df_partial["psh_pumping_coverage_share"], errors="coerce").iloc[0]) < 1.0

    raw_missing = make_raw_panel(n=48)
    raw_missing["psh_pump_mw"] = pd.NA
    df_missing = build_hourly_table(raw_missing, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assert set(df_missing["psh_pumping_data_status"].astype(str).str.lower().unique()) == {"missing"}
    assert float(pd.to_numeric(df_missing["psh_pumping_coverage_share"], errors="coerce").iloc[0]) == 0.0


def test_load_mw_clamped_when_psh_exceeds_total(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=48)
    raw["load_total_mw"] = 100.0
    raw["psh_pump_mw"] = 180.0
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    load_net = pd.to_numeric(df["load_mw"], errors="coerce")
    assert load_net.notna().all()
    assert (load_net >= 0.0).all()
    assert set(df["q_bad_load_net"].astype(bool).unique()) == {True}


def test_flex_accounting_identity_hourly(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=96)
    raw["net_position_mw"] = -350.0
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")

    surplus = pd.to_numeric(df["surplus_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    absorbed = pd.to_numeric(df["surplus_absorbed_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    unabs = pd.to_numeric(df["surplus_unabsorbed_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    flex_total = pd.to_numeric(df["flex_sink_observed_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    flex_exports = pd.to_numeric(df["flex_sink_exports_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    flex_psh = pd.to_numeric(df["flex_sink_psh_pump_mw"], errors="coerce").fillna(0.0).clip(lower=0.0)
    flex_other = pd.to_numeric(df.get("flex_sink_other_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)

    assert ((surplus - (absorbed + unabs)).abs() <= 1e-6).all()
    assert ((flex_total - absorbed).abs() <= 1e-6).all()
    assert ((flex_total - (flex_exports + flex_psh + flex_other)).abs() <= 1e-6).all()


def test_load_net_mode_depends_on_psh_coverage(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=48)
    raw.loc[raw.index[:12], "psh_pump_mw"] = pd.NA
    df_partial = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assert set(df_partial["load_net_mode"].astype(str).unique()) == {"entsoe_total_load_minus_psh_pumping"}

    raw_missing = make_raw_panel(n=48)
    raw_missing["psh_pump_mw"] = pd.NA
    df_missing = build_hourly_table(raw_missing, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assert set(df_missing["load_net_mode"].astype(str).unique()) == {"entsoe_total_load_no_pumping_adjust"}


def test_net_position_sign_auto_selects_negative_when_more_consistent(make_raw_panel, countries_cfg, thresholds_cfg):
    raw = make_raw_panel(n=72)
    raw["load_total_mw"] = 10000.0
    raw["net_position_mw"] = -500.0
    df = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    assert set(df["net_position_sign_choice"].astype(str).unique()) == {"negative_is_export"}
    assert (pd.to_numeric(df["exports_mw"], errors="coerce").fillna(0.0) >= 499.0).all()


def test_invariant_codes_in_sanity_check():
    df = pd.DataFrame(
        {
            "surplus_mw": [0.0, 0.0],
            "surplus_absorbed_mw": [0.0, 0.0],
            "surplus_unabsorbed_mw": [0.0, 0.0],
            "gen_must_run_mw": [0.0, 0.0],
            "gen_total_mw": [100.0, 100.0],
            "load_total_mw": [100.0, 100.0],
            "load_mw": [80.0, -1.0],
            "exports_mw": [0.0, 0.0],
            "psh_pump_mw": [15.0, -2.0],
        }
    )
    issues = sanity_check_core_definitions(df, far_energy=1.0, sr_energy=0.0, ir=0.0)
    assert any("INV_LOAD_001" in issue for issue in issues)
    assert any("INV_LOAD_002" in issue for issue in issues)
    assert any("INV_PSH_001" in issue for issue in issues)
