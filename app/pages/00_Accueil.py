from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import streamlit as st

_PAGE_UTILS_IMPORT_ERROR: Exception | None = None
try:
    from app.page_utils import (
        load_annual_metrics,
        load_phase2_assumptions_table,
        refresh_all_analyses_no_cache_ui,
    )
except Exception as exc:  # pragma: no cover - defensive for Streamlit cloud stale caches
    _PAGE_UTILS_IMPORT_ERROR = exc

    def refresh_all_analyses_no_cache_ui(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(
            "app.page_utils indisponible sur cette instance (cache/deploiement partiel). "
            "Rebooter l'app puis vider le cache Streamlit Cloud."
        )

    def load_annual_metrics(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("load_annual_metrics indisponible.")

    def load_phase2_assumptions_table(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("load_phase2_assumptions_table indisponible.")

_LLM_BATCH_IMPORT_ERROR: Exception | None = None
try:
    from app.llm_analysis import resolve_openai_api_key
    from app.llm_batch import (
        QUESTION_ORDER,
        build_default_selection,
        prepare_bundle_for_question,
        run_parallel_llm_generation,
    )
    from src.config_loader import load_countries
    from src.pipeline import load_assumptions_table
except Exception as exc:  # pragma: no cover - defensive
    _LLM_BATCH_IMPORT_ERROR = exc
    QUESTION_ORDER = ["Q1", "Q2", "Q3", "Q4", "Q5"]  # type: ignore[assignment]

    def resolve_openai_api_key(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("resolve_openai_api_key indisponible.")

    def build_default_selection(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("build_default_selection indisponible.")

    def prepare_bundle_for_question(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("prepare_bundle_for_question indisponible.")

    def run_parallel_llm_generation(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("run_parallel_llm_generation indisponible.")

    def load_countries(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("load_countries indisponible.")

    def load_assumptions_table(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("load_assumptions_table indisponible.")

from app.ui_components import (
    guided_header,
    inject_theme,
    render_interpretation,
    render_kpi_cards_styled,
    render_question_box,
)
from src.constants import DEFAULT_COUNTRIES, DEFAULT_YEAR_END, DEFAULT_YEAR_START
from src.reporting.interpretation_rules import QUESTION_BUSINESS_TEXT


def render() -> None:
    inject_theme()
    guided_header(
        title="TTE Capture Prices V2",
        purpose="Outil d'analyse historique des capture prices et des phases structurelles, auditable et explicable.",
        step_now="Accueil: comprendre le parcours",
        step_next="Mode d'emploi: definitions et methode",
    )

    render_kpi_cards_styled(
        [
            {"label": "Pays cibles", "value": len(DEFAULT_COUNTRIES), "help": "Perimetre par defaut verrouille a 7 pays."},
            {"label": "Fenetre historique", "value": f"{DEFAULT_YEAR_START}-{DEFAULT_YEAR_END}", "help": "Fenetre par defaut utilisee dans les analyses."},
            {"label": "Resolution", "value": "Horaire UTC", "help": "Aucun calcul infra-horaire (pas 15 min)."},
        ]
    )

    st.markdown("## Ce que fait l'outil")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            '<div class="tte-card" style="min-height:130px;">'
            "<strong>Dynamique des capture prices</strong><br>"
            "Expliquer l'evolution des capture prices PV/Wind sur base horaire pour 7 pays europeens."
            "</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="tte-card" style="min-height:130px;">'
            "<strong>Phases structurelles</strong><br>"
            "Identifier les bascules de phase et les drivers physiques/marche (SR, FAR, IR, regimes)."
            "</div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="tte-card" style="min-height:130px;">'
            "<strong>Tests auditables</strong><br>"
            "Tester les questions Q1..Q5 avec checks automatiques et exports auditables traces au run_id."
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("## Les 5 questions business")
    for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        text = QUESTION_BUSINESS_TEXT.get(qid, "")
        render_question_box(f"**{qid}** : {text}")

    st.info(
        "Le modele reste volontairement pedestre: il privilegie l'explicabilite et l'auditabilite sur la complexite. "
        "Les conclusions sont toujours conditionnelles aux hypotheses et doivent etre nuancees."
    )

    st.markdown("## Parcours recommande")
    st.markdown(
        "1. **Mode d'emploi**: comprendre les definitions et limites.\n"
        "2. **Donnees & Qualite**: charger ou recalculer les jeux de donnees.\n"
        "3. **Socle Physique**: verifier NRL/surplus/flex avant interpretation.\n"
        "4. **Q1..Q5**: repondre aux questions business module par module.\n"
        "5. **Conclusions**: lire le rapport final trace au run_id."
    )

    st.markdown("## Rafraichissement global des analyses")
    st.caption(
        "Ce bouton reconstruit toutes les analyses (Q1..Q5) sans reutiliser les caches de calculs, "
        "tout en conservant les donnees ENTSO-E brutes deja telechargees en local."
    )
    if _PAGE_UTILS_IMPORT_ERROR is not None:
        st.error("Impossible de charger le module de refresh global.")
        st.code(str(_PAGE_UTILS_IMPORT_ERROR))
    else:
        if st.button("Lancer / rafraichir toutes les analyses (sans cache calcule)", type="primary"):
            with st.spinner("Refresh global en cours (rebuild historique + run combine Q1..Q5)..."):
                try:
                    refresh_summary = refresh_all_analyses_no_cache_ui(
                        countries=DEFAULT_COUNTRIES,
                        hist_year_start=DEFAULT_YEAR_START,
                        hist_year_end=DEFAULT_YEAR_END,
                        scenario_years=list(range(2025, 2036)),
                    )
                except Exception as exc:
                    st.error(f"Echec du refresh global: {exc}")
                else:
                    run_id = str(refresh_summary.get("run_id", "UNKNOWN"))
                    st.session_state["last_full_refresh_run_id"] = run_id
                    st.success(f"Refresh termine. Nouveau run combine: {run_id}")
                    with st.expander("Details techniques du refresh", expanded=False):
                        st.json(refresh_summary)

    st.markdown("## Generation IA globale")
    st.caption(
        "Lance en une fois les generations IA Q1->Q5 en parallele, avec les selections par defaut "
        "de chaque page question."
    )
    if _LLM_BATCH_IMPORT_ERROR is not None:
        st.error("Impossible de charger le module de batch IA.")
        st.code(str(_LLM_BATCH_IMPORT_ERROR))
    elif st.button("Generer toutes les analyses IA (Q1->Q5 en parallele)", type="primary"):
        try:
            annual_hist = load_annual_metrics()
        except Exception as exc:
            st.error(f"Impossible de charger annual_metrics: {exc}")
            annual_hist = pd.DataFrame()

        if annual_hist.empty:
            st.error("Aucune metrique annuelle disponible. Le batch IA est bloque.")
        else:
            api_key = resolve_openai_api_key()
            if not api_key:
                st.error("Cle OpenAI manquante. Configure OPENAI_API_KEY dans l'environnement ou les secrets Streamlit.")
            else:
                assumptions_phase1 = load_assumptions_table()
                assumptions_phase2 = load_phase2_assumptions_table()
                countries_cfg = load_countries()

                prepared_items: list[dict] = []
                prep_progress = st.progress(0.0)
                prep_status = st.empty()
                total_q = len(QUESTION_ORDER)

                for idx, qid in enumerate(QUESTION_ORDER, start=1):
                    prep_status.text(f"Preparation bundle {qid} ({idx}/{total_q})...")
                    try:
                        selection = build_default_selection(
                            qid,
                            annual_hist=annual_hist,
                            assumptions_phase2=assumptions_phase2,
                            countries_cfg=countries_cfg,
                        )
                        prepared = prepare_bundle_for_question(
                            qid,
                            selection=selection,
                            assumptions_phase1=assumptions_phase1,
                            assumptions_phase2=assumptions_phase2,
                        )
                    except Exception as exc:
                        prepared = {
                            "question_id": qid,
                            "status": "FAILED_PREP",
                            "bundle_hash": "",
                            "error": str(exc),
                        }
                    prepared_items.append(prepared)
                    prep_progress.progress(idx / max(total_q * 2, 1))

                prep_status.text("Generation IA en parallele en cours...")
                with st.spinner("Appels IA Q1->Q5 en execution parallele..."):
                    rows = run_parallel_llm_generation(
                        prepared_items=prepared_items,
                        api_key=api_key,
                        max_workers=5,
                    )
                prep_progress.progress(1.0)
                prep_status.empty()
                prep_progress.empty()

                ok_count = sum(1 for row in rows if row.get("status") == "OK")
                fail_count = len(rows) - ok_count
                st.session_state["last_llm_batch_result"] = {
                    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                    "rows": rows,
                }
                if fail_count == 0:
                    st.success(f"Generation IA terminee: {ok_count}/{len(rows)} questions traitees.")
                else:
                    st.warning(f"Generation IA terminee avec erreurs: {ok_count} succes, {fail_count} echec(s).")

    last_batch = st.session_state.get("last_llm_batch_result")
    if isinstance(last_batch, dict) and isinstance(last_batch.get("rows"), list):
        ts = str(last_batch.get("generated_at_utc", ""))
        if ts:
            st.caption(f"Derniere execution batch IA: {ts}")
        table_rows = list(last_batch.get("rows", []))
        if table_rows:
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

    render_interpretation(
        "Suivre ce parcours dans l'ordre garantit que chaque etape repose sur des donnees validees. "
        "Ne pas sauter directement aux conclusions sans avoir verifie la qualite des donnees."
    )
