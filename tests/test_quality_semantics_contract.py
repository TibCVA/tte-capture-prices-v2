from __future__ import annotations

from pathlib import Path
import re


def test_rc_ir_gt_1_severity_contract_is_warn() -> None:
    content = Path("src/modules/reality_checks.py").read_text(encoding="utf-8")
    matches = re.findall(r'"code":\s*"RC_IR_GT_1".{0,160}?"status":\s*"([A-Z_]+)"', content, flags=re.DOTALL)
    assert matches
    assert set(matches) == {"WARN"}


def test_bundle_mismatch_check_is_explicitly_emitted() -> None:
    content = Path("src/modules/question_bundle_runner.py").read_text(encoding="utf-8")
    assert "BUNDLE_LEDGER_CONSOLIDATED_MISMATCH" in content
    assert "ledger_fail_count == 0 and consolidated_fail_count > 0" in content
    assert 'mismatch_status = "WARN" if mismatch_only_bundle_diagnostics else "FAIL"' in content


def test_q1_floor_and_effect_trace_contract_present() -> None:
    content = Path("src/modules/question_bundle_runner.py").read_text(encoding="utf-8")
    assert "Q1_SCENARIO_FLOOR_APPLIED" in content
    assert "Q1_scenario_param_trace" in content
    assert "effect_nonzero_flag" in content
    assert "h_negative_at_end_year" in content
    assert "stress_nonzero_share" in content


def test_q3_differentiation_check_contract_present() -> None:
    content = Path("src/modules/question_bundle_runner.py").read_text(encoding="utf-8")
    assert "Q3_SCENARIO_DIFFERENTIATION" in content


def test_auto_audit_bundle_exports_global_and_scope_status_files() -> None:
    content = Path("src/reporting/auto_audit_bundle.py").read_text(encoding="utf-8")
    assert "question_status_summary_global_" in content
    assert "question_status_summary_scope_DE_ES_" in content
