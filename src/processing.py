"""Hourly physical table builder (SPEC V1)."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.constants import (
    CANONICAL_ALIAS_COLUMNS,
    COL_BESS_CHARGE,
    COL_BESS_DISCHARGE,
    COL_BESS_SOC,
    COL_COUNTRY,
    COL_ENTSOE_CODE_USED,
    COL_EXPORTS,
    COL_FLEX_EFFECTIVE,
    COL_FLEX_EXPORTS,
    COL_FLEX_OBS,
    COL_FLEX_PSH,
    COL_GEN_BIOMASS,
    COL_GEN_COAL,
    COL_GEN_GAS,
    COL_GEN_HYDRO_PSH_GEN,
    COL_GEN_HYDRO_RES,
    COL_GEN_HYDRO_ROR,
    COL_GEN_LIGNITE,
    COL_GEN_MUST_RUN,
    COL_GEN_MUST_RUN_OBS,
    COL_GEN_NUCLEAR,
    COL_GEN_OTHER,
    COL_GEN_OIL,
    COL_GEN_PRIMARY,
    COL_GEN_SOLAR,
    COL_GEN_TOTAL,
    COL_GEN_VRE,
    COL_GEN_WIND_OFF,
    COL_GEN_WIND_ON,
    COL_LOAD_NET,
    COL_LOAD_NET_MODE,
    COL_LOAD_TOTAL,
    COL_MUST_RUN_MODE,
    COL_NET_POSITION,
    COL_NRL,
    COL_NRL_POS,
    COL_LOW_RESIDUAL_HOUR,
    COL_LOW_RESIDUAL_THRESHOLD,
    COL_NRL_THRESHOLD,
    COL_PRICE_DA,
    COL_PSH_PUMP,
    COL_PSH_PUMP_COVERAGE,
    COL_PSH_PUMP_STATUS,
    COL_Q_ANY_CRITICAL_MISSING,
    COL_Q_BAD_LOAD_NET,
    COL_Q_MISSING_GENERATION,
    COL_Q_MISSING_LOAD,
    COL_Q_MISSING_NET_POSITION,
    COL_Q_MISSING_PRICE,
    COL_Q_MISSING_PSH_PUMP,
    COL_REGIME,
    COL_SURPLUS,
    COL_SURPLUS_ABSORBED,
    COL_SURPLUS_UNABS,
    COL_TIMESTAMP_UTC,
    COL_YEAR,
)
from src.core.definitions import DEFAULT_MUST_RUN_CANDIDATES, compute_core_hourly_definitions


def _safe_series(df: pd.DataFrame, col: str, default: float = 0.0) -> pd.Series:
    if col not in df.columns:
        return pd.Series(default, index=df.index, dtype=float)
    return pd.to_numeric(df[col], errors="coerce")


def _must_run_candidates(country_cfg: dict[str, Any]) -> list[str]:
    must_cfg = country_cfg.get("must_run", {})
    from_cfg = must_cfg.get("candidate_components")
    if isinstance(from_cfg, list) and from_cfg:
        return [str(x) for x in from_cfg]
    return list(DEFAULT_MUST_RUN_CANDIDATES)


def _classify_regime(nrl: pd.Series, surplus: pd.Series, surplus_unabs: pd.Series, min_pos_hours: int = 200, q: float = 0.90) -> tuple[pd.Series, float]:
    regime = pd.Series("C", index=nrl.index, dtype=object)
    regime.loc[surplus > 0.0] = "B"
    regime.loc[surplus_unabs > 0.0] = "A"

    pos_nrl = nrl[(nrl > 0) & np.isfinite(nrl)]
    if len(pos_nrl) < min_pos_hours:
        threshold = np.nan
    else:
        threshold = float(pos_nrl.quantile(q))
        regime.loc[(surplus == 0.0) & (nrl >= threshold)] = "D"

    return regime, threshold


def build_hourly_table(
    raw_panel: pd.DataFrame,
    country: str,
    year: int,
    country_cfg: dict[str, Any],
    thresholds_cfg: dict[str, Any],
    entsoe_code_used: str,
) -> pd.DataFrame:
    df = raw_panel.copy()

    # identifiers
    df[COL_COUNTRY] = country
    df[COL_YEAR] = int(year)

    # Essential numeric columns.
    for col in [
        COL_PRICE_DA,
        COL_LOAD_TOTAL,
        COL_NET_POSITION,
        COL_GEN_SOLAR,
        COL_GEN_WIND_ON,
        COL_GEN_WIND_OFF,
        COL_GEN_NUCLEAR,
        COL_GEN_HYDRO_ROR,
        COL_GEN_HYDRO_RES,
        COL_GEN_HYDRO_PSH_GEN,
        COL_GEN_BIOMASS,
        COL_GEN_GAS,
        COL_GEN_COAL,
        COL_GEN_LIGNITE,
        COL_GEN_OIL,
        COL_GEN_OTHER,
        COL_PSH_PUMP,
        COL_BESS_CHARGE,
        COL_BESS_DISCHARGE,
        COL_BESS_SOC,
        "must_run_profile_override_mw",
        "must_run_scale_scenario",
    ]:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Clipping rules.
    for col in [
        COL_GEN_SOLAR,
        COL_GEN_WIND_ON,
        COL_GEN_WIND_OFF,
        COL_GEN_NUCLEAR,
        COL_GEN_HYDRO_ROR,
        COL_GEN_HYDRO_RES,
        COL_GEN_HYDRO_PSH_GEN,
        COL_GEN_BIOMASS,
        COL_GEN_GAS,
        COL_GEN_COAL,
        COL_GEN_LIGNITE,
        COL_GEN_OIL,
        COL_GEN_OTHER,
        COL_PSH_PUMP,
        COL_BESS_CHARGE,
        COL_BESS_DISCHARGE,
    ]:
        s = df[col]
        s = s.where(~(s < -0.1), np.nan)
        s = s.where(~((s >= -0.1) & (s < 0)), 0.0)
        df[col] = s

    df[COL_GEN_VRE] = (
        _safe_series(df, COL_GEN_SOLAR, 0).fillna(0)
        + _safe_series(df, COL_GEN_WIND_ON, 0).fillna(0)
        + _safe_series(df, COL_GEN_WIND_OFF, 0).fillna(0)
    )

    df[COL_GEN_TOTAL] = df[
        [
            COL_GEN_SOLAR,
            COL_GEN_WIND_ON,
            COL_GEN_WIND_OFF,
            COL_GEN_NUCLEAR,
            COL_GEN_HYDRO_ROR,
            COL_GEN_HYDRO_RES,
            COL_GEN_HYDRO_PSH_GEN,
            COL_GEN_BIOMASS,
            COL_GEN_GAS,
            COL_GEN_COAL,
            COL_GEN_LIGNITE,
            COL_GEN_OIL,
            COL_GEN_OTHER,
        ]
    ].sum(axis=1, min_count=1)

    df[COL_GEN_PRIMARY] = df[COL_GEN_TOTAL] - _safe_series(df, COL_GEN_HYDRO_PSH_GEN, 0).fillna(0)

    df[COL_EXPORTS] = _safe_series(df, COL_NET_POSITION, np.nan).clip(lower=0.0)

    # Canonical load / must-run / NRL / surplus / flex definitions.
    fallback_profile = _safe_series(df, "must_run_profile_override_mw", np.nan)
    fallback_scale = float(pd.to_numeric(df.get("must_run_scale_scenario"), errors="coerce").dropna().iloc[0]) if "must_run_scale_scenario" in df.columns and pd.to_numeric(df.get("must_run_scale_scenario"), errors="coerce").notna().any() else 1.0
    floor_q = float(country_cfg.get("must_run", {}).get("floor_quantile", 0.10))
    core = compute_core_hourly_definitions(
        df=df,
        prefer_net_of_psh_pump=True,
        psh_missing_share_threshold=0.05,
        must_run_floor_quantile=floor_q,
        must_run_candidates=_must_run_candidates(country_cfg),
        fallback_must_run_profile_mw=fallback_profile if fallback_profile.notna().any() else None,
        fallback_must_run_scale=fallback_scale,
    )
    df[COL_LOAD_NET] = core[COL_LOAD_NET]
    df[COL_LOAD_NET_MODE] = core[COL_LOAD_NET_MODE]
    df[COL_PSH_PUMP] = core[COL_PSH_PUMP]
    df[COL_PSH_PUMP_COVERAGE] = core.get(COL_PSH_PUMP_COVERAGE, np.nan)
    df[COL_PSH_PUMP_STATUS] = core.get(COL_PSH_PUMP_STATUS, "missing")
    df[COL_GEN_MUST_RUN_OBS] = core["must_run_observed_mw"]
    df[COL_GEN_MUST_RUN] = core["must_run_mw"]
    df[COL_MUST_RUN_MODE] = core["must_run_mode"]
    df[COL_NRL] = core[COL_NRL]
    df[COL_SURPLUS] = core[COL_SURPLUS]
    df[COL_NRL_POS] = df[COL_NRL].clip(lower=0.0)
    df[COL_FLEX_EXPORTS] = _safe_series(df, COL_EXPORTS, 0.0).fillna(0.0).clip(lower=0.0)
    df[COL_FLEX_PSH] = core[COL_FLEX_PSH]
    df[COL_FLEX_OBS] = core[COL_FLEX_OBS]
    df[COL_FLEX_EFFECTIVE] = core[COL_FLEX_EFFECTIVE]
    df[COL_SURPLUS_ABSORBED] = core[COL_SURPLUS_ABSORBED]
    df[COL_SURPLUS_UNABS] = core[COL_SURPLUS_UNABS]
    df[COL_BESS_CHARGE] = _safe_series(df, COL_BESS_CHARGE, 0.0).fillna(0.0).clip(lower=0.0)
    df[COL_BESS_DISCHARGE] = _safe_series(df, COL_BESS_DISCHARGE, 0.0).fillna(0.0).clip(lower=0.0)
    df[COL_BESS_SOC] = _safe_series(df, COL_BESS_SOC, 0.0).fillna(0.0).clip(lower=0.0)
    df[COL_Q_BAD_LOAD_NET] = df[COL_LOAD_NET] < 0
    df.loc[df[COL_Q_BAD_LOAD_NET], COL_LOAD_NET] = np.nan
    df[COL_Q_MISSING_PSH_PUMP] = df[COL_PSH_PUMP_STATUS].astype(str).str.lower().isin(["missing", "partial"])

    model_cfg = thresholds_cfg.get("model", {})
    regime, threshold = _classify_regime(
        df[COL_NRL],
        df[COL_SURPLUS],
        df[COL_SURPLUS_UNABS],
        min_pos_hours=int(model_cfg.get("regime_d_min_positive_hours", 200)),
        q=float(model_cfg.get("regime_d_positive_nrl_quantile", 0.90)),
    )
    df[COL_REGIME] = regime
    df[COL_NRL_THRESHOLD] = threshold

    # "Quasi-surplus" diagnostic signal (without changing A/B/C/D labels).
    nrl = pd.to_numeric(df[COL_NRL], errors="coerce")
    nrl_pos = nrl.clip(lower=0.0)
    if nrl_pos.notna().any():
        low_residual_threshold = float(nrl_pos.quantile(0.10))
    else:
        low_residual_threshold = float("nan")
    df[COL_LOW_RESIDUAL_THRESHOLD] = low_residual_threshold
    if np.isfinite(low_residual_threshold):
        df[COL_LOW_RESIDUAL_HOUR] = (nrl >= 0.0) & (nrl <= low_residual_threshold)
    else:
        df[COL_LOW_RESIDUAL_HOUR] = False

    # Quality flags.
    df[COL_Q_MISSING_PRICE] = df[COL_PRICE_DA].isna()
    df[COL_Q_MISSING_LOAD] = df[COL_LOAD_TOTAL].isna()
    df[COL_Q_MISSING_GENERATION] = df[[COL_GEN_TOTAL, COL_GEN_VRE]].isna().all(axis=1)
    df[COL_Q_MISSING_NET_POSITION] = df[COL_NET_POSITION].isna()
    df[COL_Q_ANY_CRITICAL_MISSING] = df[[COL_Q_MISSING_PRICE, COL_Q_MISSING_LOAD, COL_Q_MISSING_GENERATION]].any(axis=1)

    df[COL_ENTSOE_CODE_USED] = entsoe_code_used

    # Index and aliases.
    df = df.copy()
    df.index.name = COL_TIMESTAMP_UTC
    df[COL_TIMESTAMP_UTC] = df.index

    for canonical, alias in CANONICAL_ALIAS_COLUMNS.items():
        if canonical in df.columns:
            df[alias] = df[canonical]

    return df

