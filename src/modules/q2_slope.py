"""Q2 - Phase 2 slope and drivers."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.modules.common import assumptions_subset, robust_linreg
from src.modules.q1_transition import run_q1
from src.modules.result import ModuleResult

Q2_PARAMS = ["min_points_regression"]


def _driver_corr(df: pd.DataFrame, slope_col: str, driver: str) -> float:
    tmp = df[[slope_col, driver]].dropna()
    if len(tmp) < 2:
        return np.nan
    return float(tmp[slope_col].corr(tmp[driver]))


def run_q2(annual_df: pd.DataFrame, assumptions_df: pd.DataFrame, selection: dict[str, Any], run_id: str) -> ModuleResult:
    q1 = run_q1(annual_df, assumptions_df, selection, run_id)
    bascule = q1.tables["Q1_country_summary"][["country", "bascule_year_market"]]

    params = {
        r["param_name"]: float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q2_PARAMS)].iterrows()
    }
    min_points = int(params.get("min_points_regression", 3))

    countries = selection.get("countries", sorted(annual_df["country"].unique()))
    panel = annual_df[annual_df["country"].isin(countries)].copy().merge(bascule, on="country", how="left")

    rows = []
    checks = []
    for country, group in panel.groupby("country"):
        bascule_year = group["bascule_year_market"].dropna()
        if bascule_year.empty:
            continue
        start = int(bascule_year.iloc[0])
        gp = group[group["year"] >= start].sort_values("year")

        for tech in ["PV", "WIND"]:
            if tech == "PV":
                x = gp["pv_penetration_pct_gen"].copy()
                y = gp["capture_ratio_pv_vs_ttl"].copy()
                x_axis = "pv_penetration_pct_gen"
            else:
                x = gp["wind_penetration_pct_gen"].copy()
                y = gp["capture_ratio_wind_vs_ttl"].copy()
                x_axis = "wind_penetration_pct_gen"

            if x.dropna().empty:
                x = gp["vre_penetration_proxy"].copy()
                x_axis = "vre_penetration_proxy"

            reg = robust_linreg(x, y)
            robust_flag = "ROBUST" if reg["n"] >= min_points else "FRAGILE"

            if tech == "PV" and np.isfinite(reg["slope"]) and reg["slope"] > 0 and reg.get("p_value", 1.0) < 0.05:
                checks.append({"status": "WARN", "message": f"{country} PV slope positive and significant"})
            if np.isfinite(reg.get("r2", np.nan)) and reg["r2"] < 0.1:
                checks.append({"status": "INFO", "message": f"{country} {tech} low linear explanatory power"})

            rows.append(
                {
                    "country": country,
                    "tech": tech,
                    "x_axis_used": x_axis,
                    "phase2_years": f"{int(gp['year'].min())}-{int(gp['year'].max())}" if not gp.empty else "",
                    "slope": reg["slope"],
                    "intercept": reg["intercept"],
                    "r2": reg["r2"],
                    "p_value": reg["p_value"],
                    "n": reg["n"],
                    "robust_flag": robust_flag,
                    "mean_sr_energy_phase2": float(gp["sr_energy"].mean()),
                    "mean_far_energy_phase2": float(gp["far_energy"].mean()),
                    "mean_ir_p10_phase2": float(gp["ir_p10"].mean()),
                    "mean_ttl_phase2": float(gp["ttl_eur_mwh"].mean()),
                    "vre_load_corr_phase2": float(gp["nrl_price_corr"].mean()),
                }
            )

    slopes = pd.DataFrame(rows)

    drivers = []
    for driver in ["mean_sr_energy_phase2", "mean_far_energy_phase2", "mean_ir_p10_phase2", "mean_ttl_phase2", "vre_load_corr_phase2"]:
        pv_corr = _driver_corr(slopes[slopes["tech"] == "PV"], "slope", driver) if not slopes.empty else np.nan
        wind_corr = _driver_corr(slopes[slopes["tech"] == "WIND"], "slope", driver) if not slopes.empty else np.nan
        drivers.append(
            {
                "driver_name": driver,
                "corr_with_slope_pv": pv_corr,
                "corr_with_slope_wind": wind_corr,
                "n_countries": int(slopes["country"].nunique()) if not slopes.empty else 0,
            }
        )

    driver_corr = pd.DataFrame(drivers)
    if not checks:
        checks.append({"status": "PASS", "message": "Q2 checks pass"})

    kpis = {
        "n_slopes": int(len(slopes)),
        "n_robust": int((slopes.get("robust_flag") == "ROBUST").sum()) if not slopes.empty else 0,
    }

    narrative = (
        "Q2 estimates post-transition cannibalization slope and ranks cross-country drivers. "
        "Slope is robust when at least 3 historical points are available in Phase 2."
    )

    return ModuleResult(
        module_id="Q2",
        run_id=run_id,
        selection=selection,
        assumptions_used=assumptions_subset(assumptions_df, Q2_PARAMS),
        kpis=kpis,
        tables={"Q2_country_slopes": slopes, "Q2_driver_correlations": driver_corr},
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=[],
    )
