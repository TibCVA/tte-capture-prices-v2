from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from src.reporting.evidence_loader import compute_question_bundle_signature

SESSION_CACHE_SCHEMA_VERSION = 1
DEFAULT_SESSION_CACHE_FILE = Path("outputs/session_cache/session_state.json")
REQUIRED_QUESTIONS: tuple[str, ...] = ("Q1", "Q2", "Q3", "Q4", "Q5")


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _resolve_cache_file(cache_file: Path | None = None) -> Path:
    if cache_file is None:
        cache_file = DEFAULT_SESSION_CACHE_FILE
    return cache_file if cache_file.is_absolute() else _project_root() / cache_file


def load_session_snapshot(cache_file: Path | None = None) -> dict[str, Any] | None:
    path = _resolve_cache_file(cache_file)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def save_session_snapshot(snapshot: dict[str, Any], cache_file: Path | None = None) -> Path:
    if not isinstance(snapshot, dict):
        raise ValueError("snapshot invalide (dict attendu).")
    path = _resolve_cache_file(cache_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(snapshot)
    payload["schema_version"] = SESSION_CACHE_SCHEMA_VERSION
    payload["saved_at_utc"] = datetime.now(timezone.utc).isoformat()

    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(path)
    return path


def clear_session_snapshot(cache_file: Path | None = None) -> None:
    path = _resolve_cache_file(cache_file)
    if path.exists():
        path.unlink()


def build_question_snapshot_entry(
    *,
    question_id: str,
    result_key: str,
    run_id: str,
    out_dir: str,
    bundle_hash: str,
    signature: str,
    quality_status: str,
    check_counts: dict[str, int],
    fail_codes_top5: list[str],
) -> dict[str, Any]:
    return {
        "question_id": str(question_id).upper(),
        "result_key": str(result_key),
        "run_id": str(run_id),
        "out_dir": str(out_dir),
        "bundle_hash": str(bundle_hash),
        "signature": str(signature),
        "quality_status": str(quality_status).upper(),
        "check_counts": {str(k).upper(): int(v) for k, v in (check_counts or {}).items()},
        "fail_codes_top5": [str(code) for code in (fail_codes_top5 or [])[:5]],
    }


def validate_session_snapshot(
    snapshot: dict[str, Any],
    combined_base_dir: Path,
) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not isinstance(snapshot, dict):
        return False, ["Snapshot invalide (dict attendu)."]

    schema_version = snapshot.get("schema_version")
    if int(schema_version or 0) != SESSION_CACHE_SCHEMA_VERSION:
        errors.append(
            f"Schema snapshot incompatible: {schema_version} (attendu={SESSION_CACHE_SCHEMA_VERSION})."
        )
        return False, errors

    active_run_id = str(snapshot.get("active_run_id", "")).strip()
    if not active_run_id:
        errors.append("active_run_id manquant dans le snapshot.")
        return False, errors

    if active_run_id != "MIXED":
        run_dir = combined_base_dir / active_run_id
        if not run_dir.exists() or not run_dir.is_dir():
            errors.append(f"Run actif introuvable: {run_dir}")
            return False, errors

        run_mtime_ns = snapshot.get("run_dir_mtime_ns")
        if run_mtime_ns is not None:
            try:
                expected_mtime_ns = int(run_mtime_ns)
            except Exception:
                errors.append("run_dir_mtime_ns invalide.")
            else:
                if int(run_dir.stat().st_mtime_ns) != expected_mtime_ns:
                    errors.append("run_dir_mtime_ns incoherent (run potentiellement remplace).")

    questions = snapshot.get("questions")
    if not isinstance(questions, dict) or not questions:
        errors.append("questions manquantes dans le snapshot.")
        return False, errors

    valid_entries = 0
    for qid in REQUIRED_QUESTIONS:
        entry = questions.get(qid)
        if entry is None:
            continue
        if not isinstance(entry, dict):
            errors.append(f"Entree snapshot invalide pour {qid}.")
            continue
        entry_run_id = str(entry.get("run_id", "")).strip()
        if not entry_run_id:
            errors.append(f"run_id manquant dans l'entree snapshot {qid}.")
            continue
        if active_run_id != "MIXED" and entry_run_id != active_run_id:
            errors.append(f"run_id incoherent dans l'entree snapshot {qid}.")
            continue
        run_dir = combined_base_dir / entry_run_id
        q_dir = run_dir / qid
        if not run_dir.exists() or not run_dir.is_dir():
            errors.append(f"Run question introuvable pour {qid}: {run_dir}")
            continue
        required_paths = [
            q_dir / "summary.json",
            q_dir / "test_ledger.csv",
            q_dir / "comparison_hist_vs_scen.csv",
            q_dir / "hist",
            q_dir / "scen",
        ]
        missing = [str(p) for p in required_paths if not p.exists()]
        if missing:
            errors.append(f"Artefacts manquants pour {qid}: " + ", ".join(missing))
            continue
        signature = str(entry.get("signature", "")).strip()
        if not signature:
            errors.append(f"signature manquante dans l'entree snapshot {qid}.")
            continue
        expected_signature = compute_question_bundle_signature(run_dir, qid)
        if signature != expected_signature:
            errors.append(f"signature incoherente pour {qid}.")
            continue
        valid_entries += 1

    if valid_entries == 0:
        errors.append("Aucune entree question valide dans le snapshot.")

    last_batch = snapshot.get("last_llm_batch_result")
    if last_batch is not None:
        if not isinstance(last_batch, dict):
            errors.append("last_llm_batch_result invalide (dict attendu).")
        elif not isinstance(last_batch.get("rows", []), list):
            errors.append("last_llm_batch_result.rows invalide (list attendue).")

    return len(errors) == 0, errors
