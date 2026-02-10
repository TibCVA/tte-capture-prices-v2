from __future__ import annotations

from pathlib import Path
import json

import pandas as pd


QUESTIONS = ["Q1", "Q2", "Q3", "Q4", "Q5"]


def build_fake_combined_run(root: Path, run_id: str = "RUN_TEST", include_all_questions: bool = True) -> Path:
    run_dir = root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    questions = QUESTIONS if include_all_questions else ["Q1", "Q2", "Q3"]
    for idx, q in enumerate(questions, start=1):
        q_dir = run_dir / q
        q_dir.mkdir(parents=True, exist_ok=True)

        summary = {
            "question_id": q,
            "run_id": run_id,
            "selection": {"countries": ["FR"]},
            "scenarios": ["BASE"],
            "checks": [{"status": "PASS", "code": f"{q}_PASS", "message": "ok", "scope": "HIST", "scenario_id": ""}],
            "warnings": [],
        }
        (q_dir / "summary.json").write_text(json.dumps(summary), encoding="utf-8")

        ledger = pd.DataFrame(
            [
                {
                    "test_id": f"{q}-H-01",
                    "question_id": q,
                    "source_ref": f"Slides {idx + 1}",
                    "mode": "HIST",
                    "scenario_group": "HIST_BASE",
                    "title": "test hist",
                    "what_is_tested": "hist test",
                    "metric_rule": "rule",
                    "severity_if_fail": "HIGH",
                    "scenario_id": "",
                    "status": "PASS",
                    "value": "1",
                    "threshold": ">=0",
                    "interpretation": "ok",
                },
                {
                    "test_id": f"{q}-S-01",
                    "question_id": q,
                    "source_ref": f"Slides {idx + 1}",
                    "mode": "SCEN",
                    "scenario_group": "DEFAULT",
                    "title": "test scen",
                    "what_is_tested": "scen test",
                    "metric_rule": "rule",
                    "severity_if_fail": "HIGH",
                    "scenario_id": "BASE",
                    "status": "PASS",
                    "value": "2",
                    "threshold": ">=0",
                    "interpretation": "ok",
                },
            ]
        )
        ledger.to_csv(q_dir / "test_ledger.csv", index=False)

        cmp_df = pd.DataFrame(
            [
                {
                    "country": "FR",
                    "scenario_id": "BASE",
                    "metric": "metric_x",
                    "hist_value": 1.0,
                    "scen_value": 2.0,
                    "delta": 1.0,
                }
            ]
        )
        cmp_df.to_csv(q_dir / "comparison_hist_vs_scen.csv", index=False)
        (q_dir / "narrative.md").write_text(f"Narrative {q}\n", encoding="utf-8")

    return run_dir


def build_fake_docx(path: Path, slides: list[tuple[int, str]]) -> Path:
    import zipfile

    body_parts = []
    for slide_id, text in slides:
        body_parts.append(f"<w:p><w:r><w:t>Slide {slide_id} - {text}</w:t></w:r></w:p>")
    body_xml = "".join(body_parts)
    xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body_xml}</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", xml)
    return path

