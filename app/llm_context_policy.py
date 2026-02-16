from __future__ import annotations

import json
from collections import Counter
from typing import Any, Literal

import pandas as pd

ContextProfile = Literal["FULL", "COMPACT", "MINIMAL"]
PROFILE_ORDER: tuple[ContextProfile, ...] = ("FULL", "COMPACT", "MINIMAL")
PROFILE_SOFT_TOKEN_BUDGET: dict[ContextProfile, int] = {
    "FULL": 30000,
    "COMPACT": 22000,
    "MINIMAL": 14000,
}
HARD_CONTEXT_TOKEN_BUDGET = 18000

PROFILE_LIMITS: dict[ContextProfile, dict[str, int]] = {
    "FULL": {
        "hist_rows_per_table": 80,
        "scen_rows_per_table": 60,
        "test_rows": 180,
        "comparison_rows": 140,
        "checks_rows": 120,
    },
    "COMPACT": {
        "hist_rows_per_table": 35,
        "scen_rows_per_table": 25,
        "test_rows": 90,
        "comparison_rows": 80,
        "checks_rows": 70,
    },
    "MINIMAL": {
        "hist_rows_per_table": 15,
        "scen_rows_per_table": 10,
        "test_rows": 45,
        "comparison_rows": 40,
        "checks_rows": 40,
    },
}


def estimate_prompt_tokens_approx(instructions: str, input_items: list[dict[str, Any]]) -> int:
    payload = {
        "instructions": str(instructions or ""),
        "input": input_items if isinstance(input_items, list) else [],
    }
    txt = json.dumps(payload, ensure_ascii=False, default=str)
    # Approximation deterministic conservative.
    return max(1, int(len(txt) / 4))


def _normalize_rows(data: Any) -> tuple[list[dict[str, Any]], str]:
    if isinstance(data, dict) and isinstance(data.get("rows"), list):
        rows = [r for r in data.get("rows", []) if isinstance(r, dict)]
        note = str(data.get("note", "")).strip()
        return rows, note
    if isinstance(data, list):
        rows = [r for r in data if isinstance(r, dict)]
        return rows, ""
    return [], ""


def _status_rank(raw_status: Any) -> int:
    status = str(raw_status or "").upper().strip()
    if status == "FAIL":
        return 0
    if status == "WARN":
        return 1
    if status == "NON_TESTABLE":
        return 2
    if status == "PASS":
        return 3
    if status == "INFO":
        return 4
    return 5


def _priority_rows(rows: list[dict[str, Any]], *, row_limit: int, mode: str) -> list[dict[str, Any]]:
    if row_limit <= 0:
        return []
    if len(rows) <= row_limit:
        return rows

    indexed = list(enumerate(rows))
    if mode == "comparison":
        def _score(item: tuple[int, dict[str, Any]]) -> tuple[float, int]:
            idx, row = item
            delta = pd.to_numeric(pd.Series([row.get("delta")]), errors="coerce").iloc[0]
            delta_abs = float(abs(delta)) if pd.notna(delta) else 0.0
            status_bonus = 1.0 if str(row.get("interpretability_status", "")).upper().strip() == "INFORMATIVE" else 0.0
            return (delta_abs + status_bonus, -idx)

        ranked = sorted(indexed, key=_score, reverse=True)
    elif mode in {"checks", "ledger"}:
        ranked = sorted(indexed, key=lambda item: (_status_rank(item[1].get("status")), item[0]))
    else:
        ranked = indexed

    selected = sorted(ranked[:row_limit], key=lambda item: item[0])
    return [row for _, row in selected]


def _rank_table_name(name: str) -> tuple[int, str]:
    n = str(name or "").lower()
    if "summary" in n or "status" in n:
        return (0, n)
    if "comparison" in n or "panel" in n:
        return (1, n)
    if "quality" in n or "trace" in n:
        return (2, n)
    return (3, n)


def _check_counts(checks: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in checks:
        counts[str(row.get("status", "UNKNOWN")).upper().strip()] += 1
    out = {"PASS": 0, "WARN": 0, "FAIL": 0, "NON_TESTABLE": 0, "INFO": 0, "UNKNOWN": 0}
    for status, cnt in counts.items():
        if status in out:
            out[status] = int(cnt)
        else:
            out["UNKNOWN"] += int(cnt)
    return out


def _top_codes(checks: list[dict[str, Any]], status_filter: str, limit: int = 5) -> list[str]:
    wanted = str(status_filter).upper().strip()
    counts: Counter[str] = Counter()
    for row in checks:
        if str(row.get("status", "")).upper().strip() != wanted:
            continue
        code = str(row.get("code", "")).strip()
        if code:
            counts[code] += 1
    out: list[str] = []
    for code, count in sorted(counts.items(), key=lambda x: (-x[1], x[0]))[: int(limit)]:
        out.append(f"{code} (x{count})" if int(count) > 1 else code)
    return out


def compress_bundle_for_profile(
    bundle_data: dict[str, Any],
    profile: ContextProfile,
) -> tuple[dict[str, Any], list[str]]:
    prof = str(profile).upper().strip()
    if prof not in PROFILE_LIMITS:
        prof = "COMPACT"
    cfg = PROFILE_LIMITS[prof]  # type: ignore[index]
    notes: list[str] = [f"context_profile={prof}"]

    out: dict[str, Any] = {
        "question_id": bundle_data.get("question_id"),
        "run_id": bundle_data.get("run_id"),
        "business_question": bundle_data.get("business_question", ""),
        "definitions": bundle_data.get("definitions", []),
        "selection": bundle_data.get("selection", {}),
        "hist_kpis": bundle_data.get("hist_kpis", {}),
        "test_ledger_summary": bundle_data.get("test_ledger_summary", {}),
        "warnings": bundle_data.get("warnings", []),
    }

    # HIST tables
    hist_tables_in = bundle_data.get("hist_tables", {})
    hist_tables_out: dict[str, Any] = {}
    if isinstance(hist_tables_in, dict):
        for tname in sorted(hist_tables_in.keys(), key=_rank_table_name):
            rows, note = _normalize_rows(hist_tables_in.get(tname))
            kept = _priority_rows(rows, row_limit=int(cfg["hist_rows_per_table"]), mode="table")
            extra_note = f"rows_kept={len(kept)}/{len(rows)}"
            merged_note = " | ".join([x for x in [note, extra_note] if x])
            hist_tables_out[str(tname)] = {"rows": kept, "note": merged_note}
            if len(kept) < len(rows):
                notes.append(f"hist:{tname}:{len(kept)}/{len(rows)}")
    out["hist_tables"] = hist_tables_out

    # SCEN tables
    scen_tables_in = bundle_data.get("scen_tables", {})
    scen_tables_out: dict[str, dict[str, Any]] = {}
    if isinstance(scen_tables_in, dict):
        for sid in sorted(scen_tables_in.keys()):
            table_map = scen_tables_in.get(sid)
            if not isinstance(table_map, dict):
                continue
            scen_tables_out[str(sid)] = {}
            for tname in sorted(table_map.keys(), key=_rank_table_name):
                rows, note = _normalize_rows(table_map.get(tname))
                kept = _priority_rows(rows, row_limit=int(cfg["scen_rows_per_table"]), mode="table")
                extra_note = f"rows_kept={len(kept)}/{len(rows)}"
                merged_note = " | ".join([x for x in [note, extra_note] if x])
                scen_tables_out[str(sid)][str(tname)] = {"rows": kept, "note": merged_note}
                if len(kept) < len(rows):
                    notes.append(f"scen:{sid}:{tname}:{len(kept)}/{len(rows)}")
    out["scen_tables"] = scen_tables_out

    # Test ledger
    test_rows, test_note = _normalize_rows(bundle_data.get("test_ledger", []))
    kept_tests = _priority_rows(test_rows, row_limit=int(cfg["test_rows"]), mode="ledger")
    out["test_ledger"] = {"rows": kept_tests, "note": f"{test_note} | rows_kept={len(kept_tests)}/{len(test_rows)}".strip(" |")}
    if len(kept_tests) < len(test_rows):
        notes.append(f"test_ledger:{len(kept_tests)}/{len(test_rows)}")

    # Comparison
    comp_rows, comp_note = _normalize_rows(bundle_data.get("comparison_hist_vs_scen", []))
    kept_comp = _priority_rows(comp_rows, row_limit=int(cfg["comparison_rows"]), mode="comparison")
    out["comparison_hist_vs_scen"] = {"rows": kept_comp, "note": f"{comp_note} | rows_kept={len(kept_comp)}/{len(comp_rows)}".strip(" |")}
    if len(kept_comp) < len(comp_rows):
        notes.append(f"comparison:{len(kept_comp)}/{len(comp_rows)}")

    # Checks + summaries
    checks_rows, checks_note = _normalize_rows(bundle_data.get("checks", []))
    kept_checks = _priority_rows(checks_rows, row_limit=int(cfg["checks_rows"]), mode="checks")
    out["checks"] = {"rows": kept_checks, "note": f"{checks_note} | rows_kept={len(kept_checks)}/{len(checks_rows)}".strip(" |")}
    out["check_counts"] = _check_counts(checks_rows)
    out["top_fail_codes"] = _top_codes(checks_rows, "FAIL")
    out["top_warn_codes"] = _top_codes(checks_rows, "WARN")
    if len(kept_checks) < len(checks_rows):
        notes.append(f"checks:{len(kept_checks)}/{len(checks_rows)}")

    hard_budget = int(HARD_CONTEXT_TOKEN_BUDGET)
    estimated = estimate_prompt_tokens_approx("", [{"role": "user", "content": json.dumps(out, ensure_ascii=False, default=str)}])
    if estimated > hard_budget:
        hist_tables_trimmed = {}
        for tname, table in list(out.get("hist_tables", {}).items())[:2]:
            rows, note = _normalize_rows(table)
            hist_tables_trimmed[str(tname)] = {"rows": rows[:10], "note": str(note)}
        out["hist_tables"] = hist_tables_trimmed

        scen_trimmed: dict[str, dict[str, Any]] = {}
        for sid, table_map in list(out.get("scen_tables", {}).items())[:2]:
            if not isinstance(table_map, dict):
                continue
            scen_trimmed[str(sid)] = {}
            for tname, table in list(table_map.items())[:2]:
                rows, note = _normalize_rows(table)
                scen_trimmed[str(sid)][str(tname)] = {"rows": rows[:8], "note": str(note)}
        out["scen_tables"] = scen_trimmed

        test_rows, test_note = _normalize_rows(out.get("test_ledger", []))
        out["test_ledger"] = {"rows": test_rows[:30], "note": str(test_note)}
        comp_rows, comp_note = _normalize_rows(out.get("comparison_hist_vs_scen", []))
        out["comparison_hist_vs_scen"] = {"rows": comp_rows[:25], "note": str(comp_note)}
        checks_rows2, checks_note = _normalize_rows(out.get("checks", []))
        out["checks"] = {"rows": checks_rows2[:25], "note": str(checks_note)}
        notes.append(f"hard_cap_applied:{estimated}->{hard_budget}")

    return out, notes


def select_initial_profile(bundle_data: dict[str, Any]) -> ContextProfile:
    estimated = estimate_prompt_tokens_approx(
        instructions="",
        input_items=[{"role": "user", "content": json.dumps(bundle_data, ensure_ascii=False, default=str)}],
    )
    # Budget heuristique (approx) pour gpt-5.2-pro en pratique.
    if estimated >= 40_000:
        return "MINIMAL"
    if estimated >= 24_000:
        return "COMPACT"
    return "FULL"


def is_context_overflow_error(exc: Exception | str) -> bool:
    msg = str(exc or "").lower()
    patterns = [
        "context length",
        "context_length_exceeded",
        "maximum context length",
        "too many tokens",
        "input is too long",
        "request too large",
        "token limit",
    ]
    return any(p in msg for p in patterns)


def soft_budget_for_profile(profile: ContextProfile | str) -> int:
    prof = str(profile).upper().strip()
    if prof in PROFILE_SOFT_TOKEN_BUDGET:
        return int(PROFILE_SOFT_TOKEN_BUDGET[prof])  # type: ignore[index]
    return int(PROFILE_SOFT_TOKEN_BUDGET["COMPACT"])
