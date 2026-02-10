"""Export a structured DE/ES-style analytical package from a combined run.

This script builds a country-filtered evidence pack designed for external LLM
audit (for example ChatGPT 5.2 Pro) with explicit traceability:
- run metadata
- methods and test registry snapshot
- assumptions and source tables
- question-by-question historical/prospective outputs
- filtered checks and comparison tables
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.modules.test_registry import all_tests
from src.reporting.evidence_loader import REQUIRED_QUESTIONS, load_combined_run


QUESTION_OBJECTIVES: dict[str, str] = {
    "Q1": "Identifier la bascule Phase 1 vers Phase 2 (marche et physique), puis expliquer les drivers SR/FAR/IR.",
    "Q2": "Mesurer la pente de cannibalisation (PV/Wind) et qualifier ses drivers et sa robustesse statistique.",
    "Q3": "Evaluer la sortie de Phase 2 et quantifier les conditions minimales d'inversion (demande/must-run/flex).",
    "Q4": "Quantifier l'impact batterie (systeme et actif) et estimer des ordres de grandeur de sizing.",
    "Q5": "Mesurer l'impact CO2/gaz sur l'ancre thermique (TCA/TTL) et calculer le CO2 requis pour une cible TTL.",
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export a structured country package from outputs/combined.")
    parser.add_argument("--run-id", type=str, default=None, help="Combined run id. If omitted, latest complete run is used.")
    parser.add_argument("--countries", type=str, default="DE,ES", help="Comma-separated country list (ex: DE,ES).")
    parser.add_argument("--output-dir", type=str, default="reports", help="Root output directory.")
    return parser.parse_args()


def _safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def _safe_read_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_parquet(path)
    except Exception:
        return pd.DataFrame()


def _safe_read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _country_filter(df: pd.DataFrame, countries: list[str]) -> pd.DataFrame:
    if df.empty:
        return df
    if "country" not in df.columns:
        return df.copy()
    return df[df["country"].astype(str).isin(countries)].copy()


def _country_mentions(message: str, known_countries: list[str]) -> list[str]:
    text = str(message or "")
    found: list[str] = []
    for c in known_countries:
        if re.search(rf"(^|[^A-Z_]){re.escape(c)}($|[^A-Z_])", text):
            found.append(c)
    return sorted(set(found))


def _extract_checks_filtered(
    summary: dict[str, Any],
    question_id: str,
    target_countries: list[str],
    known_countries: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    checks_df = pd.DataFrame(summary.get("checks", []))
    if checks_df.empty:
        checks_df = pd.DataFrame(columns=["status", "code", "message", "scope", "scenario_id"])
    checks_df["question_id"] = question_id
    checks_df["mentioned_countries"] = checks_df.get("message", pd.Series(dtype=str)).apply(
        lambda x: ",".join(_country_mentions(str(x), known_countries))
    )
    checks_df["is_global"] = checks_df["mentioned_countries"].eq("")

    def _keep(row: pd.Series) -> bool:
        mentions = [x for x in str(row.get("mentioned_countries", "")).split(",") if x]
        if not mentions:
            return True
        return any(c in target_countries for c in mentions)

    checks_filtered = checks_df[checks_df.apply(_keep, axis=1)].copy()

    warnings_rows = []
    for msg in summary.get("warnings", []):
        msg = str(msg)
        mentions = _country_mentions(msg, known_countries)
        if mentions and not any(c in target_countries for c in mentions):
            continue
        warnings_rows.append(
            {
                "question_id": question_id,
                "status": "WARN",
                "code": "QUESTION_WARNING",
                "message": msg,
                "scope": "GLOBAL",
                "scenario_id": "",
                "mentioned_countries": ",".join(mentions),
                "is_global": not bool(mentions),
            }
        )
    warnings_df = pd.DataFrame(warnings_rows)
    return checks_filtered, warnings_df


def _write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def _copy_tables_filtered(source_tables_dir: Path, target_tables_dir: Path, countries: list[str]) -> list[dict[str, Any]]:
    target_tables_dir.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    if not source_tables_dir.exists():
        return entries
    for csv_path in sorted(source_tables_dir.glob("*.csv")):
        df = _safe_read_csv(csv_path)
        filtered = _country_filter(df, countries)
        out_path = target_tables_dir / csv_path.name
        _write_csv(filtered, out_path)
        entries.append(
            {
                "source": str(csv_path),
                "target": str(out_path),
                "rows_source": int(len(df)),
                "rows_filtered": int(len(filtered)),
                "country_filtered": "country" in df.columns,
            }
        )
    return entries


def _build_readme(pack_dir: Path, run_id: str, countries: list[str]) -> None:
    text = f"""# Structured Analytical Package ({", ".join(countries)}) - {run_id}

This package is designed for external analytical review by another LLM.
It is intentionally structured to separate:
- historical evidence (HIST),
- prospective evidence (SCEN),
- comparison logic (HIST vs SCEN),
- assumptions and test definitions.

## Directory map
- `manifest.json`: run metadata, sources and generation timestamp.
- `inputs/`: assumptions, test registry and core data extracts.
- `questions/Q1..Q5/`: detailed question-by-question evidence.
- `questions/Qx/hist/`: historical tables and checks.
- `questions/Qx/scen/<scenario_id>/`: prospective tables and checks by scenario.
- `questions/Qx/comparison_hist_vs_scen.csv`: country-filtered comparison deltas.
- `questions/Qx/test_ledger.csv`: test execution ledger (question scope).
- `file_index.csv`: traceability index of exported files and row counts.

## Method reference
Use root file `AUDIT_METHODS_Q1_Q5.md` for formulas, assumptions, and calculation logic.
"""
    (pack_dir / "README.md").write_text(text, encoding="utf-8")


def _build_llm_protocol(pack_dir: Path, run_id: str, countries: list[str]) -> None:
    text = f"""# LLM Audit Protocol ({", ".join(countries)}) - {run_id}

Use this protocol to review analytical consistency country-by-country and question-by-question.

## 1) Global method and assumptions
- Open `AUDIT_METHODS_Q1_Q5.md` (root project reference).
- Open `inputs/phase1_assumptions.csv`.
- Open `inputs/phase2_scenario_country_year.csv`.
- Open `inputs/test_registry.csv`.

## 2) Data quality baseline for selected countries
- Open `inputs/annual_metrics_hist.csv`.
- Open `inputs/validation_findings_hist.csv`.
- Check completeness, quality_flag, regime_coherence, nrl_price_corr.

## 3) Per-question review sequence (Q1 -> Q5)
For each `questions/Qx`:
1. Read `question_context.json` (objective, source refs, filterability notes).
2. Read `test_ledger.csv` (what each test checks, source_ref, status).
3. Read `hist/tables/*.csv` (historical outputs).
4. Read `scen/<scenario>/tables/*.csv` for each scenario.
5. Read `comparison_hist_vs_scen.csv` (delta and interpretability_status).
6. Read `checks_filtered.csv` + `warnings_filtered.csv`.

### Q1 additional mandatory tables
- `hist/tables/Q1_scope_audit.csv`
- `hist/tables/Q1_ir_diagnostics.csv`
- `hist/tables/Q1_rule_definition.csv`
- `hist/tables/Q1_before_after_bascule.csv`

## 4) Robustness rubric
- Robust: status PASS and interpretable deltas with non-null denominators.
- Fragile: WARN or low statistical strength (`n`, `p_value`, `r2`) or low coherence.
- Non-testable: explicit `NON_TESTABLE` or out-of-scope status (for example `hors_scope_stage2`).

## 5) Reporting rules for external reviewer
- No conclusion without numeric evidence (`test_id` or `table.column`).
- Distinguish historical fact vs prospective stress-test output.
- Explicitly document limits and non-testable zones.
"""
    (pack_dir / "LLM_AUDIT_PROTOCOL.md").write_text(text, encoding="utf-8")


def export_package(run_id: str | None, countries: list[str], output_dir: Path) -> Path:
    resolved_run_id, run_dir, blocks = load_combined_run(run_id=run_id, strict=True)
    countries = sorted({str(c).strip() for c in countries if str(c).strip()})
    if not countries:
        raise ValueError("No target countries supplied.")

    pack_name = f"chatgpt52_structured_{resolved_run_id}_{'_'.join(countries)}"
    pack_dir = output_dir / pack_name
    pack_dir.mkdir(parents=True, exist_ok=True)

    _build_readme(pack_dir, resolved_run_id, countries)
    _build_llm_protocol(pack_dir, resolved_run_id, countries)

    file_index_rows: list[dict[str, Any]] = []

    # Manifest
    manifest = {
        "package_name": pack_name,
        "run_id": resolved_run_id,
        "run_dir": str(run_dir),
        "countries_scope": countries,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "questions": list(REQUIRED_QUESTIONS),
        "method_reference_file": "AUDIT_METHODS_Q1_Q5.md",
    }
    (pack_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # Inputs: assumptions and registry
    inputs_dir = pack_dir / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)

    phase1 = _safe_read_csv(Path("data/assumptions/phase1_assumptions.csv"))
    _write_csv(phase1, inputs_dir / "phase1_assumptions.csv")
    file_index_rows.append(
        {"category": "inputs", "file": str(inputs_dir / "phase1_assumptions.csv"), "rows": int(len(phase1))}
    )

    phase2 = _safe_read_csv(Path("data/assumptions/phase2/phase2_scenario_country_year.csv"))
    phase2_scope = _country_filter(phase2, countries)
    _write_csv(phase2_scope, inputs_dir / "phase2_scenario_country_year.csv")
    file_index_rows.append(
        {"category": "inputs", "file": str(inputs_dir / "phase2_scenario_country_year.csv"), "rows": int(len(phase2_scope))}
    )

    annual_hist = _safe_read_parquet(Path("data/metrics/annual_metrics.parquet"))
    annual_hist_scope = _country_filter(annual_hist, countries)
    _write_csv(annual_hist_scope, inputs_dir / "annual_metrics_hist.csv")
    file_index_rows.append(
        {"category": "inputs", "file": str(inputs_dir / "annual_metrics_hist.csv"), "rows": int(len(annual_hist_scope))}
    )

    val_hist = _safe_read_parquet(Path("data/metrics/validation_findings.parquet"))
    val_hist_scope = _country_filter(val_hist, countries)
    _write_csv(val_hist_scope, inputs_dir / "validation_findings_hist.csv")
    file_index_rows.append(
        {"category": "inputs", "file": str(inputs_dir / "validation_findings_hist.csv"), "rows": int(len(val_hist_scope))}
    )

    # Scenario-level annual metrics per available scenario folder.
    scen_root = Path("data/processed/scenario")
    scen_rows: list[pd.DataFrame] = []
    if scen_root.exists():
        for scen_dir in sorted([p for p in scen_root.iterdir() if p.is_dir()]):
            annual_path = scen_dir / "annual_metrics.parquet"
            a = _safe_read_parquet(annual_path)
            if a.empty:
                continue
            a = _country_filter(a, countries)
            if a.empty:
                continue
            a["scenario_id"] = scen_dir.name
            scen_rows.append(a)
    scen_all = pd.concat(scen_rows, ignore_index=True) if scen_rows else pd.DataFrame()
    _write_csv(scen_all, inputs_dir / "annual_metrics_scenarios.csv")
    file_index_rows.append(
        {"category": "inputs", "file": str(inputs_dir / "annual_metrics_scenarios.csv"), "rows": int(len(scen_all))}
    )

    registry = pd.DataFrame([t.to_dict() for t in all_tests()])
    _write_csv(registry, inputs_dir / "test_registry.csv")
    file_index_rows.append({"category": "inputs", "file": str(inputs_dir / "test_registry.csv"), "rows": int(len(registry))})

    # Questions
    questions_dir = pack_dir / "questions"
    questions_dir.mkdir(parents=True, exist_ok=True)

    for q in REQUIRED_QUESTIONS:
        q_dir = questions_dir / q
        q_dir.mkdir(parents=True, exist_ok=True)

        summary_path = run_dir / q / "summary.json"
        test_ledger_path = run_dir / q / "test_ledger.csv"
        comparison_path = run_dir / q / "comparison_hist_vs_scen.csv"

        summary = _safe_read_json(summary_path)
        known_countries = [str(c) for c in summary.get("selection", {}).get("countries", [])]
        if not known_countries:
            known_countries = countries

        checks_filtered, warnings_df = _extract_checks_filtered(
            summary=summary,
            question_id=q,
            target_countries=countries,
            known_countries=known_countries,
        )
        _write_csv(checks_filtered, q_dir / "checks_filtered.csv")
        _write_csv(warnings_df, q_dir / "warnings_filtered.csv")
        file_index_rows.append({"category": q, "file": str(q_dir / "checks_filtered.csv"), "rows": int(len(checks_filtered))})
        file_index_rows.append({"category": q, "file": str(q_dir / "warnings_filtered.csv"), "rows": int(len(warnings_df))})

        test_ledger = _safe_read_csv(test_ledger_path)
        _write_csv(test_ledger, q_dir / "test_ledger.csv")
        file_index_rows.append({"category": q, "file": str(q_dir / "test_ledger.csv"), "rows": int(len(test_ledger))})

        comparison = _safe_read_csv(comparison_path)
        comparison_scope = _country_filter(comparison, countries)
        _write_csv(comparison_scope, q_dir / "comparison_hist_vs_scen.csv")
        file_index_rows.append(
            {"category": q, "file": str(q_dir / "comparison_hist_vs_scen.csv"), "rows": int(len(comparison_scope))}
        )

        # HIST tables
        hist_tables_src = run_dir / q / "hist" / "tables"
        hist_tables_dst = q_dir / "hist" / "tables"
        hist_entries = _copy_tables_filtered(hist_tables_src, hist_tables_dst, countries)
        for e in hist_entries:
            file_index_rows.append({"category": q, "file": e["target"], "rows": e["rows_filtered"]})
        hist_unfilterable = [Path(e["source"]).name for e in hist_entries if not e.get("country_filtered", False)]

        # SCEN tables
        scen_src_root = run_dir / q / "scen"
        scen_unfilterable: dict[str, list[str]] = {}
        if scen_src_root.exists():
            for scen_dir in sorted([p for p in scen_src_root.iterdir() if p.is_dir()]):
                scen_tables_src = scen_dir / "tables"
                scen_tables_dst = q_dir / "scen" / scen_dir.name / "tables"
                scen_entries = _copy_tables_filtered(scen_tables_src, scen_tables_dst, countries)
                for e in scen_entries:
                    file_index_rows.append({"category": q, "file": e["target"], "rows": e["rows_filtered"]})
                scen_unfilterable[scen_dir.name] = [
                    Path(e["source"]).name for e in scen_entries if not e.get("country_filtered", False)
                ]

                scen_summary = _safe_read_json(scen_dir / "summary.json")
                scen_checks, scen_warn = _extract_checks_filtered(
                    summary=scen_summary,
                    question_id=q,
                    target_countries=countries,
                    known_countries=known_countries,
                )
                _write_csv(scen_checks, q_dir / "scen" / scen_dir.name / "checks_filtered.csv")
                _write_csv(scen_warn, q_dir / "scen" / scen_dir.name / "warnings_filtered.csv")
                file_index_rows.append(
                    {
                        "category": q,
                        "file": str(q_dir / "scen" / scen_dir.name / "checks_filtered.csv"),
                        "rows": int(len(scen_checks)),
                    }
                )

        question_context = {
            "question_id": q,
            "objective": QUESTION_OBJECTIVES.get(q, ""),
            "countries_scope": countries,
            "run_id": resolved_run_id,
            "source_summary_file": str(summary_path),
            "source_refs_in_ledger": sorted(set(test_ledger.get("source_ref", pd.Series(dtype=str)).astype(str).tolist()))
            if not test_ledger.empty
            else [],
            "scenarios": sorted([str(s) for s in summary.get("scenarios", [])]),
            "country_filter_notes": {
                "hist_unfilterable_tables": hist_unfilterable,
                "scen_unfilterable_tables_by_scenario": scen_unfilterable,
            },
        }
        (q_dir / "question_context.json").write_text(
            json.dumps(question_context, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    file_index = pd.DataFrame(file_index_rows)
    _write_csv(file_index, pack_dir / "file_index.csv")

    return pack_dir


def main() -> int:
    args = _parse_args()
    countries = [c.strip() for c in str(args.countries).split(",")]
    out_dir = Path(args.output_dir)
    pack_dir = export_package(run_id=args.run_id, countries=countries, output_dir=out_dir)
    print(str(pack_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
