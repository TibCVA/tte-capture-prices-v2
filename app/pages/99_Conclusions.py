from __future__ import annotations

from pathlib import Path
import json

import pandas as pd
import streamlit as st

from app.ui_components import guided_header, inject_theme
from src.reporting.evidence_loader import (
    REQUIRED_QUESTIONS,
    assemble_complete_run_from_fragments,
    discover_complete_runs,
    latest_fragment_per_question,
)


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


def _generate_reports_for_run(run_id: str, strict: bool = True) -> tuple[bool, str]:
    try:
        from generate_report import generate_report

        result = generate_report(
            run_id=run_id,
            strict=strict,
            country_scope=[],
            docx_paths=[],
            output_dir=Path("reports"),
        )
        return True, f"Rapport genere. Verdict: {result.qc.get('verdict', 'UNKNOWN')}"
    except RuntimeError as exc:
        # Strict mode can fail quality gates while still producing report artifacts.
        paths = _report_paths(run_id)
        if paths["detailed"].exists() or paths["executive"].exists():
            return True, f"Rapport genere avec ecarts quality-gate: {exc}"
        return False, f"Echec generation rapport (strict): {exc}"
    except Exception as exc:
        return False, f"Echec generation rapport: {exc}"


def render() -> None:
    inject_theme()
    guided_header(
        title="Conclusions",
        purpose="Rapport final dense, tracable et annexes de preuve.",
        step_now="Conclusions: synthese executive + rapport detaille",
        step_next="Fin du parcours",
    )

    st.markdown("## Run combine complet")
    complete_runs = discover_complete_runs(Path("outputs/combined"))
    if not complete_runs:
        st.warning("Aucun run combine complet (Q1..Q5) n'est disponible dans `outputs/combined`.")
        fragments = latest_fragment_per_question(Path("outputs/combined"))
        st.markdown("### Fragments detectes par question")
        frag_rows = []
        for q in REQUIRED_QUESTIONS:
            p = fragments.get(q)
            frag_rows.append(
                {
                    "question": q,
                    "disponible": p is not None,
                    "source_fragment": str(p) if p is not None else "",
                }
            )
        st.dataframe(pd.DataFrame(frag_rows), use_container_width=True)

        missing = [q for q in REQUIRED_QUESTIONS if q not in fragments]
        if missing:
            st.error(f"Impossible d'assembler automatiquement un run complet. Questions manquantes: {missing}")
            st.info("Lance au moins une analyse complete sur chaque page Q1..Q5, puis reviens ici.")
            return

        if st.button("Assembler un run complet a partir des derniers fragments Q1..Q5", type="primary"):
            try:
                run_dir = assemble_complete_run_from_fragments(Path("outputs/combined"))
                st.success(f"Run assemble: {run_dir.name}")
                st.rerun()
            except Exception as exc:
                st.error(f"Echec assemblage run complet: {exc}")
        return

    labels = [p.name for p in complete_runs if _run_has_all_questions(p)]
    if not labels:
        st.error("Aucun run contenant Q1..Q5 n'a ete detecte.")
        return

    selected_run = st.selectbox("Selection du run", labels, index=0)
    run_dir = Path("outputs/combined") / selected_run
    paths = _report_paths(selected_run)

    st.caption(f"Run selectionne: `{run_dir}`")

    st.markdown("## Generation du rapport")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generer / mettre a jour le rapport pour ce run", type="primary"):
            with st.spinner("Generation rapport en cours..."):
                ok, msg = _generate_reports_for_run(selected_run, strict=False)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    with col2:
        if st.button("Verifier quality gates (strict)"):
            with st.spinner("Generation rapport (strict) en cours..."):
                ok, msg = _generate_reports_for_run(selected_run, strict=True)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    st.markdown("## Resume executif")
    exec_md = _safe_read_text(paths["executive"])
    if exec_md:
        st.markdown(exec_md)
    else:
        st.info("Aucun resume executif genere pour ce run.")

    st.markdown("## Rapport detaille")
    detailed_md = _safe_read_text(paths["detailed"])
    if detailed_md:
        st.markdown(detailed_md)
    else:
        st.warning("Rapport detaille non trouve. Clique sur le bouton de generation ci-dessus.")

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
            st.markdown("### Ecarts de couverture")
            if missing.empty:
                st.success("Aucun ecart de couverture slides.")
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
                st.success("Verdict qualite: PASS")
            else:
                st.warning(f"Verdict qualite: {verdict}")
