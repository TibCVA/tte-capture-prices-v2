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
        run_question_bundle_cached,
    )
except Exception as exc:  # pragma: no cover
    _PAGE_UTILS_IMPORT_ERROR = exc

    def _page_utils_unavailable(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("app.page_utils indisponible (cache/deploiement partiel).")

    assumptions_editor_for = _page_utils_unavailable  # type: ignore[assignment]
    build_bundle_hash = _page_utils_unavailable  # type: ignore[assignment]
    available_phase2_years = _page_utils_unavailable  # type: ignore[assignment]
    default_analysis_scenario_years = _page_utils_unavailable  # type: ignore[assignment]
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
from src.config_loader import load_countries
from app.llm_analysis import render_llm_analysis_section
from src.modules.bundle_result import export_question_bundle
from src.modules.q5_thermal_anchor import Q5_PARAMS
from src.modules.test_registry import get_default_scenarios, get_question_tests


RESULT_KEY = "q5_bundle_result"


def _spec_table() -> pd.DataFrame:
    return pd.DataFrame([s.to_dict() for s in get_question_tests("Q5")])


def render() -> None:
    if _PAGE_UTILS_IMPORT_ERROR is not None:
        st.error("Impossible de charger les utilitaires de page (page_utils).")
        st.code(str(_PAGE_UTILS_IMPORT_ERROR))
        st.info("Action recommandee: Reboot app puis Clear cache sur Streamlit Cloud.")
        return

    inject_theme()
    guided_header(
        title="Q5 - Impact CO2 / Gaz sur ancre thermique",
        purpose="Execution unifiee historique + prospectif sur sensibilites TCA/TTL et CO2 requis.",
        step_now="Q5: executer tests CO2/gaz historique/prospectif",
        step_next="Scenarios et conclusions consolidees",
    )

    st.markdown("## Question business")
    render_question_box("Comment CO2 et gaz deplacent-ils l'ancre thermique, et quel CO2 est requis pour relever le haut de courbe ?")

    show_definitions_cards(
        [
            ("TCA", "Ancre cout thermique simplifiee (gas/eff + CO2*EF/eff + VOM)."),
            ("TTL", "Q95 des prix hors surplus (regimes C/D)."),
            ("alpha", "Ecart entre TTL observe et TCA Q95."),
        ]
    )
    show_metric_explainers_tabbed(
        [
            {
                "metric": "dTCA/dCO2 et dTCA/dGas",
                "definition": "Sensibilites analytiques de l'ancre thermique aux commodites.",
                "formula": "dTCA/dGas = 1/eff ; dTCA/dCO2 = EF/eff",
                "intuition": "Mesure l'effet mecanique des commodites sur l'ancre.",
                "interpretation": "Plus eleve = ancre plus sensible.",
                "limits": "Depend du choix techno marginale.",
                "dependencies": "efficiency, emission factor, VOM.",
            },
            {
                "metric": "CO2 requis",
                "definition": "Prix CO2 implicite pour atteindre un TTL cible.",
                "formula": "resolution ttl_target = alpha + Q95(TCA_scenario)",
                "intuition": "Ordre de grandeur policy/commodites.",
                "interpretation": "Valeur elevee = cible difficile sans autres leviers.",
                "limits": "Suppose alpha relativement stable.",
                "dependencies": "ttl_target, techno marginale, scenario gaz.",
            },
        ],
        title="Comment lire les KPI Q5",
    )

    st.markdown("## Ce que cette execution teste (historique + prospectif)")
    render_spec_table_collapsible(_spec_table())

    annual = load_annual_metrics()
    if annual.empty:
        st.info("Aucune metrique annuelle disponible.")
        return

    countries = sorted(annual["country"].dropna().astype(str).unique().tolist())
    y_min = int(annual["year"].min())
    y_max = int(annual["year"].max())
    countries_cfg = load_countries().get("countries", {})

    st.markdown("## Hypotheses utilisees")
    assumptions_phase1 = assumptions_editor_for(Q5_PARAMS, "q5_bundle")
    assumptions_phase2 = load_phase2_assumptions_table()
    scenario_options = sorted(set(assumptions_phase2["scenario_id"].dropna().astype(str).tolist()))
    scenario_options = sorted(set(scenario_options + ["HIGH_BOTH"]))
    default_scen = [s for s in get_default_scenarios("Q5") if s in scenario_options]
    scenario_year_options = available_phase2_years(assumptions_phase2, scenario_ids=[s for s in scenario_options if s != "HIGH_BOTH"], countries=countries)
    default_scenario_years = default_analysis_scenario_years(scenario_year_options)
    if not scenario_year_options:
        scenario_year_options = default_scenario_years

    with st.form("q5_bundle_form"):
        selected_countries = st.multiselect("Pays", countries, default=["FR"] if "FR" in countries else countries[:1])
        year_range = st.slider("Periode historique", min_value=y_min, max_value=y_max, value=(max(y_min, 2021), y_max))
        use_country_tech = st.checkbox("Utiliser techno marginale par pays (config)", value=True)
        marginal_tech = st.selectbox("Technologie marginale (fallback)", ["CCGT", "COAL"], index=0)
        ttl_target = st.number_input("TTL cible (EUR/MWh)", value=120.0, step=5.0)
        scenario_ids = st.multiselect("Scenarios prospectifs", scenario_options, default=default_scen or scenario_options[:2])
        scenario_years = st.multiselect("Annees prospectives", scenario_year_options, default=default_scenario_years)
        force_recompute = st.checkbox("Forcer recalcul complet (ignore cache bundle)", value=False)
        run_submit = st.form_submit_button("Lancer l'analyse complete Q5", type="primary")

    if run_submit:
        countries_sel = selected_countries or (["FR"] if "FR" in countries else countries[:1])
        tech_map = {
            c: str(countries_cfg.get(c, {}).get("thermal", {}).get("marginal_tech", marginal_tech)).upper()
            for c in countries_sel
        } if use_country_tech else {c: str(marginal_tech).upper() for c in countries_sel}
        selection = {
            "country": countries_sel[0],
            "countries": countries_sel,
            "years": list(range(year_range[0], year_range[1] + 1)),
            "scenario_ids": scenario_ids,
            "scenario_years": scenario_years or default_scenario_years,
            "marginal_tech": str(marginal_tech).upper(),
            "marginal_tech_by_country": tech_map,
            "ttl_target_eur_mwh": float(ttl_target),
        }
        bundle_hash = build_bundle_hash("Q5", selection, assumptions_phase1, assumptions_phase2)
        cache_bust = datetime.utcnow().isoformat() if force_recompute else ""
        with st.spinner("Execution Q5 complete (historique + prospectif) en cours..."):
            bundle = run_question_bundle_cached("Q5", bundle_hash, selection, cache_bust=cache_bust)
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
    hist_summary = bundle.hist_result.tables.get("Q5_summary", pd.DataFrame())
    render_kpi_cards_styled(
        [
            {"label": "Scenarios executes", "value": len(bundle.scen_results), "help": "Nombre de scenarios prospectifs executes."},
            {"label": "Run ID", "value": bundle.run_id, "help": "Identifiant run unifie."},
            {"label": "Pays analyses", "value": len(bundle.selection.get("countries", [])), "help": "Nombre de pays de l'analyse Q5."},
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
        render_interpretation("Les sensibilites sont exploitables si alpha est stable. Verifier la variation de alpha avant de conclure.")

    with tab_hist:
        out = bundle.hist_result.tables.get("Q5_summary", pd.DataFrame())
        if out.empty:
            st.info("Aucun resultat historique Q5.")
        else:
            st.dataframe(out, use_container_width=True)
            dco2 = float(pd.to_numeric(out.get("dTCA_dCO2"), errors="coerce").median())
            dgas = float(pd.to_numeric(out.get("dTCA_dGas"), errors="coerce").median())
            if pd.notna(dco2) and pd.notna(dgas):
                st.info(
                    f"Mediane panel: +10 EUR/t CO2 => +{10*dco2:.2f} EUR/MWh | "
                    f"+10 EUR/MWh_th gaz => +{10*dgas:.2f} EUR/MWh"
                )
            fig_df = out[["country", "ttl_obs", "tca_q95", "alpha"]].melt(
                id_vars=["country"],
                value_vars=["ttl_obs", "tca_q95", "alpha"],
                var_name="variable",
                value_name="value",
            )
            fig = px.bar(fig_df, x="country", y="value", color="variable", barmode="group", title="Historique: TTL, TCA Q95, alpha (par pays)")
            fig.update_layout(xaxis_title="Pays", yaxis_title="EUR/MWh")
            render_plotly_styled(
                fig,
                "TTL = prix observe en queue haute. TCA = ancre theorique. Si alpha est stable, les sensibilites dTCA/dCO2 et dTCA/dGas sont exploitables.",
                key="q5_hist_ttl",
            )

    with tab_scen:
        if not bundle.scen_results:
            st.info("Aucun resultat prospectif disponible.")
        else:
            scen_sel = st.selectbox("Scenario", sorted(bundle.scen_results.keys()), key="q5_bundle_scenario")
            scen_res = bundle.scen_results[scen_sel]
            st.dataframe(scen_res.tables.get("Q5_summary", pd.DataFrame()), use_container_width=True)
            render_interpretation("Les sensibilites prospectives doivent etre comparees aux historiques. Un changement de techno marginale modifie les coefficients.")

    with tab_comp:
        render_hist_scen_comparison(bundle.comparison_table)
        render_interpretation("Les deltas importants entre HIST et SCEN sur alpha ou les sensibilites signalent une evolution du mix marginal.")

    with tab_tech:
        st.markdown("## Checks & exports")
        show_checks_summary(bundle.checks)
        if bundle.warnings:
            st.warning(" | ".join(bundle.warnings))
        st.markdown("### Exports")
        st.code(payload["out_dir"])

    show_limitations(
        [
            "Le pass-through commodites->prix reste imparfait en pratique.",
            "Le choix techno marginale influence fortement l'interpretation.",
            "L'hypothese alpha stable est une simplification explicite.",
            "Les tests NON_TESTABLE sont traces explicitement.",
        ]
    )

    render_llm_analysis_section("Q5", bundle, payload["bundle_hash"])
