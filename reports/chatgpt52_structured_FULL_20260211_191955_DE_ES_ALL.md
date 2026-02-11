# PAYLOAD LLM - Audit DE/ES

Ce document est prêt à être copié-collé dans un autre LLM pour un audit rigoureux.
Généré le: `2026-02-11 19:36:06 UTC`
Package source: `reports\chatgpt52_structured_FULL_20260211_191955_DE_ES`
Run ID: `FULL_20260211_191955`
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

Last updated: 2026-02-10 20:11 UTC
Auto-generated from Python source code by `scripts/generate_audit_methods.py`.
Regenerated automatically when analysis engine files change.

## 1. Purpose and governance

This document is the methodological reference for formulas, data, hypotheses, and checks used by Q1-Q5 (HIST + SCEN).
It is auto-generated from the live codebase to guarantee synchronization with the analysis engine.

Authoritative code paths:

- `src/metrics.py` — formules annuelles et qualite
- `src/processing.py` — construction table horaire, NRL, regimes, nettoyage
- `src/data_fetcher.py` — collecte ENTSO-E et cache
- `src/validation_report.py` — invariants durs et checks de realite
- `src/modules/q1_transition.py` .. `q5_thermal_anchor.py` — logique analytique Q1-Q5
- `src/scenario/calibration.py` — calibration historique par pays
- `src/scenario/phase2_engine.py` — projection prospective


## 2. Sources de donnees

L'outil combine plusieurs sources publiques et institutionnelles. Aucune donnee proprietaire n'est utilisee.

### 2.1 ENTSO-E Transparency Platform (source primaire historique)

Collecte via l'API ENTSO-E (bibliotheque `entsoe-py`), cle API requise.
Donnees horaires par pays-annee, stockees en cache local Parquet :

| Dataset | Contenu | Chemin cache |
|---------|---------|--------------|
| `prices_da` | Prix day-ahead (EUR/MWh) | `data/raw/entsoe/prices_da/{country}/{year}.parquet` |
| `load_total` | Charge totale (MW) | `data/raw/entsoe/load_total/{country}/{year}.parquet` |
| `generation_by_type` | Generation par filiere (MW) | `data/raw/entsoe/generation_by_type/{country}/{year}.parquet` |
| `net_position` | Position nette / flux physiques (MW) | `data/raw/entsoe/net_position/{country}/{year}.parquet` |
| `psh_pump` | Pompage STEP (MW) | `data/raw/entsoe/psh_pump/{country}/{year}.parquet` |

Mapping des codes generation ENTSO-E (PSR) vers colonnes canoniques : `data/static/entsoe_psr_mapping.csv`.

### 2.2 ENTSO-E TYNDP 2024 (source prospective)

Donnees du Ten-Year Network Development Plan 2024 pour les scenarios prospectifs :

| Fichier normalise | Contenu | Source brute |
|-------------------|---------|--------------|
| `data/external/normalized/tyndp2024_demand_scenarios.csv` | Demande annuelle par pays/scenario/annee | TYNDP 2024 XLSX |
| `data/external/normalized/tyndp2024_capacities.csv` | Capacites installees par pays/techno/scenario | TYNDP 2024 XLSX |
| `data/external/normalized/tyndp2024_fuel_co2_prices.csv` | Prix gaz et CO2 par scenario | TYNDP 2024 XLSX |

Ces donnees alimentent les hypotheses Phase 2 (`data/assumptions/phase2/phase2_scenario_country_year.csv`).

### 2.3 NREL ATB et IRENA (couts technologiques)

Benchmarks de couts utilises pour le cadrage des hypotheses :

| Fichier normalise | Source | Contenu |
|-------------------|--------|---------|
| `data/external/normalized/tech_cost_benchmarks_atb.csv` | NREL Annual Technology Baseline 2024 v3 | LCOE, CAPEX, O&M par techno |
| `data/external/normalized/tech_cost_benchmarks_irena.csv` | IRENA Renewable Power Generation Costs 2023 | LCOE renouvelable global |

### 2.4 Donnees de calibration (pre-calculees)

| Fichier | Contenu | Usage |
|---------|---------|-------|
| `data/external/normalized/interconnection_proxy_phase1.csv` | Capacite d'export estimee par pays (GW) | Calibration prospective |
| `data/external/normalized/surplus_coincidence_matrix_phase1.csv` | Facteurs de coincidence export entre pays | Calibration prospective |

### 2.5 Prix commodites journaliers (optionnel, Q5)

- `data/external/commodity_prices_daily.csv` : prix gaz (EUR/MWh_th) et CO2 (EUR/t) journaliers
- Utilise par Q5 pour la sensibilite ancre thermique aux commodites reelles
- Si absent, Q5 utilise les valeurs des hypotheses Phase 2

### 2.6 Configuration et hypotheses

| Fichier | Contenu |
|---------|---------|
| `config/countries.yaml` | Definition pays : codes ENTSO-E, fuseaux, composition must-run, flex, techno marginale |
| `config/thresholds.yaml` | Seuils modele : completude, regime D, coherence, checks |
| `data/assumptions/phase1_assumptions.csv` | Hypotheses Phase 1 : seuils Q1-Q5, rendements thermiques, VOM |
| `data/assumptions/phase2/phase2_scenario_country_year.csv` | Hypotheses Phase 2 par scenario/pays/annee : demande, capacites, prix commodites |

### 2.7 Donnees intermediaires produites par le pipeline

| Fichier | Contenu | Producteur |
|---------|---------|------------|
| `data/processed/hourly/{country}/{year}.parquet` | Table horaire canonique (prix, charge, VRE, NRL, surplus, regimes) | `src/processing.py` |
| `data/metrics/annual_metrics.parquet` | Metriques annuelles historiques par pays-annee | `src/metrics.py` |
| `data/metrics/daily_metrics.parquet` | Metriques journalieres | `src/metrics.py` |
| `data/metrics/validation_findings.parquet` | Constats de validation (severite, code, message, evidence) | `src/validation_report.py` |
| `data/processed/scenario/{scen}/hourly/{country}/{year}.parquet` | Table horaire prospective | `src/scenario/phase2_engine.py` |
| `data/processed/scenario/{scen}/annual_metrics.parquet` | Metriques annuelles prospectives | `src/metrics.py` |


## 3. Formules canoniques et pipeline de qualite

### 3.1 Variables horaires

- `gen_vre_mw = gen_solar_mw + gen_wind_on_mw + gen_wind_off_mw`
- `nrl_mw = load_mw - gen_vre_mw - gen_must_run_mw` (Net Residual Load)
- `surplus_mw = max(0, -nrl_mw)`
- `exports_mw = max(net_position_mw, 0)`
- `flex_sink_observed_mw = exports_mw + flex_sink_psh_pump_mw`
- `surplus_absorbed_mw = min(surplus_mw, flex_effective_mw)`
- `surplus_unabsorbed_mw = surplus_mw - surplus_absorbed_mw`

Nettoyage des donnees brutes : les generations negatives < -0.1 MW sont mises a NaN ; les valeurs entre -0.1 et 0 sont arrondies a 0.
La charge nette (load_mw) est calculee comme `load_total - psh_pump` si les donnees de pompage sont suffisantes (>= 95% de couverture), sinon `load_total` directement.

### 3.2 Classification des regimes (anti-circulaire, sans prix)

Les regimes sont determines uniquement par les grandeurs physiques, sans utiliser le prix :

- **A** (surplus non absorbe) : `surplus_unabsorbed_mw > 0`
- **B** (surplus absorbe) : `surplus_mw > 0` et `surplus_unabsorbed_mw == 0`
- **D** (stress thermique) : `surplus_mw == 0` et `nrl_mw >= P90(nrl positif)`, avec minimum 200 heures NRL positif
- **C** (normal) : toutes les heures restantes

Le seuil du regime D (quantile 0.90 du NRL positif) est configurable dans `config/thresholds.yaml`.

### 3.3 Metriques annuelles

- **Prix baseload** : `mean(price_da)` sur toutes les heures
- **Prix peak/offpeak** : moyennes sur heures locales 8h-20h LJ / reste
- **Capture price (techno X)** : `sum(price * gen_X) / sum(gen_X)` — moyenne ponderee par la production
- **Capture ratio vs baseload** : `capture_X / baseload`
- **Capture ratio vs TTL** : `capture_X / ttl`
- **TTL** (Top Tail Level) : `P95(price)` sur les heures en regime C ou D uniquement
- **SR** (Surplus Ratio) : `surplus_energy / gen_primary_energy` — part de l'energie en surplus
- **FAR** (Flex Absorption Ratio) : `surplus_absorbed_energy / surplus_energy` — part du surplus absorbe (NaN si pas de surplus)
- **IR** (Inflexibility Ratio) : `P10(gen_must_run_mw) / P10(load_mw)` — rapport must-run / charge en creux
- **Penetration VRE** : `gen_vre_twh / gen_primary_twh`
- **Heures negatives** : nombre d'heures avec `price < 0`
- **Heures basses** : nombre d'heures avec `price <= 5 EUR/MWh`
- **Jours spread > 50** : nombre de jours ou `max(price) - min(price) >= 50 EUR/MWh`

### 3.4 Pipeline de qualite des donnees

Le pipeline applique 3 niveaux de controle :

**Niveau 1 — Completude et flags horaires** (dans `src/processing.py`) :
- `q_missing_price` : prix day-ahead absent
- `q_missing_load` : charge totale absente
- `q_missing_generation` : generation VRE ET must-run absentes simultanement
- `q_missing_net_position` : position nette absente
- `q_any_critical_missing` : au moins un des trois premiers flags actif
- Completude = part des heures sans donnee critique manquante

**Niveau 2 — Invariants durs** (dans `src/validation_report.py`, severite ERROR) :
- `INV_NRL` : identite NRL violee (`load - vre - must_run` != nrl, tolerance 1e-6)
- `INV_SURPLUS` : identite surplus violee (`max(-nrl, 0)` != surplus)
- `INV_UNABS_NEG` : surplus non absorbe negatif (impossible physiquement)
- `INV_UNABS_GT_SURPLUS` : surplus non absorbe > surplus total
- `INV_FAR_RANGE` : FAR hors [0, 1]
- `INV_SR_RANGE` : SR hors [0, 1]

**Niveau 3 — Checks de realite** (dans `src/modules/reality_checks.py`, severite WARN/FAIL) :
- `RC_SR_RANGE` : SR hors [0, 1] → FAIL
- `RC_FAR_RANGE` : FAR hors [0, 1] → FAIL
- `RC_FAR_NAN_WHEN_NO_SURPLUS` : FAR fini alors que surplus = 0 → FAIL
- `RC_IR_NEGATIVE` : IR negatif → FAIL
- `RC_CAPTURE_RANGE` : capture price PV hors [-200, 500] EUR/MWh → WARN
- `RC_TTL_LOW` : TTL < baseload - 20 EUR/MWh → WARN
- `RC_IR_GT_1` : IR > 1 (must-run depasse la charge en creux) → WARN
- `RC_LOW_REGIME_COHERENCE` : coherence regime < 0.55 → WARN
- `RC_TTL_LOW_SAMPLE` : TTL calcule sur moins de 500 heures C+D → WARN
- `RC_NEG_NOT_IN_AB` : moins de 50% des heures negatives en regime A/B → WARN
- `RC_D_NOT_ABOVE_C` : mediane prix regime D <= mediane prix regime C → WARN

**Quality flag** (decision globale par pays-annee) :
- `OK` : completude >= 0.98
- `WARN` : completude >= 0.90 mais < 0.98
- `FAIL` : completude < 0.90 ou invariants durs violes

Tous les constats sont traces dans `data/metrics/validation_findings.parquet` avec : severite, code, message, evidence quantitative, suggestion de correction.


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
```

### Protocole d'audit LLM
Source: `reports\chatgpt52_structured_FULL_20260211_191955_DE_ES\LLM_AUDIT_PROTOCOL.md`

```markdown
# LLM Audit Protocol (DE, ES) - FULL_20260211_191955

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
```

### Manifest
Source: `reports\chatgpt52_structured_FULL_20260211_191955_DE_ES\manifest.json`

```json
{
  "package_name": "chatgpt52_structured_FULL_20260211_191955_DE_ES",
  "run_id": "FULL_20260211_191955",
  "run_dir": "outputs\\combined\\FULL_20260211_191955",
  "countries_scope": [
    "DE",
    "ES"
  ],
  "generated_at_utc": "2026-02-11T19:36:06.587598+00:00",
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

## Inputs

### Hypothèses Phase 1
Source: `reports\chatgpt52_structured_FULL_20260211_191955_DE_ES\inputs\phase1_assumptions.csv`

```csv
param_group,param_name,param_value,unit,description,source,last_updated,owner
PHASE_THRESHOLDS,capture_ratio_pv_vs_ttl_crisis_max,0.7,ratio,Seuil crise capture ratio pv/ttl,default,2026-02-09,system
PHASE_THRESHOLDS,capture_ratio_pv_vs_ttl_stage2_max,0.8,ratio,Seuil capture ratio pv/ttl,default,2026-02-09,system
PHASE_THRESHOLDS,capture_ratio_pv_stage2_max,0.8,ratio,Seuil capture ratio PV vs baseload en declenchement phase2,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,capture_ratio_wind_stage2_max,0.9,ratio,Seuil capture ratio Wind vs baseload en declenchement phase2,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,days_spread_gt50_stage2_min,150.0,days,Seuil jours spread>50,default,2026-02-09,system
PHASE_THRESHOLDS,avg_daily_spread_crisis_min,50.0,EUR/MWh,Seuil spread journalier moyen pour tagger une annee de crise,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,h_below_5_stage2_min,500.0,hours,Seuil heures basses,default,2026-02-09,system
PHASE_THRESHOLDS,h_negative_stage2_min,200.0,hours,Seuil heures negatives stage2,default,2026-02-09,system
PHASE_THRESHOLDS,h_negative_stage2_strong,300.0,hours,Seuil fort heures negatives,default,2026-02-09,system
PHASE_THRESHOLDS,stage1_capture_ratio_pv_vs_ttl_min,0.9,ratio,Stage1 min capture ratio pv vs ttl,default,2026-02-10,system
PHASE_THRESHOLDS,stage1_capture_ratio_pv_min,0.85,ratio,Stage1 min capture ratio PV vs baseload,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,stage1_capture_ratio_wind_min,0.9,ratio,Stage1 min capture ratio Wind vs baseload,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,stage1_days_spread_gt50_max,120.0,days,Stage1 max days spread gt50,default,2026-02-10,system
PHASE_THRESHOLDS,stage1_h_below_5_max,500.0,hours,Stage1 max hours below 5 (doit rester sous seuil stage2),spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,stage1_h_negative_max,200.0,hours,Stage1 max negative hours (doit rester sous seuil stage2),spec_alignment,2026-02-11,codex
PHYSICS_THRESHOLDS,far_energy_tension_max,0.95,ratio,Seuil far tension,default,2026-02-09,system
PHYSICS_THRESHOLDS,far_stage2_min,0.95,ratio,Seuil FAR minimal pour eviter stress physique stage2,spec_alignment,2026-02-11,codex
PHYSICS_THRESHOLDS,ir_p10_high_min,1.5,ratio,Seuil inflexibilite haute stage2,spec_alignment,2026-02-11,codex
PHYSICS_THRESHOLDS,ir_p10_stage2_min,1.5,ratio,Alias seuil inflexibilite haute stage2,spec_alignment,2026-02-11,codex
PHYSICS_THRESHOLDS,sr_energy_material_min,0.01,ratio,Seuil surplus ratio materialite,default,2026-02-09,system
PHYSICS_THRESHOLDS,sr_hours_material_min,0.05,share,Seuil part d'heures de surplus materialite,default,2026-02-10,system
PHYSICS_THRESHOLDS,sr_hours_stage2_min,0.1,share,Seuil part d'heures de surplus pour stress physique stage2,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,stage1_sr_hours_max,0.05,share,Stage1 max part d'heures de surplus,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,stage1_far_min,0.95,ratio,Stage1 min FAR,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,stage1_ir_p10_max,1.5,ratio,Stage1 max IR P10,spec_alignment,2026-02-11,codex
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
Q3,h_negative_target,100.0,hours,Target max negative hours for phase3 inversion proxy,default,2026-02-10,system
Q3,h_below_5_target,300.0,hours,Target max hours below 5 EUR/MWh for phase3 inversion proxy,default,2026-02-10,system
Q3,slope_capture_target,0.0,ratio/year,Target minimum capture-ratio slope for phase3 trend status,default,2026-02-10,system
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
PHASE_THRESHOLDS,q1_persistence_window_years,2.0,years,Q1: nombre d'annees consecutives requises pour valider une bascule,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,q1_lever_max_uplift,1.0,ratio,Q1: borne max d'uplift pour solveurs required_demand/flex,spec_alignment,2026-02-11,codex
Q3,stage2_recent_h_negative_min_scen,80.0,h/an,Q3 SCEN: seuil h_negative recent pour qualifier un contexte Stage2 en prospectif.,codex_adjustment,2026-02-10,codex
Q3,stage2_recent_sr_energy_min_scen,0.02,ratio,Q3 SCEN: seuil SR recent pour qualifier un contexte Stage2 meme si h_negative reste faible.,codex_adjustment,2026-02-10,codex
```

### Hypothèses Phase 2 (DE/ES)
Source: `reports\chatgpt52_structured_FULL_20260211_191955_DE_ES\inputs\phase2_scenario_country_year.csv`

```csv
scenario_id,country,year,demand_total_twh,demand_peak_gw,demand_shape_reference,cap_pv_gw,cap_wind_on_gw,cap_wind_off_gw,cap_must_run_nuclear_gw,cap_must_run_chp_gw,cap_must_run_biomass_gw,cap_must_run_hydro_ror_gw,must_run_min_output_factor,interconnection_export_gw,export_coincidence_factor,psh_pump_gw,bess_power_gw,bess_energy_gwh,bess_eta_roundtrip,co2_eur_per_t,gas_eur_per_mwh_th,marginal_tech,marginal_efficiency,marginal_emission_factor_t_per_mwh,supported_vre_share,negative_price_rule,negative_price_rule_threshold_hours,price_exposure_share,source_label,notes
BASE,DE,2025,480.1727000000001,53.353,historical_mean_2018_2024,19.466700000000003,36.46300000000001,5.3717500000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2026,489.3188400000001,54.36919999999999,historical_mean_2018_2024,19.80526,36.85368,5.46942,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2027,498.4649800000001,55.3854,historical_mean_2018_2024,20.14382,37.24436,5.56709,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2028,507.61112,56.4016,historical_mean_2018_2024,20.482380000000003,37.63504,5.66476,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2029,516.7572600000001,57.4178,historical_mean_2018_2024,20.82094,38.02572000000001,5.76243,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,DE,2031,535.04954,59.4502,historical_mean_2018_2024,21.49806,38.80708,5.95777,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2032,544.19568,60.4664,historical_mean_2018_2024,21.83662,39.19776,6.05544,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2033,553.34182,61.4826,historical_mean_2018_2024,22.17518,39.588440000000006,6.15311,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2034,562.48796,62.4988,historical_mean_2018_2024,22.51374,39.97912,6.25078,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2035,571.6341,63.515,historical_mean_2018_2024,22.8523,40.3698,6.34845,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2036,580.7802399999999,64.5312,historical_mean_2018_2024,23.19086,40.76048,6.4461200000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2037,589.92638,65.5474,historical_mean_2018_2024,23.52942,41.15116,6.54379,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2038,599.0725199999999,66.56360000000001,historical_mean_2018_2024,23.867980000000003,41.54184,6.64146,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2039,608.21866,67.5798,historical_mean_2018_2024,24.20654,41.93252,6.73913,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,ES,2025,234.2802,26.030500000000004,historical_mean_2018_2024,12.5165,13.37405,1.9703,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2026,238.74268,26.5264,historical_mean_2018_2024,12.73418,13.51734,2.00612,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2027,243.20516,27.0223,historical_mean_2018_2024,12.95186,13.66063,2.04194,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2028,247.66764,27.5182,historical_mean_2018_2024,13.16954,13.80392,2.07776,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2029,252.13012,28.014100000000003,historical_mean_2018_2024,13.38722,13.94721,2.11358,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,ES,2031,261.05508,29.0059,historical_mean_2018_2024,13.82258,14.23379,2.18522,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2032,265.51756,29.501800000000003,historical_mean_2018_2024,14.04026,14.37708,2.22104,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2033,269.98004000000003,29.9977,historical_mean_2018_2024,14.25794,14.52037,2.25686,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2034,274.44252,30.4936,historical_mean_2018_2024,14.47562,14.66366,2.29268,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2035,278.905,30.9895,historical_mean_2018_2024,14.6933,14.80695,2.3285,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2036,283.36748,31.4854,historical_mean_2018_2024,14.91098,14.95024,2.36432,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2037,287.82996,31.9813,historical_mean_2018_2024,15.12866,15.09353,2.40014,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2038,292.29244,32.4772,historical_mean_2018_2024,15.34634,15.23682,2.43596,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2039,296.75492,32.9731,historical_mean_2018_2024,15.56402,15.38011,2.47178,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,DE,2025,528.1899,58.6875,historical_mean_2018_2024,19.466700000000003,36.46300000000001,5.3717500000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2026,538.2506599999999,59.8054,historical_mean_2018_2024,19.80526,36.85368,5.46942,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2027,548.31142,60.9233,historical_mean_2018_2024,20.14382,37.24436,5.56709,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2028,558.37218,62.0412,historical_mean_2018_2024,20.482380000000003,37.63504,5.66476,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2029,568.43294,63.1591,historical_mean_2018_2024,20.82094,38.02572000000001,5.76243,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2030,578.4937,64.277,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,DE,2031,588.55446,65.3949,historical_mean_2018_2024,21.49806,38.80708,5.95777,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2032,598.61522,66.5128,historical_mean_2018_2024,21.83662,39.19776,6.05544,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2033,608.67598,67.6307,historical_mean_2018_2024,22.17518,39.588440000000006,6.15311,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2034,618.73674,68.7486,historical_mean_2018_2024,22.51374,39.97912,6.25078,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2035,628.7975,69.8665,historical_mean_2018_2024,22.8523,40.3698,6.34845,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2036,638.85826,70.98440000000001,historical_mean_2018_2024,23.19086,40.76048,6.4461200000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2037,648.91902,72.1023,historical_mean_2018_2024,23.52942,41.15116,6.54379,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2038,658.97978,73.2202,historical_mean_2018_2024,23.867980000000003,41.54184,6.64146,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2039,669.0405400000001,74.3381,historical_mean_2018_2024,24.20654,41.93252,6.73913,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2040,679.1013,75.456,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,ES,2025,257.70815000000005,28.634,historical_mean_2018_2024,12.5165,13.37405,1.9703,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2026,262.61688000000004,29.1794,historical_mean_2018_2024,12.73418,13.51734,2.00612,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2027,267.52561000000003,29.7248,historical_mean_2018_2024,12.95186,13.66063,2.04194,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2028,272.43434,30.270200000000003,historical_mean_2018_2024,13.16954,13.80392,2.07776,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2029,277.34307,30.8156,historical_mean_2018_2024,13.38722,13.94721,2.11358,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2030,282.2518,31.361,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,ES,2031,287.16053,31.9064,historical_mean_2018_2024,13.82258,14.23379,2.18522,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2032,292.06926,32.4518,historical_mean_2018_2024,14.04026,14.37708,2.22104,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2033,296.97799,32.9972,historical_mean_2018_2024,14.25794,14.52037,2.25686,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2034,301.88672,33.5426,historical_mean_2018_2024,14.47562,14.66366,2.29268,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2035,306.79545,34.088,historical_mean_2018_2024,14.6933,14.80695,2.3285,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2036,311.70418,34.6334,historical_mean_2018_2024,14.91098,14.95024,2.36432,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2037,316.61291,35.178799999999995,historical_mean_2018_2024,15.12866,15.09353,2.40014,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2038,321.52164,35.7242,historical_mean_2018_2024,15.34634,15.23682,2.43596,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2039,326.43037,36.2696,historical_mean_2018_2024,15.56402,15.38011,2.47178,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2040,331.3391,36.815,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
FLEX_UP,DE,2025,480.1727000000001,53.353,historical_mean_2018_2024,19.466700000000003,36.46300000000001,5.3717500000000005,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,0.9,1.0,0.88,80.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2026,489.3188400000001,54.36919999999999,historical_mean_2018_2024,19.80526,36.85368,5.46942,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.08,2.0,0.88,82.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2027,498.4649800000001,55.3854,historical_mean_2018_2024,20.14382,37.24436,5.56709,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.26,3.0,0.88,84.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2028,507.61112,56.4016,historical_mean_2018_2024,20.482380000000003,37.63504,5.66476,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.44,4.0,0.88,86.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2029,516.7572600000001,57.4178,historical_mean_2018_2024,20.82094,38.02572000000001,5.76243,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.62,5.0,0.88,88.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.8,6.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
FLEX_UP,DE,2031,535.04954,59.4502,historical_mean_2018_2024,21.49806,38.80708,5.95777,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.98,7.0,0.88,92.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2032,544.19568,60.4664,historical_mean_2018_2024,21.83662,39.19776,6.05544,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,2.16,8.0,0.88,94.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2033,553.34182,61.4826,historical_mean_2018_2024,22.17518,39.588440000000006,6.15311,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,2.34,9.0,0.88,96.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2034,562.48796,62.4988,historical_mean_2018_2024,22.51374,39.97912,6.25078,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,2.52,10.0,0.88,98.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2035,571.6341,63.515,historical_mean_2018_2024,22.8523,40.3698,6.34845,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,2.7,11.0,0.88,100.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2036,580.7802399999999,64.5312,historical_mean_2018_2024,23.19086,40.76048,6.4461200000000005,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,2.88,12.0,0.88,102.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2037,589.92638,65.5474,historical_mean_2018_2024,23.52942,41.15116,6.54379,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,3.06,13.0,0.88,104.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2038,599.0725199999999,66.56360000000001,historical_mean_2018_2024,23.867980000000003,41.54184,6.64146,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,3.24,14.0,0.88,106.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2039,608.21866,67.5798,historical_mean_2018_2024,24.20654,41.93252,6.73913,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,3.42,15.0,0.88,108.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,3.6,16.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
FLEX_UP,ES,2025,234.2802,26.030500000000004,historical_mean_2018_2024,12.5165,13.37405,1.9703,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,0.9,1.0,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2026,238.74268,26.5264,historical_mean_2018_2024,12.73418,13.51734,2.00612,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.08,2.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2027,243.20516,27.0223,historical_mean_2018_2024,12.95186,13.66063,2.04194,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.26,3.0,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2028,247.66764,27.5182,historical_mean_2018_2024,13.16954,13.80392,2.07776,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.44,4.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2029,252.13012,28.014100000000003,historical_mean_2018_2024,13.38722,13.94721,2.11358,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.62,5.0,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.8,6.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
FLEX_UP,ES,2031,261.05508,29.0059,historical_mean_2018_2024,13.82258,14.23379,2.18522,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,1.98,7.0,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2032,265.51756,29.501800000000003,historical_mean_2018_2024,14.04026,14.37708,2.22104,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,2.16,8.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2033,269.98004000000003,29.9977,historical_mean_2018_2024,14.25794,14.52037,2.25686,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,2.34,9.0,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2034,274.44252,30.4936,historical_mean_2018_2024,14.47562,14.66366,2.29268,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,2.52,10.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2035,278.905,30.9895,historical_mean_2018_2024,14.6933,14.80695,2.3285,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,2.7,11.0,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2036,283.36748,31.4854,historical_mean_2018_2024,14.91098,14.95024,2.36432,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,2.88,12.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2037,287.82996,31.9813,historical_mean_2018_2024,15.12866,15.09353,2.40014,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,3.06,13.0,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2038,292.29244,32.4772,historical_mean_2018_2024,15.34634,15.23682,2.43596,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,3.24,14.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2039,296.75492,32.9731,historical_mean_2018_2024,15.56402,15.38011,2.47178,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,3.42,15.0,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
FLEX_UP,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.75,0.35,1.3,3.6,16.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,DE,2025,480.1727000000001,53.353,historical_mean_2018_2024,19.466700000000003,36.46300000000001,5.3717500000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,120.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2026,489.3188400000001,54.36919999999999,historical_mean_2018_2024,19.80526,36.85368,5.46942,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,123.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2027,498.4649800000001,55.3854,historical_mean_2018_2024,20.14382,37.24436,5.56709,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,126.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2028,507.61112,56.4016,historical_mean_2018_2024,20.482380000000003,37.63504,5.66476,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,129.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2029,516.7572600000001,57.4178,historical_mean_2018_2024,20.82094,38.02572000000001,5.76243,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,132.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,135.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,DE,2031,535.04954,59.4502,historical_mean_2018_2024,21.49806,38.80708,5.95777,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,138.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2032,544.19568,60.4664,historical_mean_2018_2024,21.83662,39.19776,6.05544,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,141.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2033,553.34182,61.4826,historical_mean_2018_2024,22.17518,39.588440000000006,6.15311,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,144.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2034,562.48796,62.4988,historical_mean_2018_2024,22.51374,39.97912,6.25078,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,147.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2035,571.6341,63.515,historical_mean_2018_2024,22.8523,40.3698,6.34845,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,150.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2036,580.7802399999999,64.5312,historical_mean_2018_2024,23.19086,40.76048,6.4461200000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,153.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2037,589.92638,65.5474,historical_mean_2018_2024,23.52942,41.15116,6.54379,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,156.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2038,599.0725199999999,66.56360000000001,historical_mean_2018_2024,23.867980000000003,41.54184,6.64146,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,159.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2039,608.21866,67.5798,historical_mean_2018_2024,24.20654,41.93252,6.73913,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,162.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,165.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,ES,2025,234.2802,26.030500000000004,historical_mean_2018_2024,12.5165,13.37405,1.9703,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,120.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2026,238.74268,26.5264,historical_mean_2018_2024,12.73418,13.51734,2.00612,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,123.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2027,243.20516,27.0223,historical_mean_2018_2024,12.95186,13.66063,2.04194,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,126.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2028,247.66764,27.5182,historical_mean_2018_2024,13.16954,13.80392,2.07776,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,129.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2029,252.13012,28.014100000000003,historical_mean_2018_2024,13.38722,13.94721,2.11358,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,132.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,135.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,ES,2031,261.05508,29.0059,historical_mean_2018_2024,13.82258,14.23379,2.18522,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,138.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2032,265.51756,29.501800000000003,historical_mean_2018_2024,14.04026,14.37708,2.22104,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,141.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2033,269.98004000000003,29.9977,historical_mean_2018_2024,14.25794,14.52037,2.25686,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,144.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2034,274.44252,30.4936,historical_mean_2018_2024,14.47562,14.66366,2.29268,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,147.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2035,278.905,30.9895,historical_mean_2018_2024,14.6933,14.80695,2.3285,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,150.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2036,283.36748,31.4854,historical_mean_2018_2024,14.91098,14.95024,2.36432,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,153.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2037,287.82996,31.9813,historical_mean_2018_2024,15.12866,15.09353,2.40014,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,156.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2038,292.29244,32.4772,historical_mean_2018_2024,15.34634,15.23682,2.43596,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,159.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2039,296.75492,32.9731,historical_mean_2018_2024,15.56402,15.38011,2.47178,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,162.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,165.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,DE,2025,480.1727000000001,53.353,historical_mean_2018_2024,19.466700000000003,36.46300000000001,5.3717500000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,58.5,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2026,489.3188400000001,54.36919999999999,historical_mean_2018_2024,19.80526,36.85368,5.46942,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,59.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2027,498.4649800000001,55.3854,historical_mean_2018_2024,20.14382,37.24436,5.56709,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,60.3,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2028,507.61112,56.4016,historical_mean_2018_2024,20.482380000000003,37.63504,5.66476,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,61.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2029,516.7572600000001,57.4178,historical_mean_2018_2024,20.82094,38.02572000000001,5.76243,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,62.1,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,63.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,DE,2031,535.04954,59.4502,historical_mean_2018_2024,21.49806,38.80708,5.95777,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,63.9,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2032,544.19568,60.4664,historical_mean_2018_2024,21.83662,39.19776,6.05544,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,64.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2033,553.34182,61.4826,historical_mean_2018_2024,22.17518,39.588440000000006,6.15311,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,65.7,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2034,562.48796,62.4988,historical_mean_2018_2024,22.51374,39.97912,6.25078,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,66.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2035,571.6341,63.515,historical_mean_2018_2024,22.8523,40.3698,6.34845,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,67.5,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2036,580.7802399999999,64.5312,historical_mean_2018_2024,23.19086,40.76048,6.4461200000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,68.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2037,589.92638,65.5474,historical_mean_2018_2024,23.52942,41.15116,6.54379,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,69.3,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2038,599.0725199999999,66.56360000000001,historical_mean_2018_2024,23.867980000000003,41.54184,6.64146,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,70.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2039,608.21866,67.5798,historical_mean_2018_2024,24.20654,41.93252,6.73913,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,71.1,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,72.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,ES,2025,234.2802,26.030500000000004,historical_mean_2018_2024,12.5165,13.37405,1.9703,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,58.5,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2026,238.74268,26.5264,historical_mean_2018_2024,12.73418,13.51734,2.00612,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,59.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2027,243.20516,27.0223,historical_mean_2018_2024,12.95186,13.66063,2.04194,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,60.3,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2028,247.66764,27.5182,historical_mean_2018_2024,13.16954,13.80392,2.07776,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,61.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2029,252.13012,28.014100000000003,historical_mean_2018_2024,13.38722,13.94721,2.11358,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,62.1,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,63.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,ES,2031,261.05508,29.0059,historical_mean_2018_2024,13.82258,14.23379,2.18522,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,63.9,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2032,265.51756,29.501800000000003,historical_mean_2018_2024,14.04026,14.37708,2.22104,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,64.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2033,269.98004000000003,29.9977,historical_mean_2018_2024,14.25794,14.52037,2.25686,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,65.7,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2034,274.44252,30.4936,historical_mean_2018_2024,14.47562,14.66366,2.29268,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,66.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2035,278.905,30.9895,historical_mean_2018_2024,14.6933,14.80695,2.3285,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,67.5,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2036,283.36748,31.4854,historical_mean_2018_2024,14.91098,14.95024,2.36432,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,68.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2037,287.82996,31.9813,historical_mean_2018_2024,15.12866,15.09353,2.40014,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,69.3,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2038,292.29244,32.4772,historical_mean_2018_2024,15.34634,15.23682,2.43596,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,70.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2039,296.75492,32.9731,historical_mean_2018_2024,15.56402,15.38011,2.47178,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,71.1,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,72.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,DE,2025,480.1727000000001,53.353,historical_mean_2018_2024,19.466700000000003,36.46300000000001,5.3717500000000005,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2026,489.3188400000001,54.36919999999999,historical_mean_2018_2024,19.80526,36.85368,5.46942,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2027,498.4649800000001,55.3854,historical_mean_2018_2024,20.14382,37.24436,5.56709,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2028,507.61112,56.4016,historical_mean_2018_2024,20.482380000000003,37.63504,5.66476,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2029,516.7572600000001,57.4178,historical_mean_2018_2024,20.82094,38.02572000000001,5.76243,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,DE,2031,535.04954,59.4502,historical_mean_2018_2024,21.49806,38.80708,5.95777,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2032,544.19568,60.4664,historical_mean_2018_2024,21.83662,39.19776,6.05544,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2033,553.34182,61.4826,historical_mean_2018_2024,22.17518,39.588440000000006,6.15311,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2034,562.48796,62.4988,historical_mean_2018_2024,22.51374,39.97912,6.25078,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2035,571.6341,63.515,historical_mean_2018_2024,22.8523,40.3698,6.34845,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2036,580.7802399999999,64.5312,historical_mean_2018_2024,23.19086,40.76048,6.4461200000000005,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2037,589.92638,65.5474,historical_mean_2018_2024,23.52942,41.15116,6.54379,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2038,599.0725199999999,66.56360000000001,historical_mean_2018_2024,23.867980000000003,41.54184,6.64146,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2039,608.21866,67.5798,historical_mean_2018_2024,24.20654,41.93252,6.73913,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,ES,2025,234.2802,26.030500000000004,historical_mean_2018_2024,12.5165,13.37405,1.9703,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2026,238.74268,26.5264,historical_mean_2018_2024,12.73418,13.51734,2.00612,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2027,243.20516,27.0223,historical_mean_2018_2024,12.95186,13.66063,2.04194,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2028,247.66764,27.5182,historical_mean_2018_2024,13.16954,13.80392,2.07776,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2029,252.13012,28.014100000000003,historical_mean_2018_2024,13.38722,13.94721,2.11358,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,ES,2031,261.05508,29.0059,historical_mean_2018_2024,13.82258,14.23379,2.18522,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2032,265.51756,29.501800000000003,historical_mean_2018_2024,14.04026,14.37708,2.22104,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2033,269.98004000000003,29.9977,historical_mean_2018_2024,14.25794,14.52037,2.25686,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2034,274.44252,30.4936,historical_mean_2018_2024,14.47562,14.66366,2.29268,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2035,278.905,30.9895,historical_mean_2018_2024,14.6933,14.80695,2.3285,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2036,283.36748,31.4854,historical_mean_2018_2024,14.91098,14.95024,2.36432,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2037,287.82996,31.9813,historical_mean_2018_2024,15.12866,15.09353,2.40014,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2038,292.29244,32.4772,historical_mean_2018_2024,15.34634,15.23682,2.43596,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2039,296.75492,32.9731,historical_mean_2018_2024,15.56402,15.38011,2.47178,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
```
