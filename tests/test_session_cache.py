from __future__ import annotations

from pathlib import Path
import json

import pandas as pd

from src.reporting.evidence_loader import compute_question_bundle_signature
from src.reporting.session_cache import (
    SESSION_CACHE_SCHEMA_VERSION,
    build_question_snapshot_entry,
    clear_session_snapshot,
    load_session_snapshot,
    save_session_snapshot,
    validate_session_snapshot,
)


def _build_run(root: Path, run_id: str) -> Path:
    run_dir = root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        q_dir = run_dir / qid
        q_dir.mkdir(parents=True, exist_ok=True)
        (q_dir / "summary.json").write_text(
            json.dumps(
                {
                    "question_id": qid,
                    "run_id": run_id,
                    "selection": {"countries": ["FR"]},
                    "checks": [{"status": "PASS", "code": f"{qid}_PASS", "message": "ok", "scope": "HIST", "scenario_id": ""}],
                    "warnings": [],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        pd.DataFrame([{"test_id": f"{qid}-H-01", "status": "PASS"}]).to_csv(q_dir / "test_ledger.csv", index=False)
        pd.DataFrame([{"country": "FR", "metric": "x", "hist_value": 1.0, "scen_value": 1.0, "delta": 0.0}]).to_csv(
            q_dir / "comparison_hist_vs_scen.csv",
            index=False,
        )
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
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
    return run_dir


def test_session_cache_save_load_clear(tmp_path: Path) -> None:
    cache_file = tmp_path / "session_state.json"
    snapshot = {"active_run_id": "RUN_X", "questions": {"Q1": {"question_id": "Q1"}}}
    save_session_snapshot(snapshot, cache_file=cache_file)
    loaded = load_session_snapshot(cache_file=cache_file)
    assert isinstance(loaded, dict)
    assert loaded.get("schema_version") == SESSION_CACHE_SCHEMA_VERSION
    assert loaded.get("active_run_id") == "RUN_X"

    clear_session_snapshot(cache_file=cache_file)
    assert load_session_snapshot(cache_file=cache_file) is None


def test_validate_session_snapshot_success(tmp_path: Path) -> None:
    combined_base = tmp_path / "outputs" / "combined"
    run_dir = _build_run(combined_base, "RUN_OK")
    questions: dict[str, dict[str, object]] = {}
    for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        signature = compute_question_bundle_signature(run_dir, qid)
        questions[qid] = build_question_snapshot_entry(
            question_id=qid,
            result_key=f"{qid.lower()}_bundle_result",
            run_id="RUN_OK",
            out_dir=str(run_dir / qid),
            bundle_hash=f"RUN_OK_{qid}",
            signature=signature,
            quality_status="PASS",
            check_counts={"PASS": 1, "WARN": 0, "FAIL": 0, "NON_TESTABLE": 0, "UNKNOWN": 0},
            fail_codes_top5=[],
        )
    snapshot = {
        "schema_version": SESSION_CACHE_SCHEMA_VERSION,
        "active_run_id": "RUN_OK",
        "run_dir_mtime_ns": int(run_dir.stat().st_mtime_ns),
        "questions": questions,
        "last_llm_batch_result": {"generated_at_utc": "2026-02-13T00:00:00+00:00", "rows": []},
    }
    valid, errors = validate_session_snapshot(snapshot, combined_base)
    assert valid is True
    assert errors == []


def test_validate_session_snapshot_fails_when_run_missing(tmp_path: Path) -> None:
    combined_base = tmp_path / "outputs" / "combined"
    combined_base.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "schema_version": SESSION_CACHE_SCHEMA_VERSION,
        "active_run_id": "RUN_MISSING",
        "questions": {"Q1": {"run_id": "RUN_MISSING", "signature": "X"}},
    }
    valid, errors = validate_session_snapshot(snapshot, combined_base)
    assert valid is False
    assert errors


def test_validate_session_snapshot_fails_on_signature_mismatch(tmp_path: Path) -> None:
    combined_base = tmp_path / "outputs" / "combined"
    run_dir = _build_run(combined_base, "RUN_SIG")
    questions: dict[str, dict[str, object]] = {}
    for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        signature = "WRONG_SIGNATURE" if qid == "Q3" else compute_question_bundle_signature(run_dir, qid)
        questions[qid] = build_question_snapshot_entry(
            question_id=qid,
            result_key=f"{qid.lower()}_bundle_result",
            run_id="RUN_SIG",
            out_dir=str(run_dir / qid),
            bundle_hash=f"RUN_SIG_{qid}",
            signature=signature,
            quality_status="PASS",
            check_counts={"PASS": 1, "WARN": 0, "FAIL": 0, "NON_TESTABLE": 0, "UNKNOWN": 0},
            fail_codes_top5=[],
        )
    snapshot = {
        "schema_version": SESSION_CACHE_SCHEMA_VERSION,
        "active_run_id": "RUN_SIG",
        "run_dir_mtime_ns": int(run_dir.stat().st_mtime_ns),
        "questions": questions,
    }
    valid, errors = validate_session_snapshot(snapshot, combined_base)
    assert valid is False
    assert any("signature incoherente pour Q3" in err for err in errors)


def test_validate_session_snapshot_rejects_old_schema(tmp_path: Path) -> None:
    combined_base = tmp_path / "outputs" / "combined"
    combined_base.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "schema_version": 0,
        "active_run_id": "RUN_OLD_SCHEMA",
        "questions": {},
    }
    valid, errors = validate_session_snapshot(snapshot, combined_base)
    assert valid is False
    assert any("Schema snapshot incompatible" in err for err in errors)
