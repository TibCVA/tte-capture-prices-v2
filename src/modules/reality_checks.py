"""Common reality checks shared across Q1..Q5 modules."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.constants import (
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
    h_regime_c = row.get("h_regime_c", np.nan)
    h_regime_d = row.get("h_regime_d", np.nan)

    if _finite(sr) and not (0.0 <= float(sr) <= 1.0):
        checks.append({"status": "FAIL", "code": "RC_SR_RANGE", "message": f"{label}: SR hors [0,1]."})
    if _finite(far) and not (0.0 <= float(far) <= 1.0):
        checks.append({"status": "FAIL", "code": "RC_FAR_RANGE", "message": f"{label}: FAR hors [0,1]."})
    if _finite(surplus_twh) and float(surplus_twh) == 0.0 and _finite(far):
        checks.append({"status": "FAIL", "code": "RC_FAR_NAN_WHEN_NO_SURPLUS", "message": f"{label}: FAR doit etre NaN quand surplus=0."})
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
                        f"{label}: IR > 1 (must-run tres eleve en creux). "
                        f"p10_must_run_mw={float(p10_must_run):.2f}, p10_load_mw={float(p10_load):.2f}."
                    ),
                }
            )
        else:
            checks.append({"status": "WARN", "code": "RC_IR_GT_1", "message": f"{label}: IR > 1 (must-run tres eleve en creux)."})
    if _finite(regime_coherence) and float(regime_coherence) < 0.55:
        checks.append({"status": "WARN", "code": "RC_LOW_REGIME_COHERENCE", "message": f"{label}: regime_coherence < 0.55."})
    if _finite(h_regime_c) and _finite(h_regime_d) and (_finite(ttl)) and (float(h_regime_c) + float(h_regime_d) < 500):
        checks.append({"status": "WARN", "code": "RC_TTL_LOW_SAMPLE", "message": f"{label}: TTL calcule sur trop peu d'heures C+D (<500)."})

    return checks


def _check_hourly(hourly_df: pd.DataFrame, label: str = "") -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    if hourly_df.empty:
        return checks

    name = label or "hourly"
    p = pd.to_numeric(hourly_df.get(COL_PRICE_DA), errors="coerce")
    r = hourly_df.get(COL_REGIME).astype(str) if COL_REGIME in hourly_df.columns else pd.Series(index=hourly_df.index, dtype=object)

    neg_total = int((p < 0).sum())
    if neg_total > 0:
        neg_ab = int(((p < 0) & r.isin(["A", "B"])).sum())
        ratio = neg_ab / neg_total
        if ratio < 0.50:
            checks.append({"status": "WARN", "code": "RC_NEG_NOT_IN_AB", "message": f"{name}: seulement {ratio:.1%} des heures negatives en regime A/B."})

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
