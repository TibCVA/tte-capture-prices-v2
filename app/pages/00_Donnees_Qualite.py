from __future__ import annotations

import calendar
from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

_PAGE_UTILS_IMPORT_ERROR: Exception | None = None
try:
    from app.page_utils import country_year_selector, load_hourly_safe, load_validation_findings, run_pipeline_ui, to_plot_frame
except Exception as exc:  # pragma: no cover - defensive for Streamlit cloud stale caches
    _PAGE_UTILS_IMPORT_ERROR = exc

    def _page_utils_unavailable(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(
            "app.page_utils indisponible sur cette instance (cache/deploiement partiel). "
            "Rebooter l'app puis vider le cache Streamlit Cloud."
        )

    country_year_selector = _page_utils_unavailable  # type: ignore[assignment]
    load_hourly_safe = _page_utils_unavailable  # type: ignore[assignment]
    load_validation_findings = _page_utils_unavailable  # type: ignore[assignment]
    run_pipeline_ui = _page_utils_unavailable  # type: ignore[assignment]
    to_plot_frame = _page_utils_unavailable  # type: ignore[assignment]
from app.ui_components import (
    apply_tte_template,
    guided_header,
    inject_theme,
    render_interpretation,
    render_kpi_cards_styled,
    render_plotly_styled,
    render_question_box,
    show_definitions_cards,
    show_metric_explainers_tabbed,
)


CRITICAL_COLS = [
    "price_da_eur_mwh",
    "load_mw",
    "gen_vre_mw",
    "gen_must_run_mw",
    "nrl_mw",
    "surplus_mw",
    "regime_phys",
]


def _expected_hours(year: int) -> int:
    return 8784 if calendar.isleap(int(year)) else 8760


def _missing_share(series: pd.Series) -> float:
    if series is None or len(series) == 0:
        return 1.0
    return float(series.isna().mean())


def _quality_decision(
    completeness: float,
    hard_error_count: int,
    continuity_ok: bool,
    duplicate_timestamps: int,
    critical_missing_cols: list[str],
) -> tuple[str, list[str], list[str]]:
    reasons: list[str] = []
    actions: list[str] = []

    if hard_error_count > 0:
        reasons.append(f"{hard_error_count} check(s) ERROR dans validation findings")
        actions.append("Corriger les erreurs du pipeline avant toute conclusion")
    if not continuity_ok:
        reasons.append("Continuite temporelle non conforme (trous ou nombre d'heures incorrect)")
        actions.append("Rebuild du pays-annee et verification timezone/index")
    if duplicate_timestamps > 0:
        reasons.append(f"{duplicate_timestamps} timestamp(s) duplique(s)")
        actions.append("Dedoublonner la serie source puis relancer le pipeline")
    if completeness < 0.98:
        reasons.append(f"Completeness insuffisante ({100*completeness:.2f}% < 98.00%)")
        actions.append("Verifier disponibilite prix/load/generation et completer la source")
    if critical_missing_cols:
        reasons.append("Colonnes critiques manquantes: " + ", ".join(critical_missing_cols))
        actions.append("Verifier le mapping ENTSO-E et les colonnes canoniques du socle")

    if reasons:
        if hard_error_count > 0 or not continuity_ok or duplicate_timestamps > 0:
            return "FAIL", reasons, actions
        return "WARN", reasons, actions

    return "PASS", ["Qualite suffisante pour interpretation business"], ["Vous pouvez passer aux modules Q1..Q5"]


def _findings_error_warn(df_findings: pd.DataFrame) -> tuple[int, int]:
    if df_findings.empty:
        return 0, 0
    sev_col = "severity" if "severity" in df_findings.columns else ("status" if "status" in df_findings.columns else "")
    if not sev_col:
        return 0, 0
    sev = df_findings[sev_col].astype(str).str.upper()
    n_error = int(sev.isin(["ERROR", "FAIL"]).sum())
    n_warn = int(sev.isin(["WARN", "WARNING"]).sum())
    return n_error, n_warn


def render() -> None:
    if _PAGE_UTILS_IMPORT_ERROR is not None:
        st.error("Impossible de charger les utilitaires de page (page_utils).")
        st.code(str(_PAGE_UTILS_IMPORT_ERROR))
        st.info("Action recommandee: Streamlit Cloud > Manage app > Reboot app, puis Clear cache.")
        return

    inject_theme()
    guided_header(
        title="Donnees & Qualite",
        purpose="Diagnostiquer de facon exhaustive la qualite des donnees avant toute analyse historique ou prospective.",
        step_now="Donnees & Qualite: consolider la base",
        step_next="Socle Physique: verifier NRL, surplus et flex",
    )

    st.markdown("## Question business")
    render_question_box("Les donnees sont-elles suffisamment completes, coherentes et auditables pour tirer des conclusions robustes ?")

    show_definitions_cards(
        [
            ("Completeness", "Part d'heures sans manque critique (prix/load/generation)."),
            ("Hard checks", "Invariants physiques/comptables qui ne doivent jamais etre violes."),
            ("Reality checks", "Tests de coherence marche/physique (warnings interpretables)."),
            ("Go/No-Go", "Decision explicite PASS/WARN/FAIL avant d'ouvrir les modules Q1..Q5."),
            ("Load net mode", "Regle appliquee pour traiter le pompage PSH dans la charge."),
        ]
    )
    show_metric_explainers_tabbed(
        [
            {
                "metric": "Completeness",
                "definition": "Part des heures sans manque critique.",
                "formula": "1 - mean(q_missing_price OR q_missing_load OR q_missing_generation)",
                "intuition": "Mesure la fiabilite brute des donnees d'entree.",
                "interpretation": "Sous 98%, les conclusions deviennent fragiles.",
                "limits": "N'indique pas a lui seul la coherence economique.",
                "dependencies": "disponibilite prix/load/gen et pipeline de normalisation.",
            },
            {
                "metric": "Validation findings",
                "definition": "Liste des checks automatiques PASS/WARN/ERROR.",
                "formula": "Evaluation des invariants physiques + reality checks",
                "intuition": "Evite les conclusions sur donnees incoherentes.",
                "interpretation": "ERROR/FAIL = blocage des conclusions analytiques.",
                "limits": "Un WARN peut etre explicable, mais doit etre argumente.",
                "dependencies": "validation_report, quality_flag, coverage horaire.",
            },
        ],
        title="Comment lire les indicateurs qualite",
    )

    st.markdown("### Ce que signifie chaque colonne critique")
    col_explain = pd.DataFrame(
        [
            {"Colonne": "price_da_eur_mwh", "Description": "Prix day-ahead EPEX/marche en EUR/MWh", "Impact si manquant": "Capture prices incalculables"},
            {"Colonne": "load_mw", "Description": "Charge nette du systeme (apres traitement PSH)", "Impact si manquant": "NRL faux, tous les calculs faux"},
            {"Colonne": "gen_vre_mw", "Description": "Generation VRE totale (solaire + eolien)", "Impact si manquant": "Surplus non calculable"},
            {"Colonne": "gen_must_run_mw", "Description": "Generation non-flexible (nucleaire, biomasse, hydro RoR...)", "Impact si manquant": "NRL biaise"},
            {"Colonne": "nrl_mw", "Description": "Net Residual Load = Load - VRE - MustRun", "Impact si manquant": "Pas de classification regimes"},
            {"Colonne": "surplus_mw", "Description": "Surplus physique = max(0, -NRL)", "Impact si manquant": "SR/FAR non calculables"},
            {"Colonne": "regime_phys", "Description": "Regime horaire A/B/C/D (anti-circularite)", "Impact si manquant": "Pas de segmentation physique"},
        ]
    )
    st.dataframe(col_explain, use_container_width=True, hide_index=True)

    country, year = country_year_selector()

    st.markdown("## Hypotheses utilisees")
    st.caption("Le pipeline peut utiliser le cache gele ou forcer un rafraichissement ENTSO-E.")
    run_pipeline_ui(country, year)

    df = load_hourly_safe(country, year)
    if df is None or df.empty:
        st.info("Aucune table horaire disponible pour cette selection.")
        return

    st.markdown("## Tests empiriques")

    missing_cols = [c for c in CRITICAL_COLS if c not in df.columns]
    present_critical = [c for c in CRITICAL_COLS if c in df.columns]

    if {"q_missing_price", "q_missing_load", "q_missing_generation"}.issubset(df.columns):
        missing_any = df[["q_missing_price", "q_missing_load", "q_missing_generation"]].any(axis=1)
        completeness = 1.0 - float(missing_any.mean())
    else:
        if present_critical:
            completeness = 1.0 - float(df[present_critical].isna().any(axis=1).mean())
        else:
            completeness = 0.0

    n_hours = int(len(df))
    expected_hours = _expected_hours(year)

    idx = df.index if isinstance(df.index, pd.DatetimeIndex) else pd.to_datetime(df.get("timestamp_utc"), errors="coerce", utc=True)
    if isinstance(idx, pd.Series):
        idx = pd.DatetimeIndex(idx.dropna())
    duplicate_timestamps = int(idx.duplicated().sum()) if isinstance(idx, pd.DatetimeIndex) else 0
    continuity_ok = bool(n_hours == expected_hours and duplicate_timestamps == 0)

    load_mode = "n/a"
    if "load_net_mode" in df.columns and not df["load_net_mode"].empty:
        load_mode = str(df["load_net_mode"].iloc[0])

    findings = load_validation_findings(country, year)
    n_error, n_warn = _findings_error_warn(findings)

    go_no_go, reasons, actions = _quality_decision(
        completeness=completeness,
        hard_error_count=n_error,
        continuity_ok=continuity_ok,
        duplicate_timestamps=duplicate_timestamps,
        critical_missing_cols=missing_cols,
    )

    compl_direction = "up" if completeness >= 0.98 else "down"
    render_kpi_cards_styled(
        [
            {"label": "Completeness", "value": f"{100*completeness:.2f}%", "help": "Part d'heures sans manque critique.", "delta": ">= 98%" if completeness >= 0.98 else "< 98%", "delta_direction": compl_direction},
            {"label": "Heures observees", "value": n_hours, "help": "Nombre de lignes horaires presentes."},
            {"label": "Heures attendues", "value": expected_hours, "help": "8760 ou 8784 selon annee."},
            {"label": "Load net mode", "value": load_mode, "help": "Mode de calcul de la charge nette."},
        ]
    )

    st.markdown("## Decision Go / No-Go")
    verdict_class = {"PASS": "tte-exec-verdict-pass", "WARN": "tte-exec-verdict-warn", "FAIL": "tte-exec-verdict-fail"}.get(go_no_go, "")
    st.markdown(
        f'<div class="tte-exec-card {verdict_class}">',
        unsafe_allow_html=True,
    )
    if go_no_go == "PASS":
        st.success("PASS - Donnees suffisamment solides pour lancer les analyses Q1..Q5.")
    elif go_no_go == "WARN":
        st.warning("WARN - Analyses possibles mais avec prudence et justification explicite.")
    else:
        st.error("FAIL - Ne pas conclure tant que les erreurs critiques ne sont pas corrigees.")

    st.markdown("**Raisons**")
    for r in reasons:
        st.markdown(f"- {r}")
    st.markdown("**Actions correctives recommandees**")
    for a in actions:
        st.markdown(f"- {a}")
    st.markdown("</div>", unsafe_allow_html=True)

    render_interpretation(
        f"Verdict: **{go_no_go}**. "
        + ("Les donnees sont exploitables. " if go_no_go == "PASS" else "")
        + ("Prudence requise sur les conclusions. " if go_no_go == "WARN" else "")
        + ("Blocage: corriger les erreurs avant toute analyse. " if go_no_go == "FAIL" else "")
        + f"Completeness: {100*completeness:.2f}%, heures: {n_hours}/{expected_hours}."
    )

    st.markdown("## Resultats et interpretation")

    quality_rows: list[dict[str, Any]] = []
    for col in CRITICAL_COLS:
        if col in df.columns:
            miss = _missing_share(df[col])
            quality_rows.append(
                {
                    "colonne": col,
                    "presente": True,
                    "missing_share_pct": round(100.0 * miss, 4),
                    "statut": "OK" if miss <= 0.02 else "WARN",
                }
            )
        else:
            quality_rows.append(
                {
                    "colonne": col,
                    "presente": False,
                    "missing_share_pct": 100.0,
                    "statut": "FAIL",
                }
            )
    quality_matrix = pd.DataFrame(quality_rows)

    st.markdown("### Matrice de qualite des colonnes critiques")

    def _color_quality(row: pd.Series) -> list[str]:
        status = str(row.get("statut", "")).upper()
        color_map = {"OK": "#f0fdf4", "WARN": "#fffbeb", "FAIL": "#fef2f2"}
        bg = color_map.get(status, "")
        return [f"background-color: {bg}" if bg else "" for _ in row]

    st.dataframe(quality_matrix.style.apply(_color_quality, axis=1), use_container_width=True, hide_index=True)
    render_interpretation(
        "OK = colonne presente avec moins de 2% de manques. WARN = taux de manques eleve. FAIL = colonne absente."
    )

    plot_df = to_plot_frame(df)
    fig_price = px.line(plot_df, x="timestamp_utc", y="price_da_eur_mwh", title="Prix day-ahead (NaN visibles)")
    fig_price.update_layout(xaxis_title="Date/heure UTC", yaxis_title="EUR/MWh")
    render_plotly_styled(
        fig_price,
        "Les trous (NaN) sont visibles directement sur le graphe. Des discontinuites importantes signalent un probleme de source.",
        key="donnees_price",
    )

    fig_nrl = px.line(plot_df, x="timestamp_utc", y=["nrl_mw", "surplus_mw"], title="NRL et surplus")
    fig_nrl.update_layout(xaxis_title="Date/heure UTC", yaxis_title="MW")
    render_plotly_styled(
        fig_nrl,
        "NRL negatif = surplus. Les periodes ou surplus_mw est eleve correspondent aux heures de pression VRE maximale.",
        key="donnees_nrl",
    )

    st.markdown("### Findings automatiques")
    if findings.empty:
        st.info("Aucun finding disponible pour cette selection.")
    else:
        st.dataframe(findings.head(20), use_container_width=True)

    st.markdown("## Limites")
    st.markdown(
        "- Une bonne completeness n'exclut pas tous les biais de mapping techno.\n"
        "- Certains reality checks WARN peuvent etre rationnels dans des cas systeme atypiques.\n"
        "- Les analyses prospectives restent conditionnelles aux hypotheses scenario."
    )

    st.markdown("## Checks & exports")
    st.caption("Exports qualite: `data/metrics/validation_findings.parquet` et `data/processed/hourly/{country}/{year}.parquet`.")

    with st.expander("Voir details techniques complets", expanded=False):
        st.markdown("### Continuite temporelle")
        st.json(
            {
                "country": country,
                "year": int(year),
                "n_hours": n_hours,
                "expected_hours": expected_hours,
                "duplicate_timestamps": duplicate_timestamps,
                "continuity_ok": continuity_ok,
                "go_no_go": go_no_go,
            }
        )
        st.markdown("### Findings complets")
        st.dataframe(findings, use_container_width=True)
        st.markdown("### Apercu brut (10 lignes)")
        st.dataframe(df.head(10), use_container_width=True)
