"""Q5 - Thermal anchor sensitivity to gas and CO2."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.constants import THERMAL_DEFAULTS
from src.modules.common import assumptions_subset
from src.modules.result import ModuleResult

Q5_PARAMS = [
    "ccgt_efficiency",
    "ccgt_ef_t_per_mwh_th",
    "ccgt_vom_eur_mwh",
    "coal_efficiency",
    "coal_ef_t_per_mwh_th",
    "coal_vom_eur_mwh",
]


def load_commodity_daily(path: str = "data/external/commodity_prices_daily.csv") -> pd.DataFrame | None:
    p = Path(path)
    if not p.exists():
        return None
    df = pd.read_csv(p)
    required = {"date", "gas_price_eur_mwh_th", "co2_price_eur_t"}
    if not required.issubset(df.columns):
        return None
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    return df


def _tech_params(assumptions_df: pd.DataFrame, marginal_tech: str) -> tuple[float, float, float]:
    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q5_PARAMS)].iterrows()
    }
    tech = marginal_tech.upper()
    if tech == "CCGT":
        eff = float(params.get("ccgt_efficiency", THERMAL_DEFAULTS["CCGT"]["efficiency"]))
        ef = float(params.get("ccgt_ef_t_per_mwh_th", THERMAL_DEFAULTS["CCGT"]["emission_factor_t_per_mwh_th"]))
        vom = float(params.get("ccgt_vom_eur_mwh", THERMAL_DEFAULTS["CCGT"]["vom_eur_mwh"]))
    else:
        eff = float(params.get("coal_efficiency", THERMAL_DEFAULTS["COAL"]["efficiency"]))
        ef = float(params.get("coal_ef_t_per_mwh_th", THERMAL_DEFAULTS["COAL"]["emission_factor_t_per_mwh_th"]))
        vom = float(params.get("coal_vom_eur_mwh", THERMAL_DEFAULTS["COAL"]["vom_eur_mwh"]))
    return eff, ef, vom


def _co2_required(
    ttl_target: float,
    alpha: float,
    base_q95_without_co2: float,
    dco2: float,
) -> float:
    if not (np.isfinite(ttl_target) and np.isfinite(alpha) and np.isfinite(base_q95_without_co2) and dco2 > 0):
        return np.nan
    return (ttl_target - alpha - base_q95_without_co2) / dco2


def _co2_required_non_negative(value: float) -> float:
    if not np.isfinite(value):
        return np.nan
    return max(0.0, float(value))


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


def _ttl_regression_estimate(cd: pd.DataFrame, tca_q95: float) -> float:
    if cd is None or cd.empty or not np.isfinite(tca_q95):
        return np.nan
    x = pd.to_numeric(cd.get("tca_eur_mwh"), errors="coerce").to_numpy(dtype=float)
    y = pd.to_numeric(cd.get("price_da_eur_mwh"), errors="coerce").to_numpy(dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    if int(mask.sum()) < 5:
        return np.nan
    x = x[mask]
    y = y[mask]
    if float(np.nanstd(x)) <= 1e-9:
        return np.nan
    slope, intercept = np.polyfit(x, y, deg=1)
    return float(intercept + slope * tca_q95)


def run_q5(
    hourly_df: pd.DataFrame,
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
    commodity_daily: pd.DataFrame | None = None,
    ttl_target_eur_mwh: float | None = None,
    gas_override_eur_mwh_th: float | None = None,
    co2_override_eur_t: float | None = None,
    ttl_method: str | None = None,
    ttl_physical_margin_eur_mwh: float | None = None,
) -> ModuleResult:
    country = str(selection.get("country", ""))
    marginal_tech = str(selection.get("marginal_tech", "CCGT")).upper()
    eff, ef, vom = _tech_params(assumptions_df, marginal_tech)
    method = str(ttl_method or selection.get("ttl_method", "physical")).strip().lower()
    if method not in {"physical", "regression"}:
        method = "physical"
    margin = _safe_float(
        ttl_physical_margin_eur_mwh if ttl_physical_margin_eur_mwh is not None else selection.get("ttl_physical_margin_eur_mwh", 0.0),
        0.0,
    )

    if commodity_daily is None:
        commodity_daily = load_commodity_daily()

    if commodity_daily is None or commodity_daily.empty:
        checks = [{"status": "WARN", "code": "Q5_MISSING_COMMODITIES", "message": "Serie commodites absente: Q5 desactive."}]
        empty = pd.DataFrame(
            [
                {
                    "country": country,
                    "year_range_used": "",
                    "marginal_tech": marginal_tech,
                    "ttl_obs": np.nan,
                    "ttl_obs_price_cd": np.nan,
                    "ttl_physical": np.nan,
                    "ttl_regression": np.nan,
                    "ttl_method": method,
                    "tca_q95": np.nan,
                    "alpha": np.nan,
                    "alpha_effective": np.nan,
                    "corr_cd": np.nan,
                    "anchor_confidence": np.nan,
                    "dTCA_dCO2": ef / eff if eff > 0 else np.nan,
                    "dTCA_dGas": 1 / eff if eff > 0 else np.nan,
                    "ttl_target": ttl_target_eur_mwh,
                    "co2_required_base": np.nan,
                    "co2_required_gas_override": np.nan,
                    "co2_required_base_non_negative": np.nan,
                    "co2_required_gas_override_non_negative": np.nan,
                    "warnings_quality": "missing_commodities",
                }
            ]
        )
        return ModuleResult(
            module_id="Q5",
            run_id=run_id,
            selection=selection,
            assumptions_used=assumptions_subset(assumptions_df, Q5_PARAMS),
            kpis={},
            tables={"Q5_summary": empty},
            figures=[],
            narrative_md="Q5 ne peut pas s'executer sans series journaliere gaz/CO2.",
            checks=checks,
            warnings=["Missing commodity daily series."],
            mode=str(selection.get("mode", "HIST")).upper(),
            scenario_id=selection.get("scenario_id"),
            horizon_year=selection.get("horizon_year"),
        )

    c = commodity_daily.copy()
    c["date"] = pd.to_datetime(c["date"]).dt.tz_localize(None)
    h = hourly_df.copy()
    if not isinstance(h.index, pd.DatetimeIndex):
        if "timestamp_utc" in h.columns:
            h["timestamp_utc"] = pd.to_datetime(h["timestamp_utc"], errors="coerce", utc=True)
            h = h.dropna(subset=["timestamp_utc"]).set_index("timestamp_utc")
        else:
            raise ValueError("hourly_df must contain timestamp index or timestamp_utc.")
    if h.index.tz is None:
        h.index = h.index.tz_localize("UTC")

    h["date"] = h.index.tz_convert("UTC").tz_localize(None).floor("D")
    h = h.merge(c[["date", "gas_price_eur_mwh_th", "co2_price_eur_t"]], on="date", how="left")

    if gas_override_eur_mwh_th is not None:
        h["gas_price_eur_mwh_th"] = float(gas_override_eur_mwh_th)
    if co2_override_eur_t is not None:
        h["co2_price_eur_t"] = float(co2_override_eur_t)

    h["gas_price_eur_mwh_th"] = pd.to_numeric(h["gas_price_eur_mwh_th"], errors="coerce")
    h["co2_price_eur_t"] = pd.to_numeric(h["co2_price_eur_t"], errors="coerce")
    h["price_da_eur_mwh"] = pd.to_numeric(h["price_da_eur_mwh"], errors="coerce")
    h["tca_eur_mwh"] = h["gas_price_eur_mwh_th"] / eff + h["co2_price_eur_t"] * (ef / eff) + vom

    regime_col = "regime" if "regime" in h.columns else ("regime_phys" if "regime_phys" in h.columns else None)
    if regime_col is None:
        h["_regime_tmp"] = "C"
        regime_col = "_regime_tmp"
    cd = h[h[regime_col].isin(["C", "D"]) & h["price_da_eur_mwh"].notna() & h["tca_eur_mwh"].notna()].copy()
    ttl_obs_price_cd = float(cd["price_da_eur_mwh"].quantile(0.95)) if not cd.empty else np.nan
    tca_q95 = float(cd["tca_eur_mwh"].quantile(0.95)) if not cd.empty else np.nan
    ttl_physical = tca_q95 + margin if np.isfinite(tca_q95) else np.nan
    ttl_regression = _ttl_regression_estimate(cd, tca_q95)
    if method == "physical":
        ttl_effective = ttl_physical
        alpha_effective = margin if np.isfinite(margin) else np.nan
    else:
        ttl_effective = ttl_regression if np.isfinite(ttl_regression) else ttl_obs_price_cd
        alpha_effective = ttl_effective - tca_q95 if np.isfinite(ttl_effective) and np.isfinite(tca_q95) else np.nan
    alpha = ttl_obs_price_cd - tca_q95 if np.isfinite(ttl_obs_price_cd) and np.isfinite(tca_q95) else np.nan
    corr_cd = float(cd["price_da_eur_mwh"].corr(cd["tca_eur_mwh"])) if len(cd) >= 3 else np.nan

    dgas = 1.0 / eff if eff > 0 else np.nan
    dco2 = ef / eff if eff > 0 else np.nan

    target = float(ttl_effective) if ttl_target_eur_mwh is None else float(ttl_target_eur_mwh)
    base_q95_without_co2 = float((cd["gas_price_eur_mwh_th"] / eff + vom).quantile(0.95)) if not cd.empty else np.nan
    co2_required_base = _co2_required(target, alpha_effective, base_q95_without_co2, dco2)

    co2_required_gas_override = np.nan
    if gas_override_eur_mwh_th is not None and not cd.empty:
        base_override = float((pd.Series(float(gas_override_eur_mwh_th), index=cd.index) / eff + vom).quantile(0.95))
        co2_required_gas_override = _co2_required(target, alpha_effective, base_override, dco2)
    co2_required_base_non_negative = _co2_required_non_negative(co2_required_base)
    co2_required_gas_override_non_negative = _co2_required_non_negative(co2_required_gas_override)

    checks: list[dict[str, str]] = []
    warnings: list[str] = []
    if not (np.isfinite(dco2) and dco2 > 0):
        checks.append({"status": "FAIL", "code": "Q5_DCO2_SIGN", "message": "dTCA/dCO2 doit etre strictement positif."})
    if not (np.isfinite(dgas) and dgas > 0):
        checks.append({"status": "FAIL", "code": "Q5_DGAS_SIGN", "message": "dTCA/dGas doit etre strictement positif."})
    if np.isfinite(corr_cd) and corr_cd < 0.2:
        checks.append({"status": "WARN", "code": "Q5_LOW_CORR_CD", "message": "Relation prix-ancre faible sur regimes C/D (corr<0.2)."})
    if np.isfinite(alpha) and alpha < 0.0:
        msg = "Alpha negatif: ancre thermique potentiellement fragile sans contexte."
        checks.append({"status": "WARN", "code": "Q5_ALPHA_NEG", "message": msg})
        warnings.append(msg)
    if method == "regression" and not np.isfinite(ttl_regression):
        checks.append({"status": "WARN", "code": "Q5_REGRESSION_UNSTABLE", "message": "Regression TTL instable; fallback TTL observe applique."})
        warnings.append("Regression TTL instable; fallback observe applique.")
    if np.isfinite(co2_required_base) and co2_required_base < 0:
        checks.append(
            {
                "status": "INFO",
                "code": "Q5_CO2_TARGET_ALREADY_BELOW_BASELINE",
                "message": "CO2 requis brut negatif: cible TTL deja atteinte sans CO2 additionnel.",
            }
        )
    anchor_confidence = 1.0
    if np.isfinite(alpha) and alpha < 0.0:
        anchor_confidence -= 0.2
    if np.isfinite(corr_cd) and corr_cd < 0.2:
        anchor_confidence -= 0.2
    if method == "regression" and not np.isfinite(ttl_regression):
        anchor_confidence -= 0.2
    anchor_confidence = float(np.clip(anchor_confidence, 0.0, 1.0))
    if not checks:
        checks.append({"status": "PASS", "code": "Q5_PASS", "message": "Q5 checks passes."})

    summary = pd.DataFrame(
        [
            {
                "country": country,
                "year_range_used": f"{int(h['year'].min())}-{int(h['year'].max())}" if "year" in h.columns and h["year"].notna().any() else "",
                "marginal_tech": marginal_tech,
                "ttl_obs": ttl_effective,
                "ttl_obs_price_cd": ttl_obs_price_cd,
                "ttl_physical": ttl_physical,
                "ttl_regression": ttl_regression,
                "ttl_method": method,
                "tca_q95": tca_q95,
                "alpha": alpha,
                "alpha_effective": alpha_effective,
                "corr_cd": corr_cd,
                "anchor_confidence": anchor_confidence,
                "dTCA_dCO2": dco2,
                "dTCA_dGas": dgas,
                "ttl_target": target,
                "co2_required_base": co2_required_base,
                "co2_required_gas_override": co2_required_gas_override,
                "co2_required_base_non_negative": co2_required_base_non_negative,
                "co2_required_gas_override_non_negative": co2_required_gas_override_non_negative,
                "warnings_quality": "",
            }
        ]
    )

    narrative = (
        "Q5 calcule une ancre thermique (TCA) sur heures hors surplus (C/D), "
        "mesure son alignement au TTL observe, et derive un ordre de grandeur de CO2 requis pour une cible TTL."
    )

    return ModuleResult(
        module_id="Q5",
        run_id=run_id,
        selection=selection,
        assumptions_used=assumptions_subset(assumptions_df, Q5_PARAMS),
        kpis={
            "ttl_obs": ttl_effective,
            "ttl_method": method,
            "corr_cd": corr_cd,
            "anchor_confidence": anchor_confidence,
            "dTCA_dCO2": dco2,
            "dTCA_dGas": dgas,
        },
        tables={"Q5_summary": summary},
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
        mode=str(selection.get("mode", "HIST")).upper(),
        scenario_id=selection.get("scenario_id"),
        horizon_year=selection.get("horizon_year"),
    )
