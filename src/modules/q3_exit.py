"""Q3 - Exit from Phase 2 and inversion conditions."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.modules.common import assumptions_subset, robust_linreg
from src.modules.result import ModuleResult

Q3_PARAMS = ["trend_window_years", "sr_energy_target", "far_target", "demand_k_max"]


def _binary_search_lowest(fn, lo: float, hi: float, tol: float = 1e-4, max_iter: int = 40) -> float:
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
        r["param_name"]: float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q3_PARAMS)].iterrows()
    }
    window = int(params.get("trend_window_years", 3))
    sr_target = float(params.get("sr_energy_target", 0.01))
    far_target = float(params.get("far_target", 0.95))
    k_max = float(params.get("demand_k_max", 0.30))

    countries = selection.get("countries", sorted(annual_df["country"].unique()))
    years = selection.get("years", sorted(annual_df["year"].unique()))

    panel = annual_df[annual_df["country"].isin(countries) & annual_df["year"].isin(years)].copy().sort_values(["country", "year"])

    rows = []
    checks = []
    warnings = []

    for country, group in panel.groupby("country"):
        group = group.sort_values("year")
        if len(group) < window:
            continue
        tail = group.tail(window)

        trend_hneg = robust_linreg(tail["year"], tail["h_negative_obs"])["slope"]
        trend_cap = robust_linreg(tail["year"], tail["capture_ratio_pv_vs_ttl"])["slope"]
        trend_sr = robust_linreg(tail["year"], tail["sr_energy"])["slope"]
        trend_far = robust_linreg(tail["year"], tail["far_energy"])["slope"]

        if trend_hneg > 0 and trend_cap < 0:
            status = "degradation"
        elif abs(trend_hneg) <= 10 and abs(trend_cap) <= 0.01:
            status = "stabilisation"
        elif trend_hneg <= -10 and trend_cap >= 0.0:
            status = "amelioration"
        else:
            status = "transition_partielle"

        ref_year = int(group["year"].max())
        ref = hourly_by_country_year.get((country, ref_year))
        if ref is None:
            continue

        def demand_condition(k: float) -> bool:
            temp = ref.copy()
            temp["load_tmp"] = temp["load_mw"] * (1 + k)
            temp["nrl_tmp"] = temp["load_tmp"] - temp["gen_vre_mw"] - temp["gen_must_run_mw"]
            temp["surplus_tmp"] = (-temp["nrl_tmp"]).clip(lower=0.0)
            sr = float(temp["surplus_tmp"].sum()) / float(temp["gen_primary_mw"].sum())
            return sr <= sr_target

        inversion_k = _binary_search_lowest(demand_condition, 0.0, k_max)

        def must_run_condition(r: float) -> bool:
            temp = ref.copy()
            temp["mr_tmp"] = temp["gen_must_run_mw"] * (1 - r)
            temp["nrl_tmp"] = temp["load_mw"] - temp["gen_vre_mw"] - temp["mr_tmp"]
            temp["surplus_tmp"] = (-temp["nrl_tmp"]).clip(lower=0.0)
            sr = float(temp["surplus_tmp"].sum()) / float(temp["gen_primary_mw"].sum())
            return sr <= sr_target

        inversion_r = _binary_search_lowest(must_run_condition, 0.0, 1.0)

        surplus_energy = float(ref["surplus_mw"].fillna(0).sum())
        absorbed_current = float(ref["surplus_absorbed_mw"].fillna(0).sum())
        absorbed_target = far_target * surplus_energy
        additional_abs_needed = max(0.0, absorbed_target - absorbed_current)
        additional_sink_p95 = float(ref["surplus_unabsorbed_mw"].fillna(0).quantile(0.95))

        if inversion_k > 0.25:
            warnings.append(f"{country}: demand-only inversion is very demanding ({inversion_k:.2%})")
        if inversion_r > 0.50:
            warnings.append(f"{country}: must-run-only inversion is very demanding ({inversion_r:.2%})")

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
    if not checks:
        checks.append({"status": "PASS", "message": "Q3 checks pass"})

    kpis = {
        "n_countries": int(out["country"].nunique()) if not out.empty else 0,
        "n_amelioration": int((out.get("status") == "amelioration").sum()) if not out.empty else 0,
    }

    narrative = (
        "Q3 detects exit from Phase 2 from historical trends and provides static counterfactuals on "
        "demand, must-run, and additional flexibility."
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
    )
