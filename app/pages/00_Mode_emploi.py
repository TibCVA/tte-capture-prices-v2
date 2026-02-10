from __future__ import annotations

import pandas as pd
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
        purpose="Guide complet, pedagogique et autoportant pour comprendre definitions, hypotheses, tests et limites.",
        step_now="Mode d'emploi: poser le cadre",
        step_next="Donnees & Qualite: verifier la base avant toute conclusion",
    )

    st.markdown("## Question business")
    st.markdown(
        "Comment lire l'outil correctement, sans confusion entre physique et marche, et sans sur-interpreter les resultats ?"
    )

    st.markdown("## Methode en 4 points")
    st.markdown(
        "1. **Physique d'abord**: NRL, surplus et flex sont calcules sans utiliser le prix.\n"
        "2. **Prix ensuite**: les prix servent aux capture prices et aux checks de coherence.\n"
        "3. **Modules separables**: Q1..Q5 reutilisent le meme socle de donnees.\n"
        "4. **Audit-first**: chaque resultat est exportable avec hypotheses et checks."
    )

    st.markdown("## Conventions normatives (SPEC 0)")
    conventions = pd.DataFrame(
        [
            {
                "Bloc": "Temps",
                "Regle": "Calcul interne strictement horaire en UTC (8760/8784 heures).",
                "Pourquoi c'est critique": "Evite les biais DST et les erreurs d'aggregation.",
            },
            {
                "Bloc": "Unites",
                "Regle": "Puissance en MW, energie en MWh/TWh, prix en EUR/MWh.",
                "Pourquoi c'est critique": "Evite les comparaisons fausses entre pays/annees.",
            },
            {
                "Bloc": "Signes",
                "Regle": "Net position > 0 = export net ; < 0 = import net.",
                "Pourquoi c'est critique": "Conditionne FAR et interpretation du surplus.",
            },
            {
                "Bloc": "Anti-circularite",
                "Regle": "Les regimes physiques A/B/C/D ne sont jamais definis par le prix.",
                "Pourquoi c'est critique": "Evite un raisonnement tautologique.",
            },
            {
                "Bloc": "Donnees manquantes",
                "Regle": "Pas d'imputation silencieuse des trous critiques.",
                "Pourquoi c'est critique": "Preserve l'auditabilite et la reproductibilite.",
            },
        ]
    )
    st.dataframe(conventions, use_container_width=True, hide_index=True)

    st.markdown("## Mode HIST vs Mode SCEN")
    mode_table = pd.DataFrame(
        [
            {
                "Mode": "HIST (historique)",
                "Ce que l'on utilise": "Donnees observees ENTSO-E",
                "Ce que cela apporte": "Constats empiriques et signatures observees",
                "Limite principale": "Ne dit pas directement ce qui se passera demain",
            },
            {
                "Mode": "SCEN (prospectif)",
                "Ce que l'on utilise": "Hypotheses scenario x pays x annee + moteur mecaniste",
                "Ce que cela apporte": "Sensibilites et ordres de grandeur conditionnels",
                "Limite principale": "Ce n'est pas un modele d'equilibre complet",
            },
        ]
    )
    st.dataframe(mode_table, use_container_width=True, hide_index=True)

    st.markdown("## Phases structurelles (PS1/PS2/PS3)")
    st.markdown(
        "- **PS1**: surplus rare ou facilement absorbe, peu d'heures negatives, capture ratio relativement stable.\n"
        "- **PS2**: surplus frequent, cannibalisation active, hausse des heures basses/negatives.\n"
        "- **PS3**: adaptation systeme (flex, curtailment, demande, exports), la degradation cesse d'empirer ou s'inverse."
    )

    st.markdown("## Definitions obligatoires")
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
                "limits": "Ce n'est pas un cout marginal; demande un minimum d'heures C/D.",
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

    st.markdown("## Exemple calcule - 1 heure")
    st.markdown(
        "Exemple pedagogique (heure t): `Load=50 000 MW`, `VRE=18 000 MW`, `MustRun=34 000 MW`.\n"
        "- `NRL = 50 000 - 18 000 - 34 000 = -2 000 MW`\n"
        "- `Surplus = max(0, 2 000) = 2 000 MW`\n"
        "- Si flex observee = 1 500 MW, alors `surplus_unabsorbed = 500 MW` et regime `A`."
    )

    st.markdown("## Exemple calcule - 1 annee")
    st.markdown(
        "Exemple pedagogique simplifie:\n"
        "- Surplus annuel = `12 TWh`\n"
        "- Generation primaire = `480 TWh`\n"
        "- Surplus absorbe = `9 TWh`\n"
        "On obtient:\n"
        "- `SR = 12 / 480 = 2.5%`\n"
        "- `FAR = 9 / 12 = 75%`\n"
        "Lecture: le surplus est materialise et partiellement absorbe, donc tension potentielle sur les prix en heures de surplus."
    )

    st.markdown("## Checklist de lecture (anti-surinterpretation)")
    st.markdown(
        "1. Verifier d'abord `quality_flag`, `completeness` et les checks ERROR/WARN.\n"
        "2. Distinguer explicitement observation historique et simulation prospective.\n"
        "3. Lire les tests un par un (valeur, seuil, statut, interpretation).\n"
        "4. Verifier les limites avant toute conclusion business.\n"
        "5. Ne jamais deduire une causalite forte d'une seule correlation."
    )

    st.markdown("## Hypotheses et gouvernance")
    st.markdown(
        "- Les hypotheses sont versionnees dans `data/assumptions/phase1_assumptions.csv` et `data/assumptions/phase2/phase2_scenario_country_year.csv`.\n"
        "- Toute execution doit etre tracable via un `run_id` et des exports explicites (tables, checks, narrative).\n"
        "- Les secrets (ENTSO-E) ne sont jamais commits et restent hors code."
    )

    show_limitations(
        [
            "Pas de modele de marche complet (pas de merit-order endogene).",
            "Pas de reseau europeen integre ni de contraintes intra-zone fines.",
            "Pas de resolution 15 minutes.",
            "Les correlations ne prouvent pas la causalite.",
        ]
    )
