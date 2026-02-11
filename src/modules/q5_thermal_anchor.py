"""Q5 - Thermal anchor sensitivity to gas and CO2."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.constants import THERMAL_DEFAULTS
from src.modules.common import assumptions_subset
from src.modules.result import ModuleResult

Q5_PARAMS = [
    "ccgt_efficiency",
    "ccgt_ef_t_per_mwh_th",
    "ccgt_vom_eur_mwh",
    "coal_efficiency",
    "coal_ef_t_per_mwh_th",
    "coal_vom_eur_mwh",
]

ANCHOR_TECH_DEFAULTS = {
    "CCGT": {
        "efficiency": THERMAL_DEFAULTS["CCGT"]["efficiency"],
        "emission_factor_t_per_mwh_th": THERMAL_DEFAULTS["CCGT"]["emission_factor_t_per_mwh_th"],
        "vom_eur_mwh": THERMAL_DEFAULTS["CCGT"]["vom_eur_mwh"],
        "fuel_multiplier_vs_gas": 1.0,
    },
    "COAL": {
        "efficiency": THERMAL_DEFAULTS["COAL"]["efficiency"],
        "emission_factor_t_per_mwh_th": THERMAL_DEFAULTS["COAL"]["emission_factor_t_per_mwh_th"],
        "vom_eur_mwh": THERMAL_DEFAULTS["COAL"]["vom_eur_mwh"],
        "fuel_multiplier_vs_gas": 0.55,
    },
    "LIGNITE": {
        "efficiency": 0.35,
        "emission_factor_t_per_mwh_th": 0.41,
        "vom_eur_mwh": 5.0,
        "fuel_multiplier_vs_gas": 0.35,
    },
}


def load_commodity_daily(path: str = "data/external/commodity_prices_daily.csv") -> pd.DataFrame | None:
    p = Path(path)
    if not p.exists():
        return None
    df = pd.read_csv(p)
    required = {"date", "gas_price_eur_mwh_th", "co2_price_eur_t"}
    if not required.issubset(df.columns):
        return None
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    return df


def _safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
    except Exception:
        return float(default)
    return out if np.isfinite(out) else float(default)


def _tech_params(assumptions_df: pd.DataFrame, tech: str) -> tuple[float, float, float, float]:
    params = {
        str(r["param_name"]): float(r["param_value"])
        for _, r in assumptions_df[assumptions_df["param_name"].isin(Q5_PARAMS)].iterrows()
    }
    t = str(tech).upper()
    base = ANCHOR_TECH_DEFAULTS.get(t, ANCHOR_TECH_DEFAULTS["CCGT"])
    if t == "CCGT":
        eff = float(params.get("ccgt_efficiency", base["efficiency"]))
        ef = float(params.get("ccgt_ef_t_per_mwh_th", base["emission_factor_t_per_mwh_th"]))
        vom = float(params.get("ccgt_vom_eur_mwh", base["vom_eur_mwh"]))
        mult = float(base["fuel_multiplier_vs_gas"])
    elif t == "COAL":
        eff = float(params.get("coal_efficiency", base["efficiency"]))
        ef = float(params.get("coal_ef_t_per_mwh_th", base["emission_factor_t_per_mwh_th"]))
        vom = float(params.get("coal_vom_eur_mwh", base["vom_eur_mwh"]))
        mult = float(base["fuel_multiplier_vs_gas"])
    else:
        eff = float(base["efficiency"])
        ef = float(base["emission_factor_t_per_mwh_th"])
        vom = float(base["vom_eur_mwh"])
        mult = float(base["fuel_multiplier_vs_gas"])
    return eff, ef, vom, mult


def _build_cd_masks(h: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    if "nrl_mw" in h.columns and pd.to_numeric(h["nrl_mw"], errors="coerce").notna().sum() >= 20:
        nrl = pd.to_numeric(h["nrl_mw"], errors="coerce")
        pos = nrl[nrl >= 0]
        if pos.empty:
            cd = pd.Series(False, index=h.index)
            d = pd.Series(False, index=h.index)
        else:
            thr_d = float(pos.quantile(0.90))
            cd = nrl >= 0
            d = nrl >= thr_d
        return cd.fillna(False), d.fillna(False)
    regime_col = "regime" if "regime" in h.columns else ("regime_phys" if "regime_phys" in h.columns else None)
    if regime_col is None:
        cd = pd.Series(True, index=h.index)
        d = pd.Series(False, index=h.index)
        return cd, d
    reg = h[regime_col].astype(str)
    return reg.isin(["C", "D"]), reg.eq("D")


def _distributional_error(price_cd: pd.Series, anchor_cd: pd.Series) -> tuple[float, float, float]:
    p = pd.to_numeric(price_cd, errors="coerce").dropna()
    a = pd.to_numeric(anchor_cd, errors="coerce").dropna()
    idx = p.index.intersection(a.index)
    if len(idx) < 24:
        return np.nan, np.nan, np.nan
    p90 = float(p.loc[idx].quantile(0.90))
    p95 = float(p.loc[idx].quantile(0.95))
    a90 = float(a.loc[idx].quantile(0.90))
    a95 = float(a.loc[idx].quantile(0.95))
    err = 0.5 * abs(p90 - a90) + 0.5 * abs(p95 - a95)
    return err, p90 - a90, p95 - a95


def _daily_spread_stats(price: pd.Series) -> tuple[int, float]:
    p = pd.to_numeric(price, errors="coerce").dropna()
    if p.empty:
        return 0, np.nan
    idx = p.index
    if not isinstance(idx, pd.DatetimeIndex):
        try:
            idx = pd.to_datetime(idx, errors="coerce")
        except Exception:
            return 0, np.nan
    if not isinstance(idx, pd.DatetimeIndex):
        return 0, np.nan
    by_day = p.groupby(idx.floor("D")).agg(lambda x: float(np.nanmax(x) - np.nanmin(x)))
    days_gt50 = int((by_day > 50.0).sum())
    avg_spread = float(by_day.mean()) if len(by_day) else np.nan
    return days_gt50, avg_spread


def _pick_anchor_tech(
    assumptions_df: pd.DataFrame,
    h_cd: pd.DataFrame,
    override: str | None,
) -> tuple[str, pd.Series, dict[str, float]]:
    if override:
        tech = str(override).upper()
        eff, ef, vom, mult = _tech_params(assumptions_df, tech)
        fuel_proxy = pd.to_numeric(h_cd["gas_price_eur_mwh_th"], errors="coerce") * mult
        anchor = fuel_proxy / eff + pd.to_numeric(h_cd["co2_price_eur_t"], errors="coerce") * (ef / eff) + vom
        return tech, anchor, {"efficiency": eff, "ef": ef, "vom": vom, "multiplier": mult}

    best_tech = "CCGT"
    best_anchor = pd.Series(dtype=float)
    best_score = np.inf
    best_meta: dict[str, float] = {}
    for tech in ["CCGT", "COAL", "LIGNITE"]:
        eff, ef, vom, mult = _tech_params(assumptions_df, tech)
        fuel_proxy = pd.to_numeric(h_cd["gas_price_eur_mwh_th"], errors="coerce") * mult
        anchor = fuel_proxy / eff + pd.to_numeric(h_cd["co2_price_eur_t"], errors="coerce") * (ef / eff) + vom
        err, _, _ = _distributional_error(pd.to_numeric(h_cd["price_da_eur_mwh"], errors="coerce"), anchor)
        score = abs(err) if np.isfinite(err) else np.inf
        if score < best_score:
            best_score = score
            best_tech = tech
            best_anchor = anchor
            best_meta = {"efficiency": eff, "ef": ef, "vom": vom, "multiplier": mult}
    if best_anchor.empty:
        eff, ef, vom, mult = _tech_params(assumptions_df, "CCGT")
        fuel_proxy = pd.to_numeric(h_cd["gas_price_eur_mwh_th"], errors="coerce") * mult
        best_anchor = fuel_proxy / eff + pd.to_numeric(h_cd["co2_price_eur_t"], errors="coerce") * (ef / eff) + vom
        best_meta = {"efficiency": eff, "ef": ef, "vom": vom, "multiplier": mult}
    return best_tech, best_anchor, best_meta


def run_q5(
    hourly_df: pd.DataFrame,
    assumptions_df: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
    commodity_daily: pd.DataFrame | None = None,
    ttl_target_eur_mwh: float | None = None,
    gas_override_eur_mwh_th: float | None = None,
    co2_override_eur_t: float | None = None,
    ttl_method: str | None = None,
    ttl_physical_margin_eur_mwh: float | None = None,
) -> ModuleResult:
    country = str(selection.get("country", ""))
    override_tech = str(selection.get("marginal_tech", "")).upper().strip() or None

    if commodity_daily is None:
        commodity_daily = load_commodity_daily()
    if commodity_daily is None or commodity_daily.empty:
        checks = [{"status": "WARN", "code": "Q5_MISSING_COMMODITIES", "message": "Serie commodites absente: Q5 desactive."}]
        empty = pd.DataFrame(
            [
                {
                    "country": country,
                    "chosen_anchor_tech": "",
                    "ttl_obs": np.nan,
                    "ttl_anchor": np.nan,
                    "anchor_distribution_error_p90_p95": np.nan,
                    "required_co2_eur_t": np.nan,
                    "required_gas_eur_mwh_th": np.nan,
                    "co2_required_base_non_negative": np.nan,
                    "co2_required_gas_override_non_negative": np.nan,
                    "warnings_quality": "missing_commodities",
                }
            ]
        )
        return ModuleResult(
            module_id="Q5",
            run_id=run_id,
            selection=selection,
            assumptions_used=assumptions_subset(assumptions_df, Q5_PARAMS),
            kpis={},
            tables={"Q5_summary": empty},
            figures=[],
            narrative_md="Q5 ne peut pas s'executer sans series journaliere gaz/CO2.",
            checks=checks,
            warnings=["Missing commodity daily series."],
            mode=str(selection.get("mode", "HIST")).upper(),
            scenario_id=selection.get("scenario_id"),
            horizon_year=selection.get("horizon_year"),
        )

    c = commodity_daily.copy()
    c["date"] = pd.to_datetime(c["date"], errors="coerce").dt.tz_localize(None)
    h = hourly_df.copy()
    if not isinstance(h.index, pd.DatetimeIndex):
        if "timestamp_utc" in h.columns:
            h["timestamp_utc"] = pd.to_datetime(h["timestamp_utc"], errors="coerce", utc=True)
            h = h.dropna(subset=["timestamp_utc"]).set_index("timestamp_utc")
        else:
            raise ValueError("hourly_df must contain timestamp index or timestamp_utc.")
    if h.index.tz is None:
        h.index = h.index.tz_localize("UTC")

    h["date"] = h.index.tz_convert("UTC").tz_localize(None).floor("D")
    h["__ts_idx"] = h.index
    h = h.merge(c[["date", "gas_price_eur_mwh_th", "co2_price_eur_t"]], on="date", how="left")
    h = h.set_index("__ts_idx").sort_index()
    if gas_override_eur_mwh_th is not None:
        h["gas_price_eur_mwh_th"] = float(gas_override_eur_mwh_th)
    if co2_override_eur_t is not None:
        h["co2_price_eur_t"] = float(co2_override_eur_t)

    h["gas_price_eur_mwh_th"] = pd.to_numeric(h["gas_price_eur_mwh_th"], errors="coerce")
    h["co2_price_eur_t"] = pd.to_numeric(h["co2_price_eur_t"], errors="coerce")
    h["price_da_eur_mwh"] = pd.to_numeric(h["price_da_eur_mwh"], errors="coerce")

    if "year" not in h.columns:
        h["year"] = h.index.tz_convert("UTC").year.astype(int)
    else:
        h["year"] = pd.to_numeric(h["year"], errors="coerce").astype("Int64")

    cd_mask, d_mask = _build_cd_masks(h)
    h_cd = h[cd_mask & h["price_da_eur_mwh"].notna() & h["gas_price_eur_mwh_th"].notna() & h["co2_price_eur_t"].notna()].copy()

    chosen_tech, anchor_cd, tech_meta = _pick_anchor_tech(assumptions_df, h_cd, override=override_tech)
    eff = float(tech_meta["efficiency"])
    ef = float(tech_meta["ef"])
    vom = float(tech_meta["vom"])
    fuel_mult = float(tech_meta["multiplier"])

    # Build hourly anchor on full panel for annual aggregation.
    h["ttl_anchor_eur_mwh"] = (
        pd.to_numeric(h["gas_price_eur_mwh_th"], errors="coerce") * fuel_mult / eff
        + pd.to_numeric(h["co2_price_eur_t"], errors="coerce") * (ef / eff)
        + vom
    )
    # Rebuild C/D scoped panel after anchor creation so downstream stats have all required columns.
    h_cd = h[cd_mask & h["price_da_eur_mwh"].notna() & h["gas_price_eur_mwh_th"].notna() & h["co2_price_eur_t"].notna()].copy()

    # Annual TTL table aligned with annual_metrics: P95 in regimes C/D (or fallback cd_mask).
    annual_rows: list[dict[str, Any]] = []
    for year, gy in h.groupby("year", dropna=True):
        gy = gy.copy()
        regime_col = "regime" if "regime" in gy.columns else ("regime_phys" if "regime_phys" in gy.columns else None)
        if regime_col is not None:
            mask_cd_y = gy[regime_col].astype(str).isin(["C", "D"]) & gy["price_da_eur_mwh"].notna()
        else:
            # fallback if regime missing
            mask_cd_y = cd_mask.loc[gy.index] & gy["price_da_eur_mwh"].notna()
        ttl_year = float(pd.to_numeric(gy.loc[mask_cd_y, "price_da_eur_mwh"], errors="coerce").quantile(0.95)) if mask_cd_y.any() else np.nan
        ttl_anchor_year = float(pd.to_numeric(gy.loc[mask_cd_y, "ttl_anchor_eur_mwh"], errors="coerce").quantile(0.95)) if mask_cd_y.any() else np.nan
        days_gt50, avg_spread = _daily_spread_stats(pd.to_numeric(gy["price_da_eur_mwh"], errors="coerce"))
        crisis_year = bool(np.isfinite(avg_spread) and avg_spread > 50.0 and days_gt50 > 150)
        annual_rows.append(
            {
                "year": int(year),
                "ttl_eur_mwh": ttl_year,
                "ttl_anchor_eur_mwh": ttl_anchor_year,
                "days_spread_gt50": days_gt50,
                "avg_daily_spread_obs": avg_spread,
                "crisis_year": crisis_year,
            }
        )
    annual_ttl = pd.DataFrame(annual_rows).sort_values("year").reset_index(drop=True) if annual_rows else pd.DataFrame(columns=["year", "ttl_eur_mwh", "ttl_anchor_eur_mwh", "days_spread_gt50", "avg_daily_spread_obs", "crisis_year"])

    ttl_reference_mode = str(selection.get("ttl_reference_mode", ttl_method or "year_specific")).strip().lower()
    if ttl_reference_mode not in {"year_specific", "median_over_years_excluding_crisis"}:
        ttl_reference_mode = "year_specific"

    candidate_non_crisis = annual_ttl[(~annual_ttl["crisis_year"]) & pd.to_numeric(annual_ttl["ttl_eur_mwh"], errors="coerce").notna()] if not annual_ttl.empty else pd.DataFrame()
    requested_ref_year = selection.get("ttl_reference_year", selection.get("horizon_year"))
    ref_year = int(_safe_float(requested_ref_year, np.nan)) if np.isfinite(_safe_float(requested_ref_year, np.nan)) else None
    if ref_year is None:
        if not candidate_non_crisis.empty:
            ref_year = int(candidate_non_crisis["year"].max())
        elif not annual_ttl.empty:
            ref_year = int(annual_ttl["year"].max())

    if ttl_reference_mode == "year_specific":
        ref_row = annual_ttl[annual_ttl["year"] == int(ref_year)] if ref_year is not None and not annual_ttl.empty else pd.DataFrame()
        if ref_row.empty and not annual_ttl.empty:
            ref_row = annual_ttl.tail(1)
        ttl_obs = _safe_float(ref_row["ttl_eur_mwh"].iloc[0], np.nan) if not ref_row.empty else np.nan
        ttl_anchor = _safe_float(ref_row["ttl_anchor_eur_mwh"].iloc[0], np.nan) if not ref_row.empty else np.nan
        ref_year_used = int(ref_row["year"].iloc[0]) if not ref_row.empty else np.nan
        ref_hourly = h_cd[pd.to_numeric(h_cd["year"], errors="coerce") == int(ref_year_used)] if np.isfinite(_safe_float(ref_year_used, np.nan)) else h_cd.copy()
    else:
        med_base = candidate_non_crisis if not candidate_non_crisis.empty else annual_ttl
        ttl_obs = _safe_float(pd.to_numeric(med_base["ttl_eur_mwh"], errors="coerce").median(), np.nan) if not med_base.empty else np.nan
        ttl_anchor = _safe_float(pd.to_numeric(med_base["ttl_anchor_eur_mwh"], errors="coerce").median(), np.nan) if not med_base.empty else np.nan
        ref_year_used = np.nan
        non_crisis_years = set(pd.to_numeric(candidate_non_crisis["year"], errors="coerce").dropna().astype(int).tolist()) if not candidate_non_crisis.empty else set()
        if non_crisis_years:
            ref_hourly = h_cd[pd.to_numeric(h_cd["year"], errors="coerce").astype("Int64").isin(non_crisis_years)].copy()
        else:
            ref_hourly = h_cd.copy()

    if ref_hourly.empty:
        ref_hourly = h_cd.copy()

    ttl_target = _safe_float(ttl_target_eur_mwh, ttl_obs if np.isfinite(ttl_obs) else np.nan)
    alpha = ttl_obs - ttl_anchor if np.isfinite(ttl_obs) and np.isfinite(ttl_anchor) else np.nan
    corr_cd = float(pd.to_numeric(ref_hourly["price_da_eur_mwh"], errors="coerce").corr(pd.to_numeric(ref_hourly["ttl_anchor_eur_mwh"], errors="coerce"))) if len(ref_hourly) >= 24 else np.nan
    dist_error, p90_err, p95_err = _distributional_error(ref_hourly["price_da_eur_mwh"], ref_hourly["ttl_anchor_eur_mwh"])

    dco2 = ef / eff if eff > 0 else np.nan
    dgas = fuel_mult / eff if eff > 0 else np.nan

    fuel_term_p95 = float((pd.to_numeric(ref_hourly["gas_price_eur_mwh_th"], errors="coerce") * fuel_mult / eff).quantile(0.95)) if not ref_hourly.empty else np.nan
    co2_term_p95 = float((pd.to_numeric(ref_hourly["co2_price_eur_t"], errors="coerce") * (ef / eff)).quantile(0.95)) if not ref_hourly.empty else np.nan
    anchor_status = "ok"
    if np.isfinite(ttl_obs) and np.isfinite(ttl_target) and ttl_obs >= ttl_target:
        required_co2 = 0.0
        required_gas = 0.0
        anchor_status = "already_above_target"
    else:
        required_co2 = (ttl_target - fuel_term_p95 - vom) / dco2 if np.isfinite(ttl_target) and np.isfinite(fuel_term_p95) and np.isfinite(dco2) and dco2 > 0 else np.nan
        required_gas = (ttl_target - co2_term_p95 - vom) / dgas if np.isfinite(ttl_target) and np.isfinite(co2_term_p95) and np.isfinite(dgas) and dgas > 0 else np.nan
        required_co2 = max(0.0, float(required_co2)) if np.isfinite(required_co2) else np.nan
        required_gas = max(0.0, float(required_gas)) if np.isfinite(required_gas) else np.nan

    thermal_share = np.nan
    thermal_cols = [c for c in ["gen_gas_mw", "gen_coal_mw", "gen_lignite_mw", "gen_oil_mw", "gen_other_mw"] if c in h.columns]
    if thermal_cols and "gen_total_mw" in h.columns:
        thermal = pd.to_numeric(h[thermal_cols].sum(axis=1), errors="coerce")
        gen_total = pd.to_numeric(h["gen_total_mw"], errors="coerce")
        thermal_share = float((thermal / gen_total.replace(0, np.nan)).mean())

    checks: list[dict[str, str]] = []
    warnings: list[str] = []
    if not (np.isfinite(dco2) and dco2 > 0):
        checks.append({"status": "FAIL", "code": "Q5_DCO2_SIGN", "message": "dTCA/dCO2 doit etre strictement positif."})
    if not (np.isfinite(dgas) and dgas > 0):
        checks.append({"status": "FAIL", "code": "Q5_DGAS_SIGN", "message": "dTCA/dGas doit etre strictement positif."})
    if np.isfinite(alpha) and alpha < 0.0 and anchor_status == "already_above_target":
        checks.append({"status": "INFO", "code": "Q5_ALPHA_NEGATIVE", "message": "Alpha negatif mais TTL deja au-dessus de la cible (lecture normale)."})
    elif np.isfinite(alpha) and alpha < 0.0:
        checks.append({"status": "WARN", "code": "Q5_ALPHA_NEGATIVE", "message": "Alpha negatif hors cas already_above_target."})
    if np.isfinite(dist_error):
        bad_fit = dist_error > 35.0 and np.isfinite(thermal_share) and thermal_share >= 0.20
        checks.append(
            {
                "status": "WARN" if bad_fit else "INFO",
                "code": "Q5_DISTRIBUTIONAL_FIT",
                "message": f"Erreur distributionnelle p90/p95={dist_error:.1f} EUR/MWh ({'a revoir' if bad_fit else 'acceptable'}).",
            }
        )
    if np.isfinite(corr_cd) and corr_cd < 0.2:
        checks.append({"status": "INFO", "code": "Q5_LOW_CORR_CD", "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."})
    if ttl_reference_mode == "year_specific" and np.isfinite(_safe_float(ref_year_used, np.nan)) and not annual_ttl.empty:
        annual_same = annual_ttl[annual_ttl["year"] == int(ref_year_used)]
        ttl_annual_same_year = _safe_float(annual_same["ttl_eur_mwh"].iloc[0], np.nan) if not annual_same.empty else np.nan
        tol = _safe_float(selection.get("ttl_consistency_tolerance", 0.05), 0.05)
        if np.isfinite(ttl_obs) and np.isfinite(ttl_annual_same_year) and abs(ttl_annual_same_year) > 1e-12:
            rel_err = abs(ttl_obs - ttl_annual_same_year) / abs(ttl_annual_same_year)
            if rel_err > tol:
                checks.append(
                    {
                        "status": "FAIL",
                        "code": "Q5_TTL_INCONSISTENT_WITH_ANNUAL",
                        "message": f"TTL inconsistant vs annual metrics pour {int(ref_year_used)} (rel_err={rel_err:.2%}).",
                    }
                )
    if not checks:
        checks.append({"status": "PASS", "code": "Q5_PASS", "message": "Q5 checks passes."})

    summary = pd.DataFrame(
        [
            {
                "country": country,
                "year_range_used": f"{int(h['year'].min())}-{int(h['year'].max())}" if "year" in h.columns and h["year"].notna().any() else "",
                "ttl_reference_mode": ttl_reference_mode,
                "ttl_reference_year": ref_year_used,
                "marginal_tech": chosen_tech,
                "chosen_anchor_tech": chosen_tech,
                "ttl_obs": ttl_obs,
                "ttl_obs_price_cd": ttl_obs,
                "ttl_annual_metrics_same_year": _safe_float(
                    annual_ttl.loc[annual_ttl["year"] == int(ref_year_used), "ttl_eur_mwh"].iloc[0],
                    np.nan,
                )
                if np.isfinite(_safe_float(ref_year_used, np.nan))
                else np.nan,
                "ttl_anchor": ttl_anchor,
                "ttl_physical": ttl_anchor,
                "ttl_regression": np.nan,
                "ttl_method": "anchor_distributional",
                "tca_q95": ttl_anchor,
                "alpha": alpha,
                "alpha_effective": alpha,
                "corr_cd": corr_cd,
                "anchor_confidence": float(np.clip(1.0 - (_safe_float(dist_error, 0.0) / 80.0), 0.0, 1.0)) if np.isfinite(dist_error) else np.nan,
                "anchor_distribution_error_p90_p95": dist_error,
                "anchor_error_p90": p90_err,
                "anchor_error_p95": p95_err,
                "anchor_status": anchor_status,
                "dTCA_dCO2": dco2,
                "dTCA_dGas": dgas,
                "ttl_target": ttl_target,
                "required_co2_eur_t": required_co2,
                "required_gas_eur_mwh_th": required_gas,
                "co2_required_base": required_co2,
                "co2_required_gas_override": np.nan if gas_override_eur_mwh_th is None else required_co2,
                "co2_required_base_non_negative": required_co2 if np.isfinite(required_co2) else np.nan,
                "co2_required_gas_override_non_negative": required_co2 if gas_override_eur_mwh_th is not None and np.isfinite(required_co2) else np.nan,
                "warnings_quality": "",
            }
        ]
    )

    narrative = (
        "Q5 ancre TTL a partir d'un cout thermique explicite (fuel/eta + CO2*EF/eta + VOM), "
        "selectionne la techno marginale la plus explicative via fit distributionnel (p90/p95), "
        "et calcule required_co2/required_gas sans valeurs negatives."
    )

    return ModuleResult(
        module_id="Q5",
        run_id=run_id,
        selection=selection,
        assumptions_used=assumptions_subset(assumptions_df, Q5_PARAMS),
        kpis={
            "ttl_obs": ttl_obs,
            "chosen_anchor_tech": chosen_tech,
            "corr_cd": corr_cd,
            "anchor_distribution_error_p90_p95": dist_error,
            "dTCA_dCO2": dco2,
            "dTCA_dGas": dgas,
        },
        tables={"Q5_summary": summary},
        figures=[],
        narrative_md=narrative,
        checks=checks,
        warnings=warnings,
        mode=str(selection.get("mode", "HIST")).upper(),
        scenario_id=selection.get("scenario_id"),
        horizon_year=selection.get("horizon_year"),
    )
