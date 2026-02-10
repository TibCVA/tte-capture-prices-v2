from __future__ import annotations

import re
from pathlib import Path

import streamlit as st

from app.ui_components import guided_header, inject_theme


_REPORT_PATTERN = re.compile(r"conclusions_v2(?:_detailed)?_(\d{8}_\d{6})\.md$")


def _extract_run_id(path: Path) -> str:
    m = _REPORT_PATTERN.search(path.name)
    return m.group(1) if m else path.stem


def _extract_summary_block(content: str) -> str:
    anchors = [
        "## 8. Reponses directes aux 5 questions",
        "## 8. Synthese finale",
        "## 8.",
    ]
    start = -1
    for a in anchors:
        start = content.find(a)
        if start >= 0:
            break
    if start < 0:
        return content[:1800]
    tail = content[start:]
    end = tail.find("## 9.")
    return tail if end < 0 else tail[:end]


def render() -> None:
    inject_theme()
    guided_header(
        title="Conclusions",
        purpose="Rapport dense et traceable, consolide a partir des outputs V2.",
        step_now="Conclusions: lecture executive et preuves",
        step_next="Fin du parcours",
    )

    reports = sorted(Path("reports").glob("conclusions_v2*_*.md"), reverse=True)
    if not reports:
        st.info("Aucun rapport conclusions disponible pour le moment.")
        return

    labels = [f"{_extract_run_id(r)} | {r.name}" for r in reports]
    selected_label = st.selectbox("Run de rapport", labels, index=0, help="Le rapport detailed est recommande par defaut.")
    selected = reports[labels.index(selected_label)]

    content = selected.read_text(encoding="utf-8")
    summary = _extract_summary_block(content)

    st.markdown("## Resume executif")
    if summary:
        st.markdown(summary)
    else:
        st.info("Section resume non detectee dans ce rapport.")

    st.markdown("## Rapport detaille")
    st.caption(f"Fichier: `{selected}`")
    st.markdown(content)
