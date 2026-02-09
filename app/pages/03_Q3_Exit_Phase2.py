from __future__ import annotations

from datetime import datetime

import plotly.express as px
import streamlit as st

from app.page_utils import assumptions_editor, load_annual_metrics
from src.modules.q3_exit import run_q3
from src.modules.result import export_module_result
from src.storage import load_hourly


def render() -> None:
    st.title("Q3 — Sortie de Phase 2")
    st.markdown("Détecte la stabilisation/amélioration et calcule des contre-factuels d'inversion.")

    annual = load_annual_metrics()
    if annual.empty:
        st.info("Aucune métrique annuelle disponible.")
        return

    countries = sorted(annual["country"].unique())
    selected = st.multiselect("Pays", countries, default=countries)

    assumptions = assumptions_editor()

    if st.button("Exécuter Q3", type="primary"):
        run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        hourly_map = {}
        for _, row in annual[annual["country"].isin(selected)].iterrows():
            c = row["country"]
            y = int(row["year"])
            try:
                hourly_map[(c, y)] = load_hourly(c, y)
            except Exception:
                continue

        res = run_q3(annual, hourly_map, assumptions, {"countries": selected}, run_id)
        export_module_result(res)

        out = res.tables["Q3_status"]
        st.dataframe(out, use_container_width=True)
        if not out.empty:
            fig = px.scatter(out, x="inversion_k_demand", y="additional_absorbed_needed_TWh_year", color="status", hover_name="country")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(res.narrative_md)
        st.dataframe(res.checks, use_container_width=True)
        st.write(res.warnings)
