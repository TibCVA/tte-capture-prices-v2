from __future__ import annotations

from pathlib import Path


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_accueil_has_interrupt_recovery_hooks() -> None:
    text = _read(Path("app/pages/00_Accueil.py"))
    assert "_mark_running_batch_interrupted_if_stale" in text
    assert "Batch IA interrompu detecte apres reprise runtime" in text
    assert "_upsert_llm_batch_state" in text


def test_accueil_prepares_batch_with_reuse_first_strategy() -> None:
    text = _read(Path("app/pages/00_Accueil.py"))
    assert "build_prepared_items_for_llm_batch" in text
    assert "reutilisation des bundles existants/cache/run combine" in text
    assert "skip non bloquant" in text
