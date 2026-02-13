from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import pandas as pd

from app.llm_analysis import LLM_REPORTS_DIR, run_llm_analysis, serialize_bundle_for_llm
from app.page_utils import (
    available_phase2_years,
    build_bundle_hash,
    default_analysis_scenario_years,
    run_question_bundle_cached,
)
from src.modules.test_registry import get_default_scenarios

QUESTION_ORDER = ["Q1", "Q2", "Q3", "Q4", "Q5"]


def _normalized_country_cfg(countries_cfg: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(countries_cfg, dict):
        return {}
    nested = countries_cfg.get("countries")
    if isinstance(nested, dict):
        return nested
    return countries_cfg


def _default_scenario_ids(question_id: str, scenario_options: list[str]) -> list[str]:
    defaults = [s for s in get_default_scenarios(question_id) if s in scenario_options]
    return defaults or scenario_options[:2]


def _scenario_year_defaults(
    assumptions_phase2: pd.DataFrame,
    scenario_ids: list[str],
    countries: list[str],
) -> list[int]:
    years = available_phase2_years(
        assumptions_phase2,
        scenario_ids=scenario_ids,
        countries=countries,
    )
    return default_analysis_scenario_years(years)


def build_default_selection(
    question_id: str,
    annual_hist: pd.DataFrame,
    assumptions_phase2: pd.DataFrame,
    countries_cfg: dict[str, Any],
) -> dict[str, Any]:
    qid = str(question_id).upper()
    if qid not in QUESTION_ORDER:
        raise ValueError(f"Question non supportee: {question_id}")
    if annual_hist is None or annual_hist.empty:
        raise ValueError("annual_metrics historique vide.")

    countries_hist = sorted(annual_hist["country"].dropna().astype(str).unique().tolist())
    if not countries_hist:
        raise ValueError("Aucun pays historique disponible.")
    y_min = int(pd.to_numeric(annual_hist["year"], errors="coerce").min())
    y_max = int(pd.to_numeric(annual_hist["year"], errors="coerce").max())

    scenario_options = sorted(set(assumptions_phase2.get("scenario_id", pd.Series(dtype=str)).dropna().astype(str).tolist()))
    scenario_defaults = _default_scenario_ids(qid, scenario_options)

    if qid in {"Q1", "Q2", "Q3"}:
        scenario_years = _scenario_year_defaults(assumptions_phase2, scenario_options, countries_hist)
        years = list(range(y_min, y_max + 1))
        if qid == "Q2":
            years = list(range(2018, 2025))
        return {
            "countries": countries_hist,
            "years": years,
            "scenario_ids": scenario_defaults,
            "scenario_years": scenario_years,
        }

    cfg_countries = _normalized_country_cfg(countries_cfg)
    country_options = sorted(str(c) for c in cfg_countries.keys()) or countries_hist
    default_country = "FR" if "FR" in country_options else country_options[0]

    if qid == "Q4":
        scenario_years = _scenario_year_defaults(assumptions_phase2, scenario_options, country_options)
        default_horizon = max(scenario_years) if scenario_years else 2035
        return {
            "country": default_country,
            "countries": [default_country],
            "year": 2024,
            "years": [2024],
            "horizon_year": int(default_horizon),
            "scenario_ids": scenario_defaults,
            "scenario_years": [int(default_horizon)],
            "objective": "FAR_TARGET",
        }

    # Q5
    countries_sel = [default_country]
    q5_scenario_options = sorted(set(scenario_options + ["HIGH_BOTH"]))
    q5_default_scen = _default_scenario_ids("Q5", q5_scenario_options)
    scenario_years = _scenario_year_defaults(
        assumptions_phase2,
        [s for s in q5_scenario_options if s != "HIGH_BOTH"],
        countries_hist,
    )
    marginal_tech = "CCGT"
    tech_map = {
        c: str(cfg_countries.get(c, {}).get("thermal", {}).get("marginal_tech", marginal_tech)).upper()
        for c in countries_sel
    }
    return {
        "country": countries_sel[0],
        "countries": countries_sel,
        "years": list(range(max(y_min, 2021), y_max + 1)),
        "scenario_ids": q5_default_scen,
        "scenario_years": scenario_years,
        "marginal_tech": marginal_tech,
        "marginal_tech_by_country": tech_map,
        "ttl_target_eur_mwh": 120.0,
    }


def prepare_bundle_for_question(
    question_id: str,
    selection: dict[str, Any],
    assumptions_phase1: pd.DataFrame,
    assumptions_phase2: pd.DataFrame,
) -> dict[str, Any]:
    qid = str(question_id).upper()
    bundle_hash = build_bundle_hash(qid, selection, assumptions_phase1, assumptions_phase2)
    bundle = run_question_bundle_cached(qid, bundle_hash, selection)
    bundle_data = serialize_bundle_for_llm(bundle)
    return {
        "question_id": qid,
        "selection": selection,
        "bundle_hash": bundle_hash,
        "bundle": bundle,
        "bundle_data": bundle_data,
    }


def run_parallel_llm_generation(
    prepared_items: list[dict[str, Any]],
    api_key: str,
    max_workers: int = 5,
) -> list[dict[str, Any]]:
    if not api_key:
        raise ValueError("API key OpenAI manquante.")

    results: list[dict[str, Any]] = []
    runnable: list[dict[str, Any]] = []

    for item in prepared_items:
        qid = str(item.get("question_id", "")).upper()
        bundle_hash = str(item.get("bundle_hash", ""))
        if item.get("status") == "FAILED_PREP":
            results.append(
                {
                    "question_id": qid,
                    "status": "FAILED_PREP",
                    "bundle_hash": bundle_hash,
                    "tokens_input": 0,
                    "tokens_output": 0,
                    "error": str(item.get("error", "Preparation echouee.")),
                    "report_file": None,
                }
            )
            continue
        if not bundle_hash or not item.get("bundle_data"):
            results.append(
                {
                    "question_id": qid,
                    "status": "FAILED_PREP",
                    "bundle_hash": bundle_hash,
                    "tokens_input": 0,
                    "tokens_output": 0,
                    "error": "Bundle incomplet pour l'appel LLM.",
                    "report_file": None,
                }
            )
            continue
        runnable.append(item)

    with ThreadPoolExecutor(max_workers=max(1, int(max_workers))) as pool:
        future_map = {
            pool.submit(
                run_llm_analysis,
                item["question_id"],
                item["bundle_hash"],
                item["bundle_data"],
                api_key,
            ): item
            for item in runnable
        }

        for future in as_completed(future_map):
            item = future_map[future]
            qid = str(item["question_id"]).upper()
            bundle_hash = str(item["bundle_hash"])
            report_file = LLM_REPORTS_DIR / f"{qid}_{bundle_hash}.json"
            try:
                report = future.result()
            except Exception as exc:
                results.append(
                    {
                        "question_id": qid,
                        "status": "FAILED_LLM",
                        "bundle_hash": bundle_hash,
                        "tokens_input": 0,
                        "tokens_output": 0,
                        "error": str(exc),
                        "report_file": None,
                    }
                )
                continue

            error = report.get("error")
            if error:
                results.append(
                    {
                        "question_id": qid,
                        "status": "FAILED_LLM",
                        "bundle_hash": bundle_hash,
                        "tokens_input": 0,
                        "tokens_output": 0,
                        "error": str(error),
                        "report_file": None,
                    }
                )
                continue

            if not report_file.exists():
                results.append(
                    {
                        "question_id": qid,
                        "status": "FAILED_SAVE",
                        "bundle_hash": bundle_hash,
                        "tokens_input": int(report.get("tokens_input", 0) or 0),
                        "tokens_output": int(report.get("tokens_output", 0) or 0),
                        "error": "Rapport non trouve apres generation.",
                        "report_file": None,
                    }
                )
                continue

            results.append(
                {
                    "question_id": qid,
                    "status": "OK",
                    "bundle_hash": bundle_hash,
                    "tokens_input": int(report.get("tokens_input", 0) or 0),
                    "tokens_output": int(report.get("tokens_output", 0) or 0),
                    "error": "",
                    "report_file": str(report_file),
                }
            )

    order = {qid: idx for idx, qid in enumerate(QUESTION_ORDER)}
    return sorted(results, key=lambda row: (order.get(str(row.get("question_id", "")).upper(), 99), str(row.get("question_id", ""))))


def validate_llm_batch_rows(
    rows: list[dict[str, Any]],
    expected_by_qid: dict[str, str],
) -> tuple[list[dict[str, Any]], list[str]]:
    issues: list[str] = []
    normalized: list[dict[str, Any]] = []
    by_qid: dict[str, list[dict[str, Any]]] = {}

    for raw in rows:
        if not isinstance(raw, dict):
            issues.append("Ligne batch IA invalide (dict attendu).")
            continue
        qid = str(raw.get("question_id", "")).upper().strip()
        if not qid:
            issues.append("Ligne batch IA sans question_id.")
            continue
        row = dict(raw)
        row["question_id"] = qid
        by_qid.setdefault(qid, []).append(row)

    for qid, expected_hash in expected_by_qid.items():
        expected = str(expected_hash).strip()
        q_rows = by_qid.get(qid, [])
        if not q_rows:
            issues.append(f"Ligne manquante pour {qid}.")
            normalized.append(
                {
                    "question_id": qid,
                    "status": "FAILED_INCOMPLETE",
                    "bundle_hash": expected,
                    "tokens_input": 0,
                    "tokens_output": 0,
                    "error": "Resultat manquant dans le batch IA.",
                    "report_file": None,
                }
            )
            continue
        if len(q_rows) > 1:
            issues.append(f"Doublon de lignes pour {qid}.")
            normalized.append(
                {
                    "question_id": qid,
                    "status": "FAILED_DUPLICATE",
                    "bundle_hash": expected,
                    "tokens_input": 0,
                    "tokens_output": 0,
                    "error": "Doublon detecte pour cette question dans le batch IA.",
                    "report_file": None,
                }
            )
            continue

        row = q_rows[0]
        observed_hash = str(row.get("bundle_hash", "")).strip()
        if expected and observed_hash != expected:
            issues.append(f"bundle_hash incoherent pour {qid}.")
            normalized.append(
                {
                    "question_id": qid,
                    "status": "FAILED_MISMATCH",
                    "bundle_hash": observed_hash,
                    "tokens_input": 0,
                    "tokens_output": 0,
                    "error": f"bundle_hash incoherent (attendu={expected}, observe={observed_hash}).",
                    "report_file": None,
                }
            )
            continue
        normalized.append(row)

    for qid, q_rows in by_qid.items():
        if qid in expected_by_qid:
            continue
        for row in q_rows:
            normalized.append(row)

    order = {qid: idx for idx, qid in enumerate(QUESTION_ORDER)}
    normalized = sorted(
        normalized,
        key=lambda row: (order.get(str(row.get("question_id", "")).upper(), 99), str(row.get("question_id", ""))),
    )
    return normalized, issues
