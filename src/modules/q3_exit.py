"""Q3 - Exit from Phase 2 and inversion conditions."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.modules.common import assumptions_subset, robust_linreg
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
]


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


def _theil_sen_slope(x: pd.Series, y: pd.Series) -> float:
    xx = pd.to_numeric(x, errors="coerce")
    yy = pd.to_numeric(y, errors="coerce")
    tmp = pd.DataFrame({"x": xx, "y": yy}).dropna()
    if len(tmp) < 2:
        return np.nan
    vals = tmp.to_numpy(dtype=float)
    slopes: list[float] = []
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            dx = vals[j, 0] - vals[i, 0]
            if abs(dx) <= 1e-12:
                continue
            slopes.append((vals[j, 1] - vals[i, 1]) / dx)
    if not slopes:
        return np.nan
    return float(np.median(np.array(slopes, dtype=float)))


def _trend_with_outliers(df: pd.DataFrame, col: str) -> dict[str, Any]:
    x = pd.to_numeric(df.get("year"), errors="coerce")
    y = pd.to_numeric(df.get(col), errors="coerce")
    tmp = pd.DataFrame({"year": x, "y": y}).dropna()
    if len(tmp) < 2:
        return {"slope_ols": np.nan, "slope_theil_sen": np.nan, "slope_ols_no_outliers": np.nan, "n": int(len(tmp)), "reason": "insufficient_points"}
    std = float(tmp["y"].std(ddof=0))
    if std > 0:
        z = (tmp["y"] - float(tmp["y"].mean())) / std
        tmp["outlier"] = z.abs() > 2.5
    else:
        tmp["outlier"] = False
    ols = robust_linreg(tmp["year"], tmp["y"])
    ts = _theil_sen_slope(tmp["year"], tmp["y"])
    no = tmp[~tmp["outlier"]]
    if len(no) >= 2:
        ols_no = robust_linreg(no["year"], no["y"])
    else:
        ols_no = {"slope": np.nan}
    return {
        "slope_ols": _safe_float(ols.get("slope"), np.nan),
        "slope_theil_sen": _safe_float(ts, np.nan),
        "slope_ols_no_outliers": _safe_float(ols_no.get("slope"), np.nan),
        "n": int(len(tmp)),
        "outlier_years": ",".join([str(int(v)) for v in no[no["outlier"]]["year"].tolist()]) if "outlier" in no.columns else "",
        "reason": "ok",
    }


def _apply_lever_proxy(tail: pd.DataFrame, k_demand: float = 0.0, r_mustrun: float = 0.0, f_flex: float = 0.0) -> pd.DataFrame:
    t = tail.copy()
    k = float(max(0.0, k_demand))
    r = float(np.clip(r_mustrun, 0.0, 1.0))
    f = float(max(0.0, f_flex))
    h_factor = 1.0 + 1.6 * k + 1.4 * r + 1.2 * f
    t["h_negative_obs"] = pd.to_numeric(t.get("h_negative_obs"), errors="coerce") / h_factor
    t["h_below_5_obs"] = pd.to_numeric(t.get("h_below_5_obs"), errors="coerce") / h_factor
    t["capture_ratio_pv_vs_ttl"] = (pd.to_numeric(t.get("capture_ratio_pv_vs_ttl"), errors="coerce") + 0.08 * k + 0.10 * r + 0.08 * f).clip(lower=0.0, upper=2.0)
    t["sr_energy"] = pd.to_numeric(t.get("sr_energy"), errors="coerce") / (1.0 + k)
    far = pd.to_numeric(t.get("far_energy"), errors="coerce")
    t["far_energy"] = 1.0 - (1.0 - far) / (1.0 + 0.5 * k + 0.7 * r + 1.0 * f)
    return t


def _stage3_ready_from_tail(tail: pd.DataFrame, far_target: float, trend_capture_min: float) -> dict[str, Any]:
    th = _trend_with_outliers(tail, "h_negative_obs")
    tc = _trend_with_outliers(tail, "capture_ratio_pv_vs_ttl")
    trend_hneg = _safe_float(th["slope_theil_sen"], np.nan)
    if not np.isfinite(trend_hneg):
        trend_hneg = _safe_float(th["slope_ols"], np.nan)
    trend_capture = _safe_float(tc["slope_theil_sen"], np.nan)
    if not np.isfinite(trend_capture):
        trend_capture = _safe_float(tc["slope_ols"], np.nan)
    far_last = _safe_float(pd.to_numeric(tail.get("far_energy"), errors="coerce").iloc[-1], np.nan) if not tail.empty else np.nan
    ready = bool(
        np.isfinite(far_last)
        and far_last >= float(far_target)
        and np.isfinite(trend_hneg)
        and trend_hneg <= 0.0
        and np.isfinite(trend_capture)
        and trend_capture >= float(trend_capture_min)
    )
    return {
        "stage3_ready": ready,
        "trend_h_negative": trend_hneg,
        "trend_capture_ratio_pv_vs_ttl": trend_capture,
        "trend_h_negative_ols": _safe_float(th["slope_ols"], np.nan),
        "trend_h_negative_ols_no_outliers": _safe_float(th["slope_ols_no_outliers"], np.nan),
        "trend_capture_ols": _safe_float(tc["slope_ols"], np.nan),
        "trend_capture_ols_no_outliers": _safe_float(tc["slope_ols_no_outliers"], np.nan),
        "trend_points_n": int(min(th["n"], tc["n"])),
    }


def _solve_required_lever(
    fn,
    max_bound: float,
    *,
    tol: float = 1e-4,
    max_iter: int = 40,
) -> tuple[float | None, str]:
    if fn(0.0):
        return 0.0, "already_ready"
    hi = float(max(0.0, max_bound))
    if hi <= 0:
        return None, "invalid_bounds"
    if not fn(hi):
        return None, "beyond_bounds"
    lo = 0.0
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        if fn(mid):
            hi = mid
        else:
            lo = mid
        if abs(hi - lo) <= tol:
            break
    return float(hi), "ok"


def _hourly_after_lever(ref: pd.DataFrame, k_demand: float, r_mustrun: float, f_flex: float) -> dict[str, Any]:
    load = pd.to_numeric(ref.get("load_mw"), errors="coerce").fillna(0.0).to_numpy(dtype=float)
    vre = pd.to_numeric(ref.get("gen_vre_mw"), errors="coerce").fillna(0.0).to_numpy(dtype=float)
    mr = pd.to_numeric(ref.get("gen_must_run_mw"), errors="coerce").fillna(0.0).to_numpy(dtype=float)
    flex = pd.to_numeric(ref.get("flex_sink_observed_mw"), errors="coerce").fillna(0.0).to_numpy(dtype=float)
    if not np.isfinite(flex).any():
        flex = (
            pd.to_numeric(ref.get("exports_mw"), errors="coerce").fillna(0.0).clip(lower=0.0).to_numpy(dtype=float)
            + pd.to_numeric(ref.get("psh_pump_mw"), errors="coerce").fillna(0.0).clip(lower=0.0).to_numpy(dtype=float)
        )

    k = float(max(0.0, k_demand))
    r = float(np.clip(r_mustrun, 0.0, 1.0))
    f = float(max(0.0, f_flex))
    load_adj = load * (1.0 + k)
    mr_adj = mr * (1.0 - r)
    nrl = load_adj - vre - mr_adj
    surplus = np.maximum(0.0, -nrl)
    absorbed = np.minimum(surplus, flex * (1.0 + f))
    unabs = np.maximum(0.0, surplus - absorbed)

    base_unabs = pd.to_numeric(ref.get("surplus_unabsorbed_mw"), errors="coerce").fillna(0.0).to_numpy(dtype=float)
    delta_unabs = float(np.sum(base_unabs) - np.sum(unabs))
    additional_sink_hourly = np.maximum(0.0, absorbed - np.minimum(surplus, flex))
    if np.isfinite(additional_sink_hourly).any() and np.sum(additional_sink_hourly) > 0:
        sink_p95 = float(np.nanquantile(additional_sink_hourly, 0.95))
    else:
        hrs = int(np.sum(surplus > 0))
        sink_p95 = delta_unabs / max(1, hrs)

    return {
        "nrl": nrl,
        "surplus": surplus,
        "absorbed": absorbed,
        "unabs": unabs,
        "delta_unabs_mwh": delta_unabs,
        "sink_power_p95_mw": sink_p95,
    }


def run_q3(
    annual_df: pd.DataFrame,
    hourly_by_country_year: dict[tuple[str, int], pd.DataFrame],
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
) -> ModuleResult:
    all_params = {str(r["param_name"]): float(r["param_value"]) for _, r in assumptions_df.iterrows()}
    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q3_PARAMS)].iterrows()
    }
    window = int(params.get("trend_window_years", 3))
    require_recent_stage2 = int(params.get("require_recent_stage2", 1)) == 1
    recent_hneg_min_hist = float(params.get("stage2_recent_h_negative_min", 200.0))
    recent_hneg_min_scen = float(params.get("stage2_recent_h_negative_min_scen", 80.0))
    recent_sr_min_scen = float(params.get("stage2_recent_sr_energy_min_scen", 0.02))
    is_scen = str(selection.get("mode", "HIST")).upper() == "SCEN"
    recent_hneg_min = recent_hneg_min_scen if is_scen else recent_hneg_min_hist
    trend_cap_min = float(params.get("trend_capture_ratio_min", 0.0))
    far_target = float(params.get("far_target", 0.95))
    k_max = float(params.get("demand_k_max", 1.0))

    countries = selection.get("countries", sorted(annual_df["country"].dropna().unique().tolist()))
    years = selection.get("years", sorted(annual_df["year"].dropna().unique().tolist()))
    panel = annual_df[annual_df["country"].isin(countries) & annual_df["year"].isin(years)].copy().sort_values(["country", "year"])

    rows: list[dict[str, Any]] = []
    checks: list[dict[str, str]] = []
    warnings: list[str] = []
    checked_rows: list[pd.Series] = []

    for country, group in panel.groupby("country"):
        group = group.sort_values("year")
        if len(group) < window:
            warnings.append(f"{country}: historique insuffisant pour tendance (window={window}).")
            continue
        tail = group.tail(window).copy()
        checked_rows.append(tail.iloc[-1])

        recent_hneg = float(pd.to_numeric(tail["h_negative_obs"], errors="coerce").max())
        recent_sr = float(pd.to_numeric(tail["sr_energy"], errors="coerce").max())
        has_recent_stage2 = (recent_hneg >= recent_hneg_min) or (is_scen and recent_sr >= recent_sr_min_scen)
        if require_recent_stage2 and not has_recent_stage2:
            status = "hors_scope_stage2"
        else:
            status = "transition_partielle"

        base_stage3 = _stage3_ready_from_tail(tail, far_target=far_target, trend_capture_min=trend_cap_min)
        if status != "hors_scope_stage2" and bool(base_stage3["stage3_ready"]):
            status = "stage3_ready"
        elif status != "hors_scope_stage2":
            if np.isfinite(base_stage3["trend_h_negative"]) and base_stage3["trend_h_negative"] > 0 and np.isfinite(base_stage3["trend_capture_ratio_pv_vs_ttl"]) and base_stage3["trend_capture_ratio_pv_vs_ttl"] < 0:
                status = "degradation"
            elif np.isfinite(base_stage3["trend_h_negative"]) and abs(base_stage3["trend_h_negative"]) <= 1e-6:
                status = "stabilisation"
            elif np.isfinite(base_stage3["trend_h_negative"]) and base_stage3["trend_h_negative"] < 0:
                status = "amelioration"

        ref_year = int(group["year"].max())
        ref = hourly_by_country_year.get((country, ref_year))
        if ref is None or ref.empty:
            warnings.append(f"{country}: horaire manquant pour {ref_year}, leviers horaires limites.")
            ref = pd.DataFrame()

        def _ready_with(k: float = 0.0, r: float = 0.0, f: float = 0.0) -> bool:
            adj = _apply_lever_proxy(tail, k_demand=k, r_mustrun=r, f_flex=f)
            stage = _stage3_ready_from_tail(adj, far_target=far_target, trend_capture_min=trend_cap_min)
            return bool(stage["stage3_ready"])

        req_k, req_k_status = _solve_required_lever(lambda x: _ready_with(k=x, r=0.0, f=0.0), max_bound=k_max)
        req_r, req_r_status = _solve_required_lever(lambda x: _ready_with(k=0.0, r=x, f=0.0), max_bound=1.0)
        req_f, req_f_status = _solve_required_lever(lambda x: _ready_with(k=0.0, r=0.0, f=x), max_bound=1.0)

        lever_for_absorption = req_f if req_f is not None else 0.0
        if not ref.empty:
            base_hourly = _hourly_after_lever(ref, k_demand=0.0, r_mustrun=0.0, f_flex=0.0)
            after_hourly = _hourly_after_lever(ref, k_demand=0.0, r_mustrun=0.0, f_flex=float(lever_for_absorption))
            delta_unabs = float(max(0.0, after_hourly["delta_unabs_mwh"]))
            sink_p95 = float(after_hourly["sink_power_p95_mw"])
        else:
            base_unabs_twh = _safe_float(group.tail(1).get("surplus_unabsorbed_twh", pd.Series([np.nan])).iloc[0], np.nan)
            if np.isfinite(base_unabs_twh):
                delta_unabs = base_unabs_twh * 1e6 * float(max(0.0, lever_for_absorption))
                sink_p95 = delta_unabs / 8760.0
            else:
                delta_unabs = np.nan
                sink_p95 = np.nan

        if req_k is not None and req_k > 0.25:
            checks.append({"status": "WARN", "code": "Q3_INVERSION_K_DEMAND_LARGE", "message": f"{country}: required_k_demand={req_k:.1%} (>25%)."})
        if req_r is not None and req_r > 0.50:
            checks.append({"status": "WARN", "code": "Q3_INVERSION_R_MUSTRUN_LARGE", "message": f"{country}: required_r_mustrun={req_r:.1%} (>50%)."})
        if req_k is None and req_k_status == "beyond_bounds":
            checks.append({"status": "WARN", "code": "Q3_INVERSION_K_BEYOND_BOUNDS", "message": f"{country}: demande requise au-dela de la borne."})
        if req_r is None and req_r_status == "beyond_bounds":
            checks.append({"status": "WARN", "code": "Q3_INVERSION_R_BEYOND_BOUNDS", "message": f"{country}: flexibilisation must-run au-dela de la borne."})
        if req_f is None and req_f_status == "beyond_bounds":
            checks.append({"status": "WARN", "code": "Q3_INVERSION_F_BEYOND_BOUNDS", "message": f"{country}: flexibilite additionnelle au-dela de la borne."})

        rows.append(
            {
                "country": country,
                "reference_year": ref_year,
                "trend_window_years": window,
                "status": status,
                "stage3_ready_year": bool(base_stage3["stage3_ready"]),
                "trend_h_negative": base_stage3["trend_h_negative"],
                "trend_capture_ratio_pv_vs_ttl": base_stage3["trend_capture_ratio_pv_vs_ttl"],
                "trend_h_negative_ols": base_stage3["trend_h_negative_ols"],
                "trend_h_negative_ols_no_outliers": base_stage3["trend_h_negative_ols_no_outliers"],
                "trend_capture_ols": base_stage3["trend_capture_ols"],
                "trend_capture_ols_no_outliers": base_stage3["trend_capture_ols_no_outliers"],
                "trend_points_n": base_stage3["trend_points_n"],
                "inversion_k_demand": req_k,
                "inversion_k_demand_status": req_k_status,
                "inversion_r_mustrun": req_r,
                "inversion_r_mustrun_status": req_r_status,
                "inversion_f_flex": req_f,
                "inversion_f_flex_status": req_f_status,
                "additional_absorbed_needed_TWh_year": delta_unabs / 1e6 if np.isfinite(delta_unabs) else np.nan,
                "additional_sink_power_p95_mw": sink_p95,
                "warnings_quality": "" if str(group["quality_flag"].iloc[-1]).upper() != "FAIL" else "quality_fail",
            }
        )

    out = pd.DataFrame(rows)
    checked_df = pd.DataFrame(checked_rows) if checked_rows else pd.DataFrame()
    checks.extend(build_common_checks(checked_df))
    if not checks:
        checks.append({"status": "PASS", "code": "Q3_PASS", "message": "Q3 checks pass."})

    kpis = {
        "n_countries": int(out["country"].nunique()) if not out.empty else 0,
        "n_stage3_ready": int((out.get("stage3_ready_year") == True).sum()) if not out.empty else 0,
        "n_degradation": int((out.get("status") == "degradation").sum()) if not out.empty else 0,
    }

    narrative = (
        "Q3 teste explicitement la readiness Phase 3 (FAR cible + tendance h_negative + tendance capture), "
        "et quantifie les leviers requis (demande, must-run, flex) sans saturation silencieuse."
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

