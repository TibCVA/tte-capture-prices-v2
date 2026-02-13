from __future__ import annotations

import json
import os
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pandas as pd

from src.modules.bundle_result import QuestionBundleResult
from src.modules.result import ModuleResult


def _load_accueil_module() -> ModuleType:
    path = Path("app/pages/00_Accueil.py")
    spec = spec_from_file_location(f"tte_test_accueil_{id(path)}", str(path))
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_fake_run(root: Path, run_id: str, include_question_count: int = 5) -> Path:
    questions = ["Q1", "Q2", "Q3", "Q4", "Q5"][:include_question_count]
    run_dir = root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    for qid in questions:
        q_dir = run_dir / qid
        q_dir.mkdir(parents=True, exist_ok=True)
        summary = {
            "question_id": qid,
            "run_id": run_id,
            "selection": {"countries": ["FR"]},
            "checks": [{"status": "PASS", "code": f"{qid}_PASS", "message": "ok", "scope": "HIST", "scenario_id": ""}],
            "warnings": [],
        }
        (q_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False), encoding="utf-8")

        pd.DataFrame(
            [
                {
                    "test_id": f"{qid}-H-01",
                    "question_id": qid,
                    "source_ref": "slides",
                    "mode": "HIST",
                    "scenario_group": "HIST_BASE",
                    "title": "check hist",
                    "what_is_tested": "hist",
                    "metric_rule": "rule",
                    "severity_if_fail": "LOW",
                    "scenario_id": "",
                    "status": "PASS",
                    "value": "1",
                    "threshold": ">=0",
                    "interpretation": "ok",
                }
            ]
        ).to_csv(q_dir / "test_ledger.csv", index=False)
        pd.DataFrame(
            [
                {
                    "country": "FR",
                    "scenario_id": "BASE",
                    "metric": "metric_x",
                    "hist_value": 1.0,
                    "scen_value": 2.0,
                    "delta": 1.0,
                }
            ]
        ).to_csv(q_dir / "comparison_hist_vs_scen.csv", index=False)

        hist_dir = q_dir / "hist"
        hist_dir.mkdir(parents=True, exist_ok=True)
        (hist_dir / "summary.json").write_text(
            json.dumps(
                {
                    "module_id": qid,
                    "run_id": run_id,
                    "selection": {"countries": ["FR"]},
                    "checks": [{"status": "PASS", "code": f"{qid}_H", "message": "ok", "scope": "HIST", "scenario_id": ""}],
                    "assumptions_used": [],
                    "kpis": {},
                    "warnings": [],
                    "mode": "HIST",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        scen_dir = q_dir / "scen" / "BASE"
        scen_dir.mkdir(parents=True, exist_ok=True)
        (scen_dir / "summary.json").write_text(
            json.dumps(
                {
                    "module_id": qid,
                    "run_id": run_id,
                    "selection": {"countries": ["FR"]},
                    "checks": [{"status": "PASS", "code": f"{qid}_S", "message": "ok", "scope": "SCEN", "scenario_id": "BASE"}],
                    "assumptions_used": [],
                    "kpis": {},
                    "warnings": [],
                    "mode": "SCEN",
                    "scenario_id": "BASE",
                    "horizon_year": 2035,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (q_dir / "narrative.md").write_text(f"Narrative {qid}", encoding="utf-8")

    return run_dir


def _fake_bundle(question_id: str, run_id: str, status: str) -> QuestionBundleResult:
    checks = [{"status": status, "code": f"{question_id}_{status}", "message": "", "scope": "HIST", "scenario_id": ""}]
    return _fake_bundle_with_checks(question_id, run_id, checks)


def _fake_bundle_with_checks(question_id: str, run_id: str, checks: list[dict[str, str]]) -> QuestionBundleResult:
    return QuestionBundleResult(
        question_id=question_id,
        run_id=run_id,
        selection={"countries": ["FR"]},
        hist_result=ModuleResult(
            module_id=question_id,
            run_id=run_id,
            selection={"countries": ["FR"]},
            assumptions_used=[],
            kpis={},
            tables={},
            figures=[],
            narrative_md="",
            checks=checks,
            warnings=[],
            mode="HIST",
        ),
        scen_results={},
        test_ledger=pd.DataFrame(),
        comparison_table=pd.DataFrame(),
        checks=checks,
        warnings=[],
        narrative_md="",
    )


def test_clear_question_bundle_session_state_removes_question_keys_and_last_run() -> None:
    module = _load_accueil_module()
    session_state = {
        "q1_bundle_result": {"old": 1},
        "q2_bundle_result": {"old": 2},
        "q3_bundle_result": {"old": 3},
        "q4_bundle_result": {"old": 4},
        "q5_bundle_result": {"old": 5},
        "last_full_refresh_run_id": "RUN_OLD",
        "other_key": "kept",
    }
    module.st.session_state = session_state

    module._clear_question_bundle_session_state()

    for key in ["q1_bundle_result", "q2_bundle_result", "q3_bundle_result", "q4_bundle_result", "q5_bundle_result", "last_full_refresh_run_id"]:
        assert key not in session_state
    assert session_state["other_key"] == "kept"


def test_hydrate_loads_when_check_fail_and_marks_quality(monkeypatch, tmp_path: Path) -> None:
    module = _load_accueil_module()

    base = tmp_path / "outputs" / "combined"
    _build_fake_run(base, run_id="RUN_FAIL")
    monkeypatch.setattr(module, "_to_abs_project_path", lambda path_like: base)

    session_state = {"other": "kept"}
    fake_st = SimpleNamespace(
        session_state=session_state,
        cache_data=SimpleNamespace(clear=lambda: None),
        cache_resource=SimpleNamespace(clear=lambda: None),
    )
    module.st = fake_st

    def fake_loader(run_id: str, question_id: str, base_dir: str = "outputs/combined", **kwargs):  # noqa: ARG001
        status = "FAIL" if question_id == "Q3" else "PASS"
        return _fake_bundle(question_id, run_id, status), base / run_id / question_id

    module.load_question_bundle_from_combined_run_safe = fake_loader
    module.load_assumptions_table = lambda: pd.DataFrame()
    module.load_phase2_assumptions_table = lambda: pd.DataFrame()
    module._persist_session_cache_snapshot = lambda: (None, None)

    ok, report = module._hydrate_question_pages_from_run("RUN_FAIL")

    assert ok is True
    assert report["failed"] == {}
    assert session_state["last_full_refresh_run_id"] == "RUN_FAIL"
    assert session_state["q3_bundle_result"]["quality_status"] == "FAIL"
    assert int(session_state["q3_bundle_result"]["check_counts"]["FAIL"]) == 1
    assert int(session_state["q3_bundle_result"]["check_counts"]["INFO"]) == 0
    assert session_state["q3_bundle_result"]["fail_codes_top5"] == ["Q3_FAIL"]


def test_load_preferred_run_id_fallbacks_to_latest_valid_run(tmp_path: Path) -> None:
    module = _load_accueil_module()
    base = tmp_path / "outputs" / "combined"
    run_old = _build_fake_run(base, run_id="RUN_OLD")
    run_new = _build_fake_run(base, run_id="RUN_NEW")

    # Force deterministic mtime order if filesystem resolution is coarse.
    run_old.stat()
    (run_old / ".t").write_text("x", encoding="utf-8")
    (run_new / ".t").write_text("x", encoding="utf-8")
    _ = run_old.stat().st_mtime
    new_stamp = run_new.stat().st_mtime
    Path(run_old / ".t").unlink()
    Path(run_new / ".t").unlink()
    os.utime(run_old, (1_650_000_000, 1_650_000_000))
    os.utime(run_new, (new_stamp + 100, new_stamp + 100))

    selected_run_id, fallback = module._load_preferred_run_id(None, base_dir=str(base))

    assert fallback is True
    assert selected_run_id == "RUN_NEW"


def test_hydrate_reports_cache_persistence_status(monkeypatch, tmp_path: Path) -> None:
    module = _load_accueil_module()

    base = tmp_path / "outputs" / "combined"
    _build_fake_run(base, run_id="RUN_CACHE")
    monkeypatch.setattr(module, "_to_abs_project_path", lambda path_like: base)
    session_state: dict[str, object] = {}
    fake_st = SimpleNamespace(
        session_state=session_state,
        cache_data=SimpleNamespace(clear=lambda: None),
        cache_resource=SimpleNamespace(clear=lambda: None),
    )
    module.st = fake_st

    def fake_loader(run_id: str, question_id: str, base_dir: str = "outputs/combined", **kwargs):  # noqa: ARG001
        return _fake_bundle(question_id, run_id, "PASS"), base / run_id / question_id

    module.load_question_bundle_from_combined_run_safe = fake_loader
    module.load_assumptions_table = lambda: pd.DataFrame()
    module.load_phase2_assumptions_table = lambda: pd.DataFrame()
    module._persist_session_cache_snapshot = lambda: ("outputs/session_cache/session_state.json", None)

    ok, report = module._hydrate_question_pages_from_run("RUN_CACHE")
    assert ok is True
    assert report["cache_path"] == "outputs/session_cache/session_state.json"
    assert report["cache_error"] is None


def test_hydrate_aggregates_duplicate_fail_codes(monkeypatch, tmp_path: Path) -> None:
    module = _load_accueil_module()

    base = tmp_path / "outputs" / "combined"
    _build_fake_run(base, run_id="RUN_CODES")
    monkeypatch.setattr(module, "_to_abs_project_path", lambda path_like: base)

    session_state = {}
    fake_st = SimpleNamespace(
        session_state=session_state,
        cache_data=SimpleNamespace(clear=lambda: None),
        cache_resource=SimpleNamespace(clear=lambda: None),
    )
    module.st = fake_st

    def fake_loader(run_id: str, question_id: str, base_dir: str = "outputs/combined", **kwargs):  # noqa: ARG001
        if question_id != "Q1":
            return _fake_bundle(question_id, run_id, "PASS"), base / run_id / question_id
        checks = (
            [{"status": "FAIL", "code": "RC_IR_GT_1", "message": "", "scope": "HIST", "scenario_id": ""}] * 5
            + [{"status": "FAIL", "code": "RC_FAR_RANGE", "message": "", "scope": "HIST", "scenario_id": ""}] * 2
        )
        return _fake_bundle_with_checks(question_id, run_id, checks), base / run_id / question_id

    module.load_question_bundle_from_combined_run_safe = fake_loader
    module.load_assumptions_table = lambda: pd.DataFrame()
    module.load_phase2_assumptions_table = lambda: pd.DataFrame()
    module._persist_session_cache_snapshot = lambda: (None, None)

    ok, _ = module._hydrate_question_pages_from_run("RUN_CODES")
    assert ok is True
    assert session_state["q1_bundle_result"]["fail_codes_top5"] == ["RC_IR_GT_1 (x5)", "RC_FAR_RANGE (x2)"]


def test_build_auto_audit_bundle_after_refresh_uses_bundle_hashes(monkeypatch) -> None:
    module = _load_accueil_module()
    captured: dict[str, object] = {}

    fake_audit_module = ModuleType("src.reporting.auto_audit_bundle")

    def fake_build_auto_audit_bundle(**kwargs):  # type: ignore[no-untyped-def]
        captured.update(kwargs)
        return {
            "audit_dir": "outputs/audit_runs/RUN_AUDIT",
            "detailed_markdown_path": "outputs/audit_runs/RUN_AUDIT/reports/detailed_es_de_RUN_AUDIT.md",
            "warnings": [],
        }

    fake_audit_module.build_auto_audit_bundle = fake_build_auto_audit_bundle  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "src.reporting.auto_audit_bundle", fake_audit_module)

    module.st = SimpleNamespace(
        session_state={
            "q1_bundle_result": {"bundle_hash": "Q1_HASH"},
            "q2_bundle_result": {"bundle_hash": "Q2_HASH"},
        }
    )

    ok, report = module._build_auto_audit_bundle_after_refresh("RUN_AUDIT")
    assert ok is True
    assert report["audit_dir"] == "outputs/audit_runs/RUN_AUDIT"
    assert captured["run_id"] == "RUN_AUDIT"
    assert captured["countries"] == ["ES", "DE"]
    assert captured["include_llm_reports"] is True
    assert captured["keep_last"] == 5
    assert captured["bundle_hash_by_question"] == {"Q1": "Q1_HASH", "Q2": "Q2_HASH"}


def test_build_auto_audit_bundle_after_refresh_non_blocking_on_error(monkeypatch) -> None:
    module = _load_accueil_module()

    fake_audit_module = ModuleType("src.reporting.auto_audit_bundle")

    def fake_build_auto_audit_bundle(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        raise RuntimeError("boom-audit")

    fake_audit_module.build_auto_audit_bundle = fake_build_auto_audit_bundle  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "src.reporting.auto_audit_bundle", fake_audit_module)

    module.st = SimpleNamespace(session_state={})
    ok, report = module._build_auto_audit_bundle_after_refresh("RUN_ERR")
    assert ok is False
    assert "boom-audit" in str(report.get("error", ""))
