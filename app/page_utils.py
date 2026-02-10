"""UI helpers for Streamlit pages."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.config_loader import load_countries
from src.pipeline import build_country_year, load_assumptions_table
from src.storage import load_hourly


def country_year_selector(default_country: str = "FR", default_year: int = 2024) -> tuple[str, int]:
    countries_cfg = load_countries()
    country_list = sorted(countries_cfg["countries"].keys())
    c = st.selectbox(
        "Pays",
        country_list,
        index=country_list.index(default_country) if default_country in country_list else 0,
    )
    years = list(range(2018, 2025))
    y = st.selectbox(
        "Annee",
        years,
        index=years.index(default_year) if default_year in years else len(years) - 1,
    )
    return c, y


def run_pipeline_ui(country: str, year: int) -> dict | None:
    col1, col2 = st.columns(2)
    with col1:
        use_cache = st.checkbox("Utiliser cache gele", value=True)
    with col2:
        force_refresh = st.checkbox("Force refresh ENTSO-E", value=False)

    if st.button("Charger / recalculer", type="primary"):
        with st.spinner("Calcul en cours..."):
            res = build_country_year(country, year, force_refresh=force_refresh, use_cache_only=use_cache)
        st.success("Pipeline termine")
        st.write(res)
        return res
    return None


def load_hourly_safe(country: str, year: int) -> pd.DataFrame | None:
    try:
        return load_hourly(country, year)
    except Exception:
        return None


def load_annual_metrics() -> pd.DataFrame:
    p = Path("data/metrics/annual_metrics.parquet")
    if not p.exists():
        return pd.DataFrame()
    return pd.read_parquet(p)


def load_validation_findings(country: str | None = None, year: int | None = None) -> pd.DataFrame:
    p = Path("data/metrics/validation_findings.parquet")
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_parquet(p)
    if country is not None and "country" in df.columns:
        df = df[df["country"] == country]
    if year is not None and "year" in df.columns:
        df = df[df["year"] == year]
    return df


def assumptions_editor() -> pd.DataFrame:
    df = load_assumptions_table()
    st.subheader("Hypotheses Phase 1")
    edited = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    if st.button("Sauvegarder hypotheses"):
        edited.to_csv("data/assumptions/phase1_assumptions.csv", index=False)
        st.success("Hypotheses sauvegardees")
    return edited


def assumptions_editor_for(param_names: list[str], key_prefix: str) -> pd.DataFrame:
    df = load_assumptions_table()
    if df.empty:
        st.warning("Aucune table d'hypotheses disponible.")
        return df

    subset = df[df["param_name"].isin(param_names)].copy()
    st.subheader("Hypotheses utilisees")
    st.caption("Parametres effectivement consommes par ce module.")
    edited_subset = st.data_editor(
        subset,
        num_rows="fixed",
        use_container_width=True,
        key=f"{key_prefix}_assumptions_editor",
    )

    if st.button("Sauvegarder ces hypotheses", key=f"{key_prefix}_save_assumptions"):
        merged = df.set_index("param_name")
        for _, row in edited_subset.iterrows():
            pname = str(row["param_name"])
            if pname in merged.index:
                for col in [
                    "param_group",
                    "param_value",
                    "unit",
                    "description",
                    "source",
                    "last_updated",
                    "owner",
                ]:
                    if col in row:
                        merged.loc[pname, col] = row[col]
        merged_df = merged.reset_index()
        merged_df.to_csv("data/assumptions/phase1_assumptions.csv", index=False)
        st.success("Hypotheses module sauvegardees.")
        return merged_df

    return df
