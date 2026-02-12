"""Auditable market proxy utilities based on NRL -> price lookup tables."""

from __future__ import annotations

from dataclasses import dataclass
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


def _weighted_mean(price: pd.Series, volume: pd.Series) -> float:
    p = pd.to_numeric(price, errors="coerce")
    v = pd.to_numeric(volume, errors="coerce").fillna(0.0).clip(lower=0.0)
    den = float(v.sum())
    if den <= EPS:
        return float("nan")
    return float((p * v).sum()) / den


def _strict_decile_edges(values: pd.Series, n_deciles: int = 10) -> np.ndarray:
    vals = pd.to_numeric(values, errors="coerce").to_numpy(dtype=float)
    vals = vals[np.isfinite(vals)]
    if vals.size == 0:
        return np.linspace(-1.0, 1.0, n_deciles + 1, dtype=float)
    q = np.linspace(0.0, 1.0, n_deciles + 1, dtype=float)
    edges = np.nanquantile(vals, q).astype(float)
    # Keep exactly 10 deciles, making duplicated edges strictly increasing.
    for i in range(1, len(edges)):
        if not np.isfinite(edges[i]):
            edges[i] = edges[i - 1]
        if edges[i] <= edges[i - 1]:
            edges[i] = edges[i - 1] + 1e-6
    if edges[-1] <= edges[0]:
        edges = np.linspace(edges[0] - 1.0, edges[0] + 1.0, n_deciles + 1, dtype=float)
    return edges


@dataclass(frozen=True)
class MarketProxyBucketModel:
    residual_edges: np.ndarray
    ir_high_threshold: float
    bucket_stats: pd.DataFrame
    quality_summary: dict[str, Any]
    output_schema_version: str = "2.0.0"
    eps: float = 1e-6

    @staticmethod
    def _extract_features(hourly_df: pd.DataFrame, eps: float = 1e-6) -> pd.DataFrame:
        from src.core.canonical_metrics import build_canonical_hourly_panel

        canonical = build_canonical_hourly_panel(hourly_df)
        load = pd.to_numeric(canonical.get("load_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
        vre = pd.to_numeric(canonical.get("gen_vre_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
        must_run = pd.to_numeric(canonical.get("must_run_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
        residual = load - vre - must_run
        ir_hour = must_run / np.maximum(load, float(max(eps, 1e-12)))
        price = pd.to_numeric(canonical.get("price_eur_mwh"), errors="coerce")
        pv = pd.to_numeric(canonical.get("gen_pv_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
        wind = pd.to_numeric(canonical.get("gen_wind_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
        out = pd.DataFrame(
            {
                "spot_price_eur_mwh": price,
                "load_mw": load,
                "vre_gen_mw": vre,
                "must_run_mw": must_run,
                "residual_load_mw": residual,
                "ir_hour": ir_hour,
                "pv_gen_mw": pv,
                "wind_gen_mw": wind,
            },
            index=canonical.index,
        )
        return out

    @staticmethod
    def _assign_buckets(
        residual_load_mw: pd.Series,
        ir_hour: pd.Series,
        residual_edges: np.ndarray,
        ir_high_threshold: float,
    ) -> pd.DataFrame:
        residual = pd.to_numeric(residual_load_mw, errors="coerce")
        ir = pd.to_numeric(ir_hour, errors="coerce")
        idx = np.searchsorted(np.asarray(residual_edges, dtype=float), residual.to_numpy(dtype=float), side="right") - 1
        idx = np.clip(idx, 0, 9)
        decile = pd.Series(idx + 1, index=residual.index, dtype=int)
        ir_high = (ir >= float(ir_high_threshold)).fillna(False).astype(int)
        bucket_id = (decile - 1) * 2 + ir_high
        return pd.DataFrame(
            {
                "residual_load_decile": decile,
                "ir_high": ir_high,
                "bucket_id": bucket_id.astype(int),
                "bucket_label": decile.map(lambda d: f"d{int(d)}") + "_ir" + ir_high.astype(str),
            },
            index=residual.index,
        )

    @classmethod
    def fit_baseline(cls, hourly_df: pd.DataFrame, *, eps: float = 1e-6) -> "MarketProxyBucketModel":
        feat = cls._extract_features(hourly_df, eps=eps)
        residual_edges = _strict_decile_edges(feat["residual_load_mw"], n_deciles=10)
        ir_high_threshold = float(np.nanquantile(pd.to_numeric(feat["ir_hour"], errors="coerce"), 0.90))
        if not np.isfinite(ir_high_threshold):
            ir_high_threshold = float("inf")

        assigned = cls._assign_buckets(
            feat["residual_load_mw"],
            feat["ir_hour"],
            residual_edges=residual_edges,
            ir_high_threshold=ir_high_threshold,
        )
        df = pd.concat([feat, assigned], axis=1)

        template = pd.MultiIndex.from_product(
            [range(1, 11), [0, 1]],
            names=["residual_load_decile", "ir_high"],
        ).to_frame(index=False)
        template["bucket_id"] = (template["residual_load_decile"] - 1) * 2 + template["ir_high"]
        template["bucket_label"] = (
            "d"
            + template["residual_load_decile"].astype(int).astype(str)
            + "_ir"
            + template["ir_high"].astype(int).astype(str)
        )

        price_valid = df[pd.to_numeric(df["spot_price_eur_mwh"], errors="coerce").notna()].copy()
        grouped = price_valid.groupby(["residual_load_decile", "ir_high"], observed=False)
        stats = grouped.apply(
            lambda g: pd.Series(
                {
                    "p_neg": float((pd.to_numeric(g["spot_price_eur_mwh"], errors="coerce") < 0.0).mean()),
                    "p_low": float((pd.to_numeric(g["spot_price_eur_mwh"], errors="coerce") < 5.0).mean()),
                    "mean_price": float(pd.to_numeric(g["spot_price_eur_mwh"], errors="coerce").mean()),
                    "mean_price_pv_weighted": _weighted_mean(g["spot_price_eur_mwh"], g["pv_gen_mw"]),
                    "mean_price_wind_weighted": _weighted_mean(g["spot_price_eur_mwh"], g["wind_gen_mw"]),
                    "n_hours_bucket": int(len(g)),
                }
            )
        ).reset_index()
        bucket_stats = template.merge(stats, on=["residual_load_decile", "ir_high"], how="left")

        global_p_neg = float((pd.to_numeric(price_valid["spot_price_eur_mwh"], errors="coerce") < 0.0).mean()) if not price_valid.empty else 0.0
        global_p_low = float((pd.to_numeric(price_valid["spot_price_eur_mwh"], errors="coerce") < 5.0).mean()) if not price_valid.empty else 0.0
        global_mean = float(pd.to_numeric(price_valid["spot_price_eur_mwh"], errors="coerce").mean()) if not price_valid.empty else 0.0
        global_pv_mean = _weighted_mean(price_valid["spot_price_eur_mwh"], price_valid["pv_gen_mw"]) if not price_valid.empty else np.nan
        global_wind_mean = _weighted_mean(price_valid["spot_price_eur_mwh"], price_valid["wind_gen_mw"]) if not price_valid.empty else np.nan
        if not np.isfinite(global_pv_mean):
            global_pv_mean = global_mean
        if not np.isfinite(global_wind_mean):
            global_wind_mean = global_mean

        bucket_stats["p_neg"] = pd.to_numeric(bucket_stats["p_neg"], errors="coerce").fillna(global_p_neg).clip(lower=0.0, upper=1.0)
        bucket_stats["p_low"] = pd.to_numeric(bucket_stats["p_low"], errors="coerce").fillna(global_p_low).clip(lower=0.0, upper=1.0)
        bucket_stats["p_low"] = np.maximum(bucket_stats["p_low"].to_numpy(dtype=float), bucket_stats["p_neg"].to_numpy(dtype=float))
        bucket_stats["mean_price"] = pd.to_numeric(bucket_stats["mean_price"], errors="coerce").fillna(global_mean)
        bucket_stats["mean_price_pv_weighted"] = pd.to_numeric(bucket_stats["mean_price_pv_weighted"], errors="coerce").fillna(global_pv_mean)
        bucket_stats["mean_price_wind_weighted"] = pd.to_numeric(bucket_stats["mean_price_wind_weighted"], errors="coerce").fillna(global_wind_mean)
        bucket_stats["n_hours_bucket"] = pd.to_numeric(bucket_stats["n_hours_bucket"], errors="coerce").fillna(0.0).astype(int)

        model = cls(
            residual_edges=np.asarray(residual_edges, dtype=float),
            ir_high_threshold=float(ir_high_threshold),
            bucket_stats=bucket_stats.reset_index(drop=True),
            quality_summary={},
            eps=float(max(eps, 1e-12)),
        )
        baseline_est = model.estimate_from_features(feat)
        h_neg_obs = float(baseline_est.get("h_negative_obs", np.nan))
        h_low_obs = float(baseline_est.get("h_below_5_obs", np.nan))
        err_h_neg = abs(float(baseline_est.get("h_negative_est", np.nan)) - h_neg_obs) if np.isfinite(h_neg_obs) else np.nan
        err_h_low = abs(float(baseline_est.get("h_below_5_est", np.nan)) - h_low_obs) if np.isfinite(h_low_obs) else np.nan

        def _thresholds(obs: float) -> tuple[float, float]:
            if not np.isfinite(obs):
                return float("nan"), float("nan")
            if obs >= 100.0:
                return max(30.0, 0.10 * obs), max(15.0, 0.05 * obs)
            return 30.0, 15.0

        hn_fail_thr, hn_warn_thr = _thresholds(h_neg_obs)
        hl_fail_thr, hl_warn_thr = _thresholds(h_low_obs)
        fail_reasons: list[str] = []
        warn_reasons: list[str] = []
        if np.isfinite(err_h_neg) and np.isfinite(hn_fail_thr) and err_h_neg > hn_fail_thr:
            fail_reasons.append("err_h_negative_above_fail_threshold")
        elif np.isfinite(err_h_neg) and np.isfinite(hn_warn_thr) and err_h_neg > hn_warn_thr:
            warn_reasons.append("err_h_negative_above_warn_threshold")
        if np.isfinite(err_h_low) and np.isfinite(hl_fail_thr) and err_h_low > hl_fail_thr:
            fail_reasons.append("err_h_below_5_above_fail_threshold")
        elif np.isfinite(err_h_low) and np.isfinite(hl_warn_thr) and err_h_low > hl_warn_thr:
            warn_reasons.append("err_h_below_5_above_warn_threshold")

        quality_status = "FAIL" if fail_reasons else ("WARN" if warn_reasons else "PASS")
        quality_summary = {
            "quality_status": quality_status,
            "quality_reasons": "|".join(fail_reasons + warn_reasons),
            "h_negative_obs_before": h_neg_obs,
            "h_negative_est_before": float(baseline_est.get("h_negative_est", np.nan)),
            "h_below_5_obs_before": h_low_obs,
            "h_below_5_est_before": float(baseline_est.get("h_below_5_est", np.nan)),
            "err_h_negative": err_h_neg,
            "err_h_below_5": err_h_low,
            "err_h_negative_fail_threshold": hn_fail_thr,
            "err_h_negative_warn_threshold": hn_warn_thr,
            "err_h_below_5_fail_threshold": hl_fail_thr,
            "err_h_below_5_warn_threshold": hl_warn_thr,
            "n_hours_baseline": int(len(feat)),
        }
        return cls(
            residual_edges=np.asarray(residual_edges, dtype=float),
            ir_high_threshold=float(ir_high_threshold),
            bucket_stats=bucket_stats.reset_index(drop=True),
            quality_summary=quality_summary,
            eps=float(max(eps, 1e-12)),
        )

    def assign_buckets(self, features_df: pd.DataFrame) -> pd.DataFrame:
        return self._assign_buckets(
            features_df["residual_load_mw"],
            features_df["ir_hour"],
            residual_edges=self.residual_edges,
            ir_high_threshold=self.ir_high_threshold,
        )

    def estimate_from_features(self, features_df: pd.DataFrame) -> dict[str, float]:
        feat = features_df.copy()
        assigned = self.assign_buckets(feat)
        df = pd.concat([feat, assigned], axis=1)
        merged = df.merge(
            self.bucket_stats[
                [
                    "residual_load_decile",
                    "ir_high",
                    "p_neg",
                    "p_low",
                    "mean_price",
                    "mean_price_pv_weighted",
                    "mean_price_wind_weighted",
                ]
            ],
            on=["residual_load_decile", "ir_high"],
            how="left",
        )
        n_hours = float(len(merged))
        h_negative_est = float(pd.to_numeric(merged["p_neg"], errors="coerce").fillna(0.0).sum())
        h_below_5_est = float(pd.to_numeric(merged["p_low"], errors="coerce").fillna(0.0).sum())
        baseload_price_est = float(pd.to_numeric(merged["mean_price"], errors="coerce").mean()) if n_hours > 0 else np.nan

        pv = pd.to_numeric(merged.get("pv_gen_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
        wind = pd.to_numeric(merged.get("wind_gen_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
        pv_den = float(pv.sum())
        wind_den = float(wind.sum())
        pv_capture_price_est = (
            float((pd.to_numeric(merged["mean_price_pv_weighted"], errors="coerce").fillna(baseload_price_est) * pv).sum()) / pv_den
            if pv_den > EPS
            else np.nan
        )
        wind_capture_price_est = (
            float((pd.to_numeric(merged["mean_price_wind_weighted"], errors="coerce").fillna(baseload_price_est) * wind).sum()) / wind_den
            if wind_den > EPS
            else np.nan
        )
        capture_ratio_pv_est = pv_capture_price_est / baseload_price_est if np.isfinite(pv_capture_price_est) and np.isfinite(baseload_price_est) and abs(baseload_price_est) > EPS else np.nan
        capture_ratio_wind_est = wind_capture_price_est / baseload_price_est if np.isfinite(wind_capture_price_est) and np.isfinite(baseload_price_est) and abs(baseload_price_est) > EPS else np.nan

        out: dict[str, float] = {
            "h_negative_est": h_negative_est,
            "h_below_5_est": max(h_negative_est, h_below_5_est),
            "baseload_price_est": baseload_price_est,
            "pv_capture_price_est": pv_capture_price_est,
            "wind_capture_price_est": wind_capture_price_est,
            "capture_ratio_pv_est": capture_ratio_pv_est,
            "capture_ratio_wind_est": capture_ratio_wind_est,
            "n_hours": n_hours,
        }

        if "spot_price_eur_mwh" in merged.columns:
            price = pd.to_numeric(merged["spot_price_eur_mwh"], errors="coerce")
            out["h_negative_obs"] = float((price < 0.0).sum())
            out["h_below_5_obs"] = float((price < 5.0).sum())
            out["baseload_price_obs"] = float(price.mean()) if price.notna().any() else np.nan
            out["pv_capture_price_obs"] = _weighted_mean(price, pv)
            out["wind_capture_price_obs"] = _weighted_mean(price, wind)
            out["capture_ratio_pv_obs"] = (
                out["pv_capture_price_obs"] / out["baseload_price_obs"]
                if np.isfinite(out.get("pv_capture_price_obs", np.nan))
                and np.isfinite(out.get("baseload_price_obs", np.nan))
                and abs(float(out.get("baseload_price_obs", np.nan))) > EPS
                else np.nan
            )
            out["capture_ratio_wind_obs"] = (
                out["wind_capture_price_obs"] / out["baseload_price_obs"]
                if np.isfinite(out.get("wind_capture_price_obs", np.nan))
                and np.isfinite(out.get("baseload_price_obs", np.nan))
                and abs(float(out.get("baseload_price_obs", np.nan))) > EPS
                else np.nan
            )
        return out

    def estimate_from_hourly(self, hourly_df: pd.DataFrame) -> dict[str, float]:
        feat = self._extract_features(hourly_df, eps=self.eps)
        return self.estimate_from_features(feat)

    def bucket_edges_table(self) -> pd.DataFrame:
        edges = np.asarray(self.residual_edges, dtype=float)
        return pd.DataFrame(
            {
                "residual_load_decile": np.arange(1, 11, dtype=int),
                "residual_load_edge_low": edges[:-1],
                "residual_load_edge_high": edges[1:],
                "ir_high_threshold": float(self.ir_high_threshold),
            }
        )
