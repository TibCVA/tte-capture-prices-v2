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
    if not {"date", "gas_price_eur_mwh_th", "co2_price_eur_t"}.issubset(df.columns):
        return None
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    return df


def run_q5(
    hourly_df: pd.DataFrame,
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
    commodity_daily: pd.DataFrame | None = None,
    ttl_target_eur_mwh: float | None = None,
    gas_override_eur_mwh_th: float | None = None,
) -> ModuleResult:
    country = selection.get("country", "")
    marginal_tech = str(selection.get("marginal_tech", "CCGT")).upper()

    params = {
        r["param_name"]: float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q5_PARAMS)].iterrows()
    }

    if marginal_tech == "CCGT":
        eff = float(params.get("ccgt_efficiency", THERMAL_DEFAULTS["CCGT"]["efficiency"]))
        ef = float(params.get("ccgt_ef_t_per_mwh_th", THERMAL_DEFAULTS["CCGT"]["emission_factor_t_per_mwh_th"]))
        vom = float(params.get("ccgt_vom_eur_mwh", THERMAL_DEFAULTS["CCGT"]["vom_eur_mwh"]))
    else:
        eff = float(params.get("coal_efficiency", THERMAL_DEFAULTS["COAL"]["efficiency"]))
        ef = float(params.get("coal_ef_t_per_mwh_th", THERMAL_DEFAULTS["COAL"]["emission_factor_t_per_mwh_th"]))
        vom = float(params.get("coal_vom_eur_mwh", THERMAL_DEFAULTS["COAL"]["vom_eur_mwh"]))

    if commodity_daily is None:
        commodity_daily = load_commodity_daily()

    if commodity_daily is None or commodity_daily.empty:
        checks = [{"status": "WARN", "message": "Commodity series missing: Q5 disabled"}]
        empty = pd.DataFrame(
            [
                {
                    "country": country,
                    "year_range_used": "",
                    "marginal_tech": marginal_tech,
                    "ttl_obs": np.nan,
                    "tca_q95": np.nan,
                    "alpha": np.nan,
                    "corr_cd": np.nan,
                    "dTCA_dCO2": ef / eff,
                    "dTCA_dGas": 1 / eff,
                    "ttl_target": ttl_target_eur_mwh,
                    "co2_required_base": np.nan,
                    "co2_required_gas_override": np.nan,
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
            narrative_md="Q5 cannot run without gas/CO2 series.",
            checks=checks,
            warnings=["Missing commodity daily series"],
        )

    c = commodity_daily.copy()
    c["date"] = pd.to_datetime(c["date"]).dt.tz_localize(None)

    h = hourly_df.copy()
    h["date"] = h.index.tz_convert("UTC").tz_localize(None).floor("D")
    h = h.merge(c[["date", "gas_price_eur_mwh_th", "co2_price_eur_t"]], on="date", how="left")

    if gas_override_eur_mwh_th is not None:
        h["gas_price_eur_mwh_th"] = float(gas_override_eur_mwh_th)

    h["tca_eur_mwh"] = h["gas_price_eur_mwh_th"] / eff + h["co2_price_eur_t"] * (ef / eff) + vom

    cd = h[h["regime"].isin(["C", "D"]) & h["price_da_eur_mwh"].notna() & h["tca_eur_mwh"].notna()]
    ttl_obs = float(cd["price_da_eur_mwh"].quantile(0.95)) if not cd.empty else np.nan
    tca_q95 = float(cd["tca_eur_mwh"].quantile(0.95)) if not cd.empty else np.nan
    alpha = ttl_obs - tca_q95 if np.isfinite(ttl_obs) and np.isfinite(tca_q95) else np.nan
    corr_cd = float(cd["price_da_eur_mwh"].corr(cd["tca_eur_mwh"])) if len(cd) >= 3 else np.nan

    dgas = 1 / eff
    dco2 = ef / eff

    if ttl_target_eur_mwh is None:
        ttl_target_eur_mwh = ttl_obs

    base_q95_without_co2 = float((cd["gas_price_eur_mwh_th"] / eff + vom).quantile(0.95)) if not cd.empty else np.nan
    if np.isfinite(alpha) and np.isfinite(base_q95_without_co2) and dco2 > 0:
        co2_required = (float(ttl_target_eur_mwh) - alpha - base_q95_without_co2) / dco2
    else:
        co2_required = np.nan

    checks = []
    if np.isfinite(corr_cd) and corr_cd < 0.2:
        checks.append({"status": "WARN", "message": "Weak price-anchor relation on C/D regimes"})
    if np.isfinite(alpha) and alpha < -20:
        checks.append({"status": "WARN", "message": "Large negative alpha; marginal tech may be wrong"})
    if not checks:
        checks.append({"status": "PASS", "message": "Q5 checks pass"})

    summary = pd.DataFrame(
        [
            {
                "country": country,
                "year_range_used": f"{int(h['year'].min())}-{int(h['year'].max())}",
                "marginal_tech": marginal_tech,
                "ttl_obs": ttl_obs,
                "tca_q95": tca_q95,
                "alpha": alpha,
                "corr_cd": corr_cd,
                "dTCA_dCO2": dco2,
                "dTCA_dGas": dgas,
                "ttl_target": ttl_target_eur_mwh,
                "co2_required_base": co2_required,
                "co2_required_gas_override": co2_required if gas_override_eur_mwh_th is not None else np.nan,
                "warnings_quality": "",
            }
        ]
    )

    narrative = "Q5 links thermal anchor (TCA) to observed upper-tail prices (TTL) and estimates required CO2 for a target TTL."

    return ModuleResult(
        module_id="Q5",
        run_id=run_id,
        selection=selection,
        assumptions_used=assumptions_subset(assumptions_df, Q5_PARAMS),
        kpis={"ttl_obs": ttl_obs, "corr_cd": corr_cd},
        tables={"Q5_summary": summary},
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=[],
    )
