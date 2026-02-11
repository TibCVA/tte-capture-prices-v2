from __future__ import annotations

import pandas as pd

from src.modules.q1_transition import run_q1
from src.processing import build_hourly_table


def test_q1_transition_classification(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q1(annual_panel_fixture, assumptions, {"countries": ["FR", "DE"], "years": [2021, 2022, 2023, 2024]}, "test")
    panel = res.tables["Q1_year_panel"]
    assert (panel["phase_market"] == "phase2").any()


def test_q1_bascule_year_first_year_condition(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q1(annual_panel_fixture, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    summary = res.tables["Q1_country_summary"]
    assert summary["bascule_year_market"].notna().all()


def test_q1_no_bascule_on_quality_fail(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    df = annual_panel_fixture.copy()
    df.loc[(df["country"] == "FR") & (df["year"] == 2024), "quality_flag"] = "FAIL"
    res = run_q1(df, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    # Baseline from fixture is 2022+; quality fail on 2024 should not create illegal NaN-based bascule
    assert "Q1_CAPTURE_NAN_BASCULE" not in [c.get("code") for c in res.checks]


def test_q1_new_tables_present_and_before_after_windows(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q1(annual_panel_fixture, assumptions, {"countries": ["FR", "DE"], "years": [2021, 2022, 2023, 2024]}, "test")

    expected_tables = {
        "Q1_rule_definition",
        "Q1_rule_application",
        "Q1_before_after_bascule",
        "Q1_scope_audit",
        "Q1_ir_diagnostics",
    }
    assert expected_tables.issubset(set(res.tables.keys()))

    before_after = res.tables["Q1_before_after_bascule"]
    assert not before_after.empty
    fr = before_after[before_after["country"] == "FR"].iloc[0]
    assert int(fr["pre_window_start_year"]) == int(fr["bascule_year_market"] - 3)
    assert int(fr["pre_window_end_year"]) == int(fr["bascule_year_market"] - 1)
    assert int(fr["post_window_start_year"]) == int(fr["bascule_year_market"])
    assert int(fr["post_window_end_year"]) == int(fr["bascule_year_market"] + 2)


def test_q1_scope_review_check_triggers(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    raw = make_raw_panel(n=168, year=2024)
    hourly = build_hourly_table(raw, "DE", 2024, countries_cfg["countries"]["DE"], thresholds_cfg, "DE")
    hourly_map = {("DE", 2024): hourly}

    res = run_q1(
        annual_panel_fixture,
        assumptions,
        {"countries": ["DE"], "years": [2024]},
        "test",
        hourly_by_country_year=hourly_map,
    )

    codes = [str(c.get("code")) for c in res.checks]
    assert {"Q1_MUSTRUN_SCOPE_LOW_COVERAGE", "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE"} & set(codes)
    scope = res.tables["Q1_scope_audit"]
    assert not scope.empty
    assert 0.0 <= float(scope.iloc[0]["must_run_scope_coverage"]) <= 1.0


def test_q1_stage2_score_decomposition_sums(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q1(annual_panel_fixture, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    panel = res.tables["Q1_year_panel"]
    assert not panel.empty
    row = panel.iloc[-1]
    expected = (
        float(row["stage2_points_low_price"])
        + float(row["stage2_points_capture"])
        + float(row["stage2_points_physical"])
        + float(row["stage2_points_vol"])
    )
    assert float(row["stage2_market_score"]) == expected


def test_q1_no_false_phase2_without_low_prices(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    df = annual_panel_fixture.copy()
    mask = (df["country"] == "FR") & (df["year"] == 2024)
    df.loc[mask, "h_negative_obs"] = 0.0
    df.loc[mask, "h_below_5_obs"] = 50.0
    df.loc[mask, "sr_energy"] = 0.0
    df.loc[mask, "sr_hours"] = 0.0
    df.loc[mask, "far_energy"] = 0.99
    df.loc[mask, "ir_p10"] = 0.4
    df.loc[mask, "capture_ratio_pv"] = 0.5
    df.loc[mask, "capture_ratio_pv_vs_ttl"] = 0.5

    res = run_q1(df, assumptions, {"countries": ["FR"], "years": [2024]}, "test")
    panel = res.tables["Q1_year_panel"]
    row = panel[(panel["country"] == "FR") & (panel["year"] == 2024)].iloc[0]
    assert bool(row["is_phase2_market"]) is False


def test_q1_confidence_penalizes_low_quality(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    base = annual_panel_fixture.copy()
    base = base[base["country"] == "FR"].copy()

    good = base.copy()
    good["regime_coherence"] = 0.9
    good_res = run_q1(good, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    good_conf = float(good_res.tables["Q1_country_summary"].iloc[0]["bascule_confidence"])

    bad = base.copy()
    bad["regime_coherence"] = 0.01
    bad_res = run_q1(bad, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, "test")
    bad_conf = float(bad_res.tables["Q1_country_summary"].iloc[0]["bascule_confidence"])

    assert bad_conf < good_conf
    assert bad_conf < 0.8


def test_q1_capture_low_never_true_when_capture_ratio_pv_ge_one(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    df = annual_panel_fixture.copy()
    mask = (df["country"] == "FR") & (df["year"] == 2024)
    df.loc[mask, "capture_ratio_pv"] = 1.05
    df.loc[mask, "capture_ratio_pv_vs_ttl"] = 0.60  # reporting only, must not drive the flag.
    res = run_q1(df, assumptions, {"countries": ["FR"], "years": [2024]}, "test")
    row = res.tables["Q1_year_panel"].iloc[0]
    assert bool(row["flag_capture_pv_low"]) is False


def test_q1_stage1_healthy_year_is_tagged(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    df = annual_panel_fixture.copy()
    mask = (df["country"] == "FR") & (df["year"] == 2024)
    df.loc[mask, "capture_ratio_pv"] = 0.95
    df.loc[mask, "capture_ratio_wind"] = 0.95
    df.loc[mask, "h_negative_obs"] = 20.0
    df.loc[mask, "h_below_5_obs"] = 50.0
    df.loc[mask, "sr_hours"] = 0.02
    df.loc[mask, "sr_hours_share"] = 0.02
    df.loc[mask, "far_observed"] = 0.98
    df.loc[mask, "far_energy"] = 0.98
    df.loc[mask, "ir_p10"] = 1.0
    df.loc[mask, "avg_daily_spread_obs"] = 20.0
    df.loc[mask, "days_spread_gt50"] = 20.0
    res = run_q1(df, assumptions, {"countries": ["FR"], "years": [2024]}, "test")
    row = res.tables["Q1_year_panel"].iloc[0]
    assert bool(row["is_stage1_criteria"]) is True


def test_q1_crisis_years_are_explicitly_configured(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q1(
        annual_panel_fixture,
        assumptions,
        {"countries": ["FR"], "years": [2021, 2022, 2023, 2024], "crisis_years": [2022]},
        "test",
    )
    panel = res.tables["Q1_year_panel"]
    crisis_map = {int(r["year"]): bool(r["crisis_year"]) for _, r in panel.iterrows()}
    assert crisis_map[2022] is True
    assert crisis_map[2021] is False
    assert crisis_map[2023] is False
    assert crisis_map[2024] is False


def test_q1_stage2_candidate_not_blocked_by_market_physical_gap(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    df = annual_panel_fixture.copy()
    mask = (df["country"] == "FR") & (df["year"] == 2024)
    df.loc[mask, "quality_flag"] = "OK"
    df.loc[mask, "h_negative_obs"] = 400.0
    df.loc[mask, "h_below_5_obs"] = 700.0
    df.loc[mask, "capture_ratio_pv"] = 0.70
    df.loc[mask, "capture_ratio_wind"] = 0.85
    df.loc[mask, "sr_hours"] = 0.12
    df.loc[mask, "sr_hours_share"] = 0.12
    df.loc[mask, "far_energy"] = 0.93
    df.loc[mask, "far_observed"] = 0.93
    df.loc[mask, "ir_p10"] = 1.7

    findings = pd.DataFrame(
        [
            {
                "country": "FR",
                "year": 2024,
                "code": "RC_NEG_NOT_IN_SURPLUS",
                "evidence": "ratio=0.10",
            }
        ]
    )
    res = run_q1(
        df,
        assumptions,
        {"countries": ["FR"], "years": [2024], "crisis_years": [2022]},
        "test",
        validation_findings_df=findings,
    )
    row = res.tables["Q1_year_panel"].iloc[0]
    assert bool(row["market_physical_gap_flag"]) is True
    assert bool(row["quality_ok"]) is True
    assert bool(row["stage2_candidate_year"]) is True


def test_q1_country_summary_has_bascule_status_columns(annual_panel_fixture):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    res = run_q1(annual_panel_fixture, assumptions, {"countries": ["FR", "DE"], "years": [2021, 2022, 2023, 2024]}, "test")
    summary = res.tables["Q1_country_summary"]
    assert "bascule_status_market" in summary.columns
    assert "bascule_status_physical" in summary.columns
    assert summary["bascule_status_market"].astype(str).str.len().gt(0).all()
    assert summary["bascule_status_physical"].astype(str).str.len().gt(0).all()
