"""Validation report generation (hard tests + reality checks)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from src.constants import (
    COL_GEN_SOLAR,
    COL_LOAD_NET,
    COL_NRL,
    COL_PRICE_DA,
    COL_REGIME,
    COL_SURPLUS,
    COL_SURPLUS_ABSORBED,
    COL_SURPLUS_UNABS,
)


@dataclass
class ValidationFinding:
    severity: str
    code: str
    message: str
    evidence: str
    suggestion: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "evidence": self.evidence,
            "suggestion": self.suggestion,
        }



def _finding(severity: str, code: str, message: str, evidence: str, suggestion: str) -> ValidationFinding:
    return ValidationFinding(severity=severity, code=code, message=message, evidence=evidence, suggestion=suggestion)



def build_validation_report(df: pd.DataFrame, annual_metrics: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[ValidationFinding] = []

    # Hard invariants
    nrl_expected = df[COL_LOAD_NET] - df["gen_vre_mw"] - df["gen_must_run_mw"]
    n_bad_nrl = int((nrl_expected - df[COL_NRL]).abs().fillna(0).gt(1e-6).sum())
    if n_bad_nrl > 0:
        findings.append(_finding("ERROR", "INV_NRL", "NRL identity mismatch", f"n_bad={n_bad_nrl}", "Recompute NRL formula."))

    surplus_expected = (-df[COL_NRL]).clip(lower=0.0)
    n_bad_surplus = int((surplus_expected - df[COL_SURPLUS]).abs().fillna(0).gt(1e-6).sum())
    if n_bad_surplus > 0:
        findings.append(_finding("ERROR", "INV_SURPLUS", "Surplus identity mismatch", f"n_bad={n_bad_surplus}", "Recompute surplus formula."))

    n_bad_unabs_negative = int((df[COL_SURPLUS_UNABS] < -1e-9).sum())
    if n_bad_unabs_negative > 0:
        findings.append(_finding("ERROR", "INV_UNABS_NEG", "Negative unabsorbed surplus", f"n_bad={n_bad_unabs_negative}", "Clamp and inspect flex calculations."))

    n_bad_unabs_gt = int((df[COL_SURPLUS_UNABS] - df[COL_SURPLUS]).gt(1e-6).sum())
    if n_bad_unabs_gt > 0:
        findings.append(_finding("ERROR", "INV_UNABS_GT_SURPLUS", "Unabsorbed surplus above total surplus", f"n_bad={n_bad_unabs_gt}", "Fix absorption calculation."))

    far = annual_metrics.get("far_energy")
    if np.isfinite(far) and not (0.0 <= float(far) <= 1.0):
        findings.append(_finding("ERROR", "INV_FAR_RANGE", "FAR outside [0,1]", f"far={far}", "Verify absorbed/surplus energy totals."))

    sr = annual_metrics.get("sr_energy")
    if np.isfinite(sr) and not (0.0 <= float(sr) <= 1.0):
        findings.append(_finding("ERROR", "INV_SR_RANGE", "SR outside [0,1]", f"sr={sr}", "Verify denominator and surplus energy."))

    # Reality checks
    neg_total = int((df[COL_PRICE_DA] < 0).sum())
    if neg_total > 0:
        neg_in_ab = int(((df[COL_PRICE_DA] < 0) & df[COL_REGIME].isin(["A", "B"])) .sum())
        ratio = neg_in_ab / neg_total
        if ratio < 0.50:
            findings.append(
                _finding(
                    "WARN",
                    "RC_NEG_NOT_IN_SURPLUS",
                    "Negative prices are not mostly in surplus regimes A/B",
                    f"ratio={ratio:.3f}, neg_total={neg_total}",
                    "Review must-run perimeter, PSH handling, and price-zone mapping.",
                )
            )

    med_c = float(df.loc[df[COL_REGIME] == "C", COL_PRICE_DA].median()) if (df[COL_REGIME] == "C").any() else np.nan
    med_d = float(df.loc[df[COL_REGIME] == "D", COL_PRICE_DA].median()) if (df[COL_REGIME] == "D").any() else np.nan
    if np.isfinite(med_c) and np.isfinite(med_d) and med_d <= med_c:
        findings.append(_finding("WARN", "RC_D_NOT_HIGHER_THAN_C", "Median price in D is not above C", f"med_c={med_c:.2f}, med_d={med_d:.2f}", "Check D-threshold and stress regime definition."))

    night = df.index.tz_convert("Europe/Paris")
    mask_night = (night.hour >= 0) & (night.hour <= 4)
    pv_night = float(df.loc[mask_night, COL_GEN_SOLAR].median())
    pv_p95 = float(df[COL_GEN_SOLAR].quantile(0.95)) if df[COL_GEN_SOLAR].notna().any() else np.nan
    if np.isfinite(pv_night) and np.isfinite(pv_p95) and pv_p95 > 0 and pv_night > 0.02 * pv_p95:
        findings.append(_finding("WARN", "RC_PV_NIGHT", "Night PV appears abnormally high", f"median_night={pv_night:.2f}, p95={pv_p95:.2f}", "Check timezone conversion and PSR mapping."))

    cap_ratio = annual_metrics.get("capture_ratio_pv")
    if np.isfinite(cap_ratio) and (cap_ratio < 0.2 or cap_ratio > 1.5):
        findings.append(_finding("WARN", "RC_CAPTURE_RATIO_PV", "PV capture ratio atypical", f"capture_ratio_pv={cap_ratio:.3f}", "Inspect prices, PV profile and anchors."))

    load_neg_share = float((df[COL_LOAD_NET] < 0).mean())
    if load_neg_share > 0.001:
        findings.append(_finding("ERROR", "RC_LOAD_NET_NEG", "load_net is negative too often", f"share={load_neg_share:.4f}", "Fix PSH pump handling and load_net mode."))

    if not findings:
        findings.append(_finding("PASS", "ALL_CHECKS_PASS", "No blocking issue detected", "hard checks and reality checks passed", "Proceed to interpretation."))

    return [f.to_dict() for f in findings]

