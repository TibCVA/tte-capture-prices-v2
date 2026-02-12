"""Q2 - Phase 2 slope diagnostics (capture vs penetration)."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import t as t_dist

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


def _to_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    txt = str(value).strip().lower()
    if txt in {"1", "true", "yes", "y", "on"}:
        return True
    if txt in {"0", "false", "no", "n", "off"}:
        return False
    return default


def _years_from_csv(value: Any) -> list[int]:
    txt = str(value).strip()
    if not txt:
        return []
    out: list[int] = []
    for tok in txt.split(","):
        v = _safe_float(tok.strip(), np.nan)
        if np.isfinite(v):
            out.append(int(v))
    return out


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


def _endpoint_slope(df_xy: pd.DataFrame) -> dict[str, Any]:
    n = int(len(df_xy))
    if n not in {2, 3}:
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
    ordered = df_xy.sort_values("year").copy()
    x0 = _safe_float(ordered["x"].iloc[0], np.nan)
    x1 = _safe_float(ordered["x"].iloc[-1], np.nan)
    y0 = _safe_float(ordered["y"].iloc[0], np.nan)
    y1 = _safe_float(ordered["y"].iloc[-1], np.nan)
    dx = x1 - x0
    if not np.isfinite(dx) or abs(dx) < 1e-12:
        return {
            "slope": np.nan,
            "intercept": np.nan,
            "r2": np.nan,
            "p_value": np.nan,
            "n": n,
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
        "n": n,
        "slope_method": "endpoint_delta",
        "insufficient_points": True,
        "reason_code": "insufficient_points",
    }


def _fit_slope(df_xy: pd.DataFrame, min_points: int) -> dict[str, Any]:
    n = int(len(df_xy))
    if n >= max(4, int(min_points)) and df_xy["x"].nunique(dropna=True) > 1:
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
    if n in {2, 3}:
        return _endpoint_slope(df_xy)
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
    if method == "endpoint_delta":
        return "FRAGILE"
    return "NON_TESTABLE"


def _as_share(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    if s.notna().sum() == 0:
        return s
    q = float(s.dropna().quantile(0.9))
    if q > 1.5:
        return s / 100.0
    return s


def _as_numeric_series(df: pd.DataFrame, col: str, default: float = np.nan) -> pd.Series:
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    return pd.Series(default, index=df.index, dtype=float)


def _panel_fixed_effect_slope(df_xy_country: pd.DataFrame) -> dict[str, Any]:
    tmp = df_xy_country.copy()
    tmp["x"] = pd.to_numeric(tmp["x"], errors="coerce")
    tmp["y"] = pd.to_numeric(tmp["y"], errors="coerce")
    tmp["country"] = tmp["country"].astype(str)
    tmp = tmp.dropna(subset=["x", "y", "country"])
    if len(tmp) < 4 or tmp["country"].nunique() < 2:
        return {"slope": np.nan, "r2": np.nan, "p_value": np.nan, "n": int(len(tmp)), "reason": "insufficient_panel_points"}

    x_dm = tmp["x"] - tmp.groupby("country")["x"].transform("mean")
    y_dm = tmp["y"] - tmp.groupby("country")["y"].transform("mean")
    den = float(np.sum(np.square(x_dm.to_numpy(dtype=float))))
    if abs(den) < 1e-12:
        return {"slope": np.nan, "r2": np.nan, "p_value": np.nan, "n": int(len(tmp)), "reason": "x_within_constant"}

    slope = float(np.sum(x_dm.to_numpy(dtype=float) * y_dm.to_numpy(dtype=float)) / den)
    resid = y_dm.to_numpy(dtype=float) - slope * x_dm.to_numpy(dtype=float)
    ss_res = float(np.sum(np.square(resid)))
    ss_tot = float(np.sum(np.square(y_dm.to_numpy(dtype=float))))
    r2 = float(1.0 - (ss_res / ss_tot)) if ss_tot > 1e-12 else np.nan
    dof = int(len(tmp) - tmp["country"].nunique() - 1)
    if dof > 0:
        sigma2 = ss_res / dof
        se = np.sqrt(max(sigma2 / den, 0.0))
        if se > 0:
            t_stat = slope / se
            p_value = float(2.0 * (1.0 - t_dist.cdf(abs(t_stat), dof)))
        else:
            p_value = np.nan
    else:
        p_value = np.nan

    return {"slope": slope, "r2": r2, "p_value": p_value, "n": int(len(tmp)), "reason": "ok"}


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

    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q2_PARAMS)].iterrows()
    }
    min_points = max(4, int(params.get("min_points_regression", 4)))
    exclude_2022 = int(params.get("exclude_year_2022", 1)) == 1
    include_2022 = _to_bool(selection.get("include_2022"), default=False)
    if include_2022:
        exclude_2022 = False

    countries = selection.get("countries", sorted(annual_df["country"].dropna().unique().tolist()))
    panel = annual_df[annual_df["country"].isin(countries)].copy()
    q1_cols = [
        "country",
        "year",
        "quality_ok",
        "crisis_year",
        "is_phase2_market",
        "capture_ratio_pv",
        "capture_ratio_wind",
        "sr_energy",
        "far_observed",
        "ir_p10",
        "ttl_eur_mwh",
    ]
    panel = panel.merge(
        q1_panel[[c for c in q1_cols if c in q1_panel.columns]],
        on=["country", "year"],
        how="left",
        suffixes=("", "_q1"),
    )
    panel = panel.sort_values(["country", "year"]).reset_index(drop=True)

    load_twh = _as_numeric_series(panel, "load_net_twh", np.nan)
    pv_twh = _as_numeric_series(panel, "gen_solar_twh", np.nan)
    wind_twh = _as_numeric_series(panel, "gen_wind_on_twh", 0.0).fillna(0.0) + _as_numeric_series(panel, "gen_wind_off_twh", 0.0).fillna(0.0)
    panel["pv_penetration_share_load"] = pv_twh / load_twh.replace(0.0, np.nan)
    panel["wind_penetration_share_load"] = wind_twh / load_twh.replace(0.0, np.nan)
    panel["pv_penetration_share_load"] = panel["pv_penetration_share_load"].fillna(_as_share(panel.get("pv_penetration_pct_gen", pd.Series(np.nan, index=panel.index))))
    panel["wind_penetration_share_load"] = panel["wind_penetration_share_load"].fillna(
        _as_share(panel.get("wind_penetration_pct_gen", pd.Series(np.nan, index=panel.index)))
    )

    rows: list[dict[str, Any]] = []
    checks: list[dict[str, str]] = []
    warnings: list[str] = []
    drivers_rows: list[dict[str, Any]] = []
    phase2_benchmark_rows: dict[str, list[pd.DataFrame]] = {"PV": [], "WIND": []}
    if include_2022:
        warnings.append("includes_2022_outlier")
        checks.append(
            {
                "status": "WARN",
                "code": "includes_2022_outlier",
                "message": "include_2022=true: l'outlier 2022 est inclus dans les pentes Q2.",
            }
        )

    for country, group in panel.groupby("country"):
        group = group.sort_values("year").copy()
        for tech in ["PV", "WIND"]:
            phase2_mask = group.get("is_phase2_market", False).fillna(False).astype(bool)
            phase2_scope = group[phase2_mask].copy()
            phase2_scope["quality_ok"] = phase2_scope.get("quality_ok", True).fillna(False).astype(bool)
            phase2_scope["crisis_year"] = phase2_scope.get("crisis_year", False).fillna(False).astype(bool)
            phase2_scope["year_num"] = pd.to_numeric(phase2_scope.get("year"), errors="coerce")
            crisis_override_2022 = include_2022 & (phase2_scope["year_num"] == 2022)
            phase2_scope = phase2_scope[phase2_scope["quality_ok"] & ((~phase2_scope["crisis_year"]) | crisis_override_2022)]
            if exclude_2022:
                phase2_scope = phase2_scope[phase2_scope["year_num"] != 2022]
            phase2_scope = phase2_scope.sort_values("year")

            if phase2_scope.empty:
                warnings.append(f"{country}-{tech}: aucun point phase2 Q1 exploitable.")
                rows.append(
                    {
                        "country": country,
                        "tech": tech,
                        "phase2_start_year_for_slope": np.nan,
                        "phase2_start_reason": "q1_no_phase2_market_year",
                        "phase2_end_year": np.nan,
                        "years_used": "",
                        "n_points": 0,
                        "x_axis_used": "none",
                        "x_unit": "share_of_load",
                        "slope": np.nan,
                        "intercept": np.nan,
                        "r2": np.nan,
                        "p_value": np.nan,
                        "n": 0,
                        "slope_method": "none",
                        "method": "none",
                        "insufficient_points": True,
                        "robust_flag": "NON_TESTABLE",
                        "reason_code": "q1_no_phase2_market_year",
                        "outlier_years_count": 0,
                        "slope_all_years": np.nan,
                        "slope_excluding_outliers": np.nan,
                        "mean_sr_energy_phase2": np.nan,
                        "mean_far_energy_phase2": np.nan,
                        "mean_ir_p10_phase2": np.nan,
                        "mean_ttl_phase2": np.nan,
                        "vre_load_corr_phase2": np.nan,
                        "surplus_load_trough_share_phase2": np.nan,
                        "cross_country_benchmark_slope": np.nan,
                        "cross_country_benchmark_r2": np.nan,
                        "cross_country_benchmark_p_value": np.nan,
                        "cross_country_benchmark_n": np.nan,
                    }
                )
                continue

            if tech == "PV":
                x = (
                    pd.to_numeric(phase2_scope["pv_penetration_share_load"], errors="coerce")
                    if "pv_penetration_share_load" in phase2_scope.columns
                    else pd.Series(np.nan, index=phase2_scope.index)
                )
                y = (
                    pd.to_numeric(phase2_scope["capture_ratio_pv"], errors="coerce")
                    if "capture_ratio_pv" in phase2_scope.columns
                    else pd.Series(np.nan, index=phase2_scope.index)
                )
                x_axis = "pv_penetration_share_load"
            else:
                x = (
                    pd.to_numeric(phase2_scope["wind_penetration_share_load"], errors="coerce")
                    if "wind_penetration_share_load" in phase2_scope.columns
                    else pd.Series(np.nan, index=phase2_scope.index)
                )
                y = (
                    pd.to_numeric(phase2_scope["capture_ratio_wind"], errors="coerce")
                    if "capture_ratio_wind" in phase2_scope.columns
                    else pd.Series(np.nan, index=phase2_scope.index)
                )
                x_axis = "wind_penetration_share_load"

            fit_df = pd.DataFrame(
                {
                    "country": country,
                    "year": pd.to_numeric(phase2_scope.get("year"), errors="coerce"),
                    "x": x,
                    "y": y,
                }
            ).dropna()
            fit = _fit_slope(fit_df, min_points=min_points)
            fit["robust_flag"] = _robust_flag(fit)
            if str(fit.get("slope_method", "")) == "ols":
                slope_quality_notes = "ols_ok" if np.isfinite(_safe_float(fit.get("r2"), np.nan)) else "ols_missing_r2"
            elif str(fit.get("slope_method", "")) == "endpoint_delta":
                slope_quality_notes = "ols_not_possible_n_lt_4"
            else:
                slope_quality_notes = str(fit.get("reason_code", "insufficient_points"))
            slope_quality_flag = "PASS" if slope_quality_notes == "ols_ok" else ("WARN" if slope_quality_notes else "FAIL")

            corr_vre_load_phase2 = np.nan
            if {"gen_vre_twh", "load_net_twh"}.issubset(set(phase2_scope.columns)):
                corr_vre_load_phase2 = _safe_float(
                    pd.to_numeric(phase2_scope["gen_vre_twh"], errors="coerce").corr(
                        pd.to_numeric(phase2_scope["load_net_twh"], errors="coerce")
                    ),
                    np.nan,
                )

            years_used = ",".join([str(int(v)) for v in fit_df["year"].tolist()])
            phase2_start = int(fit_df["year"].min()) if not fit_df.empty else np.nan
            phase2_end = int(fit_df["year"].max()) if not fit_df.empty else np.nan
            phase2_benchmark_rows[tech].append(fit_df[["country", "x", "y"]].copy())

            rows.append(
                {
                    "country": country,
                    "tech": tech,
                    "phase2_start_year_for_slope": phase2_start,
                    "phase2_start_reason": "q1_phase2_market_years",
                    "phase2_end_year": phase2_end,
                    "years_used": years_used,
                    "n_points": int(fit["n"]),
                    "x_axis_used": x_axis,
                    "x_unit": "share_of_load",
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
                    "mean_sr_energy_phase2": _safe_float(pd.to_numeric(phase2_scope.get("sr_energy"), errors="coerce").mean(), np.nan),
                    "mean_far_energy_phase2": _safe_float(pd.to_numeric(phase2_scope.get("far_observed"), errors="coerce").mean(), np.nan),
                    "mean_ir_p10_phase2": _safe_float(pd.to_numeric(phase2_scope.get("ir_p10"), errors="coerce").mean(), np.nan),
                    "mean_ttl_phase2": _safe_float(pd.to_numeric(phase2_scope.get("ttl_eur_mwh"), errors="coerce").mean(), np.nan),
                    "vre_load_corr_phase2": np.nan,
                    "surplus_load_trough_share_phase2": np.nan,
                    "cross_country_benchmark_slope": np.nan,
                    "cross_country_benchmark_r2": np.nan,
                    "cross_country_benchmark_p_value": np.nan,
                    "cross_country_benchmark_n": np.nan,
                    "slope_quality_flag": slope_quality_flag,
                    "slope_quality_notes": slope_quality_notes,
                    "corr_vre_load_phase2": corr_vre_load_phase2,
                }
            )

            if (
                int(fit["n"]) >= 4
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

            if int(fit["n"]) < 4 and str(fit["slope_method"]) == "ols":
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "Q2_N_LT_4_WITH_OLS",
                        "message": f"{country}-{tech}: OLS interdit si n<4.",
                    }
                )
            if int(fit["n"]) < 4 and np.isfinite(_safe_float(fit["p_value"], np.nan)):
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "Q2_N_LT_4_WITH_PVALUE",
                        "message": f"{country}-{tech}: p_value doit etre NaN si n<4.",
                    }
                )
            if int(fit["n"]) in {2, 3}:
                xvals = fit_df["x"].to_numpy(dtype=float)
                if len(xvals) >= 2 and abs(float(xvals[-1] - xvals[0])) > 1e-12 and not np.isfinite(_safe_float(fit["slope"], np.nan)):
                    checks.append(
                        {
                            "status": "FAIL",
                            "code": "Q2_ENDPOINT_SLOPE_NAN",
                            "message": f"{country}-{tech}: pente endpoint doit etre finie si x varie.",
                        }
                    )

        # Driver diagnostics use country-level phase2_market years.
        phase_mask_drv = (
            pd.to_numeric(group["is_phase2_market"], errors="coerce").fillna(0.0) > 0.0
            if "is_phase2_market" in group.columns
            else pd.Series(False, index=group.index)
        )
        gp_drv = group[phase_mask_drv].copy()
        gp_drv["quality_ok"] = gp_drv.get("quality_ok", True).fillna(False).astype(bool)
        gp_drv["crisis_year"] = gp_drv.get("crisis_year", False).fillna(False).astype(bool)
        gp_drv["year_num"] = pd.to_numeric(gp_drv.get("year"), errors="coerce")
        crisis_override_2022 = include_2022 & (gp_drv["year_num"] == 2022)
        gp_drv = gp_drv[gp_drv["quality_ok"] & ((~gp_drv["crisis_year"]) | crisis_override_2022)]
        if exclude_2022:
            gp_drv = gp_drv[gp_drv["year_num"] != 2022]
        gp_drv = gp_drv.sort_values("year")
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
    benchmark_rows: list[dict[str, Any]] = []
    for tech in ["PV", "WIND"]:
        pieces = [df for df in phase2_benchmark_rows[tech] if not df.empty]
        if pieces:
            panel_fit = _panel_fixed_effect_slope(pd.concat(pieces, ignore_index=True))
        else:
            panel_fit = {"slope": np.nan, "r2": np.nan, "p_value": np.nan, "n": 0, "reason": "insufficient_panel_points"}
        benchmark_rows.append(
            {
                "tech": tech,
                "cross_country_benchmark_slope": _safe_float(panel_fit.get("slope"), np.nan),
                "cross_country_benchmark_r2": _safe_float(panel_fit.get("r2"), np.nan),
                "cross_country_benchmark_p_value": _safe_float(panel_fit.get("p_value"), np.nan),
                "cross_country_benchmark_n": int(_safe_float(panel_fit.get("n"), 0.0)),
                "cross_country_benchmark_reason": str(panel_fit.get("reason", "")),
            }
        )
    if not slopes.empty:
        benchmark_cols = [
            "cross_country_benchmark_slope",
            "cross_country_benchmark_r2",
            "cross_country_benchmark_p_value",
            "cross_country_benchmark_n",
            "cross_country_benchmark_reason",
        ]
        slopes = slopes.drop(columns=[c for c in benchmark_cols if c in slopes.columns], errors="ignore")
        slopes = slopes.merge(pd.DataFrame(benchmark_rows), on="tech", how="left")
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

    if not slopes.empty:
        q2_001_fail = False
        q2_2022_fail = False
        q2_002_warn = 0
        for _, row in slopes.iterrows():
            country = str(row.get("country", "?"))
            tech = str(row.get("tech", "?"))
            n_points = int(_safe_float(row.get("n_points"), 0.0))
            method = str(row.get("slope_method", "none"))
            r2 = _safe_float(row.get("r2"), np.nan)
            years_used = _years_from_csv(row.get("years_used", ""))
            notes = str(row.get("slope_quality_notes", "")).strip()
            slope = _safe_float(row.get("slope"), np.nan)
            corr_vre_load = _safe_float(row.get("corr_vre_load_phase2"), np.nan)

            if exclude_2022 and 2022 in years_used:
                q2_2022_fail = True
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "TEST_Q2_2022_001",
                        "message": f"{country}-{tech}: 2022 present dans years_used alors que exclude_year_2022=1.",
                    }
                )

            if n_points >= 3:
                if method == "ols":
                    if not np.isfinite(r2):
                        q2_001_fail = True
                        checks.append(
                            {
                                "status": "FAIL",
                                "code": "TEST_Q2_001",
                                "message": f"{country}-{tech}: r2 manquant alors que n_points>=3 et methode OLS.",
                            }
                        )
                else:
                    if not notes:
                        q2_001_fail = True
                        checks.append(
                            {
                                "status": "FAIL",
                                "code": "TEST_Q2_001",
                                "message": f"{country}-{tech}: OLS impossible sans justification dans slope_quality_notes.",
                            }
                        )

            if np.isfinite(slope) and slope > 0.0 and np.isfinite(corr_vre_load) and corr_vre_load <= -0.5:
                q2_002_warn += 1
                checks.append(
                    {
                        "status": "WARN",
                        "code": "TEST_Q2_002",
                        "message": f"{country}-{tech}: slope positive avec corr_vre_load fortement negative ({corr_vre_load:.3f}).",
                    }
                )

        if exclude_2022 and not q2_2022_fail:
            checks.append(
                {
                    "status": "PASS",
                    "code": "TEST_Q2_2022_001",
                    "message": "exclude_year_2022=1 respecte: 2022 absent de tous les years_used.",
                }
            )
        if not q2_001_fail:
            checks.append(
                {
                    "status": "PASS",
                    "code": "TEST_Q2_001",
                    "message": "r2 present pour les OLS (n>=3) ou justification explicite quand OLS impossible.",
                }
            )
        if q2_002_warn == 0:
            checks.append(
                {
                    "status": "PASS",
                    "code": "TEST_Q2_002",
                    "message": "Aucun cas physiquement suspect (slope>0 et corr_vre_load fortement negative).",
                }
            )

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
        "Q2 estime la pente de cannibalisation sur les annees explicitement phase2_market (Q1 corrige), "
        "en excluant annees de crise/qualite insuffisante; OLS si n>=4, endpoint-delta si n=2/3 (FRAGILE), "
        "avec benchmark panel fixe-pays pour contextualiser les historiques courts."
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
