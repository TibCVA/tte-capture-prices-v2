from __future__ import annotations

from datetime import datetime

import plotly.express as px
import streamlit as st

from app.page_utils import assumptions_editor, load_annual_metrics
from src.modules.q2_slope import run_q2
from src.modules.result import export_module_result


def render() -> None:
    st.title("Q2 — Pente de la Phase 2")
    st.markdown("Mesure la pente empirique de cannibalisation et ses drivers.")

    annual = load_annual_metrics()
    if annual.empty:
        st.info("Aucune métrique annuelle disponible.")
        return

    countries = sorted(annual["country"].unique())
    selected = st.multiselect("Pays", countries, default=countries)

    assumptions = assumptions_editor()

    if st.button("Exécuter Q2", type="primary"):
        run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        res = run_q2(annual, assumptions, {"countries": selected}, run_id)
        export_module_result(res)

        slopes = res.tables["Q2_country_slopes"]
        drivers = res.tables["Q2_driver_correlations"]

        st.dataframe(slopes, use_container_width=True)
        if not slopes.empty:
            fig = px.bar(slopes, x="country", y="slope", color="tech", barmode="group")
            st.plotly_chart(fig, use_container_width=True)

        st.dataframe(drivers, use_container_width=True)
        st.markdown(res.narrative_md)
        st.dataframe(res.checks, use_container_width=True)
