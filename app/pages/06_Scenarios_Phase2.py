from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

_PAGE_UTILS_IMPORT_ERROR: Exception | None = None
try:
    from app.page_utils import (
        load_phase2_assumptions_table,
        load_scenario_annual_metrics_ui,
        load_scenario_validation_findings_ui,
        phase2_assumptions_editor,
        run_phase2_scenario_ui,
    )
except Exception as exc:  # pragma: no cover - defensive for Streamlit cloud stale caches
    _PAGE_UTILS_IMPORT_ERROR = exc

    def _page_utils_unavailable(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(
            "app.page_utils indisponible sur cette instance (cache/deploiement partiel). "
            "Rebooter l'app puis vider le cache Streamlit Cloud."
        )

    load_phase2_assumptions_table = _page_utils_unavailable  # type: ignore[assignment]
    load_scenario_annual_metrics_ui = _page_utils_unavailable  # type: ignore[assignment]
    load_scenario_validation_findings_ui = _page_utils_unavailable  # type: ignore[assignment]
    phase2_assumptions_editor = _page_utils_unavailable  # type: ignore[assignment]
    run_phase2_scenario_ui = _page_utils_unavailable  # type: ignore[assignment]
from app.ui_components import guided_header, inject_theme, show_definitions, show_kpi_cards


def _safe_list(series: pd.Series) -> list[str]:
    return sorted(series.dropna().astype(str).unique().tolist())


def _scenario_stress_readout(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    rows: list[dict[str, object]] = []
    for _, r in df.iterrows():
        h_neg = float(pd.to_numeric(pd.Series([r.get("h_negative")]), errors="coerce").fillna(0.0).iloc[0])
        h_a = float(pd.to_numeric(pd.Series([r.get("h_regime_a")]), errors="coerce").fillna(0.0).iloc[0])
        sr = float(pd.to_numeric(pd.Series([r.get("sr_energy")]), errors="coerce").fillna(0.0).iloc[0])
        far = float(pd.to_numeric(pd.Series([r.get("far_energy")]), errors="coerce").fillna(float("nan")).iloc[0])

        if h_neg > 0 or h_a > 0:
            lecture = "Tension visible: surplus non absorbe detecte ou prix negatifs presents"
        elif sr <= 0.0001:
            lecture = "Peu de surplus projete: absence d'heures negatives potentiellement rationnelle"
        elif pd.notna(far) and far >= 0.98:
            lecture = "Surplus projete mais quasi entierement absorbe: negatives limitees"
        else:
            lecture = "Resultat a verifier: surplus present sans signal prix attendu"

        rows.append(
            {
                "country": r.get("country"),
                "year": int(r.get("year")),
                "h_negative": int(h_neg),
                "h_regime_a": int(h_a),
                "sr_energy": sr,
                "far_energy": far,
                "lecture": lecture,
            }
        )
    return pd.DataFrame(rows)


def render() -> None:
    if _PAGE_UTILS_IMPORT_ERROR is not None:
        st.error("Impossible de charger les utilitaires de page (page_utils).")
        st.code(str(_PAGE_UTILS_IMPORT_ERROR))
        st.info("Action recommandee: Streamlit Cloud > Manage app > Reboot app, puis Clear cache.")
        return

    inject_theme()
    guided_header(
        title="Scenarios Phase 2",
        purpose="Construire, executer et auditer les trajectoires prospectives sur le meme socle physique que l'historique.",
        step_now="Scenarios: executer et diagnostiquer le prospectif",
        step_next="Q1..Q5: analyser historique + prospectif en run unifie",
    )

    st.markdown("## Question business")
    st.markdown("Que deviennent SR/FAR/IR, regimes, capture ratios et stress prix sous hypotheses 2030/2040 ?")

    show_definitions(
        [
            ("Mode SCEN", "Calcul prospectif mecaniste, sans optimisation d'equilibre de marche."),
            ("Scenario ID", "Identifiant unique d'un jeu d'hypotheses scenario x pays x annee."),
            ("Calibration historique", "Parametres derives des observations (must-run, flex, coincidence, prix regime B)."),
            ("Comparabilite", "Les KPI sont calcules avec les memes formules qu'en historique."),
        ]
    )

    assumptions = phase2_assumptions_editor("phase2_page")
    if assumptions.empty:
        st.info("Aucune hypothese Phase 2 disponible.")
        return

    st.markdown("## Hypotheses utilisees")
    scenario_ids = _safe_list(assumptions["scenario_id"])
    countries = _safe_list(assumptions["country"])
    years = sorted(pd.to_numeric(assumptions["year"], errors="coerce").dropna().astype(int).unique().tolist())

    col1, col2, col3 = st.columns(3)
    with col1:
        scenario_id = st.selectbox("Scenario ID", scenario_ids)
    with col2:
        selected_countries = st.multiselect("Pays", countries, default=countries)
    with col3:
        selected_years = st.multiselect("Annees", years, default=years)

    run_res = run_phase2_scenario_ui(scenario_id, selected_countries, selected_years)
    if run_res is not None:
        st.session_state["phase2_last_run"] = {
            "scenario_id": scenario_id,
            "countries": selected_countries,
            "years": selected_years,
            "run_ts": datetime.utcnow().isoformat(),
        }
        with st.expander("Details execution scenario", expanded=False):
            st.json(run_res)

    st.markdown("## Tests empiriques")
    annual = load_scenario_annual_metrics_ui(scenario_id)
    if annual.empty:
        st.info("Aucun resultat prospectif trouve. Lance le scenario ci-dessus.")
        return

    annual = annual[annual["country"].isin(selected_countries) & annual["year"].isin(selected_years)].copy()
    findings = load_scenario_validation_findings_ui(scenario_id)
    if not findings.empty:
        findings = findings[findings["country"].isin(selected_countries) & findings["year"].isin(selected_years)].copy()

    n_warn = int((findings.get("severity") == "WARN").sum()) if not findings.empty else 0
    n_err = int((findings.get("severity") == "ERROR").sum()) if not findings.empty else 0
    n_neg = int((pd.to_numeric(annual.get("h_negative"), errors="coerce") > 0).sum())
    n_a = int((pd.to_numeric(annual.get("h_regime_a"), errors="coerce") > 0).sum()) if "h_regime_a" in annual.columns else 0

    show_kpi_cards(
        [
            ("Lignes annuelles", int(len(annual)), "Nombre de combinaisons pays-annee scenario."),
            ("WARN", n_warn, "Warnings reality checks sur le scenario."),
            ("ERROR", n_err, "Erreurs hard checks sur le scenario."),
            ("Pays-annees avec h_negative>0", n_neg, "Presence de prix negatifs projetes."),
            ("Pays-annees avec regime A", n_a, "Surplus non absorbe detecte."),
        ]
    )

    st.markdown("## Resultats et interpretation")

    st.markdown("### 1) Resultats annuels scenario")
    st.dataframe(annual, use_container_width=True)

    calib_cols = [c for c in annual.columns if c.startswith("calib_")]
    if calib_cols:
        st.markdown("### 2) Parametres de calibration effectivement utilises")
        st.dataframe(annual[["country", "year"] + calib_cols], use_container_width=True)

    stress_readout = _scenario_stress_readout(annual)
    if not stress_readout.empty:
        st.markdown("### 3) Lecture business du stress prospectif")
        st.dataframe(stress_readout, use_container_width=True)

    if {"country", "year", "capture_ratio_pv_vs_ttl"}.issubset(annual.columns):
        fig = px.line(
            annual.sort_values(["country", "year"]),
            x="year",
            y="capture_ratio_pv_vs_ttl",
            color="country",
            title=f"Capture ratio PV vs TTL ({scenario_id})",
            markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)

    if {"country", "year", "h_negative"}.issubset(annual.columns):
        fig2 = px.bar(
            annual.sort_values(["year", "country"]),
            x="country",
            y="h_negative",
            color="year",
            barmode="group",
            title=f"Heures negatives projetees ({scenario_id})",
        )
        st.plotly_chart(fig2, use_container_width=True)

    if {"country", "year", "h_regime_a"}.issubset(annual.columns):
        fig3 = px.bar(
            annual.sort_values(["year", "country"]),
            x="country",
            y="h_regime_a",
            color="year",
            barmode="group",
            title=f"Heures regime A (surplus non absorbe) ({scenario_id})",
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("## Limites")
    st.markdown(
        "- Le mode SCEN est mecaniste, pas un modele d'equilibre complet.\n"
        "- Les resultats dependent des hypotheses de must-run, VRE, coincidence export et flex.\n"
        "- Une absence d'heures negatives peut etre rationnelle si SR est tres faible ou FAR proche de 1, mais doit etre explicitee.\n"
        "- Les conclusions restent conditionnelles au perimetre des scenarios et a la qualite des donnees historiques de calibration."
    )

    st.markdown("## Checks & exports")
    if findings.empty:
        st.info("Aucun finding scenario disponible.")
    else:
        st.dataframe(findings, use_container_width=True)
    st.caption(f"Exports scenario: `data/processed/scenario/{scenario_id}/...`")
