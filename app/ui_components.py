"""Reusable UI components for guided Streamlit pages."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st


def inject_theme() -> None:
    st.markdown(
        """
<style>
:root {
  --tte-bg: #f8fafc;
  --tte-card: #ffffff;
  --tte-border: #dce3ea;
  --tte-primary: #0f766e;
  --tte-warn: #b45309;
  --tte-danger: #b91c1c;
}
.tte-step {
  background: linear-gradient(135deg, #ecfeff, #f0fdf4);
  border: 1px solid var(--tte-border);
  border-radius: 14px;
  padding: 0.8rem 1rem;
  margin-bottom: 0.8rem;
}
.tte-card {
  background: var(--tte-card);
  border: 1px solid var(--tte-border);
  border-radius: 12px;
  padding: 0.8rem 1rem;
}
.tte-muted { color: #334155; font-size: 0.95rem; }
.tte-pill {
  display: inline-block;
  border-radius: 999px;
  border: 1px solid var(--tte-border);
  padding: 0.2rem 0.55rem;
  font-size: 0.82rem;
  margin-right: 0.35rem;
  margin-bottom: 0.25rem;
}
.tte-pass { background: #ecfdf5; border-color: #a7f3d0; }
.tte-warn { background: #fff7ed; border-color: #fed7aa; }
.tte-fail { background: #fef2f2; border-color: #fecaca; }
</style>
""",
        unsafe_allow_html=True,
    )


def guided_header(title: str, purpose: str, step_now: str, step_next: str) -> None:
    st.markdown(
        f"""
<div class="tte-step">
  <div><strong>Etape actuelle:</strong> {step_now}</div>
  <div><strong>Etape suivante:</strong> {step_next}</div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.title(title)
    st.caption(purpose)


def show_definitions(items: list[tuple[str, str]]) -> None:
    st.markdown("### Definitions express")
    for k, v in items:
        st.markdown(f"- **{k}**: {v}")


def show_metric_explainers(items: list[dict[str, str]], title: str = "Definitions detaillees") -> None:
    """Display full KPI explicability: definition, formula, intuition, interpretation, limits, dependencies."""
    if not items:
        return
    st.markdown(f"### {title}")
    with st.expander("Voir formule, intuition, interpretation, limites et dependances", expanded=False):
        for item in items:
            metric = item.get("metric", "Metrique")
            definition = item.get("definition", "n/a")
            formula = item.get("formula", "n/a")
            intuition = item.get("intuition", "n/a")
            interpretation = item.get("interpretation", "n/a")
            limits = item.get("limits", "n/a")
            dependencies = item.get("dependencies", "n/a")
            st.markdown(f"**{metric}**")
            st.markdown(f"- Definition: {definition}")
            st.markdown(f"- Formule: `{formula}`")
            st.markdown(f"- Intuition: {intuition}")
            st.markdown(f"- Interpretation: {interpretation}")
            st.markdown(f"- Limites: {limits}")
            st.markdown(f"- Dependances: {dependencies}")


def show_kpi_cards(cards: list[tuple[str, Any, str]]) -> None:
    if not cards:
        return
    cols = st.columns(len(cards))
    for col, (label, value, help_txt) in zip(cols, cards):
        with col:
            st.metric(label, value, help=help_txt)


def show_checks_summary(checks: list[dict[str, Any]]) -> None:
    df = pd.DataFrame(checks) if checks else pd.DataFrame(columns=["status", "code", "message"])
    if df.empty:
        st.info("Aucun check retourne.")
        return
    counts = df["status"].value_counts(dropna=False).to_dict() if "status" in df.columns else {}
    st.markdown(
        "<div>"
        f"<span class='tte-pill tte-pass'>PASS: {counts.get('PASS', 0)}</span>"
        f"<span class='tte-pill tte-warn'>WARN: {counts.get('WARN', 0)}</span>"
        f"<span class='tte-pill tte-warn'>INFO: {counts.get('INFO', 0)}</span>"
        f"<span class='tte-pill tte-fail'>FAIL: {counts.get('FAIL', 0)}</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.dataframe(df, use_container_width=True)


def show_limitations(lines: list[str]) -> None:
    st.markdown("## Limites")
    for line in lines:
        st.markdown(f"- {line}")


def render_status_banner(checks: list[dict[str, Any]]) -> None:
    statuses = [str(c.get("status", "")).upper() for c in checks]
    if "FAIL" in statuses:
        st.error("Statut global: FAIL. Des points critiques restent a corriger.")
    elif "WARN" in statuses:
        st.warning("Statut global: WARN. Resultats exploitables avec prudence.")
    else:
        st.success("Statut global: PASS. Aucun echec critique detecte.")


def render_test_ledger(test_ledger: pd.DataFrame) -> None:
    st.markdown("### Ce que cette execution teste (historique + prospectif)")
    if test_ledger is None or test_ledger.empty:
        st.info("Aucun test ledger disponible.")
        return
    cols = [
        "test_id",
        "mode",
        "scenario_id",
        "title",
        "status",
        "value",
        "threshold",
        "interpretation",
        "source_ref",
    ]
    keep = [c for c in cols if c in test_ledger.columns]
    st.dataframe(test_ledger[keep], use_container_width=True)


def render_hist_scen_comparison(comparison_table: pd.DataFrame) -> None:
    st.markdown("### Comparaison historique vs prospectif")
    if comparison_table is None or comparison_table.empty:
        st.info("Aucune comparaison disponible pour cette selection.")
        return
    if "interpretability_status" in comparison_table.columns:
        counts = comparison_table["interpretability_status"].astype(str).value_counts().to_dict()
        st.markdown(
            "<div>"
            f"<span class='tte-pill tte-pass'>INFORMATIVE: {counts.get('INFORMATIVE', 0)}</span>"
            f"<span class='tte-pill tte-warn'>FRAGILE: {counts.get('FRAGILE', 0)}</span>"
            f"<span class='tte-pill tte-warn'>NON_TESTABLE: {counts.get('NON_TESTABLE', 0)}</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        non_interp = comparison_table[comparison_table["interpretability_status"].astype(str) != "INFORMATIVE"]
        if not non_interp.empty:
            st.caption("Les lignes FRAGILE/NON_TESTABLE restent visibles pour eviter toute conclusion silencieuse.")
    st.dataframe(comparison_table, use_container_width=True)


def render_robustness_panel(test_ledger: pd.DataFrame) -> None:
    st.markdown("### Robustesse vs fragilite")
    if test_ledger is None or test_ledger.empty:
        st.info("Pas de statut de robustesse disponible.")
        return
    status_counts = test_ledger["status"].astype(str).value_counts(dropna=False).rename_axis("status").reset_index(name="n")
    st.dataframe(status_counts, use_container_width=True)
    n_nt = int((test_ledger["status"].astype(str) == "NON_TESTABLE").sum())
    if n_nt > 0:
        st.info(f"{n_nt} test(s) NON_TESTABLE: donnee ou scenario manquant, sans silence.")
