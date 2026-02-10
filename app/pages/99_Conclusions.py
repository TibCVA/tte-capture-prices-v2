from __future__ import annotations

from pathlib import Path
import json
import re

import pandas as pd
import streamlit as st

from app.ui_components import (
    guided_header,
    inject_theme,
    render_interpretation,
    render_kpi_cards_styled,
)
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


def _discover_report_run_ids(reports_dir: Path = Path("reports")) -> list[str]:
    if not reports_dir.exists():
        return []
    run_ids: set[str] = set()
    pat = re.compile(r"^conclusions_v2_(?:detailed|executive)_(.+)\.md$")
    for f in reports_dir.glob("conclusions_v2_*_*.md"):
        m = pat.match(f.name)
        if m:
            run_ids.add(m.group(1))
    return sorted(run_ids, reverse=True)


def _split_report_sections(md: str) -> list[tuple[str, str]]:
    """Split a markdown report into sections by H2 headers."""
    if not md:
        return []
    parts = re.split(r"(?=^## )", md, flags=re.MULTILINE)
    sections: list[tuple[str, str]] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        lines = part.split("\n", 1)
        title = lines[0].lstrip("#").strip() if lines else "Section"
        body = lines[1].strip() if len(lines) > 1 else ""
        sections.append((title, body))
    return sections


def _render_report_artifacts(paths: dict[str, Path]) -> None:
    # --- Executive summary in styled card ---
    st.markdown("## Resume executif")
    exec_md = _safe_read_text(paths["executive"])
    if exec_md:
        st.markdown('<div class="tte-exec-card">', unsafe_allow_html=True)
        st.markdown(exec_md)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Aucun resume executif genere pour ce run.")

    # --- QC verdict banner ---
    qc = _safe_read_json(paths["qc"])
    if qc:
        verdict = str(qc.get("verdict", "UNKNOWN"))
        n_checks = len(qc.get("checks", []))
        n_pass = sum(1 for c in qc.get("checks", []) if str(c.get("status", "")).upper() == "PASS")
        if verdict == "PASS":
            st.success(f"Verdict qualite: PASS ({n_pass}/{n_checks} checks reussis)")
        else:
            st.warning(f"Verdict qualite: {verdict} ({n_pass}/{n_checks} checks reussis)")
        render_interpretation(
            f"Le rapport a ete verifie par {n_checks} quality gates automatiques. "
            + ("Tous les checks sont passes." if verdict == "PASS" else "Certains checks ne sont pas passes, verifier les details dans les annexes.")
        )

    # --- Detailed report in navigable expanders ---
    st.markdown("## Rapport detaille")
    detailed_md = _safe_read_text(paths["detailed"])
    if detailed_md:
        sections = _split_report_sections(detailed_md)
        if sections:
            for i, (title, body) in enumerate(sections):
                with st.expander(title, expanded=(i == 0)):
                    st.markdown(body)
        else:
            st.markdown(detailed_md)
    else:
        st.warning("Rapport detaille non trouve. Clique sur le bouton de generation ci-dessus.")

    # --- Annexes ---
    st.markdown("## Annexes de preuve")
    ev = _safe_read_csv(paths["evidence"])
    tt = _safe_read_csv(paths["traceability"])
    stx = _safe_read_csv(paths["slides_traceability"])

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Evidence catalog", "Test traceability", "Slides coverage", "Quality gates"]
    )
    with tab1:
        if ev.empty:
            st.info("Evidence catalog indisponible.")
        else:
            st.dataframe(ev, use_container_width=True)
            render_interpretation("Chaque ligne lie un test a une preuve (table, chart, valeur). Permet de remonter de la conclusion a la donnee.")

    with tab2:
        if tt.empty:
            st.info("Test traceability indisponible.")
        else:
            st.dataframe(tt, use_container_width=True)
            render_interpretation("Trace chaque test jusqu'a sa reference slides TTE. Verifie que toutes les exigences sont couvertes.")

    with tab3:
        if stx.empty:
            st.info("Slides traceability indisponible.")
        else:
            # Slides coverage with color
            if "covered" in stx.columns:
                def _color_coverage(row: pd.Series) -> list[str]:
                    covered = str(row.get("covered", "")).lower()
                    if covered in ("yes", "true", "1"):
                        return ["background-color: #f0fdf4"] * len(row)
                    else:
                        return ["background-color: #fef2f2"] * len(row)

                st.dataframe(stx.style.apply(_color_coverage, axis=1), use_container_width=True, hide_index=True)
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

    # --- KPI dashboard executif ---
    prebuilt_runs = _discover_report_run_ids(Path("reports"))
    complete_runs = discover_complete_runs(Path("outputs/combined"))

    render_kpi_cards_styled(
        [
            {"label": "Runs combines", "value": len(complete_runs), "help": "Nombre de runs Q1-Q5 complets disponibles."},
            {"label": "Rapports pre-generes", "value": len(prebuilt_runs), "help": "Rapports deja generes dans reports/."},
            {"label": "Questions requises", "value": len(REQUIRED_QUESTIONS), "help": "Q1-Q5 doivent toutes etre executees."},
        ]
    )

    st.markdown("## Run combine complet")
    if not complete_runs:
        st.warning("Aucun run combine complet (Q1..Q5) n'est disponible dans `outputs/combined`.")

        if prebuilt_runs:
            st.info("Des rapports pre-generes sont disponibles meme sans run combine local.")
            selected_prebuilt = st.selectbox("Selection du rapport pre-genere", prebuilt_runs, index=0)
            st.caption(f"Run rapport selectionne: `{selected_prebuilt}`")
            _render_report_artifacts(_report_paths(selected_prebuilt))
            st.markdown("---")
            st.markdown("### Optionnel: reconstruire un run combine local")
            st.caption("Necessaire uniquement si vous voulez relancer les analyses Q1..Q5 depuis l'UI.")

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

    _render_report_artifacts(paths)
