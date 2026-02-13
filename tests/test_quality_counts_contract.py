from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import app.page_utils as page_utils


def _load_accueil_module():
    path = Path("app/pages/00_Accueil.py")
    spec = spec_from_file_location(f"tte_test_accueil_quality_{id(path)}", str(path))
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_check_counts_info_not_unknown_in_page_utils() -> None:
    checks = [
        {"status": "INFO", "code": "A"},
        {"status": "PASS", "code": "B"},
        {"status": "INFO", "code": "C"},
        "invalid",
    ]
    counts = page_utils._extract_check_counts(checks)  # type: ignore[attr-defined]
    assert counts["INFO"] == 2
    assert counts["PASS"] == 1
    assert counts["UNKNOWN"] == 1


def test_fail_codes_are_aggregated_and_unique_in_page_utils() -> None:
    checks = [
        {"status": "FAIL", "code": "RC_IR_GT_1"},
        {"status": "FAIL", "code": "RC_IR_GT_1"},
        {"status": "FAIL", "code": "RC_IR_GT_1"},
        {"status": "FAIL", "code": "RC_FAR_RANGE"},
        {"status": "WARN", "code": "RC_TTL_LOW"},
    ]
    out = page_utils._extract_fail_codes(checks, limit=5)  # type: ignore[attr-defined]
    assert out == ["RC_IR_GT_1 (x3)", "RC_FAR_RANGE"]


def test_fail_codes_are_aggregated_in_accueil_helpers() -> None:
    module = _load_accueil_module()
    checks = [
        {"status": "FAIL", "code": "RC_IR_GT_1"},
        {"status": "FAIL", "code": "RC_IR_GT_1"},
        {"status": "FAIL", "code": "RC_IR_GT_1"},
        {"status": "FAIL", "code": "RC_FAR_RANGE"},
    ]
    out = module._extract_fail_codes(checks, limit=5)
    assert out == ["RC_IR_GT_1 (x3)", "RC_FAR_RANGE"]
