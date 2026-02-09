from __future__ import annotations

from datetime import datetime

import plotly.express as px
import streamlit as st

from app.page_utils import assumptions_editor, country_year_selector
from src.modules.q4_bess import run_q4
from src.modules.result import export_module_result
from src.storage import load_hourly


def render() -> None:
    st.title("Q4 — Batteries: ordre de grandeur")
    st.markdown("Simulation simple BESS sur historique: système + actif PV.")

    country, year = country_year_selector()
    try:
        hourly = load_hourly(country, year)
    except Exception:
        st.info("Construis d'abord la table horaire dans Données & Qualité.")
        return

    dispatch_mode = st.selectbox("Mode dispatch", ["SURPLUS_FIRST", "PRICE_ARBITRAGE_SIMPLE", "PV_COLOCATED"])
    assumptions = assumptions_editor()

    if st.button("Exécuter Q4", type="primary"):
        run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        res = run_q4(hourly, assumptions, {"country": country, "year": year}, run_id, dispatch_mode=dispatch_mode)
        export_module_result(res)

        summary = res.tables["Q4_sizing_summary"]
        frontier = res.tables["Q4_bess_frontier"]

        st.dataframe(summary, use_container_width=True)
        st.dataframe(frontier, use_container_width=True)

        if not frontier.empty:
            fig1 = px.line(frontier, x="required_bess_power_mw", y="far_after")
            st.plotly_chart(fig1, use_container_width=True)
            fig2 = px.line(frontier, x="required_bess_energy_mwh", y="surplus_unabs_energy_after")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(res.narrative_md)
        st.dataframe(res.checks, use_container_width=True)
        st.write(res.warnings)
