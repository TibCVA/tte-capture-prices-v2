from __future__ import annotations

import streamlit as st

from app.ui_components import guided_header, inject_theme, show_definitions, show_limitations

try:
    from app.ui_components import show_metric_explainers
except ImportError:  # Backward-compatible fallback if cloud cache serves an older ui_components module.
    def show_metric_explainers(*args, **kwargs):  # type: ignore[no-redef]
        return None


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
    show_metric_explainers(
        [
            {
                "metric": "SR",
                "definition": "Part structurelle du surplus dans l'annee.",
                "formula": "SR = surplus_twh / gen_primary_twh (ou /load_net_twh en variante explicite)",
                "intuition": "Plus SR est eleve, plus la pression de sur-injection est forte.",
                "interpretation": "SR en hausse = risque accru d'heures tres basses/negatives.",
                "limits": "Depend de la definition must-run et de la qualite generation totale.",
                "dependencies": "load_mw, gen_vre_mw, gen_must_run_mw, mapping techno.",
            },
            {
                "metric": "FAR",
                "definition": "Part du surplus absorbee par la flex observee.",
                "formula": "FAR = surplus_absorbed_energy / surplus_energy",
                "intuition": "Mesure si le systeme sait absorber le surplus.",
                "interpretation": "FAR proche de 1 = surplus majoritairement gere.",
                "limits": "NaN si surplus nul; sensible a la disponibilite net_position/psh.",
                "dependencies": "exports_mw, psh_pump_mw, surplus_mw, regles load_net.",
            },
            {
                "metric": "IR",
                "definition": "Rigidite structurelle en creux de charge.",
                "formula": "IR = P10(must_run_mw) / P10(load_mw)",
                "intuition": "Compare le plancher inflexible a la demande basse.",
                "interpretation": "IR eleve = plus de risque de surplus en heures creuses.",
                "limits": "Percentiles sensibles aux donnees manquantes.",
                "dependencies": "must_run config pays, load net mode, qualite horaires.",
            },
            {
                "metric": "TTL",
                "definition": "Niveau de queue haute des prix hors surplus.",
                "formula": "TTL = Q95(price_da_eur_mwh | regime in {C,D})",
                "intuition": "Approxime la valeur des heures thermiques/tendues.",
                "interpretation": "TTL eleve peut relever l'ancre de valeur hors surplus.",
                "limits": "Ce n'est pas un cout marginal; demande un nombre minimal d'heures C/D.",
                "dependencies": "regime_phys, prix observes, seuil regime D.",
            },
            {
                "metric": "Capture ratio",
                "definition": "Valeur captee par une techno vs reference annuelle.",
                "formula": "capture_ratio = capture_price_tech / baseload_price (ou /TTL selon module)",
                "intuition": "Mesure la cannibalisation de valeur.",
                "interpretation": "Ratio en baisse = decrochage de valeur de la techno.",
                "limits": "Ne prouve pas seul la causalite; depend du choix de reference.",
                "dependencies": "price_da, production techno, filtre qualite.",
            },
        ],
        title="Formules et interpretation des KPI pivots",
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
