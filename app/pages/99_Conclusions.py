from __future__ import annotations

from pathlib import Path

import streamlit as st


def render() -> None:
    st.title("Conclusions")
    st.markdown("Rapport dense et argumente, verifie, copie-colle depuis les analyses post-V2.")

    reports = sorted(Path("reports").glob("conclusions_v2_*.md"), reverse=True)
    if not reports:
        st.info("Aucun rapport conclusions disponible pour le moment.")
        return

    selected = st.selectbox("Rapport", [r.name for r in reports])
    content = (Path("reports") / selected).read_text(encoding="utf-8")
    st.markdown(content)
