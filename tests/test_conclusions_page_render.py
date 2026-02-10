from __future__ import annotations

from pathlib import Path
import runpy

from src.reporting.evidence_loader import discover_complete_runs
from tests._reporting_utils import build_fake_combined_run


def test_conclusions_page_helpers_and_complete_run_filter(tmp_path: Path, monkeypatch) -> None:
    base = tmp_path / "outputs" / "combined"
    complete = build_fake_combined_run(base, run_id="RUN_COMPLETE", include_all_questions=True)
    partial = build_fake_combined_run(base, run_id="RUN_PARTIAL", include_all_questions=False)

    reports = tmp_path / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "conclusions_v2_detailed_RUN_COMPLETE.md").write_text("# detailed", encoding="utf-8")
    (reports / "conclusions_v2_executive_RUN_COMPLETE.md").write_text("# executive", encoding="utf-8")
    (reports / "evidence_catalog_RUN_COMPLETE.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    (reports / "test_traceability_RUN_COMPLETE.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    (reports / "slides_traceability_RUN_COMPLETE.csv").write_text(
        "slide_id,requirement_id,covered\n2,SLIDE_02_01,yes\n", encoding="utf-8"
    )
    (reports / "report_qc_RUN_COMPLETE.json").write_text('{"verdict":"PASS"}', encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    runs = discover_complete_runs(Path("outputs/combined"))
    assert [r.name for r in runs] == ["RUN_COMPLETE"]

    ns = runpy.run_path(
        str(
            Path(__file__).resolve().parents[1]
            / "app"
            / "pages"
            / "99_Conclusions.py"
        )
    )
    assert ns["_run_has_all_questions"](complete) is True
    assert ns["_run_has_all_questions"](partial) is False
    paths = ns["_report_paths"]("RUN_COMPLETE")
    assert paths["detailed"].exists()
    assert paths["executive"].exists()
    assert ns["_safe_read_text"](paths["detailed"]).startswith("#")

