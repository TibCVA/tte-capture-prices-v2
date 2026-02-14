"""Common reality checks shared across Q1..Q5 modules."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.constants import (
    COL_LOW_RESIDUAL_HOUR,
    COL_NRL,
    COL_PRICE_DA,
    COL_REGIME,
)


def _finite(v: Any) -> bool:
    try:
        return bool(np.isfinite(float(v)))
    except Exception:
        return False


def _check_row(row: pd.Series, prefix: str = "") -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    label = prefix or f"{row.get('country', '?')}-{row.get('year', '?')}"

    sr = row.get("sr_energy", np.nan)
    far = row.get("far_energy", np.nan)
    ir = row.get("ir_p10", np.nan)
    p10_must_run = row.get("p10_must_run_mw", np.nan)
    p10_load = row.get("p10_load_mw", np.nan)
    ttl = row.get("ttl_eur_mwh", np.nan)
    baseload = row.get("baseload_price_eur_mwh", np.nan)
    capture_pv = row.get("capture_price_pv_eur_mwh", row.get("capture_rate_pv_eur_mwh", np.nan))
    regime_coherence = row.get("regime_coherence", np.nan)
    surplus_twh = row.get("surplus_twh", np.nan)
    scope_cov = row.get("must_run_scope_coverage", np.nan)
    h_regime_c = row.get("h_regime_c", np.nan)
    h_regime_d = row.get("h_regime_d", np.nan)
    share_neg_ab = row.get("share_neg_price_hours_in_AB", np.nan)
    share_neg_ab_or_low = row.get("share_neg_price_hours_in_AB_OR_LOW_RESIDUAL", np.nan)
    h_negative = row.get("h_negative_obs", row.get("h_negative", np.nan))
    h_below_5 = row.get("h_below_5_obs", row.get("h_below_5", np.nan))
    load_total_twh = row.get("load_total_twh", np.nan)
    load_net_twh = row.get("load_net_twh", np.nan)
    psh_twh = row.get("psh_pumping_twh", np.nan)
    surplus_unabs_energy = row.get(
        "surplus_unabs_energy_after",
        row.get("surplus_unabsorbed_twh_after", row.get("surplus_unabsorbed_twh", np.nan)),
    )
    must_run_twh = row.get("gen_must_run_twh", np.nan)
    gen_total_twh = row.get("gen_primary_twh", row.get("gen_total_twh", np.nan))
    n_hours = row.get("n_hours", row.get("n_hours_expected", np.nan))
    coverage_price = row.get("coverage_price", np.nan)
    coverage_load_total = row.get("coverage_load_total", np.nan)
    missing_price = row.get("missing_share_price", np.nan)
    missing_load = row.get("missing_share_load", np.nan)
    partial_year_supported = bool(row.get("partial_year_supported", False))

    if (not _finite(coverage_price)) and _finite(missing_price):
        coverage_price = 1.0 - float(missing_price)
    if (not _finite(coverage_load_total)) and _finite(missing_load):
        coverage_load_total = 1.0 - float(missing_load)

    if _finite(n_hours):
        n_h = int(round(float(n_hours)))
        if not (8759 <= n_h <= 8784):
            checks.append(
                {
                    "status": "WARN" if partial_year_supported else "FAIL",
                    "code": "TEST_DATA_001",
                    "message": f"{label}: n_hours={n_h} (attendu dans [8759,8784]).",
                }
            )
        else:
            checks.append(
                {
                    "status": "PASS",
                    "code": "TEST_DATA_001",
                    "message": f"{label}: n_hours={n_h} coherent.",
                }
            )
        if _finite(h_negative) and float(h_negative) > float(n_h) + 1e-9:
            checks.append(
                {
                    "status": "FAIL",
                    "code": "RC_HNEG_GT_NHOURS",
                    "message": f"{label}: h_negative ({float(h_negative):.1f}) > n_hours ({n_h}).",
                }
            )
        if _finite(h_below_5) and float(h_below_5) > float(n_h) + 1e-9:
            checks.append(
                {
                    "status": "FAIL",
                    "code": "RC_HB5_GT_NHOURS",
                    "message": f"{label}: h_below_5 ({float(h_below_5):.1f}) > n_hours ({n_h}).",
                }
            )
    else:
        checks.append({"status": "WARN", "code": "TEST_DATA_001", "message": f"{label}: n_hours indisponible."})
    if _finite(h_negative) and float(h_negative) < -1e-9:
        checks.append({"status": "FAIL", "code": "RC_HNEG_NEGATIVE", "message": f"{label}: h_negative negatif."})
    if _finite(h_below_5) and float(h_below_5) < -1e-9:
        checks.append({"status": "FAIL", "code": "RC_HB5_NEGATIVE", "message": f"{label}: h_below_5 negatif."})
    if _finite(h_negative) and _finite(h_below_5) and float(h_below_5) + 1e-9 < float(h_negative):
        checks.append(
            {
                "status": "FAIL",
                "code": "RC_HB5_LT_HNEG",
                "message": f"{label}: h_below_5 ({float(h_below_5):.1f}) < h_negative ({float(h_negative):.1f}).",
            }
        )

    if _finite(coverage_price) and _finite(coverage_load_total):
        cov_p = float(coverage_price)
        cov_l = float(coverage_load_total)
        if cov_p >= 0.99 and cov_l >= 0.99:
            checks.append(
                {
                    "status": "PASS",
                    "code": "TEST_DATA_002",
                    "message": f"{label}: coverage price/load ok ({cov_p:.2%}/{cov_l:.2%}).",
                }
            )
        elif cov_p >= 0.95 and cov_l >= 0.95:
            checks.append(
                {
                    "status": "WARN",
                    "code": "TEST_DATA_002",
                    "message": f"{label}: coverage price/load limite ({cov_p:.2%}/{cov_l:.2%}).",
                }
            )
        else:
            checks.append(
                {
                    "status": "FAIL",
                    "code": "TEST_DATA_002",
                    "message": f"{label}: coverage price/load insuffisante ({cov_p:.2%}/{cov_l:.2%}).",
                }
            )
    else:
        checks.append({"status": "WARN", "code": "TEST_DATA_002", "message": f"{label}: coverage price/load indisponible."})

    price_candidates = {
        "price_eur_mwh": row.get("price_eur_mwh", np.nan),
        "baseload_price_eur_mwh": row.get("baseload_price_eur_mwh", np.nan),
        "offpeak_price_eur_mwh": row.get("offpeak_price_eur_mwh", np.nan),
        "peakload_price_eur_mwh": row.get("peakload_price_eur_mwh", np.nan),
        "ttl_eur_mwh": row.get("ttl_eur_mwh", np.nan),
    }
    outliers = []
    for name, value in price_candidates.items():
        if not _finite(value):
            continue
        val = float(value)
        if val < -500.0 or val > 5000.0:
            outliers.append((name, val))
    if outliers:
        details = "; ".join([f"{name}={val:.2f}" for name, val in outliers[:3]])
        checks.append(
            {
                "status": "WARN",
                "code": "TEST_DATA_003",
                "message": f"{label}: {len(outliers)} prix hors plage [-500,5000] ({details}).",
            }
        )
    else:
        checks.append({"status": "PASS", "code": "TEST_DATA_003", "message": f"{label}: prix dans plage large attendue."})

    if _finite(sr) and not (0.0 <= float(sr) <= 1.0):
        checks.append({"status": "FAIL", "code": "RC_SR_RANGE", "message": f"{label}: SR hors [0,1]."})
    if _finite(far) and not (0.0 <= float(far) <= 1.0):
        checks.append({"status": "FAIL", "code": "RC_FAR_RANGE", "message": f"{label}: FAR hors [0,1]."})
    if _finite(surplus_twh) and float(surplus_twh) == 0.0 and _finite(far) and abs(float(far) - 1.0) > 1e-6:
        checks.append({"status": "FAIL", "code": "RC_FAR_ONE_WHEN_NO_SURPLUS", "message": f"{label}: FAR doit valoir 1 quand surplus=0."})
    if _finite(ir) and float(ir) < 0.0:
        checks.append({"status": "FAIL", "code": "RC_IR_NEGATIVE", "message": f"{label}: IR negatif."})
    if _finite(capture_pv) and not (-200.0 <= float(capture_pv) <= 500.0):
        checks.append({"status": "WARN", "code": "RC_CAPTURE_RANGE", "message": f"{label}: capture price PV hors plage attendue."})
    if _finite(ttl) and _finite(baseload) and float(ttl) < float(baseload) - 20.0:
        checks.append({"status": "WARN", "code": "RC_TTL_LOW", "message": f"{label}: TTL notablement sous baseload."})
    if _finite(ir) and float(ir) > 1.0:
        if _finite(p10_must_run) and _finite(p10_load):
            checks.append(
                {
                    "status": "WARN",
                    "code": "RC_IR_GT_1",
                    "message": (
                        f"{label}: IR > 1 (ratio hors borne). "
                        f"p10_must_run_mw={float(p10_must_run):.2f}, p10_load_mw={float(p10_load):.2f}."
                    ),
                }
            )
        else:
            checks.append({"status": "WARN", "code": "RC_IR_GT_1", "message": f"{label}: IR > 1 (ratio hors borne)."})
    if _finite(regime_coherence) and float(regime_coherence) < 0.55:
        checks.append({"status": "WARN", "code": "RC_LOW_REGIME_COHERENCE", "message": f"{label}: regime_coherence < 0.55."})
    if _finite(h_regime_c) and _finite(h_regime_d) and (_finite(ttl)) and (float(h_regime_c) + float(h_regime_d) < 500):
        checks.append({"status": "WARN", "code": "RC_TTL_LOW_SAMPLE", "message": f"{label}: TTL calcule sur trop peu d'heures C+D (<500)."})
    if _finite(scope_cov) and not (0.0 <= float(scope_cov) <= 1.0):
        checks.append({"status": "FAIL", "code": "RC_SCOPE_COVERAGE_RANGE", "message": f"{label}: must_run_scope_coverage hors [0,1]."})
    if _finite(share_neg_ab) and float(share_neg_ab) < 0.50:
        checks.append(
            {
                "status": "INFO",
                "code": "RC_NEG_NOT_IN_AB",
                "message": f"{label}: seulement {float(share_neg_ab):.1%} des heures negatives en A/B (check legacy).",
            }
        )
    if _finite(share_neg_ab_or_low) and float(share_neg_ab_or_low) < 0.70:
        checks.append(
            {
                "status": "WARN",
                "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
                "message": f"{label}: seulement {float(share_neg_ab_or_low):.1%} des heures negatives expliquees par A/B ou low residual.",
            }
        )
    if _finite(load_total_twh) and _finite(load_net_twh) and _finite(psh_twh):
        lhs = float(load_total_twh)
        rhs = float(load_net_twh) + float(psh_twh)
        rel_err = abs(lhs - rhs) / max(abs(lhs), 1e-9)
        if rel_err > 0.001:
            checks.append(
                {
                    "status": "FAIL",
                    "code": "RC_LOAD_PSH_ENERGY_IDENTITY",
                    "message": f"{label}: load_total_twh != load_net_twh + psh_pumping_twh (rel_err={rel_err:.2%}).",
                }
            )
    if _finite(psh_twh) and float(psh_twh) < -1e-9:
        checks.append(
            {
                "status": "FAIL",
                "code": "RC_PSH_PUMPING_TWH_NEGATIVE",
                "message": f"{label}: psh_pumping_twh doit etre >= 0.",
            }
        )
    if _finite(load_net_twh) and float(load_net_twh) < -1e-9:
        checks.append(
            {
                "status": "FAIL",
                "code": "RC_LOAD_NET_TWH_NEGATIVE",
                "message": f"{label}: load_net_twh doit etre >= 0.",
            }
        )
    if _finite(surplus_unabs_energy) and float(surplus_unabs_energy) < -1e-9:
        checks.append(
            {
                "status": "FAIL",
                "code": "RC_SURPLUS_UNABS_NEGATIVE",
                "message": f"{label}: surplus_unabs_energy doit etre >= 0.",
            }
        )
    for col in row.index:
        col_name = str(col)
        if not col_name.lower().endswith("_non_negative"):
            continue
        val = row.get(col, np.nan)
        if _finite(val) and float(val) < -1e-9:
            checks.append(
                {
                    "status": "FAIL",
                    "code": "RC_NON_NEGATIVE_FIELD_NEGATIVE",
                    "message": f"{label}: {col_name} doit etre >= 0.",
                }
            )
    if _finite(must_run_twh) and _finite(gen_total_twh) and float(gen_total_twh) > 0.0:
        share = float(must_run_twh) / float(gen_total_twh)
        if not (0.05 <= share <= 0.60):
            checks.append(
                {
                    "status": "WARN",
                    "code": "RC_MR_SHARE_IMPLAUSIBLE",
                    "message": f"{label}: must_run_share={share:.1%} hors plage plausible [5%,60%].",
                }
            )

    return checks


def _check_hourly(hourly_df: pd.DataFrame, label: str = "") -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    if hourly_df.empty:
        return checks

    name = label or "hourly"
    if {"load_total_mw", "load_mw", "psh_pumping_mw"}.issubset(set(hourly_df.columns)):
        load_total = pd.to_numeric(hourly_df["load_total_mw"], errors="coerce")
        load_net = pd.to_numeric(hourly_df["load_mw"], errors="coerce")
        psh = pd.to_numeric(hourly_df["psh_pumping_mw"], errors="coerce")
        mask = load_total.notna() & load_net.notna() & psh.notna()
        if bool(mask.any()):
            resid = (load_total[mask] - (load_net[mask] + psh[mask])).abs()
            max_abs = float(resid.max()) if not resid.empty else 0.0
            if max_abs > 1e-6:
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "RC_LOAD_PSH_HOURLY_IDENTITY",
                        "message": f"{name}: load_total_mw != load_mw + psh_pumping_mw (max_abs={max_abs:.6f}).",
                    }
                )
    if "psh_pumping_mw" in hourly_df.columns:
        psh = pd.to_numeric(hourly_df["psh_pumping_mw"], errors="coerce")
        if bool((psh < -1e-9).fillna(False).any()):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "RC_PSH_PUMPING_MW_NEGATIVE",
                    "message": f"{name}: psh_pumping_mw doit etre >= 0.",
                }
            )
    load_col = "load_mw" if "load_mw" in hourly_df.columns else ("load_net_mw" if "load_net_mw" in hourly_df.columns else None)
    if load_col is not None:
        load_vals = pd.to_numeric(hourly_df[load_col], errors="coerce")
        if bool((load_vals < -1e-9).fillna(False).any()):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "RC_LOAD_MW_NEGATIVE",
                    "message": f"{name}: {load_col} doit etre >= 0.",
                }
            )
    p = pd.to_numeric(hourly_df.get(COL_PRICE_DA), errors="coerce")
    r = hourly_df.get(COL_REGIME).astype(str) if COL_REGIME in hourly_df.columns else pd.Series(index=hourly_df.index, dtype=object)

    neg_total = int((p < 0).sum())
    if neg_total > 0:
        neg_mask = p < 0
        low_residual = (
            pd.to_numeric(hourly_df.get(COL_LOW_RESIDUAL_HOUR), errors="coerce").fillna(0.0) > 0
            if COL_LOW_RESIDUAL_HOUR in hourly_df.columns
            else pd.Series(False, index=hourly_df.index)
        )
        neg_ab = int((neg_mask & r.isin(["A", "B"])).sum())
        neg_ab_or_low = int((neg_mask & (r.isin(["A", "B"]) | low_residual)).sum())
        ratio_ab = neg_ab / neg_total
        ratio_ab_or_low = neg_ab_or_low / neg_total
        if ratio_ab < 0.50:
            checks.append({"status": "INFO", "code": "RC_NEG_NOT_IN_AB", "message": f"{name}: {ratio_ab:.1%} des heures negatives en regime A/B (check legacy)."})
        if ratio_ab_or_low < 0.70:
            nrl = pd.to_numeric(hourly_df.get(COL_NRL), errors="coerce")
            neg_nrl = nrl[neg_mask]
            p10 = float(neg_nrl.quantile(0.10)) if neg_nrl.notna().any() else float("nan")
            p50 = float(neg_nrl.quantile(0.50)) if neg_nrl.notna().any() else float("nan")
            p90 = float(neg_nrl.quantile(0.90)) if neg_nrl.notna().any() else float("nan")
            causes: list[str] = []
            mr = pd.to_numeric(hourly_df.get("gen_must_run_mw"), errors="coerce")
            if mr.notna().mean() < 0.95:
                causes.append("must_run_missing")
            if "psh_pumping_data_status" in hourly_df.columns:
                status = str(hourly_df["psh_pumping_data_status"].dropna().iloc[0]).lower() if hourly_df["psh_pumping_data_status"].notna().any() else "missing"
                if status in {"missing", "partial"}:
                    causes.append("psh_data_incomplete")
            if not causes:
                causes.append("price_or_regime_mapping")
            checks.append(
                {
                    "status": "WARN",
                    "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
                    "message": (
                        f"{name}: {ratio_ab_or_low:.1%} des heures negatives expliquees par A/B ou low residual "
                        f"(nrl_neg_p10={p10:.1f}, p50={p50:.1f}, p90={p90:.1f}; causes={','.join(causes[:3])})."
                    ),
                }
            )

    med_c = float(p[r == "C"].median()) if (r == "C").any() else np.nan
    med_d = float(p[r == "D"].median()) if (r == "D").any() else np.nan
    if np.isfinite(med_c) and np.isfinite(med_d) and med_d <= med_c:
        checks.append({"status": "WARN", "code": "RC_D_NOT_ABOVE_C", "message": f"{name}: median(price|D) <= median(price|C)."})

    return checks


def build_common_checks(
    annual_df: pd.DataFrame,
    hourly_by_key: dict[tuple[str, int], pd.DataFrame] | None = None,
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    if annual_df is None or annual_df.empty:
        return [{"status": "WARN", "code": "RC_NO_DATA", "message": "Aucune donnee annuelle pour checks communs."}]

    for _, row in annual_df.iterrows():
        checks.extend(_check_row(row))
        if hourly_by_key is not None:
            key = (str(row.get("country")), int(row.get("year")))
            if key in hourly_by_key:
                checks.extend(_check_hourly(hourly_by_key[key], label=f"{key[0]}-{key[1]}"))

    if not checks:
        return [{"status": "PASS", "code": "RC_COMMON_PASS", "message": "Checks communs RC-1..RC-4 OK."}]
    return checks
