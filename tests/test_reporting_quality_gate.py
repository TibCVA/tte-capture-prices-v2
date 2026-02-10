from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.reporting.interpretation_rules import narrative_quality_checks, min_words_for_question
from src.reporting.report_schema import QuestionNarrativeBlock, QuestionTestResultBlock


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
