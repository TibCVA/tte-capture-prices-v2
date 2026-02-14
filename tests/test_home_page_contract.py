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
    assert "_build_auto_audit_bundle_after_refresh(" in content
    assert "Generation du dossier d'audit automatique" in content
    assert "Dossier audit genere automatiquement" in content
    assert "## Artefacts d'audit du run" in content
    assert "Telecharger le dernier pack d'audit" in content
    assert "Statut global run" in content
    assert "Statut scope pack DE/ES" in content
    assert "Divergence global/scope DE/ES" in content
    assert 'st.session_state["last_delivery_zip_path"]' in content
    assert 'st.session_state["last_onedrive_upload_status"]' in content
    assert 'st.session_state["last_status_summary_global_path"]' in content
    assert 'st.session_state["last_status_summary_scope_path"]' in content


def test_checks_wording_is_explicit_and_not_global() -> None:
    content = Path("app/ui_components.py").read_text(encoding="utf-8")
    assert "Statut checks techniques: FAIL" in content
    assert "Statut checks techniques: WARN" in content
    assert "Statut checks techniques: PASS" in content
    assert "Statut global: FAIL" not in content
