from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
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


def _combined_runs() -> list[Path]:
    root = Path("outputs/combined")
    if not root.exists():
        return []
    runs = [p for p in root.iterdir() if p.is_dir()]
    return sorted(runs, key=lambda p: p.stat().st_mtime, reverse=True)


def _combined_question_table(run_dir: Path, question_id: str) -> pd.DataFrame:
    p = run_dir / question_id / "test_ledger.csv"
    if not p.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(p)
    except Exception:
        return pd.DataFrame()


def render() -> None:
    inject_theme()
    guided_header(
        title="Conclusions",
        purpose="Rapport dense et traceable, consolide a partir des outputs V2.",
        step_now="Conclusions: lecture executive et preuves",
        step_next="Fin du parcours",
    )

    reports = sorted(Path("reports").glob("conclusions_v2*_*.md"), reverse=True)
    combined = _combined_runs()

    st.markdown("## Resultats combines (source prioritaire)")
    if not combined:
        st.info("Aucun run combine detecte dans `outputs/combined`.")
    else:
        comb_labels = [f"{p.name}" for p in combined]
        comb_sel = st.selectbox("Run combine", comb_labels, index=0)
        comb_dir = combined[comb_labels.index(comb_sel)]
        q = st.selectbox("Question", ["Q1", "Q2", "Q3", "Q4", "Q5"], index=0)
        ledger = _combined_question_table(comb_dir, q)
        if ledger.empty:
            st.info(f"Aucun test ledger combine pour {q} dans {comb_dir.name}.")
        else:
            st.dataframe(ledger, use_container_width=True)
            status_counts = ledger["status"].astype(str).value_counts(dropna=False).rename_axis("status").reset_index(name="n")
            st.dataframe(status_counts, use_container_width=True)

    st.markdown("## Rapport Markdown")
    if not reports:
        st.info("Aucun rapport markdown disponible pour le moment.")
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
