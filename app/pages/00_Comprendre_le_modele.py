from __future__ import annotations

import pandas as pd
import streamlit as st

from app.ui_components import guided_header, inject_theme, render_interpretation


def render() -> None:
    inject_theme()
    guided_header(
        title="Comprendre le modele",
        purpose="Definitions canoniques, logique Q1..Q5, et lecture des warnings/checks.",
        step_now="Modele: definitions et interpretation",
        step_next="Executer Q1..Q5 avec hypotheses auditees",
    )

    st.markdown("## Definitions canoniques")
    defs = pd.DataFrame(
        [
            {"metric": "load_total_mw", "definition": "Charge totale publiee ENTSO-E."},
            {"metric": "load_mw", "definition": "Charge utilisee pour NRL (net of PSH pump si couverture suffisante)."},
            {"metric": "vre_mw", "definition": "PV + eolien (onshore + offshore)."},
            {"metric": "must_run_mw", "definition": "Somme des planchers techno (quantile annuel, floor approach)."},
            {"metric": "NRL_mw", "definition": "load_mw - vre_mw - must_run_mw."},
            {"metric": "surplus_mw", "definition": "max(0, -NRL_mw)."},
            {"metric": "absorbed_mw", "definition": "min(surplus_mw, flex_sinks_mw)."},
            {"metric": "unabsorbed_mw", "definition": "surplus_mw - absorbed_mw."},
            {"metric": "SR_energy", "definition": "sum(surplus_mwh) / sum(gen_primary_mwh)."},
            {"metric": "FAR_energy", "definition": "sum(absorbed_mwh) / sum(surplus_mwh), et =1 si surplus=0."},
            {"metric": "IR", "definition": "P10(must_run_mw) / P10(load_mw)."},
            {"metric": "TTL_obs", "definition": "Quantile haut (P95) du prix en regimes C/D."},
            {"metric": "TTL_anchor", "definition": "Ancre thermique: fuel/eta + co2*EF/eta + VOM."},
        ]
    )
    st.dataframe(defs, use_container_width=True, hide_index=True)

    st.markdown("## Comment lire Q1..Q5")
    q = pd.DataFrame(
        [
            {
                "module": "Q1",
                "question": "Bascule vers phase 2 ?",
                "lecture": "LOW-PRICE ou PHYSICAL obligatoire; CAPTURE seul interdit; score + persistance.",
            },
            {
                "module": "Q2",
                "question": "Pente phase 2 ?",
                "lecture": "Regressions sur fenetre phase2 coherente avec Q1, versions all_years et sans outliers.",
            },
            {
                "module": "Q3",
                "question": "Sortie phase 2 ?",
                "lecture": "Readiness stage3 via FAR cible + tendance h_negative/capture + leviers requis.",
            },
            {
                "module": "Q4",
                "question": "Sizing BESS ?",
                "lecture": "Dispatch auditable, grille (P,E) monotone, plus petite solution atteignant l'objectif.",
            },
            {
                "module": "Q5",
                "question": "Impact CO2/gaz sur TTL ?",
                "lecture": "Ancre thermique choisie generiquement, requis >=0, statut already_above_target explicite.",
            },
        ]
    )
    st.dataframe(q, use_container_width=True, hide_index=True)

    st.markdown("## Warnings et actions")
    warnings = pd.DataFrame(
        [
            {"status": "PASS", "meaning": "Regle validee.", "action": "Exploitable."},
            {"status": "INFO", "meaning": "Point de contexte.", "action": "Documenter dans la restitution."},
            {"status": "WARN", "meaning": "Fragilite ou limite explicite.", "action": "Nuancer la conclusion et traiter l'action suggeree."},
            {"status": "FAIL", "meaning": "Violation de regle critique.", "action": "Ne pas conclure avant correction."},
            {"status": "NON_TESTABLE", "meaning": "Donnee/perimetre insuffisant.", "action": "Combler donnees ou utiliser un fallback explicite."},
        ]
    )
    st.dataframe(warnings, use_container_width=True, hide_index=True)

    st.markdown("## Data quality panel")
    dq = pd.DataFrame(
        [
            {"champ": "missing_hours_pct", "interpretation": "Part d'heures invalides/manquantes."},
            {"champ": "load_net_mode", "interpretation": "net_of_psh_pump ou as_reported."},
            {"champ": "must_run_mode", "interpretation": "floor_quantile ou profile_from_hist_scaled."},
            {"champ": "must_run_scope_coverage", "interpretation": "Couverture must-run en heures low-load."},
            {"champ": "outlier_year", "interpretation": "Annee atypique detectee (z-score)."},
            {"champ": "core_sanity_issue_count", "interpretation": "Nombre d'invariants physiques violes."},
        ]
    )
    st.dataframe(dq, use_container_width=True, hide_index=True)

    st.markdown("## Gouvernance et securite")
    st.markdown("- Aucun secret n'est stocke dans le repo.")
    st.markdown("- `ENTSOE_API_KEY` doit rester une variable d'environnement.")
    st.markdown("- Les ajustements de checks doivent etre traces dans `VERIFICATION.md`.")

    render_interpretation(
        "Utiliser les modules dans l'ordre Q1 -> Q5. "
        "Si un module est WARN/FAIL, corriger la cause avant de propager des conclusions downstream."
    )


if __name__ == "__main__":
    render()
