from __future__ import annotations

from datetime import datetime
from time import perf_counter

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import (
    assumptions_editor_for,
    load_annual_metrics,
    load_commodity_daily_ui,
    load_hourly_safe,
    load_phase2_assumptions_table,
    load_scenario_annual_metrics_ui,
    load_scenario_hourly_safe,
)
from app.ui_components import guided_header, inject_theme, show_checks_summary, show_definitions, show_kpi_cards, show_limitations
from src.config_loader import load_countries
from src.modules.q5_thermal_anchor import Q5_PARAMS, run_q5
from src.modules.result import export_module_result


RESULT_KEY = "q5_last_result"


def _load_hourly_range(country: str, years: list[int], scenario_id: str | None = None) -> pd.DataFrame:
    chunks: list[pd.DataFrame] = []
    for y in years:
        h = load_scenario_hourly_safe(scenario_id, country, y) if scenario_id else load_hourly_safe(country, y)
        if h is None or h.empty:
            continue
        hx = h.copy()
        hx["year"] = y
        chunks.append(hx)
    if not chunks:
        return pd.DataFrame()
    return pd.concat(chunks, axis=0).sort_index()


def _commodity_from_phase2(scenario_id: str, country: str, years: list[int]) -> pd.DataFrame | None:
    try:
        p2 = load_phase2_assumptions_table()
    except Exception:
        return None
    scoped = p2[
        (p2["scenario_id"].astype(str) == str(scenario_id))
        & (p2["country"].astype(str) == str(country))
        & (pd.to_numeric(p2["year"], errors="coerce").isin(years))
    ].copy()
    if scoped.empty:
        return None
    rows: list[pd.DataFrame] = []
    for _, row in scoped.iterrows():
        y = int(row["year"])
        idx = pd.date_range(f"{y}-01-01", f"{y}-12-31", freq="D")
        rows.append(
            pd.DataFrame(
                {
                    "date": idx,
                    "gas_price_eur_mwh_th": float(row.get("gas_eur_per_mwh_th", float("nan"))),
                    "co2_price_eur_t": float(row.get("co2_eur_per_t", float("nan"))),
                }
            )
        )
    if not rows:
        return None
    out = pd.concat(rows, ignore_index=True)
    return out.dropna(subset=["gas_price_eur_mwh_th", "co2_price_eur_t"])


def render() -> None:
    inject_theme()
    guided_header(
        title="Q5 - Impact CO2 / Gaz sur ancre thermique",
        purpose="Mesurer comment CO2 et gaz deplacent l'ancre thermique et estimer un CO2 requis pour une cible TTL.",
        step_now="Q5: sensibilite ancre thermique",
        step_next="Conclusions: synthese complete des modules",
    )

    st.markdown("## Question business")
    st.markdown("En quoi le CO2 et le gaz impactent-ils l'ancre thermique et quel CO2 est requis pour remonter le haut de courbe ?")

    show_definitions(
        [
            ("TCA", "Ancre cout thermique simplifiee: fuel/eff + CO2*EF/eff + VOM."),
            ("TTL", "Q95 des prix sur regimes C/D (hors surplus)."),
            ("alpha", "Ecart TTL observe - TCA Q95."),
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
    countries_cfg = load_countries().get("countries", {})

    y_min = int(annual_source["year"].min())
    y_max = int(annual_source["year"].max())

    with st.form("q5_form"):
        country = st.selectbox("Pays", countries)
        year_range = st.slider("Periode historique", min_value=y_min, max_value=y_max, value=(max(y_min, 2021), y_max))
        default_marginal = str(countries_cfg.get(country, {}).get("thermal", {}).get("marginal_tech", "CCGT")).upper()
        marginal = st.selectbox("Technologie marginale", ["CCGT", "COAL"], index=0 if default_marginal == "CCGT" else 1)
        ttl_target = st.number_input("TTL cible (EUR/MWh)", value=120.0, step=5.0)

        gas_override_enabled = st.checkbox("Override gaz")
        gas_override_val = st.number_input("Gaz override (EUR/MWh_th)", value=40.0, step=1.0) if gas_override_enabled else None

        co2_override_enabled = st.checkbox("Override CO2")
        co2_override_val = st.number_input("CO2 override (EUR/t)", value=80.0, step=1.0) if co2_override_enabled else None

        run_submit = st.form_submit_button("Executer Q5", type="primary")

    st.markdown("## Hypotheses utilisees")
    assumptions = assumptions_editor_for(Q5_PARAMS, "q5")

    years = list(range(year_range[0], year_range[1] + 1))
    scoped = annual_source[(annual_source["country"] == country) & (annual_source["year"].isin(years))]
    fail_count = int((scoped["quality_flag"] == "FAIL").sum()) if not scoped.empty else 0
    if fail_count > 0:
        st.error(f"{fail_count} ligne(s) quality_flag=FAIL. Conclusions bloquees.")

    if run_submit and fail_count == 0:
        hourly = _load_hourly_range(country, years, scenario_id=scenario_id if mode == "SCEN" else None)
        if hourly.empty:
            st.info("Donnees horaires absentes pour la periode selectionnee.")
            return

        commodities = _commodity_from_phase2(scenario_id, country, years) if mode == "SCEN" else load_commodity_daily_ui()
        if commodities is None or commodities.empty:
            st.warning("Serie commodities absente ou invalide: Q5 fonctionne en mode desactive avec diagnostics seulement.")

        run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        t0 = perf_counter()
        res = run_q5(
            hourly_df=hourly,
            assumptions_df=assumptions,
            selection={
                "country": country,
                "marginal_tech": marginal,
                "mode": mode,
                "scenario_id": scenario_id,
                "horizon_year": years[-1] if years else None,
            },
            run_id=run_id,
            commodity_daily=commodities,
            ttl_target_eur_mwh=float(ttl_target),
            gas_override_eur_mwh_th=gas_override_val,
            co2_override_eur_t=co2_override_val,
        )
        out_dir = export_module_result(res)
        dt = perf_counter() - t0
        st.session_state[RESULT_KEY] = {"res": res, "runtime_sec": dt, "out_dir": str(out_dir)}

    payload = st.session_state.get(RESULT_KEY)
    if not payload:
        return

    res = payload["res"]
    summary = res.tables["Q5_summary"]

    st.markdown("## Tests empiriques")
    with st.expander("Voir details techniques", expanded=False):
        st.dataframe(summary, use_container_width=True)

    st.markdown("## Resultats et interpretation")
    show_kpi_cards(
        [
            ("TTL observe", f"{res.kpis.get('ttl_obs', float('nan')):.2f}", "Q95 prix sur regimes C/D."),
            ("Corr prix-TCA", f"{res.kpis.get('corr_cd', float('nan')):.3f}", "Cohesion empirique entre prix et ancre thermique."),
            ("Temps calcul (s)", f"{payload['runtime_sec']:.2f}", "Temps de calcul du module."),
        ]
    )

    if not summary.empty:
        row = summary.iloc[0]
        dco2 = float(row.get("dTCA_dCO2", float("nan")))
        dgas = float(row.get("dTCA_dGas", float("nan")) )
        st.info(f"Sensibilite immediate: +10 EUR/t CO2 => +{10*dco2:.2f} EUR/MWh | +10 EUR/MWh_th gaz => +{10*dgas:.2f} EUR/MWh")

        plot_df = pd.DataFrame(
            {
                "variable": ["ttl_obs", "tca_q95", "alpha"],
                "value": [float(row.get("ttl_obs", float("nan"))), float(row.get("tca_q95", float("nan"))), float(row.get("alpha", float("nan")))],
            }
        )
        st.plotly_chart(px.bar(plot_df, x="variable", y="value", title="TTL observe, TCA Q95 et alpha"), use_container_width=True)

    st.markdown("### Lecture simple")
    st.markdown(res.narrative_md)

    show_limitations(
        [
            "Resultat en ordre de grandeur, sensible au choix de techno marginale.",
            "L'hypothese alpha stable simplifie la realite des regimes de prix.",
            "Une corr prix-TCA faible fragilise l'estimation du CO2 requis.",
            "Les effets hydro/interconnexions/contraintes reseau ne sont pas explicitement modeles.",
        ]
    )

    st.markdown("## Checks & exports")
    show_checks_summary(res.checks)
    if res.warnings:
        st.warning(" | ".join(res.warnings))
    st.code(payload["out_dir"])
