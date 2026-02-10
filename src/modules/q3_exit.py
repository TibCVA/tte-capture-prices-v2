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
    "sr_energy_target",
    "far_target",
    "demand_k_max",
]


def _binary_search_lowest(fn, lo: float, hi: float, tol: float = 1e-4, max_iter: int = 40) -> float:
    if fn(lo):
        return lo
    if not fn(hi):
        return hi
    best = hi
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        if fn(mid):
            best = mid
            hi = mid
        else:
            lo = mid
        if abs(hi - lo) <= tol:
            break
    return best


def run_q3(
    annual_df: pd.DataFrame,
    hourly_by_country_year: dict[tuple[str, int], pd.DataFrame],
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
) -> ModuleResult:
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
    trend_hneg_max = float(params.get("trend_h_negative_max", -10.0))
    trend_cap_min = float(params.get("trend_capture_ratio_min", 0.0))
    sr_target = float(params.get("sr_energy_target", 0.01))
    far_target = float(params.get("far_target", 0.95))
    k_max = float(params.get("demand_k_max", 0.30))

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
        tail = group.tail(window)
        checked_rows.append(tail.iloc[-1])

        trend_hneg = robust_linreg(tail["year"], tail["h_negative_obs"])["slope"]
        trend_cap = robust_linreg(tail["year"], tail["capture_ratio_pv_vs_ttl"])["slope"]
        trend_sr = robust_linreg(tail["year"], tail["sr_energy"])["slope"]
        trend_far = robust_linreg(tail["year"], tail["far_energy"])["slope"]

        recent_hneg = float(pd.to_numeric(tail["h_negative_obs"], errors="coerce").max())
        recent_sr = float(pd.to_numeric(tail["sr_energy"], errors="coerce").max())
        if is_scen:
            has_recent_stage2 = (recent_hneg >= recent_hneg_min) or (recent_sr >= recent_sr_min_scen)
        else:
            has_recent_stage2 = recent_hneg >= recent_hneg_min
        if require_recent_stage2 and not has_recent_stage2:
            status = "hors_scope_stage2"
        elif trend_hneg > 0 and trend_cap < 0:
            status = "degradation"
        elif abs(trend_hneg) <= abs(trend_hneg_max) and abs(trend_cap) <= 0.01:
            status = "stabilisation"
        elif trend_hneg <= trend_hneg_max and trend_cap >= trend_cap_min:
            status = "amelioration"
        else:
            status = "transition_partielle"

        ref_year = int(group["year"].max())
        ref = hourly_by_country_year.get((country, ref_year))
        if ref is None:
            warnings.append(f"{country}: horaire manquant pour {ref_year}, contre-factuels non calcules.")
            continue

        def demand_condition(k: float) -> bool:
            temp = ref.copy()
            temp["load_tmp"] = pd.to_numeric(temp["load_mw"], errors="coerce") * (1 + k)
            temp["nrl_tmp"] = temp["load_tmp"] - pd.to_numeric(temp["gen_vre_mw"], errors="coerce") - pd.to_numeric(temp["gen_must_run_mw"], errors="coerce")
            temp["surplus_tmp"] = (-temp["nrl_tmp"]).clip(lower=0.0)
            gen_primary_sum = float(pd.to_numeric(temp["gen_primary_mw"], errors="coerce").sum())
            if gen_primary_sum <= 0:
                return False
            sr = float(temp["surplus_tmp"].sum()) / gen_primary_sum
            return sr <= sr_target

        inversion_k = _binary_search_lowest(demand_condition, 0.0, k_max)

        def must_run_condition(r: float) -> bool:
            temp = ref.copy()
            temp["mr_tmp"] = pd.to_numeric(temp["gen_must_run_mw"], errors="coerce") * (1 - r)
            temp["nrl_tmp"] = pd.to_numeric(temp["load_mw"], errors="coerce") - pd.to_numeric(temp["gen_vre_mw"], errors="coerce") - temp["mr_tmp"]
            temp["surplus_tmp"] = (-temp["nrl_tmp"]).clip(lower=0.0)
            gen_primary_sum = float(pd.to_numeric(temp["gen_primary_mw"], errors="coerce").sum())
            if gen_primary_sum <= 0:
                return False
            sr = float(temp["surplus_tmp"].sum()) / gen_primary_sum
            return sr <= sr_target

        inversion_r = _binary_search_lowest(must_run_condition, 0.0, 1.0)

        surplus_energy = float(pd.to_numeric(ref["surplus_mw"], errors="coerce").fillna(0).sum())
        absorbed_current = float(pd.to_numeric(ref["surplus_absorbed_mw"], errors="coerce").fillna(0).sum())
        absorbed_target = far_target * surplus_energy
        additional_abs_needed = max(0.0, absorbed_target - absorbed_current)
        additional_sink_p95 = float(pd.to_numeric(ref["surplus_unabsorbed_mw"], errors="coerce").fillna(0).quantile(0.95))

        if inversion_k > 0.25:
            checks.append({"status": "WARN", "code": "Q3_DEMAND_HIGH", "message": f"{country}: inversion_k_demand={inversion_k:.1%} (>25%)."})
        if inversion_r > 0.50:
            checks.append({"status": "WARN", "code": "Q3_MUSTRUN_HIGH", "message": f"{country}: inversion_r_mustrun={inversion_r:.1%} (>50%)."})
        if additional_abs_needed == 0.0:
            checks.append({"status": "INFO", "code": "Q3_FAR_ALREADY_REACHED", "message": f"{country}: FAR cible deja atteinte."})

        rows.append(
            {
                "country": country,
                "reference_year": ref_year,
                "trend_window_years": window,
                "trend_h_negative": trend_hneg,
                "trend_capture_ratio_pv_vs_ttl": trend_cap,
                "trend_sr_energy": trend_sr,
                "trend_far_energy": trend_far,
                "status": status,
                "inversion_k_demand": inversion_k,
                "inversion_r_mustrun": inversion_r,
                "additional_absorbed_needed_TWh_year": additional_abs_needed / 1e6,
                "additional_sink_power_p95_mw": additional_sink_p95,
                "warnings_quality": "" if group["quality_flag"].iloc[-1] != "FAIL" else "quality_fail",
            }
        )

    out = pd.DataFrame(rows)
    checked_df = pd.DataFrame(checked_rows) if checked_rows else pd.DataFrame()
    checks.extend(build_common_checks(checked_df))
    if not checks:
        checks.append({"status": "PASS", "code": "Q3_PASS", "message": "Q3 checks pass."})

    kpis = {
        "n_countries": int(out["country"].nunique()) if not out.empty else 0,
        "n_amelioration": int((out.get("status") == "amelioration").sum()) if not out.empty else 0,
        "n_degradation": int((out.get("status") == "degradation").sum()) if not out.empty else 0,
    }

    narrative = (
        "Q3 evalue la sortie de Phase 2 via tendances historiques glissantes "
        "et calcule des ordres de grandeur d'inversion (demande, must-run, flex)."
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
