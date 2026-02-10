"""Build a single markdown payload ready to copy/paste into another LLM.

The payload aggregates a structured country package produced by:
`scripts/export_structured_country_pack.py`
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a one-file LLM payload from a structured package.")
    parser.add_argument(
        "--package-dir",
        type=str,
        default="",
        help="Path to reports/chatgpt52_structured_* package. If omitted, latest is used.",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="",
        help="Output markdown file path. If omitted, generated under reports/.",
    )
    return parser.parse_args()


def _latest_structured_package() -> Path:
    candidates = sorted(
        [
            p
            for p in REPORTS_DIR.glob("chatgpt52_structured_*")
            if p.is_dir()
        ],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError("No structured package found in reports/.")
    return candidates[0]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _fence_for(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".json":
        return "json"
    if ext == ".csv":
        return "csv"
    if ext == ".md":
        return "markdown"
    return "text"


def _append_file_block(lines: list[str], path: Path, title: str) -> None:
    if not path.exists():
        return
    rel = path.relative_to(ROOT)
    lines.append(f"### {title}")
    lines.append(f"Source: `{rel}`")
    lines.append("")
    lang = _fence_for(path)
    lines.append(f"```{lang}")
    lines.append(_read_text(path).rstrip())
    lines.append("```")
    lines.append("")


def _append_question(lines: list[str], package_dir: Path, qid: str) -> None:
    q_dir = package_dir / "questions" / qid
    if not q_dir.exists():
        return

    lines.append(f"## {qid}")
    lines.append("")

    _append_file_block(lines, q_dir / "question_context.json", f"{qid} - contexte")
    _append_file_block(lines, q_dir / "test_ledger.csv", f"{qid} - test ledger")
    _append_file_block(lines, q_dir / "comparison_hist_vs_scen.csv", f"{qid} - comparaison HIST vs SCEN")
    _append_file_block(lines, q_dir / "checks_filtered.csv", f"{qid} - checks filtrés")
    _append_file_block(lines, q_dir / "warnings_filtered.csv", f"{qid} - warnings filtrés")

    hist_tables = q_dir / "hist" / "tables"
    if hist_tables.exists():
        for f in sorted(hist_tables.glob("*.csv")):
            _append_file_block(lines, f, f"{qid} - historique - {f.name}")

    scen_root = q_dir / "scen"
    if scen_root.exists():
        for scen_dir in sorted([p for p in scen_root.iterdir() if p.is_dir()]):
            lines.append(f"### {qid} - scénario `{scen_dir.name}`")
            lines.append("")
            _append_file_block(lines, scen_dir / "checks_filtered.csv", f"{qid}/{scen_dir.name} - checks")
            _append_file_block(lines, scen_dir / "warnings_filtered.csv", f"{qid}/{scen_dir.name} - warnings")
            tables_dir = scen_dir / "tables"
            if tables_dir.exists():
                for f in sorted(tables_dir.glob("*.csv")):
                    _append_file_block(lines, f, f"{qid}/{scen_dir.name} - {f.name}")


def build_payload(package_dir: Path, output_file: Path) -> Path:
    manifest_path = package_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines: list[str] = []
    lines.append("# PAYLOAD LLM - Audit DE/ES")
    lines.append("")
    lines.append("Ce document est prêt à être copié-collé dans un autre LLM pour un audit rigoureux.")
    lines.append(f"Généré le: `{generated_at}`")
    lines.append(f"Package source: `{package_dir.relative_to(ROOT)}`")
    if manifest:
        lines.append(f"Run ID: `{manifest.get('run_id', '')}`")
        lines.append(f"Countries scope: `{', '.join(manifest.get('countries_scope', []))}`")
    lines.append("")
    lines.append("## Instructions pour l'autre LLM")
    lines.append("1. Lire les sections Méthode + Inputs avant les questions.")
    lines.append("2. Analyser Q1→Q5 en séparant HIST vs SCEN.")
    lines.append("3. Citer systématiquement `test_id` ou `table.colonne` pour chaque conclusion.")
    lines.append("4. Qualifier chaque conclusion: ROBUSTE / FRAGILE / NON_TESTABLE.")
    lines.append("5. Ne pas extrapoler au-delà des données ci-dessous.")
    lines.append("")

    _append_file_block(lines, ROOT / "AUDIT_METHODS_Q1_Q5.md", "Méthode d'audit (racine)")
    _append_file_block(lines, package_dir / "LLM_AUDIT_PROTOCOL.md", "Protocole d'audit LLM")
    _append_file_block(lines, package_dir / "manifest.json", "Manifest")
    _append_file_block(lines, package_dir / "file_index.csv", "Index des fichiers exportés")

    lines.append("## Inputs")
    lines.append("")
    _append_file_block(lines, package_dir / "inputs" / "test_registry.csv", "Registry des tests")
    _append_file_block(lines, package_dir / "inputs" / "phase1_assumptions.csv", "Hypothèses Phase 1")
    _append_file_block(lines, package_dir / "inputs" / "phase2_scenario_country_year.csv", "Hypothèses Phase 2 (DE/ES)")
    _append_file_block(lines, package_dir / "inputs" / "annual_metrics_hist.csv", "Métriques annuelles historiques (DE/ES)")
    _append_file_block(lines, package_dir / "inputs" / "annual_metrics_scenarios.csv", "Métriques annuelles prospectives (DE/ES)")
    _append_file_block(lines, package_dir / "inputs" / "validation_findings_hist.csv", "Validation findings historiques (DE/ES)")

    for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        _append_question(lines, package_dir, qid)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output_file


def main() -> int:
    args = _parse_args()
    if args.package_dir:
        package_dir = Path(args.package_dir)
        if not package_dir.is_absolute():
            package_dir = ROOT / package_dir
    else:
        package_dir = _latest_structured_package()

    if not package_dir.exists():
        raise FileNotFoundError(f"Package dir not found: {package_dir}")

    if args.output_file:
        output_file = Path(args.output_file)
        if not output_file.is_absolute():
            output_file = ROOT / output_file
    else:
        output_file = REPORTS_DIR / f"llm_paste_payload_{package_dir.name}.md"

    out = build_payload(package_dir=package_dir, output_file=output_file)
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

