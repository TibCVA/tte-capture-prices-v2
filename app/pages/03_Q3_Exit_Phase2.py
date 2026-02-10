from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import (
    assumptions_editor_for,
    build_bundle_hash,
    load_annual_metrics,
    load_phase2_assumptions_table,
    run_question_bundle_cached,
)
from app.ui_components import (
    guided_header,
    inject_theme,
    render_hist_scen_comparison,
    render_robustness_panel,
    render_status_banner,
    render_test_ledger,
    show_checks_summary,
    show_definitions,
    show_kpi_cards,
    show_limitations,
)
from src.modules.bundle_result import export_question_bundle
from src.modules.q3_exit import Q3_PARAMS
from src.modules.test_registry import get_default_scenarios, get_question_tests

try:
    from app.ui_components import show_metric_explainers
except ImportError:  # pragma: no cover
    def show_metric_explainers(*args, **kwargs):  # type: ignore[no-redef]
        return None


RESULT_KEY = "q3_bundle_result"


def _spec_table() -> pd.DataFrame:
    return pd.DataFrame([s.to_dict() for s in get_question_tests("Q3")])


def render() -> None:
    inject_theme()
    guided_header(
        title="Q3 - Sortie de Phase 2 et conditions d'inversion",
        purpose="Execution unifiee historique + prospectif pour tester la transition vers phase 3.",
        step_now="Q3: executer tests de transition historique/prospectif",
        step_next="Q4: quantifier le levier batteries",
    )

    st.markdown("## Question business")
    st.markdown("Quand la phase 2 s'arrete-t-elle, et quels ordres de grandeur permettent d'inverser la trajectoire ?")

    show_definitions(
        [
            ("Tendance", "Pente observee sur fenetre glissante."),
            ("Amelioration", "Baisse des heures negatives avec stabilisation/hausse de capture ratio."),
            ("Contre-factuel", "Test statique pour quantifier un ordre de grandeur."),
        ]
    )
    show_metric_explainers(
        [
            {
                "metric": "trend_h_negative",
                "definition": "Pente du nombre d'heures negatives.",
                "formula": "OLS(h_negative ~ year)",
                "intuition": "Mesure l'aggravation ou l'amelioration du stress prix.",
                "interpretation": "Negatif = tendance vers stabilisation/amelioration.",
                "limits": "Sensible a la longueur de fenetre et aux outliers.",
                "dependencies": "qualite prix, fenetre, filtre stage2.",
            },
            {
                "metric": "inversion_k_demand / inversion_r_mustrun",
                "definition": "Levier minimal de demande ou de rigidite pour atteindre la cible.",
                "formula": "Recherche binaire sur k et r",
                "intuition": "Quantifie la difficulte relative des leviers.",
                "interpretation": "Valeurs elevees = inversion difficile avec ce levier seul.",
                "limits": "Contre-factuel statique, non trajectoire complete.",
                "dependencies": "annee reference, cibles SR/FAR, profils horaires.",
            },
        ],
        title="Comment lire les KPI Q3",
    )

    st.markdown("## Ce que cette execution teste (historique + prospectif)")
    st.dataframe(
        _spec_table()[["test_id", "mode", "title", "what_is_tested", "metric_rule", "source_ref"]],
        use_container_width=True,
    )

    annual = load_annual_metrics()
    if annual.empty:
        st.info("Aucune metrique annuelle disponible.")
        return

    countries = sorted(annual["country"].dropna().astype(str).unique().tolist())
    year_min = int(annual["year"].min())
    year_max = int(annual["year"].max())

    st.markdown("## Hypotheses utilisees")
    assumptions_phase1 = assumptions_editor_for(Q3_PARAMS, "q3_bundle")
    assumptions_phase2 = load_phase2_assumptions_table()
    scenario_options = sorted(set(assumptions_phase2["scenario_id"].dropna().astype(str).tolist()))
    default_scen = [s for s in get_default_scenarios("Q3") if s in scenario_options]

    with st.form("q3_bundle_form"):
        selected = st.multiselect("Pays", countries, default=countries)
        years = st.slider("Periode historique", min_value=year_min, max_value=year_max, value=(year_min, year_max))
        scenario_ids = st.multiselect("Scenarios prospectifs", scenario_options, default=default_scen or scenario_options[:2])
        force_recompute = st.checkbox("Forcer recalcul complet (ignore cache bundle)", value=False)
        run_submit = st.form_submit_button("Lancer l'analyse complete Q3", type="primary")

    if run_submit:
        selection = {
            "countries": selected,
            "years": list(range(years[0], years[1] + 1)),
            "scenario_ids": scenario_ids,
            "scenario_years": [2030, 2040],
        }
        bundle_hash = build_bundle_hash("Q3", selection, assumptions_phase1, assumptions_phase2)
        cache_bust = datetime.utcnow().isoformat() if force_recompute else ""
        with st.spinner("Execution Q3 complete (historique + prospectif) en cours..."):
            bundle = run_question_bundle_cached("Q3", bundle_hash, selection, cache_bust=cache_bust)
        out_dir = export_question_bundle(bundle)
        st.session_state[RESULT_KEY] = {"bundle": bundle, "out_dir": str(out_dir), "bundle_hash": bundle_hash}

    payload = st.session_state.get(RESULT_KEY)
    if not payload:
        return

    bundle = payload["bundle"]
    render_status_banner(bundle.checks)
    st.markdown("## Tests empiriques")
    render_test_ledger(bundle.test_ledger)

    st.markdown("## Resultats synthese")
    out_hist = bundle.hist_result.tables.get("Q3_status", pd.DataFrame())
    show_kpi_cards(
        [
            ("Pays hist", int(out_hist["country"].nunique()) if not out_hist.empty else 0, "Pays avec statut historique."),
            ("Scenarios executes", len(bundle.scen_results), "Nombre de scenarios prospectifs executes."),
            ("Run ID", bundle.run_id, "Identifiant run unifie."),
        ]
    )

    tab_syn, tab_hist, tab_scen, tab_comp, tab_tech = st.tabs(
        ["Synthese", "Historique", "Prospectif", "Comparaison", "Details techniques"]
    )

    with tab_syn:
        st.markdown(bundle.narrative_md)
        render_robustness_panel(bundle.test_ledger)
        if not out_hist.empty:
            st.dataframe(out_hist, use_container_width=True)

    with tab_hist:
        out = bundle.hist_result.tables.get("Q3_status", pd.DataFrame())
        if out.empty:
            st.info("Aucun resultat historique Q3.")
        else:
            st.dataframe(out, use_container_width=True)
            st.plotly_chart(
                px.scatter(
                    out,
                    x="inversion_k_demand",
                    y="inversion_r_mustrun",
                    color="status",
                    hover_name="country",
                    title="Historique: demande vs reduction must-run pour inversion",
                ),
                use_container_width=True,
            )
            st.plotly_chart(
                px.bar(
                    out.sort_values("additional_absorbed_needed_TWh_year", ascending=False),
                    x="country",
                    y="additional_absorbed_needed_TWh_year",
                    color="status",
                    title="Historique: flex additionnelle requise (TWh/an)",
                ),
                use_container_width=True,
            )

    with tab_scen:
        if not bundle.scen_results:
            st.info("Aucun resultat prospectif disponible.")
        else:
            scen_sel = st.selectbox("Scenario", sorted(bundle.scen_results.keys()), key="q3_bundle_scenario")
            scen_res = bundle.scen_results[scen_sel]
            st.dataframe(scen_res.tables.get("Q3_status", pd.DataFrame()), use_container_width=True)

    with tab_comp:
        render_hist_scen_comparison(bundle.comparison_table)

    with tab_tech:
        st.markdown("### Checks")
        show_checks_summary(bundle.checks)
        if bundle.warnings:
            st.warning(" | ".join(bundle.warnings))
        st.markdown("### Exports")
        st.code(payload["out_dir"])

    show_limitations(
        [
            "Les contre-factuels Q3 sont statiques et non une trajectoire d'investissement complete.",
            "La transition phase 3 est une signature empirique multi-indicateurs.",
            "Les scenarios prospectifs simplifient les interactions marche-reseau.",
            "Les tests NON_TESTABLE sont explicites et traceables.",
        ]
    )

    st.markdown("## Checks & exports")
    show_checks_summary(bundle.checks)
    st.code(payload["out_dir"])
