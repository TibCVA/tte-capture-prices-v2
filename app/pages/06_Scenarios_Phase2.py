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
from app.ui_components import (
    guided_header,
    inject_theme,
    render_interpretation,
    render_kpi_cards_styled,
    render_plotly_styled,
    render_question_box,
    show_definitions_cards,
)


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
    render_question_box("Que deviennent SR/FAR/IR, regimes, capture ratios et stress prix sous hypotheses 2030/2040 ?")

    show_definitions_cards(
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

    render_kpi_cards_styled(
        [
            {"label": "Lignes annuelles", "value": int(len(annual)), "help": "Nombre de combinaisons pays-annee scenario."},
            {"label": "WARN", "value": n_warn, "help": "Warnings reality checks sur le scenario.", "delta": str(n_warn), "delta_direction": "down" if n_warn > 0 else "neutral"},
            {"label": "ERROR", "value": n_err, "help": "Erreurs hard checks sur le scenario.", "delta": str(n_err), "delta_direction": "down" if n_err > 0 else "neutral"},
            {"label": "h_negative > 0", "value": n_neg, "help": "Presence de prix negatifs projetes."},
        ]
    )

    st.markdown("## Resultats et interpretation")

    st.markdown("### 1) Resultats annuels scenario")
    st.dataframe(annual, use_container_width=True)
    render_interpretation("Chaque ligne est une combinaison pays-annee sous les hypotheses du scenario selectionne.")

    calib_cols = [c for c in annual.columns if c.startswith("calib_")]
    if calib_cols:
        st.markdown("### 2) Parametres de calibration effectivement utilises")
        st.dataframe(annual[["country", "year"] + calib_cols], use_container_width=True)
        render_interpretation("Les parametres de calibration sont derives de l'historique et injectes dans le moteur prospectif.")

    stress_readout = _scenario_stress_readout(annual)
    if not stress_readout.empty:
        st.markdown("### 3) Lecture business du stress prospectif")

        def _color_stress(row: pd.Series) -> list[str]:
            lecture = str(row.get("lecture", ""))
            if "Tension" in lecture:
                return ["background-color: #fef2f2"] * len(row)
            elif "rationnelle" in lecture or "absorbe" in lecture:
                return ["background-color: #f0fdf4"] * len(row)
            else:
                return ["background-color: #fffbeb"] * len(row)

        st.dataframe(stress_readout.style.apply(_color_stress, axis=1), use_container_width=True, hide_index=True)
        render_interpretation(
            "Rouge = tension visible (surplus non absorbe ou prix negatifs). "
            "Vert = situation rationnelle. "
            "Jaune = a verifier."
        )

    if {"country", "year", "capture_ratio_pv_vs_ttl"}.issubset(annual.columns):
        fig = px.line(
            annual.sort_values(["country", "year"]),
            x="year",
            y="capture_ratio_pv_vs_ttl",
            color="country",
            title=f"Capture ratio PV vs TTL ({scenario_id})",
            markers=True,
        )
        fig.update_layout(xaxis_title="Annee", yaxis_title="Capture ratio PV/TTL")
        render_plotly_styled(
            fig,
            "Un capture ratio en baisse signale une cannibalisation croissante. Les pays en dessous de 1.0 subissent une perte de valeur.",
            key="scen_capture_ratio",
        )

    if {"country", "year", "h_negative"}.issubset(annual.columns):
        fig2 = px.bar(
            annual.sort_values(["year", "country"]),
            x="country",
            y="h_negative",
            color="year",
            barmode="group",
            title=f"Heures negatives projetees ({scenario_id})",
        )
        fig2.update_layout(xaxis_title="Pays", yaxis_title="Heures negatives")
        render_plotly_styled(
            fig2,
            "Plus les heures negatives sont elevees, plus le stress de cannibalisation est intense sous ce scenario.",
            key="scen_h_negative",
        )

    if {"country", "year", "h_regime_a"}.issubset(annual.columns):
        fig3 = px.bar(
            annual.sort_values(["year", "country"]),
            x="country",
            y="h_regime_a",
            color="year",
            barmode="group",
            title=f"Heures regime A (surplus non absorbe) ({scenario_id})",
        )
        fig3.update_layout(xaxis_title="Pays", yaxis_title="Heures regime A")
        render_plotly_styled(
            fig3,
            "Le regime A represente les heures de surplus non absorbe. Plus elles sont nombreuses, plus le systeme manque de flexibilite.",
            key="scen_h_regime_a",
        )

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
