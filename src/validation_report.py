"""Validation report generation (hard tests + reality checks)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from src.constants import (
    COL_BESS_DISCHARGE,
    COL_GEN_HYDRO_PSH_GEN,
    COL_GEN_MUST_RUN,
    COL_GEN_SOLAR,
    COL_GEN_TOTAL,
    COL_LOAD_NET,
    COL_LOW_RESIDUAL_HOUR,
    COL_NRL,
    COL_PSH_PUMP,
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


def _safe_float(v: Any, default: float = np.nan) -> float:
    try:
        out = float(v)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


def _possible_causes_neg_price_mismatch(df: pd.DataFrame, neg_mask: pd.Series) -> list[str]:
    causes: list[tuple[float, str]] = []
    if "gen_must_run_mw" in df.columns:
        mr_missing_share = float(pd.to_numeric(df["gen_must_run_mw"], errors="coerce").isna().mean())
        if mr_missing_share > 0.01:
            causes.append((mr_missing_share, "donnees must_run manquantes"))
    if "psh_pumping_data_status" in df.columns:
        psh_status = str(df["psh_pumping_data_status"].dropna().iloc[0]).lower() if df["psh_pumping_data_status"].notna().any() else "missing"
        if psh_status in {"missing", "partial"}:
            causes.append((0.8 if psh_status == "missing" else 0.5, "donnees pompage STEP partielles/manquantes"))
    if COL_PSH_PUMP in df.columns and COL_LOAD_NET in df.columns and "load_total_mw" in df.columns:
        load_total = pd.to_numeric(df["load_total_mw"], errors="coerce").fillna(0.0)
        load_net = pd.to_numeric(df[COL_LOAD_NET], errors="coerce").fillna(0.0)
        psh = pd.to_numeric(df[COL_PSH_PUMP], errors="coerce").fillna(0.0)
        lhs = float(load_total.sum())
        rhs = float((load_net + psh).sum())
        rel_gap = abs(lhs - rhs) / max(abs(lhs), 1e-9)
        if rel_gap > 0.001:
            causes.append((min(1.0, rel_gap * 10.0), "possible double comptage/mauvais netting du pompage STEP"))
    if neg_mask.any():
        reg = df[COL_REGIME].astype(str) if COL_REGIME in df.columns else pd.Series("", index=df.index)
        neg_ab_share = float(((neg_mask) & reg.isin(["A", "B"])).sum()) / float(neg_mask.sum())
        if neg_ab_share < 0.30:
            causes.append((0.35 - neg_ab_share, "mapping prix/regimes possiblement incoherent"))
    causes = sorted(causes, key=lambda x: x[0], reverse=True)
    top = [c for _, c in causes[:3]]
    if not top:
        top = ["causes non conclusives (verifier mapping prix et donnees physiques)"]
    return top


def _corr(a: pd.Series, b: pd.Series) -> float:
    x = pd.to_numeric(a, errors="coerce")
    y = pd.to_numeric(b, errors="coerce")
    tmp = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(tmp) < 12:
        return float("nan")
    return _safe_float(tmp["x"].corr(tmp["y"]), np.nan)


def _must_run_monthly_zero(df: pd.DataFrame) -> bool:
    mr = pd.to_numeric(df.get(COL_GEN_MUST_RUN), errors="coerce")
    if mr.notna().sum() == 0:
        return False
    if isinstance(df.index, pd.DatetimeIndex):
        idx = df.index
        if idx.tz is None:
            idx = idx.tz_localize("UTC")
        month_key = idx.tz_convert("UTC").to_period("M")
        by_month = mr.groupby(month_key).sum(min_count=1)
        return bool((pd.to_numeric(by_month, errors="coerce").fillna(0.0).abs() <= 1e-6).all())
    # Fallback when index is not datetime: treat as one bucket.
    return bool(abs(float(mr.fillna(0.0).sum())) <= 1e-6)



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
    surplus_total = float(pd.to_numeric(df.get(COL_SURPLUS), errors="coerce").fillna(0.0).clip(lower=0.0).sum())
    unabs_total = float(pd.to_numeric(df.get(COL_SURPLUS_UNABS), errors="coerce").fillna(0.0).clip(lower=0.0).sum())
    if surplus_total <= 1e-9:
        if np.isfinite(far) and abs(float(far) - 1.0) > 1e-6:
            findings.append(
                _finding(
                    "ERROR",
                    "INV_FAR_WHEN_ZERO_SURPLUS",
                    "FAR must equal 1 when annual surplus is zero",
                    f"far={far}, surplus_total={surplus_total}",
                    "Set FAR=1 if surplus energy is zero.",
                )
            )
        if unabs_total > 1e-6:
            findings.append(
                _finding(
                    "ERROR",
                    "INV_UNABS_WHEN_ZERO_SURPLUS",
                    "Unabsorbed surplus must be zero when surplus is zero",
                    f"surplus_unabsorbed_total={unabs_total}",
                    "Recompute absorbed/unabsorbed identities.",
                )
            )

    sr = annual_metrics.get("sr_energy")
    if np.isfinite(sr) and not (0.0 <= float(sr) <= 1.0):
        findings.append(_finding("ERROR", "INV_SR_RANGE", "SR outside [0,1]", f"sr={sr}", "Verify denominator and surplus energy."))

    mr = pd.to_numeric(df.get("gen_must_run_mw"), errors="coerce")
    total_gen = pd.to_numeric(df.get(COL_GEN_TOTAL), errors="coerce")
    if mr.notna().any() and total_gen.notna().any():
        n_mr_gt_gen = int((mr - total_gen > 1e-6).sum())
        if n_mr_gt_gen > 0:
            findings.append(
                _finding(
                    "ERROR",
                    "INV_MR_GT_GEN",
                    "Must-run exceeds total generation on some hours",
                    f"n_bad={n_mr_gt_gen}",
                    "Review must-run floor and generation mapping.",
                )
            )

    # Reality checks
    neg_total = int((df[COL_PRICE_DA] < 0).sum())
    if neg_total > 0:
        neg_mask = df[COL_PRICE_DA] < 0
        regime = df[COL_REGIME].astype(str) if COL_REGIME in df.columns else pd.Series("", index=df.index)
        low_residual = (
            pd.to_numeric(df.get(COL_LOW_RESIDUAL_HOUR), errors="coerce").fillna(0.0) > 0
            if COL_LOW_RESIDUAL_HOUR in df.columns
            else pd.Series(False, index=df.index)
        )
        nrl = pd.to_numeric(df.get(COL_NRL), errors="coerce")
        neg_in_ab = int((neg_mask & regime.isin(["A", "B"])).sum())
        neg_in_ab_or_low = int((neg_mask & (regime.isin(["A", "B"]) | low_residual)).sum())
        ratio_ab = neg_in_ab / neg_total
        ratio_ab_or_low = neg_in_ab_or_low / neg_total

        if ratio_ab < 0.50:
            findings.append(
                _finding(
                    "INFO",
                    "RC_NEG_NOT_IN_AB",
                    "Negative prices are not mostly in regimes A/B (legacy strict check).",
                    f"ratio_ab={ratio_ab:.3f}, neg_total={neg_total}",
                    "Use AB_OR_LOW_RESIDUAL principal check for interpretation.",
                )
            )

        if ratio_ab_or_low < 0.70:
            neg_nrl = nrl[neg_mask]
            nrl_p10 = _safe_float(neg_nrl.quantile(0.10), np.nan) if neg_nrl.notna().any() else np.nan
            nrl_p50 = _safe_float(neg_nrl.quantile(0.50), np.nan) if neg_nrl.notna().any() else np.nan
            nrl_p90 = _safe_float(neg_nrl.quantile(0.90), np.nan) if neg_nrl.notna().any() else np.nan
            causes = _possible_causes_neg_price_mismatch(df, neg_mask)
            findings.append(
                _finding(
                    "WARN",
                    "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
                    "Negative prices are not mostly explained by (A/B) or low residual load.",
                    (
                        f"ratio_ab_or_low_residual={ratio_ab_or_low:.3f}, ratio_ab={ratio_ab:.3f}, neg_total={neg_total}, "
                        f"nrl_neg_p10={nrl_p10:.1f}, nrl_neg_p50={nrl_p50:.1f}, nrl_neg_p90={nrl_p90:.1f}, causes={'; '.join(causes)}"
                    ),
                    "Review must-run completeness, PSH netting and price-zone mapping.",
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

    # Must-run sanity checks
    must_run = pd.to_numeric(df.get(COL_GEN_MUST_RUN), errors="coerce")
    total_gen_num = pd.to_numeric(df.get(COL_GEN_TOTAL), errors="coerce")
    if must_run.notna().sum() > 0 and total_gen_num.notna().sum() > 0:
        must_run_twh = float(must_run.fillna(0.0).clip(lower=0.0).sum()) / 1e6
        total_gen_twh = float(total_gen_num.fillna(0.0).clip(lower=0.0).sum()) / 1e6
        mr_share = must_run_twh / total_gen_twh if total_gen_twh > 0 else np.nan
        if np.isfinite(mr_share) and not (0.05 <= mr_share <= 0.60):
            findings.append(
                _finding(
                    "WARN",
                    "RC_MR_SHARE_IMPLAUSIBLE",
                    "Must-run share outside plausible range [5%, 60%].",
                    f"must_run_share={mr_share:.3f}, must_run_twh={must_run_twh:.3f}, total_gen_twh={total_gen_twh:.3f}",
                    "Review must-run perimeter and component mapping.",
                )
            )
    if _must_run_monthly_zero(df):
        findings.append(
            _finding(
                "WARN",
                "RC_MR_ALL_ZERO_MONTHS",
                "Must-run is zero on all monthly buckets.",
                "must_run_monthly_sum=0",
                "Verify must-run construction and source mapping.",
            )
        )
    if must_run.notna().sum() > 0:
        corr_psh_gen = _corr(must_run, pd.to_numeric(df.get(COL_GEN_HYDRO_PSH_GEN), errors="coerce"))
        corr_bess_dis = _corr(must_run, pd.to_numeric(df.get(COL_BESS_DISCHARGE), errors="coerce"))
        if (np.isfinite(corr_psh_gen) and corr_psh_gen > 0.85) or (np.isfinite(corr_bess_dis) and corr_bess_dis > 0.85):
            findings.append(
                _finding(
                    "WARN",
                    "RC_MR_FLEX_OVERLAP",
                    "Must-run may include flexible assets (PSH turbine / BESS discharge overlap).",
                    f"corr_mr_psh_gen={corr_psh_gen:.3f}, corr_mr_bess_discharge={corr_bess_dis:.3f}",
                    "Exclude flexible assets from must-run perimeter.",
                )
            )

    load_neg_share = float((df[COL_LOAD_NET] < 0).mean())
    if load_neg_share > 0.001:
        findings.append(_finding("ERROR", "RC_LOAD_NET_NEG", "load_net is negative too often", f"share={load_neg_share:.4f}", "Fix PSH pump handling and load_net mode."))

    if not findings:
        findings.append(_finding("PASS", "ALL_CHECKS_PASS", "No blocking issue detected", "hard checks and reality checks passed", "Proceed to interpretation."))

    return [f.to_dict() for f in findings]

