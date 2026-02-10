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
    parser = argparse.ArgumentParser(description="Generate dense and traceable final report.")
    parser.add_argument("--run-id", type=str, default=None, help="Combined run id from outputs/combined/<run_id>.")
    parser.add_argument("--strict", action="store_true", help="Enable strict quality gates (fails on unmet criteria).")
    parser.add_argument(
        "--country-scope",
        type=str,
        default="",
        help="Comma-separated country list for report header (default from assumptions).",
    )
    parser.add_argument(
        "--docx-path",
        action="append",
        default=[],
        help="Additional docx path(s) for slides requirements extraction.",
    )
    parser.add_argument("--output-dir", type=str, default="reports", help="Output directory for report artifacts.")
    return parser.parse_args()


def _series_to_markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
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
            cells = [str(row.get(c, "")) for c in preview.columns]
            rows.append("| " + " | ".join(cells) + " |")
        return "\n".join([header, sep] + rows)


def _build_cover_page(
    run_id: str,
    run_dir: Path,
    countries: list[str],
    blocks: dict[str, Any],
) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    scenario_map: dict[str, list[str]] = {}
    for q in REQUIRED_QUESTIONS:
        block = blocks[q]
        scenario_map[q] = sorted([str(s) for s in block.summary.get("scenarios", [])])

    lines = [
        f"# Rapport Final V2.3 — Run `{run_id}`",
        "",
        "## 1. Page de garde",
        f"- Date de génération: `{generated_at}`",
        f"- Run combiné source: `{run_dir}`",
        f"- Périmètre pays déclaré: `{', '.join(countries) if countries else 'non renseigné'}`",
        "- Fenêtre historique de référence: `2018–2024`",
        "- Horizons prospectifs de référence: `2030/2040`",
        "- Questions couvertes: `Q1, Q2, Q3, Q4, Q5`",
        "- Avertissement méthodologique: ce rapport n'est pas un modèle d'équilibre complet, "
        "mais une analyse empirique et scénarisée, auditable et explicitement bornée.",
        "",
        "### Scénarios exécutés par question",
    ]
    for q in REQUIRED_QUESTIONS:
        lines.append(f"- `{q}`: {', '.join(scenario_map[q]) if scenario_map[q] else 'aucun scénario'}")
    return "\n".join(lines)


def _build_methodology_section() -> str:
    lines = [
        "## 2. Méthode et gouvernance",
        "",
        "### 2.1 Conventions et garde-fous (SPEC 0)",
        "- Index interne horaire en UTC, conventions de signe et unités harmonisées.",
        "- Classification physique des régimes sans utilisation du prix (anti-circularité).",
        "- Distinction stricte entre observations historiques et simulations prospectives.",
        "",
        "### 2.2 Observé vs simulé",
        "- Historique: données ENTSO-E, métriques et tests empiriques sur années observées.",
        "- Prospectif: mêmes métriques appliquées à des chroniques scénarisées, avec hypothèses explicites.",
        "",
        "### 2.3 Qualité des données et limites structurantes",
        "- Un résultat n'est jugé robuste que s'il ne contredit aucun FAIL et explicite tout WARN.",
        "- Tout NON_TESTABLE est conservé comme zone d'incertitude, jamais masqué.",
        "- Les conclusions sont formulées au niveau des preuves disponibles, sans extrapolation hors périmètre.",
    ]
    return "\n".join(lines)


def _build_question_sections(blocks: dict[str, Any], countries: list[str]) -> tuple[str, dict[str, dict[str, Any]]]:
    lines: list[str] = ["## 3. Analyses détaillées par question", ""]
    narrative_qc: dict[str, dict[str, Any]] = {}
    for q in REQUIRED_QUESTIONS:
        block = blocks[q]
        narrative = build_question_narrative(block, country_scope=countries)
        qc = narrative_quality_checks(narrative, block)
        narrative_qc[q] = qc
        lines.append(narrative.markdown.strip())
        lines.append("")
    return "\n".join(lines), narrative_qc


def _build_appendix_section(
    blocks: dict[str, Any],
    evidence_catalog: pd.DataFrame,
    checks_catalog: pd.DataFrame,
    test_traceability: pd.DataFrame,
    slides_traceability: pd.DataFrame,
) -> str:
    lines = [
        "## 4. Annexes de preuve et traçabilité",
        "",
        "### 4.1 Ledger complet des tests",
    ]
    for q in REQUIRED_QUESTIONS:
        lines.append(f"#### {q}")
        lines.append(_series_to_markdown_table(blocks[q].ledger, max_rows=80))
        lines.append("")

    lines.extend(
        [
            "### 4.2 Checks et warnings consolidés",
            _series_to_markdown_table(checks_catalog, max_rows=120),
            "",
            "### 4.3 Traçabilité tests -> sources",
            _series_to_markdown_table(test_traceability, max_rows=160),
            "",
            "### 4.4 Couverture Slides/SPECS -> preuves",
            _series_to_markdown_table(slides_traceability, max_rows=200),
            "",
            "### 4.5 Dictionnaire de preuves",
            _series_to_markdown_table(evidence_catalog, max_rows=200),
        ]
    )
    return "\n".join(lines)


def _build_executive_summary(
    run_id: str,
    narrative_qc: dict[str, dict[str, Any]],
    slides_traceability: pd.DataFrame,
    qc_verdict: str,
) -> str:
    missing_slides = int((slides_traceability["covered"].astype(str) == "no").sum()) if not slides_traceability.empty else 0
    lines = [
        f"# Executive Summary — Run `{run_id}`",
        "",
        f"Verdict qualité global: **{qc_verdict}**.",
        f"Exigences slides non couvertes: **{missing_slides}**.",
        "",
        "## Contrôles narratifs par question",
    ]
    for q in REQUIRED_QUESTIONS:
        qqc = narrative_qc.get(q, {})
        lines.append(
            f"- `{q}`: words={qqc.get('word_count', 0)} "
            f"(min={qqc.get('min_words_required', 0)}), "
            f"word_ok={qqc.get('word_count_ok', False)}, "
            f"all_test_refs={qqc.get('all_test_ids_referenced', False)}"
        )
    lines.append("")
    lines.append(
        "Ce résumé ne remplace pas le rapport détaillé; il sert à vérifier rapidement la complétude et la traçabilité."
    )
    return "\n".join(lines)


def _quality_checks(
    blocks: dict[str, Any],
    narrative_qc: dict[str, dict[str, Any]],
    slides_traceability: pd.DataFrame,
) -> dict[str, Any]:
    # 1) Numeric consistency: delta = scen - hist where finite.
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
            if pd.notna(h) and pd.notna(s) and pd.notna(d):
                if abs((s - h) - d) > 1e-6:
                    numeric_issues.append(
                        {
                            "question_id": q,
                            "metric": str(row.get("metric", "")),
                            "country": str(row.get("country", "")),
                            "scenario_id": str(row.get("scenario_id", "")),
                            "hist_value": h,
                            "scen_value": s,
                            "delta": d,
                            "expected_delta": s - h,
                        }
                    )

    # 2) Logic coherence: if FAIL in ledger, it must appear in checks/warnings context.
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
                logic_issues.append(
                    {"question_id": q, "issue": "FAIL ledger sans FAIL check consolidé", "n_fail": n_fail}
                )

    # 3) Narrative quality gates
    narrative_issues: list[dict[str, Any]] = []
    for q in REQUIRED_QUESTIONS:
        qqc = narrative_qc.get(q, {})
        if not qqc.get("word_count_ok", False):
            narrative_issues.append({"question_id": q, "issue": "densité insuffisante", **qqc})
        if not qqc.get("all_test_ids_referenced", False):
            narrative_issues.append({"question_id": q, "issue": "tests non référencés", **qqc})

    slide_missing = int((slides_traceability["covered"].astype(str) == "no").sum()) if not slides_traceability.empty else 0

    all_pass = not numeric_issues and not logic_issues and not narrative_issues and slide_missing == 0
    verdict = "PASS" if all_pass else "NON_COMPLET"
    return {
        "verdict": verdict,
        "numeric_issues": numeric_issues,
        "logic_issues": logic_issues,
        "narrative_issues": narrative_issues,
        "slides_missing_count": slide_missing,
        "all_pass": all_pass,
    }


def generate_report(
    run_id: str | None,
    strict: bool,
    country_scope: list[str],
    docx_paths: list[Path],
    output_dir: Path,
) -> ReportBuildResult:
    if strict and not run_id:
        raise ValueError("Strict mode requires --run-id to avoid accidental cross-run interpretation.")

    resolved_run_id, run_dir, blocks = load_combined_run(run_id=run_id, strict=True)

    output_dir.mkdir(parents=True, exist_ok=True)
    evidence_catalog = build_evidence_catalog(run_dir, blocks)
    test_traceability = build_test_traceability(run_dir, blocks)
    checks_catalog = build_checks_catalog(run_dir, blocks)

    requirements = extract_requirements(docx_paths)
    slides_traceability = map_requirements_to_evidence(requirements, evidence_catalog)

    cover = _build_cover_page(resolved_run_id, run_dir, country_scope, blocks)
    method = _build_methodology_section()
    question_sections, narrative_qc = _build_question_sections(blocks, country_scope)
    appendix = _build_appendix_section(blocks, evidence_catalog, checks_catalog, test_traceability, slides_traceability)

    qc = _quality_checks(blocks, narrative_qc, slides_traceability)
    verdict = qc["verdict"]

    if verdict != "PASS":
        gap_lines = ["## 5. Écarts restants (obligatoire)", ""]
        if qc["slides_missing_count"] > 0:
            gap_lines.append(f"- Couverture slides incomplète: `{qc['slides_missing_count']}` exigences non couvertes.")
        for issue in qc["numeric_issues"]:
            gap_lines.append(f"- Numeric issue: {issue}")
        for issue in qc["logic_issues"]:
            gap_lines.append(f"- Logic issue: {issue}")
        for issue in qc["narrative_issues"]:
            gap_lines.append(f"- Narrative issue: {issue.get('question_id')}: {issue.get('issue')}")
        gaps = "\n".join(gap_lines)
    else:
        gaps = "## 5. Écarts restants (obligatoire)\n\nAucun écart critique détecté par les quality gates.\n"

    detailed_text = "\n\n".join([cover, method, question_sections, appendix, gaps]).strip() + "\n"
    executive_text = _build_executive_summary(resolved_run_id, narrative_qc, slides_traceability, verdict)

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

    if strict and verdict != "PASS":
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
