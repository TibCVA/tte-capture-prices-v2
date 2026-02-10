# Compliance Evidence Index

- Run ID: `20260210_133946`
- Matrix: `C:\Users\cval-tlacour\OneDrive - CVA corporate value associate GmbH\Desktop\automation-stack\projects\tte-capture-prices-v2\reports\compliance_matrix_full.csv`
- Slides: `C:\Users\cval-tlacour\OneDrive - CVA corporate value associate GmbH\Desktop\automation-stack\projects\tte-capture-prices-v2\reports\slides_coverage_detailed.csv`
- Pytest: `PASS` -> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
- Q4 perf: cold=0.586s warm=0.014s cold_cache=False warm_cache=True

## SPEC_0
- Counts: OK=15 PARTIEL=0 MANQUANT=0

- `S0-001` [OK] (critical) :: Index interne UTC timezone-aware et granularite horaire. -> `src/time_utils.py:22`
- `S0-002` [OK] (high) :: Pas de temps unique 1H. -> `src/time_utils.py:25`
- `S0-003` [OK] (critical) :: Classification regime A/B/C/D sans variable prix. -> `src/processing.py:108`
- `S0-004` [OK] (critical) :: NRL = load - VRE - must-run. -> `src/processing.py:227`
- `S0-005` [OK] (critical) :: Surplus = max(0, -NRL). -> `src/processing.py:228`
- `S0-006` [OK] (critical) :: Surplus non absorbe borne et non negatif. -> `src/processing.py:239`
- `S0-007` [OK] (critical) :: Cle ENTSOE lue via variable environnement/.env, jamais hardcodee. -> `src/data_fetcher.py:54`
- `S0-008` [OK] (high) :: Run context (run_id hash + snapshot config) disponible en utilitaire. -> `src/pipeline.py:14`
- `S0-009` [OK] (critical) :: Run trail complet outputs/runs/<run_id>/run_config_snapshot.json + data_manifest.csv dans flux principal. -> `outputs/runs/*/{run_config_snapshot.json,data_manifest.csv}`
- `S0-010` [OK] (high) :: FAR = NaN si surplus nul. -> `src/metrics.py:151`
- `S0-011` [OK] (high) :: IR base sur P10(must-run)/P10(load). -> `src/metrics.py:155`
- `S0-012` [OK] (high) :: TTL calcule en Q95 sur regimes C/D. -> `src/metrics.py:134`
- `S0-013` [OK] (critical) :: Batterie de tests unitaires/integration/reality executee. -> `python -m pytest -q :: -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html`
- `S0-014` [OK] (medium) :: Explicabilite KPI complete (definition + formule + intuition + limites + dependances) partout. -> `app/ui_components.py:75`
- `S0-015` [OK] (high) :: Separation explicite mode HIST vs SCEN dans pages Q1..Q5. -> `app/pages/01_Q1_Phase1_to_Phase2.py`

## SPEC_1
- Counts: OK=22 PARTIEL=0 MANQUANT=0

- `S1-001` [OK] (critical) :: Cache freeze-first ENTSOE present (prices/load/generation/net_position/psh). -> `data/raw/entsoe/*/{country}/{year}.parquet`
- `S1-002` [OK] (high) :: Metadonnees .meta.json par dataset/pays/annee. -> `data/raw/entsoe/*/{country}/{year}.meta.json`
- `S1-003` [OK] (critical) :: Schema horaire canonique present. -> `data/processed/hourly/FR/2024.parquet`
- `S1-004` [OK] (high) :: Alias obligatoires canonique + alias exposes. -> `data/processed/hourly/FR/2024.parquet`
- `S1-005` [OK] (high) :: Regle load/pompage (minus_psh_pump vs includes_pumping) implementee. -> `src/processing.py:213`
- `S1-006` [OK] (high) :: Must-run configurable par pays via config/countries.yaml. -> `src/processing.py:86`
- `S1-007` [OK] (critical) :: Regimes A/B/C/D conformes et testables. -> `src/processing.py:111`
- `S1-008` [OK] (critical) :: Table annuelle consolidee disponible. -> `data/metrics/annual_metrics.parquet`
- `S1-009` [OK] (high) :: Table journaliere disponible. -> `data/metrics/daily_metrics.parquet`
- `S1-010` [OK] (critical) :: Validation findings hard+reality disponibles. -> `data/metrics/validation_findings.parquet`
- `S1-011` [OK] (critical) :: KPIs annuels de base presents (SR/FAR/IR/TTL/capture/prix stress/quality). -> `data/metrics/annual_metrics.parquet`
- `S1-012` [OK] (high) :: Tests socle imposes presents. -> `tests/test_time_normalization.py; tests/test_physical_formulas.py; tests/test_schema_stability.py`
- `S1-013` [OK] (medium) :: Page Donnees & Qualite disponible. -> `app/pages/00_Donnees_Qualite.py:119`
- `S1-014` [OK] (medium) :: Page Socle Physique disponible. -> `app/pages/00_Socle_Physique.py:21`
- `S1-015` [OK] (critical) :: Execution historique complete 7 pays x 2018-2024. -> `hourly files: 49/49`
- `S1-016` [OK] (critical) :: Panel annuel complet pour fenetre historique verrouillee. -> `data/metrics/annual_metrics.parquet rows for 7x2018-2024`
- `S1-017` [OK] (critical) :: Jeux TYNDP 2024 raw+normalized integres. -> `data/external/raw/tyndp2024/* ; data/external/normalized/tyndp2024_*.csv`
- `S1-018` [OK] (high) :: Benchmarks NREL ATB integres. -> `data/external/raw/nrel_atb/* ; data/external/normalized/tech_cost_benchmarks_atb.csv`
- `S1-019` [OK] (high) :: Benchmark IRENA integre. -> `data/external/raw/irena/IRENAInsights_RPGC2023.pdf ; data/external/normalized/tech_cost_benchmarks_irena.csv`
- `S1-020` [OK] (high) :: Table policy distortion versionnee presente. -> `assumptions/policy_distortion.csv`
- `S1-021` [OK] (medium) :: Proxy interconnexions phase1 present. -> `data/external/normalized/interconnection_proxy_phase1.csv`
- `S1-022` [OK] (medium) :: Matrice coincidence surplus phase1 presente. -> `data/external/normalized/surplus_coincidence_matrix_phase1.csv`

## SPEC_2
- Counts: OK=22 PARTIEL=0 MANQUANT=0

- `S2-001` [OK] (critical) :: Contrat ModuleResult present avec champs standard. -> `src/modules/result.py:13`
- `S2-002` [OK] (high) :: Exports pack standard phase1/phase2. -> `src/modules/result.py:45`
- `S2-003` [OK] (critical) :: 5 modules Q1..Q5 presentes. -> `src/modules/q1_transition.py; src/modules/q2_slope.py; src/modules/q3_exit.py; src/modules/q4_bess.py; src/modules/q5_thermal_anchor.py`
- `S2-004` [OK] (critical) :: 5 pages Streamlit Q1..Q5 presentes. -> `app/pages/01_Q1...py .. 05_Q5...py`
- `S2-005` [OK] (high) :: Sections fixes obligatoires sur pages Q1..Q5. -> `tests/test_ui_pages_contract.py`
- `S2-006` [OK] (high) :: Calculs lourds declenches via form submit. -> `tests/test_ui_pages_contract.py::test_q_pages_use_form_submit_for_heavy_runs`
- `S2-007` [OK] (high) :: Blocage conclusions si quality_flag=FAIL (Q1). -> `app/pages/01_Q1_Phase1_to_Phase2.py`
- `S2-008` [OK] (high) :: Blocage conclusions si quality_flag=FAIL (Q2). -> `app/pages/02_Q2_Phase2_Slope.py`
- `S2-009` [OK] (high) :: Blocage conclusions si quality_flag=FAIL (Q3). -> `app/pages/03_Q3_Exit_Phase2.py`
- `S2-010` [OK] (high) :: Blocage conclusions si quality_flag=FAIL (Q4). -> `app/pages/04_Q4_BESS_OrderOfMagnitude.py`
- `S2-011` [OK] (high) :: Blocage conclusions si quality_flag=FAIL (Q5). -> `app/pages/05_Q5_CO2_Gas_Anchor.py`
- `S2-012` [OK] (high) :: Q1 score marche + stress physique + annee de bascule. -> `src/modules/q1_transition.py:78`
- `S2-013` [OK] (high) :: Q2 pente OLS + robustesse n>=3 + ranking drivers. -> `src/modules/q2_slope.py:10`
- `S2-014` [OK] (high) :: Q3 tendances + contre-factuels demande/must-run/flex. -> `src/modules/q3_exit.py:26`
- `S2-015` [OK] (critical) :: Q4 dispatch BESS 3 modes (SURPLUS_FIRST/ARBITRAGE/PV_COLOCATED). -> `src/modules/q4_bess.py:105`
- `S2-016` [OK] (high) :: Q5 TCA/TTL + sensibilites + CO2 requis. -> `src/modules/q5_thermal_anchor.py:55`
- `S2-017` [OK] (critical) :: Table hypotheses Phase2 scenario x pays x annee. -> `data/assumptions/phase2/phase2_scenario_country_year.csv`
- `S2-018` [OK] (critical) :: Moteur scenario phase2 implemente. -> `src/scenario/phase2_engine.py:348`
- `S2-019` [OK] (critical) :: Couverture scenario complete sur scenarios x 7 pays x 2030/2040. -> `scenario hourly files: 84/84`
- `S2-020` [OK] (high) :: Execution scenario minimum 2 scenarios x 3 pays x 2 horizons. -> `data/processed/scenario/*/annual_metrics.parquet`
- `S2-021` [OK] (high) :: Suite tests modules Q1..Q5 + integration. -> `tests/test_q1_transition.py; test_q2_slope.py; test_q3_exit.py; test_q4_bess.py; test_q5_thermal_anchor.py; test_phase1_modules_integration.py`
- `S2-022` [OK] (high) :: Tests moteur scenario et validations hypotheses Phase2. -> `tests/test_phase2_engine.py; tests/test_phase2_validators.py`

## V2.1
- Counts: OK=10 PARTIEL=0 MANQUANT=0

- `V21-001` [OK] (high) :: Cache streamlit applique sur chargements lourds. -> `app/page_utils.py:29`
- `V21-002` [OK] (high) :: Forms submit pour eviter reruns lourds. -> `app/page_utils.py:65`
- `V21-003` [OK] (critical) :: Cache persistant Q4 par hash hypotheses/grille/mode. -> `src/modules/q4_bess.py:26`
- `V21-004` [OK] (high) :: Diagnostics Q4: compute_time_sec/cache_hit/engine_version. -> `src/modules/q4_bess.py:359`
- `V21-005` [OK] (high) :: SLO Q4 cold <35s. -> `Q4 cold wall=0.586s`
- `V21-006` [OK] (high) :: SLO Q4 warm <3s. -> `Q4 warm wall=0.014s`
- `V21-007` [OK] (high) :: Cache hit/miss verifiable entre run1 et run2. -> `cold_cache_hit=False warm_cache_hit=True`
- `V21-008` [OK] (medium) :: Navigation guidee accueil->mode emploi->donnees->socle->Q1..Q5->conclusions. -> `streamlit_app.py:10`
- `V21-009` [OK] (medium) :: Header etape actuelle/etape suivante sur pages. -> `app/ui_components.py:55`
- `V21-010` [OK] (medium) :: UX neophyte completement didactique et non-obscurci sur toutes pages. -> `app/ui_components.py:75`

## REPORTING
- Counts: OK=2 PARTIEL=0 MANQUANT=0

- `REP-001` [OK] (high) :: Rapport final detaille present en markdown versionne. -> `reports/conclusions_v2_detailed_*.md`
- `REP-002` [OK] (high) :: Page Conclusions charge rapport et resume executif. -> `app/pages/99_Conclusions.py`

## SLIDES
- Counts: OK=33 PARTIEL=0 MANQUANT=0

- `SLIDE-01` [OK] (medium) :: Couverture explicite slide 1. -> `app/pages/00_Accueil.py`
- `SLIDE-02` [OK] (medium) :: Couverture explicite slide 2. -> `src/modules/q1_transition.py:66`
- `SLIDE-03` [OK] (medium) :: Couverture explicite slide 3. -> `src/modules/q1_transition.py:66`
- `SLIDE-04` [OK] (medium) :: Couverture explicite slide 4. -> `src/modules/q1_transition.py:66`
- `SLIDE-05` [OK] (medium) :: Couverture explicite slide 5. -> `src/modules/q1_transition.py:66`
- `SLIDE-06` [OK] (medium) :: Couverture explicite slide 6. -> `src/modules/q1_transition.py:66`
- `SLIDE-07` [OK] (medium) :: Couverture explicite slide 7. -> `src/modules/q1_transition.py:66`
- `SLIDE-08` [OK] (medium) :: Couverture explicite slide 8. -> `src/modules/q2_slope.py:58`
- `SLIDE-09` [OK] (medium) :: Couverture explicite slide 9. -> `src/modules/q2_slope.py:58`
- `SLIDE-10` [OK] (medium) :: Couverture explicite slide 10. -> `src/modules/q2_slope.py:58`
- `SLIDE-11` [OK] (medium) :: Couverture explicite slide 11. -> `src/modules/q2_slope.py:58`
- `SLIDE-12` [OK] (medium) :: Couverture explicite slide 12. -> `src/modules/q2_slope.py:58`
- `SLIDE-13` [OK] (medium) :: Couverture explicite slide 13. -> `src/modules/q2_slope.py:58`
- `SLIDE-14` [OK] (medium) :: Couverture explicite slide 14. -> `src/modules/q3_exit.py:44`
- `SLIDE-15` [OK] (medium) :: Couverture explicite slide 15. -> `src/modules/q3_exit.py:44`
- `SLIDE-16` [OK] (medium) :: Couverture explicite slide 16. -> `src/modules/q3_exit.py:44`
- `SLIDE-17` [OK] (medium) :: Couverture explicite slide 17. -> `src/modules/q3_exit.py:44`
- `SLIDE-18` [OK] (medium) :: Couverture explicite slide 18. -> `src/modules/q3_exit.py:44`
- `SLIDE-19` [OK] (medium) :: Couverture explicite slide 19. -> `src/modules/q3_exit.py:44`
- `SLIDE-20` [OK] (medium) :: Couverture explicite slide 20. -> `src/modules/q4_bess.py:304`
- `SLIDE-21` [OK] (medium) :: Couverture explicite slide 21. -> `src/modules/q4_bess.py:304`
- `SLIDE-22` [OK] (medium) :: Couverture explicite slide 22. -> `src/modules/q4_bess.py:304`
- `SLIDE-23` [OK] (medium) :: Couverture explicite slide 23. -> `src/modules/q4_bess.py:304`
- `SLIDE-24` [OK] (medium) :: Couverture explicite slide 24. -> `src/modules/q4_bess.py:304`
- `SLIDE-25` [OK] (medium) :: Couverture explicite slide 25. -> `src/modules/q4_bess.py:304`
- `SLIDE-26` [OK] (medium) :: Couverture explicite slide 26. -> `src/modules/q5_thermal_anchor.py:66`
- `SLIDE-27` [OK] (medium) :: Couverture explicite slide 27. -> `src/modules/q5_thermal_anchor.py:66`
- `SLIDE-28` [OK] (medium) :: Couverture explicite slide 28. -> `src/modules/q5_thermal_anchor.py:66`
- `SLIDE-29` [OK] (medium) :: Couverture explicite slide 29. -> `src/modules/q5_thermal_anchor.py:66`
- `SLIDE-30` [OK] (medium) :: Couverture explicite slide 30. -> `src/modules/q5_thermal_anchor.py:66`
- `SLIDE-31` [OK] (medium) :: Couverture explicite slide 31. -> `src/modules/q5_thermal_anchor.py:66`
- `SLIDE-32` [OK] (medium) :: Couverture explicite slide 32. -> `streamlit_app.py:10`
- `SLIDE-33` [OK] (low) :: Couverture explicite slide 33. -> `config/countries.yaml:1`
