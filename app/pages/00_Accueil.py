from __future__ import annotations

import streamlit as st

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
    render_interpretation(
        "Suivre ce parcours dans l'ordre garantit que chaque etape repose sur des donnees validees. "
        "Ne pas sauter directement aux conclusions sans avoir verifie la qualite des donnees."
    )
