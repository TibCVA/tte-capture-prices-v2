from __future__ import annotations

from pathlib import Path


def test_home_page_contains_global_llm_batch_controls() -> None:
    content = Path("app/pages/00_Accueil.py").read_text(encoding="utf-8")

    assert "## Generation IA globale" in content
    assert "Generer toutes les analyses IA (Q1->Q5 en parallele)" in content
    assert "run_parallel_llm_generation(" in content
    assert "validate_llm_batch_rows(" in content
    assert 'st.session_state["last_llm_batch_result"]' in content


def test_home_page_contains_session_cache_controls() -> None:
    content = Path("app/pages/00_Accueil.py").read_text(encoding="utf-8")
    assert "Reinitialiser cache analyses" in content
    assert "_restore_session_from_disk_if_needed()" in content
    assert "Analyses chargees malgre checks FAIL" in content
