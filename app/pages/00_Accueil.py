from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import json
import os

import pandas as pd
import streamlit as st

from src.reporting.evidence_loader import (
    compute_question_bundle_signature,
    discover_complete_runs,
    validate_combined_run,
)
from src.reporting.session_cache import clear_session_snapshot

_PAGE_UTILS_IMPORT_ERROR: Exception | None = None
_PAGE_UTILS_COMBINED_BUNDLE_AVAILABLE = True

try:
    import app.page_utils as _page_utils

    load_annual_metrics = _page_utils.load_annual_metrics
    load_phase2_assumptions_table = _page_utils.load_phase2_assumptions_table
    refresh_all_analyses_no_cache_ui = _page_utils.refresh_all_analyses_no_cache_ui
    build_bundle_hash = _page_utils.build_bundle_hash
    restore_question_payload_from_session_cache = getattr(
        _page_utils,
        "restore_question_payload_from_session_cache",
        None,
    )
    persist_question_payloads_to_session_cache = getattr(
        _page_utils,
        "persist_question_payloads_to_session_cache",
        None,
    )

    load_question_bundle_from_combined_run = getattr(_page_utils, "load_question_bundle_from_combined_run", None)
    load_question_bundle_from_combined_run_safe = getattr(
        _page_utils,
        "load_question_bundle_from_combined_run_safe",
        load_question_bundle_from_combined_run,
    )
    if callable(load_question_bundle_from_combined_run) and callable(load_question_bundle_from_combined_run_safe):
        _PAGE_UTILS_COMBINED_BUNDLE_AVAILABLE = True
    else:
        _PAGE_UTILS_COMBINED_BUNDLE_AVAILABLE = False
        load_question_bundle_from_combined_run = None
        load_question_bundle_from_combined_run_safe = None
        if not callable(restore_question_payload_from_session_cache):
            restore_question_payload_from_session_cache = None
        if not callable(persist_question_payloads_to_session_cache):
            persist_question_payloads_to_session_cache = None
except Exception as exc:  # pragma: no cover - defensive for Streamlit cloud stale caches
    _PAGE_UTILS_IMPORT_ERROR = exc
    _PAGE_UTILS_COMBINED_BUNDLE_AVAILABLE = False

    def refresh_all_analyses_no_cache_ui(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(f"app.page_utils indisponible (refresh_all_analyses_no_cache_ui). Cause: {exc}")

    def load_annual_metrics(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(f"app.page_utils indisponible (load_annual_metrics). Cause: {exc}")

    def build_bundle_hash(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(f"app.page_utils indisponible (build_bundle_hash). Cause: {exc}")

    def load_question_bundle_from_combined_run(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(f"app.page_utils indisponible (load_question_bundle_from_combined_run). Cause: {exc}")

    def load_question_bundle_from_combined_run_safe(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(
            f"app.page_utils indisponible (load_question_bundle_from_combined_run_safe). Cause: {exc}"
        )

    def load_phase2_assumptions_table(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(f"app.page_utils indisponible (load_phase2_assumptions_table). Cause: {exc}")

    def restore_question_payload_from_session_cache(*args, **kwargs):  # type: ignore[no-redef]
        return False

    def persist_question_payloads_to_session_cache(*args, **kwargs):  # type: ignore[no-redef]
        return None


if not _PAGE_UTILS_COMBINED_BUNDLE_AVAILABLE:
    _PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR = (
        _PAGE_UTILS_IMPORT_ERROR
        if _PAGE_UTILS_IMPORT_ERROR is not None
        else RuntimeError(
            "app.page_utils ne contient pas load_question_bundle_from_combined_run (fallback local actif)."
        )
    )
else:
    _PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR = None

from src.modules.bundle_result import QuestionBundleResult
from src.modules.result import ModuleResult


def _to_abs_project_path(path_like: str | Path) -> Path:
    path = Path(path_like)
    app_root = Path(__file__).resolve().parents[2]
    return path if path.is_absolute() else app_root / path


def _prime_onedrive_env_from_streamlit_secrets() -> None:
    try:
        onedrive_secrets = st.secrets.get("onedrive", {})
    except Exception:
        onedrive_secrets = {}

    mapping = {
        "ONEDRIVE_TENANT_ID": ["tenant_id", "ONEDRIVE_TENANT_ID"],
        "ONEDRIVE_CLIENT_ID": ["client_id", "ONEDRIVE_CLIENT_ID"],
        "ONEDRIVE_CLIENT_SECRET": ["client_secret", "ONEDRIVE_CLIENT_SECRET"],
        "ONEDRIVE_DRIVE_ID": ["drive_id", "ONEDRIVE_DRIVE_ID"],
        "ONEDRIVE_TARGET_DIR": ["target_dir", "ONEDRIVE_TARGET_DIR"],
    }
    for env_name, candidates in mapping.items():
        if str(os.environ.get(env_name, "")).strip():
            continue
        value = ""
        if isinstance(onedrive_secrets, dict):
            for key in candidates:
                raw = onedrive_secrets.get(key)
                if str(raw or "").strip():
                    value = str(raw).strip()
                    break
        if not value:
            for key in candidates:
                try:
                    raw_global = st.secrets.get(key)
                except Exception:
                    raw_global = None
                if str(raw_global or "").strip():
                    value = str(raw_global).strip()
                    break
        if value:
            os.environ[env_name] = value


def _safe_read_json(path: Path) -> dict:
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


def _safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def _load_tables_dir(tables_dir: Path) -> dict[str, pd.DataFrame]:
    out: dict[str, pd.DataFrame] = {}
    if not tables_dir.exists():
        return out
    for csv_path in sorted(tables_dir.glob("*.csv")):
        out[csv_path.stem] = _safe_read_csv(csv_path)
    return out


def _load_module_result_from_export(
    module_dir: Path,
    *,
    default_mode: str,
    default_run_id: str,
    default_selection: dict,
    default_module_id: str,
    scenario_id: str | None = None,
) -> ModuleResult:
    summary = _safe_read_json(module_dir / "summary.json")
    if not summary:
        raise FileNotFoundError(f"summary.json manquant/invalide: {module_dir / 'summary.json'}")
    checks = summary.get("checks", [])
    if not isinstance(checks, list):
        checks = []
    warnings = summary.get("warnings", [])
    if not isinstance(warnings, list):
        warnings = []
    kpis = summary.get("kpis", {})
    if not isinstance(kpis, dict):
        kpis = {}
    selection = summary.get("selection", default_selection)
    if not isinstance(selection, dict):
        selection = default_selection

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


def _load_question_bundle_from_combined_run_local(
    run_id: str,
    question_id: str,
    base_dir: str = "outputs/combined",
) -> tuple[QuestionBundleResult, Path]:
    qid = str(question_id).upper()
    if not str(run_id).strip():
        raise ValueError("run_id vide.")
    q_dir = _to_abs_project_path(base_dir) / str(run_id) / qid
    if not q_dir.exists():
        raise FileNotFoundError(f"Bundle introuvable: {q_dir}")

    bundle_summary = _safe_read_json(q_dir / "summary.json")
    if not bundle_summary:
        raise FileNotFoundError(f"summary.json manquant/invalide: {q_dir / 'summary.json'}")

    default_selection = bundle_summary.get("selection", {})
    if not isinstance(default_selection, dict):
        default_selection = {}

    hist_dir = q_dir / "hist"
    if not hist_dir.exists():
        raise FileNotFoundError(f"Resultat historique introuvable: {hist_dir}")

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
    if scen_root.exists():
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
        checks = []
    warnings = bundle_summary.get("warnings", [])
    if not isinstance(warnings, list):
        warnings = []

    bundle = QuestionBundleResult(
        question_id=qid,
        run_id=str(bundle_summary.get("run_id", run_id)),
        selection=default_selection,
        hist_result=hist_result,
        scen_results=scen_results,
        test_ledger=_safe_read_csv(q_dir / "test_ledger.csv"),
        comparison_table=_safe_read_csv(q_dir / "comparison_hist_vs_scen.csv"),
        checks=checks,
        warnings=[str(w) for w in warnings],
        narrative_md=_safe_read_text(q_dir / "narrative.md"),
    )
    return bundle, q_dir


if load_question_bundle_from_combined_run is None:  # type: ignore[comparison-overlap]
    if _PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR is None:
        _PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR = RuntimeError(
            "app.page_utils ne contient pas load_question_bundle_from_combined_run (fallback local actif)."
        )
    load_question_bundle_from_combined_run = _load_question_bundle_from_combined_run_local

if not callable(load_question_bundle_from_combined_run_safe):
    load_question_bundle_from_combined_run_safe = load_question_bundle_from_combined_run
if not callable(restore_question_payload_from_session_cache):
    def restore_question_payload_from_session_cache(*args, **kwargs):  # type: ignore[no-redef]
        return False
if not callable(persist_question_payloads_to_session_cache):
    def persist_question_payloads_to_session_cache(*args, **kwargs):  # type: ignore[no-redef]
        return None

_LLM_BATCH_IMPORT_ERROR: Exception | None = None
try:
    from app.llm_analysis import resolve_openai_api_key, serialize_bundle_for_llm
    from app.llm_batch import (
        QUESTION_ORDER,
        run_parallel_llm_generation,
        validate_llm_batch_rows,
    )
    from src.pipeline import load_assumptions_table
except Exception as exc:  # pragma: no cover - defensive
    _LLM_BATCH_IMPORT_ERROR = exc
    QUESTION_ORDER = ["Q1", "Q2", "Q3", "Q4", "Q5"]  # type: ignore[assignment]

    def resolve_openai_api_key(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("resolve_openai_api_key indisponible.")

    def serialize_bundle_for_llm(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("serialize_bundle_for_llm indisponible.")

    def run_parallel_llm_generation(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("run_parallel_llm_generation indisponible.")

    def validate_llm_batch_rows(*args, **kwargs):  # type: ignore[no-redef]
        return [], ["validate_llm_batch_rows indisponible."]

    def load_assumptions_table(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("load_assumptions_table indisponible.")

try:
    from src.runtime.llm_batch_events import append_llm_batch_event
except Exception:
    def append_llm_batch_event(*args, **kwargs):  # type: ignore[no-redef]
        return None

from app.ui_components import (
    guided_header,
    inject_theme,
    render_interpretation,
    render_kpi_cards_styled,
    render_question_box,
)
from src.constants import DEFAULT_COUNTRIES, DEFAULT_YEAR_END, DEFAULT_YEAR_START
from src.modules.bundle_result import QuestionBundleResult, export_question_bundle
from src.reporting.interpretation_rules import QUESTION_BUSINESS_TEXT

_RESULT_STATE_KEY_BY_QUESTION = {
    "Q1": "q1_bundle_result",
    "Q2": "q2_bundle_result",
    "Q3": "q3_bundle_result",
    "Q4": "q4_bundle_result",
    "Q5": "q5_bundle_result",
}
_RESULT_STATE_KEYS = tuple(_RESULT_STATE_KEY_BY_QUESTION.values())
_ACCUEIL_QUESTION_ORDER = tuple(QUESTION_ORDER)


def _snapshot_question_bundle_session_state() -> dict[str, object]:
    state_snapshot: dict[str, object] = {}
    for key in _RESULT_STATE_KEYS + (
        "last_full_refresh_run_id",
        "last_llm_batch_result",
        "llm_batch_running",
        "llm_batch_state",
        "last_delivery_zip_path",
        "last_delivery_manifest",
        "last_onedrive_upload_status",
    ):
        if key in st.session_state:
            state_snapshot[key] = st.session_state.get(key)
    return state_snapshot


def _restore_question_bundle_session_state(snapshot: dict[str, object]) -> None:
    for key in _RESULT_STATE_KEYS:
        st.session_state.pop(key, None)
    st.session_state.pop("last_full_refresh_run_id", None)
    st.session_state.pop("last_llm_batch_result", None)
    st.session_state.pop("llm_batch_running", None)
    st.session_state.pop("llm_batch_state", None)
    st.session_state.pop("last_delivery_zip_path", None)
    st.session_state.pop("last_delivery_manifest", None)
    st.session_state.pop("last_onedrive_upload_status", None)
    for key, value in snapshot.items():
        st.session_state[key] = value


def _extract_check_counts(checks: list[dict] | object) -> dict[str, int]:
    counts: dict[str, int] = {"PASS": 0, "WARN": 0, "FAIL": 0, "NON_TESTABLE": 0, "INFO": 0, "UNKNOWN": 0}
    if not isinstance(checks, list):
        return counts
    for raw in checks:
        if not isinstance(raw, dict):
            counts["UNKNOWN"] += 1
            continue
        status = str(raw.get("status", "UNKNOWN")).upper().strip()
        if status in counts:
            counts[status] += 1
        else:
            counts["UNKNOWN"] += 1
    return counts


def _extract_fail_codes(checks: list[dict] | object, limit: int = 5) -> list[str]:
    if not isinstance(checks, list):
        return []
    code_counts: Counter[str] = Counter()
    for raw in checks:
        if not isinstance(raw, dict):
            continue
        status = str(raw.get("status", "")).upper().strip()
        if status != "FAIL":
            continue
        code = str(raw.get("code", "")).strip()
        if not code:
            continue
        code_counts[code] += 1
    fail_codes: list[str] = []
    for code, count in sorted(code_counts.items(), key=lambda item: (-item[1], item[0]))[: int(limit)]:
        fail_codes.append(f"{code} (x{count})" if int(count) > 1 else code)
    return fail_codes


def _quality_status_from_counts(check_counts: dict[str, int]) -> str:
    if int(check_counts.get("FAIL", 0)) > 0:
        return "FAIL"
    if int(check_counts.get("WARN", 0)) > 0:
        return "WARN"
    return "PASS"


def _current_question_payloads() -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for qid in _ACCUEIL_QUESTION_ORDER:
        key = _RESULT_STATE_KEY_BY_QUESTION.get(qid)
        if not key:
            continue
        payload = st.session_state.get(key)
        if isinstance(payload, dict):
            out[qid] = payload
    return out


def _persist_session_cache_snapshot() -> tuple[str | None, str | None]:
    payloads = _current_question_payloads()
    last_batch = st.session_state.get("last_llm_batch_result")
    llm_batch_state = st.session_state.get("llm_batch_state")
    has_batch_payload = isinstance(last_batch, dict) and isinstance(last_batch.get("rows"), list)
    has_batch_state = isinstance(llm_batch_state, dict)
    if not payloads and not has_batch_payload and not has_batch_state:
        return None, None
    try:
        cache_path = persist_question_payloads_to_session_cache(
            payloads,
            last_llm_batch_result=last_batch if isinstance(last_batch, dict) else None,
            llm_batch_state=llm_batch_state if isinstance(llm_batch_state, dict) else None,
            base_dir="outputs/combined",
        )
    except Exception as exc:
        return None, str(exc)
    if cache_path is None:
        return None, None
    return str(cache_path), None


def _restore_session_from_disk_if_needed() -> tuple[list[str], dict[str, str]]:
    restored: list[str] = []
    failed: dict[str, str] = {}
    for qid in _ACCUEIL_QUESTION_ORDER:
        result_key = _RESULT_STATE_KEY_BY_QUESTION.get(qid)
        if not result_key:
            continue
        if result_key in st.session_state:
            continue
        try:
            ok = restore_question_payload_from_session_cache(
                question_id=qid,
                result_key=result_key,
                base_dir="outputs/combined",
            )
        except Exception as exc:
            failed[qid] = str(exc)
            continue
        if ok:
            restored.append(qid)
    return restored, failed


def _load_preferred_run_id(
    requested_run_id: str | None,
    base_dir: str = "outputs/combined",
) -> tuple[str, bool]:
    base = _to_abs_project_path(base_dir)
    requested = str(requested_run_id or "").strip()
    if requested:
        candidate = base / requested
        if candidate.exists() and candidate.is_dir():
            valid, _ = validate_combined_run(candidate)
            if valid:
                return requested, False
    # fallback to latest complete run
    runs = discover_complete_runs(base)
    if not runs:
        raise FileNotFoundError("Aucun run combine complet disponible pour le prechargement auto.")
    for run in runs:
        valid, issues = validate_combined_run(run)
        if valid:
            return run.name, True
    raise FileNotFoundError(
        "Aucun run combine strictement valide pour le prechargement auto: " + " | ".join(issues)
    )


def _make_bundle_signature(run_id: str, question_id: str, run_dir: Path) -> str:
    _ = run_id
    return compute_question_bundle_signature(run_dir, question_id)


def _clear_question_bundle_session_state() -> None:
    for key in _RESULT_STATE_KEYS:
        st.session_state.pop(key, None)
    st.session_state.pop("last_full_refresh_run_id", None)
    st.session_state.pop("last_llm_batch_result", None)
    st.session_state.pop("llm_batch_running", None)
    st.session_state.pop("llm_batch_state", None)
    st.session_state.pop("llm_batch_started_at_utc", None)
    st.session_state.pop("last_delivery_zip_path", None)
    st.session_state.pop("last_delivery_manifest", None)
    st.session_state.pop("last_onedrive_upload_status", None)
    st.session_state.pop("last_status_summary_global_path", None)
    st.session_state.pop("last_status_summary_scope_path", None)


def _collect_bundle_hash_by_question() -> dict[str, str]:
    out: dict[str, str] = {}
    for qid in _ACCUEIL_QUESTION_ORDER:
        result_key = _RESULT_STATE_KEY_BY_QUESTION.get(qid)
        if not result_key:
            continue
        payload = st.session_state.get(result_key)
        if not isinstance(payload, dict):
            continue
        bundle_hash = str(payload.get("bundle_hash", "")).strip()
        if bundle_hash:
            out[qid] = bundle_hash
    return out


def _build_auto_audit_bundle_after_refresh(run_id: str) -> tuple[bool, dict[str, object]]:
    run_id_clean = str(run_id).strip()
    if not run_id_clean:
        return False, {"error": "run_id vide"}
    try:
        from src.reporting.auto_audit_bundle import build_auto_audit_bundle
    except Exception as exc:
        return False, {"error": f"auto_audit_bundle import impossible: {exc}"}

    try:
        result = build_auto_audit_bundle(
            run_id=run_id_clean,
            countries=["ES", "DE"],
            include_llm_reports=True,
            bundle_hash_by_question=_collect_bundle_hash_by_question(),
            keep_last=5,
        )
    except Exception as exc:
        return False, {"error": str(exc)}

    delivery_report: dict[str, object] = {}
    try:
        from src.reporting.audit_delivery import build_delivery_package

        delivery_report = build_delivery_package(
            run_id=run_id_clean,
            audit_dir=Path(str(result.get("audit_dir", "")).strip()),
            countries=["ES", "DE"],
            include_llm_reports=True,
        )
    except Exception as exc:
        delivery_report = {"status": "FAILED_BUILD", "error": str(exc)}

    result["delivery"] = delivery_report
    status_global_path = str(result.get("question_status_summary_global_path", result.get("question_status_summary_path", ""))).strip()
    status_scope_path = str(result.get("question_status_summary_scope_path", "")).strip()
    st.session_state["last_status_summary_global_path"] = status_global_path
    st.session_state["last_status_summary_scope_path"] = status_scope_path
    st.session_state["last_delivery_zip_path"] = str(delivery_report.get("zip_path", "")).strip()
    st.session_state["last_delivery_manifest"] = str(delivery_report.get("delivery_manifest_path", "")).strip()

    zip_path = str(delivery_report.get("zip_path", "")).strip()
    upload_report: dict[str, object]
    if not zip_path:
        upload_report = {"status": "SKIPPED_NO_ZIP", "message": "ZIP de livraison indisponible."}
    else:
        try:
            _prime_onedrive_env_from_streamlit_secrets()
            from src.reporting.onedrive_uploader import upload_delivery_package

            upload_report = upload_delivery_package(Path(zip_path))
        except Exception as exc:
            upload_report = {"status": "FAILED", "error": str(exc)}
    result["onedrive_upload"] = upload_report
    st.session_state["last_onedrive_upload_status"] = upload_report
    return True, result


def _hydrate_question_pages_from_run(run_id: str, *, allow_fail_checks: bool = True) -> tuple[bool, dict[str, object]]:
    previous_state = _snapshot_question_bundle_session_state()
    run_id_clean = str(run_id).strip()
    if not run_id_clean:
        _restore_question_bundle_session_state(previous_state)
        return False, {"loaded": [], "failed": {"run": "run_id vide."}, "checks": {}, "signatures": {}, "preload_status": "PASS1_FAIL"}

    base = _to_abs_project_path("outputs/combined")
    run_dir = base / run_id_clean
    pass1_ok, pass1_issues = validate_combined_run(run_dir)
    if not pass1_ok:
        _restore_question_bundle_session_state(previous_state)
        return False, {
            "loaded": [],
            "failed": {"run": " | ".join(pass1_issues)},
            "checks": {},
            "signatures": {},
            "preload_status": "PASS1_FAIL",
        }

    pass1_signatures: dict[str, str] = {}
    for qid in _ACCUEIL_QUESTION_ORDER:
        pass1_signatures[qid] = _make_bundle_signature(run_id_clean, qid, run_dir)

    assumptions_phase1 = pd.DataFrame()
    assumptions_phase2 = pd.DataFrame()
    try:
        assumptions_phase1 = load_assumptions_table()
        assumptions_phase2 = load_phase2_assumptions_table()
    except Exception:
        pass

    loaded_payloads: dict[str, dict[str, object]] = {}
    failed: dict[str, str] = {}
    pass2_signatures: dict[str, str] = {}
    pass2_checks: dict[str, dict[str, int]] = {}
    pass2_fail_codes: dict[str, list[str]] = {}

    for qid_raw in _ACCUEIL_QUESTION_ORDER:
        qid = str(qid_raw).upper()
        result_key = _RESULT_STATE_KEY_BY_QUESTION.get(qid)
        if not result_key:
            failed[qid] = "Cle de session manquante."
            continue
        try:
            bundle, out_dir = load_question_bundle_from_combined_run_safe(
                run_id=run_id_clean,
                question_id=qid,
                allow_fail_checks=allow_fail_checks,
                expected_signature=pass1_signatures.get(qid),
            )
        except Exception as exc:
            failed[qid] = str(exc)
            continue

        if not isinstance(bundle, QuestionBundleResult):
            failed[qid] = "Type de bundle invalide."
            continue
        if bundle.run_id != run_id_clean:
            failed[qid] = f"run_id incoherent: {bundle.run_id}"
            continue

        checks = _extract_check_counts(bundle.checks)
        if checks.get("FAIL", 0) > 0 and not allow_fail_checks:
            failed[qid] = f"Checks FAIL detectes: {checks}"
            continue
        fail_codes = _extract_fail_codes(bundle.checks, limit=5)
        quality_status = _quality_status_from_counts(checks)

        signature = compute_question_bundle_signature(run_dir, qid)
        if signature != pass1_signatures.get(qid):
            failed[qid] = "Signature incoherente entre passes."
            continue
        pass2_signatures[qid] = signature
        pass2_checks[qid] = checks
        pass2_fail_codes[qid] = fail_codes

        bundle_hash = f"{run_id_clean}_{qid}"
        if isinstance(bundle.selection, dict) and not assumptions_phase1.empty:
            try:
                bundle_hash = build_bundle_hash(qid, bundle.selection, assumptions_phase1, assumptions_phase2)
            except Exception:
                bundle_hash = f"{run_id_clean}_{qid}"

        loaded_payloads[qid] = {
            "bundle": bundle,
            "out_dir": str(out_dir),
            "bundle_hash": bundle_hash,
            "quality_status": quality_status,
            "check_counts": checks,
            "fail_codes_top5": fail_codes,
        }

    # Pass 3: verification non destructive avant ecriture de session.
    if len(loaded_payloads) != len(_ACCUEIL_QUESTION_ORDER) or failed:
        _restore_question_bundle_session_state(previous_state)
        return False, {
            "loaded": [],
            "failed": failed,
            "checks": pass2_checks,
            "fail_codes": pass2_fail_codes,
            "signatures": pass2_signatures,
            "preload_status": "PASS3_FAIL",
            "pass2_signatures": pass2_signatures,
        }

    loaded_run_ids = {str(p["bundle"].run_id) for p in loaded_payloads.values() if isinstance(p.get("bundle"), QuestionBundleResult)}  # type: ignore[index]
    if len(loaded_run_ids) != 1 or run_id_clean not in loaded_run_ids:
        _restore_question_bundle_session_state(previous_state)
        return False, {
            "loaded": [],
            "failed": {"run": "run_id incoherent entre questions."},
            "checks": pass2_checks,
            "fail_codes": pass2_fail_codes,
            "signatures": pass2_signatures,
            "preload_status": "PASS3_FAIL",
            "pass2_signatures": pass2_signatures,
        }

    for qid in _ACCUEIL_QUESTION_ORDER:
        if pass2_signatures.get(qid) != _make_bundle_signature(run_id_clean, qid, run_dir):
            _restore_question_bundle_session_state(previous_state)
            return False, {
                "loaded": [],
                "failed": {"run": "Signature incoherente entre pass2 et pass3."},
                "checks": pass2_checks,
                "fail_codes": pass2_fail_codes,
                "signatures": pass2_signatures,
                "preload_status": "PASS3_FAIL",
                "pass2_signatures": pass2_signatures,
            }

    # Commit transactionnel: on clear puis on Ã©crit l'Ã©tat de session.
    _clear_question_bundle_session_state()
    for qid, payload in loaded_payloads.items():
        result_key = _RESULT_STATE_KEY_BY_QUESTION.get(qid)
        if not result_key:
            _restore_question_bundle_session_state(previous_state)
            return False, {
                "loaded": [],
                "failed": {"run": "Cle de session manquante en commit."},
                "checks": pass2_checks,
                "fail_codes": pass2_fail_codes,
                "signatures": pass2_signatures,
                "preload_status": "PASS3_FAIL",
                "pass2_signatures": pass2_signatures,
            }
        if not all(field in payload for field in ["bundle", "out_dir", "bundle_hash"]):
            _restore_question_bundle_session_state(previous_state)
            return False, {
                "loaded": [],
                "failed": {"run": f"Payload incomplet pour {qid}."},
                "checks": pass2_checks,
                "fail_codes": pass2_fail_codes,
                "signatures": pass2_signatures,
                "preload_status": "PASS3_FAIL",
                "pass2_signatures": pass2_signatures,
            }
        st.session_state[result_key] = payload

    st.session_state["last_full_refresh_run_id"] = run_id_clean
    cache_path, cache_error = _persist_session_cache_snapshot()
    try:
        st.cache_data.clear()
    except Exception:
        pass
    try:
        st.cache_resource.clear()
    except Exception:
        pass
    return True, {
        "loaded": sorted(_ACCUEIL_QUESTION_ORDER),
        "failed": {},
        "checks": pass2_checks,
        "fail_codes": pass2_fail_codes,
        "signatures": pass2_signatures,
        "preload_status": "OK",
        "pass2_signatures": pass2_signatures,
        "cache_path": cache_path,
        "cache_error": cache_error,
    }


def _hydrate_question_pages_from_prepared(prepared_items: list[dict]) -> tuple[list[str], dict[str, str]]:
    loaded: list[str] = []
    failed: dict[str, str] = {}
    loaded_run_ids: set[str] = set()
    for item in prepared_items:
        qid = str(item.get("question_id", "")).upper()
        if not qid:
            continue
        result_key = _RESULT_STATE_KEY_BY_QUESTION.get(qid)
        if not result_key:
            continue
        if str(item.get("status", "")).upper() == "FAILED_PREP":
            failed[qid] = str(item.get("error", "Preparation echouee."))
            continue

        bundle = item.get("bundle", None)
        if bundle is None:
            failed[qid] = "Bundle absent apres preparation."
            continue

        bundle_hash = str(item.get("bundle_hash", "")).strip()
        if not bundle_hash:
            failed[qid] = "Bundle hash absent apres preparation."
            continue

        try:
            out_dir = export_question_bundle(bundle)
        except Exception as exc:
            failed[qid] = f"Export bundle impossible: {exc}"
            continue

        checks = _extract_check_counts(getattr(bundle, "checks", []))
        fail_codes = _extract_fail_codes(getattr(bundle, "checks", []), limit=5)
        st.session_state[result_key] = {
            "bundle": bundle,
            "out_dir": str(out_dir),
            "bundle_hash": bundle_hash,
            "quality_status": _quality_status_from_counts(checks),
            "check_counts": checks,
            "fail_codes_top5": fail_codes,
        }
        loaded_run_ids.add(str(getattr(bundle, "run_id", "")).strip())
        loaded.append(qid)
    run_ids = {rid for rid in loaded_run_ids if rid}
    if len(run_ids) == 1:
        st.session_state["last_full_refresh_run_id"] = next(iter(run_ids))
    _persist_session_cache_snapshot()
    return loaded, failed


def _prepared_item_from_payload(qid: str, payload: dict[str, object], source: str) -> dict[str, object]:
    bundle = payload.get("bundle")
    if not isinstance(bundle, QuestionBundleResult):
        raise TypeError(f"{qid}: payload bundle invalide.")
    bundle_hash = str(payload.get("bundle_hash", "")).strip() or f"{bundle.run_id}_{qid}"
    bundle_data = serialize_bundle_for_llm(bundle)
    return {
        "question_id": qid,
        "bundle_hash": bundle_hash,
        "bundle": bundle,
        "bundle_data": bundle_data,
        "source": source,
    }


def build_prepared_items_for_llm_batch() -> tuple[list[dict[str, object]], dict[str, str], dict[str, str]]:
    prepared_items: list[dict[str, object]] = []
    failed: dict[str, str] = {}
    source_by_qid: dict[str, str] = {}
    fallback_run_id: str | None = None

    for qid in _ACCUEIL_QUESTION_ORDER:
        result_key = _RESULT_STATE_KEY_BY_QUESTION.get(qid, "")
        payload = st.session_state.get(result_key)
        if isinstance(payload, dict):
            try:
                prepared_items.append(_prepared_item_from_payload(qid, payload, "session"))
                source_by_qid[qid] = "session"
                continue
            except Exception:
                pass

        restored_ok = False
        try:
            restored_ok = bool(
                restore_question_payload_from_session_cache(
                    question_id=qid,
                    result_key=result_key,
                    base_dir="outputs/combined",
                )
            )
        except Exception:
            restored_ok = False
        if restored_ok:
            payload = st.session_state.get(result_key)
            if isinstance(payload, dict):
                try:
                    prepared_items.append(_prepared_item_from_payload(qid, payload, "session_cache"))
                    source_by_qid[qid] = "session_cache"
                    continue
                except Exception:
                    pass

        if fallback_run_id is None:
            try:
                preferred = str(st.session_state.get("last_full_refresh_run_id", "")).strip() or None
                fallback_run_id, _ = _load_preferred_run_id(preferred, base_dir="outputs/combined")
            except Exception:
                fallback_run_id = ""
        if fallback_run_id:
            try:
                bundle, out_dir = load_question_bundle_from_combined_run_safe(
                    run_id=fallback_run_id,
                    question_id=qid,
                    base_dir="outputs/combined",
                    allow_fail_checks=True,
                )
                checks = _extract_check_counts(bundle.checks)
                fail_codes = _extract_fail_codes(bundle.checks, limit=5)
                payload = {
                    "bundle": bundle,
                    "out_dir": str(out_dir),
                    "bundle_hash": f"{bundle.run_id}_{qid}",
                    "quality_status": _quality_status_from_counts(checks),
                    "check_counts": checks,
                    "fail_codes_top5": fail_codes,
                }
                st.session_state[result_key] = payload
                st.session_state["last_full_refresh_run_id"] = str(bundle.run_id)
                prepared_items.append(_prepared_item_from_payload(qid, payload, "combined_run"))
                source_by_qid[qid] = "combined_run"
                continue
            except Exception as exc:
                failed[qid] = f"chargement run combine impossible: {exc}"

        if qid not in failed:
            failed[qid] = "aucun bundle disponible (session/cache/run combine)."
        prepared_items.append(
            {
                "question_id": qid,
                "status": "FAILED_PREP",
                "bundle_hash": "",
                "error": failed[qid],
                "source": "missing",
            }
        )
        source_by_qid[qid] = "missing"

    return prepared_items, failed, source_by_qid


def _merge_llm_batch_rows(
    previous_rows: list[dict[str, object]],
    new_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    merged: dict[str, dict[str, object]] = {}

    for raw in previous_rows:
        if not isinstance(raw, dict):
            continue
        qid = str(raw.get("question_id", "")).upper().strip()
        if not qid:
            continue
        merged[qid] = dict(raw)

    for raw in new_rows:
        if not isinstance(raw, dict):
            continue
        qid = str(raw.get("question_id", "")).upper().strip()
        if not qid:
            continue
        candidate = dict(raw)
        status = str(candidate.get("status", "")).upper().strip()
        existing = merged.get(qid)
        if status.startswith("FAILED_") and isinstance(existing, dict):
            if str(existing.get("status", "")).upper().strip() == "OK":
                existing["last_attempt_status"] = status
                existing["last_attempt_error"] = str(candidate.get("error", "")).strip()
                existing["attempted_at_utc"] = datetime.now(timezone.utc).isoformat()
                merged[qid] = existing
                continue
        merged[qid] = candidate

    order = {qid: idx for idx, qid in enumerate(_ACCUEIL_QUESTION_ORDER)}
    return sorted(
        merged.values(),
        key=lambda row: (order.get(str(row.get("question_id", "")).upper(), 99), str(row.get("question_id", ""))),
    )


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _heartbeat_timeout_seconds() -> int:
    raw = str(os.getenv("LLM_BATCH_HEARTBEAT_TIMEOUT_S", "180")).strip()
    try:
        value = int(raw)
    except Exception:
        value = 180
    return value if value > 0 else 180


def _mark_running_batch_interrupted_if_stale() -> bool:
    state = st.session_state.get("llm_batch_state")
    if not isinstance(state, dict):
        return False
    if str(state.get("status", "")).upper().strip() != "RUNNING":
        return False
    hb_raw = str(state.get("heartbeat_utc", "")).strip()
    if not hb_raw:
        return False
    try:
        heartbeat = datetime.fromisoformat(hb_raw.replace("Z", "+00:00"))
    except Exception:
        return False
    age_seconds = (datetime.now(timezone.utc) - heartbeat.astimezone(timezone.utc)).total_seconds()
    if age_seconds <= float(_heartbeat_timeout_seconds()):
        return False
    state["status"] = "INTERRUPTED"
    state["interrupted_at_utc"] = _utc_now_iso()
    state["last_error"] = f"Batch interrompu (heartbeat > {_heartbeat_timeout_seconds()}s)."
    st.session_state["llm_batch_state"] = state
    _persist_session_cache_snapshot()
    append_llm_batch_event(
        "interrupted",
        {
            "batch_id": str(state.get("batch_id", "")),
            "reason": str(state.get("last_error", "")),
            "completed_qids": list(state.get("completed_qids", [])),
            "expected_qids": list(state.get("expected_qids", [])),
        },
    )
    return True


def _upsert_llm_batch_state(
    *,
    batch_id: str,
    status: str,
    expected_qids: list[str],
    completed_qids: list[str],
    last_error: str = "",
) -> None:
    st.session_state["llm_batch_state"] = {
        "batch_id": str(batch_id),
        "started_at_utc": str(st.session_state.get("llm_batch_started_at_utc", _utc_now_iso())),
        "status": str(status).upper(),
        "expected_qids": [str(q).upper() for q in expected_qids if str(q).strip()],
        "completed_qids": [str(q).upper() for q in completed_qids if str(q).strip()],
        "heartbeat_utc": _utc_now_iso(),
        "last_error": str(last_error or "").strip(),
    }


def _last_llm_batch_event_label() -> str:
    log_path = Path("outputs/audit/llm_batch_events.jsonl")
    abs_path = _to_abs_project_path(log_path)
    if not abs_path.exists():
        return ""
    try:
        lines = abs_path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return ""
    if not lines:
        return ""
    try:
        payload = json.loads(lines[-1])
    except Exception:
        return ""
    event_type = str(payload.get("event_type", "")).strip()
    ts = str(payload.get("timestamp_utc", "")).strip()
    details = payload.get("payload", {})
    if isinstance(details, dict):
        qid = str(details.get("question_id", "")).strip()
        status = str(details.get("status", "")).strip()
        if qid and status:
            return f"Dernier evenement batch IA: {event_type} | {qid} -> {status} | {ts}"
    return f"Dernier evenement batch IA: {event_type} | {ts}"


def render() -> None:
    inject_theme()
    guided_header(
        title="TTE Capture Prices V2",
        purpose="Outil d'analyse historique des capture prices et des phases structurelles, auditable et explicable.",
        step_now="Accueil: comprendre le parcours",
        step_next="Mode d'emploi: definitions et methode",
    )
    restored_q, _ = _restore_session_from_disk_if_needed()
    if restored_q:
        st.info(
            "Restauration automatique des analyses depuis le cache local: "
            + ", ".join(restored_q)
        )
    if _mark_running_batch_interrupted_if_stale():
        st.warning("Batch IA interrompu detecte apres reprise runtime. Les resultats partiels ont ete restaures.")

    llm_batch_state = st.session_state.get("llm_batch_state")
    if isinstance(llm_batch_state, dict):
        status = str(llm_batch_state.get("status", "")).upper().strip()
        expected = list(llm_batch_state.get("expected_qids", []))
        completed = list(llm_batch_state.get("completed_qids", []))
        if status:
            st.caption(
                f"Etat batch IA: {status} | progression {len(completed)}/{len(expected)}"
                + (f" | batch_id={llm_batch_state.get('batch_id', '')}" if llm_batch_state.get("batch_id") else "")
            )
    last_event_label = _last_llm_batch_event_label()
    if last_event_label:
        st.caption(last_event_label)

    render_kpi_cards_styled(
        [
            {"label": "Pays cibles", "value": len(DEFAULT_COUNTRIES), "help": "Perimetre par defaut verrouille a 7 pays."},
            {"label": "Fenetre historique", "value": f"{DEFAULT_YEAR_START}-{DEFAULT_YEAR_END}", "help": "Fenetre par defaut utilisee dans les analyses."},
            {"label": "Resolution", "value": "Horaire UTC", "help": "Aucun calcul infra-horaire (pas 15 min)."},
        ]
    )

    st.markdown("## Ce que fait l'outil")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            '<div class="tte-card" style="min-height:130px;">'
            "<strong>Dynamique des capture prices</strong><br>"
            "Expliquer l'evolution des capture prices PV/Wind sur base horaire pour 7 pays europeens."
            "</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="tte-card" style="min-height:130px;">'
            "<strong>Phases structurelles</strong><br>"
            "Identifier les bascules de phase et les drivers physiques/marche (SR, FAR, IR, regimes)."
            "</div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="tte-card" style="min-height:130px;">'
            "<strong>Tests auditables</strong><br>"
            "Tester les questions Q1..Q5 avec checks automatiques et exports auditables traces au run_id."
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("## Les 5 questions business")
    for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        text = QUESTION_BUSINESS_TEXT.get(qid, "")
        render_question_box(f"**{qid}** : {text}")

    st.info(
        "Le modele reste volontairement pedestre: il privilegie l'explicabilite et l'auditabilite sur la complexite. "
        "Les conclusions sont toujours conditionnelles aux hypotheses et doivent etre nuancees."
    )

    st.markdown("## Parcours recommande")
    st.markdown(
        "1. **Mode d'emploi**: comprendre les definitions et limites.\n"
        "2. **Donnees & Qualite**: charger ou recalculer les jeux de donnees.\n"
        "3. **Socle Physique**: verifier NRL/surplus/flex avant interpretation.\n"
        "4. **Q1..Q5**: repondre aux questions business module par module.\n"
        "5. **Conclusions**: lire le rapport final trace au run_id."
    )

    st.markdown("## Rafraichissement global des analyses")
    st.caption(
        "Ce bouton reconstruit toutes les analyses (Q1..Q5) sans reutiliser les caches de calculs, "
        "tout en conservant les donnees ENTSO-E brutes deja telechargees en local."
    )
    if st.button("Reinitialiser cache analyses"):
        _clear_question_bundle_session_state()
        try:
            clear_session_snapshot()
        except Exception as exc:
            st.warning(f"Cache fichier non purge completement: {exc}")
        try:
            st.cache_data.clear()
        except Exception:
            pass
        try:
            st.cache_resource.clear()
        except Exception:
            pass
        st.success("Cache analyses reinitialise (session + persistance locale).")
    if _PAGE_UTILS_IMPORT_ERROR is not None:
        st.error("Impossible de charger le module de refresh global.")
        st.code(str(_PAGE_UTILS_IMPORT_ERROR))
    else:
        if st.button("Lancer / rafraichir toutes les analyses (sans cache calcule)", type="primary"):
            with st.spinner("Refresh global en cours (rebuild historique + run combine Q1..Q5)..."):
                try:
                    refresh_summary = refresh_all_analyses_no_cache_ui(
                        countries=DEFAULT_COUNTRIES,
                        hist_year_start=DEFAULT_YEAR_START,
                        hist_year_end=DEFAULT_YEAR_END,
                        scenario_years=list(range(2025, 2036)),
                    )
                except Exception as exc:
                    st.error(f"Echec du refresh global: {exc}")
                else:
                    requested_run_id = str(refresh_summary.get("run_id", "")).strip()
                    if not requested_run_id:
                        st.error("Run_id invalide retourne par le refresh global.")
                    else:
                        try:
                            resolved_run_id, fallback_run = _load_preferred_run_id(
                                requested_run_id,
                                base_dir="outputs/combined",
                            )
                        except Exception as exc:
                            st.error(f"Prechargement impossible: {exc}")
                            with st.expander("Details techniques du refresh", expanded=False):
                                st.json(refresh_summary)
                        else:
                            if fallback_run:
                                st.warning(
                                    "Run_id demande introuvable ou incomplet, utilisation du run combine complet le plus recent: "
                                    + resolved_run_id
                                )
                            if _PAGE_UTILS_COMBINED_BUNDLE_AVAILABLE is False:
                                st.info(
                                    "Prechargement local actif par compatibilite page_utils."
                                )
                            st.success(f"Refresh termine. Nouveau run combine: {resolved_run_id}")
                            st.caption(
                                f"Run choisi: {resolved_run_id} | "
                                f"Questions lancees: Q1..Q5 | "
                                f"Historique: {DEFAULT_YEAR_START}-{DEFAULT_YEAR_END} | "
                                "Scenarios: 2025-2035"
                            )
                            if _PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR is not None and fallback_run:
                                st.info(
                                    "Prechargement en mode fallback local actif via 00_Accueil (mode de compatibilite)."
                                )
                            with st.spinner("Chargement automatique des resultats Q1..Q5 dans les pages..."):
                                preload_ok, preload_report = _hydrate_question_pages_from_run(
                                    resolved_run_id,
                                    allow_fail_checks=True,
                                )

                            if preload_ok:
                                checks_by_q = preload_report.get("checks", {})
                                fail_codes_by_q = preload_report.get("fail_codes", {})
                                if isinstance(checks_by_q, dict) and checks_by_q:
                                    details = []
                                    fail_q: list[str] = []
                                    for qid in _ACCUEIL_QUESTION_ORDER:
                                        q_checks = checks_by_q.get(qid, {})
                                        if not isinstance(q_checks, dict):
                                            continue
                                        q_checks_parts = [f"{k}={v}" for k, v in q_checks.items()]
                                        details.append(f"{qid}: " + ", ".join(q_checks_parts))
                                        if int(q_checks.get("FAIL", 0)) > 0:
                                            fail_q.append(qid)
                                    if details:
                                        st.info("Checks par question: " + " | ".join(details))
                                    if fail_q:
                                        st.warning(
                                            "Analyses chargees malgre checks FAIL: "
                                            + ", ".join(fail_q)
                                            + ". Les onglets Q affichent les resultats avec alerte qualite."
                                        )
                                if isinstance(fail_codes_by_q, dict):
                                    fail_details = []
                                    for qid in _ACCUEIL_QUESTION_ORDER:
                                        codes = fail_codes_by_q.get(qid, [])
                                        if not isinstance(codes, list) or not codes:
                                            continue
                                        fail_details.append(f"{qid}: {', '.join(str(c) for c in codes)}")
                                    if fail_details:
                                        st.caption("Top FAIL codes: " + " | ".join(fail_details))
                                cache_path = str(preload_report.get("cache_path", "")).strip()
                                cache_error = str(preload_report.get("cache_error", "")).strip()
                                if cache_path:
                                    st.caption(f"Cache session mis a jour: {cache_path}")
                                if cache_error:
                                    st.warning(f"Cache session non persiste: {cache_error}")
                                st.success("Prechargement auto complete des sections Q1..Q5.")
                            else:
                                failed_q = preload_report.get("failed", {})
                                if isinstance(failed_q, dict) and failed_q:
                                    st.error("Prechargement bloque: " + " | ".join([f"{qid}: {msg}" for qid, msg in failed_q.items()]))
                                else:
                                    st.error("Prechargement bloque (raison inconnue).")
                                if _PAGE_UTILS_COMBINED_BUNDLE_AVAILABLE is False and _PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR is not None:
                                    st.info(
                                        "Prechargement local actif par compatibilite page_utils: "
                                        + str(_PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR)
                                    )
                            with st.spinner("Generation du dossier d'audit automatique..."):
                                audit_ok, audit_report = _build_auto_audit_bundle_after_refresh(resolved_run_id)
                            refresh_summary["auto_audit_bundle"] = audit_report
                            if audit_ok:
                                audit_dir = str(audit_report.get("audit_dir", "")).strip()
                                md_path = str(audit_report.get("detailed_markdown_path", "")).strip()
                                if audit_dir:
                                    st.success(f"Dossier audit genere automatiquement: {audit_dir}")
                                if md_path:
                                    st.caption(f"Markdown detaille ES/DE: {md_path}")
                                warnings = audit_report.get("warnings", [])
                                if isinstance(warnings, list) and warnings:
                                    st.warning("Audit auto warnings: " + " | ".join([str(w) for w in warnings]))
                                status_global_df: pd.DataFrame | None = None
                                status_scope_df: pd.DataFrame | None = None
                                status_global_path = str(
                                    audit_report.get(
                                        "question_status_summary_global_path",
                                        audit_report.get("question_status_summary_path", ""),
                                    )
                                ).strip()
                                status_scope_path = str(audit_report.get("question_status_summary_scope_path", "")).strip()
                                if status_global_path:
                                    st.session_state["last_status_summary_global_path"] = status_global_path
                                    st.caption(f"Statut global run: {status_global_path}")
                                    try:
                                        status_global_df = pd.read_csv(status_global_path)
                                    except Exception as exc:
                                        st.warning(f"Lecture statut global impossible: {exc}")
                                    else:
                                        if status_global_df.empty:
                                            st.info("Statut global run: tableau vide.")
                                        else:
                                            st.dataframe(status_global_df, use_container_width=True, hide_index=True)
                                if status_scope_path:
                                    st.session_state["last_status_summary_scope_path"] = status_scope_path
                                    st.caption(f"Statut scope pack DE/ES: {status_scope_path}")
                                    try:
                                        status_scope_df = pd.read_csv(status_scope_path)
                                    except Exception as exc:
                                        st.warning(f"Lecture statut scope DE/ES impossible: {exc}")
                                    else:
                                        if status_scope_df.empty:
                                            st.info("Statut scope pack DE/ES: tableau vide.")
                                        else:
                                            st.dataframe(status_scope_df, use_container_width=True, hide_index=True)
                                if (
                                    isinstance(status_global_df, pd.DataFrame)
                                    and isinstance(status_scope_df, pd.DataFrame)
                                    and not status_global_df.empty
                                    and not status_scope_df.empty
                                ):
                                    global_view = status_global_df[
                                        ["question_id", "quality_status", "top_fail_codes"]
                                    ].rename(
                                        columns={
                                            "quality_status": "quality_status_global",
                                            "top_fail_codes": "top_fail_codes_global",
                                        }
                                    )
                                    scope_view = status_scope_df[
                                        ["question_id", "quality_status", "top_fail_codes"]
                                    ].rename(
                                        columns={
                                            "quality_status": "quality_status_scope",
                                            "top_fail_codes": "top_fail_codes_scope",
                                        }
                                    )
                                    merged_status = global_view.merge(scope_view, on="question_id", how="inner")
                                    diverged = merged_status[
                                        (merged_status["quality_status_global"].astype(str).str.upper() == "FAIL")
                                        & (merged_status["quality_status_scope"].astype(str).str.upper() != "FAIL")
                                    ]
                                    if not diverged.empty:
                                        details: list[str] = []
                                        for _, row in diverged.iterrows():
                                            qid = str(row.get("question_id", "")).strip()
                                            global_codes = str(row.get("top_fail_codes_global", "")).strip() or "n/a"
                                            scope_codes = str(row.get("top_fail_codes_scope", "")).strip() or "n/a"
                                            details.append(
                                                f"{qid}: global FAIL ({global_codes}) / scope {row.get('quality_status_scope', '')} ({scope_codes})"
                                            )
                                        st.info("Divergence global/scope DE/ES: " + " | ".join(details))

                                delivery_report = audit_report.get("delivery", {})
                                if isinstance(delivery_report, dict):
                                    delivery_status = str(delivery_report.get("status", "")).upper().strip()
                                    if delivery_status and delivery_status != "READY":
                                        st.warning(
                                            "Livraison pack audit: "
                                            + str(delivery_report.get("error", delivery_status))
                                        )
                                    zip_path = str(delivery_report.get("zip_path", "")).strip()
                                    manifest_path = str(delivery_report.get("delivery_manifest_path", "")).strip()
                                    if zip_path:
                                        st.caption(f"Pack livraison: {zip_path}")
                                        try:
                                            from src.reporting.audit_delivery import read_delivery_zip_bytes

                                            zip_bytes = read_delivery_zip_bytes(zip_path)
                                        except Exception as exc:
                                            st.warning(f"Impossible de charger le ZIP de livraison: {exc}")
                                        else:
                                            st.download_button(
                                                label=f"Telecharger {Path(zip_path).name}",
                                                data=zip_bytes,
                                                file_name=Path(zip_path).name,
                                                mime="application/zip",
                                                use_container_width=True,
                                                key=f"dl_delivery_refresh_{resolved_run_id}",
                                            )
                                    if manifest_path:
                                        st.caption(f"Manifest livraison: {manifest_path}")

                                upload_report = audit_report.get("onedrive_upload", {})
                                if isinstance(upload_report, dict):
                                    status = str(upload_report.get("status", "")).upper()
                                    if status == "UPLOADED":
                                        st.success("OneDrive upload: UPLOADED")
                                    elif status.startswith("SKIPPED"):
                                        st.info("OneDrive upload: " + str(upload_report.get("message", status)))
                                    elif status:
                                        st.warning("OneDrive upload: " + str(upload_report.get("error", status)))
                            else:
                                st.warning(
                                    "Generation auto du dossier d'audit non bloquante: "
                                    + str(audit_report.get("error", "erreur inconnue"))
                                )
                            with st.expander("Details techniques du refresh", expanded=False):
                                st.json(refresh_summary)
                                if isinstance(preload_report, dict):
                                    st.code(preload_report)

    st.markdown("## Artefacts d'audit du run")
    last_zip_path = str(st.session_state.get("last_delivery_zip_path", "")).strip()
    last_manifest_path = str(st.session_state.get("last_delivery_manifest", "")).strip()
    if last_zip_path and Path(last_zip_path).exists():
        st.caption(f"Dernier pack: {last_zip_path}")
        try:
            from src.reporting.audit_delivery import read_delivery_zip_bytes

            _latest_zip_bytes = read_delivery_zip_bytes(last_zip_path)
        except Exception as exc:
            st.warning(f"ZIP indisponible pour telechargement: {exc}")
        else:
            st.download_button(
                label="Telecharger le dernier pack d'audit",
                data=_latest_zip_bytes,
                file_name=Path(last_zip_path).name,
                mime="application/zip",
                use_container_width=True,
                key="dl_delivery_latest",
            )
    else:
        st.caption("Aucun pack d'audit livre dans cette session.")
    if last_manifest_path:
        st.caption(f"Dernier manifest: {last_manifest_path}")
    last_status_global_path = str(st.session_state.get("last_status_summary_global_path", "")).strip()
    last_status_scope_path = str(st.session_state.get("last_status_summary_scope_path", "")).strip()
    if last_status_global_path:
        st.caption(f"Statut global run: {last_status_global_path}")
    if last_status_scope_path:
        st.caption(f"Statut scope pack DE/ES: {last_status_scope_path}")
    last_upload_status = st.session_state.get("last_onedrive_upload_status")
    if isinstance(last_upload_status, dict) and last_upload_status:
        status = str(last_upload_status.get("status", "")).upper()
        if status == "UPLOADED":
            st.success("Statut upload OneDrive: UPLOADED")
        elif status.startswith("SKIPPED"):
            st.info("Statut upload OneDrive: " + str(last_upload_status.get("message", status)))
        else:
            st.warning("Statut upload OneDrive: " + str(last_upload_status.get("error", status)))

    st.markdown("## Generation IA globale")
    st.caption(
        "Lance en une fois les generations IA Q1->Q5 en parallele, avec les selections par defaut "
        "de chaque page question."
    )
    if _LLM_BATCH_IMPORT_ERROR is not None:
        st.error("Impossible de charger le module de batch IA.")
        st.code(str(_LLM_BATCH_IMPORT_ERROR))
    elif st.button("Generer toutes les analyses IA (Q1->Q5 en parallele)", type="primary"):
        if bool(st.session_state.get("llm_batch_running", False)):
            st.warning("Un batch IA est deja en cours. Attendre la fin avant de relancer.")
        else:
            st.session_state["llm_batch_running"] = True
            try:
                api_key = resolve_openai_api_key()
                if not api_key:
                    st.error("Cle OpenAI manquante. Configure OPENAI_API_KEY dans l'environnement ou les secrets Streamlit.")
                else:
                    prep_progress = st.progress(0.0)
                    prep_status = st.empty()
                    prep_status.text("Preparation IA: reutilisation des bundles existants/cache/run combine...")
                    prepared_items, prep_failed, prep_sources = build_prepared_items_for_llm_batch()
                    prep_progress.progress(0.4)

                    prep_status.text("Prechargement des sections Q1..Q5...")
                    loaded_q, failed_q = _hydrate_question_pages_from_prepared(prepared_items)
                    prep_progress.progress(0.6)

                    if prep_sources:
                        src_msg = ", ".join([f"{qid}:{src}" for qid, src in sorted(prep_sources.items())])
                        st.caption("Sources bundles batch IA: " + src_msg)
                    if prep_failed:
                        st.warning(
                            "Questions sans bundle pret (skip non bloquant): "
                            + " | ".join([f"{qid}: {msg}" for qid, msg in prep_failed.items()])
                        )

                    expected_qids = [
                        str(item.get("question_id", "")).upper()
                        for item in prepared_items
                        if str(item.get("question_id", "")).strip()
                    ]
                    st.session_state["llm_batch_started_at_utc"] = _utc_now_iso()
                    batch_id = f"LLM_BATCH_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
                    _upsert_llm_batch_state(
                        batch_id=batch_id,
                        status="RUNNING",
                        expected_qids=expected_qids,
                        completed_qids=[],
                    )
                    _persist_session_cache_snapshot()
                    append_llm_batch_event(
                        "start",
                        {
                            "batch_id": batch_id,
                            "expected_qids": expected_qids,
                            "sources": prep_sources,
                        },
                    )

                    prep_status.text("Generation IA en parallele en cours...")
                    llm_progress = st.progress(0.0)
                    llm_status = st.empty()
                    llm_total = max(1, len(expected_qids))
                    llm_done = {"count": 0}

                    def _on_llm_item_done(row: dict) -> None:
                        llm_done["count"] = int(llm_done.get("count", 0)) + 1
                        done = int(llm_done["count"])
                        qid = str(row.get("question_id", "")).upper()
                        status = str(row.get("status", "")).upper()
                        llm_progress.progress(min(done / llm_total, 1.0))
                        llm_status.text(f"IA {done}/{llm_total}: {qid} -> {status}")

                        previous_batch = st.session_state.get("last_llm_batch_result")
                        previous_rows = []
                        if isinstance(previous_batch, dict) and isinstance(previous_batch.get("rows"), list):
                            previous_rows = list(previous_batch.get("rows", []))
                        merged_incremental = _merge_llm_batch_rows(previous_rows, [row])
                        st.session_state["last_llm_batch_result"] = {
                            "generated_at_utc": _utc_now_iso(),
                            "rows": merged_incremental,
                        }
                        state = st.session_state.get("llm_batch_state")
                        if isinstance(state, dict):
                            completed = {str(q).upper() for q in state.get("completed_qids", []) if str(q).strip()}
                            if qid:
                                completed.add(qid)
                            _upsert_llm_batch_state(
                                batch_id=str(state.get("batch_id", batch_id)),
                                status=str(state.get("status", "RUNNING")),
                                expected_qids=list(state.get("expected_qids", expected_qids)),
                                completed_qids=sorted(completed),
                                last_error=str(state.get("last_error", "")),
                            )
                        _persist_session_cache_snapshot()
                        append_llm_batch_event(
                            "item_done",
                            {
                                "batch_id": batch_id,
                                "question_id": qid,
                                "status": status,
                                "error": str(row.get("error", "")).strip(),
                            },
                        )

                    raw_timeout = str(os.getenv("LLM_BATCH_TIMEOUT_S", "420")).strip()
                    try:
                        batch_timeout_s = int(raw_timeout)
                    except Exception:
                        batch_timeout_s = 420
                    if batch_timeout_s <= 0:
                        batch_timeout_s = 420

                    raw_workers = str(os.getenv("LLM_BATCH_MAX_WORKERS", "2")).strip()
                    try:
                        max_workers = int(raw_workers)
                    except Exception:
                        max_workers = 2
                    if max_workers <= 0:
                        max_workers = 2

                    with st.spinner("Appels IA Q1->Q5 en execution parallele..."):
                        raw_rows = run_parallel_llm_generation(
                            prepared_items=prepared_items,
                            api_key=api_key,
                            max_workers=max_workers,
                            batch_timeout_s=batch_timeout_s,
                            on_item_done=_on_llm_item_done,
                        )
                    llm_progress.progress(1.0)
                    llm_status.text(f"IA {llm_total}/{llm_total}: traitement termine.")
                    expected_by_qid = {
                        str(item.get("question_id", "")).upper(): str(item.get("bundle_hash", "")).strip()
                        for item in prepared_items
                        if str(item.get("status", "")).upper() != "FAILED_PREP"
                        and str(item.get("bundle_hash", "")).strip()
                    }
                    rows, row_issues = validate_llm_batch_rows(raw_rows, expected_by_qid)
                    prep_progress.progress(1.0)
                    prep_status.empty()
                    prep_progress.empty()
                    llm_status.empty()
                    llm_progress.empty()

                    previous_batch = st.session_state.get("last_llm_batch_result")
                    previous_rows = []
                    if isinstance(previous_batch, dict) and isinstance(previous_batch.get("rows"), list):
                        previous_rows = list(previous_batch.get("rows", []))
                    merged_rows = _merge_llm_batch_rows(previous_rows, rows)
                    st.session_state["last_llm_batch_result"] = {
                        "generated_at_utc": _utc_now_iso(),
                        "rows": merged_rows,
                    }

                    if loaded_q:
                        st.info(f"Sections prechargees apres batch IA: {', '.join(loaded_q)}")
                    if failed_q:
                        st.warning(
                            "Prechargement partiel apres batch IA: "
                            + " | ".join([f"{qid}: {msg}" for qid, msg in failed_q.items()])
                        )
                    if row_issues:
                        st.warning("Controles batch IA: " + " | ".join(row_issues))
                    ok_count = sum(1 for row in merged_rows if str(row.get("status", "")).upper() == "OK")
                    raw_fail_rows = [row for row in rows if str(row.get("status", "")).upper().startswith("FAILED_")]
                    raw_fail_count = len(raw_fail_rows)
                    preserved_rows = [
                        row
                        for row in merged_rows
                        if str(row.get("status", "")).upper() == "OK"
                        and str(row.get("last_attempt_status", "")).upper().startswith("FAILED_")
                    ]
                    if preserved_rows:
                        preserved_q = ", ".join(str(r.get("question_id", "")) for r in preserved_rows if str(r.get("question_id", "")).strip())
                        st.info(
                            "Generation IA: rapports precedents conserves pour les questions en echec de la tentative courante"
                            + (f" ({preserved_q})." if preserved_q else ".")
                        )
                    final_status = "COMPLETED" if raw_fail_count == 0 else "COMPLETED_PARTIAL"
                    _upsert_llm_batch_state(
                        batch_id=batch_id,
                        status=final_status,
                        expected_qids=expected_qids,
                        completed_qids=expected_qids,
                        last_error="" if raw_fail_count == 0 else "Batch termine avec echecs partiels.",
                    )
                    _persist_session_cache_snapshot()
                    append_llm_batch_event(
                        "completed",
                        {
                            "batch_id": batch_id,
                            "status": final_status,
                            "ok_count": ok_count,
                            "failed_count": raw_fail_count,
                            "issues": row_issues,
                        },
                    )
                    if raw_fail_count == 0:
                        st.success(f"Generation IA terminee: {ok_count}/{len(merged_rows)} questions traitees.")
                    else:
                        st.warning(
                            "Generation IA terminee avec succes partiel non bloquant: "
                            + f"{ok_count} questions disponibles, {raw_fail_count} echec(s) sur la tentative courante."
                        )
            except Exception as exc:
                state = st.session_state.get("llm_batch_state")
                if isinstance(state, dict):
                    _upsert_llm_batch_state(
                        batch_id=str(state.get("batch_id", "")),
                        status="FAILED",
                        expected_qids=list(state.get("expected_qids", [])),
                        completed_qids=list(state.get("completed_qids", [])),
                        last_error=str(exc),
                    )
                    _persist_session_cache_snapshot()
                append_llm_batch_event("failed", {"error": str(exc)})
                st.error(f"Echec batch IA: {exc}")
            finally:
                st.session_state["llm_batch_running"] = False

    last_batch = st.session_state.get("last_llm_batch_result")
    if isinstance(last_batch, dict) and isinstance(last_batch.get("rows"), list):
        ts = str(last_batch.get("generated_at_utc", ""))
        if ts:
            st.caption(f"Derniere execution batch IA: {ts}")
        table_rows = list(last_batch.get("rows", []))
        if table_rows:
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

    render_interpretation(
        "Suivre ce parcours dans l'ordre garantit que chaque etape repose sur des donnees validees. "
        "Ne pas sauter directement aux conclusions sans avoir verifie la qualite des donnees."
    )



