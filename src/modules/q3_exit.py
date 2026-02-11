"""Q3 - Exit from Phase 2 and pragmatic stop-condition proxies."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.modules.common import assumptions_subset
from src.modules.q1_transition import run_q1
from src.modules.q2_slope import run_q2
from src.modules.reality_checks import build_common_checks
from src.modules.result import ModuleResult

Q3_PARAMS = [
    "trend_window_years",
    "require_recent_stage2",
    "stage2_recent_h_negative_min",
    "stage2_recent_h_negative_min_scen",
    "stage2_recent_sr_energy_min_scen",
    "trend_h_negative_max",
    "trend_capture_ratio_min",
    "h_negative_target",
    "h_below_5_target",
    "sr_energy_target",
    "far_target",
    "demand_k_max",
    "slope_capture_target",
]


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


def _trend_slope(year: pd.Series, value: pd.Series) -> float:
    x = pd.to_numeric(year, errors="coerce")
    y = pd.to_numeric(value, errors="coerce")
    tmp = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(tmp) < 2:
        return np.nan
    x0 = float(tmp["x"].iloc[0])
    x1 = float(tmp["x"].iloc[-1])
    y0 = float(tmp["y"].iloc[0])
    y1 = float(tmp["y"].iloc[-1])
    dx = x1 - x0
    if abs(dx) < 1e-12:
        return np.nan
    return float((y1 - y0) / dx)


def run_q3(
    annual_df: pd.DataFrame,
    hourly_by_country_year: dict[tuple[str, int], pd.DataFrame],
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
    validation_findings_df: pd.DataFrame | None = None,
) -> ModuleResult:
    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q3_PARAMS)].iterrows()
    }
    trend_window = max(2, int(params.get("trend_window_years", 3)))
    sr_energy_target = float(params.get("sr_energy_target", 0.01))
    slope_capture_target = float(params.get("slope_capture_target", params.get("trend_capture_ratio_min", 0.0)))

    q1 = run_q1(
        annual_df,
        assumptions_df,
        selection,
        run_id=f"{run_id}_Q1",
        hourly_by_country_year=hourly_by_country_year,
        validation_findings_df=validation_findings_df,
    )
    q2 = run_q2(
        annual_df,
        assumptions_df,
        selection,
        run_id=f"{run_id}_Q2",
        hourly_by_country_year=hourly_by_country_year,
        validation_findings_df=validation_findings_df,
    )

    q1_panel = q1.tables["Q1_year_panel"].copy()
    q1_summary = q1.tables["Q1_country_summary"][["country", "bascule_year_market"]].copy()
    q2_slopes = q2.tables.get("Q2_country_slopes", pd.DataFrame()).copy()

    countries = selection.get("countries", sorted(annual_df["country"].dropna().astype(str).unique().tolist()))
    rows: list[dict[str, Any]] = []
    checks: list[dict[str, str]] = []
    warnings: list[str] = []

    for country in countries:
        c_panel = q1_panel[q1_panel["country"].astype(str) == str(country)].sort_values("year").copy()
        c_sum = q1_summary[q1_summary["country"].astype(str) == str(country)].copy()
        bascule = _safe_float(c_sum["bascule_year_market"].iloc[0], np.nan) if not c_sum.empty else np.nan

        if not np.isfinite(bascule):
            rows.append(
                {
                    "country": country,
                    "reference_year": np.nan,
                    "in_phase2": False,
                    "status": "HORS_SCOPE_PHASE2",
                    "reason_code": "q1_no_bascule",
                    "status_explanation": "Absence de bascule marche Q1.",
                    "stage3_ready_year": False,
                    "phase2_slope_capture_ratio_pv": np.nan,
                    "phase2_slope_method": "insufficient",
                    "trend_capture_ratio_pv": np.nan,
                    "trend_h_negative": np.nan,
                    "stop_possible_if": np.nan,
                    "stop_condition_detail": "non_applicable",
                    "surplus_energy_twh_recent": np.nan,
                    "target_absorption_twh": np.nan,
                    "demand_uplift_twh": np.nan,
                    "inversion_k_demand": np.nan,
                    "inversion_k_demand_status": "insufficient_scope",
                    "inversion_r_mustrun": np.nan,
                    "inversion_r_mustrun_status": "proxy_not_computed",
                    "inversion_f_flex": np.nan,
                    "inversion_f_flex_status": "proxy_not_computed",
                    "additional_absorbed_needed_TWh_year": np.nan,
                    "additional_sink_power_p95_mw": np.nan,
                    "warnings_quality": "q1_no_bascule",
                }
            )
            continue

        c_phase2 = c_panel[c_panel["year"] >= int(bascule)].copy()
        c_phase2["quality_ok"] = c_phase2.get("quality_ok", True).fillna(False).astype(bool)
        c_phase2["crisis_year"] = c_phase2.get("crisis_year", False).fillna(False).astype(bool)
        c_phase2 = c_phase2[c_phase2["quality_ok"] & (~c_phase2["crisis_year"])].sort_values("year")
        if c_phase2.empty:
            rows.append(
                {
                    "country": country,
                    "reference_year": np.nan,
                    "in_phase2": False,
                    "status": "HORS_SCOPE_PHASE2",
                    "reason_code": "phase2_window_empty",
                    "status_explanation": "Fenetre post-bascule vide apres filtres qualite/crise.",
                    "stage3_ready_year": False,
                    "phase2_slope_capture_ratio_pv": np.nan,
                    "phase2_slope_method": "insufficient",
                    "trend_capture_ratio_pv": np.nan,
                    "trend_h_negative": np.nan,
                    "stop_possible_if": np.nan,
                    "stop_condition_detail": "non_applicable",
                    "surplus_energy_twh_recent": np.nan,
                    "target_absorption_twh": np.nan,
                    "demand_uplift_twh": np.nan,
                    "inversion_k_demand": np.nan,
                    "inversion_k_demand_status": "insufficient_scope",
                    "inversion_r_mustrun": np.nan,
                    "inversion_r_mustrun_status": "proxy_not_computed",
                    "inversion_f_flex": np.nan,
                    "inversion_f_flex_status": "proxy_not_computed",
                    "additional_absorbed_needed_TWh_year": np.nan,
                    "additional_sink_power_p95_mw": np.nan,
                    "warnings_quality": "phase2_window_empty",
                }
            )
            continue

        recent = c_phase2.tail(trend_window).copy()
        last = recent.iloc[-1]

        q2_row = q2_slopes[
            (q2_slopes.get("country", pd.Series(dtype=object)).astype(str) == str(country))
            & (q2_slopes.get("tech", pd.Series(dtype=object)).astype(str) == "PV")
        ]
        q2_slope = np.nan
        q2_method = "insufficient"
        if not q2_row.empty:
            q2_slope = _safe_float(q2_row.iloc[0].get("slope"), np.nan)
            q2_method = str(q2_row.iloc[0].get("slope_method", "insufficient"))

        low_price = bool(last.get("low_price_family", False))
        value = bool(last.get("value_family", False))
        physical = bool(last.get("physical_family", False))
        stop_possible = (not low_price) or (not value) or (not physical)
        stop_drivers: list[str] = []
        if not low_price:
            stop_drivers.append("LOW_PRICE_FALSE")
        if not value:
            stop_drivers.append("VALUE_FALSE")
        if not physical:
            stop_drivers.append("PHYSICAL_FALSE")

        surplus_twh = _safe_float(last.get("surplus_twh"), np.nan)
        load_twh = _safe_float(last.get("load_net_twh"), np.nan)
        target_abs_twh = load_twh * sr_energy_target if np.isfinite(load_twh) else np.nan
        demand_uplift_twh = max(0.0, surplus_twh - target_abs_twh) if np.isfinite(surplus_twh) and np.isfinite(target_abs_twh) else np.nan
        k_demand = demand_uplift_twh / load_twh if np.isfinite(demand_uplift_twh) and np.isfinite(load_twh) and load_twh > 0 else np.nan

        trend_capture = _trend_slope(recent.get("year"), recent.get("capture_ratio_pv"))
        trend_hneg = _trend_slope(recent.get("year"), recent.get("h_negative_obs"))

        if stop_possible:
            status = "STOP_POSSIBLE"
            reason_code = "family_relief_detected"
            status_explanation = "Au moins une famille de stress est redevenue inactive."
        else:
            if np.isfinite(q2_slope) and q2_slope >= slope_capture_target:
                status = "PHASE2_IMPROVING"
                reason_code = "capture_slope_non_negative"
                status_explanation = "Pente capture ratio PV non negative sur la fenetre phase 2."
            else:
                status = "PHASE2_ACTIVE"
                reason_code = "all_families_still_active"
                status_explanation = "Familles de stress toujours actives au recent."

        rows.append(
            {
                "country": country,
                "reference_year": int(_safe_float(last.get("year"), np.nan)),
                "in_phase2": True,
                "status": status,
                "reason_code": reason_code,
                "status_explanation": status_explanation,
                "stage3_ready_year": bool(stop_possible),
                "phase2_slope_capture_ratio_pv": q2_slope,
                "phase2_slope_method": q2_method,
                "trend_capture_ratio_pv": trend_capture,
                "trend_h_negative": trend_hneg,
                "stop_possible_if": bool(stop_possible),
                "stop_condition_detail": ";".join(stop_drivers) if stop_drivers else "none",
                "surplus_energy_twh_recent": surplus_twh,
                "target_absorption_twh": target_abs_twh,
                "demand_uplift_twh": demand_uplift_twh,
                "inversion_k_demand": k_demand,
                "inversion_k_demand_status": "proxy_from_surplus_gap" if np.isfinite(k_demand) else "insufficient_data",
                "inversion_r_mustrun": np.nan,
                "inversion_r_mustrun_status": "proxy_not_computed",
                "inversion_f_flex": np.nan,
                "inversion_f_flex_status": "proxy_not_computed",
                "additional_absorbed_needed_TWh_year": demand_uplift_twh,
                "additional_sink_power_p95_mw": np.nan,
                "warnings_quality": "",
            }
        )

    out = pd.DataFrame(rows)
    if not out.empty:
        key_cols = ["phase2_slope_capture_ratio_pv", "demand_uplift_twh", "inversion_k_demand"]
        for _, r in out.iterrows():
            if bool(r.get("in_phase2", False)):
                all_nan = all(not np.isfinite(_safe_float(r.get(c), np.nan)) for c in key_cols)
                if all_nan:
                    checks.append(
                        {
                            "status": "FAIL",
                            "code": "Q3_IN_PHASE2_ALL_NAN",
                            "message": f"{r['country']}: in_phase2 mais colonnes clefs vides.",
                        }
                    )

    checks.extend(build_common_checks(q1_panel))
    if not checks:
        checks.append({"status": "PASS", "code": "Q3_PASS", "message": "Q3 checks pass."})

    kpis = {
        "n_countries": int(out["country"].nunique()) if not out.empty else 0,
        "n_in_phase2": int((out.get("in_phase2") == True).sum()) if not out.empty else 0,
        "n_stop_possible": int((out.get("status") == "STOP_POSSIBLE").sum()) if not out.empty else 0,
    }

    narrative = (
        "Q3 applique une lecture pragmatique de sortie phase 2: statut hors scope explicite, "
        "pente capture issue de Q2, et proxy de demande base sur le surplus annuel."
    )

    return ModuleResult(
        module_id="Q3",
        run_id=run_id,
        selection=selection,
        assumptions_used=assumptions_subset(assumptions_df, Q3_PARAMS),
        kpis=kpis,
        tables={"Q3_status": out},
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
        mode=str(selection.get("mode", "HIST")).upper(),
        scenario_id=selection.get("scenario_id"),
        horizon_year=selection.get("horizon_year"),
    )

