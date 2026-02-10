from __future__ import annotations

import plotly.express as px
import streamlit as st

from app.page_utils import country_year_selector, load_hourly_safe, load_validation_findings, run_pipeline_ui
from app.ui_components import guided_header, inject_theme, show_definitions, show_kpi_cards


def render() -> None:
    inject_theme()
    guided_header(
        title="Donnees & Qualite",
        purpose="Charger/recalculer un pays-annee et verifier la qualite des donnees avant toute analyse.",
        step_now="Donnees & Qualite: consolider la base",
        step_next="Socle Physique: verifier NRL, surplus et flex",
    )

    st.markdown("## Question business")
    st.markdown("Les donnees sont-elles suffisamment completes et coherentes pour tirer des conclusions ?")

    show_definitions(
        [
            ("Completeness", "Part d'heures sans manque critique (prix/load/generation)."),
            ("Validation findings", "Resultats des checks automatiques PASS/WARN/ERROR."),
            ("Load net mode", "Regle appliquee pour traiter le pompage PSH dans la charge."),
        ]
    )

    country, year = country_year_selector()

    st.markdown("## Hypotheses utilisees")
    st.caption("Le pipeline peut utiliser le cache gele ou forcer un rafraichissement ENTSO-E.")
    run_pipeline_ui(country, year)

    df = load_hourly_safe(country, year)
    if df is None or df.empty:
        st.info("Aucune table horaire disponible pour cette selection.")
        return

    st.markdown("## Tests empiriques")
    missing_any = df[["q_missing_price", "q_missing_load", "q_missing_generation"]].any(axis=1)
    completeness = 1.0 - float(missing_any.mean())
    n_hours = int(len(df))

    load_mode = "n/a"
    if "load_net_mode" in df.columns and not df["load_net_mode"].empty:
        load_mode = str(df["load_net_mode"].iloc[0])

    show_kpi_cards(
        [
            ("Completeness", f"{100*completeness:.2f}%", "Part d'heures sans manque critique."),
            ("Heures", n_hours, "Nombre de lignes horaires presentes."),
            ("Load net mode", load_mode, "Mode de calcul de la charge nette."),
        ]
    )

    st.markdown("## Resultats et interpretation")
    fig_price = px.line(df.reset_index(), x="timestamp_utc", y="price_da_eur_mwh", title="Prix day-ahead (NaN visibles)")
    st.plotly_chart(fig_price, use_container_width=True)

    fig_nrl = px.line(df.reset_index(), x="timestamp_utc", y=["nrl_mw", "surplus_mw"], title="NRL et surplus")
    st.plotly_chart(fig_nrl, use_container_width=True)

    findings = load_validation_findings(country, year)
    st.markdown("### Top findings")
    st.dataframe(findings.head(15), use_container_width=True)

    st.markdown("## Limites")
    st.markdown(
        "- Un pays-annee avec donnees manquantes peut rester lisible mais moins robuste.\n"
        "- Les checks WARN n'invalident pas automatiquement l'analyse mais exigent prudence.\n"
        "- Les modules Q1..Q5 doivent etre lances seulement apres verification qualite."
    )

    st.markdown("## Checks & exports")
    if findings.empty:
        st.info("Aucun finding disponible pour cette selection.")
    else:
        st.caption("Les findings complets sont exportes dans `data/metrics/validation_findings.parquet`.")
        with st.expander("Voir details techniques", expanded=False):
            st.dataframe(findings, use_container_width=True)
