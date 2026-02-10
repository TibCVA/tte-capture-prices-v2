from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import (
    load_phase2_assumptions_table,
    load_scenario_annual_metrics_ui,
    load_scenario_validation_findings_ui,
    phase2_assumptions_editor,
    run_phase2_scenario_ui,
)
from app.ui_components import guided_header, inject_theme, show_definitions, show_kpi_cards


def _safe_list(series: pd.Series) -> list[str]:
    return sorted(series.dropna().astype(str).unique().tolist())


def render() -> None:
    inject_theme()
    guided_header(
        title="Scenarios Phase 2",
        purpose="Construire et comparer des trajectoires prospectives sur le meme socle physique que l'historique.",
        step_now="Scenarios: executer le prospectif",
        step_next="Q1..Q5: analyser en mode prospectif",
    )

    st.markdown("## Question business")
    st.markdown("Que donnent les indicateurs Q1..Q5 sous hypotheses prospectives (demande, mix, flex, CO2/gaz) ?")

    show_definitions(
        [
            ("Mode SCEN", "Calcul prospectif mecaniste, sans optimisation d'equilibre de marche."),
            ("Scenario ID", "Identifiant unique d'un jeu d'hypotheses scenario x pays x annee."),
            ("Comparabilite", "Les KPI sont calcules avec les memes formules qu'en historique."),
        ]
    )

    assumptions = phase2_assumptions_editor("phase2_page")
    if assumptions.empty:
        st.info("Aucune hypothese Phase 2 disponible.")
        return

    st.markdown("## Hypotheses utilisees")
    scenario_ids = _safe_list(assumptions["scenario_id"])
    countries = _safe_list(assumptions["country"])
    years = sorted(pd.to_numeric(assumptions["year"], errors="coerce").dropna().astype(int).unique().tolist())

    col1, col2, col3 = st.columns(3)
    with col1:
        scenario_id = st.selectbox("Scenario ID", scenario_ids)
    with col2:
        selected_countries = st.multiselect("Pays", countries, default=countries)
    with col3:
        selected_years = st.multiselect("Annees", years, default=years)

    run_res = run_phase2_scenario_ui(scenario_id, selected_countries, selected_years)
    if run_res is not None:
        st.session_state["phase2_last_run"] = {
            "scenario_id": scenario_id,
            "countries": selected_countries,
            "years": selected_years,
            "run_ts": datetime.utcnow().isoformat(),
        }
        with st.expander("Details execution scenario", expanded=False):
            st.json(run_res)

    st.markdown("## Tests empiriques")
    annual = load_scenario_annual_metrics_ui(scenario_id)
    if annual.empty:
        st.info("Aucun resultat prospectif trouve. Lance le scenario ci-dessus.")
        return
    annual = annual[annual["country"].isin(selected_countries) & annual["year"].isin(selected_years)].copy()
    findings = load_scenario_validation_findings_ui(scenario_id)
    if not findings.empty:
        findings = findings[findings["country"].isin(selected_countries) & findings["year"].isin(selected_years)].copy()

    n_warn = int((findings.get("severity") == "WARN").sum()) if not findings.empty else 0
    n_err = int((findings.get("severity") == "ERROR").sum()) if not findings.empty else 0

    show_kpi_cards(
        [
            ("Lignes annuelles", int(len(annual)), "Nombre de combinaisons pays-annee scenario."),
            ("WARN", n_warn, "Warnings reality checks sur le scenario."),
            ("ERROR", n_err, "Erreurs hard checks sur le scenario."),
        ]
    )

    st.markdown("## Resultats et interpretation")
    st.dataframe(annual, use_container_width=True)

    if {"country", "year", "capture_ratio_pv_vs_ttl"}.issubset(annual.columns):
        fig = px.line(
            annual.sort_values(["country", "year"]),
            x="year",
            y="capture_ratio_pv_vs_ttl",
            color="country",
            title=f"Capture ratio PV vs TTL ({scenario_id})",
            markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)

    if {"country", "year", "h_negative"}.issubset(annual.columns):
        fig2 = px.bar(
            annual.sort_values(["year", "country"]),
            x="country",
            y="h_negative",
            color="year",
            barmode="group",
            title=f"Heures negatives projetees ({scenario_id})",
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("## Limites")
    st.markdown(
        "- Le mode SCEN est mecaniste, pas un modele d'equilibre complet.\n"
        "- Les resultats dependent fortement des hypotheses de flexibilite/export et de must-run.\n"
        "- Les conclusions sont fragilisees si des findings `ERROR` persistent.\n"
        "- L'analyse doit toujours etre relue avec Q1..Q5 pour interpretation business."
    )

    st.markdown("## Checks & exports")
    if findings.empty:
        st.info("Aucun finding scenario disponible.")
    else:
        st.dataframe(findings, use_container_width=True)
        st.caption(f"Exports scenario: `data/processed/scenario/{scenario_id}/...`")
