from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.modules.bundle_result import QuestionBundleResult, export_question_bundle
from src.modules.result import ModuleResult


def _fake_module(module_id: str, run_id: str, mode: str = "HIST", scenario_id: str | None = None) -> ModuleResult:
    return ModuleResult(
        module_id=module_id,
        run_id=run_id,
        selection={"mode": mode, "scenario_id": scenario_id},
        assumptions_used=[],
        kpis={"k": 1},
        tables={f"{module_id}_table": pd.DataFrame([{"a": 1, "b": 2}])},
        figures=[],
        narrative_md=f"{module_id} narrative",
        checks=[{"status": "PASS", "code": "OK", "message": "ok"}],
        warnings=[],
        mode=mode,
        scenario_id=scenario_id,
    )


def test_export_question_bundle_writes_expected_files(tmp_path: Path) -> None:
    run_id = "BUNDLE_EXPORT_TEST"
    hist = _fake_module("Q1", run_id, mode="HIST")
    scen = {"BASE": _fake_module("Q1", run_id, mode="SCEN", scenario_id="BASE")}
    bundle = QuestionBundleResult(
        question_id="Q1",
        run_id=run_id,
        selection={"countries": ["FR"]},
        hist_result=hist,
        scen_results=scen,
        test_ledger=pd.DataFrame([{"test_id": "Q1-H-01", "status": "PASS"}]),
        comparison_table=pd.DataFrame([{"metric": "x", "hist_value": 1, "scen_value": 2}]),
        checks=[{"status": "PASS", "code": "BUNDLE", "message": "ok"}],
        warnings=[],
        narrative_md="bundle narrative",
    )

    out = export_question_bundle(bundle, base_dir=str(tmp_path))
    assert (out / "summary.json").exists()
    assert (out / "narrative.md").exists()
    assert (out / "test_ledger.csv").exists()
    assert (out / "comparison_hist_vs_scen.csv").exists()
    assert (out / "hist" / "summary.json").exists()
    assert (out / "hist" / "tables" / "Q1_table.csv").exists()
    assert (out / "scen" / "BASE" / "summary.json").exists()
    assert (out / "scen" / "BASE" / "tables" / "Q1_table.csv").exists()
