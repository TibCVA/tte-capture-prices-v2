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


def test_ui_status_wording_is_explicit_for_checks() -> None:
    ui_content = _read(Path("app/ui_components.py"))
    assert "Statut checks techniques: FAIL" in ui_content
    assert "Statut checks techniques: WARN" in ui_content
    assert "Statut checks techniques: PASS" in ui_content


def test_q_pages_show_checks_vs_tests_distinction() -> None:
    for page in Q_PAGES:
        text = _read(page)
        assert "FAIL sur checks techniques (different du test_ledger ci-dessous)." in text
        assert "Tests empiriques:" in text
        assert "Voir l'onglet Details techniques > Checks & exports pour le detail des checks." in text
