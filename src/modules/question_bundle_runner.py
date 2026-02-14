"""Unified HIST+SCEN question runner with test ledger and comparison output."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.config_loader import load_countries
from src.constants import DEFAULT_COUNTRIES
from src.hash_utils import hash_object
from src.metrics import compute_annual_metrics
from src.modules.bundle_result import QuestionBundleResult
from src.modules.q1_transition import run_q1, stage2_active_from_metrics
from src.modules.q2_slope import run_q2
from src.modules.q3_exit import run_q3
from src.modules.q4_bess import run_q4
from src.modules.q5_thermal_anchor import run_q5
from src.modules.result import ModuleResult
from src.modules.test_registry import QuestionTestSpec, get_default_scenarios, get_question_tests
from src.scenario.phase2_engine import apply_q1_scenario_to_hourly_inputs, run_phase2_scenario
from src.storage import (
    load_hourly,
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


def _stage2_active_hist_reference(row: pd.Series, params: dict[str, float]) -> bool:
    try:
        if stage2_active_from_metrics(row, params):
            return True
    except Exception:
        pass

    h_negative_stage2_min = _safe_float(params.get("h_negative_stage2_min"), 200.0)
    h_below_5_stage2_min = _safe_float(params.get("h_below_5_stage2_min"), 500.0)
    sr_hours_stage2_min = _safe_float(params.get("sr_hours_stage2_min"), 0.10)
    far_stage2_min = _safe_float(params.get("far_stage2_min"), 0.95)
    ir_p10_stage2_min = _safe_float(params.get("ir_p10_stage2_min"), 1.5)
    capture_ratio_pv_stage2_max = _safe_float(params.get("capture_ratio_pv_stage2_max"), 0.80)
    capture_ratio_wind_stage2_max = _safe_float(params.get("capture_ratio_wind_stage2_max"), 0.90)

    h_negative = _safe_float(row.get("h_negative_obs_at_end_year", row.get("h_negative_obs")), np.nan)
    h_below_5 = _safe_float(row.get("h_below_5_obs_at_end_year", row.get("h_below_5_obs")), np.nan)
    sr_hours = _safe_float(row.get("sr_hours_at_end_year", row.get("sr_hours")), np.nan)
    far_observed = _safe_float(row.get("far_observed_at_end_year", row.get("far_observed")), np.nan)
    ir_p10 = _safe_float(row.get("ir_p10_at_end_year", row.get("ir_p10")), np.nan)
    capture_ratio_pv = _safe_float(row.get("capture_ratio_pv_at_end_year", row.get("capture_ratio_pv")), np.nan)
    capture_ratio_wind = _safe_float(row.get("capture_ratio_wind_at_end_year", row.get("capture_ratio_wind")), np.nan)

    return bool(
        (np.isfinite(h_negative) and h_negative >= h_negative_stage2_min)
        or (np.isfinite(h_below_5) and h_below_5 >= h_below_5_stage2_min)
        or (np.isfinite(sr_hours) and sr_hours >= sr_hours_stage2_min)
        or (np.isfinite(far_observed) and far_observed < far_stage2_min)
        or (np.isfinite(ir_p10) and ir_p10 >= ir_p10_stage2_min)
        or (np.isfinite(capture_ratio_pv) and capture_ratio_pv <= capture_ratio_pv_stage2_max)
        or (np.isfinite(capture_ratio_wind) and capture_ratio_wind <= capture_ratio_wind_stage2_max)
    )


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
    if "PASS" in statuses:
        return "PASS"
    if "NON_TESTABLE" in statuses:
        return "NON_TESTABLE"
    return "PASS"


def _is_hard_test(spec: QuestionTestSpec) -> bool:
    sev = str(spec.severity_if_fail or "").upper().strip()
    return sev in {"CRITICAL", "HIGH"}


def _status_from_threshold(spec: QuestionTestSpec, *, condition_met: bool, evaluable: bool) -> str:
    if not evaluable:
        return "NON_TESTABLE"
    if bool(condition_met):
        return "PASS"
    return "FAIL" if _is_hard_test(spec) else "WARN"


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


def _derive_q1_hourly_scenario_params(
    assumptions_phase2: pd.DataFrame,
    *,
    scenario_id: str,
    country: str,
    scenario_years: list[int],
) -> dict[str, Any]:
    sid = str(scenario_id).strip().upper()
    params: dict[str, Any] = {"scenario_id": str(scenario_id)}
    floor_reasons: list[str] = []

    def _apply_q1_floor_if_needed(demand_factor: float, must_run_scale: float) -> tuple[float, float]:
        demand_val = float(demand_factor)
        must_run_val = float(must_run_scale)
        if sid == "DEMAND_UP":
            if not np.isfinite(demand_val):
                demand_val = 1.03
                floor_reasons.append("demand_factor_floor_missing_assumptions")
            elif demand_val < 1.03:
                demand_val = 1.03
                floor_reasons.append("demand_factor_floor_raised_to_1.03")
        if sid == "LOW_RIGIDITY":
            if not np.isfinite(must_run_val):
                must_run_val = 0.97
                floor_reasons.append("must_run_scale_floor_missing_assumptions")
            elif must_run_val > 0.97:
                must_run_val = 0.97
                floor_reasons.append("must_run_scale_floor_lowered_to_0.97")
        return demand_val, must_run_val

    def _attach_floor_metadata() -> None:
        if floor_reasons:
            params["_q1_floor_applied"] = True
            params["_q1_floor_reason"] = "; ".join(sorted(set([str(x) for x in floor_reasons if str(x).strip()])))

    if assumptions_phase2 is None or assumptions_phase2.empty:
        demand_floor, must_run_floor = _apply_q1_floor_if_needed(np.nan, np.nan)
        if np.isfinite(demand_floor):
            params["demand_factor"] = float(max(0.0, demand_floor))
            params["demand_uplift"] = float(max(-1.0, demand_floor - 1.0))
        if np.isfinite(must_run_floor):
            params["must_run_scale"] = float(np.clip(must_run_floor, 0.0, 2.0))
            params["rigidity_reduction"] = float(max(0.0, 1.0 - must_run_floor))
        _attach_floor_metadata()
        return params

    p2 = assumptions_phase2.copy()
    p2["scenario_id"] = p2["scenario_id"].astype(str)
    p2["country"] = p2["country"].astype(str)
    p2["year"] = pd.to_numeric(p2["year"], errors="coerce")
    years_set = {int(y) for y in scenario_years}

    scen = p2[
        (p2["scenario_id"] == str(scenario_id))
        & (p2["country"] == str(country))
        & (p2["year"].isin(years_set))
    ].copy()
    base = p2[
        (p2["scenario_id"] == "BASE")
        & (p2["country"] == str(country))
        & (p2["year"].isin(years_set))
    ].copy()
    if scen.empty or base.empty:
        demand_floor, must_run_floor = _apply_q1_floor_if_needed(np.nan, np.nan)
        if np.isfinite(demand_floor):
            params["demand_factor"] = float(max(0.0, demand_floor))
            params["demand_uplift"] = float(max(-1.0, demand_floor - 1.0))
        if np.isfinite(must_run_floor):
            params["must_run_scale"] = float(np.clip(must_run_floor, 0.0, 2.0))
            params["rigidity_reduction"] = float(max(0.0, 1.0 - must_run_floor))
        _attach_floor_metadata()
        return params

    merged = scen.merge(
        base[["year", "demand_total_twh", "must_run_min_output_factor"]],
        on="year",
        how="inner",
        suffixes=("_scen", "_base"),
    )
    if merged.empty:
        demand_floor, must_run_floor = _apply_q1_floor_if_needed(np.nan, np.nan)
        if np.isfinite(demand_floor):
            params["demand_factor"] = float(max(0.0, demand_floor))
            params["demand_uplift"] = float(max(-1.0, demand_floor - 1.0))
        if np.isfinite(must_run_floor):
            params["must_run_scale"] = float(np.clip(must_run_floor, 0.0, 2.0))
            params["rigidity_reduction"] = float(max(0.0, 1.0 - must_run_floor))
        _attach_floor_metadata()
        return params

    demand_ratio = (
        pd.to_numeric(merged.get("demand_total_twh_scen"), errors="coerce")
        / pd.to_numeric(merged.get("demand_total_twh_base"), errors="coerce").replace(0.0, np.nan)
    )
    must_run_ratio = (
        pd.to_numeric(merged.get("must_run_min_output_factor_scen"), errors="coerce")
        / pd.to_numeric(merged.get("must_run_min_output_factor_base"), errors="coerce").replace(0.0, np.nan)
    )
    demand_factor = _safe_float(demand_ratio.median(), np.nan)
    must_run_scale = _safe_float(must_run_ratio.median(), np.nan)
    demand_factor, must_run_scale = _apply_q1_floor_if_needed(demand_factor, must_run_scale)
    if np.isfinite(demand_factor):
        params["demand_factor"] = float(max(0.0, demand_factor))
        params["demand_uplift"] = float(max(-1.0, demand_factor - 1.0))
    if np.isfinite(must_run_scale):
        params["must_run_scale"] = float(np.clip(must_run_scale, 0.0, 2.0))
        params["rigidity_reduction"] = float(max(0.0, 1.0 - must_run_scale))
    _attach_floor_metadata()
    return params


def _build_q1_historical_scenario_inputs(
    *,
    scenario_id: str,
    countries: list[str],
    historical_years: list[int],
    scenario_years_for_params: list[int],
    annual_hist: pd.DataFrame,
    hourly_hist_map: dict[tuple[str, int], pd.DataFrame],
    assumptions_phase2: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[tuple[str, int], pd.DataFrame], list[dict[str, Any]]]:
    annual_rows: list[dict[str, Any]] = []
    hourly_map: dict[tuple[str, int], pd.DataFrame] = {}
    floor_events: list[dict[str, Any]] = []
    countries_cfg = load_countries().get("countries", {})

    for country in countries:
        country_cfg = countries_cfg.get(str(country))
        if not isinstance(country_cfg, dict):
            continue
        scen_params = _derive_q1_hourly_scenario_params(
            assumptions_phase2,
            scenario_id=scenario_id,
            country=str(country),
            scenario_years=scenario_years_for_params if scenario_years_for_params else historical_years,
        )
        if bool(scen_params.get("_q1_floor_applied", False)):
            floor_events.append(
                {
                    "country": str(country),
                    "scenario_id": str(scenario_id),
                    "reason": str(scen_params.get("_q1_floor_reason", "floor_applied")).strip(),
                }
            )
        for year in historical_years:
            key = (str(country), int(year))
            hourly = hourly_hist_map.get(key)
            if hourly is None or hourly.empty:
                try:
                    hourly = load_hourly(str(country), int(year))
                except Exception:
                    continue
            hourly_s = apply_q1_scenario_to_hourly_inputs(hourly, scen_params)
            if hourly_s.empty:
                continue
            hourly_s = hourly_s.copy()
            hourly_s["scenario_id"] = str(scenario_id)
            try:
                annual_row = compute_annual_metrics(
                    hourly_s,
                    country_cfg,
                    data_version_hash=hash_object(
                        {
                            "source": "q1_hist_scenario_transform",
                            "scenario_id": str(scenario_id),
                            "country": str(country),
                            "year": int(year),
                            "params": scen_params,
                        }
                    ),
                )
            except Exception:
                continue
            annual_row["scenario_id"] = str(scenario_id)
            annual_row["mode"] = "SCEN"
            annual_row["horizon_year"] = int(year)
            annual_rows.append(annual_row)
            hourly_map[key] = hourly_s

    if not annual_rows:
        return pd.DataFrame(), hourly_map, floor_events
    annual_df = pd.DataFrame(annual_rows).sort_values(["country", "year"]).reset_index(drop=True)
    return annual_df, hourly_map, floor_events


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


def _clone_hist_result_as_base_scenario(hist_result: ModuleResult, run_id: str) -> ModuleResult:
    cloned_tables: dict[str, pd.DataFrame] = {}
    for name, table in hist_result.tables.items():
        if isinstance(table, pd.DataFrame):
            cloned_tables[name] = table.copy(deep=True)
    return ModuleResult(
        module_id=hist_result.module_id,
        run_id=f"{run_id}_BASE_FROM_HIST",
        selection={**hist_result.selection, "mode": "SCEN", "scenario_id": "BASE"},
        assumptions_used=list(hist_result.assumptions_used),
        kpis=dict(hist_result.kpis),
        tables=cloned_tables,
        figures=list(hist_result.figures),
        narrative_md=hist_result.narrative_md,
        checks=[
            {
                "status": "WARN",
                "code": "BUNDLE_BASE_FALLBACK_HIST",
                "message": "Scenario BASE absent: fallback explicite sur les sorties historiques.",
            }
        ],
        warnings=["BASE fallback to HIST outputs."],
        mode="SCEN",
        scenario_id="BASE",
        horizon_year=hist_result.horizon_year,
    )


def _check_non_negative_fields(modules: list[tuple[str, ModuleResult]]) -> list[dict[str, Any]]:
    fails: list[str] = []
    for scope, module in modules:
        for table_name, table in module.tables.items():
            if not isinstance(table, pd.DataFrame) or table.empty:
                continue
            for col in [c for c in table.columns if str(c).lower().endswith("_non_negative")]:
                vals = pd.to_numeric(table[col], errors="coerce")
                bad_mask = vals < -1e-9
                if bool(bad_mask.fillna(False).any()):
                    fails.append(f"{scope}:{table_name}.{col}")
    if fails:
        preview = ", ".join(fails[:5])
        return [
            {
                "status": "FAIL",
                "code": "BUNDLE_NON_NEGATIVE_FIELD_NEGATIVE",
                "message": f"Champs *_non_negative negatifs detectes ({preview}).",
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        ]
    return [
        {
            "status": "PASS",
            "code": "BUNDLE_NON_NEGATIVE_FIELD_NEGATIVE",
            "message": "Tous les champs *_non_negative restent >= 0.",
            "scope": "BUNDLE",
            "scenario_id": "",
        }
    ]


def _check_q4_reporting_consistency(
    hist_result: ModuleResult,
    scen_results: dict[str, ModuleResult],
    comparison: pd.DataFrame,
) -> list[dict[str, Any]]:
    hist = hist_result.tables.get("Q4_sizing_summary", pd.DataFrame())
    if hist.empty:
        return []
    cmp_all = comparison.copy()
    for c in ["scenario_id", "country", "metric", "hist_value", "scen_value"]:
        if c not in cmp_all.columns:
            cmp_all[c] = np.nan if c in {"hist_value", "scen_value"} else ""
    metrics = ["far_after", "surplus_unabs_energy_after", "pv_capture_price_after"]
    if not {"country", *metrics}.issubset(set(hist.columns)):
        return []
    mismatches: list[str] = []
    for sid, scen_res in scen_results.items():
        scen = scen_res.tables.get("Q4_sizing_summary", pd.DataFrame())
        if scen.empty or (not {"country", *metrics}.issubset(set(scen.columns))):
            continue
        merged = hist[["country"] + metrics].merge(
            scen[["country"] + metrics],
            on="country",
            how="inner",
            suffixes=("_hist", "_scen"),
        )
        if merged.empty:
            continue
        cmp_sid = cmp_all[cmp_all["scenario_id"].astype(str) == str(sid)].copy()
        for _, row in merged.iterrows():
            country = str(row.get("country", ""))
            for metric in metrics:
                ref = cmp_sid[
                    (cmp_sid["country"].astype(str) == country)
                    & (cmp_sid["metric"].astype(str) == metric)
                ]
                if ref.empty:
                    mismatches.append(f"{sid}:{country}:{metric}:missing")
                    continue
                h_cmp = _safe_float(ref.iloc[0].get("hist_value"), np.nan)
                s_cmp = _safe_float(ref.iloc[0].get("scen_value"), np.nan)
                h_det = _safe_float(row.get(f"{metric}_hist"), np.nan)
                s_det = _safe_float(row.get(f"{metric}_scen"), np.nan)
                if np.isfinite(h_cmp) and np.isfinite(h_det) and abs(h_cmp - h_det) > 1e-9:
                    mismatches.append(f"{sid}:{country}:{metric}:hist")
                if np.isfinite(s_cmp) and np.isfinite(s_det) and abs(s_cmp - s_det) > 1e-9:
                    mismatches.append(f"{sid}:{country}:{metric}:scen")
    if mismatches:
        return [
            {
                "status": "FAIL",
                "code": "Q4_REPORTING_CONSISTENCY",
                "message": f"Incoherence comparaison/detail Q4 ({'; '.join(mismatches[:5])}).",
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        ]
    return [
        {
            "status": "PASS",
            "code": "Q4_REPORTING_CONSISTENCY",
            "message": "Comparaison Q4 coherente avec Q4_sizing_summary (meme colonnes, meme valeurs).",
            "scope": "BUNDLE",
            "scenario_id": "",
        }
    ]


def _check_q5_ttl_obs_consistency(
    hist_result: ModuleResult,
    scen_results: dict[str, ModuleResult],
    comparison: pd.DataFrame,
) -> list[dict[str, Any]]:
    hist = hist_result.tables.get("Q5_summary", pd.DataFrame())
    if hist.empty or "ttl_obs" not in hist.columns:
        return []
    cmp_ttl = comparison.copy()
    for c in ["metric", "scenario_id", "hist_value", "scen_value"]:
        if c not in cmp_ttl.columns:
            cmp_ttl[c] = np.nan if c in {"hist_value", "scen_value"} else ""
    cmp_ttl = cmp_ttl[cmp_ttl["metric"].astype(str) == "ttl_obs"].copy()
    mismatches: list[str] = []
    for sid, scen_res in scen_results.items():
        scen = scen_res.tables.get("Q5_summary", pd.DataFrame())
        if scen.empty or "ttl_obs" not in scen.columns:
            continue
        scen_countries = scen.get("country", pd.Series(dtype=object)).astype(str)
        scen_vals = pd.to_numeric(scen.get("ttl_obs"), errors="coerce")
        expected_scen_mean = _safe_float(scen_vals.mean(), np.nan)
        hist_mask = hist.get("country", pd.Series(dtype=object)).astype(str).isin(set(scen_countries.tolist()))
        expected_hist_mean = _safe_float(pd.to_numeric(hist.loc[hist_mask, "ttl_obs"], errors="coerce").mean(), np.nan)
        cmp_sid = cmp_ttl[cmp_ttl.get("scenario_id", pd.Series(dtype=object)).astype(str) == str(sid)]
        if cmp_sid.empty:
            mismatches.append(f"{sid}:missing")
            continue
        cmp_hist_mean = _safe_float(pd.to_numeric(cmp_sid.get("hist_value"), errors="coerce").mean(), np.nan)
        cmp_scen_mean = _safe_float(pd.to_numeric(cmp_sid.get("scen_value"), errors="coerce").mean(), np.nan)
        if np.isfinite(expected_hist_mean) and np.isfinite(cmp_hist_mean) and abs(expected_hist_mean - cmp_hist_mean) > 1e-9:
            mismatches.append(f"{sid}:hist_mean")
        if np.isfinite(expected_scen_mean) and np.isfinite(cmp_scen_mean) and abs(expected_scen_mean - cmp_scen_mean) > 1e-9:
            mismatches.append(f"{sid}:scen_mean")
    if mismatches:
        return [
            {
                "status": "FAIL",
                "code": "Q5_REPORTING_TTL_OBS_CONSISTENCY",
                "message": f"ttl_obs incoherent entre comparaison et detail ({'; '.join(mismatches[:5])}).",
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        ]
    return [
        {
            "status": "PASS",
            "code": "Q5_REPORTING_TTL_OBS_CONSISTENCY",
            "message": "ttl_obs comparaison/detail coherent (moyennes alignees).",
            "scope": "BUNDLE",
            "scenario_id": "",
        }
    ]


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


def _q5_base_anchor_from_row(
    row: pd.Series,
    *,
    status_override: str = "ok",
    reason_override: str = "",
    source_year_override: float | None = None,
) -> dict[str, Any]:
    out = {
        "base_tca_eur_mwh": _safe_float(
            row.get("tca_current_eur_mwh", row.get("ttl_anchor_formula")),
            np.nan,
        ),
        "base_tca_ccgt_eur_mwh": _safe_float(
            row.get("tca_ccgt_eur_mwh", row.get("tca_current_eur_mwh", row.get("ttl_anchor_formula"))),
            np.nan,
        ),
        "base_tca_coal_eur_mwh": _safe_float(row.get("tca_coal_eur_mwh"), np.nan),
        "base_ttl_observed_eur_mwh": _safe_float(row.get("ttl_observed_eur_mwh", row.get("ttl_obs")), np.nan),
        "base_ttl_model_eur_mwh": _safe_float(row.get("ttl_model_eur_mwh", row.get("ttl_observed_eur_mwh", row.get("ttl_obs"))), np.nan),
        "base_gas_eur_per_mwh_th": _safe_float(row.get("assumed_gas_price_eur_mwh_th"), np.nan),
        "base_co2_eur_per_t": _safe_float(row.get("assumed_co2_price_eur_t"), np.nan),
        "base_year_reference": _safe_float(
            row.get("ttl_reference_year", row.get("year")),
            np.nan,
        ),
        "base_ref_status_override": str(status_override),
        "base_ref_reason_override": str(reason_override or ""),
    }
    if source_year_override is not None and np.isfinite(_safe_float(source_year_override, np.nan)):
        out["base_ref_source_year"] = float(source_year_override)
        out["base_year_reference"] = float(source_year_override)
    return out


def _resolve_q5_base_anchor_for_country(
    *,
    country: str,
    years: list[int],
    annual_hist: pd.DataFrame,
    assumptions_phase1: pd.DataFrame,
    assumptions_phase2: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
) -> tuple[dict[str, Any], str]:
    # 1) Preferred: derive from BASE scenario outputs for same country/years.
    ok, reason = _ensure_scenario_outputs(
        scenario_id="BASE",
        countries=[country],
        scenario_years=years,
        assumptions_phase2=assumptions_phase2,
        annual_hist=annual_hist,
        hourly_hist_map={},
    )
    if ok:
        hourly_map = _load_scenario_hourly_map("BASE", [country], years)
        hourly = _concat_hourly(country, years, hourly_map)
        commodity = _phase2_commodity_daily(assumptions_phase2, "BASE", country, years)
        if not hourly.empty and not commodity.empty:
            base_sel = {
                **selection,
                "country": country,
                "mode": "SCEN",
                "scenario_id": "BASE",
                "horizon_year": max(years) if years else None,
            }
            base_res = run_q5(
                hourly_df=hourly,
                assumptions_df=assumptions_phase1,
                selection=base_sel,
                run_id=f"{run_id}_{country}_BASE_REF",
                commodity_daily=commodity,
                ttl_target_eur_mwh=_safe_float(selection.get("ttl_target_eur_mwh"), 120.0),
                ttl_method=str(selection.get("ttl_reference_mode", "year_specific")),
            )
            base_tbl = base_res.tables.get("Q5_summary", pd.DataFrame())
            if not base_tbl.empty:
                return _q5_base_anchor_from_row(base_tbl.iloc[0], status_override="ok"), "ok"

    # 2) Fallback: derive BASE from latest historical year for that country.
    years_hist = (
        annual_hist[annual_hist["country"].astype(str) == str(country)]["year"].dropna().astype(int).tolist()
        if annual_hist is not None and not annual_hist.empty and {"country", "year"}.issubset(annual_hist.columns)
        else []
    )
    if years_hist:
        hist_year = int(max(years_hist))
        try:
            hourly_hist = load_hourly(country, hist_year)
            hist_sel = {
                **selection,
                "country": country,
                "year": hist_year,
                "horizon_year": max(years) if years else None,
                "mode": "HIST",
                "scenario_id": "HIST",
                "ttl_reference_mode": "year_specific",
                "ttl_reference_year": hist_year,
            }
            hist_res = run_q5(
                hourly_df=hourly_hist,
                assumptions_df=assumptions_phase1,
                selection=hist_sel,
                run_id=f"{run_id}_{country}_HIST_REF",
                commodity_daily=None,
                ttl_target_eur_mwh=_safe_float(selection.get("ttl_target_eur_mwh"), 120.0),
                ttl_method=str(selection.get("ttl_reference_mode", "year_specific")),
            )
            hist_tbl = hist_res.tables.get("Q5_summary", pd.DataFrame())
            if not hist_tbl.empty:
                anchor = _q5_base_anchor_from_row(
                    hist_tbl.iloc[0],
                    status_override="warn_fallback_from_hist",
                    reason_override=f"fallback_from_hist:{hist_year}",
                    source_year_override=float(hist_year),
                )
                return anchor, "warn_fallback_from_hist"
        except Exception:
            pass

    return {}, f"missing_phase2_assumptions_or_hist_ref:{reason}"


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
    invalid_pairs: list[tuple[str, int]] = []

    if annual.empty:
        missing_pairs = [(c, y) for c in countries for y in scenario_years]
    else:
        annual = annual.copy()
        if "country" in annual.columns:
            annual["country"] = annual["country"].astype(str)
        if "year" in annual.columns:
            annual["year"] = pd.to_numeric(annual["year"], errors="coerce")
        if "scenario_id" not in annual.columns:
            annual["scenario_id"] = scenario_id
        for c in countries:
            for y in scenario_years:
                row = annual[(annual["country"] == str(c)) & (annual["year"] == int(y))]
                if row.empty:
                    missing_pairs.append((c, y))
                    continue
                if not scenario_hourly_output_path(scenario_id, c, int(y)).exists():
                    missing_pairs.append((c, y))
                    continue
                # Quality guard for stale scenario files from older engines.
                far = _safe_float(row.iloc[0].get("far_observed"), np.nan)
                sid = str(row.iloc[0].get("scenario_id", ""))
                if sid.strip() == "":
                    invalid_pairs.append((c, y))
                    continue
                if not np.isfinite(far):
                    invalid_pairs.append((c, y))
                    continue
                if ("sr_hours" in row.columns) and ("h_negative" in row.columns):
                    sr_h = _safe_float(row.iloc[0].get("sr_hours"), np.nan)
                    h_neg = _safe_float(row.iloc[0].get("h_negative"), np.nan)
                    h_low = _safe_float(row.iloc[0].get("h_below_5"), np.nan)
                    # If all stress proxies are exactly zero, row is likely stale/non-usable.
                    if np.isfinite(sr_h) and np.isfinite(h_neg) and np.isfinite(h_low):
                        if abs(sr_h) < 1e-12 and abs(h_neg) < 1e-12 and abs(h_low) < 1e-12:
                            invalid_pairs.append((c, y))

        # Scenario reality guard: if VRE rises materially but stress proxies stay zero across all requested years.
        for c in countries:
            c_rows = annual[(annual["country"] == str(c)) & (annual["year"].isin([int(y) for y in scenario_years]))].sort_values("year")
            if c_rows.empty:
                continue
            vre = pd.to_numeric(c_rows.get("vre_penetration_share_gen"), errors="coerce")
            if vre.notna().sum() >= 2 and float(vre.max() - vre.min()) >= 0.03:
                h_neg = pd.to_numeric(c_rows.get("h_negative"), errors="coerce").fillna(0.0)
                h_low = pd.to_numeric(c_rows.get("h_below_5"), errors="coerce").fillna(0.0)
                sr_h = pd.to_numeric(c_rows.get("sr_hours"), errors="coerce").fillna(0.0)
                if bool(((h_neg.abs() < 1e-12) & (h_low.abs() < 1e-12) & (sr_h.abs() < 1e-12)).all()):
                    for y in c_rows["year"].dropna().astype(int).tolist():
                        invalid_pairs.append((str(c), int(y)))

    missing_pairs = sorted(set(missing_pairs + invalid_pairs))
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
    validation_findings_hist: pd.DataFrame | None = None,
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
            validation_findings_df=validation_findings_hist,
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
                        "horizon_year": max(years) if years else None,
                        "ttl_reference_mode": str(selection.get("ttl_reference_mode", "year_specific")),
                    },
                    run_id=f"{run_id}_{country}",
                    commodity_daily=selection.get("commodity_daily"),
                    ttl_target_eur_mwh=_safe_float(selection.get("ttl_target_eur_mwh"), 120.0),
                    gas_override_eur_mwh_th=selection.get("gas_override_eur_mwh_th"),
                    co2_override_eur_t=selection.get("co2_override_eur_t"),
                    ttl_method=str(selection.get("ttl_reference_mode", "year_specific")),
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
    hourly_hist_map: dict[tuple[str, int], pd.DataFrame] | None = None,
) -> ModuleResult | None:
    qid = question_id.upper()
    if hourly_hist_map is None:
        hourly_hist_map = {}
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
            hourly_map_future = _load_scenario_hourly_map(scenario_id, countries, scenario_years)
            hist_years = _selection_years(selection, annual_hist)
            annual_hist_scen, hourly_map_hist_scen, floor_events = _build_q1_historical_scenario_inputs(
                scenario_id=scenario_id,
                countries=countries,
                historical_years=hist_years,
                scenario_years_for_params=scenario_years,
                annual_hist=annual_hist,
                hourly_hist_map=hourly_hist_map,
                assumptions_phase2=assumptions_phase2,
            )
            annual_all = pd.concat([annual_hist_scen, annual_scen], ignore_index=True) if not annual_hist_scen.empty else annual_scen.copy()
            if not annual_all.empty:
                annual_all = (
                    annual_all.sort_values(["country", "year"])
                    .drop_duplicates(subset=["country", "year"], keep="last")
                    .reset_index(drop=True)
                )
            years_full = sorted(set(pd.to_numeric(annual_all.get("year"), errors="coerce").dropna().astype(int).tolist()))
            if years_full:
                scen_sel["years"] = years_full
                scen_sel["horizon_year"] = int(max(years_full))
            hourly_map_all = dict(hourly_map_hist_scen)
            hourly_map_all.update(hourly_map_future)
            res = run_q1(annual_all, assumptions_phase1, scen_sel, run_id, hourly_by_country_year=hourly_map_all)
            if floor_events:
                for event in floor_events:
                    res.checks.append(
                        {
                            "status": "WARN",
                            "code": "Q1_SCENARIO_FLOOR_APPLIED",
                            "message": (
                                f"{str(event.get('country', '')).strip()}-{str(event.get('scenario_id', scenario_id)).strip()}: "
                                + str(event.get("reason", "floor_applied"))
                            ),
                        }
                    )
            return res
        if qid == "Q2":
            hourly_map = _load_scenario_hourly_map(scenario_id, countries, scenario_years)
            hist_ref = run_q2(
                annual_hist[annual_hist["country"].astype(str).isin(countries)].copy(),
                assumptions_phase1,
                {**selection, "countries": countries, "mode": "HIST"},
                run_id=f"{run_id}_HIST_PHASE2_REF",
                hourly_by_country_year=None,
            )
            slopes_ref = hist_ref.tables.get("Q2_country_slopes", pd.DataFrame()).copy()
            phase2_years_by_country_tech: dict[str, list[int]] = {}
            phase2_start_year_by_country_tech: dict[str, int] = {}
            if not slopes_ref.empty:
                for _, r in slopes_ref.iterrows():
                    c = str(r.get("country", "")).strip()
                    t = str(r.get("tech", "")).strip().upper()
                    if not c or not t:
                        continue
                    key = f"{c}|{t}"
                    years_used_raw = str(r.get("years_used", "")).strip()
                    years_used_vals: list[int] = []
                    if years_used_raw:
                        for tok in years_used_raw.split(","):
                            yv = _safe_float(tok.strip(), np.nan)
                            if np.isfinite(yv):
                                years_used_vals.append(int(yv))
                    if years_used_vals:
                        phase2_years_by_country_tech[key] = sorted(set(years_used_vals))
                    y_start = _safe_float(r.get("phase2_start_year_for_slope"), np.nan)
                    if np.isfinite(y_start):
                        phase2_start_year_by_country_tech[key] = int(y_start)
            scen_sel = {
                **scen_sel,
                "phase2_years_by_country_tech": phase2_years_by_country_tech,
                "phase2_start_year_by_country_tech": phase2_start_year_by_country_tech,
            }
            return run_q2(annual_scen, assumptions_phase1, scen_sel, run_id, hourly_by_country_year=hourly_map)
        hourly_map = _load_scenario_hourly_map(scenario_id, countries, scenario_years)
        annual_hist_scoped = annual_hist[annual_hist["country"].astype(str).isin(countries)].copy()
        annual_all = pd.concat([annual_hist_scoped, annual_scen], ignore_index=True)
        if not annual_all.empty:
            annual_all["country"] = annual_all["country"].astype(str)
            annual_all["year"] = pd.to_numeric(annual_all["year"], errors="coerce")
            annual_all = (
                annual_all.sort_values(["country", "year"])
                .drop_duplicates(subset=["country", "year"], keep="last")
                .reset_index(drop=True)
            )
        hourly_map_all = dict(hourly_hist_map)
        hourly_map_all.update(hourly_map)
        q3_hist_stage2_reference_by_country: dict[str, bool] = {}
        all_params = {
            str(r["param_name"]): float(r["param_value"])
            for _, r in assumptions_phase1.iterrows()
            if str(r.get("param_name", "")).strip() != ""
        }
        for country in countries:
            c_rows = annual_hist_scoped[annual_hist_scoped["country"].astype(str) == str(country)].copy()
            if c_rows.empty:
                continue
            c_rows["year"] = pd.to_numeric(c_rows["year"], errors="coerce")
            c_rows = c_rows.sort_values("year")
            q3_hist_stage2_reference_by_country[str(country)] = bool(
                _stage2_active_hist_reference(c_rows.iloc[-1], all_params)
            )
        scen_sel = {
            **scen_sel,
            "q3_hist_stage2_reference_by_country": q3_hist_stage2_reference_by_country,
            "q3_force_scenario_applicability_from_hist": True,
        }
        assumptions_q3 = assumptions_phase1.copy()
        if len(scenario_years) < 3:
            mask = assumptions_q3["param_name"].astype(str) == "trend_window_years"
            if mask.any():
                assumptions_q3.loc[mask, "param_value"] = 2
        return run_q3(annual_all if not annual_all.empty else annual_scen, hourly_map_all, assumptions_q3, scen_sel, run_id)

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
        base_anchor_by_country_input = selection.get("base_anchor_by_country", {})
        base_anchor_by_country: dict[str, dict[str, Any]] = {}
        if isinstance(base_anchor_by_country_input, dict):
            for c, payload in base_anchor_by_country_input.items():
                if isinstance(payload, dict):
                    base_anchor_by_country[str(c)] = dict(payload)
        sid_upper = str(scenario_id).upper()
        requires_base_ref = sid_upper.startswith("HIGH_") and sid_upper not in {"BASE", "HIST"}
        if requires_base_ref:
            for c in countries:
                c_key = str(c)
                anchor_ref = base_anchor_by_country.get(c_key, {})
                if not (isinstance(anchor_ref, dict) and anchor_ref):
                    resolved_anchor, _ = _resolve_q5_base_anchor_for_country(
                        country=c_key,
                        years=years,
                        annual_hist=annual_hist,
                        assumptions_phase1=assumptions_phase1,
                        assumptions_phase2=assumptions_phase2,
                        selection=selection,
                        run_id=run_id,
                    )
                    if resolved_anchor:
                        base_anchor_by_country[c_key] = resolved_anchor
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
            anchor_ref = base_anchor_by_country.get(str(country), {}) if isinstance(base_anchor_by_country, dict) else {}
            if requires_base_ref and not (isinstance(anchor_ref, dict) and anchor_ref):
                scen_sel["base_ref_status_override"] = "missing_base"
                scen_sel["base_ref_reason_override"] = "missing_phase2_assumptions_table_for_this_year"
            elif isinstance(anchor_ref, dict):
                for key in [
                    "base_tca_eur_mwh",
                    "base_tca_ccgt_eur_mwh",
                    "base_tca_coal_eur_mwh",
                    "base_ttl_observed_eur_mwh",
                    "base_ttl_model_eur_mwh",
                    "base_gas_eur_per_mwh_th",
                    "base_co2_eur_per_t",
                    "base_year_reference",
                    "base_ref_source_year",
                ]:
                    value = _safe_float(anchor_ref.get(key), np.nan)
                    if np.isfinite(value):
                        scen_sel[key] = value
                status_override = str(anchor_ref.get("base_ref_status_override", "")).strip()
                reason_override = str(anchor_ref.get("base_ref_reason_override", "")).strip()
                if status_override:
                    scen_sel["base_ref_status_override"] = status_override
                if reason_override:
                    scen_sel["base_ref_reason_override"] = reason_override
            runs.append(
                run_q5(
                    hourly_df=hourly,
                    assumptions_df=assumptions_phase1,
                    selection=scen_sel,
                    run_id=f"{run_id}_{country}",
                    commodity_daily=commodity,
                    ttl_target_eur_mwh=_safe_float(selection.get("ttl_target_eur_mwh"), 120.0),
                    ttl_method=str(selection.get("ttl_reference_mode", "year_specific")),
                )
            )
        if not runs:
            return None
        merged = _merge_module_results(
            runs,
            module_id="Q5",
            run_id=run_id,
            selection={**selection, "countries": countries},
            mode="SCEN",
            scenario_id=scenario_id,
            horizon_year=max(years) if years else None,
            narrative_title=f"Q5 scenario {scenario_id}",
        )
        if requires_base_ref:
            q5_tbl = merged.tables.get("Q5_summary", pd.DataFrame())
            if not q5_tbl.empty and "base_ref_status" in q5_tbl.columns:
                status_series = q5_tbl["base_ref_status"].astype(str).str.lower()
                missing_mask = ~status_series.isin(["ok", "warn_fallback_from_hist"])
                if bool(missing_mask.any()):
                    missing_countries = sorted(set(q5_tbl.loc[missing_mask, "country"].astype(str).tolist()))
                    msg = (
                        "Q5 base reference unresolved for countries: "
                        + ", ".join(missing_countries)
                        + ". Action: provide phase2 BASE assumptions for this year or historical fallback inputs."
                    )
                    merged.checks.append(
                        {
                            "status": "FAIL",
                            "code": "Q5_BASE_SCENARIO_MISSING",
                            "message": msg,
                        }
                    )
                    merged.warnings.append(msg)
                else:
                    merged.checks.append(
                        {
                            "status": "PASS",
                            "code": "Q5_BASE_SCENARIO_MISSING",
                            "message": "BASE reference resolved (ok or warn_fallback_from_hist) for all countries.",
                        }
                    )
        return merged

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
        merged = hist[["country", "bascule_year_market", "bascule_status_market"]].merge(
            scen[["country", "bascule_year_market", "bascule_status_market"]],
            on="country",
            how="inner",
            suffixes=("_hist", "_scen"),
        )
        for _, r in merged.iterrows():
            h = _safe_float(r.get("bascule_year_market_hist"), np.nan)
            s = _safe_float(r.get("bascule_year_market_scen"), np.nan)
            hist_value: int | None = int(h) if np.isfinite(h) else None
            scen_value: int | None = int(s) if np.isfinite(s) else None
            delta_years: int | None = (int(scen_value - hist_value) if (hist_value is not None and scen_value is not None) else None)
            scen_status = str(r.get("bascule_status_market_scen", "")).strip().lower()
            hist_status = str(r.get("bascule_status_market_hist", "")).strip().lower()
            if scen_value is None:
                if scen_status in {"not_reached_in_window", "not_reached_by_horizon"}:
                    cmp_status = "OK_NOT_REACHED"
                    cmp_reason = "bascule_not_reached_by_horizon"
                else:
                    cmp_status = "NOT_APPLICABLE"
                    cmp_reason = f"bascule_missing_scenario:{scen_status or 'unknown'}"
            elif hist_value is None:
                cmp_status = "NOT_IN_SCOPE"
                cmp_reason = f"historical_bascule_missing:{hist_status or 'unknown'}"
            else:
                cmp_status = "OK"
                cmp_reason = "delta_interpretable"
            rows.append(
                {
                    "country": r["country"],
                    "scenario_id": sid,
                    "metric": "bascule_year_market",
                    "hist_value": hist_value,
                    "scen_value": scen_value,
                    "delta_years": delta_years,
                    "delta": delta_years,
                    "status": cmp_status,
                    "reason": cmp_reason,
                    "hist_bascule_status": hist_status,
                    "scen_bascule_status": scen_status,
                }
            )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    for col in ["hist_value", "scen_value", "delta_years", "delta"]:
        coerced = [int(v) if np.isfinite(_safe_float(v, np.nan)) else None for v in out[col].tolist()]
        out[col] = pd.Series(coerced, index=out.index, dtype=object)
    return out


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
        metric_cols = ["far_after", "surplus_unabs_energy_after", "pv_capture_price_after"]
        for optional_metric in ["far_before", "surplus_unabs_energy_before"]:
            if optional_metric in hist.columns:
                metric_cols.append(optional_metric)
        for sid, res in scen_results.items():
            scen = res.tables.get("Q4_sizing_summary", pd.DataFrame())
            if scen.empty:
                continue
            if not req_cols.issubset(set(scen.columns)):
                continue
            scen_metric_cols = [m for m in metric_cols if m in scen.columns]
            merged = hist[["country"] + scen_metric_cols].merge(
                scen[["country"] + scen_metric_cols],
                on="country",
                how="inner",
                suffixes=("_hist", "_scen"),
            )
            for _, r in merged.iterrows():
                for metric in scen_metric_cols:
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
        if qid == "Q1":
            cmp_status = str(row.get("status", "")).upper().strip()
            cmp_reason = str(row.get("reason", "")).strip()
            if cmp_status in {"OK", "OK_NOT_REACHED"}:
                statuses.append("INFORMATIVE")
                reasons.append(cmp_reason or "delta_interpretable")
            elif cmp_status == "NOT_IN_SCOPE":
                statuses.append("NON_TESTABLE")
                reasons.append(cmp_reason or "historical_bascule_missing")
            else:
                statuses.append("NON_TESTABLE")
                reasons.append(cmp_reason or "scenario_bascule_missing")
            continue

        h = _safe_float(row.get("hist_value"), np.nan)
        s = _safe_float(row.get("scen_value"), np.nan)
        d = _safe_float(row.get("delta"), np.nan)
        scen_status = str(row.get("scen_status", "")).lower().strip()

        if qid == "Q3" and scen_status in {"hors_scope_stage2", "hors_scope_phase2"}:
            statuses.append("NON_TESTABLE")
            reasons.append("scenario_hors_scope_phase2")
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
    expected_scenario_ids: list[str] | None = None,
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
                        s = summary.copy()
                        for c in [
                            "bascule_status_market",
                            "bascule_status_physical",
                            "market_physical_gap_at_bascule",
                            "sr_energy_at_bascule",
                            "far_energy_at_bascule",
                        ]:
                            if c not in s.columns:
                                s[c] = np.nan if c.endswith("_at_bascule") else ""

                        strict_count = 0
                        explained_count = 0
                        reasons: dict[str, int] = {}

                        for _, r in s.iterrows():
                            m_year = _safe_float(r.get("bascule_year_market"), np.nan)
                            p_year = _safe_float(r.get("bascule_year_physical"), np.nan)
                            m_status = str(r.get("bascule_status_market", "")).strip().lower()
                            p_status = str(r.get("bascule_status_physical", "")).strip().lower()
                            gap_flag = bool(r.get("market_physical_gap_at_bascule", False))
                            sr = _safe_float(r.get("sr_energy_at_bascule"), np.nan)
                            far = _safe_float(r.get("far_energy_at_bascule"), np.nan)
                            high_far_low_sr = bool(np.isfinite(far) and np.isfinite(sr) and far >= 0.95 and sr <= 0.05)

                            reason = "unexplained"
                            strict = False
                            explained = False
                            m_exists = np.isfinite(m_year)
                            p_exists = np.isfinite(p_year)

                            if m_exists and p_exists:
                                if int(m_year) == int(p_year):
                                    strict = True
                                    explained = True
                                    reason = "strict_equal_year"
                                elif abs(int(m_year) - int(p_year)) <= 1:
                                    explained = True
                                    reason = "lag_within_1y"
                                elif gap_flag:
                                    explained = True
                                    reason = "market_physical_gap_flag"
                                elif high_far_low_sr:
                                    explained = True
                                    reason = "high_far_low_sr_divergence"
                                else:
                                    reason = "year_gap_unexplained"
                            elif (not m_exists) and (not p_exists):
                                if m_status == "already_phase2_at_window_start" and p_status == "already_phase2_at_window_start":
                                    explained = True
                                    reason = "both_already_phase2_window_start"
                                elif m_status == "not_reached_in_window" and p_status == "not_reached_in_window":
                                    explained = True
                                    reason = "both_not_reached_in_window"
                                else:
                                    reason = "both_missing_unexplained"
                            elif m_exists and (not p_exists):
                                if m_status == "already_phase2_at_window_start":
                                    explained = True
                                    reason = "market_already_phase2_window_start"
                                elif p_status == "not_reached_in_window" and (gap_flag or high_far_low_sr):
                                    explained = True
                                    reason = "physical_not_reached_but_explained"
                                else:
                                    reason = "market_only_unexplained"
                            else:  # physical exists, market missing
                                if m_status == "already_phase2_at_window_start":
                                    explained = True
                                    reason = "market_already_phase2_before_window"
                                elif m_status == "not_reached_in_window" and p_status == "already_phase2_at_window_start":
                                    explained = True
                                    reason = "physical_already_phase2_window_start"
                                else:
                                    reason = "physical_only_unexplained"

                            strict_count += int(strict)
                            explained_count += int(explained)
                            reasons[reason] = reasons.get(reason, 0) + 1

                        total = int(len(s))
                        strict_share = (strict_count / total) if total > 0 else np.nan
                        concordant_share = (explained_count / total) if total > 0 else np.nan
                        if concordant_share >= 0.80:
                            status = "PASS"
                            interp = "Concordance satisfaisante en comptant les divergences expliquees."
                        elif concordant_share >= 0.50:
                            status = "WARN"
                            interp = "Concordance partielle; divergences a expliquer pays par pays."
                        else:
                            status = "FAIL"
                            interp = "Concordance insuffisante entre diagnostic marche et physique."
                        reason_parts = [f"{k}:{v}" for k, v in sorted(reasons.items(), key=lambda kv: (-kv[1], kv[0]))[:6]]
                        _append_test_row(
                            rows,
                            spec,
                            status,
                            f"strict={strict_share:.2%}; concordant_ou_explique={concordant_share:.2%}; n={total}; explained={explained_count}; reasons={';'.join(reason_parts)}",
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
                    allowed = {"HORS_SCOPE_PHASE2", "CONTINUES", "STOP_POSSIBLE", "STOP_CONFIRMED", "BACK_TO_STAGE1"}
                    ok = (not out.empty) and out["status"].astype(str).str.upper().isin(allowed).all()
                    _append_test_row(rows, spec, "PASS" if ok else "WARN", int(out["status"].nunique()) if not out.empty else 0, "status valides", "Les statuts business sont renseignes.")
            elif qid == "Q4":
                if spec.test_id == "Q4-H-01":
                    expected_modes = {"HIST_PRICE_ARBITRAGE_SIMPLE", "HIST_PV_COLOCATED"}
                    ok = expected_modes.issubset(set(extra_hist.keys()))
                    n_extra = int(len(extra_hist))
                    n_total = 1 + n_extra  # +1 pour le mode SURPLUS_FIRST porte par hist_result
                    value = f"extra_dispatch_modes_executed={n_extra}; total_dispatch_modes_executed={n_total}; extras={','.join(sorted(extra_hist.keys()))}"
                    _append_test_row(
                        rows,
                        spec,
                        _status_from_threshold(spec, condition_met=ok, evaluable=True),
                        value,
                        "extra_dispatch_modes_executed=2 (total_dispatch_modes_executed=3)",
                        "Convention explicite: les modes supplementaires sont comptes hors SURPLUS_FIRST.",
                    )
                else:
                    # Q4-H-02 must stay strict on physical invariants while avoiding
                    # strategy-mode artefacts (PRICE_ARBITRAGE/PV_COLOCATED) that are
                    # not the physically-grounded reference mode for Q4.
                    extra_relevant_fail_codes = {
                        "Q4_EMPTY",
                        "Q4_FRONTIER_KEY_MISSING",
                        "Q4_SUMMARY_FAR_INVALID",
                        "Q4_SOC_NEG",
                        "Q4_SOC_ABOVE_EMAX",
                        "Q4_CHARGE_ABOVE_PMAX",
                        "Q4_DISCHARGE_ABOVE_PMAX",
                        "Q4_FREE_ENERGY_NO_CHARGE",
                        "Q4_ENERGY_BALANCE",
                        "Q4_ENERGY_BALANCE_RESIDUAL",
                        "Q4_SIMULTANEOUS_CHARGE_DISCHARGE",
                        "Q4_CHARGE_EXCEEDS_SURPLUS",
                        "Q4_ZERO_SIZE_NOT_ZERO_FLOW",
                        "Q4_ZERO_SIZE_AFTER_DIFFERS_FROM_BEFORE",
                        "Q4_NO_IMPACT_WITHOUT_DISPATCH",
                        "Q4_SOC_END_BOUNDARY",
                    }
                    hist_country = ""
                    hist_year = ""
                    hist_frontier = hist_result.tables.get("Q4_bess_frontier", pd.DataFrame())
                    if isinstance(hist_frontier, pd.DataFrame) and not hist_frontier.empty:
                        hist_country = str(hist_frontier.iloc[0].get("country", "")).strip()
                        hist_year_val = _safe_float(hist_frontier.iloc[0].get("year"), np.nan)
                        hist_year = str(int(hist_year_val)) if np.isfinite(hist_year_val) else ""
                    if not hist_country:
                        hist_country = str(hist_result.selection.get("country", "")).strip()
                    if not hist_year:
                        hist_year_val = _safe_float(hist_result.selection.get("year"), np.nan)
                        hist_year = str(int(hist_year_val)) if np.isfinite(hist_year_val) else ""

                    hist_fails = [
                        {
                            **c,
                            "_mode": "HIST_SURPLUS_FIRST",
                            "_country": hist_country,
                            "_year": hist_year,
                        }
                        for c in hist_result.checks
                        if str(c.get("status", "")).upper() == "FAIL"
                    ]
                    extra_relevant_fails: list[dict[str, Any]] = []
                    for mode_key, mode_res in extra_hist.items():
                        mode_country = ""
                        mode_year = ""
                        mode_frontier = mode_res.tables.get("Q4_bess_frontier", pd.DataFrame())
                        if isinstance(mode_frontier, pd.DataFrame) and not mode_frontier.empty:
                            mode_country = str(mode_frontier.iloc[0].get("country", "")).strip()
                            mode_year_val = _safe_float(mode_frontier.iloc[0].get("year"), np.nan)
                            mode_year = str(int(mode_year_val)) if np.isfinite(mode_year_val) else ""
                        if not mode_country:
                            mode_country = str(mode_res.selection.get("country", "")).strip()
                        if not mode_year:
                            mode_year_val = _safe_float(mode_res.selection.get("year"), np.nan)
                            mode_year = str(int(mode_year_val)) if np.isfinite(mode_year_val) else ""
                        for c in mode_res.checks:
                            if str(c.get("status", "")).upper() != "FAIL":
                                continue
                            code = str(c.get("code", "")).upper()
                            if code in extra_relevant_fail_codes:
                                extra_relevant_fails.append(
                                    {
                                        **c,
                                        "_mode": str(mode_key),
                                        "_country": mode_country,
                                        "_year": mode_year,
                                    }
                                )
                    evaluated_checks = hist_result.checks + [c for r in extra_hist.values() for c in r.checks]
                    has_fail = bool(hist_fails or extra_relevant_fails)
                    has_warn = any(str(c.get("status", "")).upper() == "WARN" for c in evaluated_checks)
                    fail_codes: dict[str, int] = {}
                    fail_context: dict[str, int] = {}
                    if has_fail:
                        for c in (hist_fails + extra_relevant_fails):
                            code = str(c.get("code", "")).strip().upper() or "UNKNOWN"
                            fail_codes[code] = int(fail_codes.get(code, 0)) + 1
                            mode_ctx = str(c.get("_mode", "")).strip()
                            country_ctx = str(c.get("_country", "")).strip()
                            year_ctx = str(c.get("_year", "")).strip()
                            ctx_parts = [code]
                            if mode_ctx:
                                ctx_parts.append(mode_ctx)
                            if country_ctx:
                                ctx_parts.append(country_ctx)
                            if year_ctx:
                                ctx_parts.append(year_ctx)
                            ctx_key = "@".join(ctx_parts)
                            fail_context[ctx_key] = int(fail_context.get(ctx_key, 0)) + 1
                    fail_top = sorted(fail_codes.items(), key=lambda item: (-item[1], item[0]))[:5]
                    fail_top_text = ",".join([f"{code}(x{count})" if int(count) > 1 else code for code, count in fail_top])
                    fail_ctx_top = sorted(fail_context.items(), key=lambda item: (-item[1], item[0]))[:5]
                    fail_ctx_text = ";".join([f"{ctx}(x{count})" if int(count) > 1 else ctx for ctx, count in fail_ctx_top])
                    if has_fail:
                        status = "FAIL"
                        value = f"FAIL_CODES:{fail_top_text}" if fail_top_text else "FAIL"
                        if fail_ctx_text:
                            value = value + f";CTX:{fail_ctx_text}"
                        interp = "Au moins un invariant physique batterie est viole."
                        if fail_top_text:
                            interp += f" Codes: {fail_top_text}."
                        if fail_ctx_text:
                            interp += f" Contextes: {fail_ctx_text}."
                    else:
                        status = "PASS"
                        value = "WARN" if has_warn else "PASS"
                        interp = "Les invariants physiques batterie sont respectes."
                        if has_warn:
                            interp += " Des avertissements non-physiques peuvent subsister (objectif/scenario)."
                    _append_test_row(rows, spec, status, value, "aucun FAIL physique", interp)
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
                        if "dTCA_dFuel" in out.columns:
                            dfuel = pd.to_numeric(out["dTCA_dFuel"], errors="coerce")
                        else:
                            dfuel = pd.to_numeric(out["dTCA_dGas"], errors="coerce") if "dTCA_dGas" in out.columns else pd.Series(dtype=float)
                        ok_share = float(((dco2 > 0) & (dfuel > 0)).mean()) if len(out) else 0.0
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
            scenario_ids_eval = [str(s) for s in (expected_scenario_ids or sorted(scen_results.keys())) if str(s).strip()]
            if not scenario_ids_eval and scen_results:
                scenario_ids_eval = sorted([str(s) for s in scen_results.keys()])
            if not scenario_ids_eval:
                _append_test_row(rows, spec, "NON_TESTABLE", "", "scenario runs disponibles", "Aucun scenario exploitable.")
                continue
            for sid in scenario_ids_eval:
                scen_res = scen_results.get(sid)
                if scen_res is None:
                    _append_test_row(
                        rows,
                        spec,
                        "NON_TESTABLE",
                        "",
                        "scenario run disponible",
                        "Scenario non produit (missing_output).",
                        sid,
                    )
                    continue
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
                            status = "NON_TESTABLE"
                            if req_defined_share > 0.0:
                                interp = "Aucun delta bascule comparable vs BASE (finite_share=0), meme si des solveurs sont renseignes."
                            else:
                                interp = "Aucun delta defini vs BASE (finite_share=0)."
                        elif nonzero_share >= 0.20:
                            status = _status_from_threshold(spec, condition_met=True, evaluable=True)
                            interp = "Sensibilite scenario observable vs BASE."
                        else:
                            status = _status_from_threshold(spec, condition_met=False, evaluable=True)
                            if nonzero_share == 0.0:
                                interp = "Delta vs BASE defini mais nul sur tous les pays."
                            else:
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
                            status_up = out["status"].astype(str).str.upper()
                            share_hs = float((status_up.isin(["HORS_SCOPE_STAGE2", "HORS_SCOPE_PHASE2"])).mean()) if "status" in out.columns else np.nan
                            if np.isfinite(share_hs) and share_hs >= 0.80:
                                _append_test_row(
                                    rows,
                                    spec,
                                    "NON_TESTABLE",
                                    f"hors_scope={share_hs:.2%}",
                                    "hors_scope < 80%",
                                    "Scenario majoritairement hors scope Stage 2: test non interpretable.",
                                    sid,
                                )
                            else:
                                _append_test_row(rows, spec, "PASS", int(len(out)), "colonnes inversion presentes", "Les ordres de grandeur d'inversion sont quantifies.", sid)
                    else:
                        if out.empty or "status" not in out.columns:
                            _append_test_row(rows, spec, "NON_TESTABLE", "", "status scenario disponibles", "Impossible d'evaluer la transition phase 3 (sortie scenario manquante).", sid)
                        else:
                            status_up = out["status"].astype(str).str.upper()
                            share_hs = float((status_up.isin(["HORS_SCOPE_STAGE2", "HORS_SCOPE_PHASE2"])).mean())
                            if share_hs >= 0.80:
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


def _check_q1_scenario_effect_present(comparison: pd.DataFrame) -> list[dict[str, Any]]:
    if comparison is None or comparison.empty:
        return [
            {
                "status": "NON_TESTABLE",
                "code": "Q1_SCENARIO_EFFECT_PRESENT",
                "message": "Comparaison Q1 indisponible.",
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        ]
    if "scenario_id" not in comparison.columns or "delta" not in comparison.columns:
        return [
            {
                "status": "NON_TESTABLE",
                "code": "Q1_SCENARIO_EFFECT_PRESENT",
                "message": "Colonnes scenario_id/delta manquantes pour Q1.",
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        ]

    scen_ids = comparison["scenario_id"].astype(str).str.upper().str.strip()
    non_base = comparison[scen_ids != "BASE"].copy()
    if non_base.empty:
        return [
            {
                "status": "NON_TESTABLE",
                "code": "Q1_SCENARIO_EFFECT_PRESENT",
                "message": "Aucun scenario non-BASE a evaluer pour Q1.",
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        ]

    delta = pd.to_numeric(non_base["delta"], errors="coerce")
    finite = delta[np.isfinite(delta)]
    if finite.empty:
        return [
            {
                "status": "NON_TESTABLE",
                "code": "Q1_SCENARIO_EFFECT_PRESENT",
                "message": "Aucun delta fini sur scenarios non-BASE pour Q1.",
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        ]

    nonzero = int((finite.abs() > 1e-9).sum())
    total = int(len(finite))
    share = nonzero / total if total > 0 else 0.0
    status = "FAIL" if nonzero == 0 else "PASS"
    return [
        {
            "status": status,
            "code": "Q1_SCENARIO_EFFECT_PRESENT",
            "message": (
                f"nonzero_share={share:.2%}; nonzero={nonzero}; finite={total}. "
                + ("Les scenarios non-BASE n'ont aucun effet detectable." if status == "FAIL" else "Effet scenario detectable.")
            ),
            "scope": "BUNDLE",
            "scenario_id": "",
        }
    ]


def _check_q3_scenario_stress_sufficiency(comparison: pd.DataFrame) -> list[dict[str, Any]]:
    if comparison is None or comparison.empty:
        return [
            {
                "status": "NON_TESTABLE",
                "code": "Q3_SCENARIO_STRESS_SUFFICIENCY",
                "message": "Comparaison Q3 indisponible.",
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        ]
    if "scenario_id" not in comparison.columns or "scen_status" not in comparison.columns:
        return [
            {
                "status": "NON_TESTABLE",
                "code": "Q3_SCENARIO_STRESS_SUFFICIENCY",
                "message": "Colonnes scenario_id/scen_status manquantes pour Q3.",
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        ]

    scen_ids = comparison["scenario_id"].astype(str).str.upper().str.strip()
    non_base = comparison[scen_ids != "BASE"].copy()
    if non_base.empty:
        return [
            {
                "status": "NON_TESTABLE",
                "code": "Q3_SCENARIO_STRESS_SUFFICIENCY",
                "message": "Aucun scenario non-BASE a evaluer pour Q3.",
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        ]

    rows: list[tuple[str, float]] = []
    for sid, grp in non_base.groupby("scenario_id"):
        statuses = grp["scen_status"].astype(str).str.upper().str.strip()
        if len(statuses) == 0:
            continue
        share_hors_scope = float((statuses == "HORS_SCOPE_PHASE2").mean())
        rows.append((str(sid), share_hors_scope))

    if not rows:
        return [
            {
                "status": "NON_TESTABLE",
                "code": "Q3_SCENARIO_STRESS_SUFFICIENCY",
                "message": "Impossible de calculer la part hors scope sur scenarios non-BASE.",
                "scope": "BUNDLE",
                "scenario_id": "",
            }
        ]

    fail_all = all(share >= 0.90 for _, share in rows)
    details = "; ".join([f"{sid}:{share:.0%}" for sid, share in rows])
    return [
        {
            "status": "FAIL" if fail_all else "PASS",
            "code": "Q3_SCENARIO_STRESS_SUFFICIENCY",
            "message": (
                f"hors_scope_share_non_base={details}. "
                + ("Stress scenario insuffisant (>=90% hors scope sur tous les scenarios non-BASE)." if fail_all else "Stress scenario exploitable.")
            ),
            "scope": "BUNDLE",
            "scenario_id": "",
        }
    ]


def run_question_bundle(
    question_id: str,
    annual_hist: pd.DataFrame,
    hourly_hist_map: dict[tuple[str, int], pd.DataFrame],
    assumptions_phase1: pd.DataFrame,
    assumptions_phase2: pd.DataFrame,
    selection: dict[str, Any],
    run_id: str,
    validation_findings_hist: pd.DataFrame | None = None,
) -> QuestionBundleResult:
    qid = str(question_id).upper()
    countries = _selection_countries(selection, annual_hist)
    years = _selection_years(selection, annual_hist)
    scenario_ids = [str(s) for s in selection.get("scenario_ids", get_default_scenarios(qid))]
    scenario_ids = [s for s in scenario_ids if s]
    if qid == "Q5" and "BASE" in scenario_ids:
        scenario_ids = ["BASE"] + [s for s in scenario_ids if s != "BASE"]
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
        validation_findings_hist=validation_findings_hist,
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
        scen_selection = {**selection, "run_id": run_id}
        if qid == "Q5" and sid != "BASE" and "BASE" in scen_results:
            base_tbl = scen_results["BASE"].tables.get("Q5_summary", pd.DataFrame())
            if not base_tbl.empty:
                base_map: dict[str, dict[str, float]] = {}
                for _, brow in base_tbl.iterrows():
                    ctry = str(brow.get("country", "")).strip()
                    if not ctry:
                        continue
                    base_map[ctry] = {
                        "base_tca_eur_mwh": _safe_float(
                            brow.get("tca_current_eur_mwh", brow.get("ttl_anchor_formula")),
                            np.nan,
                        ),
                        "base_tca_ccgt_eur_mwh": _safe_float(
                            brow.get("tca_ccgt_eur_mwh", brow.get("tca_current_eur_mwh", brow.get("ttl_anchor_formula"))),
                            np.nan,
                        ),
                        "base_tca_coal_eur_mwh": _safe_float(
                            brow.get("tca_coal_eur_mwh"),
                            np.nan,
                        ),
                        "base_ttl_observed_eur_mwh": _safe_float(
                            brow.get("ttl_observed_eur_mwh", brow.get("ttl_obs")),
                            np.nan,
                        ),
                        "base_ttl_model_eur_mwh": _safe_float(
                            brow.get("ttl_model_eur_mwh", brow.get("ttl_observed_eur_mwh", brow.get("ttl_obs"))),
                            np.nan,
                        ),
                        "base_gas_eur_per_mwh_th": _safe_float(
                            brow.get("assumed_gas_price_eur_mwh_th"),
                            np.nan,
                        ),
                        "base_co2_eur_per_t": _safe_float(
                            brow.get("assumed_co2_price_eur_t"),
                            np.nan,
                        ),
                        "base_year_reference": _safe_float(
                            brow.get("ttl_reference_year", brow.get("year")),
                            np.nan,
                        ),
                    }
                if base_map:
                    scen_selection["base_anchor_by_country"] = base_map

        scen_res = _run_scen_module(
            question_id=qid,
            scenario_id=sid,
            annual_hist=annual_hist,
            hourly_hist_map=hourly_hist_map,
            assumptions_phase1=assumptions_phase1,
            assumptions_phase2=assumptions_phase2,
            selection=scen_selection,
            scenario_years=scenario_years,
        )
        if scen_res is None:
            warnings.append(f"{sid}: scenario result non disponible.")
            continue
        scen_results[sid] = scen_res

    if qid in {"Q1", "Q2"} and "BASE" in [str(s) for s in scenario_ids]:
        if "BASE" not in scen_results:
            warnings.append("BASE: fallback explicite sur historique (scenario non disponible).")
        else:
            warnings.append("BASE: normalise sur historique pour garantir comparabilite Q1/Q2.")
        scen_results["BASE"] = _clone_hist_result_as_base_scenario(hist_result, run_id=run_id)

    specs = get_question_tests(qid)
    ledger = _evaluate_test_ledger(
        qid,
        specs,
        hist_result,
        scen_results,
        extra_hist,
        expected_scenario_ids=scenario_ids,
    )
    comparison = _comparison_for_question(qid, hist_result, scen_results, extra_hist)
    comparison = _annotate_comparison_interpretability(qid, comparison)

    checks: list[dict[str, Any]] = []
    q4_extra_mode_checks = pd.DataFrame()
    for c in hist_result.checks:
        checks.append({**c, "scope": "HIST", "scenario_id": ""})
    for sid, scen_res in scen_results.items():
        for c in scen_res.checks:
            checks.append({**c, "scope": "SCEN", "scenario_id": sid})
    if qid == "Q4" and extra_hist:
        rows_extra: list[dict[str, Any]] = []
        for mode_key, mode_res in extra_hist.items():
            mode_suffix = str(mode_key).strip()
            if mode_suffix.upper().startswith("HIST_"):
                mode_suffix = mode_suffix[len("HIST_") :]
            mode_scope = f"HIST_MODE_{mode_suffix}"
            mode_frontier = mode_res.tables.get("Q4_bess_frontier", pd.DataFrame())
            mode_country = str(mode_res.selection.get("country", "")).strip()
            mode_year = _safe_float(mode_res.selection.get("year"), np.nan)
            mode_power = np.nan
            mode_duration = np.nan
            mode_dispatch = str(mode_res.selection.get("dispatch_mode", mode_suffix)).strip()
            if isinstance(mode_frontier, pd.DataFrame) and not mode_frontier.empty:
                first_row = mode_frontier.iloc[0]
                mode_country = str(first_row.get("country", mode_country)).strip()
                mode_year = _safe_float(first_row.get("year", mode_year), mode_year)
                mode_power = _safe_float(first_row.get("bess_power_mw_test"), np.nan)
                mode_duration = _safe_float(first_row.get("bess_duration_h_test"), np.nan)
                mode_dispatch = str(first_row.get("dispatch_mode", mode_dispatch)).strip()
            for c in mode_res.checks:
                checks.append({**c, "scope": mode_scope, "scenario_id": str(mode_key)})
                rows_extra.append(
                    {
                        "mode_key": str(mode_key),
                        "scope": mode_scope,
                        "dispatch_mode": mode_dispatch,
                        "country": mode_country,
                        "year": int(mode_year) if np.isfinite(mode_year) else np.nan,
                        "scenario_id": str(mode_res.scenario_id or mode_key),
                        "bess_power_mw_test": mode_power,
                        "bess_duration_h_test": mode_duration,
                        "status": str(c.get("status", "")),
                        "code": str(c.get("code", "")),
                        "message": str(c.get("message", "")),
                    }
                )
        if rows_extra:
            q4_extra_mode_checks = pd.DataFrame(rows_extra)
            hist_result.tables["Q4_extra_mode_checks"] = q4_extra_mode_checks

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
                if "FAIL" in statuses:
                    checks.append(
                        {
                            "status": "FAIL",
                            "code": "Q1_S02_NO_SENSITIVITY",
                            "message": "Q1-S-02: au moins un scenario non-BASE est en echec explicite.",
                            "scope": "BUNDLE",
                            "scenario_id": "",
                        }
                    )
                elif statuses.issubset({"WARN", "NON_TESTABLE"}):
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
        if qid == "Q5":
            base_res = scen_results.get("BASE")
            co2_res = scen_results.get("HIGH_CO2")
            gas_res = scen_results.get("HIGH_GAS")
            base_tbl = base_res.tables.get("Q5_summary", pd.DataFrame()) if base_res is not None else pd.DataFrame()
            co2_tbl = co2_res.tables.get("Q5_summary", pd.DataFrame()) if co2_res is not None else pd.DataFrame()
            gas_tbl = gas_res.tables.get("Q5_summary", pd.DataFrame()) if gas_res is not None else pd.DataFrame()

            def _first_numeric_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
                for c in candidates:
                    if c in df.columns:
                        return c
                return None

            if base_tbl.empty or (co2_tbl.empty and gas_tbl.empty):
                checks.append(
                    {
                        "status": "WARN",
                        "code": "TEST_Q5_001",
                        "message": "Comparaison BASE/HIGH_CO2/HIGH_GAS indisponible (table Q5_summary manquante).",
                        "scope": "BUNDLE",
                        "scenario_id": "",
                    }
                )
                checks.append(
                    {
                        "status": "WARN",
                        "code": "TEST_Q5_002",
                        "message": "Impossible d'evaluer la coherence delta_ttl_vs_base vs delta_tca_vs_base (donnees manquantes).",
                        "scope": "BUNDLE",
                        "scenario_id": "",
                    }
                )
            else:
                # Harmonized key for cross-scenario matching.
                def _norm(df: pd.DataFrame, sid: str) -> pd.DataFrame:
                    out_df = df.copy()
                    out_df["scenario_id"] = sid
                    if "country" not in out_df.columns:
                        out_df["country"] = ""
                    if "year" in out_df.columns:
                        out_df["year_key"] = pd.to_numeric(out_df["year"], errors="coerce")
                    elif "ttl_reference_year" in out_df.columns:
                        out_df["year_key"] = pd.to_numeric(out_df["ttl_reference_year"], errors="coerce")
                    else:
                        out_df["year_key"] = np.nan
                    return out_df

                base_n = _norm(base_tbl, "BASE")
                tca_col = _first_numeric_col(base_n, ["tca_ccgt_eur_mwh", "tca_q95", "ttl_anchor_formula", "ttl_anchor"])
                ttl_col = _first_numeric_col(base_n, ["ttl_eur_mwh", "ttl_obs", "ttl_target", "ttl_anchor"])
                if tca_col is None:
                    checks.append(
                        {
                            "status": "WARN",
                            "code": "TEST_Q5_001",
                            "message": "Colonne TCA absente de Q5_summary (BASE).",
                            "scope": "BUNDLE",
                            "scenario_id": "",
                        }
                    )
                else:
                    tca_fail = False
                    sign_pairs = 0
                    sign_same = 0

                    def _eval_vs_base(scen_df: pd.DataFrame, sid: str) -> None:
                        nonlocal tca_fail, sign_pairs, sign_same
                        if scen_df.empty:
                            return
                        s_n = _norm(scen_df, sid)
                        merge_cols = ["country", "year_key"]
                        merged = s_n.merge(
                            base_n[merge_cols + [tca_col] + ([ttl_col] if ttl_col is not None else [])].rename(
                                columns={
                                    tca_col: "tca_base",
                                    ttl_col: "ttl_base" if ttl_col is not None else ttl_col,
                                }
                            ),
                            on=merge_cols,
                            how="inner",
                        )
                        if merged.empty:
                            return
                        tca_scen = pd.to_numeric(merged.get(tca_col), errors="coerce")
                        tca_base = pd.to_numeric(merged.get("tca_base"), errors="coerce")
                        delta_tca = tca_scen - tca_base
                        bad = delta_tca < -1e-9
                        if bool(bad.any()):
                            tca_fail = True
                            bad_rows = merged[bad].head(3)
                            for _, bad_row in bad_rows.iterrows():
                                checks.append(
                                    {
                                        "status": "FAIL",
                                        "code": "TEST_Q5_001",
                                        "message": f"{sid}<{bad_row.get('country','?')}>: tca scenario < base.",
                                        "scope": "BUNDLE",
                                        "scenario_id": "",
                                    }
                                )
                        if ttl_col is None or "ttl_base" not in merged.columns:
                            return
                        ttl_scen = pd.to_numeric(merged.get(ttl_col), errors="coerce")
                        ttl_base = pd.to_numeric(merged.get("ttl_base"), errors="coerce")
                        delta_ttl = ttl_scen - ttl_base
                        for dtca, dttl in zip(delta_tca.to_numpy(dtype=float), delta_ttl.to_numpy(dtype=float)):
                            if not (np.isfinite(dtca) and np.isfinite(dttl)):
                                continue
                            sign_tca = 0 if abs(dtca) <= 1e-9 else (1 if dtca > 0 else -1)
                            sign_ttl = 0 if abs(dttl) <= 1e-9 else (1 if dttl > 0 else -1)
                            if sign_tca == 0 or sign_ttl == 0:
                                continue
                            sign_pairs += 1
                            if sign_tca == sign_ttl:
                                sign_same += 1

                    _eval_vs_base(co2_tbl, "HIGH_CO2")
                    _eval_vs_base(gas_tbl, "HIGH_GAS")

                    if not tca_fail:
                        checks.append(
                            {
                                "status": "PASS",
                                "code": "TEST_Q5_001",
                                "message": "HIGH_CO2/HIGH_GAS: TCA scenario >= BASE sur les paires comparables.",
                                "scope": "BUNDLE",
                                "scenario_id": "",
                            }
                        )
                    if sign_pairs > 0:
                        share = sign_same / sign_pairs
                        checks.append(
                            {
                                "status": "PASS" if share >= 0.5 else "WARN",
                                "code": "TEST_Q5_002",
                                "message": f"Coherence signe delta_ttl vs delta_tca: {share:.1%} ({sign_same}/{sign_pairs}).",
                                "scope": "BUNDLE",
                                "scenario_id": "",
                            }
                        )
                    else:
                        checks.append(
                            {
                                "status": "WARN",
                                "code": "TEST_Q5_002",
                                "message": "Aucune paire exploitable pour comparer les signes delta_ttl_vs_base et delta_tca_vs_base.",
                                "scope": "BUNDLE",
                                "scenario_id": "",
                            }
                        )

    module_scopes: list[tuple[str, ModuleResult]] = [("HIST", hist_result)]
    module_scopes.extend([(f"SCEN:{sid}", res) for sid, res in scen_results.items()])
    checks.extend(_check_non_negative_fields(module_scopes))
    if qid == "Q4":
        checks.extend(_check_q4_reporting_consistency(hist_result, scen_results, comparison))
    if qid == "Q5":
        checks.extend(_check_q5_ttl_obs_consistency(hist_result, scen_results, comparison))
    if qid == "Q1":
        checks.extend(_check_q1_scenario_effect_present(comparison))
    if qid == "Q3":
        checks.extend(_check_q3_scenario_stress_sufficiency(comparison))

    if not ledger.empty:
        ledger_fail_count = int((ledger["status"].astype(str) == "FAIL").sum())
        consolidated_fail_checks = [
            c
            for c in checks
            if str(c.get("status", "")).upper() == "FAIL"
            and str(c.get("code", "")).upper() != "BUNDLE_LEDGER_STATUS"
        ]
        consolidated_fail_count = int(len(consolidated_fail_checks))
        if ledger_fail_count == 0 and consolidated_fail_count > 0:
            mismatch_only_bundle_diagnostics = bool(
                all(
                    str(c.get("scope", "")).upper() == "BUNDLE"
                    and not str(c.get("code", "")).upper().startswith("TEST_")
                    for c in consolidated_fail_checks
                )
            )
            mismatch_status = "WARN" if mismatch_only_bundle_diagnostics else "FAIL"
            mismatch_reason = (
                "ecart lie uniquement a des checks bundle diagnostiques."
                if mismatch_only_bundle_diagnostics
                else "ecart lie a des checks consolides critiques."
            )
            checks.append(
                {
                    "status": mismatch_status,
                    "code": "BUNDLE_LEDGER_CONSOLIDATED_MISMATCH",
                    "message": (
                        "Le ledger affiche FAIL=0 alors que des checks consolides sont en FAIL "
                        f"({mismatch_reason})"
                    ),
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
    checks_df = pd.DataFrame(checks)
    check_pass = int((checks_df.get("status", pd.Series(dtype=object)).astype(str).str.upper() == "PASS").sum()) if not checks_df.empty else 0
    check_warn = int((checks_df.get("status", pd.Series(dtype=object)).astype(str).str.upper() == "WARN").sum()) if not checks_df.empty else 0
    check_fail = int((checks_df.get("status", pd.Series(dtype=object)).astype(str).str.upper() == "FAIL").sum()) if not checks_df.empty else 0
    check_nt = int((checks_df.get("status", pd.Series(dtype=object)).astype(str).str.upper() == "NON_TESTABLE").sum()) if not checks_df.empty else 0

    narrative = (
        f"Analyse complete {qid}: historique + prospectif en un seul run. "
        f"Statut global={overall}. Tests PASS={n_pass}, WARN={n_warn}, FAIL={n_fail}, NON_TESTABLE={n_nt}. "
        f"Checks PASS={check_pass}, WARN={check_warn}, FAIL={check_fail}, NON_TESTABLE={check_nt}. "
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
