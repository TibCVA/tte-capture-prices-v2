from __future__ import annotations

import streamlit as st

from app.ui_components import guided_header, inject_theme, show_kpi_cards
from src.constants import DEFAULT_COUNTRIES, DEFAULT_YEAR_END, DEFAULT_YEAR_START


def render() -> None:
    inject_theme()
    guided_header(
        title="TTE Capture Prices V2",
        purpose="Outil d'analyse historique des capture prices et des phases structurelles, auditable et explicable.",
        step_now="Accueil: comprendre le parcours",
        step_next="Mode d'emploi: definitions et methode",
    )

    st.markdown("## Ce que fait l'outil")
    st.markdown(
        "- Expliquer la dynamique des capture prices PV/Wind sur base horaire.\n"
        "- Identifier les bascules de phase et les drivers physiques/marche.\n"
        "- Tester les questions Q1..Q5 avec checks automatiques et exports auditables."
    )

    show_kpi_cards(
        [
            ("Pays cibles", len(DEFAULT_COUNTRIES), "Perimetre par defaut verrouille a 7 pays."),
            ("Fenetre historique", f"{DEFAULT_YEAR_START}-{DEFAULT_YEAR_END}", "Fenetre par defaut utilisee dans les analyses."),
            ("Resolution", "Horaire UTC", "Aucun calcul infra-horaire (pas 15 min)."),
        ]
    )

    st.markdown("## Parcours recommande")
    st.markdown(
        "1. **Mode d'emploi**: comprendre les definitions et limites.\n"
        "2. **Donnees & Qualite**: charger ou recalculer les jeux de donnees.\n"
        "3. **Socle Physique**: verifier NRL/surplus/flex avant interpretation.\n"
        "4. **Q1..Q5**: repondre aux questions business module par module.\n"
        "5. **Conclusions**: lire le rapport final trace au run_id."
    )

    st.info("Le modele reste volontairement pedestre: il privilegie l'explicabilite et l'auditabilite sur la complexite.")
