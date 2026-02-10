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
