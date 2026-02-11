"""Q2 - Phase 2 slope and drivers."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.modules.common import assumptions_subset, robust_linreg
from src.modules.q1_transition import run_q1
from src.modules.reality_checks import build_common_checks
from src.modules.result import ModuleResult

Q2_PARAMS = [
    "min_points_regression",
    "exclude_year_2022",
]


def _driver_corr(df: pd.DataFrame, slope_col: str, driver: str) -> float:
    tmp = df[[slope_col, driver]].dropna()
    if len(tmp) < 2:
        return np.nan
    return float(tmp[slope_col].corr(tmp[driver]))


def _hourly_driver_features(hourly: pd.DataFrame) -> dict[str, float]:
    if hourly is None or hourly.empty:
        return {
            "vre_load_corr_phase2": np.nan,
            "surplus_load_trough_share_phase2": np.nan,
        }

    temp = hourly.copy()
    temp["gen_vre_mw"] = pd.to_numeric(temp.get("gen_vre_mw"), errors="coerce")
    temp["load_mw"] = pd.to_numeric(temp.get("load_mw"), errors="coerce")
    temp["surplus_mw"] = pd.to_numeric(temp.get("surplus_mw"), errors="coerce").fillna(0.0)
    temp = temp.dropna(subset=["gen_vre_mw", "load_mw"])
    if temp.empty:
        return {
            "vre_load_corr_phase2": np.nan,
            "surplus_load_trough_share_phase2": np.nan,
        }

    corr = float(temp["gen_vre_mw"].corr(temp["load_mw"])) if len(temp) >= 3 else np.nan
    p25 = float(temp["load_mw"].quantile(0.25))
    surplus_total = float(temp["surplus_mw"].sum())
    surplus_low_load = float(temp.loc[temp["load_mw"] <= p25, "surplus_mw"].sum())
    trough_share = np.nan if surplus_total <= 0 else surplus_low_load / surplus_total

    return {
        "vre_load_corr_phase2": corr,
        "surplus_load_trough_share_phase2": trough_share,
    }


def _delta_slope_two_point(x: pd.Series, y: pd.Series) -> dict[str, float]:
    tmp = pd.DataFrame({"x": pd.to_numeric(x, errors="coerce"), "y": pd.to_numeric(y, errors="coerce")}).dropna()
    n = int(len(tmp))
    if n < 2:
        return {"slope": np.nan, "intercept": np.nan, "r2": np.nan, "p_value": np.nan, "n": n}
    x0 = float(tmp["x"].iloc[0])
    x1 = float(tmp["x"].iloc[-1])
    y0 = float(tmp["y"].iloc[0])
    y1 = float(tmp["y"].iloc[-1])
    dx = x1 - x0
    if abs(dx) < 1e-12:
        return {"slope": np.nan, "intercept": np.nan, "r2": np.nan, "p_value": np.nan, "n": n}
    slope = (y1 - y0) / dx
    intercept = y0 - slope * x0
    return {"slope": float(slope), "intercept": float(intercept), "r2": np.nan, "p_value": np.nan, "n": n}


def _classify_robust_flag(n: int, p_value: float, r2: float, slope_method: str, slope: float) -> str:
    if n <= 0 or not np.isfinite(slope):
        return "NON_TESTABLE"
    if slope_method == "two_point":
        return "FRAGILE"
    if np.isfinite(p_value) and p_value > 0.25:
        return "NOT_SIGNIFICANT"
    if np.isfinite(r2) and r2 < 0.10:
        return "NOT_SIGNIFICANT"
    if n >= 6 and np.isfinite(p_value) and p_value <= 0.10 and np.isfinite(r2) and r2 >= 0.30:
        return "ROBUST"
    if (3 <= n <= 5) or (np.isfinite(p_value) and 0.10 < p_value <= 0.25) or (np.isfinite(r2) and 0.10 <= r2 < 0.30):
        return "FRAGILE"
    return "FRAGILE"


def _x_unit_for_axis(x_axis: str) -> str:
    return "pct_point" if "_pct_" in str(x_axis) else "share_point"


def _slope_conditional_ttl(gp: pd.DataFrame, x_col: str, y_col: str) -> float:
    cols = [x_col, y_col, "ttl_eur_mwh"]
    if any(c not in gp.columns for c in cols):
        return np.nan
    tmp = gp[cols].copy()
    tmp[x_col] = pd.to_numeric(tmp[x_col], errors="coerce")
    tmp[y_col] = pd.to_numeric(tmp[y_col], errors="coerce")
    tmp["ttl_eur_mwh"] = pd.to_numeric(tmp["ttl_eur_mwh"], errors="coerce")
    tmp = tmp.dropna()
    if len(tmp) < 3:
        return np.nan
    x1 = tmp[x_col].to_numpy(dtype=float)
    x2 = tmp["ttl_eur_mwh"].to_numpy(dtype=float)
    y = tmp[y_col].to_numpy(dtype=float)
    X = np.column_stack([np.ones(len(tmp)), x1, x2])
    try:
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    except Exception:
        return np.nan
    if len(beta) < 2:
        return np.nan
    return float(beta[1])


def run_q2(
    annual_df: pd.DataFrame,
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
    hourly_by_country_year: dict[tuple[str, int], pd.DataFrame] | None = None,
) -> ModuleResult:
    q1 = run_q1(annual_df, assumptions_df, selection, run_id)
    q1_panel = q1.tables["Q1_year_panel"]
    bascule = q1.tables["Q1_country_summary"][["country", "bascule_year_market"]]

    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q2_PARAMS)].iterrows()
    }
    min_points = int(params.get("min_points_regression", 3))
    exclude_2022 = int(params.get("exclude_year_2022", 0)) == 1

    countries = selection.get("countries", sorted(annual_df["country"].dropna().unique().tolist()))
    panel = annual_df[annual_df["country"].isin(countries)].copy().merge(bascule, on="country", how="left")
    panel = panel.sort_values(["country", "year"])

    rows: list[dict[str, Any]] = []
    checks: list[dict[str, str]] = []
    warnings: list[str] = []

    for country, group in panel.groupby("country"):
        bascule_year = group["bascule_year_market"].dropna()
        if bascule_year.empty:
            warnings.append(f"{country}: pas de bascule Q1, pente Q2 non calculable.")
            for tech in ["PV", "WIND"]:
                rows.append(
                    {
                        "country": country,
                        "tech": tech,
                        "x_axis_used": "none",
                        "phase2_years": "",
                        "slope": np.nan,
                        "intercept": np.nan,
                        "r2": np.nan,
                        "p_value": np.nan,
                        "n": 0,
                        "slope_method": "NONE_NO_BASCULE",
                        "robust_flag": "NON_TESTABLE",
                        "mean_sr_energy_phase2": np.nan,
                        "mean_far_energy_phase2": np.nan,
                        "mean_ir_p10_phase2": np.nan,
                        "mean_ttl_phase2": np.nan,
                        "vre_load_corr_phase2": np.nan,
                        "surplus_load_trough_share_phase2": np.nan,
                    }
                )
            continue
        start = int(bascule_year.iloc[0])
        gp = group[group["year"] >= start].copy().sort_values("year")
        if exclude_2022:
            gp = gp[gp["year"] != 2022]
        if gp.empty:
            warnings.append(f"{country}: panel Phase 2 vide apres filtrage, pente Q2 non calculable.")
            for tech in ["PV", "WIND"]:
                rows.append(
                    {
                        "country": country,
                        "tech": tech,
                        "x_axis_used": "none",
                        "phase2_years": "",
                        "slope": np.nan,
                        "intercept": np.nan,
                        "r2": np.nan,
                        "p_value": np.nan,
                        "n": 0,
                        "slope_method": "NONE_EMPTY_PANEL",
                        "robust_flag": "NON_TESTABLE",
                        "mean_sr_energy_phase2": np.nan,
                        "mean_far_energy_phase2": np.nan,
                        "mean_ir_p10_phase2": np.nan,
                        "mean_ttl_phase2": np.nan,
                        "vre_load_corr_phase2": np.nan,
                        "surplus_load_trough_share_phase2": np.nan,
                    }
                )
            continue

        hourly_phase2 = []
        if hourly_by_country_year is not None:
            for y in gp["year"].dropna().astype(int).tolist():
                key = (country, y)
                if key in hourly_by_country_year:
                    h = hourly_by_country_year[key].copy()
                    h["year"] = y
                    hourly_phase2.append(h)
        hourly_concat = pd.concat(hourly_phase2, ignore_index=False) if hourly_phase2 else pd.DataFrame()
        h_features = _hourly_driver_features(hourly_concat)

        for tech in ["PV", "WIND"]:
            if tech == "PV":
                x = pd.to_numeric(gp.get("pv_penetration_pct_gen"), errors="coerce")
                y = pd.to_numeric(gp.get("capture_ratio_pv_vs_ttl"), errors="coerce")
                x_axis = "pv_penetration_pct_gen"
                y_col = "capture_ratio_pv_vs_ttl"
            else:
                x = pd.to_numeric(gp.get("wind_penetration_pct_gen"), errors="coerce")
                y = pd.to_numeric(gp.get("capture_ratio_wind_vs_ttl"), errors="coerce")
                x_axis = "wind_penetration_pct_gen"
                y_col = "capture_ratio_wind_vs_ttl"

            if x.notna().sum() < min_points:
                x = pd.to_numeric(gp.get("sr_energy"), errors="coerce")
                x_axis = "sr_energy"

            reg = robust_linreg(x, y)
            slope_method = "OLS"
            if reg["n"] == 2:
                # With two horizon points (typical in SCEN), expose directional slope via delta.
                reg_delta = _delta_slope_two_point(x, y)
                if np.isfinite(reg_delta["slope"]):
                    reg = reg_delta
                    slope_method = "two_point"
            robust_flag = _classify_robust_flag(
                n=int(reg["n"]),
                p_value=float(reg.get("p_value", np.nan)),
                r2=float(reg.get("r2", np.nan)),
                slope_method=slope_method,
                slope=float(reg.get("slope", np.nan)),
            )
            slope_conditional_ttl = _slope_conditional_ttl(gp, x_axis, y_col)
            x_unit = _x_unit_for_axis(x_axis)

            if robust_flag == "FRAGILE":
                checks.append({"status": "WARN", "code": "Q2_FRAGILE", "message": f"{country}-{tech}: n={reg['n']} < {min_points}."})
            if robust_flag == "NOT_SIGNIFICANT":
                checks.append({"status": "WARN", "code": "Q2_NOT_SIGNIFICANT", "message": f"{country}-{tech}: signal statistique faible (p-value/R2)."})
            if tech == "PV" and np.isfinite(reg["slope"]) and reg["slope"] > 0 and reg.get("p_value", 1.0) < 0.05:
                checks.append({"status": "WARN", "code": "Q2_POSITIVE_PV_SLOPE", "message": f"{country}: slope PV positive et significative."})
            if np.isfinite(reg.get("r2", np.nan)) and reg["r2"] < 0.1:
                checks.append({"status": "INFO", "code": "Q2_LOW_R2", "message": f"{country}-{tech}: R2 faible ({reg['r2']:.2f})."})

            rows.append(
                {
                    "country": country,
                    "tech": tech,
                    "x_axis_used": x_axis,
                    "x_unit": x_unit,
                    "phase2_years": f"{int(gp['year'].min())}-{int(gp['year'].max())}" if not gp.empty else "",
                    "slope": reg["slope"],
                    "slope_simple": reg["slope"],
                    "slope_conditional_ttl": slope_conditional_ttl,
                    "intercept": reg["intercept"],
                    "r2": reg["r2"],
                    "p_value": reg["p_value"],
                    "n": reg["n"],
                    "slope_method": slope_method,
                    "robust_flag": robust_flag,
                    "mean_sr_energy_phase2": float(pd.to_numeric(gp.get("sr_energy"), errors="coerce").mean()),
                    "mean_far_energy_phase2": float(pd.to_numeric(gp.get("far_energy"), errors="coerce").mean()),
                    "mean_ir_p10_phase2": float(pd.to_numeric(gp.get("ir_p10"), errors="coerce").mean()),
                    "mean_ttl_phase2": float(pd.to_numeric(gp.get("ttl_eur_mwh"), errors="coerce").mean()),
                    "vre_load_corr_phase2": h_features["vre_load_corr_phase2"],
                    "surplus_load_trough_share_phase2": h_features["surplus_load_trough_share_phase2"],
                }
            )

    slopes = pd.DataFrame(rows)
    if slopes.empty:
        checks.append({"status": "WARN", "code": "Q2_NO_SLOPE", "message": "Aucune pente Q2 n'a pu etre calculee."})

    drivers = []
    driver_names = [
        "mean_sr_energy_phase2",
        "mean_far_energy_phase2",
        "mean_ir_p10_phase2",
        "mean_ttl_phase2",
        "vre_load_corr_phase2",
        "surplus_load_trough_share_phase2",
    ]
    for driver in driver_names:
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

    checks.extend(build_common_checks(q1_panel))
    if not checks:
        checks.append({"status": "PASS", "code": "Q2_PASS", "message": "Q2 checks pass."})

    kpis = {
        "n_slopes": int(len(slopes)),
        "n_robust": int((slopes.get("robust_flag") == "ROBUST").sum()) if not slopes.empty else 0,
    }

    narrative = (
        "Q2 mesure la pente empirique de cannibalisation apres bascule Q1 "
        "et classe les drivers transverses (SR/FAR/IR/correlation charge-VRE)."
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
        warnings=warnings,
        mode=str(selection.get("mode", "HIST")).upper(),
        scenario_id=selection.get("scenario_id"),
        horizon_year=selection.get("horizon_year"),
    )
