# PAYLOAD LLM - Audit DE/ES

Ce document est prêt à être copié-collé dans un autre LLM pour un audit rigoureux.
Généré le: `2026-02-10 17:46:52 UTC`
Package source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES`
Run ID: `FULL_20260210_172152`
Countries scope: `DE, ES`

## Instructions pour l'autre LLM
1. Lire les sections Méthode + Inputs avant les questions.
2. Analyser Q1→Q5 en séparant HIST vs SCEN.
3. Citer systématiquement `test_id` ou `table.colonne` pour chaque conclusion.
4. Qualifier chaque conclusion: ROBUSTE / FRAGILE / NON_TESTABLE.
5. Ne pas extrapoler au-delà des données ci-dessous.

### Méthode d'audit (racine)
Source: `AUDIT_METHODS_Q1_Q5.md`

```markdown
# Audit Methods Reference (Q1-Q5)

Last updated: 2026-02-10
Scope: full auditability reference for formulas, data, hypotheses, and checks used by Q1-Q5 (HIST + SCEN).
Maintenance rule: update this file whenever calculation logic changes in `src/modules/*.py`, `src/metrics.py`, or `src/scenario/*.py`.

## 1. Purpose and governance

This document is the root methodological reference requested for external audit.
It describes:

1. Which data are used.
2. Which formulas are applied.
3. Which assumptions are configurable.
4. Which checks decide robustness vs fragility vs non-testable.
5. Which files contain outputs per question.

Authoritative code paths:

- `src/metrics.py`
- `src/modules/q1_transition.py`
- `src/modules/q2_slope.py`
- `src/modules/q3_exit.py`
- `src/modules/q4_bess.py`
- `src/modules/q5_thermal_anchor.py`
- `src/scenario/calibration.py`
- `src/scenario/phase2_engine.py`


## 2. Data sources and storage

### 2.1 Historical (HIST)

- ENTSO-E raw cache:
  - `data/raw/entsoe/prices_da/{country}/{year}.parquet`
  - `data/raw/entsoe/load_total/{country}/{year}.parquet`
  - `data/raw/entsoe/generation_by_type/{country}/{year}.parquet`
  - `data/raw/entsoe/net_position/{country}/{year}.parquet`
  - optional: `data/raw/entsoe/psh_pump/{country}/{year}.parquet`
- Canonical hourly:
  - `data/processed/hourly/{country}/{year}.parquet`
- Historical annual metrics:
  - `data/metrics/annual_metrics.parquet`
- Historical daily metrics:
  - `data/metrics/daily_metrics.parquet`
- Validation findings:
  - `data/metrics/validation_findings.parquet`

### 2.2 Prospective (SCEN)

- Scenario assumptions table:
  - `data/assumptions/phase2/phase2_scenario_country_year.csv`
- Scenario hourly outputs:
  - `data/processed/scenario/{scenario_id}/hourly/{country}/{year}.parquet`
- Scenario annual metrics:
  - `data/processed/scenario/{scenario_id}/annual_metrics.parquet`
- Scenario validation findings:
  - `data/processed/scenario/{scenario_id}/validation_findings.parquet`

### 2.3 Common assumptions

- Phase 1 assumptions:
  - `data/assumptions/phase1_assumptions.csv`
- Country config (timezones, must-run config, ENTSO-E code):
  - `config/countries.yaml`
- PSR mapping:
  - `data/static/entsoe_psr_mapping.csv`


## 3. Canonical physical and market formulas

Main implementation: `src/metrics.py` and preprocessing pipeline.

### 3.1 Core hourly variables

- `gen_vre_mw = gen_solar_mw + gen_wind_on_mw + gen_wind_off_mw`
- `nrl_mw = load_mw - gen_vre_mw - gen_must_run_mw`
- `surplus_mw = max(0, -nrl_mw)`
- `exports_mw = max(net_position_mw, 0)`
- `flex_sink_observed_mw = exports_mw + flex_sink_psh_pump_mw`
- `surplus_absorbed_mw = min(surplus_mw, flex_effective_mw)`
- `surplus_unabsorbed_mw = surplus_mw - surplus_absorbed_mw`

### 3.2 Regime classification (anti-circular)

Regimes are physical-first (no price input):

- A: `surplus_unabsorbed_mw > 0`
- B: `surplus_mw > 0` and `surplus_unabsorbed_mw == 0`
- D: `surplus_mw == 0` and `nrl_mw >= threshold_peak_mw`
- C: remaining hours

Threshold D default: `P90(nrl_mw on positive nrl)` with minimum positive-hour guard.

### 3.3 Annual metrics

- Baseload price: average of hourly DA price.
- Capture price (tech X): `sum(price * gen_X) / sum(gen_X)`.
- Capture ratio vs baseload: `capture_X / baseload`.
- TTL (price-based): `P95(price)` on regimes C + D.
- SR (energy share):
  - `sr_energy_share_load = surplus_energy / load_net_energy`
  - `sr_energy_share_gen = surplus_energy / gen_primary_energy` (main SR alias)
- FAR: `surplus_absorbed_energy / surplus_energy` (NaN if denominator = 0).
- IR: `P10(gen_must_run_mw) / P10(load_mw)`.

### 3.4 Quality and reality indicators

- Completeness from missing critical flags.
- Quality flag:
  - `OK` if completeness >= 0.98
  - `WARN` if 0.90 <= completeness < 0.98
  - `FAIL` otherwise
- Regime coherence score from expected price ranges by regime.
- NRL-price correlation.


## 4. Question-by-question analytical logic

## 4.1 Q1 - Transition Phase 1 -> Phase 2

Code: `src/modules/q1_transition.py`

### Objective

Detect transition year with two independent diagnostics:

1. Market symptoms.
2. Physical stress.

### Inputs

- `annual_metrics.parquet` country-year panel.
- Phase 1 thresholds from `phase1_assumptions.csv`.

### Calculations

1. `stage2_market_score` from points on:
   - `h_negative_obs`
   - `h_below_5_obs`
   - `capture_ratio_pv_vs_ttl`
   - `days_spread_gt50`
2. Phase2 market condition:
   - score >= 2
   - optional non-capture signal gate (`q1_require_non_capture_signal`)
3. Physical stress flags:
   - `sr_energy >= sr_energy_material_min`
   - `far_energy <= far_energy_tension_max`
   - `ir_p10 >= ir_p10_high_min`
4. Transition years:
   - market transition year
   - physical transition year
5. Confidence penalty from coherence/completeness.

### Outputs

- `Q1_country_summary`
- `Q1_year_panel`
- checks/warnings on incoherent transition signals.

### Robustness qualification

- `quality_flag == FAIL` invalidates strong conclusions.
- capture-only signals are warned.


## 4.2 Q2 - Phase 2 slope and drivers

Code: `src/modules/q2_slope.py`

### Objective

Estimate cannibalization slope for PV/Wind after Q1 transition, and rank drivers.

### Inputs

- annual metrics.
- Q1 transition result.
- optional hourly data for driver features.

### Calculations

1. Build Phase2 subset per country (years >= transition year).
2. Regression per tech:
   - preferred x: penetration (`pv_penetration_pct_gen` or `wind_penetration_pct_gen`)
   - fallback x: `sr_energy`
   - y: capture ratio vs TTL
3. Estimator:
   - OLS when data sufficient
   - `DELTA_2PT` directional slope when only two points
4. Driver features:
   - mean SR/FAR/IR/TTL on phase2 subset
   - hourly `corr(gen_vre_mw, load_mw)`
   - surplus share in low-load quartile
5. Cross-country driver correlations against slope.

### Outputs

- `Q2_country_slopes`
- `Q2_driver_correlations`
- robustness flag per slope (`ROBUST`, `FRAGILE`, `NON_TESTABLE`).


## 4.3 Q3 - Exit Phase 2 and inversion conditions

Code: `src/modules/q3_exit.py`

### Objective

Classify trend status and estimate static inversion orders of magnitude.

### Inputs

- annual panel.
- hourly reference year per country.
- Q3 assumptions (trend window, targets, gates).

### Calculations

1. Trends on rolling window:
   - `trend_h_negative`
   - `trend_capture_ratio_pv_vs_ttl`
   - `trend_sr_energy`
   - `trend_far_energy`
2. Status assignment:
   - `degradation`, `stabilisation`, `amelioration`, `transition_partielle`
   - `hors_scope_stage2` if stage2 gate not met.
3. Counterfactuals (binary search):
   - demand uplift `k` required for SR target
   - must-run reduction `r` required for SR target
   - additional absorbed energy needed for FAR target
4. Additional sink power proxy:
   - `P95(surplus_unabsorbed_mw)`.

### Outputs

- `Q3_status`.

### Interpretation rule

`hors_scope_stage2` means the scenario is not stressed enough for a phase2-exit statement.
This is explicit non-testability, not silent success.


## 4.4 Q4 - BESS sizing and impact

Code: `src/modules/q4_bess.py`

### Objective

Quantify battery impact in three modes and estimate minimum sizing for target objective.

### Modes

- `SURPLUS_FIRST` (system stress absorption)
- `PRICE_ARBITRAGE_SIMPLE` (simple value spread)
- `PV_COLOCATED` (PV + storage value uplift)

### Inputs

- hourly panel for selected country-year.
- Q4 assumptions:
  - `bess_eta_roundtrip`
  - `bess_max_cycles_per_day`
  - `bess_soc_init_frac`
  - `target_far`
  - `target_surplus_unabs_energy_twh`
- power and duration grids from UI selection.

### Calculations

1. Numpy dispatch simulation with daily masks.
2. SOC and power constraints enforced each hour.
3. Post-BESS absorbed and unabsorbed surplus recomputation.
4. Frontier over grid:
   - FAR before/after
   - unabsorbed energy before/after
   - capture uplift (PV colocated mode)
   - price-taker revenue
5. Objective selection:
   - `FAR_TARGET` or `SURPLUS_UNABS_TARGET`
   - choose minimum feasible by power then energy.

### Invariants

- `0 <= SOC <= Emax`
- `charge <= Pmax`
- `discharge <= Pmax`
- discharged energy <= charged energy * eta
- monotonic checks for surplus reduction in `SURPLUS_FIRST`.

### Outputs

- `Q4_sizing_summary`
- `Q4_bess_frontier`
- persistent cache under `data/cache/q4/...`.


## 4.5 Q5 - CO2/Gas thermal anchor

Code: `src/modules/q5_thermal_anchor.py`

### Objective

Measure thermal anchor behavior and sensitivities to gas/CO2 on non-surplus hours.

### Inputs

- hourly panel with price and regime.
- commodity daily series:
  - `date`
  - `gas_price_eur_mwh_th`
  - `co2_price_eur_t`
- thermal parameters from assumptions:
  - efficiency, emission factor, VOM by technology (CCGT/COAL).

### Calculations

1. Thermal anchor:
   - `tca = gas/eff + co2*(ef/eff) + vom`
2. Restrict to regimes C/D for comparison.
3. Compute:
   - `ttl_obs = P95(price on C/D)`
   - `tca_q95 = P95(tca on C/D)`
   - `alpha = ttl_obs - tca_q95`
   - `corr_cd = corr(price, tca) on C/D`
4. Sensitivities:
   - `dTCA/dGas = 1/eff`
   - `dTCA/dCO2 = ef/eff`
5. CO2 required for target TTL:
   - solve from `ttl_target ~= alpha + tca_q95_scenario`.
   - expose raw and non-negative-clamped versions.

### Outputs

- `Q5_summary`
- checks on derivative signs and weak/fragile anchor relation.


## 5. Prospective engine (SCEN) mechanics

Main code: `src/scenario/calibration.py`, `src/scenario/phase2_engine.py`.

### 5.1 Historical calibration per country

Calibrated values include:

- must-run floors (`mr_p10_mw`, `mr_mean_mw`)
- export and PSH realization factors
- stress penalty from coincidence
- regime-B price fit (`floor/cap/intercept/slope/pass-through`)
- C/D levels and NRL quantiles
- surplus percentile scaling.

### 5.2 Prospective physical projection

1. Select historical reference year by country.
2. Scale load profile to target annual demand.
3. Scale VRE profiles to target capacities with historical-energy floor logic.
4. Build must-run profiles from scenario capacities and calibrated floors/caps.
5. Apply conservative flex ordering:
   - exports sink
   - PSH sink
   - BESS sink
6. Recompute surplus absorption and unabsorbed surplus.
7. Reclassify regimes (A/B/C/D) after BESS.
8. Inject synthetic piecewise-affine prices with calibrated regime-B behavior.

### 5.3 Scenario audit columns

Scenario annual outputs include calibration traces:

- `calib_export_cap_eff_gw`
- `calib_export_coincidence_used`
- `calib_flex_realization_factor`
- `calib_price_b_floor`
- `calib_price_b_intercept`
- `calib_price_b_slope_surplus_norm`
- and other calibration context fields.


## 6. Standard evidence outputs

Per question bundle output:

- `outputs/combined/{run_id}/Qx/summary.json`
- `outputs/combined/{run_id}/Qx/test_ledger.csv`
- `outputs/combined/{run_id}/Qx/comparison_hist_vs_scen.csv`
- `outputs/combined/{run_id}/Qx/hist/tables/*.csv`
- `outputs/combined/{run_id}/Qx/scen/{scenario_id}/tables/*.csv`

Status semantics:

- `PASS`: test passed.
- `WARN`: potential fragility/inconsistency, interpret with caution.
- `FAIL`: hard inconsistency.
- `NON_TESTABLE`: not enough signal/data to claim result.


## 7. External-audit workflow (recommended)

1. Use one single complete run id (no mixed runs).
2. Export country-scoped package with:
   - `python scripts/export_structured_country_pack.py --run-id <RUN_ID> --countries DE,ES`
3. Audit by question:
   - start from `questions/Qx/question_context.json`
   - review `test_ledger.csv`
   - review HIST and SCEN tables
   - review `comparison_hist_vs_scen.csv`
   - cross-check with assumptions in `inputs/`.


## 8. Known limitations to keep explicit

1. No full equilibrium dispatch model.
2. Scenario logic is pragmatic stress-testing, not market forecast.
3. Some question/scenario pairs can be `NON_TESTABLE` by design when stress is absent.
4. Correlations and slopes are explanatory signals, not automatic causal proof.
```

### Protocole d'audit LLM
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\LLM_AUDIT_PROTOCOL.md`

```markdown
# LLM Audit Protocol (DE, ES) - FULL_20260210_172152

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

## 4) Robustness rubric
- Robust: status PASS and interpretable deltas with non-null denominators.
- Fragile: WARN or low statistical strength (`n`, `p_value`, `r2`) or low coherence.
- Non-testable: explicit `NON_TESTABLE` or out-of-scope status (for example `hors_scope_stage2`).

## 5) Reporting rules for external reviewer
- No conclusion without numeric evidence (`test_id` or `table.column`).
- Distinguish historical fact vs prospective stress-test output.
- Explicitly document limits and non-testable zones.
```

### Manifest
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\manifest.json`

```json
{
  "package_name": "chatgpt52_structured_FULL_20260210_172152_DE_ES",
  "run_id": "FULL_20260210_172152",
  "run_dir": "outputs\\combined\\FULL_20260210_172152",
  "countries_scope": [
    "DE",
    "ES"
  ],
  "generated_at_utc": "2026-02-10T17:40:47.640620+00:00",
  "questions": [
    "Q1",
    "Q2",
    "Q3",
    "Q4",
    "Q5"
  ],
  "method_reference_file": "AUDIT_METHODS_Q1_Q5.md"
}
```

### Index des fichiers exportés
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\file_index.csv`

```csv
category,file,rows
inputs,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\inputs\phase1_assumptions.csv,39
inputs,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\inputs\phase2_scenario_country_year.csv,24
inputs,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\inputs\annual_metrics_hist.csv,14
inputs,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\inputs\validation_findings_hist.csv,14
inputs,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\inputs\annual_metrics_scenarios.csv,24
inputs,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\inputs\test_registry.csv,24
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\checks_filtered.csv,18
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\warnings_filtered.csv,0
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\test_ledger.csv,16
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\comparison_hist_vs_scen.csv,8
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\hist\tables\Q1_country_summary.csv,2
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\hist\tables\Q1_year_panel.csv,14
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\BASE\tables\Q1_country_summary.csv,2
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\BASE\tables\Q1_year_panel.csv,4
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\BASE\checks_filtered.csv,3
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\DEMAND_UP\tables\Q1_country_summary.csv,2
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\DEMAND_UP\tables\Q1_year_panel.csv,4
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\DEMAND_UP\checks_filtered.csv,3
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\FLEX_UP\tables\Q1_country_summary.csv,2
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\FLEX_UP\tables\Q1_year_panel.csv,4
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\FLEX_UP\checks_filtered.csv,3
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\LOW_RIGIDITY\tables\Q1_country_summary.csv,2
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\LOW_RIGIDITY\tables\Q1_year_panel.csv,4
Q1,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\LOW_RIGIDITY\checks_filtered.csv,3
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\checks_filtered.csv,12
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\warnings_filtered.csv,3
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\test_ledger.csv,9
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\comparison_hist_vs_scen.csv,12
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\hist\tables\Q2_country_slopes.csv,4
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\hist\tables\Q2_driver_correlations.csv,6
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\BASE\tables\Q2_country_slopes.csv,4
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\BASE\tables\Q2_driver_correlations.csv,6
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\BASE\checks_filtered.csv,3
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_CO2\tables\Q2_country_slopes.csv,4
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_CO2\tables\Q2_driver_correlations.csv,6
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_CO2\checks_filtered.csv,3
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_GAS\tables\Q2_country_slopes.csv,4
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_GAS\tables\Q2_driver_correlations.csv,6
Q2,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_GAS\checks_filtered.csv,3
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\checks_filtered.csv,17
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\warnings_filtered.csv,0
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\test_ledger.csv,10
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\comparison_hist_vs_scen.csv,16
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\hist\tables\Q3_status.csv,2
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\BASE\tables\Q3_status.csv,2
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\BASE\checks_filtered.csv,3
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\DEMAND_UP\tables\Q3_status.csv,2
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\DEMAND_UP\checks_filtered.csv,3
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\FLEX_UP\tables\Q3_status.csv,2
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\FLEX_UP\checks_filtered.csv,3
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\LOW_RIGIDITY\tables\Q3_status.csv,2
Q3,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\LOW_RIGIDITY\checks_filtered.csv,3
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\checks_filtered.csv,41
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\warnings_filtered.csv,26
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\test_ledger.csv,10
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\comparison_hist_vs_scen.csv,28
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\hist\tables\Q4_bess_frontier.csv,168
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\hist\tables\Q4_sizing_summary.csv,2
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\BASE\tables\Q4_bess_frontier.csv,168
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\BASE\tables\Q4_sizing_summary.csv,2
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\BASE\checks_filtered.csv,8
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\FLEX_UP\tables\Q4_bess_frontier.csv,168
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\FLEX_UP\tables\Q4_sizing_summary.csv,2
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\FLEX_UP\checks_filtered.csv,8
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_CO2\tables\Q4_bess_frontier.csv,168
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_CO2\tables\Q4_sizing_summary.csv,2
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_CO2\checks_filtered.csv,8
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_GAS\tables\Q4_bess_frontier.csv,168
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_GAS\tables\Q4_sizing_summary.csv,2
Q4,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_GAS\checks_filtered.csv,8
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\checks_filtered.csv,44
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\warnings_filtered.csv,0
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\test_ledger.csv,10
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\comparison_hist_vs_scen.csv,24
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\hist\tables\Q5_summary.csv,2
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\BASE\tables\Q5_summary.csv,2
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\BASE\checks_filtered.csv,7
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_BOTH\tables\Q5_summary.csv,2
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_BOTH\checks_filtered.csv,11
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_CO2\tables\Q5_summary.csv,2
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_CO2\checks_filtered.csv,7
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_GAS\tables\Q5_summary.csv,2
Q5,reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_GAS\checks_filtered.csv,7
```

## Inputs

### Registry des tests
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\inputs\test_registry.csv`

```csv
test_id,question_id,source_ref,mode,scenario_group,title,what_is_tested,metric_rule,severity_if_fail
Q1-H-01,Q1,SPEC2-Q1/Slides 2-4,HIST,HIST_BASE,Score marche de bascule,La signature marche de phase 2 est calculee et exploitable.,stage2_market_score present et non vide,HIGH
Q1-H-02,Q1,SPEC2-Q1/Slides 3-4,HIST,HIST_BASE,Stress physique SR/FAR/IR,La bascule physique est fondee sur SR/FAR/IR.,sr_energy/far_energy/ir_p10 presentes,CRITICAL
Q1-H-03,Q1,SPEC2-Q1,HIST,HIST_BASE,Concordance marche vs physique,La relation entre bascule marche et bascule physique est mesurable.,bascule_year_market et bascule_year_physical comparables,MEDIUM
Q1-H-04,Q1,Slides 4-6,HIST,HIST_BASE,Robustesse seuils,Le diagnostic reste stable sous variation raisonnable de seuils.,delta bascules sous choc de seuil <= 50%,MEDIUM
Q1-S-01,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Bascule projetee par scenario,Chaque scenario fournit un diagnostic de bascule projetee.,Q1_country_summary non vide en SCEN,HIGH
Q1-S-02,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY,Les leviers scenario modifient la bascule vs BASE.,delta bascule_year_market vs BASE calculable,MEDIUM
Q1-S-03,Q1,SPEC2-Q1,SCEN,DEFAULT,Qualite de causalite,Le regime_coherence respecte le seuil d'interpretation.,part regime_coherence >= seuil min,MEDIUM
Q2-H-01,Q2,SPEC2-Q2/Slides 10,HIST,HIST_BASE,Pentes OLS post-bascule,Les pentes PV/Wind sont estimees en historique.,Q2_country_slopes non vide,HIGH
Q2-H-02,Q2,SPEC2-Q2/Slides 10-12,HIST,HIST_BASE,Robustesse statistique,R2/p-value/n sont disponibles pour qualifier la robustesse.,"colonnes r2,p_value,n presentes",MEDIUM
Q2-H-03,Q2,Slides 10-13,HIST,HIST_BASE,Drivers physiques,Les drivers SR/FAR/IR/corr VRE-load sont exploites.,driver correlations non vides,MEDIUM
Q2-S-01,Q2,SPEC2-Q2/Slides 11,SCEN,DEFAULT,Pentes projetees,Les pentes sont reproduites en mode scenario.,Q2_country_slopes non vide en SCEN,HIGH
Q2-S-02,Q2,SPEC2-Q2,SCEN,DEFAULT,Delta pente vs BASE,Les differences de pente vs BASE sont calculables.,delta slope par pays/tech vs BASE,MEDIUM
Q3-H-01,Q3,SPEC2-Q3/Slides 16,HIST,HIST_BASE,Tendances glissantes,Les tendances h_negative et capture_ratio sont estimees.,Q3_status non vide,HIGH
Q3-H-02,Q3,SPEC2-Q3,HIST,HIST_BASE,Statuts sortie phase 2,Les statuts degradation/stabilisation/amelioration sont attribues.,status dans ensemble attendu,MEDIUM
Q3-S-01,Q3,SPEC2-Q3/Slides 17,SCEN,DEFAULT,Conditions minimales d'inversion,Les besoins demande/must-run/flex sont quantifies en scenario.,"inversion_k, inversion_r et additional_absorbed presentes",HIGH
Q3-S-02,Q3,Slides 17-19,SCEN,DEFAULT,Validation entree phase 3,Le statut prospectif est interpretable pour la transition phase 3.,status non vide en SCEN,MEDIUM
Q4-H-01,Q4,SPEC2-Q4/Slides 22,HIST,HIST_BASE,Simulation BESS 3 modes,"SURPLUS_FIRST, PRICE_ARBITRAGE_SIMPLE et PV_COLOCATED sont executes.",3 modes executes avec sorties non vides,CRITICAL
Q4-H-02,Q4,SPEC2-Q4,HIST,HIST_BASE,Invariants physiques BESS,Bornes SOC/puissance/energie respectees.,aucun check FAIL Q4,CRITICAL
Q4-S-01,Q4,SPEC2-Q4/Slides 23,SCEN,DEFAULT,Comparaison effet batteries par scenario,Impact FAR/surplus/capture compare entre scenarios utiles.,Q4 summary non vide pour >=1 scenario,HIGH
Q4-S-02,Q4,Slides 23-25,SCEN,DEFAULT,Sensibilite valeur commodites,Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.,delta pv_capture ou revenus vs BASE,MEDIUM
Q5-H-01,Q5,SPEC2-Q5/Slides 28,HIST,HIST_BASE,Ancre thermique historique,TTL/TCA/alpha/corr sont estimes hors surplus.,Q5_summary non vide avec ttl_obs et tca_q95,HIGH
Q5-H-02,Q5,SPEC2-Q5,HIST,HIST_BASE,Sensibilites analytiques,dTCA/dCO2 et dTCA/dGas sont positives.,dTCA_dCO2 > 0 et dTCA_dGas > 0,CRITICAL
Q5-S-01,Q5,SPEC2-Q5/Slides 29,SCEN,DEFAULT,Sensibilites scenarisees,BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.,Q5_summary non vide sur scenarios selectionnes,HIGH
Q5-S-02,Q5,SPEC2-Q5/Slides 31,SCEN,DEFAULT,CO2 requis pour TTL cible,Le CO2 requis est calcule et interpretable.,co2_required_* non NaN,MEDIUM
```

### Hypothèses Phase 1
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\inputs\phase1_assumptions.csv`

```csv
param_group,param_name,param_value,unit,description,source,last_updated,owner
PHASE_THRESHOLDS,capture_ratio_pv_vs_ttl_crisis_max,0.7,ratio,Seuil crise capture ratio pv/ttl,default,2026-02-09,system
PHASE_THRESHOLDS,capture_ratio_pv_vs_ttl_stage2_max,0.8,ratio,Seuil capture ratio pv/ttl,default,2026-02-09,system
PHASE_THRESHOLDS,days_spread_gt50_stage2_min,150.0,days,Seuil jours spread>50,default,2026-02-09,system
PHASE_THRESHOLDS,h_below_5_stage2_min,500.0,hours,Seuil heures basses,default,2026-02-09,system
PHASE_THRESHOLDS,h_negative_stage2_min,200.0,hours,Seuil heures negatives stage2,default,2026-02-09,system
PHASE_THRESHOLDS,h_negative_stage2_strong,300.0,hours,Seuil fort heures negatives,default,2026-02-09,system
PHASE_THRESHOLDS,stage1_capture_ratio_pv_vs_ttl_min,0.9,ratio,Stage1 min capture ratio pv vs ttl,default,2026-02-10,system
PHASE_THRESHOLDS,stage1_days_spread_gt50_max,120.0,days,Stage1 max days spread gt50,default,2026-02-10,system
PHASE_THRESHOLDS,stage1_h_below_5_max,300.0,hours,Stage1 max hours below 5,default,2026-02-10,system
PHASE_THRESHOLDS,stage1_h_negative_max,100.0,hours,Stage1 max negative hours,default,2026-02-10,system
PHYSICS_THRESHOLDS,far_energy_tension_max,0.95,ratio,Seuil far tension,default,2026-02-09,system
PHYSICS_THRESHOLDS,ir_p10_high_min,0.7,ratio,Seuil inflexibilite haute,default,2026-02-09,system
PHYSICS_THRESHOLDS,sr_energy_material_min,0.01,ratio,Seuil surplus ratio materialite,default,2026-02-09,system
Q2,exclude_year_2022,0.0,bool,Exclude 2022 from regressions (1=yes),default,2026-02-10,system
Q2,min_points_regression,3.0,count,Nombre minimal de points regression,default,2026-02-09,system
Q3,demand_k_max,0.3,ratio,Borne max hausse demande,default,2026-02-09,system
Q3,far_target,0.95,ratio,Cible FAR inversion,default,2026-02-09,system
Q3,require_recent_stage2,1.0,bool,Require recent stage2 stress,default,2026-02-10,system
Q3,sr_energy_target,0.01,ratio,Cible SR inversion,default,2026-02-09,system
Q3,stage2_recent_h_negative_min,200.0,hours,Recent stage2 threshold on negative hours,default,2026-02-10,system
Q3,trend_capture_ratio_min,0.0,ratio/year,Improvement threshold for capture trend,default,2026-02-10,system
Q3,trend_h_negative_max,-10.0,hours/year,Improvement threshold for h_negative trend,default,2026-02-10,system
Q3,trend_window_years,3.0,years,Fenetre tendance Q3,default,2026-02-09,system
Q4,bess_eta_roundtrip,0.88,ratio,Rendement roundtrip BESS,default,2026-02-09,system
Q4,bess_max_cycles_per_day,1.0,cycles/day,Cycles max journaliers BESS,default,2026-02-09,system
Q4,bess_soc_init_frac,0.5,ratio,SOC initial fraction,default,2026-02-09,system
Q4,target_far,0.95,ratio,Cible FAR pour sizing,default,2026-02-09,system
Q4,target_surplus_unabs_energy_twh,0.0,TWh,Cible surplus non absorbe,default,2026-02-09,system
Q5,ccgt_ef_t_per_mwh_th,0.202,tCO2/MWhth,Facteur emission CCGT,default,2026-02-09,system
Q5,ccgt_efficiency,0.55,ratio,Rendement CCGT,default,2026-02-09,system
Q5,ccgt_vom_eur_mwh,3.0,EUR/MWh,VOM CCGT,default,2026-02-09,system
Q5,coal_ef_t_per_mwh_th,0.341,tCO2/MWhth,Facteur emission charbon,default,2026-02-09,system
Q5,coal_efficiency,0.38,ratio,Rendement charbon,default,2026-02-09,system
Q5,coal_vom_eur_mwh,4.0,EUR/MWh,VOM charbon,default,2026-02-09,system
QUALITY,regime_coherence_min_for_causality,0.55,ratio,Seuil coherence minimale causalite,default,2026-02-09,system
PHASE_THRESHOLDS,q1_require_non_capture_signal,1.0,bool01,"Q1: exiger au moins un signal non-capture (h_negative, h_below_5 ou spread) pour classer phase2.",codex_adjustment,2026-02-10,codex
PHASE_THRESHOLDS,q1_min_non_capture_flags,1.0,count,Q1: nombre minimal de flags non-capture requis pour phase2.,codex_adjustment,2026-02-10,codex
Q3,stage2_recent_h_negative_min_scen,80.0,h/an,Q3 SCEN: seuil h_negative recent pour qualifier un contexte Stage2 en prospectif.,codex_adjustment,2026-02-10,codex
Q3,stage2_recent_sr_energy_min_scen,0.02,ratio,Q3 SCEN: seuil SR recent pour qualifier un contexte Stage2 meme si h_negative reste faible.,codex_adjustment,2026-02-10,codex
```

### Hypothèses Phase 2 (DE/ES)
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\inputs\phase2_scenario_country_year.csv`

```csv
scenario_id,country,year,demand_total_twh,demand_peak_gw,demand_shape_reference,cap_pv_gw,cap_wind_on_gw,cap_wind_off_gw,cap_must_run_nuclear_gw,cap_must_run_chp_gw,cap_must_run_biomass_gw,cap_must_run_hydro_ror_gw,must_run_min_output_factor,interconnection_export_gw,export_coincidence_factor,psh_pump_gw,bess_power_gw,bess_energy_gwh,bess_eta_roundtrip,co2_eur_per_t,gas_eur_per_mwh_th,marginal_tech,marginal_efficiency,marginal_emission_factor_t_per_mwh,supported_vre_share,negative_price_rule,negative_price_rule_threshold_hours,price_exposure_share,source_label,notes
BASE,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,DE,2030,578.4937,64.277,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,DE,2040,679.1013,75.456,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,ES,2030,282.2518,31.361,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,ES,2040,331.3391,36.815,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
FLEX_UP,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.8,6.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
FLEX_UP,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,3.6,16.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
FLEX_UP,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.8,6.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
FLEX_UP,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,3.6,16.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,135.0,42.0,coal,0.38,0.341,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,165.0,48.0,coal,0.38,0.341,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,135.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,165.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,63.0,coal,0.38,0.341,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,72.0,coal,0.38,0.341,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,63.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,72.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6,0.65,internal_assumption,Auto-generated baseline for phase2 engine
```

### Métriques annuelles historiques (DE/ES)
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\inputs\annual_metrics_hist.csv`

```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative_obs,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,h_negative,h_below_5
DE,2018,8760,8760,8750,8760,8760,0.0,0.001141552511415525,0.0,0.00011415525114155251,minus_psh_pump,observed,"DE_AT_LU,DE_LU",d09251118754e4daccbc432c71f13ae370edd44e7a89e70648f6c5593e7047bf,559.9527225899999,546.468202485,42.53518894,93.84295614749999,19.0654565625,155.44360164999998,575.9773977325,205.21734064749998,34.114891,0.26987795399949416,0.07384871195892748,0.1960292420405667,0.28445132021065167,44.47275456621005,52.1181577266922,40.218063255152806,43.77257363689873,38.17753675887097,0.9842559576949769,0.8584477649576012,43.77257363689873,38.17753675887097,0.9842559576949769,0.8584477649576012,0.6027951641084436,0.525745521081731,133,232,38,38,32.14734972677596,99.53,1.0689941175000002,0.0,0.001956187226702075,0.0018559653932748086,0.0018559653932748086,0.032534246575342464,1.0,1.0,0.4059062367977894,0.3751052180982559,72.61599999999999,72.61599999999999,,none,0,285,7628,847,0.9843607305936073,0.7143395206268766,0.9988584474885844,OK,133.0,232.0
DE,2019,8760,8759,8759,8760,8760,0.00011415525114155251,0.00011415525114155251,0.0,0.00011415525114155251,minus_psh_pump,observed,"DE_AT_LU,DE_LU",6b1885d2f025c19044eb8b2114907646d0a46055c4e549b3cb8cf747514b1f18,502.47891799250004,491.50658644500004,41.83308617,99.9897749475,24.3804648275,166.203325945,515.6919337375,156.9665405575,34.1900773,0.32229188604994086,0.08112030348586775,0.24117158256407312,0.3381507603939266,37.669692887315904,44.45564814814815,33.892615958770214,34.906182773392544,32.78952818581776,0.926638368882113,0.8704485137137555,34.906182773392544,32.78952818581776,0.926638368882113,0.8704485137137555,0.5957093107616995,0.5595864595845751,211,335,31,31,29.95035519125683,117.32000000000001,1.27199858,0.03480772249999999,0.00258795836125044,0.0024665861472393693,0.0024665861472393693,0.03995433789954338,0.9726354077376408,0.9726354077376408,0.3020039544090348,0.31932150317217467,58.596,58.596,,none,8,342,7569,841,0.9982874757392396,0.8187692611447057,0.9997716894977169,OK,211.0,335.0
DE,2020,8784,8783,8783,8784,8784,0.00011384335154826958,0.00011384335154826958,0.0,0.00011384335154826958,minus_psh_pump,observed,"DE_AT_LU,DE_LU",a7cab4363eb99fae2c73215fa1f13fa3261829e9946ac6fa91f6de4b6830b3aa,490.2538991575,477.63568764250005,45.93743737,103.4146983125,26.88256224,176.2346979225,493.92594583249996,138.029930155,21.1321214,0.35680388813238145,0.09300470598395795,0.26379918214842346,0.3689730530655152,30.47081976545599,37.464856870229006,26.57132470296152,24.511203174738068,25.24537518940176,0.8044156134757428,0.8285098787536335,24.511203174738068,25.24537518940176,0.8044156134757428,0.8285098787536335,0.4419259738163702,0.4551627651813639,298,598,42,42,32.382179836512265,164.57999999999998,0.8798671800000001,0.0,0.0018421303155608454,0.0017813746927527884,0.0017813746927527884,0.030851548269581055,1.0,1.0,0.254416125535358,0.2889528984870114,55.4645,55.4645,,none,0,271,7661,852,0.9995445747466697,0.7943725226201258,0.9997723132969034,OK,298.0,598.0
DE,2021,8760,8759,8759,8760,8760,0.00011415525114155251,0.00011415525114155251,0.0,0.00011415525114155251,minus_psh_pump,observed,"DE_AT_LU,DE_LU",08c9fdcad24ab9af3184de28e095a15f6393e683a1028e3c18c87608cb7ca633,509.6973813775,499.18620870750004,46.4220778,89.86921309,24.0098839125,160.30117480250001,504.186187665,150.0659387725,23.4870805,0.3179404329676125,0.09207328351256729,0.2258671494550452,0.32112500707412184,96.86022947825094,115.51968071519796,86.47433979029678,75.45790652091513,83.19114655913475,0.7790391053931841,0.8588782724060605,75.45790652091513,83.19114655913475,0.7790391053931841,0.8588782724060605,0.3017290382106689,0.33265148473173023,139,248,202,202,80.08633879781421,351.21000000000004,0.72547869,0.0,0.001453322782851753,0.0014389102830441578,0.0014389102830441578,0.02442922374429224,1.0,1.0,0.28457991137002403,0.3005868458306974,250.085,250.085,,none,0,214,7691,855,0.9704304144308711,0.5173371335649842,0.9997716894977169,OK,139.0,248.0
DE,2022,8760,8759,8759,8760,8760,0.00011415525114155251,0.00011415525114155251,0.0,0.00011415525114155251,minus_psh_pump,observed,"DE_AT_LU,DE_LU",d2d97d1ce7bee1bfcce2ac2adeafececfcff7195165c70c4d2b8bd14d851763f,487.25054390749995,473.6585899075,55.987503705,101.2674993075,24.7436552725,181.998658285,490.9224705575,152.84826037,28.8383439,0.3707279034881398,0.1140455103662695,0.2566823931218703,0.384240172484874,235.46672222856492,267.36034935897436,217.82031033871255,222.26978029580732,173.5038161884555,0.9439541103394327,0.7368506876315086,222.26978029580732,173.5038161884555,0.9439541103394327,0.7368506876315086,0.427631029678141,0.3338088311915953,69,161,358,358,186.4810382513661,687.46,3.9815930525,0.0,0.00840603999872051,0.008110431465845176,0.008110431465845176,0.09920091324200914,1.0,1.0,0.3303288814071253,0.322660277243778,519.77,519.77,,none,0,869,7102,789,0.9316131978536363,0.5921283955916561,0.9997716894977169,OK,69.0,161.0
ES,2018,8760,8759,8757,8760,8760,0.00011415525114155251,0.00034246575342465754,0.0,0.00011415525114155251,minus_psh_pump,observed,ES,59edc76cd36a1fb56d32cc9a61fc9bedb32352778ce036ae583b0da40541c2fd,254.516312,251.148938,12.023741,48.902871,0.0,60.926612,246.072839,66.932674,1.6264807,0.24759584295282586,0.04886252805820637,0.19873331489461948,0.24259155736505644,57.300062792556226,61.49363026819923,54.96591434156745,59.342028861067455,53.09425838495249,1.0356363670298891,0.926600352554062,59.342028861067455,53.09425838495249,1.0356363670298891,0.926600352554062,0.8028523535604548,0.7183247880638646,0,57,5,5,18.345327868852458,63.3,0.072822,0.0,0.000289955436721775,0.0002959367652924913,0.0002959367652924913,0.009817351598173516,1.0,1.0,0.3089813620268453,0.2664146318284247,73.914,73.914,,none,0,86,7806,868,0.9923507249686038,0.743452289193609,0.9995433789954338,OK,0.0,57.0
ES,2019,8760,8759,8759,8760,8760,0.00011415525114155251,0.00011415525114155251,0.0,0.00011415525114155251,minus_psh_pump,observed,ES,57d9b3841908e0cac77f77bf02bcdfd2a8a7645f4917b38eac43d3792e51918a,249.964346,246.74796,14.421334,52.346548,0.0,66.767882,246.324252,67.57312,2.5393687999999996,0.27105687506563503,0.05854613941951603,0.212510735646119,0.2705914245451107,47.67961867793127,51.243438697318005,45.69598898169539,48.57853958864,45.65081383781028,1.0188533578001284,0.9574492226159511,48.57853958864,45.65081383781028,1.0188533578001284,0.9574492226159511,0.7557921367349668,0.7102421445011323,0,69,2,2,16.83762295081967,55.23,0.109492,0.0,0.0004437402440936087,0.00044450353187310194,0.00044450353187310194,0.010616438356164383,1.0,1.0,0.3036748524442235,0.2738235654451448,64.275,64.275,,none,0,93,7800,867,0.9932640712410092,0.7041166167477712,0.9997716894977169,OK,0.0,69.0
ES,2020,8784,8783,8783,8784,8784,0.00011384335154826958,0.00011384335154826958,0.0,0.00011384335154826958,minus_psh_pump,observed,ES,2a11bf132af5390284b3a95781cc63e9e48366a5967c4390a59d8fa1aae57d07,237.904532,233.058185,20.030933,53.148687,0.0,73.17962,238.656838,69.740548,5.5799319,0.3066311471033568,0.08393194667231786,0.222699200431039,0.3139972106107322,33.95808038255721,37.37387722646311,32.05361766270615,32.896135604866735,32.37432130900995,0.9687277736041889,0.9533613485890453,32.896135604866735,32.37432130900995,0.9687277736041889,0.9533613485890453,0.6308225743051842,0.6208161637840369,0,60,0,0,16.82008174386921,49.489999999999995,0.833753,0.001627,0.00357744569237077,0.0034935223603356383,0.0034935223603356383,0.04667577413479053,0.9980485827337353,0.9980485827337353,0.32694697911298387,0.29920686330873497,52.14799999999999,52.14799999999999,,none,1,409,7536,838,0.9945348969600364,0.738484478902048,0.9997723132969034,OK,0.0,60.0
ES,2021,8760,8759,8759,8760,8760,0.00011415525114155251,0.00011415525114155251,0.0,0.00011415525114155251,minus_psh_pump,observed,ES,91e8ccdd3850fe64732e5aec2b46a6fa90cc87e34b301772e5e9a9f0765705c4,243.928617,239.347595,25.354406,59.007867,0.0,84.362273,247.29159,66.875375,6.879464,0.3411449333962388,0.10252837955386998,0.23861655384236882,0.3524676026095019,111.94053088252083,119.24339399744571,107.87574195841478,102.39616733438757,103.78184356536731,0.9147371959656877,0.9271158779324007,102.39616733438757,103.78184356536731,0.9147371959656877,0.9271158779324007,0.39850619705930174,0.4038989825466718,0,202,130,130,49.48653005464481,248.98000000000002,1.29433,0.000548,0.005407741824186702,0.0052340235266391385,0.0052340235266391385,0.059817351598173515,0.9995766149281868,0.9995766149281868,0.3011517583195657,0.2793750270386953,256.95,256.95,,none,2,522,7412,824,0.9414316702819957,0.3850997910457044,0.9997716894977169,OK,0.0,202.0
ES,2022,8760,8759,8759,8760,8760,0.00011415525114155251,0.00011415525114155251,0.0,0.0028538812785388126,minus_psh_pump,observed,ES,1f9b313972dc9219f280cce5858a65c97a874b520e5057ba859b67e42188973b,236.074608,229.8533736,31.0917916,58.817717200000004,0.0,89.9095088,261.42073980000004,66.9526826,19.3090617,0.3439264569015652,0.11893391329160333,0.22499254360996188,0.3911602748823,167.52426875214064,170.57403846153846,165.83686291895728,151.07895653475305,160.5904117834413,0.9018332547284886,0.958609835933931,151.07895653475305,160.5904117834413,0.9018332547284886,0.958609835933931,0.5524031844748077,0.5871807490600939,0,114,329,329,94.1781693989071,281.45000000000005,2.142444,0.005393799999999999,0.009320916053763763,0.008195386493202785,0.008195386493202785,0.09440639269406392,0.9974824079415846,0.9974824079415846,0.32430274908945766,0.2912510638899894,273.49399999999997,273.49399999999997,,none,13,814,7140,793,0.9090078776115995,0.4968847220316642,0.9997716894977169,OK,0.0,114.0
ES,2023,8760,8759,8759,8760,8760,0.00011415525114155251,0.00011415525114155251,0.0,0.00011415525114155251,minus_psh_pump,observed,ES,823d7db4f2d488e067685a05be1b823289e5c560541ca3b22227de4780e94c84,229.124044,220.782428,40.4262,61.05184,0.0,101.47804,244.850968,64.702416,13.448894600000001,0.4144481879279317,0.16510533052089058,0.24934285740704118,0.4596291512837244,87.11351866651445,87.7176858974359,86.77923922681326,73.07910508828432,76.31964002657413,0.8388951130311212,0.8760941033588467,73.07910508828432,76.31964002657413,0.8388951130311212,0.8760941033588467,0.4852433556322538,0.506760423275593,0,558,273,273,73.0756830601093,190.0,7.30862,0.1082995,0.033103268526424576,0.029849259162414255,0.029849259162414255,0.21358447488584476,0.9851819495335645,0.9851819495335645,0.323024782884982,0.29302617271448816,150.603,150.603,,none,174,1697,6199,690,0.8813791528713324,0.766054563817711,0.9997716894977169,OK,0.0,558.0
ES,2024,8784,8783,8783,8784,8784,0.00011384335154826958,0.00011384335154826958,0.0,0.00011384335154826958,minus_psh_pump,observed,ES,7b926545becc351d1798edbf5659a6389dc97c559a709dc083a0937c00375591,232.02486,223.123972,47.252452,58.9115,0.0,106.163952,242.172744,64.546884,12.3539402,0.4383810921347945,0.19511878677808597,0.2432623053567085,0.4758070190683052,63.03954912899921,60.2145038167939,64.6146408937755,42.801173474764866,55.609473014267174,0.6789574809169381,0.8821362744913085,42.801173474764866,55.609473014267174,0.6789574809169381,0.8821362744913085,0.303382290011092,0.39416978320291446,247,1690,271,271,71.06787465940056,173.81,8.639112,0.2995817,0.03871888763256689,0.03567334563463508,0.03567334563463508,0.24533242258652094,0.9653226280664032,0.9653226280664032,0.317822347234112,0.2892541540377089,141.08,141.08,,none,338,1817,5966,663,0.9105089377205966,0.7025818862484758,0.9997723132969034,OK,247.0,1690.0
DE,2023,8760,8759,8759,8760,8760,0.00011415525114155251,0.00011415525114155251,0.0,0.00011415525114155251,minus_psh_pump,observed,"DE_AT_LU,DE_LU",665add90b6dbd1e6064d153dc4fc9879ade96a1336b5746ce7f0ed15e4701e76,463.039837155,450.36638116750004,55.798730455,119.46608692750002,23.5168147175,198.7816321,444.473392015,128.784043015,16.7474867,0.4472295432552947,0.1255389669155199,0.3216905763397747,0.441377599244179,95.1827480305971,106.2381314102564,89.06591948927115,72.18210511017934,79.91071132318326,0.7583528171195051,0.8395503699630048,72.18210511017934,79.91071132318326,0.7583528171195051,0.8395503699630048,0.42475053024702447,0.4702289709496485,300,530,340,340,97.58131147540985,594.9,6.0900480275,0.04532175250000007,0.013522430363724225,0.01370171564126942,0.01370171564126942,0.12990867579908677,0.9925580632048637,0.9925580632048637,0.2534351283923276,0.2859213010225441,169.94,169.94,,none,46,1092,6859,763,0.9554743692202307,0.8425914461889957,0.9997716894977169,OK,300.0,530.0
DE,2024,8784,8783,8783,8784,8784,0.00011384335154826958,0.00011384335154826958,0.0,0.00011384335154826958,minus_psh_pump,observed,"DE_AT_LU,DE_LU",b93be6909a4bd71719b1711c2cd72a4765db54dc541bc67c20b93bca4544aa88,470.357313537993,457.307284095493,63.44404522,112.996908715,25.661745662500003,202.1026995975,428.492190735,123.19544645750001,11.7971791,0.47166017016746503,0.1480634807163541,0.323596689451111,0.44194069639025857,78.51545827166116,87.85491730279898,73.30828338357865,46.22796099131209,65.83122843523844,0.5887752808034911,0.838449266989748,46.22796099131209,65.83122843523844,0.5887752808034911,0.838449266989748,0.3127631743940469,0.44539243215884755,457,756,315,315,110.90152588555858,828.93,6.656885419468001,0.06289054750000006,0.01455670104322663,0.015535604996789628,0.015535604996789628,0.11646174863387979,0.9905525567082651,0.9905525567082651,0.2383825230901549,0.26936247411545183,147.80499999999995,147.80499999999995,,none,57,966,6985,776,0.9806444267334624,0.7988162259598485,0.9997723132969034,OK,457.0,756.0
```

### Métriques annuelles prospectives (DE/ES)
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\inputs\annual_metrics_scenarios.csv`

```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm
DE,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:BASE,3c673d51e6f45cac5ae37faaed11ee61d33aef687f7d60b6535c9c52727efc1f,525.9034,524.423312869,31.697453747499996,98.74950692264126,21.756967075256217,152.20392774539746,176.5478818501475,22.6446,3.4586516,0.8621113215880268,0.17954026644400387,0.6825710551440229,0.2902310481063944,126.8851482532473,134.8957779383934,122.4272072131127,122.4715392464344,121.69258827712454,0.9652157162002611,0.9590766922086181,122.4715392464344,121.69258827712454,0.9652157162002611,0.9590766922086181,0.5978761206044051,0.5940734723602696,0,0,0,0,121,121,32.443118408552564,95.37989405474895,0.0,0.0,0.0,0.0,0.0,0.0,,,0.05069604702394818,0.04318000257485993,204.84433986529757,204.84433986529757,,none,0,0,7884,876,1.0,0.6729421509073772,1.0,OK,BASE,SCEN,2030,9425.893,21.1595,38.4164,5.8601,1.6500000000000001,0.45,0.8914973010374386,-26.5825,0.10500000000000001,-21.08173750012614
DE,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:BASE,61e8ec3925a709261922e373bc87c0c11ab25ca49e1bf3b6db221fa86737697c,617.3648,615.8812870144999,36.75064727891181,109.3064128317157,25.451076930673285,171.50813704130078,195.91705033430082,22.70664,3.4966016,0.8754120008883853,0.18758268979755854,0.687829311090827,0.2784759671343333,138.01219566964647,145.97391811676596,133.6002857785675,133.15273800112763,132.62324489460528,0.9647896503280717,0.9609530828134893,133.15273800112763,132.62324489460528,0.9647896503280717,0.9609530828134893,0.6001143033753848,0.5977278981723613,0,0,0,0,122,122,35.457981764211375,103.1412567759477,0.0,0.0,0.0,0.0,0.0,0.0,,,0.043264048243779316,0.036868533723554114,221.8789608116333,221.8789608116333,,none,0,0,7905,879,1.0,0.6808902763526699,1.0,OK,BASE,SCEN,2040,9425.893,24.5451,42.3232,6.8368,1.6500000000000001,0.45,0.8914973010374386,-26.5825,0.10500000000000001,-21.08173750012614
ES,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:BASE,f4745b5be052577b9c5a1b8dffadc62e0e29186528f69bdfb370d4d96195da76,256.5926,255.23969,31.101249710331462,46.29946036015223,0.0,77.4007100704837,120.57657087048369,22.644600000000004,6.6676834000000005,0.6419216395996451,0.2579377526313848,0.38398388696826025,0.30324715592031826,98.66115688731401,97.31064458352448,99.4127213037086,92.13420270147233,96.19877619118401,0.9338447430400959,0.9750420451795188,92.13420270147233,96.19877619118401,0.9338447430400959,0.9750420451795188,0.5703919152839889,0.5955552074125496,0,0,0,0,197,197,41.31304690736875,79.58802578261405,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0944955713769326,0.08871896059738986,161.5278902675193,161.5278902675193,,none,0,0,7884,876,1.0,0.7162492897942901,1.0,OK,BASE,SCEN,2030,6237.200000000001,13.6049,14.0905,2.1494,1.6500000000000001,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475
ES,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:BASE,dce1e53ca70c1a732fd92714fb132f899b3a6ee779f8d2b7648d26108105465b,301.2174,299.86286160000003,36.137043115351815,51.0458476562065,0.0,87.18289077155832,130.46665917155832,22.70664,6.671025300000001,0.6682388537052703,0.27698297285157797,0.39125588085369223,0.290742542462145,105.51371698585235,104.257888452442,106.20962196933453,98.40603141928085,103.01805804292654,0.9326373312436285,0.976347540260946,98.40603141928085,103.01805804292654,0.9326373312436285,0.976347540260946,0.5701749971834855,0.5968975692577833,0,0,0,0,198,198,44.54542933422071,85.78810122554783,0.0,0.0,0.0,0.0,0.0,0.0,,,0.08064739954379686,0.07572341529338623,172.5891733334165,172.5891733334165,,none,0,0,7905,879,1.0,0.7218755416093814,1.0,OK,BASE,SCEN,2040,6237.200000000001,15.7817,15.5234,2.5076,1.6500000000000001,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475
DE,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:DEMAND_UP,27e465e68b67d2c941180cca1c2006df1d46a847b0eea49f89f4e65ebffd0689,578.4937000000001,577.0136128690001,31.697453747499996,98.74950692264126,21.756967075256217,152.20392774539746,176.5478818501475,22.6446,3.4586516,0.8621113215880268,0.17954026644400387,0.6825710551440229,0.2637787468975233,128.6041244627808,137.37106632026098,123.72529327983342,124.33686924114802,123.64805811999652,0.9668186752216664,0.9614626174433574,124.33686924114802,123.64805811999652,0.9668186752216664,0.9614626174433574,0.5971518379471358,0.5938436894510023,0,0,0,0,119,119,32.89345644125173,97.58259643274272,0.0,0.0,0.0,0.0,0.0,0.0,,,0.04606303708740628,0.03924448140383999,208.21650598713427,208.21650598713427,,none,0,0,7884,876,1.0,0.6782905135897174,1.0,OK,DEMAND_UP,SCEN,2030,9425.893,21.1595,38.4164,5.8601,1.6500000000000001,0.45,0.8914973010374386,-26.5825,0.10500000000000001,-21.08173750012614
DE,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:DEMAND_UP,54e995b6e77f5907e9facb41bd5542b4a755f7068ce1391e5220f78244283858,679.1013,677.6177870144999,36.75064727891181,109.3064128317157,25.451076930673285,171.50813704130078,195.91705033430082,22.70664,3.4966016,0.8754120008883853,0.18758268979755854,0.687829311090827,0.25310453817474954,140.025314250469,148.6850412325381,135.2266120374753,135.34675865661825,134.9028395556721,0.9665877872233729,0.9634175097394596,135.34675865661825,134.9028395556721,0.9665877872233729,0.9634175097394596,0.5991217231431424,0.5971566847533442,0,0,0,0,121,121,36.289160701628525,105.72032655546892,0.0,0.0,0.0,0.0,0.0,0.0,,,0.03931190101673813,0.033509509985035435,225.90861494147683,225.90861494147683,,none,0,0,7905,879,1.0,0.68579579593025,1.0,OK,DEMAND_UP,SCEN,2040,9425.893,24.5451,42.3232,6.8368,1.6500000000000001,0.45,0.8914973010374386,-26.5825,0.10500000000000001,-21.08173750012614
ES,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:DEMAND_UP,08c732c86e912850ebbc702d88571c992a2db19749593b78709c89775e2b5540,282.2518,280.89889,31.101249710331462,46.29946036015223,0.0,77.4007100704837,120.57657087048369,22.644600000000004,6.6676834000000005,0.6419216395996451,0.2579377526313848,0.38398388696826025,0.27554651451447065,100.2119227992864,99.0544876129467,100.85603918230272,93.77119541313097,97.87297645108453,0.9357289311866064,0.9766599993008165,93.77119541313097,97.87297645108453,0.9357289311866064,0.9766599993008165,0.5700742879112846,0.5950107291508077,0,0,0,0,195,195,42.008991886179494,82.0703956245834,0.0,0.0,0.0,0.0,0.0,0.0,,,0.08583552164462828,0.08061477209824505,164.48943129272254,164.48943129272254,,none,0,0,7884,876,1.0,0.7213663787266826,1.0,OK,DEMAND_UP,SCEN,2030,6237.200000000001,13.6049,14.0905,2.1494,1.6500000000000001,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475
ES,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:DEMAND_UP,6409045417df95b541cc1594c2adaa7eac3ebe10896d1f8593e3b5b1c1d3f818,331.3391,329.9845616,36.137043115351815,51.0458476562065,0.0,87.18289077155832,130.46665917155832,22.70664,6.671025300000001,0.6682388537052703,0.27698297285157797,0.39125588085369223,0.2642029383097004,107.32957859597659,106.3439477786375,107.87575618265495,100.31173346110411,104.95432195259197,0.9346140623425913,0.9778695055505076,100.31173346110411,104.95432195259197,0.9346140623425913,0.9778695055505076,0.5696061837867059,0.595968474839665,0,0,0,0,197,197,45.595846875534555,88.70395134534763,0.0,0.0,0.0,0.0,0.0,0.0,,,0.07326076434136554,0.06881121919735289,176.10717073722418,176.10717073722418,,none,0,0,7905,879,1.0,0.7268893808842096,1.0,OK,DEMAND_UP,SCEN,2040,6237.200000000001,15.7817,15.5234,2.5076,1.6500000000000001,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475
DE,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:FLEX_UP,03f6358ad20b0a5f40421def3bba794d385757efeb418d334d14d73d3a1a1322,525.9034,524.1057758522501,31.697453747499996,98.74950692264126,21.756967075256217,152.20392774539746,176.5478818501475,22.6446,4.8190211,0.8621113215880268,0.17954026644400387,0.6825710551440229,0.2904068887580912,126.87562866427379,134.8857858302721,122.4179505825562,122.45418727107236,121.6822557604586,0.9651513735163352,0.959067214417062,122.45418727107236,121.6822557604586,0.9651513735163352,0.959067214417062,0.597791412501787,0.5940230315393383,0,0,0,0,121,121,32.46244925212925,95.4033539304072,0.0,0.0,0.0,0.0,0.0,0.0,,,0.05077107901863202,0.04320616380000305,204.84433986529757,204.84433986529757,,none,0,0,7884,876,1.0,0.6729174044621066,1.0,OK,FLEX_UP,SCEN,2030,9425.893,21.1595,38.4164,5.8601,2.4375,0.35,0.8914973010374386,-26.5825,0.10500000000000001,-21.08173750012614
DE,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:FLEX_UP,5c538bf0b2662e4071ad6ea87a6fa3ee76b537b3467f56416646790ae069c283,617.3648,615.5633899977499,36.75064727891181,109.3064128317157,25.451076930673285,171.50813704130078,195.91705033430082,22.70664,4.8740938,0.8754120008883853,0.18758268979755854,0.687829311090827,0.2786197812087683,138.00269393782315,145.96435759007062,133.5908166273421,133.13539945763245,132.61294875607456,0.9647304386508305,0.9609446379055692,133.13539945763245,132.61294875607456,0.9647304386508305,0.9609446379055692,0.6000361592222314,0.5976814938693437,0,0,0,0,122,122,35.47685301428027,103.16471665160596,0.0,0.0,0.0,0.0,0.0,0.0,,,0.043313538462713214,0.036887573837168904,221.8789608116333,221.8789608116333,,none,0,0,7905,879,1.0,0.6808667111263013,1.0,OK,FLEX_UP,SCEN,2040,9425.893,24.5451,42.3232,6.8368,2.4375,0.35,0.8914973010374386,-26.5825,0.10500000000000001,-21.08173750012614
ES,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:FLEX_UP,122858f11c51bd8db0d818b3df452676fde034f7afd7256c62c2352b394a8110,256.5926,254.955638,31.101249710331462,46.29946036015223,0.0,77.4007100704837,120.57657087048369,22.644600000000004,8.7176561,0.6419216395996451,0.2579377526313848,0.38398388696826025,0.3035850106224507,98.64545138178808,97.28700685315945,99.40143010667519,92.10420292763541,96.18188646279201,0.9336893048536417,0.9750260667421824,92.10420292763541,96.18188646279201,0.9336893048536417,0.9750260667421824,0.5702061902442622,0.5954506451083925,0,0,0,0,197,197,41.35050447623986,79.63159560325163,0.0,0.0,0.0,0.0,0.0,0.0,,,0.09460179329127333,0.08881780445271034,161.5278902675193,161.5278902675193,,none,0,0,7884,876,1.0,0.7153709736484742,1.0,OK,FLEX_UP,SCEN,2030,6237.200000000001,13.6049,14.0905,2.1494,2.4375,0.35,0.8687903652597629,-0.02,8.33,-19.73003920827475
ES,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:FLEX_UP,802762580d7d0d4956576acb8e70a0c9479817f5723f22ad0d31e2c6f3863d8c,301.2174,299.57876039999996,36.137043115351815,51.0458476562065,0.0,87.18289077155832,130.46665917155832,22.70664,8.720998,0.6682388537052703,0.27698297285157797,0.39125588085369223,0.2910182639622082,105.49805168000357,104.23534303346838,106.19776921024919,98.37607547031715,103.0011759228295,0.9324918697902708,0.9763324941322369,98.37607547031715,103.0011759228295,0.9324918697902708,0.9763324941322369,0.5700014292337403,0.5967997524609878,0,0,0,0,198,198,44.58258671337139,85.8316710461854,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0807263472501742,0.07579522650298008,172.5891733334165,172.5891733334165,,none,0,0,7905,879,1.0,0.7211496720486239,1.0,OK,FLEX_UP,SCEN,2040,6237.200000000001,15.7817,15.5234,2.5076,2.4375,0.35,0.8687903652597629,-0.02,8.33,-19.73003920827475
DE,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:HIGH_CO2,795ee0abfe8a551ee309b48f5ae25dfab04b30a852354c5a00d6723b03bfdba1,525.9034,524.423312869,31.697453747499996,98.74950692264126,21.756967075256217,152.20392774539746,176.5478818501475,22.6446,3.4586516,0.8621113215880268,0.17954026644400387,0.6825710551440229,0.2902310481063944,137.3843587795631,145.73640104789126,132.73642054494977,132.7682232005389,131.99277182212148,0.9663998462413694,0.9607554527652413,132.7682232005389,131.99277182212148,0.9663998462413694,0.9607554527652413,0.6063087998823109,0.6027675685297967,0,0,0,0,121,121,33.778137821839884,99.4180519494858,0.0,0.0,0.0,0.0,0.0,0.0,,,0.05069604702394818,0.04318000257485993,218.97789249687654,218.97789249687654,,none,0,0,7884,876,1.0,0.6697974141701357,1.0,OK,HIGH_CO2,SCEN,2030,9425.893,21.1595,38.4164,5.8601,1.6500000000000001,0.45,0.8914973010374386,-26.5825,0.10500000000000001,-21.08173750012614
DE,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:HIGH_CO2,f3555e16470f1919c1e88006de1810dc781f1aadff65fcca7d16fb7236d44422,617.3648,615.8812870144999,36.75064727891181,109.3064128317157,25.451076930673285,171.50813704130078,195.91705033430082,22.70664,3.4966016,0.8754120008883853,0.18758268979755854,0.687829311090827,0.2784759671343333,150.84490121681358,159.1747175891058,146.22901571114846,145.73395548404667,145.2226148422671,0.966117875436699,0.9627280317120867,145.73395548404667,145.2226148422671,0.966117875436699,0.9627280317120867,0.6093746300241895,0.6072365009013929,0,0,0,0,122,122,37.09867443594519,108.07678309173713,0.0,0.0,0.0,0.0,0.0,0.0,,,0.043264048243779316,0.036868533723554114,239.15330291689645,239.15330291689645,,none,0,0,7905,879,1.0,0.6771769965967225,1.0,OK,HIGH_CO2,SCEN,2040,9425.893,24.5451,42.3232,6.8368,1.6500000000000001,0.45,0.8914973010374386,-26.5825,0.10500000000000001,-21.08173750012614
ES,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:HIGH_CO2,2bc97d936b7e2eaec1b5d32a43d6bb4b84f719970bf3c551c6121e161483136b,256.5926,255.23969,31.101249710331462,46.29946036015223,0.0,77.4007100704837,120.57657087048369,22.644600000000004,6.6676834000000005,0.6419216395996451,0.2579377526313848,0.38398388696826025,0.30324715592031826,102.9582477964049,101.58441156367076,103.72279205385395,96.30062690358723,100.4440585703068,0.9353366919570852,0.9755804971441453,96.30062690358723,100.4440585703068,0.9353366919570852,0.9755804971441453,0.5755736355638228,0.6003382721482935,0,0,0,0,197,197,42.202629619738346,81.24075305534133,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0944955713769326,0.08871896059738986,167.31243572206478,167.31243572206478,,none,0,0,7884,876,1.0,0.71470883497246,1.0,OK,HIGH_CO2,SCEN,2030,6237.200000000001,13.6049,14.0905,2.1494,1.6500000000000001,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475
ES,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:HIGH_CO2,c000c326671768c97f3f39256ca409002ede415a32987fee83d7f31dae43d91d,301.2174,299.86286160000003,36.137043115351815,51.0458476562065,0.0,87.18289077155832,130.46665917155832,22.70664,6.671025300000001,0.6682388537052703,0.27698297285157797,0.39125588085369223,0.290742542462145,110.76585496399444,109.48331629407676,111.47656110592337,103.49761706397925,108.21021537791208,0.9343819636260848,0.9769275505803381,103.49761706397925,108.21021537791208,0.9343819636260848,0.9769275505803381,0.576077553646011,0.6023083228658329,0,0,0,0,198,198,45.6352385985259,87.80810122554783,0.0,0.0,0.0,0.0,0.0,0.0,,,0.08064739954379686,0.07572341529338623,179.65917333341653,179.65917333341653,,none,0,0,7905,879,1.0,0.7199931117432893,1.0,OK,HIGH_CO2,SCEN,2040,6237.200000000001,15.7817,15.5234,2.5076,1.6500000000000001,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475
DE,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:HIGH_GAS,db7553debe836954275fe59471b10bde27aad0964d52317289a3eae8f0d7bcd3,525.9034,524.423312869,31.697453747499996,98.74950692264126,21.756967075256217,152.20392774539746,176.5478818501475,22.6446,3.4586516,0.8621113215880268,0.17954026644400387,0.6825710551440229,0.2902310481063944,141.25356930587887,149.73143028765733,136.5356125548252,136.56279783465166,135.78863613929045,0.9667918375848646,0.9613111853141613,136.56279783465166,135.78863613929045,0.9667918375848646,0.9613111853141613,0.6091483263245608,0.6056951215827772,0,0,0,0,121,121,34.27012444824196,100.90620984422264,0.0,0.0,0.0,0.0,0.0,0.0,,,0.05069604702394818,0.04318000257485993,224.1864451284555,224.1864451284555,,none,0,0,7884,876,1.0,0.6687040869626171,1.0,OK,HIGH_GAS,SCEN,2030,9425.893,21.1595,38.4164,5.8601,1.6500000000000001,0.45,0.8914973010374386,-26.5825,0.10500000000000001,-21.08173750012614
DE,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:HIGH_GAS,95128d6b65057fd35d18eaee73a65115cc09772f185c9617933f9dcbc3487cbd,617.3648,615.8812870144999,36.75064727891181,109.3064128317157,25.451076930673285,171.50813704130078,195.91705033430082,22.70664,3.4966016,0.8754120008883853,0.18758268979755854,0.687829311090827,0.2784759671343333,154.43367970761022,162.86643676972017,149.76075063497606,149.25240313522823,148.74613898918716,0.966449827639983,0.9631716298595533,149.25240313522823,148.74613898918716,0.966449827639983,0.9631716298595533,0.6117297286970032,0.6096547414793693,0,0,0,0,122,122,37.557508510231735,109.4570462496319,0.0,0.0,0.0,0.0,0.0,0.0,,,0.043264048243779316,0.036868533723554114,243.98422396952805,243.98422396952805,,none,0,0,7905,879,1.0,0.6762004267817918,1.0,OK,HIGH_GAS,SCEN,2040,9425.893,24.5451,42.3232,6.8368,1.6500000000000001,0.45,0.8914973010374386,-26.5825,0.10500000000000001,-21.08173750012614
ES,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:HIGH_GAS,407ed2414a631aa7b9dd4021f1b71fc6876b06d6526a85a66394908884f40494,256.5926,255.23969,31.101249710331462,46.29946036015223,0.0,77.4007100704837,120.57657087048369,22.644600000000004,6.6676834000000005,0.6419216395996451,0.2579377526313848,0.38398388696826025,0.30324715592031826,108.58842961458673,107.18403364656872,109.36998046246029,101.75960514860247,106.00635924526304,0.937112779969083,0.9762214963556592,101.75960514860247,106.00635924526304,0.937112779969083,0.9762214963556592,0.5818441127980567,0.6061263303443472,0,0,0,0,197,197,43.3681884871005,83.40620760079588,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0944955713769326,0.08871896059738986,174.89152663115567,174.89152663115567,,none,0,0,7884,876,1.0,0.7127880822625251,1.0,OK,HIGH_GAS,SCEN,2030,6237.200000000001,13.6049,14.0905,2.1494,1.6500000000000001,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475
ES,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:HIGH_GAS,f5fccdb8f7b1bda1be059ff1827cdf7f83365eaed9bccad359e6374ac554b4e6,301.2174,299.86286160000003,36.137043115351815,51.0458476562065,0.0,87.18289077155832,130.46665917155832,22.70664,6.671025300000001,0.6682388537052703,0.27698297285157797,0.39125588085369223,0.290742542462145,116.85946959390007,115.54594139566737,117.58734827699716,109.40495630431789,114.23423950464145,0.9362095916104406,0.9775351531340883,109.40495630431789,114.23423950464145,0.9362095916104406,0.9775351531340883,0.5823690484942318,0.6080756083913779,0,0,0,0,198,198,46.89965276746321,90.15173758918418,0.0,0.0,0.0,0.0,0.0,0.0,,,0.08064739954379686,0.07572341529338623,187.8619006061438,187.8619006061438,,none,0,0,7905,879,1.0,0.7179210078489119,1.0,OK,HIGH_GAS,SCEN,2040,6237.200000000001,15.7817,15.5234,2.5076,1.6500000000000001,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475
DE,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:LOW_RIGIDITY,6822b3bcaa37e5fdfe6fe33a858fb86ff423e25f218903448d669bba4ef52b2b,525.9034,524.423312869,31.697453747499996,98.74950692264126,21.756967075256217,152.20392774539746,171.19552185014746,17.29224,3.4586516,0.8890648896682362,0.18515352156959877,0.7039113680986374,0.2902310481063944,127.05800620843969,135.0552260542705,122.60752778677266,122.6165086811288,121.86322563093229,0.9650435445994283,0.9591148898638837,122.6165086811288,121.86322563093229,0.9650435445994283,0.9591148898638837,0.5977187820637748,0.5940467526433022,0,0,0,0,122,122,32.72793668961861,95.55565577835456,0.0,0.0,0.0,0.0,0.0,0.0,,,0.03871334500010588,0.03297382014807486,205.14079925306075,205.14079925306075,,none,0,0,7884,876,1.0,0.6730077697988456,1.0,OK,LOW_RIGIDITY,SCEN,2030,9425.893,21.1595,38.4164,5.8601,1.6500000000000001,0.45,0.8914973010374386,-26.5825,0.10500000000000001,-21.08173750012614
DE,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:LOW_RIGIDITY,44075226f72526b300818ad8076af9efa828b4f9f9333f44a7d2ef4878afafc9,617.3648,615.8812870144999,36.75064727891181,109.3064128317157,25.451076930673285,171.50813704130078,190.5500263343008,17.339616,3.4966016,0.9000688183606286,0.1928661359218944,0.7072026824387344,0.2784759671343333,138.18507049247427,146.1588580248104,133.76647485353644,133.31322818131866,132.79007724104682,0.9647440762320201,0.9609582045860644,133.31322818131866,132.79007724104682,0.9647440762320201,0.9609582045860644,0.5999659874227242,0.5976115866274452,0,0,0,0,122,122,35.52503700469273,103.31705810147854,0.0,0.0,0.0,0.0,0.0,0.0,,,0.03303800047706785,0.028154153025259504,222.20130970089272,222.20130970089272,,none,0,0,7905,879,1.0,0.6809304253072952,1.0,OK,LOW_RIGIDITY,SCEN,2040,9425.893,24.5451,42.3232,6.8368,1.6500000000000001,0.45,0.8914973010374386,-26.5825,0.10500000000000001,-21.08173750012614
ES,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:LOW_RIGIDITY,0a97a667845796f7f9d14e1303a8f2f68fde91570e85a6e1b8c8918b47c8eb24,256.5926,255.23969,31.101249710331462,46.29946036015223,0.0,77.4007100704837,115.2242108704837,17.29224,6.6676834000000005,0.6717399883734936,0.26991939866952464,0.40182058970396894,0.30324715592031826,98.98059642880098,97.6451187971206,99.72379400208153,92.44237525715238,96.53949978970414,0.933944415294045,0.9753376244721582,92.44237525715238,96.53949978970414,0.933944415294045,0.9753376244721582,0.570441195105838,0.5957236330391433,0,0,0,0,196,196,41.27425075912336,79.86783396069681,0.0,0.0,0.0,0.0,0.0,0.0,,,0.07216025450602126,0.0677490244561886,162.05417149089467,162.05417149089467,,none,0,0,7884,876,1.0,0.7158297461481474,1.0,OK,LOW_RIGIDITY,SCEN,2030,6237.200000000001,13.6049,14.0905,2.1494,1.6500000000000001,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475
ES,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:LOW_RIGIDITY,0a84191e7a1d1f5f2aafb74b583a46cff6215323bd67f93cf80faca90f1b5abf,301.2174,299.86286160000003,36.137043115351815,51.0458476562065,0.0,87.18289077155832,125.09963517155832,17.339616,6.671025300000001,0.6969076340790125,0.2888660951392419,0.4080415389397705,0.290742542462145,105.83318335371787,104.57387025083115,106.53101927697357,98.70838037659337,103.32908509984469,0.9326789315850792,0.9763391955668201,98.70838037659337,103.32908509984469,0.9326789315850792,0.9763391955668201,0.5702021567545948,0.5968942753859813,0,0,0,0,197,197,44.49741248034485,86.06799694489395,0.0,0.0,0.0,0.0,0.0,0.0,,,0.06158528692435397,0.05782515349676767,173.11120136480955,173.11120136480955,,none,0,0,7905,879,1.0,0.7214704573561171,1.0,OK,LOW_RIGIDITY,SCEN,2040,6237.200000000001,15.7817,15.5234,2.5076,1.6500000000000001,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475
```

### Validation findings historiques (DE/ES)
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\inputs\validation_findings_hist.csv`

```csv
severity,code,message,evidence,suggestion,country,year
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,DE,2018
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,DE,2019
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,DE,2020
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,DE,2021
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,DE,2022
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,ES,2018
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,ES,2019
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,ES,2020
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,ES,2021
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,ES,2022
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,ES,2023
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,ES,2024
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,DE,2023
PASS,ALL_CHECKS_PASS,No blocking issue detected,hard checks and reality checks passed,Proceed to interpretation.,DE,2024
```

## Q1

### Q1 - contexte
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\question_context.json`

```json
{
  "question_id": "Q1",
  "objective": "Identifier la bascule Phase 1 vers Phase 2 (marche et physique), puis expliquer les drivers SR/FAR/IR.",
  "countries_scope": [
    "DE",
    "ES"
  ],
  "run_id": "FULL_20260210_172152",
  "source_summary_file": "outputs\\combined\\FULL_20260210_172152\\Q1\\summary.json",
  "source_refs_in_ledger": [
    "SPEC2-Q1",
    "SPEC2-Q1/Slides 2-4",
    "SPEC2-Q1/Slides 3-4",
    "SPEC2-Q1/Slides 5",
    "Slides 4-6"
  ],
  "scenarios": [
    "BASE",
    "DEMAND_UP",
    "FLEX_UP",
    "LOW_RIGIDITY"
  ],
  "country_filter_notes": {
    "hist_unfilterable_tables": [],
    "scen_unfilterable_tables_by_scenario": {
      "BASE": [],
      "DEMAND_UP": [],
      "FLEX_UP": [],
      "LOW_RIGIDITY": []
    }
  }
}
```

### Q1 - test ledger
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\test_ledger.csv`

```csv
test_id,question_id,source_ref,mode,scenario_group,title,what_is_tested,metric_rule,severity_if_fail,scenario_id,status,value,threshold,interpretation
Q1-H-01,Q1,SPEC2-Q1/Slides 2-4,HIST,HIST_BASE,Score marche de bascule,La signature marche de phase 2 est calculee et exploitable.,stage2_market_score present et non vide,HIGH,,PASS,4.1020408163265305,score present,Le score de bascule marche est exploitable.
Q1-H-02,Q1,SPEC2-Q1/Slides 3-4,HIST,HIST_BASE,Stress physique SR/FAR/IR,La bascule physique est fondee sur SR/FAR/IR.,sr_energy/far_energy/ir_p10 presentes,CRITICAL,,PASS,"far_energy,ir_p10,sr_energy",SR/FAR/IR presents,Le stress physique est calculable.
Q1-H-03,Q1,SPEC2-Q1,HIST,HIST_BASE,Concordance marche vs physique,La relation entre bascule marche et bascule physique est mesurable.,bascule_year_market et bascule_year_physical comparables,MEDIUM,,PASS,strict=42.86%; concordant_ou_explique=100.00%,concordant_ou_explique >= 80%,Concordance satisfaisante en comptant les divergences expliquees (pas de stress physique structurel).
Q1-H-04,Q1,Slides 4-6,HIST,HIST_BASE,Robustesse seuils,Le diagnostic reste stable sous variation raisonnable de seuils.,delta bascules sous choc de seuil <= 50%,MEDIUM,,PASS,0.957,confidence moyenne >=0.60,Proxy de robustesse du diagnostic de bascule.
Q1-S-01,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Bascule projetee par scenario,Chaque scenario fournit un diagnostic de bascule projetee.,Q1_country_summary non vide en SCEN,HIGH,BASE,PASS,7,>0 lignes,La bascule projetee est produite.
Q1-S-01,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Bascule projetee par scenario,Chaque scenario fournit un diagnostic de bascule projetee.,Q1_country_summary non vide en SCEN,HIGH,DEMAND_UP,PASS,7,>0 lignes,La bascule projetee est produite.
Q1-S-01,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Bascule projetee par scenario,Chaque scenario fournit un diagnostic de bascule projetee.,Q1_country_summary non vide en SCEN,HIGH,FLEX_UP,PASS,7,>0 lignes,La bascule projetee est produite.
Q1-S-01,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Bascule projetee par scenario,Chaque scenario fournit un diagnostic de bascule projetee.,Q1_country_summary non vide en SCEN,HIGH,LOW_RIGIDITY,PASS,7,>0 lignes,La bascule projetee est produite.
Q1-S-02,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY,Les leviers scenario modifient la bascule vs BASE.,delta bascule_year_market vs BASE calculable,MEDIUM,BASE,PASS,2,>=1 bascule,Le scenario fournit une variation exploitable.
Q1-S-02,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY,Les leviers scenario modifient la bascule vs BASE.,delta bascule_year_market vs BASE calculable,MEDIUM,DEMAND_UP,PASS,1,>=1 bascule,Le scenario fournit une variation exploitable.
Q1-S-02,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY,Les leviers scenario modifient la bascule vs BASE.,delta bascule_year_market vs BASE calculable,MEDIUM,FLEX_UP,PASS,2,>=1 bascule,Le scenario fournit une variation exploitable.
Q1-S-02,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY,Les leviers scenario modifient la bascule vs BASE.,delta bascule_year_market vs BASE calculable,MEDIUM,LOW_RIGIDITY,PASS,1,>=1 bascule,Le scenario fournit une variation exploitable.
Q1-S-03,Q1,SPEC2-Q1,SCEN,DEFAULT,Qualite de causalite,Le regime_coherence respecte le seuil d'interpretation.,part regime_coherence >= seuil min,MEDIUM,BASE,PASS,100.00%,>=50% lignes >=0.55,La coherence scenario est lisible.
Q1-S-03,Q1,SPEC2-Q1,SCEN,DEFAULT,Qualite de causalite,Le regime_coherence respecte le seuil d'interpretation.,part regime_coherence >= seuil min,MEDIUM,DEMAND_UP,PASS,100.00%,>=50% lignes >=0.55,La coherence scenario est lisible.
Q1-S-03,Q1,SPEC2-Q1,SCEN,DEFAULT,Qualite de causalite,Le regime_coherence respecte le seuil d'interpretation.,part regime_coherence >= seuil min,MEDIUM,FLEX_UP,PASS,100.00%,>=50% lignes >=0.55,La coherence scenario est lisible.
Q1-S-03,Q1,SPEC2-Q1,SCEN,DEFAULT,Qualite de causalite,Le regime_coherence respecte le seuil d'interpretation.,part regime_coherence >= seuil min,MEDIUM,LOW_RIGIDITY,PASS,100.00%,>=50% lignes >=0.55,La coherence scenario est lisible.
```

### Q1 - comparaison HIST vs SCEN
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\comparison_hist_vs_scen.csv`

```csv
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
DE,BASE,bascule_year_market,2019.0,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,BASE,bascule_year_market,2022.0,2030.0,8.0,,INFORMATIVE,delta_interpretable
DE,DEMAND_UP,bascule_year_market,2019.0,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,DEMAND_UP,bascule_year_market,2022.0,2030.0,8.0,,INFORMATIVE,delta_interpretable
DE,FLEX_UP,bascule_year_market,2019.0,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,FLEX_UP,bascule_year_market,2022.0,2030.0,8.0,,INFORMATIVE,delta_interpretable
DE,LOW_RIGIDITY,bascule_year_market,2019.0,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,LOW_RIGIDITY,bascule_year_market,2022.0,2030.0,8.0,,INFORMATIVE,delta_interpretable
```

### Q1 - checks filtrés
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\checks_filtered.csv`

```csv
status,code,message,scope,scenario_id,question_id,mentioned_countries,is_global
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2018: signal stage2 majoritairement capture-only.,HIST,,Q1,DE,False
WARN,Q1_CAPTURE_ONLY_SIGNAL,ES 2019: signal stage2 majoritairement capture-only.,HIST,,Q1,ES,False
WARN,Q1_CAPTURE_ONLY_SIGNAL,ES 2020: signal stage2 majoritairement capture-only.,HIST,,Q1,ES,False
WARN,Q1_CAPTURE_ONLY_SIGNAL,ES 2021: signal stage2 majoritairement capture-only.,HIST,,Q1,ES,False
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2030: signal stage2 majoritairement capture-only.,SCEN,BASE,Q1,DE,False
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2040: signal stage2 majoritairement capture-only.,SCEN,BASE,Q1,DE,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,SCEN,BASE,Q1,,True
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2030: signal stage2 majoritairement capture-only.,SCEN,DEMAND_UP,Q1,DE,False
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2040: signal stage2 majoritairement capture-only.,SCEN,DEMAND_UP,Q1,DE,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,SCEN,DEMAND_UP,Q1,,True
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2030: signal stage2 majoritairement capture-only.,SCEN,FLEX_UP,Q1,DE,False
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2040: signal stage2 majoritairement capture-only.,SCEN,FLEX_UP,Q1,DE,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,SCEN,FLEX_UP,Q1,,True
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2030: signal stage2 majoritairement capture-only.,SCEN,LOW_RIGIDITY,Q1,DE,False
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2040: signal stage2 majoritairement capture-only.,SCEN,LOW_RIGIDITY,Q1,DE,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,SCEN,LOW_RIGIDITY,Q1,,True
PASS,BUNDLE_LEDGER_STATUS,"ledger: FAIL=0, WARN=0",BUNDLE,,Q1,,True
WARN,BUNDLE_INFORMATIVENESS,share_tests_informatifs=100.00% ; share_compare_informatifs=21.43%,BUNDLE,,Q1,,True
```

### Q1 - warnings filtrés
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\warnings_filtered.csv`

```csv

```

### Q1 - historique - Q1_country_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\hist\tables\Q1_country_summary.csv`

```csv
country,bascule_year_market,bascule_year_physical,bascule_confidence,drivers_at_bascule,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,h_negative_at_bascule,notes_quality
DE,2019,,1.0,"h_negative, capture_ratio",0.0024665861472393,0.9726354077376408,0.3020039544090348,58.596,0.5957093107616995,211,ok
ES,2022,,1.0,capture_ratio,0.0081953864932027,0.9974824079415846,0.3243027490894576,273.494,0.5524031844748077,0,ok
```

### Q1 - historique - Q1_year_panel.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\hist\tables\Q1_year_panel.csv`

```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative_obs,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,h_negative,h_below_5,stage2_market_score,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_stage2,flag_days_spread_stage2,flag_non_capture_stage2,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,phase_market,stress_phys_state,quality_ok,flag_sr_stress,flag_far_tension,flag_ir_high
DE,2018,8760,8760,8750,8760,8760,0.0,0.0011415525114155,0.0,0.0001141552511415,minus_psh_pump,observed,"DE_AT_LU,DE_LU",d09251118754e4daccbc432c71f13ae370edd44e7a89e70648f6c5593e7047bf,559.9527225899999,546.468202485,42.53518894,93.8429561475,19.0654565625,155.44360164999998,575.9773977325,205.2173406475,34.114891,0.2698779539994941,0.0738487119589274,0.1960292420405667,0.2844513202106516,44.47275456621005,52.1181577266922,40.218063255152806,43.77257363689873,38.17753675887097,0.9842559576949768,0.8584477649576012,43.77257363689873,38.17753675887097,0.9842559576949768,0.8584477649576012,0.6027951641084436,0.525745521081731,133,232,38,38,32.14734972677596,99.53,1.0689941175000002,0.0,0.001956187226702,0.0018559653932748,0.0018559653932748,0.0325342465753424,1.0,1.0,0.4059062367977894,0.3751052180982559,72.61599999999999,72.61599999999999,,none,0,285,7628,847,0.9843607305936072,0.7143395206268766,0.9988584474885844,OK,133.0,232.0,3,False,False,True,False,0,True,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
DE,2019,8760,8759,8759,8760,8760,0.0001141552511415,0.0001141552511415,0.0,0.0001141552511415,minus_psh_pump,observed,"DE_AT_LU,DE_LU",6b1885d2f025c19044eb8b2114907646d0a46055c4e549b3cb8cf747514b1f18,502.4789179925,491.506586445,41.83308617,99.9897749475,24.3804648275,166.203325945,515.6919337375,156.9665405575,34.1900773,0.3222918860499408,0.0811203034858677,0.2411715825640731,0.3381507603939266,37.669692887315904,44.45564814814815,33.892615958770214,34.906182773392544,32.78952818581776,0.926638368882113,0.8704485137137555,34.906182773392544,32.78952818581776,0.926638368882113,0.8704485137137555,0.5957093107616995,0.5595864595845751,211,335,31,31,29.95035519125683,117.32,1.27199858,0.0348077224999999,0.0025879583612504,0.0024665861472393,0.0024665861472393,0.0399543378995433,0.9726354077376408,0.9726354077376408,0.3020039544090348,0.3193215031721746,58.596,58.596,,none,8,342,7569,841,0.9982874757392396,0.8187692611447057,0.9997716894977168,OK,211.0,335.0,4,True,False,True,False,1,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
DE,2020,8784,8783,8783,8784,8784,0.0001138433515482,0.0001138433515482,0.0,0.0001138433515482,minus_psh_pump,observed,"DE_AT_LU,DE_LU",a7cab4363eb99fae2c73215fa1f13fa3261829e9946ac6fa91f6de4b6830b3aa,490.2538991575,477.6356876425001,45.93743737,103.4146983125,26.88256224,176.2346979225,493.9259458325,138.029930155,21.1321214,0.3568038881323814,0.0930047059839579,0.2637991821484234,0.3689730530655152,30.47081976545599,37.464856870229006,26.57132470296152,24.511203174738068,25.24537518940176,0.8044156134757428,0.8285098787536335,24.511203174738068,25.24537518940176,0.8044156134757428,0.8285098787536335,0.4419259738163702,0.4551627651813639,298,598,42,42,32.382179836512265,164.57999999999998,0.8798671800000001,0.0,0.0018421303155608,0.0017813746927527,0.0017813746927527,0.030851548269581,1.0,1.0,0.254416125535358,0.2889528984870114,55.4645,55.4645,,none,0,271,7661,852,0.9995445747466696,0.7943725226201258,0.9997723132969034,OK,298.0,598.0,5,True,True,True,False,2,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
DE,2021,8760,8759,8759,8760,8760,0.0001141552511415,0.0001141552511415,0.0,0.0001141552511415,minus_psh_pump,observed,"DE_AT_LU,DE_LU",08c9fdcad24ab9af3184de28e095a15f6393e683a1028e3c18c87608cb7ca633,509.6973813775,499.1862087075,46.4220778,89.86921309,24.0098839125,160.3011748025,504.186187665,150.0659387725,23.4870805,0.3179404329676125,0.0920732835125672,0.2258671494550452,0.3211250070741218,96.86022947825094,115.51968071519796,86.47433979029678,75.45790652091513,83.19114655913475,0.7790391053931841,0.8588782724060605,75.45790652091513,83.19114655913475,0.7790391053931841,0.8588782724060605,0.3017290382106689,0.3326514847317302,139,248,202,202,80.08633879781421,351.21000000000004,0.72547869,0.0,0.0014533227828517,0.0014389102830441,0.0014389102830441,0.0244292237442922,1.0,1.0,0.284579911370024,0.3005868458306974,250.085,250.085,,none,0,214,7691,855,0.9704304144308712,0.5173371335649842,0.9997716894977168,OK,139.0,248.0,4,False,False,True,True,1,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
DE,2022,8760,8759,8759,8760,8760,0.0001141552511415,0.0001141552511415,0.0,0.0001141552511415,minus_psh_pump,observed,"DE_AT_LU,DE_LU",d2d97d1ce7bee1bfcce2ac2adeafececfcff7195165c70c4d2b8bd14d851763f,487.2505439075,473.6585899075,55.987503705,101.2674993075,24.7436552725,181.998658285,490.9224705575,152.84826037,28.8383439,0.3707279034881398,0.1140455103662695,0.2566823931218703,0.384240172484874,235.4667222285649,267.3603493589744,217.82031033871252,222.2697802958073,173.5038161884555,0.9439541103394328,0.7368506876315086,222.2697802958073,173.5038161884555,0.9439541103394328,0.7368506876315086,0.427631029678141,0.3338088311915953,69,161,358,358,186.4810382513661,687.46,3.9815930525,0.0,0.0084060399987205,0.0081104314658451,0.0081104314658451,0.0992009132420091,1.0,1.0,0.3303288814071253,0.322660277243778,519.77,519.77,,none,0,869,7102,789,0.9316131978536364,0.5921283955916561,0.9997716894977168,OK,69.0,161.0,4,False,False,True,True,1,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
DE,2023,8760,8759,8759,8760,8760,0.0001141552511415,0.0001141552511415,0.0,0.0001141552511415,minus_psh_pump,observed,"DE_AT_LU,DE_LU",665add90b6dbd1e6064d153dc4fc9879ade96a1336b5746ce7f0ed15e4701e76,463.039837155,450.3663811675,55.798730455,119.46608692750002,23.5168147175,198.7816321,444.473392015,128.784043015,16.7474867,0.4472295432552947,0.1255389669155199,0.3216905763397747,0.441377599244179,95.1827480305971,106.2381314102564,89.06591948927115,72.18210511017934,79.91071132318326,0.7583528171195051,0.8395503699630048,72.18210511017934,79.91071132318326,0.7583528171195051,0.8395503699630048,0.4247505302470244,0.4702289709496485,300,530,340,340,97.58131147540983,594.9,6.0900480275,0.0453217525,0.0135224303637242,0.0137017156412694,0.0137017156412694,0.1299086757990867,0.9925580632048636,0.9925580632048636,0.2534351283923276,0.2859213010225441,169.94,169.94,,none,46,1092,6859,763,0.9554743692202308,0.8425914461889957,0.9997716894977168,OK,300.0,530.0,8,True,True,True,True,3,False,False,True,phase2,surplus_present_mais_absorbe,True,True,False,False
DE,2024,8784,8783,8783,8784,8784,0.0001138433515482,0.0001138433515482,0.0,0.0001138433515482,minus_psh_pump,observed,"DE_AT_LU,DE_LU",b93be6909a4bd71719b1711c2cd72a4765db54dc541bc67c20b93bca4544aa88,470.357313537993,457.307284095493,63.44404522,112.996908715,25.661745662500003,202.1026995975,428.492190735,123.1954464575,11.7971791,0.471660170167465,0.1480634807163541,0.323596689451111,0.4419406963902585,78.51545827166116,87.85491730279898,73.30828338357865,46.22796099131209,65.83122843523844,0.5887752808034911,0.838449266989748,46.22796099131209,65.83122843523844,0.5887752808034911,0.838449266989748,0.3127631743940469,0.4453924321588475,457,756,315,315,110.90152588555858,828.93,6.656885419468001,0.0628905475,0.0145567010432266,0.0155356049967896,0.0155356049967896,0.1164617486338797,0.9905525567082653,0.9905525567082653,0.2383825230901549,0.2693624741154518,147.80499999999995,147.80499999999995,,none,57,966,6985,776,0.9806444267334624,0.7988162259598485,0.9997723132969034,OK,457.0,756.0,8,True,True,True,True,3,False,False,True,phase2,surplus_present_mais_absorbe,True,True,False,False
ES,2018,8760,8759,8757,8760,8760,0.0001141552511415,0.0003424657534246,0.0,0.0001141552511415,minus_psh_pump,observed,ES,59edc76cd36a1fb56d32cc9a61fc9bedb32352778ce036ae583b0da40541c2fd,254.516312,251.148938,12.023741,48.902871,0.0,60.926612,246.072839,66.932674,1.6264807,0.2475958429528258,0.0488625280582063,0.1987333148946194,0.2425915573650564,57.30006279255623,61.49363026819923,54.96591434156745,59.342028861067455,53.09425838495249,1.0356363670298891,0.926600352554062,59.342028861067455,53.09425838495249,1.0356363670298891,0.926600352554062,0.8028523535604548,0.7183247880638646,0,57,5,5,18.345327868852458,63.3,0.072822,0.0,0.0002899554367217,0.0002959367652924,0.0002959367652924,0.0098173515981735,1.0,1.0,0.3089813620268453,0.2664146318284247,73.914,73.914,,none,0,86,7806,868,0.9923507249686038,0.743452289193609,0.9995433789954338,OK,0.0,57.0,0,False,False,False,False,0,False,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
ES,2019,8760,8759,8759,8760,8760,0.0001141552511415,0.0001141552511415,0.0,0.0001141552511415,minus_psh_pump,observed,ES,57d9b3841908e0cac77f77bf02bcdfd2a8a7645f4917b38eac43d3792e51918a,249.964346,246.74796,14.421334,52.346548,0.0,66.767882,246.324252,67.57312,2.5393688,0.271056875065635,0.058546139419516,0.212510735646119,0.2705914245451107,47.67961867793127,51.243438697318005,45.69598898169539,48.57853958864,45.65081383781028,1.0188533578001284,0.9574492226159512,48.57853958864,45.65081383781028,1.0188533578001284,0.9574492226159512,0.7557921367349668,0.7102421445011323,0,69,2,2,16.83762295081967,55.23,0.109492,0.0,0.0004437402440936,0.0004445035318731,0.0004445035318731,0.0106164383561643,1.0,1.0,0.3036748524442235,0.2738235654451448,64.275,64.275,,none,0,93,7800,867,0.9932640712410092,0.7041166167477712,0.9997716894977168,OK,0.0,69.0,1,False,False,True,False,0,True,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
ES,2020,8784,8783,8783,8784,8784,0.0001138433515482,0.0001138433515482,0.0,0.0001138433515482,minus_psh_pump,observed,ES,2a11bf132af5390284b3a95781cc63e9e48366a5967c4390a59d8fa1aae57d07,237.904532,233.058185,20.030933,53.148687,0.0,73.17962,238.656838,69.740548,5.5799319,0.3066311471033568,0.0839319466723178,0.222699200431039,0.3139972106107322,33.95808038255721,37.37387722646311,32.05361766270615,32.896135604866735,32.37432130900995,0.9687277736041888,0.9533613485890452,32.896135604866735,32.37432130900995,0.9687277736041888,0.9533613485890452,0.6308225743051842,0.6208161637840369,0,60,0,0,16.82008174386921,49.49,0.833753,0.001627,0.0035774456923707,0.0034935223603356,0.0034935223603356,0.0466757741347905,0.9980485827337352,0.9980485827337352,0.3269469791129838,0.2992068633087349,52.14799999999999,52.14799999999999,,none,1,409,7536,838,0.9945348969600364,0.738484478902048,0.9997723132969034,OK,0.0,60.0,3,False,False,True,False,0,True,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
ES,2021,8760,8759,8759,8760,8760,0.0001141552511415,0.0001141552511415,0.0,0.0001141552511415,minus_psh_pump,observed,ES,91e8ccdd3850fe64732e5aec2b46a6fa90cc87e34b301772e5e9a9f0765705c4,243.928617,239.347595,25.354406,59.007867,0.0,84.362273,247.29159,66.875375,6.879464,0.3411449333962388,0.1025283795538699,0.2386165538423688,0.3524676026095019,111.94053088252085,119.24339399744572,107.87574195841478,102.39616733438756,103.78184356536732,0.9147371959656876,0.9271158779324008,102.39616733438756,103.78184356536732,0.9147371959656876,0.9271158779324008,0.3985061970593017,0.4038989825466718,0,202,130,130,49.48653005464481,248.98,1.29433,0.000548,0.0054077418241867,0.0052340235266391,0.0052340235266391,0.0598173515981735,0.9995766149281868,0.9995766149281868,0.3011517583195657,0.2793750270386953,256.95,256.95,,none,2,522,7412,824,0.9414316702819956,0.3850997910457044,0.9997716894977168,OK,0.0,202.0,3,False,False,True,False,0,True,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
ES,2022,8760,8759,8759,8760,8760,0.0001141552511415,0.0001141552511415,0.0,0.0028538812785388,minus_psh_pump,observed,ES,1f9b313972dc9219f280cce5858a65c97a874b520e5057ba859b67e42188973b,236.074608,229.8533736,31.0917916,58.8177172,0.0,89.9095088,261.42073980000004,66.9526826,19.3090617,0.3439264569015652,0.1189339132916033,0.2249925436099618,0.3911602748823,167.52426875214064,170.57403846153846,165.83686291895728,151.07895653475305,160.5904117834413,0.9018332547284886,0.958609835933931,151.07895653475305,160.5904117834413,0.9018332547284886,0.958609835933931,0.5524031844748077,0.5871807490600939,0,114,329,329,94.1781693989071,281.45000000000005,2.142444,0.0053937999999999,0.0093209160537637,0.0081953864932027,0.0081953864932027,0.0944063926940639,0.9974824079415846,0.9974824079415846,0.3243027490894576,0.2912510638899894,273.494,273.494,,none,13,814,7140,793,0.9090078776115996,0.4968847220316642,0.9997716894977168,OK,0.0,114.0,4,False,False,True,True,1,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
ES,2023,8760,8759,8759,8760,8760,0.0001141552511415,0.0001141552511415,0.0,0.0001141552511415,minus_psh_pump,observed,ES,823d7db4f2d488e067685a05be1b823289e5c560541ca3b22227de4780e94c84,229.124044,220.782428,40.4262,61.05184,0.0,101.47804,244.850968,64.702416,13.4488946,0.4144481879279317,0.1651053305208905,0.2493428574070411,0.4596291512837244,87.11351866651445,87.7176858974359,86.77923922681326,73.07910508828432,76.31964002657413,0.8388951130311212,0.8760941033588467,73.07910508828432,76.31964002657413,0.8388951130311212,0.8760941033588467,0.4852433556322538,0.506760423275593,0,558,273,273,73.0756830601093,190.0,7.30862,0.1082995,0.0331032685264245,0.0298492591624142,0.0298492591624142,0.2135844748858447,0.9851819495335644,0.9851819495335644,0.323024782884982,0.2930261727144881,150.603,150.603,,none,174,1697,6199,690,0.8813791528713324,0.766054563817711,0.9997716894977168,OK,0.0,558.0,5,False,True,True,True,2,False,False,True,phase2,surplus_present_mais_absorbe,True,True,False,False
ES,2024,8784,8783,8783,8784,8784,0.0001138433515482,0.0001138433515482,0.0,0.0001138433515482,minus_psh_pump,observed,ES,7b926545becc351d1798edbf5659a6389dc97c559a709dc083a0937c00375591,232.02486,223.123972,47.252452,58.9115,0.0,106.163952,242.172744,64.546884,12.3539402,0.4383810921347945,0.1951187867780859,0.2432623053567085,0.4758070190683052,63.03954912899921,60.2145038167939,64.6146408937755,42.80117347476487,55.60947301426717,0.6789574809169381,0.8821362744913085,42.80117347476487,55.60947301426717,0.6789574809169381,0.8821362744913085,0.303382290011092,0.3941697832029144,247,1690,271,271,71.06787465940056,173.81,8.639112,0.2995817,0.0387188876325668,0.035673345634635,0.035673345634635,0.2453324225865209,0.9653226280664032,0.9653226280664032,0.317822347234112,0.2892541540377089,141.08,141.08,,none,338,1817,5966,663,0.9105089377205966,0.7025818862484758,0.9997723132969034,OK,247.0,1690.0,6,True,True,True,True,3,False,False,True,phase2,surplus_present_mais_absorbe,True,True,False,False
```

### Q1 - scénario `BASE`

### Q1/BASE - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\BASE\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2030: signal stage2 majoritairement capture-only.,Q1,DE,False
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2040: signal stage2 majoritairement capture-only.,Q1,DE,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,Q1,,True
```

### Q1/BASE - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\BASE\warnings_filtered.csv`

```csv

```

### Q1/BASE - Q1_country_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\BASE\tables\Q1_country_summary.csv`

```csv
country,bascule_year_market,bascule_year_physical,bascule_confidence,drivers_at_bascule,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,h_negative_at_bascule,notes_quality
DE,,,0.0,capture_ratio,0.0,,0.0432640482437793,221.8789608116333,0.6001143033753848,0,ok
ES,2030.0,,1.0,capture_ratio,0.0,,0.0944955713769326,161.5278902675193,0.5703919152839889,0,ok
```

### Q1/BASE - Q1_year_panel.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\BASE\tables\Q1_year_panel.csv`

```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm,stage2_market_score,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_stage2,flag_days_spread_stage2,flag_non_capture_stage2,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,phase_market,stress_phys_state,quality_ok,flag_sr_stress,flag_far_tension,flag_ir_high
DE,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:BASE,3c673d51e6f45cac5ae37faaed11ee61d33aef687f7d60b6535c9c52727efc1f,525.9034,524.423312869,31.6974537475,98.74950692264126,21.756967075256217,152.20392774539746,176.5478818501475,22.6446,3.4586516,0.8621113215880268,0.1795402664440038,0.6825710551440229,0.2902310481063944,126.8851482532473,134.8957779383934,122.4272072131127,122.4715392464344,121.69258827712454,0.9652157162002613,0.959076692208618,122.4715392464344,121.69258827712454,0.9652157162002613,0.959076692208618,0.5978761206044051,0.5940734723602696,0,0,0,0,121,121,32.443118408552564,95.37989405474896,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0506960470239481,0.0431800025748599,204.8443398652976,204.8443398652976,,none,0,0,7884,876,1.0,0.6729421509073772,1.0,OK,BASE,SCEN,2030,9425.893,21.1595,38.4164,5.8601,1.65,0.45,0.8914973010374386,-26.5825,0.105,-21.08173750012614,3,False,False,True,False,0,True,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
DE,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:BASE,61e8ec3925a709261922e373bc87c0c11ab25ca49e1bf3b6db221fa86737697c,617.3648,615.8812870144999,36.75064727891181,109.3064128317157,25.451076930673285,171.50813704130078,195.9170503343008,22.70664,3.4966016,0.8754120008883853,0.1875826897975585,0.687829311090827,0.2784759671343333,138.01219566964647,145.97391811676596,133.6002857785675,133.15273800112763,132.62324489460528,0.9647896503280716,0.9609530828134892,133.15273800112763,132.62324489460528,0.9647896503280716,0.9609530828134892,0.6001143033753848,0.5977278981723613,0,0,0,0,122,122,35.457981764211375,103.1412567759477,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0432640482437793,0.0368685337235541,221.8789608116333,221.8789608116333,,none,0,0,7905,879,1.0,0.6808902763526699,1.0,OK,BASE,SCEN,2040,9425.893,24.5451,42.3232,6.8368,1.65,0.45,0.8914973010374386,-26.5825,0.105,-21.08173750012614,3,False,False,True,False,0,True,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
ES,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:BASE,f4745b5be052577b9c5a1b8dffadc62e0e29186528f69bdfb370d4d96195da76,256.5926,255.23969,31.101249710331462,46.29946036015223,0.0,77.4007100704837,120.57657087048368,22.644600000000004,6.6676834000000005,0.6419216395996451,0.2579377526313848,0.3839838869682602,0.3032471559203182,98.661156887314,97.31064458352448,99.4127213037086,92.13420270147232,96.198776191184,0.933844743040096,0.9750420451795188,92.13420270147232,96.198776191184,0.933844743040096,0.9750420451795188,0.5703919152839889,0.5955552074125496,0,0,0,0,197,197,41.31304690736875,79.58802578261405,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0944955713769326,0.0887189605973898,161.5278902675193,161.5278902675193,,none,0,0,7884,876,1.0,0.7162492897942901,1.0,OK,BASE,SCEN,2030,6237.200000000001,13.6049,14.0905,2.1494,1.65,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475,4,False,False,True,True,1,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
ES,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:BASE,dce1e53ca70c1a732fd92714fb132f899b3a6ee779f8d2b7648d26108105465b,301.2174,299.86286160000003,36.137043115351815,51.0458476562065,0.0,87.18289077155832,130.46665917155832,22.70664,6.671025300000001,0.6682388537052703,0.2769829728515779,0.3912558808536922,0.290742542462145,105.51371698585235,104.257888452442,106.20962196933452,98.40603141928084,103.01805804292654,0.9326373312436284,0.976347540260946,98.40603141928084,103.01805804292654,0.9326373312436284,0.976347540260946,0.5701749971834855,0.5968975692577833,0,0,0,0,198,198,44.54542933422071,85.78810122554783,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0806473995437968,0.0757234152933862,172.5891733334165,172.5891733334165,,none,0,0,7905,879,1.0,0.7218755416093814,1.0,OK,BASE,SCEN,2040,6237.200000000001,15.7817,15.5234,2.5076,1.65,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475,4,False,False,True,True,1,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
```

### Q1 - scénario `DEMAND_UP`

### Q1/DEMAND_UP - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\DEMAND_UP\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2030: signal stage2 majoritairement capture-only.,Q1,DE,False
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2040: signal stage2 majoritairement capture-only.,Q1,DE,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,Q1,,True
```

### Q1/DEMAND_UP - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\DEMAND_UP\warnings_filtered.csv`

```csv

```

### Q1/DEMAND_UP - Q1_country_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\DEMAND_UP\tables\Q1_country_summary.csv`

```csv
country,bascule_year_market,bascule_year_physical,bascule_confidence,drivers_at_bascule,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,h_negative_at_bascule,notes_quality
DE,,,0.0,capture_ratio,0.0,,0.0393119010167381,225.90861494147683,0.5991217231431424,0,ok
ES,2030.0,,1.0,capture_ratio,0.0,,0.0858355216446282,164.48943129272254,0.5700742879112846,0,ok
```

### Q1/DEMAND_UP - Q1_year_panel.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\DEMAND_UP\tables\Q1_year_panel.csv`

```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm,stage2_market_score,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_stage2,flag_days_spread_stage2,flag_non_capture_stage2,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,phase_market,stress_phys_state,quality_ok,flag_sr_stress,flag_far_tension,flag_ir_high
DE,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:DEMAND_UP,27e465e68b67d2c941180cca1c2006df1d46a847b0eea49f89f4e65ebffd0689,578.4937000000001,577.0136128690001,31.6974537475,98.74950692264126,21.756967075256217,152.20392774539746,176.5478818501475,22.6446,3.4586516,0.8621113215880268,0.1795402664440038,0.6825710551440229,0.2637787468975233,128.6041244627808,137.37106632026098,123.72529327983342,124.33686924114802,123.64805811999652,0.9668186752216664,0.9614626174433574,124.33686924114802,123.64805811999652,0.9668186752216664,0.9614626174433574,0.5971518379471358,0.5938436894510023,0,0,0,0,119,119,32.89345644125173,97.58259643274272,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0460630370874062,0.0392444814038399,208.21650598713427,208.21650598713427,,none,0,0,7884,876,1.0,0.6782905135897174,1.0,OK,DEMAND_UP,SCEN,2030,9425.893,21.1595,38.4164,5.8601,1.65,0.45,0.8914973010374386,-26.5825,0.105,-21.08173750012614,3,False,False,True,False,0,True,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
DE,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:DEMAND_UP,54e995b6e77f5907e9facb41bd5542b4a755f7068ce1391e5220f78244283858,679.1013,677.6177870144999,36.75064727891181,109.3064128317157,25.451076930673285,171.50813704130078,195.9170503343008,22.70664,3.4966016,0.8754120008883853,0.1875826897975585,0.687829311090827,0.2531045381747495,140.025314250469,148.6850412325381,135.2266120374753,135.34675865661825,134.9028395556721,0.9665877872233728,0.9634175097394596,135.34675865661825,134.9028395556721,0.9665877872233728,0.9634175097394596,0.5991217231431424,0.5971566847533442,0,0,0,0,121,121,36.289160701628525,105.72032655546892,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0393119010167381,0.0335095099850354,225.90861494147683,225.90861494147683,,none,0,0,7905,879,1.0,0.68579579593025,1.0,OK,DEMAND_UP,SCEN,2040,9425.893,24.5451,42.3232,6.8368,1.65,0.45,0.8914973010374386,-26.5825,0.105,-21.08173750012614,3,False,False,True,False,0,True,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
ES,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:DEMAND_UP,08c732c86e912850ebbc702d88571c992a2db19749593b78709c89775e2b5540,282.2518,280.89889,31.101249710331462,46.29946036015223,0.0,77.4007100704837,120.57657087048368,22.644600000000004,6.6676834000000005,0.6419216395996451,0.2579377526313848,0.3839838869682602,0.2755465145144706,100.2119227992864,99.0544876129467,100.85603918230272,93.77119541313095,97.87297645108453,0.9357289311866064,0.9766599993008164,93.77119541313095,97.87297645108453,0.9357289311866064,0.9766599993008164,0.5700742879112846,0.5950107291508077,0,0,0,0,195,195,42.00899188617949,82.0703956245834,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0858355216446282,0.080614772098245,164.48943129272254,164.48943129272254,,none,0,0,7884,876,1.0,0.7213663787266826,1.0,OK,DEMAND_UP,SCEN,2030,6237.200000000001,13.6049,14.0905,2.1494,1.65,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475,4,False,False,True,True,1,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
ES,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:DEMAND_UP,6409045417df95b541cc1594c2adaa7eac3ebe10896d1f8593e3b5b1c1d3f818,331.3391,329.9845616,36.137043115351815,51.0458476562065,0.0,87.18289077155832,130.46665917155832,22.70664,6.671025300000001,0.6682388537052703,0.2769829728515779,0.3912558808536922,0.2642029383097004,107.3295785959766,106.3439477786375,107.87575618265495,100.31173346110413,104.95432195259195,0.9346140623425911,0.9778695055505076,100.31173346110413,104.95432195259195,0.9346140623425911,0.9778695055505076,0.5696061837867059,0.595968474839665,0,0,0,0,197,197,45.59584687553456,88.70395134534763,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0732607643413655,0.0688112191973528,176.10717073722418,176.10717073722418,,none,0,0,7905,879,1.0,0.7268893808842096,1.0,OK,DEMAND_UP,SCEN,2040,6237.200000000001,15.7817,15.5234,2.5076,1.65,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475,4,False,False,True,True,1,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
```

### Q1 - scénario `FLEX_UP`

### Q1/FLEX_UP - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\FLEX_UP\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2030: signal stage2 majoritairement capture-only.,Q1,DE,False
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2040: signal stage2 majoritairement capture-only.,Q1,DE,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,Q1,,True
```

### Q1/FLEX_UP - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\FLEX_UP\warnings_filtered.csv`

```csv

```

### Q1/FLEX_UP - Q1_country_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\FLEX_UP\tables\Q1_country_summary.csv`

```csv
country,bascule_year_market,bascule_year_physical,bascule_confidence,drivers_at_bascule,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,h_negative_at_bascule,notes_quality
DE,,,0.0,capture_ratio,0.0,,0.0433135384627132,221.8789608116333,0.6000361592222314,0,ok
ES,2030.0,,1.0,capture_ratio,0.0,,0.0946017932912733,161.5278902675193,0.5702061902442622,0,ok
```

### Q1/FLEX_UP - Q1_year_panel.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\FLEX_UP\tables\Q1_year_panel.csv`

```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm,stage2_market_score,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_stage2,flag_days_spread_stage2,flag_non_capture_stage2,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,phase_market,stress_phys_state,quality_ok,flag_sr_stress,flag_far_tension,flag_ir_high
DE,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:FLEX_UP,03f6358ad20b0a5f40421def3bba794d385757efeb418d334d14d73d3a1a1322,525.9034,524.1057758522501,31.6974537475,98.74950692264126,21.756967075256217,152.20392774539746,176.5478818501475,22.6446,4.8190211,0.8621113215880268,0.1795402664440038,0.6825710551440229,0.2904068887580912,126.8756286642738,134.8857858302721,122.4179505825562,122.45418727107236,121.6822557604586,0.9651513735163352,0.959067214417062,122.45418727107236,121.6822557604586,0.9651513735163352,0.959067214417062,0.597791412501787,0.5940230315393383,0,0,0,0,121,121,32.46244925212925,95.4033539304072,0.0,0.0,0.0,0.0,0.0,0.0,,,0.050771079018632,0.043206163800003,204.8443398652976,204.8443398652976,,none,0,0,7884,876,1.0,0.6729174044621066,1.0,OK,FLEX_UP,SCEN,2030,9425.893,21.1595,38.4164,5.8601,2.4375,0.35,0.8914973010374386,-26.5825,0.105,-21.08173750012614,3,False,False,True,False,0,True,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
DE,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:FLEX_UP,5c538bf0b2662e4071ad6ea87a6fa3ee76b537b3467f56416646790ae069c283,617.3648,615.5633899977499,36.75064727891181,109.3064128317157,25.451076930673285,171.50813704130078,195.9170503343008,22.70664,4.8740938,0.8754120008883853,0.1875826897975585,0.687829311090827,0.2786197812087683,138.00269393782315,145.96435759007062,133.5908166273421,133.13539945763245,132.61294875607456,0.9647304386508304,0.9609446379055692,133.13539945763245,132.61294875607456,0.9647304386508304,0.9609446379055692,0.6000361592222314,0.5976814938693437,0,0,0,0,122,122,35.47685301428027,103.16471665160596,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0433135384627132,0.0368875738371689,221.8789608116333,221.8789608116333,,none,0,0,7905,879,1.0,0.6808667111263013,1.0,OK,FLEX_UP,SCEN,2040,9425.893,24.5451,42.3232,6.8368,2.4375,0.35,0.8914973010374386,-26.5825,0.105,-21.08173750012614,3,False,False,True,False,0,True,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
ES,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:FLEX_UP,122858f11c51bd8db0d818b3df452676fde034f7afd7256c62c2352b394a8110,256.5926,254.955638,31.101249710331462,46.29946036015223,0.0,77.4007100704837,120.57657087048368,22.644600000000004,8.7176561,0.6419216395996451,0.2579377526313848,0.3839838869682602,0.3035850106224507,98.64545138178808,97.28700685315944,99.4014301066752,92.1042029276354,96.181886462792,0.9336893048536417,0.9750260667421824,92.1042029276354,96.181886462792,0.9336893048536417,0.9750260667421824,0.5702061902442622,0.5954506451083925,0,0,0,0,197,197,41.35050447623986,79.63159560325163,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0946017932912733,0.0888178044527103,161.5278902675193,161.5278902675193,,none,0,0,7884,876,1.0,0.7153709736484742,1.0,OK,FLEX_UP,SCEN,2030,6237.200000000001,13.6049,14.0905,2.1494,2.4375,0.35,0.8687903652597629,-0.02,8.33,-19.73003920827475,4,False,False,True,True,1,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
ES,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:FLEX_UP,802762580d7d0d4956576acb8e70a0c9479817f5723f22ad0d31e2c6f3863d8c,301.2174,299.5787604,36.137043115351815,51.0458476562065,0.0,87.18289077155832,130.46665917155832,22.70664,8.720998,0.6682388537052703,0.2769829728515779,0.3912558808536922,0.2910182639622082,105.49805168000356,104.23534303346838,106.1977692102492,98.37607547031716,103.0011759228295,0.9324918697902708,0.9763324941322368,98.37607547031716,103.0011759228295,0.9324918697902708,0.9763324941322368,0.5700014292337403,0.5967997524609878,0,0,0,0,198,198,44.58258671337139,85.8316710461854,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0807263472501742,0.07579522650298,172.5891733334165,172.5891733334165,,none,0,0,7905,879,1.0,0.7211496720486239,1.0,OK,FLEX_UP,SCEN,2040,6237.200000000001,15.7817,15.5234,2.5076,2.4375,0.35,0.8687903652597629,-0.02,8.33,-19.73003920827475,4,False,False,True,True,1,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
```

### Q1 - scénario `LOW_RIGIDITY`

### Q1/LOW_RIGIDITY - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\LOW_RIGIDITY\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2030: signal stage2 majoritairement capture-only.,Q1,DE,False
WARN,Q1_CAPTURE_ONLY_SIGNAL,DE 2040: signal stage2 majoritairement capture-only.,Q1,DE,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,Q1,,True
```

### Q1/LOW_RIGIDITY - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\LOW_RIGIDITY\warnings_filtered.csv`

```csv

```

### Q1/LOW_RIGIDITY - Q1_country_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\LOW_RIGIDITY\tables\Q1_country_summary.csv`

```csv
country,bascule_year_market,bascule_year_physical,bascule_confidence,drivers_at_bascule,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,h_negative_at_bascule,notes_quality
DE,,,0.0,capture_ratio,0.0,,0.0330380004770678,222.20130970089272,0.5999659874227242,0,ok
ES,2030.0,,1.0,capture_ratio,0.0,,0.0721602545060212,162.05417149089467,0.570441195105838,0,ok
```

### Q1/LOW_RIGIDITY - Q1_year_panel.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q1\scen\LOW_RIGIDITY\tables\Q1_year_panel.csv`

```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm,stage2_market_score,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_stage2,flag_days_spread_stage2,flag_non_capture_stage2,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,phase_market,stress_phys_state,quality_ok,flag_sr_stress,flag_far_tension,flag_ir_high
DE,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:LOW_RIGIDITY,6822b3bcaa37e5fdfe6fe33a858fb86ff423e25f218903448d669bba4ef52b2b,525.9034,524.423312869,31.6974537475,98.74950692264126,21.756967075256217,152.20392774539746,171.19552185014746,17.29224,3.4586516,0.8890648896682362,0.1851535215695987,0.7039113680986374,0.2902310481063944,127.05800620843968,135.0552260542705,122.60752778677266,122.6165086811288,121.86322563093228,0.9650435445994284,0.9591148898638836,122.6165086811288,121.86322563093228,0.9650435445994284,0.9591148898638836,0.5977187820637748,0.5940467526433022,0,0,0,0,122,122,32.72793668961861,95.55565577835456,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0387133450001058,0.0329738201480748,205.14079925306075,205.14079925306075,,none,0,0,7884,876,1.0,0.6730077697988456,1.0,OK,LOW_RIGIDITY,SCEN,2030,9425.893,21.1595,38.4164,5.8601,1.65,0.45,0.8914973010374386,-26.5825,0.105,-21.08173750012614,3,False,False,True,False,0,True,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
DE,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:LOW_RIGIDITY,44075226f72526b300818ad8076af9efa828b4f9f9333f44a7d2ef4878afafc9,617.3648,615.8812870144999,36.75064727891181,109.3064128317157,25.451076930673285,171.50813704130078,190.5500263343008,17.339616,3.4966016,0.9000688183606286,0.1928661359218944,0.7072026824387344,0.2784759671343333,138.18507049247427,146.1588580248104,133.76647485353644,133.31322818131866,132.79007724104682,0.96474407623202,0.9609582045860644,133.31322818131866,132.79007724104682,0.96474407623202,0.9609582045860644,0.5999659874227242,0.5976115866274452,0,0,0,0,122,122,35.52503700469273,103.31705810147854,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0330380004770678,0.0281541530252595,222.20130970089272,222.20130970089272,,none,0,0,7905,879,1.0,0.6809304253072952,1.0,OK,LOW_RIGIDITY,SCEN,2040,9425.893,24.5451,42.3232,6.8368,1.65,0.45,0.8914973010374386,-26.5825,0.105,-21.08173750012614,3,False,False,True,False,0,True,False,False,uncertain,pas_de_surplus_structurel,True,False,False,False
ES,2030,8760,8760,8760,8760,8760,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:LOW_RIGIDITY,0a97a667845796f7f9d14e1303a8f2f68fde91570e85a6e1b8c8918b47c8eb24,256.5926,255.23969,31.101249710331462,46.29946036015223,0.0,77.4007100704837,115.2242108704837,17.29224,6.6676834000000005,0.6717399883734936,0.2699193986695246,0.4018205897039689,0.3032471559203182,98.98059642880098,97.6451187971206,99.72379400208152,92.44237525715238,96.53949978970414,0.933944415294045,0.9753376244721582,92.44237525715238,96.53949978970414,0.933944415294045,0.9753376244721582,0.570441195105838,0.5957236330391433,0,0,0,0,196,196,41.27425075912336,79.86783396069681,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0721602545060212,0.0677490244561886,162.05417149089467,162.05417149089467,,none,0,0,7884,876,1.0,0.7158297461481474,1.0,OK,LOW_RIGIDITY,SCEN,2030,6237.200000000001,13.6049,14.0905,2.1494,1.65,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475,4,False,False,True,True,1,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
ES,2040,8784,8784,8784,8784,8784,0.0,0.0,0.0,0.0,minus_psh_pump,observed,SCEN:LOW_RIGIDITY,0a84191e7a1d1f5f2aafb74b583a46cff6215323bd67f93cf80faca90f1b5abf,301.2174,299.86286160000003,36.137043115351815,51.0458476562065,0.0,87.18289077155832,125.09963517155832,17.339616,6.671025300000001,0.6969076340790125,0.2888660951392419,0.4080415389397705,0.290742542462145,105.83318335371789,104.57387025083116,106.53101927697357,98.70838037659335,103.32908509984468,0.9326789315850792,0.97633919556682,98.70838037659335,103.32908509984468,0.9326789315850792,0.97633919556682,0.5702021567545948,0.5968942753859813,0,0,0,0,197,197,44.49741248034485,86.06799694489395,0.0,0.0,0.0,0.0,0.0,0.0,,,0.0615852869243539,0.0578251534967676,173.11120136480957,173.11120136480957,,none,0,0,7905,879,1.0,0.7214704573561171,1.0,OK,LOW_RIGIDITY,SCEN,2040,6237.200000000001,15.7817,15.5234,2.5076,1.65,0.45,0.8687903652597629,-0.02,8.33,-19.73003920827475,4,False,False,True,True,1,False,False,True,phase2,pas_de_surplus_structurel,True,False,False,False
```

## Q2

### Q2 - contexte
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\question_context.json`

```json
{
  "question_id": "Q2",
  "objective": "Mesurer la pente de cannibalisation (PV/Wind) et qualifier ses drivers et sa robustesse statistique.",
  "countries_scope": [
    "DE",
    "ES"
  ],
  "run_id": "FULL_20260210_172152",
  "source_summary_file": "outputs\\combined\\FULL_20260210_172152\\Q2\\summary.json",
  "source_refs_in_ledger": [
    "SPEC2-Q2",
    "SPEC2-Q2/Slides 10",
    "SPEC2-Q2/Slides 10-12",
    "SPEC2-Q2/Slides 11",
    "Slides 10-13"
  ],
  "scenarios": [
    "BASE",
    "HIGH_CO2",
    "HIGH_GAS"
  ],
  "country_filter_notes": {
    "hist_unfilterable_tables": [
      "Q2_driver_correlations.csv"
    ],
    "scen_unfilterable_tables_by_scenario": {
      "BASE": [
        "Q2_driver_correlations.csv"
      ],
      "HIGH_CO2": [
        "Q2_driver_correlations.csv"
      ],
      "HIGH_GAS": [
        "Q2_driver_correlations.csv"
      ]
    }
  }
}
```

### Q2 - test ledger
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\test_ledger.csv`

```csv
test_id,question_id,source_ref,mode,scenario_group,title,what_is_tested,metric_rule,severity_if_fail,scenario_id,status,value,threshold,interpretation
Q2-H-01,Q2,SPEC2-Q2/Slides 10,HIST,HIST_BASE,Pentes OLS post-bascule,Les pentes PV/Wind sont estimees en historique.,Q2_country_slopes non vide,HIGH,,PASS,14,>0 lignes,Les pentes historiques sont calculees.
Q2-H-02,Q2,SPEC2-Q2/Slides 10-12,HIST,HIST_BASE,Robustesse statistique,R2/p-value/n sont disponibles pour qualifier la robustesse.,"colonnes r2,p_value,n presentes",MEDIUM,,PASS,"n,p_value,r2","r2,p_value,n disponibles",La robustesse statistique est lisible.
Q2-H-03,Q2,Slides 10-13,HIST,HIST_BASE,Drivers physiques,Les drivers SR/FAR/IR/corr VRE-load sont exploites.,driver correlations non vides,MEDIUM,,PASS,6,>0 lignes,Les drivers de pente sont disponibles.
Q2-S-01,Q2,SPEC2-Q2/Slides 11,SCEN,DEFAULT,Pentes projetees,Les pentes sont reproduites en mode scenario.,Q2_country_slopes non vide en SCEN,HIGH,BASE,PASS,14,>0 lignes,Pentes prospectives calculees.
Q2-S-01,Q2,SPEC2-Q2/Slides 11,SCEN,DEFAULT,Pentes projetees,Les pentes sont reproduites en mode scenario.,Q2_country_slopes non vide en SCEN,HIGH,HIGH_CO2,PASS,14,>0 lignes,Pentes prospectives calculees.
Q2-S-01,Q2,SPEC2-Q2/Slides 11,SCEN,DEFAULT,Pentes projetees,Les pentes sont reproduites en mode scenario.,Q2_country_slopes non vide en SCEN,HIGH,HIGH_GAS,PASS,14,>0 lignes,Pentes prospectives calculees.
Q2-S-02,Q2,SPEC2-Q2,SCEN,DEFAULT,Delta pente vs BASE,Les differences de pente vs BASE sont calculables.,delta slope par pays/tech vs BASE,MEDIUM,BASE,WARN,finite=14.29%; robust=0.00%,finite_share >= 20%,Delta de pente partiellement exploitable; beaucoup de valeurs non finies.
Q2-S-02,Q2,SPEC2-Q2,SCEN,DEFAULT,Delta pente vs BASE,Les differences de pente vs BASE sont calculables.,delta slope par pays/tech vs BASE,MEDIUM,HIGH_CO2,WARN,finite=14.29%; robust=0.00%,finite_share >= 20%,Delta de pente partiellement exploitable; beaucoup de valeurs non finies.
Q2-S-02,Q2,SPEC2-Q2,SCEN,DEFAULT,Delta pente vs BASE,Les differences de pente vs BASE sont calculables.,delta slope par pays/tech vs BASE,MEDIUM,HIGH_GAS,WARN,finite=14.29%; robust=0.00%,finite_share >= 20%,Delta de pente partiellement exploitable; beaucoup de valeurs non finies.
```

### Q2 - comparaison HIST vs SCEN
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\comparison_hist_vs_scen.csv`

```csv
country,tech,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
DE,PV,BASE,slope,-2.327766838978395,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,WIND,BASE,slope,0.5350253354052343,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,PV,BASE,slope,-3.115488502913144,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,WIND,BASE,slope,-4.980736473613575,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,PV,HIGH_CO2,slope,-2.327766838978395,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,WIND,HIGH_CO2,slope,0.5350253354052343,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,PV,HIGH_CO2,slope,-3.115488502913144,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,WIND,HIGH_CO2,slope,-4.980736473613575,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,PV,HIGH_GAS,slope,-2.327766838978395,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,WIND,HIGH_GAS,slope,0.5350253354052343,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,PV,HIGH_GAS,slope,-3.115488502913144,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,WIND,HIGH_GAS,slope,-4.980736473613575,,,,NON_TESTABLE,delta_non_interpretable_nan
```

### Q2 - checks filtrés
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\checks_filtered.csv`

```csv
status,code,message,scope,scenario_id,question_id,mentioned_countries,is_global
INFO,Q2_LOW_R2,DE-WIND: R2 faible (0.06).,HIST,,Q2,DE,False
WARN,Q2_FRAGILE,ES-PV: n=2 < 3.,SCEN,BASE,Q2,ES,False
WARN,Q2_FRAGILE,ES-WIND: n=2 < 3.,SCEN,BASE,Q2,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,SCEN,BASE,Q2,,True
WARN,Q2_FRAGILE,ES-PV: n=2 < 3.,SCEN,HIGH_CO2,Q2,ES,False
WARN,Q2_FRAGILE,ES-WIND: n=2 < 3.,SCEN,HIGH_CO2,Q2,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,SCEN,HIGH_CO2,Q2,,True
WARN,Q2_FRAGILE,ES-PV: n=2 < 3.,SCEN,HIGH_GAS,Q2,ES,False
WARN,Q2_FRAGILE,ES-WIND: n=2 < 3.,SCEN,HIGH_GAS,Q2,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,SCEN,HIGH_GAS,Q2,,True
WARN,BUNDLE_LEDGER_STATUS,"ledger: FAIL=0, WARN=3",BUNDLE,,Q2,,True
WARN,BUNDLE_INFORMATIVENESS,share_tests_informatifs=100.00% ; share_compare_informatifs=14.29%,BUNDLE,,Q2,,True
```

### Q2 - warnings filtrés
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\warnings_filtered.csv`

```csv
question_id,status,code,message,scope,scenario_id,mentioned_countries,is_global
Q2,WARN,QUESTION_WARNING,"BASE: DE: pas de bascule Q1, pente Q2 non calculable.",GLOBAL,,DE,False
Q2,WARN,QUESTION_WARNING,"HIGH_CO2: DE: pas de bascule Q1, pente Q2 non calculable.",GLOBAL,,DE,False
Q2,WARN,QUESTION_WARNING,"HIGH_GAS: DE: pas de bascule Q1, pente Q2 non calculable.",GLOBAL,,DE,False
```

### Q2 - historique - Q2_country_slopes.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\hist\tables\Q2_country_slopes.csv`

```csv
country,tech,x_axis_used,phase2_years,slope,intercept,r2,p_value,n,slope_method,robust_flag,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2
DE,PV,pv_penetration_pct_gen,2019-2024,-2.327766838978395,0.6710851129884647,0.2995432221518992,0.2610126852558038,6,OLS,ROBUST,0.00717243720449,0.992624337941795,0.2771910873673374,200.27675,0.2374520070022607,0.601948261932339
DE,WIND,wind_penetration_pct_gen,2019-2024,0.5350253354052343,0.2872062540597112,0.0641806521186109,0.6281212218496589,6,OLS,ROBUST,0.00717243720449,0.992624337941795,0.2771910873673374,200.27675,0.2374520070022607,0.601948261932339
ES,PV,pv_penetration_pct_gen,2022-2024,-3.115488502913144,0.9446133885005366,0.8612032684521528,0.243035957328681,3,OLS,ROBUST,0.0245726637634173,0.9826623285138508,0.3217166264028505,188.3923333333333,0.1305265263884011,0.5024495615741936
ES,WIND,wind_penetration_pct_gen,2022-2024,-4.980736473613575,1.6874253416851972,0.4239048193597569,0.5486326810978256,3,OLS,ROBUST,0.0245726637634173,0.9826623285138508,0.3217166264028505,188.3923333333333,0.1305265263884011,0.5024495615741936
```

### Q2 - historique - Q2_driver_correlations.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\hist\tables\Q2_driver_correlations.csv`

```csv
driver_name,corr_with_slope_pv,corr_with_slope_wind,n_countries
mean_sr_energy_phase2,-0.3820091615317603,0.0254507755860652,7
mean_far_energy_phase2,-0.8495009512618577,0.071051763820914,7
mean_ir_p10_phase2,-0.4957611680656518,0.10973028371647,7
mean_ttl_phase2,0.0662206727873414,0.5927507182155464,7
vre_load_corr_phase2,0.510008279044118,0.1700231030656055,7
surplus_load_trough_share_phase2,0.3754385083890953,0.6896032391244143,7
```

### Q2 - scénario `BASE`

### Q2/BASE - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\BASE\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
WARN,Q2_FRAGILE,ES-PV: n=2 < 3.,Q2,ES,False
WARN,Q2_FRAGILE,ES-WIND: n=2 < 3.,Q2,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,Q2,,True
```

### Q2/BASE - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\BASE\warnings_filtered.csv`

```csv
question_id,status,code,message,scope,scenario_id,mentioned_countries,is_global
Q2,WARN,QUESTION_WARNING,"DE: pas de bascule Q1, pente Q2 non calculable.",GLOBAL,,DE,False
```

### Q2/BASE - Q2_country_slopes.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\BASE\tables\Q2_country_slopes.csv`

```csv
country,tech,x_axis_used,phase2_years,slope,intercept,r2,p_value,n,slope_method,robust_flag,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2
DE,PV,none,,,,,,0,NONE_NO_BASCULE,NON_TESTABLE,,,,,,
DE,WIND,none,,,,,,0,NONE_NO_BASCULE,NON_TESTABLE,,,,,,
ES,PV,sr_energy,2030-2040,,,,,2,OLS,FRAGILE,0.0,,0.0875714854603647,167.0585318004679,0.286816937893073,
ES,WIND,sr_energy,2030-2040,,,,,2,OLS,FRAGILE,0.0,,0.0875714854603647,167.0585318004679,0.286816937893073,
```

### Q2/BASE - Q2_driver_correlations.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\BASE\tables\Q2_driver_correlations.csv`

```csv
driver_name,corr_with_slope_pv,corr_with_slope_wind,n_countries
mean_sr_energy_phase2,,,7
mean_far_energy_phase2,,,7
mean_ir_p10_phase2,,,7
mean_ttl_phase2,,,7
vre_load_corr_phase2,,,7
surplus_load_trough_share_phase2,,,7
```

### Q2 - scénario `HIGH_CO2`

### Q2/HIGH_CO2 - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_CO2\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
WARN,Q2_FRAGILE,ES-PV: n=2 < 3.,Q2,ES,False
WARN,Q2_FRAGILE,ES-WIND: n=2 < 3.,Q2,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,Q2,,True
```

### Q2/HIGH_CO2 - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_CO2\warnings_filtered.csv`

```csv
question_id,status,code,message,scope,scenario_id,mentioned_countries,is_global
Q2,WARN,QUESTION_WARNING,"DE: pas de bascule Q1, pente Q2 non calculable.",GLOBAL,,DE,False
```

### Q2/HIGH_CO2 - Q2_country_slopes.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_CO2\tables\Q2_country_slopes.csv`

```csv
country,tech,x_axis_used,phase2_years,slope,intercept,r2,p_value,n,slope_method,robust_flag,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2
DE,PV,none,,,,,,0,NONE_NO_BASCULE,NON_TESTABLE,,,,,,
DE,WIND,none,,,,,,0,NONE_NO_BASCULE,NON_TESTABLE,,,,,,
ES,PV,sr_energy,2030-2040,,,,,2,OLS,FRAGILE,0.0,,0.0875714854603647,173.48580452774064,0.286816937893073,
ES,WIND,sr_energy,2030-2040,,,,,2,OLS,FRAGILE,0.0,,0.0875714854603647,173.48580452774064,0.286816937893073,
```

### Q2/HIGH_CO2 - Q2_driver_correlations.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_CO2\tables\Q2_driver_correlations.csv`

```csv
driver_name,corr_with_slope_pv,corr_with_slope_wind,n_countries
mean_sr_energy_phase2,,,7
mean_far_energy_phase2,,,7
mean_ir_p10_phase2,,,7
mean_ttl_phase2,,,7
vre_load_corr_phase2,,,7
surplus_load_trough_share_phase2,,,7
```

### Q2 - scénario `HIGH_GAS`

### Q2/HIGH_GAS - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_GAS\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
WARN,Q2_FRAGILE,ES-PV: n=2 < 3.,Q2,ES,False
WARN,Q2_FRAGILE,ES-WIND: n=2 < 3.,Q2,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,Q2,,True
```

### Q2/HIGH_GAS - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_GAS\warnings_filtered.csv`

```csv
question_id,status,code,message,scope,scenario_id,mentioned_countries,is_global
Q2,WARN,QUESTION_WARNING,"DE: pas de bascule Q1, pente Q2 non calculable.",GLOBAL,,DE,False
```

### Q2/HIGH_GAS - Q2_country_slopes.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_GAS\tables\Q2_country_slopes.csv`

```csv
country,tech,x_axis_used,phase2_years,slope,intercept,r2,p_value,n,slope_method,robust_flag,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2
DE,PV,none,,,,,,0,NONE_NO_BASCULE,NON_TESTABLE,,,,,,
DE,WIND,none,,,,,,0,NONE_NO_BASCULE,NON_TESTABLE,,,,,,
ES,PV,sr_energy,2030-2040,,,,,2,OLS,FRAGILE,0.0,,0.0875714854603647,181.3767136186497,0.286816937893073,
ES,WIND,sr_energy,2030-2040,,,,,2,OLS,FRAGILE,0.0,,0.0875714854603647,181.3767136186497,0.286816937893073,
```

### Q2/HIGH_GAS - Q2_driver_correlations.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q2\scen\HIGH_GAS\tables\Q2_driver_correlations.csv`

```csv
driver_name,corr_with_slope_pv,corr_with_slope_wind,n_countries
mean_sr_energy_phase2,,,7
mean_far_energy_phase2,,,7
mean_ir_p10_phase2,,,7
mean_ttl_phase2,,,7
vre_load_corr_phase2,,,7
surplus_load_trough_share_phase2,,,7
```

## Q3

### Q3 - contexte
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\question_context.json`

```json
{
  "question_id": "Q3",
  "objective": "Evaluer la sortie de Phase 2 et quantifier les conditions minimales d'inversion (demande/must-run/flex).",
  "countries_scope": [
    "DE",
    "ES"
  ],
  "run_id": "FULL_20260210_172152",
  "source_summary_file": "outputs\\combined\\FULL_20260210_172152\\Q3\\summary.json",
  "source_refs_in_ledger": [
    "SPEC2-Q3",
    "SPEC2-Q3/Slides 16",
    "SPEC2-Q3/Slides 17",
    "Slides 17-19"
  ],
  "scenarios": [
    "BASE",
    "DEMAND_UP",
    "FLEX_UP",
    "LOW_RIGIDITY"
  ],
  "country_filter_notes": {
    "hist_unfilterable_tables": [],
    "scen_unfilterable_tables_by_scenario": {
      "BASE": [],
      "DEMAND_UP": [],
      "FLEX_UP": [],
      "LOW_RIGIDITY": []
    }
  }
}
```

### Q3 - test ledger
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\test_ledger.csv`

```csv
test_id,question_id,source_ref,mode,scenario_group,title,what_is_tested,metric_rule,severity_if_fail,scenario_id,status,value,threshold,interpretation
Q3-H-01,Q3,SPEC2-Q3/Slides 16,HIST,HIST_BASE,Tendances glissantes,Les tendances h_negative et capture_ratio sont estimees.,Q3_status non vide,HIGH,,PASS,7,>0 lignes,Les tendances historiques sont calculees.
Q3-H-02,Q3,SPEC2-Q3,HIST,HIST_BASE,Statuts sortie phase 2,Les statuts degradation/stabilisation/amelioration sont attribues.,status dans ensemble attendu,MEDIUM,,PASS,2,status valides,Les statuts business sont renseignes.
Q3-S-01,Q3,SPEC2-Q3/Slides 17,SCEN,DEFAULT,Conditions minimales d'inversion,Les besoins demande/must-run/flex sont quantifies en scenario.,"inversion_k, inversion_r et additional_absorbed presentes",HIGH,BASE,PASS,hors_scope=85.71%; inversion=0,hors_scope < 80% ou inversion deja atteinte,Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites.
Q3-S-01,Q3,SPEC2-Q3/Slides 17,SCEN,DEFAULT,Conditions minimales d'inversion,Les besoins demande/must-run/flex sont quantifies en scenario.,"inversion_k, inversion_r et additional_absorbed presentes",HIGH,DEMAND_UP,PASS,hors_scope=100.00%; inversion=0,hors_scope < 80% ou inversion deja atteinte,Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites.
Q3-S-01,Q3,SPEC2-Q3/Slides 17,SCEN,DEFAULT,Conditions minimales d'inversion,Les besoins demande/must-run/flex sont quantifies en scenario.,"inversion_k, inversion_r et additional_absorbed presentes",HIGH,FLEX_UP,PASS,hors_scope=85.71%; inversion=0,hors_scope < 80% ou inversion deja atteinte,Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites.
Q3-S-01,Q3,SPEC2-Q3/Slides 17,SCEN,DEFAULT,Conditions minimales d'inversion,Les besoins demande/must-run/flex sont quantifies en scenario.,"inversion_k, inversion_r et additional_absorbed presentes",HIGH,LOW_RIGIDITY,PASS,hors_scope=100.00%; inversion=0,hors_scope < 80% ou inversion deja atteinte,Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites.
Q3-S-02,Q3,Slides 17-19,SCEN,DEFAULT,Validation entree phase 3,Le statut prospectif est interpretable pour la transition phase 3.,status non vide en SCEN,MEDIUM,BASE,PASS,hors_scope=85.71%; inversion=0,hors_scope < 80% ou inversion deja atteinte,Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise.
Q3-S-02,Q3,Slides 17-19,SCEN,DEFAULT,Validation entree phase 3,Le statut prospectif est interpretable pour la transition phase 3.,status non vide en SCEN,MEDIUM,DEMAND_UP,PASS,hors_scope=100.00%; inversion=0,hors_scope < 80% ou inversion deja atteinte,Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise.
Q3-S-02,Q3,Slides 17-19,SCEN,DEFAULT,Validation entree phase 3,Le statut prospectif est interpretable pour la transition phase 3.,status non vide en SCEN,MEDIUM,FLEX_UP,PASS,hors_scope=85.71%; inversion=0,hors_scope < 80% ou inversion deja atteinte,Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise.
Q3-S-02,Q3,Slides 17-19,SCEN,DEFAULT,Validation entree phase 3,Le statut prospectif est interpretable pour la transition phase 3.,status non vide en SCEN,MEDIUM,LOW_RIGIDITY,PASS,hors_scope=100.00%; inversion=0,hors_scope < 80% ou inversion deja atteinte,Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise.
```

### Q3 - comparaison HIST vs SCEN
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\comparison_hist_vs_scen.csv`

```csv
country,scenario_id,metric,hist_value,scen_value,delta,hist_status,scen_status,interpretability_status,interpretability_reason
DE,BASE,inversion_k_demand,0.0583007812499999,0.0,-0.0583007812499999,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
DE,BASE,inversion_r_mustrun,0.285400390625,0.0,-0.285400390625,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
ES,BASE,inversion_k_demand,0.1746826171875,0.0,-0.1746826171875,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
ES,BASE,inversion_r_mustrun,0.533203125,0.0,-0.533203125,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
DE,DEMAND_UP,inversion_k_demand,0.0583007812499999,0.0,-0.0583007812499999,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
DE,DEMAND_UP,inversion_r_mustrun,0.285400390625,0.0,-0.285400390625,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
ES,DEMAND_UP,inversion_k_demand,0.1746826171875,0.0,-0.1746826171875,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
ES,DEMAND_UP,inversion_r_mustrun,0.533203125,0.0,-0.533203125,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
DE,FLEX_UP,inversion_k_demand,0.0583007812499999,0.0,-0.0583007812499999,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
DE,FLEX_UP,inversion_r_mustrun,0.285400390625,0.0,-0.285400390625,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
ES,FLEX_UP,inversion_k_demand,0.1746826171875,0.0,-0.1746826171875,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
ES,FLEX_UP,inversion_r_mustrun,0.533203125,0.0,-0.533203125,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
DE,LOW_RIGIDITY,inversion_k_demand,0.0583007812499999,0.0,-0.0583007812499999,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
DE,LOW_RIGIDITY,inversion_r_mustrun,0.285400390625,0.0,-0.285400390625,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
ES,LOW_RIGIDITY,inversion_k_demand,0.1746826171875,0.0,-0.1746826171875,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
ES,LOW_RIGIDITY,inversion_r_mustrun,0.533203125,0.0,-0.533203125,degradation,hors_scope_stage2,INFORMATIVE,scenario_de_stressed_hors_scope_stage2
```

### Q3 - checks filtrés
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\checks_filtered.csv`

```csv
status,code,message,scope,scenario_id,question_id,mentioned_countries,is_global
INFO,Q3_FAR_ALREADY_REACHED,DE: FAR cible deja atteinte.,HIST,,Q3,DE,False
WARN,Q3_MUSTRUN_HIGH,ES: inversion_r_mustrun=53.3% (>50%).,HIST,,Q3,ES,False
INFO,Q3_FAR_ALREADY_REACHED,ES: FAR cible deja atteinte.,HIST,,Q3,ES,False
INFO,Q3_FAR_ALREADY_REACHED,DE: FAR cible deja atteinte.,SCEN,BASE,Q3,DE,False
INFO,Q3_FAR_ALREADY_REACHED,ES: FAR cible deja atteinte.,SCEN,BASE,Q3,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,SCEN,BASE,Q3,,True
INFO,Q3_FAR_ALREADY_REACHED,DE: FAR cible deja atteinte.,SCEN,DEMAND_UP,Q3,DE,False
INFO,Q3_FAR_ALREADY_REACHED,ES: FAR cible deja atteinte.,SCEN,DEMAND_UP,Q3,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,SCEN,DEMAND_UP,Q3,,True
INFO,Q3_FAR_ALREADY_REACHED,DE: FAR cible deja atteinte.,SCEN,FLEX_UP,Q3,DE,False
INFO,Q3_FAR_ALREADY_REACHED,ES: FAR cible deja atteinte.,SCEN,FLEX_UP,Q3,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,SCEN,FLEX_UP,Q3,,True
INFO,Q3_FAR_ALREADY_REACHED,DE: FAR cible deja atteinte.,SCEN,LOW_RIGIDITY,Q3,DE,False
INFO,Q3_FAR_ALREADY_REACHED,ES: FAR cible deja atteinte.,SCEN,LOW_RIGIDITY,Q3,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,SCEN,LOW_RIGIDITY,Q3,,True
PASS,BUNDLE_LEDGER_STATUS,"ledger: FAIL=0, WARN=0",BUNDLE,,Q3,,True
PASS,BUNDLE_INFORMATIVENESS,share_tests_informatifs=100.00% ; share_compare_informatifs=92.86%,BUNDLE,,Q3,,True
```

### Q3 - warnings filtrés
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\warnings_filtered.csv`

```csv

```

### Q3 - historique - Q3_status.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\hist\tables\Q3_status.csv`

```csv
country,reference_year,trend_window_years,trend_h_negative,trend_capture_ratio_pv_vs_ttl,trend_sr_energy,trend_far_energy,status,inversion_k_demand,inversion_r_mustrun,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality
DE,2024,3,194.0,-0.057433927642047,0.0037125867654722,-0.0047237216458674,degradation,0.0583007812499999,0.285400390625,0.0,0.0,
ES,2024,3,123.5,-0.1245104472318578,0.0137389795707161,-0.0160798899375906,degradation,0.1746826171875,0.533203125,0.0,0.0,
```

### Q3 - scénario `BASE`

### Q3/BASE - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\BASE\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
INFO,Q3_FAR_ALREADY_REACHED,DE: FAR cible deja atteinte.,Q3,DE,False
INFO,Q3_FAR_ALREADY_REACHED,ES: FAR cible deja atteinte.,Q3,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,Q3,,True
```

### Q3/BASE - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\BASE\warnings_filtered.csv`

```csv

```

### Q3/BASE - Q3_status.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\BASE\tables\Q3_status.csv`

```csv
country,reference_year,trend_window_years,trend_h_negative,trend_capture_ratio_pv_vs_ttl,trend_sr_energy,trend_far_energy,status,inversion_k_demand,inversion_r_mustrun,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality
DE,2040,2,0.0,0.0002238182770979,0.0,,hors_scope_stage2,0.0,0.0,0.0,0.0,
ES,2040,2,0.0,-2.1691810050339377e-05,0.0,,hors_scope_stage2,0.0,0.0,0.0,0.0,
```

### Q3 - scénario `DEMAND_UP`

### Q3/DEMAND_UP - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\DEMAND_UP\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
INFO,Q3_FAR_ALREADY_REACHED,DE: FAR cible deja atteinte.,Q3,DE,False
INFO,Q3_FAR_ALREADY_REACHED,ES: FAR cible deja atteinte.,Q3,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,Q3,,True
```

### Q3/DEMAND_UP - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\DEMAND_UP\warnings_filtered.csv`

```csv

```

### Q3/DEMAND_UP - Q3_status.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\DEMAND_UP\tables\Q3_status.csv`

```csv
country,reference_year,trend_window_years,trend_h_negative,trend_capture_ratio_pv_vs_ttl,trend_sr_energy,trend_far_energy,status,inversion_k_demand,inversion_r_mustrun,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality
DE,2040,2,0.0,0.0001969885196006,0.0,,hors_scope_stage2,0.0,0.0,0.0,0.0,
ES,2040,2,0.0,-4.681041245786499e-05,0.0,,hors_scope_stage2,0.0,0.0,0.0,0.0,
```

### Q3 - scénario `FLEX_UP`

### Q3/FLEX_UP - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\FLEX_UP\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
INFO,Q3_FAR_ALREADY_REACHED,DE: FAR cible deja atteinte.,Q3,DE,False
INFO,Q3_FAR_ALREADY_REACHED,ES: FAR cible deja atteinte.,Q3,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,Q3,,True
```

### Q3/FLEX_UP - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\FLEX_UP\warnings_filtered.csv`

```csv

```

### Q3/FLEX_UP - Q3_status.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\FLEX_UP\tables\Q3_status.csv`

```csv
country,reference_year,trend_window_years,trend_h_negative,trend_capture_ratio_pv_vs_ttl,trend_sr_energy,trend_far_energy,status,inversion_k_demand,inversion_r_mustrun,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality
DE,2040,2,0.0,0.0002244746720444,0.0,,hors_scope_stage2,0.0,0.0,0.0,0.0,
ES,2040,2,0.0,-2.047610105219144e-05,0.0,,hors_scope_stage2,0.0,0.0,0.0,0.0,
```

### Q3 - scénario `LOW_RIGIDITY`

### Q3/LOW_RIGIDITY - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\LOW_RIGIDITY\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
INFO,Q3_FAR_ALREADY_REACHED,DE: FAR cible deja atteinte.,Q3,DE,False
INFO,Q3_FAR_ALREADY_REACHED,ES: FAR cible deja atteinte.,Q3,ES,False
PASS,RC_COMMON_PASS,Checks communs RC-1..RC-4 OK.,Q3,,True
```

### Q3/LOW_RIGIDITY - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\LOW_RIGIDITY\warnings_filtered.csv`

```csv

```

### Q3/LOW_RIGIDITY - Q3_status.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q3\scen\LOW_RIGIDITY\tables\Q3_status.csv`

```csv
country,reference_year,trend_window_years,trend_h_negative,trend_capture_ratio_pv_vs_ttl,trend_sr_energy,trend_far_energy,status,inversion_k_demand,inversion_r_mustrun,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality
DE,2040,2,0.0,0.0002247205358949,0.0,,hors_scope_stage2,0.0,0.0,0.0,0.0,
ES,2040,2,0.0,-2.390383512431704e-05,0.0,,hors_scope_stage2,0.0,0.0,0.0,0.0,
```

## Q4

### Q4 - contexte
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\question_context.json`

```json
{
  "question_id": "Q4",
  "objective": "Quantifier l'impact batterie (systeme et actif) et estimer des ordres de grandeur de sizing.",
  "countries_scope": [
    "DE",
    "ES"
  ],
  "run_id": "FULL_20260210_172152",
  "source_summary_file": "outputs\\combined\\FULL_20260210_172152\\Q4\\summary.json",
  "source_refs_in_ledger": [
    "SPEC2-Q4",
    "SPEC2-Q4/Slides 22",
    "SPEC2-Q4/Slides 23",
    "Slides 23-25"
  ],
  "scenarios": [
    "BASE",
    "FLEX_UP",
    "HIGH_CO2",
    "HIGH_GAS"
  ],
  "country_filter_notes": {
    "hist_unfilterable_tables": [
      "Q4_bess_frontier.csv"
    ],
    "scen_unfilterable_tables_by_scenario": {
      "BASE": [
        "Q4_bess_frontier.csv"
      ],
      "FLEX_UP": [
        "Q4_bess_frontier.csv"
      ],
      "HIGH_CO2": [
        "Q4_bess_frontier.csv"
      ],
      "HIGH_GAS": [
        "Q4_bess_frontier.csv"
      ]
    }
  }
}
```

### Q4 - test ledger
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\test_ledger.csv`

```csv
test_id,question_id,source_ref,mode,scenario_group,title,what_is_tested,metric_rule,severity_if_fail,scenario_id,status,value,threshold,interpretation
Q4-H-01,Q4,SPEC2-Q4/Slides 22,HIST,HIST_BASE,Simulation BESS 3 modes,"SURPLUS_FIRST, PRICE_ARBITRAGE_SIMPLE et PV_COLOCATED sont executes.",3 modes executes avec sorties non vides,CRITICAL,,PASS,"HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED",3 modes executes,Les trois modes Q4 sont disponibles.
Q4-H-02,Q4,SPEC2-Q4,HIST,HIST_BASE,Invariants physiques BESS,Bornes SOC/puissance/energie respectees.,aucun check FAIL Q4,CRITICAL,,PASS,PASS,pas de FAIL,Les invariants physiques batterie sont respectes.
Q4-S-01,Q4,SPEC2-Q4/Slides 23,SCEN,DEFAULT,Comparaison effet batteries par scenario,Impact FAR/surplus/capture compare entre scenarios utiles.,Q4 summary non vide pour >=1 scenario,HIGH,BASE,PASS,7,>0 lignes,Resultats Q4 prospectifs disponibles.
Q4-S-01,Q4,SPEC2-Q4/Slides 23,SCEN,DEFAULT,Comparaison effet batteries par scenario,Impact FAR/surplus/capture compare entre scenarios utiles.,Q4 summary non vide pour >=1 scenario,HIGH,FLEX_UP,PASS,7,>0 lignes,Resultats Q4 prospectifs disponibles.
Q4-S-01,Q4,SPEC2-Q4/Slides 23,SCEN,DEFAULT,Comparaison effet batteries par scenario,Impact FAR/surplus/capture compare entre scenarios utiles.,Q4 summary non vide pour >=1 scenario,HIGH,HIGH_CO2,PASS,7,>0 lignes,Resultats Q4 prospectifs disponibles.
Q4-S-01,Q4,SPEC2-Q4/Slides 23,SCEN,DEFAULT,Comparaison effet batteries par scenario,Impact FAR/surplus/capture compare entre scenarios utiles.,Q4 summary non vide pour >=1 scenario,HIGH,HIGH_GAS,PASS,7,>0 lignes,Resultats Q4 prospectifs disponibles.
Q4-S-02,Q4,Slides 23-25,SCEN,DEFAULT,Sensibilite valeur commodites,Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.,delta pv_capture ou revenus vs BASE,MEDIUM,BASE,PASS,share_finite=100.00%,>=80% valeurs finies,Sensibilite valeur exploitable sur le panel.
Q4-S-02,Q4,Slides 23-25,SCEN,DEFAULT,Sensibilite valeur commodites,Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.,delta pv_capture ou revenus vs BASE,MEDIUM,FLEX_UP,PASS,share_finite=100.00%,>=80% valeurs finies,Sensibilite valeur exploitable sur le panel.
Q4-S-02,Q4,Slides 23-25,SCEN,DEFAULT,Sensibilite valeur commodites,Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.,delta pv_capture ou revenus vs BASE,MEDIUM,HIGH_CO2,PASS,share_finite=100.00%,>=80% valeurs finies,Sensibilite valeur exploitable sur le panel.
Q4-S-02,Q4,Slides 23-25,SCEN,DEFAULT,Sensibilite valeur commodites,Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.,delta pv_capture ou revenus vs BASE,MEDIUM,HIGH_GAS,PASS,share_finite=100.00%,>=80% valeurs finies,Sensibilite valeur exploitable sur le panel.
```

### Q4 - comparaison HIST vs SCEN
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\comparison_hist_vs_scen.csv`

```csv
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
DE,BASE,far_after,0.9905525567082653,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,BASE,surplus_unabs_energy_after,0.0628905475,0.0,-0.0628905475,,INFORMATIVE,delta_interpretable
DE,BASE,pv_capture_price_after,46.22796099131209,133.15273800112763,86.92477700981554,,INFORMATIVE,delta_interpretable
ES,BASE,far_after,0.9653226280664032,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,BASE,surplus_unabs_energy_after,0.2995817,0.0,-0.2995817,,INFORMATIVE,delta_interpretable
ES,BASE,pv_capture_price_after,42.80117347476487,98.40603141928084,55.60485794451599,,INFORMATIVE,delta_interpretable
DE,FLEX_UP,far_after,0.9905525567082653,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,FLEX_UP,surplus_unabs_energy_after,0.0628905475,0.0,-0.0628905475,,INFORMATIVE,delta_interpretable
DE,FLEX_UP,pv_capture_price_after,46.22796099131209,133.13539945763245,86.90743846632036,,INFORMATIVE,delta_interpretable
ES,FLEX_UP,far_after,0.9653226280664032,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,FLEX_UP,surplus_unabs_energy_after,0.2995817,0.0,-0.2995817,,INFORMATIVE,delta_interpretable
ES,FLEX_UP,pv_capture_price_after,42.80117347476487,98.37607547031716,55.57490199555228,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,far_after,0.9905525567082653,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,HIGH_CO2,surplus_unabs_energy_after,0.0628905475,0.0,-0.0628905475,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,pv_capture_price_after,46.22796099131209,145.73395548404667,99.5059944927346,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,far_after,0.9653226280664032,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,HIGH_CO2,surplus_unabs_energy_after,0.2995817,0.0,-0.2995817,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,pv_capture_price_after,42.80117347476487,103.49761706397923,60.69644358921438,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,far_after,0.9905525567082653,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,HIGH_GAS,surplus_unabs_energy_after,0.0628905475,0.0,-0.0628905475,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,pv_capture_price_after,46.22796099131209,149.25240313522823,103.02444214391616,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,far_after,0.9653226280664032,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,HIGH_GAS,surplus_unabs_energy_after,0.2995817,0.0,-0.2995817,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,pv_capture_price_after,42.80117347476487,109.40495630431788,66.60378282955303,,INFORMATIVE,delta_interpretable
DE,HIST_PRICE_ARBITRAGE_SIMPLE,far_after,0.9905525567082653,0.9905525567082653,0.0,,FRAGILE,delta_quasi_nul_vs_historique
ES,HIST_PRICE_ARBITRAGE_SIMPLE,far_after,0.9653226280664032,0.9653226280664032,0.0,,FRAGILE,delta_quasi_nul_vs_historique
DE,HIST_PV_COLOCATED,far_after,0.9905525567082653,0.9905525567082653,0.0,,FRAGILE,delta_quasi_nul_vs_historique
ES,HIST_PV_COLOCATED,far_after,0.9653226280664032,0.9653226280664032,0.0,,FRAGILE,delta_quasi_nul_vs_historique
```

### Q4 - checks filtrés
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\checks_filtered.csv`

```csv
status,code,message,scope,scenario_id,question_id,mentioned_countries,is_global
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,HIST,,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,HIST,,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,HIST,,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,HIST,,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,HIST,,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,HIST,,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,HIST,,Q4,,True
FAIL,Q4_SURPLUS_INCREASE,Surplus non absorbe augmente en mode SURPLUS_FIRST.,SCEN,BASE,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,BASE,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,BASE,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,BASE,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,BASE,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,BASE,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,BASE,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,BASE,Q4,,True
FAIL,Q4_SURPLUS_INCREASE,Surplus non absorbe augmente en mode SURPLUS_FIRST.,SCEN,FLEX_UP,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,FLEX_UP,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,FLEX_UP,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,FLEX_UP,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,FLEX_UP,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,FLEX_UP,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,FLEX_UP,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,FLEX_UP,Q4,,True
FAIL,Q4_SURPLUS_INCREASE,Surplus non absorbe augmente en mode SURPLUS_FIRST.,SCEN,HIGH_CO2,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_CO2,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_CO2,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_CO2,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_CO2,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_CO2,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_CO2,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_CO2,Q4,,True
FAIL,Q4_SURPLUS_INCREASE,Surplus non absorbe augmente en mode SURPLUS_FIRST.,SCEN,HIGH_GAS,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_GAS,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_GAS,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_GAS,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_GAS,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_GAS,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_GAS,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,SCEN,HIGH_GAS,Q4,,True
PASS,BUNDLE_LEDGER_STATUS,"ledger: FAIL=0, WARN=0",BUNDLE,,Q4,,True
PASS,BUNDLE_INFORMATIVENESS,share_tests_informatifs=100.00% ; share_compare_informatifs=66.33%,BUNDLE,,Q4,,True
```

### Q4 - warnings filtrés
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\warnings_filtered.csv`

```csv
question_id,status,code,message,scope,scenario_id,mentioned_countries,is_global
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,BASE: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,BASE: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,BASE: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,BASE: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,BASE: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,BASE: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,FLEX_UP: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,FLEX_UP: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,FLEX_UP: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,FLEX_UP: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,FLEX_UP: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,FLEX_UP: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,HIGH_CO2: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,HIGH_CO2: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,HIGH_CO2: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,HIGH_CO2: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,HIGH_CO2: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,HIGH_CO2: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,HIGH_GAS: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,HIGH_GAS: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,HIGH_GAS: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,HIGH_GAS: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,HIGH_GAS: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,HIGH_GAS: Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
```

### Q4 - historique - Q4_bess_frontier.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\hist\tables\Q4_bess_frontier.csv`

```csv
dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,revenue_bess_price_taker,soc_min,soc_max,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,initial_deliverable_mwh,engine_version,compute_time_sec,cache_hit
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,0.9314362994898376,0.9314362994898376,0.0479559767319999,0.0479559767319999,39.10758174005171,39.10758174005171,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,0.9314362994898376,0.9314362994898376,0.0479559767319999,0.0479559767319999,39.10758174005171,39.10758174005171,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,0.9314362994898376,0.9314362994898376,0.0479559767319999,0.0479559767319999,39.10758174005171,39.10758174005171,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,0.9314362994898376,0.9314362994898376,0.0479559767319999,0.0479559767319999,39.10758174005171,39.10758174005171,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,0.9314362994898376,0.9597276885521075,0.0479559767319999,0.0281679374999999,39.10758174005171,39.10758174005171,1727290.5928096755,0.0,469.04157598234303,250.0,250.0,19788.039232,17647.995312151168,234.5207879911715,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,0.9314362994898376,0.9705223983408284,0.0479559767319999,0.0206177199999999,39.10758174005171,39.10758174005171,2335601.505613262,0.0,938.083151964686,250.0,250.0,27338.256731999994,24526.707500142336,469.041575982343,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,0.9314362994898376,0.974010908562442,0.0479559767319999,0.0181777274999999,39.10758174005171,39.10758174005171,2462875.0503788227,0.0,1407.124727947029,250.0,250.0,29778.249231999995,26908.42168813351,703.5623639735145,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,0.9314362994898376,0.9745547318049296,0.0479559767319999,0.0177973575,39.10758174005171,39.10758174005171,2337955.834643081,0.0,1641.6455159382006,250.0,250.0,30158.61923199999,27477.668076124675,938.083151964686,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,0.9314362994898376,0.9751682539802228,0.0479559767319999,0.0173682374999999,39.10758174005171,39.10758174005171,2711001.5422180807,0.0,938.083151964686,500.0,500.0,30587.739231999996,27386.252100142337,469.041575982343,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,0.9314362994898376,0.9872389260474462,0.0479559767319999,0.008925565,39.10758174005171,39.10758174005171,3316187.6365040718,0.0,1876.166303929372,500.0,500.0,39030.41173199999,35284.84547612468,938.083151964686,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,0.9314362994898376,0.9907067446217772,0.0479559767319999,0.006500045,39.10758174005171,39.10758174005171,3424356.087857598,0.0,2814.2494558940584,500.0,500.0,41455.93173199999,37888.34465210702,1407.124727947029,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,0.9314362994898376,0.991535961761126,0.0479559767319999,0.00592006,39.10758174005171,39.10758174005171,3221341.983292116,0.0,3258.8985247174387,500.0,500.0,42035.91673199998,38867.77302808936,1876.166303929372,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,0.9314362994898376,0.9833685729031856,0.0479559767319999,0.0116326324999999,39.10758174005171,39.10758174005171,3238527.902016486,0.0,1407.124727947029,750.0,750.0,36323.34423199999,32668.105288133516,703.5623639735145,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,0.9314362994898376,0.993297521865942,0.0479559767319999,0.0046879599999999,39.10758174005171,39.10758174005171,3675703.400357883,0.0,2814.249455894058,750.0,750.0,43268.01673199999,39482.97945210702,1407.124727947029,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,0.9314362994898376,0.9972419596143188,0.0479559767319999,0.0019290749999999,39.10758174005171,39.10758174005171,3755654.896565376,0.0,4221.374183841087,750.0,750.0,46026.90173199999,42614.360616080536,2110.6870919205435,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,0.9314362994898376,0.9973138067039764,0.0479559767319999,0.0018788224999999,39.10758174005171,39.10758174005171,3518036.3997931518,0.0,4268.515207435193,750.0,750.0,46077.15423199999,43362.14518005405,2814.249455894058,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,0.9314362994898376,0.9881941874517416,0.0479559767319999,0.0082574199999999,39.10758174005171,39.10758174005171,3584339.279420891,0.0,1876.166303929372,905.4375000000008,1000.0,39698.55673199999,35872.81307612468,938.083151964686,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,0.9314362994898376,0.9968207064130502,0.0479559767319999,0.0022237149999999,39.10758174005171,39.10758174005171,3900687.043298693,0.0,3752.332607858744,1000.0,1000.0,45732.26173199999,42120.55662808937,1876.166303929372,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,0.9314362994898376,0.9996005321831134,0.0479559767319999,0.0002794025,39.10758174005171,39.10758174005171,3865136.959625152,0.0,4812.099215880527,1000.0,1000.0,47676.574231999984,44769.63478005405,2814.249455894058,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,0.9314362994898376,0.9996005321831134,0.0479559767319999,0.0002794025,39.10758174005171,39.10758174005171,3636925.751260187,0.0,4812.099215880527,1000.0,1000.0,47676.574231999984,45707.71793201873,3752.332607858744,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,0.9314362994898376,0.993297521865942,0.0479559767319999,0.0046879599999999,39.10758174005171,39.10758174005171,3968219.7600447023,0.0,2814.249455894058,1212.8100000000009,1500.0,43268.01673199999,39482.97945210702,1407.124727947029,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,0.9314362994898376,1.0,0.0479559767319999,0.0,39.10758174005171,39.10758174005171,4076376.822483315,0.0,5074.20199374734,1212.8100000000009,1500.0,47955.97673199999,45015.508980054045,2814.249455894058,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,0.9314362994898376,1.0,0.0479559767319999,0.0,39.10758174005171,39.10758174005171,3904171.9152337047,0.0,5074.20199374734,1212.8100000000009,1500.0,47955.97673199999,46422.63370800107,4221.374183841087,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,0.9314362994898376,1.0,0.0479559767319999,0.0,39.10758174005171,39.10758174005171,3688155.5469272574,0.0,6000.0,1212.8100000000009,1500.0,47955.97673199999,47829.7584359481,5628.498911788116,v2.1.0,0.4445706999977119,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,0.9753756800932872,0.9753756800932872,0.0653106699999999,0.0653106699999999,53.46276957278948,53.46276957278948,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,0.9753756800932872,0.9753756800932872,0.0653106699999999,0.0653106699999999,53.46276957278948,53.46276957278948,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,0.9753756800932872,0.9753756800932872,0.0653106699999999,0.0653106699999999,53.46276957278948,53.46276957278948,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,0.9753756800932872,0.9753756800932872,0.0653106699999999,0.0653106699999999,53.46276957278948,53.46276957278948,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,0.9753756800932872,0.9852731042412398,0.0653106699999999,0.0390598982091109,53.46276957278948,53.46276957278948,1858961.7552350007,0.0,500.0,250.0,250.0,26250.77179088901,23335.199963973504,234.5207879911715,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,0.9753756800932872,0.9884258866405284,0.0653106699999999,0.0306978264182219,53.46276957278948,53.46276957278948,2202788.4509225585,0.0,1000.0,250.0,250.0,34612.84358177805,30928.343927947026,469.041575982343,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,0.9753756800932872,0.9890998517805336,0.0653106699999999,0.0289102799999999,53.46276957278948,53.46276957278948,2047339.8417925185,0.0,1500.0,250.0,250.0,36400.38999999999,32735.905563973512,703.5623639735145,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,0.9753756800932872,0.9892883686025684,0.0653106699999999,0.0284102799999999,53.46276957278948,53.46276957278948,1842851.958309586,0.0,1545.7051935781758,250.0,250.0,36900.38999999999,33410.42635196468,938.083151964686,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,0.9753756800932872,0.9896548541957274,0.0653106699999999,0.0274382564182219,53.46276957278948,53.46276957278948,2621706.0954700075,0.0,1000.0,500.0,500.0,37872.41358177803,33796.76552794702,469.041575982343,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,0.9753756800932872,0.9923323233356074,0.0653106699999999,0.0203368499999999,53.46276957278948,53.46276957278948,2757082.74892953,0.0,2000.0,500.0,500.0,44973.81999999999,40515.04475196469,938.083151964686,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,0.9753756800932872,0.9928527881185536,0.0653106699999999,0.0189564299999999,53.46276957278948,53.46276957278948,2453577.8960462883,0.0,3000.0,500.0,500.0,46354.23999999999,42198.85592794701,1407.124727947029,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,0.9753756800932872,0.993229821762623,0.0653106699999999,0.0179564299999999,53.46276957278948,53.46276957278948,2209888.439335172,0.0,3091.410387156352,500.0,500.0,47354.23999999998,43547.89750392936,1876.166303929372,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,0.9753756800932872,0.9918558528639276,0.0653106699999999,0.0216005846273329,53.46276957278948,53.46276957278948,3087085.465358237,0.0,1500.0,750.0,750.0,43710.08537266708,39168.43749192054,703.5623639735145,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,0.9753756800932872,0.9935832870336015,0.0653106699999999,0.0170189399999999,53.46276957278948,53.46276957278948,2950035.1975202947,0.0,3000.0,750.0,750.0,48291.73,43903.84712794703,1407.124727947029,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,0.9753756800932872,0.9941488374997056,0.0653106699999999,0.0155189399999999,53.46276957278948,53.46276957278948,2593731.136251432,0.0,4500.0,750.0,750.0,49791.73,45927.40949192054,2110.6870919205435,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,0.9753756800932872,0.9947143879658098,0.0653106699999999,0.0140189399999999,53.46276957278948,53.46276957278948,2363521.7443367587,0.0,4637.115580734528,750.0,750.0,51291.73,47950.97185589405,2814.249455894058,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,0.9753756800932872,0.9929827327639824,0.0653106699999999,0.0186117799999999,53.46276957278948,53.46276957278948,3336471.1777968574,0.0,2000.0,1000.0,1000.0,46698.89,42033.106351964685,938.083151964686,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,0.9753756800932872,0.994172059001844,0.0653106699999999,0.0154573499999999,53.46276957278948,53.46276957278948,3012631.697131648,0.0,4000.0,1000.0,1000.0,49853.31999999999,45747.087903929365,1876.166303929372,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,0.9753756800932872,0.9949261262899828,0.0653106699999999,0.0134573499999999,53.46276957278948,53.46276957278948,2674513.72511675,0.0,6000.0,1000.0,1000.0,51853.31999999999,48445.17105589406,2814.249455894058,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,0.9753756800932872,0.9956801935781214,0.0653106699999999,0.0114573499999999,53.46276957278948,53.46276957278948,2495365.706574345,0.0,6182.820774312703,1000.0,1000.0,53853.31999999999,51143.25420785874,3752.332607858744,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,0.9753756800932872,0.9941426541479432,0.0653106699999999,0.0155353399999999,53.46276957278948,53.46276957278948,3543770.645574922,0.0,3000.0,1500.0,1500.0,49775.32999999999,45209.41512794703,1407.124727947029,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,0.9753756800932872,0.9952737550801514,0.0653106699999999,0.0125353399999999,53.46276957278948,53.46276957278948,3129127.1693779025,0.0,6000.0,1500.0,1500.0,52775.32999999999,49256.53985589407,2814.249455894058,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,0.9753756800932872,0.9964048560123596,0.0653106699999999,0.0095353399999999,53.46276957278948,53.46276957278948,2908034.621414852,0.0,9000.0,1500.0,1500.0,55775.32999999999,53303.66458384108,4221.374183841087,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,0.9753756800932872,0.9975359569445676,0.0653106699999999,0.00653534,53.46276957278948,53.46276957278948,2806083.3249255177,0.0,9201.070056447326,1500.0,1500.0,58775.32999999999,57350.78931178811,5628.498911788116,v2.1.0,0.4498683999991044,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,0.9905525567082653,0.9905525567082653,0.0628905475,0.0628905475,46.22796099131209,46.22796099131209,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,0.9905525567082653,0.9905525567082653,0.0628905475,0.0628905475,46.22796099131209,46.22796099131209,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,0.9905525567082653,0.9905525567082653,0.0628905475,0.0628905475,46.22796099131209,46.22796099131209,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,0.9905525567082653,0.9905525567082653,0.0628905475,0.0628905475,46.22796099131209,46.22796099131209,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,0.9905525567082653,0.9917778803809596,0.0628905475,0.054733708209111,46.22796099131209,46.22796099131209,1036855.4314372694,0.0,500.0,250.0,250.0,8156.839290889036,7412.539363973523,234.5207879911715,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,0.9905525567082653,0.9923414698785556,0.0628905475,0.0509819575,46.22796099131209,46.22796099131209,1461411.4576309766,0.0,938.083151964686,250.0,250.0,11908.590000000006,10948.600775982348,469.041575982343,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,0.9905525567082653,0.9924916902799876,0.0628905475,0.0499819575,46.22796099131209,46.22796099131209,1509337.2686784645,0.0,1407.124727947029,250.0,250.0,12908.590000000006,12063.121563973518,703.5623639735145,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,0.9905525567082653,0.99250838840426,0.0628905475,0.0498708,46.22796099131209,46.22796099131209,1485889.9353350848,0.0,1511.3997059115432,250.0,250.0,13019.747500000003,12395.460951964693,938.083151964686,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,0.9905525567082653,0.9927831540741672,0.0628905475,0.048041716418222,46.22796099131209,46.22796099131209,1914513.6279515363,0.0,1000.0,500.0,500.0,14848.831081778057,13536.012927947031,469.041575982343,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,0.9905525567082653,0.9937571063821432,0.0628905475,0.0415582275,46.22796099131209,46.22796099131209,2649798.6937759523,0.0,1876.166303929372,500.0,500.0,21332.320000000007,19710.52475196469,938.083151964686,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,0.9905525567082653,0.9940575471850074,0.0628905475,0.0395582275,46.22796099131209,46.22796099131209,2754886.1216889285,0.0,2814.249455894058,500.0,500.0,23332.320000000007,21939.566327947035,1407.124727947029,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,0.9905525567082653,0.9940742453092796,0.0628905475,0.03944707,46.22796099131209,46.22796099131209,2699925.7898531696,0.0,2918.524433858572,500.0,500.0,23443.477500000008,22506.42650392937,1876.166303929372,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,0.9905525567082653,0.9936602743673624,0.0628905475,0.0422028271273329,46.22796099131209,46.22796099131209,2694679.196539807,0.0,1500.0,750.0,750.0,20687.7203726671,18908.756291920567,703.5623639735145,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,0.9905525567082653,0.9949958196812912,0.0628905475,0.033312255,46.22796099131209,46.22796099131209,3717487.503726929,0.0,2814.249455894058,750.0,750.0,29578.292500000018,27436.02212794705,1407.124727947029,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,0.9905525567082653,0.9954464808855876,0.0628905475,0.030312255,46.22796099131209,46.22796099131209,3883975.048805393,0.0,4221.374183841087,750.0,750.0,32578.292500000018,30779.58449192056,2110.6870919205435,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,0.9905525567082653,0.9954546787884448,0.0628905475,0.0302576825,46.22796099131209,46.22796099131209,3794820.707157253,0.0,4272.567726651673,750.0,750.0,32632.865000000005,31531.170655894068,2814.249455894058,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,0.9905525567082653,0.9944346243773254,0.0628905475,0.0370480678364439,46.22796099131209,46.22796099131209,3379159.650790076,0.0,2000.0,1000.0,1000.0,25842.479663556136,23679.465255894083,938.083151964686,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,0.9905525567082653,0.9960208384505862,0.0628905475,0.0264888225,46.22796099131209,46.22796099131209,4591627.340720907,0.0,3752.332607858744,1000.0,1000.0,36401.72500000004,33909.6843039294,1876.166303929372,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,0.9905525567082653,0.9965843962953748,0.0628905475,0.0227372825,46.22796099131209,46.22796099131209,4797914.176294859,0.0,5395.422771850969,1000.0,1000.0,40153.26500000004,38149.12265589408,2814.249455894058,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,0.9905525567082653,0.9965843962953748,0.0628905475,0.0227372825,46.22796099131209,46.22796099131209,4674879.25122734,0.0,5395.422771850969,1000.0,1000.0,40153.26500000004,39087.20580785877,3752.332607858744,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,0.9905525567082653,0.9956380945186344,0.0628905475,0.029036705,46.22796099131209,46.22796099131209,4505306.09543693,0.0,2999.689733374434,1500.0,1500.0,33853.84250000002,31198.506127947046,1407.124727947029,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,0.9905525567082653,0.9978042028547988,0.0628905475,0.01461717,46.22796099131209,46.22796099131209,6143342.761628859,0.0,5628.498911788116,1500.0,1500.0,48273.37750000003,45294.82165589408,2814.249455894058,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,0.9905525567082653,0.9982863607706632,0.0628905475,0.0114075,46.22796099131209,46.22796099131209,6258497.806573788,0.0,6744.667769321776,1500.0,1500.0,51483.04750000005,49526.45598384113,4221.374183841087,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,0.9905525567082653,0.9982863607706632,0.0628905475,0.0114075,46.22796099131209,46.22796099131209,6080459.12290551,0.0,6744.667769321776,1500.0,1500.0,51483.04750000005,50933.58071178816,5628.498911788116,v2.1.0,0.4139543999917805,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,0.9653226280664032,0.9653226280664032,0.2995817,0.2995817,42.80117347476487,42.80117347476487,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,0.9653226280664032,0.9653226280664032,0.2995817,0.2995817,42.80117347476487,42.80117347476487,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,0.9653226280664032,0.9653226280664032,0.2995817,0.2995817,42.80117347476487,42.80117347476487,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,0.9653226280664032,0.9653226280664032,0.2995817,0.2995817,42.80117347476487,42.80117347476487,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,0.9653226280664032,0.969356685012072,0.2995817,0.2647310302319887,42.80117347476487,42.80117347476487,2499796.970854916,0.0,500.0,250.0,250.0,34850.66976801126,30903.110183841087,234.5207879911715,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,0.9653226280664032,0.9719721127724472,0.2995817,0.2421360568821993,42.80117347476487,42.80117347476487,4002521.950667413,0.0,1000.0,250.0,250.0,57445.6431178006,51021.20751964686,469.041575982343,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,0.9653226280664032,0.9733602144157312,0.2995817,0.2301440913184828,42.80117347476487,42.80117347476487,4698599.582029509,0.0,1500.0,250.0,250.0,69437.6086815172,61808.65800370867,703.5623639735145,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,0.9653226280664032,0.9741127410780088,0.2995817,0.2236429292000802,42.80117347476487,42.80117347476487,4930644.740818493,0.0,2000.0,250.0,250.0,75938.77079991973,67764.20145589407,938.083151964686,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,0.9653226280664032,0.9730473964842709,0.2995817,0.2328465604639774,42.80117347476487,42.80117347476487,4817718.309709832,0.0,1000.0,500.0,500.0,66735.13953602253,59195.96436768217,469.041575982343,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,0.9653226280664032,0.977660978584102,0.2995817,0.1929893079823398,42.80117347476487,42.80117347476487,7483437.168325379,0.0,2000.0,500.0,500.0,106592.39201766014,94739.3881275056,938.083151964686,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,0.9653226280664032,0.9801078186465269,0.2995817,0.1718507826369655,42.80117347476487,42.80117347476487,8768842.281479463,0.0,3000.0,500.0,500.0,127730.91736303444,113810.33200741732,1407.124727947029,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,0.9653226280664032,0.9812937535246494,0.2995817,0.1616053584001605,42.80117347476487,42.80117347476487,9044145.964116102,0.0,4000.0,500.0,500.0,137976.3415998395,123295.34691178812,1876.166303929372,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,0.9653226280664032,0.976424466522882,0.2995817,0.2036716741685731,42.80117347476487,42.80117347476487,6929252.860468533,0.0,1500.0,750.0,750.0,95910.02583142692,85104.3850956292,703.5623639735145,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,0.9653226280664032,0.982274311066518,0.2995817,0.1531342119735098,42.80117347476487,42.80117347476487,10368221.721188068,0.0,3000.0,750.0,750.0,146447.4880264902,130280.9141912584,1407.124727947029,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,0.9653226280664032,0.985420934352681,0.2995817,0.1259501809825405,42.80117347476487,42.80117347476487,12086294.20122847,0.0,4500.0,750.0,750.0,173631.51901745948,154906.4238272849,2110.6870919205435,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,0.9653226280664032,0.9869245834988316,0.2995817,0.1129599876002407,42.80117347476487,42.80117347476487,12358835.780654153,0.0,6000.0,750.0,750.0,186621.71239975924,167041.35636768217,2814.249455894058,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,0.9653226280664032,0.9793896560559292,0.2995817,0.1780550696913505,42.80117347476487,42.80117347476487,8803646.146830399,0.0,2000.0,1000.0,1000.0,121526.63030864947,107881.51782357624,938.083151964686,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,0.9653226280664032,0.986007136385698,0.2995817,0.1208859159646797,42.80117347476487,42.80117347476487,12796838.161312109,0.0,4000.0,1000.0,1000.0,178695.78403532028,159128.4562550112,1876.166303929372,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,0.9653226280664032,0.9895306205880818,0.2995817,0.090446141310054,42.80117347476487,42.80117347476487,14732806.560344623,0.0,6000.0,1000.0,1000.0,209135.558689946,186853.54110304653,2814.249455894058,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,0.9653226280664032,0.9910779140263488,0.2995817,0.0770788999999999,42.80117347476487,42.80117347476487,14848873.771271529,0.0,7377.128547193561,1000.0,1000.0,222502.8,199554.7966078588,3752.332607858744,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,0.9653226280664032,0.984481725056654,0.2995817,0.1340641152823599,42.80117347476487,42.80117347476487,12086637.04863045,0.0,3000.0,1500.0,1500.0,165517.58471764007,147062.5992794703,1407.124727947029,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,0.9653226280664032,0.9917510006919352,0.2995817,0.0712640289102948,42.80117347476487,42.80117347476487,16510578.385764362,0.0,6000.0,1500.0,1500.0,228317.6710897052,203733.80001483465,2814.249455894058,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,0.9653226280664032,0.9951130921072784,0.2995817,0.0422185446189041,42.80117347476487,42.80117347476487,18210984.114635915,0.0,9000.0,1500.0,1500.0,257363.15538109583,230700.95091920544,4221.374183841087,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,0.9653226280664032,0.9960806272681728,0.2995817,0.0338599,42.80117347476487,42.80117347476487,17662410.271187287,0.0,10052.499056453576,1500.0,1500.0,265721.8,239463.6829117881,5628.498911788116,v2.1.0,0.4159198999986984,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,0.7911028464042443,0.7911028464042443,12.73752722,12.73752722,39.24796162782507,39.24796162782507,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,0.7911028464042443,0.7911028464042443,12.73752722,12.73752722,39.24796162782507,39.24796162782507,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,0.7911028464042443,0.7911028464042443,12.73752722,12.73752722,39.24796162782507,39.24796162782507,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,0.7911028464042443,0.7911028464042443,12.73752722,12.73752722,39.24796162782507,39.24796162782507,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,0.7911028464042443,0.793781491299773,12.73752722,12.574196548986956,39.24796162782507,39.24796162782507,6556286.162065834,0.0,500.0,250.0,250.0,163330.67101304443,143745.5112794703,234.5207879911715,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,0.7911028464042443,0.7963771952073787,12.73752722,12.415923213955448,39.24796162782507,39.24796162782507,12292529.303524151,0.0,1000.0,250.0,250.0,321604.0060445516,283260.5668951878,469.041575982343,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,0.7911028464042443,0.7988059325439245,12.73752722,12.267830684201083,39.24796162782507,39.24796162782507,15359033.673722276,0.0,1500.0,250.0,250.0,469696.5357989165,413816.51386702,703.5623639735145,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,0.7911028464042443,0.8010607714974883,12.73752722,12.130341627728276,39.24796162782507,39.24796162782507,17531001.38913453,0.0,2000.0,250.0,250.0,607185.592271724,535041.4043510818,938.083151964686,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,0.7911028464042443,0.7964378240813219,12.73752722,12.412226361610276,39.24796162782507,39.24796162782507,13144189.853783026,0.0,1000.0,500.0,500.0,325300.85838972527,286293.79695894057,469.041575982343,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,0.7911028464042443,0.8016144259467787,12.73752722,12.096582485983545,39.24796162782507,39.24796162782507,24616879.36367905,0.0,2000.0,500.0,500.0,640944.7340164562,564529.4490864462,938.083151964686,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,0.7911028464042443,0.8064101477133828,12.73752722,11.80416281682962,39.24796162782507,39.24796162782507,30744074.187616035,0.0,3000.0,500.0,500.0,933364.4031703796,822327.7995178811,1407.124727947029,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,0.7911028464042443,0.8108648044833043,12.73752722,11.532539623856712,39.24796162782507,39.24796162782507,35044855.07624681,0.0,4000.0,500.0,500.0,1204987.5961432876,1061825.2509100223,1876.166303929372,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,0.7911028464042443,0.7990793859208429,12.73752722,12.251156834069835,39.24796162782507,39.24796162782507,19752691.59564119,0.0,1500.0,750.0,750.0,486370.3859301628,428049.5019825168,703.5623639735145,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,0.7911028464042443,0.8067936883215853,12.73752722,11.780776385502708,39.24796162782507,39.24796162782507,36924073.27403598,0.0,3000.0,750.0,750.0,956750.8344972912,842687.8590855633,1407.124727947029,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,0.7911028464042443,0.8139229416726922,12.73752722,11.34606936793498,39.24796162782507,39.24796162782507,46213170.8608059,0.0,4500.0,750.0,750.0,1391457.8520650216,1225933.5969091393,2110.6870919205435,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,0.7911028464042443,0.8204951939849203,12.73752722,10.945325550785068,39.24796162782507,39.24796162782507,52576881.1281072,0.0,6000.0,750.0,750.0,1792201.669214931,1579291.7183650336,2814.249455894058,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,0.7911028464042443,0.8016991867898808,12.73752722,12.09141418412964,39.24796162782507,39.24796162782507,26352082.686379828,0.0,2000.0,1000.0,1000.0,646113.0358703596,568838.3531178811,938.083151964686,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,0.7911028464042443,0.8119003246875639,12.73752722,11.469398664003611,39.24796162782507,39.24796162782507,49099770.064560905,0.0,4000.0,1000.0,1000.0,1268128.5559963884,1117150.093980751,1876.166303929372,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,0.7911028464042443,0.8213206590916351,12.73752722,10.894992723913305,39.24796162782507,39.24796162782507,61669457.43311803,0.0,6000.0,1000.0,1000.0,1842534.4960866957,1623565.404412186,2814.249455894058,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,0.7911028464042443,0.8299128361918838,12.73752722,10.371083767713424,39.24796162782507,39.24796162782507,70033881.7836378,0.0,8000.0,1000.0,1000.0,2366443.452286575,2085543.3690200453,3752.332607858744,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,0.7911028464042443,0.8068676763675017,12.73752722,11.776264956157735,39.24796162782507,39.24796162782507,39630283.27768111,0.0,3000.0,1500.0,1500.0,961262.2638422642,846638.7153091396,1407.124727947029,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,0.7911028464042443,0.8219579634276201,12.73752722,10.856133021005418,39.24796162782507,39.24796162782507,73128055.83588904,0.0,6000.0,1500.0,1500.0,1881394.1989945823,1657761.9429711266,2814.249455894058,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,0.7911028464042443,0.8357729867255173,12.73752722,10.013760435869957,39.24796162782507,39.24796162782507,92302920.78466396,0.0,9000.0,1500.0,1500.0,2723766.784130043,2400456.942618279,4221.374183841087,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,0.7911028464042443,0.84814284556221,12.73752722,9.25950691480554,39.24796162782507,39.24796162782507,104695652.76155524,0.0,12000.0,1500.0,1500.0,3478020.3051944617,3065607.165882915,5628.498911788116,v2.1.0,0.8221879000193439,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,0.927500635216397,0.927500635216397,0.001712,0.001712,96.09890313752672,96.09890313752672,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,0.927500635216397,0.927500635216397,0.001712,0.001712,96.09890313752672,96.09890313752672,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,0.927500635216397,0.927500635216397,0.001712,0.001712,96.09890313752672,96.09890313752672,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,0.927500635216397,0.927500635216397,0.001712,0.001712,96.09890313752672,96.09890313752672,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,0.927500635216397,0.9576522401964936,0.001712,0.001,96.09890313752672,96.09890313752672,54282.17362083905,0.0,250.0,250.0,234.5207879911715,712.0,861.0807879911715,234.5207879911715,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,0.927500635216397,0.9576522401964936,0.001712,0.001,96.09890313752672,96.09890313752672,79297.35804167809,0.0,500.0,250.0,250.0,712.0,1095.6015759823429,469.041575982343,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,0.927500635216397,0.9576522401964936,0.001712,0.001,96.09890313752672,96.09890313752672,102761.07366251716,0.0,750.0,250.0,250.0,712.0,1330.1223639735144,703.5623639735145,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,0.927500635216397,0.9576522401964936,0.001712,0.001,96.09890313752672,96.09890313752672,132318.41085933853,0.0,1000.0,250.0,250.0,712.0,1564.6431519646858,938.083151964686,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,0.927500635216397,0.9686203099856018,0.001712,0.000741,96.09890313752672,96.09890313752672,86728.93324167811,0.0,500.0,500.0,469.041575982343,971.0,1323.5215759823432,469.041575982343,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,0.927500635216397,0.9686203099856018,0.001712,0.000741,96.09890313752672,96.09890313752672,137322.8012833562,0.0,1000.0,500.0,500.0,971.0,1792.563151964686,938.083151964686,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,0.927500635216397,0.9686203099856018,0.001712,0.000741,96.09890313752672,96.09890313752672,185806.6005250343,0.0,1500.0,500.0,500.0,971.0,2261.604727947029,1407.124727947029,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,0.927500635216397,0.9686203099856018,0.001712,0.000741,96.09890313752672,96.09890313752672,246152.2629186771,0.0,2000.0,500.0,500.0,971.0,2730.646303929372,1876.166303929372,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,0.927500635216397,0.9792072499364785,0.001712,0.000491,96.09890313752672,96.09890313752672,119111.21686251716,0.0,750.0,750.0,703.5623639735145,1221.0,1778.0423639735145,703.5623639735145,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,0.927500635216397,0.9792072499364785,0.001712,0.000491,96.09890313752672,96.09890313752672,195283.7685250343,0.0,1500.0,750.0,750.0,1221.0,2481.604727947029,1407.124727947029,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,0.927500635216397,0.9792072499364785,0.001712,0.000491,96.09890313752672,96.09890313752672,268787.6513875514,0.0,2250.0,750.0,750.0,1221.0,3185.167091920543,2110.6870919205435,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,0.927500635216397,0.9792072499364785,0.001712,0.000491,96.09890313752672,96.09890313752672,359921.63897801563,0.0,3000.0,750.0,750.0,1221.0,3888.7294558940575,2814.249455894058,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,0.927500635216397,0.989794189887355,0.001712,0.000241,96.09890313752672,96.09890313752672,151493.5004833562,0.0,1000.0,1000.0,938.083151964686,1471.0,2232.563151964686,938.083151964686,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,0.927500635216397,0.989794189887355,0.001712,0.000241,96.09890313752672,96.09890313752672,253244.7357667124,0.0,2000.0,1000.0,1000.0,1471.0,3170.646303929372,1876.166303929372,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,0.927500635216397,0.989794189887355,0.001712,0.000241,96.09890313752672,96.09890313752672,351768.70225006854,0.0,3000.0,1000.0,1000.0,1471.0,4108.7294558940575,2814.249455894058,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,0.927500635216397,0.989794189887355,0.001712,0.000241,96.09890313752672,96.09890313752672,473691.0150373542,0.0,4000.0,1000.0,1000.0,1471.0,5046.812607858743,3752.332607858744,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,0.927500635216397,1.0,0.001712,0.0,96.09890313752672,96.09890313752672,214659.7269250343,0.0,1500.0,1241.0,1407.124727947029,1712.0,2913.6847279470294,1407.124727947029,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,0.927500635216397,1.0,0.001712,0.0,96.09890313752672,96.09890313752672,370050.3782500686,0.0,3000.0,1241.0,1500.0,1712.0,4320.809455894058,2814.249455894058,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,0.927500635216397,1.0,0.001712,0.0,96.09890313752672,96.09890313752672,519074.9103751028,0.0,4500.0,1241.0,1500.0,1712.0,5727.934183841086,4221.374183841087,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,0.927500635216397,1.0,0.001712,0.0,96.09890313752672,96.09890313752672,702724.3007560312,0.0,6000.0,1241.0,1500.0,1712.0,7135.058911788115,5628.498911788116,v2.1.0,0.3654830000014044,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,46.5701146150674,46.5701146150674,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,46.5701146150674,46.5701146150674,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,46.5701146150674,46.5701146150674,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,46.5701146150674,46.5701146150674,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,46.5701146150674,46.5701146150674,19807.62575373434,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,46.5701146150674,46.5701146150674,34638.62690114985,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,46.5701146150674,46.5701146150674,49022.26604065723,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,46.5701146150674,46.5701146150674,58073.85472087631,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,46.5701146150674,46.5701146150674,39615.25150746868,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,46.5701146150674,46.5701146150674,69277.2538022997,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,46.5701146150674,46.5701146150674,98044.53208131446,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,46.5701146150674,46.5701146150674,116147.7094417526,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,46.5701146150674,46.5701146150674,59422.87726120303,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,46.5701146150674,46.5701146150674,103915.88070344955,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,46.5701146150674,46.5701146150674,147066.7981219717,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,46.5701146150674,46.5701146150674,174221.5641626289,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,46.5701146150674,46.5701146150674,79230.50301493736,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,46.5701146150674,46.5701146150674,138554.5076045994,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,46.5701146150674,46.5701146150674,196089.06416262893,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,46.5701146150674,46.5701146150674,232295.4188835052,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,46.5701146150674,46.5701146150674,118845.75452240606,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,46.5701146150674,46.5701146150674,207831.7614068991,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,46.5701146150674,46.5701146150674,294133.5962439434,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3381249000085518,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,46.5701146150674,46.5701146150674,348443.1283252578,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3381249000085518,True
```

### Q4 - historique - Q4_sizing_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\hist\tables\Q4_sizing_summary.csv`

```csv
country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,revenue_bess_price_taker,soc_min,soc_max,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,initial_deliverable_mwh,engine_version,compute_time_sec,cache_hit,notes_quality
DE,2024,SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,0.9905525567082653,0.9905525567082653,0.0628905475,0.0628905475,46.22796099131209,46.22796099131209,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4139543999917805,True,ok
ES,2024,SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,0.9653226280664032,0.9653226280664032,0.2995817,0.2995817,42.80117347476487,42.80117347476487,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4159198999986984,True,ok
```

### Q4 - scénario `BASE`

### Q4/BASE - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\BASE\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
FAIL,Q4_SURPLUS_INCREASE,Surplus non absorbe augmente en mode SURPLUS_FIRST.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
```

### Q4/BASE - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\BASE\warnings_filtered.csv`

```csv
question_id,status,code,message,scope,scenario_id,mentioned_countries,is_global
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
```

### Q4/BASE - Q4_bess_frontier.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\BASE\tables\Q4_bess_frontier.csv`

```csv
dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,revenue_bess_price_taker,soc_min,soc_max,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,initial_deliverable_mwh,engine_version,compute_time_sec,cache_hit
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,0.947655098457812,0.7934613351283482,0.0015369460628298,0.0060643688008615,94.77843633699256,94.77843633699256,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,0.947655098457812,0.7934613351283482,0.0015369460628298,0.0060643688008615,94.77843633699256,94.77843633699256,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,0.947655098457812,0.7934613351283482,0.0015369460628298,0.0060643688008615,94.77843633699256,94.77843633699256,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,0.947655098457812,0.7934613351283482,0.0015369460628298,0.0060643688008615,94.77843633699256,94.77843633699256,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,0.947655098457812,0.81561865003255,0.0015369460628298,0.0054137878101331,94.77843633699256,94.77843633699256,96380.37043029592,0.0,469.041575982343,250.0,250.0,650.5809907283236,807.0320598320964,234.5207879911715,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,0.947655098457812,0.8241330837540903,0.0015369460628298,0.0051637878101331,94.77843633699256,94.77843633699256,144889.15510718455,0.0,703.5623639735145,250.0,250.0,900.5809907283236,1261.5528478232677,469.041575982343,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,0.947655098457812,0.8241330837540903,0.0015369460628298,0.0051637878101331,94.77843633699256,94.77843633699256,164725.9959474475,0.0,750.0,250.0,250.0,900.5809907283236,1496.0736358144395,703.5623639735145,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,0.947655098457812,0.8241330837540903,0.0015369460628298,0.0051637878101331,94.77843633699256,94.77843633699256,185536.696077707,0.0,1000.0,250.0,250.0,900.5809907283236,1730.5944238056109,938.083151964686,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,0.947655098457812,0.8326475174756308,0.0015369460628298,0.0049137878101331,94.77843633699256,94.77843633699256,176992.54888039062,0.0,938.083151964686,500.0,500.0,1150.5809907283235,1481.552847823268,469.041575982343,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,0.947655098457812,0.8394163369488622,0.0015369460628298,0.0047150423710763,94.77843633699256,94.77843633699256,240479.58504493677,0.0,1124.522899873724,500.0,500.0,1349.3264297851554,2125.490410175623,938.083151964686,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,0.947655098457812,0.8394163369488622,0.0015369460628298,0.0047150423710763,94.77843633699256,94.77843633699256,280147.2924582657,0.0,1500.0,500.0,500.0,1349.3264297851554,2594.531986157965,1407.124727947029,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,0.947655098457812,0.8394163369488622,0.0015369460628298,0.0047150423710763,94.77843633699256,94.77843633699256,321772.4530439712,0.0,2000.0,500.0,500.0,1349.3264297851554,3063.573562140308,1876.166303929372,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,94.77843633699256,94.77843633699256,243764.71836780637,0.0,1300.52571661072,687.6196330446637,750.0,1536.9460628298189,2056.0748992637555,703.5623639735145,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,94.77843633699256,94.77843633699256,305753.2222639837,0.0,1500.0,687.6196330446637,750.0,1536.9460628298189,2759.63726323727,1407.124727947029,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,94.77843633699256,94.77843633699256,365304.4001253621,0.0,2250.0,687.6196330446637,750.0,1536.9460628298189,3463.1996272107835,2110.6870919205435,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,94.77843633699256,94.77843633699256,427744.0211665135,0.0,3000.0,687.6196330446637,750.0,1536.9460628298189,4166.7619911842985,2814.249455894058,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,94.77843633699256,94.77843633699256,264471.2540498978,0.0,1300.52571661072,687.6196330446637,1000.0,1536.9460628298189,2290.595687254927,938.083151964686,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,94.77843633699256,94.77843633699256,347332.0765495929,0.0,2000.0,687.6196330446637,1000.0,1536.9460628298189,3228.6788392196127,1876.166303929372,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,94.77843633699256,94.77843633699256,426810.0998317913,0.0,3000.0,687.6196330446637,1000.0,1536.9460628298189,4166.7619911842985,2814.249455894058,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,94.77843633699256,94.77843633699256,510064.1813283886,0.0,4000.0,687.6196330446637,1000.0,1536.9460628298189,5104.845143148985,3752.332607858744,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,94.77843633699256,94.77843633699256,305993.0974685979,0.0,1500.0,687.6196330446637,1407.124727947029,1536.9460628298189,2759.63726323727,1407.124727947029,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,94.77843633699256,94.77843633699256,430535.7485157168,0.0,3000.0,687.6196330446637,1500.0,1536.9460628298189,4166.7619911842985,2814.249455894058,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,94.77843633699256,94.77843633699256,549885.5400846477,0.0,4500.0,687.6196330446637,1500.0,1536.9460628298189,5573.886719131328,4221.374183841087,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,94.77843633699256,94.77843633699256,674768.5424921369,0.0,6000.0,687.6196330446637,1500.0,1536.9460628298189,6981.011447078356,5628.498911788116,v2.1.0,0.4702618999872356,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,30557.55881498197,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,60967.5799700326,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,91011.22650933784,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,120446.95361741248,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,61115.11762996394,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,121935.1599400652,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,182022.45301867567,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,240893.90723482493,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,91672.67644494592,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,182902.7399100978,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,273033.6795280135,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,361340.8608522373,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,122230.23525992788,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,243870.3198801304,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,364044.90603735135,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,481787.81446964986,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,183345.35288989183,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,365805.4798201956,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,546067.359056027,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,1.0,1.0,0.0,0.0,143.30496358646832,143.30496358646832,722681.7217044747,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.2887174999923445,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,133.15273800112763,133.15273800112763,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,133.15273800112763,133.15273800112763,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,133.15273800112763,133.15273800112763,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,133.15273800112763,133.15273800112763,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,133.15273800112763,133.15273800112763,29413.769259352983,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,133.15273800112763,133.15273800112763,58763.91696801622,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,133.15273800112763,133.15273800112763,87887.67454463574,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,133.15273800112763,133.15273800112763,117257.07975212968,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,133.15273800112763,133.15273800112763,58827.53851870597,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,133.15273800112763,133.15273800112763,117527.83393603245,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,133.15273800112763,133.15273800112763,175775.34908927148,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,133.15273800112763,133.15273800112763,234514.15950425935,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,133.15273800112763,133.15273800112763,88241.30777805897,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,133.15273800112763,133.15273800112763,176291.75090404868,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,133.15273800112763,133.15273800112763,263663.0236339072,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,133.15273800112763,133.15273800112763,351771.23925638903,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,133.15273800112763,133.15273800112763,117655.07703741196,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,133.15273800112763,133.15273800112763,235055.6678720649,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,133.15273800112763,133.15273800112763,351550.6981785429,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,133.15273800112763,133.15273800112763,469028.3190085188,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,133.15273800112763,133.15273800112763,176482.61555611793,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,133.15273800112763,133.15273800112763,352583.5018080973,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,133.15273800112763,133.15273800112763,527326.0472678144,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,133.15273800112763,133.15273800112763,703542.4785127781,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3421105000306852,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,98.40603141928084,98.40603141928084,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,98.40603141928084,98.40603141928084,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,98.40603141928084,98.40603141928084,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,98.40603141928084,98.40603141928084,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,98.40603141928084,98.40603141928084,23506.42937883265,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,98.40603141928084,98.40603141928084,46572.10495977416,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,98.40603141928084,98.40603141928084,69504.8273619282,0.0,483.49910455548695,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,98.40603141928084,98.40603141928084,91861.15148144716,0.0,733.499104555487,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,98.40603141928084,98.40603141928084,47012.8587576653,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,98.40603141928084,98.40603141928084,93144.20991954832,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,98.40603141928084,98.40603141928084,139009.6547238564,0.0,966.998209110974,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,98.40603141928084,98.40603141928084,183722.30296289435,0.0,1466.998209110974,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,98.40603141928084,98.40603141928084,70519.28813649795,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,98.40603141928084,98.40603141928084,139716.31487932248,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,98.40603141928084,98.40603141928084,208514.48208578452,0.0,1450.4973136664607,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,98.40603141928084,98.40603141928084,275583.4544443415,0.0,2200.4973136664607,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,98.40603141928084,98.40603141928084,94025.7175153306,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,98.40603141928084,98.40603141928084,186288.41983909663,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,98.40603141928084,98.40603141928084,278019.3094477128,0.0,1933.996418221948,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,98.40603141928084,98.40603141928084,367444.6059257887,0.0,2933.996418221948,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,98.40603141928084,98.40603141928084,141038.5762729959,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,98.40603141928084,98.40603141928084,279432.62975864497,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,98.40603141928084,98.40603141928084,417028.9641715691,0.0,2900.994627332921,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,98.40603141928084,98.40603141928084,551166.908888683,0.0,4400.9946273329215,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3471649999846704,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,141.4176326086802,141.4176326086802,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,141.4176326086802,141.4176326086802,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,141.4176326086802,141.4176326086802,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,141.4176326086802,141.4176326086802,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,141.4176326086802,141.4176326086802,33539.13830585784,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,141.4176326086802,141.4176326086802,66493.04579197383,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,141.4176326086802,141.4176326086802,100049.07428852268,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,141.4176326086802,141.4176326086802,132675.18534335878,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,141.4176326086802,141.4176326086802,67078.27661171567,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,141.4176326086802,141.4176326086802,132986.09158394765,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,141.4176326086802,141.4176326086802,200098.14857704536,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,141.4176326086802,141.4176326086802,265350.3706867176,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,141.4176326086802,141.4176326086802,100617.41491757352,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,141.4176326086802,141.4176326086802,199479.13737592148,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,141.4176326086802,141.4176326086802,300147.222865568,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,141.4176326086802,141.4176326086802,398025.5560300764,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,141.4176326086802,141.4176326086802,134156.55322343134,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,141.4176326086802,141.4176326086802,265972.1831678953,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,141.4176326086802,141.4176326086802,400196.2971540907,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,141.4176326086802,141.4176326086802,530700.7413734351,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,141.4176326086802,141.4176326086802,201234.829835147,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,141.4176326086802,141.4176326086802,398958.27475184295,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,141.4176326086802,141.4176326086802,600294.445731136,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,141.4176326086802,141.4176326086802,796051.1120601527,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.6303388000233099,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,122.1267440828592,122.1267440828592,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,122.1267440828592,122.1267440828592,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,122.1267440828592,122.1267440828592,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,122.1267440828592,122.1267440828592,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,122.1267440828592,122.1267440828592,27649.82382290588,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,122.1267440828592,122.1267440828592,55233.3406897914,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,122.1267440828592,122.1267440828592,82917.66802319854,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,122.1267440828592,122.1267440828592,110003.03047664744,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,122.1267440828592,122.1267440828592,55299.64764581176,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,122.1267440828592,122.1267440828592,110466.6813795828,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,122.1267440828592,122.1267440828592,165835.33604639707,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,122.1267440828592,122.1267440828592,220006.0609532949,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,122.1267440828592,122.1267440828592,82949.47146871765,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,122.1267440828592,122.1267440828592,165700.02206937416,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,122.1267440828592,122.1267440828592,248753.0040695956,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,122.1267440828592,122.1267440828592,330009.0914299423,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,122.1267440828592,122.1267440828592,110599.29529162352,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,122.1267440828592,122.1267440828592,220933.3627591656,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,122.1267440828592,122.1267440828592,331670.6720927941,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,122.1267440828592,122.1267440828592,440012.1219065897,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,122.1267440828592,122.1267440828592,165898.9429374353,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,122.1267440828592,122.1267440828592,331400.0441387483,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,122.1267440828592,122.1267440828592,497506.0081391912,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,122.1267440828592,122.1267440828592,660018.1828598846,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.2916393000050448,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,99.79309069495268,99.79309069495268,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,99.79309069495268,99.79309069495268,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,99.79309069495268,99.79309069495268,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,99.79309069495268,99.79309069495268,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,99.79309069495268,99.79309069495268,22819.71467027487,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,99.79309069495268,99.79309069495268,45578.42222713762,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,99.79309069495268,99.79309069495268,68095.71542368489,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,99.79309069495268,99.79309069495268,90892.78826398996,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,99.79309069495268,99.79309069495268,45639.42934054974,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,99.79309069495268,99.79309069495268,91156.84445427524,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,99.79309069495268,99.79309069495268,136191.43084736975,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,99.79309069495268,99.79309069495268,181785.57652797992,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,99.79309069495268,99.79309069495268,68459.1440108246,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,99.79309069495268,99.79309069495268,136735.26668141288,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,99.79309069495268,99.79309069495268,204287.14627105463,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,99.79309069495268,99.79309069495268,272678.3647919699,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,99.79309069495268,99.79309069495268,91278.85868109947,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,99.79309069495268,99.79309069495268,182313.68890855048,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,99.79309069495268,99.79309069495268,272382.86169473955,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,99.79309069495268,99.79309069495268,363571.1530559599,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,99.79309069495268,99.79309069495268,136918.2880216492,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,99.79309069495268,99.79309069495268,273470.5333628257,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,99.79309069495268,99.79309069495268,408574.2925421093,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,99.79309069495268,99.79309069495268,545356.7295839398,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.312926199985668,True
```

### Q4/BASE - Q4_sizing_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\BASE\tables\Q4_sizing_summary.csv`

```csv
country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,revenue_bess_price_taker,soc_min,soc_max,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,initial_deliverable_mwh,engine_version,compute_time_sec,cache_hit,notes_quality
DE,2040,SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,133.15273800112763,133.15273800112763,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3421105000306852,True,ok
ES,2040,SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,98.40603141928084,98.40603141928084,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3471649999846704,True,ok
```

### Q4 - scénario `FLEX_UP`

### Q4/FLEX_UP - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\FLEX_UP\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
FAIL,Q4_SURPLUS_INCREASE,Surplus non absorbe augmente en mode SURPLUS_FIRST.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
```

### Q4/FLEX_UP - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\FLEX_UP\warnings_filtered.csv`

```csv
question_id,status,code,message,scope,scenario_id,mentioned_countries,is_global
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
```

### Q4/FLEX_UP - Q4_bess_frontier.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\FLEX_UP\tables\Q4_bess_frontier.csv`

```csv
dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,revenue_bess_price_taker,soc_min,soc_max,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,initial_deliverable_mwh,engine_version,compute_time_sec,cache_hit
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,20803.654026139346,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,41619.89321624119,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,61562.87928586864,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,82377.33974131457,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,41607.30805227869,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,83239.78643248237,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,123125.75857173729,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,164754.67948262914,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,62410.96207841802,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,124859.67964872356,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,184688.63785760588,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,247132.01922394373,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,83214.61610455737,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,166479.57286496475,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,246251.5171434745,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,329509.3589652583,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,124821.92415683604,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,249719.35929744717,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,369377.27571521176,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,1.0,0.916528210803929,0.0,0.0024508908027816,94.77843633699256,94.77843633699256,494264.03844788746,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.2754930999944918,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,30557.55881498197,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,60967.5799700326,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,91011.22650933784,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,120446.95361741248,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,61115.11762996394,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,121935.1599400652,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,182022.45301867567,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,240893.90723482493,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,91672.67644494592,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,182902.7399100978,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,273033.6795280135,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,361340.8608522373,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,122230.23525992788,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,243870.3198801304,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,364044.90603735135,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,481787.81446964986,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,183345.35288989183,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,365805.4798201956,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,546067.359056027,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,1.0,1.0,0.0,0.0,143.3037824237792,143.3037824237792,722681.7217044747,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3156029999954626,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,133.13539945763245,133.13539945763245,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,133.13539945763245,133.13539945763245,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,133.13539945763245,133.13539945763245,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,133.13539945763245,133.13539945763245,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,133.13539945763245,133.13539945763245,29413.769259352983,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,133.13539945763245,133.13539945763245,58763.91696801622,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,133.13539945763245,133.13539945763245,87887.67454463574,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,133.13539945763245,133.13539945763245,117257.07975212968,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,133.13539945763245,133.13539945763245,58827.53851870597,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,133.13539945763245,133.13539945763245,117527.83393603245,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,133.13539945763245,133.13539945763245,175775.34908927148,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,133.13539945763245,133.13539945763245,234514.15950425935,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,133.13539945763245,133.13539945763245,88241.30777805897,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,133.13539945763245,133.13539945763245,176291.75090404868,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,133.13539945763245,133.13539945763245,263663.0236339072,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,133.13539945763245,133.13539945763245,351771.23925638903,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,133.13539945763245,133.13539945763245,117655.07703741196,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,133.13539945763245,133.13539945763245,235055.6678720649,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,133.13539945763245,133.13539945763245,351550.6981785429,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,133.13539945763245,133.13539945763245,469028.3190085188,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,133.13539945763245,133.13539945763245,176482.61555611793,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,133.13539945763245,133.13539945763245,352583.5018080973,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,133.13539945763245,133.13539945763245,527326.0472678144,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,133.13539945763245,133.13539945763245,703542.4785127781,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3046438000164926,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,98.37607547031716,98.37607547031716,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,98.37607547031716,98.37607547031716,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,98.37607547031716,98.37607547031716,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,98.37607547031716,98.37607547031716,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,98.37607547031716,98.37607547031716,23506.42937883265,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,98.37607547031716,98.37607547031716,46572.10495977416,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,98.37607547031716,98.37607547031716,69504.8273619282,0.0,483.49910455548695,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,98.37607547031716,98.37607547031716,91861.15148144716,0.0,733.499104555487,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,98.37607547031716,98.37607547031716,47012.8587576653,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,98.37607547031716,98.37607547031716,93144.20991954832,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,98.37607547031716,98.37607547031716,139009.6547238564,0.0,966.998209110974,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,98.37607547031716,98.37607547031716,183722.30296289435,0.0,1466.998209110974,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,98.37607547031716,98.37607547031716,70519.28813649795,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,98.37607547031716,98.37607547031716,139716.31487932248,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,98.37607547031716,98.37607547031716,208514.48208578452,0.0,1450.4973136664607,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,98.37607547031716,98.37607547031716,275583.4544443415,0.0,2200.4973136664607,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,98.37607547031716,98.37607547031716,94025.7175153306,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,98.37607547031716,98.37607547031716,186288.41983909663,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,98.37607547031716,98.37607547031716,278019.3094477128,0.0,1933.996418221948,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,98.37607547031716,98.37607547031716,367444.6059257887,0.0,2933.996418221948,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,98.37607547031716,98.37607547031716,141038.5762729959,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,98.37607547031716,98.37607547031716,279432.62975864497,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,98.37607547031716,98.37607547031716,417028.9641715691,0.0,2900.994627332921,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,98.37607547031716,98.37607547031716,551166.908888683,0.0,4400.9946273329215,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3302688000258058,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,141.39276677627964,141.39276677627964,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,141.39276677627964,141.39276677627964,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,141.39276677627964,141.39276677627964,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,141.39276677627964,141.39276677627964,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,141.39276677627964,141.39276677627964,33539.13830585784,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,141.39276677627964,141.39276677627964,66493.04579197383,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,141.39276677627964,141.39276677627964,100049.07428852268,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,141.39276677627964,141.39276677627964,132660.39973468456,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,141.39276677627964,141.39276677627964,67078.27661171567,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,141.39276677627964,141.39276677627964,132986.09158394765,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,141.39276677627964,141.39276677627964,200098.14857704536,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,141.39276677627964,141.39276677627964,265320.7994693691,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,141.39276677627964,141.39276677627964,100617.41491757352,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,141.39276677627964,141.39276677627964,199479.13737592148,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,141.39276677627964,141.39276677627964,300147.222865568,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,141.39276677627964,141.39276677627964,397981.1992040537,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,141.39276677627964,141.39276677627964,134156.55322343134,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,141.39276677627964,141.39276677627964,265972.1831678953,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,141.39276677627964,141.39276677627964,400196.2971540907,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,141.39276677627964,141.39276677627964,530641.5989387382,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,141.39276677627964,141.39276677627964,201234.829835147,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,141.39276677627964,141.39276677627964,398958.27475184295,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,141.39276677627964,141.39276677627964,600294.445731136,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,141.39276677627964,141.39276677627964,795962.3984081073,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.5992816000361927,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,122.1248991661791,122.1248991661791,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,122.1248991661791,122.1248991661791,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,122.1248991661791,122.1248991661791,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,122.1248991661791,122.1248991661791,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,122.1248991661791,122.1248991661791,27649.82382290588,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,122.1248991661791,122.1248991661791,55233.3406897914,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,122.1248991661791,122.1248991661791,82917.66802319854,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,122.1248991661791,122.1248991661791,110003.03047664744,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,122.1248991661791,122.1248991661791,55299.64764581176,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,122.1248991661791,122.1248991661791,110466.6813795828,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,122.1248991661791,122.1248991661791,165835.33604639707,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,122.1248991661791,122.1248991661791,220006.0609532949,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,122.1248991661791,122.1248991661791,82949.47146871765,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,122.1248991661791,122.1248991661791,165700.02206937416,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,122.1248991661791,122.1248991661791,248753.0040695956,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,122.1248991661791,122.1248991661791,330009.0914299423,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,122.1248991661791,122.1248991661791,110599.29529162352,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,122.1248991661791,122.1248991661791,220933.3627591656,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,122.1248991661791,122.1248991661791,331670.6720927941,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,122.1248991661791,122.1248991661791,440012.1219065897,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,122.1248991661791,122.1248991661791,165898.9429374353,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,122.1248991661791,122.1248991661791,331400.0441387483,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,122.1248991661791,122.1248991661791,497506.0081391912,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,122.1248991661791,122.1248991661791,660018.1828598846,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3167781999800354,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,99.79309069495268,99.79309069495268,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,99.79309069495268,99.79309069495268,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,99.79309069495268,99.79309069495268,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,99.79309069495268,99.79309069495268,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,99.79309069495268,99.79309069495268,22819.71467027487,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,99.79309069495268,99.79309069495268,45578.42222713762,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,99.79309069495268,99.79309069495268,68095.71542368489,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,99.79309069495268,99.79309069495268,90892.78826398996,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,99.79309069495268,99.79309069495268,45639.42934054974,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,99.79309069495268,99.79309069495268,91156.84445427524,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,99.79309069495268,99.79309069495268,136191.43084736975,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,99.79309069495268,99.79309069495268,181785.57652797992,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,99.79309069495268,99.79309069495268,68459.1440108246,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,99.79309069495268,99.79309069495268,136735.26668141288,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,99.79309069495268,99.79309069495268,204287.14627105463,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,99.79309069495268,99.79309069495268,272678.3647919699,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,99.79309069495268,99.79309069495268,91278.85868109947,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,99.79309069495268,99.79309069495268,182313.68890855048,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,99.79309069495268,99.79309069495268,272382.86169473955,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,99.79309069495268,99.79309069495268,363571.1530559599,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,99.79309069495268,99.79309069495268,136918.2880216492,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,99.79309069495268,99.79309069495268,273470.5333628257,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,99.79309069495268,99.79309069495268,408574.2925421093,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.312926199985668,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,99.79309069495268,99.79309069495268,545356.7295839398,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.312926199985668,True
```

### Q4/FLEX_UP - Q4_sizing_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\FLEX_UP\tables\Q4_sizing_summary.csv`

```csv
country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,revenue_bess_price_taker,soc_min,soc_max,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,initial_deliverable_mwh,engine_version,compute_time_sec,cache_hit,notes_quality
DE,2040,SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,133.13539945763245,133.13539945763245,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3046438000164926,True,ok
ES,2040,SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,98.37607547031716,98.37607547031716,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3302688000258058,True,ok
```

### Q4 - scénario `HIGH_CO2`

### Q4/HIGH_CO2 - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_CO2\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
FAIL,Q4_SURPLUS_INCREASE,Surplus non absorbe augmente en mode SURPLUS_FIRST.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
```

### Q4/HIGH_CO2 - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_CO2\warnings_filtered.csv`

```csv
question_id,status,code,message,scope,scenario_id,mentioned_countries,is_global
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
```

### Q4/HIGH_CO2 - Q4_bess_frontier.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_CO2\tables\Q4_bess_frontier.csv`

```csv
dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,revenue_bess_price_taker,soc_min,soc_max,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,initial_deliverable_mwh,engine_version,compute_time_sec,cache_hit
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,0.947655098457812,0.7934613351283482,0.0015369460628298,0.0060643688008615,99.93631604715236,99.93631604715236,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,0.947655098457812,0.7934613351283482,0.0015369460628298,0.0060643688008615,99.93631604715236,99.93631604715236,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,0.947655098457812,0.7934613351283482,0.0015369460628298,0.0060643688008615,99.93631604715236,99.93631604715236,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,0.947655098457812,0.7934613351283482,0.0015369460628298,0.0060643688008615,99.93631604715236,99.93631604715236,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,0.947655098457812,0.81561865003255,0.0015369460628298,0.0054137878101331,99.93631604715236,99.93631604715236,100455.882332448,0.0,469.041575982343,250.0,250.0,650.5809907283236,807.0320598320964,234.5207879911715,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,0.947655098457812,0.8241330837540903,0.0015369460628298,0.0051637878101331,99.93631604715236,99.93631604715236,151259.99698869206,0.0,703.5623639735145,250.0,250.0,900.5809907283236,1261.5528478232677,469.041575982343,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,0.947655098457812,0.8241330837540903,0.0015369460628298,0.0051637878101331,99.93631604715236,99.93631604715236,172281.16780831042,0.0,750.0,250.0,250.0,900.5809907283236,1496.0736358144395,703.5623639735145,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,0.947655098457812,0.8241330837540903,0.0015369460628298,0.0051637878101331,99.93631604715236,99.93631604715236,194276.1979179253,0.0,1000.0,250.0,250.0,900.5809907283236,1730.5944238056109,938.083151964686,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,0.947655098457812,0.8326475174756308,0.0015369460628298,0.0049137878101331,99.93631604715236,99.93631604715236,184474.39076189816,0.0,938.083151964686,500.0,500.0,1150.5809907283235,1481.552847823268,469.041575982343,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,0.947655098457812,0.8394163369488622,0.0015369460628298,0.0047150423710763,99.93631604715236,99.93631604715236,251213.31161632368,0.0,1124.522899873724,500.0,500.0,1349.3264297851554,2125.490410175623,938.083151964686,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,0.947655098457812,0.8394163369488622,0.0015369460628298,0.0047150423710763,99.93631604715236,99.93631604715236,293249.6789883635,0.0,1500.0,500.0,500.0,1349.3264297851554,2594.531986157965,1407.124727947029,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,0.947655098457812,0.8394163369488622,0.0015369460628298,0.0047150423710763,99.93631604715236,99.93631604715236,337243.4995327798,0.0,2000.0,500.0,500.0,1349.3264297851554,3063.573562140308,1876.166303929372,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,99.93631604715236,99.93631604715236,254147.89660908835,0.0,1300.52571661072,687.6196330446637,750.0,1536.9460628298189,2056.0748992637555,703.5623639735145,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,99.93631604715236,99.93631604715236,319689.3904433319,0.0,1500.0,687.6196330446637,750.0,1536.9460628298189,2759.63726323727,1407.124727947029,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,99.93631604715236,99.93631604715236,382793.55824277655,0.0,2250.0,687.6196330446637,750.0,1536.9460628298189,3463.1996272107835,2110.6870919205435,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,99.93631604715236,99.93631604715236,448786.16922199423,0.0,3000.0,687.6196330446637,750.0,1536.9460628298189,4166.7619911842985,2814.249455894058,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,99.93631604715236,99.93631604715236,276038.7622705352,0.0,1300.52571661072,687.6196330446637,1000.0,1536.9460628298189,2290.595687254927,938.083151964686,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,99.93631604715236,99.93631604715236,363636.904687652,0.0,2000.0,687.6196330446637,1000.0,1536.9460628298189,3228.6788392196127,1876.166303929372,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,99.93631604715236,99.93631604715236,447852.247887272,0.0,3000.0,687.6196330446637,1000.0,1536.9460628298189,4166.7619911842985,2814.249455894058,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,99.93631604715236,99.93631604715236,535843.649301291,0.0,4000.0,687.6196330446637,1000.0,1536.9460628298189,5104.845143148985,3752.332607858744,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,99.93631604715236,99.93631604715236,319929.2656479461,0.0,1500.0,687.6196330446637,1407.124727947029,1536.9460628298189,2759.63726323727,1407.124727947029,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,99.93631604715236,99.93631604715236,451577.8965711975,0.0,3000.0,687.6196330446637,1500.0,1536.9460628298189,4166.7619911842985,2814.249455894058,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,99.93631604715236,99.93631604715236,578033.668016261,0.0,4500.0,687.6196330446637,1500.0,1536.9460628298189,5573.886719131328,4221.374183841087,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,99.93631604715236,99.93631604715236,710022.6502998826,0.0,6000.0,687.6196330446637,1500.0,1536.9460628298189,6981.011447078356,5628.498911788116,v2.1.0,0.3604755999986082,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,33451.26761680724,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,66754.99757368315,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,99692.35291481367,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,132021.78882471356,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,66902.53523361449,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,133509.9951473663,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,199384.70582962732,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,264043.5776494271,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,100353.80285042174,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,200264.99272104944,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,299077.058744441,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,396065.3664741407,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,133805.07046722897,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,267019.9902947326,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,398769.4116592547,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,528087.1552988542,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,200707.60570084347,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,400529.9854420989,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,598154.117488882,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,1.0,1.0,0.0,0.0,156.02260503206747,156.02260503206747,792130.7329482813,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3690468000131659,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,145.73395548404667,145.73395548404667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,145.73395548404667,145.73395548404667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,145.73395548404667,145.73395548404667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,145.73395548404667,145.73395548404667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,145.73395548404667,145.73395548404667,32307.478061178263,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,145.73395548404667,145.73395548404667,64551.334571666775,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,145.73395548404667,145.73395548404667,96568.80095011156,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,145.73395548404667,145.73395548404667,128831.91495943078,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,145.73395548404667,145.73395548404667,64614.95612235653,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,145.73395548404667,145.73395548404667,129102.66914333357,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,145.73395548404667,145.73395548404667,193137.60190022312,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,145.73395548404667,145.73395548404667,257663.8299188616,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,145.73395548404667,145.73395548404667,96922.4341835348,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,145.73395548404667,145.73395548404667,193654.00371500035,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,145.73395548404667,145.73395548404667,289706.4028503347,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,145.73395548404667,145.73395548404667,386495.7448782924,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,145.73395548404667,145.73395548404667,129229.91224471306,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,145.73395548404667,145.73395548404667,258205.3382866671,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,145.73395548404667,145.73395548404667,386275.20380044624,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,145.73395548404667,145.73395548404667,515327.6598377231,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,145.73395548404667,145.73395548404667,193844.8683670696,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,145.73395548404667,145.73395548404667,387308.0074300007,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,145.73395548404667,145.73395548404667,579412.8057006694,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,145.73395548404667,145.73395548404667,772991.4897565847,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.318632600014098,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,103.49761706397923,103.49761706397923,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,103.49761706397923,103.49761706397923,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,103.49761706397923,103.49761706397923,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,103.49761706397923,103.49761706397923,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,103.49761706397923,103.49761706397923,24690.759358188065,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,103.49761706397923,103.49761706397923,48940.76491848499,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,103.49761706397923,103.49761706397923,73057.81729999444,0.0,483.49910455548695,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,103.49761706397923,103.49761706397923,96598.47139886882,0.0,733.499104555487,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,103.49761706397923,103.49761706397923,49381.51871637613,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,103.49761706397923,103.49761706397923,97881.52983696996,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,103.49761706397923,103.49761706397923,146115.63459998887,0.0,966.998209110974,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,103.49761706397923,103.49761706397923,193196.94279773763,0.0,1466.998209110974,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,103.49761706397923,103.49761706397923,74072.2780745642,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,103.49761706397923,103.49761706397923,146822.29475545496,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,103.49761706397923,103.49761706397923,219173.45189998328,0.0,1450.4973136664607,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,103.49761706397923,103.49761706397923,289795.41419660643,0.0,2200.4973136664607,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,103.49761706397923,103.49761706397923,98763.03743275226,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,103.49761706397923,103.49761706397923,195763.05967393995,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,103.49761706397923,103.49761706397923,292231.26919997775,0.0,1933.996418221948,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,103.49761706397923,103.49761706397923,386393.88559547527,0.0,2933.996418221948,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,103.49761706397923,103.49761706397923,148144.5561491284,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,103.49761706397923,103.49761706397923,293644.5895109099,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,103.49761706397923,103.49761706397923,438346.90379996656,0.0,2900.994627332921,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,103.49761706397923,103.49761706397923,579590.8283932129,0.0,4400.9946273329215,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3180531999678351,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,146.5825566444785,146.5825566444785,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,146.5825566444785,146.5825566444785,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,146.5825566444785,146.5825566444785,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,146.5825566444785,146.5825566444785,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,146.5825566444785,146.5825566444785,34723.468285213254,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,146.5825566444785,146.5825566444785,68861.70575068465,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,146.5825566444785,146.5825566444785,103602.0642265889,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,146.5825566444785,146.5825566444785,137412.50526078045,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,146.5825566444785,146.5825566444785,69446.93657042651,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,146.5825566444785,146.5825566444785,137723.4115013693,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,146.5825566444785,146.5825566444785,207204.1284531778,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,146.5825566444785,146.5825566444785,274825.0105215609,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,146.5825566444785,146.5825566444785,104170.40485563976,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,146.5825566444785,146.5825566444785,206585.11725205395,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,146.5825566444785,146.5825566444785,310806.1926797667,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,146.5825566444785,146.5825566444785,412237.5157823413,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,146.5825566444785,146.5825566444785,138893.873140853,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,146.5825566444785,146.5825566444785,275446.8230027386,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,146.5825566444785,146.5825566444785,414408.2569063556,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,146.5825566444785,146.5825566444785,549650.0210431218,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,146.5825566444785,146.5825566444785,208340.80971127952,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,146.5825566444785,146.5825566444785,413170.2345041079,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,146.5825566444785,146.5825566444785,621612.3853595334,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,146.5825566444785,146.5825566444785,824475.0315646826,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.6308683999814093,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,127.33548519545622,127.33548519545622,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,127.33548519545622,127.33548519545622,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,127.33548519545622,127.33548519545622,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,127.33548519545622,127.33548519545622,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,127.33548519545622,127.33548519545622,28834.15380226129,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,127.33548519545622,127.33548519545622,57602.000648502224,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,127.33548519545622,127.33548519545622,86470.65796126478,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,127.33548519545622,127.33548519545622,114740.3503940691,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,127.33548519545622,127.33548519545622,57668.30760452259,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,127.33548519545622,127.33548519545622,115204.00129700443,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,127.33548519545622,127.33548519545622,172941.31592252955,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,127.33548519545622,127.33548519545622,229480.7007881382,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,127.33548519545622,127.33548519545622,86502.46140678388,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,127.33548519545622,127.33548519545622,172806.00194550666,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,127.33548519545622,127.33548519545622,259411.97388379436,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,127.33548519545622,127.33548519545622,344221.05118220724,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,127.33548519545622,127.33548519545622,115336.61520904518,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,127.33548519545622,127.33548519545622,230408.0025940089,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,127.33548519545622,127.33548519545622,345882.6318450591,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,127.33548519545622,127.33548519545622,458961.4015762764,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,127.33548519545622,127.33548519545622,173004.92281356777,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,127.33548519545622,127.33548519545622,345612.00389101333,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,127.33548519545622,127.33548519545622,518823.9477675887,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,127.33548519545622,127.33548519545622,688442.1023644145,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3297201000386849,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,104.91467753795732,104.91467753795732,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,104.91467753795732,104.91467753795732,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,104.91467753795732,104.91467753795732,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,104.91467753795732,104.91467753795732,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,104.91467753795732,104.91467753795732,24004.044649630287,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,104.91467753795732,104.91467753795732,47947.082185848456,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,104.91467753795732,104.91467753795732,71648.70536175114,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,104.91467753795732,104.91467753795732,95630.10818141163,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,104.91467753795732,104.91467753795732,48008.08929926057,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,104.91467753795732,104.91467753795732,95894.16437169693,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,104.91467753795732,104.91467753795732,143297.41072350228,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,104.91467753795732,104.91467753795732,191260.2163628233,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,104.91467753795732,104.91467753795732,72012.13394889087,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,104.91467753795732,104.91467753795732,143841.24655754538,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,104.91467753795732,104.91467753795732,214946.11608525345,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,104.91467753795732,104.91467753795732,286890.32454423496,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,104.91467753795732,104.91467753795732,96016.17859852116,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,104.91467753795732,104.91467753795732,191788.32874339385,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,104.91467753795732,104.91467753795732,286594.82144700456,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,104.91467753795732,104.91467753795732,382520.4327256466,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,104.91467753795732,104.91467753795732,144024.26789778174,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,104.91467753795732,104.91467753795732,287682.4931150908,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,104.91467753795732,104.91467753795732,429892.2321705069,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.332448499975726,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,104.91467753795732,104.91467753795732,573780.6490884699,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.332448499975726,True
```

### Q4/HIGH_CO2 - Q4_sizing_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_CO2\tables\Q4_sizing_summary.csv`

```csv
country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,revenue_bess_price_taker,soc_min,soc_max,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,initial_deliverable_mwh,engine_version,compute_time_sec,cache_hit,notes_quality
DE,2040,SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,145.73395548404667,145.73395548404667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.318632600014098,True,ok
ES,2040,SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,103.49761706397923,103.49761706397923,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3180531999678351,True,ok
```

### Q4 - scénario `HIGH_GAS`

### Q4/HIGH_GAS - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_GAS\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
FAIL,Q4_SURPLUS_INCREASE,Surplus non absorbe augmente en mode SURPLUS_FIRST.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
INFO,Q4_CACHE_HIT,Resultat charge depuis cache persistant Q4.,Q4,,True
```

### Q4/HIGH_GAS - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_GAS\warnings_filtered.csv`

```csv
question_id,status,code,message,scope,scenario_id,mentioned_countries,is_global
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
Q4,WARN,QUESTION_WARNING,Objectif non atteint sur la grille de sizing; meilleur compromis retourne.,GLOBAL,,,True
```

### Q4/HIGH_GAS - Q4_bess_frontier.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_GAS\tables\Q4_bess_frontier.csv`

```csv
dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,revenue_bess_price_taker,soc_min,soc_max,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,initial_deliverable_mwh,engine_version,compute_time_sec,cache_hit
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,0.947655098457812,0.7934613351283482,0.0015369460628298,0.0060643688008615,105.92057072437647,105.92057072437647,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,0.947655098457812,0.7934613351283482,0.0015369460628298,0.0060643688008615,105.92057072437647,105.92057072437647,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,0.947655098457812,0.7934613351283482,0.0015369460628298,0.0060643688008615,105.92057072437647,105.92057072437647,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,0.947655098457812,0.7934613351283482,0.0015369460628298,0.0060643688008615,105.92057072437647,105.92057072437647,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,0.947655098457812,0.81561865003255,0.0015369460628298,0.0054137878101331,105.92057072437647,105.92057072437647,105184.35653755516,0.0,469.041575982343,250.0,250.0,650.5809907283236,807.0320598320964,234.5207879911715,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,0.947655098457812,0.8241330837540903,0.0015369460628298,0.0051637878101331,105.92057072437647,105.92057072437647,158651.54981071115,0.0,703.5623639735145,250.0,250.0,900.5809907283236,1261.5528478232677,469.041575982343,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,0.947655098457812,0.8241330837540903,0.0015369460628298,0.0051637878101331,105.92057072437647,105.92057072437647,181046.79924724135,0.0,750.0,250.0,250.0,900.5809907283236,1496.0736358144395,703.5623639735145,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,0.947655098457812,0.8241330837540903,0.0015369460628298,0.0051637878101331,105.92057072437647,105.92057072437647,204415.90797376825,0.0,1000.0,250.0,250.0,900.5809907283236,1730.5944238056109,938.083151964686,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,0.947655098457812,0.8326475174756308,0.0015369460628298,0.0049137878101331,105.92057072437647,105.92057072437647,193154.9435839172,0.0,938.083151964686,500.0,500.0,1150.5809907283235,1481.552847823268,469.041575982343,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,0.947655098457812,0.8394163369488622,0.0015369460628298,0.0047150423710763,105.92057072437647,105.92057072437647,263666.7531559436,0.0,1124.522899873724,500.0,500.0,1349.3264297851554,2125.490410175623,938.083151964686,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,0.947655098457812,0.8394163369488622,0.0015369460628298,0.0047150423710763,105.92057072437647,105.92057072437647,308451.2777618072,0.0,1500.0,500.0,500.0,1349.3264297851554,2594.531986157965,1407.124727947029,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,0.947655098457812,0.8394163369488622,0.0015369460628298,0.0047150423710763,105.92057072437647,105.92057072437647,355193.2555400473,0.0,2000.0,500.0,500.0,1349.3264297851554,3063.573562140308,1876.166303929372,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,105.92057072437647,105.92057072437647,266194.6263597746,0.0,1300.52571661072,687.6196330446637,750.0,1536.9460628298189,2056.0748992637555,703.5623639735145,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,105.92057072437647,105.92057072437647,335858.3560447539,0.0,1500.0,687.6196330446637,750.0,1536.9460628298189,2759.63726323727,1407.124727947029,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,105.92057072437647,105.92057072437647,403084.7596949344,0.0,2250.0,687.6196330446637,750.0,1536.9460628298189,3463.1996272107835,2110.6870919205435,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,105.92057072437647,105.92057072437647,473199.6065248877,0.0,3000.0,687.6196330446637,750.0,1536.9460628298189,4166.7619911842985,2814.249455894058,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,105.92057072437647,105.92057072437647,289459.57063813333,0.0,1300.52571661072,687.6196330446637,1000.0,1536.9460628298189,2290.595687254927,938.083151964686,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,105.92057072437647,105.92057072437647,382554.02752289776,0.0,2000.0,687.6196330446637,1000.0,1536.9460628298189,3228.6788392196127,1876.166303929372,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,105.92057072437647,105.92057072437647,472265.6851901654,0.0,3000.0,687.6196330446637,1000.0,1536.9460628298189,4166.7619911842985,2814.249455894058,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,105.92057072437647,105.92057072437647,565753.401071832,0.0,4000.0,687.6196330446637,1000.0,1536.9460628298189,5104.845143148985,3752.332607858744,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,105.92057072437647,105.92057072437647,336098.23124936805,0.0,1500.0,687.6196330446637,1407.124727947029,1536.9460628298189,2759.63726323727,1407.124727947029,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,105.92057072437647,105.92057072437647,475991.3338740909,0.0,3000.0,687.6196330446637,1500.0,1536.9460628298189,4166.7619911842985,2814.249455894058,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,105.92057072437647,105.92057072437647,610691.5770206258,0.0,4500.0,687.6196330446637,1500.0,1536.9460628298189,5573.886719131328,4221.374183841087,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,0.947655098457812,0.8458062366705363,0.0015369460628298,0.0045274227380316,105.92057072437647,105.92057072437647,750925.031005719,0.0,6000.0,687.6196330446637,1500.0,1536.9460628298189,6981.011447078356,5628.498911788116,v2.1.0,0.4025658000027761,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,34260.51862536888,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,68373.49959080642,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,102120.10594049856,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,135258.7928589601,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,68521.03725073776,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,136746.99918161283,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,204240.21188099717,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,270517.5857179202,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,102781.55587610663,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,205120.4987724193,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,306360.3178214957,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,405776.3785768803,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,137042.07450147552,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,273493.99836322566,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,408480.4237619943,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,541035.1714358404,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,205563.1117522133,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,410240.9975448385,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,612720.6356429914,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,1.0,1.0,0.0,0.0,159.57920483916783,159.57920483916783,811552.7571537606,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.2874174000462517,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,149.25240313522823,149.25240313522823,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,149.25240313522823,149.25240313522823,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,149.25240313522823,149.25240313522823,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,149.25240313522823,149.25240313522823,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,149.25240313522823,149.25240313522823,33116.7290697399,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,149.25240313522823,149.25240313522823,66169.83658879006,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,149.25240313522823,149.25240313522823,98996.55397579649,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,149.25240313522823,149.25240313522823,132068.91899367736,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,149.25240313522823,149.25240313522823,66233.4581394798,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,149.25240313522823,149.25240313522823,132339.67317758012,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,149.25240313522823,149.25240313522823,197993.10795159292,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,149.25240313522823,149.25240313522823,264137.8379873547,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,149.25240313522823,149.25240313522823,99350.1872092197,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,149.25240313522823,149.25240313522823,198509.50976637017,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,149.25240313522823,149.25240313522823,296989.66192738945,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,149.25240313522823,149.25240313522823,396206.756981032,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,149.25240313522823,149.25240313522823,132466.9162789596,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,149.25240313522823,149.25240313522823,264679.34635516023,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,149.25240313522823,149.25240313522823,395986.2159031859,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,149.25240313522823,149.25240313522823,528275.6759747094,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,149.25240313522823,149.25240313522823,198700.3744184394,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,149.25240313522823,149.25240313522823,397019.0195327404,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,149.25240313522823,149.25240313522823,593979.3238547789,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,149.25240313522823,149.25240313522823,792413.5139620639,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3443929000059142,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,109.40495630431788,109.40495630431788,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,109.40495630431788,109.40495630431788,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,109.40495630431788,109.40495630431788,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,109.40495630431788,109.40495630431788,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,109.40495630431788,109.40495630431788,26064.83797509997,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,109.40495630431788,109.40495630431788,51688.922152308805,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,109.40495630431788,109.40495630431788,77180.05315073016,0.0,483.49910455548695,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,109.40495630431788,109.40495630431788,102094.78586651648,0.0,733.499104555487,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,109.40495630431788,109.40495630431788,52129.67595019995,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,109.40495630431788,109.40495630431788,103377.8443046176,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,109.40495630431788,109.40495630431788,154360.10630146033,0.0,966.998209110974,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,109.40495630431788,109.40495630431788,204189.5717330329,0.0,1466.998209110974,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,109.40495630431788,109.40495630431788,78194.51392529992,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,109.40495630431788,109.40495630431788,155066.76645692642,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,109.40495630431788,109.40495630431788,231540.15945219045,0.0,1450.4973136664607,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,109.40495630431788,109.40495630431788,306284.3575995494,0.0,2200.4973136664607,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,109.40495630431788,109.40495630431788,104259.3519003999,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,109.40495630431788,109.40495630431788,206755.6886092352,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,109.40495630431788,109.40495630431788,308720.21260292066,0.0,1933.996418221948,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,109.40495630431788,109.40495630431788,408379.1434660658,0.0,2933.996418221948,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,109.40495630431788,109.40495630431788,156389.02785059984,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,109.40495630431788,109.40495630431788,310133.53291385283,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,109.40495630431788,109.40495630431788,463080.3189043809,0.0,2900.994627332921,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,109.40495630431788,109.40495630431788,612568.7151990988,0.0,4400.9946273329215,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3382575999712571,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,152.5749842611698,152.5749842611698,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,152.5749842611698,152.5749842611698,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,152.5749842611698,152.5749842611698,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,152.5749842611698,152.5749842611698,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,152.5749842611698,152.5749842611698,36097.54690212516,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,152.5749842611698,152.5749842611698,71609.86298450848,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,152.5749842611698,152.5749842611698,107724.30007732465,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,152.5749842611698,152.5749842611698,142908.8197284281,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,152.5749842611698,152.5749842611698,72195.09380425033,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,152.5749842611698,152.5749842611698,143219.72596901696,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,152.5749842611698,152.5749842611698,215448.6001546493,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,152.5749842611698,152.5749842611698,285817.6394568562,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,152.5749842611698,152.5749842611698,108292.6407063755,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,152.5749842611698,152.5749842611698,214829.5889535254,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,152.5749842611698,152.5749842611698,323172.900231974,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,152.5749842611698,152.5749842611698,428726.4591852843,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,152.5749842611698,152.5749842611698,144390.18760850065,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,152.5749842611698,152.5749842611698,286439.4519380339,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,152.5749842611698,152.5749842611698,430897.2003092986,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,152.5749842611698,152.5749842611698,571635.2789137124,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,152.5749842611698,152.5749842611698,216585.281412751,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,152.5749842611698,152.5749842611698,429659.1779070508,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,152.5749842611698,152.5749842611698,646345.8004639479,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,152.5749842611698,152.5749842611698,857452.9183705685,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.6704207000439055,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,133.3787500866691,133.3787500866691,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,133.3787500866691,133.3787500866691,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,133.3787500866691,133.3787500866691,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,133.3787500866691,133.3787500866691,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,133.3787500866691,133.3787500866691,30208.2324191732,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,133.3787500866691,133.3787500866691,60350.15788232604,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,133.3787500866691,133.3787500866691,90592.8938120005,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,133.3787500866691,133.3787500866691,120236.66486171674,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,133.3787500866691,133.3787500866691,60416.4648383464,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,133.3787500866691,133.3787500866691,120700.31576465208,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,133.3787500866691,133.3787500866691,181185.787624001,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,133.3787500866691,133.3787500866691,240473.32972343348,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,133.3787500866691,133.3787500866691,90624.6972575196,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,133.3787500866691,133.3787500866691,181050.4736469781,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,133.3787500866691,133.3787500866691,271778.68143600144,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,133.3787500866691,133.3787500866691,360709.99458515015,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,133.3787500866691,133.3787500866691,120832.9296766928,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,133.3787500866691,133.3787500866691,241400.6315293041,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,133.3787500866691,133.3787500866691,362371.575248002,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,133.3787500866691,133.3787500866691,480946.65944686695,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,133.3787500866691,133.3787500866691,181249.3945150392,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,133.3787500866691,133.3787500866691,362100.9472939562,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,133.3787500866691,133.3787500866691,543557.3628720029,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,133.3787500866691,133.3787500866691,721419.9891703003,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.3247897000401281,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,110.85682464923818,110.85682464923818,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,4.0,,,0.0,0.0,110.85682464923818,110.85682464923818,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,6.0,,,0.0,0.0,110.85682464923818,110.85682464923818,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,0.0,0.0,8.0,,,0.0,0.0,110.85682464923818,110.85682464923818,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,250.0,500.0,2.0,,,0.0,0.0,110.85682464923818,110.85682464923818,25378.1232665422,0.0,250.0,0.0,234.5207879911715,0.0,234.5207879911715,234.5207879911715,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,250.0,1000.0,4.0,,,0.0,0.0,110.85682464923818,110.85682464923818,50695.239419672274,0.0,500.0,0.0,250.0,0.0,469.0415759823429,469.041575982343,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,250.0,1500.0,6.0,,,0.0,0.0,110.85682464923818,110.85682464923818,75770.94121248687,0.0,750.0,0.0,250.0,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,250.0,2000.0,8.0,,,0.0,0.0,110.85682464923818,110.85682464923818,101126.42264905928,0.0,1000.0,0.0,250.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,500.0,1000.0,2.0,,,0.0,0.0,110.85682464923818,110.85682464923818,50756.24653308439,0.0,500.0,0.0,469.041575982343,0.0,469.041575982343,469.041575982343,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,500.0,2000.0,4.0,,,0.0,0.0,110.85682464923818,110.85682464923818,101390.47883934456,0.0,1000.0,0.0,500.0,0.0,938.0831519646858,938.083151964686,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,500.0,3000.0,6.0,,,0.0,0.0,110.85682464923818,110.85682464923818,151541.88242497374,0.0,1500.0,0.0,500.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,500.0,4000.0,8.0,,,0.0,0.0,110.85682464923818,110.85682464923818,202252.84529811857,0.0,2000.0,0.0,500.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,750.0,1500.0,2.0,,,0.0,0.0,110.85682464923818,110.85682464923818,76134.3697996266,0.0,750.0,0.0,703.5623639735145,0.0,703.5623639735145,703.5623639735145,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,750.0,3000.0,4.0,,,0.0,0.0,110.85682464923818,110.85682464923818,152085.71825901684,0.0,1500.0,0.0,750.0,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,750.0,4500.0,6.0,,,0.0,0.0,110.85682464923818,110.85682464923818,227312.8236374606,0.0,2250.0,0.0,750.0,0.0,2110.687091920543,2110.6870919205435,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,750.0,6000.0,8.0,,,0.0,0.0,110.85682464923818,110.85682464923818,303379.26794717787,0.0,3000.0,0.0,750.0,0.0,2814.249455894057,2814.249455894058,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,1000.0,2000.0,2.0,,,0.0,0.0,110.85682464923818,110.85682464923818,101512.49306616878,0.0,1000.0,0.0,938.083151964686,0.0,938.083151964686,938.083151964686,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,1000.0,4000.0,4.0,,,0.0,0.0,110.85682464923818,110.85682464923818,202780.9576786891,0.0,2000.0,0.0,1000.0,0.0,1876.166303929372,1876.166303929372,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,1000.0,6000.0,6.0,,,0.0,0.0,110.85682464923818,110.85682464923818,303083.7648499475,0.0,3000.0,0.0,1000.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,1000.0,8000.0,8.0,,,0.0,0.0,110.85682464923818,110.85682464923818,404505.69059623714,0.0,4000.0,0.0,1000.0,0.0,3752.332607858744,3752.332607858744,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,1500.0,3000.0,2.0,,,0.0,0.0,110.85682464923818,110.85682464923818,152268.7395992532,0.0,1500.0,0.0,1407.124727947029,0.0,1407.124727947029,1407.124727947029,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,1500.0,6000.0,4.0,,,0.0,0.0,110.85682464923818,110.85682464923818,304171.4365180337,0.0,3000.0,0.0,1500.0,0.0,2814.249455894058,2814.249455894058,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,1500.0,9000.0,6.0,,,0.0,0.0,110.85682464923818,110.85682464923818,454625.6472749212,0.0,4500.0,0.0,1500.0,0.0,4221.374183841086,4221.374183841087,v2.1.0,0.2789835999719798,True
SURPLUS_FIRST,FAR_TARGET,1500.0,12000.0,8.0,,,0.0,0.0,110.85682464923818,110.85682464923818,606758.5358943557,0.0,6000.0,0.0,1500.0,0.0,5628.498911788115,5628.498911788116,v2.1.0,0.2789835999719798,True
```

### Q4/HIGH_GAS - Q4_sizing_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q4\scen\HIGH_GAS\tables\Q4_sizing_summary.csv`

```csv
country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,revenue_bess_price_taker,soc_min,soc_max,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,initial_deliverable_mwh,engine_version,compute_time_sec,cache_hit,notes_quality
DE,2040,SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,149.25240313522823,149.25240313522823,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3443929000059142,True,ok
ES,2040,SURPLUS_FIRST,FAR_TARGET,0.0,0.0,2.0,,,0.0,0.0,109.40495630431788,109.40495630431788,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,v2.1.0,0.3382575999712571,True,ok
```

## Q5

### Q5 - contexte
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\question_context.json`

```json
{
  "question_id": "Q5",
  "objective": "Mesurer l'impact CO2/gaz sur l'ancre thermique (TCA/TTL) et calculer le CO2 requis pour une cible TTL.",
  "countries_scope": [
    "DE",
    "ES"
  ],
  "run_id": "FULL_20260210_172152",
  "source_summary_file": "outputs\\combined\\FULL_20260210_172152\\Q5\\summary.json",
  "source_refs_in_ledger": [
    "SPEC2-Q5",
    "SPEC2-Q5/Slides 28",
    "SPEC2-Q5/Slides 29",
    "SPEC2-Q5/Slides 31"
  ],
  "scenarios": [
    "BASE",
    "HIGH_BOTH",
    "HIGH_CO2",
    "HIGH_GAS"
  ],
  "country_filter_notes": {
    "hist_unfilterable_tables": [],
    "scen_unfilterable_tables_by_scenario": {
      "BASE": [],
      "HIGH_BOTH": [],
      "HIGH_CO2": [],
      "HIGH_GAS": []
    }
  }
}
```

### Q5 - test ledger
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\test_ledger.csv`

```csv
test_id,question_id,source_ref,mode,scenario_group,title,what_is_tested,metric_rule,severity_if_fail,scenario_id,status,value,threshold,interpretation
Q5-H-01,Q5,SPEC2-Q5/Slides 28,HIST,HIST_BASE,Ancre thermique historique,TTL/TCA/alpha/corr sont estimes hors surplus.,Q5_summary non vide avec ttl_obs et tca_q95,HIGH,,PASS,share_fini=100.00%,>=80% lignes ttl/tca finies,L'ancre thermique est quantifiable sur la majorite des pays.
Q5-H-02,Q5,SPEC2-Q5,HIST,HIST_BASE,Sensibilites analytiques,dTCA/dCO2 et dTCA/dGas sont positives.,dTCA_dCO2 > 0 et dTCA_dGas > 0,CRITICAL,,PASS,share_positive=100.00%,100% lignes >0,Sensibilites analytiques globalement coherentes.
Q5-S-01,Q5,SPEC2-Q5/Slides 29,SCEN,DEFAULT,Sensibilites scenarisees,BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.,Q5_summary non vide sur scenarios selectionnes,HIGH,BASE,PASS,7,>0 lignes,Sensibilites scenario calculees.
Q5-S-01,Q5,SPEC2-Q5/Slides 29,SCEN,DEFAULT,Sensibilites scenarisees,BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.,Q5_summary non vide sur scenarios selectionnes,HIGH,HIGH_CO2,PASS,7,>0 lignes,Sensibilites scenario calculees.
Q5-S-01,Q5,SPEC2-Q5/Slides 29,SCEN,DEFAULT,Sensibilites scenarisees,BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.,Q5_summary non vide sur scenarios selectionnes,HIGH,HIGH_GAS,PASS,7,>0 lignes,Sensibilites scenario calculees.
Q5-S-01,Q5,SPEC2-Q5/Slides 29,SCEN,DEFAULT,Sensibilites scenarisees,BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.,Q5_summary non vide sur scenarios selectionnes,HIGH,HIGH_BOTH,PASS,7,>0 lignes,Sensibilites scenario calculees.
Q5-S-02,Q5,SPEC2-Q5/Slides 31,SCEN,DEFAULT,CO2 requis pour TTL cible,Le CO2 requis est calcule et interpretable.,co2_required_* non NaN,MEDIUM,BASE,PASS,share_finite=100.00%,>=80% valeurs finies,CO2 requis interpretable sur le panel.
Q5-S-02,Q5,SPEC2-Q5/Slides 31,SCEN,DEFAULT,CO2 requis pour TTL cible,Le CO2 requis est calcule et interpretable.,co2_required_* non NaN,MEDIUM,HIGH_CO2,PASS,share_finite=100.00%,>=80% valeurs finies,CO2 requis interpretable sur le panel.
Q5-S-02,Q5,SPEC2-Q5/Slides 31,SCEN,DEFAULT,CO2 requis pour TTL cible,Le CO2 requis est calcule et interpretable.,co2_required_* non NaN,MEDIUM,HIGH_GAS,PASS,share_finite=100.00%,>=80% valeurs finies,CO2 requis interpretable sur le panel.
Q5-S-02,Q5,SPEC2-Q5/Slides 31,SCEN,DEFAULT,CO2 requis pour TTL cible,Le CO2 requis est calcule et interpretable.,co2_required_* non NaN,MEDIUM,HIGH_BOTH,PASS,share_finite=100.00%,>=80% valeurs finies,CO2 requis interpretable sur le panel.
```

### Q5 - comparaison HIST vs SCEN
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\comparison_hist_vs_scen.csv`

```csv
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
DE,BASE,ttl_obs,288.6709999999999,219.15565729933,-69.51534270066992,,INFORMATIVE,delta_interpretable
DE,BASE,tca_q95,438.6194473684211,229.0263157894737,-209.5931315789474,,INFORMATIVE,delta_interpretable
DE,BASE,co2_required_base_non_negative,0.0,44.07873966643583,44.07873966643583,,INFORMATIVE,delta_interpretable
ES,BASE,ttl_obs,216.0,170.38790045594791,-45.612099544052086,,INFORMATIVE,delta_interpretable
ES,BASE,tca_q95,288.85923636363634,130.67272727272726,-158.18650909090908,,INFORMATIVE,delta_interpretable
ES,BASE,co2_required_base_non_negative,0.0,81.71611261994379,81.71611261994379,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,ttl_obs,288.6709999999999,236.4299994045931,-52.24100059540677,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,tca_q95,438.6194473684211,278.38157894736844,-160.23786842105267,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,co2_required_base_non_negative,0.0,79.82873966643585,79.82873966643585,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,ttl_obs,216.0,177.44541899020564,-38.55458100979436,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,tca_q95,288.85923636363634,150.87272727272727,-137.98650909090907,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,co2_required_base_non_negative,0.0,117.50009680884608,117.50009680884608,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,ttl_obs,288.6709999999999,241.2609204572247,-47.41007954277518,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,tca_q95,438.6194473684211,292.1842105263158,-146.43523684210533,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,co2_required_base_non_negative,0.0,19.44530858139184,19.44530858139184,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,ttl_obs,216.0,185.6481462629329,-30.351853737067103,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,tca_q95,288.85923636363634,174.3090909090909,-114.55014545454544,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,co2_required_base_non_negative,0.0,40.1659383930045,40.1659383930045,,INFORMATIVE,delta_interpretable
DE,HIGH_BOTH,ttl_obs,288.6709999999999,219.15565729933,-69.51534270066992,,INFORMATIVE,delta_interpretable
DE,HIGH_BOTH,tca_q95,438.6194473684211,341.5394736842105,-97.0799736842106,,INFORMATIVE,delta_interpretable
DE,HIGH_BOTH,co2_required_base_non_negative,0.0,99.07873966643584,99.07873966643584,,INFORMATIVE,delta_interpretable
ES,HIGH_BOTH,ttl_obs,216.0,170.38790045594791,-45.612099544052086,,INFORMATIVE,delta_interpretable
ES,HIGH_BOTH,tca_q95,288.85923636363634,194.5090909090909,-94.35014545454544,,INFORMATIVE,delta_interpretable
ES,HIGH_BOTH,co2_required_base_non_negative,0.0,136.7161126199438,136.7161126199438,,INFORMATIVE,delta_interpretable
```

### Q5 - checks filtrés
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\checks_filtered.csv`

```csv
status,code,message,scope,scenario_id,question_id,mentioned_countries,is_global
INFO,Q5_CO2_TARGET_ALREADY_BELOW_BASELINE,CO2 requis brut negatif: cible TTL deja atteinte sans CO2 additionnel.,HIST,,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,HIST,,Q5,,True
INFO,Q5_CO2_TARGET_ALREADY_BELOW_BASELINE,CO2 requis brut negatif: cible TTL deja atteinte sans CO2 additionnel.,HIST,,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,HIST,,Q5,,True
INFO,Q5_CO2_TARGET_ALREADY_BELOW_BASELINE,CO2 requis brut negatif: cible TTL deja atteinte sans CO2 additionnel.,HIST,,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,HIST,,Q5,,True
INFO,Q5_CO2_TARGET_ALREADY_BELOW_BASELINE,CO2 requis brut negatif: cible TTL deja atteinte sans CO2 additionnel.,HIST,,Q5,,True
INFO,Q5_CO2_TARGET_ALREADY_BELOW_BASELINE,CO2 requis brut negatif: cible TTL deja atteinte sans CO2 additionnel.,HIST,,Q5,,True
INFO,Q5_CO2_TARGET_ALREADY_BELOW_BASELINE,CO2 requis brut negatif: cible TTL deja atteinte sans CO2 additionnel.,HIST,,Q5,,True
INFO,Q5_CO2_TARGET_ALREADY_BELOW_BASELINE,CO2 requis brut negatif: cible TTL deja atteinte sans CO2 additionnel.,HIST,,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,BASE,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,SCEN,BASE,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,BASE,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,BASE,Q5,,True
PASS,Q5_PASS,Q5 checks passes.,SCEN,BASE,Q5,,True
PASS,Q5_PASS,Q5 checks passes.,SCEN,BASE,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,BASE,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,HIGH_CO2,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,SCEN,HIGH_CO2,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,SCEN,HIGH_CO2,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,HIGH_CO2,Q5,,True
PASS,Q5_PASS,Q5 checks passes.,SCEN,HIGH_CO2,Q5,,True
PASS,Q5_PASS,Q5 checks passes.,SCEN,HIGH_CO2,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,HIGH_CO2,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,HIGH_GAS,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,SCEN,HIGH_GAS,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,SCEN,HIGH_GAS,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,HIGH_GAS,Q5,,True
INFO,Q5_CO2_TARGET_ALREADY_BELOW_BASELINE,CO2 requis brut negatif: cible TTL deja atteinte sans CO2 additionnel.,SCEN,HIGH_GAS,Q5,,True
PASS,Q5_PASS,Q5 checks passes.,SCEN,HIGH_GAS,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,HIGH_GAS,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,HIGH_BOTH,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,SCEN,HIGH_BOTH,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,SCEN,HIGH_BOTH,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,HIGH_BOTH,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,SCEN,HIGH_BOTH,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,HIGH_BOTH,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,SCEN,HIGH_BOTH,Q5,,True
PASS,Q5_PASS,Q5 checks passes.,SCEN,HIGH_BOTH,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,SCEN,HIGH_BOTH,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,SCEN,HIGH_BOTH,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,SCEN,HIGH_BOTH,Q5,,True
PASS,BUNDLE_LEDGER_STATUS,"ledger: FAIL=0, WARN=0",BUNDLE,,Q5,,True
PASS,BUNDLE_INFORMATIVENESS,share_tests_informatifs=100.00% ; share_compare_informatifs=98.81%,BUNDLE,,Q5,,True
```

### Q5 - warnings filtrés
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\warnings_filtered.csv`

```csv

```

### Q5 - historique - Q5_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\hist\tables\Q5_summary.csv`

```csv
country,year_range_used,marginal_tech,ttl_obs,tca_q95,alpha,corr_cd,dTCA_dCO2,dTCA_dGas,ttl_target,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
DE,2018-2024,COAL,288.6709999999999,438.6194473684211,-149.94844736842123,0.8818358874738825,0.8973684210526316,2.631578947368421,160.0,-60.55598240469188,,0.0,,
ES,2018-2024,CCGT,216.0,288.85923636363634,-72.85923636363634,0.7251840607282367,0.3672727272727272,1.818181818181818,160.0,-77.11594059405948,,0.0,,
```

### Q5 - scénario `BASE`

### Q5/BASE - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\BASE\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
PASS,Q5_PASS,Q5 checks passes.,Q5,,True
PASS,Q5_PASS,Q5 checks passes.,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
```

### Q5/BASE - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\BASE\warnings_filtered.csv`

```csv

```

### Q5/BASE - Q5_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\BASE\tables\Q5_summary.csv`

```csv
country,year_range_used,marginal_tech,ttl_obs,tca_q95,alpha,corr_cd,dTCA_dCO2,dTCA_dGas,ttl_target,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
DE,2030-2040,COAL,219.15565729933,229.0263157894737,-9.87065849014374,0.199451274769226,0.8973684210526316,2.631578947368421,160.0,44.07873966643583,,44.07873966643583,,
ES,2030-2040,CCGT,170.38790045594791,130.67272727272726,39.71517318322066,0.1535935581861058,0.3672727272727272,1.818181818181818,160.0,81.71611261994379,,81.71611261994379,,
```

### Q5 - scénario `HIGH_BOTH`

### Q5/HIGH_BOTH - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_BOTH\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,Q5,,True
PASS,Q5_PASS,Q5 checks passes.,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,Q5,,True
```

### Q5/HIGH_BOTH - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_BOTH\warnings_filtered.csv`

```csv

```

### Q5/HIGH_BOTH - Q5_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_BOTH\tables\Q5_summary.csv`

```csv
country,year_range_used,marginal_tech,ttl_obs,tca_q95,alpha,corr_cd,dTCA_dCO2,dTCA_dGas,ttl_target,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
DE,2030-2040,COAL,219.15565729933,341.5394736842105,-122.38381638488056,0.199451274769226,0.8973684210526316,2.631578947368421,160.0,99.07873966643584,,99.07873966643584,,
ES,2030-2040,CCGT,170.38790045594791,194.5090909090909,-24.121190453142987,0.1535935581861063,0.3672727272727272,1.818181818181818,160.0,136.7161126199438,,136.7161126199438,,
```

### Q5 - scénario `HIGH_CO2`

### Q5/HIGH_CO2 - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_CO2\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
PASS,Q5_PASS,Q5 checks passes.,Q5,,True
PASS,Q5_PASS,Q5 checks passes.,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
```

### Q5/HIGH_CO2 - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_CO2\warnings_filtered.csv`

```csv

```

### Q5/HIGH_CO2 - Q5_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_CO2\tables\Q5_summary.csv`

```csv
country,year_range_used,marginal_tech,ttl_obs,tca_q95,alpha,corr_cd,dTCA_dCO2,dTCA_dGas,ttl_target,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
DE,2030-2040,COAL,236.4299994045931,278.38157894736844,-41.951579542775335,0.228477586365217,0.8973684210526316,2.631578947368421,160.0,79.82873966643585,,79.82873966643585,,
ES,2030-2040,CCGT,177.44541899020564,150.87272727272727,26.572691717478364,0.1702685915675326,0.3672727272727272,1.818181818181818,160.0,117.50009680884608,,117.50009680884608,,
```

### Q5 - scénario `HIGH_GAS`

### Q5/HIGH_GAS - checks
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_GAS\checks_filtered.csv`

```csv
status,code,message,question_id,mentioned_countries,is_global
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,Q5,,True
WARN,Q5_ALPHA_NEG,Alpha tres negatif: techno marginale possiblement inadaptee.,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
INFO,Q5_CO2_TARGET_ALREADY_BELOW_BASELINE,CO2 requis brut negatif: cible TTL deja atteinte sans CO2 additionnel.,Q5,,True
PASS,Q5_PASS,Q5 checks passes.,Q5,,True
WARN,Q5_LOW_CORR_CD,Relation prix-ancre faible sur regimes C/D (corr<0.2).,Q5,,True
```

### Q5/HIGH_GAS - warnings
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_GAS\warnings_filtered.csv`

```csv

```

### Q5/HIGH_GAS - Q5_summary.csv
Source: `reports\chatgpt52_structured_FULL_20260210_172152_DE_ES\questions\Q5\scen\HIGH_GAS\tables\Q5_summary.csv`

```csv
country,year_range_used,marginal_tech,ttl_obs,tca_q95,alpha,corr_cd,dTCA_dCO2,dTCA_dGas,ttl_target,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
DE,2030-2040,COAL,241.2609204572247,292.1842105263158,-50.92329006909108,0.2208315169968148,0.8973684210526316,2.631578947368421,160.0,19.44530858139184,,19.44530858139184,,
ES,2030-2040,CCGT,185.6481462629329,174.3090909090909,11.339055353841983,0.1750043797464875,0.3672727272727272,1.818181818181818,160.0,40.1659383930045,,40.1659383930045,,
```
