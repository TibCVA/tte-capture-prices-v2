# Audit Methods Reference (Q1-Q5)

Last updated: 2026-02-10 19:30 UTC
Auto-generated from Python source code by `scripts/generate_audit_methods.py`.
Regenerated automatically when analysis engine files change.

## 1. Purpose and governance

This document is the methodological reference for formulas, data, hypotheses, and checks used by Q1-Q5 (HIST + SCEN).
It is auto-generated from the live codebase to guarantee synchronization with the analysis engine.

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

- ENTSO-E raw cache: `data/raw/entsoe/prices_da/{country}/{year}.parquet` (+ load_total, generation_by_type, net_position)
- Canonical hourly: `data/processed/hourly/{country}/{year}.parquet`
- Historical annual metrics: `data/metrics/annual_metrics.parquet`
- Historical daily metrics: `data/metrics/daily_metrics.parquet`
- Validation findings: `data/metrics/validation_findings.parquet`

### 2.2 Prospective (SCEN)

- Scenario assumptions: `data/assumptions/phase2/phase2_scenario_country_year.csv`
- Scenario hourly outputs: `data/processed/scenario/{scenario_id}/hourly/{country}/{year}.parquet`
- Scenario annual metrics: `data/processed/scenario/{scenario_id}/annual_metrics.parquet`

### 2.3 Common assumptions

- Phase 1 assumptions: `data/assumptions/phase1_assumptions.csv`
- Country config: `config/countries.yaml`
- PSR mapping: `data/static/entsoe_psr_mapping.csv`


## 3. Canonical physical and market formulas

Implementation: `src/metrics.py` and preprocessing pipeline.

### 3.1 Core hourly variables

- `gen_vre_mw = gen_solar_mw + gen_wind_on_mw + gen_wind_off_mw`
- `nrl_mw = load_mw - gen_vre_mw - gen_must_run_mw`
- `surplus_mw = max(0, -nrl_mw)`
- `exports_mw = max(net_position_mw, 0)`
- `flex_sink_observed_mw = exports_mw + flex_sink_psh_pump_mw`
- `surplus_absorbed_mw = min(surplus_mw, flex_effective_mw)`
- `surplus_unabsorbed_mw = surplus_mw - surplus_absorbed_mw`

### 3.2 Regime classification (anti-circular, no price input)

- A: `surplus_unabsorbed_mw > 0`
- B: `surplus_mw > 0` and `surplus_unabsorbed_mw == 0`
- D: `surplus_mw == 0` and `nrl_mw >= threshold_peak_mw`
- C: remaining hours

Threshold D default: `P90(nrl_mw on positive nrl)` with minimum positive-hour guard.

### 3.3 Annual metrics

- Baseload price: `mean(price_da)`
- Capture price (tech X): `sum(price * gen_X) / sum(gen_X)`
- Capture ratio vs baseload: `capture_X / baseload`
- Capture ratio vs TTL: `capture_X / ttl`
- TTL (price-based): `P95(price)` on regimes C + D
- SR (energy share): `surplus_energy / gen_primary_energy`
- FAR: `surplus_absorbed_energy / surplus_energy` (NaN if denominator = 0)
- IR: `P10(gen_must_run_mw) / P10(load_mw)`

### 3.4 Quality indicators

- Completeness: share of hours without critical missing data
- Quality flag: `OK` if completeness >= 0.98, `WARN` if >= 0.90, `FAIL` otherwise
- Regime coherence: share of hours where price aligns with expected regime pattern
- NRL-price correlation: Pearson correlation on non-missing hours


## 4. Question-by-question analytical logic

## 4.1 Q1 - Transition Phase 1 -> Phase 2

Q1 - Phase 1 to Phase 2 transition analysis.

### Objective

Detect transition year with two independent diagnostics: market symptoms and physical stress.

### Configurable parameters (current values)

| Parametre | Valeur | Unite | Description |
|-----------|--------|-------|-------------|
| `capture_ratio_pv_vs_ttl_crisis_max` | 0.7 | ratio | Seuil crise capture ratio pv/ttl |
| `capture_ratio_pv_vs_ttl_stage2_max` | 0.8 | ratio | Seuil capture ratio pv/ttl |
| `days_spread_gt50_stage2_min` | 150.0 | days | Seuil jours spread>50 |
| `h_below_5_stage2_min` | 500.0 | hours | Seuil heures basses |
| `h_negative_stage2_min` | 200.0 | hours | Seuil heures negatives stage2 |
| `h_negative_stage2_strong` | 300.0 | hours | Seuil fort heures negatives |
| `stage1_capture_ratio_pv_vs_ttl_min` | 0.9 | ratio | Stage1 min capture ratio pv vs ttl |
| `stage1_days_spread_gt50_max` | 120.0 | days | Stage1 max days spread gt50 |
| `stage1_h_below_5_max` | 300.0 | hours | Stage1 max hours below 5 |
| `stage1_h_negative_max` | 100.0 | hours | Stage1 max negative hours |
| `far_energy_tension_max` | 0.95 | ratio | Seuil far tension |
| `ir_p10_high_min` | 0.7 | ratio | Seuil inflexibilite haute |
| `sr_energy_material_min` | 0.01 | ratio | Seuil surplus ratio materialite |
| `regime_coherence_min_for_causality` | 0.55 | ratio | Seuil coherence minimale causalite |
| `q1_require_non_capture_signal` | 1.0 | bool01 | Q1: exiger au moins un signal non-capture (h_negative, h_below_5 ou spread) pour classer phase2. |
| `q1_min_non_capture_flags` | 1.0 | count | Q1: nombre minimal de flags non-capture requis pour phase2. |


### Calculations

1. `stage2_market_score` from points on: `h_negative_obs`, `h_below_5_obs`, `capture_ratio_pv_vs_ttl`, `days_spread_gt50`
2. Phase2 market condition: score >= 2, with optional non-capture signal gate (`q1_require_non_capture_signal`)
3. Physical stress flags: `sr_energy >= sr_energy_material_min`, `far_energy <= far_energy_tension_max`, `ir_p10 >= ir_p10_high_min`
4. Transition years: market transition year, physical transition year
5. Confidence penalty from coherence/completeness

### Outputs

- `Q1_country_summary`
- `Q1_year_panel`
- checks/warnings on incoherent transition signals

### Robustness

- `quality_flag == FAIL` invalidates strong conclusions
- capture-only signals are warned


## 4.2 Q2 - Phase 2 slope and drivers

Q2 - Phase 2 slope and drivers.

### Objective

Estimate cannibalization slope for PV/Wind after Q1 transition, and rank drivers.

### Configurable parameters (current values)

| Parametre | Valeur | Unite | Description |
|-----------|--------|-------|-------------|
| `exclude_year_2022` | 0.0 | bool | Exclude 2022 from regressions (1=yes) |
| `min_points_regression` | 3.0 | count | Nombre minimal de points regression |


### Calculations

1. Build Phase2 subset per country (years >= transition year from Q1)
2. Regression per tech: preferred x = penetration, fallback x = `sr_energy`, y = capture ratio vs TTL
3. Estimator: OLS when data sufficient, `DELTA_2PT` directional slope when only two points
4. Driver features: mean SR/FAR/IR/TTL on phase2 subset, hourly `corr(gen_vre_mw, load_mw)`, surplus share in low-load quartile
5. Cross-country driver correlations against slope

### Outputs

- `Q2_country_slopes`
- `Q2_driver_correlations`
- robustness flag per slope (`ROBUST`, `FRAGILE`, `NON_TESTABLE`)


## 4.3 Q3 - Exit Phase 2 and inversion conditions

Q3 - Exit from Phase 2 and inversion conditions.

### Objective

Classify trend status and estimate static inversion orders of magnitude.

### Configurable parameters (current values)

| Parametre | Valeur | Unite | Description |
|-----------|--------|-------|-------------|
| `demand_k_max` | 0.3 | ratio | Borne max hausse demande |
| `far_target` | 0.95 | ratio | Cible FAR inversion |
| `require_recent_stage2` | 1.0 | bool | Require recent stage2 stress |
| `sr_energy_target` | 0.01 | ratio | Cible SR inversion |
| `stage2_recent_h_negative_min` | 200.0 | hours | Recent stage2 threshold on negative hours |
| `trend_capture_ratio_min` | 0.0 | ratio/year | Improvement threshold for capture trend |
| `trend_h_negative_max` | -10.0 | hours/year | Improvement threshold for h_negative trend |
| `trend_window_years` | 3.0 | years | Fenetre tendance Q3 |
| `stage2_recent_h_negative_min_scen` | 80.0 | h/an | Q3 SCEN: seuil h_negative recent pour qualifier un contexte Stage2 en prospectif. |
| `stage2_recent_sr_energy_min_scen` | 0.02 | ratio | Q3 SCEN: seuil SR recent pour qualifier un contexte Stage2 meme si h_negative reste faible. |


### Calculations

1. Trends on rolling window: `trend_h_negative`, `trend_capture_ratio_pv_vs_ttl`, `trend_sr_energy`, `trend_far_energy`
2. Status assignment: `degradation`, `stabilisation`, `amelioration`, `transition_partielle`, `hors_scope_stage2`
3. Counterfactuals (binary search): demand uplift `k` for SR target, must-run reduction `r` for SR target, additional absorbed energy for FAR target
4. Additional sink power proxy: `P95(surplus_unabsorbed_mw)`

### Outputs

- `Q3_status`

### Interpretation

`hors_scope_stage2` means the scenario is not stressed enough for a phase2-exit statement (explicit non-testability).


## 4.4 Q4 - BESS sizing and impact

Q4 - BESS sizing and impact simulation.

### Objective

Quantify battery impact in three dispatch modes and estimate minimum sizing for target objective.

### Dispatch modes

- `SURPLUS_FIRST` (system stress absorption)
- `PRICE_ARBITRAGE_SIMPLE` (simple value spread)
- `PV_COLOCATED` (PV + storage value uplift)

### Configurable parameters (current values)

| Parametre | Valeur | Unite | Description |
|-----------|--------|-------|-------------|
| `bess_eta_roundtrip` | 0.88 | ratio | Rendement roundtrip BESS |
| `bess_max_cycles_per_day` | 1.0 | cycles/day | Cycles max journaliers BESS |
| `bess_soc_init_frac` | 0.5 | ratio | SOC initial fraction |
| `target_far` | 0.95 | ratio | Cible FAR pour sizing |
| `target_surplus_unabs_energy_twh` | 0.0 | TWh | Cible surplus non absorbe |


### Calculations

1. Numpy dispatch simulation with daily masks
2. SOC and power constraints enforced each hour
3. Post-BESS absorbed and unabsorbed surplus recomputation
4. Frontier over grid: FAR before/after, unabsorbed energy before/after, capture uplift, price-taker revenue
5. Objective selection: `FAR_TARGET` or `SURPLUS_UNABS_TARGET`, choose minimum feasible by power then energy

### Invariants

- `0 <= SOC <= Emax`
- `charge <= Pmax`, `discharge <= Pmax`
- discharged energy <= charged energy * eta
- monotonic surplus reduction in `SURPLUS_FIRST`

### Outputs

- `Q4_sizing_summary`
- `Q4_bess_frontier`


## 4.5 Q5 - CO2/Gas thermal anchor

Q5 - Thermal anchor sensitivity to gas and CO2.

### Objective

Measure thermal anchor behavior and sensitivities to gas/CO2 on non-surplus hours.

### Thermal defaults (from `src/constants.py`)

- **CCGT**: efficiency=0.55, emission_factor=0.202 tCO2/MWhth, VOM=3.0 EUR/MWh
- **COAL**: efficiency=0.38, emission_factor=0.341 tCO2/MWhth, VOM=4.0 EUR/MWh

### Configurable parameters (current values)

| Parametre | Valeur | Unite | Description |
|-----------|--------|-------|-------------|
| `ccgt_ef_t_per_mwh_th` | 0.202 | tCO2/MWhth | Facteur emission CCGT |
| `ccgt_efficiency` | 0.55 | ratio | Rendement CCGT |
| `ccgt_vom_eur_mwh` | 3.0 | EUR/MWh | VOM CCGT |
| `coal_ef_t_per_mwh_th` | 0.341 | tCO2/MWhth | Facteur emission charbon |
| `coal_efficiency` | 0.38 | ratio | Rendement charbon |
| `coal_vom_eur_mwh` | 4.0 | EUR/MWh | VOM charbon |


### Calculations

1. Thermal anchor: `tca = gas/eff + co2*(ef/eff) + vom`
2. Restrict to regimes C/D for comparison
3. Compute: `ttl_obs = P95(price on C/D)`, `tca_q95 = P95(tca on C/D)`, `alpha = ttl_obs - tca_q95`, `corr_cd = corr(price, tca) on C/D`
4. Sensitivities: `dTCA/dGas = 1/eff`, `dTCA/dCO2 = ef/eff`
5. CO2 required for target TTL: solve from `ttl_target = alpha + tca_q95_scenario`

### Outputs

- `Q5_summary`
- checks on derivative signs and weak/fragile anchor relation


## 5. Prospective engine (SCEN) mechanics

Main code: `src/scenario/calibration.py`, `src/scenario/phase2_engine.py`.

### 5.1 Historical calibration per country

Calibrated values include: must-run floors, export and PSH realization factors, stress penalty, regime-B price fit, C/D levels, NRL quantiles, surplus percentile scaling.

### 5.2 Prospective physical projection

1. Select historical reference year by country
2. Scale load profile to target annual demand
3. Scale VRE profiles to target capacities
4. Build must-run profiles from scenario capacities and calibrated floors/caps
5. Apply conservative flex ordering: exports sink, PSH sink, BESS sink
6. Recompute surplus absorption and unabsorbed surplus
7. Reclassify regimes (A/B/C/D) after BESS
8. Inject synthetic piecewise-affine prices with calibrated regime-B behavior


## 6. Standard evidence outputs

Per question bundle: `outputs/combined/{run_id}/Qx/` with summary.json, test_ledger.csv, comparison_hist_vs_scen.csv, hist/tables/*.csv, scen/{scenario_id}/tables/*.csv.

Status semantics: `PASS` (test passed), `WARN` (potential fragility), `FAIL` (hard inconsistency), `NON_TESTABLE` (not enough signal/data).


## 7. Known limitations

1. No full equilibrium dispatch model.
2. Scenario logic is pragmatic stress-testing, not market forecast.
3. Some question/scenario pairs can be `NON_TESTABLE` by design when stress is absent.
4. Correlations and slopes are explanatory signals, not automatic causal proof.
