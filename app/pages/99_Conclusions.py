from __future__ import annotations

from pathlib import Path
import json

import pandas as pd
import streamlit as st

from app.ui_components import guided_header, inject_theme
from src.reporting.evidence_loader import REQUIRED_QUESTIONS, discover_complete_runs


def _safe_read_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def _safe_read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _report_paths(run_id: str) -> dict[str, Path]:
    reports = Path("reports")
    return {
        "detailed": reports / f"conclusions_v2_detailed_{run_id}.md",
        "executive": reports / f"conclusions_v2_executive_{run_id}.md",
        "evidence": reports / f"evidence_catalog_{run_id}.csv",
        "traceability": reports / f"test_traceability_{run_id}.csv",
        "slides_traceability": reports / f"slides_traceability_{run_id}.csv",
        "qc": reports / f"report_qc_{run_id}.json",
    }


def _run_has_all_questions(run_dir: Path) -> bool:
    for q in REQUIRED_QUESTIONS:
        if not (run_dir / q / "summary.json").exists():
            return False
    return True


def render() -> None:
    inject_theme()
    guided_header(
        title="Conclusions",
        purpose="Rapport final dense, traçable et annexes de preuve.",
        step_now="Conclusions: synthese executive + rapport detaille",
        step_next="Fin du parcours",
    )

    st.markdown("## Run combiné complet")
    complete_runs = discover_complete_runs(Path("outputs/combined"))
    if not complete_runs:
        st.error("Aucun run combiné complet (Q1..Q5) n'est disponible dans `outputs/combined`.")
        return

    labels = [p.name for p in complete_runs if _run_has_all_questions(p)]
    if not labels:
        st.error("Aucun run contenant Q1..Q5 n'a été détecté.")
        return

    selected_run = st.selectbox("Sélection du run", labels, index=0)
    run_dir = Path("outputs/combined") / selected_run
    paths = _report_paths(selected_run)

    st.caption(f"Run sélectionné: `{run_dir}`")

    st.markdown("## Résumé exécutif")
    exec_md = _safe_read_text(paths["executive"])
    if exec_md:
        st.markdown(exec_md)
    else:
        st.info("Aucun résumé exécutif généré pour ce run.")

    st.markdown("## Rapport détaillé")
    detailed_md = _safe_read_text(paths["detailed"])
    if detailed_md:
        st.markdown(detailed_md)
    else:
        st.warning("Rapport détaillé non trouvé. Lance `generate_report.py --run-id <run_id>`.")

    st.markdown("## Annexes de preuve")
    ev = _safe_read_csv(paths["evidence"])
    tt = _safe_read_csv(paths["traceability"])
    stx = _safe_read_csv(paths["slides_traceability"])
    qc = _safe_read_json(paths["qc"])

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Evidence catalog", "Test traceability", "Slides coverage", "Quality gates"]
    )
    with tab1:
        if ev.empty:
            st.info("Evidence catalog indisponible.")
        else:
            st.dataframe(ev, use_container_width=True)
    with tab2:
        if tt.empty:
            st.info("Test traceability indisponible.")
        else:
            st.dataframe(tt, use_container_width=True)
    with tab3:
        if stx.empty:
            st.info("Slides traceability indisponible.")
        else:
            st.dataframe(stx, use_container_width=True)
            missing = stx[stx["covered"].astype(str).str.lower() == "no"] if "covered" in stx.columns else pd.DataFrame()
            st.markdown("### Écarts de couverture")
            if missing.empty:
                st.success("Aucun écart de couverture slides.")
            else:
                st.error(f"{len(missing)} exigence(s) slides non couverte(s).")
                st.dataframe(missing, use_container_width=True)
    with tab4:
        if not qc:
            st.info("Fichier report_qc indisponible.")
        else:
            st.json(qc)
            verdict = str(qc.get("verdict", "UNKNOWN"))
            if verdict == "PASS":
                st.success("Verdict qualité: PASS")
            else:
                st.warning(f"Verdict qualité: {verdict}")

