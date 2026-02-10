"""Extract and map slide requirements to evidence rows."""

from __future__ import annotations

from pathlib import Path
import re
import zipfile

import pandas as pd


_SLIDE_MARKER_RE = re.compile(r"\bSlide\s+(\d+)\s*(?:-|:|--)\s*", flags=re.IGNORECASE)


def _read_docx_text(docx_path: Path) -> str:
    with zipfile.ZipFile(docx_path, "r") as zf:
        xml = zf.read("word/document.xml").decode("utf-8", errors="ignore")
    text = re.sub(r"<[^>]+>", " ", xml)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _slide_to_question(slide_id: int) -> str:
    if 2 <= slide_id <= 7:
        return "Q1"
    if 8 <= slide_id <= 13:
        return "Q2"
    if 14 <= slide_id <= 19:
        return "Q3"
    if 20 <= slide_id <= 25:
        return "Q4"
    if 26 <= slide_id <= 31:
        return "Q5"
    if slide_id in {1, 32, 33}:
        return "GLOBAL"
    return "UNKNOWN"


def _atomize_requirements(slide_id: int, slide_text: str) -> list[dict[str, str]]:
    clean = re.sub(r"\s+", " ", str(slide_text)).strip()
    if not clean:
        return []
    parts = [p.strip() for p in re.split(r"[.;:]\s+", clean) if p.strip()]
    rows: list[dict[str, str]] = []
    for idx, part in enumerate(parts, start=1):
        rows.append(
            {
                "slide_id": str(slide_id),
                "requirement_id": f"SLIDE_{slide_id:02d}_{idx:02d}",
                "question_id": _slide_to_question(slide_id),
                "source_ref": f"Slides {slide_id}",
                "requirement_text": part,
            }
        )
    return rows


def extract_requirements_from_docx(docx_path: Path) -> pd.DataFrame:
    cols = ["slide_id", "requirement_id", "question_id", "source_ref", "requirement_text", "docx"]
    if not docx_path.exists():
        return pd.DataFrame(columns=cols)

    text = _read_docx_text(docx_path)
    matches = list(_SLIDE_MARKER_RE.finditer(text))
    if not matches:
        return pd.DataFrame(columns=cols)

    rows: list[dict[str, str]] = []
    for i, m in enumerate(matches):
        slide_id = int(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        for row in _atomize_requirements(slide_id, body):
            row["docx"] = str(docx_path)
            rows.append(row)

    return pd.DataFrame(rows, columns=cols)


def extract_requirements(docx_paths: list[Path]) -> pd.DataFrame:
    cols = ["slide_id", "requirement_id", "question_id", "source_ref", "requirement_text", "docx"]
    frames = [extract_requirements_from_docx(p) for p in docx_paths]
    frames = [f for f in frames if not f.empty]
    if not frames:
        return pd.DataFrame(columns=cols)
    out = pd.concat(frames, ignore_index=True)
    out["slide_id"] = pd.to_numeric(out["slide_id"], errors="coerce").astype("Int64")
    out = out.sort_values(["slide_id", "requirement_id"]).reset_index(drop=True)
    return out


def _extract_slide_ids_from_source_ref(source_ref: str) -> set[int]:
    ref = str(source_ref)
    out: set[int] = set()

    for m in re.finditer(r"[Ss]lides?\s+(\d+)\s*-\s*(\d+)", ref):
        a = int(m.group(1))
        b = int(m.group(2))
        lo, hi = (a, b) if a <= b else (b, a)
        out.update(range(lo, hi + 1))

    for m in re.finditer(r"[Ss]lides?\s+(\d+)", ref):
        out.add(int(m.group(1)))

    for m in re.finditer(r"[Ss]lide\s+(\d+)", ref):
        out.add(int(m.group(1)))

    return out


def map_requirements_to_evidence(requirements: pd.DataFrame, evidence: pd.DataFrame) -> pd.DataFrame:
    out_cols = [
        "slide_id",
        "requirement_id",
        "question_id",
        "requirement_text",
        "covered",
        "coverage_method",
        "evidence_ref",
        "test_id",
        "report_section",
    ]
    if requirements.empty:
        return pd.DataFrame(columns=out_cols)

    ev = evidence.copy()
    if not ev.empty:
        ev["slide_ids"] = ev["source_ref"].astype(str).map(_extract_slide_ids_from_source_ref)
    else:
        ev = pd.DataFrame(columns=["slide_ids", "evidence_ref", "test_id", "question_id"])

    rows: list[dict[str, str]] = []
    for _, req in requirements.iterrows():
        slide_id = int(req["slide_id"])
        req_q = str(req.get("question_id", "")).upper()

        if not ev.empty:
            matches = ev[ev["slide_ids"].map(lambda s: slide_id in s if isinstance(s, set) else False)]
        else:
            matches = pd.DataFrame()
        coverage_method = "direct_slide_match"

        if matches.empty and not ev.empty:
            if req_q in {"Q1", "Q2", "Q3", "Q4", "Q5"} and "question_id" in ev.columns:
                q_matches = ev[ev["question_id"].astype(str).str.upper() == req_q]
                if not q_matches.empty:
                    matches = q_matches
                    coverage_method = "question_fallback"
            elif req_q in {"GLOBAL", "UNKNOWN"}:
                matches = ev.copy()
                coverage_method = "global_fallback"

        covered = not matches.empty
        evidence_ref = "; ".join(matches["evidence_ref"].astype(str).unique()[:3]) if covered else ""
        test_id = "; ".join(matches["test_id"].astype(str).unique()[:5]) if covered else ""
        rows.append(
            {
                "slide_id": slide_id,
                "requirement_id": str(req.get("requirement_id", "")),
                "question_id": str(req.get("question_id", "")),
                "requirement_text": str(req.get("requirement_text", "")),
                "covered": "yes" if covered else "no",
                "coverage_method": coverage_method if covered else "none",
                "evidence_ref": evidence_ref,
                "test_id": test_id,
                "report_section": str(req.get("question_id", "GLOBAL")),
            }
        )

    return pd.DataFrame(rows, columns=out_cols)
