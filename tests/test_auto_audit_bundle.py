from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.reporting.auto_audit_bundle import build_auto_audit_bundle
from tests._reporting_utils import build_fake_combined_run


def _ensure_strict_run_layout(run_dir: Path) -> None:
    for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        q_dir = run_dir / qid
        summary_path = q_dir / "summary.json"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        run_id = str(summary.get("run_id", run_dir.name))

        hist_dir = q_dir / "hist"
        hist_dir.mkdir(parents=True, exist_ok=True)
        (hist_dir / "summary.json").write_text(
            json.dumps(
                {
                    "module_id": qid,
                    "run_id": run_id,
                    "selection": {"countries": ["FR"]},
                    "checks": [{"status": "PASS", "code": f"{qid}_H_PASS", "message": "ok"}],
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
                    "checks": [{"status": "PASS", "code": f"{qid}_S_PASS", "message": "ok"}],
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


def test_build_auto_audit_bundle_generates_expected_artifacts(tmp_path: Path, monkeypatch) -> None:
    run_id = "RUN_AUTO_01"
    base_combined = tmp_path / "outputs" / "combined"
    run_dir = build_fake_combined_run(base_combined, run_id=run_id, include_all_questions=True)
    _ensure_strict_run_layout(run_dir)

    q1_summary_path = run_dir / "Q1" / "summary.json"
    q1_summary = json.loads(q1_summary_path.read_text(encoding="utf-8"))
    q1_summary["checks"] = [
        {"status": "FAIL", "code": "RC_IR_GT_1", "message": "IR > 1", "scope": "HIST", "scenario_id": ""}
    ]
    q1_summary_path.write_text(json.dumps(q1_summary, ensure_ascii=False), encoding="utf-8")

    llm_src = tmp_path / "outputs" / "llm_reports"
    llm_src.mkdir(parents=True, exist_ok=True)
    (llm_src / "Q1_HASHQ1.json").write_text('{"status":"OK"}', encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    result = build_auto_audit_bundle(
        run_id=run_id,
        countries=["ES", "DE"],
        include_llm_reports=True,
        bundle_hash_by_question={"Q1": "HASHQ1"},
        keep_last=5,
        combined_base_dir=Path("outputs/combined"),
        audit_root_dir=Path("outputs/audit_runs"),
    )

    audit_dir = Path(result["audit_dir"])
    assert audit_dir.exists()
    assert (audit_dir / "manifest.json").exists()
    assert (audit_dir / "combined_run" / "Q1" / "summary.json").exists()
    assert (audit_dir / "reports" / f"evidence_catalog_{run_id}.csv").exists()
    assert (audit_dir / "reports" / f"test_traceability_{run_id}.csv").exists()
    assert (audit_dir / "reports" / f"checks_catalog_{run_id}.csv").exists()
    assert (audit_dir / "reports" / f"question_status_summary_{run_id}.csv").exists()
    assert (audit_dir / "reports" / f"question_fail_matrix_{run_id}.csv").exists()
    assert (audit_dir / "reports" / f"detailed_es_de_{run_id}.md").exists()
    assert (audit_dir / "llm_reports" / "Q1_HASHQ1.json").exists()

    fail_matrix = pd.read_csv(audit_dir / "reports" / f"question_fail_matrix_{run_id}.csv")
    assert "RC_IR_GT_1" in fail_matrix.get("code", pd.Series(dtype=str)).astype(str).tolist()


def test_build_auto_audit_bundle_applies_retention(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    base_combined = Path("outputs/combined")
    audit_root = Path("outputs/audit_runs")

    for idx in range(1, 5):
        run_id = f"RUN_KEEP_{idx}"
        run_dir = build_fake_combined_run(base_combined, run_id=run_id, include_all_questions=True)
        _ensure_strict_run_layout(run_dir)
        _ = build_auto_audit_bundle(
            run_id=run_id,
            countries=["ES", "DE"],
            include_llm_reports=False,
            bundle_hash_by_question={},
            keep_last=2,
            combined_base_dir=base_combined,
            audit_root_dir=audit_root,
        )

    kept = sorted([p.name for p in audit_root.iterdir() if p.is_dir()])
    assert len(kept) == 2
    assert "RUN_KEEP_3" in kept
    assert "RUN_KEEP_4" in kept
