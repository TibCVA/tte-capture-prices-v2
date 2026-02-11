"""Reusable UI components for guided Streamlit pages."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st
import numpy as np


# ---------------------------------------------------------------------------
# Plotly template (uniform palette, font, grid, margins)
# ---------------------------------------------------------------------------

TTE_PLOTLY_TEMPLATE = dict(
    layout=dict(
        font=dict(family="Inter, system-ui, sans-serif", size=13),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        colorway=[
            "#0f766e",  # teal (primary)
            "#2563eb",  # blue
            "#d97706",  # amber
            "#dc2626",  # red
            "#7c3aed",  # violet
            "#059669",  # emerald
            "#64748b",  # slate
            "#0891b2",  # cyan
        ],
        xaxis=dict(gridcolor="#e2e8f0", gridwidth=1),
        yaxis=dict(gridcolor="#e2e8f0", gridwidth=1),
        margin=dict(l=60, r=20, t=50, b=50),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        title=dict(font=dict(size=15, color="#1e293b")),
    ),
)

# Regime / phase color maps for chart usage
REGIME_COLORS = {"A": "#dc2626", "B": "#d97706", "C": "#0f766e", "D": "#7c3aed"}
PHASE_COLORS = {"stage_1": "#059669", "stage_2": "#d97706", "stage_3": "#7c3aed", "stage_4": "#dc2626", "unknown": "#94a3b8"}


# ---------------------------------------------------------------------------
# Theme injection (original CSS preserved, new classes appended)
# ---------------------------------------------------------------------------

def inject_theme() -> None:
    st.markdown(
        """
<style>
/* --- Original v2 classes (do NOT remove) --- */
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

/* --- NEW: Interpretation "So What" box --- */
.tte-interpretation {
  background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
  border-left: 4px solid var(--tte-primary);
  border-radius: 0 8px 8px 0;
  padding: 0.7rem 1rem;
  margin: 0.6rem 0 1rem 0;
  font-size: 0.93rem;
  color: #1e293b;
  line-height: 1.6;
}

/* --- NEW: Question business callout --- */
.tte-question-box {
  background: linear-gradient(135deg, #eff6ff, #eef2ff);
  border: 1px solid #bfdbfe;
  border-radius: 12px;
  padding: 1rem 1.2rem;
  margin: 0.4rem 0 1rem 0;
  font-size: 1.02rem;
  font-weight: 500;
  color: #1e40af;
  line-height: 1.6;
}

/* --- NEW: Styled KPI card --- */
.tte-kpi-card {
  background: var(--tte-card);
  border: 1px solid var(--tte-border);
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  min-height: 100px;
}
.tte-kpi-card .kpi-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0.3rem 0;
}
.tte-kpi-card .kpi-label {
  font-size: 0.82rem;
  color: #64748b;
  margin-bottom: 0.2rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.tte-kpi-card .kpi-help {
  font-size: 0.78rem;
  color: #94a3b8;
  margin-top: 0.2rem;
}
.tte-kpi-delta-up { color: #15803d !important; font-size: 0.85rem; }
.tte-kpi-delta-down { color: #b91c1c !important; font-size: 0.85rem; }
.tte-kpi-delta-neutral { color: #6b7280 !important; font-size: 0.85rem; }

/* --- NEW: Narrative block --- */
.tte-narrative {
  background: var(--tte-card);
  border: 1px solid var(--tte-border);
  border-radius: 12px;
  padding: 1.2rem 1.5rem;
  margin: 0.8rem 0;
  line-height: 1.7;
  font-size: 0.95rem;
}

/* --- NEW: Definition card --- */
.tte-def-card {
  background: var(--tte-card);
  border: 1px solid var(--tte-border);
  border-radius: 10px;
  padding: 0.6rem 1rem;
  margin-bottom: 0.5rem;
  display: flex;
  gap: 0.6rem;
  align-items: baseline;
}
.tte-def-card .def-term {
  font-weight: 700;
  color: var(--tte-primary);
  min-width: 80px;
  flex-shrink: 0;
}
.tte-def-card .def-text {
  color: #334155;
  font-size: 0.92rem;
}

/* --- NEW: Executive card (conclusions) --- */
.tte-exec-card {
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  border: 2px solid var(--tte-primary);
  border-radius: 14px;
  padding: 1.5rem;
  margin: 1rem 0;
}
.tte-exec-verdict-pass { border-color: #15803d !important; }
.tte-exec-verdict-warn { border-color: var(--tte-warn) !important; }
.tte-exec-verdict-fail { border-color: var(--tte-danger) !important; }

/* --- NEW: Divider --- */
.tte-divider {
  border: none;
  border-top: 1px solid var(--tte-border);
  margin: 1.5rem 0;
}

/* --- NEW: Regime color badges --- */
.tte-regime-a { background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; border-radius: 8px; padding: 0.5rem; text-align: center; }
.tte-regime-b { background: #fff7ed; border: 1px solid #fed7aa; color: #92400e; border-radius: 8px; padding: 0.5rem; text-align: center; }
.tte-regime-c { background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46; border-radius: 8px; padding: 0.5rem; text-align: center; }
.tte-regime-d { background: #f5f3ff; border: 1px solid #c4b5fd; color: #5b21b6; border-radius: 8px; padding: 0.5rem; text-align: center; }

/* --- NEW: Section title with accent --- */
.tte-section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--tte-primary);
  border-bottom: 2px solid var(--tte-primary);
  padding-bottom: 0.4rem;
  margin-top: 1.5rem;
  margin-bottom: 0.8rem;
}
</style>
""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Original functions (signatures unchanged)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# NEW: Enhanced rendering functions
# ---------------------------------------------------------------------------

def render_question_box(text: str) -> None:
    """Render a business question in a styled callout box."""
    st.markdown(f'<div class="tte-question-box">{text}</div>', unsafe_allow_html=True)


def render_interpretation(text: str) -> None:
    """Render a 'So what' interpretation box after a chart or table."""
    st.markdown(f'<div class="tte-interpretation">{text}</div>', unsafe_allow_html=True)


def render_kpi_cards_styled(cards: list[dict[str, Any]]) -> None:
    """Render styled KPI cards with optional delta coloring.

    Each card dict: {"label": str, "value": str|int|float, "help": str,
                     "delta": str|None, "delta_direction": "up"|"down"|"neutral"|None}
    """
    if not cards:
        return
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        label = card.get("label", "")
        value = card.get("value", "")
        help_txt = card.get("help", "")
        delta = card.get("delta")
        direction = card.get("delta_direction", "neutral")

        delta_html = ""
        if delta is not None:
            css_class = f"tte-kpi-delta-{direction}" if direction in ("up", "down", "neutral") else "tte-kpi-delta-neutral"
            arrow = {"up": "&#9650;", "down": "&#9660;", "neutral": "&#9679;"}.get(direction, "")
            delta_html = f'<div class="{css_class}">{arrow} {delta}</div>'

        with col:
            st.markdown(
                f"""<div class="tte-kpi-card">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  {delta_html}
  <div class="kpi-help">{help_txt}</div>
</div>""",
                unsafe_allow_html=True,
            )


def render_test_ledger_styled(test_ledger: pd.DataFrame) -> None:
    """Enhanced test ledger with status pills summary and row coloring."""
    st.markdown("### Ce que cette execution teste (historique + prospectif)")
    if test_ledger is None or test_ledger.empty:
        st.info("Aucun test ledger disponible.")
        return

    # Summary pills
    if "status" in test_ledger.columns:
        counts = test_ledger["status"].astype(str).value_counts(dropna=False).to_dict()
        total = len(test_ledger)
        n_pass = counts.get("PASS", 0)
        n_warn = counts.get("WARN", 0)
        n_fail = counts.get("FAIL", 0)
        n_nt = counts.get("NON_TESTABLE", 0)
        st.markdown(
            f"<div style='margin-bottom:0.5rem;'>"
            f"<span class='tte-pill tte-pass'>PASS: {n_pass}</span>"
            f"<span class='tte-pill tte-warn'>WARN: {n_warn}</span>"
            f"<span class='tte-pill tte-fail'>FAIL: {n_fail}</span>"
            f"<span class='tte-pill'>NON_TESTABLE: {n_nt}</span>"
            f"<span class='tte-muted' style='margin-left:0.5rem;'>Total: {total}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # Filter columns
    cols = ["test_id", "mode", "scenario_id", "title", "status", "value", "threshold", "interpretation", "source_ref"]
    keep = [c for c in cols if c in test_ledger.columns]
    display_df = test_ledger[keep].copy()

    # Apply row coloring via Styler
    def _color_row(row: pd.Series) -> list[str]:
        status = str(row.get("status", "")).upper()
        color_map = {"PASS": "#f0fdf4", "WARN": "#fffbeb", "FAIL": "#fef2f2", "NON_TESTABLE": "#f5f5f5"}
        bg = color_map.get(status, "")
        return [f"background-color: {bg}" if bg else "" for _ in row]

    styled = display_df.style.apply(_color_row, axis=1)
    st.dataframe(styled, use_container_width=True, hide_index=True)

    # Brief interpretation legend
    render_interpretation(
        "PASS = conforme a la regle definie. "
        "WARN = exploitable avec prudence. "
        "FAIL = non conforme, conclusion invalidee. "
        "NON_TESTABLE = donnee ou perimetre insuffisant."
    )


def render_narrative_styled(markdown_text: str) -> None:
    """Render a narrative markdown block in a styled container."""
    if not markdown_text:
        st.info("Aucun narratif disponible.")
        return
    st.markdown(f'<div class="tte-narrative">', unsafe_allow_html=True)
    st.markdown(markdown_text)
    st.markdown("</div>", unsafe_allow_html=True)


def render_spec_table_collapsible(spec_df: pd.DataFrame) -> None:
    """Render a spec table inside a collapsible expander."""
    with st.expander("Voir les tests prevus (spec technique)", expanded=False):
        st.caption("Chaque test est defini par un identifiant, un mode (HIST/SCEN), une regle metrique et une reference aux slides TTE.")
        cols = ["test_id", "mode", "title", "what_is_tested", "metric_rule", "source_ref"]
        keep = [c for c in cols if c in spec_df.columns]
        st.dataframe(spec_df[keep] if keep else spec_df, use_container_width=True, hide_index=True)


def show_definitions_cards(items: list[tuple[str, str]]) -> None:
    """Render definitions as styled cards instead of plain bullets."""
    st.markdown("### Definitions express")
    for term, definition in items:
        st.markdown(
            f'<div class="tte-def-card">'
            f'<span class="def-term">{term}</span>'
            f'<span class="def-text">{definition}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )


def show_metric_explainers_tabbed(items: list[dict[str, str]], title: str = "Definitions detaillees") -> None:
    """Display metric explainers with one expander per metric (instead of one big expander)."""
    if not items:
        return
    st.markdown(f"### {title}")
    for item in items:
        metric = item.get("metric", "Metrique")
        definition = item.get("definition", "n/a")
        formula = item.get("formula", "n/a")
        intuition = item.get("intuition", "n/a")
        interpretation = item.get("interpretation", "n/a")
        limits = item.get("limits", "n/a")
        dependencies = item.get("dependencies", "n/a")
        with st.expander(f"{metric}", expanded=False):
            st.markdown(f"**Definition** : {definition}")
            st.code(formula, language=None)
            st.markdown(f"**Intuition** : {intuition}")
            st.markdown(f"**Comment lire** : {interpretation}")
            st.markdown(f"**Limites** : {limits}")
            st.markdown(f"**Dependances** : {dependencies}")


def apply_tte_template(fig: Any) -> Any:
    """Apply the TTE Plotly template to a figure and return it."""
    layout_opts = TTE_PLOTLY_TEMPLATE.get("layout", {})
    fig.update_layout(**layout_opts)
    return fig


def render_plotly_styled(fig: Any, interpretation: str = "", key: str = "") -> None:
    """Render a Plotly chart with TTE template and optional interpretation box."""
    fig = apply_tte_template(fig)
    st.plotly_chart(fig, use_container_width=True, key=key or None)
    if interpretation:
        render_interpretation(interpretation)


def render_status_interpretation(checks: list[dict[str, Any]]) -> None:
    """Render a contextual interpretation after the status banner."""
    statuses = [str(c.get("status", "")).upper() for c in checks]
    if "FAIL" in statuses:
        render_interpretation(
            "Des points critiques sont detectes. Ne pas conclure tant que les erreurs ne sont pas corrigees. "
            "Consulter l'onglet 'Details techniques' pour identifier les checks en echec."
        )
    elif "WARN" in statuses:
        render_interpretation(
            "Certains tests revelent des fragilites. Les conclusions doivent etre nuancees et les warnings "
            "explicites dans toute restitution."
        )
    else:
        render_interpretation(
            "Tous les tests ont ete valides. Les resultats sont exploitables pour des conclusions business."
        )


def render_regime_cards() -> None:
    """Render the 4 physical regimes as colored cards in 4 columns."""
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            '<div class="tte-regime-a"><strong>Regime A</strong><br>Surplus non absorbe<br>'
            '<span style="font-size:0.82rem;">Pression prix maximale</span></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="tte-regime-b"><strong>Regime B</strong><br>Surplus absorbe<br>'
            '<span style="font-size:0.82rem;">Flex suffisante</span></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="tte-regime-c"><strong>Regime C</strong><br>Normal / thermique<br>'
            '<span style="font-size:0.82rem;">Pas de surplus</span></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            '<div class="tte-regime-d"><strong>Regime D</strong><br>Tension / rarete<br>'
            '<span style="font-size:0.82rem;">NRL > P90</span></div>',
            unsafe_allow_html=True,
        )


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


def derive_outlier_flags_from_q2(slopes_df: pd.DataFrame) -> pd.DataFrame:
    """Build country-year outlier flags from Q2 slope table (years_used vs years_used_no_outliers)."""
    if slopes_df is None or slopes_df.empty:
        return pd.DataFrame(columns=["country", "year", "outlier_year"])
    rows: list[dict[str, Any]] = []
    for _, row in slopes_df.iterrows():
        country = str(row.get("country", "")).strip()
        used = _parse_years_csv(row.get("years_used", ""))
        kept = _parse_years_csv(row.get("years_used_no_outliers", ""))
        for y in sorted(used.difference(kept)):
            rows.append({"country": country, "year": int(y), "outlier_year": True})
    if not rows:
        return pd.DataFrame(columns=["country", "year", "outlier_year"])
    out = pd.DataFrame(rows)
    out = out.groupby(["country", "year"], as_index=False)["outlier_year"].max()
    return out


def render_data_quality_panel(
    annual_df: pd.DataFrame,
    *,
    countries: list[str] | None = None,
    years: list[int] | None = None,
    extra_country_year_df: pd.DataFrame | None = None,
    title: str = "Data quality",
) -> pd.DataFrame:
    """Render a country-year quality panel with canonical fields used by Q1..Q5 pages."""
    st.markdown(f"### {title}")
    if annual_df is None or annual_df.empty:
        st.info("Aucune table annuelle disponible pour le panneau de qualite.")
        return pd.DataFrame()

    panel = annual_df.copy()
    if "country" not in panel.columns or "year" not in panel.columns:
        st.info("Colonnes country/year absentes, impossible d'afficher le panneau de qualite.")
        return pd.DataFrame()

    if countries:
        scoped_c = {str(c) for c in countries}
        panel = panel[panel["country"].astype(str).isin(scoped_c)]
    if years:
        scoped_y = {int(y) for y in years}
        panel = panel[pd.to_numeric(panel["year"], errors="coerce").astype("Int64").isin(list(scoped_y))]

    if panel.empty:
        st.info("Aucune ligne sur le perimetre selectionne.")
        return pd.DataFrame()

    if "completeness" in panel.columns:
        comp = pd.to_numeric(panel["completeness"], errors="coerce")
        panel["missing_hours_pct"] = (1.0 - comp).clip(lower=0.0, upper=1.0) * 100.0
    elif "missing_hours_pct" in panel.columns:
        panel["missing_hours_pct"] = pd.to_numeric(panel["missing_hours_pct"], errors="coerce")
    else:
        panel["missing_hours_pct"] = np.nan

    for src in ["missing_share_price", "missing_share_load", "missing_share_generation", "missing_share_net_position"]:
        if src in panel.columns:
            panel[f"{src}_pct"] = pd.to_numeric(panel[src], errors="coerce") * 100.0

    if extra_country_year_df is not None and not extra_country_year_df.empty:
        extra = extra_country_year_df.copy()
        keep = [c for c in ["country", "year", "load_net_mode", "must_run_mode", "must_run_mode_hourly", "must_run_scope_coverage", "outlier_year"] if c in extra.columns]
        if {"country", "year"}.issubset(set(keep)):
            extra = extra[keep].copy()
            if "must_run_mode_hourly" in extra.columns and "must_run_mode" not in extra.columns:
                extra["must_run_mode"] = extra["must_run_mode_hourly"]
            panel = panel.merge(extra, on=["country", "year"], how="left", suffixes=("", "_extra"))
            for c in ["load_net_mode", "must_run_mode", "must_run_scope_coverage", "outlier_year"]:
                c_extra = f"{c}_extra"
                if c_extra in panel.columns:
                    if c in panel.columns:
                        panel[c] = panel[c].where(panel[c].notna(), panel[c_extra])
                    else:
                        panel[c] = panel[c_extra]
                    panel = panel.drop(columns=[c_extra])

    cols = [
        "country",
        "year",
        "quality_flag",
        "missing_hours_pct",
        "missing_share_price_pct",
        "missing_share_load_pct",
        "missing_share_generation_pct",
        "missing_share_net_position_pct",
        "load_net_mode",
        "must_run_mode",
        "must_run_scope_coverage",
        "outlier_year",
        "core_sanity_issue_count",
        "core_sanity_issues",
    ]
    keep_cols = [c for c in cols if c in panel.columns]
    out = panel[keep_cols].copy()
    out = out.sort_values(["country", "year"]).reset_index(drop=True)
    st.dataframe(out, use_container_width=True, hide_index=True)
    return out


def render_livrables_panel(
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
