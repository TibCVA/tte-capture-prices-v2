from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

_PAGE_UTILS_IMPORT_ERROR: Exception | None = None
try:
    from app.page_utils import (
        available_phase2_years,
        assumptions_editor_for,
        build_bundle_hash,
        country_year_selector,
        default_analysis_scenario_years,
        load_annual_metrics,
        load_phase2_assumptions_table,
        restore_question_payload_from_session_cache,
        run_question_bundle_cached,
    )
except Exception as exc:  # pragma: no cover
    _PAGE_UTILS_IMPORT_ERROR = exc

    def _page_utils_unavailable(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("app.page_utils indisponible (cache/deploiement partiel).")

    assumptions_editor_for = _page_utils_unavailable  # type: ignore[assignment]
    build_bundle_hash = _page_utils_unavailable  # type: ignore[assignment]
    available_phase2_years = _page_utils_unavailable  # type: ignore[assignment]
    country_year_selector = _page_utils_unavailable  # type: ignore[assignment]
    default_analysis_scenario_years = _page_utils_unavailable  # type: ignore[assignment]
    load_annual_metrics = _page_utils_unavailable  # type: ignore[assignment]
    load_phase2_assumptions_table = _page_utils_unavailable  # type: ignore[assignment]
    restore_question_payload_from_session_cache = _page_utils_unavailable  # type: ignore[assignment]
    run_question_bundle_cached = _page_utils_unavailable  # type: ignore[assignment]
from app.ui_shims import (
    guided_header,
    inject_theme,
    render_data_quality_panel,
    render_hist_scen_comparison,
    render_interpretation,
    render_kpi_cards_styled,
    render_livrables_panel,
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
from src.config_loader import load_countries
from app.llm_analysis import render_llm_analysis_section
from src.modules.bundle_result import export_question_bundle
from src.modules.q4_bess import Q4_PARAMS
from src.modules.test_registry import get_default_scenarios, get_question_tests


RESULT_KEY = "q4_bundle_result"
DEFAULT_POWER_GRID = [0.0, 200.0, 500.0, 1000.0, 2000.0, 4000.0, 6000.0, 8000.0]
DEFAULT_DURATION_GRID = [1.0, 2.0, 4.0, 6.0, 8.0, 10.0]


def _spec_table() -> pd.DataFrame:
    return pd.DataFrame([s.to_dict() for s in get_question_tests("Q4")])


def render() -> None:
    if _PAGE_UTILS_IMPORT_ERROR is not None:
        st.error("Impossible de charger les utilitaires de page (page_utils).")
        st.code(str(_PAGE_UTILS_IMPORT_ERROR))
        st.info("Action recommandee: Reboot app puis Clear cache sur Streamlit Cloud.")
        return

    inject_theme()
    guided_header(
        title="Q4 - Batteries: ordres de grandeur et impact",
        purpose="Run unifie historique + prospectif avec tests systeme et actif pour le stockage.",
        step_now="Q4: executer tests batteries historique/prospectif",
        step_next="Q5: sensibilite CO2/gaz et ancre thermique",
    )

    st.markdown("## Question business")
    render_question_box("Quel niveau de batteries permet de reduire le stress surplus et d'ameliorer la valeur captee ?")

    show_definitions_cards(
        [
            ("Puissance BESS", "Debut maximal charge/decharge en MW."),
            ("Energie BESS", "Capacite stockable en MWh."),
            ("Duree", "Energie / puissance en heures."),
            ("Price-taker", "Le module Q4 ne reboucle pas le prix sur le dispatch."),
        ]
    )
    show_metric_explainers_tabbed(
        [
            {
                "metric": "FAR avant/apres",
                "definition": "Part du surplus absorbee avant/apres ajout BESS.",
                "formula": "FAR = surplus_absorbed / surplus_total",
                "intuition": "Mesure l'efficacite physique du stockage.",
                "interpretation": "Hausse de FAR = stress surplus mieux absorbe.",
                "limits": "Ne modelise pas effet endogene sur prix.",
                "dependencies": "surplus profile, puissance/energie, dispatch mode.",
            },
            {
                "metric": "Sizing minimal",
                "definition": "Plus petite combinaison puissance/duree atteignant l'objectif.",
                "formula": "Recherche sur grille power x duration",
                "intuition": "Donne un ordre de grandeur actionnable.",
                "interpretation": "Duree >8h => besoin potentiel de stockage long.",
                "limits": "Resolution limitee a la grille testee.",
                "dependencies": "objectif FAR/surplus, grille, mode dispatch.",
            },
        ],
        title="Comment lire les KPI Q4",
    )

    st.markdown("## Ce que cette execution teste (historique + prospectif)")
    render_spec_table_collapsible(_spec_table())

    country_options = sorted(load_countries().get("countries", {}).keys())
    annual = load_annual_metrics()
    default_country = "FR" if "FR" in country_options else (country_options[0] if country_options else "FR")
    year_options = list(range(2018, 2025))

    st.markdown("## Hypotheses utilisees")
    assumptions_phase1 = assumptions_editor_for(Q4_PARAMS, "q4_bundle")
    assumptions_phase2 = load_phase2_assumptions_table()
    scenario_options = sorted(set(assumptions_phase2["scenario_id"].dropna().astype(str).tolist()))
    default_scen = [s for s in get_default_scenarios("Q4") if s in scenario_options]
    scenario_year_options = available_phase2_years(assumptions_phase2, scenario_ids=scenario_options, countries=country_options)
    default_scenario_years = default_analysis_scenario_years(scenario_year_options)
    default_horizon = max(default_scenario_years) if default_scenario_years else max(scenario_year_options) if scenario_year_options else 2035

    with st.form("q4_bundle_form"):
        selected_countries = st.multiselect("Pays", country_options, default=[default_country])
        year = st.selectbox("Annee historique de reference", year_options, index=len(year_options) - 1)
        objective = st.selectbox("Objectif sizing", ["FAR_TARGET", "SURPLUS_UNABS_TARGET"])
        horizon_year = st.selectbox(
            "Horizon prospectif",
            scenario_year_options or [default_horizon],
            index=(scenario_year_options.index(default_horizon) if scenario_year_options and default_horizon in scenario_year_options else 0),
        )
        scenario_ids = st.multiselect("Scenarios prospectifs", scenario_options, default=default_scen or scenario_options[:2])
        with st.expander("Parametres avances (grilles Q4)", expanded=False):
            power_grid = st.multiselect("Puissances (MW)", DEFAULT_POWER_GRID, default=DEFAULT_POWER_GRID)
            duration_grid = st.multiselect("Durees (h)", DEFAULT_DURATION_GRID, default=DEFAULT_DURATION_GRID)
            force_recompute = st.checkbox("Forcer recalcul complet (ignore cache bundle)", value=False)
        run_submit = st.form_submit_button("Lancer l'analyse complete Q4", type="primary")

    if run_submit:
        countries = selected_countries or [default_country]
        selection = {
            "country": countries[0],
            "countries": countries,
            "year": int(year),
            "years": [int(year)],
            "horizon_year": int(horizon_year),
            "scenario_years": [int(horizon_year)],
            "objective": objective,
            "power_grid": power_grid or DEFAULT_POWER_GRID,
            "duration_grid": duration_grid or DEFAULT_DURATION_GRID,
            "scenario_ids": scenario_ids,
        }
        bundle_hash = build_bundle_hash("Q4", selection, assumptions_phase1, assumptions_phase2)
        cache_bust = datetime.utcnow().isoformat() if force_recompute else ""
        with st.spinner("Execution Q4 complete (historique + prospectif) en cours..."):
            bundle = run_question_bundle_cached("Q4", bundle_hash, selection, cache_bust=cache_bust)
        out_dir = export_question_bundle(bundle)
        st.session_state[RESULT_KEY] = {"bundle": bundle, "out_dir": str(out_dir), "bundle_hash": bundle_hash}

    if RESULT_KEY not in st.session_state:
        try:
            restore_question_payload_from_session_cache("Q4", RESULT_KEY)
        except Exception:
            pass
    payload = st.session_state.get(RESULT_KEY)
    if not payload:
        return

    bundle = payload["bundle"]
    if str(payload.get("quality_status", "")).upper() == "FAIL":
        counts = payload.get("check_counts", {})
        fail_codes = payload.get("fail_codes_top5", [])
        fail_count = int(counts.get("FAIL", 0)) if isinstance(counts, dict) else 0
        st.error(f"Analyses chargees malgre checks FAIL. Nombre de FAIL: {fail_count}.")
        if isinstance(fail_codes, list) and fail_codes:
            st.caption("Top FAIL codes: " + ", ".join(str(code) for code in fail_codes))
    render_status_banner(bundle.checks)
    render_status_interpretation(bundle.checks)

    st.markdown("## Tests empiriques")
    render_test_ledger(bundle.test_ledger)
    render_test_ledger_styled(bundle.test_ledger)

    st.markdown("## Resultats synthese")
    hist_summary = bundle.hist_result.tables.get("Q4_sizing_summary", pd.DataFrame())
    render_kpi_cards_styled(
        [
            {"label": "Scenario hist", "value": "SURPLUS_FIRST + 2 modes", "help": "Le run historique inclut aussi PRICE_ARBITRAGE_SIMPLE et PV_COLOCATED."},
            {"label": "Scenarios executes", "value": len(bundle.scen_results), "help": "Nombre de scenarios prospectifs executes."},
            {"label": "Pays analyses", "value": len(bundle.selection.get("countries", [])), "help": "Nombre de pays traites sur cette execution."},
            {"label": "Run ID", "value": bundle.run_id, "help": "Identifiant run unifie."},
        ]
    )

    tab_syn, tab_hist, tab_scen, tab_comp, tab_tech = st.tabs(
        ["Synthese", "Historique", "Prospectif", "Comparaison", "Details techniques"]
    )

    with tab_syn:
        render_narrative_styled(bundle.narrative_md)
        render_robustness_panel(bundle.test_ledger)
        if not hist_summary.empty:
            st.dataframe(hist_summary, use_container_width=True)
        render_interpretation("Le sizing optimal depend du profil de surplus. Un resultat identique pour plusieurs durees signale un plateau d'efficacite.")

    with tab_hist:
        frontier = bundle.hist_result.tables.get("Q4_bess_frontier", pd.DataFrame())
        summary = bundle.hist_result.tables.get("Q4_sizing_summary", pd.DataFrame())
        if summary.empty:
            st.info("Aucun resultat historique Q4.")
        else:
            st.dataframe(summary, use_container_width=True)
        if not frontier.empty:
            st.dataframe(frontier, use_container_width=True)
            fig1 = px.line(frontier.sort_values("required_bess_power_mw"), x="required_bess_power_mw", y="far_after", color="required_bess_duration_h", title="Historique: FAR apres vs puissance")
            fig1.update_layout(xaxis_title="Puissance BESS (MW)", yaxis_title="FAR apres BESS")
            render_plotly_styled(
                fig1,
                "Chaque courbe = une duree de stockage. Le plateau indique le seuil au-dela duquel ajouter de la puissance n'ameliore plus FAR.",
                key="q4_hist_far",
            )
            fig2 = px.line(frontier.sort_values("required_bess_energy_mwh"), x="required_bess_energy_mwh", y="surplus_unabs_energy_after", color="required_bess_duration_h", title="Historique: surplus non absorbe apres vs energie")
            fig2.update_layout(xaxis_title="Energie BESS (MWh)", yaxis_title="Surplus non absorbe (MWh)")
            render_plotly_styled(
                fig2,
                "Capacite en MWh necessaire pour absorber le surplus residuel. Au-dela d'un seuil, le gain marginal diminue.",
                key="q4_hist_surplus",
            )

    with tab_scen:
        if not bundle.scen_results:
            st.info("Aucun resultat prospectif disponible.")
        else:
            scen_sel = st.selectbox("Scenario", sorted(bundle.scen_results.keys()), key="q4_bundle_scenario")
            scen_res = bundle.scen_results[scen_sel]
            st.dataframe(scen_res.tables.get("Q4_sizing_summary", pd.DataFrame()), use_container_width=True)
            st.dataframe(scen_res.tables.get("Q4_bess_frontier", pd.DataFrame()), use_container_width=True)
            render_interpretation("Les besoins prospectifs sont generalement superieurs aux besoins historiques du fait de la penetration VRE accrue.")

    with tab_comp:
        render_hist_scen_comparison(bundle.comparison_table)
        render_interpretation("Les deltas importants entre HIST et SCEN signalent des evolutions structurelles.")

    with tab_tech:
        st.markdown("## Checks & exports")
        show_checks_summary(bundle.checks)
        render_data_quality_panel(
            annual_df=annual,
            countries=[str(c) for c in bundle.selection.get("countries", [])],
            years=[int(y) for y in bundle.selection.get("years", [])],
        )
        render_livrables_panel(
            run_id=bundle.run_id,
            out_dir=payload["out_dir"],
            hist_tables=list(bundle.hist_result.tables.keys()),
            scenario_ids=sorted(bundle.scen_results.keys()),
        )
        if bundle.warnings:
            st.warning(" | ".join(bundle.warnings))

    show_limitations(
        [
            "Q4 reste price-taker: pas de rebouclage endogene des prix.",
            "Les contraintes reseau fines intra-zone ne sont pas modelisees.",
            "Le dispatch est volontairement simple et auditable.",
            "Les tests NON_TESTABLE sont signales explicitement.",
        ]
    )

    render_llm_analysis_section("Q4", bundle, payload["bundle_hash"])
