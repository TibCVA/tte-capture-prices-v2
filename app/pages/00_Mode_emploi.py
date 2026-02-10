from __future__ import annotations

import streamlit as st

from app.ui_components import guided_header, inject_theme, show_definitions, show_limitations


def render() -> None:
    inject_theme()
    guided_header(
        title="Mode d'emploi",
        purpose="Guide rapide pour lire correctement les modules et eviter les sur-interpretations.",
        step_now="Mode d'emploi: poser le cadre",
        step_next="Donnees & Qualite: verifier la base avant toute conclusion",
    )

    st.markdown("## Methode en 4 points")
    st.markdown(
        "1. **Physique d'abord**: NRL, surplus et flex sont calcules sans utiliser le prix.\n"
        "2. **Prix ensuite**: les prix servent aux capture prices et aux checks de coherence.\n"
        "3. **Modules separables**: Q1..Q5 reutilisent le meme socle de donnees.\n"
        "4. **Audit-first**: chaque resultat est exportable avec hypotheses et checks."
    )

    show_definitions(
        [
            ("NRL", "Load - VRE - MustRun."),
            ("Surplus", "max(0, -NRL)."),
            ("SR", "Part d'energie en surplus sur l'annee."),
            ("FAR", "Part du surplus absorbee par la flex."),
            ("IR", "P10(MustRun)/P10(Load)."),
            ("TTL", "Q95 des prix sur regimes C/D (hors surplus)."),
            ("Capture price", "Prix moyen pondere par la production d'une techno."),
        ]
    )

    st.markdown("## Regimes physiques A/B/C/D")
    st.markdown(
        "- **A**: surplus non absorbe (pression prix tres bas).\n"
        "- **B**: surplus absorbe (surplus present mais gere).\n"
        "- **C**: normal hors surplus.\n"
        "- **D**: tension (NRL eleve)."
    )

    st.markdown("## Lecture des resultats")
    st.markdown(
        "- Commencer par le flag qualite (`quality_flag`).\n"
        "- Lire les checks PASS/WARN/FAIL avant la narrative.\n"
        "- Separer ce qui est observe (historique) de ce qui est simule."
    )

    show_limitations(
        [
            "Pas de modele de marche complet (pas de merit-order endogene).",
            "Pas de reseau europeen integre ni de contraintes intra-zone fines.",
            "Pas de resolution 15 minutes.",
            "Les correlations ne prouvent pas la causalite.",
        ]
    )
