from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import assumptions_editor_for, country_year_selector, load_annual_metrics
from src.modules.q4_bess import Q4_PARAMS, run_q4
from src.modules.result import export_module_result
from src.storage import load_hourly


def render() -> None:
    st.title("Q4 - Batteries: ordre de grandeur et impact")

    st.markdown(
        """
## 1) Question business
Quantifier le niveau de BESS necessaire pour absorber le surplus et ameliorer les indicateurs de valeur.

### Definitions express
- `Puissance BESS (MW)`: debit max charge/decharge.
- `Energie BESS (MWh)`: capacite totale stockable.
- `Duree (h)`: energie / puissance.
- `Price-taker`: le BESS ne modifie pas les prix du marche.
"""
    )

    country, year = country_year_selector()
    annual = load_annual_metrics()
    annual_row = annual[(annual["country"] == country) & (annual["year"] == year)] if not annual.empty else pd.DataFrame()
    if not annual_row.empty and str(annual_row.iloc[0].get("quality_flag", "OK")) == "FAIL":
        st.error("quality_flag=FAIL pour ce pays/annee. Conclusions bloquees.")
        return

    try:
        hourly = load_hourly(country, year)
    except Exception:
        st.info("Construis d'abord la table horaire dans Donnees & Qualite.")
        return

    dispatch_mode = st.selectbox("Mode dispatch", ["SURPLUS_FIRST", "PRICE_ARBITRAGE_SIMPLE", "PV_COLOCATED"])
    objective = st.selectbox("Objectif sizing", ["FAR_TARGET", "SURPLUS_UNABS_TARGET"])

    st.markdown("## 2) Hypotheses et sources")
    assumptions = assumptions_editor_for(Q4_PARAMS, "q4")

    if not st.button("Executer Q4", type="primary"):
        return

    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    res = run_q4(
        hourly,
        assumptions,
        {"country": country, "year": year, "objective": objective},
        run_id,
        dispatch_mode=dispatch_mode,
    )
    out_dir = export_module_result(res)

    summary = res.tables["Q4_sizing_summary"]
    frontier = res.tables["Q4_bess_frontier"]

    st.markdown("## 3) Tests empiriques")
    st.dataframe(frontier, use_container_width=True)

    st.markdown("## 4) Resultats et interpretation")
    st.dataframe(summary, use_container_width=True)

    if not frontier.empty:
        st.plotly_chart(
            px.line(
                frontier.sort_values("required_bess_power_mw"),
                x="required_bess_power_mw",
                y="far_after",
                color="required_bess_duration_h",
                title="FAR apres vs puissance BESS",
            ),
            use_container_width=True,
        )
        st.plotly_chart(
            px.line(
                frontier.sort_values("required_bess_energy_mwh"),
                x="required_bess_energy_mwh",
                y="surplus_unabs_energy_after",
                color="required_bess_duration_h",
                title="Surplus non absorbe apres vs energie BESS",
            ),
            use_container_width=True,
        )
        st.plotly_chart(
            px.line(
                frontier.sort_values("required_bess_duration_h"),
                x="required_bess_duration_h",
                y="pv_capture_price_after",
                color="required_bess_power_mw",
                title="Capture price PV apres vs duree BESS",
            ),
            use_container_width=True,
        )

    st.markdown("### Lecture simple")
    st.markdown(res.narrative_md)

    st.markdown("## 5) Limites et risques de lecture")
    st.markdown(
        """
- Modele price-taker, sans effet du BESS sur le prix.
- Pas de contraintes reseau intra-zone.
- Dispatch volontairement simple, non MILP.
- Interpretation economique a completer par CAPEX/OPEX hors Q4 historique.
"""
    )

    st.markdown("## 6) Checks et exports")
    st.dataframe(pd.DataFrame(res.checks), use_container_width=True)
    if res.warnings:
        st.warning(" | ".join(res.warnings))
    st.code(str(out_dir))
