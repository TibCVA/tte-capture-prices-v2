from __future__ import annotations

from datetime import datetime

import streamlit as st

from app.page_utils import assumptions_editor, country_year_selector
from src.modules.q5_thermal_anchor import load_commodity_daily, run_q5
from src.modules.result import export_module_result
from src.storage import load_hourly


def render() -> None:
    st.title("Q5 — Impact CO2 / Gaz")
    st.markdown("Ancre thermique (TCA), queue haute TTL et CO2 requis pour cible TTL.")

    country, year = country_year_selector()
    try:
        hourly = load_hourly(country, year)
    except Exception:
        st.info("Construis d'abord la table horaire dans Données & Qualité.")
        return

    marginal = st.selectbox("Technologie marginale", ["CCGT", "COAL"])
    ttl_target = st.number_input("TTL cible (EUR/MWh)", value=120.0, step=5.0)
    gas_override = st.checkbox("Override gas")
    gas_override_val = st.number_input("Gas override EUR/MWh_th", value=40.0, step=1.0) if gas_override else None

    assumptions = assumptions_editor()

    if st.button("Exécuter Q5", type="primary"):
        run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        commodities = load_commodity_daily()
        res = run_q5(
            hourly_df=hourly,
            assumptions_df=assumptions,
            selection={"country": country, "year": year, "marginal_tech": marginal},
            run_id=run_id,
            commodity_daily=commodities,
            ttl_target_eur_mwh=ttl_target,
            gas_override_eur_mwh_th=gas_override_val,
        )
        export_module_result(res)
        st.dataframe(res.tables["Q5_summary"], use_container_width=True)
        st.markdown(res.narrative_md)
        st.dataframe(res.checks, use_container_width=True)
        st.write(res.warnings)
