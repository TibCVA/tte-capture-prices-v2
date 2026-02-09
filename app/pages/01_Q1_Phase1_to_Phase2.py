from __future__ import annotations

from datetime import datetime

import plotly.express as px
import streamlit as st

from app.page_utils import assumptions_editor, load_annual_metrics
from src.modules.q1_transition import run_q1
from src.modules.result import export_module_result


def render() -> None:
    st.title("Q1 — Passage Phase 1 -> Phase 2")
    st.markdown("Détecte la bascule par score marché et stress physique.")

    annual = load_annual_metrics()
    if annual.empty:
        st.info("Aucune métrique annuelle disponible.")
        return

    countries = sorted(annual["country"].unique())
    selected_countries = st.multiselect("Pays", countries, default=countries)
    year_min = int(annual["year"].min())
    year_max = int(annual["year"].max())
    years = st.slider("Années", min_value=year_min, max_value=year_max, value=(year_min, year_max))

    assumptions = assumptions_editor()

    if st.button("Exécuter Q1", type="primary"):
        run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        sel = {"countries": selected_countries, "years": list(range(years[0], years[1] + 1))}
        res = run_q1(annual, assumptions, sel, run_id)
        export_module_result(res)

        st.subheader("KPI")
        st.json(res.kpis)

        df_sum = res.tables["Q1_country_summary"]
        st.dataframe(df_sum, use_container_width=True)

        panel = res.tables["Q1_year_panel"]
        if not panel.empty:
            fig1 = px.scatter(panel, x="sr_energy", y="capture_ratio_pv_vs_ttl", color="country")
            st.plotly_chart(fig1, use_container_width=True)
            fig2 = px.scatter(panel, x="sr_hours", y="h_negative_obs", color="country")
            st.plotly_chart(fig2, use_container_width=True)
            fig3 = px.scatter(panel, x="sr_energy", y="far_energy", color="h_negative_obs")
            st.plotly_chart(fig3, use_container_width=True)
            fig4 = px.scatter(panel, x="ir_p10", y="capture_ratio_pv_vs_ttl", color="sr_energy")
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown(res.narrative_md)
        st.subheader("Checks")
        st.dataframe(res.checks, use_container_width=True)
        st.subheader("Warnings")
        st.write(res.warnings)
