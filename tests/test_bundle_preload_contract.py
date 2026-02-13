from __future__ import annotations

from pathlib import Path
import json

import pandas as pd
import pytest

import app.page_utils as page_utils
from src.reporting.evidence_loader import (
    compute_question_bundle_signature,
    load_question_bundle_from_combined_run_verified,
    validate_combined_run,
)


def _write_module_summary(path: Path, run_id: str, module_id: str) -> None:
    summary = {
        "module_id": module_id,
        "run_id": run_id,
        "selection": {"countries": ["FR"]},
        "checks": [{"status": "PASS", "code": "OK", "message": "ok", "scope": "HIST", "scenario_id": ""}],
        "assumptions_used": [],
        "kpis": {},
        "warnings": [],
        "mode": "HIST",
    }
    path.write_text(json.dumps(summary, ensure_ascii=False), encoding="utf-8")


def _build_test_run(root: Path, run_id: str, include_all_questions: bool = True) -> Path:
    qs = ["Q1", "Q2", "Q3", "Q4", "Q5"] if include_all_questions else ["Q1", "Q2", "Q3"]
    run_dir = root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    for qid in qs:
        q_dir = run_dir / qid
        q_dir.mkdir(parents=True, exist_ok=True)

        q_summary = {
            "question_id": qid,
            "run_id": run_id,
            "selection": {"countries": ["FR"]},
            "checks": [{"status": "PASS", "code": f"{qid}_PASS", "message": "ok", "scope": "HIST", "scenario_id": ""}],
            "warnings": [],
            "scenarios": ["BASE"],
        }
        (q_dir / "summary.json").write_text(json.dumps(q_summary, ensure_ascii=False), encoding="utf-8")

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
        _write_module_summary(hist_dir / "summary.json", run_id, module_id=qid)

        scen_dir = q_dir / "scen" / "BASE"
        scen_dir.mkdir(parents=True, exist_ok=True)
        (scen_dir / "summary.json").write_text(json.dumps({
            "module_id": qid,
            "run_id": run_id,
            "selection": {"countries": ["FR"]},
            "checks": [{"status": "PASS", "code": f"{qid}_SCEN_PASS", "message": "ok", "scope": "SCEN", "scenario_id": "BASE"}],
            "assumptions_used": [],
            "kpis": {},
            "warnings": [],
            "mode": "SCEN",
            "scenario_id": "BASE",
            "horizon_year": 2035,
        }, ensure_ascii=False), encoding="utf-8")
        (q_dir / "narrative.md").write_text(f"Narrative {qid}", encoding="utf-8")

    return run_dir


def _build_test_run_with_missing_summary(root: Path, run_id: str, missing_question: str) -> Path:
    run_dir = _build_test_run(root, run_id)
    q_dir = run_dir / missing_question
    (q_dir / "summary.json").unlink()
    return run_dir


def test_load_question_bundle_from_combined_run_falls_back_to_local_when_verified_loader_absent(monkeypatch, tmp_path: Path) -> None:
    base = tmp_path / "outputs" / "combined"
    _build_test_run(base, run_id="RUN_LOCAL_FALLBACK")

    monkeypatch.setattr(page_utils, "_load_question_bundle_from_combined_run_verified", None)
    bundle, q_dir = page_utils.load_question_bundle_from_combined_run(
        run_id="RUN_LOCAL_FALLBACK",
        question_id="Q1",
        base_dir=str(base),
    )

    assert bundle.question_id == "Q1"
    assert q_dir == base / "RUN_LOCAL_FALLBACK" / "Q1"
    assert bundle.run_id == "RUN_LOCAL_FALLBACK"


def test_validate_combined_run_rejects_missing_summary(tmp_path: Path) -> None:
    base = tmp_path / "outputs" / "combined"
    run_dir = _build_test_run_with_missing_summary(base, run_id="RUN_MISSING_SUMMARY", missing_question="Q2")

    valid, errors = validate_combined_run(run_dir)
    assert valid is False
    assert any("summary.json manquant pour Q2" in error for error in errors)


def test_load_question_bundle_from_combined_run_verified_requires_complete_run(tmp_path: Path) -> None:
    base = tmp_path / "outputs" / "combined"
    run_dir = _build_test_run(base, run_id="RUN_INCOMPLETE", include_all_questions=True)
    # remove a required file to make the run invalid
    (run_dir / "Q1" / "comparison_hist_vs_scen.csv").unlink()

    with pytest.raises(ValueError, match="Run combine incomplet ou invalide"):
        load_question_bundle_from_combined_run_verified(run_id="RUN_INCOMPLETE", question_id="Q1", base_dir=str(base))


def test_load_question_bundle_from_combined_run_verified_success(tmp_path: Path) -> None:
    base = tmp_path / "outputs" / "combined"
    _build_test_run(base, run_id="RUN_OK", include_all_questions=True)

    for question_id in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        bundle, q_dir = load_question_bundle_from_combined_run_verified(
            run_id="RUN_OK",
            question_id=question_id,
            base_dir=str(base),
        )
        assert bundle.question_id == question_id
        assert bundle.run_id == "RUN_OK"
        assert q_dir == base / "RUN_OK" / question_id
        assert isinstance(bundle.test_ledger, pd.DataFrame)


def test_load_question_bundle_from_combined_run_safe_allows_fail_checks_by_default(monkeypatch, tmp_path: Path) -> None:
    base = tmp_path / "outputs" / "combined"
    run_dir = _build_test_run(base, run_id="RUN_FAIL_ALLOWED", include_all_questions=True)
    q1_summary = json.loads((run_dir / "Q1" / "summary.json").read_text(encoding="utf-8"))
    q1_summary["checks"] = [{"status": "FAIL", "code": "Q1_FAIL", "message": "boom", "scope": "HIST", "scenario_id": ""}]
    (run_dir / "Q1" / "summary.json").write_text(json.dumps(q1_summary, ensure_ascii=False), encoding="utf-8")

    monkeypatch.setattr(page_utils, "_load_question_bundle_from_combined_run_verified", None)
    bundle, _ = page_utils.load_question_bundle_from_combined_run_safe(
        run_id="RUN_FAIL_ALLOWED",
        question_id="Q1",
        base_dir=str(base),
        allow_fail_checks=True,
    )
    assert bundle.question_id == "Q1"
    assert any(str(check.get("status", "")).upper() == "FAIL" for check in bundle.checks)


def test_load_question_bundle_from_combined_run_safe_rejects_fail_when_disallowed(monkeypatch, tmp_path: Path) -> None:
    base = tmp_path / "outputs" / "combined"
    run_dir = _build_test_run(base, run_id="RUN_FAIL_BLOCKED", include_all_questions=True)
    q1_summary = json.loads((run_dir / "Q1" / "summary.json").read_text(encoding="utf-8"))
    q1_summary["checks"] = [{"status": "FAIL", "code": "Q1_FAIL", "message": "boom", "scope": "HIST", "scenario_id": ""}]
    (run_dir / "Q1" / "summary.json").write_text(json.dumps(q1_summary, ensure_ascii=False), encoding="utf-8")

    monkeypatch.setattr(page_utils, "_load_question_bundle_from_combined_run_verified", None)
    with pytest.raises(ValueError, match="Checks FAIL detectes"):
        page_utils.load_question_bundle_from_combined_run_safe(
            run_id="RUN_FAIL_BLOCKED",
            question_id="Q1",
            base_dir=str(base),
            allow_fail_checks=False,
        )


def test_load_question_bundle_from_combined_run_safe_rejects_signature_mismatch(monkeypatch, tmp_path: Path) -> None:
    base = tmp_path / "outputs" / "combined"
    _build_test_run(base, run_id="RUN_SIGNATURE", include_all_questions=True)
    monkeypatch.setattr(page_utils, "_load_question_bundle_from_combined_run_verified", None)

    run_dir = base / "RUN_SIGNATURE"
    expected_signature = compute_question_bundle_signature(run_dir, "Q1")
    wrong_signature = expected_signature + "_WRONG"
    with pytest.raises(ValueError, match="Signature incompatible"):
        page_utils.load_question_bundle_from_combined_run_safe(
            run_id="RUN_SIGNATURE",
            question_id="Q1",
            base_dir=str(base),
            expected_signature=wrong_signature,
        )
