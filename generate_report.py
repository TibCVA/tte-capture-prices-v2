from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def _latest_combined_run_dir() -> Path | None:
    root = Path("outputs/combined")
    if not root.exists():
        return None
    runs = [p for p in root.iterdir() if p.is_dir()]
    if not runs:
        return None
    runs = sorted(runs, key=lambda p: p.stat().st_mtime, reverse=True)
    return runs[0]


def _latest_question_dir(question_id: str) -> Path | None:
    root = Path("outputs/combined")
    if not root.exists():
        return None
    candidates: list[Path] = []
    for run_dir in root.iterdir():
        if not run_dir.is_dir():
            continue
        q_dir = run_dir / question_id
        if q_dir.exists() and q_dir.is_dir():
            candidates.append(q_dir)
    if not candidates:
        return None
    candidates = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


def _read_csv_safe(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def _read_md_safe(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _section_for_question(q_dir: Path | None, question_id: str) -> str:
    if q_dir is None:
        return f"## {question_id}\nAucun resultat combine disponible.\n"
    if not q_dir.exists():
        return f"## {question_id}\nAucun resultat combine disponible.\n"

    summary = _read_csv_safe(q_dir / "comparison_hist_vs_scen.csv")
    ledger = _read_csv_safe(q_dir / "test_ledger.csv")
    narrative = _read_md_safe(q_dir / "narrative.md")

    lines: list[str] = []
    lines.append(f"## {question_id}")
    if narrative:
        lines.append(narrative)
        lines.append("")

    if not ledger.empty:
        lines.append("### Tests executes")
        keep = [c for c in ["test_id", "mode", "scenario_id", "status", "value", "threshold", "interpretation", "source_ref"] if c in ledger.columns]
        lines.append("```text")
        lines.append(ledger[keep].to_string(index=False))
        lines.append("```")
        lines.append("")
    else:
        lines.append("### Tests executes")
        lines.append("Aucun test ledger disponible.")
        lines.append("")

    if not summary.empty:
        lines.append("### Comparaison historique vs prospectif")
        lines.append("```text")
        lines.append(summary.to_string(index=False))
        lines.append("```")
        lines.append("")
    else:
        lines.append("### Comparaison historique vs prospectif")
        lines.append("Aucune comparaison disponible.")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    reports = Path("reports")
    reports.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    combined_run = _latest_combined_run_dir()
    if combined_run is None:
        text = (
            f"# Rapport Final Detaille V2 - Run {run_id}\n\n"
            "Aucun output combine trouve dans `outputs/combined`.\n"
            "Lance d'abord une analyse complete Q1..Q5 depuis l'application.\n"
        )
    else:
        lines: list[str] = []
        lines.append(f"# Rapport Final Detaille V2 - Run {run_id}")
        lines.append("")
        lines.append("Generation combine-first: ce rapport lit d'abord les outputs unifies Q1..Q5.")
        lines.append(f"Dernier run combine detecte: `{combined_run}`")
        lines.append("")
        lines.append("## Resume executif")
        lines.append(
            "Le rapport consolide les tests historiques et prospectifs executes par question, "
            "avec separation explicite des statuts PASS/WARN/FAIL/NON_TESTABLE et comparaison historique vs scenario."
        )
        lines.append("")

        for q in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
            q_dir = _latest_question_dir(q)
            lines.append(_section_for_question(q_dir, q))

        lines.append("## Synthese finale")
        lines.append(
            "Les conclusions doivent etre lues avec les limits explicites de chaque question. "
            "Chaque assertion est tracee a un test_id et une source_ref (SPEC/Slides)."
        )
        text = "\n".join(lines)

    detailed = reports / f"conclusions_v2_detailed_{run_id}.md"
    detailed.write_text(text, encoding="utf-8")
    short = reports / f"conclusions_v2_{run_id}.md"
    short.write_text(f"# Conclusions V2 - Run {run_id}\n\nVoir `{detailed.name}`.\n", encoding="utf-8")

    print("RUN_ID", run_id)
    print("REPORT_DETAILED", detailed)
    print("REPORT_SHORT", short)


if __name__ == "__main__":
    main()
