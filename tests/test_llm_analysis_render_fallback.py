from __future__ import annotations

import json
from pathlib import Path

from app import llm_analysis


def _write_report(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_load_report_with_fallback_returns_latest_valid_when_exact_missing(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(llm_analysis, "LLM_REPORTS_DIR", tmp_path)
    _write_report(
        tmp_path / "Q1_HASH_OLD.json",
        {
            "question_id": "Q1",
            "bundle_hash": "HASH_OLD",
            "generated_at": "2026-01-01T00:00:00+00:00",
            "report_md": "ancien rapport",
        },
    )
    # Invalid newer payload should be ignored.
    _write_report(
        tmp_path / "Q1_HASH_BAD.json",
        {
            "question_id": "Q1",
            "bundle_hash": "HASH_BAD",
            "generated_at": "2026-01-02T00:00:00+00:00",
            "error": "failed",
        },
    )

    report, is_fallback = llm_analysis.load_report_with_fallback("Q1", "HASH_NEW")
    assert is_fallback is True
    assert report is not None
    assert report["bundle_hash"] == "HASH_OLD"


def test_load_report_with_fallback_prefers_exact_bundle_report(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(llm_analysis, "LLM_REPORTS_DIR", tmp_path)
    _write_report(
        tmp_path / "Q2_HASH_OLD.json",
        {
            "question_id": "Q2",
            "bundle_hash": "HASH_OLD",
            "generated_at": "2026-01-01T00:00:00+00:00",
            "report_md": "old",
        },
    )
    _write_report(
        tmp_path / "Q2_HASH_NEW.json",
        {
            "question_id": "Q2",
            "bundle_hash": "HASH_NEW",
            "generated_at": "2026-01-03T00:00:00+00:00",
            "report_md": "new",
        },
    )

    report, is_fallback = llm_analysis.load_report_with_fallback("Q2", "HASH_NEW")
    assert is_fallback is False
    assert report is not None
    assert report["bundle_hash"] == "HASH_NEW"
