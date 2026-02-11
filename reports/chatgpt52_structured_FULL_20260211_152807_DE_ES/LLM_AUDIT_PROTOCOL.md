# LLM Audit Protocol (DE, ES) - FULL_20260211_152807

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
