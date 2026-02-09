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
    COL_NRL_THRESHOLD,
    COL_PRICE_DA,
    COL_PSH_PUMP,
    COL_Q_ANY_CRITICAL_MISSING,
    COL_Q_BAD_LOAD_NET,
    COL_Q_MISSING_GENERATION,
    COL_Q_MISSING_LOAD,
    COL_Q_MISSING_NET_POSITION,
    COL_Q_MISSING_PRICE,
    COL_Q_MISSING_PSH_PUMP,
    COL_REGIME,
    COL_SINK_NON_BESS_ALIAS,
    COL_SURPLUS,
    COL_SURPLUS_ABSORBED,
    COL_SURPLUS_UNABS,
    COL_TIMESTAMP_UTC,
    COL_YEAR,
)


MUST_RUN_COMPONENT_MAP = {
    "nuclear": COL_GEN_NUCLEAR,
    "hydro_ror": COL_GEN_HYDRO_ROR,
    "hydro_res": COL_GEN_HYDRO_RES,
    "biomass": COL_GEN_BIOMASS,
    "coal": COL_GEN_COAL,
    "lignite": COL_GEN_LIGNITE,
    "gas": COL_GEN_GAS,
    "other": COL_GEN_OTHER,
}



def _safe_series(df: pd.DataFrame, col: str, default: float = 0.0) -> pd.Series:
    if col not in df.columns:
        return pd.Series(default, index=df.index, dtype=float)
    return pd.to_numeric(df[col], errors="coerce")


def _compute_must_run(df: pd.DataFrame, country_cfg: dict[str, Any]) -> tuple[pd.Series, pd.Series, str]:
    must_cfg = country_cfg.get("must_run", {})
    mode = str(must_cfg.get("mode", "observed"))

    obs = pd.Series(0.0, index=df.index)
    for comp in must_cfg.get("observed_components", []):
        col = MUST_RUN_COMPONENT_MAP.get(str(comp))
        if col:
            obs = obs.add(_safe_series(df, col, default=0.0).fillna(0.0), fill_value=0.0)

    if mode == "observed":
        return obs, obs, mode

    floor_gw = float(must_cfg.get("floor_gw", 0.0))
    floor_mw = floor_gw * 1000.0
    modulation = float(must_cfg.get("modulation_pct", 1.0))
    modulation = min(max(modulation, 0.0), 1.0)
    floor_based = np.maximum(floor_mw, obs.values * modulation)
    used = np.minimum(obs.values, floor_based)
    return obs, pd.Series(used, index=df.index), "floor"


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

    # essential numeric columns
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
    ]:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # clipping rules
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
    ]:
        s = df[col]
        s = s.where(~(s < -0.1), np.nan)
        s = s.where(~((s >= -0.1) & (s < 0)), 0.0)
        df[col] = s

    df[COL_GEN_VRE] = _safe_series(df, COL_GEN_SOLAR, 0).fillna(0) + _safe_series(df, COL_GEN_WIND_ON, 0).fillna(0) + _safe_series(df, COL_GEN_WIND_OFF, 0).fillna(0)

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

    mr_obs, mr_used, mr_mode = _compute_must_run(df, country_cfg)
    df[COL_GEN_MUST_RUN_OBS] = mr_obs
    df[COL_GEN_MUST_RUN] = mr_used

    df[COL_EXPORTS] = _safe_series(df, COL_NET_POSITION, np.nan).clip(lower=0.0)

    # load_net treatment with psh
    psh_missing_share = float(df[COL_PSH_PUMP].isna().mean())
    if psh_missing_share <= 0.05:
        df[COL_LOAD_NET_MODE] = "minus_psh_pump"
        df[COL_LOAD_NET] = _safe_series(df, COL_LOAD_TOTAL) - _safe_series(df, COL_PSH_PUMP, 0).fillna(0)
        df[COL_Q_BAD_LOAD_NET] = df[COL_LOAD_NET] < 0
        df.loc[df[COL_Q_BAD_LOAD_NET], COL_LOAD_NET] = np.nan
        df[COL_FLEX_PSH] = _safe_series(df, COL_PSH_PUMP, 0).clip(lower=0.0)
        df[COL_Q_MISSING_PSH_PUMP] = False
    else:
        df[COL_LOAD_NET_MODE] = "includes_pumping"
        df[COL_LOAD_NET] = _safe_series(df, COL_LOAD_TOTAL)
        df[COL_Q_BAD_LOAD_NET] = False
        df[COL_FLEX_PSH] = 0.0
        df[COL_Q_MISSING_PSH_PUMP] = True

    df[COL_NRL] = df[COL_LOAD_NET] - df[COL_GEN_VRE] - df[COL_GEN_MUST_RUN]
    df[COL_SURPLUS] = (-df[COL_NRL]).clip(lower=0.0)
    df[COL_NRL_POS] = df[COL_NRL].clip(lower=0.0)

    df[COL_FLEX_EXPORTS] = _safe_series(df, COL_EXPORTS, 0).fillna(0)
    df[COL_BESS_CHARGE] = 0.0
    df[COL_BESS_DISCHARGE] = 0.0
    df[COL_BESS_SOC] = 0.0
    df[COL_FLEX_OBS] = df[COL_FLEX_EXPORTS] + df[COL_FLEX_PSH]
    df[COL_FLEX_EFFECTIVE] = df[COL_FLEX_OBS] + df[COL_BESS_CHARGE]

    df[COL_SURPLUS_ABSORBED] = np.minimum(df[COL_SURPLUS].fillna(0), df[COL_FLEX_EFFECTIVE].fillna(0))
    df[COL_SURPLUS_UNABS] = (df[COL_SURPLUS] - df[COL_SURPLUS_ABSORBED]).clip(lower=0.0)

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

    # quality flags
    df[COL_Q_MISSING_PRICE] = df[COL_PRICE_DA].isna()
    df[COL_Q_MISSING_LOAD] = df[COL_LOAD_TOTAL].isna()
    df[COL_Q_MISSING_GENERATION] = df[[COL_GEN_VRE, COL_GEN_MUST_RUN_OBS]].isna().all(axis=1)
    df[COL_Q_MISSING_NET_POSITION] = df[COL_NET_POSITION].isna()
    df[COL_Q_ANY_CRITICAL_MISSING] = df[[COL_Q_MISSING_PRICE, COL_Q_MISSING_LOAD, COL_Q_MISSING_GENERATION]].any(axis=1)

    df[COL_MUST_RUN_MODE] = mr_mode
    df[COL_ENTSOE_CODE_USED] = entsoe_code_used

    # index and aliases
    df = df.copy()
    df.index.name = COL_TIMESTAMP_UTC
    df[COL_TIMESTAMP_UTC] = df.index

    for canonical, alias in CANONICAL_ALIAS_COLUMNS.items():
        if canonical in df.columns:
            df[alias] = df[canonical]

    return df

