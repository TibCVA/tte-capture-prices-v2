from __future__ import annotations

from time import perf_counter
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import (
    assumptions_editor_for,
    load_annual_metrics,
    load_phase2_assumptions_table,
    load_scenario_annual_metrics_ui,
)
from app.ui_components import guided_header, inject_theme, show_checks_summary, show_definitions, show_kpi_cards, show_limitations
from src.modules.q1_transition import Q1_PARAMS, run_q1
from src.modules.result import export_module_result


RESULT_KEY = "q1_last_result"


def render() -> None:
    inject_theme()
    guided_header(
        title="Q1 - Passage Phase 1 vers Phase 2",
        purpose="Identifier l'annee de bascule par pays et expliquer les drivers dominants.",
        step_now="Q1: detecter la bascule",
        step_next="Q2: mesurer la pente post-bascule",
    )

    st.markdown("## Question business")
    st.markdown("Quels parametres expliquent le passage de la phase 1 a la phase 2 ?")

    show_definitions(
        [
            ("SR", "Part d'energie en surplus sur l'annee."),
            ("FAR", "Part du surplus absorbee par la flexibilite."),
            ("IR", "Rigidite du systeme en creux de charge."),
            ("Capture ratio PV vs TTL", "Valeur captee par le PV relative a l'ancre hors surplus."),
        ]
    )

    annual = load_annual_metrics()
    if annual.empty:
        st.info("Aucune metrique annuelle disponible.")
        return

    mode_label = st.selectbox("Mode d'analyse", ["Historique", "Prospectif (Phase 2)"], index=0)
    mode = "SCEN" if mode_label.startswith("Prospectif") else "HIST"
    scenario_id: str | None = None
    annual_source = annual
    if mode == "SCEN":
        try:
            p2 = load_phase2_assumptions_table()
            scenario_ids = sorted(p2["scenario_id"].dropna().astype(str).unique().tolist())
        except Exception:
            scenario_ids = []
        if not scenario_ids:
            st.warning("Aucun scenario_id trouve dans les hypotheses Phase 2.")
            return
        scenario_id = st.selectbox("Scenario ID", scenario_ids)
        annual_source = load_scenario_annual_metrics_ui(scenario_id)
        if annual_source.empty:
            st.info("Aucun resultat prospectif disponible. Lance d'abord la page Scenarios Phase 2.")
            return

    countries = sorted(annual_source["country"].dropna().unique().tolist())
    year_min = int(annual_source["year"].min())
    year_max = int(annual_source["year"].max())

    with st.form("q1_form"):
        selected_countries = st.multiselect("Pays", countries, default=countries)
        years = st.slider("Periode", min_value=year_min, max_value=year_max, value=(year_min, year_max))
        run_submit = st.form_submit_button("Executer Q1", type="primary")

    st.markdown("## Hypotheses utilisees")
    assumptions = assumptions_editor_for(Q1_PARAMS, "q1")

    scoped = annual_source[
        annual_source["country"].isin(selected_countries) & annual_source["year"].between(years[0], years[1])
    ].copy()
    fail_count = int((scoped["quality_flag"] == "FAIL").sum()) if not scoped.empty else 0
    if fail_count > 0:
        st.error(f"{fail_count} ligne(s) quality_flag=FAIL dans la selection. Conclusions bloquees.")

    if run_submit and fail_count == 0 and not scoped.empty:
        run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        sel = {
            "countries": selected_countries,
            "years": list(range(years[0], years[1] + 1)),
            "mode": mode,
            "scenario_id": scenario_id,
            "horizon_year": years[1] if mode == "SCEN" else None,
        }
        t0 = perf_counter()
        res = run_q1(annual_source, assumptions, sel, run_id)
        out_dir = export_module_result(res)
        dt = perf_counter() - t0
        st.session_state[RESULT_KEY] = {"res": res, "runtime_sec": dt, "out_dir": str(out_dir)}

    payload = st.session_state.get(RESULT_KEY)
    if not payload:
        return

    res = payload["res"]
    panel = res.tables["Q1_year_panel"]
    summary = res.tables["Q1_country_summary"]

    st.markdown("## Tests empiriques")
    with st.expander("Voir details techniques", expanded=False):
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

    st.markdown("## Resultats et interpretation")
    show_kpi_cards(
        [
            ("Pays analyses", res.kpis.get("n_countries", 0), "Nombre de pays pris en compte."),
            ("Bascules marche", res.kpis.get("n_bascule_market", 0), "Nombre de pays avec bascule marche detectee."),
            ("Temps calcul (s)", f"{payload['runtime_sec']:.2f}", "Temps de calcul de ce module."),
        ]
    )

    st.dataframe(summary, use_container_width=True)

    if not panel.empty:
        st.plotly_chart(
            px.scatter(panel, x="sr_energy", y="capture_ratio_pv_vs_ttl", color="country", title="Capture ratio PV vs SR"),
            use_container_width=True,
        )
        st.plotly_chart(
            px.scatter(panel, x="sr_hours", y="h_negative_obs", color="country", title="Heures negatives vs SR heures"),
            use_container_width=True,
        )

    st.markdown("### Lecture simple")
    st.markdown(res.narrative_md)

    show_limitations(
        [
            "La bascule reste un diagnostic empirique, pas une preuve causale.",
            "Les seuils et le perimetre must-run influencent le verdict.",
            "Un regime_coherence faible rend l'interpretation plus fragile.",
            "Les conclusions sont bloquees si quality_flag=FAIL.",
        ]
    )

    st.markdown("## Checks & exports")
    show_checks_summary(res.checks)
    if res.warnings:
        st.warning(" | ".join(res.warnings))
    st.code(payload["out_dir"])
