"""Shared helpers for Q modules."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def assumptions_subset(assumptions_df: pd.DataFrame, keys: list[str]) -> list[dict[str, Any]]:
    if assumptions_df.empty:
        return []
    out = assumptions_df[assumptions_df["param_name"].isin(keys)].copy()
    return out.to_dict(orient="records")


def ensure_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")


def robust_linreg(x: pd.Series, y: pd.Series) -> dict[str, Any]:
    from scipy.stats import linregress

    tmp = pd.DataFrame({"x": pd.to_numeric(x, errors="coerce"), "y": pd.to_numeric(y, errors="coerce")}).dropna()
    n = len(tmp)
    if n < 2:
        return {"slope": np.nan, "intercept": np.nan, "r2": np.nan, "p_value": np.nan, "n": n}
    if tmp["x"].nunique(dropna=True) <= 1:
        return {"slope": np.nan, "intercept": np.nan, "r2": np.nan, "p_value": np.nan, "n": int(n)}

    reg = linregress(tmp["x"], tmp["y"])
    return {
        "slope": float(reg.slope),
        "intercept": float(reg.intercept),
        "r2": float(reg.rvalue**2),
        "p_value": float(reg.pvalue),
        "n": int(n),
    }

