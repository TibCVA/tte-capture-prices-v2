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


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


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


def _x_unit_for_axis(x_axis: str) -> str:
    return "pct_point" if "_pct_" in str(x_axis) else "share_point"


def _phase2_start_year(group: pd.DataFrame, bascule_year: float, selection: dict[str, Any]) -> tuple[float, str]:
    scenario_start = np.nan
    if str(selection.get("mode", "HIST")).upper() == "SCEN":
        years = [int(y) for y in selection.get("scenario_years", []) if str(y).strip()]
        if years:
            scenario_start = float(min(years))
    if np.isfinite(bascule_year):
        start = int(bascule_year)
        if np.isfinite(scenario_start):
            return float(max(start, int(scenario_start))), "q1_bascule_or_scenario_start"
        return float(start), "q1_bascule"
    if np.isfinite(scenario_start):
        return float(int(scenario_start)), "q1_no_bascule_use_scenario_start"
    return float("nan"), "q1_no_bascule"


def _with_outliers(gp: pd.DataFrame, z_th: float = 2.5) -> pd.DataFrame:
    out = gp.copy()
    out["outlier_year"] = False
    for col in ["ttl_eur_mwh", "baseload_price_eur_mwh"]:
        if col in out.columns:
            s = pd.to_numeric(out[col], errors="coerce")
        else:
            s = pd.Series(np.nan, index=out.index, dtype=float)
        if s.notna().sum() < 3:
            continue
        std = float(s.std(ddof=0))
        if std <= 0:
            continue
        z = (s - float(s.mean())) / std
        out.loc[z.abs() > z_th, "outlier_year"] = True
    return out


def _regression_summary(x: pd.Series, y: pd.Series, min_points: int) -> dict[str, Any]:
    reg = robust_linreg(x, y)
    method = "OLS"
    reason = "ok"
    robust_flag = "ROBUST"

    if int(reg["n"]) < min_points and int(reg["n"]) >= 2:
        delta = _delta_slope_two_point(x, y)
        if np.isfinite(delta["slope"]):
            reg = delta
            method = "two_point"
            robust_flag = "FRAGILE"
            reason = "insufficient_points"
    if int(reg["n"]) < 2 or not np.isfinite(reg["slope"]):
        robust_flag = "NON_TESTABLE"
        reason = "insufficient_points"
    elif np.isfinite(reg.get("p_value", np.nan)) and reg["p_value"] > 0.25:
        robust_flag = "NOT_SIGNIFICANT"
        reason = "p_value_high"
    elif np.isfinite(reg.get("r2", np.nan)) and reg["r2"] < 0.10:
        robust_flag = "NOT_SIGNIFICANT"
        reason = "r2_low"
    elif int(reg["n"]) < min_points:
        robust_flag = "FRAGILE"
        reason = "insufficient_points"

    return {
        "slope": float(reg["slope"]) if np.isfinite(reg["slope"]) else np.nan,
        "intercept": float(reg["intercept"]) if np.isfinite(reg["intercept"]) else np.nan,
        "r2": float(reg["r2"]) if np.isfinite(reg["r2"]) else np.nan,
        "p_value": float(reg["p_value"]) if np.isfinite(reg["p_value"]) else np.nan,
        "n": int(reg["n"]),
        "slope_method": method,
        "robust_flag": robust_flag,
        "reason_code": reason,
    }


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
) -> ModuleResult:
    q1 = run_q1(annual_df, assumptions_df, selection, run_id, hourly_by_country_year=hourly_by_country_year)
    q1_panel = q1.tables["Q1_year_panel"]
    bascule = q1.tables["Q1_country_summary"][["country", "bascule_year_market"]]

    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q2_PARAMS)].iterrows()
    }
    min_points = max(2, int(params.get("min_points_regression", 5)))
    exclude_2022 = int(params.get("exclude_year_2022", 0)) == 1

    countries = selection.get("countries", sorted(annual_df["country"].dropna().unique().tolist()))
    panel = annual_df[annual_df["country"].isin(countries)].copy().merge(bascule, on="country", how="left")
    panel = panel.sort_values(["country", "year"])

    rows: list[dict[str, Any]] = []
    checks: list[dict[str, str]] = []
    warnings: list[str] = []

    for country, group in panel.groupby("country"):
        group = group.sort_values("year")
        start, start_reason = _phase2_start_year(group, _safe_float(group["bascule_year_market"].dropna().iloc[0], np.nan) if group["bascule_year_market"].notna().any() else np.nan, selection)
        if not np.isfinite(start):
            warnings.append(f"{country}: pas de bascule Q1 ni horizon scenario pour pente Q2.")
            for tech in ["PV", "WIND"]:
                rows.append(
                    {
                        "country": country,
                        "tech": tech,
                        "phase2_start_year_for_slope": np.nan,
                        "phase2_start_reason": start_reason,
                        "phase2_end_year": np.nan,
                        "years_used": "",
                        "years_used_no_outliers": "",
                        "x_axis_used": "none",
                        "x_unit": "",
                        "slope": np.nan,
                        "intercept": np.nan,
                        "r2": np.nan,
                        "p_value": np.nan,
                        "n": 0,
                        "slope_method": "NONE",
                        "robust_flag": "NON_TESTABLE",
                        "reason_code": "q1_no_bascule",
                        "slope_all_years": np.nan,
                        "slope_excluding_outliers": np.nan,
                        "vre_load_corr_phase2": np.nan,
                        "surplus_load_trough_share_phase2": np.nan,
                    }
                )
            continue

        gp = group[group["year"] >= int(start)].copy().sort_values("year")
        if exclude_2022:
            gp = gp[gp["year"] != 2022]
        gp = _with_outliers(gp, z_th=2.5)
        gp_no = gp[~gp["outlier_year"]].copy()

        if gp.empty:
            for tech in ["PV", "WIND"]:
                rows.append(
                    {
                        "country": country,
                        "tech": tech,
                        "phase2_start_year_for_slope": start,
                        "phase2_start_reason": start_reason,
                        "phase2_end_year": np.nan,
                        "years_used": "",
                        "years_used_no_outliers": "",
                        "x_axis_used": "none",
                        "x_unit": "",
                        "slope": np.nan,
                        "intercept": np.nan,
                        "r2": np.nan,
                        "p_value": np.nan,
                        "n": 0,
                        "slope_method": "NONE",
                        "robust_flag": "NON_TESTABLE",
                        "reason_code": "phase2_window_empty",
                        "slope_all_years": np.nan,
                        "slope_excluding_outliers": np.nan,
                        "vre_load_corr_phase2": np.nan,
                        "surplus_load_trough_share_phase2": np.nan,
                    }
                )
            continue

        for tech in ["PV", "WIND"]:
            if tech == "PV":
                x = pd.to_numeric(gp.get("pv_penetration_pct_gen"), errors="coerce")
                y = pd.to_numeric(gp.get("capture_ratio_pv_vs_ttl"), errors="coerce")
                x_no = pd.to_numeric(gp_no.get("pv_penetration_pct_gen"), errors="coerce")
                y_no = pd.to_numeric(gp_no.get("capture_ratio_pv_vs_ttl"), errors="coerce")
                x_axis = "pv_penetration_pct_gen"
            else:
                x = pd.to_numeric(gp.get("wind_penetration_pct_gen"), errors="coerce")
                y = pd.to_numeric(gp.get("capture_ratio_wind_vs_ttl"), errors="coerce")
                x_no = pd.to_numeric(gp_no.get("wind_penetration_pct_gen"), errors="coerce")
                y_no = pd.to_numeric(gp_no.get("capture_ratio_wind_vs_ttl"), errors="coerce")
                x_axis = "wind_penetration_pct_gen"

            if x.notna().sum() < min_points:
                x = pd.to_numeric(gp.get("sr_energy"), errors="coerce")
                x_no = pd.to_numeric(gp_no.get("sr_energy"), errors="coerce")
                x_axis = "sr_energy"

            all_reg = _regression_summary(x, y, min_points=min_points)
            no_reg = _regression_summary(x_no, y_no, min_points=min_points)
            chosen = no_reg if np.isfinite(no_reg["slope"]) else all_reg
            x_unit = _x_unit_for_axis(x_axis)

            if chosen["robust_flag"] == "NOT_SIGNIFICANT":
                checks.append({"status": "INFO", "code": "Q2_NOT_SIGNIFICANT", "message": f"{country}-{tech}: signal statistique faible (p-value/R2)."})
            if chosen["robust_flag"] == "FRAGILE":
                checks.append({"status": "INFO", "code": "Q2_FRAGILE", "message": f"{country}-{tech}: n insuffisant pour robustesse pleine."})
            if np.isfinite(chosen["slope"]) and abs(float(chosen["slope"])) > 0.2:
                checks.append({"status": "WARN", "code": "Q2_UNLIKELY_SLOPE", "message": f"{country}-{tech}: pente atypique abs>0.2/an."})

            rows.append(
                {
                    "country": country,
                    "tech": tech,
                    "phase2_start_year_for_slope": float(start),
                    "phase2_start_reason": start_reason,
                    "phase2_end_year": int(gp["year"].max()),
                    "years_used": ",".join([str(int(yv)) for yv in gp["year"].tolist()]),
                    "years_used_no_outliers": ",".join([str(int(yv)) for yv in gp_no["year"].tolist()]),
                    "x_axis_used": x_axis,
                    "x_unit": x_unit,
                    "slope": chosen["slope"],
                    "intercept": chosen["intercept"],
                    "r2": chosen["r2"],
                    "p_value": chosen["p_value"],
                    "n": chosen["n"],
                    "slope_method": chosen["slope_method"],
                    "robust_flag": chosen["robust_flag"],
                    "reason_code": chosen["reason_code"],
                    "slope_all_years": all_reg["slope"],
                    "slope_excluding_outliers": no_reg["slope"],
                    "outlier_years_count": int(gp["outlier_year"].sum()),
                    "mean_sr_energy_phase2": float(pd.to_numeric(gp.get("sr_energy"), errors="coerce").mean()),
                    "mean_far_energy_phase2": float(pd.to_numeric(gp.get("far_energy"), errors="coerce").mean()),
                    "mean_ir_p10_phase2": float(pd.to_numeric(gp.get("ir_p10"), errors="coerce").mean()),
                    "mean_ttl_phase2": float(pd.to_numeric(gp.get("ttl_eur_mwh"), errors="coerce").mean()),
                    "vre_load_corr_phase2": np.nan,
                    "surplus_load_trough_share_phase2": np.nan,
                }
            )

    slopes = pd.DataFrame(rows)
    if slopes.empty:
        checks.append({"status": "WARN", "code": "Q2_NO_SLOPE", "message": "Aucune pente Q2 n'a pu etre calculee."})

    # Drivers: simple sign-aware diagnostics.
    drivers = []
    expected_sign = {
        "sr_energy": -1,
        "far_energy": 1,
        "vre_penetration_share_gen": -1,
        "nrl_p10_proxy": 1,
        "nrl_p50_proxy": 1,
        "nrl_p90_proxy": 1,
        "exports_pos_share_proxy": 1,
        "ir_p10": -1,
    }
    for country, gp in panel.groupby("country"):
        gp = gp.sort_values("year")
        y = pd.to_numeric(gp.get("capture_ratio_pv_vs_ttl"), errors="coerce")
        nrl_p10_proxy = pd.to_numeric(gp.get("p10_load_mw"), errors="coerce") - pd.to_numeric(gp.get("p10_must_run_mw"), errors="coerce")
        nrl_p50_proxy = pd.to_numeric(gp.get("p50_load_mw"), errors="coerce") - pd.to_numeric(gp.get("p50_must_run_mw"), errors="coerce")
        nrl_p90_proxy = pd.to_numeric(gp.get("p50_load_mw"), errors="coerce")
        exports_share = pd.to_numeric(gp.get("exports_twh"), errors="coerce") / pd.to_numeric(gp.get("load_net_twh"), errors="coerce")
        var_map = {
            "sr_energy": pd.to_numeric(gp.get("sr_energy"), errors="coerce"),
            "far_energy": pd.to_numeric(gp.get("far_energy"), errors="coerce"),
            "vre_penetration_share_gen": pd.to_numeric(gp.get("vre_penetration_share_gen"), errors="coerce"),
            "nrl_p10_proxy": nrl_p10_proxy,
            "nrl_p50_proxy": nrl_p50_proxy,
            "nrl_p90_proxy": nrl_p90_proxy,
            "exports_pos_share_proxy": exports_share,
            "ir_p10": pd.to_numeric(gp.get("ir_p10"), errors="coerce"),
        }
        for name, x in var_map.items():
            corr, elast = _corr_and_elasticity(y, x)
            exp = expected_sign[name]
            obs_sign = 0 if not np.isfinite(corr) or abs(corr) < 1e-9 else (1 if corr > 0 else -1)
            sign_conflict = bool(obs_sign != 0 and obs_sign != exp and abs(corr) >= 0.10)
            drivers.append(
                {
                    "country": country,
                    "driver_name": name,
                    "corr_capture_pv": corr,
                    "elasticity_capture_pv": elast,
                    "expected_sign": exp,
                    "observed_sign": obs_sign,
                    "sign_conflict": sign_conflict,
                }
            )

    drivers_country = pd.DataFrame(drivers)
    driver_rows = []
    if not slopes.empty:
        for driver in sorted(expected_sign.keys()):
            pv_scope = slopes[slopes["tech"] == "PV"]
            wind_scope = slopes[slopes["tech"] == "WIND"]
            merged_pv = pv_scope[["country", "slope"]].merge(
                drivers_country[drivers_country["driver_name"] == driver][["country", "corr_capture_pv", "sign_conflict"]],
                on="country",
                how="left",
            )
            merged_wind = wind_scope[["country", "slope"]].merge(
                drivers_country[drivers_country["driver_name"] == driver][["country", "corr_capture_pv", "sign_conflict"]],
                on="country",
                how="left",
            )
            corr_with_slope_pv = float(merged_pv["slope"].corr(merged_pv["corr_capture_pv"])) if len(merged_pv.dropna()) >= 2 else np.nan
            corr_with_slope_wind = float(merged_wind["slope"].corr(merged_wind["corr_capture_pv"])) if len(merged_wind.dropna()) >= 2 else np.nan
            driver_rows.append(
                {
                    "driver_name": driver,
                    "corr_with_slope_pv": corr_with_slope_pv,
                    "corr_with_slope_wind": corr_with_slope_wind,
                    "n_countries": int(slopes["country"].nunique()),
                    "expected_sign": expected_sign[driver],
                    "sign_conflict_share": float(pd.to_numeric(drivers_country[drivers_country["driver_name"] == driver]["sign_conflict"], errors="coerce").mean()) if not drivers_country.empty else np.nan,
                }
            )
    driver_corr = pd.DataFrame(driver_rows)

    checks.extend(build_common_checks(q1_panel))
    if not checks:
        checks.append({"status": "PASS", "code": "Q2_PASS", "message": "Q2 checks pass."})

    kpis = {
        "n_slopes": int(len(slopes)),
        "n_robust": int((slopes.get("robust_flag") == "ROBUST").sum()) if not slopes.empty else 0,
    }

    narrative = (
        "Q2 mesure la pente de cannibalisation avec fenetre Phase2 coherente (Q1 + horizon scenario), "
        "sorties all_years/excluding_outliers, et tableau de drivers avec signe attendu et conflits de signe."
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
