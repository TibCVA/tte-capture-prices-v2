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

Q2_OUTPUT_SCHEMA_VERSION = "2.0.0"


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
    if n < 2:
        return {
            "slope": np.nan,
            "intercept": np.nan,
            "r2": np.nan,
            "p_value": np.nan,
            "n": n,
            "slope_method": "none",
            "insufficient_points": True,
            "reason_code": "INSUFFICIENT_POINTS",
        }
    if n < int(max(3, min_points)):
        return _endpoint_slope(df_xy)
    if df_xy["x"].nunique(dropna=True) > 1:
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
    return {
        "slope": np.nan,
        "intercept": np.nan,
        "r2": np.nan,
        "p_value": np.nan,
        "n": int(n),
        "slope_method": "none",
        "insufficient_points": True,
        "reason_code": "X_CONSTANT",
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


def _leave_one_out_relative_variation(df_xy: pd.DataFrame, slope_ref: float) -> float:
    if not (np.isfinite(slope_ref) and len(df_xy) >= 6):
        return np.nan
    if abs(slope_ref) <= 1e-12:
        return np.nan
    loo_slopes: list[float] = []
    for i in range(len(df_xy)):
        sub = df_xy.drop(df_xy.index[i])
        if len(sub) < 4 or sub["x"].nunique(dropna=True) <= 1:
            continue
        reg = robust_linreg(sub["x"], sub["y"])
        slope_i = _safe_float(reg.get("slope"), np.nan)
        if np.isfinite(slope_i):
            loo_slopes.append(float(slope_i))
    if not loo_slopes:
        return np.nan
    ref_abs = abs(float(slope_ref))
    rel = [abs(v - slope_ref) / ref_abs for v in loo_slopes]
    return float(max(rel)) if rel else np.nan


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
    q1_summary = q1.tables.get("Q1_country_summary", pd.DataFrame()).copy()

    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q2_PARAMS)].iterrows()
    }
    min_points = max(3, int(params.get("min_points_regression", 4)))
    exclude_2022 = int(params.get("exclude_year_2022", 1)) == 1
    include_2022 = _to_bool(selection.get("include_2022"), default=False)
    if include_2022:
        exclude_2022 = False
    scenario_id_effective = str(selection.get("scenario_id") or ("HIST" if str(selection.get("mode", "HIST")).upper() == "HIST" else "SCEN"))

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
    gen_total_twh = _as_numeric_series(panel, "gen_total_twh", np.nan)
    if gen_total_twh.notna().sum() == 0:
        gen_total_twh = load_twh.copy()
    panel["pv_penetration_share_generation"] = pv_twh / gen_total_twh.replace(0.0, np.nan)
    panel["wind_penetration_share_generation"] = wind_twh / gen_total_twh.replace(0.0, np.nan)
    panel["pv_penetration_share_generation"] = panel["pv_penetration_share_generation"].fillna(
        _as_share(panel.get("pv_penetration_pct_gen", pd.Series(np.nan, index=panel.index)))
    )
    panel["wind_penetration_share_generation"] = panel["wind_penetration_share_generation"].fillna(
        _as_share(panel.get("wind_penetration_pct_gen", pd.Series(np.nan, index=panel.index)))
    )
    panel["pv_penetration_share_load"] = pv_twh / load_twh.replace(0.0, np.nan)
    panel["wind_penetration_share_load"] = wind_twh / load_twh.replace(0.0, np.nan)
    panel["pv_penetration_share_load"] = panel["pv_penetration_share_load"].fillna(_as_share(panel.get("pv_penetration_pct_gen", pd.Series(np.nan, index=panel.index))))
    panel["wind_penetration_share_load"] = panel["wind_penetration_share_load"].fillna(
        _as_share(panel.get("wind_penetration_pct_gen", pd.Series(np.nan, index=panel.index)))
    )

    phase2_years_ref_raw = selection.get("phase2_years_by_country_tech", {})
    phase2_start_ref_raw = selection.get("phase2_start_year_by_country_tech", {})

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
        c_summary = (
            q1_summary[q1_summary["country"].astype(str) == str(country)].copy()
            if "country" in q1_summary.columns
            else pd.DataFrame()
        )
        for tech in ["PV", "WIND"]:
            years_num = pd.to_numeric(group.get("year"), errors="coerce")
            ref_key = f"{str(country)}|{str(tech).upper()}"
            ref_years: list[int] = []
            if isinstance(phase2_years_ref_raw, dict):
                raw_vals = phase2_years_ref_raw.get(ref_key, [])
                if isinstance(raw_vals, (list, tuple, set, np.ndarray, pd.Series)):
                    for yv in raw_vals:
                        yy = _safe_float(yv, np.nan)
                        if np.isfinite(yy):
                            ref_years.append(int(yy))
                else:
                    ref_years = _years_from_csv(raw_vals)
            ref_years = sorted(set(ref_years))
            if ref_years:
                phase2_start_year = float(min(ref_years))
                if isinstance(phase2_start_ref_raw, dict):
                    phase2_start_override = _safe_float(phase2_start_ref_raw.get(ref_key), np.nan)
                    if np.isfinite(phase2_start_override):
                        phase2_start_year = float(int(phase2_start_override))
                phase2_start_reason = "hist_phase2_reference"
                phase2_scope = group[years_num.isin(ref_years)].copy()
            else:
                phase2_start_year, phase2_start_reason = _phase2_start_year(c_summary, tech=tech)
                if np.isfinite(phase2_start_year):
                    phase2_scope = group[years_num >= float(phase2_start_year)].copy()
                else:
                    phase2_mask = pd.to_numeric(group.get("is_phase2_market"), errors="coerce").fillna(0.0) > 0.0
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
                        "scenario_id": scenario_id_effective,
                        "country": country,
                        "tech": tech,
                        "phase2_start_year_for_slope": np.nan,
                        "phase2_start_reason": phase2_start_reason if phase2_start_reason else "q1_no_phase2_market_year",
                        "phase2_end_year": np.nan,
                        "years_used": "",
                        "n_points": 0,
                        "x_axis_used": "none",
                        "x_axis_default": f"{str(tech).lower()}_penetration_share_generation",
                        "x_unit": "share_of_generation",
                        "slope": np.nan,
                        "slope_per_1pp": np.nan,
                        "slope_unit": "capture_ratio_per_share_generation",
                        "intercept": np.nan,
                        "r2": np.nan,
                        "p_value": np.nan,
                        "loo_slope_rel_var_max": np.nan,
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
                        "penetration_share_generation_mean_phase2": np.nan,
                        "penetration_share_load_mean_phase2": np.nan,
                        "slope_quality_flag": "WARN",
                        "slope_quality_notes": "INSUFFICIENT_POINTS",
                    }
                )
                continue

            if tech == "PV":
                x_gen = pd.to_numeric(phase2_scope.get("pv_penetration_share_generation"), errors="coerce")
                x_load = pd.to_numeric(phase2_scope.get("pv_penetration_share_load"), errors="coerce")
                x = x_gen.copy()
                x_axis = "pv_penetration_share_generation"
                if x.notna().sum() == 0:
                    x = x_load
                    x_axis = "pv_penetration_share_load"
                y = (
                    pd.to_numeric(phase2_scope["capture_ratio_pv"], errors="coerce")
                    if "capture_ratio_pv" in phase2_scope.columns
                    else pd.Series(np.nan, index=phase2_scope.index)
                )
                x_unit = "share_of_generation" if x_axis.endswith("_generation") else "share_of_load"
            else:
                x_gen = pd.to_numeric(phase2_scope.get("wind_penetration_share_generation"), errors="coerce")
                x_load = pd.to_numeric(phase2_scope.get("wind_penetration_share_load"), errors="coerce")
                x = x_gen.copy()
                x_axis = "wind_penetration_share_generation"
                if x.notna().sum() == 0:
                    x = x_load
                    x_axis = "wind_penetration_share_load"
                y = (
                    pd.to_numeric(phase2_scope["capture_ratio_wind"], errors="coerce")
                    if "capture_ratio_wind" in phase2_scope.columns
                    else pd.Series(np.nan, index=phase2_scope.index)
                )
                x_unit = "share_of_generation" if x_axis.endswith("_generation") else "share_of_load"

            fit_df = pd.DataFrame(
                {
                    "country": country,
                    "year": pd.to_numeric(phase2_scope.get("year"), errors="coerce"),
                    "x": x,
                    "y": y,
                }
            ).dropna()
            fit = _fit_slope(fit_df, min_points=min_points)
            n_points_fit = int(_safe_float(fit.get("n"), 0.0))
            slope_value = _safe_float(fit.get("slope"), np.nan)
            p_val_fit = _safe_float(fit.get("p_value"), np.nan)
            loo_rel_var_max = _leave_one_out_relative_variation(fit_df, slope_value)
            is_strict_pass = bool(
                str(fit.get("slope_method", "")).lower() == "ols"
                and n_points_fit >= 6
                and np.isfinite(slope_value)
                and np.isfinite(p_val_fit)
                and p_val_fit <= 0.05
                and np.isfinite(loo_rel_var_max)
                and loo_rel_var_max <= 0.20
            )
            if is_strict_pass:
                slope_quality_flag = "PASS"
                slope_quality_notes = "OLS_STRICT_PASS"
                fit["robust_flag"] = "ROBUST"
            else:
                notes: list[str] = []
                if n_points_fit < 3:
                    notes.append("INSUFFICIENT_POINTS")
                if n_points_fit < 6:
                    notes.append("N_LT_6")
                if str(fit.get("slope_method", "")).lower() != "ols":
                    notes.append("METHOD_NOT_OLS")
                if not np.isfinite(p_val_fit):
                    notes.append("PVALUE_MISSING")
                elif p_val_fit > 0.05:
                    notes.append("PVALUE_GT_0_05")
                if not np.isfinite(loo_rel_var_max):
                    notes.append("LOO_NOT_AVAILABLE")
                elif loo_rel_var_max > 0.20:
                    notes.append("LOO_UNSTABLE")
                slope_quality_flag = "WARN"
                slope_quality_notes = "|".join(notes) if notes else str(fit.get("reason_code", "WARN"))
                fit["robust_flag"] = "NON_TESTABLE" if n_points_fit < 3 else "FRAGILE"

            corr_vre_load_phase2 = np.nan
            if {"gen_vre_twh", "load_net_twh"}.issubset(set(phase2_scope.columns)):
                corr_vre_load_phase2 = _safe_float(
                    pd.to_numeric(phase2_scope["gen_vre_twh"], errors="coerce").corr(
                        pd.to_numeric(phase2_scope["load_net_twh"], errors="coerce")
                    ),
                    np.nan,
                )

            years_used = ",".join([str(int(v)) for v in fit_df["year"].tolist()])
            phase2_years_set = set(pd.to_numeric(phase2_scope.get("year"), errors="coerce").dropna().astype(int).tolist())
            fit_years_set = set(pd.to_numeric(fit_df.get("year"), errors="coerce").dropna().astype(int).tolist())
            if not fit_years_set.issubset(phase2_years_set):
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "Q2_YEARS_USED_OUTSIDE_PHASE2",
                        "message": f"{country}-{tech}: years_used doit etre un sous-ensemble des annees phase2 Q1.",
                    }
                )
            phase2_start = int(fit_df["year"].min()) if not fit_df.empty else np.nan
            phase2_end = int(fit_df["year"].max()) if not fit_df.empty else np.nan
            phase2_benchmark_rows[tech].append(fit_df[["country", "x", "y"]].copy())

            rows.append(
                {
                    "scenario_id": scenario_id_effective,
                    "country": country,
                    "tech": tech,
                    "phase2_start_year_for_slope": int(phase2_start_year) if np.isfinite(phase2_start_year) else phase2_start,
                    "phase2_start_reason": phase2_start_reason if phase2_start_reason else "q1_phase2_market_years",
                    "phase2_end_year": phase2_end,
                    "years_used": years_used,
                    "n_points": int(fit["n"]),
                    "x_axis_used": x_axis,
                    "x_axis_default": f"{str(tech).lower()}_penetration_share_generation",
                    "x_unit": x_unit,
                    "slope": fit["slope"],
                    "slope_per_1pp": _safe_float(fit.get("slope"), np.nan) * 0.01 if np.isfinite(_safe_float(fit.get("slope"), np.nan)) else np.nan,
                    "slope_unit": "capture_ratio_per_share_generation" if x_unit == "share_of_generation" else "capture_ratio_per_share_load",
                    "intercept": fit["intercept"],
                    "r2": fit["r2"],
                    "p_value": fit["p_value"],
                    "loo_slope_rel_var_max": loo_rel_var_max,
                    "n": int(fit["n"]),
                    "slope_method": fit["slope_method"],
                    "method": fit["slope_method"],
                    "insufficient_points": bool(fit["insufficient_points"]),
                    "robust_flag": fit["robust_flag"],
                    "reason_code": str(fit["reason_code"]).lower(),
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
                    "penetration_share_generation_mean_phase2": _safe_float(pd.to_numeric(phase2_scope.get(f"{str(tech).lower()}_penetration_share_generation"), errors="coerce").mean(), np.nan),
                    "penetration_share_load_mean_phase2": _safe_float(pd.to_numeric(phase2_scope.get(f"{str(tech).lower()}_penetration_share_load"), errors="coerce").mean(), np.nan),
                    "slope_quality_flag": slope_quality_flag,
                    "slope_quality_notes": slope_quality_notes,
                    "corr_vre_load_phase2": corr_vre_load_phase2,
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
            if slope_quality_flag == "PASS" and _safe_float(fit.get("p_value"), np.nan) > 0.05:
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "Q2_PASS_WITH_PVALUE_GT_0_05",
                        "message": f"{country}-{tech}: slope_quality_flag=PASS interdit si p_value>0.05.",
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
                    "scenario_id": scenario_id_effective,
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
    has_fail = any(str(c.get("status", "")).upper() == "FAIL" for c in checks)
    has_warn = any(str(c.get("status", "")).upper() == "WARN" for c in checks)
    module_quality_status = "FAIL" if has_fail else ("WARN" if has_warn else "PASS")

    if not slopes.empty:
        q2_quality_summary = (
            slopes[["country", "scenario_id", "phase2_end_year"]]
            .rename(columns={"phase2_end_year": "year"})
            .copy()
        )
        q2_quality_summary["year"] = pd.to_numeric(q2_quality_summary["year"], errors="coerce")
        q2_quality_summary = q2_quality_summary.groupby(["country", "scenario_id"], as_index=False, dropna=False)["year"].max()
    else:
        q2_quality_summary = pd.DataFrame(
            {
                "country": [str(c) for c in sorted(set([str(c) for c in countries]))],
                "scenario_id": scenario_id_effective,
                "year": np.nan,
            }
        )
    if not q2_quality_summary.empty:
        q2_quality_summary["module_id"] = "Q2"
        q2_quality_summary["quality_status"] = module_quality_status
        q2_quality_summary["output_schema_version"] = Q2_OUTPUT_SCHEMA_VERSION

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
            "q2_quality_summary": q2_quality_summary,
        },
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
        mode=str(selection.get("mode", "HIST")).upper(),
        scenario_id=selection.get("scenario_id"),
        horizon_year=selection.get("horizon_year"),
    )
