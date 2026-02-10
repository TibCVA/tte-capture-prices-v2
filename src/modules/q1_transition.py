"""Q1 - Phase 1 to Phase 2 transition analysis."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.modules.common import assumptions_subset
from src.modules.reality_checks import build_common_checks
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
    "stage1_h_negative_max",
    "stage1_h_below_5_max",
    "stage1_capture_ratio_pv_vs_ttl_min",
    "stage1_days_spread_gt50_max",
]


def _safe_param(params: dict[str, float], key: str, default: float) -> float:
    v = params.get(key, default)
    try:
        return float(v)
    except Exception:
        return float(default)


def _market_score(row: pd.Series, p: dict[str, float]) -> int:
    score = 0
    if float(row.get("h_negative_obs", 0.0)) >= _safe_param(p, "h_negative_stage2_min", 200.0):
        score += 1
    if float(row.get("h_negative_obs", 0.0)) >= _safe_param(p, "h_negative_stage2_strong", 300.0):
        score += 2
    if float(row.get("h_below_5_obs", 0.0)) >= _safe_param(p, "h_below_5_stage2_min", 500.0):
        score += 1
    if float(row.get("capture_ratio_pv_vs_ttl", np.nan)) <= _safe_param(p, "capture_ratio_pv_vs_ttl_stage2_max", 0.8):
        score += 1
    if float(row.get("capture_ratio_pv_vs_ttl", np.nan)) <= _safe_param(p, "capture_ratio_pv_vs_ttl_crisis_max", 0.7):
        score += 2
    if float(row.get("days_spread_gt50", 0.0)) >= _safe_param(p, "days_spread_gt50_stage2_min", 150.0):
        score += 1
    return score


def _is_stage1(row: pd.Series, p: dict[str, float]) -> bool:
    return bool(
        float(row.get("h_negative_obs", np.nan)) <= _safe_param(p, "stage1_h_negative_max", 100.0)
        and float(row.get("h_below_5_obs", np.nan)) <= _safe_param(p, "stage1_h_below_5_max", 300.0)
        and float(row.get("capture_ratio_pv_vs_ttl", np.nan)) >= _safe_param(p, "stage1_capture_ratio_pv_vs_ttl_min", 0.9)
        and float(row.get("days_spread_gt50", np.nan)) <= _safe_param(p, "stage1_days_spread_gt50_max", 120.0)
    )


def run_q1(annual_df: pd.DataFrame, assumptions_df: pd.DataFrame, selection: dict[str, Any], run_id: str) -> ModuleResult:
    countries = selection.get("countries", sorted(annual_df["country"].dropna().unique().tolist()))
    years = selection.get("years", sorted(annual_df["year"].dropna().unique().tolist()))

    panel = annual_df[annual_df["country"].isin(countries) & annual_df["year"].isin(years)].copy()
    panel = panel.sort_values(["country", "year"]).reset_index(drop=True)

    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q1_PARAMS)].iterrows()
    }

    panel["stage2_market_score"] = panel.apply(lambda row: _market_score(row, params), axis=1)
    panel["is_stage1_criteria"] = panel.apply(lambda row: _is_stage1(row, params), axis=1)
    panel["phase_market"] = np.select(
        [
            panel["stage2_market_score"] >= 2,
            panel["is_stage1_criteria"],
        ],
        [
            "phase2",
            "phase1",
        ],
        default="uncertain",
    )

    panel["stress_phys_state"] = np.select(
        [
            panel["sr_energy"] < _safe_param(params, "sr_energy_material_min", 0.01),
            (panel["sr_energy"] >= _safe_param(params, "sr_energy_material_min", 0.01))
            & (panel["far_energy"] > _safe_param(params, "far_energy_tension_max", 0.95)),
            (panel["sr_energy"] >= _safe_param(params, "sr_energy_material_min", 0.01))
            & (panel["far_energy"] <= _safe_param(params, "far_energy_tension_max", 0.95)),
        ],
        [
            "pas_de_surplus_structurel",
            "surplus_present_mais_absorbe",
            "surplus_non_absorbe",
        ],
        default="unknown",
    )

    panel["quality_ok"] = panel["quality_flag"].fillna("WARN") != "FAIL"
    panel["flag_h_negative_stage2"] = panel["h_negative_obs"] >= _safe_param(params, "h_negative_stage2_min", 200.0)
    panel["flag_h_below_5_stage2"] = panel["h_below_5_obs"] >= _safe_param(params, "h_below_5_stage2_min", 500.0)
    panel["flag_capture_stage2"] = panel["capture_ratio_pv_vs_ttl"] <= _safe_param(params, "capture_ratio_pv_vs_ttl_stage2_max", 0.8)
    panel["flag_days_spread_stage2"] = panel["days_spread_gt50"] >= _safe_param(params, "days_spread_gt50_stage2_min", 150.0)
    panel["flag_sr_stress"] = panel["sr_energy"] >= _safe_param(params, "sr_energy_material_min", 0.01)
    panel["flag_far_tension"] = panel["far_energy"] <= _safe_param(params, "far_energy_tension_max", 0.95)
    panel["flag_ir_high"] = panel["ir_p10"] >= _safe_param(params, "ir_p10_high_min", 0.70)

    checks: list[dict[str, str]] = []
    warnings: list[str] = []

    summary_rows: list[dict[str, Any]] = []
    for country, group in panel.groupby("country"):
        group = group.sort_values("year")
        market_candidates = group[
            (group["phase_market"] == "phase2")
            & (group["quality_ok"])
            & (group["capture_ratio_pv_vs_ttl"].notna())
        ]
        physical_candidates = group[
            (group["sr_energy"] >= _safe_param(params, "sr_energy_material_min", 0.01))
            & (group["far_energy"] <= _safe_param(params, "far_energy_tension_max", 0.95))
            & (group["quality_ok"])
        ]

        market_year = int(market_candidates["year"].min()) if not market_candidates.empty else np.nan
        physical_year = int(physical_candidates["year"].min()) if not physical_candidates.empty else np.nan

        at = group[group["year"] == market_year].iloc[0] if np.isfinite(market_year) else group.iloc[-1]
        drivers: list[str] = []
        if at.get("flag_sr_stress", False):
            drivers.append("SR")
        if at.get("flag_far_tension", False):
            drivers.append("FAR")
        if at.get("flag_ir_high", False):
            drivers.append("IR")
        if at.get("flag_h_negative_stage2", False):
            drivers.append("h_negative")
        if at.get("flag_capture_stage2", False):
            drivers.append("capture_ratio")

        confidence = 1.0 if np.isfinite(market_year) else 0.0
        if float(at.get("regime_coherence", 1.0)) < _safe_param(params, "regime_coherence_min_for_causality", 0.55):
            confidence -= 0.30
            warnings.append(f"{country}: regime_coherence faible autour de la bascule.")
        if float(at.get("completeness", 1.0)) < 0.98:
            confidence -= 0.20
            warnings.append(f"{country}: completude < 0.98 autour de la bascule.")
        confidence = max(0.0, min(1.0, confidence))

        if np.isfinite(market_year) and pd.isna(at.get("capture_ratio_pv_vs_ttl", np.nan)):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q1_CAPTURE_NAN_BASCULE",
                    "message": f"{country}: bascule detectee avec capture_ratio_pv_vs_ttl NaN.",
                }
            )

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
                "notes_quality": "coherence_low"
                if float(at.get("regime_coherence", 1.0)) < _safe_param(params, "regime_coherence_min_for_causality", 0.55)
                else "ok",
            }
        )

    for _, row in panel.iterrows():
        if row["phase_market"] == "phase2" and float(row.get("h_negative_obs", 0.0)) < 100 and float(row.get("capture_ratio_pv_vs_ttl", 1.0)) > 0.9:
            checks.append(
                {
                    "status": "WARN",
                    "code": "Q1_INCOHERENT_BASCULE",
                    "message": f"{row['country']} {int(row['year'])}: bascule incoherente avec symptomes marche.",
                }
            )

    checks.extend(build_common_checks(panel))
    if not checks:
        checks.append({"status": "PASS", "code": "Q1_PASS", "message": "Q1 checks pass."})

    summary = pd.DataFrame(summary_rows)
    kpis = {
        "n_countries": int(summary["country"].nunique()) if not summary.empty else 0,
        "n_bascule_market": int(summary["bascule_year_market"].notna().sum()) if not summary.empty else 0,
        "n_bascule_physical": int(summary["bascule_year_physical"].notna().sum()) if not summary.empty else 0,
    }

    narrative = (
        "Q1 identifie la bascule Phase 1 -> Phase 2 via deux diagnostics independants: "
        "symptomes de marche (score) et stress physique (SR/FAR/IR). "
        "La bascule est retenue seulement sur donnees de qualite non FAIL."
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
        mode=str(selection.get("mode", "HIST")).upper(),
        scenario_id=selection.get("scenario_id"),
        horizon_year=selection.get("horizon_year"),
    )
