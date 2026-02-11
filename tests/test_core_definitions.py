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
