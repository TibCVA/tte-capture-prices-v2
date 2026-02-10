"""Unified HIST+SCEN question runner with test ledger and comparison output."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.constants import DEFAULT_COUNTRIES
from src.modules.bundle_result import QuestionBundleResult
from src.modules.q1_transition import run_q1
from src.modules.q2_slope import run_q2
from src.modules.q3_exit import run_q3
from src.modules.q4_bess import run_q4
from src.modules.q5_thermal_anchor import run_q5
from src.modules.result import ModuleResult
from src.modules.test_registry import QuestionTestSpec, get_default_scenarios, get_question_tests
from src.scenario.phase2_engine import run_phase2_scenario
from src.storage import (
    load_scenario_annual_metrics,
    load_scenario_hourly,
    scenario_hourly_output_path,
)


def _safe_float(v: Any, default: float = np.nan) -> float:
    try:
        x = float(v)
        if np.isfinite(x):
            return x
        return float(default)
    except Exception:
        return float(default)


def _status_from_checks(checks: list[dict[str, Any]]) -> str:
    statuses = {str(c.get("status", "")).upper() for c in checks}
    if "FAIL" in statuses:
        return "FAIL"
    if "WARN" in statuses:
        return "WARN"
    return "PASS"


def _append_test_row(
    rows: list[dict[str, Any]],
    spec: QuestionTestSpec,
    status: str,
    value: Any,
    threshold: str,
    interpretation: str,
    scenario_id: str | None = None,
) -> None:
    rows.append(
        {
            "test_id": spec.test_id,
            "question_id": spec.question_id,
            "source_ref": spec.source_ref,
            "mode": spec.mode,
            "scenario_group": spec.scenario_group,
            "title": spec.title,
            "what_is_tested": spec.what_is_tested,
            "metric_rule": spec.metric_rule,
            "severity_if_fail": spec.severity_if_fail,
            "scenario_id": scenario_id or "",
            "status": status,
            "value": value,
            "threshold": threshold,
            "interpretation": interpretation,
        }
    )


def _selection_countries(selection: dict[str, Any], annual_hist: pd.DataFrame) -> list[str]:
    countries = selection.get("countries")
    if countries:
        return sorted(set([str(c) for c in countries]))
    if annual_hist is not None and not annual_hist.empty and "country" in annual_hist.columns:
        return sorted(annual_hist["country"].dropna().astype(str).unique().tolist())
    return list(DEFAULT_COUNTRIES)


def _selection_years(selection: dict[str, Any], annual_hist: pd.DataFrame) -> list[int]:
    years = selection.get("years")
    if years:
        return sorted(set([int(y) for y in years]))
    if annual_hist is not None and not annual_hist.empty and "year" in annual_hist.columns:
        return sorted(annual_hist["year"].dropna().astype(int).unique().tolist())
    return list(range(2018, 2025))


def _selection_scenario_years(selection: dict[str, Any], assumptions_phase2: pd.DataFrame, scenario_ids: list[str], countries: list[str]) -> list[int]:
    selected = selection.get("scenario_years")
    if selected:
        return sorted(set([int(y) for y in selected]))
    if assumptions_phase2 is None or assumptions_phase2.empty:
        return [2030, 2040]
    p2 = assumptions_phase2.copy()
    p2["scenario_id"] = p2["scenario_id"].astype(str)
    p2["country"] = p2["country"].astype(str)
    p2["year"] = pd.to_numeric(p2["year"], errors="coerce")
    scoped = p2[p2["scenario_id"].isin(scenario_ids) & p2["country"].isin(countries)]
    if scoped.empty:
        return [2030, 2040]
    return sorted(scoped["year"].dropna().astype(int).unique().tolist())


def _hourly_map_subset(hourly_hist_map: dict[tuple[str, int], pd.DataFrame], countries: list[str], years: list[int]) -> dict[tuple[str, int], pd.DataFrame]:
    out: dict[tuple[str, int], pd.DataFrame] = {}
    for c in countries:
        for y in years:
            key = (c, y)
            if key in hourly_hist_map:
                out[key] = hourly_hist_map[key]
    return out


def _load_scenario_annual_safe(scenario_id: str) -> pd.DataFrame:
    try:
        return load_scenario_annual_metrics(scenario_id)
    except Exception:
        return pd.DataFrame()


def _load_scenario_hourly_map(scenario_id: str, countries: list[str], years: list[int]) -> dict[tuple[str, int], pd.DataFrame]:
    out: dict[tuple[str, int], pd.DataFrame] = {}
    for c in countries:
        for y in years:
            try:
                out[(c, y)] = load_scenario_hourly(scenario_id, c, int(y))
            except Exception:
                continue
    return out


def _concat_hourly(country: str, years: list[int], hourly_map: dict[tuple[str, int], pd.DataFrame]) -> pd.DataFrame:
    chunks: list[pd.DataFrame] = []
    for y in years:
        key = (country, int(y))
        if key not in hourly_map:
            continue
        h = hourly_map[key].copy()
        h["year"] = int(y)
        chunks.append(h)
    if not chunks:
        return pd.DataFrame()
    return pd.concat(chunks, axis=0).sort_index()


def _phase2_commodity_daily(assumptions_phase2: pd.DataFrame, scenario_id: str, country: str, years: list[int]) -> pd.DataFrame:
    p2 = assumptions_phase2.copy()
    p2["scenario_id"] = p2["scenario_id"].astype(str)
    p2["country"] = p2["country"].astype(str)
    p2["year"] = pd.to_numeric(p2["year"], errors="coerce").astype("Int64")
    scoped = p2[
        (p2["scenario_id"] == str(scenario_id))
        & (p2["country"] == str(country))
        & (p2["year"].isin([int(y) for y in years]))
    ].copy()
    rows: list[pd.DataFrame] = []
    for _, row in scoped.iterrows():
        y = int(row["year"])
        idx = pd.date_range(f"{y}-01-01", f"{y}-12-31", freq="D")
        rows.append(
            pd.DataFrame(
                {
                    "date": idx,
                    "gas_price_eur_mwh_th": _safe_float(row.get("gas_eur_per_mwh_th"), np.nan),
                    "co2_price_eur_t": _safe_float(row.get("co2_eur_per_t"), np.nan),
                }
            )
        )
    if not rows:
        return pd.DataFrame(columns=["date", "gas_price_eur_mwh_th", "co2_price_eur_t"])
    out = pd.concat(rows, ignore_index=True)
    return out.dropna(subset=["gas_price_eur_mwh_th", "co2_price_eur_t"])


def _phase2_commodity_daily_high_both(assumptions_phase2: pd.DataFrame, country: str, years: list[int]) -> pd.DataFrame:
    p2 = assumptions_phase2.copy()
    p2["scenario_id"] = p2["scenario_id"].astype(str)
    p2["country"] = p2["country"].astype(str)
    p2["year"] = pd.to_numeric(p2["year"], errors="coerce").astype("Int64")
    rows: list[pd.DataFrame] = []
    for y in years:
        row_co2 = p2[(p2["scenario_id"] == "HIGH_CO2") & (p2["country"] == country) & (p2["year"] == int(y))]
        row_gas = p2[(p2["scenario_id"] == "HIGH_GAS") & (p2["country"] == country) & (p2["year"] == int(y))]
        if row_co2.empty or row_gas.empty:
            continue
        idx = pd.date_range(f"{int(y)}-01-01", f"{int(y)}-12-31", freq="D")
        rows.append(
            pd.DataFrame(
                {
                    "date": idx,
                    "gas_price_eur_mwh_th": _safe_float(row_gas.iloc[0].get("gas_eur_per_mwh_th"), np.nan),
                    "co2_price_eur_t": _safe_float(row_co2.iloc[0].get("co2_eur_per_t"), np.nan),
                }
            )
        )
    if not rows:
        return pd.DataFrame(columns=["date", "gas_price_eur_mwh_th", "co2_price_eur_t"])
    out = pd.concat(rows, ignore_index=True)
    return out.dropna(subset=["gas_price_eur_mwh_th", "co2_price_eur_t"])


def _ensure_scenario_outputs(
    scenario_id: str,
    countries: list[str],
    scenario_years: list[int],
    assumptions_phase2: pd.DataFrame,
    annual_hist: pd.DataFrame,
    hourly_hist_map: dict[tuple[str, int], pd.DataFrame],
) -> tuple[bool, str]:
    if scenario_id == "HIGH_BOTH":
        return True, "derived_scenario"

    annual = _load_scenario_annual_safe(scenario_id)
    missing_pairs: list[tuple[str, int]] = []

    if annual.empty:
        missing_pairs = [(c, y) for c in countries for y in scenario_years]
    else:
        for c in countries:
            for y in scenario_years:
                row = annual[(annual["country"].astype(str) == str(c)) & (pd.to_numeric(annual["year"], errors="coerce") == int(y))]
                if row.empty:
                    missing_pairs.append((c, y))
                elif not scenario_hourly_output_path(scenario_id, c, int(y)).exists():
                    missing_pairs.append((c, y))

    if not missing_pairs:
        return True, "already_available"

    try:
        run_phase2_scenario(
            scenario_id=scenario_id,
            countries=sorted(set([c for c, _ in missing_pairs])),
            years=sorted(set([y for _, y in missing_pairs])),
            assumptions_phase2=assumptions_phase2,
            annual_hist=annual_hist,
            hourly_hist_map=hourly_hist_map,
        )
    except Exception as exc:  # pragma: no cover
        return False, f"scenario_build_error: {exc}"

    return True, "built"


def _run_hist_module(
    question_id: str,
    annual_hist: pd.DataFrame,
    hourly_hist_map: dict[tuple[str, int], pd.DataFrame],
    assumptions_phase1: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
) -> tuple[ModuleResult, dict[str, ModuleResult]]:
    qid = question_id.upper()
    extra: dict[str, ModuleResult] = {}

    if qid == "Q1":
        res = run_q1(annual_hist, assumptions_phase1, {**selection, "mode": "HIST"}, run_id)
        return res, extra
    if qid == "Q2":
        res = run_q2(annual_hist, assumptions_phase1, {**selection, "mode": "HIST"}, run_id, hourly_by_country_year=hourly_hist_map)
        return res, extra
    if qid == "Q3":
        res = run_q3(annual_hist, hourly_hist_map, assumptions_phase1, {**selection, "mode": "HIST"}, run_id)
        return res, extra
    if qid == "Q4":
        country = str(selection.get("country", "FR"))
        year = int(selection.get("year", max(_selection_years(selection, annual_hist))))
        key = (country, year)
        if key not in hourly_hist_map:
            raise ValueError(f"Missing historical hourly data for {country}-{year}.")
        hourly = hourly_hist_map[key]
        common_sel = {
            **selection,
            "country": country,
            "year": year,
            "mode": "HIST",
            "scenario_id": None,
            "horizon_year": year,
        }
        res = run_q4(hourly, assumptions_phase1, common_sel, run_id, dispatch_mode="SURPLUS_FIRST")
        extra["HIST_PRICE_ARBITRAGE_SIMPLE"] = run_q4(
            hourly,
            assumptions_phase1,
            common_sel,
            f"{run_id}_HIST_PRICE",
            dispatch_mode="PRICE_ARBITRAGE_SIMPLE",
        )
        extra["HIST_PV_COLOCATED"] = run_q4(
            hourly,
            assumptions_phase1,
            common_sel,
            f"{run_id}_HIST_PV",
            dispatch_mode="PV_COLOCATED",
        )
        return res, extra
    if qid == "Q5":
        country = str(selection.get("country", "FR"))
        years = sorted(set([int(y) for y in selection.get("years", _selection_years(selection, annual_hist))]))
        hourly = _concat_hourly(country, years, hourly_hist_map)
        if hourly.empty:
            raise ValueError(f"Missing historical hourly data for {country} and years={years}.")
        res = run_q5(
            hourly_df=hourly,
            assumptions_df=assumptions_phase1,
            selection={
                "country": country,
                "marginal_tech": selection.get("marginal_tech", "CCGT"),
                "mode": "HIST",
            },
            run_id=run_id,
            commodity_daily=selection.get("commodity_daily"),
            ttl_target_eur_mwh=_safe_float(selection.get("ttl_target_eur_mwh"), 120.0),
            gas_override_eur_mwh_th=selection.get("gas_override_eur_mwh_th"),
            co2_override_eur_t=selection.get("co2_override_eur_t"),
        )
        return res, extra

    raise ValueError(f"Unsupported question_id={question_id}")


def _run_scen_module(
    question_id: str,
    scenario_id: str,
    annual_hist: pd.DataFrame,
    assumptions_phase1: pd.DataFrame,
    assumptions_phase2: pd.DataFrame,
    selection: dict[str, Any],
    scenario_years: list[int],
) -> ModuleResult | None:
    qid = question_id.upper()
    countries = _selection_countries(selection, annual_hist)
    run_id = f"{selection.get('run_id')}_{scenario_id}"

    if qid in {"Q1", "Q2", "Q3"}:
        annual_scen = _load_scenario_annual_safe(scenario_id)
        if annual_scen.empty:
            return None
        annual_scen = annual_scen[
            annual_scen["country"].astype(str).isin(countries)
            & pd.to_numeric(annual_scen["year"], errors="coerce").isin(scenario_years)
        ].copy()
        if annual_scen.empty:
            return None
        scen_sel = {
            **selection,
            "mode": "SCEN",
            "scenario_id": scenario_id,
            "horizon_year": max(scenario_years) if scenario_years else None,
            "years": scenario_years,
        }
        if qid == "Q1":
            return run_q1(annual_scen, assumptions_phase1, scen_sel, run_id)
        if qid == "Q2":
            hourly_map = _load_scenario_hourly_map(scenario_id, countries, scenario_years)
            return run_q2(annual_scen, assumptions_phase1, scen_sel, run_id, hourly_by_country_year=hourly_map)
        hourly_map = _load_scenario_hourly_map(scenario_id, countries, scenario_years)
        assumptions_q3 = assumptions_phase1.copy()
        if len(scenario_years) < 3:
            mask = assumptions_q3["param_name"].astype(str) == "trend_window_years"
            if mask.any():
                assumptions_q3.loc[mask, "param_value"] = 2
        return run_q3(annual_scen, hourly_map, assumptions_q3, scen_sel, run_id)

    if qid == "Q4":
        country = str(selection.get("country", "FR"))
        year = int(selection.get("horizon_year", max(scenario_years) if scenario_years else 2040))
        try:
            hourly = load_scenario_hourly(scenario_id, country, year)
        except Exception:
            return None
        scen_sel = {
            **selection,
            "country": country,
            "year": year,
            "mode": "SCEN",
            "scenario_id": scenario_id,
            "horizon_year": year,
        }
        return run_q4(hourly, assumptions_phase1, scen_sel, run_id, dispatch_mode="SURPLUS_FIRST")

    if qid == "Q5":
        country = str(selection.get("country", "FR"))
        years = sorted(set([int(y) for y in scenario_years]))
        if scenario_id == "HIGH_BOTH":
            base_sid = "BASE"
            hourly_map = _load_scenario_hourly_map(base_sid, [country], years)
            hourly = _concat_hourly(country, years, hourly_map)
            commodity = _phase2_commodity_daily_high_both(assumptions_phase2, country, years)
        else:
            hourly_map = _load_scenario_hourly_map(scenario_id, [country], years)
            hourly = _concat_hourly(country, years, hourly_map)
            commodity = _phase2_commodity_daily(assumptions_phase2, scenario_id, country, years)
        if hourly.empty:
            return None
        scen_sel = {
            **selection,
            "country": country,
            "mode": "SCEN",
            "scenario_id": scenario_id,
            "horizon_year": max(years) if years else None,
        }
        return run_q5(
            hourly_df=hourly,
            assumptions_df=assumptions_phase1,
            selection=scen_sel,
            run_id=run_id,
            commodity_daily=commodity,
            ttl_target_eur_mwh=_safe_float(selection.get("ttl_target_eur_mwh"), 120.0),
        )

    return None


def _q1_comparison(hist_result: ModuleResult, scen_results: dict[str, ModuleResult]) -> pd.DataFrame:
    hist = hist_result.tables.get("Q1_country_summary", pd.DataFrame()).copy()
    if hist.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for sid, res in scen_results.items():
        scen = res.tables.get("Q1_country_summary", pd.DataFrame())
        if scen.empty:
            continue
        merged = hist[["country", "bascule_year_market"]].merge(
            scen[["country", "bascule_year_market"]],
            on="country",
            how="inner",
            suffixes=("_hist", "_scen"),
        )
        for _, r in merged.iterrows():
            h = _safe_float(r.get("bascule_year_market_hist"), np.nan)
            s = _safe_float(r.get("bascule_year_market_scen"), np.nan)
            rows.append(
                {
                    "country": r["country"],
                    "scenario_id": sid,
                    "metric": "bascule_year_market",
                    "hist_value": h,
                    "scen_value": s,
                    "delta": s - h if np.isfinite(h) and np.isfinite(s) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def _q2_comparison(hist_result: ModuleResult, scen_results: dict[str, ModuleResult]) -> pd.DataFrame:
    hist = hist_result.tables.get("Q2_country_slopes", pd.DataFrame()).copy()
    if hist.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for sid, res in scen_results.items():
        scen = res.tables.get("Q2_country_slopes", pd.DataFrame())
        if scen.empty:
            continue
        merged = hist[["country", "tech", "slope"]].merge(
            scen[["country", "tech", "slope"]],
            on=["country", "tech"],
            how="inner",
            suffixes=("_hist", "_scen"),
        )
        for _, r in merged.iterrows():
            h = _safe_float(r.get("slope_hist"), np.nan)
            s = _safe_float(r.get("slope_scen"), np.nan)
            rows.append(
                {
                    "country": r["country"],
                    "tech": r["tech"],
                    "scenario_id": sid,
                    "metric": "slope",
                    "hist_value": h,
                    "scen_value": s,
                    "delta": s - h if np.isfinite(h) and np.isfinite(s) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def _q3_comparison(hist_result: ModuleResult, scen_results: dict[str, ModuleResult]) -> pd.DataFrame:
    hist = hist_result.tables.get("Q3_status", pd.DataFrame()).copy()
    if hist.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for sid, res in scen_results.items():
        scen = res.tables.get("Q3_status", pd.DataFrame())
        if scen.empty:
            continue
        merged = hist[["country", "inversion_k_demand", "inversion_r_mustrun"]].merge(
            scen[["country", "inversion_k_demand", "inversion_r_mustrun"]],
            on="country",
            how="inner",
            suffixes=("_hist", "_scen"),
        )
        for _, r in merged.iterrows():
            hk = _safe_float(r.get("inversion_k_demand_hist"), np.nan)
            sk = _safe_float(r.get("inversion_k_demand_scen"), np.nan)
            hr = _safe_float(r.get("inversion_r_mustrun_hist"), np.nan)
            sr = _safe_float(r.get("inversion_r_mustrun_scen"), np.nan)
            rows.append(
                {
                    "country": r["country"],
                    "scenario_id": sid,
                    "metric": "inversion_k_demand",
                    "hist_value": hk,
                    "scen_value": sk,
                    "delta": sk - hk if np.isfinite(hk) and np.isfinite(sk) else np.nan,
                }
            )
            rows.append(
                {
                    "country": r["country"],
                    "scenario_id": sid,
                    "metric": "inversion_r_mustrun",
                    "hist_value": hr,
                    "scen_value": sr,
                    "delta": sr - hr if np.isfinite(hr) and np.isfinite(sr) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def _q4_comparison(hist_result: ModuleResult, scen_results: dict[str, ModuleResult], extra_hist: dict[str, ModuleResult]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    hist = hist_result.tables.get("Q4_sizing_summary", pd.DataFrame())
    if not hist.empty:
        hrow = hist.iloc[0]
        for sid, res in scen_results.items():
            scen = res.tables.get("Q4_sizing_summary", pd.DataFrame())
            if scen.empty:
                continue
            srow = scen.iloc[0]
            for metric in ["far_after", "surplus_unabs_energy_after", "pv_capture_price_after"]:
                h = _safe_float(hrow.get(metric), np.nan)
                s = _safe_float(srow.get(metric), np.nan)
                rows.append(
                    {
                        "country": str(hrow.get("country", "")),
                        "scenario_id": sid,
                        "metric": metric,
                        "hist_value": h,
                        "scen_value": s,
                        "delta": s - h if np.isfinite(h) and np.isfinite(s) else np.nan,
                    }
                )
        for mode_key, mode_res in extra_hist.items():
            mode_summary = mode_res.tables.get("Q4_sizing_summary", pd.DataFrame())
            if mode_summary.empty:
                continue
            mrow = mode_summary.iloc[0]
            rows.append(
                {
                    "country": str(mrow.get("country", "")),
                    "scenario_id": mode_key,
                    "metric": "far_after",
                    "hist_value": _safe_float(hrow.get("far_after"), np.nan),
                    "scen_value": _safe_float(mrow.get("far_after"), np.nan),
                    "delta": _safe_float(mrow.get("far_after"), np.nan) - _safe_float(hrow.get("far_after"), np.nan),
                }
            )
    return pd.DataFrame(rows)


def _q5_comparison(hist_result: ModuleResult, scen_results: dict[str, ModuleResult]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    hist = hist_result.tables.get("Q5_summary", pd.DataFrame())
    if hist.empty:
        return pd.DataFrame()
    hrow = hist.iloc[0]
    for sid, res in scen_results.items():
        scen = res.tables.get("Q5_summary", pd.DataFrame())
        if scen.empty:
            continue
        srow = scen.iloc[0]
        for metric in ["ttl_obs", "tca_q95", "co2_required_base"]:
            h = _safe_float(hrow.get(metric), np.nan)
            s = _safe_float(srow.get(metric), np.nan)
            rows.append(
                {
                    "country": str(hrow.get("country", "")),
                    "scenario_id": sid,
                    "metric": metric,
                    "hist_value": h,
                    "scen_value": s,
                    "delta": s - h if np.isfinite(h) and np.isfinite(s) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def _comparison_for_question(
    question_id: str,
    hist_result: ModuleResult,
    scen_results: dict[str, ModuleResult],
    extra_hist: dict[str, ModuleResult],
) -> pd.DataFrame:
    qid = question_id.upper()
    if qid == "Q1":
        return _q1_comparison(hist_result, scen_results)
    if qid == "Q2":
        return _q2_comparison(hist_result, scen_results)
    if qid == "Q3":
        return _q3_comparison(hist_result, scen_results)
    if qid == "Q4":
        return _q4_comparison(hist_result, scen_results, extra_hist)
    if qid == "Q5":
        return _q5_comparison(hist_result, scen_results)
    return pd.DataFrame()


def _evaluate_test_ledger(
    question_id: str,
    specs: list[QuestionTestSpec],
    hist_result: ModuleResult,
    scen_results: dict[str, ModuleResult],
    extra_hist: dict[str, ModuleResult],
) -> pd.DataFrame:
    qid = question_id.upper()
    rows: list[dict[str, Any]] = []

    for spec in specs:
        if spec.mode == "HIST":
            if qid == "Q1":
                panel = hist_result.tables.get("Q1_year_panel", pd.DataFrame())
                summary = hist_result.tables.get("Q1_country_summary", pd.DataFrame())
                if spec.test_id == "Q1-H-01":
                    ok = (not panel.empty) and ("stage2_market_score" in panel.columns)
                    value = float(panel["stage2_market_score"].mean()) if ok else np.nan
                    _append_test_row(rows, spec, "PASS" if ok else "FAIL", value, "score present", "Le score de bascule marche est exploitable.")
                elif spec.test_id == "Q1-H-02":
                    req = {"sr_energy", "far_energy", "ir_p10"}
                    ok = req.issubset(set(panel.columns))
                    _append_test_row(rows, spec, "PASS" if ok else "FAIL", ",".join(sorted(req & set(panel.columns))), "SR/FAR/IR presents", "Le stress physique est calculable.")
                elif spec.test_id == "Q1-H-03":
                    if summary.empty:
                        _append_test_row(rows, spec, "NON_TESTABLE", "", "summary non vide", "Pas de resume Q1 historique.")
                    else:
                        share = float(
                            (
                                summary["bascule_year_market"].notna()
                                & summary["bascule_year_physical"].notna()
                            ).mean()
                        )
                        status = "PASS" if share >= 0.5 else "WARN"
                        _append_test_row(rows, spec, status, f"{share:.2%}", ">=50%", "Concordance mesuree entre bascules marche et physique.")
                else:
                    if summary.empty:
                        _append_test_row(rows, spec, "NON_TESTABLE", "", "summary non vide", "Impossible d'evaluer robustesse sans bascules.")
                    else:
                        conf = float(pd.to_numeric(summary["bascule_confidence"], errors="coerce").mean())
                        status = "PASS" if conf >= 0.6 else "WARN"
                        _append_test_row(rows, spec, status, f"{conf:.3f}", "confidence moyenne >=0.60", "Proxy de robustesse du diagnostic de bascule.")
            elif qid == "Q2":
                slopes = hist_result.tables.get("Q2_country_slopes", pd.DataFrame())
                drivers = hist_result.tables.get("Q2_driver_correlations", pd.DataFrame())
                if spec.test_id == "Q2-H-01":
                    status = "PASS" if not slopes.empty else "FAIL"
                    _append_test_row(rows, spec, status, int(len(slopes)), ">0 lignes", "Les pentes historiques sont calculees.")
                elif spec.test_id == "Q2-H-02":
                    req = {"r2", "p_value", "n"}
                    ok = req.issubset(set(slopes.columns)) and not slopes.empty
                    _append_test_row(rows, spec, "PASS" if ok else "FAIL", ",".join(sorted(req & set(slopes.columns))), "r2,p_value,n disponibles", "La robustesse statistique est lisible.")
                else:
                    status = "PASS" if not drivers.empty else "WARN"
                    _append_test_row(rows, spec, status, int(len(drivers)), ">0 lignes", "Les drivers de pente sont disponibles.")
            elif qid == "Q3":
                out = hist_result.tables.get("Q3_status", pd.DataFrame())
                if spec.test_id == "Q3-H-01":
                    status = "PASS" if not out.empty else "FAIL"
                    _append_test_row(rows, spec, status, int(len(out)), ">0 lignes", "Les tendances historiques sont calculees.")
                else:
                    allowed = {"degradation", "stabilisation", "amelioration", "transition_partielle", "hors_scope_stage2"}
                    ok = (not out.empty) and out["status"].astype(str).isin(allowed).all()
                    _append_test_row(rows, spec, "PASS" if ok else "WARN", int(out["status"].nunique()) if not out.empty else 0, "status valides", "Les statuts business sont renseignes.")
            elif qid == "Q4":
                if spec.test_id == "Q4-H-01":
                    expected_modes = {"HIST_PRICE_ARBITRAGE_SIMPLE", "HIST_PV_COLOCATED"}
                    ok = expected_modes.issubset(set(extra_hist.keys()))
                    _append_test_row(rows, spec, "PASS" if ok else "FAIL", ",".join(sorted(extra_hist.keys())), "3 modes executes", "Les trois modes Q4 sont disponibles.")
                else:
                    all_checks = hist_result.checks + [c for r in extra_hist.values() for c in r.checks]
                    has_fail = any(str(c.get("status", "")).upper() == "FAIL" for c in all_checks)
                    _append_test_row(rows, spec, "PASS" if not has_fail else "FAIL", _status_from_checks(all_checks), "pas de FAIL", "Les invariants physiques batterie sont respectes.")
            elif qid == "Q5":
                out = hist_result.tables.get("Q5_summary", pd.DataFrame())
                if spec.test_id == "Q5-H-01":
                    if out.empty:
                        _append_test_row(rows, spec, "FAIL", "", "summary non vide", "Q5 historique absent.")
                    else:
                        row = out.iloc[0]
                        ok = np.isfinite(_safe_float(row.get("ttl_obs"))) and np.isfinite(_safe_float(row.get("tca_q95")))
                        _append_test_row(rows, spec, "PASS" if ok else "WARN", f"ttl={row.get('ttl_obs')}, tca={row.get('tca_q95')}", "ttl/tca finis", "L'ancre thermique est quantifiable.")
                else:
                    if out.empty:
                        _append_test_row(rows, spec, "FAIL", "", "summary non vide", "Q5 historique absent.")
                    else:
                        row = out.iloc[0]
                        ok = _safe_float(row.get("dTCA_dCO2"), -1.0) > 0 and _safe_float(row.get("dTCA_dGas"), -1.0) > 0
                        _append_test_row(rows, spec, "PASS" if ok else "FAIL", f"dCO2={row.get('dTCA_dCO2')}, dGas={row.get('dTCA_dGas')}", ">0", "Sensibilites analytiques coherentes.")
        else:
            if not scen_results:
                _append_test_row(rows, spec, "NON_TESTABLE", "", "scenario runs disponibles", "Aucun scenario exploitable.")
                continue
            for sid, scen_res in scen_results.items():
                if qid == "Q1":
                    summary = scen_res.tables.get("Q1_country_summary", pd.DataFrame())
                    if spec.test_id == "Q1-S-01":
                        ok = not summary.empty
                        _append_test_row(rows, spec, "PASS" if ok else "FAIL", int(len(summary)), ">0 lignes", "La bascule projetee est produite.", sid)
                    elif spec.test_id == "Q1-S-02":
                        val = int(summary["bascule_year_market"].notna().sum()) if not summary.empty else 0
                        _append_test_row(rows, spec, "PASS" if val > 0 else "WARN", val, ">=1 bascule", "Le scenario fournit une variation exploitable.", sid)
                    else:
                        panel = scen_res.tables.get("Q1_year_panel", pd.DataFrame())
                        if panel.empty or "regime_coherence" not in panel.columns:
                            _append_test_row(rows, spec, "NON_TESTABLE", "", "regime_coherence present", "Donnees insuffisantes.", sid)
                        else:
                            share = float((pd.to_numeric(panel["regime_coherence"], errors="coerce") >= 0.55).mean())
                            _append_test_row(rows, spec, "PASS" if share >= 0.5 else "WARN", f"{share:.2%}", ">=50% lignes >=0.55", "La coherence scenario est lisible.", sid)
                elif qid == "Q2":
                    slopes = scen_res.tables.get("Q2_country_slopes", pd.DataFrame())
                    if spec.test_id == "Q2-S-01":
                        _append_test_row(rows, spec, "PASS" if not slopes.empty else "FAIL", int(len(slopes)), ">0 lignes", "Pentes prospectives calculees.", sid)
                    else:
                        robust_share = float((slopes["robust_flag"] == "ROBUST").mean()) if not slopes.empty and "robust_flag" in slopes.columns else np.nan
                        status = "PASS" if np.isfinite(robust_share) and robust_share >= 0.3 else "WARN"
                        _append_test_row(rows, spec, status, f"{robust_share:.2%}" if np.isfinite(robust_share) else "", ">=30% robustes", "Delta de pente interpretable avec robustesse.", sid)
                elif qid == "Q3":
                    out = scen_res.tables.get("Q3_status", pd.DataFrame())
                    if spec.test_id == "Q3-S-01":
                        req = {"inversion_k_demand", "inversion_r_mustrun", "additional_absorbed_needed_TWh_year"}
                        ok = (not out.empty) and req.issubset(set(out.columns))
                        _append_test_row(rows, spec, "PASS" if ok else "FAIL", int(len(out)), "colonnes inversion presentes", "Les ordres de grandeur d'inversion sont quantifies.", sid)
                    else:
                        ok = (not out.empty) and out["status"].notna().all()
                        _append_test_row(rows, spec, "PASS" if ok else "WARN", int(out["status"].nunique()) if not out.empty else 0, "status renseignes", "La lecture de transition phase 3 est possible.", sid)
                elif qid == "Q4":
                    out = scen_res.tables.get("Q4_sizing_summary", pd.DataFrame())
                    if spec.test_id == "Q4-S-01":
                        _append_test_row(rows, spec, "PASS" if not out.empty else "FAIL", int(len(out)), ">0 lignes", "Resultats Q4 prospectifs disponibles.", sid)
                    else:
                        if out.empty:
                            _append_test_row(rows, spec, "NON_TESTABLE", "", "summary non vide", "Pas de sortie scenario.", sid)
                        else:
                            row = out.iloc[0]
                            val = _safe_float(row.get("pv_capture_price_after"), np.nan)
                            _append_test_row(rows, spec, "PASS" if np.isfinite(val) else "WARN", val, "capture apres finite", "Sensibilite valeur exploitable.", sid)
                elif qid == "Q5":
                    out = scen_res.tables.get("Q5_summary", pd.DataFrame())
                    if spec.test_id == "Q5-S-01":
                        _append_test_row(rows, spec, "PASS" if not out.empty else "FAIL", int(len(out)), ">0 lignes", "Sensibilites scenario calculees.", sid)
                    else:
                        if out.empty:
                            _append_test_row(rows, spec, "NON_TESTABLE", "", "co2_required present", "Sortie scenario absente.", sid)
                        else:
                            row = out.iloc[0]
                            v = _safe_float(row.get("co2_required_base"), np.nan)
                            _append_test_row(rows, spec, "PASS" if np.isfinite(v) else "WARN", v, "valeur finie", "CO2 requis interpretable.", sid)
    return pd.DataFrame(rows)


def run_question_bundle(
    question_id: str,
    annual_hist: pd.DataFrame,
    hourly_hist_map: dict[tuple[str, int], pd.DataFrame],
    assumptions_phase1: pd.DataFrame,
    assumptions_phase2: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
) -> QuestionBundleResult:
    qid = str(question_id).upper()
    countries = _selection_countries(selection, annual_hist)
    years = _selection_years(selection, annual_hist)
    scenario_ids = [str(s) for s in selection.get("scenario_ids", get_default_scenarios(qid))]
    scenario_ids = [s for s in scenario_ids if s]
    scenario_years = _selection_scenario_years(selection, assumptions_phase2, [s for s in scenario_ids if s != "HIGH_BOTH"], countries)

    hist_sel = {**selection, "countries": countries, "years": years, "mode": "HIST", "run_id": run_id}
    hist_hourly_map = _hourly_map_subset(hourly_hist_map, countries, years)
    hist_result, extra_hist = _run_hist_module(
        question_id=qid,
        annual_hist=annual_hist,
        hourly_hist_map=hist_hourly_map,
        assumptions_phase1=assumptions_phase1,
        selection=hist_sel,
        run_id=f"{run_id}_HIST",
    )

    scen_results: dict[str, ModuleResult] = {}
    warnings: list[str] = []

    for sid in scenario_ids:
        ok, reason = _ensure_scenario_outputs(
            scenario_id=sid,
            countries=countries,
            scenario_years=scenario_years,
            assumptions_phase2=assumptions_phase2,
            annual_hist=annual_hist,
            hourly_hist_map=hourly_hist_map,
        )
        if not ok:
            warnings.append(f"{sid}: {reason}")
            continue
        scen_res = _run_scen_module(
            question_id=qid,
            scenario_id=sid,
            annual_hist=annual_hist,
            assumptions_phase1=assumptions_phase1,
            assumptions_phase2=assumptions_phase2,
            selection={**selection, "run_id": run_id},
            scenario_years=scenario_years,
        )
        if scen_res is None:
            warnings.append(f"{sid}: scenario result non disponible.")
            continue
        scen_results[sid] = scen_res

    specs = get_question_tests(qid)
    ledger = _evaluate_test_ledger(qid, specs, hist_result, scen_results, extra_hist)
    comparison = _comparison_for_question(qid, hist_result, scen_results, extra_hist)

    checks: list[dict[str, Any]] = []
    for c in hist_result.checks:
        checks.append({**c, "scope": "HIST", "scenario_id": ""})
    for sid, scen_res in scen_results.items():
        for c in scen_res.checks:
            checks.append({**c, "scope": "SCEN", "scenario_id": sid})

    if not ledger.empty:
        n_fail = int((ledger["status"].astype(str) == "FAIL").sum())
        n_warn = int((ledger["status"].astype(str) == "WARN").sum())
        checks.append(
            {
                "status": "FAIL" if n_fail > 0 else ("WARN" if n_warn > 0 else "PASS"),
                "code": "BUNDLE_LEDGER_STATUS",
                "message": f"ledger: FAIL={n_fail}, WARN={n_warn}",
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        )

    warnings.extend(hist_result.warnings)
    for sid, scen_res in scen_results.items():
        for w in scen_res.warnings:
            warnings.append(f"{sid}: {w}")

    overall = _status_from_checks(checks)
    n_pass = int((ledger["status"] == "PASS").sum()) if not ledger.empty else 0
    n_warn = int((ledger["status"] == "WARN").sum()) if not ledger.empty else 0
    n_fail = int((ledger["status"] == "FAIL").sum()) if not ledger.empty else 0
    n_nt = int((ledger["status"] == "NON_TESTABLE").sum()) if not ledger.empty else 0

    narrative = (
        f"Analyse complete {qid}: historique + prospectif en un seul run. "
        f"Statut global={overall}. Tests PASS={n_pass}, WARN={n_warn}, FAIL={n_fail}, NON_TESTABLE={n_nt}. "
        "Les resultats sont separes entre historique et scenarios, puis compares dans une table unique."
    )

    return QuestionBundleResult(
        question_id=qid,
        run_id=run_id,
        selection={
            **selection,
            "countries": countries,
            "years": years,
            "scenario_ids": scenario_ids,
            "scenario_years": scenario_years,
        },
        hist_result=hist_result,
        scen_results=scen_results,
        test_ledger=ledger,
        comparison_table=comparison,
        checks=checks,
        warnings=warnings,
        narrative_md=narrative,
    )
