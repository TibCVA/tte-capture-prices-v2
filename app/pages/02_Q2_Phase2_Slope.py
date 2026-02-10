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
from app.llm_analysis import render_llm_analysis_section
from src.modules.bundle_result import export_question_bundle
from src.modules.q2_slope import Q2_PARAMS
from src.modules.test_registry import get_default_scenarios, get_question_tests


RESULT_KEY = "q2_bundle_result"


def _spec_table() -> pd.DataFrame:
    return pd.DataFrame([s.to_dict() for s in get_question_tests("Q2")])


def render() -> None:
    if _PAGE_UTILS_IMPORT_ERROR is not None:
        st.error("Impossible de charger les utilitaires de page (page_utils).")
        st.code(str(_PAGE_UTILS_IMPORT_ERROR))
        st.info("Action recommandee: Reboot app puis Clear cache sur Streamlit Cloud.")
        return

    inject_theme()
    guided_header(
        title="Q2 - Pente de la Phase 2 et drivers",
        purpose="Execution unifiee historique + prospectif pour mesurer les pentes et leurs drivers.",
        step_now="Q2: executer tous les tests pente",
        step_next="Q3: transition vers phase 3",
    )

    st.markdown("## Question business")
    render_question_box("Quelle est la pente de degradation de la valeur captee, et quels facteurs la pilotent ?")

    show_definitions_cards(
        [
            ("Pente", "Variation du capture ratio avec la penetration."),
            ("R2 / p-value", "Robustesse statistique de la regression lineaire."),
            ("Driver", "Facteur explicatif observe (SR, FAR, IR, corr VRE-load, TTL)."),
        ]
    )
    show_metric_explainers_tabbed(
        [
            {
                "metric": "Slope",
                "definition": "Coefficient de regression du capture ratio sur l'axe choisi.",
                "formula": "y = a + b*x",
                "intuition": "b negatif = cannibalisation qui s'accelere.",
                "interpretation": "Plus b est negatif, plus la pente de phase 2 est forte.",
                "limits": "Descriptif, non causal; sensible au faible n.",
                "dependencies": "bascule Q1, qualite donnees, proxy penetration.",
            },
            {
                "metric": "Robust flag",
                "definition": "Etat robuste/fragile selon nombre de points et fit.",
                "formula": "ROBUST si n>=seuil; sinon FRAGILE",
                "intuition": "Evite la sur-interpretation des regressions courtes.",
                "interpretation": "FRAGILE = conclusion a utiliser avec prudence.",
                "limits": "n suffisant ne garantit pas causalite.",
                "dependencies": "periode, exclusions, disponibilite variables.",
            },
        ],
        title="Comment lire les KPI Q2",
    )

    st.markdown("## Ce que cette execution teste (historique + prospectif)")
    render_spec_table_collapsible(_spec_table())

    annual = load_annual_metrics()
    if annual.empty:
        st.info("Aucune metrique annuelle disponible.")
        return

    countries = sorted(annual["country"].dropna().astype(str).unique().tolist())

    st.markdown("## Hypotheses utilisees")
    assumptions_phase1 = assumptions_editor_for(Q2_PARAMS, "q2_bundle")
    assumptions_phase2 = load_phase2_assumptions_table()
    scenario_options = sorted(set(assumptions_phase2["scenario_id"].dropna().astype(str).tolist()))
    default_scen = [s for s in get_default_scenarios("Q2") if s in scenario_options]

    with st.form("q2_bundle_form"):
        selected = st.multiselect("Pays", countries, default=countries)
        scenario_ids = st.multiselect("Scenarios prospectifs", scenario_options, default=default_scen or scenario_options[:2])
        force_recompute = st.checkbox("Forcer recalcul complet (ignore cache bundle)", value=False)
        run_submit = st.form_submit_button("Lancer l'analyse complete Q2", type="primary")

    if run_submit:
        selection = {
            "countries": selected,
            "years": list(range(2018, 2025)),
            "scenario_ids": scenario_ids,
            "scenario_years": [2030, 2040],
        }
        bundle_hash = build_bundle_hash("Q2", selection, assumptions_phase1, assumptions_phase2)
        cache_bust = datetime.utcnow().isoformat() if force_recompute else ""
        with st.spinner("Execution Q2 complete (historique + prospectif) en cours..."):
            bundle = run_question_bundle_cached("Q2", bundle_hash, selection, cache_bust=cache_bust)
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
    slopes_hist = bundle.hist_result.tables.get("Q2_country_slopes", pd.DataFrame())
    render_kpi_cards_styled(
        [
            {"label": "Pentes hist", "value": int(len(slopes_hist)), "help": "Nombre de regressions historiques calculees."},
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
        if not slopes_hist.empty:
            st.dataframe(slopes_hist, use_container_width=True)
        render_interpretation("Les pentes negatives confirment une cannibalisation active. Verifier la robustesse (R2, n) avant de conclure.")

    with tab_hist:
        slopes = bundle.hist_result.tables.get("Q2_country_slopes", pd.DataFrame())
        drivers = bundle.hist_result.tables.get("Q2_driver_correlations", pd.DataFrame())
        if slopes.empty:
            st.info("Aucun resultat historique Q2.")
        else:
            st.dataframe(slopes, use_container_width=True)
            fig = px.bar(slopes, x="country", y="slope", color="tech", barmode="group", title="Historique: pentes par pays/tech")
            fig.update_layout(xaxis_title="Pays", yaxis_title="Pente (coefficient)")
            render_plotly_styled(
                fig,
                "Les barres negatives indiquent une cannibalisation active. Plus la barre est longue, plus la pente est prononcee.",
                key="q2_hist_slopes",
            )
        if not drivers.empty:
            st.dataframe(drivers, use_container_width=True)
            render_interpretation("Les correlations drivers ne prouvent pas la causalite mais identifient les facteurs associes.")

    with tab_scen:
        if not bundle.scen_results:
            st.info("Aucun resultat prospectif disponible.")
        else:
            scen_sel = st.selectbox("Scenario", sorted(bundle.scen_results.keys()), key="q2_bundle_scenario")
            scen_res = bundle.scen_results[scen_sel]
            st.dataframe(scen_res.tables.get("Q2_country_slopes", pd.DataFrame()), use_container_width=True)
            st.dataframe(scen_res.tables.get("Q2_driver_correlations", pd.DataFrame()), use_container_width=True)
            render_interpretation("Les pentes prospectives prolongent la tendance historique sous hypotheses. Comparer avec l'onglet Comparaison.")

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
            "La pente reste un indicateur empirique, pas une causalite structurelle.",
            "Les regressions fragiles (faible n ou faible fit) doivent etre explicites.",
            "Les scenarios prospectifs simplifient la dynamique d'investissement.",
            "Les tests NON_TESTABLE sont explicitement traces.",
        ]
    )

    render_llm_analysis_section("Q2", bundle, payload["bundle_hash"])
