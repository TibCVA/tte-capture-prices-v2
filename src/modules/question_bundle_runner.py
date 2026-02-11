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


DEFAULT_SCENARIO_YEARS = list(range(2025, 2036))


def _safe_float(v: Any, default: float = np.nan) -> float:
    try:
        x = float(v)
        if np.isfinite(x):
            return x
        return float(default)
    except Exception:
        return float(default)


def _max_finite(values: pd.Series, default: float = 0.0) -> float:
    arr = pd.to_numeric(values, errors="coerce").to_numpy(dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float(default)
    return float(np.max(arr))


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
        return list(DEFAULT_SCENARIO_YEARS)
    p2 = assumptions_phase2.copy()
    p2["scenario_id"] = p2["scenario_id"].astype(str)
    p2["country"] = p2["country"].astype(str)
    p2["year"] = pd.to_numeric(p2["year"], errors="coerce")
    scoped = p2[p2["scenario_id"].isin(scenario_ids) & p2["country"].isin(countries)]
    if scoped.empty:
        return list(DEFAULT_SCENARIO_YEARS)
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


def _pick_country_year(country: str, preferred_year: int, candidate_years: list[int], hourly_map: dict[tuple[str, int], pd.DataFrame]) -> int | None:
    candidates = [int(preferred_year)] + [int(y) for y in candidate_years if int(y) != int(preferred_year)]
    for y in candidates:
        if (country, int(y)) in hourly_map:
            return int(y)
    return None


def _merge_tables(results: list[ModuleResult]) -> dict[str, pd.DataFrame]:
    table_names: set[str] = set()
    for r in results:
        table_names.update(r.tables.keys())
    merged: dict[str, pd.DataFrame] = {}
    for name in sorted(table_names):
        parts = [r.tables[name] for r in results if name in r.tables and isinstance(r.tables[name], pd.DataFrame) and not r.tables[name].empty]
        if parts:
            merged[name] = pd.concat(parts, ignore_index=True)
        else:
            merged[name] = pd.DataFrame()
    return merged


def _merge_module_results(
    results: list[ModuleResult],
    module_id: str,
    run_id: str,
    selection: dict[str, Any],
    mode: str,
    scenario_id: str | None,
    horizon_year: int | None,
    narrative_title: str,
) -> ModuleResult:
    if not results:
        return ModuleResult(
            module_id=module_id,
            run_id=run_id,
            selection=selection,
            assumptions_used=[],
            kpis={"n_runs": 0, "n_countries": 0},
            tables={},
            figures=[],
            narrative_md=f"{narrative_title}: aucune sortie disponible.",
            checks=[{"status": "FAIL", "code": f"{module_id}_NO_RESULT", "message": "Aucune sortie module disponible."}],
            warnings=["Aucun result mergeable."],
            mode=mode,
            scenario_id=scenario_id,
            horizon_year=horizon_year,
        )

    assumptions_used = results[0].assumptions_used
    tables = _merge_tables(results)
    checks = [c for r in results for c in r.checks]
    warnings = [w for r in results for w in r.warnings]
    countries = sorted({str(r.selection.get("country", "")) for r in results if str(r.selection.get("country", ""))})
    total_time = float(sum(_safe_float(r.kpis.get("compute_time_sec"), 0.0) for r in results))

    kpis = {
        "n_runs": int(len(results)),
        "n_countries": int(len(countries)),
        "countries": countries,
        "compute_time_sec_total": total_time,
    }
    if module_id == "Q4":
        kpis["cache_hit_share"] = float(np.mean([1.0 if bool(r.kpis.get("cache_hit", False)) else 0.0 for r in results]))

    narrative = (
        f"{narrative_title}: aggregation multi-pays ({len(countries)} pays). "
        "Les tables detaillees conservent les lignes par pays."
    )

    return ModuleResult(
        module_id=module_id,
        run_id=run_id,
        selection=selection,
        assumptions_used=assumptions_used,
        kpis=kpis,
        tables=tables,
        figures=[],
        narrative_md=narrative,
        checks=checks if checks else [{"status": "PASS", "code": f"{module_id}_MERGE_PASS", "message": "Merge multi-pays ok."}],
        warnings=warnings,
        mode=mode,
        scenario_id=scenario_id,
        horizon_year=horizon_year,
    )


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
        res = run_q1(
            annual_hist,
            assumptions_phase1,
            {**selection, "mode": "HIST"},
            run_id,
            hourly_by_country_year=hourly_hist_map,
        )
        return res, extra
    if qid == "Q2":
        res = run_q2(annual_hist, assumptions_phase1, {**selection, "mode": "HIST"}, run_id, hourly_by_country_year=hourly_hist_map)
        return res, extra
    if qid == "Q3":
        res = run_q3(annual_hist, hourly_hist_map, assumptions_phase1, {**selection, "mode": "HIST"}, run_id)
        return res, extra
    if qid == "Q4":
        countries = _selection_countries(selection, annual_hist)
        candidate_years = _selection_years(selection, annual_hist)
        preferred_year = int(selection.get("year", max(candidate_years) if candidate_years else 2024))

        hist_runs: list[ModuleResult] = []
        mode_price_runs: list[ModuleResult] = []
        mode_pv_runs: list[ModuleResult] = []
        for country in countries:
            year = _pick_country_year(country, preferred_year, candidate_years, hourly_hist_map)
            if year is None:
                continue
            hourly = hourly_hist_map[(country, year)]
            common_sel = {
                **selection,
                "country": country,
                "year": int(year),
                "mode": "HIST",
                "scenario_id": None,
                "horizon_year": int(year),
            }
            hist_runs.append(run_q4(hourly, assumptions_phase1, common_sel, f"{run_id}_{country}", dispatch_mode="SURPLUS_FIRST"))
            mode_price_runs.append(
                run_q4(
                    hourly,
                    assumptions_phase1,
                    common_sel,
                    f"{run_id}_{country}_HIST_PRICE",
                    dispatch_mode="PRICE_ARBITRAGE_SIMPLE",
                )
            )
            mode_pv_runs.append(
                run_q4(
                    hourly,
                    assumptions_phase1,
                    common_sel,
                    f"{run_id}_{country}_HIST_PV",
                    dispatch_mode="PV_COLOCATED",
                )
            )
        if not hist_runs:
            raise ValueError("Missing historical hourly data for selected countries in Q4.")
        res = _merge_module_results(
            hist_runs,
            module_id="Q4",
            run_id=run_id,
            selection={**selection, "countries": countries},
            mode="HIST",
            scenario_id=None,
            horizon_year=preferred_year,
            narrative_title="Q4 historique",
        )
        extra["HIST_PRICE_ARBITRAGE_SIMPLE"] = _merge_module_results(
            mode_price_runs,
            module_id="Q4",
            run_id=f"{run_id}_HIST_PRICE",
            selection={**selection, "countries": countries, "dispatch_mode": "PRICE_ARBITRAGE_SIMPLE"},
            mode="HIST",
            scenario_id=None,
            horizon_year=preferred_year,
            narrative_title="Q4 historique mode PRICE_ARBITRAGE_SIMPLE",
        )
        extra["HIST_PV_COLOCATED"] = _merge_module_results(
            mode_pv_runs,
            module_id="Q4",
            run_id=f"{run_id}_HIST_PV",
            selection={**selection, "countries": countries, "dispatch_mode": "PV_COLOCATED"},
            mode="HIST",
            scenario_id=None,
            horizon_year=preferred_year,
            narrative_title="Q4 historique mode PV_COLOCATED",
        )
        return res, extra
    if qid == "Q5":
        countries = _selection_countries(selection, annual_hist)
        years = sorted(set([int(y) for y in selection.get("years", _selection_years(selection, annual_hist))]))
        runs: list[ModuleResult] = []
        tech_map = selection.get("marginal_tech_by_country", {})
        for country in countries:
            hourly = _concat_hourly(country, years, hourly_hist_map)
            if hourly.empty:
                continue
            marginal_tech = (
                str(tech_map.get(country, selection.get("marginal_tech", "CCGT"))).upper()
                if isinstance(tech_map, dict)
                else str(selection.get("marginal_tech", "CCGT")).upper()
            )
            runs.append(
                run_q5(
                    hourly_df=hourly,
                    assumptions_df=assumptions_phase1,
                    selection={
                        "country": country,
                        "marginal_tech": marginal_tech,
                        "mode": "HIST",
                    },
                    run_id=f"{run_id}_{country}",
                    commodity_daily=selection.get("commodity_daily"),
                    ttl_target_eur_mwh=_safe_float(selection.get("ttl_target_eur_mwh"), 120.0),
                    gas_override_eur_mwh_th=selection.get("gas_override_eur_mwh_th"),
                    co2_override_eur_t=selection.get("co2_override_eur_t"),
                )
            )
        if not runs:
            raise ValueError(f"Missing historical hourly data for countries={countries} and years={years}.")
        res = _merge_module_results(
            runs,
            module_id="Q5",
            run_id=run_id,
            selection={**selection, "countries": countries},
            mode="HIST",
            scenario_id=None,
            horizon_year=max(years) if years else None,
            narrative_title="Q5 historique",
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
            hourly_map = _load_scenario_hourly_map(scenario_id, countries, scenario_years)
            return run_q1(annual_scen, assumptions_phase1, scen_sel, run_id, hourly_by_country_year=hourly_map)
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
        year = int(selection.get("horizon_year", max(scenario_years) if scenario_years else max(DEFAULT_SCENARIO_YEARS)))
        runs: list[ModuleResult] = []
        for country in countries:
            try:
                hourly = load_scenario_hourly(scenario_id, country, year)
            except Exception:
                continue
            scen_sel = {
                **selection,
                "country": country,
                "year": year,
                "mode": "SCEN",
                "scenario_id": scenario_id,
                "horizon_year": year,
            }
            runs.append(run_q4(hourly, assumptions_phase1, scen_sel, f"{run_id}_{country}", dispatch_mode="SURPLUS_FIRST"))
        if not runs:
            return None
        return _merge_module_results(
            runs,
            module_id="Q4",
            run_id=run_id,
            selection={**selection, "countries": countries},
            mode="SCEN",
            scenario_id=scenario_id,
            horizon_year=year,
            narrative_title=f"Q4 scenario {scenario_id}",
        )

    if qid == "Q5":
        years = sorted(set([int(y) for y in scenario_years]))
        runs: list[ModuleResult] = []
        tech_map = selection.get("marginal_tech_by_country", {})
        for country in countries:
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
                continue
            marginal_tech = (
                str(tech_map.get(country, selection.get("marginal_tech", "CCGT"))).upper()
                if isinstance(tech_map, dict)
                else str(selection.get("marginal_tech", "CCGT")).upper()
            )
            scen_sel = {
                **selection,
                "country": country,
                "marginal_tech": marginal_tech,
                "mode": "SCEN",
                "scenario_id": scenario_id,
                "horizon_year": max(years) if years else None,
            }
            runs.append(
                run_q5(
                    hourly_df=hourly,
                    assumptions_df=assumptions_phase1,
                    selection=scen_sel,
                    run_id=f"{run_id}_{country}",
                    commodity_daily=commodity,
                    ttl_target_eur_mwh=_safe_float(selection.get("ttl_target_eur_mwh"), 120.0),
                )
            )
        if not runs:
            return None
        return _merge_module_results(
            runs,
            module_id="Q5",
            run_id=run_id,
            selection={**selection, "countries": countries},
            mode="SCEN",
            scenario_id=scenario_id,
            horizon_year=max(years) if years else None,
            narrative_title=f"Q5 scenario {scenario_id}",
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
        merged = hist[["country", "status", "inversion_k_demand", "inversion_r_mustrun"]].merge(
            scen[["country", "status", "inversion_k_demand", "inversion_r_mustrun"]],
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
                    "hist_status": str(r.get("status_hist", "")),
                    "scen_status": str(r.get("status_scen", "")),
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
                    "hist_status": str(r.get("status_hist", "")),
                    "scen_status": str(r.get("status_scen", "")),
                }
            )
    return pd.DataFrame(rows)


def _q4_comparison(hist_result: ModuleResult, scen_results: dict[str, ModuleResult], extra_hist: dict[str, ModuleResult]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    hist = hist_result.tables.get("Q4_sizing_summary", pd.DataFrame())
    if not hist.empty:
        req_cols = {"country", "far_after", "surplus_unabs_energy_after", "pv_capture_price_after"}
        if not req_cols.issubset(set(hist.columns)):
            return pd.DataFrame()
        for sid, res in scen_results.items():
            scen = res.tables.get("Q4_sizing_summary", pd.DataFrame())
            if scen.empty:
                continue
            if not req_cols.issubset(set(scen.columns)):
                continue
            merged = hist[["country", "far_after", "surplus_unabs_energy_after", "pv_capture_price_after"]].merge(
                scen[["country", "far_after", "surplus_unabs_energy_after", "pv_capture_price_after"]],
                on="country",
                how="inner",
                suffixes=("_hist", "_scen"),
            )
            for _, r in merged.iterrows():
                for metric in ["far_after", "surplus_unabs_energy_after", "pv_capture_price_after"]:
                    h = _safe_float(r.get(f"{metric}_hist"), np.nan)
                    s = _safe_float(r.get(f"{metric}_scen"), np.nan)
                    rows.append(
                        {
                            "country": str(r.get("country", "")),
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
            if not {"country", "far_after"}.issubset(set(mode_summary.columns)):
                continue
            merged_mode = hist[["country", "far_after"]].merge(mode_summary[["country", "far_after"]], on="country", how="inner", suffixes=("_hist", "_mode"))
            for _, r in merged_mode.iterrows():
                h = _safe_float(r.get("far_after_hist"), np.nan)
                s = _safe_float(r.get("far_after_mode"), np.nan)
                rows.append(
                    {
                        "country": str(r.get("country", "")),
                        "scenario_id": mode_key,
                        "metric": "far_after",
                        "hist_value": h,
                        "scen_value": s,
                        "delta": s - h if np.isfinite(h) and np.isfinite(s) else np.nan,
                    }
                )
    return pd.DataFrame(rows)


def _q5_comparison(hist_result: ModuleResult, scen_results: dict[str, ModuleResult]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    hist = hist_result.tables.get("Q5_summary", pd.DataFrame())
    if hist.empty:
        return pd.DataFrame()
    metric_col = "co2_required_base_non_negative" if "co2_required_base_non_negative" in hist.columns else "co2_required_base"
    req_cols = {"country", "ttl_obs", "tca_q95", metric_col}
    if not req_cols.issubset(set(hist.columns)):
        return pd.DataFrame()
    for sid, res in scen_results.items():
        scen = res.tables.get("Q5_summary", pd.DataFrame())
        if scen.empty:
            continue
        if not req_cols.issubset(set(scen.columns)):
            continue
        merged = hist[["country", "ttl_obs", "tca_q95", metric_col]].merge(
            scen[["country", "ttl_obs", "tca_q95", metric_col]],
            on="country",
            how="inner",
            suffixes=("_hist", "_scen"),
        )
        for _, r in merged.iterrows():
            for metric in ["ttl_obs", "tca_q95", metric_col]:
                h = _safe_float(r.get(f"{metric}_hist"), np.nan)
                s = _safe_float(r.get(f"{metric}_scen"), np.nan)
                rows.append(
                    {
                        "country": str(r.get("country", "")),
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


def _annotate_comparison_interpretability(question_id: str, comparison: pd.DataFrame) -> pd.DataFrame:
    if comparison is None or comparison.empty:
        return pd.DataFrame(columns=["country", "scenario_id", "metric", "hist_value", "scen_value", "delta", "interpretability_status", "interpretability_reason"])

    qid = str(question_id).upper()
    out = comparison.copy()
    for c in ["hist_value", "scen_value", "delta"]:
        if c not in out.columns:
            out[c] = np.nan
    if "scen_status" not in out.columns:
        out["scen_status"] = ""

    statuses: list[str] = []
    reasons: list[str] = []
    for _, row in out.iterrows():
        h = _safe_float(row.get("hist_value"), np.nan)
        s = _safe_float(row.get("scen_value"), np.nan)
        d = _safe_float(row.get("delta"), np.nan)
        scen_status = str(row.get("scen_status", "")).lower().strip()

        if qid == "Q3" and scen_status == "hors_scope_stage2":
            statuses.append("NON_TESTABLE")
            reasons.append("scenario_hors_scope_stage2")
            continue
        if not (np.isfinite(h) and np.isfinite(s) and np.isfinite(d)):
            statuses.append("NON_TESTABLE")
            reasons.append("delta_non_interpretable_nan")
            continue
        if abs(d) < 1e-9:
            statuses.append("FRAGILE")
            reasons.append("delta_quasi_nul_vs_historique")
            continue
        statuses.append("INFORMATIVE")
        reasons.append("delta_interpretable")

    out["interpretability_status"] = statuses
    out["interpretability_reason"] = reasons
    return out


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
                        both = summary["bascule_year_market"].notna() & summary["bascule_year_physical"].notna()
                        market_only = summary["bascule_year_market"].notna() & summary["bascule_year_physical"].isna()
                        sr_vals = pd.to_numeric(summary.get("sr_energy_at_bascule"), errors="coerce")
                        far_vals = pd.to_numeric(summary.get("far_energy_at_bascule"), errors="coerce")
                        explained_div = market_only & (
                            (sr_vals.fillna(0.0) <= 0.01) & ((far_vals.fillna(1.0) >= 0.95) | far_vals.isna())
                        )
                        concordant_share = float((both | explained_div).mean())
                        strict_share = float(both.mean())
                        if concordant_share >= 0.80:
                            status = "PASS"
                            interp = "Concordance satisfaisante en comptant les divergences expliquees (pas de stress physique structurel)."
                        elif concordant_share >= 0.50:
                            status = "WARN"
                            interp = "Concordance partielle; divergences a expliquer pays par pays."
                        else:
                            status = "FAIL"
                            interp = "Concordance insuffisante entre diagnostic marche et physique."
                        _append_test_row(
                            rows,
                            spec,
                            status,
                            f"strict={strict_share:.2%}; concordant_ou_explique={concordant_share:.2%}",
                            "concordant_ou_explique >= 80%",
                            interp,
                        )
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
                        ttl = pd.to_numeric(out["ttl_obs"], errors="coerce") if "ttl_obs" in out.columns else pd.Series(dtype=float)
                        tca = pd.to_numeric(out["tca_q95"], errors="coerce") if "tca_q95" in out.columns else pd.Series(dtype=float)
                        share = float((np.isfinite(ttl) & np.isfinite(tca)).mean()) if len(out) else 0.0
                        status = "PASS" if share >= 0.8 else ("WARN" if share > 0 else "FAIL")
                        _append_test_row(
                            rows,
                            spec,
                            status,
                            f"share_fini={share:.2%}",
                            ">=80% lignes ttl/tca finies",
                            "L'ancre thermique est quantifiable sur la majorite des pays." if status == "PASS" else "Ancre thermique partielle sur le scope courant.",
                        )
                else:
                    if out.empty:
                        _append_test_row(rows, spec, "FAIL", "", "summary non vide", "Q5 historique absent.")
                    else:
                        dco2 = pd.to_numeric(out["dTCA_dCO2"], errors="coerce") if "dTCA_dCO2" in out.columns else pd.Series(dtype=float)
                        dgas = pd.to_numeric(out["dTCA_dGas"], errors="coerce") if "dTCA_dGas" in out.columns else pd.Series(dtype=float)
                        ok_share = float(((dco2 > 0) & (dgas > 0)).mean()) if len(out) else 0.0
                        status = "PASS" if ok_share == 1.0 else ("WARN" if ok_share > 0 else "FAIL")
                        _append_test_row(
                            rows,
                            spec,
                            status,
                            f"share_positive={ok_share:.2%}",
                            "100% lignes >0",
                            "Sensibilites analytiques globalement coherentes.",
                        )
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
                        if sid == "BASE":
                            _append_test_row(
                                rows,
                                spec,
                                "PASS",
                                "reference_scenario",
                                "scenario de reference",
                                "BASE est la reference explicite pour le calcul de sensibilite; pas de delta attendu.",
                                sid,
                            )
                            continue

                        base_res = scen_results.get("BASE")
                        base_summary = base_res.tables.get("Q1_country_summary", pd.DataFrame()) if base_res is not None else pd.DataFrame()
                        if base_summary.empty or summary.empty:
                            _append_test_row(
                                rows,
                                spec,
                                "NON_TESTABLE",
                                "",
                                "delta vs BASE disponible",
                                "Impossible d'evaluer la sensibilite sans BASE et scenario courant.",
                                sid,
                            )
                            continue

                        merged = base_summary[["country", "bascule_year_market"]].merge(
                            summary[
                                [
                                    "country",
                                    "bascule_year_market",
                                    "required_demand_uplift_to_avoid_phase2",
                                    "required_flex_uplift_to_avoid_phase2",
                                    "required_demand_uplift_status",
                                    "required_flex_uplift_status",
                                ]
                            ]
                            if {"required_demand_uplift_to_avoid_phase2", "required_flex_uplift_to_avoid_phase2"}.issubset(set(summary.columns))
                            else summary[["country", "bascule_year_market"]],
                            on="country",
                            how="outer",
                            suffixes=("_base", "_scen"),
                        )
                        n_countries = int(len(merged))
                        if n_countries == 0:
                            _append_test_row(
                                rows,
                                spec,
                                "NON_TESTABLE",
                                "n_countries=0",
                                "n_countries>0",
                                "Aucun pays commun pour calculer delta vs BASE.",
                                sid,
                            )
                            continue

                        base_vals = pd.to_numeric(merged["bascule_year_market_base"], errors="coerce")
                        scen_vals = pd.to_numeric(merged["bascule_year_market_scen"], errors="coerce")
                        finite_mask = np.isfinite(base_vals) & np.isfinite(scen_vals)
                        finite_share = float(finite_mask.mean())
                        deltas = (scen_vals - base_vals).where(finite_mask, np.nan)
                        nonzero_share = float((deltas.abs().fillna(0.0) > 0.0).mean())
                        req_defined_share = 0.0
                        if "required_demand_uplift_to_avoid_phase2" in merged.columns or "required_flex_uplift_to_avoid_phase2" in merged.columns:
                            k = pd.to_numeric(merged.get("required_demand_uplift_to_avoid_phase2"), errors="coerce")
                            f = pd.to_numeric(merged.get("required_flex_uplift_to_avoid_phase2"), errors="coerce")
                            status_k = merged.get("required_demand_uplift_status", pd.Series(dtype=object)).astype(str)
                            status_f = merged.get("required_flex_uplift_status", pd.Series(dtype=object)).astype(str)
                            status_known = status_k.isin(["ok", "already_not_phase2", "beyond_plausible_bounds"]) | status_f.isin(["ok", "already_not_phase2", "beyond_plausible_bounds"])
                            req_defined_share = float((np.isfinite(k) | np.isfinite(f) | status_known).mean())

                        if finite_share == 0.0:
                            if req_defined_share > 0.0:
                                status = "PASS"
                                interp = "Delta vs BASE nul/non defini, mais solveur required_lever disponible et interpretable."
                            else:
                                status = "NON_TESTABLE"
                                interp = "Aucun delta defini vs BASE (finite_share=0)."
                        elif nonzero_share == 0.0:
                            if req_defined_share > 0.0:
                                status = "PASS"
                                interp = "Delta nul vs BASE, mais required_lever renseigne (interpretabilite preservee)."
                            else:
                                status = "WARN"
                                interp = "Delta vs BASE defini mais nul sur tous les pays."
                        elif nonzero_share >= 0.20:
                            status = "PASS"
                            interp = "Sensibilite scenario observable vs BASE."
                        else:
                            status = "WARN"
                            interp = "Sensibilite faible: deltas non nuls sur moins de 20% des pays."

                        _append_test_row(
                            rows,
                            spec,
                            status,
                            f"finite_share={finite_share:.2%}; nonzero_share={nonzero_share:.2%}; req_defined={req_defined_share:.2%}; n_countries={n_countries}",
                            "nonzero_share >= 20% (scenarios non-BASE)",
                            interp,
                            sid,
                        )
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
                        if slopes.empty:
                            _append_test_row(rows, spec, "NON_TESTABLE", "", "slopes scenario disponibles", "Aucune pente scenario disponible pour delta vs BASE.", sid)
                        else:
                            slope_vals = pd.to_numeric(slopes.get("slope"), errors="coerce")
                            finite_share = float(np.isfinite(slope_vals).mean())
                            robust_share = (
                                float((slopes["robust_flag"].astype(str) == "ROBUST").mean())
                                if "robust_flag" in slopes.columns
                                else np.nan
                            )
                            reason_known_share = (
                                float(slopes["reason_code"].astype(str).ne("").mean())
                                if "reason_code" in slopes.columns
                                else 0.0
                            )
                            if finite_share >= 0.20:
                                status = "PASS"
                                interp = "Delta de pente exploitable directionnellement; robustesse statistique a lire a part."
                            elif finite_share > 0:
                                status = "WARN"
                                interp = "Delta de pente partiellement exploitable; beaucoup de valeurs non finies."
                            else:
                                if reason_known_share > 0.0:
                                    status = "WARN"
                                    interp = "Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable."
                                else:
                                    status = "NON_TESTABLE"
                                    interp = "Delta de pente non interpretable (aucune pente finie)."
                            _append_test_row(
                                rows,
                                spec,
                                status,
                                f"finite={finite_share:.2%}; robust={robust_share:.2%}; reason_known={reason_known_share:.2%}" if np.isfinite(robust_share) else f"finite={finite_share:.2%}; reason_known={reason_known_share:.2%}",
                                "finite_share >= 20%",
                                interp,
                                sid,
                            )
                elif qid == "Q3":
                    out = scen_res.tables.get("Q3_status", pd.DataFrame())
                    if spec.test_id == "Q3-S-01":
                        req = {"inversion_k_demand", "inversion_r_mustrun", "additional_absorbed_needed_TWh_year"}
                        ok = (not out.empty) and req.issubset(set(out.columns))
                        if not ok:
                            _append_test_row(rows, spec, "FAIL", int(len(out)), "colonnes inversion presentes", "Les ordres de grandeur d'inversion sont incomplets.", sid)
                        else:
                            share_hs = float((out["status"].astype(str) == "hors_scope_stage2").mean()) if "status" in out.columns else np.nan
                            if np.isfinite(share_hs) and share_hs >= 0.80:
                                k_vals = pd.to_numeric(out.get("inversion_k_demand"), errors="coerce")
                                r_vals = pd.to_numeric(out.get("inversion_r_mustrun"), errors="coerce")
                                add_vals = pd.to_numeric(out.get("additional_absorbed_needed_TWh_year"), errors="coerce")
                                k_status_known = "inversion_k_demand_status" in out.columns and out["inversion_k_demand_status"].astype(str).ne("").any()
                                r_status_known = "inversion_r_mustrun_status" in out.columns and out["inversion_r_mustrun_status"].astype(str).ne("").any()
                                f_status_known = "inversion_f_flex_status" in out.columns and out["inversion_f_flex_status"].astype(str).ne("").any()
                                already_de_stressed = bool(
                                    _max_finite(k_vals, default=0.0) <= 1e-6
                                    and _max_finite(r_vals, default=0.0) <= 1e-6
                                    and _max_finite(add_vals, default=0.0) <= 1e-3
                                )
                                if already_de_stressed:
                                    _append_test_row(
                                        rows,
                                        spec,
                                        "PASS",
                                        f"hors_scope={share_hs:.2%}; inversion=0",
                                        "hors_scope < 80% ou inversion deja atteinte",
                                        "Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites.",
                                        sid,
                                    )
                                else:
                                    if k_status_known or r_status_known or f_status_known:
                                        _append_test_row(
                                            rows,
                                            spec,
                                            "WARN",
                                            f"hors_scope={share_hs:.2%}; statuses_known=1",
                                            "hors_scope < 80%",
                                            "Majoritairement hors scope Stage 2, mais solveurs explicites (borne/ready) disponibles.",
                                            sid,
                                        )
                                    else:
                                        _append_test_row(
                                            rows,
                                            spec,
                                            "NON_TESTABLE",
                                            f"hors_scope={share_hs:.2%}",
                                            "hors_scope < 80%",
                                            "Le scenario reste majoritairement hors scope Stage 2 sans preuve claire d'inversion.",
                                            sid,
                                        )
                            else:
                                _append_test_row(rows, spec, "PASS", int(len(out)), "colonnes inversion presentes", "Les ordres de grandeur d'inversion sont quantifies.", sid)
                    else:
                        if out.empty or "status" not in out.columns:
                            _append_test_row(rows, spec, "NON_TESTABLE", "", "status scenario disponibles", "Impossible d'evaluer la transition phase 3 (sortie scenario manquante).", sid)
                        else:
                            share_hs = float((out["status"].astype(str) == "hors_scope_stage2").mean())
                            if share_hs >= 0.80:
                                k_vals = pd.to_numeric(out.get("inversion_k_demand"), errors="coerce")
                                r_vals = pd.to_numeric(out.get("inversion_r_mustrun"), errors="coerce")
                                add_vals = pd.to_numeric(out.get("additional_absorbed_needed_TWh_year"), errors="coerce")
                                k_status_known = "inversion_k_demand_status" in out.columns and out["inversion_k_demand_status"].astype(str).ne("").any()
                                r_status_known = "inversion_r_mustrun_status" in out.columns and out["inversion_r_mustrun_status"].astype(str).ne("").any()
                                f_status_known = "inversion_f_flex_status" in out.columns and out["inversion_f_flex_status"].astype(str).ne("").any()
                                already_de_stressed = bool(
                                    _max_finite(k_vals, default=0.0) <= 1e-6
                                    and _max_finite(r_vals, default=0.0) <= 1e-6
                                    and _max_finite(add_vals, default=0.0) <= 1e-3
                                )
                                if already_de_stressed:
                                    _append_test_row(
                                        rows,
                                        spec,
                                        "PASS",
                                        f"hors_scope={share_hs:.2%}; inversion=0",
                                        "hors_scope < 80% ou inversion deja atteinte",
                                        "Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise.",
                                        sid,
                                    )
                                else:
                                    if k_status_known or r_status_known or f_status_known:
                                        _append_test_row(
                                            rows,
                                            spec,
                                            "WARN",
                                            f"hors_scope={share_hs:.2%}; statuses_known=1",
                                            "hors_scope < 80%",
                                            "Lecture limitee (hors scope majoritaire) mais solveurs explicites disponibles.",
                                            sid,
                                        )
                                    else:
                                        _append_test_row(
                                            rows,
                                            spec,
                                            "NON_TESTABLE",
                                            f"hors_scope={share_hs:.2%}",
                                            "hors_scope < 80%",
                                            "Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3.",
                                            sid,
                                        )
                            elif share_hs >= 0.40:
                                _append_test_row(
                                    rows,
                                    spec,
                                    "WARN",
                                    f"hors_scope={share_hs:.2%}",
                                    "hors_scope < 40%",
                                    "Lecture partiellement informative: forte part de cas hors scope Stage 2.",
                                    sid,
                                )
                            else:
                                _append_test_row(rows, spec, "PASS", int(out["status"].nunique()), "status renseignes", "La lecture de transition phase 3 est possible.", sid)
                elif qid == "Q4":
                    out = scen_res.tables.get("Q4_sizing_summary", pd.DataFrame())
                    if spec.test_id == "Q4-S-01":
                        _append_test_row(rows, spec, "PASS" if not out.empty else "FAIL", int(len(out)), ">0 lignes", "Resultats Q4 prospectifs disponibles.", sid)
                    else:
                        if out.empty:
                            _append_test_row(rows, spec, "NON_TESTABLE", "", "summary non vide", "Pas de sortie scenario.", sid)
                        else:
                            vals = pd.to_numeric(out["pv_capture_price_after"], errors="coerce") if "pv_capture_price_after" in out.columns else pd.Series(dtype=float)
                            share_finite = float(np.isfinite(vals).mean())
                            status = "PASS" if share_finite >= 0.8 else ("WARN" if share_finite > 0 else "NON_TESTABLE")
                            _append_test_row(
                                rows,
                                spec,
                                status,
                                f"share_finite={share_finite:.2%}",
                                ">=80% valeurs finies",
                                "Sensibilite valeur exploitable sur le panel." if status == "PASS" else "Sensibilite valeur partielle/non disponible.",
                                sid,
                            )
                elif qid == "Q5":
                    out = scen_res.tables.get("Q5_summary", pd.DataFrame())
                    if spec.test_id == "Q5-S-01":
                        _append_test_row(rows, spec, "PASS" if not out.empty else "FAIL", int(len(out)), ">0 lignes", "Sensibilites scenario calculees.", sid)
                    else:
                        if out.empty:
                            _append_test_row(rows, spec, "NON_TESTABLE", "", "co2_required present", "Sortie scenario absente.", sid)
                        else:
                            if "co2_required_base_non_negative" in out.columns:
                                vals = pd.to_numeric(out["co2_required_base_non_negative"], errors="coerce")
                            elif "co2_required_base" in out.columns:
                                vals = pd.to_numeric(out["co2_required_base"], errors="coerce")
                            else:
                                vals = pd.Series(dtype=float)
                            share_finite = float(np.isfinite(vals).mean())
                            status = "PASS" if share_finite >= 0.8 else ("WARN" if share_finite > 0 else "NON_TESTABLE")
                            _append_test_row(
                                rows,
                                spec,
                                status,
                                f"share_finite={share_finite:.2%}",
                                ">=80% valeurs finies",
                                "CO2 requis interpretable sur le panel." if status == "PASS" else "CO2 requis partiel/non interpretable.",
                                sid,
                            )
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
    comparison = _annotate_comparison_interpretability(qid, comparison)

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
        n_total = int(len(ledger))
        n_non_testable = int((ledger["status"].astype(str) == "NON_TESTABLE").sum())
        test_informative_share = (n_total - n_non_testable) / n_total if n_total > 0 else np.nan
        comp_informative_share = np.nan
        if comparison is not None and not comparison.empty and "interpretability_status" in comparison.columns:
            comp_total = int(len(comparison))
            comp_info = int((comparison["interpretability_status"].astype(str) == "INFORMATIVE").sum())
            comp_informative_share = comp_info / comp_total if comp_total > 0 else np.nan
        info_status = "PASS"
        if np.isfinite(test_informative_share) and test_informative_share < 0.50:
            info_status = "WARN"
        if np.isfinite(comp_informative_share) and comp_informative_share < 0.30:
            info_status = "WARN"
        checks.append(
            {
                "status": info_status,
                "code": "BUNDLE_INFORMATIVENESS",
                "message": (
                    f"share_tests_informatifs={test_informative_share:.2%} ; "
                    f"share_compare_informatifs={comp_informative_share:.2%}" if np.isfinite(comp_informative_share)
                    else f"share_tests_informatifs={test_informative_share:.2%} ; share_compare_informatifs=n/a"
                ),
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        )

        if qid == "Q1":
            s02 = ledger[
                (ledger["test_id"].astype(str) == "Q1-S-02")
                & (ledger["mode"].astype(str) == "SCEN")
                & (ledger["scenario_id"].astype(str) != "BASE")
            ].copy()
            if not s02.empty:
                statuses = set(s02["status"].astype(str))
                if statuses.issubset({"WARN", "NON_TESTABLE"}):
                    checks.append(
                        {
                            "status": "WARN",
                            "code": "Q1_S02_NO_SENSITIVITY",
                            "message": "Q1-S-02: aucune sensibilite scenario non-BASE clairement observable vs BASE.",
                            "scope": "BUNDLE",
                            "scenario_id": "",
                        }
                    )
                else:
                    checks.append(
                        {
                            "status": "PASS",
                            "code": "Q1_S02_NO_SENSITIVITY",
                            "message": "Q1-S-02: au moins un scenario non-BASE montre une sensibilite observable.",
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
