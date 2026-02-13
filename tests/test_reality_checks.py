from __future__ import annotations

import pandas as pd

from src.modules.reality_checks import build_common_checks


def _first_status(checks: list[dict[str, str]], code: str) -> str:
    for c in checks:
        if str(c.get("code")) == code:
            return str(c.get("status"))
    return ""


def test_data_001_fails_when_hour_count_invalid():
    annual = pd.DataFrame(
        [
            {
                "country": "FR",
                "year": 2024,
                "n_hours": 8700,
                "coverage_price": 1.0,
                "coverage_load_total": 1.0,
                "ttl_eur_mwh": 80.0,
            }
        ]
    )
    checks = build_common_checks(annual)
    assert _first_status(checks, "TEST_DATA_001") == "FAIL"


def test_data_002_warns_with_coverage_fallback_from_missing_shares():
    annual = pd.DataFrame(
        [
            {
                "country": "FR",
                "year": 2024,
                "n_hours": 8760,
                "missing_share_price": 0.02,
                "missing_share_load": 0.03,
                "ttl_eur_mwh": 80.0,
            }
        ]
    )
    checks = build_common_checks(annual)
    assert _first_status(checks, "TEST_DATA_002") == "WARN"


def test_data_003_warns_on_large_price_outlier():
    annual = pd.DataFrame(
        [
            {
                "country": "FR",
                "year": 2024,
                "n_hours": 8760,
                "coverage_price": 1.0,
                "coverage_load_total": 1.0,
                "baseload_price_eur_mwh": 6000.0,
                "ttl_eur_mwh": 80.0,
            }
        ]
    )
    checks = build_common_checks(annual)
    assert _first_status(checks, "TEST_DATA_003") == "WARN"


def test_h_below_5_cannot_be_lower_than_h_negative():
    annual = pd.DataFrame(
        [
            {
                "country": "FR",
                "year": 2024,
                "n_hours": 8760,
                "h_negative": 120.0,
                "h_below_5": 80.0,
                "coverage_price": 1.0,
                "coverage_load_total": 1.0,
            }
        ]
    )
    checks = build_common_checks(annual)
    assert _first_status(checks, "RC_HB5_LT_HNEG") == "FAIL"


def test_non_negative_suffix_field_cannot_be_negative():
    annual = pd.DataFrame(
        [
            {
                "country": "FR",
                "year": 2024,
                "n_hours": 8760,
                "coverage_price": 1.0,
                "coverage_load_total": 1.0,
                "co2_required_base_non_negative": -1.0,
            }
        ]
    )
    checks = build_common_checks(annual)
    assert _first_status(checks, "RC_NON_NEGATIVE_FIELD_NEGATIVE") == "FAIL"
