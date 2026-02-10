"""Shared conventions and unit helpers."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

PENETRATION_UNIT_CANONICAL = "pct"

PCT_MIN = 0.0
PCT_MAX = 100.0
SHARE_MIN = 0.0
SHARE_MAX = 1.0


def to_pct(value: float) -> float:
    """Convert a share in [0,1] to percent in [0,100]."""
    try:
        x = float(value)
    except Exception:
        return float("nan")
    if not np.isfinite(x):
        return float("nan")
    return float(100.0 * x)


def to_share(value: float) -> float:
    """Convert a percent in [0,100] to share in [0,1]."""
    try:
        x = float(value)
    except Exception:
        return float("nan")
    if not np.isfinite(x):
        return float("nan")
    return float(x / 100.0)


def clip_01(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").clip(lower=SHARE_MIN, upper=SHARE_MAX)


def assert_pct_column_bounds(df: pd.DataFrame, columns: Iterable[str], atol: float = 1e-9) -> list[str]:
    issues: list[str] = []
    for col in columns:
        if col not in df.columns:
            continue
        vals = pd.to_numeric(df[col], errors="coerce").dropna()
        if vals.empty:
            continue
        if (vals < (PCT_MIN - atol)).any() or (vals > (PCT_MAX + atol)).any():
            issues.append(col)
    return issues


def assert_share_bounds(df: pd.DataFrame, columns: Iterable[str], atol: float = 1e-9) -> list[str]:
    issues: list[str] = []
    for col in columns:
        if col not in df.columns:
            continue
        vals = pd.to_numeric(df[col], errors="coerce").dropna()
        if vals.empty:
            continue
        if (vals < (SHARE_MIN - atol)).any() or (vals > (SHARE_MAX + atol)).any():
            issues.append(col)
    return issues
