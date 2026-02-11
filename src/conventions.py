"""Shared conventions for units and bounded indicators."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

PENETRATION_UNIT_CANONICAL = "pct"


def to_pct(value: float) -> float:
    if not np.isfinite(value):
        return float("nan")
    return float(value) * 100.0


def to_share(value: float) -> float:
    if not np.isfinite(value):
        return float("nan")
    return float(value) / 100.0


def clip01(value: float) -> float:
    if not np.isfinite(value):
        return float("nan")
    return float(np.clip(value, 0.0, 1.0))


def assert_pct_column_bounds(df: pd.DataFrame, columns: Iterable[str]) -> list[str]:
    issues: list[str] = []
    for col in columns:
        if col not in df.columns:
            continue
        s = pd.to_numeric(df[col], errors="coerce")
        bad = s[(s < -1e-9) | (s > 100.0 + 1e-9)]
        if not bad.empty:
            issues.append(f"{col}: {len(bad)} values outside [0,100]")
    return issues


def assert_share_bounds(df: pd.DataFrame, columns: Iterable[str]) -> list[str]:
    issues: list[str] = []
    for col in columns:
        if col not in df.columns:
            continue
        s = pd.to_numeric(df[col], errors="coerce")
        bad = s[(s < -1e-9) | (s > 1.0 + 1e-9)]
        if not bad.empty:
            issues.append(f"{col}: {len(bad)} values outside [0,1]")
    return issues
