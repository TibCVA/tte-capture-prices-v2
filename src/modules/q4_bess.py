"""Q4 - BESS sizing and impact simulation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any, Callable

import numpy as np
import pandas as pd

from src.core.market_proxy import MarketProxyBucketModel
from src.hash_utils import hash_object
from src.modules.common import assumptions_subset
from src.modules.result import ModuleResult

Q4_PARAMS = [
    "bess_eta_roundtrip",
    "bess_max_cycles_per_day",
    "bess_soc_init_frac",
    "target_far",
    "target_surplus_unabs_energy_twh",
]

Q4_ENGINE_VERSION = "v2.2.2"
Q4_CACHE_BASE = Path("data/cache/q4")
Q4_OUTPUT_SCHEMA_VERSION = "2.0.0"


@dataclass
class BessConfig:
    power_mw: float
    duration_h: float
    eta_roundtrip: float
    max_cycles_per_day: float
    soc_start_mwh: float = 0.0
    soc_end_target_mwh: float = 0.0

    @property
    def energy_mwh(self) -> float:
        return self.power_mw * self.duration_h

    @property
    def eta_charge(self) -> float:
        return float(np.sqrt(self.eta_roundtrip))

    @property
    def eta_discharge(self) -> float:
        return float(np.sqrt(self.eta_roundtrip))


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


def _ensure_ts_index(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.index, pd.DatetimeIndex):
        out = df.copy()
        if out.index.tz is None:
            out.index = out.index.tz_localize("UTC")
        return out.sort_index()
    if "timestamp_utc" in df.columns:
        out = df.copy()
        out["timestamp_utc"] = pd.to_datetime(out["timestamp_utc"], errors="coerce", utc=True)
        out = out.dropna(subset=["timestamp_utc"]).set_index("timestamp_utc")
        return out.sort_index()
    raise ValueError("Hourly dataframe must have DatetimeIndex or timestamp_utc.")


def _to_float_array(df: pd.DataFrame, col: str) -> np.ndarray:
    if col not in df.columns:
        return np.zeros(len(df), dtype=np.float64)
    return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=np.float64, na_value=np.nan)


def _day_slices(ts_index: pd.DatetimeIndex) -> list[tuple[int, int]]:
    day_key = ts_index.tz_convert("UTC").floor("D").view("int64")
    if len(day_key) == 0:
        return []
    breaks = np.flatnonzero(np.r_[True, day_key[1:] != day_key[:-1], True])
    slices: list[tuple[int, int]] = []
    for i in range(len(breaks) - 1):
        slices.append((int(breaks[i]), int(breaks[i + 1])))
    return slices


def _precompute_low_high_masks(price: np.ndarray, day_ranges: list[tuple[int, int]], duration_values: list[float]) -> dict[float, tuple[np.ndarray, np.ndarray]]:
    out: dict[float, tuple[np.ndarray, np.ndarray]] = {}
    n_total = int(len(price))
    for d in duration_values:
        k = max(1, int(np.ceil(float(d))))
        low_mask = np.zeros(n_total, dtype=bool)
        high_mask = np.zeros(n_total, dtype=bool)
        for start, end in day_ranges:
            segment = price[start:end]
            finite = np.isfinite(segment)
            if not finite.any():
                continue
            finite_idx = np.nonzero(finite)[0]
            vals = segment[finite]
            k_eff = min(k, len(vals))
            order = np.argsort(vals)
            low_local = finite_idx[order[:k_eff]]
            high_local = finite_idx[order[-k_eff:]]
            low_mask[start + low_local] = True
            high_mask[start + high_local] = True
        out[float(d)] = (low_mask, high_mask)
    return out


def _simulate_dispatch_arrays(
    price: np.ndarray,
    nrl: np.ndarray,
    surplus: np.ndarray,
    surplus_unabs: np.ndarray,
    pv: np.ndarray,
    flex_sink_observed: np.ndarray,
    day_ranges: list[tuple[int, int]],
    masks_by_duration: dict[float, tuple[np.ndarray, np.ndarray]],
    cfg: BessConfig,
    dispatch_mode: str,
) -> dict[str, np.ndarray | float]:
    n = len(price)
    charge = np.zeros(n, dtype=np.float64)
    discharge = np.zeros(n, dtype=np.float64)
    soc_series = np.zeros(n, dtype=np.float64)

    low_mask, high_mask = masks_by_duration.get(
        float(cfg.duration_h),
        (np.zeros(n, dtype=bool), np.zeros(n, dtype=bool)),
    )
    nrl_valid = nrl[np.isfinite(nrl)]
    low_residual_thr = float(np.nanquantile(nrl_valid, 0.20)) if len(nrl_valid) else np.nan

    soc = float(cfg.soc_start_mwh)
    soc_start = float(cfg.soc_start_mwh)
    soc_target = float(cfg.soc_end_target_mwh)
    eta_c = float(cfg.eta_charge)
    eta_d = float(cfg.eta_discharge)
    pmax = float(cfg.power_mw)
    emax = float(cfg.energy_mwh)
    max_daily_throughput = max(0.0, float(cfg.max_cycles_per_day)) * emax
    tol = 1e-12
    charge_vs_surplus_violation_hours = 0.0

    for start, end in day_ranges:
        daily_charge = 0.0
        daily_discharge = 0.0

        for i in range(start, end):
            desired_charge = 0.0
            desired_discharge = 0.0
            boundary_forced_discharge = False

            if dispatch_mode == "SURPLUS_FIRST":
                # Strict physical mode: charge only against available unabsorbed surplus.
                if surplus_unabs[i] > 0.0:
                    desired_charge = min(pmax, surplus_unabs[i])
                desired_discharge = 0.0
            elif dispatch_mode == "PRICE_ARBITRAGE_SIMPLE":
                if low_mask[i]:
                    desired_charge = pmax
                elif high_mask[i]:
                    desired_discharge = pmax
            elif dispatch_mode == "LOW_RESIDUAL_FIRST":
                if np.isfinite(low_residual_thr) and np.isfinite(nrl[i]) and nrl[i] <= low_residual_thr:
                    desired_charge = pmax
                elif high_mask[i]:
                    desired_discharge = pmax
            elif dispatch_mode == "PV_COLOCATED":
                if pv[i] > 0.0:
                    desired_charge = min(pmax, pv[i])
                if high_mask[i]:
                    desired_discharge = pmax
            else:
                raise ValueError(f"Unknown dispatch_mode={dispatch_mode}")

            # No simultaneous charge/discharge by design.
            if desired_discharge > 0.0:
                desired_charge = 0.0

            # Enforce terminal SOC boundary (default: SOC_end=0).
            remaining_future_hours = max(0, n - i - 1)
            max_soc_if_no_discharge_now = soc_target + (remaining_future_hours * pmax / eta_d if eta_d > 0 else 0.0)
            max_soc_if_no_discharge_now = min(emax, max(0.0, max_soc_if_no_discharge_now))
            if soc > max_soc_if_no_discharge_now + tol:
                desired_discharge = max(desired_discharge, (soc - max_soc_if_no_discharge_now) * eta_d)
                desired_charge = 0.0
                boundary_forced_discharge = True

            if max_daily_throughput > 0:
                remaining_charge = max(0.0, max_daily_throughput - daily_charge)
                remaining_discharge = max(0.0, max_daily_throughput - daily_discharge)
                if boundary_forced_discharge:
                    # Never let cycle caps violate annual SOC boundary.
                    remaining_discharge = max(remaining_discharge, desired_discharge)
            else:
                remaining_charge = 0.0
                remaining_discharge = 0.0

            soc_headroom = max(0.0, max_soc_if_no_discharge_now - soc)
            ch = min(
                pmax,
                desired_charge,
                max(0.0, soc_headroom / eta_c) if eta_c > 0 else 0.0,
                remaining_charge,
            )
            soc += ch * eta_c
            daily_charge += ch

            dis = min(
                pmax,
                desired_discharge,
                max(0.0, soc * eta_d),
                remaining_discharge,
            )
            soc -= dis / eta_d
            daily_discharge += dis

            if soc < 0.0:
                soc = 0.0
            elif soc > emax:
                soc = emax

            charge[i] = ch
            discharge[i] = dis
            soc_series[i] = soc
            if dispatch_mode == "SURPLUS_FIRST" and ch > surplus_unabs[i] + tol:
                charge_vs_surplus_violation_hours += 1.0

    flex_after = flex_sink_observed + charge
    absorbed_after = np.minimum(surplus, flex_after)
    unabs_after = np.maximum(0.0, surplus - absorbed_after)
    price_clean = np.where(np.isfinite(price), price, 0.0)
    revenue = float(np.sum((discharge - charge) * price_clean))

    return {
        "charge": charge,
        "discharge": discharge,
        "soc": soc_series,
        "absorbed_after": absorbed_after,
        "unabs_after": unabs_after,
        "revenue": revenue,
        "soc_min": float(np.min(soc_series)) if len(soc_series) else 0.0,
        "soc_max": float(np.max(soc_series)) if len(soc_series) else 0.0,
        "charge_max": float(np.max(charge)) if len(charge) else 0.0,
        "discharge_max": float(np.max(discharge)) if len(discharge) else 0.0,
        "charge_sum": float(np.sum(charge)),
        "discharge_sum": float(np.sum(discharge)),
        "charge_hours": float(np.sum(charge > tol)),
        "soc_start": soc_start,
        "soc_end": float(soc),
        "simultaneous_charge_discharge_hours": float(np.sum((charge > tol) & (discharge > tol))),
        "charge_vs_surplus_violation_hours": float(charge_vs_surplus_violation_hours),
    }


def _compute_far_array(surplus: np.ndarray, absorbed: np.ndarray) -> float:
    s = float(np.nansum(np.where(np.isfinite(surplus), surplus, 0.0)))
    a = float(np.nansum(np.where(np.isfinite(absorbed), absorbed, 0.0)))
    if s <= 0.0:
        return 1.0
    return a / s


def _pv_capture(price: np.ndarray, pv: np.ndarray) -> float:
    p = np.where(np.isfinite(price), price, 0.0)
    g = np.where(np.isfinite(pv), pv, 0.0)
    den = float(np.sum(g))
    if den <= 0:
        return np.nan
    return float(np.sum(p * g)) / den


def _capture_ratio(price: np.ndarray, gen: np.ndarray) -> float:
    cap = _pv_capture(price, gen)
    base = float(np.nanmean(price)) if len(price) else np.nan
    if not np.isfinite(cap) or not np.isfinite(base) or abs(base) <= 1e-12:
        return np.nan
    return float(cap / base)


def _daily_spread_metrics(price: np.ndarray, day_ranges: list[tuple[int, int]]) -> tuple[int, float]:
    spreads: list[float] = []
    for start, end in day_ranges:
        seg = price[start:end]
        finite = seg[np.isfinite(seg)]
        if len(finite) == 0:
            continue
        spreads.append(float(np.max(finite) - np.min(finite)))
    if not spreads:
        return 0, np.nan
    arr = np.asarray(spreads, dtype=float)
    return int(np.sum(arr >= 50.0)), float(np.nanmean(arr))


def _negative_price_reducible_upper_bound_hours(
    *,
    neg_mask: np.ndarray,
    surplus_unabs_before: np.ndarray,
    power_mw: float,
    energy_mwh: float,
    max_cycles_per_day: float,
    day_ranges: list[tuple[int, int]],
) -> int:
    """Upper bound on negative-price hours that could be removed by charging.

    Conservative and auditable proxy:
    - candidate hour requires absorbing `surplus_unabs_before[h]` within power limit
    - daily removable energy budget is `energy_mwh * max_cycles_per_day`
    - within each day, we greedily absorb smallest oversupplies first to maximize count
    """
    p = float(max(0.0, power_mw))
    e = float(max(0.0, energy_mwh))
    cpd = float(max(0.0, max_cycles_per_day))
    if p <= 0.0 or e <= 0.0 or cpd <= 0.0 or int(np.sum(neg_mask)) <= 0:
        return 0

    reducible = 0
    for start, end in day_ranges:
        day_neg = neg_mask[start:end]
        if not bool(np.any(day_neg)):
            continue
        day_surplus = np.asarray(surplus_unabs_before[start:end], dtype=float)
        day_need = day_surplus[day_neg]
        day_need = day_need[np.isfinite(day_need)]
        day_need = day_need[day_need > 0.0]
        if day_need.size == 0:
            continue
        day_need = np.sort(day_need)
        remaining = e * cpd
        for need in day_need:
            if need <= p + 1e-9 and need <= remaining + 1e-9:
                reducible += 1
                remaining -= need
            if remaining <= 1e-9:
                break
    return int(reducible)


def _calibrate_price_model(price: np.ndarray, nrl: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(nrl, dtype=float)
    y = np.asarray(price, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    if int(mask.sum()) < 16:
        return (
            np.asarray([-2000.0, -500.0, 0.0, 1000.0, 4000.0], dtype=float),
            np.asarray([-20.0, 0.0, 35.0, 110.0, 250.0], dtype=float),
        )
    xv = x[mask]
    yv = y[mask]
    qx = np.nanquantile(xv, [0.01, 0.10, 0.50, 0.90, 0.99]).astype(float)
    qy = np.nanquantile(yv, [0.05, 0.20, 0.50, 0.80, 0.95]).astype(float)
    # Enforce monotonicity to avoid pathological inversions.
    qy = np.maximum.accumulate(qy)
    if len(np.unique(qx)) < 5:
        qx = np.asarray([-2000.0, -500.0, 0.0, 1000.0, 4000.0], dtype=float)
    return qx, qy


def _price_from_nrl(nrl: np.ndarray, x_knots: np.ndarray, y_knots: np.ndarray) -> np.ndarray:
    x = np.asarray(nrl, dtype=float)
    y = np.interp(x, x_knots, y_knots, left=float(y_knots[0]), right=float(y_knots[-1]))
    return y.astype(float)


def _family_flags_from_metrics(metrics: dict[str, float], thresholds: dict[str, float]) -> dict[str, bool]:
    h_neg = _safe_float(metrics.get("h_negative"), np.nan)
    h_b5 = _safe_float(metrics.get("h_below_5"), np.nan)
    spread_days = _safe_float(metrics.get("days_spread_gt50"), np.nan)
    sr_hours_share = _safe_float(metrics.get("sr_hours_share"), np.nan)
    far = _safe_float(metrics.get("far_after"), np.nan)
    ir = _safe_float(metrics.get("ir_p10"), np.nan)
    low_residual_share = _safe_float(metrics.get("low_residual_share"), np.nan)
    cap_pv = _safe_float(metrics.get("capture_ratio_pv"), np.nan)
    cap_wind = _safe_float(metrics.get("capture_ratio_wind"), np.nan)

    low_price = bool(
        (np.isfinite(h_neg) and h_neg >= thresholds["h_negative_stage2_min"])
        or (np.isfinite(h_b5) and h_b5 >= thresholds["h_below_5_stage2_min"])
        or (np.isfinite(spread_days) and spread_days >= thresholds["days_spread_gt50_stage2_min"])
    )
    physical = bool(
        (np.isfinite(sr_hours_share) and sr_hours_share >= thresholds["sr_hours_stage2_min"])
        or (np.isfinite(far) and far <= thresholds["far_stage2_min"])
        or (np.isfinite(ir) and ir >= thresholds["ir_p10_stage2_min"])
        or (np.isfinite(low_residual_share) and low_residual_share >= thresholds["low_residual_hours_stage2_min"])
    )
    value_pv = bool(np.isfinite(cap_pv) and cap_pv <= thresholds["capture_ratio_pv_stage2_max"])
    value_wind = bool(np.isfinite(cap_wind) and cap_wind <= thresholds["capture_ratio_wind_stage2_max"])
    return {
        "LOW_PRICE": low_price,
        "PHYSICAL": physical,
        "VALUE_PV": value_pv,
        "VALUE_WIND": value_wind,
    }


def _resolve_bascule_family_set(selection: dict[str, Any], baseline_flags: dict[str, bool]) -> set[str]:
    raw = selection.get("bascule_families_active")
    if raw is None:
        return {k for k, v in baseline_flags.items() if bool(v)}
    if isinstance(raw, str):
        return {p.strip().upper() for p in raw.split(",") if p.strip()}
    if isinstance(raw, (list, tuple, set)):
        return {str(p).strip().upper() for p in raw if str(p).strip()}
    return {k for k, v in baseline_flags.items() if bool(v)}


def _selection_grids(selection: dict[str, Any], pv_capacity_proxy_mw: float) -> tuple[list[float], list[float]]:
    proxy = float(max(1.0, pv_capacity_proxy_mw))
    default_power_grid = [round(proxy * x, 3) for x in [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]]
    default_duration_grid = [0.0, 1.0, 2.0, 4.0, 6.0, 8.0, 12.0]
    power_grid = [float(x) for x in selection.get("power_grid", default_power_grid)]
    duration_grid = [float(x) for x in selection.get("duration_grid", default_duration_grid)]
    power_grid = sorted(set([x for x in power_grid if x >= 0.0]))
    duration_grid = sorted(set([x for x in duration_grid if x >= 0.0]))
    if not power_grid:
        power_grid = [0.0]
    if not duration_grid:
        duration_grid = [0.0]
    return power_grid, duration_grid


def _resolve_soc_boundary_mode(selection: dict[str, Any]) -> str:
    mode = str(selection.get("bess_soc_boundary_mode", "ZERO_END")).strip().upper()
    if mode in {"ZERO_END", "ZERO"}:
        return "ZERO_END"
    if mode in {"CYCLIC", "CYCLIC_SAME_AS_START"}:
        return "CYCLIC"
    return "ZERO_END"


def _soc_boundary_targets(energy_mwh: float, mode: str, soc_init_frac: float) -> tuple[float, float]:
    e = max(0.0, float(energy_mwh))
    if e <= 0.0:
        return 0.0, 0.0
    if mode == "CYCLIC":
        frac = float(np.clip(soc_init_frac, 0.0, 1.0))
        start = frac * e
        return start, start
    return 0.0, 0.0


def _objective_satisfied(frontier: pd.DataFrame, objective: str, targets: dict[str, float]) -> pd.DataFrame:
    if frontier.empty:
        return pd.DataFrame()
    if objective == "FAR_TARGET":
        return frontier[frontier["far_after"] >= targets["target_far"]].sort_values(
            ["required_bess_power_mw", "required_bess_energy_mwh"]
        )
    if objective == "SURPLUS_UNABS_TARGET":
        return frontier[frontier["surplus_unabs_energy_after"] <= targets["target_unabs"]].sort_values(
            ["required_bess_power_mw", "required_bess_energy_mwh"]
        )
    if objective == "LOW_PRICE_TARGET":
        hneg_col = "h_negative_est_after" if "h_negative_est_after" in frontier.columns else (
            "h_negative_proxy_after" if "h_negative_proxy_after" in frontier.columns else "h_negative_after"
        )
        hlow_col = "h_below_5_est_after" if "h_below_5_est_after" in frontier.columns else (
            "h_below_5_proxy_after" if "h_below_5_proxy_after" in frontier.columns else "h_below_5_after"
        )
        mask = (
            (pd.to_numeric(frontier[hneg_col], errors="coerce") <= targets["h_negative_target"])
            & (pd.to_numeric(frontier[hlow_col], errors="coerce") <= targets["h_below_5_target"])
        )
        return frontier[mask].sort_values(["required_bess_power_mw", "required_bess_energy_mwh"])
    if objective == "VALUE_TARGET":
        mask = (
            (pd.to_numeric(frontier["capture_ratio_pv_after"], errors="coerce") >= targets["capture_ratio_pv_target"])
            | (pd.to_numeric(frontier["capture_ratio_wind_after"], errors="coerce") >= targets["capture_ratio_wind_target"])
        )
        return frontier[mask].sort_values(["required_bess_power_mw", "required_bess_energy_mwh"])
    if objective == "PHASE_TARGET":
        mask = pd.to_numeric(frontier["turned_off_family_any"], errors="coerce").fillna(0.0) > 0
        return frontier[mask].sort_values(["required_bess_power_mw", "required_bess_energy_mwh"])
    return pd.DataFrame()


def _expand_grid_once(
    power_grid: list[float],
    duration_grid: list[float],
    *,
    power_cap_mw: float,
    duration_cap_h: float,
) -> tuple[list[float], list[float], bool]:
    p_new = sorted(set([float(x) for x in power_grid if x >= 0.0]))
    d_new = sorted(set([float(x) for x in duration_grid if x >= 0.0]))
    changed = False

    p_max = max(p_new) if p_new else 0.0
    d_max = max(d_new) if d_new else 0.0

    if power_cap_mw > p_max + 1e-9:
        cand = min(power_cap_mw, p_max * 1.5 if p_max > 0 else max(1.0, power_cap_mw * 0.25))
        p_new.extend([cand, power_cap_mw])
        changed = True
    if duration_cap_h > d_max + 1e-9:
        cand_d = min(duration_cap_h, d_max * 1.5 if d_max > 0 else max(1.0, duration_cap_h * 0.25))
        d_new.extend([cand_d, duration_cap_h])
        changed = True

    p_new = sorted(set([round(float(x), 6) for x in p_new if x >= 0.0]))
    d_new = sorted(set([round(float(x), 6) for x in d_new if x >= 0.0]))
    return p_new, d_new, changed


def _hourly_signature(df: pd.DataFrame) -> str:
    if df.empty:
        return "empty"
    payload: dict[str, Any] = {
        "rows": int(len(df)),
        "ts_min": str(df.index.min()),
        "ts_max": str(df.index.max()),
    }
    for col in ["surplus_mw", "surplus_unabsorbed_mw", "gen_solar_mw", "price_da_eur_mwh", "flex_sink_observed_mw"]:
        if col in df.columns:
            s = pd.to_numeric(df[col], errors="coerce")
            payload[f"sum_{col}"] = float(np.nan_to_num(s.to_numpy(dtype=float), nan=0.0).sum())
            payload[f"mean_{col}"] = float(s.mean(skipna=True)) if s.notna().any() else np.nan
    return hash_object(payload)[:20]


def _assumption_hash(
    assumptions_df: pd.DataFrame,
    dispatch_mode: str,
    objective: str,
    soc_boundary_mode: str,
    power_grid: list[float],
    duration_grid: list[float],
    data_signature: str,
) -> str:
    sub = assumptions_subset(assumptions_df, Q4_PARAMS)
    payload = {
        "engine_version": Q4_ENGINE_VERSION,
        "dispatch_mode": dispatch_mode,
        "objective": objective,
        "soc_boundary_mode": soc_boundary_mode,
        "power_grid": power_grid,
        "duration_grid": duration_grid,
        "data_signature": data_signature,
        "assumptions": sub,
    }
    return hash_object(payload)[:20]


def _cache_paths(country: str, year: int, dispatch_mode: str, assumption_hash: str) -> tuple[Path, Path]:
    base = Q4_CACHE_BASE / str(country) / str(year) / str(dispatch_mode)
    return base / f"{assumption_hash}.parquet", base / f"{assumption_hash}.meta.json"


def _save_cache(frontier: pd.DataFrame, frontier_path: Path, meta_path: Path, meta: dict[str, Any]) -> None:
    frontier_path.parent.mkdir(parents=True, exist_ok=True)
    frontier.to_parquet(frontier_path, index=False)
    import json

    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2, default=str)


def _load_cache(frontier_path: Path, meta_path: Path) -> tuple[pd.DataFrame | None, dict[str, Any]]:
    if not frontier_path.exists():
        return None, {}
    frontier = pd.read_parquet(frontier_path)
    meta: dict[str, Any] = {}
    if meta_path.exists():
        import json

        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return frontier, meta


def run_q4(
    hourly_df: pd.DataFrame,
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
    dispatch_mode: str = "SURPLUS_FIRST",
    progress_callback: Callable[[str, float], None] | None = None,
) -> ModuleResult:
    t_start = perf_counter()

    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q4_PARAMS)].iterrows()
    }
    all_params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df.iterrows()
        if str(r.get("param_name", "")).strip() != ""
    }
    eta_rt = float(params.get("bess_eta_roundtrip", 0.88))
    soc_init = float(params.get("bess_soc_init_frac", 0.5))
    soc_boundary_mode = _resolve_soc_boundary_mode(selection)
    max_cycles_day = float(params.get("bess_max_cycles_per_day", 1.0))
    target_far = float(params.get("target_far", 0.95))
    target_unabs = float(params.get("target_surplus_unabs_energy_twh", 0.0))

    objective = str(selection.get("objective", "LOW_PRICE_TARGET")).upper()
    if objective not in {"FAR_TARGET", "SURPLUS_UNABS_TARGET", "LOW_PRICE_TARGET", "VALUE_TARGET", "PHASE_TARGET"}:
        objective = "LOW_PRICE_TARGET"

    thresholds = {
        "h_negative_stage2_min": float(all_params.get("h_negative_stage2_min", 200.0)),
        "h_below_5_stage2_min": float(all_params.get("h_below_5_stage2_min", 500.0)),
        "days_spread_gt50_stage2_min": float(all_params.get("days_spread_gt50_stage2_min", 150.0)),
        "sr_hours_stage2_min": float(all_params.get("sr_hours_stage2_min", 0.10)),
        "far_stage2_min": float(all_params.get("far_stage2_min", 0.95)),
        "ir_p10_stage2_min": float(all_params.get("ir_p10_stage2_min", 1.5)),
        "low_residual_hours_stage2_min": float(all_params.get("low_residual_hours_stage2_min", 0.10)),
        "capture_ratio_pv_stage2_max": float(all_params.get("capture_ratio_pv_stage2_max", 0.80)),
        "capture_ratio_wind_stage2_max": float(all_params.get("capture_ratio_wind_stage2_max", 0.90)),
    }
    targets = {
        "target_far": target_far,
        "target_unabs": target_unabs,
        "h_negative_target": float(
            selection.get(
                "h_negative_target",
                all_params.get("stage1_h_negative_max", all_params.get("h_negative_target", 100.0)),
            )
        ),
        "h_below_5_target": float(
            selection.get(
                "h_below_5_target",
                all_params.get("stage1_h_below_5_max", all_params.get("h_below_5_target", 300.0)),
            )
        ),
        "capture_ratio_pv_target": float(
            selection.get("capture_ratio_pv_target", all_params.get("stage1_capture_ratio_pv_min", 0.85))
        ),
        "capture_ratio_wind_target": float(
            selection.get("capture_ratio_wind_target", all_params.get("stage1_capture_ratio_wind_min", 0.90))
        ),
    }

    base = _ensure_ts_index(hourly_df)
    pv_series_proxy = pd.to_numeric(base.get("gen_solar_mw"), errors="coerce")
    pv_capacity_proxy = (
        float(np.nanquantile(pv_series_proxy.to_numpy(dtype=float), 0.99))
        if pv_series_proxy.notna().any()
        else float(np.nanmax(pd.to_numeric(base.get("gen_vre_mw"), errors="coerce").to_numpy(dtype=float)))
        if "gen_vre_mw" in base.columns
        else 1000.0
    )
    if not np.isfinite(pv_capacity_proxy) or pv_capacity_proxy <= 0:
        pv_capacity_proxy = 1000.0
    power_grid, duration_grid = _selection_grids(selection, pv_capacity_proxy_mw=pv_capacity_proxy)
    force_recompute = bool(selection.get("force_recompute", False))

    data_signature = _hourly_signature(base)

    country = str(selection.get("country", ""))
    year = int(selection.get("year", 0))
    scenario_id = str(selection.get("scenario_id", "") or "")
    mode = str(selection.get("mode", "HIST")).upper()
    scenario_id_effective = scenario_id if scenario_id else ("HIST" if mode == "HIST" else "SCEN")
    assumption_hash = _assumption_hash(
        assumptions_df=assumptions_df,
        dispatch_mode=dispatch_mode,
        objective=objective,
        soc_boundary_mode=soc_boundary_mode,
        power_grid=power_grid,
        duration_grid=duration_grid,
        data_signature=data_signature,
    )
    frontier_path, meta_path = _cache_paths(country, year, dispatch_mode, assumption_hash)

    if progress_callback:
        progress_callback("Initialisation Q4", 0.02)

    checks: list[dict[str, str]] = []
    warnings: list[str] = []

    frontier: pd.DataFrame
    cache_hit = False
    proxy_quality_status = "NOT_RUN"
    proxy_quality_reasons = "not_run"
    grid_expansions_used = 0
    grid_power_cap_mw = np.nan
    grid_duration_cap_h = np.nan
    cached_frontier, cached_meta = (None, {})
    if not force_recompute:
        cached_frontier, cached_meta = _load_cache(frontier_path, meta_path)
    if cached_frontier is not None:
        frontier = cached_frontier.copy()
        cache_hit = True
        if "proxy_quality_status" in frontier.columns and frontier["proxy_quality_status"].notna().any():
            proxy_quality_status = str(frontier["proxy_quality_status"].dropna().iloc[0])
        if "proxy_quality_reasons" in frontier.columns and frontier["proxy_quality_reasons"].notna().any():
            proxy_quality_reasons = str(frontier["proxy_quality_reasons"].dropna().iloc[0])
        grid_expansions_used = int(cached_meta.get("grid_expansions_used", 0)) if isinstance(cached_meta, dict) else 0
        if "engine_version" not in frontier.columns:
            frontier["engine_version"] = str(cached_meta.get("engine_version", Q4_ENGINE_VERSION))
        if "compute_time_sec" not in frontier.columns:
            frontier["compute_time_sec"] = float(cached_meta.get("compute_time_sec", 0.0))
        if "scenario_id" not in frontier.columns:
            frontier["scenario_id"] = scenario_id_effective
        else:
            sid = frontier["scenario_id"].astype(str).replace({"nan": "", "None": ""})
            sid = sid.mask(sid.str.strip().eq(""), scenario_id_effective)
            frontier["scenario_id"] = sid
        if "country" not in frontier.columns:
            frontier["country"] = country
        else:
            ctry = frontier["country"].astype(str).replace({"nan": "", "None": ""})
            ctry = ctry.mask(ctry.str.strip().eq(""), country)
            frontier["country"] = ctry
        if "year" not in frontier.columns:
            frontier["year"] = year
        else:
            y = pd.to_numeric(frontier["year"], errors="coerce")
            frontier["year"] = y.fillna(year).astype(int)
        frontier["cache_hit"] = True
        if progress_callback:
            progress_callback("Chargement cache Q4", 0.95)
    else:
        for c in ["surplus_mw", "surplus_unabsorbed_mw", "gen_solar_mw", "price_da_eur_mwh", "flex_sink_observed_mw", "surplus_absorbed_mw"]:
            if c not in base.columns:
                base[c] = 0.0

        price = _to_float_array(base, "price_da_eur_mwh")
        surplus = np.where(np.isfinite(_to_float_array(base, "surplus_mw")), _to_float_array(base, "surplus_mw"), 0.0)
        pv = np.where(np.isfinite(_to_float_array(base, "gen_solar_mw")), _to_float_array(base, "gen_solar_mw"), 0.0)
        flex_sink_observed = np.where(np.isfinite(_to_float_array(base, "flex_sink_observed_mw")), _to_float_array(base, "flex_sink_observed_mw"), 0.0)
        absorbed_base_model = np.minimum(surplus, flex_sink_observed)
        surplus_unabs_model = np.maximum(0.0, surplus - absorbed_base_model)
        if "nrl_mw" in base.columns:
            nrl = np.where(np.isfinite(_to_float_array(base, "nrl_mw")), _to_float_array(base, "nrl_mw"), 0.0)
        elif {"load_mw", "gen_vre_mw", "gen_must_run_mw"}.issubset(set(base.columns)):
            load_arr = np.where(np.isfinite(_to_float_array(base, "load_mw")), _to_float_array(base, "load_mw"), 0.0)
            vre_arr = np.where(np.isfinite(_to_float_array(base, "gen_vre_mw")), _to_float_array(base, "gen_vre_mw"), 0.0)
            must_run_arr = np.where(np.isfinite(_to_float_array(base, "gen_must_run_mw")), _to_float_array(base, "gen_must_run_mw"), 0.0)
            nrl = load_arr - vre_arr - must_run_arr
        else:
            # Fallback when NRL inputs are missing.
            nrl = np.where(surplus > 0.0, -surplus, 0.0)

        total_surplus_mwh = float(np.sum(surplus))
        if total_surplus_mwh <= 1e-9:
            base_far = 1.0
            unabs_before_twh = 0.0
            far_before_trivial = True
        else:
            base_far = _compute_far_array(surplus, absorbed_base_model)
            unabs_before_twh = float(np.sum(surplus_unabs_model) / 1e6)
            far_before_trivial = False

        pv_before = _pv_capture(price, pv)
        baseload_before = float(np.nanmean(price)) if len(price) else np.nan
        capture_ratio_pv_before = (pv_before / baseload_before) if np.isfinite(pv_before) and np.isfinite(baseload_before) and abs(baseload_before) > 1e-12 else np.nan
        wind = np.where(
            np.isfinite(_to_float_array(base, "gen_wind_on_mw") + _to_float_array(base, "gen_wind_off_mw")),
            _to_float_array(base, "gen_wind_on_mw") + _to_float_array(base, "gen_wind_off_mw"),
            0.0,
        )
        wind_before = _pv_capture(price, wind)
        capture_ratio_wind_before = (
            wind_before / baseload_before
            if np.isfinite(wind_before) and np.isfinite(baseload_before) and abs(baseload_before) > 1e-12
            else np.nan
        )
        h_negative_before = int(np.nansum(np.where(np.isfinite(price), price < 0.0, 0)))
        h_below_5_before = int(np.nansum(np.where(np.isfinite(price), price < 5.0, 0)))
        day_ranges = _day_slices(base.index)
        spread_days_before, avg_spread_before = _daily_spread_metrics(price, day_ranges)
        nrl_pos = nrl[np.isfinite(nrl) & (nrl > 0.0)]
        low_residual_thr = float(np.nanquantile(nrl_pos, 0.10)) if len(nrl_pos) else np.nan
        low_residual_before = (
            (nrl >= 0.0) & (nrl <= low_residual_thr)
            if np.isfinite(low_residual_thr)
            else np.zeros(len(nrl), dtype=bool)
        )
        low_residual_share_before = float(np.mean(low_residual_before)) if len(low_residual_before) else np.nan
        load_arr = np.where(np.isfinite(_to_float_array(base, "load_mw")), _to_float_array(base, "load_mw"), 0.0)
        vre_arr = np.where(np.isfinite(_to_float_array(base, "gen_vre_mw")), _to_float_array(base, "gen_vre_mw"), 0.0)
        must_run_arr = np.where(np.isfinite(_to_float_array(base, "gen_must_run_mw")), _to_float_array(base, "gen_must_run_mw"), 0.0)
        if not np.isfinite(vre_arr).any() or float(np.nanmax(np.abs(vre_arr))) <= 1e-12:
            vre_arr = np.maximum(0.0, load_arr - must_run_arr - nrl)
        p10_load = float(np.nanquantile(load_arr[load_arr > 0.0], 0.10)) if np.any(load_arr > 0.0) else np.nan
        p10_mr = float(np.nanquantile(must_run_arr[must_run_arr >= 0.0], 0.10)) if len(must_run_arr) else np.nan
        ir_before = (p10_mr / p10_load) if np.isfinite(p10_mr) and np.isfinite(p10_load) and p10_load > 0 else np.nan
        sr_hours_share_before = float(np.mean(surplus > 0.0)) if len(surplus) else np.nan
        try:
            market_proxy_model = MarketProxyBucketModel.fit_baseline(base, eps=1e-6)
            proxy_quality_status = str(market_proxy_model.quality_summary.get("quality_status", "FAIL")).upper()
            proxy_quality_reasons = str(market_proxy_model.quality_summary.get("quality_reasons", "")).strip()
        except Exception as exc:
            market_proxy_model = None
            proxy_quality_status = "FAIL"
            proxy_quality_reasons = f"market_proxy_fit_error:{exc}"

        if market_proxy_model is None or proxy_quality_status == "FAIL":
            fail_msg = f"Q4 proxy FAIL: {proxy_quality_reasons or 'market_proxy_invalid'}"
            return ModuleResult(
                module_id="Q4",
                run_id=run_id,
                selection={**selection, "dispatch_mode": dispatch_mode},
                assumptions_used=assumptions_subset(assumptions_df, Q4_PARAMS),
                kpis={
                    "objective": objective,
                    "objective_met": False,
                    "objective_reason": "market_proxy_invalid",
                    "objective_not_reached": True,
                    "compute_time_sec": float(perf_counter() - t_start),
                    "cache_hit": cache_hit,
                    "engine_version": Q4_ENGINE_VERSION,
                    "assumption_hash": assumption_hash,
                },
                    tables={
                        "Q4_sizing_summary": pd.DataFrame(
                            [
                                {
                                    "scenario_id": scenario_id_effective,
                                "country": country,
                                "year": year,
                                "status": "FAIL",
                                "reason": "market_proxy_invalid",
                                "proxy_quality_status": proxy_quality_status,
                                "proxy_quality_reasons": proxy_quality_reasons,
                                    "output_schema_version": Q4_OUTPUT_SCHEMA_VERSION,
                                }
                            ]
                        ),
                        "Q4_bess_frontier": pd.DataFrame(),
                        "q4_quality_summary": pd.DataFrame(
                            [
                                {
                                    "module_id": "Q4",
                                    "country": country,
                                    "year": year,
                                    "scenario_id": scenario_id_effective,
                                    "quality_status": "FAIL",
                                    "proxy_quality_status": proxy_quality_status,
                                    "proxy_quality_reasons": proxy_quality_reasons,
                                    "output_schema_version": Q4_OUTPUT_SCHEMA_VERSION,
                                }
                            ]
                        ),
                    },
                figures=[],
                narrative_md="Q4 interrompu: proxy marche invalide.",
                checks=[
                    {
                        "status": "FAIL",
                        "code": "Q4_MARKET_PROXY_INVALID",
                        "message": fail_msg,
                    }
                ],
                warnings=warnings + [fail_msg],
                mode=str(selection.get("mode", "HIST")).upper(),
                scenario_id=scenario_id_effective,
                horizon_year=selection.get("horizon_year"),
            )

        baseline_est = market_proxy_model.estimate_from_hourly(base)
        h_negative_obs_before = float(h_negative_before)
        h_below_5_obs_before = float(h_below_5_before)
        h_negative_est_before = _safe_float(baseline_est.get("h_negative_est"), h_negative_obs_before)
        h_below_5_est_before = _safe_float(baseline_est.get("h_below_5_est"), h_below_5_obs_before)
        h_below_5_est_before = max(h_negative_est_before, h_below_5_est_before)
        h_negative_proxy_before = h_negative_est_before
        h_below_5_proxy_before = h_below_5_est_before
        baseload_price_est_before = _safe_float(baseline_est.get("baseload_price_est"), baseload_before)
        pv_capture_price_obs_before = _safe_float(baseline_est.get("pv_capture_price_obs"), pv_before)
        wind_capture_price_obs_before = _safe_float(baseline_est.get("wind_capture_price_obs"), wind_before)
        pv_capture_price_est_before = _safe_float(baseline_est.get("pv_capture_price_est"), pv_before)
        wind_capture_price_est_before = _safe_float(baseline_est.get("wind_capture_price_est"), wind_before)
        capture_ratio_pv_est_before = _safe_float(baseline_est.get("capture_ratio_pv_est"), capture_ratio_pv_before)
        capture_ratio_wind_est_before = _safe_float(baseline_est.get("capture_ratio_wind_est"), capture_ratio_wind_before)

        baseline_metrics = {
            "h_negative": float(h_negative_est_before),
            "h_below_5": float(h_below_5_est_before),
            "days_spread_gt50": float(spread_days_before),
            "sr_hours_share": float(sr_hours_share_before),
            "far_after": float(base_far),
            "ir_p10": float(ir_before) if np.isfinite(ir_before) else np.nan,
            "low_residual_share": float(low_residual_share_before) if np.isfinite(low_residual_share_before) else np.nan,
            "capture_ratio_pv": float(capture_ratio_pv_est_before) if np.isfinite(capture_ratio_pv_est_before) else np.nan,
            "capture_ratio_wind": float(capture_ratio_wind_est_before) if np.isfinite(capture_ratio_wind_est_before) else np.nan,
        }
        baseline_family_flags = _family_flags_from_metrics(baseline_metrics, thresholds)
        bascule_families_active = _resolve_bascule_family_set(selection, baseline_family_flags)

        if progress_callback:
            progress_callback("Pre-calcul des structures journalieres", 0.10)

        masks_by_duration = _precompute_low_high_masks(price, day_ranges, duration_grid)

        def _simulate_frontier_for_grid(power_vals: list[float], duration_vals: list[float], progress_base: float, progress_span: float) -> pd.DataFrame:
            missing_duration_masks = [float(d) for d in duration_vals if float(d) not in masks_by_duration]
            if missing_duration_masks:
                masks_by_duration.update(_precompute_low_high_masks(price, day_ranges, missing_duration_masks))

            rows: list[dict[str, Any]] = []
            combos: list[tuple[float, float]] = []
            seen_nonzero: set[tuple[float, float]] = set()
            zero_added = False
            for p in power_vals:
                for d in duration_vals:
                    p_val = float(p)
                    d_val = float(d)
                    e_val = p_val * d_val
                    if (abs(p_val) <= 1e-12) or (abs(e_val) <= 1e-12):
                        if not zero_added:
                            combos.append((0.0, 0.0))
                            zero_added = True
                        continue
                    key = (round(p_val, 9), round(e_val, 9))
                    if key in seen_nonzero:
                        continue
                    seen_nonzero.add(key)
                    combos.append((p_val, d_val))
            if not combos:
                combos = [(0.0, 0.0)]

            total_scenarios = max(1, len(combos))
            scenario_idx = 0
            for p, d in combos:
                scenario_idx += 1
                if progress_callback:
                    progress_callback(
                        f"Simulation scenario {scenario_idx}/{total_scenarios}",
                        progress_base + progress_span * (scenario_idx / total_scenarios),
                    )
                cfg_tmp = BessConfig(
                    power_mw=float(p),
                    duration_h=float(d),
                    eta_roundtrip=eta_rt,
                    max_cycles_per_day=max_cycles_day,
                )
                soc_start_mwh, soc_end_target_mwh = _soc_boundary_targets(
                    energy_mwh=cfg_tmp.energy_mwh,
                    mode=soc_boundary_mode,
                    soc_init_frac=soc_init,
                )
                cfg = BessConfig(
                    power_mw=float(p),
                    duration_h=float(d),
                    eta_roundtrip=eta_rt,
                    max_cycles_per_day=max_cycles_day,
                    soc_start_mwh=soc_start_mwh,
                    soc_end_target_mwh=soc_end_target_mwh,
                )
                sim = _simulate_dispatch_arrays(
                    price=price,
                    nrl=nrl,
                    surplus=surplus,
                    surplus_unabs=surplus_unabs_model,
                    pv=pv,
                    flex_sink_observed=flex_sink_observed,
                    day_ranges=day_ranges,
                    masks_by_duration=masks_by_duration,
                    cfg=cfg,
                    dispatch_mode=dispatch_mode,
                )

                if total_surplus_mwh <= 1e-9:
                    far_after = 1.0
                    unabs_after_twh = 0.0
                    far_after_trivial = True
                else:
                    far_after = _compute_far_array(surplus, sim["absorbed_after"])
                    unabs_after_twh = float(np.sum(sim["unabs_after"]) / 1e6)
                    far_after_trivial = False
                nrl_after = nrl + sim["charge"] - sim["discharge"]

                # Keep price-based outputs for value diagnostics, but low-price counters use proxy/upper-bound.
                price_after = np.array(price, dtype=float, copy=True)
                if cfg.power_mw > 0.0 and cfg.energy_mwh > 0.0:
                    full_absorb_mask = (surplus > 0.0) & (sim["unabs_after"] <= 1e-9)
                    price_after[full_absorb_mask] = np.maximum(price_after[full_absorb_mask], 0.0)
                spread_days_after, avg_spread_after = _daily_spread_metrics(price_after, day_ranges)
                baseload_after = float(np.nanmean(price_after)) if len(price_after) else np.nan
                revenue = float(np.sum((sim["discharge"] - sim["charge"]) * price_after))

                if dispatch_mode == "PV_COLOCATED":
                    pv_to_grid = np.maximum(0.0, pv - sim["charge"])
                    pv_shifted = sim["discharge"]
                    delivered_pv = pv_to_grid + pv_shifted
                else:
                    delivered_pv = pv
                pv_after = _pv_capture(price_after, delivered_pv)
                wind_after = _pv_capture(price_after, wind)
                capture_ratio_pv_after = (
                    pv_after / baseload_after
                    if np.isfinite(pv_after) and np.isfinite(baseload_after) and abs(baseload_after) > 1e-12
                    else np.nan
                )
                capture_ratio_wind_after = (
                    wind_after / baseload_after
                    if np.isfinite(wind_after) and np.isfinite(baseload_after) and abs(baseload_after) > 1e-12
                    else np.nan
                )

                neg_mask_before = np.where(np.isfinite(price), price < 0.0, False)
                reducible_upper_bound_hours = _negative_price_reducible_upper_bound_hours(
                    neg_mask=neg_mask_before,
                    surplus_unabs_before=surplus_unabs_model,
                    power_mw=cfg.power_mw,
                    energy_mwh=cfg.energy_mwh,
                    max_cycles_per_day=cfg.max_cycles_per_day,
                    day_ranges=day_ranges,
                )
                h_negative_upper_bound_after = int(max(0, h_negative_before - reducible_upper_bound_hours))
                load_after = load_arr + sim["charge"] - sim["discharge"]
                residual_after = nrl_after
                ir_hour_after = must_run_arr / np.maximum(load_after, 1e-6)
                features_after = pd.DataFrame(
                    {
                        "spot_price_eur_mwh": pd.to_numeric(pd.Series(price, index=base.index), errors="coerce"),
                        "load_mw": pd.to_numeric(pd.Series(load_after, index=base.index), errors="coerce").fillna(0.0).clip(lower=0.0),
                        "vre_gen_mw": pd.to_numeric(pd.Series(vre_arr, index=base.index), errors="coerce").fillna(0.0).clip(lower=0.0),
                        "must_run_mw": pd.to_numeric(pd.Series(must_run_arr, index=base.index), errors="coerce").fillna(0.0).clip(lower=0.0),
                        "residual_load_mw": pd.to_numeric(pd.Series(residual_after, index=base.index), errors="coerce"),
                        "ir_hour": pd.to_numeric(pd.Series(ir_hour_after, index=base.index), errors="coerce"),
                        "pv_gen_mw": pd.to_numeric(pd.Series(pv, index=base.index), errors="coerce").fillna(0.0).clip(lower=0.0),
                        "wind_gen_mw": pd.to_numeric(pd.Series(wind, index=base.index), errors="coerce").fillna(0.0).clip(lower=0.0),
                    },
                    index=base.index,
                )
                est_after = market_proxy_model.estimate_from_features(features_after)
                h_negative_est_after_raw = _safe_float(est_after.get("h_negative_est"), np.nan)
                h_below_5_est_after_raw = _safe_float(est_after.get("h_below_5_est"), np.nan)
                if cfg.power_mw <= 0.0 or cfg.energy_mwh <= 0.0:
                    h_negative_est_after_raw = float(h_negative_est_before)
                    h_below_5_est_after_raw = float(h_below_5_est_before)
                    h_negative_est_after = float(h_negative_est_before)
                    h_below_5_est_after = float(h_below_5_est_before)
                    baseload_price_est_after = float(baseload_price_est_before)
                    pv_capture_price_est_after = float(pv_capture_price_est_before)
                    wind_capture_price_est_after = float(wind_capture_price_est_before)
                    capture_ratio_pv_est_after = float(capture_ratio_pv_est_before)
                    capture_ratio_wind_est_after = float(capture_ratio_wind_est_before)
                else:
                    h_negative_est_after = min(float(h_negative_est_before), float(h_negative_est_after_raw))
                    h_below_5_est_after = min(float(h_below_5_est_before), float(h_below_5_est_after_raw))
                    h_below_5_est_after = max(h_below_5_est_after, h_negative_est_after)
                    baseload_price_est_after = _safe_float(est_after.get("baseload_price_est"), np.nan)
                    pv_capture_price_est_after = _safe_float(est_after.get("pv_capture_price_est"), np.nan)
                    wind_capture_price_est_after = _safe_float(est_after.get("wind_capture_price_est"), np.nan)
                    capture_ratio_pv_est_after = _safe_float(est_after.get("capture_ratio_pv_est"), np.nan)
                    capture_ratio_wind_est_after = _safe_float(est_after.get("capture_ratio_wind_est"), np.nan)

                nrl_after_pos = nrl_after[nrl_after > 0.0]
                low_residual_thr_after = float(np.nanquantile(nrl_after_pos, 0.10)) if len(nrl_after_pos) else np.nan
                low_residual_after = (
                    (nrl_after >= 0.0) & (nrl_after <= low_residual_thr_after)
                    if np.isfinite(low_residual_thr_after)
                    else np.zeros(len(nrl_after), dtype=bool)
                )
                sr_hours_share_after = float(np.mean(np.maximum(0.0, -nrl_after) > 0.0))
                p10_load_after = float(np.nanquantile(load_after[load_after > 0.0], 0.10)) if np.any(load_after > 0.0) else np.nan
                ir_after = (p10_mr / p10_load_after) if np.isfinite(p10_mr) and np.isfinite(p10_load_after) and p10_load_after > 0 else np.nan
                metrics_after = {
                    "h_negative": float(h_negative_est_after),
                    "h_below_5": float(h_below_5_est_after),
                    "days_spread_gt50": float(spread_days_after),
                    "sr_hours_share": float(sr_hours_share_after),
                    "far_after": float(far_after),
                    "ir_p10": float(ir_after) if np.isfinite(ir_after) else np.nan,
                    "low_residual_share": float(np.mean(low_residual_after)) if len(low_residual_after) else np.nan,
                    "capture_ratio_pv": float(capture_ratio_pv_est_after) if np.isfinite(capture_ratio_pv_est_after) else np.nan,
                    "capture_ratio_wind": float(capture_ratio_wind_est_after) if np.isfinite(capture_ratio_wind_est_after) else np.nan,
                }
                family_after = _family_flags_from_metrics(metrics_after, thresholds)
                turned_off_family = {
                    fam: bool(fam in bascule_families_active and not family_after.get(fam, False))
                    for fam in ["LOW_PRICE", "PHYSICAL", "VALUE_PV", "VALUE_WIND"]
                }
                turned_off_any = bool(any(turned_off_family.values()))
                n_days = max(1, len(day_ranges))
                if cfg.energy_mwh > 0.0 and cfg.max_cycles_per_day > 0.0:
                    cycles_realized_per_day = float(sim["discharge_sum"]) / (cfg.energy_mwh * n_days)
                    cycles_realized_per_day = float(np.clip(cycles_realized_per_day, 0.0, cfg.max_cycles_per_day))
                else:
                    cycles_realized_per_day = 0.0

                rows.append(
                    {
                        "scenario_id": scenario_id_effective,
                        "country": country,
                        "year": year,
                        "dispatch_mode": dispatch_mode,
                        "objective": objective,
                        "bess_power_mw_test": cfg.power_mw,
                        "bess_energy_mwh_test": cfg.energy_mwh,
                        "bess_duration_h_test": cfg.duration_h,
                        "required_bess_power_mw": cfg.power_mw,
                        "required_bess_energy_mwh": cfg.energy_mwh,
                        "required_bess_duration_h": cfg.duration_h,
                        "far_before": base_far,
                        "far_after": far_after,
                        "far_before_trivial": far_before_trivial,
                        "far_after_trivial": far_after_trivial,
                        "h_negative_obs_before": h_negative_obs_before,
                        "h_negative_est_before": h_negative_est_before,
                        "h_negative_est_after": h_negative_est_after,
                        "h_negative_before": h_negative_obs_before,
                        "h_negative_after": h_negative_est_after,
                        "h_negative_proxy_before": h_negative_est_before,
                        "h_negative_proxy_after": h_negative_est_after,
                        "h_negative_proxy_raw_after": h_negative_est_after_raw,
                        "h_negative_reducible_upper_bound": reducible_upper_bound_hours,
                        "h_negative_upper_bound_after": h_negative_upper_bound_after,
                        "h_below_5_obs_before": h_below_5_obs_before,
                        "h_below_5_est_before": h_below_5_est_before,
                        "h_below_5_est_after": h_below_5_est_after,
                        "h_below_5_before": h_below_5_obs_before,
                        "h_below_5_after": h_below_5_est_after,
                        "h_below_5_proxy_before": h_below_5_est_before,
                        "h_below_5_proxy_after": h_below_5_est_after,
                        "h_below_5_proxy_raw_after": h_below_5_est_after_raw,
                        "delta_h_negative_est": float(h_negative_est_after - h_negative_est_before),
                        "delta_h_below_5_est": float(h_below_5_est_after - h_below_5_est_before),
                        "delta_h_negative": float(h_negative_est_after - h_negative_est_before),
                        "delta_h_below_5": float(h_below_5_est_after - h_below_5_est_before),
                        "h_negative_after_source": "est_proxy",
                        "h_below_5_after_source": "est_proxy",
                        "baseload_price_obs_before": baseload_before,
                        "baseload_price_est_before": baseload_price_est_before,
                        "baseload_price_est_after": baseload_price_est_after,
                        "baseload_price_before": baseload_before,
                        "baseload_price_after": baseload_price_est_after,
                        "capture_ratio_pv_obs_before": capture_ratio_pv_before,
                        "capture_ratio_pv_est_before": capture_ratio_pv_est_before,
                        "capture_ratio_pv_est_after": capture_ratio_pv_est_after,
                        "capture_ratio_pv_before": capture_ratio_pv_est_before,
                        "capture_ratio_pv_after": capture_ratio_pv_est_after,
                        "capture_ratio_wind_obs_before": capture_ratio_wind_before,
                        "capture_ratio_wind_est_before": capture_ratio_wind_est_before,
                        "capture_ratio_wind_est_after": capture_ratio_wind_est_after,
                        "capture_ratio_wind_before": capture_ratio_wind_est_before,
                        "capture_ratio_wind_after": capture_ratio_wind_est_after,
                        "delta_capture_ratio_est_pv": (capture_ratio_pv_est_after - capture_ratio_pv_est_before)
                        if np.isfinite(capture_ratio_pv_est_after) and np.isfinite(capture_ratio_pv_est_before)
                        else np.nan,
                        "delta_capture_ratio_est_wind": (capture_ratio_wind_est_after - capture_ratio_wind_est_before)
                        if np.isfinite(capture_ratio_wind_est_after) and np.isfinite(capture_ratio_wind_est_before)
                        else np.nan,
                        "delta_capture_ratio_pv": (capture_ratio_pv_est_after - capture_ratio_pv_est_before)
                        if np.isfinite(capture_ratio_pv_est_after) and np.isfinite(capture_ratio_pv_est_before)
                        else np.nan,
                        "delta_capture_ratio_wind": (capture_ratio_wind_est_after - capture_ratio_wind_est_before)
                        if np.isfinite(capture_ratio_wind_est_after) and np.isfinite(capture_ratio_wind_est_before)
                        else np.nan,
                        "surplus_unabs_energy_before": unabs_before_twh,
                        "surplus_unabs_energy_after": unabs_after_twh,
                        "pv_capture_price_obs_before": pv_capture_price_obs_before,
                        "pv_capture_price_est_before": pv_capture_price_est_before,
                        "pv_capture_price_est_after": pv_capture_price_est_after,
                        "pv_capture_price_before": pv_capture_price_est_before,
                        "pv_capture_price_after": pv_capture_price_est_after,
                        "wind_capture_price_obs_before": wind_capture_price_obs_before,
                        "wind_capture_price_est_before": wind_capture_price_est_before,
                        "wind_capture_price_est_after": wind_capture_price_est_after,
                        "wind_capture_price_before": wind_capture_price_est_before,
                        "wind_capture_price_after": wind_capture_price_est_after,
                        "days_spread_gt50_before": spread_days_before,
                        "days_spread_gt50_after": spread_days_after,
                        "avg_daily_spread_before": avg_spread_before,
                        "avg_daily_spread_after": avg_spread_after,
                        "low_residual_share_before": low_residual_share_before,
                        "low_residual_share_after": float(np.mean(low_residual_after)) if len(low_residual_after) else np.nan,
                        "sr_hours_share_before": sr_hours_share_before,
                        "sr_hours_share_after": sr_hours_share_after,
                        "ir_p10_before": ir_before,
                        "ir_p10_after": ir_after,
                        "turned_off_family_low_price": bool(turned_off_family["LOW_PRICE"]),
                        "turned_off_family_physical": bool(turned_off_family["PHYSICAL"]),
                        "turned_off_family_value_pv": bool(turned_off_family["VALUE_PV"]),
                        "turned_off_family_value_wind": bool(turned_off_family["VALUE_WIND"]),
                        "turned_off_family_any": turned_off_any,
                        "revenue_bess_price_taker": revenue,
                        "soc_min": float(sim["soc_min"]),
                        "soc_max": float(sim["soc_max"]),
                        "soc_start_mwh": float(sim["soc_start"]),
                        "soc_end_mwh": float(sim["soc_end"]),
                        "soc_end_target_mwh": float(cfg.soc_end_target_mwh),
                        "charge_max": float(sim["charge_max"]),
                        "discharge_max": float(sim["discharge_max"]),
                        "charge_sum_mwh": float(sim["charge_sum"]),
                        "discharge_sum_mwh": float(sim["discharge_sum"]),
                        "charge_hours": float(sim.get("charge_hours", 0.0)),
                        "cycles_assumed_per_day": float(cfg.max_cycles_per_day),
                        "cycles_realized_per_day": float(cycles_realized_per_day),
                        "simultaneous_charge_discharge_hours": float(sim["simultaneous_charge_discharge_hours"]),
                        "eta_roundtrip": float(cfg.eta_roundtrip),
                        "eta_charge": float(cfg.eta_charge),
                        "eta_discharge": float(cfg.eta_discharge),
                        "soc_boundary_mode": soc_boundary_mode,
                        "charge_vs_surplus_violation_hours": float(sim.get("charge_vs_surplus_violation_hours", 0.0)),
                        "proxy_quality_status": proxy_quality_status,
                        "proxy_quality_reasons": proxy_quality_reasons,
                        "output_schema_version": Q4_OUTPUT_SCHEMA_VERSION,
                    }
                )
            return pd.DataFrame(rows)

        current_power_grid = list(power_grid)
        current_duration_grid = list(duration_grid)
        frontier = _simulate_frontier_for_grid(current_power_grid, current_duration_grid, progress_base=0.10, progress_span=0.72)

        feasible = _objective_satisfied(frontier, objective, targets)
        zero_mask = (
            pd.to_numeric(frontier.get("required_bess_power_mw"), errors="coerce").fillna(np.inf).abs() <= 1e-9
        ) & (
            pd.to_numeric(frontier.get("required_bess_energy_mwh"), errors="coerce").fillna(np.inf).abs() <= 1e-9
        )
        baseline_rows = frontier[zero_mask].sort_values(["required_bess_power_mw", "required_bess_energy_mwh"])
        baseline_row = baseline_rows.iloc[0] if not baseline_rows.empty else None
        if baseline_row is None:
            baseline_meets = False
        elif objective == "FAR_TARGET":
            baseline_meets = bool(_safe_float(baseline_row.get("far_after"), -np.inf) >= targets["target_far"])
        elif objective == "SURPLUS_UNABS_TARGET":
            baseline_meets = bool(_safe_float(baseline_row.get("surplus_unabs_energy_after"), np.inf) <= targets["target_unabs"])
        elif objective == "LOW_PRICE_TARGET":
            baseline_meets = bool(
                (_safe_float(baseline_row.get("h_negative_est_after", baseline_row.get("h_negative_after")), np.inf) <= targets["h_negative_target"])
                and (_safe_float(baseline_row.get("h_below_5_est_after", baseline_row.get("h_below_5_after")), np.inf) <= targets["h_below_5_target"])
            )
        elif objective == "VALUE_TARGET":
            baseline_meets = bool(
                (_safe_float(baseline_row.get("capture_ratio_pv_after"), -np.inf) >= targets["capture_ratio_pv_target"])
                or (_safe_float(baseline_row.get("capture_ratio_wind_after"), -np.inf) >= targets["capture_ratio_wind_target"])
            )
        elif objective == "PHASE_TARGET":
            baseline_meets = bool(_safe_float(baseline_row.get("turned_off_family_any"), 0.0) > 0.0)
        else:
            baseline_meets = False

        peak_load_proxy = float(np.nanmax(pd.to_numeric(base.get("load_mw"), errors="coerce").to_numpy(dtype=float))) if "load_mw" in base.columns else np.nan
        if not np.isfinite(peak_load_proxy) or peak_load_proxy <= 0:
            peak_load_proxy = max(1.0, float(pv_capacity_proxy))
        grid_expand_peak_load_fraction_cap = float(selection.get("grid_expand_peak_load_fraction_cap", 1.0))
        grid_power_cap_mw = float(selection.get("grid_expand_power_cap_mw", peak_load_proxy * grid_expand_peak_load_fraction_cap))
        grid_duration_cap_h = float(selection.get("grid_expand_duration_cap_h", 24.0))
        max_expansions = int(selection.get("grid_expand_max_steps", 2))
        grid_power_cap_mw = max(grid_power_cap_mw, max(current_power_grid) if current_power_grid else 0.0)
        grid_duration_cap_h = max(grid_duration_cap_h, max(current_duration_grid) if current_duration_grid else 0.0)

        while feasible.empty and (not baseline_meets) and grid_expansions_used < max_expansions:
            p_new, d_new, changed = _expand_grid_once(
                current_power_grid,
                current_duration_grid,
                power_cap_mw=grid_power_cap_mw,
                duration_cap_h=grid_duration_cap_h,
            )
            if (not changed) or (p_new == current_power_grid and d_new == current_duration_grid):
                break
            grid_expansions_used += 1
            current_power_grid = p_new
            current_duration_grid = d_new
            frontier = _simulate_frontier_for_grid(
                current_power_grid,
                current_duration_grid,
                progress_base=0.12,
                progress_span=0.74,
            )
            feasible = _objective_satisfied(frontier, objective, targets)

        power_grid = current_power_grid
        duration_grid = current_duration_grid

        if frontier.empty:
            return ModuleResult(
                module_id="Q4",
                run_id=run_id,
                selection=selection,
                assumptions_used=assumptions_subset(assumptions_df, Q4_PARAMS),
                kpis={},
                tables={"Q4_sizing_summary": pd.DataFrame(), "Q4_bess_frontier": pd.DataFrame()},
                figures=[],
                narrative_md="Q4 impossible: aucune simulation produite.",
                checks=[{"status": "FAIL", "code": "Q4_EMPTY", "message": "Aucune simulation Q4."}],
                warnings=["Aucune simulation Q4."],
            )

        compute_time_sec = float(perf_counter() - t_start)
        frontier["engine_version"] = Q4_ENGINE_VERSION
        frontier["compute_time_sec"] = compute_time_sec
        frontier["cache_hit"] = False
        frontier["scenario_id"] = frontier["scenario_id"].astype(str).replace({"nan": "", "None": ""})
        frontier.loc[frontier["scenario_id"].str.strip().eq(""), "scenario_id"] = scenario_id_effective
        frontier["country"] = frontier["country"].astype(str).replace({"nan": "", "None": ""})
        frontier.loc[frontier["country"].str.strip().eq(""), "country"] = country
        frontier["year"] = pd.to_numeric(frontier["year"], errors="coerce").fillna(year).astype(int)
        # Aliases kept for downstream joins expecting frontier-style names.
        frontier["bess_power_mw"] = pd.to_numeric(frontier["required_bess_power_mw"], errors="coerce")
        frontier["duration_h"] = pd.to_numeric(frontier["required_bess_duration_h"], errors="coerce")
        frontier["bess_energy_mwh"] = pd.to_numeric(frontier["required_bess_energy_mwh"], errors="coerce")
        _save_cache(
            frontier=frontier,
            frontier_path=frontier_path,
            meta_path=meta_path,
            meta={
                "engine_version": Q4_ENGINE_VERSION,
                "compute_time_sec": compute_time_sec,
                "assumption_hash": assumption_hash,
                "data_signature": data_signature,
                "dispatch_mode": dispatch_mode,
                "country": country,
                "year": year,
                "grid_expansions_used": int(grid_expansions_used),
                "power_grid": [float(x) for x in power_grid],
                "duration_grid": [float(x) for x in duration_grid],
            },
        )
        if progress_callback:
            progress_callback("Aggregation et sauvegarde cache Q4", 0.92)

    # Keep stable frontier aliases for downstream joins, including cache-hit runs.
    frontier["bess_power_mw_test"] = pd.to_numeric(
        frontier.get("bess_power_mw_test", frontier.get("required_bess_power_mw")),
        errors="coerce",
    )
    frontier["bess_duration_h_test"] = pd.to_numeric(
        frontier.get("bess_duration_h_test", frontier.get("required_bess_duration_h")),
        errors="coerce",
    )
    frontier["bess_energy_mwh_test"] = pd.to_numeric(
        frontier.get("bess_energy_mwh_test", frontier.get("required_bess_energy_mwh")),
        errors="coerce",
    )
    frontier["bess_power_mw"] = pd.to_numeric(frontier.get("required_bess_power_mw"), errors="coerce")
    frontier["duration_h"] = pd.to_numeric(frontier.get("required_bess_duration_h"), errors="coerce")
    frontier["bess_energy_mwh"] = pd.to_numeric(frontier.get("required_bess_energy_mwh"), errors="coerce")
    dedupe_cols = [
        "country",
        "scenario_id",
        "year",
        "required_bess_power_mw",
        "required_bess_energy_mwh",
        "eta_roundtrip",
    ]
    existing_dedupe_cols = [c for c in dedupe_cols if c in frontier.columns]
    dropped_duplicates = 0
    if existing_dedupe_cols:
        dup_mask = frontier.duplicated(subset=existing_dedupe_cols, keep="first")
        dropped_duplicates = int(dup_mask.sum())
        if dropped_duplicates > 0:
            frontier = frontier.loc[~dup_mask].copy()
    default_cols: dict[str, Any] = {
        "soc_start_mwh": 0.0,
        "soc_end_mwh": 0.0,
        "soc_end_target_mwh": 0.0,
        "eta_roundtrip": eta_rt,
        "eta_charge": float(np.sqrt(eta_rt)),
        "eta_discharge": float(np.sqrt(eta_rt)),
        "simultaneous_charge_discharge_hours": 0.0,
        "far_before_trivial": False,
        "far_after_trivial": False,
        "soc_boundary_mode": soc_boundary_mode,
        "h_negative_before": 0.0,
        "h_negative_after": 0.0,
        "h_below_5_before": 0.0,
        "h_below_5_after": 0.0,
        "delta_h_negative": 0.0,
        "delta_h_below_5": 0.0,
        "capture_ratio_pv_before": np.nan,
        "capture_ratio_pv_after": np.nan,
        "capture_ratio_wind_before": np.nan,
        "capture_ratio_wind_after": np.nan,
        "delta_capture_ratio_pv": np.nan,
        "delta_capture_ratio_wind": np.nan,
        "turned_off_family_low_price": False,
        "turned_off_family_physical": False,
        "turned_off_family_value_pv": False,
        "turned_off_family_value_wind": False,
        "turned_off_family_any": False,
        "charge_vs_surplus_violation_hours": 0.0,
        "cycles_assumed_per_day": max_cycles_day,
        "cycles_realized_per_day": 0.0,
    }
    for col, default_val in default_cols.items():
        if col not in frontier.columns:
            frontier[col] = default_val

    tol = 1e-6
    if dropped_duplicates > 0:
        checks.append(
            {
                "status": "WARN",
                "code": "Q4_DUPLICATE_GRID_ROWS_REMOVED",
                "message": f"{dropped_duplicates} doublons de grille ont ete supprimes.",
            }
        )

    # Hard invariants
    if (frontier["soc_min"] < -tol).any():
        checks.append({"status": "FAIL", "code": "Q4_SOC_NEG", "message": "SOC negatif detecte."})
    if (frontier["soc_max"] - frontier["required_bess_energy_mwh"] > tol).any():
        checks.append({"status": "FAIL", "code": "Q4_SOC_ABOVE_EMAX", "message": "SOC > Emax detecte."})
    if (frontier["charge_max"] - frontier["required_bess_power_mw"] > tol).any():
        checks.append({"status": "FAIL", "code": "Q4_CHARGE_ABOVE_PMAX", "message": "Charge > Pmax detectee."})
    if (frontier["discharge_max"] - frontier["required_bess_power_mw"] > tol).any():
        checks.append({"status": "FAIL", "code": "Q4_DISCHARGE_ABOVE_PMAX", "message": "Decharge > Pmax detectee."})

    charge_sum = pd.to_numeric(frontier.get("charge_sum_mwh"), errors="coerce").fillna(0.0)
    discharge_sum = pd.to_numeric(frontier.get("discharge_sum_mwh"), errors="coerce").fillna(0.0)
    soc_start = pd.to_numeric(frontier.get("soc_start_mwh"), errors="coerce").fillna(0.0)
    soc_end = pd.to_numeric(frontier.get("soc_end_mwh"), errors="coerce").fillna(0.0)
    eta_rt_series = pd.to_numeric(frontier.get("eta_roundtrip"), errors="coerce").fillna(eta_rt).clip(lower=0.0)
    p_mw = pd.to_numeric(frontier.get("required_bess_power_mw"), errors="coerce").fillna(0.0)
    e_mwh = pd.to_numeric(frontier.get("required_bess_energy_mwh"), errors="coerce").fillna(0.0)

    no_charge_free_energy = (charge_sum.abs() <= tol) & (discharge_sum > tol)
    if bool(no_charge_free_energy.any()):
        checks.append(
            {
                "status": "FAIL",
                "code": "Q4_FREE_ENERGY_NO_CHARGE",
                "message": "Decharge strictement positive detectee sans charge (free energy).",
            }
        )

    balance_rhs = charge_sum * eta_rt_series + (soc_start - soc_end) + tol
    if bool((discharge_sum - balance_rhs > 0.0).any()):
        checks.append(
            {
                "status": "FAIL",
                "code": "Q4_ENERGY_BALANCE",
                "message": "Energie dechargee > energie chargee*eta + variation SOC.",
            }
        )

    if "simultaneous_charge_discharge_hours" in frontier.columns:
        simultaneous = pd.to_numeric(frontier["simultaneous_charge_discharge_hours"], errors="coerce").fillna(0.0)
        if bool((simultaneous > 0.0).any()):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q4_SIMULTANEOUS_CHARGE_DISCHARGE",
                    "message": "Charge et decharge simultanees detectees.",
                }
            )
    if "charge_vs_surplus_violation_hours" in frontier.columns:
        violations = pd.to_numeric(frontier["charge_vs_surplus_violation_hours"], errors="coerce").fillna(0.0)
        if bool((violations > 0.0).any()):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q4_CHARGE_EXCEEDS_SURPLUS",
                    "message": "Mode SURPLUS_FIRST: charge superieure au surplus disponible detectee.",
                }
            )

    zero_size = (e_mwh <= tol) | (p_mw <= tol)
    if bool(zero_size.any()):
        zero_violation = (
            (charge_sum[zero_size].abs() > tol)
            | (discharge_sum[zero_size].abs() > tol)
            | (soc_start[zero_size].abs() > tol)
            | (soc_end[zero_size].abs() > tol)
            | (pd.to_numeric(frontier.loc[zero_size, "soc_min"], errors="coerce").fillna(0.0).abs() > tol)
            | (pd.to_numeric(frontier.loc[zero_size, "soc_max"], errors="coerce").fillna(0.0).abs() > tol)
        )
        if bool(zero_violation.any()):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q4_ZERO_SIZE_NOT_ZERO_FLOW",
                    "message": "Cas P=0 ou E=0 non nul (charge/decharge/SOC) detecte.",
                }
            )
        metric_pairs = [
            ("h_negative_after", "h_negative_before"),
            ("h_below_5_after", "h_below_5_before"),
            ("capture_ratio_pv_after", "capture_ratio_pv_before"),
            ("capture_ratio_wind_after", "capture_ratio_wind_before"),
            ("surplus_unabs_energy_after", "surplus_unabs_energy_before"),
            ("far_after", "far_before"),
        ]
        mismatch = pd.Series(False, index=frontier.index)
        for after_col, before_col in metric_pairs:
            after_v = pd.to_numeric(frontier.get(after_col), errors="coerce")
            before_v = pd.to_numeric(frontier.get(before_col), errors="coerce")
            both = after_v.notna() & before_v.notna()
            mismatch = mismatch | (both & ((after_v - before_v).abs() > 1e-9))
        if bool((mismatch & zero_size).any()):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q4_ZERO_SIZE_AFTER_DIFFERS_FROM_BEFORE",
                    "message": "Invariance violee: avec P=0 ou E=0, les metriques after doivent egaler before.",
                }
            )

    if soc_boundary_mode == "ZERO_END":
        soc_end_tol = np.maximum(1.0, e_mwh.to_numpy(dtype=float)) * 1e-6
        soc_end_abs = np.abs(soc_end.to_numpy(dtype=float))
        if bool(np.any(soc_end_abs > soc_end_tol)):
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q4_SOC_END_BOUNDARY",
                    "message": "Contrainte SOC_end=0 violee (mode ZERO_END).",
                }
            )

    if dispatch_mode == "SURPLUS_FIRST":
        if (frontier["surplus_unabs_energy_after"] - frontier["surplus_unabs_energy_before"] > 1e-9).any():
            checks.append({"status": "FAIL", "code": "Q4_SURPLUS_INCREASE", "message": "Surplus non absorbe augmente en mode SURPLUS_FIRST."})
        for d in sorted(set(pd.to_numeric(frontier["required_bess_duration_h"], errors="coerce").dropna().tolist())):
            subset = frontier[pd.to_numeric(frontier["required_bess_duration_h"], errors="coerce") == float(d)].sort_values("required_bess_power_mw")
            if len(subset) >= 2 and (subset["far_after"].diff().dropna() < -1e-8).any():
                checks.append(
                    {
                        "status": "WARN",
                        "code": "Q4_FAR_NON_MONOTONIC",
                        "message": f"FAR diminue quand la puissance augmente (duration={d}h).",
                    }
                )
        # Pairwise dominance monotonicity: if (P2>=P1 and E2>=E1), stress should not worsen.
        if not frontier.empty:
            p = pd.to_numeric(frontier["required_bess_power_mw"], errors="coerce")
            e = pd.to_numeric(frontier["required_bess_energy_mwh"], errors="coerce")
            unabs = pd.to_numeric(frontier["surplus_unabs_energy_after"], errors="coerce")
            far_vals = pd.to_numeric(frontier["far_after"], errors="coerce")
            n_rows = len(frontier)
            surplus_dominance_fail = False
            far_dominance_fail = False
            for i in range(n_rows):
                if not (np.isfinite(p.iloc[i]) and np.isfinite(e.iloc[i]) and np.isfinite(unabs.iloc[i]) and np.isfinite(far_vals.iloc[i])):
                    continue
                dominating = (
                    (p >= p.iloc[i] - 1e-9)
                    & (e >= e.iloc[i] - 1e-9)
                    & np.isfinite(unabs)
                    & np.isfinite(far_vals)
                )
                if (unabs[dominating] > unabs.iloc[i] + 1e-9).any():
                    surplus_dominance_fail = True
                if (far_vals[dominating] < far_vals.iloc[i] - 1e-9).any():
                    far_dominance_fail = True
                if surplus_dominance_fail and far_dominance_fail:
                    break
            if surplus_dominance_fail:
                checks.append(
                    {
                        "status": "WARN",
                        "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
                        "message": "Surplus non absorbe non monotone en dominance (P,E).",
                    }
                )
            if far_dominance_fail:
                checks.append(
                    {
                        "status": "WARN",
                        "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
                        "message": "FAR non monotone en dominance (P,E).",
                    }
                )

    # Behavioral monotonic checks (hard constraints).
    duration_vals = sorted(set(pd.to_numeric(frontier["required_bess_duration_h"], errors="coerce").dropna().tolist()))
    hneg_monotonic_col = "h_negative_est_after" if "h_negative_est_after" in frontier.columns else "h_negative_after"
    for d in duration_vals:
        subset = frontier[pd.to_numeric(frontier["required_bess_duration_h"], errors="coerce") == float(d)].sort_values("required_bess_power_mw")
        if len(subset) < 2:
            continue
        unabs_after = pd.to_numeric(subset["surplus_unabs_energy_after"], errors="coerce")
        if (unabs_after.diff().dropna() > 1e-9).any():
            checks.append(
                {
                    "status": "WARN",
                    "code": "Q4_SURPLUS_UNABS_NON_MONOTONIC_POWER",
                    "message": f"surplus_unabs_energy_after doit etre non-croissant avec la puissance (duration={d}h).",
                }
            )
        hneg = pd.to_numeric(subset[hneg_monotonic_col], errors="coerce")
        if (hneg.diff().dropna() > 1e-9).any():
            checks.append(
                {
                    "status": "WARN",
                    "code": "Q4_HNEG_NON_MONOTONIC",
                    "message": f"h_negative augmente localement avec la puissance (duration={d}h).",
                }
            )

    power_vals = sorted(set(pd.to_numeric(frontier["required_bess_power_mw"], errors="coerce").dropna().tolist()))
    for p_val in power_vals:
        subset = frontier[pd.to_numeric(frontier["required_bess_power_mw"], errors="coerce") == float(p_val)].sort_values("required_bess_energy_mwh")
        if len(subset) < 2:
            continue
        unabs_after = pd.to_numeric(subset["surplus_unabs_energy_after"], errors="coerce")
        hneg_after = pd.to_numeric(subset[hneg_monotonic_col], errors="coerce")
        if (unabs_after.diff().dropna() > 1e-9).any():
            checks.append(
                {
                    "status": "WARN",
                    "code": "Q4_SURPLUS_UNABS_NON_MONOTONIC_ENERGY",
                    "message": f"surplus_unabs_energy_after doit etre non-croissant avec l'energie (power={p_val}MW).",
                }
            )
        if (hneg_after.diff().dropna() > 1e-9).any():
            checks.append(
                {
                    "status": "WARN",
                    "code": "Q4_HNEG_NON_MONOTONIC_ENERGY",
                    "message": f"h_negative_after doit etre non-croissant avec l'energie (power={p_val}MW).",
                }
            )

    # Efficient frontier on (power, energy, surplus_unabs_energy_after): keep non-dominated points.
    frontier["on_efficient_frontier"] = True
    p_ser = pd.to_numeric(frontier.get("required_bess_power_mw"), errors="coerce")
    e_ser = pd.to_numeric(frontier.get("required_bess_energy_mwh"), errors="coerce")
    u_ser = pd.to_numeric(frontier.get("surplus_unabs_energy_after"), errors="coerce")
    for i in frontier.index:
        pi = _safe_float(p_ser.loc[i], np.nan)
        ei = _safe_float(e_ser.loc[i], np.nan)
        ui = _safe_float(u_ser.loc[i], np.nan)
        if not (np.isfinite(pi) and np.isfinite(ei) and np.isfinite(ui)):
            frontier.at[i, "on_efficient_frontier"] = False
            continue
        dominates_i = (
            (p_ser <= pi + 1e-9)
            & (e_ser <= ei + 1e-9)
            & (u_ser <= ui + 1e-9)
            & (
                (p_ser < pi - 1e-9)
                | (e_ser < ei - 1e-9)
                | (u_ser < ui - 1e-9)
            )
        )
        dominates_i.loc[i] = False
        if bool(dominates_i.fillna(False).any()):
            frontier.at[i, "on_efficient_frontier"] = False

    hneg_before_max = _safe_float(pd.to_numeric(frontier.get("h_negative_est_before", frontier.get("h_negative_before")), errors="coerce").max(), np.nan)
    if np.isfinite(hneg_before_max) and hneg_before_max > 0:
        improved = (pd.to_numeric(frontier.get("delta_h_negative"), errors="coerce") < 0.0).fillna(False)
        if not bool(improved.any()):
            checks.append(
                {
                    "status": "WARN",
                    "code": "Q4_BESS_INEFFECTIVE",
                    "message": "h_negative>0 mais aucun point de frontier ne reduit h_negative.",
                }
            )
    hneg_after_ser = pd.to_numeric(frontier.get("h_negative_est_after", frontier.get("h_negative_after")), errors="coerce")
    hbelow_after_ser = pd.to_numeric(frontier.get("h_below_5_est_after", frontier.get("h_below_5_after")), errors="coerce")
    bad_order = hbelow_after_ser < hneg_after_ser
    if bool(bad_order.fillna(False).any()):
        checks.append(
            {
                "status": "FAIL",
                "code": "Q4_HBELOW_LT_HNEG",
                "message": "h_below_5_after doit etre >= h_negative_after sur toute la frontier.",
            }
        )
    charge_hours_ser = (
        pd.to_numeric(frontier["charge_hours"], errors="coerce").fillna(0.0)
        if "charge_hours" in frontier.columns
        else pd.Series(0.0, index=frontier.index, dtype=float)
    )
    delta_hneg_est_ser = (
        pd.to_numeric(frontier["delta_h_negative_est"], errors="coerce")
        if "delta_h_negative_est" in frontier.columns
        else pd.to_numeric(frontier.get("delta_h_negative", pd.Series(np.nan, index=frontier.index)), errors="coerce")
    )
    delta_h5_est_ser = (
        pd.to_numeric(frontier["delta_h_below_5_est"], errors="coerce")
        if "delta_h_below_5_est" in frontier.columns
        else pd.to_numeric(frontier.get("delta_h_below_5", pd.Series(np.nan, index=frontier.index)), errors="coerce")
    )
    over_hneg_bound = (-delta_hneg_est_ser) > (charge_hours_ser + 5.0)
    if bool(over_hneg_bound.fillna(False).any()):
        checks.append(
            {
                "status": "FAIL",
                "code": "Q4_DELTA_HNEG_ABOVE_CHARGE_HOURS",
                "message": "Reduction h_negative_est ne peut pas depasser charge_hours (+tol).",
            }
        )
    over_h5_bound = (-delta_h5_est_ser) > (charge_hours_ser + 5.0)
    if bool(over_h5_bound.fillna(False).any()):
        checks.append(
            {
                "status": "FAIL",
                "code": "Q4_DELTA_H5_ABOVE_CHARGE_HOURS",
                "message": "Reduction h_below_5_est ne peut pas depasser charge_hours (+tol).",
            }
        )
    total_charge_mwh = pd.to_numeric(frontier.get("charge_sum_mwh", pd.Series(np.nan, index=frontier.index)), errors="coerce")
    total_discharge_mwh = pd.to_numeric(frontier.get("discharge_sum_mwh", pd.Series(np.nan, index=frontier.index)), errors="coerce")
    eta_rt_ser = pd.to_numeric(frontier.get("eta_roundtrip", pd.Series(0.0, index=frontier.index)), errors="coerce").fillna(0.0)
    bad_eta = total_discharge_mwh > (total_charge_mwh * eta_rt_ser + 1e-6)
    if bool(bad_eta.fillna(False).any()):
        checks.append(
            {
                "status": "FAIL",
                "code": "Q4_ENERGY_SANITY_ETA_RT",
                "message": "total_discharge_mwh doit rester <= total_charge_mwh * eta_roundtrip (+tol).",
            }
        )

    # Objective satisfaction and selection rule.
    feasible = _objective_satisfied(frontier, objective, targets)
    zero_mask = (p_mw.abs() <= tol) & (e_mwh.abs() <= tol)
    baseline_rows = frontier[zero_mask].sort_values(["required_bess_power_mw", "required_bess_energy_mwh"])
    baseline_row = baseline_rows.iloc[0] if not baseline_rows.empty else None
    base_far_val = _safe_float(frontier.get("far_before", pd.Series(dtype=float)).iloc[0], np.nan) if ("far_before" in frontier.columns and not frontier.empty) else np.nan

    objective_met = False
    objective_reason = ""
    objective_recommendation = ""
    not_sensitive = False
    objective_direction = "higher_is_better"
    if objective == "FAR_TARGET":
        objective_target_value = targets["target_far"]
        objective_direction = "higher_is_better"
    elif objective == "SURPLUS_UNABS_TARGET":
        objective_target_value = targets["target_unabs"]
        objective_direction = "lower_is_better"
    elif objective == "LOW_PRICE_TARGET":
        objective_target_value = targets["h_negative_target"]
        objective_direction = "lower_is_better"
    elif objective == "VALUE_TARGET":
        objective_target_value = min(targets["capture_ratio_pv_target"], targets["capture_ratio_wind_target"])
        objective_direction = "higher_is_better"
    else:
        objective_target_value = 1.0
        objective_direction = "higher_is_better"

    if baseline_row is not None:
        nonzero_rows = frontier[~zero_mask].copy()
        has_effect = False
        for mcol in [
            "far_after",
            "surplus_unabs_energy_after",
            "h_negative_after",
            "h_below_5_after",
            "capture_ratio_pv_after",
            "capture_ratio_wind_after",
        ]:
            if mcol not in frontier.columns:
                continue
            base_val = _safe_float(baseline_row.get(mcol), np.nan)
            vals = pd.to_numeric(nonzero_rows.get(mcol), errors="coerce")
            if vals.empty:
                continue
            if np.isfinite(base_val):
                if bool((vals - base_val).abs().fillna(0.0).gt(1e-9).any()):
                    has_effect = True
                    break
            elif vals.notna().any():
                has_effect = True
                break
        not_sensitive = bool(nonzero_rows.empty or (not has_effect))

        if objective == "FAR_TARGET":
            baseline_met = bool(_safe_float(baseline_row.get("far_after"), -np.inf) >= targets["target_far"])
        elif objective == "SURPLUS_UNABS_TARGET":
            baseline_met = bool(_safe_float(baseline_row.get("surplus_unabs_energy_after"), np.inf) <= targets["target_unabs"])
        elif objective == "LOW_PRICE_TARGET":
            baseline_met = bool(
                (_safe_float(baseline_row.get("h_negative_est_after", baseline_row.get("h_negative_after")), np.inf) <= targets["h_negative_target"])
                and (_safe_float(baseline_row.get("h_below_5_est_after", baseline_row.get("h_below_5_after")), np.inf) <= targets["h_below_5_target"])
            )
        elif objective == "VALUE_TARGET":
            baseline_met = bool(
                (_safe_float(baseline_row.get("capture_ratio_pv_after"), -np.inf) >= targets["capture_ratio_pv_target"])
                or (_safe_float(baseline_row.get("capture_ratio_wind_after"), -np.inf) >= targets["capture_ratio_wind_target"])
            )
        else:
            baseline_met = bool(_safe_float(baseline_row.get("turned_off_family_any"), 0.0) > 0.0)
        if baseline_met:
            objective_met = True
            objective_reason = "already_met"
            best = baseline_row
        elif not_sensitive:
            objective_met = False
            objective_reason = "not_sensitive"
            objective_recommendation = "not_sensitive_to_bess"
            best = baseline_row
            checks.append(
                {
                    "status": "WARN",
                    "code": "Q4_NOT_SENSITIVE",
                    "message": "Les configurations BESS testees ne modifient pas les metriques cibles; required=0.",
                }
            )
        else:
            best = None
    else:
        best = None

    if (not objective_met) and (not not_sensitive):
        if not feasible.empty:
            objective_met = True
            objective_reason = "met_after_grid_expansion" if grid_expansions_used > 0 else "met_in_grid"
            best = feasible.iloc[0]
        else:
            if objective == "FAR_TARGET":
                best = frontier.sort_values(["far_after", "required_bess_power_mw", "required_bess_energy_mwh"], ascending=[False, True, True]).iloc[0]
                baseline_metric = base_far_val
                best_metric = _safe_float(best.get("far_after"), np.nan)
                improvement = best_metric - baseline_metric if np.isfinite(best_metric) and np.isfinite(baseline_metric) else np.nan
            elif objective == "SURPLUS_UNABS_TARGET":
                best = frontier.sort_values(["surplus_unabs_energy_after", "required_bess_power_mw", "required_bess_energy_mwh"]).iloc[0]
                baseline_metric = _safe_float(baseline_row.get("surplus_unabs_energy_after"), np.nan) if baseline_row is not None else np.nan
                best_metric = _safe_float(best.get("surplus_unabs_energy_after"), np.nan)
                improvement = baseline_metric - best_metric if np.isfinite(best_metric) and np.isfinite(baseline_metric) else np.nan
            elif objective == "LOW_PRICE_TARGET":
                hneg_sort_col = "h_negative_est_after" if "h_negative_est_after" in frontier.columns else "h_negative_after"
                hlow_sort_col = "h_below_5_est_after" if "h_below_5_est_after" in frontier.columns else "h_below_5_after"
                best = frontier.sort_values(
                    [hneg_sort_col, hlow_sort_col, "required_bess_power_mw", "required_bess_energy_mwh"]
                ).iloc[0]
                baseline_metric = _safe_float(
                    baseline_row.get("h_negative_est_after", baseline_row.get("h_negative_after")),
                    np.nan,
                ) if baseline_row is not None else np.nan
                best_metric = _safe_float(best.get("h_negative_est_after", best.get("h_negative_after")), np.nan)
                improvement = baseline_metric - best_metric if np.isfinite(best_metric) and np.isfinite(baseline_metric) else np.nan
            elif objective == "VALUE_TARGET":
                best = frontier.sort_values(
                    ["capture_ratio_pv_after", "capture_ratio_wind_after", "required_bess_power_mw", "required_bess_energy_mwh"],
                    ascending=[False, False, True, True],
                ).iloc[0]
                baseline_metric = _safe_float(baseline_row.get("capture_ratio_pv_after"), np.nan) if baseline_row is not None else np.nan
                best_metric = _safe_float(best.get("capture_ratio_pv_after"), np.nan)
                improvement = best_metric - baseline_metric if np.isfinite(best_metric) and np.isfinite(baseline_metric) else np.nan
            else:
                best = frontier.sort_values(
                    ["turned_off_family_any", "required_bess_power_mw", "required_bess_energy_mwh"],
                    ascending=[False, True, True],
                ).iloc[0]
                baseline_metric = _safe_float(baseline_row.get("turned_off_family_any"), np.nan) if baseline_row is not None else np.nan
                best_metric = _safe_float(best.get("turned_off_family_any"), np.nan)
                improvement = best_metric - baseline_metric if np.isfinite(best_metric) and np.isfinite(baseline_metric) else np.nan

            p_max_grid = float(p_mw.max()) if len(p_mw) else 0.0
            d_max_grid = float(pd.to_numeric(frontier["required_bess_duration_h"], errors="coerce").max()) if len(frontier) else 0.0
            on_boundary = bool(
                abs(_safe_float(best.get("required_bess_power_mw"), 0.0) - p_max_grid) <= 1e-9
                or abs(_safe_float(best.get("required_bess_duration_h"), 0.0) - d_max_grid) <= 1e-9
            )
            if np.isfinite(improvement) and improvement <= 1e-6:
                objective_reason = "unreachable_under_policy"
            elif on_boundary:
                objective_reason = "grid_too_small"
            else:
                objective_reason = "unreachable_under_policy"

            if objective_reason == "grid_too_small":
                rec_p = max(p_max_grid + 1.0, p_max_grid * 1.5)
                rec_d = max(d_max_grid + 0.5, d_max_grid * 1.5)
                objective_recommendation = f"expand_grid_to_power_mw>={rec_p:.1f};duration_h>={rec_d:.1f}"
                warnings.append(
                    f"Objectif non atteint: grille trop petite (raison=grid_too_small). "
                    f"Recommendation: power >= {rec_p:.1f} MW, duration >= {rec_d:.1f} h."
                )
                checks.append(
                    {
                        "status": "WARN",
                        "code": "Q4_OBJECTIVE_NOT_REACHED_GRID",
                        "message": "Objectif non atteint sur la grille courante; augmenter les bornes de recherche.",
                    }
                )
            else:
                objective_recommendation = "review_policy_constraints_or_targets"
                warnings.append("Objectif non atteint: contraintes de policy/dispatch limitantes (raison=unreachable_under_policy).")
                checks.append(
                    {
                        "status": "WARN",
                        "code": "Q4_OBJECTIVE_UNREACHABLE",
                        "message": "Objectif non atteint sous les contraintes de policy actuelles.",
                    }
                )

    objective_value_after = np.nan
    if best is not None:
        if objective == "FAR_TARGET":
            objective_value_after = _safe_float(best.get("far_after"), np.nan)
        elif objective == "SURPLUS_UNABS_TARGET":
            objective_value_after = _safe_float(best.get("surplus_unabs_energy_after"), np.nan)
        elif objective == "LOW_PRICE_TARGET":
            objective_value_after = _safe_float(best.get("h_negative_est_after", best.get("h_negative_after")), np.nan)
        elif objective == "VALUE_TARGET":
            objective_value_after = _safe_float(best.get("capture_ratio_pv_after"), np.nan)
        else:
            objective_value_after = _safe_float(best.get("turned_off_family_any"), np.nan)

    if np.isfinite(objective_value_after) and np.isfinite(_safe_float(objective_target_value, np.nan)):
        if objective_direction == "lower_is_better":
            objective_met = bool(objective_value_after <= float(objective_target_value) + 1e-9)
        elif objective_direction == "higher_is_better":
            objective_met = bool(objective_value_after >= float(objective_target_value) - 1e-9)
    if (not objective_met) and objective_reason in {"already_met", "met_in_grid", "met_after_grid_expansion"}:
        objective_reason = "not_achievable"

    objective_not_reached = not objective_met

    summary = pd.DataFrame(
        [
            {
                "scenario_id": scenario_id_effective,
                "country": country,
                "year": year,
                **best.to_dict(),
                "objective_met": objective_met,
                "objective_reason": objective_reason,
                "objective_not_reached": objective_not_reached,
                "status": (
                    "already_ok"
                    if objective_reason == "already_met"
                    else ("not_sensitive" if objective_reason == "not_sensitive" else ("ok" if objective_met else "not_achievable"))
                ),
                "reason": objective_reason,
                "objective_target_value": objective_target_value,
                "objective_direction": objective_direction,
                "objective_value_after": objective_value_after,
                "objective_recommendation": objective_recommendation,
                "pv_capacity_proxy_mw": float(pv_capacity_proxy),
                "power_grid_max_mw": float(pd.to_numeric(frontier["required_bess_power_mw"], errors="coerce").max()) if not frontier.empty else np.nan,
                "duration_grid_max_h": float(pd.to_numeric(frontier["required_bess_duration_h"], errors="coerce").max()) if not frontier.empty else np.nan,
                "grid_expansions_used": int(grid_expansions_used),
                "notes_quality": "ok",
                "proxy_quality_status": proxy_quality_status,
                "proxy_quality_reasons": proxy_quality_reasons,
                "output_schema_version": Q4_OUTPUT_SCHEMA_VERSION,
            }
        ]
    )
    summary["bess_power_mw"] = pd.to_numeric(summary["required_bess_power_mw"], errors="coerce")
    summary["duration_h"] = pd.to_numeric(summary["required_bess_duration_h"], errors="coerce")
    summary["bess_energy_mwh"] = pd.to_numeric(summary["required_bess_energy_mwh"], errors="coerce")

    if dispatch_mode == "PRICE_ARBITRAGE_SIMPLE" and float(summary["revenue_bess_price_taker"].iloc[0]) < 0:
        warnings.append("Revenu d'arbitrage annuel negatif: spread insuffisant ou regle de dispatch trop simple.")
    if float(summary["required_bess_duration_h"].iloc[0]) > 8.0:
        warnings.append("Besoin de stockage long (>8h): batterie courte potentiellement insuffisante.")
    for col in ["far_before", "far_after"]:
        vals_frontier = pd.to_numeric(frontier.get(col), errors="coerce")
        val = _safe_float(summary[col].iloc[0], np.nan)
        if vals_frontier.isna().any() or (vals_frontier < 0.0).any() or (vals_frontier > 1.0).any() or (not np.isfinite(val)) or val < 0.0 or val > 1.0:
            checks.append(
                {
                    "status": "FAIL",
                    "code": "Q4_SUMMARY_FAR_INVALID",
                    "message": f"{col} invalide dans Q4_sizing_summary.",
                }
            )
    key_cols = ["scenario_id", "country", "year"]
    for col in key_cols:
        if col not in frontier.columns:
            frontier[col] = scenario_id_effective if col == "scenario_id" else (country if col == "country" else year)
    frontier["scenario_id"] = frontier["scenario_id"].astype(str).replace({"nan": "", "None": ""})
    frontier.loc[frontier["scenario_id"].str.strip().eq(""), "scenario_id"] = scenario_id_effective
    frontier["country"] = frontier["country"].astype(str).replace({"nan": "", "None": ""})
    frontier.loc[frontier["country"].str.strip().eq(""), "country"] = country
    frontier["year"] = pd.to_numeric(frontier["year"], errors="coerce").fillna(year).astype(int)
    if frontier[key_cols].isna().any().any():
        checks.append({"status": "FAIL", "code": "Q4_FRONTIER_KEY_MISSING", "message": "Cles manquantes dans Q4_bess_frontier."})

    physics_fail_codes = {
        "Q4_SOC_NEG",
        "Q4_SOC_ABOVE_EMAX",
        "Q4_CHARGE_ABOVE_PMAX",
        "Q4_DISCHARGE_ABOVE_PMAX",
        "Q4_FREE_ENERGY_NO_CHARGE",
        "Q4_ENERGY_BALANCE",
        "Q4_SIMULTANEOUS_CHARGE_DISCHARGE",
        "Q4_CHARGE_EXCEEDS_SURPLUS",
        "Q4_ZERO_SIZE_NOT_ZERO_FLOW",
        "Q4_ZERO_SIZE_AFTER_DIFFERS_FROM_BEFORE",
        "Q4_SOC_END_BOUNDARY",
    }
    monotonic_fail_codes = {
        "Q4_SURPLUS_INCREASE",
        "Q4_FAR_NON_MONOTONIC",
        "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
        "Q4_FAR_NON_MONOTONIC_DOMINANCE",
        "Q4_SURPLUS_UNABS_NON_MONOTONIC_POWER",
        "Q4_HNEG_NON_MONOTONIC",
        "Q4_SURPLUS_UNABS_NON_MONOTONIC_ENERGY",
        "Q4_HNEG_NON_MONOTONIC_ENERGY",
    }
    has_physics_fail = any(
        str(c.get("status", "")).upper() == "FAIL" and str(c.get("code", "")).upper() in physics_fail_codes
        for c in checks
    )
    has_monotonic_fail = any(
        str(c.get("status", "")).upper() == "FAIL" and str(c.get("code", "")).upper() in monotonic_fail_codes
        for c in checks
    )
    checks.append(
        {
            "status": "FAIL" if has_physics_fail else "PASS",
            "code": "TEST_Q4_001",
            "message": "Invariants physiques batterie (SOC, puissance, energie) valides." if not has_physics_fail else "Violation d'un invariant physique batterie.",
        }
    )
    checks.append(
        {
            "status": "FAIL" if has_monotonic_fail else "PASS",
            "code": "TEST_Q4_002",
            "message": "Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus)." if not has_monotonic_fail else "Violation de monotonicite sur la frontier BESS.",
        }
    )

    # Reporting semantics: frontier grid columns are test sizes, not "required" values.
    frontier_out = frontier.copy()
    if "bess_power_mw_test" not in frontier_out.columns:
        frontier_out["bess_power_mw_test"] = pd.to_numeric(frontier_out.get("required_bess_power_mw"), errors="coerce")
    if "bess_energy_mwh_test" not in frontier_out.columns:
        frontier_out["bess_energy_mwh_test"] = pd.to_numeric(frontier_out.get("required_bess_energy_mwh"), errors="coerce")
    if "bess_duration_h_test" not in frontier_out.columns:
        frontier_out["bess_duration_h_test"] = pd.to_numeric(frontier_out.get("required_bess_duration_h"), errors="coerce")
    frontier_out = frontier_out.drop(
        columns=[c for c in ["required_bess_power_mw", "required_bess_energy_mwh", "required_bess_duration_h"] if c in frontier_out.columns]
    )

    monotonicity_check_flag = "PASS" if not has_monotonic_fail else "WARN"
    physics_check_flag = "PASS" if not has_physics_fail else "FAIL"
    q4_bess_sizing_curve = pd.DataFrame(
        {
            "country": frontier_out.get("country"),
            "scenario_id": frontier_out.get("scenario_id"),
            "year": pd.to_numeric(frontier_out.get("year"), errors="coerce"),
            "bess_power_gw": pd.to_numeric(frontier_out.get("bess_power_mw_test"), errors="coerce") / 1000.0,
            "bess_energy_gwh": pd.to_numeric(frontier_out.get("bess_energy_mwh_test"), errors="coerce") / 1000.0,
            "cycles_assumed_per_day": pd.to_numeric(frontier_out.get("cycles_assumed_per_day"), errors="coerce"),
            "cycles_realized_per_day": pd.to_numeric(frontier_out.get("cycles_realized_per_day"), errors="coerce"),
            "eta_roundtrip": pd.to_numeric(frontier_out.get("eta_roundtrip"), errors="coerce"),
            "far_energy_after": pd.to_numeric(frontier_out.get("far_after"), errors="coerce"),
            "surplus_unabsorbed_twh_after": pd.to_numeric(frontier_out.get("surplus_unabs_energy_after"), errors="coerce"),
            "h_negative_proxy_after": pd.to_numeric(frontier_out.get("h_negative_proxy_after", frontier_out.get("h_negative_after")), errors="coerce"),
            "h_negative_reducible_upper_bound": pd.to_numeric(frontier_out.get("h_negative_reducible_upper_bound"), errors="coerce"),
            "h_negative_upper_bound_after": pd.to_numeric(frontier_out.get("h_negative_upper_bound_after"), errors="coerce"),
            "on_efficient_frontier": frontier_out.get("on_efficient_frontier"),
            "monotonicity_check_flag": monotonicity_check_flag,
            "physics_check_flag": physics_check_flag,
            "notes": f"dispatch_mode={dispatch_mode}; objective={objective}",
        }
    )
    has_fail_checks = any(str(c.get("status", "")).upper() == "FAIL" for c in checks)
    has_warn_checks = any(str(c.get("status", "")).upper() == "WARN" for c in checks)
    module_quality_status = "FAIL" if has_fail_checks else ("WARN" if has_warn_checks else "PASS")
    q4_quality_summary = pd.DataFrame(
        [
            {
                "module_id": "Q4",
                "country": country,
                "year": year,
                "scenario_id": scenario_id_effective,
                "quality_status": module_quality_status,
                "proxy_quality_status": proxy_quality_status,
                "proxy_quality_reasons": proxy_quality_reasons,
                "output_schema_version": Q4_OUTPUT_SCHEMA_VERSION,
            }
        ]
    )

    if cache_hit:
        checks.append({"status": "INFO", "code": "Q4_CACHE_HIT", "message": "Resultat charge depuis cache persistant Q4."})
    if not checks:
        checks.append({"status": "PASS", "code": "Q4_PASS", "message": "Q4 invariants et checks passes."})

    total_time = float(perf_counter() - t_start)
    if progress_callback:
        progress_callback("Q4 termine", 1.0)

    narrative = (
        "Q4 estime un ordre de grandeur BESS sur historique avec dispatch explicite. "
        "Le moteur impose conservation d'energie (pas de free energy) et contrainte SOC de fin (ZERO_END par defaut). "
        "Les resultats doivent etre lus comme benchmark mecaniste (price-taker), pas comme optimisation de marche."
    )

    return ModuleResult(
        module_id="Q4",
        run_id=run_id,
        selection={**selection, "dispatch_mode": dispatch_mode},
        assumptions_used=assumptions_subset(assumptions_df, Q4_PARAMS),
        kpis={
            "best_far_after": float(summary["far_after"].iloc[0]),
            "objective": objective,
            "objective_met": bool(summary["objective_met"].iloc[0]),
            "objective_reason": str(summary["objective_reason"].iloc[0]),
            "objective_not_reached": bool(summary["objective_not_reached"].iloc[0]),
            "compute_time_sec": total_time,
            "cache_hit": cache_hit,
            "engine_version": Q4_ENGINE_VERSION,
            "assumption_hash": assumption_hash,
        },
        tables={
            "Q4_sizing_summary": summary,
            "Q4_bess_frontier": frontier_out,
            "q4_bess_sizing_curve": q4_bess_sizing_curve,
            "q4_quality_summary": q4_quality_summary,
        },
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
        mode=str(selection.get("mode", "HIST")).upper(),
        scenario_id=scenario_id_effective,
        horizon_year=selection.get("horizon_year"),
    )
