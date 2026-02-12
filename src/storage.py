"""Storage helpers for processed outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.constants import COL_COUNTRY, COL_YEAR


PROCESSED_BASE = Path("data/processed/hourly")
METRICS_BASE = Path("data/metrics")
SCENARIO_BASE = Path("data/processed/scenario")


def hourly_output_path(country: str, year: int) -> Path:
    return PROCESSED_BASE / country / f"{year}.parquet"


def save_hourly(df: pd.DataFrame, country: str, year: int) -> Path:
    path = hourly_output_path(country, year)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=True)
    return path


def load_hourly(country: str, year: int) -> pd.DataFrame:
    path = hourly_output_path(country, year)
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_parquet(path)


def scenario_hourly_output_path(scenario_id: str, country: str, year: int) -> Path:
    return SCENARIO_BASE / scenario_id / "hourly" / country / f"{year}.parquet"


def save_scenario_hourly(df: pd.DataFrame, scenario_id: str, country: str, year: int) -> Path:
    path = scenario_hourly_output_path(scenario_id, country, year)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=True)
    return path


def load_scenario_hourly(scenario_id: str, country: str, year: int) -> pd.DataFrame:
    path = scenario_hourly_output_path(scenario_id, country, year)
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_parquet(path)


def save_scenario_annual_metrics_row(row: dict, scenario_id: str) -> Path:
    path = SCENARIO_BASE / scenario_id / "annual_metrics.parquet"
    df = pd.DataFrame([row])
    upsert_table(path, df, keys=["scenario_id", COL_COUNTRY, COL_YEAR])
    return path


def load_scenario_annual_metrics(scenario_id: str) -> pd.DataFrame:
    path = SCENARIO_BASE / scenario_id / "annual_metrics.parquet"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_parquet(path)


def save_scenario_validation_findings(df: pd.DataFrame, scenario_id: str) -> Path:
    path = SCENARIO_BASE / scenario_id / "validation_findings.parquet"
    key_cols = [c for c in ["scenario_id", "country", "year", "code", "severity"] if c in df.columns]
    if key_cols:
        upsert_table(path, df, keys=key_cols)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, index=False)
    return path


def load_scenario_validation_findings(scenario_id: str) -> pd.DataFrame:
    path = SCENARIO_BASE / scenario_id / "validation_findings.parquet"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_parquet(path)


def upsert_table(path: Path, df_new: pd.DataFrame, keys: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            df_old = pd.read_parquet(path)
            all_df = pd.concat([df_old, df_new], ignore_index=True)
            all_df = all_df.drop_duplicates(subset=keys, keep="last")
        except Exception:
            # Defensive path for partially-written/corrupted parquet files.
            all_df = df_new.copy()
    else:
        all_df = df_new.copy()
    all_df.to_parquet(path, index=False)


def save_annual_metrics_row(row: dict) -> Path:
    path = METRICS_BASE / "annual_metrics.parquet"
    df = pd.DataFrame([row])
    upsert_table(path, df, keys=[COL_COUNTRY, COL_YEAR])
    return path


def save_daily_metrics(df: pd.DataFrame) -> Path:
    path = METRICS_BASE / "daily_metrics.parquet"
    upsert_table(path, df, keys=["country", "date_local"])
    return path


def save_validation_findings(df: pd.DataFrame) -> Path:
    path = METRICS_BASE / "validation_findings.parquet"
    key_cols = [c for c in ["country", "year", "code", "severity"] if c in df.columns]
    if key_cols:
        upsert_table(path, df, keys=key_cols)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, index=False)
    return path

