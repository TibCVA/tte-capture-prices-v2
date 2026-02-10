from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.reporting.evidence_loader import (
    REQUIRED_QUESTIONS,
    build_checks_catalog,
    build_evidence_catalog,
    build_test_traceability,
    load_combined_run,
)
from src.reporting.interpretation_rules import build_question_narrative, narrative_quality_checks
from src.reporting.report_schema import ReportBuildResult
from src.reporting.slides_requirements import extract_requirements, map_requirements_to_evidence


DEFAULT_DOCX_PATHS = [
    Path(r"C:\Users\cval-tlacour\OneDrive - CVA corporate value associate GmbH\Desktop\TTE Capture prices\Slides content 1.docx"),
    Path(r"C:\Users\cval-tlacour\OneDrive - CVA corporate value associate GmbH\Desktop\TTE Capture prices\Slides content 2.docx"),
]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate detailed and traceable final report.")
    parser.add_argument("--run-id", type=str, default=None, help="Combined run id from outputs/combined/<run_id>.")
    parser.add_argument("--strict", action="store_true", help="Enable strict quality gates.")
    parser.add_argument("--country-scope", type=str, default="", help="Comma-separated country list for report header.")
    parser.add_argument("--docx-path", action="append", default=[], help="Additional docx path(s) for slide requirement extraction.")
    parser.add_argument("--output-dir", type=str, default="reports", help="Output directory.")
    return parser.parse_args()


def _table_md(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df.empty:
        return "_Aucune ligne._"
    preview = df.head(max_rows).copy()
    try:
        return preview.to_markdown(index=False)
    except Exception:
        cols = [str(c) for c in preview.columns]
        header = "| " + " | ".join(cols) + " |"
        sep = "| " + " | ".join(["---"] * len(cols)) + " |"
        rows: list[str] = []
        for _, row in preview.iterrows():
            rows.append("| " + " | ".join([str(row.get(c, "")) for c in preview.columns]) + " |")
        return "\n".join([header, sep] + rows)


def _cover_page(run_id: str, run_dir: Path, countries: list[str], blocks: dict[str, Any]) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        f"# Rapport Final V2.3 - Run `{run_id}`",
        "",
        "## 1. Page de garde",
        f"- Date de generation: `{generated_at}`",
        f"- Run combine source: `{run_dir}`",
        f"- Perimetre pays declare: `{', '.join(countries) if countries else 'non renseigne'}`",
        "- Fenetre historique de reference: `2018-2024`",
        "- Horizons prospectifs de reference: `2030/2040`",
        "- Questions couvertes: `Q1, Q2, Q3, Q4, Q5`",
        "- Avertissement methodologique: cette analyse est empirique et scenarisee; ce n'est pas un modele d'equilibre complet.",
        "",
        "### Scenarios executes par question",
    ]
    for q in REQUIRED_QUESTIONS:
        scenarios = sorted([str(s) for s in blocks[q].summary.get("scenarios", [])])
        lines.append(f"- `{q}`: {', '.join(scenarios) if scenarios else 'aucun scenario'}")
    return "\n".join(lines)


def _methodology_section() -> str:
    return "\n".join(
        [
            "## 2. Methode et gouvernance",
            "",
            "### 2.1 Conventions SPEC 0",
            "- Index horaire UTC et conventions de signe harmonisees.",
            "- Regimes physiques A/B/C/D definis sans prix (anti-circularite).",
            "- Distinction stricte entre observe (HIST) et simule (SCEN).",
            "",
            "### 2.2 Qualite des donnees",
            "- Les hard checks invalident une conclusion en cas de FAIL.",
            "- Les WARN sont conserves et interpretes explicitement.",
            "- Les NON_TESTABLE restent visibles et ne sont jamais masques.",
            "",
            "### 2.3 Cadre d'interpretation",
            "- Une correlation est un signal explicatif, pas une preuve causale automatique.",
            "- Toute conclusion est bornee au perimetre pays/periode/scenario execute.",
        ]
    )


def _question_sections(blocks: dict[str, Any], countries: list[str]) -> tuple[str, dict[str, dict[str, Any]]]:
    lines: list[str] = ["## 3. Analyses detaillees par question", ""]
    narrative_qc: dict[str, dict[str, Any]] = {}

    for q in REQUIRED_QUESTIONS:
        narrative = build_question_narrative(blocks[q], country_scope=countries)
        qc = narrative_quality_checks(narrative, blocks[q])
        narrative_qc[q] = qc
        lines.append(narrative.markdown.strip())
        lines.append("")

    return "\n".join(lines), narrative_qc


def _appendix_section(
    blocks: dict[str, Any],
    evidence_catalog: pd.DataFrame,
    checks_catalog: pd.DataFrame,
    test_traceability: pd.DataFrame,
    slides_traceability: pd.DataFrame,
) -> str:
    lines = [
        "## 4. Annexes de preuve et tracabilite",
        "",
        "### 4.1 Ledger complet des tests",
    ]

    for q in REQUIRED_QUESTIONS:
        lines.append(f"#### {q}")
        lines.append(_table_md(blocks[q].ledger, max_rows=200))
        lines.append("")

    lines.extend(
        [
            "### 4.2 Checks et warnings consolides",
            _table_md(checks_catalog, max_rows=250),
            "",
            "### 4.3 Tracabilite tests -> sources",
            _table_md(test_traceability, max_rows=250),
            "",
            "### 4.4 Couverture Slides/SPECS -> preuves",
            _table_md(slides_traceability, max_rows=400),
            "",
            "### 4.5 Catalogue de preuves",
            _table_md(evidence_catalog, max_rows=400),
        ]
    )

    return "\n".join(lines)


def _executive_summary(run_id: str, narrative_qc: dict[str, dict[str, Any]], qc: dict[str, Any]) -> str:
    lines = [
        f"# Executive Summary - Run `{run_id}`",
        "",
        f"Verdict qualite global: **{qc.get('verdict', 'NON_COMPLET')}**.",
        f"Slides - docx fournis/existants: **{qc.get('slides_docx_provided_count', 0)}/{qc.get('slides_docx_existing_count', 0)}**.",
        f"Slides - exigences extraites: **{qc.get('slides_requirements_count', 0)}**.",
        f"Slides - lignes de tracabilite: **{qc.get('slides_trace_rows', 0)}**.",
        f"Slides - couvertes oui/non: **{qc.get('slides_covered_yes', 0)}/{qc.get('slides_covered_no', 0)}**.",
        "",
        "## Controles narratifs par question",
    ]

    for q in REQUIRED_QUESTIONS:
        qqc = narrative_qc.get(q, {})
        lines.append(
            f"- `{q}`: words={qqc.get('word_count', 0)} / min={qqc.get('min_words_required', 0)}, "
            f"word_ok={qqc.get('word_count_ok', False)}, all_test_refs={qqc.get('all_test_ids_referenced', False)}"
        )

    lines.append("")
    lines.append("Le detail complet (preuves, tests, limites, interpretation) se trouve dans le rapport detaille.")
    return "\n".join(lines)


def _quality_checks(
    blocks: dict[str, Any],
    narrative_qc: dict[str, dict[str, Any]],
    slides_traceability: pd.DataFrame,
    requirements_count: int,
    slides_docx_provided_count: int,
    slides_docx_existing_count: int,
) -> dict[str, Any]:
    numeric_issues: list[dict[str, Any]] = []
    for q in REQUIRED_QUESTIONS:
        cmp_df = blocks[q].comparison
        if cmp_df.empty:
            continue
        for _, row in cmp_df.iterrows():
            try:
                h = float(row.get("hist_value"))
                s = float(row.get("scen_value"))
                d = float(row.get("delta"))
            except Exception:
                continue
            if pd.notna(h) and pd.notna(s) and pd.notna(d) and abs((s - h) - d) > 1e-6:
                numeric_issues.append(
                    {
                        "question_id": q,
                        "metric": str(row.get("metric", "")),
                        "hist": h,
                        "scen": s,
                        "delta": d,
                    }
                )

    logic_issues: list[dict[str, Any]] = []
    for q in REQUIRED_QUESTIONS:
        ledger = blocks[q].ledger
        if ledger.empty:
            logic_issues.append({"question_id": q, "issue": "ledger vide"})
            continue
        n_fail = int((ledger["status"].astype(str) == "FAIL").sum())
        if n_fail > 0:
            checks_df = blocks[q].checks
            has_fail_check = False
            if not checks_df.empty and "status" in checks_df.columns:
                has_fail_check = (checks_df["status"].astype(str).str.upper() == "FAIL").any()
            if not has_fail_check:
                logic_issues.append({"question_id": q, "issue": "FAIL ledger sans FAIL check consolide", "n_fail": n_fail})

    narrative_issues: list[dict[str, Any]] = []
    for q in REQUIRED_QUESTIONS:
        qqc = narrative_qc.get(q, {})
        if not qqc.get("word_count_ok", False):
            narrative_issues.append({"question_id": q, "issue": "densite insuffisante", **qqc})
        if not qqc.get("all_test_ids_referenced", False):
            narrative_issues.append({"question_id": q, "issue": "tests non references", **qqc})

    slides_trace_rows = int(len(slides_traceability))
    slides_covered_no = int((slides_traceability["covered"].astype(str) == "no").sum()) if not slides_traceability.empty else 0
    slides_covered_yes = int((slides_traceability["covered"].astype(str) == "yes").sum()) if not slides_traceability.empty else 0

    slides_extraction_empty_with_docs = bool(slides_docx_existing_count > 0 and int(requirements_count) == 0)
    slides_trace_empty = bool(int(requirements_count) > 0 and slides_trace_rows == 0)

    if slides_docx_provided_count > 0 and slides_docx_existing_count == 0:
        logic_issues.append(
            {
                "question_id": "GLOBAL",
                "issue": "aucun docx de slides fourni n'existe sur disque",
                "slides_docx_provided_count": slides_docx_provided_count,
            }
        )
    if slides_extraction_empty_with_docs:
        logic_issues.append(
            {
                "question_id": "GLOBAL",
                "issue": "extraction slides vide alors que des docx valides existent",
                "slides_docx_existing_count": slides_docx_existing_count,
            }
        )
    if slides_trace_empty:
        logic_issues.append(
            {
                "question_id": "GLOBAL",
                "issue": "slides_traceability vide alors que des exigences slides existent",
                "slides_requirements_count": int(requirements_count),
            }
        )
    if int(requirements_count) > 0 and slides_trace_rows != int(requirements_count):
        logic_issues.append(
            {
                "question_id": "GLOBAL",
                "issue": "nombre de lignes slides_traceability different du nombre d'exigences extraites",
                "slides_requirements_count": int(requirements_count),
                "slides_trace_rows": slides_trace_rows,
            }
        )

    all_pass = (
        not numeric_issues
        and not logic_issues
        and not narrative_issues
        and slides_covered_no == 0
        and not slides_extraction_empty_with_docs
        and not slides_trace_empty
    )
    return {
        "verdict": "PASS" if all_pass else "NON_COMPLET",
        "numeric_issues": numeric_issues,
        "logic_issues": logic_issues,
        "narrative_issues": narrative_issues,
        "slides_missing_count": slides_covered_no,
        "slides_docx_provided_count": int(slides_docx_provided_count),
        "slides_docx_existing_count": int(slides_docx_existing_count),
        "slides_requirements_count": int(requirements_count),
        "slides_trace_rows": slides_trace_rows,
        "slides_covered_yes": slides_covered_yes,
        "slides_covered_no": slides_covered_no,
        "slides_extraction_empty_with_docs": slides_extraction_empty_with_docs,
        "slides_trace_empty": slides_trace_empty,
        "all_pass": all_pass,
    }


def generate_report(run_id: str | None, strict: bool, country_scope: list[str], docx_paths: list[Path], output_dir: Path) -> ReportBuildResult:
    if strict and not run_id:
        raise ValueError("Strict mode requires --run-id to avoid accidental cross-run interpretation.")

    resolved_run_id, run_dir, blocks = load_combined_run(run_id=run_id, strict=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    evidence_catalog = build_evidence_catalog(run_dir, blocks)
    test_traceability = build_test_traceability(run_dir, blocks)
    checks_catalog = build_checks_catalog(run_dir, blocks)

    docx_paths = [Path(p) for p in docx_paths]
    existing_docx = [p for p in docx_paths if p.exists()]
    requirements = extract_requirements(existing_docx)
    slides_traceability = map_requirements_to_evidence(requirements, evidence_catalog)

    cover = _cover_page(resolved_run_id, run_dir, country_scope, blocks)
    method = _methodology_section()
    question_sections, narrative_qc = _question_sections(blocks, country_scope)
    appendix = _appendix_section(blocks, evidence_catalog, checks_catalog, test_traceability, slides_traceability)
    qc = _quality_checks(
        blocks,
        narrative_qc,
        slides_traceability,
        requirements_count=int(len(requirements)),
        slides_docx_provided_count=int(len(docx_paths)),
        slides_docx_existing_count=int(len(existing_docx)),
    )

    if qc["verdict"] != "PASS":
        gap_lines = ["## 5. Ecarts restants (obligatoire)", ""]
        if qc["slides_missing_count"] > 0:
            gap_lines.append(f"- Couverture slides incomplete: `{qc['slides_missing_count']}` exigence(s) non couverte(s).")
        for issue in qc["numeric_issues"]:
            gap_lines.append(f"- Numeric issue: {issue}")
        for issue in qc["logic_issues"]:
            gap_lines.append(f"- Logic issue: {issue}")
        for issue in qc["narrative_issues"]:
            gap_lines.append(f"- Narrative issue: {issue.get('question_id')}: {issue.get('issue')}")
        gaps = "\n".join(gap_lines)
    else:
        gaps = "## 5. Ecarts restants (obligatoire)\n\nAucun ecart critique detecte par les quality gates.\n"

    detailed_text = "\n\n".join([cover, method, question_sections, appendix, gaps]).strip() + "\n"
    executive_text = _executive_summary(resolved_run_id, narrative_qc, qc)

    detailed_path = output_dir / f"conclusions_v2_detailed_{resolved_run_id}.md"
    executive_path = output_dir / f"conclusions_v2_executive_{resolved_run_id}.md"
    evidence_path = output_dir / f"evidence_catalog_{resolved_run_id}.csv"
    traceability_path = output_dir / f"test_traceability_{resolved_run_id}.csv"
    slides_trace_path = output_dir / f"slides_traceability_{resolved_run_id}.csv"
    qc_path = output_dir / f"report_qc_{resolved_run_id}.json"

    detailed_path.write_text(detailed_text, encoding="utf-8")
    executive_path.write_text(executive_text, encoding="utf-8")
    evidence_catalog.to_csv(evidence_path, index=False)
    test_traceability.to_csv(traceability_path, index=False)
    slides_traceability.to_csv(slides_trace_path, index=False)
    qc_path.write_text(json.dumps(qc, ensure_ascii=False, indent=2), encoding="utf-8")

    if strict and qc["verdict"] != "PASS":
        raise RuntimeError(f"Strict report quality gate failed for run {resolved_run_id}. See {qc_path}.")

    return ReportBuildResult(
        run_id=resolved_run_id,
        detailed_report_path=detailed_path,
        executive_report_path=executive_path,
        evidence_catalog_path=evidence_path,
        test_traceability_path=traceability_path,
        slides_traceability_path=slides_trace_path,
        qc_path=qc_path,
        qc=qc,
    )


def main() -> None:
    args = _parse_args()
    output_dir = Path(args.output_dir)
    country_scope = [c.strip() for c in str(args.country_scope).split(",") if c.strip()]
    docx_paths = [Path(p) for p in args.docx_path] if args.docx_path else []
    if not docx_paths:
        docx_paths = DEFAULT_DOCX_PATHS

    result = generate_report(
        run_id=args.run_id,
        strict=bool(args.strict),
        country_scope=country_scope,
        docx_paths=docx_paths,
        output_dir=output_dir,
    )

    print("RUN_ID", result.run_id)
    print("REPORT_DETAILED", result.detailed_report_path)
    print("REPORT_EXECUTIVE", result.executive_report_path)
    print("EVIDENCE_CATALOG", result.evidence_catalog_path)
    print("TEST_TRACEABILITY", result.test_traceability_path)
    print("SLIDES_TRACEABILITY", result.slides_traceability_path)
    print("REPORT_QC", result.qc_path)
    print("VERDICT", result.qc.get("verdict"))


if __name__ == "__main__":
    main()
