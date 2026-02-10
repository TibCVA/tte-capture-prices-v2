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


def test_q_pages_have_required_sections() -> None:
    required_literals = [
        "## Question business",
        "## Hypotheses utilisees",
        "## Tests empiriques",
        "## Resultats et interpretation",
        "## Checks & exports",
    ]

    for page in Q_PAGES:
        content = _read(page)
        for lit in required_literals:
            assert lit in content, f"Missing section '{lit}' in {page}"
        assert ("## Limites" in content) or ("show_limitations(" in content), f"Missing limites section in {page}"


def test_q_pages_use_form_submit_for_heavy_runs() -> None:
    for page in Q_PAGES:
        content = _read(page)
        assert "st.form_submit_button(" in content, f"Missing st.form_submit_button in {page}"
