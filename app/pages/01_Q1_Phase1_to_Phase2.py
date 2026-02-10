from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import assumptions_editor_for, load_annual_metrics
from src.modules.q1_transition import Q1_PARAMS, run_q1
from src.modules.result import export_module_result


def _definitions_block() -> None:
    st.markdown("""
### Definitions express
- `SR`: part d'energie en surplus sur l'annee.
- `FAR`: part du surplus absorbee par la flex observee.
- `IR`: rigidite du systeme en creux de charge.
- `TTL`: queue haute des prix hors surplus (regimes C/D).
- `Capture ratio PV vs TTL`: valeur captee PV relative a l'ancre hors surplus.
""")


def render() -> None:
    st.title("Q1 - Passage Phase 1 -> Phase 2")

    st.markdown("""
## 1) Question business
Identifier quand la bascule vers Phase 2 se produit, avec un diagnostic marche et un diagnostic physique.
""")

    _definitions_block()

    annual = load_annual_metrics()
    if annual.empty:
        st.info("Aucune metrique annuelle disponible.")
        return

    countries = sorted(annual["country"].dropna().unique().tolist())
    selected_countries = st.multiselect("Pays", countries, default=countries)
    year_min = int(annual["year"].min())
    year_max = int(annual["year"].max())
    years = st.slider("Annees", min_value=year_min, max_value=year_max, value=(year_min, year_max))

    st.markdown("## 2) Hypotheses et sources")
    assumptions = assumptions_editor_for(Q1_PARAMS, "q1")

    scoped = annual[
        annual["country"].isin(selected_countries) & annual["year"].between(years[0], years[1])
    ].copy()
    fail_count = int((scoped["quality_flag"] == "FAIL").sum()) if not scoped.empty else 0
    if fail_count > 0:
        st.error(
            f"{fail_count} ligne(s) quality_flag=FAIL dans la selection. Conclusions bloquees tant que ces donnees ne sont pas corrigees."
        )

    run_clicked = st.button("Executer Q1", type="primary", disabled=scoped.empty or fail_count > 0)
    if not run_clicked:
        return

    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    sel = {
        "countries": selected_countries,
        "years": list(range(years[0], years[1] + 1)),
    }
    res = run_q1(annual, assumptions, sel, run_id)
    out_dir = export_module_result(res)

    st.markdown("## 3) Tests empiriques")
    panel = res.tables["Q1_year_panel"]
    st.dataframe(
        panel[
            [
                "country",
                "year",
                "phase_market",
                "stress_phys_state",
                "stage2_market_score",
                "flag_h_negative_stage2",
                "flag_capture_stage2",
                "flag_sr_stress",
                "flag_far_tension",
            ]
        ],
        use_container_width=True,
    )

    st.markdown("## 4) Resultats et interpretation")
    summary = res.tables["Q1_country_summary"]
    st.dataframe(summary, use_container_width=True)

    if not panel.empty:
        st.plotly_chart(
            px.scatter(panel, x="sr_energy", y="capture_ratio_pv_vs_ttl", color="country", title="capture_ratio_pv_vs_ttl vs SR"),
            use_container_width=True,
        )
        st.plotly_chart(
            px.scatter(panel, x="sr_hours", y="h_negative_obs", color="country", title="h_negative vs SR_hours"),
            use_container_width=True,
        )
        st.plotly_chart(
            px.scatter(panel, x="sr_energy", y="far_energy", color="h_negative_obs", title="SR vs FAR (couleur=h_negative)"),
            use_container_width=True,
        )
        st.plotly_chart(
            px.scatter(panel, x="ir_p10", y="capture_ratio_pv_vs_ttl", color="sr_energy", title="capture_ratio vs IR (couleur=SR)"),
            use_container_width=True,
        )

    st.markdown("### Lecture simple")
    st.markdown(res.narrative_md)

    st.markdown("## 5) Limites et risques de lecture")
    st.markdown(
        """
- La bascule est un diagnostic empirique, pas une preuve causale.
- Les resultats dependent du perimetre must-run et de la qualite des prix.
- Un regime_coherence faible fragilise l'interpretation causale.
- Les seuils sont parametriques et doivent etre documentes run par run.
"""
    )

    st.markdown("## 6) Checks et exports")
    st.dataframe(pd.DataFrame(res.checks), use_container_width=True)
    if res.warnings:
        st.warning(" | ".join(res.warnings))
    st.code(str(out_dir))
