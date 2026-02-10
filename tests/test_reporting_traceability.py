from __future__ import annotations

from pathlib import Path

import pandas as pd

from generate_report import generate_report
from src.reporting.evidence_loader import load_combined_run
from tests._reporting_utils import build_fake_combined_run, build_fake_docx


def test_detailed_report_contains_all_test_ids_and_source_refs(tmp_path: Path, monkeypatch) -> None:
    combined = tmp_path / "outputs" / "combined"
    reports = tmp_path / "reports"
    build_fake_combined_run(combined, run_id="RUN_TRACE", include_all_questions=True)
    monkeypatch.chdir(tmp_path)

    docx = build_fake_docx(tmp_path / "slides.docx", [(2, "Q1 requirement"), (8, "Q2 requirement"), (14, "Q3 requirement"), (20, "Q4 requirement"), (26, "Q5 requirement")])
    result = generate_report(
        run_id="RUN_TRACE",
        strict=False,
        country_scope=["FR"],
        docx_paths=[docx],
        output_dir=reports,
    )

    text = result.detailed_report_path.read_text(encoding="utf-8")
    _, _, blocks = load_combined_run(run_id="RUN_TRACE", base_dir=combined, strict=True)

    all_test_ids: list[str] = []
    all_source_refs: list[str] = []
    for block in blocks.values():
        all_test_ids.extend(block.ledger["test_id"].astype(str).tolist())
        all_source_refs.extend(block.ledger["source_ref"].astype(str).tolist())

    for tid in all_test_ids:
        assert tid in text
    for src in all_source_refs:
        assert src in text
