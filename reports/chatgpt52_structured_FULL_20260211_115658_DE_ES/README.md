# Structured Analytical Package (DE, ES) - FULL_20260211_115658

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
