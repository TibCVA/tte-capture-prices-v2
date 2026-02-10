from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

_PAGE_UTILS_IMPORT_ERROR: Exception | None = None
try:
    from app.page_utils import (
        assumptions_editor_for,
        build_bundle_hash,
        load_annual_metrics,
        load_phase2_assumptions_table,
        run_question_bundle_cached,
    )
except Exception as exc:  # pragma: no cover
    _PAGE_UTILS_IMPORT_ERROR = exc

    def _page_utils_unavailable(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("app.page_utils indisponible (cache/deploiement partiel).")

    assumptions_editor_for = _page_utils_unavailable  # type: ignore[assignment]
    build_bundle_hash = _page_utils_unavailable  # type: ignore[assignment]
    load_annual_metrics = _page_utils_unavailable  # type: ignore[assignment]
    load_phase2_assumptions_table = _page_utils_unavailable  # type: ignore[assignment]
    run_question_bundle_cached = _page_utils_unavailable  # type: ignore[assignment]
from app.ui_components import (
    guided_header,
    inject_theme,
    render_hist_scen_comparison,
    render_interpretation,
    render_kpi_cards_styled,
    render_narrative_styled,
    render_plotly_styled,
    render_question_box,
    render_robustness_panel,
    render_spec_table_collapsible,
    render_status_banner,
    render_status_interpretation,
    render_test_ledger,
    render_test_ledger_styled,
    show_checks_summary,
    show_definitions_cards,
    show_limitations,
    show_metric_explainers_tabbed,
)
from src.modules.bundle_result import export_question_bundle
from src.modules.q3_exit import Q3_PARAMS
from src.modules.test_registry import get_default_scenarios, get_question_tests


RESULT_KEY = "q3_bundle_result"


def _spec_table() -> pd.DataFrame:
    return pd.DataFrame([s.to_dict() for s in get_question_tests("Q3")])


def render() -> None:
    if _PAGE_UTILS_IMPORT_ERROR is not None:
        st.error("Impossible de charger les utilitaires de page (page_utils).")
        st.code(str(_PAGE_UTILS_IMPORT_ERROR))
        st.info("Action recommandee: Reboot app puis Clear cache sur Streamlit Cloud.")
        return

    inject_theme()
    guided_header(
        title="Q3 - Sortie de Phase 2 et conditions d'inversion",
        purpose="Execution unifiee historique + prospectif pour tester la transition vers phase 3.",
        step_now="Q3: executer tests de transition historique/prospectif",
        step_next="Q4: quantifier le levier batteries",
    )

    st.markdown("## Question business")
    render_question_box("Quand la phase 2 s'arrete-t-elle, et quels ordres de grandeur permettent d'inverser la trajectoire ?")

    show_definitions_cards(
        [
            ("Tendance", "Pente observee sur fenetre glissante."),
            ("Amelioration", "Baisse des heures negatives avec stabilisation/hausse de capture ratio."),
            ("Contre-factuel", "Test statique pour quantifier un ordre de grandeur."),
        ]
    )
    show_metric_explainers_tabbed(
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
    render_spec_table_collapsible(_spec_table())

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
    render_status_interpretation(bundle.checks)

    st.markdown("## Tests empiriques")
    render_test_ledger(bundle.test_ledger)
    render_test_ledger_styled(bundle.test_ledger)

    st.markdown("## Resultats synthese")
    out_hist = bundle.hist_result.tables.get("Q3_status", pd.DataFrame())
    render_kpi_cards_styled(
        [
            {"label": "Pays hist", "value": int(out_hist["country"].nunique()) if not out_hist.empty else 0, "help": "Pays avec statut historique."},
            {"label": "Scenarios executes", "value": len(bundle.scen_results), "help": "Nombre de scenarios prospectifs executes."},
            {"label": "Run ID", "value": bundle.run_id, "help": "Identifiant run unifie."},
        ]
    )

    tab_syn, tab_hist, tab_scen, tab_comp, tab_tech = st.tabs(
        ["Synthese", "Historique", "Prospectif", "Comparaison", "Details techniques"]
    )

    with tab_syn:
        render_narrative_styled(bundle.narrative_md)
        render_robustness_panel(bundle.test_ledger)
        if not out_hist.empty:
            st.dataframe(out_hist, use_container_width=True)
        render_interpretation("La sortie de phase 2 est un diagnostic multi-leviers. Un seul contre-factuel ne suffit pas a conclure.")

    with tab_hist:
        out = bundle.hist_result.tables.get("Q3_status", pd.DataFrame())
        if out.empty:
            st.info("Aucun resultat historique Q3.")
        else:
            st.dataframe(out, use_container_width=True)
            fig1 = px.scatter(
                out,
                x="inversion_k_demand",
                y="inversion_r_mustrun",
                color="status",
                hover_name="country",
                title="Historique: demande vs reduction must-run pour inversion",
            )
            fig1.update_layout(xaxis_title="k demande (multiplicateur)", yaxis_title="r must-run (reduction)")
            render_plotly_styled(
                fig1,
                "Les pays eloignes de l'origine necessitent des leviers importants. Un pays en haut a droite a besoin de plus de demande ET moins de rigidite.",
                key="q3_hist_inversion",
            )
            fig2 = px.bar(
                out.sort_values("additional_absorbed_needed_TWh_year", ascending=False),
                x="country",
                y="additional_absorbed_needed_TWh_year",
                color="status",
                title="Historique: flex additionnelle requise (TWh/an)",
            )
            fig2.update_layout(xaxis_title="Pays", yaxis_title="TWh/an supplementaires")
            render_plotly_styled(
                fig2,
                "Ampleur de la flexibilite supplementaire necessaire. Les pays en degradation ont les besoins les plus eleves.",
                key="q3_hist_flex",
            )

    with tab_scen:
        if not bundle.scen_results:
            st.info("Aucun resultat prospectif disponible.")
        else:
            scen_sel = st.selectbox("Scenario", sorted(bundle.scen_results.keys()), key="q3_bundle_scenario")
            scen_res = bundle.scen_results[scen_sel]
            st.dataframe(scen_res.tables.get("Q3_status", pd.DataFrame()), use_container_width=True)
            render_interpretation("Les leviers prospectifs doivent etre compares aux leviers historiques pour evaluer la trajectoire.")

    with tab_comp:
        render_hist_scen_comparison(bundle.comparison_table)
        render_interpretation("Des deltas importants entre HIST et SCEN signalent des evolutions structurelles. Les lignes FRAGILE/NON_TESTABLE invitent a la prudence.")

    with tab_tech:
        st.markdown("## Checks & exports")
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
