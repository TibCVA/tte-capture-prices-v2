"""Auditable hourly BESS dispatch helpers."""

from __future__ import annotations

from typing import Any

import numpy as np


def _as_array(values: Any, n: int | None = None) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim == 0:
        if n is None:
            return np.asarray([float(arr)], dtype=float)
        return np.full(int(n), float(arr), dtype=float)
    if n is not None and len(arr) != int(n):
        raise ValueError(f"Array length mismatch: expected {n}, got {len(arr)}")
    return arr.astype(float, copy=False)


def run_bess_dispatch(
    surplus_raw_mw: Any,
    deficit_raw_mw: Any,
    pv_mw: Any,
    price_proxy: Any,
    bess_power_mw: float,
    bess_energy_mwh: float,
    eta_roundtrip: float,
    dispatch_mode: str,
    objective: str | None = None,
    params: dict[str, Any] | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, float]]:
    """Run a simple, auditable hourly dispatch with hard physical limits."""

    _ = objective
    cfg = dict(params or {})
    mode = str(dispatch_mode or "SURPLUS_FIRST").upper()

    surplus = _as_array(surplus_raw_mw)
    n = int(len(surplus))
    deficit = np.clip(_as_array(deficit_raw_mw, n=n), 0.0, None)
    pv = np.clip(_as_array(pv_mw, n=n), 0.0, None)
    price = _as_array(price_proxy, n=n)

    pmax = float(max(0.0, bess_power_mw))
    emax = float(max(0.0, bess_energy_mwh))
    eta_rt = float(np.clip(eta_roundtrip, 1e-6, 1.0))
    eta_c = float(np.sqrt(eta_rt))
    eta_d = float(np.sqrt(eta_rt))
    tol = 1e-9

    if n == 0 or pmax <= 0.0 or emax <= 0.0:
        zeros = np.zeros(n, dtype=float)
        diagnostics = {
            "soc_min": 0.0,
            "soc_max": 0.0,
            "soc_start": 0.0,
            "soc_end": 0.0,
            "charge_max": 0.0,
            "discharge_max": 0.0,
            "charge_sum": 0.0,
            "discharge_sum": 0.0,
            "charge_hours": 0.0,
            "discharge_hours": 0.0,
            "cycles_realized_per_day": 0.0,
            "simultaneous_charge_discharge_hours": 0.0,
            "charge_vs_surplus_violation_hours": 0.0,
            "energy_balance_residual": 0.0,
            "price_p20": float("nan"),
            "price_p80": float("nan"),
        }
        return zeros, zeros, zeros, diagnostics

    finite_price = price[np.isfinite(price)]
    p20 = float(np.nanquantile(finite_price, 0.20)) if finite_price.size else float("nan")
    p80 = float(np.nanquantile(finite_price, 0.80)) if finite_price.size else float("nan")
    if np.isfinite(p20) and np.isfinite(p80) and p20 > p80:
        p20, p80 = p80, p20

    soc_start_cfg = float(cfg.get("soc_start_mwh", cfg.get("soc_init_frac", 0.0) * emax))
    soc_target = float(np.clip(cfg.get("soc_end_target_mwh", 0.0), 0.0, emax))
    soc = float(np.clip(soc_start_cfg, 0.0, emax))
    soc_start = float(soc)
    max_cycles_per_day = float(max(0.0, cfg.get("max_cycles_per_day", np.inf)))
    max_daily_throughput = (max_cycles_per_day * emax) if np.isfinite(max_cycles_per_day) else np.inf

    day_ids_input = cfg.get("day_ids")
    if day_ids_input is None:
        day_ids = np.arange(n, dtype=int) // 24
    else:
        day_ids = _as_array(day_ids_input, n=n).astype(int)

    charge = np.zeros(n, dtype=float)
    discharge = np.zeros(n, dtype=float)
    soc_series = np.zeros(n, dtype=float)
    charge_vs_surplus_violation_hours = 0.0

    per_day_charge: dict[int, float] = {}
    per_day_discharge: dict[int, float] = {}
    pv_share = float(np.clip(cfg.get("pv_charge_share", 1.0), 0.0, 1.0))
    cap_pv_to_surplus = bool(cfg.get("pv_charge_cap_to_surplus", False))

    for i in range(n):
        day_id = int(day_ids[i])
        day_charge = float(per_day_charge.get(day_id, 0.0))
        day_discharge = float(per_day_discharge.get(day_id, 0.0))
        remaining_charge_budget = max(0.0, max_daily_throughput - day_charge) if np.isfinite(max_daily_throughput) else np.inf
        remaining_discharge_budget = max(0.0, max_daily_throughput - day_discharge) if np.isfinite(max_daily_throughput) else np.inf

        remaining_future_hours = max(0, n - i - 1)
        max_soc_if_no_discharge_now = soc_target + (remaining_future_hours * pmax / eta_d if eta_d > 0 else 0.0)
        max_soc_if_no_discharge_now = float(np.clip(max_soc_if_no_discharge_now, 0.0, emax))

        charge_opp = 0.0
        discharge_opp = 0.0
        charge_condition = False
        discharge_condition = False
        price_i = price[i]

        if mode == "SURPLUS_FIRST":
            charge_opp = float(max(0.0, surplus[i]))
            discharge_opp = float(max(0.0, deficit[i]))
            charge_condition = charge_opp > tol
            discharge_condition = (not charge_condition) and (discharge_opp > tol)
        elif mode == "PV_COLOCATED":
            charge_opp = float(max(0.0, pv[i] * pv_share))
            if cap_pv_to_surplus:
                charge_opp = float(min(charge_opp, max(0.0, surplus[i])))
            discharge_opp = float(max(0.0, deficit[i]))
            charge_condition = charge_opp > tol
            discharge_condition = (not charge_condition) and (discharge_opp > tol)
        elif mode == "PRICE_ARBITRAGE_SIMPLE":
            charge_opp = float(pmax)
            discharge_opp = float(max(0.0, deficit[i]))
            charge_condition = bool(np.isfinite(price_i) and np.isfinite(p20) and price_i <= p20 + tol)
            discharge_condition = (not charge_condition) and bool(np.isfinite(price_i) and np.isfinite(p80) and price_i >= p80 - tol)
        elif mode == "LOW_RESIDUAL_FIRST":
            charge_opp = float(max(0.0, surplus[i]))
            discharge_opp = float(max(0.0, deficit[i]))
            charge_condition = charge_opp > tol
            discharge_condition = (not charge_condition) and bool(np.isfinite(price_i) and np.isfinite(p80) and price_i >= p80 - tol)
        else:
            raise ValueError(f"Unsupported dispatch_mode={dispatch_mode}")

        # Terminal SOC feasibility: force discharge when SOC is above the maximum removable envelope.
        forced_terminal_discharge = bool(soc > max_soc_if_no_discharge_now + tol)
        if forced_terminal_discharge:
            discharge_opp = max(discharge_opp, (soc - max_soc_if_no_discharge_now) * eta_d)
            charge_condition = False
            discharge_condition = True
            # Priority to terminal feasibility over daily throughput cap.
            remaining_discharge_budget = np.inf

        ch = 0.0
        dis = 0.0
        if charge_condition and not discharge_condition:
            # Keep terminal SOC feasible given remaining discharge hours.
            terminal_charge_headroom = (
                max(0.0, (max_soc_if_no_discharge_now - soc) / eta_c)
                if eta_c > 0.0
                else 0.0
            )
            ch = min(
                pmax,
                charge_opp,
                max(0.0, (emax - soc) / eta_c) if eta_c > 0 else 0.0,
                terminal_charge_headroom,
                remaining_charge_budget,
            )
        elif discharge_condition:
            dis = min(
                pmax,
                discharge_opp,
                max(0.0, soc * eta_d),
                remaining_discharge_budget,
            )

        if mode == "SURPLUS_FIRST" and ch > surplus[i] + 1e-6:
            charge_vs_surplus_violation_hours += 1.0

        soc = soc + ch * eta_c - dis / eta_d
        soc = float(np.clip(soc, 0.0, emax))
        charge[i] = ch
        discharge[i] = dis
        soc_series[i] = soc
        per_day_charge[day_id] = day_charge + ch
        per_day_discharge[day_id] = day_discharge + dis

    charge_sum = float(np.sum(charge))
    discharge_sum = float(np.sum(discharge))
    n_days = int(cfg.get("n_days", max(1, len(np.unique(day_ids)))))
    cycles_realized = (charge_sum / (emax * max(1, n_days))) if emax > 0 else 0.0
    energy_balance_residual = float(soc - (soc_start + charge_sum * eta_c - discharge_sum / eta_d))
    simultaneous = float(np.sum((charge > tol) & (discharge > tol)))

    diagnostics = {
        "soc_min": float(np.min(soc_series)) if n else 0.0,
        "soc_max": float(np.max(soc_series)) if n else 0.0,
        "soc_start": float(soc_start),
        "soc_end": float(soc),
        "charge_max": float(np.max(charge)) if n else 0.0,
        "discharge_max": float(np.max(discharge)) if n else 0.0,
        "charge_sum": charge_sum,
        "discharge_sum": discharge_sum,
        "charge_hours": float(np.sum(charge > tol)),
        "discharge_hours": float(np.sum(discharge > tol)),
        "cycles_realized_per_day": float(max(0.0, cycles_realized)),
        "simultaneous_charge_discharge_hours": simultaneous,
        "charge_vs_surplus_violation_hours": float(charge_vs_surplus_violation_hours),
        "energy_balance_residual": float(energy_balance_residual),
        "price_p20": p20,
        "price_p80": p80,
    }
    return charge, discharge, soc_series, diagnostics
