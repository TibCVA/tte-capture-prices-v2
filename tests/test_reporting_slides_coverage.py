from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.reporting.slides_requirements import extract_requirements, map_requirements_to_evidence
from tests._reporting_utils import build_fake_docx


def test_slides_extraction_and_mapping(tmp_path: Path) -> None:
    docx1 = build_fake_docx(tmp_path / "slides1.docx", [(2, "Q1 test expected"), (8, "Q2 expected")])
    docx2 = build_fake_docx(tmp_path / "slides2.docx", [(14, "Q3 expected"), (30, "Q5 expected")])

    requirements = extract_requirements([docx1, docx2])
    assert not requirements.empty
    assert {"slide_id", "requirement_id", "source_ref", "requirement_text"}.issubset(requirements.columns)

    evidence = pd.DataFrame(
        [
            {
                "question_id": "Q1",
                "test_id": "Q1-H-01",
                "source_ref": "Slides 2-4",
                "mode": "HIST",
                "scenario_id": "",
                "status": "PASS",
                "value": "1",
                "threshold": ">=0",
                "interpretation": "ok",
                "evidence_ref": "x",
            }
        ]
    )
    mapped = map_requirements_to_evidence(requirements, evidence)
    assert not mapped.empty
    assert {"requirement_id", "covered", "evidence_ref", "report_section"}.issubset(mapped.columns)
    assert set(mapped["covered"].astype(str).unique()).issubset({"yes", "no"})
    # At least one uncovered requirement is explicit when evidence is partial.
    assert (mapped["covered"].astype(str) == "no").any()


def test_slides_extraction_supports_unicode_dash_markers(tmp_path: Path) -> None:
    import zipfile

    path = tmp_path / "slides_unicode.docx"
    xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body>"
        "<w:p><w:r><w:t>Slide 1 — Introduction</w:t></w:r></w:p>"
        "<w:p><w:r><w:t>Slide 2 – Q1 test attendu</w:t></w:r></w:p>"
        "<w:p><w:r><w:t>Slide 3 : Q2 test attendu</w:t></w:r></w:p>"
        "</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", xml)

    requirements = extract_requirements([path])
    assert not requirements.empty
    assert set(requirements["slide_id"].dropna().astype(int).tolist()) == {1, 2, 3}
