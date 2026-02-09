"""Q1 - Phase 1 to Phase 2 transition analysis."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.modules.common import assumptions_subset
from src.modules.result import ModuleResult

Q1_PARAMS = [
    "h_negative_stage2_min",
    "h_negative_stage2_strong",
    "h_below_5_stage2_min",
    "capture_ratio_pv_vs_ttl_stage2_max",
    "capture_ratio_pv_vs_ttl_crisis_max",
    "days_spread_gt50_stage2_min",
    "sr_energy_material_min",
    "far_energy_tension_max",
    "ir_p10_high_min",
    "regime_coherence_min_for_causality",
]


def _market_score(row: pd.Series, p: dict[str, Any]) -> int:
    score = 0
    if row.get("h_negative_obs", 0) >= p["h_negative_stage2_min"]:
        score += 1
    if row.get("h_negative_obs", 0) >= p["h_negative_stage2_strong"]:
        score += 2
    if row.get("h_below_5_obs", 0) >= p["h_below_5_stage2_min"]:
        score += 1
    if row.get("capture_ratio_pv_vs_ttl", np.nan) <= p["capture_ratio_pv_vs_ttl_stage2_max"]:
        score += 1
    if row.get("capture_ratio_pv_vs_ttl", np.nan) <= p["capture_ratio_pv_vs_ttl_crisis_max"]:
        score += 2
    if row.get("days_spread_gt50", 0) >= p["days_spread_gt50_stage2_min"]:
        score += 1
    return score


def run_q1(annual_df: pd.DataFrame, assumptions_df: pd.DataFrame, selection: dict[str, Any], run_id: str) -> ModuleResult:
    countries = selection.get("countries", sorted(annual_df["country"].unique()))
    years = selection.get("years", sorted(annual_df["year"].unique()))

    panel = annual_df[annual_df["country"].isin(countries) & annual_df["year"].isin(years)].copy()
    panel = panel.sort_values(["country", "year"]).reset_index(drop=True)

    params = {
        r["param_name"]: float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q1_PARAMS)].iterrows()
    }

    panel["stage2_market_score"] = panel.apply(lambda row: _market_score(row, params), axis=1)
    panel["phase_market"] = np.where(panel["stage2_market_score"] >= 2, "phase2", "phase1")

    panel["stress_phys_state"] = np.select(
        [
            panel["sr_energy"] < params["sr_energy_material_min"],
            (panel["sr_energy"] >= params["sr_energy_material_min"]) & (panel["far_energy"] > params["far_energy_tension_max"]),
            (panel["sr_energy"] >= params["sr_energy_material_min"]) & (panel["far_energy"] <= params["far_energy_tension_max"]),
        ],
        [
            "pas_de_surplus_structurel",
            "surplus_present_mais_absorbe",
            "surplus_non_absorbe",
        ],
        default="unknown",
    )

    panel["quality_ok"] = panel["quality_flag"].fillna("WARN") != "FAIL"

    summary_rows = []
    warnings = []
    for country, group in panel.groupby("country"):
        group = group.sort_values("year")
        market_candidates = group[(group["phase_market"] == "phase2") & group["quality_ok"]]
        physical_candidates = group[
            (group["sr_energy"] >= params["sr_energy_material_min"])
            & (group["far_energy"] <= params["far_energy_tension_max"])
        ]

        market_year = int(market_candidates["year"].min()) if not market_candidates.empty else np.nan
        physical_year = int(physical_candidates["year"].min()) if not physical_candidates.empty else np.nan

        if np.isfinite(market_year):
            at = group[group["year"] == market_year].iloc[0]
            drivers = []
            if at["sr_energy"] >= params["sr_energy_material_min"]:
                drivers.append("SR")
            if at["far_energy"] <= params["far_energy_tension_max"]:
                drivers.append("FAR")
            if at["ir_p10"] >= params["ir_p10_high_min"]:
                drivers.append("IR")
            if at["h_negative_obs"] >= params["h_negative_stage2_min"]:
                drivers.append("h_negative")
            confidence = 1.0
            if at.get("regime_coherence", 1.0) < params["regime_coherence_min_for_causality"]:
                confidence -= 0.3
                warnings.append(f"{country}: regime_coherence low around transition")
            if at.get("completeness", 1.0) < 0.98:
                confidence -= 0.2
            confidence = max(0.0, min(1.0, confidence))
        else:
            at = group.iloc[-1]
            drivers = []
            confidence = 0.0

        summary_rows.append(
            {
                "country": country,
                "bascule_year_market": market_year,
                "bascule_year_physical": physical_year,
                "bascule_confidence": confidence,
                "drivers_at_bascule": ", ".join(drivers[:3]),
                "sr_energy_at_bascule": at.get("sr_energy", np.nan),
                "far_energy_at_bascule": at.get("far_energy", np.nan),
                "ir_p10_at_bascule": at.get("ir_p10", np.nan),
                "ttl_at_bascule": at.get("ttl_eur_mwh", np.nan),
                "capture_ratio_pv_vs_ttl_at_bascule": at.get("capture_ratio_pv_vs_ttl", np.nan),
                "h_negative_at_bascule": at.get("h_negative_obs", np.nan),
                "notes_quality": "coherence_low" if at.get("regime_coherence", 1.0) < params["regime_coherence_min_for_causality"] else "ok",
            }
        )

    summary = pd.DataFrame(summary_rows)

    checks = []
    for _, row in panel.iterrows():
        if row["stage2_market_score"] >= 2 and row["h_negative_obs"] < 100 and row["capture_ratio_pv_vs_ttl"] > 0.9:
            checks.append({"status": "WARN", "message": f"{row['country']} {int(row['year'])}: transition inconsistent with market symptoms"})
    if not checks:
        checks.append({"status": "PASS", "message": "Q1 checks pass"})

    kpis = {
        "n_countries": int(summary["country"].nunique()),
        "n_bascule_detected": int(summary["bascule_year_market"].notna().sum()),
    }

    narrative = (
        "Q1 detects transition to Phase 2 using independent market and physical diagnostics. "
        "Joint reading of SR/FAR/IR provides system context while price and capture symptoms confirm observed transition."
    )

    return ModuleResult(
        module_id="Q1",
        run_id=run_id,
        selection=selection,
        assumptions_used=assumptions_subset(assumptions_df, Q1_PARAMS),
        kpis=kpis,
        tables={"Q1_country_summary": summary, "Q1_year_panel": panel},
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
    )
