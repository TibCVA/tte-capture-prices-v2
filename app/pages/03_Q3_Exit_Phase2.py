from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import assumptions_editor_for, load_annual_metrics
from src.modules.q3_exit import Q3_PARAMS, run_q3
from src.modules.result import export_module_result
from src.storage import load_hourly


def render() -> None:
    st.title("Q3 - Sortie de Phase 2 et conditions d'inversion")

    st.markdown(
        """
## 1) Question business
Detecter les signaux de stabilisation/amelioration apres stress et chiffrer des ordres de grandeur d'inversion.

### Definitions express
- `Trend`: pente sur fenetre glissante (annees).
- `Amelioration`: baisse des heures negatives et stabilisation/hausse capture ratio.
- `Contre-factuel`: test statique (demande, must-run, flex), pas un plan d'investissement.
"""
    )

    annual = load_annual_metrics()
    if annual.empty:
        st.info("Aucune metrique annuelle disponible.")
        return

    countries = sorted(annual["country"].dropna().unique().tolist())
    selected = st.multiselect("Pays", countries, default=countries)

    st.markdown("## 2) Hypotheses et sources")
    assumptions = assumptions_editor_for(Q3_PARAMS, "q3")

    scoped = annual[annual["country"].isin(selected)].copy()
    fail_count = int((scoped["quality_flag"] == "FAIL").sum()) if not scoped.empty else 0
    if fail_count > 0:
        st.error(f"{fail_count} ligne(s) quality_flag=FAIL. Conclusions bloquees.")

    if not st.button("Executer Q3", type="primary", disabled=scoped.empty or fail_count > 0):
        return

    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    hourly_map: dict[tuple[str, int], pd.DataFrame] = {}
    for _, row in scoped.iterrows():
        c = str(row["country"])
        y = int(row["year"])
        try:
            hourly_map[(c, y)] = load_hourly(c, y)
        except Exception:
            continue

    res = run_q3(
        annual,
        hourly_map,
        assumptions,
        {"countries": selected, "years": sorted(scoped["year"].dropna().astype(int).unique().tolist())},
        run_id,
    )
    out_dir = export_module_result(res)

    out = res.tables["Q3_status"]

    st.markdown("## 3) Tests empiriques")
    st.dataframe(out, use_container_width=True)

    st.markdown("## 4) Resultats et interpretation")
    if not out.empty:
        st.plotly_chart(
            px.scatter(
                out,
                x="inversion_k_demand",
                y="inversion_r_mustrun",
                color="status",
                hover_name="country",
                title="Contre-factuels inversion demande vs must-run",
            ),
            use_container_width=True,
        )
        st.plotly_chart(
            px.bar(
                out.sort_values("additional_absorbed_needed_TWh_year", ascending=False),
                x="country",
                y="additional_absorbed_needed_TWh_year",
                color="status",
                title="Flex additionnelle requise (TWh/an)",
            ),
            use_container_width=True,
        )

    st.markdown("### Lecture simple")
    st.markdown(res.narrative_md)

    st.markdown("## 5) Limites et risques de lecture")
    st.markdown(
        """
- Les contre-factuels sont statiques et unidimensionnels.
- Les interactions investissement/prix/reseau ne sont pas modelisees.
- Le resultat ne remplace pas une trajectoire industrielle.
- La qualite des donnees annuelles conditionne la robustesse des trends.
"""
    )

    st.markdown("## 6) Checks et exports")
    st.dataframe(pd.DataFrame(res.checks), use_container_width=True)
    if res.warnings:
        st.warning(" | ".join(res.warnings))
    st.code(str(out_dir))
