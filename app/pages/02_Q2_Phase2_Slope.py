from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import assumptions_editor_for, load_annual_metrics
from src.modules.q2_slope import Q2_PARAMS, run_q2
from src.modules.result import export_module_result
from src.storage import load_hourly


def render() -> None:
    st.title("Q2 - Pente de la Phase 2 et drivers")

    st.markdown(
        """
## 1) Question business
Mesurer la pente de cannibalisation en Phase 2 et identifier les drivers dominants par pays.

### Definitions express
- `Pente`: variation du capture ratio quand la penetration augmente.
- `ROBUST`: regression avec nombre de points suffisant (`n >= min_points_regression`).
- `Driver`: variable correlatee a la pente (SR, FAR, IR, corr charge-VRE, etc.).
"""
    )

    annual = load_annual_metrics()
    if annual.empty:
        st.info("Aucune metrique annuelle disponible.")
        return

    countries = sorted(annual["country"].dropna().unique().tolist())
    selected = st.multiselect("Pays", countries, default=countries)

    st.markdown("## 2) Hypotheses et sources")
    assumptions = assumptions_editor_for(Q2_PARAMS, "q2")

    scoped = annual[annual["country"].isin(selected)].copy()
    fail_count = int((scoped["quality_flag"] == "FAIL").sum()) if not scoped.empty else 0
    if fail_count > 0:
        st.error(f"{fail_count} ligne(s) quality_flag=FAIL. Conclusions bloquees.")

    if not st.button("Executer Q2", type="primary", disabled=scoped.empty or fail_count > 0):
        return

    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    # Optional hourly context for stronger driver diagnostics
    hourly_map: dict[tuple[str, int], pd.DataFrame] = {}
    for _, row in scoped.iterrows():
        c = str(row["country"])
        y = int(row["year"])
        try:
            hourly_map[(c, y)] = load_hourly(c, y)
        except Exception:
            continue

    res = run_q2(annual, assumptions, {"countries": selected}, run_id, hourly_by_country_year=hourly_map)
    out_dir = export_module_result(res)

    st.markdown("## 3) Tests empiriques")
    slopes = res.tables["Q2_country_slopes"]
    drivers = res.tables["Q2_driver_correlations"]
    st.dataframe(slopes, use_container_width=True)

    st.markdown("## 4) Resultats et interpretation")
    if not slopes.empty:
        st.plotly_chart(
            px.bar(slopes, x="country", y="slope", color="tech", barmode="group", title="Pentes par pays et techno"),
            use_container_width=True,
        )

        # one regression scatter by country-tech
        csel = st.selectbox("Pays (scatter de regression)", sorted(slopes["country"].unique().tolist()))
        tsel = st.selectbox("Tech", ["PV", "WIND"])
        sub = slopes[(slopes["country"] == csel) & (slopes["tech"] == tsel)]
        if not sub.empty:
            row = sub.iloc[0]
            st.write(
                f"{csel}-{tsel}: slope={row['slope']:.4f}, r2={row['r2']:.3f}, p_value={row['p_value']:.3f}, n={int(row['n'])}, robust={row['robust_flag']}"
            )

    st.dataframe(drivers, use_container_width=True)
    st.markdown("### Lecture simple")
    st.markdown(res.narrative_md)

    st.markdown("## 5) Limites et risques de lecture")
    st.markdown(
        """
- La pente est un indicateur empirique, pas une loi causale.
- Faible `n` ou `r2` faible => interpretation prudente.
- Les proxies de penetration peuvent modifier la pente estimee.
- Les correlations drivers sont descriptives, pas causales.
"""
    )

    st.markdown("## 6) Checks et exports")
    st.dataframe(pd.DataFrame(res.checks), use_container_width=True)
    if res.warnings:
        st.warning(" | ".join(res.warnings))
    st.code(str(out_dir))
