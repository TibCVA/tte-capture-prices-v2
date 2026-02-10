from __future__ import annotations

from datetime import datetime
from time import perf_counter

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import assumptions_editor_for, country_year_selector, load_annual_metrics, load_hourly_safe
from app.ui_components import guided_header, inject_theme, show_checks_summary, show_definitions, show_kpi_cards, show_limitations
from src.modules.q4_bess import Q4_PARAMS, run_q4
from src.modules.result import export_module_result


RESULT_KEY = "q4_last_result"
DEFAULT_POWER_GRID = [0.0, 200.0, 500.0, 1000.0, 2000.0, 4000.0, 6000.0, 8000.0]
DEFAULT_DURATION_GRID = [1.0, 2.0, 4.0, 6.0, 8.0, 10.0]


def _mode_label(mode: str) -> str:
    return {
        "SURPLUS_FIRST": "Vue systeme (surplus d'abord)",
        "PRICE_ARBITRAGE_SIMPLE": "Vue actif BESS (arbitrage simple)",
        "PV_COLOCATED": "Vue actif PV+Storage (co-localise)",
    }.get(mode, mode)


def render() -> None:
    inject_theme()
    guided_header(
        title="Q4 - Batteries: ordres de grandeur et impact",
        purpose="Estimer le niveau de stockage necessaire et son impact sur les indicateurs systeme et valeur PV.",
        step_now="Q4: quantifier l'effet BESS",
        step_next="Q5: tester l'impact CO2/gaz sur l'ancre thermique",
    )

    st.markdown("## Question business")
    st.markdown("Quel niveau de batteries (avec solaire) permet de stopper la degradation et sous quelles conditions ?")

    show_definitions(
        [
            ("Puissance BESS (MW)", "Debit maximal de charge/decharge."),
            ("Energie BESS (MWh)", "Capacite maximale stockable."),
            ("Duree (h)", "Energie / puissance, indicateur de stockage court vs long."),
            ("Price-taker", "La batterie ne modifie pas les prix de marche dans ce module."),
        ]
    )

    country, year = country_year_selector()

    annual = load_annual_metrics()
    annual_row = annual[(annual["country"] == country) & (annual["year"] == year)] if not annual.empty else pd.DataFrame()
    if not annual_row.empty and str(annual_row.iloc[0].get("quality_flag", "OK")) == "FAIL":
        st.error("quality_flag=FAIL pour ce pays/annee. Conclusions bloquees.")
        return

    hourly = load_hourly_safe(country, year)
    if hourly is None or hourly.empty:
        st.info("Construis d'abord la table horaire dans Donnees & Qualite.")
        return

    with st.form("q4_form"):
        dispatch_mode = st.selectbox(
            "Mode d'analyse",
            ["SURPLUS_FIRST", "PRICE_ARBITRAGE_SIMPLE", "PV_COLOCATED"],
            format_func=_mode_label,
        )
        objective = st.selectbox("Objectif sizing", ["FAR_TARGET", "SURPLUS_UNABS_TARGET"])

        with st.expander("Parametres avances (grille complete par defaut)", expanded=False):
            power_grid = st.multiselect("Puissances testees (MW)", DEFAULT_POWER_GRID, default=DEFAULT_POWER_GRID)
            duration_grid = st.multiselect("Durees testees (h)", DEFAULT_DURATION_GRID, default=DEFAULT_DURATION_GRID)
            force_recompute = st.checkbox("Forcer recalcul Q4", value=False)

        run_submit = st.form_submit_button("Executer Q4", type="primary")

    st.markdown("## Hypotheses utilisees")
    assumptions = assumptions_editor_for(Q4_PARAMS, "q4")

    if run_submit:
        run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        progress_bar = st.progress(0)
        progress_text = st.empty()

        def _cb(msg: str, frac: float) -> None:
            progress_text.info(msg)
            progress_bar.progress(min(100, max(0, int(frac * 100))))

        sel = {
            "country": country,
            "year": year,
            "objective": objective,
            "power_grid": power_grid or DEFAULT_POWER_GRID,
            "duration_grid": duration_grid or DEFAULT_DURATION_GRID,
            "force_recompute": force_recompute,
        }

        t0 = perf_counter()
        res = run_q4(
            hourly,
            assumptions,
            sel,
            run_id,
            dispatch_mode=dispatch_mode,
            progress_callback=_cb,
        )
        dt = perf_counter() - t0
        out_dir = export_module_result(res)

        progress_bar.progress(100)
        progress_text.success("Q4 termine")

        st.session_state[RESULT_KEY] = {
            "res": res,
            "runtime_sec": dt,
            "out_dir": str(out_dir),
            "country": country,
            "year": year,
            "mode": dispatch_mode,
        }

    payload = st.session_state.get(RESULT_KEY)
    if not payload:
        return

    res = payload["res"]
    summary = res.tables["Q4_sizing_summary"]
    frontier = res.tables["Q4_bess_frontier"]

    st.markdown("## Tests empiriques")
    with st.expander("Voir details techniques", expanded=False):
        st.dataframe(frontier, use_container_width=True)

    st.markdown("## Resultats et interpretation")
    cache_hit = bool(res.kpis.get("cache_hit", False))
    show_kpi_cards(
        [
            ("Mode", _mode_label(str(payload.get("mode", ""))), "Perspective choisie pour la simulation."),
            ("Temps calcul (s)", f"{payload['runtime_sec']:.2f}", "Temps de calcul de ce run."),
            ("Cache", "HIT" if cache_hit else "MISS", "HIT = resultat charge depuis cache persistant Q4."),
        ]
    )

    st.dataframe(summary, use_container_width=True)

    if not frontier.empty:
        st.plotly_chart(
            px.line(
                frontier.sort_values("required_bess_power_mw"),
                x="required_bess_power_mw",
                y="far_after",
                color="required_bess_duration_h",
                title="Impact systeme: FAR apres vs puissance BESS",
            ),
            use_container_width=True,
        )
        st.plotly_chart(
            px.line(
                frontier.sort_values("required_bess_energy_mwh"),
                x="required_bess_energy_mwh",
                y="surplus_unabs_energy_after",
                color="required_bess_duration_h",
                title="Impact systeme: surplus non absorbe apres vs energie BESS",
            ),
            use_container_width=True,
        )
        st.plotly_chart(
            px.line(
                frontier.sort_values("required_bess_duration_h"),
                x="required_bess_duration_h",
                y="pv_capture_price_after",
                color="required_bess_power_mw",
                title="Impact actif PV: capture price apres vs duree BESS",
            ),
            use_container_width=True,
        )

    if payload.get("mode") == "SURPLUS_FIRST":
        st.info("Lecture systeme: l'objectif principal est la reduction du surplus non absorbe et l'amelioration du FAR.")
    elif payload.get("mode") == "PV_COLOCATED":
        st.info("Lecture actif PV: la batterie charge sur production PV et deplace l'energie vers les heures plus valorisees.")
    else:
        st.info("Lecture actif BESS: l'arbitrage simple donne un ordre de grandeur du revenu price-taker.")

    st.markdown("### Lecture simple")
    st.markdown(res.narrative_md)

    show_limitations(
        [
            "Le module reste price-taker, sans effet endogene du BESS sur les prix.",
            "Aucune contrainte reseau intra-zone n'est modelisee.",
            "Le dispatch est volontairement simple (pas d'optimiseur MILP).",
            "L'analyse economique complete CAPEX/OPEX est a completer hors Q4 historique.",
        ]
    )

    st.markdown("## Checks & exports")
    show_checks_summary(res.checks)
    if res.warnings:
        st.warning(" | ".join(res.warnings))
    st.code(payload["out_dir"])
