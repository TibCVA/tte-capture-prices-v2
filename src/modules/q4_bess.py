"""Q4 - BESS sizing and impact simulation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from src.modules.common import assumptions_subset
from src.modules.result import ModuleResult

Q4_PARAMS = [
    "bess_eta_roundtrip",
    "bess_max_cycles_per_day",
    "bess_soc_init_frac",
    "target_far",
    "target_surplus_unabs_energy_twh",
]


@dataclass
class BessConfig:
    power_mw: float
    duration_h: float
    eta_roundtrip: float
    soc_init_frac: float

    @property
    def energy_mwh(self) -> float:
        return self.power_mw * self.duration_h


def _dispatch_surplus_first(df: pd.DataFrame, cfg: BessConfig) -> pd.DataFrame:
    out = df.copy()
    eta_c = np.sqrt(cfg.eta_roundtrip)
    eta_d = np.sqrt(cfg.eta_roundtrip)

    soc = cfg.soc_init_frac * cfg.energy_mwh
    charge = np.zeros(len(out), dtype=float)
    discharge = np.zeros(len(out), dtype=float)
    soc_series = np.zeros(len(out), dtype=float)

    date_utc = out.index.tz_convert("UTC").floor("D")
    grouped = pd.Series(range(len(out)), index=out.index).groupby(date_utc)

    for _, idx_positions in grouped:
        idx_list = list(idx_positions.values)
        day_prices = out.iloc[idx_list]["price_da_eur_mwh"]
        n_top = max(1, int(np.ceil(cfg.duration_h)))
        top_hours = day_prices.nlargest(min(n_top, len(day_prices))).index
        top_set = set(top_hours)

        for i in idx_list:
            ts = out.index[i]
            surplus_unabs = float(out.iloc[i]["surplus_unabsorbed_mw"])

            ch = min(cfg.power_mw, surplus_unabs, max(0.0, (cfg.energy_mwh - soc) / eta_c))
            soc += ch * eta_c
            charge[i] = ch

            if ts in top_set:
                nrl_pos = max(0.0, float(out.iloc[i]["nrl_mw"]))
                dis = min(cfg.power_mw, nrl_pos if nrl_pos > 0 else cfg.power_mw, max(0.0, soc * eta_d))
                soc -= dis / eta_d
                discharge[i] = dis

            soc = min(max(soc, 0.0), cfg.energy_mwh)
            soc_series[i] = soc

    out["bess_charge_mw"] = charge
    out["bess_discharge_mw"] = discharge
    out["bess_soc_mwh"] = soc_series
    out["flex_effective_mw_after"] = out["flex_sink_observed_mw"] + out["bess_charge_mw"]
    out["surplus_absorbed_mw_after"] = np.minimum(out["surplus_mw"], out["flex_effective_mw_after"])
    out["surplus_unabsorbed_mw_after"] = (out["surplus_mw"] - out["surplus_absorbed_mw_after"]).clip(lower=0.0)
    return out


def _dispatch_price_arbitrage(df: pd.DataFrame, cfg: BessConfig) -> pd.DataFrame:
    out = df.copy()
    eta_c = np.sqrt(cfg.eta_roundtrip)
    eta_d = np.sqrt(cfg.eta_roundtrip)
    soc = cfg.soc_init_frac * cfg.energy_mwh

    charge = np.zeros(len(out), dtype=float)
    discharge = np.zeros(len(out), dtype=float)
    soc_series = np.zeros(len(out), dtype=float)

    date_utc = out.index.tz_convert("UTC").floor("D")
    grouped = pd.Series(range(len(out)), index=out.index).groupby(date_utc)

    for _, idx_positions in grouped:
        idx_list = list(idx_positions.values)
        day = out.iloc[idx_list]
        n_h = max(1, int(np.ceil(cfg.duration_h)))
        charge_hours = set(day["price_da_eur_mwh"].nsmallest(min(n_h, len(day))).index)
        discharge_hours = set(day["price_da_eur_mwh"].nlargest(min(n_h, len(day))).index)

        for i in idx_list:
            ts = out.index[i]
            if ts in charge_hours:
                ch = min(cfg.power_mw, max(0.0, (cfg.energy_mwh - soc) / eta_c))
                soc += ch * eta_c
                charge[i] = ch
            elif ts in discharge_hours:
                dis = min(cfg.power_mw, max(0.0, soc * eta_d))
                soc -= dis / eta_d
                discharge[i] = dis

            soc = min(max(soc, 0.0), cfg.energy_mwh)
            soc_series[i] = soc

    out["bess_charge_mw"] = charge
    out["bess_discharge_mw"] = discharge
    out["bess_soc_mwh"] = soc_series
    out["revenue_bess_price_taker_eur"] = out["bess_discharge_mw"] * out["price_da_eur_mwh"] - out["bess_charge_mw"] * out["price_da_eur_mwh"]
    return out


def _dispatch_pv_colocated(df: pd.DataFrame, cfg: BessConfig) -> pd.DataFrame:
    out = _dispatch_surplus_first(df, cfg)
    out["bess_charge_mw"] = np.minimum(out["bess_charge_mw"], out["gen_solar_mw"].fillna(0.0))
    return out


def _compute_far(surplus: pd.Series, absorbed: pd.Series) -> float:
    s = float(surplus.fillna(0).sum())
    a = float(absorbed.fillna(0).sum())
    return np.nan if s <= 0 else a / s


def run_q4(hourly_df: pd.DataFrame, assumptions_df: pd.DataFrame, selection: dict[str, Any], run_id: str, dispatch_mode: str = "SURPLUS_FIRST") -> ModuleResult:
    params = {
        r["param_name"]: float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q4_PARAMS)].iterrows()
    }
    eta_rt = float(params.get("bess_eta_roundtrip", 0.88))
    soc_init = float(params.get("bess_soc_init_frac", 0.5))
    target_far = float(params.get("target_far", 0.95))

    base_far = _compute_far(hourly_df["surplus_mw"], hourly_df["surplus_absorbed_mw"])

    rows = []
    best = None
    for power_mw in [0, 200, 500, 1000, 2000, 4000, 6000]:
        for duration_h in [1, 2, 4, 6, 8]:
            cfg = BessConfig(power_mw=float(power_mw), duration_h=float(duration_h), eta_roundtrip=eta_rt, soc_init_frac=soc_init)
            if dispatch_mode == "SURPLUS_FIRST":
                sim = _dispatch_surplus_first(hourly_df, cfg)
            elif dispatch_mode == "PRICE_ARBITRAGE_SIMPLE":
                sim = _dispatch_price_arbitrage(hourly_df, cfg)
            else:
                sim = _dispatch_pv_colocated(hourly_df, cfg)

            far_after = _compute_far(sim["surplus_mw"], sim.get("surplus_absorbed_mw_after", sim["surplus_absorbed_mw"]))
            unabs_before = float(hourly_df["surplus_unabsorbed_mw"].fillna(0).sum()) / 1e6
            unabs_after = float(sim.get("surplus_unabsorbed_mw_after", hourly_df["surplus_unabsorbed_mw"]).fillna(0).sum()) / 1e6

            pv_before = np.nan
            pv_after = np.nan
            if float(hourly_df["gen_solar_mw"].fillna(0).sum()) > 0:
                pv_before = float((hourly_df["price_da_eur_mwh"] * hourly_df["gen_solar_mw"].fillna(0)).sum() / hourly_df["gen_solar_mw"].fillna(0).sum())
                pv_to_grid = hourly_df["gen_solar_mw"].fillna(0) - sim["bess_charge_mw"].fillna(0)
                pv_shifted = sim["bess_discharge_mw"].fillna(0)
                delivered = pv_to_grid + pv_shifted
                den = float(delivered.sum())
                if den > 0:
                    pv_after = float((hourly_df["price_da_eur_mwh"] * delivered).sum() / den)

            revenue = float(sim.get("revenue_bess_price_taker_eur", pd.Series(0, index=sim.index)).sum())

            row = {
                "objective": "FAR_TARGET",
                "required_bess_power_mw": cfg.power_mw,
                "required_bess_energy_mwh": cfg.energy_mwh,
                "required_bess_duration_h": cfg.duration_h,
                "far_before": base_far,
                "far_after": far_after,
                "surplus_unabs_energy_before": unabs_before,
                "surplus_unabs_energy_after": unabs_after,
                "pv_capture_price_before": pv_before,
                "pv_capture_price_after": pv_after,
                "revenue_bess_price_taker": revenue,
            }
            rows.append(row)

            if best is None and np.isfinite(far_after) and far_after >= target_far:
                best = row

    frontier = pd.DataFrame(rows)
    if best is None:
        best = frontier.sort_values(["surplus_unabs_energy_after", "required_bess_power_mw", "required_bess_energy_mwh"]).iloc[0].to_dict()

    summary = pd.DataFrame([
        {
            "country": selection.get("country", ""),
            "year": selection.get("year", ""),
            **best,
            "notes_quality": "ok",
        }
    ])

    checks = []
    if (frontier["surplus_unabs_energy_after"] > frontier["surplus_unabs_energy_before"]).any():
        checks.append({"status": "WARN", "message": "Some configurations increase unabsorbed surplus; inspect assumptions."})
    else:
        checks.append({"status": "PASS", "message": "Q4 invariants pass"})

    warnings = []
    if (frontier["revenue_bess_price_taker"] < 0).all():
        warnings.append("Arbitrage revenue is negative across the full grid")
    if float(summary["required_bess_duration_h"].iloc[0]) > 8:
        warnings.append("Long-duration storage need detected (>8h)")

    narrative = "Q4 estimates BESS order of magnitude on historical data with explicit and auditable dispatch."

    return ModuleResult(
        module_id="Q4",
        run_id=run_id,
        selection=selection,
        assumptions_used=assumptions_subset(assumptions_df, Q4_PARAMS),
        kpis={"best_far_after": float(summary["far_after"].iloc[0])},
        tables={"Q4_sizing_summary": summary, "Q4_bess_frontier": frontier},
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
    )
