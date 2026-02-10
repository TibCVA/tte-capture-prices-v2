from __future__ import annotations

from datetime import datetime
from time import perf_counter

import pandas as pd
import plotly.express as px
import streamlit as st

from app.page_utils import assumptions_editor_for, load_annual_metrics, load_hourly_safe
from app.ui_components import guided_header, inject_theme, show_checks_summary, show_definitions, show_kpi_cards, show_limitations
from src.modules.q2_slope import Q2_PARAMS, run_q2
from src.modules.result import export_module_result


RESULT_KEY = "q2_last_result"


def _top_driver_lines(drivers: pd.DataFrame) -> list[str]:
    if drivers.empty:
        return ["Aucun driver exploitable sur la selection."]
    d = drivers.copy()
    d["abs_pv"] = pd.to_numeric(d["corr_with_slope_pv"], errors="coerce").abs()
    d = d.sort_values("abs_pv", ascending=False)
    lines: list[str] = []
    for _, row in d.head(3).iterrows():
        corr_pv = row.get("corr_with_slope_pv")
        corr_w = row.get("corr_with_slope_wind")
        lines.append(
            f"{row['driver_name']}: corr pente PV={corr_pv:.3f} | corr pente Wind={corr_w:.3f}" if pd.notna(corr_pv) and pd.notna(corr_w) else f"{row['driver_name']}: correlation partielle"
        )
    return lines


def render() -> None:
    inject_theme()
    guided_header(
        title="Q2 - Pente de la Phase 2 et drivers",
        purpose="Mesurer la vitesse de degradation des capture ratios apres bascule et identifier les facteurs dominants.",
        step_now="Q2: mesurer la pente post-bascule",
        step_next="Q3: evaluer la stabilisation et les conditions d'inversion",
    )

    st.markdown("## Question business")
    st.markdown("Quelle est la pente de la phase 2, et quels facteurs pilotent cette pente ?")

    show_definitions(
        [
            ("Pente", "Variation empirique du capture ratio quand la penetration augmente."),
            ("ROBUST", "Regression avec nombre de points suffisant (n >= seuil)."),
            ("Driver", "Variable corrigee a la pente (SR, FAR, IR, corr load-VRE, TTL)."),
        ]
    )

    annual = load_annual_metrics()
    if annual.empty:
        st.info("Aucune metrique annuelle disponible.")
        return

    countries = sorted(annual["country"].dropna().unique().tolist())
    with st.form("q2_form"):
        selected = st.multiselect("Pays", countries, default=countries)
        run_submit = st.form_submit_button("Executer Q2", type="primary")

    st.markdown("## Hypotheses utilisees")
    assumptions = assumptions_editor_for(Q2_PARAMS, "q2")

    scoped = annual[annual["country"].isin(selected)].copy()
    fail_count = int((scoped["quality_flag"] == "FAIL").sum()) if not scoped.empty else 0
    if fail_count > 0:
        st.error(f"{fail_count} ligne(s) quality_flag=FAIL. Conclusions bloquees.")

    if run_submit and fail_count == 0 and not scoped.empty:
        run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        t0 = perf_counter()

        hourly_map: dict[tuple[str, int], pd.DataFrame] = {}
        for _, row in scoped.iterrows():
            c = str(row["country"])
            y = int(row["year"])
            h = load_hourly_safe(c, y)
            if h is not None and not h.empty:
                hourly_map[(c, y)] = h

        res = run_q2(annual, assumptions, {"countries": selected}, run_id, hourly_by_country_year=hourly_map)
        out_dir = export_module_result(res)
        dt = perf_counter() - t0
        st.session_state[RESULT_KEY] = {"res": res, "runtime_sec": dt, "out_dir": str(out_dir)}

    payload = st.session_state.get(RESULT_KEY)
    if not payload:
        return

    res = payload["res"]
    slopes = res.tables["Q2_country_slopes"]
    drivers = res.tables["Q2_driver_correlations"]

    st.markdown("## Tests empiriques")
    with st.expander("Voir details techniques", expanded=False):
        st.dataframe(slopes, use_container_width=True)
        st.dataframe(drivers, use_container_width=True)

    st.markdown("## Resultats et interpretation")
    show_kpi_cards(
        [
            ("Pentes calculees", res.kpis.get("n_slopes", 0), "Nombre total de regressions calculees."),
            ("Pentes robustes", res.kpis.get("n_robust", 0), "Nombre de regressions robustes."),
            ("Temps calcul (s)", f"{payload['runtime_sec']:.2f}", "Temps total de calcul du module."),
        ]
    )

    if not slopes.empty:
        st.plotly_chart(
            px.bar(slopes, x="country", y="slope", color="tech", barmode="group", title="Pentes par pays et techno"),
            use_container_width=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            csel = st.selectbox("Pays (scatter regression)", sorted(slopes["country"].unique().tolist()), key="q2_country")
        with col2:
            tsel = st.selectbox("Tech", ["PV", "WIND"], key="q2_tech")

        row = slopes[(slopes["country"] == csel) & (slopes["tech"] == tsel)]
        if not row.empty:
            r = row.iloc[0]
            st.info(
                f"{csel}-{tsel}: slope={r['slope']:.4f}, R2={r['r2']:.3f}, p-value={r['p_value']:.3f}, n={int(r['n'])}, robustesse={r['robust_flag']}"
            )

    st.markdown("### Ce qui pilote la pente")
    for line in _top_driver_lines(drivers):
        st.markdown(f"- {line}")

    st.markdown("### Ne pas sur-interpreter")
    st.warning("Une pente robuste exige n suffisant, qualite OK et relation lineaire minimale. Les correlations drivers restent descriptives.")

    st.markdown("### Lecture simple")
    st.markdown(res.narrative_md)

    show_limitations(
        [
            "La pente est un indicateur empirique et non une preuve causale.",
            "Un faible R2 implique une relation lineaire peu informative.",
            "Les proxies de penetration peuvent biaiser la pente.",
            "Les comparaisons pays doivent etre lues avec les flags qualite.",
        ]
    )

    st.markdown("## Checks & exports")
    show_checks_summary(res.checks)
    if res.warnings:
        st.warning(" | ".join(res.warnings))
    st.code(payload["out_dir"])
