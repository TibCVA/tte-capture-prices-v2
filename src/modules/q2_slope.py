"""Q2 - Phase 2 slope diagnostics (capture vs penetration)."""

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


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


def _phase2_start_year(country_summary: pd.DataFrame, tech: str) -> tuple[float, str]:
    t = str(tech).upper()
    tech_col = "bascule_year_market_pv" if t == "PV" else "bascule_year_market_wind"
    fallback_col = "bascule_year_market_country" if "bascule_year_market_country" in country_summary.columns else "bascule_year_market"
    if country_summary.empty:
        return float("nan"), "q1_no_bascule"
    if tech_col in country_summary.columns:
        bascule = _safe_float(country_summary[tech_col].iloc[0], np.nan)
        if np.isfinite(bascule):
            return float(int(bascule)), f"q1_bascule_{t.lower()}"
    bascule = _safe_float(country_summary.get(fallback_col, pd.Series([np.nan])).iloc[0], np.nan)
    if not np.isfinite(bascule):
        return float("nan"), "q1_no_bascule"
    return float(int(bascule)), "q1_bascule_country_fallback"


def _delta_slope_two_point(df_xy: pd.DataFrame) -> dict[str, Any]:
    if len(df_xy) != 2:
        return {
            "slope": np.nan,
            "intercept": np.nan,
            "r2": np.nan,
            "p_value": np.nan,
            "n": int(len(df_xy)),
            "slope_method": "none",
            "insufficient_points": True,
            "reason_code": "insufficient_points",
        }
    x0 = _safe_float(df_xy["x"].iloc[0], np.nan)
    x1 = _safe_float(df_xy["x"].iloc[1], np.nan)
    y0 = _safe_float(df_xy["y"].iloc[0], np.nan)
    y1 = _safe_float(df_xy["y"].iloc[1], np.nan)
    dx = x1 - x0
    if not np.isfinite(dx) or abs(dx) < 1e-12:
        return {
            "slope": np.nan,
            "intercept": np.nan,
            "r2": np.nan,
            "p_value": np.nan,
            "n": 2,
            "slope_method": "none",
            "insufficient_points": True,
            "reason_code": "x_constant",
        }
    slope = (y1 - y0) / dx
    intercept = y0 - slope * x0
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "r2": np.nan,
        "p_value": np.nan,
        "n": 2,
        "slope_method": "two_point",
        "insufficient_points": True,
        "reason_code": "insufficient_points",
    }


def _fit_slope(df_xy: pd.DataFrame, min_points: int) -> dict[str, Any]:
    n = int(len(df_xy))
    if n >= max(3, int(min_points)) and df_xy["x"].nunique(dropna=True) > 1:
        reg = robust_linreg(df_xy["x"], df_xy["y"])
        return {
            "slope": _safe_float(reg.get("slope"), np.nan),
            "intercept": _safe_float(reg.get("intercept"), np.nan),
            "r2": _safe_float(reg.get("r2"), np.nan),
            "p_value": _safe_float(reg.get("p_value"), np.nan),
            "n": int(reg.get("n", n)),
            "slope_method": "ols",
            "insufficient_points": False,
            "reason_code": "ok",
        }
    if n == 2:
        return _delta_slope_two_point(df_xy)
    return {
        "slope": np.nan,
        "intercept": np.nan,
        "r2": np.nan,
        "p_value": np.nan,
        "n": n,
        "slope_method": "none",
        "insufficient_points": True,
        "reason_code": "insufficient_points",
    }


def _robust_flag(fit: dict[str, Any]) -> str:
    method = str(fit.get("slope_method", "insufficient"))
    if method == "ols":
        p_val = _safe_float(fit.get("p_value"), np.nan)
        r2 = _safe_float(fit.get("r2"), np.nan)
        if np.isfinite(p_val) and np.isfinite(r2) and p_val <= 0.10 and r2 >= 0.10:
            return "ROBUST"
        return "NOT_SIGNIFICANT"
    if method == "two_point":
        return "FRAGILE"
    return "NON_TESTABLE"


def _corr_and_elasticity(y: pd.Series, x: pd.Series) -> tuple[float, float]:
    tmp = pd.DataFrame({"y": pd.to_numeric(y, errors="coerce"), "x": pd.to_numeric(x, errors="coerce")}).dropna()
    if len(tmp) < 3:
        return np.nan, np.nan
    corr = float(tmp["y"].corr(tmp["x"]))
    sx = float(tmp["x"].std(ddof=0))
    sy = float(tmp["y"].std(ddof=0))
    mx = float(tmp["x"].mean())
    my = float(tmp["y"].mean())
    if sx <= 0 or sy <= 0 or my == 0:
        return corr, np.nan
    elasticity = corr * (sy / sx) * (mx / my)
    return corr, float(elasticity)


def run_q2(
    annual_df: pd.DataFrame,
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
    hourly_by_country_year: dict[tuple[str, int], pd.DataFrame] | None = None,
    validation_findings_df: pd.DataFrame | None = None,
) -> ModuleResult:
    q1 = run_q1(
        annual_df,
        assumptions_df,
        selection,
        run_id,
        hourly_by_country_year=hourly_by_country_year,
        validation_findings_df=validation_findings_df,
    )
    q1_panel = q1.tables["Q1_year_panel"].copy()
    q1_summary_cols = [c for c in ["country", "bascule_year_market", "bascule_year_market_country", "bascule_year_market_pv", "bascule_year_market_wind"] if c in q1.tables["Q1_country_summary"].columns]
    q1_summary = q1.tables["Q1_country_summary"][q1_summary_cols].copy()

    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q2_PARAMS)].iterrows()
    }
    min_points = max(3, int(params.get("min_points_regression", 3)))
    exclude_2022 = int(params.get("exclude_year_2022", 0)) == 1

    countries = selection.get("countries", sorted(annual_df["country"].dropna().unique().tolist()))
    panel = annual_df[annual_df["country"].isin(countries)].copy()
    panel = panel.merge(
        q1_panel[
            [
                "country",
                "year",
                "quality_ok",
                "crisis_year",
                "capture_ratio_pv",
                "capture_ratio_wind",
                "pv_penetration_pct_gen",
                "wind_penetration_pct_gen",
                "sr_energy",
                "far_observed",
                "ir_p10",
                "ttl_eur_mwh",
            ]
        ],
        on=["country", "year"],
        how="left",
        suffixes=("", "_q1"),
    )
    panel = panel.merge(q1_summary, on="country", how="left")
    panel = panel.sort_values(["country", "year"]).reset_index(drop=True)

    rows: list[dict[str, Any]] = []
    checks: list[dict[str, str]] = []
    warnings: list[str] = []
    drivers_rows: list[dict[str, Any]] = []

    for country, group in panel.groupby("country"):
        group = group.sort_values("year").copy()
        start_cols = [c for c in ["bascule_year_market_pv", "bascule_year_market_wind", "bascule_year_market_country", "bascule_year_market"] if c in group.columns]
        for tech in ["PV", "WIND"]:
            start_year, start_reason = _phase2_start_year(group[start_cols], tech=tech)
            if not np.isfinite(start_year):
                warnings.append(f"{country}-{tech}: bascule Q1 absente, pente non calculee.")
                rows.append(
                    {
                        "country": country,
                        "tech": tech,
                        "phase2_start_year_for_slope": np.nan,
                        "phase2_start_reason": start_reason,
                        "phase2_end_year": np.nan,
                        "years_used": "",
                        "n_points": 0,
                        "x_axis_used": "none",
                        "x_unit": "pct_point",
                        "slope": np.nan,
                        "intercept": np.nan,
                        "r2": np.nan,
                        "p_value": np.nan,
                        "n": 0,
                        "slope_method": "none",
                        "method": "none",
                        "insufficient_points": True,
                        "robust_flag": "NON_TESTABLE",
                        "reason_code": "q1_no_bascule",
                        "outlier_years_count": 0,
                        "slope_all_years": np.nan,
                        "slope_excluding_outliers": np.nan,
                        "mean_sr_energy_phase2": np.nan,
                        "mean_far_energy_phase2": np.nan,
                        "mean_ir_p10_phase2": np.nan,
                        "mean_ttl_phase2": np.nan,
                        "vre_load_corr_phase2": np.nan,
                        "surplus_load_trough_share_phase2": np.nan,
                    }
                )
                continue

            gp = group[group["year"] >= int(start_year)].copy()
            gp["quality_ok"] = gp.get("quality_ok", True).fillna(False).astype(bool)
            gp["crisis_year"] = gp.get("crisis_year", False).fillna(False).astype(bool)
            gp = gp[gp["quality_ok"] & (~gp["crisis_year"])]
            if exclude_2022:
                gp = gp[pd.to_numeric(gp["year"], errors="coerce") != 2022]
            gp = gp.sort_values("year")

            if tech == "PV":
                x = pd.to_numeric(gp.get("pv_penetration_pct_gen"), errors="coerce")
                y = pd.to_numeric(gp.get("capture_ratio_pv"), errors="coerce")
                x_axis = "pv_penetration_pct_gen"
            else:
                x = pd.to_numeric(gp.get("wind_penetration_pct_gen"), errors="coerce")
                y = pd.to_numeric(gp.get("capture_ratio_wind"), errors="coerce")
                x_axis = "wind_penetration_pct_gen"

            # Compatibility fallback: if penetration axis is unavailable, fall back to SR proxy.
            if x.notna().sum() == 0:
                x = pd.to_numeric(gp.get("sr_energy"), errors="coerce")
                x_axis = "sr_energy"

            fit_df = pd.DataFrame(
                {
                    "year": pd.to_numeric(gp.get("year"), errors="coerce"),
                    "x": x,
                    "y": y,
                }
            ).dropna()
            fit = _fit_slope(fit_df, min_points=min_points)
            fit["robust_flag"] = _robust_flag(fit)

            years_used = ",".join([str(int(v)) for v in fit_df["year"].tolist()])
            phase2_end = int(fit_df["year"].max()) if not fit_df.empty else np.nan

            rows.append(
                {
                    "country": country,
                    "tech": tech,
                    "phase2_start_year_for_slope": float(start_year),
                    "phase2_start_reason": start_reason,
                    "phase2_end_year": phase2_end,
                    "years_used": years_used,
                    "n_points": int(fit["n"]),
                    "x_axis_used": x_axis,
                    "x_unit": "pct_point",
                    "slope": fit["slope"],
                    "intercept": fit["intercept"],
                    "r2": fit["r2"],
                    "p_value": fit["p_value"],
                    "n": int(fit["n"]),
                    "slope_method": fit["slope_method"],
                    "method": fit["slope_method"],
                    "insufficient_points": bool(fit["insufficient_points"]),
                    "robust_flag": fit["robust_flag"],
                    "reason_code": fit["reason_code"],
                    "outlier_years_count": 0,
                    "slope_all_years": fit["slope"],
                    "slope_excluding_outliers": fit["slope"],
                    "mean_sr_energy_phase2": _safe_float(pd.to_numeric(gp.get("sr_energy"), errors="coerce").mean(), np.nan),
                    "mean_far_energy_phase2": _safe_float(pd.to_numeric(gp.get("far_observed"), errors="coerce").mean(), np.nan),
                    "mean_ir_p10_phase2": _safe_float(pd.to_numeric(gp.get("ir_p10"), errors="coerce").mean(), np.nan),
                    "mean_ttl_phase2": _safe_float(pd.to_numeric(gp.get("ttl_eur_mwh"), errors="coerce").mean(), np.nan),
                    "vre_load_corr_phase2": np.nan,
                    "surplus_load_trough_share_phase2": np.nan,
                }
            )

            if (
                int(fit["n"]) >= 3
                and str(fit["slope_method"]) == "ols"
                and str(fit["robust_flag"]) == "ROBUST"
                and np.isfinite(_safe_float(fit["slope"], np.nan))
                and _safe_float(fit["slope"], np.nan) > 0.0
            ):
                checks.append(
                    {
                        "status": "WARN",
                        "code": "Q2_POSITIVE_ROBUST_SLOPE",
                        "message": f"{country}-{tech}: pente robuste positive (exception possible meteo/structure).",
                    }
                )

            if int(fit["n"]) < 3 and str(fit["slope_method"]) == "ols":
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "Q2_N_LT_3_WITH_OLS",
                        "message": f"{country}-{tech}: OLS interdit si n<3.",
                    }
                )
            if int(fit["n"]) < 3 and np.isfinite(_safe_float(fit["p_value"], np.nan)):
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "Q2_N_LT_3_WITH_PVALUE",
                        "message": f"{country}-{tech}: p_value doit etre NaN si n<3.",
                    }
                )
            if int(fit["n"]) == 2:
                xvals = fit_df["x"].to_numpy(dtype=float)
                if len(xvals) == 2 and abs(float(xvals[1] - xvals[0])) > 1e-12 and not np.isfinite(_safe_float(fit["slope"], np.nan)):
                    checks.append(
                        {
                            "status": "FAIL",
                            "code": "Q2_TWO_POINT_SLOPE_NAN",
                            "message": f"{country}-{tech}: pente doit etre finie en two-point si x varie.",
                        }
                    )

        # Driver diagnostics use country-level post-bascule country window.
        start_country, _ = _phase2_start_year(group[start_cols], tech="PV")
        gp_drv = group[group["year"] >= int(start_country)].copy() if np.isfinite(start_country) else group.iloc[0:0].copy()
        gp_drv["quality_ok"] = gp_drv.get("quality_ok", True).fillna(False).astype(bool)
        gp_drv["crisis_year"] = gp_drv.get("crisis_year", False).fillna(False).astype(bool)
        gp_drv = gp_drv[gp_drv["quality_ok"] & (~gp_drv["crisis_year"])].sort_values("year")
        y_drv = pd.to_numeric(gp_drv.get("capture_ratio_pv"), errors="coerce")
        var_map = {
            "sr_energy": pd.to_numeric(gp_drv.get("sr_energy"), errors="coerce"),
            "far_energy": pd.to_numeric(gp_drv.get("far_observed"), errors="coerce"),
            "vre_penetration_share_gen": pd.to_numeric(gp_drv.get("vre_penetration_share_gen"), errors="coerce"),
            "ir_p10": pd.to_numeric(gp_drv.get("ir_p10"), errors="coerce"),
        }
        for name, x_drv in var_map.items():
            corr, elast = _corr_and_elasticity(y_drv, x_drv)
            drivers_rows.append(
                {
                    "country": country,
                    "driver_name": name,
                    "corr_capture_pv": corr,
                    "elasticity_capture_pv": elast,
                    "expected_sign": np.nan,
                    "observed_sign": 0 if not np.isfinite(corr) or abs(corr) < 1e-9 else (1 if corr > 0 else -1),
                    "sign_conflict": False,
                }
            )

    slopes = pd.DataFrame(rows)
    drivers_country = pd.DataFrame(drivers_rows)
    driver_corr_rows: list[dict[str, Any]] = []
    if not drivers_country.empty and not slopes.empty:
        pv_scope = slopes[slopes["tech"] == "PV"][["country", "slope"]].copy()
        for drv, grp in drivers_country.groupby("driver_name"):
            merged = pv_scope.merge(grp[["country", "corr_capture_pv"]], on="country", how="left")
            corr_with_slope = float(merged["slope"].corr(merged["corr_capture_pv"])) if len(merged.dropna()) >= 2 else np.nan
            driver_corr_rows.append(
                {
                    "driver_name": drv,
                    "corr_with_slope_pv": corr_with_slope,
                    "corr_with_slope_wind": np.nan,
                    "n_countries": int(slopes["country"].nunique()),
                    "expected_sign": np.nan,
                    "sign_conflict_share": 0.0,
                }
            )
    driver_corr = pd.DataFrame(driver_corr_rows)

    checks.extend(build_common_checks(q1_panel))
    if slopes.empty:
        checks.append({"status": "WARN", "code": "Q2_NO_SLOPE", "message": "Aucune pente Q2 calculee."})
    if not checks:
        checks.append({"status": "PASS", "code": "Q2_PASS", "message": "Q2 checks pass."})

    kpis = {
        "n_slopes": int(len(slopes)),
        "n_robust": int((slopes.get("robust_flag") == "ROBUST").sum()) if not slopes.empty else 0,
    }

    narrative = (
        "Q2 estime la pente de cannibalisation sur la fenetre post-bascule Q1 (phase 2), "
        "en excluant annees de crise et qualite insuffisante; OLS si n>=3, two-point delta si n=2."
    )

    return ModuleResult(
        module_id="Q2",
        run_id=run_id,
        selection=selection,
        assumptions_used=assumptions_subset(assumptions_df, Q2_PARAMS),
        kpis=kpis,
        tables={
            "Q2_country_slopes": slopes,
            "Q2_driver_correlations": driver_corr,
            "Q2_driver_diagnostics": drivers_country,
        },
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
        mode=str(selection.get("mode", "HIST")).upper(),
        scenario_id=selection.get("scenario_id"),
        horizon_year=selection.get("horizon_year"),
    )
