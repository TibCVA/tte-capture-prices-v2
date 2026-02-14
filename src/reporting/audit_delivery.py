from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import zipfile
from typing import Any

from scripts.generate_extrait_data_outil_v7 import generate_extrait


DEFAULT_RUNTIME_EVENTS_PATH = Path("outputs/audit/runtime_events.jsonl")
DEFAULT_COUNTRY_SCOPE = ["ES", "DE"]


def _append_runtime_event(event_type: str, payload: dict[str, Any], log_path: Path = DEFAULT_RUNTIME_EVENTS_PATH) -> Path:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    line = {
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "event_type": str(event_type),
        "payload": payload,
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    return log_path


def _copy_tree_if_exists(src: Path, dst: Path, required: bool) -> None:
    if not src.exists():
        if required:
            raise FileNotFoundError(f"Dossier requis introuvable: {src}")
        return
    shutil.copytree(src, dst)


def _zip_directory(source_dir: Path, zip_path: Path, arc_root: str) -> int:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in sorted(source_dir.rglob("*")):
            if item.is_file():
                rel = item.relative_to(source_dir).as_posix()
                zf.write(item, arcname=f"{arc_root}/{rel}")
    try:
        return int(zip_path.stat().st_size)
    except Exception:
        return 0


def read_delivery_zip_bytes(zip_path: Path | str) -> bytes:
    path = Path(zip_path)
    if not path.exists():
        raise FileNotFoundError(f"ZIP introuvable: {path}")
    return path.read_bytes()


def build_delivery_package(
    run_id: str,
    *,
    audit_dir: Path | str,
    countries: list[str] | None = None,
    include_llm_reports: bool = True,
) -> dict[str, Any]:
    run_id_clean = str(run_id).strip()
    if not run_id_clean:
        raise ValueError("run_id vide.")

    audit_root = Path(audit_dir)
    if not audit_root.exists():
        raise FileNotFoundError(f"audit_dir introuvable: {audit_root}")

    country_scope = [str(c).upper().strip() for c in (countries or DEFAULT_COUNTRY_SCOPE) if str(c).strip()]
    if not country_scope:
        country_scope = list(DEFAULT_COUNTRY_SCOPE)
    country_scope = [c for c in country_scope if c in {"DE", "ES"}]
    if set(country_scope) != {"DE", "ES"}:
        country_scope = ["DE", "ES"]
    else:
        country_scope = ["DE", "ES"]

    package_name = f"FULL_{run_id_clean}_{'_'.join(country_scope)}"
    delivery_base = audit_root / "delivery"
    delivery_dir = delivery_base / package_name
    if delivery_dir.exists():
        shutil.rmtree(delivery_dir, ignore_errors=True)
    delivery_dir.mkdir(parents=True, exist_ok=True)

    _copy_tree_if_exists(audit_root / "combined_run", delivery_dir / "combined_run", required=True)
    _copy_tree_if_exists(audit_root / "reports", delivery_dir / "reports", required=True)
    if include_llm_reports:
        _copy_tree_if_exists(audit_root / "llm_reports", delivery_dir / "llm_reports", required=False)

    results_xlsx_path = delivery_dir / f"results_es_de_{run_id_clean}.xlsx"
    extrait_md_path = delivery_dir / "reports" / f"extrait_es_de_{run_id_clean}.md"
    extrait_docx_path = delivery_dir / "reports" / f"extrait_es_de_{run_id_clean}.docx"
    extrait_result = generate_extrait(
        run_id=run_id_clean,
        countries=["ES", "DE"],
        output_docx=extrait_docx_path,
        output_md=extrait_md_path,
        output_xlsx=results_xlsx_path,
        generate_docx=False,
        combined_base_dir=Path("outputs/combined"),
    )

    audit_manifest: dict[str, Any] = {}
    audit_manifest_path = audit_root / "manifest.json"
    if audit_manifest_path.exists():
        try:
            audit_manifest = json.loads(audit_manifest_path.read_text(encoding="utf-8"))
        except Exception:
            audit_manifest = {}

    delivery_manifest_path = delivery_dir / "delivery_manifest.json"
    zip_path = delivery_base / f"{package_name}.zip"

    manifest = {
        "run_id": run_id_clean,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "countries": ["ES", "DE"],
        "package_name": package_name,
        "audit_dir": str(audit_root),
        "delivery_dir": str(delivery_dir),
        "zip_path": str(zip_path),
        "reports_dir": str(delivery_dir / "reports"),
        "combined_run_dir": str(delivery_dir / "combined_run"),
        "llm_reports_dir": str(delivery_dir / "llm_reports") if (delivery_dir / "llm_reports").exists() else "",
        "results_xlsx_path": str(results_xlsx_path),
        "extrait_result": extrait_result,
        "critical_fail_codes_global": list(audit_manifest.get("critical_fail_codes_global", []))
        if isinstance(audit_manifest.get("critical_fail_codes_global", []), list)
        else [],
        "critical_fail_codes_scope_de_es": list(audit_manifest.get("critical_fail_codes_scope_de_es", []))
        if isinstance(audit_manifest.get("critical_fail_codes_scope_de_es", []), list)
        else [],
    }
    delivery_manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    zip_size = _zip_directory(delivery_dir, zip_path, package_name)
    event_log_path = _append_runtime_event(
        "delivery_package_built",
        {
            "run_id": run_id_clean,
            "delivery_dir": str(delivery_dir),
            "zip_path": str(zip_path),
            "zip_size_bytes": zip_size,
        },
    )

    return {
        "run_id": run_id_clean,
        "status": "READY",
        "countries": ["ES", "DE"],
        "package_name": package_name,
        "delivery_dir": str(delivery_dir),
        "zip_path": str(zip_path),
        "zip_size_bytes": zip_size,
        "delivery_manifest_path": str(delivery_manifest_path),
        "results_xlsx_path": str(results_xlsx_path),
        "event_log_path": str(event_log_path),
    }
