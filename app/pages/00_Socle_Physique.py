from __future__ import annotations

import plotly.express as px
import streamlit as st

_PAGE_UTILS_IMPORT_ERROR: Exception | None = None
try:
    from app.page_utils import country_year_selector, load_hourly_safe, to_plot_frame
except Exception as exc:  # pragma: no cover - defensive for Streamlit cloud stale caches
    _PAGE_UTILS_IMPORT_ERROR = exc

    def _page_utils_unavailable(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(
            "app.page_utils indisponible sur cette instance (cache/deploiement partiel). "
            "Rebooter l'app puis vider le cache Streamlit Cloud."
        )

    country_year_selector = _page_utils_unavailable  # type: ignore[assignment]
    load_hourly_safe = _page_utils_unavailable  # type: ignore[assignment]
    to_plot_frame = _page_utils_unavailable  # type: ignore[assignment]
from app.ui_components import (
    REGIME_COLORS,
    guided_header,
    inject_theme,
    render_interpretation,
    render_kpi_cards_styled,
    render_plotly_styled,
    render_question_box,
    render_regime_cards,
    show_definitions_cards,
    show_metric_explainers_tabbed,
)


def render() -> None:
    if _PAGE_UTILS_IMPORT_ERROR is not None:
        st.error("Impossible de charger les utilitaires de page (page_utils).")
        st.code(str(_PAGE_UTILS_IMPORT_ERROR))
        st.info("Action recommandee: Streamlit Cloud > Manage app > Reboot app, puis Clear cache.")
        return

    inject_theme()
    guided_header(
        title="Socle Physique",
        purpose="Visualiser la logique physique horaire (NRL, surplus, flex) qui alimente tous les modules Q1..Q5.",
        step_now="Socle Physique: verifier les mecanismes horaires",
        step_next="Q1: detecter la bascule de phase",
    )

    st.markdown("## Question business")
    render_question_box("La physique du systeme (surplus et absorption) est-elle coherentement reconstruite heure par heure ?")

    show_definitions_cards(
        [
            ("NRL", "Load net - VRE - MustRun. Besoin residuel net du systeme."),
            ("Surplus", "Energie excedentaire quand NRL est negatif."),
            ("Flex effective", "Absorption via exports, pompage et BESS si active."),
            ("Regimes A/B/C/D", "Classification physique anti-circularite (voir ci-dessous)."),
        ]
    )
    show_metric_explainers_tabbed(
        [
            {
                "metric": "NRL",
                "definition": "Besoin residuel net du systeme apres VRE et must-run.",
                "formula": "NRL = load_mw - gen_vre_mw - gen_must_run_mw",
                "intuition": "NRL negatif signale un excedent a absorber.",
                "interpretation": "NRL plus negatif = pression accrue vers prix bas.",
                "limits": "Depend du perimetre must-run.",
                "dependencies": "load net mode, mapping generation, hypotheses must-run.",
            },
            {
                "metric": "Regimes A/B/C/D",
                "definition": "Classification physique horaire sans prix.",
                "formula": "A: surplus_unabsorbed>0; B: surplus>0 et unabsorbed=0; D: NRL>=seuil; C sinon",
                "intuition": "Structure le raisonnement piecewise sans circularite prix.",
                "interpretation": "A/B = heures de surplus, D = heures tendues.",
                "limits": "Seuil regime D parametrique.",
                "dependencies": "surplus, flex_effective, threshold nrl positif.",
            },
        ],
        title="Comment lire le socle physique",
    )

    country, year = country_year_selector()
    df = load_hourly_safe(country, year)
    if df is None or df.empty:
        st.info("Aucune table horaire disponible.")
        return

    st.markdown("## Tests empiriques")
    share_surplus = float((df["surplus_mw"] > 0).mean())
    share_unabs = float((df["surplus_unabsorbed_mw"] > 0).mean())
    share_a = float((df["regime"] == "A").mean()) if "regime" in df.columns else 0.0

    render_kpi_cards_styled(
        [
            {"label": "Heures surplus", "value": f"{100*share_surplus:.1f}%", "help": "Part d'heures avec surplus."},
            {"label": "Heures surplus non absorbe", "value": f"{100*share_unabs:.1f}%", "help": "Part d'heures en surplus non absorbe."},
            {"label": "Part regime A", "value": f"{100*share_a:.1f}%", "help": "Regime A = surplus non absorbe.", "delta": f"{100*share_a:.1f}%", "delta_direction": "down" if share_a > 0.05 else "neutral"},
        ]
    )

    st.markdown("## Resultats et interpretation")
    view = to_plot_frame(df).tail(168)
    fig_lines = px.line(view, x="timestamp_utc", y=["nrl_mw", "surplus_mw", "flex_effective_mw"], title="Dernieres 168h: NRL, surplus, flex")
    fig_lines.update_layout(xaxis_title="Date/heure UTC", yaxis_title="MW")
    render_plotly_styled(
        fig_lines,
        "Les heures ou surplus_mw depasse flex_effective_mw correspondent au regime A (surplus non absorbe). "
        "C'est le mecanisme physique central de la cannibalisation des prix.",
        key="socle_lines",
    )

    reg = df["regime"].value_counts(dropna=False).rename_axis("regime").reset_index(name="hours") if "regime" in df.columns else None
    if reg is not None:
        color_map = {k: v for k, v in REGIME_COLORS.items() if k in reg["regime"].values}
        fig_bar = px.bar(reg, x="regime", y="hours", title="Distribution des regimes physiques", color="regime", color_discrete_map=color_map)
        fig_bar.update_layout(xaxis_title="Regime", yaxis_title="Heures", showlegend=False)
        render_plotly_styled(
            fig_bar,
            "Regime A = pression maximale (surplus non absorbe). B = surplus absorbe. C = normal/thermique. D = tension/rarete.",
            key="socle_regimes",
        )

    st.markdown("### Regimes en detail")
    render_regime_cards()

    with st.expander("Voir details techniques", expanded=False):
        cols = [c for c in ["nrl_mw", "surplus_mw", "flex_effective_mw", "surplus_unabsorbed_mw", "regime"] if c in df.columns]
        st.dataframe(df[cols].head(72), use_container_width=True)

    st.markdown("## Limites")
    st.markdown(
        "- Le socle reste volontairement simplifie (pas de contraintes reseau fines).\n"
        "- La definition must-run influence NRL et surplus.\n"
        "- La qualite des series net_position/psh impacte la lecture de la flex."
    )

    st.markdown("## Checks & exports")
    st.caption("Les checks detailes sont visibles dans la page Donnees & Qualite et dans `validation_findings`.")
