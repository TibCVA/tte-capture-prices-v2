from __future__ import annotations

import plotly.express as px
import streamlit as st

from app.page_utils import country_year_selector, load_hourly_safe


def render() -> None:
    st.title("Socle Physique")
    country, year = country_year_selector()
    df = load_hourly_safe(country, year)
    if df is None:
        st.info("Aucune table horaire disponible.")
        return

    st.markdown("**Definitions express**: NRL, Surplus, Flex, Regimes A/B/C/D")

    view = df.reset_index().tail(48)
    fig1 = px.line(view, x="timestamp_utc", y=["nrl_mw", "surplus_mw", "flex_effective_mw"])
    st.plotly_chart(fig1, use_container_width=True)

    reg = df["regime"].value_counts().rename_axis("regime").reset_index(name="hours")
    fig2 = px.bar(reg, x="regime", y="hours")
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(df[["nrl_mw", "surplus_mw", "surplus_unabsorbed_mw", "regime"]].head(24), use_container_width=True)
