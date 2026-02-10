from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import assumptions_editor_for, load_annual_metrics
from src.modules.q5_thermal_anchor import Q5_PARAMS, load_commodity_daily, run_q5
from src.modules.result import export_module_result
from src.storage import load_hourly


def _load_hourly_range(country: str, years: list[int]) -> pd.DataFrame:
    chunks = []
    for y in years:
        try:
            h = load_hourly(country, y)
            h = h.copy()
            h["year"] = y
            chunks.append(h)
        except Exception:
            continue
    if not chunks:
        return pd.DataFrame()
    return pd.concat(chunks, axis=0).sort_index()


def render() -> None:
    st.title("Q5 - Impact CO2 / Gaz sur ancre thermique")

    st.markdown(
        """
## 1) Question business
Mesurer comment CO2 et gaz deplacent l'ancre thermique (TCA) et ce que cela implique pour TTL hors surplus.

### Definitions express
- `TCA`: cout marginal thermique simplifie (fuel/eff + CO2*EF/eff + VOM).
- `TTL`: Q95 du prix sur regimes C/D.
- `alpha`: ecart TTL observe - TCA Q95.
"""
    )

    annual = load_annual_metrics()
    if annual.empty:
        st.info("Aucune metrique annuelle disponible.")
        return

    countries = sorted(annual["country"].dropna().unique().tolist())
    country = st.selectbox("Pays", countries)
    y_min = int(annual["year"].min())
    y_max = int(annual["year"].max())
    year_range = st.slider("Periode historique", min_value=y_min, max_value=y_max, value=(max(y_min, 2021), y_max))

    marginal = st.selectbox("Technologie marginale", ["CCGT", "COAL"])
    ttl_target = st.number_input("TTL cible (EUR/MWh)", value=120.0, step=5.0)

    gas_override_enabled = st.checkbox("Override gas")
    gas_override_val = st.number_input("Gas override EUR/MWh_th", value=40.0, step=1.0) if gas_override_enabled else None
    co2_override_enabled = st.checkbox("Override CO2")
    co2_override_val = st.number_input("CO2 override EUR/t", value=80.0, step=1.0) if co2_override_enabled else None

    st.markdown("## 2) Hypotheses et sources")
    assumptions = assumptions_editor_for(Q5_PARAMS, "q5")

    years = list(range(year_range[0], year_range[1] + 1))
    hourly = _load_hourly_range(country, years)
    if hourly.empty:
        st.info("Donnees horaires absentes pour la periode selectionnee.")
        return

    scoped = annual[(annual["country"] == country) & (annual["year"].isin(years))]
    fail_count = int((scoped["quality_flag"] == "FAIL").sum()) if not scoped.empty else 0
    if fail_count > 0:
        st.error(f"{fail_count} ligne(s) quality_flag=FAIL. Conclusions bloquees.")
        return

    if not st.button("Executer Q5", type="primary"):
        return

    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    commodities = load_commodity_daily()
    res = run_q5(
        hourly_df=hourly,
        assumptions_df=assumptions,
        selection={"country": country, "marginal_tech": marginal},
        run_id=run_id,
        commodity_daily=commodities,
        ttl_target_eur_mwh=ttl_target,
        gas_override_eur_mwh_th=gas_override_val,
        co2_override_eur_t=co2_override_val,
    )
    out_dir = export_module_result(res)

    summary = res.tables["Q5_summary"]

    st.markdown("## 3) Tests empiriques")
    st.dataframe(summary, use_container_width=True)

    st.markdown("## 4) Resultats et interpretation")
    if not summary.empty:
        row = summary.iloc[0]
        st.write(
            f"Sensibilite: +10 EUR/t CO2 -> +{10 * float(row['dTCA_dCO2']):.2f} EUR/MWh ; +10 EUR/MWh_th gaz -> +{10 * float(row['dTCA_dGas']):.2f} EUR/MWh"
        )

        plot_df = pd.DataFrame(
            {
                "variable": ["ttl_obs", "tca_q95", "alpha"],
                "value": [float(row["ttl_obs"]), float(row["tca_q95"]), float(row["alpha"])],
            }
        )
        st.plotly_chart(px.bar(plot_df, x="variable", y="value", title="TTL, TCA Q95 et alpha"), use_container_width=True)

    st.markdown("### Lecture simple")
    st.markdown(res.narrative_md)

    st.markdown("## 5) Limites et risques de lecture")
    st.markdown(
        """
- Resultat en ordre de grandeur, sensible au choix techno marginale.
- Hypothese alpha stable simplifiee.
- Corr faible prix/TCA => conclusion CO2 requise fragile.
- Ne capture pas tous les effets hydro/interconnexions/contraintes reseau.
"""
    )

    st.markdown("## 6) Checks et exports")
    st.dataframe(pd.DataFrame(res.checks), use_container_width=True)
    if res.warnings:
        st.warning(" | ".join(res.warnings))
    st.code(str(out_dir))
