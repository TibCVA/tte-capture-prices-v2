from __future__ import annotations

import json
from pathlib import Path
import zipfile

import pandas as pd

from src.reporting.audit_delivery import build_delivery_package, read_delivery_zip_bytes


def _build_minimal_audit_dir(audit_dir: Path, run_id: str) -> None:
    (audit_dir / "combined_run" / "Q1").mkdir(parents=True, exist_ok=True)
    (audit_dir / "combined_run" / "Q1" / "summary.json").write_text(
        json.dumps({"question_id": "Q1", "run_id": run_id}, ensure_ascii=False),
        encoding="utf-8",
    )
    reports_dir = audit_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    for name in [
        f"checks_catalog_{run_id}.csv",
        f"question_fail_matrix_{run_id}.csv",
        f"question_status_summary_{run_id}.csv",
        f"question_status_summary_global_{run_id}.csv",
        f"question_status_summary_scope_DE_ES_{run_id}.csv",
        f"test_traceability_{run_id}.csv",
        f"evidence_catalog_{run_id}.csv",
        f"detailed_es_de_{run_id}.md",
    ]:
        (reports_dir / name).write_text("col\nvalue\n", encoding="utf-8")
    (audit_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "critical_fail_codes_global": ["Q1_SCENARIO_EFFECT_PRESENT"],
                "critical_fail_codes_scope_de_es": ["Q1_SCENARIO_EFFECT_PRESENT"],
                "ceo_decision": "NO-GO",
                "ceo_critical_fail_codes_scope_de_es": ["Q1_SCENARIO_EFFECT_PRESENT"],
                "ceo_non_critical_fail_codes_scope_de_es": [],
                "ceo_no_go_reasons": [{"question_id": "Q1", "code": "Q1_SCENARIO_EFFECT_PRESENT", "reason": "critical_fail_code_in_scope_de_es"}],
                "ceo_scope_summary": [{"question_id": "Q1", "quality_status": "FAIL", "top_fail_codes": "Q1_SCENARIO_EFFECT_PRESENT"}],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (audit_dir / "llm_reports").mkdir(parents=True, exist_ok=True)
    (audit_dir / "llm_reports" / "Q1_HASH.json").write_text('{"status":"OK"}', encoding="utf-8")


def test_build_delivery_package_creates_zip_and_manifest(tmp_path: Path, monkeypatch) -> None:
    run_id = "RUN_DELIVERY_01"
    audit_dir = tmp_path / "outputs" / "audit_runs" / run_id
    _build_minimal_audit_dir(audit_dir, run_id)

    combined_dir = tmp_path / "outputs" / "combined" / run_id / "Q1"
    combined_dir.mkdir(parents=True, exist_ok=True)
    (combined_dir / "summary.json").write_text(
        json.dumps({"selection": {"years": [2024], "scenario_years": [2030], "scenario_ids": ["BASE"]}, "checks": []}),
        encoding="utf-8",
    )

    import src.reporting.audit_delivery as delivery_mod

    def fake_generate_extrait(**kwargs):  # type: ignore[no-untyped-def]
        output_md = Path(kwargs["output_md"])
        output_xlsx = Path(kwargs["output_xlsx"])
        output_md.parent.mkdir(parents=True, exist_ok=True)
        output_md.write_text("# fake", encoding="utf-8")
        with pd.ExcelWriter(output_xlsx) as writer:
            pd.DataFrame([{"country": "DE", "metric": 1}]).to_excel(writer, sheet_name="A1_annual_metrics", index=False)
            pd.DataFrame([{"test_id": "Q1-H-01", "status": "PASS"}]).to_excel(writer, sheet_name="test_ledger", index=False)
        return {"output_md": str(output_md), "output_xlsx": str(output_xlsx), "docx_generated": False, "rows": {}}

    monkeypatch.setattr(delivery_mod, "generate_extrait", fake_generate_extrait)
    monkeypatch.chdir(tmp_path)

    result = build_delivery_package(
        run_id=run_id,
        audit_dir=audit_dir,
        countries=["ES", "DE"],
        include_llm_reports=True,
    )

    zip_path = Path(result["zip_path"])
    manifest_path = Path(result["delivery_manifest_path"])
    xlsx_path = Path(result["results_xlsx_path"])
    assert zip_path.exists()
    assert manifest_path.exists()
    assert xlsx_path.exists()
    assert len(read_delivery_zip_bytes(zip_path)) > 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "critical_fail_codes_global" in manifest
    assert "critical_fail_codes_scope_de_es" in manifest
    assert manifest.get("ceo_decision") == "NO-GO"
    assert "ceo_critical_fail_codes_scope_de_es" in manifest
    assert "ceo_non_critical_fail_codes_scope_de_es" in manifest
    assert "ceo_no_go_reasons" in manifest
    assert "ceo_scope_summary" in manifest

    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        assert any(name.endswith("delivery_manifest.json") for name in names)
        assert any("/combined_run/Q1/summary.json" in name for name in names)
        assert any("/reports/checks_catalog_" in name for name in names)
        assert any("/reports/question_status_summary_global_" in name for name in names)
        assert any("/reports/question_status_summary_scope_DE_ES_" in name for name in names)
        assert any("/results_es_de_" in name and name.endswith(".xlsx") for name in names)
