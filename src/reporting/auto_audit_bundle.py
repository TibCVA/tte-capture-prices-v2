from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
from typing import Any

import pandas as pd

from src.reporting.evidence_loader import (
    REQUIRED_QUESTIONS,
    build_checks_catalog,
    build_evidence_catalog,
    build_test_traceability,
    load_combined_run,
    validate_combined_run,
)


DEFAULT_AUDIT_ROOT = Path("outputs/audit_runs")
DEFAULT_COMBINED_BASE = Path("outputs/combined")
DEFAULT_LLM_REPORTS_DIR = Path("outputs/llm_reports")
DEFAULT_COUNTRY_SCOPE = ["ES", "DE"]


def _status_from_check_counts(check_counts: dict[str, int]) -> str:
    if int(check_counts.get("FAIL", 0)) > 0:
        return "FAIL"
    if int(check_counts.get("WARN", 0)) > 0:
        return "WARN"
    return "PASS"


def _status_count(series: pd.Series | object) -> dict[str, int]:
    out: dict[str, int] = {"PASS": 0, "WARN": 0, "FAIL": 0, "NON_TESTABLE": 0, "INFO": 0, "UNKNOWN": 0}
    if not isinstance(series, pd.Series):
        return out
    counts = series.astype(str).str.upper().value_counts(dropna=False).to_dict()
    for key, value in counts.items():
        if key in out:
            out[key] = int(value)
        else:
            out["UNKNOWN"] += int(value)
    return out


def _top_fail_codes(checks_df: pd.DataFrame, limit: int = 5) -> list[str]:
    if checks_df.empty:
        return []
    fail_rows = checks_df[checks_df.get("status", pd.Series(dtype=object)).astype(str).str.upper() == "FAIL"].copy()
    if fail_rows.empty:
        return []
    code_col = "code" if "code" in fail_rows.columns else ("check_code" if "check_code" in fail_rows.columns else None)
    if not code_col:
        return []
    counts = Counter([str(x).strip() for x in fail_rows[code_col].tolist() if str(x).strip()])
    out: list[str] = []
    for code, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[: int(limit)]:
        out.append(f"{code} (x{count})" if int(count) > 1 else code)
    return out


def _build_question_status_summary(
    run_id: str,
    blocks: dict[str, Any],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for qid in REQUIRED_QUESTIONS:
        block = blocks.get(qid)
        if block is None:
            rows.append(
                {
                    "run_id": run_id,
                    "question_id": qid,
                    "tests_PASS": 0,
                    "tests_WARN": 0,
                    "tests_FAIL": 0,
                    "tests_NON_TESTABLE": 0,
                    "tests_UNKNOWN": 0,
                    "checks_PASS": 0,
                    "checks_WARN": 0,
                    "checks_FAIL": 0,
                    "checks_NON_TESTABLE": 0,
                    "checks_INFO": 0,
                    "checks_UNKNOWN": 0,
                    "quality_status": "MISSING",
                    "top_fail_codes": "",
                }
            )
            continue

        test_counts = _status_count(block.ledger.get("status", pd.Series(dtype=object)))
        check_counts = _status_count(block.checks.get("status", pd.Series(dtype=object)))
        rows.append(
            {
                "run_id": run_id,
                "question_id": qid,
                "tests_PASS": int(test_counts.get("PASS", 0)),
                "tests_WARN": int(test_counts.get("WARN", 0)),
                "tests_FAIL": int(test_counts.get("FAIL", 0)),
                "tests_NON_TESTABLE": int(test_counts.get("NON_TESTABLE", 0)),
                "tests_UNKNOWN": int(test_counts.get("UNKNOWN", 0)),
                "checks_PASS": int(check_counts.get("PASS", 0)),
                "checks_WARN": int(check_counts.get("WARN", 0)),
                "checks_FAIL": int(check_counts.get("FAIL", 0)),
                "checks_NON_TESTABLE": int(check_counts.get("NON_TESTABLE", 0)),
                "checks_INFO": int(check_counts.get("INFO", 0)),
                "checks_UNKNOWN": int(check_counts.get("UNKNOWN", 0)),
                "quality_status": _status_from_check_counts(check_counts),
                "top_fail_codes": " | ".join(_top_fail_codes(block.checks)),
            }
        )

    return pd.DataFrame(rows)


_COUNTRY_YEAR_IN_MESSAGE_RE = re.compile(r"\b([A-Z_]{2,})-(\d{4})\b")


def _country_from_check_message(value: Any) -> str:
    txt = str(value or "")
    m = _COUNTRY_YEAR_IN_MESSAGE_RE.search(txt)
    if not m:
        return ""
    return str(m.group(1)).upper().strip()


def _build_question_status_summary_scope(
    run_id: str,
    global_status: pd.DataFrame,
    checks_catalog: pd.DataFrame,
    scope_countries: list[str],
) -> pd.DataFrame:
    scope_set = {str(c).upper().strip() for c in scope_countries if str(c).strip()}
    if not scope_set:
        scope_set = {"DE", "ES"}

    out = global_status.copy()
    for col in [
        "checks_PASS",
        "checks_WARN",
        "checks_FAIL",
        "checks_NON_TESTABLE",
        "checks_INFO",
        "checks_UNKNOWN",
        "quality_status",
        "top_fail_codes",
    ]:
        if col not in out.columns:
            out[col] = 0 if col.startswith("checks_") else ""

    checks = checks_catalog.copy()
    if checks.empty:
        out["quality_status"] = "MISSING_SCOPE"
        out["top_fail_codes"] = ""
        return out

    if "scope" not in checks.columns:
        checks["scope"] = ""
    if "message" not in checks.columns:
        checks["message"] = ""
    if "country" in checks.columns:
        checks["country_scope"] = checks["country"].astype(str).str.upper().str.strip()
    else:
        checks["country_scope"] = checks["message"].map(_country_from_check_message)
    checks["is_bundle_scope"] = checks["scope"].astype(str).str.upper().eq("BUNDLE")
    checks["in_scope"] = checks["country_scope"].astype(str).isin(scope_set)

    for qid in REQUIRED_QUESTIONS:
        q_mask = checks["question_id"].astype(str).str.upper().eq(str(qid).upper())
        q_checks_all = checks[q_mask].copy()
        q_checks = q_checks_all[q_checks_all["is_bundle_scope"] | q_checks_all["in_scope"]].copy()
        check_counts = _status_count(q_checks.get("status", pd.Series(dtype=object)))
        fail_codes = _top_fail_codes(q_checks, limit=5)
        row_mask = out["question_id"].astype(str).str.upper().eq(str(qid).upper())
        if not bool(row_mask.any()):
            continue
        out.loc[row_mask, "checks_PASS"] = int(check_counts.get("PASS", 0))
        out.loc[row_mask, "checks_WARN"] = int(check_counts.get("WARN", 0))
        out.loc[row_mask, "checks_FAIL"] = int(check_counts.get("FAIL", 0))
        out.loc[row_mask, "checks_NON_TESTABLE"] = int(check_counts.get("NON_TESTABLE", 0))
        out.loc[row_mask, "checks_INFO"] = int(check_counts.get("INFO", 0))
        out.loc[row_mask, "checks_UNKNOWN"] = int(check_counts.get("UNKNOWN", 0))
        out.loc[row_mask, "quality_status"] = _status_from_check_counts(check_counts)
        out.loc[row_mask, "top_fail_codes"] = " | ".join(fail_codes)

    return out


def _critical_fail_codes_from_status(status_df: pd.DataFrame, limit: int = 12) -> list[str]:
    if status_df is None or status_df.empty:
        return []
    out: list[str] = []
    seen: set[str] = set()
    for _, row in status_df.iterrows():
        quality_status = str(row.get("quality_status", "")).upper().strip()
        if quality_status != "FAIL":
            continue
        raw_codes = str(row.get("top_fail_codes", "")).strip()
        if not raw_codes:
            continue
        parts = [str(x).strip() for x in raw_codes.split("|")]
        for part in parts:
            if not part:
                continue
            if part in seen:
                continue
            seen.add(part)
            out.append(part)
            if len(out) >= int(limit):
                return out
    return out


def _build_question_fail_matrix(run_id: str, checks_catalog: pd.DataFrame) -> pd.DataFrame:
    if checks_catalog.empty:
        return pd.DataFrame(
            columns=[
                "run_id",
                "question_id",
                "code",
                "scope",
                "scenario_id",
                "frequency",
                "message_sample",
            ]
        )

    required_cols = {"question_id", "status", "code", "scope", "scenario_id", "message"}
    for col in required_cols:
        if col not in checks_catalog.columns:
            checks_catalog[col] = ""

    fail_rows = checks_catalog[checks_catalog["status"].astype(str).str.upper() == "FAIL"].copy()
    if fail_rows.empty:
        return pd.DataFrame(
            columns=[
                "run_id",
                "question_id",
                "code",
                "scope",
                "scenario_id",
                "frequency",
                "message_sample",
            ]
        )

    grouped = (
        fail_rows.groupby(["question_id", "code", "scope", "scenario_id"], dropna=False)
        .agg(
            frequency=("code", "count"),
            message_sample=("message", "first"),
        )
        .reset_index()
    )
    grouped.insert(0, "run_id", run_id)
    grouped = grouped.sort_values(["question_id", "frequency", "code"], ascending=[True, False, True]).reset_index(drop=True)
    return grouped


def _fallback_detailed_markdown(run_id: str, countries: list[str], blocks: dict[str, Any], output_md: Path) -> None:
    lines: list[str] = []
    lines.append(f"# Detailed auto audit - {run_id}")
    lines.append("")
    lines.append(f"Country scope: {', '.join(countries)}")
    lines.append("")
    for qid in REQUIRED_QUESTIONS:
        block = blocks.get(qid)
        lines.append(f"## {qid}")
        if block is None:
            lines.append("Missing question block.")
            lines.append("")
            continue
        test_counts = _status_count(block.ledger.get("status", pd.Series(dtype=object)))
        check_counts = _status_count(block.checks.get("status", pd.Series(dtype=object)))
        lines.append(
            "Tests: "
            + f"PASS={int(test_counts.get('PASS', 0))}, "
            + f"WARN={int(test_counts.get('WARN', 0))}, "
            + f"FAIL={int(test_counts.get('FAIL', 0))}, "
            + f"NON_TESTABLE={int(test_counts.get('NON_TESTABLE', 0))}"
        )
        lines.append(
            "Checks: "
            + f"PASS={int(check_counts.get('PASS', 0))}, "
            + f"WARN={int(check_counts.get('WARN', 0))}, "
            + f"FAIL={int(check_counts.get('FAIL', 0))}, "
            + f"INFO={int(check_counts.get('INFO', 0))}"
        )
        fail_codes = _top_fail_codes(block.checks)
        if fail_codes:
            lines.append("Top FAIL codes: " + ", ".join(fail_codes))
        lines.append("")
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text("\n".join(lines), encoding="utf-8")


def _generate_detailed_markdown_es_de(
    run_id: str,
    *,
    countries: list[str],
    blocks: dict[str, Any],
    output_md: Path,
    warnings: list[str],
) -> None:
    try:
        from scripts.generate_extrait_data_outil_v7 import generate_extrait

        _ = generate_extrait(
            run_id=run_id,
            countries=countries,
            output_docx=output_md.with_suffix(".docx"),
            output_md=output_md,
            generate_docx=False,
        )
    except Exception as exc:
        warnings.append(f"Detailed markdown fallback active: {exc}")
        _fallback_detailed_markdown(run_id, countries, blocks, output_md)


def _copy_llm_reports(
    run_id: str,
    *,
    include_llm_reports: bool,
    bundle_hash_by_question: dict[str, str] | None,
    out_dir: Path,
) -> dict[str, Any]:
    copied: list[str] = []
    missing: list[str] = []

    if not include_llm_reports:
        return {"copied": copied, "missing": missing}
    if not isinstance(bundle_hash_by_question, dict) or not bundle_hash_by_question:
        return {"copied": copied, "missing": missing}

    llm_src = DEFAULT_LLM_REPORTS_DIR
    if not llm_src.exists():
        missing.append(f"llm_reports_dir_missing:{llm_src}")
        return {"copied": copied, "missing": missing}

    llm_dst = out_dir / "llm_reports"
    llm_dst.mkdir(parents=True, exist_ok=True)
    for qid in REQUIRED_QUESTIONS:
        bundle_hash = str(bundle_hash_by_question.get(qid, "")).strip()
        if not bundle_hash:
            continue
        src = llm_src / f"{qid}_{bundle_hash}.json"
        if src.exists():
            dst = llm_dst / src.name
            shutil.copy2(src, dst)
            copied.append(str(dst))
        else:
            missing.append(str(src))
    return {"copied": copied, "missing": missing}


def _apply_retention(audit_root_dir: Path, keep_last: int, protected_run_id: str) -> list[str]:
    if keep_last <= 0:
        return []
    if not audit_root_dir.exists():
        return []
    dirs = [p for p in audit_root_dir.iterdir() if p.is_dir()]
    dirs = sorted(dirs, key=lambda p: p.stat().st_mtime, reverse=True)
    removed: list[str] = []
    for idx, old_dir in enumerate(dirs):
        if idx < keep_last:
            continue
        if old_dir.name == protected_run_id:
            continue
        shutil.rmtree(old_dir, ignore_errors=True)
        removed.append(str(old_dir))
    return removed


def build_auto_audit_bundle(
    run_id: str,
    *,
    countries: list[str] | None = None,
    include_llm_reports: bool = True,
    bundle_hash_by_question: dict[str, str] | None = None,
    keep_last: int = 5,
    combined_base_dir: Path = DEFAULT_COMBINED_BASE,
    audit_root_dir: Path = DEFAULT_AUDIT_ROOT,
) -> dict[str, Any]:
    run_id_clean = str(run_id).strip()
    if not run_id_clean:
        raise ValueError("run_id vide.")

    run_dir = Path(combined_base_dir) / run_id_clean
    valid, issues = validate_combined_run(run_dir)
    if not valid:
        raise ValueError("Run combine invalide: " + " | ".join(issues))

    _, _, blocks = load_combined_run(run_id=run_id_clean, base_dir=Path(combined_base_dir), strict=True)

    audit_dir = Path(audit_root_dir) / run_id_clean
    reports_dir = audit_dir / "reports"
    snapshot_dir = audit_dir / "combined_run"
    warnings: list[str] = []

    if audit_dir.exists():
        shutil.rmtree(audit_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    shutil.copytree(run_dir, snapshot_dir)

    evidence_catalog = build_evidence_catalog(run_dir, blocks)
    traceability = build_test_traceability(run_dir, blocks)
    checks_catalog = build_checks_catalog(run_dir, blocks)
    q_status = _build_question_status_summary(run_id_clean, blocks)
    q_status_scope = _build_question_status_summary_scope(
        run_id_clean,
        q_status,
        checks_catalog,
        scope_countries=["DE", "ES"],
    )
    critical_fail_codes_global = _critical_fail_codes_from_status(q_status)
    critical_fail_codes_scope_de_es = _critical_fail_codes_from_status(q_status_scope)
    fail_matrix = _build_question_fail_matrix(run_id_clean, checks_catalog)

    evidence_path = reports_dir / f"evidence_catalog_{run_id_clean}.csv"
    traceability_path = reports_dir / f"test_traceability_{run_id_clean}.csv"
    checks_path = reports_dir / f"checks_catalog_{run_id_clean}.csv"
    status_path = reports_dir / f"question_status_summary_{run_id_clean}.csv"
    status_global_path = reports_dir / f"question_status_summary_global_{run_id_clean}.csv"
    status_scope_path = reports_dir / f"question_status_summary_scope_DE_ES_{run_id_clean}.csv"
    fail_matrix_path = reports_dir / f"question_fail_matrix_{run_id_clean}.csv"
    detailed_md_path = reports_dir / f"detailed_es_de_{run_id_clean}.md"

    evidence_catalog.to_csv(evidence_path, index=False)
    traceability.to_csv(traceability_path, index=False)
    checks_catalog.to_csv(checks_path, index=False)
    q_status.to_csv(status_path, index=False)
    q_status.to_csv(status_global_path, index=False)
    q_status_scope.to_csv(status_scope_path, index=False)
    fail_matrix.to_csv(fail_matrix_path, index=False)

    country_scope = [str(c).upper().strip() for c in (countries or DEFAULT_COUNTRY_SCOPE) if str(c).strip()]
    if set(country_scope) != {"ES", "DE"}:
        warnings.append("Country scope forced to strict ES+DE for detailed markdown.")
    country_scope = ["ES", "DE"]
    _generate_detailed_markdown_es_de(
        run_id_clean,
        countries=country_scope,
        blocks=blocks,
        output_md=detailed_md_path,
        warnings=warnings,
    )

    llm_info = _copy_llm_reports(
        run_id_clean,
        include_llm_reports=include_llm_reports,
        bundle_hash_by_question=bundle_hash_by_question,
        out_dir=audit_dir,
    )

    removed_dirs = _apply_retention(Path(audit_root_dir), int(keep_last), run_id_clean)

    manifest = {
        "run_id": run_id_clean,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "country_scope": country_scope,
        "audit_dir": str(audit_dir),
        "snapshot_dir": str(snapshot_dir),
        "reports": {
            "evidence_catalog": str(evidence_path),
            "test_traceability": str(traceability_path),
            "checks_catalog": str(checks_path),
            "question_status_summary": str(status_path),
            "question_status_summary_global": str(status_global_path),
            "question_status_summary_scope_de_es": str(status_scope_path),
            "question_fail_matrix": str(fail_matrix_path),
            "detailed_markdown": str(detailed_md_path),
        },
        "llm_reports": llm_info,
        "critical_fail_codes_global": critical_fail_codes_global,
        "critical_fail_codes_scope_de_es": critical_fail_codes_scope_de_es,
        "retention_removed": removed_dirs,
        "warnings": warnings,
    }
    manifest_path = audit_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "run_id": run_id_clean,
        "audit_dir": str(audit_dir),
        "manifest_path": str(manifest_path),
        "detailed_markdown_path": str(detailed_md_path),
        "question_status_summary_path": str(status_path),
        "question_status_summary_global_path": str(status_global_path),
        "question_status_summary_scope_path": str(status_scope_path),
        "critical_fail_codes_global": critical_fail_codes_global,
        "critical_fail_codes_scope_de_es": critical_fail_codes_scope_de_es,
        "warnings": warnings,
        "llm_reports_copied": llm_info.get("copied", []),
        "llm_reports_missing": llm_info.get("missing", []),
        "retention_removed": removed_dirs,
    }
