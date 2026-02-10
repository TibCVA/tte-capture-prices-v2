from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from generate_report import generate_report
from src.reporting.interpretation_rules import narrative_quality_checks, min_words_for_question
from src.reporting.report_schema import QuestionNarrativeBlock, QuestionTestResultBlock
from tests._reporting_utils import build_fake_combined_run


def _block_with_test(test_id: str = "Q1-H-01") -> QuestionTestResultBlock:
    ledger = pd.DataFrame(
        [
            {
                "test_id": test_id,
                "mode": "HIST",
                "source_ref": "Slides 2",
                "status": "PASS",
                "value": "1",
                "threshold": ">=0",
                "interpretation": "ok",
            }
        ]
    )
    return QuestionTestResultBlock(
        question_id="Q1",
        summary={},
        ledger=ledger,
        comparison=pd.DataFrame(),
        checks=pd.DataFrame(),
        warnings=[],
        files={},
    )


def test_quality_gate_fails_when_word_count_too_low() -> None:
    block = _block_with_test()
    narrative = QuestionNarrativeBlock(
        question_id="Q1",
        title="Q1",
        markdown="Texte court avec [evidence:Q1-H-01].",
        word_count=6,
        referenced_test_ids=["Q1-H-01"],
    )
    qc = narrative_quality_checks(narrative, block)
    assert qc["word_count_ok"] is False
    assert qc["word_count"] < min_words_for_question("Q1")


def test_quality_gate_fails_when_test_id_not_referenced() -> None:
    block = _block_with_test("Q1-H-99")
    narrative = QuestionNarrativeBlock(
        question_id="Q1",
        title="Q1",
        markdown=" ".join(["mot"] * 1300),  # above threshold
        word_count=1300,
        referenced_test_ids=[],
    )
    qc = narrative_quality_checks(narrative, block)
    assert qc["all_test_ids_referenced"] is False
    assert "Q1-H-99" in qc["missing_test_ids_in_text"]


def test_generate_report_marks_non_complet_when_slides_extraction_is_empty(tmp_path: Path, monkeypatch) -> None:
    combined = tmp_path / "outputs" / "combined"
    reports = tmp_path / "reports"
    build_fake_combined_run(combined, run_id="RUN_EMPTY_SLIDES", include_all_questions=True)
    monkeypatch.chdir(tmp_path)

    empty_docx = tmp_path / "slides_empty.docx"
    import zipfile

    xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body><w:p><w:r><w:t>Document sans marqueur de slide</w:t></w:r></w:p></w:body></w:document>"
    )
    with zipfile.ZipFile(empty_docx, "w") as zf:
        zf.writestr("word/document.xml", xml)

    result = generate_report(
        run_id="RUN_EMPTY_SLIDES",
        strict=False,
        country_scope=["FR"],
        docx_paths=[empty_docx],
        output_dir=reports,
    )
    assert result.qc["verdict"] == "NON_COMPLET"
    assert result.qc["slides_docx_existing_count"] == 1
    assert result.qc["slides_requirements_count"] == 0
    assert result.qc["slides_extraction_empty_with_docs"] is True


def test_generate_report_strict_fails_when_slides_extraction_is_empty(tmp_path: Path, monkeypatch) -> None:
    combined = tmp_path / "outputs" / "combined"
    reports = tmp_path / "reports"
    build_fake_combined_run(combined, run_id="RUN_EMPTY_SLIDES_STRICT", include_all_questions=True)
    monkeypatch.chdir(tmp_path)

    empty_docx = tmp_path / "slides_empty_strict.docx"
    import zipfile

    xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body><w:p><w:r><w:t>No slide markers here</w:t></w:r></w:p></w:body></w:document>"
    )
    with zipfile.ZipFile(empty_docx, "w") as zf:
        zf.writestr("word/document.xml", xml)

    with pytest.raises(RuntimeError):
        generate_report(
            run_id="RUN_EMPTY_SLIDES_STRICT",
            strict=True,
            country_scope=["FR"],
            docx_paths=[empty_docx],
            output_dir=reports,
        )
