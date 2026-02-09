from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import country_year_selector, load_hourly_safe, load_validation_findings, run_pipeline_ui


def render() -> None:
    st.title("Données & Qualité")
    country, year = country_year_selector()

    run_pipeline_ui(country, year)

    df = load_hourly_safe(country, year)
    if df is None:
        st.info("Aucune table horaire disponible pour cette sélection.")
        return

    st.subheader("Completeness")
    completeness = 1.0 - float(df[["q_missing_price", "q_missing_load", "q_missing_generation"]].any(axis=1).mean())
    st.metric("Completeness", f"{100*completeness:.2f}%")
    st.write("load_net_mode:", df["load_net_mode"].iloc[0])

    st.subheader("Prix observé")
    fig_price = px.line(df.reset_index(), x="timestamp_utc", y="price_da_eur_mwh")
    st.plotly_chart(fig_price, use_container_width=True)

    st.subheader("NRL")
    fig_nrl = px.line(df.reset_index(), x="timestamp_utc", y="nrl_mw")
    st.plotly_chart(fig_nrl, use_container_width=True)

    findings = load_validation_findings(country, year)
    st.subheader("Validation findings")
    st.dataframe(findings.head(20), use_container_width=True)
