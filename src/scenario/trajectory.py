"""Helpers to build explicit annual phase2 trajectories."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

KEY_COLS = ["scenario_id", "country", "year"]

BOUNDED_01_COLS = {
    "must_run_min_output_factor",
    "export_coincidence_factor",
    "bess_eta_roundtrip",
    "supported_vre_share",
    "price_exposure_share",
    "marginal_efficiency",
}

NON_NEGATIVE_COLS = {
    "demand_total_twh",
    "demand_peak_gw",
    "cap_pv_gw",
    "cap_wind_on_gw",
    "cap_wind_off_gw",
    "cap_must_run_nuclear_gw",
    "cap_must_run_chp_gw",
    "cap_must_run_biomass_gw",
    "cap_must_run_hydro_ror_gw",
    "must_run_min_output_factor",
    "interconnection_export_gw",
    "export_coincidence_factor",
    "psh_pump_gw",
    "bess_power_gw",
    "bess_energy_gwh",
    "bess_eta_roundtrip",
    "co2_eur_per_t",
    "gas_eur_per_mwh_th",
    "marginal_efficiency",
    "marginal_emission_factor_t_per_mwh",
    "supported_vre_share",
    "negative_price_rule_threshold_hours",
    "price_exposure_share",
}

INTEGER_COLS = {"negative_price_rule_threshold_hours"}

CATEGORICAL_FROZEN_2030 = {
    "demand_shape_reference",
    "marginal_tech",
    "negative_price_rule",
    "source_label",
    "notes",
}

SOURCE_LABEL_SUFFIX = "interpolated_2025_2039_from_2030_2040"


def _to_num(v: Any) -> float:
    try:
        out = float(v)
        if np.isfinite(out):
            return out
    except Exception:
        pass
    return float("nan")


def _interpolate(v0: Any, v1: Any, t: float) -> float:
    a = _to_num(v0)
    b = _to_num(v1)
    if np.isfinite(a) and np.isfinite(b):
        return float(a + t * (b - a))
    if np.isfinite(a):
        return float(a)
    if np.isfinite(b):
        return float(b)
    return float("nan")


def _clip_numeric(col: str, value: float) -> float:
    out = float(value)
    if col in BOUNDED_01_COLS:
        out = min(max(out, 0.0), 1.0)
    if col in NON_NEGATIVE_COLS:
        out = max(out, 0.0)
    if col in INTEGER_COLS and np.isfinite(out):
        out = float(int(round(out)))
    return out


def _numeric_columns(df: pd.DataFrame) -> list[str]:
    numeric_cols: list[str] = []
    for col in df.columns:
        if col in KEY_COLS:
            continue
        if col in CATEGORICAL_FROZEN_2030:
            continue
        series = pd.to_numeric(df[col], errors="coerce")
        if series.notna().any():
            numeric_cols.append(col)
    return numeric_cols


def expand_phase2_trajectory(
    assumptions_df: pd.DataFrame,
    start_year: int = 2025,
    end_year: int = 2039,
    anchor_start_year: int = 2030,
    anchor_end_year: int = 2040,
) -> pd.DataFrame:
    """Expand a sparse phase2 assumptions table into explicit annual rows.

    Existing rows are preserved. Missing rows between `start_year` and
    `anchor_end_year` are generated from linear interpolation/extrapolation
    between anchor years.
    """
    if assumptions_df is None or assumptions_df.empty:
        return pd.DataFrame(columns=list(assumptions_df.columns) if assumptions_df is not None else [])

    for col in KEY_COLS:
        if col not in assumptions_df.columns:
            raise ValueError(f"Missing required key column: {col}")

    df = assumptions_df.copy()
    original_columns = list(df.columns)
    df["scenario_id"] = df["scenario_id"].astype(str)
    df["country"] = df["country"].astype(str)
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["year"]).copy()
    df["year"] = df["year"].astype(int)

    numeric_cols = _numeric_columns(df)
    target_years = list(range(int(start_year), int(anchor_end_year) + 1))

    rows: list[dict[str, Any]] = []
    grouped = df.sort_values(["scenario_id", "country", "year"]).groupby(["scenario_id", "country"], dropna=False)

    for (scenario_id, country), group in grouped:
        group = group.sort_values("year").drop_duplicates(subset=["year"], keep="first")
        by_year = {int(r["year"]): r for _, r in group.iterrows()}
        anchor_start = by_year.get(int(anchor_start_year))
        anchor_end = by_year.get(int(anchor_end_year))

        if anchor_start is None or anchor_end is None:
            for _, row in group.iterrows():
                rows.append(row.to_dict())
            continue

        for year in target_years:
            if year in by_year:
                rows.append(by_year[year].to_dict())
                continue

            t = float(year - int(anchor_start_year)) / float(int(anchor_end_year) - int(anchor_start_year))
            new_row: dict[str, Any] = {}
            for col in original_columns:
                if col == "scenario_id":
                    new_row[col] = scenario_id
                elif col == "country":
                    new_row[col] = country
                elif col == "year":
                    new_row[col] = int(year)
                elif col in numeric_cols:
                    val = _interpolate(anchor_start.get(col), anchor_end.get(col), t)
                    new_row[col] = _clip_numeric(col, val) if np.isfinite(val) else np.nan
                elif col in CATEGORICAL_FROZEN_2030:
                    if col == "source_label":
                        base_label = str(anchor_start.get("source_label", "")).strip()
                        new_row[col] = f"{base_label}_{SOURCE_LABEL_SUFFIX}" if base_label else SOURCE_LABEL_SUFFIX
                    elif col == "notes":
                        base_notes = str(anchor_start.get("notes", "")).strip()
                        suffix = "generated annual trajectory row"
                        new_row[col] = f"{base_notes} | {suffix}" if base_notes else suffix
                    else:
                        new_row[col] = anchor_start.get(col)
                else:
                    new_row[col] = anchor_start.get(col)
            rows.append(new_row)

    out = pd.DataFrame(rows)
    if out.empty:
        return pd.DataFrame(columns=original_columns)

    for col in original_columns:
        if col not in out.columns:
            out[col] = np.nan
    out = out[original_columns].copy()
    out = out.drop_duplicates(subset=["scenario_id", "country", "year"], keep="first")
    out = out.sort_values(["scenario_id", "country", "year"]).reset_index(drop=True)
    return out
