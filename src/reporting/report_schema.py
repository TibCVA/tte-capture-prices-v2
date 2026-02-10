"""Data contracts for reporting artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class EvidenceRecord:
    question_id: str
    test_id: str
    source_ref: str
    mode: str
    scenario_id: str
    status: str
    value: str
    threshold: str
    interpretation: str
    evidence_ref: str


@dataclass
class QuestionTestResultBlock:
    question_id: str
    summary: dict[str, Any]
    ledger: pd.DataFrame
    comparison: pd.DataFrame
    checks: pd.DataFrame
    warnings: list[str] = field(default_factory=list)
    files: dict[str, Path] = field(default_factory=dict)


@dataclass
class QuestionNarrativeBlock:
    question_id: str
    title: str
    markdown: str
    word_count: int
    referenced_test_ids: list[str] = field(default_factory=list)


@dataclass
class ReportBuildResult:
    run_id: str
    detailed_report_path: Path
    executive_report_path: Path
    evidence_catalog_path: Path
    test_traceability_path: Path
    slides_traceability_path: Path
    qc_path: Path
    qc: dict[str, Any]
