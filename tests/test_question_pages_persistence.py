from __future__ import annotations

from pathlib import Path


Q_PAGES = [
    Path("app/pages/01_Q1_Phase1_to_Phase2.py"),
    Path("app/pages/02_Q2_Phase2_Slope.py"),
    Path("app/pages/03_Q3_Exit_Phase2.py"),
    Path("app/pages/04_Q4_BESS_OrderOfMagnitude.py"),
    Path("app/pages/05_Q5_CO2_Gas_Anchor.py"),
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_q_pages_restore_payload_from_session_cache_contract() -> None:
    for page in Q_PAGES:
        text = _read(page)
        assert "restore_question_payload_from_session_cache" in text
        assert "if RESULT_KEY not in st.session_state:" in text


def test_q_pages_show_quality_fail_banner_contract() -> None:
    for page in Q_PAGES:
        text = _read(page)
        assert "FAIL sur checks techniques (different du test_ledger ci-dessous)." in text
        assert "quality_status" in text
