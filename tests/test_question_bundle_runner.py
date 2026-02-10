from __future__ import annotations

import pandas as pd

from src.config_loader import load_phase2_assumptions
from src.modules.question_bundle_runner import _annotate_comparison_interpretability, _evaluate_test_ledger, run_question_bundle
from src.modules.result import ModuleResult
from src.modules.test_registry import get_question_tests
from src.processing import build_hourly_table


def _build_hourly_map_for_fixture(
    countries_cfg: dict,
    thresholds_cfg: dict,
    make_raw_panel,
    countries: list[str],
    years: list[int],
) -> dict[tuple[str, int], pd.DataFrame]:
    out: dict[tuple[str, int], pd.DataFrame] = {}
    for country in countries:
        cfg = countries_cfg["countries"][country]
        for year in years:
            raw = make_raw_panel(n=168, year=year)
            out[(country, year)] = build_hourly_table(raw, country, year, cfg, thresholds_cfg, country)
    return out


def test_run_question_bundle_q1_hist_and_scen(
    annual_panel_fixture,
    countries_cfg,
    thresholds_cfg,
    make_raw_panel,
):
    assumptions_phase1 = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions_phase2 = load_phase2_assumptions()
    hourly_hist_map = _build_hourly_map_for_fixture(
        countries_cfg=countries_cfg,
        thresholds_cfg=thresholds_cfg,
        make_raw_panel=make_raw_panel,
        countries=["FR", "DE"],
        years=[2021, 2022, 2023, 2024],
    )

    bundle = run_question_bundle(
        question_id="Q1",
        annual_hist=annual_panel_fixture,
        hourly_hist_map=hourly_hist_map,
        assumptions_phase1=assumptions_phase1,
        assumptions_phase2=assumptions_phase2,
        selection={
            "countries": ["FR", "DE"],
            "years": [2021, 2022, 2023, 2024],
            "scenario_ids": ["BASE"],
            "scenario_years": [2030, 2040],
        },
        run_id="TEST_BUNDLE_Q1",
    )

    assert bundle.question_id == "Q1"
    assert bundle.hist_result.module_id == "Q1"
    assert "BASE" in bundle.scen_results
    assert not bundle.test_ledger.empty
    assert {"test_id", "mode", "status"}.issubset(bundle.test_ledger.columns)


def test_run_question_bundle_q4_executes_hist_modes(
    annual_panel_fixture,
    countries_cfg,
    thresholds_cfg,
    make_raw_panel,
):
    assumptions_phase1 = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions_phase2 = load_phase2_assumptions()
    hourly_hist_map = _build_hourly_map_for_fixture(
        countries_cfg=countries_cfg,
        thresholds_cfg=thresholds_cfg,
        make_raw_panel=make_raw_panel,
        countries=["FR"],
        years=[2024],
    )

    bundle = run_question_bundle(
        question_id="Q4",
        annual_hist=annual_panel_fixture,
        hourly_hist_map=hourly_hist_map,
        assumptions_phase1=assumptions_phase1,
        assumptions_phase2=assumptions_phase2,
        selection={
            "country": "FR",
            "countries": ["FR"],
            "year": 2024,
            "years": [2024],
            "objective": "FAR_TARGET",
            "power_grid": [0.0, 200.0, 500.0],
            "duration_grid": [2.0, 4.0],
            "scenario_ids": [],
            "scenario_years": [2040],
            "horizon_year": 2040,
        },
        run_id="TEST_BUNDLE_Q4",
    )

    assert bundle.question_id == "Q4"
    assert bundle.hist_result.module_id == "Q4"
    assert not bundle.test_ledger.empty
    assert "Q4-H-01" in bundle.test_ledger["test_id"].tolist()


def test_run_question_bundle_q4_multicountry_hist(
    annual_panel_fixture,
    countries_cfg,
    thresholds_cfg,
    make_raw_panel,
):
    assumptions_phase1 = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions_phase2 = load_phase2_assumptions()
    hourly_hist_map = _build_hourly_map_for_fixture(
        countries_cfg=countries_cfg,
        thresholds_cfg=thresholds_cfg,
        make_raw_panel=make_raw_panel,
        countries=["FR", "DE"],
        years=[2024],
    )

    bundle = run_question_bundle(
        question_id="Q4",
        annual_hist=annual_panel_fixture,
        hourly_hist_map=hourly_hist_map,
        assumptions_phase1=assumptions_phase1,
        assumptions_phase2=assumptions_phase2,
        selection={
            "countries": ["FR", "DE"],
            "year": 2024,
            "years": [2024],
            "objective": "FAR_TARGET",
            "power_grid": [0.0, 200.0],
            "duration_grid": [2.0],
            "scenario_ids": [],
            "scenario_years": [2040],
            "horizon_year": 2040,
        },
        run_id="TEST_BUNDLE_Q4_MULTI",
    )
    out = bundle.hist_result.tables.get("Q4_sizing_summary", pd.DataFrame())
    assert not out.empty
    assert {"FR", "DE"}.issubset(set(out["country"].astype(str)))


def test_run_question_bundle_q5_multicountry_hist(
    annual_panel_fixture,
    countries_cfg,
    thresholds_cfg,
    make_raw_panel,
):
    assumptions_phase1 = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions_phase2 = load_phase2_assumptions()
    hourly_hist_map = _build_hourly_map_for_fixture(
        countries_cfg=countries_cfg,
        thresholds_cfg=thresholds_cfg,
        make_raw_panel=make_raw_panel,
        countries=["FR", "DE"],
        years=[2021, 2022, 2023, 2024],
    )

    bundle = run_question_bundle(
        question_id="Q5",
        annual_hist=annual_panel_fixture,
        hourly_hist_map=hourly_hist_map,
        assumptions_phase1=assumptions_phase1,
        assumptions_phase2=assumptions_phase2,
        selection={
            "countries": ["FR", "DE"],
            "years": [2021, 2022, 2023, 2024],
            "scenario_ids": [],
            "scenario_years": [2030, 2040],
            "marginal_tech": "CCGT",
        },
        run_id="TEST_BUNDLE_Q5_MULTI",
    )
    out = bundle.hist_result.tables.get("Q5_summary", pd.DataFrame())
    assert not out.empty
    assert {"FR", "DE"}.issubset(set(out["country"].astype(str)))


def test_q3_comparison_annotation_flags_non_testable_and_fragile() -> None:
    raw = pd.DataFrame(
        [
            {
                "country": "FR",
                "scenario_id": "BASE",
                "metric": "inversion_k_demand",
                "hist_value": 0.10,
                "scen_value": 0.15,
                "delta": 0.05,
                "scen_status": "hors_scope_stage2",
            },
            {
                "country": "DE",
                "scenario_id": "BASE",
                "metric": "inversion_k_demand",
                "hist_value": 0.20,
                "scen_value": 0.20,
                "delta": 0.0,
                "scen_status": "stabilisation",
            },
            {
                "country": "ES",
                "scenario_id": "BASE",
                "metric": "inversion_k_demand",
                "hist_value": 0.10,
                "scen_value": 0.25,
                "delta": 0.15,
                "scen_status": "amelioration",
            },
        ]
    )
    out = _annotate_comparison_interpretability("Q3", raw)
    assert {"interpretability_status", "interpretability_reason"}.issubset(out.columns)
    assert out.loc[out["country"] == "FR", "interpretability_status"].iloc[0] == "NON_TESTABLE"
    assert out.loc[out["country"] == "DE", "interpretability_status"].iloc[0] == "FRAGILE"
    assert out.loc[out["country"] == "ES", "interpretability_status"].iloc[0] == "INFORMATIVE"


def _empty_module_result(module_id: str, mode: str, scenario_id: str | None = None) -> ModuleResult:
    return ModuleResult(
        module_id=module_id,
        run_id=f"TEST_{module_id}",
        selection={"mode": mode, "scenario_id": scenario_id},
        assumptions_used=[],
        kpis={},
        tables={},
        figures=[],
        narrative_md="",
        checks=[],
        warnings=[],
        mode=mode,
        scenario_id=scenario_id,
    )


def test_q1_s02_warn_when_all_non_base_deltas_are_zero() -> None:
    spec = [s for s in get_question_tests("Q1", mode="SCEN") if s.test_id == "Q1-S-02"]
    hist = _empty_module_result("Q1", "HIST")
    scen_results = {
        "BASE": ModuleResult(
            module_id="Q1",
            run_id="TEST_Q1_BASE",
            selection={"mode": "SCEN", "scenario_id": "BASE"},
            assumptions_used=[],
            kpis={},
            tables={"Q1_country_summary": pd.DataFrame([{"country": "FR", "bascule_year_market": 2030.0}])},
            figures=[],
            narrative_md="",
            checks=[],
            warnings=[],
            mode="SCEN",
            scenario_id="BASE",
        ),
        "DEMAND_UP": ModuleResult(
            module_id="Q1",
            run_id="TEST_Q1_DEMAND",
            selection={"mode": "SCEN", "scenario_id": "DEMAND_UP"},
            assumptions_used=[],
            kpis={},
            tables={"Q1_country_summary": pd.DataFrame([{"country": "FR", "bascule_year_market": 2030.0}])},
            figures=[],
            narrative_md="",
            checks=[],
            warnings=[],
            mode="SCEN",
            scenario_id="DEMAND_UP",
        ),
    }
    ledger = _evaluate_test_ledger("Q1", spec, hist, scen_results, {})
    row = ledger[ledger["scenario_id"] == "DEMAND_UP"].iloc[0]
    assert row["status"] == "WARN"


def test_q1_s02_pass_when_nonzero_share_reaches_threshold() -> None:
    spec = [s for s in get_question_tests("Q1", mode="SCEN") if s.test_id == "Q1-S-02"]
    hist = _empty_module_result("Q1", "HIST")
    base_df = pd.DataFrame(
        [
            {"country": "FR", "bascule_year_market": 2030.0},
            {"country": "DE", "bascule_year_market": 2030.0},
            {"country": "ES", "bascule_year_market": 2030.0},
            {"country": "NL", "bascule_year_market": 2030.0},
            {"country": "BE", "bascule_year_market": 2030.0},
        ]
    )
    scen_df = base_df.copy()
    scen_df.loc[scen_df["country"] == "FR", "bascule_year_market"] = 2031.0  # 1/5 -> 20%

    scen_results = {
        "BASE": ModuleResult(
            module_id="Q1",
            run_id="TEST_Q1_BASE",
            selection={"mode": "SCEN", "scenario_id": "BASE"},
            assumptions_used=[],
            kpis={},
            tables={"Q1_country_summary": base_df},
            figures=[],
            narrative_md="",
            checks=[],
            warnings=[],
            mode="SCEN",
            scenario_id="BASE",
        ),
        "FLEX_UP": ModuleResult(
            module_id="Q1",
            run_id="TEST_Q1_FLEX",
            selection={"mode": "SCEN", "scenario_id": "FLEX_UP"},
            assumptions_used=[],
            kpis={},
            tables={"Q1_country_summary": scen_df},
            figures=[],
            narrative_md="",
            checks=[],
            warnings=[],
            mode="SCEN",
            scenario_id="FLEX_UP",
        ),
    }
    ledger = _evaluate_test_ledger("Q1", spec, hist, scen_results, {})
    row = ledger[ledger["scenario_id"] == "FLEX_UP"].iloc[0]
    assert row["status"] == "PASS"
