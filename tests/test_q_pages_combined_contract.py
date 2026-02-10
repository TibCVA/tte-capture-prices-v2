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


def test_q_pages_have_combined_flow_literals() -> None:
    for page in Q_PAGES:
        text = _read(page)
        assert "## Ce que cette execution teste (historique + prospectif)" in text
        assert "run_question_bundle_cached(" in text
        assert "render_test_ledger(" in text
        assert "render_hist_scen_comparison(" in text
        assert "st.tabs(" in text


def test_q_pages_keep_submit_gate_for_heavy_run() -> None:
    for page in Q_PAGES:
        text = _read(page)
        assert "st.form_submit_button(" in text
        assert "Lancer l'analyse complete" in text
