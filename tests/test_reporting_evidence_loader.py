from __future__ import annotations

from pathlib import Path

from src.reporting.evidence_loader import build_evidence_catalog, load_combined_run, resolve_run_dir
from tests._reporting_utils import build_fake_combined_run


def test_load_combined_run_single_coherent_run(tmp_path: Path) -> None:
    base = tmp_path / "outputs" / "combined"
    run_dir = build_fake_combined_run(base, run_id="RUN_OK", include_all_questions=True)

    run_id, resolved_dir, blocks = load_combined_run(run_id="RUN_OK", base_dir=base, strict=True)

    assert run_id == "RUN_OK"
    assert resolved_dir == run_dir
    assert set(blocks.keys()) == {"Q1", "Q2", "Q3", "Q4", "Q5"}


def test_resolve_run_dir_rejects_incomplete_run_in_strict(tmp_path: Path) -> None:
    base = tmp_path / "outputs" / "combined"
    build_fake_combined_run(base, run_id="RUN_PARTIAL", include_all_questions=False)

    try:
        resolve_run_dir(run_id="RUN_PARTIAL", base_dir=base, strict=True)
        assert False, "Expected ValueError for incomplete strict run"
    except ValueError:
        pass


def test_build_evidence_catalog_not_empty(tmp_path: Path) -> None:
    base = tmp_path / "outputs" / "combined"
    run_dir = build_fake_combined_run(base, run_id="RUN_EVID", include_all_questions=True)
    _, _, blocks = load_combined_run(run_id="RUN_EVID", base_dir=base, strict=True)
    evidence = build_evidence_catalog(run_dir, blocks)

    assert not evidence.empty
    assert {"question_id", "test_id", "source_ref", "evidence_ref"}.issubset(evidence.columns)

