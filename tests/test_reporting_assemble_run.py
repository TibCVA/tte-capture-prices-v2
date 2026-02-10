from __future__ import annotations

from pathlib import Path

from src.reporting.evidence_loader import (
    assemble_complete_run_from_fragments,
    can_assemble_complete_run,
    discover_complete_runs,
    latest_fragment_per_question,
)
from tests._reporting_utils import build_fake_combined_run


def test_assemble_complete_run_from_latest_fragments(tmp_path: Path) -> None:
    base = tmp_path / "outputs" / "combined"
    # Create per-question fragments in separate runs.
    for q in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        run_dir = build_fake_combined_run(base, run_id=f"RUN_{q}", include_all_questions=True)
        # Keep only one question folder to emulate fragmented exports.
        for other in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
            if other != q:
                other_dir = run_dir / other
                if other_dir.exists():
                    for p in other_dir.rglob("*"):
                        pass
                    import shutil

                    shutil.rmtree(other_dir)

    assert can_assemble_complete_run(base) is True
    latest = latest_fragment_per_question(base)
    assert set(latest.keys()) == {"Q1", "Q2", "Q3", "Q4", "Q5"}

    run_dir = assemble_complete_run_from_fragments(base, run_id="ASSEMBLED_TEST")
    assert run_dir.exists()
    assert (run_dir / "_assembled_from.json").exists()
    for q in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        assert (run_dir / q / "summary.json").exists()

    complete = discover_complete_runs(base)
    assert any(p.name == "ASSEMBLED_TEST" for p in complete)

