"""Compatibility shims for Streamlit pages that depend on app.ui_components."""

from __future__ import annotations

from typing import Any, Callable

import pandas as pd
import streamlit as st

_UI_IMPORT_ERROR: Exception | None = None
_UI_MODULE: Any | None = None
try:
    from app import ui_components as _UI_MODULE
except Exception as exc:  # pragma: no cover - defensive for stale cloud deployments
    _UI_IMPORT_ERROR = exc
    _UI_MODULE = None


def _resolve(name: str, fallback: Callable[..., Any]) -> Callable[..., Any]:
    if _UI_MODULE is None:
        return fallback
    attr = getattr(_UI_MODULE, name, None)
    if callable(attr):
        return attr
    return fallback


def _warn_degraded_once() -> None:
    if st.session_state.get("_ui_shims_warned"):
        return
    st.session_state["_ui_shims_warned"] = True
    if _UI_IMPORT_ERROR is not None:
        st.warning("Chargement partiel de `app.ui_components`: mode degrade active.")
        st.code(str(_UI_IMPORT_ERROR))


def _fallback_inject_theme() -> None:
    return


def _fallback_guided_header(title: str, purpose: str, step_now: str, step_next: str) -> None:
    _warn_degraded_once()
    st.title(title)
    st.caption(purpose)
    st.info(f"{step_now} -> {step_next}")


def _fallback_render_interpretation(text: str) -> None:
    st.info(str(text))


def _fallback_render_question_box(text: str) -> None:
    st.info(str(text))


def _fallback_show_definitions_cards(items: list[tuple[str, str]]) -> None:
    if not items:
        return
    lines = [f"- **{k}**: {v}" for k, v in items]
    st.markdown("\n".join(lines))


def _fallback_show_metric_explainers_tabbed(items: list[dict[str, str]], title: str = "Definitions detaillees") -> None:
    st.markdown(f"### {title}")
    if not items:
        st.caption("Aucun detail disponible.")
        return
    for item in items:
        metric = str(item.get("metric", "")).strip() or "Metric"
        definition = str(item.get("definition", "")).strip()
        formula = str(item.get("formula", "")).strip()
        interpretation = str(item.get("interpretation", "")).strip()
        st.markdown(f"**{metric}**")
        if definition:
            st.caption(definition)
        if formula:
            st.code(formula)
        if interpretation:
            st.write(interpretation)


def _fallback_render_spec_table_collapsible(spec_df: pd.DataFrame) -> None:
    with st.expander("Specification des tests", expanded=False):
        if spec_df is None or spec_df.empty:
            st.caption("Aucune specification disponible.")
        else:
            st.dataframe(spec_df, use_container_width=True, hide_index=True)


def _fallback_render_status_banner(checks: list[dict[str, Any]]) -> None:
    statuses = {str(c.get("status", "")).upper() for c in checks or []}
    if "FAIL" in statuses:
        st.error("Statut checks techniques: FAIL. Des checks critiques sont en echec.")
    elif "WARN" in statuses:
        st.warning("Statut checks techniques: WARN. Des checks ont remonte des warnings.")
    else:
        st.success("Statut checks techniques: PASS. Checks passes ou non renseignes.")


def _fallback_render_status_interpretation(checks: list[dict[str, Any]]) -> None:
    statuses = {str(c.get("status", "")).upper() for c in checks or []}
    if "FAIL" in statuses:
        _fallback_render_interpretation("Des erreurs critiques limitent la fiabilite des conclusions.")
    elif "WARN" in statuses:
        _fallback_render_interpretation("Warnings presents: conclusions a nuancer.")
    else:
        _fallback_render_interpretation("Checks globalement conformes.")


def _fallback_render_test_ledger(test_ledger: pd.DataFrame) -> None:
    if test_ledger is None or test_ledger.empty:
        st.caption("Aucun test_ledger disponible.")
        return
    st.dataframe(test_ledger, use_container_width=True)


def _fallback_render_test_ledger_styled(test_ledger: pd.DataFrame) -> None:
    _fallback_render_test_ledger(test_ledger)


def _fallback_render_kpi_cards_styled(cards: list[dict[str, Any]]) -> None:
    if not cards:
        return
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        with col:
            label = str(card.get("label", "KPI"))
            value = card.get("value", "n/a")
            help_text = str(card.get("help", "")).strip()
            st.metric(label, value)
            if help_text:
                st.caption(help_text)


def _fallback_render_robustness_panel(test_ledger: pd.DataFrame) -> None:
    st.markdown("### Robustesse")
    if test_ledger is None or test_ledger.empty or "status" not in test_ledger.columns:
        st.caption("Aucun indicateur de robustesse disponible.")
        return
    status_counts = test_ledger["status"].astype(str).value_counts(dropna=False).to_dict()
    st.json(status_counts)


def _fallback_render_narrative_styled(markdown_text: str) -> None:
    if markdown_text:
        st.markdown(markdown_text)


def _fallback_render_hist_scen_comparison(comparison_table: pd.DataFrame) -> None:
    if comparison_table is None or comparison_table.empty:
        st.caption("Aucune comparaison HIST vs SCEN disponible.")
        return
    st.dataframe(comparison_table, use_container_width=True)


def _fallback_render_plotly_styled(fig: Any, interpretation: str = "", key: str = "") -> None:
    st.plotly_chart(fig, use_container_width=True, key=key or None)
    if interpretation:
        _fallback_render_interpretation(interpretation)


def _fallback_show_checks_summary(checks: list[dict[str, Any]]) -> None:
    if not checks:
        st.caption("Aucun check disponible.")
        return
    st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)


def _fallback_show_limitations(lines: list[str]) -> None:
    if not lines:
        return
    st.markdown("## Limites")
    st.markdown("\n".join(f"- {line}" for line in lines))


def _parse_years_csv(value: Any) -> set[int]:
    if value is None:
        return set()
    text = str(value).strip()
    if not text:
        return set()
    out: set[int] = set()
    for tok in text.split(","):
        tok = tok.strip()
        if not tok:
            continue
        try:
            out.add(int(float(tok)))
        except Exception:
            continue
    return out


def _fallback_derive_outlier_flags_from_q2(slopes_df: pd.DataFrame) -> pd.DataFrame:
    if slopes_df is None or slopes_df.empty:
        return pd.DataFrame(columns=["country", "year", "outlier_year"])
    rows: list[dict[str, Any]] = []
    for _, row in slopes_df.iterrows():
        country = str(row.get("country", "")).strip()
        used = _parse_years_csv(row.get("years_used", ""))
        kept = _parse_years_csv(row.get("years_used_no_outliers", ""))
        for year in sorted(used.difference(kept)):
            rows.append({"country": country, "year": int(year), "outlier_year": True})
    if not rows:
        return pd.DataFrame(columns=["country", "year", "outlier_year"])
    out = pd.DataFrame(rows)
    return out.groupby(["country", "year"], as_index=False)["outlier_year"].max()


def _fallback_render_data_quality_panel(
    annual_df: pd.DataFrame,
    *,
    countries: list[str] | None = None,
    years: list[int] | None = None,
    extra_country_year_df: pd.DataFrame | None = None,
    title: str = "Data quality",
) -> pd.DataFrame:
    st.markdown(f"### {title}")
    if annual_df is None or annual_df.empty:
        st.info("Aucune table annuelle disponible pour le panneau de qualite.")
        return pd.DataFrame()

    panel = annual_df.copy()
    if "country" not in panel.columns or "year" not in panel.columns:
        st.info("Colonnes country/year absentes, impossible d'afficher le panneau de qualite.")
        return pd.DataFrame()

    if countries:
        panel = panel[panel["country"].astype(str).isin({str(c) for c in countries})]
    if years:
        y_filter = {int(y) for y in years}
        panel = panel[pd.to_numeric(panel["year"], errors="coerce").astype("Int64").isin(list(y_filter))]

    if extra_country_year_df is not None and not extra_country_year_df.empty:
        extra = extra_country_year_df.copy()
        if {"country", "year"}.issubset(extra.columns):
            panel = panel.merge(extra, on=["country", "year"], how="left", suffixes=("", "_extra"))

    keep = [
        "country",
        "year",
        "quality_flag",
        "completeness",
        "regime_coherence",
        "nrl_price_corr",
        "outlier_year",
    ]
    keep_cols = [c for c in keep if c in panel.columns]
    out = panel[keep_cols].sort_values(["country", "year"]).reset_index(drop=True) if keep_cols else panel
    st.dataframe(out, use_container_width=True, hide_index=True)
    return out


def _fallback_render_livrables_panel(
    *,
    run_id: str,
    out_dir: str,
    hist_tables: list[str],
    scenario_ids: list[str],
) -> None:
    st.markdown("## Livrables")
    st.markdown(f"- Run ID: `{run_id}`")
    st.markdown(f"- Repertoire export: `{out_dir}`")
    st.markdown(f"- Tables historiques: `{', '.join(sorted(hist_tables)) if hist_tables else 'n/a'}`")
    st.markdown(f"- Scenarios exportes: `{', '.join(sorted(scenario_ids)) if scenario_ids else 'aucun'}`")


inject_theme = _resolve("inject_theme", _fallback_inject_theme)
guided_header = _resolve("guided_header", _fallback_guided_header)
render_interpretation = _resolve("render_interpretation", _fallback_render_interpretation)
render_question_box = _resolve("render_question_box", _fallback_render_question_box)
show_definitions_cards = _resolve("show_definitions_cards", _fallback_show_definitions_cards)
show_metric_explainers_tabbed = _resolve("show_metric_explainers_tabbed", _fallback_show_metric_explainers_tabbed)
render_spec_table_collapsible = _resolve("render_spec_table_collapsible", _fallback_render_spec_table_collapsible)
render_status_banner = _resolve("render_status_banner", _fallback_render_status_banner)
render_status_interpretation = _resolve("render_status_interpretation", _fallback_render_status_interpretation)
render_test_ledger = _resolve("render_test_ledger", _fallback_render_test_ledger)
render_test_ledger_styled = _resolve("render_test_ledger_styled", _fallback_render_test_ledger_styled)
render_kpi_cards_styled = _resolve("render_kpi_cards_styled", _fallback_render_kpi_cards_styled)
render_robustness_panel = _resolve("render_robustness_panel", _fallback_render_robustness_panel)
render_narrative_styled = _resolve("render_narrative_styled", _fallback_render_narrative_styled)
render_hist_scen_comparison = _resolve("render_hist_scen_comparison", _fallback_render_hist_scen_comparison)
render_plotly_styled = _resolve("render_plotly_styled", _fallback_render_plotly_styled)
show_checks_summary = _resolve("show_checks_summary", _fallback_show_checks_summary)
show_limitations = _resolve("show_limitations", _fallback_show_limitations)
derive_outlier_flags_from_q2 = _resolve("derive_outlier_flags_from_q2", _fallback_derive_outlier_flags_from_q2)
render_data_quality_panel = _resolve("render_data_quality_panel", _fallback_render_data_quality_panel)
render_livrables_panel = _resolve("render_livrables_panel", _fallback_render_livrables_panel)


__all__ = [
    "derive_outlier_flags_from_q2",
    "guided_header",
    "inject_theme",
    "render_data_quality_panel",
    "render_hist_scen_comparison",
    "render_interpretation",
    "render_kpi_cards_styled",
    "render_livrables_panel",
    "render_narrative_styled",
    "render_plotly_styled",
    "render_question_box",
    "render_robustness_panel",
    "render_spec_table_collapsible",
    "render_status_banner",
    "render_status_interpretation",
    "render_test_ledger",
    "render_test_ledger_styled",
    "show_checks_summary",
    "show_definitions_cards",
    "show_limitations",
    "show_metric_explainers_tabbed",
]
