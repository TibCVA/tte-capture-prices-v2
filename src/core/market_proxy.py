"""Auditable market proxy utilities based on NRL -> price lookup tables."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

EPS = 1e-12


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


def _strictly_increasing_edges(raw_edges: np.ndarray) -> np.ndarray:
    edges = np.asarray(raw_edges, dtype=float)
    edges = edges[np.isfinite(edges)]
    if edges.size == 0:
        return np.asarray([-1.0, 1.0], dtype=float)
    edges = np.unique(edges)
    if edges.size == 1:
        v = float(edges[0])
        return np.asarray([v - 1.0, v + 1.0], dtype=float)
    return edges


def _bin_index(values: np.ndarray, edges: np.ndarray) -> np.ndarray:
    idx = np.searchsorted(edges, values, side="right") - 1
    return np.clip(idx, 0, len(edges) - 2)


def fit_market_proxy(
    hourly_df: pd.DataFrame,
    *,
    nrl_col: str = "nrl_mw",
    price_col: str = "price_da_eur_mwh",
    n_bins: int = 20,
    enforce_monotonic_price: bool = True,
) -> pd.DataFrame:
    """Fit a lookup table mapping NRL bins to expected price and event probabilities."""

    nrl = pd.to_numeric(hourly_df.get(nrl_col), errors="coerce")
    price = pd.to_numeric(hourly_df.get(price_col), errors="coerce")
    tmp = pd.DataFrame({"nrl_mw": nrl, "price_eur_mwh": price}).dropna()

    if tmp.empty:
        return pd.DataFrame(
            [
                {
                    "bin_id": 0,
                    "bin_low": -1.0,
                    "bin_high": 1.0,
                    "bin_mid": 0.0,
                    "mean_price": 0.0,
                    "p_neg": 0.0,
                    "p_below5": 0.0,
                    "count": 0,
                    "source_points": 0,
                    "fit_status": "missing_data",
                }
            ]
        )

    q = np.linspace(0.0, 1.0, max(2, int(n_bins)) + 1)
    edges = _strictly_increasing_edges(np.nanquantile(tmp["nrl_mw"].to_numpy(dtype=float), q))
    n_bins_eff = max(1, len(edges) - 1)

    idx = _bin_index(tmp["nrl_mw"].to_numpy(dtype=float), edges)
    tmp = tmp.assign(bin_id=idx)
    grouped = tmp.groupby("bin_id", observed=True)

    mean_price = grouped["price_eur_mwh"].mean()
    p_neg = grouped["price_eur_mwh"].apply(lambda s: float((s < 0.0).mean()))
    p_below5 = grouped["price_eur_mwh"].apply(lambda s: float((s < 5.0).mean()))
    counts = grouped["price_eur_mwh"].count()

    out = pd.DataFrame(
        {
            "bin_id": np.arange(n_bins_eff, dtype=int),
            "bin_low": edges[:-1],
            "bin_high": edges[1:],
        }
    )
    out["bin_mid"] = 0.5 * (out["bin_low"] + out["bin_high"])
    out = out.merge(mean_price.rename("mean_price"), left_on="bin_id", right_index=True, how="left")
    out = out.merge(p_neg.rename("p_neg"), left_on="bin_id", right_index=True, how="left")
    out = out.merge(p_below5.rename("p_below5"), left_on="bin_id", right_index=True, how="left")
    out = out.merge(counts.rename("count"), left_on="bin_id", right_index=True, how="left")

    for col in ["mean_price", "p_neg", "p_below5"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
        out[col] = out[col].interpolate(limit_direction="both")
    out["count"] = pd.to_numeric(out["count"], errors="coerce").fillna(0).astype(int)

    if enforce_monotonic_price and not out.empty:
        out["mean_price"] = np.maximum.accumulate(out["mean_price"].to_numpy(dtype=float))

    out["p_neg"] = out["p_neg"].clip(lower=0.0, upper=1.0)
    out["p_below5"] = out["p_below5"].clip(lower=0.0, upper=1.0)
    out["p_below5"] = np.maximum(out["p_below5"], out["p_neg"])
    out["source_points"] = int(len(tmp))
    out["fit_status"] = "ok"
    return out.reset_index(drop=True)


def predict_prices(
    mapping: pd.DataFrame,
    nrl_series: pd.Series | np.ndarray,
    *,
    ttl_shift_eur_mwh: float = 0.0,
    shift_top_nrl_quantile: float = 0.90,
) -> pd.Series:
    """Predict price from NRL using the fitted lookup table."""

    nrl = pd.to_numeric(pd.Series(nrl_series), errors="coerce")
    if mapping is None or mapping.empty:
        base = pd.Series(np.nan, index=nrl.index, dtype=float)
    else:
        table = mapping.sort_values("bin_id").reset_index(drop=True)
        edges = np.r_[table["bin_low"].to_numpy(dtype=float), table["bin_high"].to_numpy(dtype=float)[-1]]
        means = table["mean_price"].to_numpy(dtype=float)
        idx = _bin_index(nrl.to_numpy(dtype=float), edges)
        base = pd.Series(means[idx], index=nrl.index, dtype=float)

    shift = _safe_float(ttl_shift_eur_mwh, 0.0)
    if np.isfinite(shift) and abs(shift) > EPS and nrl.notna().any():
        q = float(np.nanquantile(nrl.to_numpy(dtype=float), float(np.clip(shift_top_nrl_quantile, 0.5, 0.99))))
        mask = nrl >= q
        base.loc[mask.fillna(False)] = pd.to_numeric(base.loc[mask.fillna(False)], errors="coerce").fillna(0.0) + shift

    return base


def predict_event_counts(predicted_price_series: pd.Series | np.ndarray) -> dict[str, float]:
    p = pd.to_numeric(pd.Series(predicted_price_series), errors="coerce")
    h_negative_pred = int((p < 0.0).sum())
    h_below5_pred = int((p < 5.0).sum())
    if h_below5_pred < h_negative_pred:
        h_below5_pred = h_negative_pred
    return {"h_negative_pred": float(h_negative_pred), "h_below5_pred": float(h_below5_pred)}


def predict_capture_ratio(
    predicted_price_series: pd.Series | np.ndarray,
    gen_series: pd.Series | np.ndarray,
    avg_price: float | None = None,
) -> float:
    price = pd.to_numeric(pd.Series(predicted_price_series), errors="coerce")
    gen = pd.to_numeric(pd.Series(gen_series), errors="coerce").fillna(0.0).clip(lower=0.0)
    den = float(gen.sum())
    if den <= EPS:
        return float("nan")
    capture_price = float((price * gen).sum()) / den
    ref = _safe_float(avg_price, np.nan)
    if not np.isfinite(ref):
        ref = _safe_float(price.mean(), np.nan)
    if not np.isfinite(ref) or abs(ref) <= EPS:
        return float("nan")
    return float(capture_price / ref)
