"""Load and normalize reporting evidence from combined runs."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json

import pandas as pd

from src.reporting.report_schema import QuestionTestResultBlock

REQUIRED_QUESTIONS: tuple[str, ...] = ("Q1", "Q2", "Q3", "Q4", "Q5")


def _safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def _safe_read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def question_dir(run_dir: Path, question_id: str) -> Path:
    return run_dir / str(question_id).upper()


def is_complete_run(run_dir: Path) -> bool:
    if not run_dir.exists() or not run_dir.is_dir():
        return False
    for q in REQUIRED_QUESTIONS:
        q_dir = question_dir(run_dir, q)
        if not q_dir.exists():
            return False
        if not (q_dir / "summary.json").exists():
            return False
        if not (q_dir / "test_ledger.csv").exists():
            return False
        if not (q_dir / "comparison_hist_vs_scen.csv").exists():
            return False
    return True


def discover_complete_runs(base_dir: Path = Path("outputs/combined")) -> list[Path]:
    if not base_dir.exists():
        return []
    runs = [p for p in base_dir.iterdir() if p.is_dir() and is_complete_run(p)]
    return sorted(runs, key=lambda p: p.stat().st_mtime, reverse=True)


def resolve_run_dir(
    run_id: str | None = None,
    base_dir: Path = Path("outputs/combined"),
    strict: bool = True,
) -> Path:
    if run_id:
        run_dir = base_dir / run_id
        if not run_dir.exists():
            raise FileNotFoundError(f"Combined run not found: {run_dir}")
        if strict and not is_complete_run(run_dir):
            raise ValueError(f"Combined run is incomplete (Q1..Q5 required): {run_dir}")
        return run_dir

    candidates = discover_complete_runs(base_dir=base_dir)
    if candidates:
        return candidates[0]
    if strict:
        raise ValueError("No complete combined run found (requires Q1..Q5).")

    runs = [p for p in base_dir.iterdir() if p.is_dir()] if base_dir.exists() else []
    if not runs:
        raise ValueError("No combined run found.")
    return sorted(runs, key=lambda p: p.stat().st_mtime, reverse=True)[0]


def load_question_block(run_dir: Path, question_id: str) -> QuestionTestResultBlock:
    qid = str(question_id).upper()
    q_dir = question_dir(run_dir, qid)
    summary_path = q_dir / "summary.json"
    ledger_path = q_dir / "test_ledger.csv"
    comparison_path = q_dir / "comparison_hist_vs_scen.csv"
    summary = _safe_read_json(summary_path)
    ledger = _safe_read_csv(ledger_path)
    comparison = _safe_read_csv(comparison_path)

    checks = pd.DataFrame(summary.get("checks", []))
    warnings = [str(w) for w in summary.get("warnings", [])]

    return QuestionTestResultBlock(
        question_id=qid,
        summary=summary,
        ledger=ledger,
        comparison=comparison,
        checks=checks,
        warnings=warnings,
        files={
            "summary": summary_path,
            "ledger": ledger_path,
            "comparison": comparison_path,
            "narrative": q_dir / "narrative.md",
        },
    )


def load_combined_run(
    run_id: str | None = None,
    base_dir: Path = Path("outputs/combined"),
    strict: bool = True,
) -> tuple[str, Path, dict[str, QuestionTestResultBlock]]:
    run_dir = resolve_run_dir(run_id=run_id, base_dir=base_dir, strict=strict)
    resolved_run_id = run_dir.name

    blocks: dict[str, QuestionTestResultBlock] = {}
    questions = REQUIRED_QUESTIONS if strict else tuple(sorted([p.name for p in run_dir.iterdir() if p.is_dir()]))
    for qid in questions:
        q_dir = question_dir(run_dir, qid)
        if not q_dir.exists():
            if strict:
                raise ValueError(f"Missing question directory: {qid} in {run_dir}")
            continue
        blocks[qid] = load_question_block(run_dir, qid)

    if strict and set(blocks.keys()) != set(REQUIRED_QUESTIONS):
        missing = sorted(set(REQUIRED_QUESTIONS) - set(blocks.keys()))
        raise ValueError(f"Incomplete run. Missing questions: {missing}")

    return resolved_run_id, run_dir, blocks


def build_evidence_catalog(run_dir: Path, blocks: dict[str, QuestionTestResultBlock]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for qid, block in blocks.items():
        if block.ledger.empty:
            continue
        for _, row in block.ledger.iterrows():
            rows.append(
                {
                    "run_id": run_dir.name,
                    "question_id": qid,
                    "test_id": str(row.get("test_id", "")),
                    "source_ref": str(row.get("source_ref", "")),
                    "mode": str(row.get("mode", "")),
                    "scenario_id": str(row.get("scenario_id", "")),
                    "status": str(row.get("status", "")),
                    "value": str(row.get("value", "")),
                    "threshold": str(row.get("threshold", "")),
                    "interpretation": str(row.get("interpretation", "")),
                    "evidence_ref": f"{block.files.get('ledger', Path())}#test_id={row.get('test_id', '')}",
                }
            )
    return pd.DataFrame(rows)


def build_test_traceability(run_dir: Path, blocks: dict[str, QuestionTestResultBlock]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for qid, block in blocks.items():
        if block.ledger.empty:
            continue
        for _, row in block.ledger.iterrows():
            rows.append(
                {
                    "run_id": run_dir.name,
                    "question_id": qid,
                    "test_id": str(row.get("test_id", "")),
                    "source_ref": str(row.get("source_ref", "")),
                    "mode": str(row.get("mode", "")),
                    "scenario_id": str(row.get("scenario_id", "")),
                    "status": str(row.get("status", "")),
                    "evidence_ref": f"{block.files.get('ledger', Path())}",
                }
            )
    return pd.DataFrame(rows)


def build_checks_catalog(run_dir: Path, blocks: dict[str, QuestionTestResultBlock]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for qid, block in blocks.items():
        if block.checks.empty:
            continue
        for _, row in block.checks.iterrows():
            rows.append(
                {
                    "run_id": run_dir.name,
                    "question_id": qid,
                    "status": str(row.get("status", "")),
                    "code": str(row.get("code", "")),
                    "message": str(row.get("message", "")),
                    "scope": str(row.get("scope", "")),
                    "scenario_id": str(row.get("scenario_id", "")),
                    "evidence_ref": f"{block.files.get('summary', Path())}",
                }
            )
    return pd.DataFrame(rows)

