from __future__ import annotations

import plotly.express as px
import streamlit as st

from app.page_utils import country_year_selector, load_hourly_safe, to_plot_frame
from app.ui_components import guided_header, inject_theme, show_definitions, show_kpi_cards

try:
    from app.ui_components import show_metric_explainers
except ImportError:  # Backward-compatible fallback if cloud cache serves an older ui_components module.
    def show_metric_explainers(*args, **kwargs):  # type: ignore[no-redef]
        return None


def render() -> None:
    inject_theme()
    guided_header(
        title="Socle Physique",
        purpose="Visualiser la logique physique horaire (NRL, surplus, flex) qui alimente tous les modules Q1..Q5.",
        step_now="Socle Physique: verifier les mecanismes horaires",
        step_next="Q1: detecter la bascule de phase",
    )

    st.markdown("## Question business")
    st.markdown("La physique du systeme (surplus et absorption) est-elle coherentement reconstruite heure par heure ?")

    show_definitions(
        [
            ("NRL", "Load net - VRE - MustRun."),
            ("Surplus", "Energie excedentaire quand NRL est negatif."),
            ("Flex effective", "Absorption via exports, pompage et BESS si active."),
            ("Regimes A/B/C/D", "Classification physique anti-circularite."),
        ]
    )
    show_metric_explainers(
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

    show_kpi_cards(
        [
            ("Heures surplus", f"{100*share_surplus:.1f}%", "Part d'heures avec surplus."),
            ("Heures surplus non absorbe", f"{100*share_unabs:.1f}%", "Part d'heures en surplus non absorbe."),
            ("Part regime A", f"{100*share_a:.1f}%", "Regime A = surplus non absorbe."),
        ]
    )

    st.markdown("## Resultats et interpretation")
    view = to_plot_frame(df).tail(168)
    st.plotly_chart(
        px.line(view, x="timestamp_utc", y=["nrl_mw", "surplus_mw", "flex_effective_mw"], title="Dernieres 168h: NRL, surplus, flex"),
        use_container_width=True,
    )

    reg = df["regime"].value_counts(dropna=False).rename_axis("regime").reset_index(name="hours") if "regime" in df.columns else None
    if reg is not None:
        st.plotly_chart(px.bar(reg, x="regime", y="hours", title="Distribution des regimes physiques"), use_container_width=True)

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
