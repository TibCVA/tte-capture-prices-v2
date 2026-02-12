from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import json
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.modules.test_registry import all_tests
from src.reporting.evidence_loader import load_combined_run


DEFAULT_COUNTRIES = ["FR", "DE", "ES", "NL", "BE", "CZ", "IT_NORD"]
DEFAULT_SCENARIOS = ["BASE", "DEMAND_UP", "LOW_RIGIDITY", "HIGH_CO2", "HIGH_GAS"]


@dataclass
class RequirementRow:
    requirement_id: str
    source_spec: str
    module_area: str
    status: str
    evidence_type: str
    evidence_ref: str
    severity: str

    def to_dict(self) -> dict[str, str]:
        return {
            "requirement_id": self.requirement_id,
            "source_spec": self.source_spec,
            "module_area": self.module_area,
            "status": self.status,
            "evidence_type": self.evidence_type,
            "evidence_ref": self.evidence_ref,
            "severity": self.severity,
        }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run integral compliance audit and emit traceable artifacts.")
    parser.add_argument("--run-id", required=True, help="Combined run id under outputs/combined/<run_id>")
    parser.add_argument("--reports-dir", default="reports", help="Output reports directory")
    parser.add_argument("--annual-hist-path", default="data/metrics/annual_metrics.parquet")
    parser.add_argument("--scenario-root", default="data/processed/scenario")
    parser.add_argument("--phase2-assumptions-path", default="data/assumptions/phase2/phase2_scenario_country_year.csv")
    parser.add_argument("--countries", default=",".join(DEFAULT_COUNTRIES))
    return parser.parse_args()


def _status_from_ledger_rows(df: pd.DataFrame) -> str:
    if df.empty:
        return "MANQUANT"
    statuses = set(df["status"].astype(str).str.upper().tolist())
    if "FAIL" in statuses:
        return "MANQUANT"
    if statuses.issubset({"NON_TESTABLE"}):
        return "PARTIEL"
    if "WARN" in statuses or "NON_TESTABLE" in statuses:
        return "PARTIEL"
    return "OK"


def _severity_norm(v: str) -> str:
    s = str(v).upper()
    if s in {"CRITICAL", "HIGH", "MEDIUM", "LOW"}:
        return s
    return "MEDIUM"


def _load_report_qc(reports_dir: Path, run_id: str) -> dict:
    qc_path = reports_dir / f"report_qc_{run_id}.json"
    if not qc_path.exists():
        return {}
    try:
        return json.loads(qc_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _load_slides_trace(reports_dir: Path, run_id: str) -> pd.DataFrame:
    p = reports_dir / f"slides_traceability_{run_id}.csv"
    if not p.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(p)
    except Exception:
        return pd.DataFrame()


def _scenario_coverage(
    scenario_root: Path,
    scenario_id: str,
    countries: list[str],
    phase2_assumptions: pd.DataFrame | None = None,
) -> tuple[str, str]:
    p = scenario_root / scenario_id / "annual_metrics.parquet"
    if not p.exists():
        return "MANQUANT", f"{p} absent"
    df = pd.read_parquet(p)
    if df.empty:
        return "MANQUANT", f"{p} vide"
    scoped = df[df["country"].astype(str).isin(countries)].copy()
    expected_rows = np.nan
    if phase2_assumptions is not None and not phase2_assumptions.empty:
        p2 = phase2_assumptions.copy()
        if {"scenario_id", "country", "year"}.issubset(set(p2.columns)):
            expected_rows = float(
                len(
                    p2[
                        (p2["scenario_id"].astype(str) == str(scenario_id))
                        & (p2["country"].astype(str).isin(countries))
                    ]
                )
            )
    if not np.isfinite(expected_rows) or expected_rows <= 0:
        scenario_years = (
            pd.to_numeric(scoped.get("year", pd.Series(dtype=float)), errors="coerce")
            .dropna()
            .astype(int)
            .nunique()
        )
        expected_rows = float(len(countries) * max(1, int(scenario_years)))

    expected_rows_i = int(expected_rows)
    n_rows = int(len(scoped))
    n_neg = int((pd.to_numeric(scoped.get("h_negative", np.nan), errors="coerce") > 0).sum())
    n_a = int((pd.to_numeric(scoped.get("h_regime_a", np.nan), errors="coerce") > 0).sum())
    if n_rows < expected_rows_i:
        return "PARTIEL", f"rows={n_rows}/{expected_rows_i}"
    if n_neg == 0 and n_a == 0:
        return "PARTIEL", f"rows={n_rows}/{expected_rows_i}; h_negative>0={n_neg}; h_regime_a>0={n_a}"
    return "OK", f"rows={n_rows}/{expected_rows_i}; h_negative>0={n_neg}; h_regime_a>0={n_a}"


def _q3_informativeness(run_dir: Path) -> tuple[str, str]:
    p = run_dir / "Q3" / "comparison_hist_vs_scen.csv"
    if not p.exists():
        return "MANQUANT", "comparison Q3 absente"
    df = pd.read_csv(p)
    if df.empty:
        return "PARTIEL", "comparison Q3 vide"
    if "interpretability_status" not in df.columns:
        return "PARTIEL", "colonne interpretability_status absente"
    share_info = float((df["interpretability_status"].astype(str) == "INFORMATIVE").mean())
    if share_info >= 0.30:
        return "OK", f"share_informative={share_info:.2%}"
    if share_info > 0:
        return "PARTIEL", f"share_informative={share_info:.2%}"
    return "PARTIEL", f"share_informative={share_info:.2%}"


def run_audit(
    run_id: str,
    reports_dir: Path,
    annual_hist_path: Path,
    scenario_root: Path,
    countries: list[str],
    phase2_assumptions_path: Path,
) -> dict:
    _, run_dir, blocks = load_combined_run(run_id=run_id, strict=True)
    annual_hist = pd.read_parquet(annual_hist_path) if annual_hist_path.exists() else pd.DataFrame()
    phase2_assumptions = pd.read_csv(phase2_assumptions_path) if phase2_assumptions_path.exists() else pd.DataFrame()
    qc = _load_report_qc(reports_dir, run_id)
    slides_trace = _load_slides_trace(reports_dir, run_id)

    rows: list[RequirementRow] = []

    # Atomic registry requirements (SPEC/Slides mapped tests)
    tests = all_tests()
    for spec in tests:
        block = blocks.get(spec.question_id)
        led = block.ledger if block is not None else pd.DataFrame()
        if not led.empty:
            led = led[led["test_id"].astype(str) == spec.test_id].copy()
        status = _status_from_ledger_rows(led)
        if led.empty:
            evidence_ref = f"{spec.question_id}:test_id={spec.test_id} absent"
        else:
            status_counts = led["status"].astype(str).value_counts().to_dict()
            evidence_ref = f"{spec.question_id}:{spec.test_id}:{status_counts}"
        rows.append(
            RequirementRow(
                requirement_id=f"TEST_{spec.test_id}",
                source_spec=spec.source_ref,
                module_area=spec.question_id,
                status=status,
                evidence_type="test",
                evidence_ref=evidence_ref,
                severity=_severity_norm(spec.severity_if_fail),
            )
        )

    # Semantic compliance: metric_rule text and implemented behavior for Q1-S-02.
    q1_s02_specs = [s for s in tests if s.test_id == "Q1-S-02"]
    q1_s02_spec = q1_s02_specs[0] if q1_s02_specs else None
    q1_block = blocks.get("Q1")
    q1_ledger = q1_block.ledger.copy() if q1_block is not None else pd.DataFrame()
    q1_s02_rows = q1_ledger[q1_ledger.get("test_id", pd.Series(dtype=str)).astype(str) == "Q1-S-02"].copy() if not q1_ledger.empty else pd.DataFrame()
    metric_rule_ok = bool(q1_s02_spec is not None and "BASE" in str(q1_s02_spec.metric_rule).upper())
    behavior_ok = False
    if not q1_s02_rows.empty:
        values = q1_s02_rows.get("value", pd.Series(dtype=str)).astype(str).str.lower()
        behavior_ok = bool(values.str.contains("finite_share=").any() and values.str.contains("nonzero_share=").any())
    q1_s02_status = "OK" if metric_rule_ok and behavior_ok else "PARTIEL"
    q1_s02_evidence = (
        f"metric_rule={getattr(q1_s02_spec, 'metric_rule', 'missing')} ; "
        f"ledger_rows={int(len(q1_s02_rows))} ; behavior_tokens={'ok' if behavior_ok else 'missing'}"
    )
    rows.append(
        RequirementRow(
            requirement_id="SEM_Q1_S02_RULE_LOGIC",
            source_spec="SPEC2-Q1/Slides 5",
            module_area="Q1",
            status=q1_s02_status,
            evidence_type="code+runtime",
            evidence_ref=q1_s02_evidence,
            severity="HIGH",
        )
    )

    # Historical data quality requirements
    hist = annual_hist.copy()
    if not hist.empty:
        hist = hist[hist["country"].astype(str).isin(countries)]
        hist = hist[pd.to_numeric(hist["year"], errors="coerce").between(2018, 2024)]
    expected_hist_rows = len(countries) * 7
    n_hist_rows = int(len(hist))
    hist_cov_status = "OK" if n_hist_rows >= expected_hist_rows else "PARTIEL"
    rows.append(
        RequirementRow(
            requirement_id="DQ_HIST_COVERAGE_2018_2024",
            source_spec="SPEC1-Donnees historiques",
            module_area="GLOBAL",
            status=hist_cov_status,
            evidence_type="runtime",
            evidence_ref=f"annual_metrics rows={n_hist_rows}/{expected_hist_rows}",
            severity="CRITICAL",
        )
    )

    completeness_min = float(pd.to_numeric(hist.get("completeness", np.nan), errors="coerce").min()) if not hist.empty else np.nan
    comp_status = "OK" if np.isfinite(completeness_min) and completeness_min >= 0.98 else "PARTIEL"
    rows.append(
        RequirementRow(
            requirement_id="DQ_HIST_COMPLETENESS_MIN_098",
            source_spec="SPEC0-0.3.3 & SPEC1-tests quality",
            module_area="GLOBAL",
            status=comp_status,
            evidence_type="runtime",
            evidence_ref=f"completeness_min={completeness_min:.6f}" if np.isfinite(completeness_min) else "completeness indisponible",
            severity="HIGH",
        )
    )

    quality_fail = int((hist.get("quality_flag", pd.Series(dtype=str)).astype(str).str.upper() == "FAIL").sum()) if not hist.empty else 0
    qf_status = "OK" if quality_fail == 0 else "PARTIEL"
    rows.append(
        RequirementRow(
            requirement_id="DQ_HIST_QUALITYFLAG_NO_FAIL",
            source_spec="SPEC1-data quality",
            module_area="GLOBAL",
            status=qf_status,
            evidence_type="runtime",
            evidence_ref=f"quality_flag_FAIL={quality_fail}",
            severity="HIGH",
        )
    )

    # Scenario coverage requirements
    for sid in DEFAULT_SCENARIOS:
        st, ev = _scenario_coverage(scenario_root, sid, countries, phase2_assumptions=phase2_assumptions)
        rows.append(
            RequirementRow(
                requirement_id=f"SCEN_{sid}_COVERAGE",
                source_spec="SPEC2-prospectif Q1..Q5",
                module_area="SCENARIO",
                status=st,
                evidence_type="runtime",
                evidence_ref=ev,
                severity="HIGH",
            )
        )

    # Q3 informativeness
    q3_st, q3_ev = _q3_informativeness(run_dir)
    rows.append(
        RequirementRow(
            requirement_id="Q3_SCEN_INFORMATIVENESS",
            source_spec="SPEC2-Q3",
            module_area="Q3",
            status=q3_st,
            evidence_type="runtime",
            evidence_ref=q3_ev,
            severity="MEDIUM",
        )
    )

    # Reporting/slides hard gates
    req_count = int(qc.get("slides_requirements_count", 0))
    trace_rows = int(qc.get("slides_trace_rows", 0))
    covered_no = int(qc.get("slides_covered_no", 0))
    st_extract = "OK" if req_count > 0 else "MANQUANT"
    st_trace = "OK" if trace_rows > 0 and covered_no == 0 else "PARTIEL"
    st_qc = "OK" if str(qc.get("verdict", "")).upper() == "PASS" else "PARTIEL"

    rows.extend(
        [
            RequirementRow(
                requirement_id="RPT_SLIDES_EXTRACTION_NON_EMPTY",
                source_spec="Plan audit integral",
                module_area="REPORTING",
                status=st_extract,
                evidence_type="code",
                evidence_ref=f"slides_requirements_count={req_count}",
                severity="CRITICAL",
            ),
            RequirementRow(
                requirement_id="RPT_SLIDES_TRACEABILITY_COMPLETE",
                source_spec="Plan audit integral",
                module_area="REPORTING",
                status=st_trace,
                evidence_type="runtime",
                evidence_ref=f"slides_trace_rows={trace_rows}; covered_no={covered_no}",
                severity="CRITICAL",
            ),
            RequirementRow(
                requirement_id="RPT_QUALITY_GATES_PASS",
                source_spec="Plan audit integral",
                module_area="REPORTING",
                status=st_qc,
                evidence_type="runtime",
                evidence_ref=f"report_qc.verdict={qc.get('verdict')}",
                severity="HIGH",
            ),
        ]
    )

    matrix = pd.DataFrame([r.to_dict() for r in rows])
    matrix = matrix.sort_values(["status", "module_area", "requirement_id"]).reset_index(drop=True)

    # Slides detailed coverage (direct artifact)
    slides_detail = slides_trace.copy()
    if not slides_detail.empty:
        slides_detail["covered"] = slides_detail["covered"].astype(str)
        slides_detail["status"] = np.where(slides_detail["covered"] == "yes", "OK", "MANQUANT")

    # Critical gaps
    critical_gaps = matrix[
        (matrix["status"] != "OK") & (matrix["severity"].isin(["CRITICAL", "HIGH"]))
    ].copy()

    # Verdict
    all_ok = bool((matrix["status"] == "OK").all())
    verdict = "100% atteint" if all_ok else "NON 100%"

    reports_dir.mkdir(parents=True, exist_ok=True)
    matrix.to_csv(reports_dir / "compliance_matrix_full.csv", index=False)
    if not slides_detail.empty:
        slides_detail.to_csv(reports_dir / "slides_coverage_detailed.csv", index=False)
    else:
        pd.DataFrame(
            columns=[
                "slide_id",
                "requirement_id",
                "question_id",
                "requirement_text",
                "covered",
                "coverage_method",
                "evidence_ref",
                "test_id",
                "report_section",
                "status",
            ]
        ).to_csv(reports_dir / "slides_coverage_detailed.csv", index=False)

    evidence_lines = [
        f"# Compliance Evidence Index - {run_id}",
        "",
        f"- Matrice totale: **{len(matrix)}** exigences",
        f"- OK: **{int((matrix['status'] == 'OK').sum())}**",
        f"- PARTIEL: **{int((matrix['status'] == 'PARTIEL').sum())}**",
        f"- MANQUANT: **{int((matrix['status'] == 'MANQUANT').sum())}**",
        "",
        "## Evidence refs par module",
    ]
    for module, g in matrix.groupby("module_area"):
        evidence_lines.append(f"### {module}")
        for _, r in g.head(120).iterrows():
            evidence_lines.append(
                f"- `{r['requirement_id']}` [{r['status']}] -> {r['evidence_ref']} ({r['source_spec']})"
            )
        evidence_lines.append("")
    (reports_dir / "compliance_evidence_index.md").write_text("\n".join(evidence_lines), encoding="utf-8")

    gap_lines = [f"# Compliance Gaps Critical - {run_id}", ""]
    if critical_gaps.empty:
        gap_lines.append("Aucun gap critique (CRITICAL/HIGH) ouvert.")
    else:
        gap_lines.append("## Gaps critiques a corriger en priorite")
        for _, r in critical_gaps.iterrows():
            gap_lines.append(
                f"- `{r['requirement_id']}` [{r['severity']}] [{r['status']}] :: {r['evidence_ref']} :: source={r['source_spec']}"
            )
    (reports_dir / "compliance_gaps_critical.md").write_text("\n".join(gap_lines), encoding="utf-8")

    verdict_lines = [
        f"# Compliance Verdict - {run_id}",
        "",
        f"Verdict: **{verdict}**",
        "",
        "## Justification",
        f"- Exigences totales: {len(matrix)}",
        f"- OK: {int((matrix['status'] == 'OK').sum())}",
        f"- PARTIEL: {int((matrix['status'] == 'PARTIEL').sum())}",
        f"- MANQUANT: {int((matrix['status'] == 'MANQUANT').sum())}",
        "",
        "## Regle de decision",
        "- 100% atteint <=> toutes les exigences atomiques sont OK.",
        "- Sinon verdict NON 100% avec gaps explicites.",
    ]
    (reports_dir / f"compliance_verdict_{run_id}.md").write_text("\n".join(verdict_lines), encoding="utf-8")

    audit_lines: list[str] = [
        f"# Audit integral Q1-Q5 - {run_id}",
        "",
        "## 1) Qualite des donnees historiques",
        f"- Pays audites: {', '.join(countries)}",
        f"- Lignes annuelles historiques (2018-2024): {n_hist_rows}/{expected_hist_rows}",
        f"- Completeness minimale: {completeness_min:.6f}" if np.isfinite(completeness_min) else "- Completeness minimale: n/a",
        f"- quality_flag FAIL: {quality_fail}",
        "",
        "## 2) Resultats par question (ledger + comparaison)",
    ]
    for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        block = blocks[qid]
        led = block.ledger.copy()
        cmp = block.comparison.copy()
        status_counts = led["status"].astype(str).value_counts().to_dict() if not led.empty else {}
        audit_lines.append(f"### {qid}")
        audit_lines.append(
            f"- Ledger: PASS={status_counts.get('PASS', 0)}, WARN={status_counts.get('WARN', 0)}, FAIL={status_counts.get('FAIL', 0)}, NON_TESTABLE={status_counts.get('NON_TESTABLE', 0)}"
        )
        if not cmp.empty and "interpretability_status" in cmp.columns:
            c_counts = cmp["interpretability_status"].astype(str).value_counts().to_dict()
            audit_lines.append(
                f"- Comparaison HIST/SCEN: INFORMATIVE={c_counts.get('INFORMATIVE', 0)}, FRAGILE={c_counts.get('FRAGILE', 0)}, NON_TESTABLE={c_counts.get('NON_TESTABLE', 0)}"
            )
        else:
            audit_lines.append(f"- Comparaison HIST/SCEN: lignes={len(cmp)} (pas de statut interpretabilite explicite)")
        audit_lines.append("")

    audit_lines.append("## 3) Couverture slides/specs")
    audit_lines.append(f"- Exigences slides extraites: {req_count}")
    audit_lines.append(f"- Lignes de traceabilite slides: {trace_rows}")
    audit_lines.append(f"- Couvertes OUI/NON: {int(qc.get('slides_covered_yes', 0))}/{covered_no}")
    audit_lines.append("")
    audit_lines.append("## 4) Verdict")
    audit_lines.append(f"- Verdict conformite atomique: {verdict}")
    audit_lines.append(
        f"- Exigences OK/PARTIEL/MANQUANT: {int((matrix['status'] == 'OK').sum())}/{int((matrix['status'] == 'PARTIEL').sum())}/{int((matrix['status'] == 'MANQUANT').sum())}"
    )
    (reports_dir / f"audit_integral_{run_id}.md").write_text("\n".join(audit_lines), encoding="utf-8")

    return {
        "run_id": run_id,
        "matrix_rows": int(len(matrix)),
        "ok": int((matrix["status"] == "OK").sum()),
        "partiel": int((matrix["status"] == "PARTIEL").sum()),
        "manquant": int((matrix["status"] == "MANQUANT").sum()),
        "verdict": verdict,
    }


def main() -> None:
    args = _parse_args()
    countries = [c.strip() for c in str(args.countries).split(",") if c.strip()]
    stats = run_audit(
        run_id=args.run_id,
        reports_dir=Path(args.reports_dir),
        annual_hist_path=Path(args.annual_hist_path),
        scenario_root=Path(args.scenario_root),
        countries=countries,
        phase2_assumptions_path=Path(args.phase2_assumptions_path),
    )
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
