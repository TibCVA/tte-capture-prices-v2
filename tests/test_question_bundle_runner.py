from __future__ import annotations

import numpy as np
import pandas as pd

import src.modules.question_bundle_runner as qbundle_runner
from src.config_loader import load_phase2_assumptions
from src.modules.question_bundle_runner import (
    _annotate_comparison_interpretability,
    _check_q1_scenario_effect_present,
    _check_q3_scenario_stress_sufficiency,
    _evaluate_test_ledger,
    _q1_comparison,
    run_question_bundle,
)
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
    if "BASE" not in bundle.scen_results:
        scen_rows = bundle.test_ledger[bundle.test_ledger["mode"].astype(str).str.upper() == "SCEN"]
        assert not scen_rows.empty
        assert scen_rows["status"].astype(str).isin(["NON_TESTABLE", "PASS", "WARN"]).all()
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
    mode_scopes = {str(c.get("scope", "")) for c in bundle.checks}
    assert any(scope.startswith("HIST_MODE_") for scope in mode_scopes)
    assert "Q4_extra_mode_checks" in bundle.hist_result.tables


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


def test_q1_comparison_encodes_not_reached_without_nan() -> None:
    hist = ModuleResult(
        module_id="Q1",
        run_id="TEST_Q1_HIST",
        selection={"mode": "HIST"},
        assumptions_used=[],
        kpis={},
        tables={
            "Q1_country_summary": pd.DataFrame(
                [
                    {"country": "FR", "bascule_year_market": 2028.0, "bascule_status_market": "reached"},
                    {"country": "DE", "bascule_year_market": 2032.0, "bascule_status_market": "reached"},
                ]
            )
        },
        figures=[],
        narrative_md="",
        checks=[],
        warnings=[],
        mode="HIST",
        scenario_id="HIST",
    )
    scen = ModuleResult(
        module_id="Q1",
        run_id="TEST_Q1_SCEN",
        selection={"mode": "SCEN", "scenario_id": "LOW_RIGIDITY"},
        assumptions_used=[],
        kpis={},
        tables={
            "Q1_country_summary": pd.DataFrame(
                [
                    {"country": "FR", "bascule_year_market": 2030.0, "bascule_status_market": "reached"},
                    {"country": "DE", "bascule_year_market": np.nan, "bascule_status_market": "not_reached_in_window"},
                ]
            )
        },
        figures=[],
        narrative_md="",
        checks=[],
        warnings=[],
        mode="SCEN",
        scenario_id="LOW_RIGIDITY",
    )

    cmp = _q1_comparison(hist, {"LOW_RIGIDITY": scen})
    assert not cmp.empty
    assert cmp["reason"].astype(str).str.contains("delta_non_interpretable_nan").sum() == 0
    for v in cmp["scen_value"].tolist():
        assert isinstance(v, int) or (v is None)
    de = cmp[cmp["country"].astype(str) == "DE"].iloc[0]
    assert str(de["status"]) == "OK_NOT_REACHED"
    assert str(de["reason"]) == "bascule_not_reached_by_horizon"

    annotated = _annotate_comparison_interpretability("Q1", cmp)
    assert annotated["interpretability_reason"].astype(str).str.contains("delta_non_interpretable_nan").sum() == 0


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
        "LOW_RIGIDITY": ModuleResult(
            module_id="Q1",
            run_id="TEST_Q1_LOW_RIGIDITY",
            selection={"mode": "SCEN", "scenario_id": "LOW_RIGIDITY"},
            assumptions_used=[],
            kpis={},
            tables={"Q1_country_summary": scen_df},
            figures=[],
            narrative_md="",
            checks=[],
            warnings=[],
            mode="SCEN",
            scenario_id="LOW_RIGIDITY",
        ),
    }
    ledger = _evaluate_test_ledger("Q1", spec, hist, scen_results, {})
    row = ledger[ledger["scenario_id"] == "LOW_RIGIDITY"].iloc[0]
    assert row["status"] == "PASS"


def test_q3_s01_non_testable_when_hors_scope_majority() -> None:
    spec = [s for s in get_question_tests("Q3", mode="SCEN") if s.test_id == "Q3-S-01"]
    hist = _empty_module_result("Q3", "HIST")
    scen_results = {
        "BASE": ModuleResult(
            module_id="Q3",
            run_id="TEST_Q3_BASE",
            selection={"mode": "SCEN", "scenario_id": "BASE"},
            assumptions_used=[],
            kpis={},
            tables={
                "Q3_status": pd.DataFrame(
                    [
                        {
                            "country": "FR",
                            "status": "HORS_SCOPE_PHASE2",
                            "inversion_k_demand": 0.0,
                            "inversion_r_mustrun": 0.0,
                            "additional_absorbed_needed_TWh_year": 0.0,
                        }
                    ]
                )
            },
            figures=[],
            narrative_md="",
            checks=[],
            warnings=[],
            mode="SCEN",
            scenario_id="BASE",
        )
    }
    ledger = _evaluate_test_ledger("Q3", spec, hist, scen_results, {}, expected_scenario_ids=["BASE"])
    row = ledger.iloc[0]
    assert row["status"] == "NON_TESTABLE"


def test_evaluate_test_ledger_marks_missing_requested_scenario_non_testable() -> None:
    spec = [s for s in get_question_tests("Q1", mode="SCEN") if s.test_id == "Q1-S-01"]
    hist = _empty_module_result("Q1", "HIST")
    scen_results = {
        "BASE": ModuleResult(
            module_id="Q1",
            run_id="TEST_Q1_BASE_ONLY",
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
        )
    }
    ledger = _evaluate_test_ledger(
        "Q1",
        spec,
        hist,
        scen_results,
        {},
        expected_scenario_ids=["BASE", "DEMAND_UP"],
    )
    missing = ledger[ledger["scenario_id"].astype(str) == "DEMAND_UP"]
    assert not missing.empty
    assert set(missing["status"].astype(str).unique()) == {"NON_TESTABLE"}


def test_q4_h02_ignores_non_physical_extra_mode_fails() -> None:
    spec = [s for s in get_question_tests("Q4", mode="HIST") if s.test_id == "Q4-H-02"]
    hist = _empty_module_result("Q4", "HIST")
    hist.checks = [{"status": "PASS", "code": "Q4_PASS", "message": "ok"}]

    extra_mode = _empty_module_result("Q4", "HIST")
    extra_mode.checks = [
        {"status": "FAIL", "code": "Q4_SURPLUS_UNABS_NON_MONOTONIC_ENERGY", "message": "mode-specific artefact"},
        {"status": "FAIL", "code": "Q4_HNEG_NON_MONOTONIC_ENERGY", "message": "mode-specific artefact"},
    ]
    ledger = _evaluate_test_ledger("Q4", spec, hist, {}, {"HIST_PRICE_ARBITRAGE_SIMPLE": extra_mode})
    row = ledger.iloc[0]
    assert row["status"] == "PASS"


def test_q4_h02_fails_on_relevant_hist_physical_fail() -> None:
    spec = [s for s in get_question_tests("Q4", mode="HIST") if s.test_id == "Q4-H-02"]
    hist = _empty_module_result("Q4", "HIST")
    hist.checks = [{"status": "FAIL", "code": "Q4_ZERO_SIZE_AFTER_DIFFERS_FROM_BEFORE", "message": "invariant"}]

    ledger = _evaluate_test_ledger("Q4", spec, hist, {}, {})
    row = ledger.iloc[0]
    assert row["status"] == "FAIL"


def test_q4_h02_fails_on_relevant_extra_mode_physical_fail() -> None:
    spec = [s for s in get_question_tests("Q4", mode="HIST") if s.test_id == "Q4-H-02"]
    hist = _empty_module_result("Q4", "HIST")
    hist.checks = [{"status": "PASS", "code": "Q4_PASS", "message": "ok"}]

    extra_mode = _empty_module_result("Q4", "HIST")
    extra_mode.checks = [{"status": "FAIL", "code": "Q4_SOC_NEG", "message": "soc negative"}]
    ledger = _evaluate_test_ledger("Q4", spec, hist, {}, {"HIST_PV_COLOCATED": extra_mode})
    row = ledger.iloc[0]
    assert row["status"] == "FAIL"
    assert "FAIL_CODES:" in str(row["value"])
    assert "Q4_SOC_NEG" in str(row["value"])


def test_q1_scenario_effect_present_fails_when_non_base_delta_is_zero() -> None:
    comparison = pd.DataFrame(
        [
            {"country": "DE", "scenario_id": "BASE", "delta": 0.0},
            {"country": "ES", "scenario_id": "DEMAND_UP", "delta": 0.0},
            {"country": "DE", "scenario_id": "LOW_RIGIDITY", "delta": 0.0},
        ]
    )
    checks = _check_q1_scenario_effect_present(comparison)
    assert len(checks) == 1
    assert checks[0]["code"] == "Q1_SCENARIO_EFFECT_PRESENT"
    assert checks[0]["status"] == "FAIL"


def test_q3_scenario_stress_sufficiency_fails_when_all_non_base_are_hors_scope() -> None:
    comparison = pd.DataFrame(
        [
            {"country": "DE", "scenario_id": "BASE", "scen_status": "stable"},
            {"country": "DE", "scenario_id": "DEMAND_UP", "scen_status": "HORS_SCOPE_PHASE2"},
            {"country": "ES", "scenario_id": "DEMAND_UP", "scen_status": "HORS_SCOPE_PHASE2"},
            {"country": "DE", "scenario_id": "LOW_RIGIDITY", "scen_status": "HORS_SCOPE_PHASE2"},
            {"country": "ES", "scenario_id": "LOW_RIGIDITY", "scen_status": "HORS_SCOPE_PHASE2"},
        ]
    )
    checks = _check_q3_scenario_stress_sufficiency(comparison)
    assert len(checks) == 1
    assert checks[0]["code"] == "Q3_SCENARIO_STRESS_SUFFICIENCY"
    assert checks[0]["status"] == "FAIL"


def test_run_question_bundle_q5_adds_market_coherence_checks(monkeypatch) -> None:
    assumptions_phase1 = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions_phase2 = load_phase2_assumptions()
    annual_hist = pd.DataFrame([{"country": "FR", "year": 2024}])

    def _mk_q5_result(run_id: str, scenario_id: str | None, tca: float, ttl: float) -> ModuleResult:
        table = pd.DataFrame(
            [
                {
                    "country": "FR",
                    "year": 2030,
                    "tca_ccgt_eur_mwh": tca,
                    "ttl_eur_mwh": ttl,
                }
            ]
        )
        mode = "SCEN" if scenario_id is not None else "HIST"
        return ModuleResult(
            module_id="Q5",
            run_id=run_id,
            selection={"mode": mode, "scenario_id": scenario_id},
            assumptions_used=[],
            kpis={},
            tables={"Q5_summary": table},
            figures=[],
            narrative_md="",
            checks=[],
            warnings=[],
            mode=mode,
            scenario_id=scenario_id,
            horizon_year=2030,
        )

    def _fake_run_hist_module(**kwargs):
        return _mk_q5_result("HIST", None, tca=100.0, ttl=150.0), {}

    def _fake_run_scen_module(**kwargs):
        sid = str(kwargs["scenario_id"])
        if sid == "BASE":
            return _mk_q5_result("BASE", "BASE", tca=100.0, ttl=150.0)
        if sid == "HIGH_CO2":
            return _mk_q5_result("HIGH_CO2", "HIGH_CO2", tca=120.0, ttl=170.0)
        if sid == "HIGH_GAS":
            return _mk_q5_result("HIGH_GAS", "HIGH_GAS", tca=130.0, ttl=165.0)
        return None

    monkeypatch.setattr(qbundle_runner, "_run_hist_module", _fake_run_hist_module)
    monkeypatch.setattr(qbundle_runner, "_run_scen_module", _fake_run_scen_module)
    monkeypatch.setattr(qbundle_runner, "_ensure_scenario_outputs", lambda **kwargs: (True, "ok"))

    bundle = run_question_bundle(
        question_id="Q5",
        annual_hist=annual_hist,
        hourly_hist_map={},
        assumptions_phase1=assumptions_phase1,
        assumptions_phase2=assumptions_phase2,
        selection={
            "countries": ["FR"],
            "years": [2024],
            "scenario_ids": ["BASE", "HIGH_CO2", "HIGH_GAS"],
            "scenario_years": [2030],
        },
        run_id="TEST_Q5_BUNDLE_CHECKS",
    )

    q5_001 = [c for c in bundle.checks if str(c.get("code")) == "TEST_Q5_001"]
    q5_002 = [c for c in bundle.checks if str(c.get("code")) == "TEST_Q5_002"]
    assert q5_001 and any(str(c.get("status")) == "PASS" for c in q5_001)
    assert q5_002 and any(str(c.get("status")) == "PASS" for c in q5_002)


def test_q5_high_scenario_uses_fallback_base_anchor_when_base_missing(monkeypatch) -> None:
    assumptions_phase1 = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    assumptions_phase2 = load_phase2_assumptions()
    annual_hist = pd.DataFrame([{"country": "FR", "year": 2024}])
    idx = pd.date_range("2035-01-01", periods=48, freq="h", tz="UTC")
    hourly = pd.DataFrame(
        {
            "price_da_eur_mwh": 60.0,
            "load_mw": 1000.0,
            "gen_vre_mw": 500.0,
            "gen_must_run_mw": 450.0,
            "nrl_mw": 50.0,
            "surplus_mw": 0.0,
            "surplus_unabsorbed_mw": 0.0,
            "gen_solar_mw": 200.0,
        },
        index=idx,
    )

    monkeypatch.setattr(
        qbundle_runner,
        "_load_scenario_hourly_map",
        lambda scenario_id, countries, years: {(str(countries[0]), int(years[0])): hourly.copy()},
    )
    monkeypatch.setattr(
        qbundle_runner,
        "_phase2_commodity_daily",
        lambda assumptions_phase2, scenario_id, country, years: pd.DataFrame(
            {
                "date": pd.date_range("2035-01-01", periods=10, freq="D"),
                "gas_price_eur_mwh_th": 45.0,
                "co2_price_eur_t": 120.0,
            }
        ),
    )
    monkeypatch.setattr(
        qbundle_runner,
        "_resolve_q5_base_anchor_for_country",
        lambda **kwargs: (
            {
                "base_tca_eur_mwh": 100.0,
                "base_tca_ccgt_eur_mwh": 100.0,
                "base_tca_coal_eur_mwh": 90.0,
                "base_ttl_model_eur_mwh": 120.0,
                "base_ttl_observed_eur_mwh": 120.0,
                "base_gas_eur_per_mwh_th": 35.0,
                "base_co2_eur_per_t": 80.0,
                "base_year_reference": 2024.0,
                "base_ref_source_year": 2024.0,
                "base_ref_status_override": "warn_fallback_from_hist",
                "base_ref_reason_override": "fallback_from_hist:2024",
            },
            "warn_fallback_from_hist",
        ),
    )

    def _fake_run_q5(hourly_df, assumptions_df, selection, run_id, **kwargs):
        row = {
            "country": str(selection.get("country", "")),
            "scenario_id": str(selection.get("scenario_id", "")),
            "base_ref_status": str(selection.get("base_ref_status_override", "ok")),
            "status": str(selection.get("base_ref_status_override", "ok")),
            "base_ref_reason": str(selection.get("base_ref_reason_override", "")),
        }
        return ModuleResult(
            module_id="Q5",
            run_id=run_id,
            selection=selection,
            assumptions_used=[],
            kpis={},
            tables={"Q5_summary": pd.DataFrame([row]), "q5_quality_summary": pd.DataFrame([{"quality_status": "WARN"}])},
            figures=[],
            narrative_md="",
            checks=[],
            warnings=[],
            mode="SCEN",
            scenario_id=str(selection.get("scenario_id", "")),
            horizon_year=selection.get("horizon_year"),
        )

    monkeypatch.setattr(qbundle_runner, "run_q5", _fake_run_q5)

    res = qbundle_runner._run_scen_module(
        question_id="Q5",
        scenario_id="HIGH_CO2",
        annual_hist=annual_hist,
        assumptions_phase1=assumptions_phase1,
        assumptions_phase2=assumptions_phase2,
        selection={"countries": ["FR"], "ttl_target_eur_mwh": 160.0},
        scenario_years=[2035],
    )
    assert res is not None
    q5_summary = res.tables.get("Q5_summary", pd.DataFrame())
    assert not q5_summary.empty
    assert set(q5_summary["base_ref_status"].astype(str).unique()) == {"warn_fallback_from_hist"}
    base_checks = [c for c in res.checks if str(c.get("code")) == "Q5_BASE_SCENARIO_MISSING"]
    assert base_checks and any(str(c.get("status")) == "PASS" for c in base_checks)
