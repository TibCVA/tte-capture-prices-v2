"""Load and normalize reporting evidence from combined runs."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
import shutil

import pandas as pd

from src.hash_utils import hash_object
from src.reporting.report_schema import QuestionTestResultBlock
from src.modules.bundle_result import QuestionBundleResult
from src.modules.result import ModuleResult

REQUIRED_QUESTIONS: tuple[str, ...] = ("Q1", "Q2", "Q3", "Q4", "Q5")


def _safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def _safe_read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _safe_read_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _parse_json_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Fichier JSON manquant: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"Fichier JSON invalide: {path} ({exc})") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"Fichier JSON invalide (objet attendue): {path}")
    return payload


def _parse_csv_file(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Fichier CSV manquant: {path}")
    try:
        return pd.read_csv(path)
    except Exception as exc:
        raise ValueError(f"Fichier CSV invalide: {path} ({exc})") from exc


def _load_module_result_from_export(
    module_dir: Path,
    *,
    default_mode: str,
    default_run_id: str,
    default_selection: dict[str, Any],
    default_module_id: str,
    scenario_id: str | None = None,
) -> ModuleResult:
    summary = _parse_json_file(module_dir / "summary.json")
    checks = summary.get("checks")
    if not isinstance(checks, list):
        raise ValueError(f"summary.json invalide: checks doit être une liste dans {module_dir / 'summary.json'}")
    warnings = summary.get("warnings", [])
    if not isinstance(warnings, list):
        warnings = []
    kpis = summary.get("kpis", {})
    if not isinstance(kpis, dict):
        raise ValueError(f"summary.json invalide: kpis doit être un dict dans {module_dir / 'summary.json'}")

    selection = summary.get("selection", default_selection)
    if not isinstance(selection, dict):
        raise ValueError(f"summary.json invalide: selection doit être un dict dans {module_dir / 'summary.json'}")

    horizon_year_raw = summary.get("horizon_year", None)
    try:
        horizon_year = int(horizon_year_raw) if horizon_year_raw is not None else None
    except Exception:
        horizon_year = None

    scenario = summary.get("scenario_id", scenario_id)
    if scenario is not None:
        scenario = str(scenario)

    return ModuleResult(
        module_id=str(summary.get("module_id", default_module_id)),
        run_id=str(summary.get("run_id", default_run_id)),
        selection=selection,
        assumptions_used=summary.get("assumptions_used", []),
        kpis=kpis,
        tables=_load_tables_dir(module_dir / "tables"),
        figures=[],
        narrative_md=_safe_read_text(module_dir / "narrative.md"),
        checks=checks,
        warnings=[str(w) for w in warnings],
        mode=str(summary.get("mode", default_mode)).upper(),
        scenario_id=scenario,
        horizon_year=horizon_year,
    )


def _load_tables_dir(tables_dir: Path) -> dict[str, pd.DataFrame]:
    out: dict[str, pd.DataFrame] = {}
    if not tables_dir.exists():
        return out
    for csv_path in sorted(tables_dir.glob("*.csv")):
        out[csv_path.stem] = _parse_csv_file(csv_path)
    return out


def compute_question_bundle_signature(run_dir: Path, question_id: str) -> str:
    qid = str(question_id).upper()
    payload = {
        "run_id": run_dir.name,
        "question_id": qid,
        "run_dir_mtime_ns": int(run_dir.stat().st_mtime_ns),
    }
    return hash_object(payload)


def question_dir(run_dir: Path, question_id: str) -> Path:
    return run_dir / str(question_id).upper()


def validate_combined_run(run_dir: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not run_dir.exists():
        return False, [f"Run introuvable: {run_dir}"]
    if not run_dir.is_dir():
        return False, [f"Run invalide (pas un dossier): {run_dir}"]

    for q in REQUIRED_QUESTIONS:
        q_dir = question_dir(run_dir, q)
        if not q_dir.exists():
            errors.append(f"Question manquante: {q}")
            continue
        if not q_dir.is_dir():
            errors.append(f"Question non valide (pas un dossier): {q_dir}")
            continue

        summary_path = q_dir / "summary.json"
        ledger_path = q_dir / "test_ledger.csv"
        comparison_path = q_dir / "comparison_hist_vs_scen.csv"
        hist_dir = q_dir / "hist"
        scen_dir = q_dir / "scen"

        if not summary_path.exists():
            errors.append(f"summary.json manquant pour {q}: {summary_path}")
        else:
            try:
                summary = _parse_json_file(summary_path)
            except Exception as exc:
                errors.append(str(exc))
            else:
                if not summary.get("run_id"):
                    errors.append(f"summary.json incomplet pour {q}: run_id manquant.")
                if not isinstance(summary.get("checks", []), list):
                    errors.append(f"summary.json invalide pour {q}: checks doit être une liste.")

        try:
            _ = _parse_csv_file(ledger_path)
        except Exception as exc:
            errors.append(str(exc))

        try:
            _ = _parse_csv_file(comparison_path)
        except Exception as exc:
            errors.append(str(exc))

        if not hist_dir.exists() or not hist_dir.is_dir():
            errors.append(f"Repertoire hist manquant pour {q}: {hist_dir}")
        else:
            try:
                _ = _parse_json_file(hist_dir / "summary.json")
            except Exception as exc:
                # not obligatoire selon certaines executions, mais nécessaire pour un preload robuste
                errors.append(str(exc))

        if not scen_dir.exists() or not scen_dir.is_dir():
            errors.append(f"Repertoire scen manquant pour {q}: {scen_dir}")
        else:
            for scenario_dir in sorted([p for p in scen_dir.iterdir() if p.is_dir()]):
                try:
                    _ = _parse_json_file(scenario_dir / "summary.json")
                except Exception as exc:
                    errors.append(str(exc))

    return len(errors) == 0, errors


def load_question_bundle_from_combined_run_verified(
    run_id: str,
    question_id: str,
    base_dir: str | Path = "outputs/combined",
) -> tuple[QuestionBundleResult, Path]:
    if not str(run_id).strip():
        raise ValueError("run_id vide.")
    run_dir = _to_abs_project_path(base_dir, run_id)
    qid = str(question_id).upper()
    if qid not in REQUIRED_QUESTIONS:
        raise ValueError(f"question_id invalide: {question_id}")

    q_dir = question_dir(run_dir, qid)
    valid, errors = validate_combined_run(run_dir)
    if not valid:
        raise ValueError(f"Run combine incomplet ou invalide: {run_id} | " + " | ".join(errors))
    if not q_dir.exists():
        raise FileNotFoundError(f"Bundle introuvable: {q_dir}")

    bundle_summary = _parse_json_file(q_dir / "summary.json")
    default_selection = bundle_summary.get("selection", {})
    if not isinstance(default_selection, dict):
        raise ValueError(f"summary.json invalide: selection doit être un dict dans {q_dir / 'summary.json'}")

    hist_dir = q_dir / "hist"
    hist_result = _load_module_result_from_export(
        hist_dir,
        default_mode="HIST",
        default_run_id=str(bundle_summary.get("run_id", run_id)),
        default_selection=default_selection,
        default_module_id=qid,
        scenario_id=None,
    )

    scen_results: dict[str, ModuleResult] = {}
    scen_root = q_dir / "scen"
    for scen_dir in sorted([p for p in scen_root.iterdir() if p.is_dir()]):
        scen_id = str(scen_dir.name)
        scen_results[scen_id] = _load_module_result_from_export(
            scen_dir,
            default_mode="SCEN",
            default_run_id=str(bundle_summary.get("run_id", run_id)),
            default_selection=default_selection,
            default_module_id=qid,
            scenario_id=scen_id,
        )

    checks = bundle_summary.get("checks", [])
    if not isinstance(checks, list):
        raise ValueError(f"summary.json invalide: checks doit être une liste dans {q_dir / 'summary.json'}")
    warnings = bundle_summary.get("warnings", [])
    if not isinstance(warnings, list):
        warnings = []

    bundle = QuestionBundleResult(
        question_id=qid,
        run_id=str(bundle_summary.get("run_id", run_id)),
        selection=default_selection,
        hist_result=hist_result,
        scen_results=scen_results,
        test_ledger=_parse_csv_file(q_dir / "test_ledger.csv"),
        comparison_table=_parse_csv_file(q_dir / "comparison_hist_vs_scen.csv"),
        checks=checks,
        warnings=[str(w) for w in warnings],
        narrative_md=_safe_read_text(q_dir / "narrative.md"),
    )
    return bundle, q_dir


def _to_abs_project_path(base_dir: str | Path, run_id: str | Path | None = None) -> Path:
    project_root = Path(__file__).resolve().parents[2]
    base_path = Path(base_dir)
    abs_base = base_path if base_path.is_absolute() else project_root / base_path
    if run_id is None:
        return abs_base
    return abs_base / str(run_id)


def is_complete_run(run_dir: Path) -> bool:
    if not run_dir.exists() or not run_dir.is_dir():
        return False
    for q in REQUIRED_QUESTIONS:
        q_dir = question_dir(run_dir, q)
        if not q_dir.exists():
            return False
        if not (q_dir / "summary.json").exists():
            return False
        if not (q_dir / "test_ledger.csv").exists():
            return False
        if not (q_dir / "comparison_hist_vs_scen.csv").exists():
            return False
    return True


def discover_complete_runs(base_dir: Path = Path("outputs/combined")) -> list[Path]:
    if not base_dir.exists():
        return []
    runs = [p for p in base_dir.iterdir() if p.is_dir() and is_complete_run(p)]
    return sorted(runs, key=lambda p: p.stat().st_mtime, reverse=True)


def discover_question_fragments(base_dir: Path = Path("outputs/combined")) -> dict[str, list[Path]]:
    fragments: dict[str, list[Path]] = {q: [] for q in REQUIRED_QUESTIONS}
    if not base_dir.exists():
        return fragments
    for run_dir in base_dir.iterdir():
        if not run_dir.is_dir():
            continue
        for q in REQUIRED_QUESTIONS:
            q_dir = question_dir(run_dir, q)
            if not q_dir.exists():
                continue
            if (q_dir / "summary.json").exists() and (q_dir / "test_ledger.csv").exists() and (q_dir / "comparison_hist_vs_scen.csv").exists():
                fragments[q].append(q_dir)
    for q in REQUIRED_QUESTIONS:
        fragments[q] = sorted(fragments[q], key=lambda p: p.stat().st_mtime, reverse=True)
    return fragments


def latest_fragment_per_question(base_dir: Path = Path("outputs/combined")) -> dict[str, Path]:
    frags = discover_question_fragments(base_dir=base_dir)
    out: dict[str, Path] = {}
    for q, items in frags.items():
        if items:
            out[q] = items[0]
    return out


def can_assemble_complete_run(base_dir: Path = Path("outputs/combined")) -> bool:
    latest = latest_fragment_per_question(base_dir=base_dir)
    return all(q in latest for q in REQUIRED_QUESTIONS)


def assemble_complete_run_from_fragments(
    base_dir: Path = Path("outputs/combined"),
    run_id: str | None = None,
    overwrite: bool = False,
) -> Path:
    latest = latest_fragment_per_question(base_dir=base_dir)
    missing = [q for q in REQUIRED_QUESTIONS if q not in latest]
    if missing:
        raise ValueError(f"Cannot assemble complete run, missing fragments for: {missing}")

    if run_id is None:
        run_id = "ASSEMBLED_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = base_dir / run_id
    if run_dir.exists():
        if overwrite:
            shutil.rmtree(run_dir)
        else:
            raise FileExistsError(f"Run dir already exists: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=True)

    provenance: dict[str, str] = {}
    for q in REQUIRED_QUESTIONS:
        src_q_dir = latest[q]
        dst_q_dir = run_dir / q
        shutil.copytree(src_q_dir, dst_q_dir)
        provenance[q] = str(src_q_dir)

    meta = {
        "assembled_run_id": run_id,
        "assembled_at_utc": datetime.now(timezone.utc).isoformat(),
        "provenance": provenance,
    }
    (run_dir / "_assembled_from.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return run_dir


def resolve_run_dir(
    run_id: str | None = None,
    base_dir: Path = Path("outputs/combined"),
    strict: bool = True,
) -> Path:
    if run_id:
        run_dir = base_dir / run_id
        if not run_dir.exists():
            raise FileNotFoundError(f"Combined run not found: {run_dir}")
        if strict and not is_complete_run(run_dir):
            raise ValueError(f"Combined run is incomplete (Q1..Q5 required): {run_dir}")
        return run_dir

    candidates = discover_complete_runs(base_dir=base_dir)
    if candidates:
        return candidates[0]
    if strict:
        raise ValueError("No complete combined run found (requires Q1..Q5).")

    runs = [p for p in base_dir.iterdir() if p.is_dir()] if base_dir.exists() else []
    if not runs:
        raise ValueError("No combined run found.")
    return sorted(runs, key=lambda p: p.stat().st_mtime, reverse=True)[0]


def load_question_block(run_dir: Path, question_id: str) -> QuestionTestResultBlock:
    qid = str(question_id).upper()
    q_dir = question_dir(run_dir, qid)
    summary_path = q_dir / "summary.json"
    ledger_path = q_dir / "test_ledger.csv"
    comparison_path = q_dir / "comparison_hist_vs_scen.csv"
    summary = _safe_read_json(summary_path)
    ledger = _safe_read_csv(ledger_path)
    comparison = _safe_read_csv(comparison_path)

    checks = pd.DataFrame(summary.get("checks", []))
    warnings = [str(w) for w in summary.get("warnings", [])]

    return QuestionTestResultBlock(
        question_id=qid,
        summary=summary,
        ledger=ledger,
        comparison=comparison,
        checks=checks,
        warnings=warnings,
        files={
            "summary": summary_path,
            "ledger": ledger_path,
            "comparison": comparison_path,
            "narrative": q_dir / "narrative.md",
        },
    )


def load_combined_run(
    run_id: str | None = None,
    base_dir: Path = Path("outputs/combined"),
    strict: bool = True,
) -> tuple[str, Path, dict[str, QuestionTestResultBlock]]:
    run_dir = resolve_run_dir(run_id=run_id, base_dir=base_dir, strict=strict)
    resolved_run_id = run_dir.name

    blocks: dict[str, QuestionTestResultBlock] = {}
    questions = REQUIRED_QUESTIONS if strict else tuple(sorted([p.name for p in run_dir.iterdir() if p.is_dir()]))
    for qid in questions:
        q_dir = question_dir(run_dir, qid)
        if not q_dir.exists():
            if strict:
                raise ValueError(f"Missing question directory: {qid} in {run_dir}")
            continue
        blocks[qid] = load_question_block(run_dir, qid)

    if strict and set(blocks.keys()) != set(REQUIRED_QUESTIONS):
        missing = sorted(set(REQUIRED_QUESTIONS) - set(blocks.keys()))
        raise ValueError(f"Incomplete run. Missing questions: {missing}")

    return resolved_run_id, run_dir, blocks


def build_evidence_catalog(run_dir: Path, blocks: dict[str, QuestionTestResultBlock]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for qid, block in blocks.items():
        if block.ledger.empty:
            continue
        for _, row in block.ledger.iterrows():
            rows.append(
                {
                    "run_id": run_dir.name,
                    "question_id": qid,
                    "test_id": str(row.get("test_id", "")),
                    "source_ref": str(row.get("source_ref", "")),
                    "mode": str(row.get("mode", "")),
                    "scenario_id": str(row.get("scenario_id", "")),
                    "status": str(row.get("status", "")),
                    "value": str(row.get("value", "")),
                    "threshold": str(row.get("threshold", "")),
                    "interpretation": str(row.get("interpretation", "")),
                    "evidence_ref": f"{block.files.get('ledger', Path())}#test_id={row.get('test_id', '')}",
                }
            )
    return pd.DataFrame(rows)


def build_test_traceability(run_dir: Path, blocks: dict[str, QuestionTestResultBlock]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for qid, block in blocks.items():
        if block.ledger.empty:
            continue
        for _, row in block.ledger.iterrows():
            rows.append(
                {
                    "run_id": run_dir.name,
                    "question_id": qid,
                    "test_id": str(row.get("test_id", "")),
                    "source_ref": str(row.get("source_ref", "")),
                    "mode": str(row.get("mode", "")),
                    "scenario_id": str(row.get("scenario_id", "")),
                    "status": str(row.get("status", "")),
                    "evidence_ref": f"{block.files.get('ledger', Path())}",
                }
            )
    return pd.DataFrame(rows)


def build_checks_catalog(run_dir: Path, blocks: dict[str, QuestionTestResultBlock]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for qid, block in blocks.items():
        if block.checks.empty:
            continue
        for _, row in block.checks.iterrows():
            rows.append(
                {
                    "run_id": run_dir.name,
                    "question_id": qid,
                    "status": str(row.get("status", "")),
                    "code": str(row.get("code", "")),
                    "message": str(row.get("message", "")),
                    "scope": str(row.get("scope", "")),
                    "scenario_id": str(row.get("scenario_id", "")),
                    "evidence_ref": f"{block.files.get('summary', Path())}",
                }
            )
    return pd.DataFrame(rows)
