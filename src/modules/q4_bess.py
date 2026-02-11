"""Q4 - BESS sizing and impact simulation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any, Callable

import numpy as np
import pandas as pd

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

Q4_ENGINE_VERSION = "v2.2.1"
Q4_CACHE_BASE = Path("data/cache/q4")


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

    low_mask, high_mask = masks_by_duration[float(cfg.duration_h)]

    soc = float(cfg.soc_start_mwh)
    soc_start = float(cfg.soc_start_mwh)
    soc_target = float(cfg.soc_end_target_mwh)
    eta_c = float(cfg.eta_charge)
    eta_d = float(cfg.eta_discharge)
    pmax = float(cfg.power_mw)
    emax = float(cfg.energy_mwh)
    max_daily_throughput = max(0.0, float(cfg.max_cycles_per_day)) * emax
    tol = 1e-12

    for start, end in day_ranges:
        daily_charge = 0.0
        daily_discharge = 0.0

        for i in range(start, end):
            desired_charge = 0.0
            desired_discharge = 0.0
            boundary_forced_discharge = False

            if dispatch_mode == "SURPLUS_FIRST":
                # Conservative stress-absorption mode:
                # charge only on physical surplus (NRL<0), discharge only when NRL>0.
                if nrl[i] < 0.0 and surplus_unabs[i] > 0.0:
                    desired_charge = min(surplus_unabs[i], abs(nrl[i]))
                if nrl[i] > 0.0:
                    desired_discharge = min(pmax, nrl[i])
            elif dispatch_mode == "PRICE_ARBITRAGE_SIMPLE":
                if low_mask[i]:
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
        "soc_start": soc_start,
        "soc_end": float(soc),
        "simultaneous_charge_discharge_hours": float(np.sum((charge > tol) & (discharge > tol))),
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


def _objective_satisfied(frontier: pd.DataFrame, objective: str, target_far: float, target_unabs: float) -> pd.DataFrame:
    if frontier.empty:
        return pd.DataFrame()
    if objective == "FAR_TARGET":
        return frontier[frontier["far_after"] >= target_far].sort_values(
            ["required_bess_power_mw", "required_bess_energy_mwh"]
        )
    return frontier[frontier["surplus_unabs_energy_after"] <= target_unabs].sort_values(
        ["required_bess_power_mw", "required_bess_energy_mwh"]
    )


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
    eta_rt = float(params.get("bess_eta_roundtrip", 0.88))
    soc_init = float(params.get("bess_soc_init_frac", 0.5))
    soc_boundary_mode = _resolve_soc_boundary_mode(selection)
    max_cycles_day = float(params.get("bess_max_cycles_per_day", 1.0))
    target_far = float(params.get("target_far", 0.95))
    target_unabs = float(params.get("target_surplus_unabs_energy_twh", 0.0))

    objective = str(selection.get("objective", "FAR_TARGET")).upper()
    if objective not in {"FAR_TARGET", "SURPLUS_UNABS_TARGET"}:
        objective = "FAR_TARGET"

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

    frontier: pd.DataFrame
    cache_hit = False
    grid_expansions_used = 0
    grid_power_cap_mw = np.nan
    grid_duration_cap_h = np.nan
    cached_frontier, cached_meta = (None, {})
    if not force_recompute:
        cached_frontier, cached_meta = _load_cache(frontier_path, meta_path)
    if cached_frontier is not None:
        frontier = cached_frontier.copy()
        cache_hit = True
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
        h_negative_before = int(np.nansum(np.where(np.isfinite(price), price < 0.0, 0)))
        h_below_5_before = int(np.nansum(np.where(np.isfinite(price), price <= 5.0, 0)))
        day_ranges = _day_slices(base.index)

        if progress_callback:
            progress_callback("Pre-calcul des structures journalieres", 0.10)

        masks_by_duration = _precompute_low_high_masks(price, day_ranges, duration_grid)

        def _simulate_frontier_for_grid(power_vals: list[float], duration_vals: list[float], progress_base: float, progress_span: float) -> pd.DataFrame:
            missing_duration_masks = [float(d) for d in duration_vals if float(d) not in masks_by_duration]
            if missing_duration_masks:
                masks_by_duration.update(_precompute_low_high_masks(price, day_ranges, missing_duration_masks))

            rows: list[dict[str, Any]] = []
            total_scenarios = max(1, len(power_vals) * len(duration_vals))
            scenario_idx = 0
            for p in power_vals:
                for d in duration_vals:
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
                    revenue = float(sim["revenue"])

                    if dispatch_mode == "PV_COLOCATED":
                        pv_to_grid = np.maximum(0.0, pv - sim["charge"])
                        pv_shifted = sim["discharge"]
                        delivered = pv_to_grid + pv_shifted
                        den = float(np.sum(delivered))
                        pv_after = np.nan if den <= 0 else float(np.sum(np.where(np.isfinite(price), price, 0.0) * delivered) / den)
                    else:
                        pv_after = pv_before
                    capture_ratio_pv_after = (pv_after / baseload_before) if np.isfinite(pv_after) and np.isfinite(baseload_before) and abs(baseload_before) > 1e-12 else np.nan

                    rows.append(
                        {
                            "scenario_id": scenario_id_effective,
                            "country": country,
                            "year": year,
                            "dispatch_mode": dispatch_mode,
                            "objective": objective,
                            "required_bess_power_mw": cfg.power_mw,
                            "required_bess_energy_mwh": cfg.energy_mwh,
                            "required_bess_duration_h": cfg.duration_h,
                            "far_before": base_far,
                            "far_after": far_after,
                            "far_before_trivial": far_before_trivial,
                            "far_after_trivial": far_after_trivial,
                            "h_negative_before": h_negative_before,
                            "h_negative_after": h_negative_before,
                            "h_below_5_before": h_below_5_before,
                            "h_below_5_after": h_below_5_before,
                            "baseload_price_before": baseload_before,
                            "capture_ratio_pv_before": capture_ratio_pv_before,
                            "capture_ratio_pv_after": capture_ratio_pv_after,
                            "surplus_unabs_energy_before": unabs_before_twh,
                            "surplus_unabs_energy_after": unabs_after_twh,
                            "pv_capture_price_before": pv_before,
                            "pv_capture_price_after": pv_after,
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
                            "simultaneous_charge_discharge_hours": float(sim["simultaneous_charge_discharge_hours"]),
                            "eta_roundtrip": float(cfg.eta_roundtrip),
                            "eta_charge": float(cfg.eta_charge),
                            "eta_discharge": float(cfg.eta_discharge),
                            "soc_boundary_mode": soc_boundary_mode,
                        }
                    )
            return pd.DataFrame(rows)

        current_power_grid = list(power_grid)
        current_duration_grid = list(duration_grid)
        frontier = _simulate_frontier_for_grid(current_power_grid, current_duration_grid, progress_base=0.10, progress_span=0.72)

        feasible = _objective_satisfied(frontier, objective, target_far, target_unabs)
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
            baseline_meets = bool(_safe_float(baseline_row.get("far_after"), -np.inf) >= target_far)
        else:
            baseline_meets = bool(_safe_float(baseline_row.get("surplus_unabs_energy_after"), np.inf) <= target_unabs)

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
            feasible = _objective_satisfied(frontier, objective, target_far, target_unabs)

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
    frontier["bess_power_mw"] = pd.to_numeric(frontier.get("required_bess_power_mw"), errors="coerce")
    frontier["duration_h"] = pd.to_numeric(frontier.get("required_bess_duration_h"), errors="coerce")
    frontier["bess_energy_mwh"] = pd.to_numeric(frontier.get("required_bess_energy_mwh"), errors="coerce")
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
    }
    for col, default_val in default_cols.items():
        if col not in frontier.columns:
            frontier[col] = default_val

    checks: list[dict[str, str]] = []
    warnings: list[str] = []
    tol = 1e-6

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
                        "status": "FAIL",
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
                        "status": "FAIL",
                        "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
                        "message": "Surplus non absorbe non monotone en dominance (P,E).",
                    }
                )
            if far_dominance_fail:
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
                        "message": "FAR non monotone en dominance (P,E).",
                    }
                )

    # Objective satisfaction and selection rule.
    feasible = _objective_satisfied(frontier, objective, target_far, target_unabs)
    zero_mask = (p_mw.abs() <= tol) & (e_mwh.abs() <= tol)
    baseline_rows = frontier[zero_mask].sort_values(["required_bess_power_mw", "required_bess_energy_mwh"])
    baseline_row = baseline_rows.iloc[0] if not baseline_rows.empty else None
    base_far_val = _safe_float(frontier.get("far_before", pd.Series(dtype=float)).iloc[0], np.nan) if ("far_before" in frontier.columns and not frontier.empty) else np.nan

    objective_met = False
    objective_reason = ""
    objective_recommendation = ""
    objective_target_value = target_far if objective == "FAR_TARGET" else target_unabs

    if baseline_row is not None:
        if objective == "FAR_TARGET":
            baseline_met = bool(_safe_float(baseline_row.get("far_after"), -np.inf) >= target_far)
        else:
            baseline_met = bool(_safe_float(baseline_row.get("surplus_unabs_energy_after"), np.inf) <= target_unabs)
        if baseline_met:
            objective_met = True
            objective_reason = "already_met"
            best = baseline_row
        else:
            best = None
    else:
        best = None

    if not objective_met:
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
            else:
                best = frontier.sort_values(["surplus_unabs_energy_after", "required_bess_power_mw", "required_bess_energy_mwh"]).iloc[0]
                baseline_metric = _safe_float(baseline_row.get("surplus_unabs_energy_after"), np.nan) if baseline_row is not None else np.nan
                best_metric = _safe_float(best.get("surplus_unabs_energy_after"), np.nan)
                improvement = baseline_metric - best_metric if np.isfinite(best_metric) and np.isfinite(baseline_metric) else np.nan

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
                "objective_target_value": objective_target_value,
                "objective_recommendation": objective_recommendation,
                "pv_capacity_proxy_mw": float(pv_capacity_proxy),
                "power_grid_max_mw": float(pd.to_numeric(frontier["required_bess_power_mw"], errors="coerce").max()) if not frontier.empty else np.nan,
                "duration_grid_max_h": float(pd.to_numeric(frontier["required_bess_duration_h"], errors="coerce").max()) if not frontier.empty else np.nan,
                "grid_expansions_used": int(grid_expansions_used),
                "notes_quality": "ok",
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
        tables={"Q4_sizing_summary": summary, "Q4_bess_frontier": frontier},
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
        mode=str(selection.get("mode", "HIST")).upper(),
        scenario_id=selection.get("scenario_id"),
        horizon_year=selection.get("horizon_year"),
    )
