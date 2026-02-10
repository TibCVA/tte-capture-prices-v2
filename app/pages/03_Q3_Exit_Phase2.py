from __future__ import annotations

from datetime import datetime
from time import perf_counter

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import (
    assumptions_editor_for,
    collect_hourly_map,
    load_annual_metrics,
    load_phase2_assumptions_table,
    load_scenario_annual_metrics_ui,
)
from app.ui_components import guided_header, inject_theme, show_checks_summary, show_definitions, show_kpi_cards, show_limitations
from src.modules.q3_exit import Q3_PARAMS, run_q3
from src.modules.result import export_module_result


RESULT_KEY = "q3_last_result"


STATUS_LABELS = {
    "degradation": "degradation",
    "stabilisation": "stabilisation",
    "amelioration": "amelioration",
    "transition_partielle": "transition partielle",
    "hors_scope_stage2": "hors scope stage2",
}


def render() -> None:
    inject_theme()
    guided_header(
        title="Q3 - Sortie de Phase 2 et conditions d'inversion",
        purpose="Detecter les signaux de stabilisation et chiffrer les ordres de grandeur pour inverser la tendance.",
        step_now="Q3: analyser la sortie de phase 2",
        step_next="Q4: quantifier le levier batteries",
    )

    st.markdown("## Question business")
    st.markdown("Quand la phase 2 s'arrete-t-elle, et que faudrait-il pour inverser la dynamique ?")

    show_definitions(
        [
            ("Trend", "Pente estimee sur une fenetre glissante de plusieurs annees."),
            ("Amelioration", "Baisse des heures negatives avec stabilisation/hausse du capture ratio."),
            ("Contre-factuel", "Test statique pour evaluer un ordre de grandeur, pas un plan d'investissement."),
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

    with st.form("q3_form"):
        selected = st.multiselect("Pays", countries, default=countries)
        years = st.slider("Periode", min_value=year_min, max_value=year_max, value=(year_min, year_max))
        run_submit = st.form_submit_button("Executer Q3", type="primary")

    st.markdown("## Hypotheses utilisees")
    assumptions = assumptions_editor_for(Q3_PARAMS, "q3")

    scoped = annual_source[annual_source["country"].isin(selected) & annual_source["year"].between(years[0], years[1])].copy()
    fail_count = int((scoped["quality_flag"] == "FAIL").sum()) if not scoped.empty else 0
    if fail_count > 0:
        st.error(f"{fail_count} ligne(s) quality_flag=FAIL. Conclusions bloquees.")

    if run_submit and fail_count == 0 and not scoped.empty:
        run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        t0 = perf_counter()
        years_list = list(range(years[0], years[1] + 1))
        hourly_map = collect_hourly_map(selected, years_list, scenario_id=scenario_id if mode == "SCEN" else None)

        res = run_q3(
            annual_source,
            hourly_map,
            assumptions,
            {
                "countries": selected,
                "years": years_list,
                "mode": mode,
                "scenario_id": scenario_id,
                "horizon_year": years[1],
            },
            run_id,
        )
        out_dir = export_module_result(res)
        dt = perf_counter() - t0
        st.session_state[RESULT_KEY] = {"res": res, "runtime_sec": dt, "out_dir": str(out_dir)}

    payload = st.session_state.get(RESULT_KEY)
    if not payload:
        return

    res = payload["res"]
    out = res.tables["Q3_status"]

    st.markdown("## Tests empiriques")
    with st.expander("Voir details techniques", expanded=False):
        st.dataframe(out, use_container_width=True)

    st.markdown("## Resultats et interpretation")
    show_kpi_cards(
        [
            ("Pays analyses", res.kpis.get("n_countries", 0), "Nombre de pays avec resultat Q3."),
            ("Amelioration", res.kpis.get("n_amelioration", 0), "Pays en amelioration sur la fenetre retenue."),
            ("Temps calcul (s)", f"{payload['runtime_sec']:.2f}", "Temps total de calcul."),
        ]
    )

    if not out.empty:
        d = out.copy()
        d["status_label"] = d["status"].map(STATUS_LABELS).fillna(d["status"])

        st.plotly_chart(
            px.scatter(
                d,
                x="inversion_k_demand",
                y="inversion_r_mustrun",
                color="status_label",
                hover_name="country",
                title="Ordres de grandeur: demande additionnelle vs reduction must-run",
            ),
            use_container_width=True,
        )

        st.plotly_chart(
            px.bar(
                d.sort_values("additional_absorbed_needed_TWh_year", ascending=False),
                x="country",
                y="additional_absorbed_needed_TWh_year",
                color="status_label",
                title="Flex additionnelle requise (TWh/an)",
            ),
            use_container_width=True,
        )

        st.markdown("### Lecture business des statuts")
        for _, row in d.sort_values("country").iterrows():
            st.markdown(
                f"- **{row['country']}**: {row['status_label']} | k_demande={row['inversion_k_demand']:.2%} | r_must-run={row['inversion_r_mustrun']:.2%}"
            )

    st.markdown("### Lecture simple")
    st.markdown(res.narrative_md)

    st.warning("Ces contre-factuels sont statiques et ne representent pas une trajectoire d'investissement complete.")

    show_limitations(
        [
            "Les interactions prix-investissement-reseau ne sont pas modelees.",
            "Les ordres de grandeur dependent de l'annee de reference.",
            "Une serie horaire manquante reduit la couverture Q3.",
            "Les statuts restent sensibles aux seuils de tendance.",
        ]
    )

    st.markdown("## Checks & exports")
    show_checks_summary(res.checks)
    if res.warnings:
        st.warning(" | ".join(res.warnings))
    st.code(payload["out_dir"])
