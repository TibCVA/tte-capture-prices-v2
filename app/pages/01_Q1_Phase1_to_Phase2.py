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
        default_analysis_scenario_years,
        load_annual_metrics,
        load_phase2_assumptions_table,
        restore_question_payload_from_session_cache,
        run_question_bundle_cached,
    )
except Exception as exc:  # pragma: no cover - defensive for Streamlit cloud stale caches
    _PAGE_UTILS_IMPORT_ERROR = exc

    def _page_utils_unavailable(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(
            "app.page_utils indisponible sur cette instance (cache/deploiement partiel). "
            "Rebooter l'app puis vider le cache Streamlit Cloud."
        )

    assumptions_editor_for = _page_utils_unavailable  # type: ignore[assignment]
    build_bundle_hash = _page_utils_unavailable  # type: ignore[assignment]
    available_phase2_years = _page_utils_unavailable  # type: ignore[assignment]
    default_analysis_scenario_years = _page_utils_unavailable  # type: ignore[assignment]
    load_annual_metrics = _page_utils_unavailable  # type: ignore[assignment]
    load_phase2_assumptions_table = _page_utils_unavailable  # type: ignore[assignment]
    restore_question_payload_from_session_cache = _page_utils_unavailable  # type: ignore[assignment]
    run_question_bundle_cached = _page_utils_unavailable  # type: ignore[assignment]
_UI_COMPONENTS_IMPORT_ERROR: Exception | None = None
try:
    from app.ui_components import (
        guided_header,
        inject_theme,
        render_hist_scen_comparison,
        render_interpretation,
        render_kpi_cards_styled,
        render_livrables_panel,
        render_narrative_styled,
        render_plotly_styled,
        render_question_box,
        render_robustness_panel,
        render_data_quality_panel,
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
except Exception as exc:  # pragma: no cover - defensive for Streamlit cloud stale caches
    _UI_COMPONENTS_IMPORT_ERROR = exc

    def _ui_components_unavailable(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(
            "app.ui_components indisponible sur cette instance (cache/deploiement partiel). "
            "Rebooter l'app puis vider le cache Streamlit Cloud."
        )

    guided_header = _ui_components_unavailable  # type: ignore[assignment]
    inject_theme = _ui_components_unavailable  # type: ignore[assignment]
    render_hist_scen_comparison = _ui_components_unavailable  # type: ignore[assignment]
    render_interpretation = _ui_components_unavailable  # type: ignore[assignment]
    render_kpi_cards_styled = _ui_components_unavailable  # type: ignore[assignment]
    render_livrables_panel = _ui_components_unavailable  # type: ignore[assignment]
    render_narrative_styled = _ui_components_unavailable  # type: ignore[assignment]
    render_plotly_styled = _ui_components_unavailable  # type: ignore[assignment]
    render_question_box = _ui_components_unavailable  # type: ignore[assignment]
    render_robustness_panel = _ui_components_unavailable  # type: ignore[assignment]
    render_data_quality_panel = _ui_components_unavailable  # type: ignore[assignment]
    render_spec_table_collapsible = _ui_components_unavailable  # type: ignore[assignment]
    render_status_banner = _ui_components_unavailable  # type: ignore[assignment]
    render_status_interpretation = _ui_components_unavailable  # type: ignore[assignment]
    render_test_ledger = _ui_components_unavailable  # type: ignore[assignment]
    render_test_ledger_styled = _ui_components_unavailable  # type: ignore[assignment]
    show_checks_summary = _ui_components_unavailable  # type: ignore[assignment]
    show_definitions_cards = _ui_components_unavailable  # type: ignore[assignment]
    show_limitations = _ui_components_unavailable  # type: ignore[assignment]
    show_metric_explainers_tabbed = _ui_components_unavailable  # type: ignore[assignment]
from app.llm_analysis import render_llm_analysis_section
from src.modules.bundle_result import export_question_bundle
from src.modules.q1_transition import Q1_PARAMS
from src.modules.test_registry import get_default_scenarios, get_question_tests


RESULT_KEY = "q1_bundle_result"


def _spec_table() -> pd.DataFrame:
    rows = [s.to_dict() for s in get_question_tests("Q1")]
    return pd.DataFrame(rows)


def render() -> None:
    if _PAGE_UTILS_IMPORT_ERROR is not None:
        st.error("Impossible de charger les utilitaires de page (page_utils).")
        st.code(str(_PAGE_UTILS_IMPORT_ERROR))
        st.info("Action recommandee: Streamlit Cloud > Manage app > Reboot app, puis Clear cache.")
        return
    if _UI_COMPONENTS_IMPORT_ERROR is not None:
        st.error("Impossible de charger les composants UI partages (ui_components).")
        st.code(str(_UI_COMPONENTS_IMPORT_ERROR))
        st.info("Action recommandee: Streamlit Cloud > Manage app > Reboot app, puis Clear cache.")
        return

    inject_theme()
    guided_header(
        title="Q1 - Passage Phase 1 vers Phase 2",
        purpose="Analyse complete historique + prospectif pour detecter la bascule et ses drivers.",
        step_now="Q1: executer tous les tests historique/prospectif",
        step_next="Q2: pente post-bascule avec la meme logique unifiee",
    )

    st.markdown("## Question business")
    render_question_box("Quels parametres expliquent le passage de la phase 1 a la phase 2, historiquement et en projection ?")

    show_definitions_cards(
        [
            ("SR", "Part d'energie en surplus sur l'annee."),
            ("FAR", "Part du surplus absorbee par la flexibilite."),
            ("IR", "Rigidite du systeme en creux de charge."),
            ("Bascule", "Premiere annee ou les signaux phase 2 deviennent structurels."),
        ]
    )
    show_metric_explainers_tabbed(
        [
            {
                "metric": "Stage2 Market Score",
                "definition": "Score de symptomes marche de phase 2.",
                "formula": "Score = familles actives LOW_PRICE + VALUE + PHYSICAL (0..3); stage2_candidate=(score>=2) & quality_ok_data & hors crisis_year explicite",
                "intuition": "Plus le score monte, plus la pression de cannibalisation est visible.",
                "interpretation": "Score eleve + stress physique eleve => bascule robuste.",
                "limits": "Seuils parametriques et non causaux.",
                "dependencies": "qualite data (coverage/unites/bornes), seuils hypotheses, liste explicite des annees de crise.",
            },
            {
                "metric": "Stress physique",
                "definition": "Etat du systeme selon SR/FAR/IR.",
                "formula": "Combinaison de SR, FAR et IR",
                "intuition": "Distingue surplus absorbe vs non absorbe.",
                "interpretation": "Stress eleve avec score marche eleve = bascule plus credibilisee.",
                "limits": "Depend des conventions must-run/flex.",
                "dependencies": "NRL, surplus, exports, PSH, BESS.",
            },
        ],
        title="Comment lire les KPI Q1",
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
    assumptions_phase1 = assumptions_editor_for(Q1_PARAMS, "q1_bundle")
    assumptions_phase2 = load_phase2_assumptions_table()
    scenario_options = sorted(set(assumptions_phase2["scenario_id"].dropna().astype(str).tolist()))
    default_scen = [s for s in get_default_scenarios("Q1") if s in scenario_options]
    scenario_year_options = available_phase2_years(assumptions_phase2, scenario_ids=scenario_options, countries=countries)
    default_scenario_years = default_analysis_scenario_years(scenario_year_options)
    if not scenario_year_options:
        scenario_year_options = default_scenario_years

    with st.form("q1_bundle_form"):
        selected_countries = st.multiselect("Pays", countries, default=countries)
        years = st.slider("Periode historique", min_value=year_min, max_value=year_max, value=(year_min, year_max))
        scenario_ids = st.multiselect("Scenarios prospectifs", scenario_options, default=default_scen or scenario_options[:2])
        scenario_years = st.multiselect("Annees prospectives", scenario_year_options, default=default_scenario_years)
        force_recompute = st.checkbox("Forcer recalcul complet (ignore cache bundle)", value=False)
        run_submit = st.form_submit_button("Lancer l'analyse complete Q1", type="primary")

    if run_submit:
        selection = {
            "countries": selected_countries,
            "years": list(range(years[0], years[1] + 1)),
            "scenario_ids": scenario_ids,
            "scenario_years": scenario_years or default_scenario_years,
        }
        bundle_hash = build_bundle_hash("Q1", selection, assumptions_phase1, assumptions_phase2)
        cache_bust = datetime.utcnow().isoformat() if force_recompute else ""
        with st.spinner("Execution Q1 complete (historique + prospectif) en cours..."):
            bundle = run_question_bundle_cached("Q1", bundle_hash, selection, cache_bust=cache_bust)
        out_dir = export_question_bundle(bundle)
        st.session_state[RESULT_KEY] = {"bundle": bundle, "out_dir": str(out_dir), "bundle_hash": bundle_hash}

    if RESULT_KEY not in st.session_state:
        try:
            restore_question_payload_from_session_cache("Q1", RESULT_KEY)
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
    hist_summary = bundle.hist_result.tables.get("Q1_country_summary", pd.DataFrame())
    render_kpi_cards_styled(
        [
            {"label": "Pays analyses (hist)", "value": int(hist_summary["country"].nunique()) if not hist_summary.empty else 0, "help": "Pays historiques analyses."},
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
        if not hist_summary.empty:
            st.dataframe(hist_summary, use_container_width=True)
        rule_def = bundle.hist_result.tables.get("Q1_rule_definition", pd.DataFrame())
        if not rule_def.empty:
            st.markdown("### Regle de bascule (definition)")
            st.dataframe(rule_def, use_container_width=True)
        before_after = bundle.hist_result.tables.get("Q1_before_after_bascule", pd.DataFrame())
        if not before_after.empty:
            st.markdown("### Avant / apres bascule")
            st.dataframe(before_after, use_container_width=True)
        render_interpretation("La bascule est un diagnostic multi-indicateurs. Un seul signal ne suffit pas a conclure.")

    with tab_hist:
        panel = bundle.hist_result.tables.get("Q1_year_panel", pd.DataFrame())
        if panel.empty:
            st.info("Aucun resultat historique.")
        else:
            st.dataframe(panel, use_container_width=True)
            fig1 = px.scatter(panel, x="sr_energy", y="capture_ratio_pv_vs_ttl", color="country", title="Historique: capture ratio PV vs SR")
            fig1.update_layout(xaxis_title="SR (energie)", yaxis_title="Capture ratio PV/TTL")
            render_plotly_styled(
                fig1,
                "Plus le SR augmente, plus le capture ratio tend a se degrader. Les pays en bas a droite sont les plus avances en phase 2.",
                key="q1_hist_sr_cr",
            )
            fig2 = px.scatter(panel, x="sr_hours", y="h_negative_obs", color="country", title="Historique: heures negatives vs SR heures")
            fig2.update_layout(xaxis_title="SR (heures)", yaxis_title="Heures negatives")
            render_plotly_styled(
                fig2,
                "Un nombre eleve d'heures negatives combine a un SR eleve confirme une cannibalisation structurelle.",
                key="q1_hist_sr_neg",
            )

    with tab_scen:
        if not bundle.scen_results:
            st.info("Aucun resultat prospectif disponible.")
        else:
            scen_sel = st.selectbox("Scenario", sorted(bundle.scen_results.keys()), key="q1_bundle_scenario")
            scen_res = bundle.scen_results[scen_sel]
            st.markdown(f"**Scenario:** `{scen_sel}`")
            st.dataframe(scen_res.tables.get("Q1_country_summary", pd.DataFrame()), use_container_width=True)
            st.dataframe(scen_res.tables.get("Q1_year_panel", pd.DataFrame()), use_container_width=True)
            render_interpretation("Les resultats prospectifs doivent etre lus en comparaison avec l'historique (onglet Comparaison).")

    with tab_comp:
        render_hist_scen_comparison(bundle.comparison_table)
        render_interpretation("Les deltas importants entre HIST et SCEN signalent des evolutions structurelles. Les lignes FRAGILE/NON_TESTABLE invitent a la prudence.")

    with tab_tech:
        st.markdown("## Checks & exports")
        show_checks_summary(bundle.checks)
        rule_apply = bundle.hist_result.tables.get("Q1_rule_application", pd.DataFrame())
        if not rule_apply.empty:
            st.markdown("### Application de la regle par pays-annee")
            st.dataframe(rule_apply, use_container_width=True)
        scope_audit = bundle.hist_result.tables.get("Q1_scope_audit", pd.DataFrame())
        if not scope_audit.empty:
            st.markdown("### Audit de perimetre must-run / NRL")
            st.dataframe(scope_audit, use_container_width=True)
        ir_diag = bundle.hist_result.tables.get("Q1_ir_diagnostics", pd.DataFrame())
        if not ir_diag.empty:
            st.markdown("### Diagnostics IR")
            st.dataframe(ir_diag, use_container_width=True)
        render_data_quality_panel(
            annual_df=annual,
            countries=[str(c) for c in bundle.selection.get("countries", [])],
            years=[int(y) for y in bundle.selection.get("years", [])],
            extra_country_year_df=scope_audit if not scope_audit.empty else None,
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
            "La bascule reste un diagnostic empirique, pas une preuve causale.",
            "Les seuils Q1 influencent le verdict et doivent etre audites.",
            "Les scenarios prospectifs sont mecanistes, pas un modele d'equilibre.",
            "Les tests NON_TESTABLE sont explicites et ne doivent pas etre ignores.",
        ]
    )

    render_llm_analysis_section("Q1", bundle, payload["bundle_hash"])
