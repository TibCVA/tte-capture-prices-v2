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
    max_cycles_per_day: float

    @property
    def energy_mwh(self) -> float:
        return self.power_mw * self.duration_h

    @property
    def eta_charge(self) -> float:
        return float(np.sqrt(self.eta_roundtrip))

    @property
    def eta_discharge(self) -> float:
        return float(np.sqrt(self.eta_roundtrip))


def _ensure_ts_index(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.index, pd.DatetimeIndex):
        out = df.copy()
        if out.index.tz is None:
            out.index = out.index.tz_localize("UTC")
        return out
    if "timestamp_utc" in df.columns:
        out = df.copy()
        out["timestamp_utc"] = pd.to_datetime(out["timestamp_utc"], errors="coerce", utc=True)
        out = out.dropna(subset=["timestamp_utc"]).set_index("timestamp_utc")
        return out
    raise ValueError("Hourly dataframe must have DatetimeIndex or timestamp_utc.")


def _daily_sets(day_df: pd.DataFrame, duration_h: float) -> tuple[set[pd.Timestamp], set[pd.Timestamp]]:
    n = max(1, int(np.ceil(duration_h)))
    low = set(day_df["price_da_eur_mwh"].nsmallest(min(n, len(day_df))).index)
    high = set(day_df["price_da_eur_mwh"].nlargest(min(n, len(day_df))).index)
    return low, high


def _simulate_dispatch(df: pd.DataFrame, cfg: BessConfig, dispatch_mode: str) -> tuple[pd.DataFrame, dict[str, float]]:
    out = _ensure_ts_index(df)
    out = out.sort_index().copy()

    for c in ["surplus_mw", "surplus_unabsorbed_mw", "nrl_mw", "gen_solar_mw", "price_da_eur_mwh", "flex_sink_observed_mw"]:
        if c not in out.columns:
            out[c] = 0.0
        out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0.0)

    soc = cfg.soc_init_frac * cfg.energy_mwh
    charge = np.zeros(len(out), dtype=float)
    discharge = np.zeros(len(out), dtype=float)
    soc_series = np.zeros(len(out), dtype=float)

    idx_by_day = pd.Series(np.arange(len(out)), index=out.index).groupby(out.index.tz_convert("UTC").floor("D"))
    max_daily_throughput = max(0.0, cfg.max_cycles_per_day) * cfg.energy_mwh

    for _, idx_positions in idx_by_day:
        pos = list(idx_positions.values)
        day = out.iloc[pos]
        low_set, high_set = _daily_sets(day, cfg.duration_h)
        daily_charge_in = 0.0
        daily_discharge_out = 0.0

        for i in pos:
            ts = out.index[i]
            price = float(out.iloc[i]["price_da_eur_mwh"])
            surplus_unabs = float(out.iloc[i]["surplus_unabsorbed_mw"])
            pv = max(0.0, float(out.iloc[i]["gen_solar_mw"]))

            desired_charge = 0.0
            desired_discharge = 0.0

            if dispatch_mode == "SURPLUS_FIRST":
                if surplus_unabs > 0:
                    desired_charge = surplus_unabs
                if ts in high_set:
                    desired_discharge = cfg.power_mw
            elif dispatch_mode == "PRICE_ARBITRAGE_SIMPLE":
                if ts in low_set:
                    desired_charge = cfg.power_mw
                elif ts in high_set:
                    desired_discharge = cfg.power_mw
            elif dispatch_mode == "PV_COLOCATED":
                if pv > 0:
                    desired_charge = min(cfg.power_mw, pv)
                if ts in high_set:
                    desired_discharge = cfg.power_mw
            else:
                raise ValueError(f"Unknown dispatch_mode={dispatch_mode}")

            if max_daily_throughput > 0:
                remaining_charge = max(0.0, max_daily_throughput - daily_charge_in)
                remaining_discharge = max(0.0, max_daily_throughput - daily_discharge_out)
            else:
                remaining_charge = 0.0
                remaining_discharge = 0.0

            ch = min(
                cfg.power_mw,
                desired_charge,
                max(0.0, (cfg.energy_mwh - soc) / cfg.eta_charge),
                remaining_charge,
            )
            soc += ch * cfg.eta_charge
            daily_charge_in += ch

            dis = min(
                cfg.power_mw,
                desired_discharge,
                max(0.0, soc * cfg.eta_discharge),
                remaining_discharge,
            )
            soc -= dis / cfg.eta_discharge
            daily_discharge_out += dis

            soc = min(max(soc, 0.0), cfg.energy_mwh)
            charge[i] = ch
            discharge[i] = dis
            soc_series[i] = soc

    out["bess_charge_mw"] = charge
    out["bess_discharge_mw"] = discharge
    out["bess_soc_mwh"] = soc_series
    out["flex_effective_mw_after"] = out["flex_sink_observed_mw"] + out["bess_charge_mw"]
    out["surplus_absorbed_mw_after"] = np.minimum(out["surplus_mw"], out["flex_effective_mw_after"])
    out["surplus_unabsorbed_mw_after"] = (out["surplus_mw"] - out["surplus_absorbed_mw_after"]).clip(lower=0.0)

    diag = {
        "soc_min": float(out["bess_soc_mwh"].min()),
        "soc_max": float(out["bess_soc_mwh"].max()),
        "charge_max": float(out["bess_charge_mw"].max()),
        "discharge_max": float(out["bess_discharge_mw"].max()),
        "charge_sum": float(out["bess_charge_mw"].sum()),
        "discharge_sum": float(out["bess_discharge_mw"].sum()),
    }
    return out, diag


def _compute_far(surplus: pd.Series, absorbed: pd.Series) -> float:
    s = float(pd.to_numeric(surplus, errors="coerce").fillna(0.0).sum())
    a = float(pd.to_numeric(absorbed, errors="coerce").fillna(0.0).sum())
    return np.nan if s <= 0.0 else a / s


def _pv_capture(price: pd.Series, pv: pd.Series) -> float:
    p = pd.to_numeric(price, errors="coerce")
    g = pd.to_numeric(pv, errors="coerce").fillna(0.0)
    den = float(g.sum())
    if den <= 0:
        return np.nan
    return float((p * g).sum()) / den


def run_q4(
    hourly_df: pd.DataFrame,
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
    dispatch_mode: str = "SURPLUS_FIRST",
) -> ModuleResult:
    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q4_PARAMS)].iterrows()
    }
    eta_rt = float(params.get("bess_eta_roundtrip", 0.88))
    soc_init = float(params.get("bess_soc_init_frac", 0.5))
    max_cycles_day = float(params.get("bess_max_cycles_per_day", 1.0))
    target_far = float(params.get("target_far", 0.95))
    target_unabs = float(params.get("target_surplus_unabs_energy_twh", 0.0))

    objective = str(selection.get("objective", "FAR_TARGET")).upper()
    if objective not in {"FAR_TARGET", "SURPLUS_UNABS_TARGET"}:
        objective = "FAR_TARGET"

    base = _ensure_ts_index(hourly_df)
    base_far = _compute_far(base["surplus_mw"], base["surplus_absorbed_mw"])
    unabs_before_twh = float(pd.to_numeric(base["surplus_unabsorbed_mw"], errors="coerce").fillna(0.0).sum()) / 1e6
    pv_before = _pv_capture(base["price_da_eur_mwh"], base["gen_solar_mw"])

    default_power_grid = [0.0, 200.0, 500.0, 1000.0, 2000.0, 4000.0, 6000.0, 8000.0]
    default_duration_grid = [1.0, 2.0, 4.0, 6.0, 8.0, 10.0]
    power_grid = [float(x) for x in selection.get("power_grid", default_power_grid)]
    duration_grid = [float(x) for x in selection.get("duration_grid", default_duration_grid)]
    rows: list[dict[str, Any]] = []
    checks: list[dict[str, str]] = []
    warnings: list[str] = []

    for p in power_grid:
        for d in duration_grid:
            cfg = BessConfig(
                power_mw=float(p),
                duration_h=float(d),
                eta_roundtrip=eta_rt,
                soc_init_frac=soc_init,
                max_cycles_per_day=max_cycles_day,
            )
            sim, diag = _simulate_dispatch(base, cfg, dispatch_mode=dispatch_mode)

            far_after = _compute_far(sim["surplus_mw"], sim["surplus_absorbed_mw_after"])
            unabs_after_twh = float(sim["surplus_unabsorbed_mw_after"].sum()) / 1e6
            revenue = float((sim["bess_discharge_mw"] * sim["price_da_eur_mwh"] - sim["bess_charge_mw"] * sim["price_da_eur_mwh"]).sum())

            if dispatch_mode == "PV_COLOCATED":
                pv_to_grid = (pd.to_numeric(base["gen_solar_mw"], errors="coerce").fillna(0.0) - sim["bess_charge_mw"]).clip(lower=0.0)
                pv_shifted = sim["bess_discharge_mw"]
                delivered = pv_to_grid + pv_shifted
                den = float(delivered.sum())
                pv_after = np.nan if den <= 0 else float((base["price_da_eur_mwh"] * delivered).sum()) / den
            else:
                pv_after = pv_before

            rows.append(
                {
                    "dispatch_mode": dispatch_mode,
                    "objective": objective,
                    "required_bess_power_mw": cfg.power_mw,
                    "required_bess_energy_mwh": cfg.energy_mwh,
                    "required_bess_duration_h": cfg.duration_h,
                    "far_before": base_far,
                    "far_after": far_after,
                    "surplus_unabs_energy_before": unabs_before_twh,
                    "surplus_unabs_energy_after": unabs_after_twh,
                    "pv_capture_price_before": pv_before,
                    "pv_capture_price_after": pv_after,
                    "revenue_bess_price_taker": revenue,
                    "soc_min": diag["soc_min"],
                    "soc_max": diag["soc_max"],
                    "charge_max": diag["charge_max"],
                    "discharge_max": diag["discharge_max"],
                    "charge_sum_mwh": diag["charge_sum"],
                    "discharge_sum_mwh": diag["discharge_sum"],
                    "initial_deliverable_mwh": cfg.soc_init_frac * cfg.energy_mwh * cfg.eta_discharge,
                }
            )

    frontier = pd.DataFrame(rows)
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

    # Hard invariants
    if (frontier["soc_min"] < -1e-6).any():
        checks.append({"status": "FAIL", "code": "Q4_SOC_NEG", "message": "SOC negatif detecte."})
    if (frontier["soc_max"] - frontier["required_bess_energy_mwh"] > 1e-6).any():
        checks.append({"status": "FAIL", "code": "Q4_SOC_ABOVE_EMAX", "message": "SOC > Emax detecte."})
    if (frontier["charge_max"] - frontier["required_bess_power_mw"] > 1e-6).any():
        checks.append({"status": "FAIL", "code": "Q4_CHARGE_ABOVE_PMAX", "message": "Charge > Pmax detectee."})
    if (frontier["discharge_max"] - frontier["required_bess_power_mw"] > 1e-6).any():
        checks.append({"status": "FAIL", "code": "Q4_DISCHARGE_ABOVE_PMAX", "message": "Decharge > Pmax detectee."})
    if (frontier["discharge_sum_mwh"] - (frontier["charge_sum_mwh"] * eta_rt + frontier["initial_deliverable_mwh"]) > 1e-3).any():
        checks.append({"status": "FAIL", "code": "Q4_ENERGY_BALANCE", "message": "Energie dechargee > energie chargee * eta."})

    if dispatch_mode == "SURPLUS_FIRST":
        if (frontier["surplus_unabs_energy_after"] - frontier["surplus_unabs_energy_before"] > 1e-9).any():
            checks.append({"status": "FAIL", "code": "Q4_SURPLUS_INCREASE", "message": "Surplus non absorbe augmente en mode SURPLUS_FIRST."})
        for d in duration_grid:
            subset = frontier[frontier["required_bess_duration_h"] == d].sort_values("required_bess_power_mw")
            if len(subset) >= 2 and (subset["far_after"].diff().dropna() < -1e-8).any():
                checks.append({"status": "FAIL", "code": "Q4_FAR_NON_MONOTONIC", "message": f"FAR diminue quand la puissance augmente (duration={d}h)."})

    # Objective satisfaction
    if objective == "FAR_TARGET":
        feasible = frontier[frontier["far_after"] >= target_far].sort_values(
            ["required_bess_power_mw", "required_bess_energy_mwh"]
        )
    else:
        feasible = frontier[frontier["surplus_unabs_energy_after"] <= target_unabs].sort_values(
            ["required_bess_power_mw", "required_bess_energy_mwh"]
        )
    if feasible.empty:
        if objective == "FAR_TARGET":
            best = frontier.sort_values(["far_after", "required_bess_power_mw"], ascending=[False, True]).iloc[0]
        else:
            best = frontier.sort_values(["surplus_unabs_energy_after", "required_bess_power_mw"]).iloc[0]
        warnings.append("Objectif non atteint sur la grille de sizing; meilleur compromis retourne.")
    else:
        best = feasible.iloc[0]

    summary = pd.DataFrame(
        [
            {
                "country": selection.get("country", ""),
                "year": selection.get("year", ""),
                **best.to_dict(),
                "notes_quality": "ok",
            }
        ]
    )

    if dispatch_mode == "PRICE_ARBITRAGE_SIMPLE" and float(summary["revenue_bess_price_taker"].iloc[0]) < 0:
        warnings.append("Revenu d'arbitrage annuel negatif: spread insuffisant ou regle de dispatch trop simple.")
    if float(summary["required_bess_duration_h"].iloc[0]) > 8.0:
        warnings.append("Besoin de stockage long (>8h): batterie courte potentiellement insuffisante.")

    if not checks:
        checks.append({"status": "PASS", "code": "Q4_PASS", "message": "Q4 invariants et checks passes."})

    narrative = (
        "Q4 estime un ordre de grandeur BESS sur historique avec dispatch explicite. "
        "Les resultats doivent etre lus comme benchmark mecaniste (price-taker), pas comme optimisation de marche."
    )

    return ModuleResult(
        module_id="Q4",
        run_id=run_id,
        selection=selection,
        assumptions_used=assumptions_subset(assumptions_df, Q4_PARAMS),
        kpis={"best_far_after": float(summary["far_after"].iloc[0]), "objective": objective},
        tables={"Q4_sizing_summary": summary, "Q4_bess_frontier": frontier},
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
    )
