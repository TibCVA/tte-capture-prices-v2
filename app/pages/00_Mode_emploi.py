from __future__ import annotations

import pandas as pd
import streamlit as st

from app.ui_components import (
    guided_header,
    inject_theme,
    render_interpretation,
    render_question_box,
    render_regime_cards,
    show_definitions_cards,
    show_limitations,
    show_metric_explainers_tabbed,
)
from src.reporting.interpretation_rules import QUESTION_BUSINESS_TEXT


def render() -> None:
    inject_theme()
    guided_header(
        title="Mode d'emploi",
        purpose="Guide complet, pedagogique et autoportant pour comprendre definitions, hypotheses, tests et limites.",
        step_now="Mode d'emploi: poser le cadre",
        step_next="Donnees & Qualite: verifier la base avant toute conclusion",
    )

    # ----------------------------------------------------------------
    # Sommaire
    # ----------------------------------------------------------------
    st.markdown("## Question business")
    render_question_box(
        "Comment lire l'outil correctement, sans confusion entre physique et marche, et sans sur-interpreter les resultats ?"
    )

    st.markdown("### Sommaire")
    st.markdown(
        "1. [Pipeline visuel](#pipeline-visuel)\n"
        "2. [Methode en 4 points](#methode-en-4-points)\n"
        "3. [Conventions normatives (SPEC 0)](#conventions-normatives-spec-0)\n"
        "4. [Mode HIST vs Mode SCEN](#mode-hist-vs-mode-scen)\n"
        "5. [Definitions obligatoires](#definitions-obligatoires)\n"
        "6. [Regimes physiques A/B/C/D](#regimes-physiques-a-b-c-d)\n"
        "7. [Pourquoi ces 5 questions](#pourquoi-ces-5-questions)\n"
        "8. [Donnees sources](#donnees-sources)\n"
        "9. [Glossaire complet](#glossaire-complet)\n"
        "10. [Exemples calcules](#exemples-calcules)\n"
        "11. [Checklist anti-surinterpretation](#checklist-de-lecture-anti-surinterpretation)\n"
        "12. [Hypotheses et gouvernance](#hypotheses-et-gouvernance)\n"
        "13. [Limites](#limites)"
    )

    # ----------------------------------------------------------------
    # Pipeline visuel
    # ----------------------------------------------------------------
    st.markdown("## Pipeline visuel")
    st.markdown(
        '<div class="tte-card" style="text-align:center; padding:1.2rem;">'
        "<strong>ENTSO-E API</strong> &rarr; "
        "<strong>Donnees brutes (parquets)</strong> &rarr; "
        "<strong>Normalisation horaire</strong> &rarr; "
        "<strong>NRL / Surplus / Flex</strong> &rarr; "
        "<strong>Regimes A/B/C/D</strong> &rarr; "
        "<strong>Metriques annuelles</strong> &rarr; "
        "<strong>Q1-Q5</strong> &rarr; "
        "<strong>Conclusions</strong>"
        "</div>",
        unsafe_allow_html=True,
    )
    render_interpretation(
        "Chaque etape alimente la suivante. Les regimes physiques sont calcules SANS utiliser les prix (anti-circularite). "
        "Les prix interviennent uniquement pour les capture prices et les checks de coherence marche."
    )

    # ----------------------------------------------------------------
    # Methode en 4 points
    # ----------------------------------------------------------------
    st.markdown("## Methode en 4 points")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            '<div class="tte-card" style="min-height:120px;">'
            "<strong>1. Physique d'abord</strong><br>"
            "NRL, surplus et flex calcules sans prix."
            "</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="tte-card" style="min-height:120px;">'
            "<strong>2. Prix ensuite</strong><br>"
            "Prix pour capture prices et checks coherence."
            "</div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="tte-card" style="min-height:120px;">'
            "<strong>3. Modules separables</strong><br>"
            "Q1..Q5 reutilisent le meme socle de donnees."
            "</div>",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            '<div class="tte-card" style="min-height:120px;">'
            "<strong>4. Audit-first</strong><br>"
            "Chaque resultat exportable avec hypotheses et checks."
            "</div>",
            unsafe_allow_html=True,
        )

    # ----------------------------------------------------------------
    # Conventions normatives
    # ----------------------------------------------------------------
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
    render_interpretation(
        "Ces conventions s'appliquent a TOUTES les etapes du pipeline. Toute deviation est un flag ERROR."
    )

    # ----------------------------------------------------------------
    # Mode HIST vs SCEN
    # ----------------------------------------------------------------
    st.markdown("## Mode HIST vs Mode SCEN")
    ch, cs = st.columns(2)
    with ch:
        st.markdown(
            '<div class="tte-card" style="min-height:140px;">'
            "<strong>HIST (historique)</strong><br><br>"
            "<em>Donnees:</em> Observations ENTSO-E<br>"
            "<em>Apport:</em> Constats empiriques et signatures observees<br>"
            "<em>Limite:</em> Ne dit pas directement ce qui se passera demain"
            "</div>",
            unsafe_allow_html=True,
        )
    with cs:
        st.markdown(
            '<div class="tte-card" style="min-height:140px;">'
            "<strong>SCEN (prospectif)</strong><br><br>"
            "<em>Donnees:</em> Hypotheses scenario x pays x annee + moteur mecaniste<br>"
            "<em>Apport:</em> Sensibilites et ordres de grandeur conditionnels<br>"
            "<em>Limite:</em> Ce n'est pas un modele d'equilibre complet"
            "</div>",
            unsafe_allow_html=True,
        )
    render_interpretation(
        "Les deux modes utilisent les MEMES formules et le MEME code. "
        "Seule la source de donnees change. Cela garantit la comparabilite des resultats."
    )

    # ----------------------------------------------------------------
    # Definitions obligatoires
    # ----------------------------------------------------------------
    st.markdown("## Definitions obligatoires")
    show_definitions_cards(
        [
            ("NRL", "Load - VRE - MustRun. Besoin residuel net du systeme."),
            ("Surplus", "max(0, -NRL). Energie excedentaire quand NRL est negatif."),
            ("SR", "Part d'energie en surplus sur l'annee (surplus_twh / gen_primary_twh)."),
            ("FAR", "Part du surplus absorbee par la flex (surplus_absorbed / surplus_total)."),
            ("IR", "P10(MustRun)/P10(Load). Rigidite structurelle en creux de charge."),
            ("TTL", "Q95 des prix sur regimes C/D (hors surplus). Approxime l'ancre thermique."),
            ("Capture price", "Prix moyen pondere par la production d'une techno. Mesure la valeur captee."),
        ]
    )
    show_metric_explainers_tabbed(
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

    # ----------------------------------------------------------------
    # Regimes physiques
    # ----------------------------------------------------------------
    st.markdown("## Regimes physiques A/B/C/D")
    render_regime_cards()
    render_interpretation(
        "Les regimes sont determines UNIQUEMENT par la physique (surplus, flex, NRL). "
        "Le prix n'intervient jamais dans la classification. C'est le fondement de l'anti-circularite."
    )

    st.markdown("## Phases structurelles (PS1/PS2/PS3)")
    cp1, cp2, cp3 = st.columns(3)
    with cp1:
        st.markdown(
            '<div class="tte-card" style="border-left:4px solid #059669; min-height:100px;">'
            "<strong>Phase 1</strong><br>"
            "Surplus rare ou facilement absorbe. Peu d'heures negatives. Capture ratio relativement stable."
            "</div>",
            unsafe_allow_html=True,
        )
    with cp2:
        st.markdown(
            '<div class="tte-card" style="border-left:4px solid #d97706; min-height:100px;">'
            "<strong>Phase 2</strong><br>"
            "Surplus frequent, cannibalisation active, hausse des heures basses/negatives."
            "</div>",
            unsafe_allow_html=True,
        )
    with cp3:
        st.markdown(
            '<div class="tte-card" style="border-left:4px solid #7c3aed; min-height:100px;">'
            "<strong>Phase 3</strong><br>"
            "Adaptation systeme (flex, curtailment, demande, exports). Degradation cesse ou s'inverse."
            "</div>",
            unsafe_allow_html=True,
        )

    # ----------------------------------------------------------------
    # Pourquoi ces 5 questions
    # ----------------------------------------------------------------
    st.markdown("## Pourquoi ces 5 questions")
    render_interpretation(
        "Les 5 questions suivent le cycle de vie complet d'un marche en penetration VRE croissante: "
        "detection de bascule (Q1), vitesse de degradation (Q2), conditions de sortie (Q3), "
        "levier batteries (Q4), et sensibilite aux commodites (Q5)."
    )
    for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        text = QUESTION_BUSINESS_TEXT.get(qid, "")
        render_question_box(f"**{qid}** : {text}")

    # ----------------------------------------------------------------
    # Donnees sources
    # ----------------------------------------------------------------
    st.markdown("## Donnees sources")
    st.markdown(
        '<div class="tte-card">',
        unsafe_allow_html=True,
    )
    st.markdown(
        "**Source principale**: ENTSO-E Transparency Platform\n\n"
        "- **Couverture**: FR, DE, ES, NL, BE, CZ, IT_NORD (7 pays)\n"
        "- **Periode**: 2018-2024 (historique), 2030/2040 (prospectif)\n"
        "- **Resolution**: Horaire UTC stricte (8760/8784 heures par an)\n"
        "- **Variables cles**: prix day-ahead, charge totale, generation par techno, echanges transfrontaliers, pompage PSH\n"
        "- **Completeness attendue**: >= 98% pour chaque colonne critique\n"
        "- **Format**: parquets normalises dans `data/processed/hourly/{country}/{year}.parquet`"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    render_interpretation(
        "La qualite des conclusions depend directement de la completeness des donnees ENTSO-E. "
        "Toute serie en dessous de 98% declenche un warning qualite."
    )

    # ----------------------------------------------------------------
    # Glossaire complet
    # ----------------------------------------------------------------
    st.markdown("## Glossaire complet")
    glossary = pd.DataFrame(
        [
            {"Terme": "NRL", "Formule": "Load - VRE - MustRun", "Unite": "MW", "Utilise dans": "Tous les modules"},
            {"Terme": "Surplus", "Formule": "max(0, -NRL)", "Unite": "MW / TWh", "Utilise dans": "Tous les modules"},
            {"Terme": "SR (Surplus Ratio)", "Formule": "surplus_twh / gen_primary_twh", "Unite": "%", "Utilise dans": "Q1, Q2, Q3"},
            {"Terme": "FAR (Flex Absorption Ratio)", "Formule": "surplus_absorbed / surplus_total", "Unite": "%", "Utilise dans": "Q1, Q3, Q4"},
            {"Terme": "IR (Inflexibility Ratio)", "Formule": "P10(must_run) / P10(load)", "Unite": "ratio", "Utilise dans": "Q1, Q3"},
            {"Terme": "TTL (Thermal Tail Level)", "Formule": "Q95(prix | regime C/D)", "Unite": "EUR/MWh", "Utilise dans": "Q2, Q5"},
            {"Terme": "TCA (Thermal Cost Anchor)", "Formule": "gas/eff + CO2*EF/eff + VOM", "Unite": "EUR/MWh", "Utilise dans": "Q5"},
            {"Terme": "Capture price", "Formule": "sum(prix*prod) / sum(prod)", "Unite": "EUR/MWh", "Utilise dans": "Q1, Q2"},
            {"Terme": "Capture ratio", "Formule": "capture_price / reference", "Unite": "ratio", "Utilise dans": "Q1, Q2"},
            {"Terme": "Regime A", "Formule": "surplus_unabsorbed > 0", "Unite": "heures", "Utilise dans": "Socle, Q1"},
            {"Terme": "Regime B", "Formule": "surplus > 0 et unabsorbed = 0", "Unite": "heures", "Utilise dans": "Socle, Q1"},
            {"Terme": "Regime C", "Formule": "NRL >= 0, pas de surplus", "Unite": "heures", "Utilise dans": "Socle, Q5"},
            {"Terme": "Regime D", "Formule": "NRL >= seuil tension", "Unite": "heures", "Utilise dans": "Socle, Q5"},
            {"Terme": "alpha", "Formule": "TTL_obs - TCA_Q95", "Unite": "EUR/MWh", "Utilise dans": "Q5"},
        ]
    )
    st.dataframe(glossary, use_container_width=True, hide_index=True)

    # ----------------------------------------------------------------
    # Exemples calcules
    # ----------------------------------------------------------------
    st.markdown("## Exemples calcules")
    with st.expander("Exemple 1 heure", expanded=True):
        st.markdown(
            '<div class="tte-card">',
            unsafe_allow_html=True,
        )
        st.markdown(
            "**Donnees**: `Load = 50 000 MW`, `VRE = 18 000 MW`, `MustRun = 34 000 MW`\n\n"
            "**Etape 1**: `NRL = 50 000 - 18 000 - 34 000 = -2 000 MW`\n\n"
            "**Etape 2**: `Surplus = max(0, 2 000) = 2 000 MW`\n\n"
            "**Etape 3**: Si flex observee = 1 500 MW, alors `surplus_unabsorbed = 500 MW`\n\n"
            "**Conclusion**: Regime **A** (surplus non absorbe). Pression prix tres basse sur cette heure."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Exemple 1 annee", expanded=False):
        st.markdown(
            '<div class="tte-card">',
            unsafe_allow_html=True,
        )
        st.markdown(
            "**Donnees simplifiees**: Surplus annuel = `12 TWh`, Generation primaire = `480 TWh`, Surplus absorbe = `9 TWh`\n\n"
            "**SR** = 12 / 480 = **2.5%**\n\n"
            "**FAR** = 9 / 12 = **75%**\n\n"
            "**Lecture**: Le surplus est materialise et partiellement absorbe. "
            "Le quart restant (3 TWh) genere une tension potentielle sur les prix en heures de surplus."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------------------
    # Checklist
    # ----------------------------------------------------------------
    st.markdown("## Checklist de lecture (anti-surinterpretation)")
    st.markdown(
        "1. Verifier d'abord `quality_flag`, `completeness` et les checks ERROR/WARN.\n"
        "2. Distinguer explicitement observation historique et simulation prospective.\n"
        "3. Lire les tests un par un (valeur, seuil, statut, interpretation).\n"
        "4. Verifier les limites avant toute conclusion business.\n"
        "5. Ne jamais deduire une causalite forte d'une seule correlation."
    )

    # ----------------------------------------------------------------
    # Hypotheses et gouvernance
    # ----------------------------------------------------------------
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
