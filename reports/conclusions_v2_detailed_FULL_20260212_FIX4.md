# Rapport Final V2.3 - Run `FULL_20260212_FIX4`

## 1. Page de garde
- Date de generation: `2026-02-12 01:51:10 UTC`
- Run combine source: `outputs\combined\FULL_20260212_FIX4`
- Perimetre pays declare: `non renseigne`
- Fenetre historique de reference: `2018-2024`
- Horizons prospectifs de reference: `2030/2040`
- Questions couvertes: `Q1, Q2, Q3, Q4, Q5`
- Avertissement methodologique: cette analyse est empirique et scenarisee; ce n'est pas un modele d'equilibre complet.

### Scenarios executes par question
- `Q1`: DEMAND_UP, LOW_RIGIDITY
- `Q2`: HIGH_CO2, HIGH_GAS
- `Q3`: DEMAND_UP, LOW_RIGIDITY
- `Q4`: HIGH_CO2, HIGH_GAS
- `Q5`: HIGH_BOTH, HIGH_CO2, HIGH_GAS

## 2. Methode et gouvernance

### 2.1 Conventions SPEC 0
- Index horaire UTC et conventions de signe harmonisees.
- Regimes physiques A/B/C/D definis sans prix (anti-circularite).
- Distinction stricte entre observe (HIST) et simule (SCEN).

### 2.2 Qualite des donnees
- Les hard checks invalident une conclusion en cas de FAIL.
- Les WARN sont conserves et interpretes explicitement.
- Les NON_TESTABLE restent visibles et ne sont jamais masques.

### 2.3 Cadre d'interpretation
- Une correlation est un signal explicatif, pas une preuve causale automatique.
- Toute conclusion est bornee au perimetre pays/periode/scenario execute.

## 3. Analyses detaillees par question

## Q1 - Analyse detaillee

### Question business
Identifier de facon auditable la bascule de Phase 1 vers Phase 2 et distinguer explicitement les signaux marche et les signaux physiques.

### Definitions operationnelles
- SR mesure l'intensite du surplus en energie.
- FAR mesure la part du surplus absorbee par la flexibilite.
- IR mesure la rigidite structurelle en creux de charge.
- La bascule marche et la bascule physique doivent etre lues ensemble.

### Perimetre des tests executes
Le perimetre couvre `perimetre du run` et un run combine unique. Les resultats historiques et prospectifs sont presentes separement puis compares.
10 tests ont ete executes, dont HIST=4 et SCEN=6. Repartition des statuts: PASS=7, WARN=1, FAIL=0, NON_TESTABLE=2. Le perimetre prospectif couvre 6 ligne(s) de test scenario.

### Audit block
- Definitions: negative price = `price < 0`, low-price hours = `price < 5`.
- Definitions: `load_mw = load_total_mw - psh_pumping_mw`; PSH pumping is counted as a flexibility sink and not double-counted in load.
- Thresholds: h_negative>=200.0000, h_below_5>=500.0000, low_price_share>=0.0571, capture_ratio_pv<=0.8000, capture_ratio_wind<=0.9000, sr_energy>=0.0100, sr_hours>=0.1000, ir_p10>=1.5000.
- Years used: [2018, 2019, 2020, 2021, 2022, 2023, 2024].
- Quality flags: {'OK': 49}.

### Resultats historiques test par test
- **Q1-H-01** (HIST/nan) - Score marche de bascule. Ce test verifie: La signature marche de phase 2 est calculee et exploitable.. Regle: `stage2_market_score present et non vide`. Valeur observee: `1.2245` ; seuil/regle de comparaison: `score present` ; statut: `PASS`. Interpretation metier: Le score de bascule marche est exploitable.. Resultat conforme a la regle definie. [evidence:Q1-H-01] [source:SPEC2-Q1/Slides 2-4]
- **Q1-H-02** (HIST/nan) - Stress physique SR/FAR/IR. Ce test verifie: La bascule physique est fondee sur SR/FAR/IR.. Regle: `sr_energy/far_energy/ir_p10 presentes`. Valeur observee: `far_energy,ir_p10,sr_energy` ; seuil/regle de comparaison: `SR/FAR/IR presents` ; statut: `PASS`. Interpretation metier: Le stress physique est calculable.. Resultat conforme a la regle definie. [evidence:Q1-H-02] [source:SPEC2-Q1/Slides 3-4]
- **Q1-H-03** (HIST/nan) - Concordance marche vs physique. Ce test verifie: La relation entre bascule marche et bascule physique est mesurable.. Regle: `bascule_year_market et bascule_year_physical comparables`. Valeur observee: `strict=14.29%; concordant_ou_explique=100.00%; n=7; explained=7; reasons=physical_not_reached_but_explained:3;physical_already_phase2_window_start:2;both_not_reached_in_window:1;strict_equal_year:1` ; seuil/regle de comparaison: `concordant_ou_explique >= 80%` ; statut: `PASS`. Interpretation metier: Concordance satisfaisante en comptant les divergences expliquees.. Resultat conforme a la regle definie. [evidence:Q1-H-03] [source:SPEC2-Q1]
- **Q1-H-04** (HIST/nan) - Robustesse seuils. Ce test verifie: Le diagnostic reste stable sous variation raisonnable de seuils.. Regle: `delta bascules sous choc de seuil <= 50%`. Valeur observee: `0.4860` ; seuil/regle de comparaison: `confidence moyenne >=0.60` ; statut: `WARN`. Interpretation metier: Proxy de robustesse du diagnostic de bascule.. Resultat exploitable avec prudence et justification explicite. [evidence:Q1-H-04] [source:Slides 4-6]

### Resultats prospectifs test par test (par scenario)
#### Scenario `DEMAND_UP`
- **Q1-S-01** (SCEN/DEMAND_UP) - Bascule projetee par scenario. Ce test verifie: Chaque scenario fournit un diagnostic de bascule projetee.. Regle: `Q1_country_summary non vide en SCEN`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: La bascule projetee est produite.. Resultat conforme a la regle definie. [evidence:Q1-S-01] [source:SPEC2-Q1/Slides 5]
- **Q1-S-02** (SCEN/DEMAND_UP) - Effets DEMAND_UP/LOW_RIGIDITY. Ce test verifie: Les leviers scenario modifient la bascule vs BASE.. Regle: `delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share)`. Valeur observee: `NaN` ; seuil/regle de comparaison: `delta vs BASE disponible` ; statut: `NON_TESTABLE`. Interpretation metier: Impossible d'evaluer la sensibilite sans BASE et scenario courant.. Resultat non testable faute de donnees ou de perimetre suffisant. [evidence:Q1-S-02] [source:SPEC2-Q1/Slides 5]
- **Q1-S-03** (SCEN/DEMAND_UP) - Qualite de causalite. Ce test verifie: Le regime_coherence respecte le seuil d'interpretation.. Regle: `part regime_coherence >= seuil min`. Valeur observee: `100.00%` ; seuil/regle de comparaison: `>=50% lignes >=0.55` ; statut: `PASS`. Interpretation metier: La coherence scenario est lisible.. Resultat conforme a la regle definie. [evidence:Q1-S-03] [source:SPEC2-Q1]
#### Scenario `LOW_RIGIDITY`
- **Q1-S-01** (SCEN/LOW_RIGIDITY) - Bascule projetee par scenario. Ce test verifie: Chaque scenario fournit un diagnostic de bascule projetee.. Regle: `Q1_country_summary non vide en SCEN`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: La bascule projetee est produite.. Resultat conforme a la regle definie. [evidence:Q1-S-01] [source:SPEC2-Q1/Slides 5]
- **Q1-S-02** (SCEN/LOW_RIGIDITY) - Effets DEMAND_UP/LOW_RIGIDITY. Ce test verifie: Les leviers scenario modifient la bascule vs BASE.. Regle: `delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share)`. Valeur observee: `NaN` ; seuil/regle de comparaison: `delta vs BASE disponible` ; statut: `NON_TESTABLE`. Interpretation metier: Impossible d'evaluer la sensibilite sans BASE et scenario courant.. Resultat non testable faute de donnees ou de perimetre suffisant. [evidence:Q1-S-02] [source:SPEC2-Q1/Slides 5]
- **Q1-S-03** (SCEN/LOW_RIGIDITY) - Qualite de causalite. Ce test verifie: Le regime_coherence respecte le seuil d'interpretation.. Regle: `part regime_coherence >= seuil min`. Valeur observee: `100.00%` ; seuil/regle de comparaison: `>=50% lignes >=0.55` ; statut: `PASS`. Interpretation metier: La coherence scenario est lisible.. Resultat conforme a la regle definie. [evidence:Q1-S-03] [source:SPEC2-Q1]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 14 ligne(s), 1 metrique(s) et 2 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| bascule_year_market | DEMAND_UP | 0.0000 | NaN | NaN | NaN | NaN |
| bascule_year_market | LOW_RIGIDITY | 0.0000 | NaN | NaN | NaN | NaN |

Historique Q1: 7 pays avec bascule analysee; confiance moyenne=0.4857.
Synthese scenario Q1:
| scenario_id | countries | mean_bascule_year_market | mean_bascule_confidence |
| --- | --- | --- | --- |
| DEMAND_UP | 7.0000 | NaN | 0.0000 |
| LOW_RIGIDITY | 7.0000 | NaN | 0.0000 |

### Robustesse / fragilite
Statuts ledger: PASS=7, WARN=1, FAIL=0, NON_TESTABLE=2. Checks severes: 135 sur 773.
Une conclusion est dite robuste uniquement si elle est compatible avec les tests PASS dominants, sans contradiction non expliquee par des FAIL/WARN critiques.

### Risques de mauvaise lecture
- Risque 1: confondre correlation et causalite.
- Risque 2: ignorer les NON_TESTABLE et sur-vendre une conclusion.
- Risque 3: extrapoler hors perimetre pays/periode/scenario sans nouveau run.

### Reponse conclusive a la question
La reponse ci-dessus est strictement bornee aux preuves chiffrees du run courant. Lorsqu'un signal est fragile, la conclusion est formulee comme hypothese de travail et non comme fait etabli.

### Actions/priorites de decision
1. Traiter en priorite les tests FAIL et les checks severes.
2. Challenger les hypotheses prospectives qui pilotent le plus les deltas vs historique.
3. Rejouer le bundle sur perimetre elargi avant decision strategique irreversible.

### Table de tracabilite test par test
| test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | NaN | PASS | 1.2244897959183674 | score present | Le score de bascule marche est exploitable. |
| Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | NaN | PASS | far_energy,ir_p10,sr_energy | SR/FAR/IR presents | Le stress physique est calculable. |
| Q1-H-03 | SPEC2-Q1 | HIST | NaN | PASS | strict=14.29%; concordant_ou_explique=100.00%; n=7; explained=7; reasons=physical_not_reached_but_explained:3;physical_already_phase2_window_start:2;both_not_reached_in_window:1;strict_equal_year:1 | concordant_ou_explique >= 80% | Concordance satisfaisante en comptant les divergences expliquees. |
| Q1-H-04 | Slides 4-6 | HIST | NaN | WARN | 0.486 | confidence moyenne >=0.60 | Proxy de robustesse du diagnostic de bascule. |
| Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. |
| Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 7 | >0 lignes | La bascule projetee est produite. |
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | NON_TESTABLE | NaN | delta vs BASE disponible | Impossible d'evaluer la sensibilite sans BASE et scenario courant. |
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | NON_TESTABLE | NaN | delta vs BASE disponible | Impossible d'evaluer la sensibilite sans BASE et scenario courant. |
| Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
| Q1-S-03 | SPEC2-Q1 | SCEN | LOW_RIGIDITY | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |

### References de preuve
[evidence:Q1-H-01] [evidence:Q1-H-02] [evidence:Q1-H-03] [evidence:Q1-H-04] [evidence:Q1-S-01] [evidence:Q1-S-02] [evidence:Q1-S-03]

## Q2 - Analyse detaillee

### Question business
Mesurer la pente de cannibalisation de valeur, qualifier sa robustesse statistique et relier cette pente aux drivers SR/FAR/IR sans surinterpreter la causalite.

### Definitions operationnelles
- La pente est une mesure empirique historique/prospective, pas une loi physique.
- La robustesse statistique depend de n, p-value et R2.
- Un driver correlle est un facteur explicatif plausible, pas une preuve causale.

### Perimetre des tests executes
Le perimetre couvre `perimetre du run` et un run combine unique. Les resultats historiques et prospectifs sont presentes separement puis compares.
7 tests ont ete executes, dont HIST=3 et SCEN=4. Repartition des statuts: PASS=5, WARN=2, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 4 ligne(s) de test scenario.

### Audit block
- Definitions: negative price = `price < 0`, low-price hours = `price < 5`.
- Definitions: `load_mw = load_total_mw - psh_pumping_mw`; PSH pumping is counted as a flexibility sink and not double-counted in load.
- Years used for regressions: [2019, 2020, 2023, 2024].
- Regression x-axis: ['none', 'pv_penetration_share_load', 'wind_penetration_share_load'].
- Robustness flags: {'FRAGILE': 6, 'NON_TESTABLE': 6, 'ROBUST': 1, 'NOT_SIGNIFICANT': 1}.

### Resultats historiques test par test
- **Q2-H-01** (HIST/nan) - Pentes OLS post-bascule. Ce test verifie: Les pentes PV/Wind sont estimees en historique.. Regle: `Q2_country_slopes non vide`. Valeur observee: `14.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Les pentes historiques sont calculees.. Resultat conforme a la regle definie. [evidence:Q2-H-01] [source:SPEC2-Q2/Slides 10]
- **Q2-H-02** (HIST/nan) - Robustesse statistique. Ce test verifie: R2/p-value/n sont disponibles pour qualifier la robustesse.. Regle: `colonnes r2,p_value,n presentes`. Valeur observee: `n,p_value,r2` ; seuil/regle de comparaison: `r2,p_value,n disponibles` ; statut: `PASS`. Interpretation metier: La robustesse statistique est lisible.. Resultat conforme a la regle definie. [evidence:Q2-H-02] [source:SPEC2-Q2/Slides 10-12]
- **Q2-H-03** (HIST/nan) - Drivers physiques. Ce test verifie: Les drivers SR/FAR/IR/corr VRE-load sont exploites.. Regle: `driver correlations non vides`. Valeur observee: `4.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Les drivers de pente sont disponibles.. Resultat conforme a la regle definie. [evidence:Q2-H-03] [source:Slides 10-13]

### Resultats prospectifs test par test (par scenario)
#### Scenario `HIGH_CO2`
- **Q2-S-01** (SCEN/HIGH_CO2) - Pentes projetees. Ce test verifie: Les pentes sont reproduites en mode scenario.. Regle: `Q2_country_slopes non vide en SCEN`. Valeur observee: `14.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Pentes prospectives calculees.. Resultat conforme a la regle definie. [evidence:Q2-S-01] [source:SPEC2-Q2/Slides 11]
- **Q2-S-02** (SCEN/HIGH_CO2) - Delta pente vs BASE. Ce test verifie: Les differences de pente vs BASE sont calculables.. Regle: `delta slope par pays/tech vs BASE`. Valeur observee: `finite=14.29%; robust=14.29%; reason_known=100.00%` ; seuil/regle de comparaison: `finite_share >= 20%` ; statut: `WARN`. Interpretation metier: Delta de pente partiellement exploitable; beaucoup de valeurs non finies.. Resultat exploitable avec prudence et justification explicite. [evidence:Q2-S-02] [source:SPEC2-Q2]
#### Scenario `HIGH_GAS`
- **Q2-S-01** (SCEN/HIGH_GAS) - Pentes projetees. Ce test verifie: Les pentes sont reproduites en mode scenario.. Regle: `Q2_country_slopes non vide en SCEN`. Valeur observee: `14.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Pentes prospectives calculees.. Resultat conforme a la regle definie. [evidence:Q2-S-01] [source:SPEC2-Q2/Slides 11]
- **Q2-S-02** (SCEN/HIGH_GAS) - Delta pente vs BASE. Ce test verifie: Les differences de pente vs BASE sont calculables.. Regle: `delta slope par pays/tech vs BASE`. Valeur observee: `finite=14.29%; robust=14.29%; reason_known=100.00%` ; seuil/regle de comparaison: `finite_share >= 20%` ; statut: `WARN`. Interpretation metier: Delta de pente partiellement exploitable; beaucoup de valeurs non finies.. Resultat exploitable avec prudence et justification explicite. [evidence:Q2-S-02] [source:SPEC2-Q2]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 28 ligne(s), 1 metrique(s) et 2 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| slope | HIGH_CO2 | 2.0000 | 2.7811 | 2.7811 | -8.4701 | 14.0323 |
| slope | HIGH_GAS | 2.0000 | 1.6851 | 1.6851 | -9.9059 | 13.2761 |

Distribution des pentes historiques par techno:
| tech | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- |
| PV | 4.0000 | 37.1629 | -5.7056 | -19.5119 | 179.5749 |
| WIND | 4.0000 | -0.1525 | -0.3523 | -0.4812 | 0.5755 |

### Robustesse / fragilite
Statuts ledger: PASS=5, WARN=2, FAIL=0, NON_TESTABLE=0. Checks severes: 101 sur 719.
Une conclusion est dite robuste uniquement si elle est compatible avec les tests PASS dominants, sans contradiction non expliquee par des FAIL/WARN critiques.

### Risques de mauvaise lecture
- Risque 1: confondre correlation et causalite.
- Risque 2: ignorer les NON_TESTABLE et sur-vendre une conclusion.
- Risque 3: extrapoler hors perimetre pays/periode/scenario sans nouveau run.

### Reponse conclusive a la question
La reponse ci-dessus est strictement bornee aux preuves chiffrees du run courant. Lorsqu'un signal est fragile, la conclusion est formulee comme hypothese de travail et non comme fait etabli.

### Actions/priorites de decision
1. Traiter en priorite les tests FAIL et les checks severes.
2. Challenger les hypotheses prospectives qui pilotent le plus les deltas vs historique.
3. Rejouer le bundle sur perimetre elargi avant decision strategique irreversible.

### Table de tracabilite test par test
| test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | NaN | PASS | 14 | >0 lignes | Les pentes historiques sont calculees. |
| Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | NaN | PASS | n,p_value,r2 | r2,p_value,n disponibles | La robustesse statistique est lisible. |
| Q2-H-03 | Slides 10-13 | HIST | NaN | PASS | 4 | >0 lignes | Les drivers de pente sont disponibles. |
| Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | 14 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | 14 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | finite=14.29%; robust=14.29%; reason_known=100.00% | finite_share >= 20% | Delta de pente partiellement exploitable; beaucoup de valeurs non finies. |
| Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | finite=14.29%; robust=14.29%; reason_known=100.00% | finite_share >= 20% | Delta de pente partiellement exploitable; beaucoup de valeurs non finies. |

### References de preuve
[evidence:Q2-H-01] [evidence:Q2-H-02] [evidence:Q2-H-03] [evidence:Q2-S-01] [evidence:Q2-S-02]

## Q3 - Analyse detaillee

### Question business
Qualifier la dynamique de sortie de Phase 2 et chiffrer les ordres de grandeur des leviers d'inversion (demande, must-run, flex).

### Definitions operationnelles
- Le statut (degradation/stabilisation/amelioration) est multi-indicateurs.
- Les contre-factuels demande/must-run/flex sont des ordres de grandeur statiques.
- L'entree en Phase 3 demande une convergence de signaux, pas un seul KPI.

### Perimetre des tests executes
Le perimetre couvre `perimetre du run` et un run combine unique. Les resultats historiques et prospectifs sont presentes separement puis compares.
6 tests ont ete executes, dont HIST=2 et SCEN=4. Repartition des statuts: PASS=4, WARN=2, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 4 ligne(s) de test scenario.

### Audit block
- Definitions: negative price = `price < 0`, low-price hours = `price < 5`.
- Definitions: `load_mw = load_total_mw - psh_pumping_mw`; PSH pumping is counted as a flexibility sink and not double-counted in load.
- Years used: [2024].
- Quality flags: {'nan': 4, 'q1_no_bascule': 3}.
- Scenario assumptions present in rows: scenario_id, assumed_demand_multiplier, assumed_must_run_reduction_factor, assumed_flex_multiplier.

### Resultats historiques test par test
- **Q3-H-01** (HIST/nan) - Tendances glissantes. Ce test verifie: Les tendances h_negative et capture_ratio sont estimees.. Regle: `Q3_status non vide`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Les tendances historiques sont calculees.. Resultat conforme a la regle definie. [evidence:Q3-H-01] [source:SPEC2-Q3/Slides 16]
- **Q3-H-02** (HIST/nan) - Statuts sortie phase 2. Ce test verifie: Les statuts degradation/stabilisation/amelioration sont attribues.. Regle: `status dans ensemble attendu`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `status valides` ; statut: `PASS`. Interpretation metier: Les statuts business sont renseignes.. Resultat conforme a la regle definie. [evidence:Q3-H-02] [source:SPEC2-Q3]

### Resultats prospectifs test par test (par scenario)
#### Scenario `DEMAND_UP`
- **Q3-S-01** (SCEN/DEMAND_UP) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `colonnes inversion presentes` ; statut: `PASS`. Interpretation metier: Les ordres de grandeur d'inversion sont quantifies.. Resultat conforme a la regle definie. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/DEMAND_UP) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `hors_scope=42.86%` ; seuil/regle de comparaison: `hors_scope < 40%` ; statut: `WARN`. Interpretation metier: Lecture partiellement informative: forte part de cas hors scope Stage 2.. Resultat exploitable avec prudence et justification explicite. [evidence:Q3-S-02] [source:Slides 17-19]
#### Scenario `LOW_RIGIDITY`
- **Q3-S-01** (SCEN/LOW_RIGIDITY) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `colonnes inversion presentes` ; statut: `PASS`. Interpretation metier: Les ordres de grandeur d'inversion sont quantifies.. Resultat conforme a la regle definie. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/LOW_RIGIDITY) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `hors_scope=42.86%` ; seuil/regle de comparaison: `hors_scope < 40%` ; statut: `WARN`. Interpretation metier: Lecture partiellement informative: forte part de cas hors scope Stage 2.. Resultat exploitable avec prudence et justification explicite. [evidence:Q3-S-02] [source:Slides 17-19]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 28 ligne(s), 2 metrique(s) et 2 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| inversion_k_demand | DEMAND_UP | 3.0000 | -0.0018 | 0.0000 | -0.0054 | 0.0000 |
| inversion_k_demand | LOW_RIGIDITY | 3.0000 | -0.0018 | 0.0000 | -0.0054 | 0.0000 |
| inversion_r_mustrun | DEMAND_UP | 4.0000 | -0.1859 | 0.0000 | -0.7435 | 0.0000 |
| inversion_r_mustrun | LOW_RIGIDITY | 4.0000 | -0.1859 | 0.0000 | -0.7435 | 0.0000 |

Distribution des statuts historiques Q3:
| status | n |
| --- | --- |
| CONTINUES | 4.0000 |
| HORS_SCOPE_PHASE2 | 3.0000 |

### Robustesse / fragilite
Statuts ledger: PASS=4, WARN=2, FAIL=0, NON_TESTABLE=0. Checks severes: 104 sur 713.
Une conclusion est dite robuste uniquement si elle est compatible avec les tests PASS dominants, sans contradiction non expliquee par des FAIL/WARN critiques.

### Risques de mauvaise lecture
- Risque 1: confondre correlation et causalite.
- Risque 2: ignorer les NON_TESTABLE et sur-vendre une conclusion.
- Risque 3: extrapoler hors perimetre pays/periode/scenario sans nouveau run.

### Reponse conclusive a la question
La reponse ci-dessus est strictement bornee aux preuves chiffrees du run courant. Lorsqu'un signal est fragile, la conclusion est formulee comme hypothese de travail et non comme fait etabli.

### Actions/priorites de decision
1. Traiter en priorite les tests FAIL et les checks severes.
2. Challenger les hypotheses prospectives qui pilotent le plus les deltas vs historique.
3. Rejouer le bundle sur perimetre elargi avant decision strategique irreversible.

### Table de tracabilite test par test
| test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | NaN | PASS | 7 | >0 lignes | Les tendances historiques sont calculees. |
| Q3-H-02 | SPEC2-Q3 | HIST | NaN | PASS | 2 | status valides | Les statuts business sont renseignes. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | WARN | hors_scope=42.86% | hors_scope < 40% | Lecture partiellement informative: forte part de cas hors scope Stage 2. |
| Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | WARN | hors_scope=42.86% | hors_scope < 40% | Lecture partiellement informative: forte part de cas hors scope Stage 2. |

### References de preuve
[evidence:Q3-H-01] [evidence:Q3-H-02] [evidence:Q3-S-01] [evidence:Q3-S-02]

Lecture complementaire: sur le test `Q3-H-01`, la verification porte sur `Les tendances h_negative et capture_ratio sont estimees.` avec une valeur observee `7.0000` comparee a `>0 lignes`. Le statut `PASS` implique la lecture suivante: Resultat conforme a la regle definie. En decision, la consequence directe est: Les tendances historiques sont calculees.. [evidence:Q3-H-01] [source:SPEC2-Q3/Slides 16]
Lecture complementaire: sur le test `Q3-H-02`, la verification porte sur `Les statuts degradation/stabilisation/amelioration sont attribues.` avec une valeur observee `2.0000` comparee a `status valides`. Le statut `PASS` implique la lecture suivante: Resultat conforme a la regle definie. En decision, la consequence directe est: Les statuts business sont renseignes.. [evidence:Q3-H-02] [source:SPEC2-Q3]
Lecture complementaire: sur le test `Q3-S-01`, la verification porte sur `Les besoins demande/must-run/flex sont quantifies en scenario.` avec une valeur observee `7.0000` comparee a `colonnes inversion presentes`. Le statut `PASS` implique la lecture suivante: Resultat conforme a la regle definie. En decision, la consequence directe est: Les ordres de grandeur d'inversion sont quantifies.. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
Lecture complementaire: sur le test `Q3-S-01`, la verification porte sur `Les besoins demande/must-run/flex sont quantifies en scenario.` avec une valeur observee `7.0000` comparee a `colonnes inversion presentes`. Le statut `PASS` implique la lecture suivante: Resultat conforme a la regle definie. En decision, la consequence directe est: Les ordres de grandeur d'inversion sont quantifies.. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]

## Q4 - Analyse detaillee

### Question business
Quantifier l'effet des batteries sous angle systeme et sous angle actif PV, avec verification stricte des invariants physiques.

### Definitions operationnelles
- SURPLUS_FIRST cible d'abord l'absorption du surplus systeme.
- PRICE_ARBITRAGE_SIMPLE fournit une lecture economique simplifiee de l'actif batterie.
- PV_COLOCATED mesure le gain de valeur d'un couple PV + batterie.

### Perimetre des tests executes
Le perimetre couvre `perimetre du run` et un run combine unique. Les resultats historiques et prospectifs sont presentes separement puis compares.
6 tests ont ete executes, dont HIST=2 et SCEN=4. Repartition des statuts: PASS=6, WARN=0, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 4 ligne(s) de test scenario.

### Audit block
- Definitions: negative price = `price < 0`, low-price hours = `price < 5`.
- Definitions: `load_mw = load_total_mw - psh_pumping_mw`; PSH pumping is counted as a flexibility sink and not double-counted in load.
- Years used: [2024].
- Dispatch modes: ['SURPLUS_FIRST'].
- Grid columns: `bess_power_mw_test`, `bess_energy_mwh_test`, `bess_duration_h_test`.
- Quality/status flags: {'met_in_grid': 3, 'unreachable_under_policy': 2, 'grid_too_small': 1, 'already_met': 1}.

### Resultats historiques test par test
- **Q4-H-01** (HIST/nan) - Simulation BESS 3 modes. Ce test verifie: SURPLUS_FIRST, PRICE_ARBITRAGE_SIMPLE et PV_COLOCATED sont executes.. Regle: `3 modes executes avec sorties non vides`. Valeur observee: `HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED` ; seuil/regle de comparaison: `3 modes executes` ; statut: `PASS`. Interpretation metier: Les trois modes Q4 sont disponibles.. Resultat conforme a la regle definie. [evidence:Q4-H-01] [source:SPEC2-Q4/Slides 22]
- **Q4-H-02** (HIST/nan) - Invariants physiques BESS. Ce test verifie: Bornes SOC/puissance/energie respectees (mode physique de reference) avec garde-fous structurels sur modes alternatifs.. Regle: `aucun FAIL physique/structurel pertinent`. Valeur observee: `WARN` ; seuil/regle de comparaison: `aucun FAIL physique` ; statut: `PASS`. Interpretation metier: Les invariants physiques batterie sont respectes. Des avertissements non-physiques peuvent subsister (objectif/scenario).. Resultat conforme a la regle definie. [evidence:Q4-H-02] [source:SPEC2-Q4]

### Resultats prospectifs test par test (par scenario)
#### Scenario `HIGH_CO2`
- **Q4-S-01** (SCEN/HIGH_CO2) - Comparaison effet batteries par scenario. Ce test verifie: Impact FAR/surplus/capture compare entre scenarios utiles.. Regle: `Q4 summary non vide pour >=1 scenario`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Resultats Q4 prospectifs disponibles.. Resultat conforme a la regle definie. [evidence:Q4-S-01] [source:SPEC2-Q4/Slides 23]
- **Q4-S-02** (SCEN/HIGH_CO2) - Sensibilite valeur commodites. Ce test verifie: Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.. Regle: `delta pv_capture ou revenus vs BASE`. Valeur observee: `share_finite=100.00%` ; seuil/regle de comparaison: `>=80% valeurs finies` ; statut: `PASS`. Interpretation metier: Sensibilite valeur exploitable sur le panel.. Resultat conforme a la regle definie. [evidence:Q4-S-02] [source:Slides 23-25]
#### Scenario `HIGH_GAS`
- **Q4-S-01** (SCEN/HIGH_GAS) - Comparaison effet batteries par scenario. Ce test verifie: Impact FAR/surplus/capture compare entre scenarios utiles.. Regle: `Q4 summary non vide pour >=1 scenario`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Resultats Q4 prospectifs disponibles.. Resultat conforme a la regle definie. [evidence:Q4-S-01] [source:SPEC2-Q4/Slides 23]
- **Q4-S-02** (SCEN/HIGH_GAS) - Sensibilite valeur commodites. Ce test verifie: Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.. Regle: `delta pv_capture ou revenus vs BASE`. Valeur observee: `share_finite=100.00%` ; seuil/regle de comparaison: `>=80% valeurs finies` ; statut: `PASS`. Interpretation metier: Sensibilite valeur exploitable sur le panel.. Resultat conforme a la regle definie. [evidence:Q4-S-02] [source:Slides 23-25]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 56 ligne(s), 3 metrique(s) et 4 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| far_after | HIGH_CO2 | 7.0000 | 0.0751 | 0.0000 | -0.2491 | 0.6853 |
| far_after | HIGH_GAS | 7.0000 | 0.0751 | 0.0000 | -0.2491 | 0.6853 |
| far_after | HIST_PRICE_ARBITRAGE_SIMPLE | 7.0000 | -0.0013 | 0.0000 | -0.0093 | 0.0011 |
| far_after | HIST_PV_COLOCATED | 7.0000 | -0.0003 | 0.0000 | -0.0016 | 0.0010 |
| pv_capture_price_after | HIGH_CO2 | 7.0000 | 66.9466 | 54.9417 | 28.6881 | 98.6087 |
| pv_capture_price_after | HIGH_GAS | 7.0000 | 72.1019 | 60.6583 | 34.5235 | 104.3699 |
| surplus_unabs_energy_after | HIGH_CO2 | 7.0000 | -0.8167 | -0.0012 | -5.7031 | 0.0092 |
| surplus_unabs_energy_after | HIGH_GAS | 7.0000 | -0.8167 | -0.0012 | -5.7031 | 0.0092 |

Synthese sizing historique Q4:
| scenario_id | country | year | dispatch_mode | objective | bess_power_mw_test | bess_energy_mwh_test | bess_duration_h_test | required_bess_power_mw | required_bess_energy_mwh | required_bess_duration_h | far_before | far_after | far_before_trivial | far_after_trivial | h_negative_before | h_negative_after | h_below_5_before | h_below_5_after | delta_h_negative | delta_h_below_5 | baseload_price_before | baseload_price_after | capture_ratio_pv_before | capture_ratio_pv_after | capture_ratio_wind_before | capture_ratio_wind_after | delta_capture_ratio_pv | delta_capture_ratio_wind | surplus_unabs_energy_before | surplus_unabs_energy_after | pv_capture_price_before | pv_capture_price_after | wind_capture_price_before | wind_capture_price_after | days_spread_gt50_before | days_spread_gt50_after | avg_daily_spread_before | avg_daily_spread_after | low_residual_share_before | low_residual_share_after | sr_hours_share_before | sr_hours_share_after | ir_p10_before | ir_p10_after | turned_off_family_low_price | turned_off_family_physical | turned_off_family_value_pv | turned_off_family_value_wind | turned_off_family_any | revenue_bess_price_taker | soc_min | soc_max | soc_start_mwh | soc_end_mwh | soc_end_target_mwh | charge_max | discharge_max | charge_sum_mwh | discharge_sum_mwh | simultaneous_charge_discharge_hours | eta_roundtrip | eta_charge | eta_discharge | soc_boundary_mode | charge_vs_surplus_violation_hours | engine_version | compute_time_sec | cache_hit | bess_power_mw | duration_h | bess_energy_mwh | objective_met | objective_reason | objective_not_reached | objective_target_value | objective_recommendation | pv_capacity_proxy_mw | power_grid_max_mw | duration_grid_max_h | grid_expansions_used | notes_quality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HIST | BE | 2 024.00 | SURPLUS_FIRST | LOW_PRICE_TARGET | 250.0000 | 500.0000 | 2.0000 | 250.0000 | 500.0000 | 2.0000 | 0.9878 | 0.9891 | 0.0000 | 0.0000 | 404.0000 | 144.0000 | 738.0000 | 738.0000 | -260.0000 | 0.0000 | 70.3232 | 70.9575 | 0.5561 | 0.5986 | 0.8570 | 0.8598 | 0.0425 | 0.0028 | 0.0052 | 0.0046 | 39.1076 | 42.4745 | 60.2685 | 61.0126 | 303.0000 | 300.0000 | 92.3692 | 88.4909 | 0.0947 | 0.0947 | 0.0540 | 0.0540 | 0.3944 | 0.3944 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NaN | 0.0000 | 500.0000 | 0.0000 | 0.0000 | 0.0000 | 250.0000 | 250.0000 | 533.0018 | 469.0416 | 0.0000 | 0.8800 | 0.9381 | 0.9381 | ZERO_END | 0.0000 | v2.2.2 | 0.5133 | 1.0000 | 250.0000 | 2.0000 | 500.0000 | 1.0000 | met_in_grid | 0.0000 | 200.0000 | NaN | 6 151.41 | 1 500.00 | 8.0000 | 0.0000 | ok |
| HIST | CZ | 2 024.00 | SURPLUS_FIRST | LOW_PRICE_TARGET | 250.0000 | 1 000.00 | 4.0000 | 250.0000 | 1 000.00 | 4.0000 | 0.9887 | 0.9892 | 0.0000 | 0.0000 | 315.0000 | 250.0000 | 530.0000 | 530.0000 | -65.0000 | 0.0000 | 85.1061 | 85.2754 | 0.6282 | 0.6363 | 0.9337 | 0.9343 | 0.0081 | 0.0005 | 0.0225 | 0.0214 | 53.4628 | 54.2594 | 79.4661 | 79.6689 | 321.0000 | 321.0000 | 113.8115 | 113.0826 | 0.0648 | 0.0648 | 0.3533 | 0.3533 | 0.8497 | 0.8497 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NaN | 0.0000 | 1 000.00 | 0.0000 | 0.0000 | 0.0000 | 250.0000 | 250.0000 | 1 066.00 | 938.0832 | 0.0000 | 0.8800 | 0.9381 | 0.9381 | ZERO_END | 0.0000 | v2.2.2 | 1.6497 | 1.0000 | 250.0000 | 4.0000 | 1 000.00 | 0.0000 | unreachable_under_policy | 1.0000 | 200.0000 | review_policy_constraints_or_targets | 2 445.38 | 10 560.95 | 24.0000 | 1.0000 | ok |
| HIST | DE | 2 024.00 | SURPLUS_FIRST | LOW_PRICE_TARGET | 250.0000 | 500.0000 | 2.0000 | 250.0000 | 500.0000 | 2.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 457.0000 | 96.0000 | 756.0000 | 756.0000 | -361.0000 | 0.0000 | 78.5155 | 79.1031 | 0.5888 | 0.6195 | 0.8384 | 0.8380 | 0.0307 | -0.0005 | 0.0000 | 0.0000 | 46.2280 | 49.0015 | 65.8312 | 66.2865 | 319.0000 | 319.0000 | 112.0063 | 108.2080 | 0.0926 | 0.0926 | 0.0757 | 0.0757 | 0.2263 | 0.2263 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NaN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.8800 | 0.9381 | 0.9381 | ZERO_END | 0.0000 | v2.2.2 | 0.8010 | 1.0000 | 250.0000 | 2.0000 | 500.0000 | 1.0000 | met_in_grid | 0.0000 | 200.0000 | NaN | 40 714.24 | 1 500.00 | 8.0000 | 0.0000 | ok |
| HIST | ES | 2 024.00 | SURPLUS_FIRST | LOW_PRICE_TARGET | 250.0000 | 500.0000 | 2.0000 | 250.0000 | 500.0000 | 2.0000 | 0.9994 | 0.9996 | 0.0000 | 0.0000 | 247.0000 | 74.0000 | 1 642.00 | 1 642.00 | -173.0000 | 0.0000 | 63.0395 | 63.0482 | 0.6790 | 0.6792 | 0.8821 | 0.8821 | 0.0003 | -0.0001 | 0.0021 | 0.0016 | 42.8012 | 42.8235 | 55.6095 | 55.6139 | 272.0000 | 272.0000 | 71.5241 | 71.4851 | 0.0838 | 0.0837 | 0.1692 | 0.1693 | 0.2952 | 0.2952 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NaN | 0.0000 | 500.0000 | 0.0000 | 0.0000 | 0.0000 | 250.0000 | 250.0000 | 533.0018 | 469.0416 | 0.0000 | 0.8800 | 0.9381 | 0.9381 | ZERO_END | 0.0000 | v2.2.2 | 0.6280 | 1.0000 | 250.0000 | 2.0000 | 500.0000 | 1.0000 | met_in_grid | 0.0000 | 200.0000 | NaN | 20 284.00 | 1 500.00 | 8.0000 | 0.0000 | ok |
| HIST | FR | 2 024.00 | SURPLUS_FIRST | LOW_PRICE_TARGET | 82 800.00 | 1 987 200.0 | 24.0000 | 82 800.00 | 1 987 200.0 | 24.0000 | 0.8581 | 0.8965 | 0.0000 | 0.0000 | 352.0000 | 203.0000 | 1 018.00 | 1 018.00 | -149.0000 | 0.0000 | 58.0131 | 58.1423 | 0.6765 | 0.6811 | 0.9026 | 0.9019 | 0.0046 | -0.0006 | 7.8214 | 5.7031 | 39.2480 | 39.6010 | 52.3599 | 52.4404 | 284.0000 | 284.0000 | 77.0648 | 76.6765 | 0.0151 | 0.0155 | 0.8503 | 0.8518 | 1.0632 | 1.0625 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NaN | 0.0000 | 1 987 200.0 | 0.0000 | 0.0000 | 0.0000 | 9 023.50 | 82 800.00 | 2 118 362.3 | 1 864 158.8 | 0.0000 | 0.8800 | 0.9381 | 0.9381 | ZERO_END | 0.0000 | v2.2.2 | 1.8746 | 1.0000 | 82 800.00 | 24.0000 | 1 987 200.0 | 0.0000 | grid_too_small | 1.0000 | 200.0000 | expand_grid_to_power_mw>=124200.0;duration_h>=36.0 | 12 893.80 | 82 800.00 | 24.0000 | 1.0000 | ok |
| HIST | IT_NORD | 2 024.00 | SURPLUS_FIRST | LOW_PRICE_TARGET | 0.0000 | 0.0000 | 2.0000 | 0.0000 | 0.0000 | 2.0000 | 0.3147 | 0.3147 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 11.0000 | 11.0000 | 0.0000 | 0.0000 | 107.4096 | 107.4096 | 0.8947 | 0.8947 | 0.9820 | 0.9820 | 0.0000 | 0.0000 | 0.0012 | 0.0012 | 96.0989 | 96.0989 | 105.4720 | 105.4720 | 276.0000 | 276.0000 | 65.9688 | 65.9688 | 0.1002 | 0.1002 | 0.0006 | 0.0006 | 0.1506 | 0.1506 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NaN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.8800 | 0.9381 | 0.9381 | ZERO_END | 0.0000 | v2.2.2 | 0.6421 | 1.0000 | 0.0000 | 2.0000 | 0.0000 | 1.0000 | already_met | 0.0000 | 200.0000 | NaN | 6 024.00 | 1 500.00 | 8.0000 | 0.0000 | ok |
| HIST | NL | 2 024.00 | SURPLUS_FIRST | LOW_PRICE_TARGET | 0.0000 | 0.0000 | 2.0000 | 0.0000 | 0.0000 | 2.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 458.0000 | 458.0000 | 774.0000 | 774.0000 | 0.0000 | 0.0000 | 77.2893 | 77.2893 | 0.6025 | 0.6025 | 0.8839 | 0.8839 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 46.5701 | 46.5701 | 68.3161 | 68.3161 | 317.0000 | 317.0000 | 113.7168 | 113.7168 | 0.1002 | 0.1002 | 0.0000 | 0.0000 | 0.0007 | 0.0007 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NaN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.8800 | 0.9381 | 0.9381 | ZERO_END | 0.0000 | v2.2.2 | 1.7140 | 1.0000 | 0.0000 | 2.0000 | 0.0000 | 0.0000 | unreachable_under_policy | 1.0000 | 200.0000 | review_policy_constraints_or_targets | 339.3714 | 19 477.15 | 24.0000 | 1.0000 | ok |
Apercu frontiere historique Q4:
| dispatch_mode | bess_power_mw_test | bess_duration_h_test | far_after | surplus_unabs_energy_after | pv_capture_price_after |
| --- | --- | --- | --- | --- | --- |
| SURPLUS_FIRST | 0.0000 | 2.0000 | 0.9878 | 0.0052 | 39.1076 |
| SURPLUS_FIRST | 0.0000 | 4.0000 | 0.9878 | 0.0052 | 39.1076 |
| SURPLUS_FIRST | 0.0000 | 6.0000 | 0.9878 | 0.0052 | 39.1076 |
| SURPLUS_FIRST | 0.0000 | 8.0000 | 0.9878 | 0.0052 | 39.1076 |
| SURPLUS_FIRST | 250.0000 | 2.0000 | 0.9891 | 0.0046 | 42.4745 |
| SURPLUS_FIRST | 250.0000 | 4.0000 | 0.9904 | 0.0041 | 42.4745 |
| SURPLUS_FIRST | 250.0000 | 6.0000 | 0.9916 | 0.0036 | 42.4745 |
| SURPLUS_FIRST | 250.0000 | 8.0000 | 0.9929 | 0.0030 | 42.4803 |
| SURPLUS_FIRST | 500.0000 | 2.0000 | 0.9904 | 0.0041 | 42.4745 |
| SURPLUS_FIRST | 500.0000 | 4.0000 | 0.9929 | 0.0030 | 42.4804 |
| SURPLUS_FIRST | 500.0000 | 6.0000 | 0.9954 | 0.0020 | 42.4861 |
| SURPLUS_FIRST | 500.0000 | 8.0000 | 0.9979 | 0.0009 | 42.4864 |
| SURPLUS_FIRST | 750.0000 | 2.0000 | 0.9916 | 0.0036 | 42.4844 |
| SURPLUS_FIRST | 750.0000 | 4.0000 | 0.9954 | 0.0020 | 42.4969 |
| SURPLUS_FIRST | 750.0000 | 6.0000 | 0.9991 | 0.0004 | 42.4973 |
| SURPLUS_FIRST | 750.0000 | 8.0000 | 1.0000 | 0.0000 | 42.4973 |
| SURPLUS_FIRST | 1 000.00 | 2.0000 | 0.9929 | 0.0030 | 42.4902 |
| SURPLUS_FIRST | 1 000.00 | 4.0000 | 0.9979 | 0.0009 | 42.4973 |
| SURPLUS_FIRST | 1 000.00 | 6.0000 | 1.0000 | 0.0000 | 42.4973 |
| SURPLUS_FIRST | 1 000.00 | 8.0000 | 1.0000 | 0.0000 | 42.4973 |
| SURPLUS_FIRST | 1 500.00 | 2.0000 | 0.9954 | 0.0020 | 42.4969 |
| SURPLUS_FIRST | 1 500.00 | 4.0000 | 1.0000 | 0.0000 | 42.4973 |
| SURPLUS_FIRST | 1 500.00 | 6.0000 | 1.0000 | 0.0000 | 42.4973 |
| SURPLUS_FIRST | 1 500.00 | 8.0000 | 1.0000 | 0.0000 | 42.4973 |
| SURPLUS_FIRST | 0.0000 | 2.0000 | 0.9887 | 0.0225 | 53.4628 |
| SURPLUS_FIRST | 0.0000 | 4.0000 | 0.9887 | 0.0225 | 53.4628 |
| SURPLUS_FIRST | 0.0000 | 6.0000 | 0.9887 | 0.0225 | 53.4628 |
| SURPLUS_FIRST | 0.0000 | 8.0000 | 0.9887 | 0.0225 | 53.4628 |
| SURPLUS_FIRST | 0.0000 | 12.0000 | 0.9887 | 0.0225 | 53.4628 |
| SURPLUS_FIRST | 0.0000 | 24.0000 | 0.9887 | 0.0225 | 53.4628 |

### Robustesse / fragilite
Statuts ledger: PASS=6, WARN=0, FAIL=0, NON_TESTABLE=0. Checks severes: 4 sur 69.
Une conclusion est dite robuste uniquement si elle est compatible avec les tests PASS dominants, sans contradiction non expliquee par des FAIL/WARN critiques.

### Risques de mauvaise lecture
- Risque 1: confondre correlation et causalite.
- Risque 2: ignorer les NON_TESTABLE et sur-vendre une conclusion.
- Risque 3: extrapoler hors perimetre pays/periode/scenario sans nouveau run.

### Reponse conclusive a la question
La reponse ci-dessus est strictement bornee aux preuves chiffrees du run courant. Lorsqu'un signal est fragile, la conclusion est formulee comme hypothese de travail et non comme fait etabli.

### Actions/priorites de decision
1. Traiter en priorite les tests FAIL et les checks severes.
2. Challenger les hypotheses prospectives qui pilotent le plus les deltas vs historique.
3. Rejouer le bundle sur perimetre elargi avant decision strategique irreversible.

### Table de tracabilite test par test
| test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q4-H-01 | SPEC2-Q4/Slides 22 | HIST | NaN | PASS | HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED | 3 modes executes | Les trois modes Q4 sont disponibles. |
| Q4-H-02 | SPEC2-Q4 | HIST | NaN | PASS | WARN | aucun FAIL physique | Les invariants physiques batterie sont respectes. Des avertissements non-physiques peuvent subsister (objectif/scenario). |
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | 7 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | 7 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. |
| Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. |

### References de preuve
[evidence:Q4-H-01] [evidence:Q4-H-02] [evidence:Q4-S-01] [evidence:Q4-S-02]

## Q5 - Analyse detaillee

### Question business
Mesurer l'impact du gaz et du CO2 sur l'ancre thermique et en deduire des sensibilites decisionnelles traceables.

### Definitions operationnelles
- TTL est une statistique de prix hors surplus ; TCA est une ancre cout explicative.
- dTCA/dCO2 et dTCA/dGas sont des sensibilites marginales.
- Le CO2 requis est un ordre de grandeur conditionnel, pas une prediction de marche.

### Perimetre des tests executes
Le perimetre couvre `perimetre du run` et un run combine unique. Les resultats historiques et prospectifs sont presentes separement puis compares.
8 tests ont ete executes, dont HIST=2 et SCEN=6. Repartition des statuts: PASS=8, WARN=0, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 6 ligne(s) de test scenario.

### Audit block
- Definitions: negative price = `price < 0`, low-price hours = `price < 5`.
- Definitions: `load_mw = load_total_mw - psh_pumping_mw`; PSH pumping is counted as a flexibility sink and not double-counted in load.
- Years used: [2024].
- Anchor assumptions columns: `scenario_id`, `assumed_co2_price_eur_t`, `assumed_gas_price_eur_mwh_th`, `assumed_efficiency`, `assumed_emission_factor_t_per_mwh_th`, `chosen_anchor_tech`.
- Quality flags: {'target_above_anchor': 7}.

### Resultats historiques test par test
- **Q5-H-01** (HIST/nan) - Ancre thermique historique. Ce test verifie: TTL/TCA/alpha/corr sont estimes hors surplus.. Regle: `Q5_summary non vide avec ttl_obs et tca_q95`. Valeur observee: `share_fini=100.00%` ; seuil/regle de comparaison: `>=80% lignes ttl/tca finies` ; statut: `PASS`. Interpretation metier: L'ancre thermique est quantifiable sur la majorite des pays.. Resultat conforme a la regle definie. [evidence:Q5-H-01] [source:SPEC2-Q5/Slides 28]
- **Q5-H-02** (HIST/nan) - Sensibilites analytiques. Ce test verifie: dTCA/dCO2 et dTCA/dGas sont positives.. Regle: `dTCA_dCO2 > 0 et dTCA_dGas > 0`. Valeur observee: `share_positive=100.00%` ; seuil/regle de comparaison: `100% lignes >0` ; statut: `PASS`. Interpretation metier: Sensibilites analytiques globalement coherentes.. Resultat conforme a la regle definie. [evidence:Q5-H-02] [source:SPEC2-Q5]

### Resultats prospectifs test par test (par scenario)
#### Scenario `HIGH_BOTH`
- **Q5-S-01** (SCEN/HIGH_BOTH) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/HIGH_BOTH) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `share_finite=100.00%` ; seuil/regle de comparaison: `>=80% valeurs finies` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable sur le panel.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]
#### Scenario `HIGH_CO2`
- **Q5-S-01** (SCEN/HIGH_CO2) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/HIGH_CO2) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `share_finite=100.00%` ; seuil/regle de comparaison: `>=80% valeurs finies` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable sur le panel.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]
#### Scenario `HIGH_GAS`
- **Q5-S-01** (SCEN/HIGH_GAS) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/HIGH_GAS) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `share_finite=100.00%` ; seuil/regle de comparaison: `>=80% valeurs finies` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable sur le panel.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 63 ligne(s), 3 metrique(s) et 3 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| co2_required_base_non_negative | HIGH_BOTH | 7.0000 | -16.9960 | -44.7030 | -45.7921 | 51.9971 |
| co2_required_base_non_negative | HIGH_CO2 | 7.0000 | 22.0776 | 10.0000 | 8.9109 | 51.9971 |
| co2_required_base_non_negative | HIGH_GAS | 7.0000 | -66.9960 | -94.7030 | -95.7921 | 1.9971 |
| tca_q95 | HIGH_BOTH | 7.0000 | 78.1952 | 68.2596 | 66.2381 | 104.7831 |
| tca_q95 | HIGH_CO2 | 7.0000 | 39.6699 | 27.3505 | 25.3290 | 72.2173 |
| tca_q95 | HIGH_GAS | 7.0000 | 52.2587 | 49.8959 | 47.8745 | 59.9147 |
| ttl_obs | HIGH_BOTH | 7.0000 | 25.0262 | 23.1050 | -4.0515 | 66.5890 |
| ttl_obs | HIGH_CO2 | 7.0000 | 34.1040 | 29.5322 | 2.3758 | 82.2930 |
| ttl_obs | HIGH_GAS | 7.0000 | 41.1745 | 37.4231 | 10.2667 | 87.3127 |

Synthese historique Q5:
| scenario_id | country | year_range_used | ttl_reference_mode | ttl_reference_year | marginal_tech | chosen_anchor_tech | fuel_used | assumed_co2_price_eur_t | assumed_gas_price_eur_mwh_th | assumed_coal_price_eur_mwh_th | assumed_efficiency | assumed_emission_factor_t_per_mwh_th | assumed_vom_eur_mwh | assumed_fuel_multiplier_vs_gas | ttl_obs | ttl_obs_price_cd | ttl_annual_metrics_same_year | ttl_anchor | ttl_anchor_formula | ttl_physical | ttl_regression | ttl_method | tca_q95 | alpha | alpha_effective | corr_cd | anchor_confidence | anchor_distribution_error_p90_p95 | anchor_error_p90 | anchor_error_p95 | anchor_status | dTCA_dCO2 | dTCA_dFuel | dTCA_dGas | eta_implicit_from_dTCA_dFuel | ef_implicit_t_per_mwh_e | ttl_target | anchor_gap_to_target | required_co2_eur_t | required_gas_eur_mwh_th | required_co2_abs_eur_t | required_gas_abs_eur_mwh_th | delta_co2_vs_scenario | delta_gas_vs_scenario | required_co2_abs_raw_eur_t | required_gas_abs_raw_eur_mwh_th | co2_required_base | co2_required_gas_override | co2_required_base_non_negative | co2_required_gas_override_non_negative | warnings_quality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HIST | BE | 2018-2024 | year_specific | 2 024.00 | CCGT | CCGT | gas | 70.6900 | 46.9000 | NaN | 0.5500 | 0.2020 | 3.0000 | 1.0000 | 131.8560 | 131.8560 | 131.8560 | 112.8001 | 114.2352 | 112.8001 | NaN | anchor_distributional | 112.8001 | 19.0559 | 19.0559 | 0.3553 | 0.8306 | 13.5515 | 8.0466 | 19.0564 | target_above_anchor | 0.3673 | 1.8182 | 1.8182 | 0.5500 | 0.3673 | 160.0000 | 45.7648 | 195.2970 | 72.0706 | 195.2970 | 72.0706 | 124.6070 | 25.1706 | 195.2970 | 72.0706 | 195.2970 | NaN | 195.2970 | NaN | NaN |
| HIST | CZ | 2018-2024 | year_specific | 2 024.00 | COAL | COAL | coal | 70.9300 | 47.0200 | 25.8610 | 0.3800 | 0.3410 | 4.0000 | 0.5500 | 170.0000 | 170.0000 | 170.0000 | 132.3046 | 135.7056 | 132.3046 | NaN | anchor_distributional | 132.3046 | 37.6954 | 37.6954 | 0.3580 | 0.6651 | 26.7926 | 15.8898 | 37.6954 | target_above_anchor | 0.8974 | 2.6316 | 1.4474 | 0.3800 | 0.8974 | 160.0000 | 24.2944 | 98.0029 | 63.8052 | 98.0029 | 63.8052 | 27.0729 | 16.7852 | 98.0029 | 63.8052 | 98.0029 | NaN | 98.0029 | NaN | NaN |
| HIST | DE | 2018-2024 | year_specific | 2 024.00 | COAL | COAL | coal | 70.8300 | 46.9000 | 25.7950 | 0.3800 | 0.3410 | 4.0000 | 0.5500 | 146.0690 | 146.0690 | 146.0690 | 131.5195 | 135.4422 | 131.5195 | NaN | anchor_distributional | 131.5195 | 14.5495 | 14.5495 | 0.2787 | 0.9006 | 7.9516 | -1.3508 | 14.5525 | target_above_anchor | 0.8974 | 2.6316 | 1.4474 | 0.3800 | 0.8974 | 160.0000 | 24.5578 | 98.1965 | 63.8672 | 98.1965 | 63.8672 | 27.3665 | 16.9672 | 98.1965 | 63.8672 | 98.1965 | NaN | 98.1965 | NaN | NaN |
| HIST | ES | 2018-2024 | year_specific | 2 024.00 | CCGT | CCGT | gas | 70.6900 | 47.0200 | NaN | 0.5500 | 0.2020 | 3.0000 | 1.0000 | 140.0000 | 140.0000 | 140.0000 | 113.0085 | 114.4534 | 113.0085 | NaN | anchor_distributional | 113.0085 | 26.9915 | 26.9915 | 0.6329 | 0.7319 | 21.4505 | 15.9096 | 26.9915 | target_above_anchor | 0.3673 | 1.8182 | 1.8182 | 0.5500 | 0.3673 | 160.0000 | 45.5466 | 194.7030 | 72.0706 | 194.7030 | 72.0706 | 124.0130 | 25.0506 | 194.7030 | 72.0706 | 194.7030 | NaN | 194.7030 | NaN | NaN |
| HIST | FR | 2018-2024 | year_specific | 2 024.00 | CCGT | CCGT | gas | 68.2500 | 47.7300 | NaN | 0.5500 | 0.2020 | 3.0000 | 1.0000 | 158.5440 | 158.5440 | 158.5440 | 114.5801 | 114.8482 | 114.5801 | NaN | anchor_distributional | 114.5801 | 43.9639 | 43.9639 | 0.5684 | 0.5451 | 36.3912 | 28.8064 | 43.9759 | target_above_anchor | 0.3673 | 1.8182 | 1.8182 | 0.5500 | 0.3673 | 160.0000 | 45.1518 | 191.1881 | 72.5635 | 191.1881 | 72.5635 | 122.9381 | 24.8335 | 191.1881 | 72.5635 | 191.1881 | NaN | 191.1881 | NaN | NaN |
| HIST | IT_NORD | 2018-2024 | year_specific | 2 024.00 | CCGT | CCGT | gas | 70.8300 | 46.8000 | NaN | 0.5500 | 0.2020 | 3.0000 | 1.0000 | 157.0795 | 157.0795 | 157.0795 | 112.5586 | 114.1048 | 112.5586 | NaN | anchor_distributional | 112.5586 | 44.5209 | 44.5209 | 0.5457 | 0.5106 | 39.1519 | 33.7765 | 44.5274 | target_above_anchor | 0.3673 | 1.8182 | 1.8182 | 0.5500 | 0.3673 | 160.0000 | 45.8952 | 195.7921 | 72.0423 | 195.7921 | 72.0423 | 124.9621 | 25.2423 | 195.7921 | 72.0423 | 195.7921 | NaN | 195.7921 | NaN | NaN |
| HIST | NL | 2018-2024 | year_specific | 2 024.00 | CCGT | CCGT | gas | 70.8300 | 46.8000 | NaN | 0.5500 | 0.2020 | 3.0000 | 1.0000 | 138.9780 | 138.9780 | 138.9780 | 112.5586 | 114.1048 | 112.5586 | NaN | anchor_distributional | 112.5586 | 26.4194 | 26.4194 | 0.2888 | 0.7432 | 20.5479 | 14.6755 | 26.4204 | target_above_anchor | 0.3673 | 1.8182 | 1.8182 | 0.5500 | 0.3673 | 160.0000 | 45.8952 | 195.7921 | 72.0423 | 195.7921 | 72.0423 | 124.9621 | 25.2423 | 195.7921 | 72.0423 | 195.7921 | NaN | 195.7921 | NaN | NaN |

### Robustesse / fragilite
Statuts ledger: PASS=8, WARN=0, FAIL=0, NON_TESTABLE=0. Checks severes: 3 sur 72.
Une conclusion est dite robuste uniquement si elle est compatible avec les tests PASS dominants, sans contradiction non expliquee par des FAIL/WARN critiques.

### Risques de mauvaise lecture
- Risque 1: confondre correlation et causalite.
- Risque 2: ignorer les NON_TESTABLE et sur-vendre une conclusion.
- Risque 3: extrapoler hors perimetre pays/periode/scenario sans nouveau run.

### Reponse conclusive a la question
La reponse ci-dessus est strictement bornee aux preuves chiffrees du run courant. Lorsqu'un signal est fragile, la conclusion est formulee comme hypothese de travail et non comme fait etabli.

### Actions/priorites de decision
1. Traiter en priorite les tests FAIL et les checks severes.
2. Challenger les hypotheses prospectives qui pilotent le plus les deltas vs historique.
3. Rejouer le bundle sur perimetre elargi avant decision strategique irreversible.

### Table de tracabilite test par test
| test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | NaN | PASS | share_fini=100.00% | >=80% lignes ttl/tca finies | L'ancre thermique est quantifiable sur la majorite des pays. |
| Q5-H-02 | SPEC2-Q5 | HIST | NaN | PASS | share_positive=100.00% | 100% lignes >0 | Sensibilites analytiques globalement coherentes. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | 7 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | 7 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | 7 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. |

### References de preuve
[evidence:Q5-H-01] [evidence:Q5-H-02] [evidence:Q5-S-01] [evidence:Q5-S-02]


## 4. Annexes de preuve et tracabilite

### 4.1 Ledger complet des tests
#### Q1
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1-H-01 | Q1 | SPEC2-Q1/Slides 2-4 | HIST | HIST_BASE | Score marche de bascule | La signature marche de phase 2 est calculee et exploitable. | stage2_market_score present et non vide | HIGH | nan | PASS | 1.2244897959183674 | score present | Le score de bascule marche est exploitable. |
| Q1-H-02 | Q1 | SPEC2-Q1/Slides 3-4 | HIST | HIST_BASE | Stress physique SR/FAR/IR | La bascule physique est fondee sur SR/FAR/IR. | sr_energy/far_energy/ir_p10 presentes | CRITICAL | nan | PASS | far_energy,ir_p10,sr_energy | SR/FAR/IR presents | Le stress physique est calculable. |
| Q1-H-03 | Q1 | SPEC2-Q1 | HIST | HIST_BASE | Concordance marche vs physique | La relation entre bascule marche et bascule physique est mesurable. | bascule_year_market et bascule_year_physical comparables | MEDIUM | nan | PASS | strict=14.29%; concordant_ou_explique=100.00%; n=7; explained=7; reasons=physical_not_reached_but_explained:3;physical_already_phase2_window_start:2;both_not_reached_in_window:1;strict_equal_year:1 | concordant_ou_explique >= 80% | Concordance satisfaisante en comptant les divergences expliquees. |
| Q1-H-04 | Q1 | Slides 4-6 | HIST | HIST_BASE | Robustesse seuils | Le diagnostic reste stable sous variation raisonnable de seuils. | delta bascules sous choc de seuil <= 50% | MEDIUM | nan | WARN | 0.486 | confidence moyenne >=0.60 | Proxy de robustesse du diagnostic de bascule. |
| Q1-S-01 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Bascule projetee par scenario | Chaque scenario fournit un diagnostic de bascule projetee. | Q1_country_summary non vide en SCEN | HIGH | DEMAND_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. |
| Q1-S-01 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Bascule projetee par scenario | Chaque scenario fournit un diagnostic de bascule projetee. | Q1_country_summary non vide en SCEN | HIGH | LOW_RIGIDITY | PASS | 7 | >0 lignes | La bascule projetee est produite. |
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share) | MEDIUM | DEMAND_UP | NON_TESTABLE | nan | delta vs BASE disponible | Impossible d'evaluer la sensibilite sans BASE et scenario courant. |
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share) | MEDIUM | LOW_RIGIDITY | NON_TESTABLE | nan | delta vs BASE disponible | Impossible d'evaluer la sensibilite sans BASE et scenario courant. |
| Q1-S-03 | Q1 | SPEC2-Q1 | SCEN | DEFAULT | Qualite de causalite | Le regime_coherence respecte le seuil d'interpretation. | part regime_coherence >= seuil min | MEDIUM | DEMAND_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
| Q1-S-03 | Q1 | SPEC2-Q1 | SCEN | DEFAULT | Qualite de causalite | Le regime_coherence respecte le seuil d'interpretation. | part regime_coherence >= seuil min | MEDIUM | LOW_RIGIDITY | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |

#### Q2
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q2-H-01 | Q2 | SPEC2-Q2/Slides 10 | HIST | HIST_BASE | Pentes OLS post-bascule | Les pentes PV/Wind sont estimees en historique. | Q2_country_slopes non vide | HIGH | nan | PASS | 14 | >0 lignes | Les pentes historiques sont calculees. |
| Q2-H-02 | Q2 | SPEC2-Q2/Slides 10-12 | HIST | HIST_BASE | Robustesse statistique | R2/p-value/n sont disponibles pour qualifier la robustesse. | colonnes r2,p_value,n presentes | MEDIUM | nan | PASS | n,p_value,r2 | r2,p_value,n disponibles | La robustesse statistique est lisible. |
| Q2-H-03 | Q2 | Slides 10-13 | HIST | HIST_BASE | Drivers physiques | Les drivers SR/FAR/IR/corr VRE-load sont exploites. | driver correlations non vides | MEDIUM | nan | PASS | 4 | >0 lignes | Les drivers de pente sont disponibles. |
| Q2-S-01 | Q2 | SPEC2-Q2/Slides 11 | SCEN | DEFAULT | Pentes projetees | Les pentes sont reproduites en mode scenario. | Q2_country_slopes non vide en SCEN | HIGH | HIGH_CO2 | PASS | 14 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | Q2 | SPEC2-Q2/Slides 11 | SCEN | DEFAULT | Pentes projetees | Les pentes sont reproduites en mode scenario. | Q2_country_slopes non vide en SCEN | HIGH | HIGH_GAS | PASS | 14 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-02 | Q2 | SPEC2-Q2 | SCEN | DEFAULT | Delta pente vs BASE | Les differences de pente vs BASE sont calculables. | delta slope par pays/tech vs BASE | MEDIUM | HIGH_CO2 | WARN | finite=14.29%; robust=14.29%; reason_known=100.00% | finite_share >= 20% | Delta de pente partiellement exploitable; beaucoup de valeurs non finies. |
| Q2-S-02 | Q2 | SPEC2-Q2 | SCEN | DEFAULT | Delta pente vs BASE | Les differences de pente vs BASE sont calculables. | delta slope par pays/tech vs BASE | MEDIUM | HIGH_GAS | WARN | finite=14.29%; robust=14.29%; reason_known=100.00% | finite_share >= 20% | Delta de pente partiellement exploitable; beaucoup de valeurs non finies. |

#### Q3
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q3-H-01 | Q3 | SPEC2-Q3/Slides 16 | HIST | HIST_BASE | Tendances glissantes | Les tendances h_negative et capture_ratio sont estimees. | Q3_status non vide | HIGH | nan | PASS | 7 | >0 lignes | Les tendances historiques sont calculees. |
| Q3-H-02 | Q3 | SPEC2-Q3 | HIST | HIST_BASE | Statuts sortie phase 2 | Les statuts degradation/stabilisation/amelioration sont attribues. | status dans ensemble attendu | MEDIUM | nan | PASS | 2 | status valides | Les statuts business sont renseignes. |
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | DEMAND_UP | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | LOW_RIGIDITY | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | DEMAND_UP | WARN | hors_scope=42.86% | hors_scope < 40% | Lecture partiellement informative: forte part de cas hors scope Stage 2. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | LOW_RIGIDITY | WARN | hors_scope=42.86% | hors_scope < 40% | Lecture partiellement informative: forte part de cas hors scope Stage 2. |

#### Q4
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q4-H-01 | Q4 | SPEC2-Q4/Slides 22 | HIST | HIST_BASE | Simulation BESS 3 modes | SURPLUS_FIRST, PRICE_ARBITRAGE_SIMPLE et PV_COLOCATED sont executes. | 3 modes executes avec sorties non vides | CRITICAL | nan | PASS | HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED | 3 modes executes | Les trois modes Q4 sont disponibles. |
| Q4-H-02 | Q4 | SPEC2-Q4 | HIST | HIST_BASE | Invariants physiques BESS | Bornes SOC/puissance/energie respectees (mode physique de reference) avec garde-fous structurels sur modes alternatifs. | aucun FAIL physique/structurel pertinent | CRITICAL | nan | PASS | WARN | aucun FAIL physique | Les invariants physiques batterie sont respectes. Des avertissements non-physiques peuvent subsister (objectif/scenario). |
| Q4-S-01 | Q4 | SPEC2-Q4/Slides 23 | SCEN | DEFAULT | Comparaison effet batteries par scenario | Impact FAR/surplus/capture compare entre scenarios utiles. | Q4 summary non vide pour >=1 scenario | HIGH | HIGH_CO2 | PASS | 7 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | Q4 | SPEC2-Q4/Slides 23 | SCEN | DEFAULT | Comparaison effet batteries par scenario | Impact FAR/surplus/capture compare entre scenarios utiles. | Q4 summary non vide pour >=1 scenario | HIGH | HIGH_GAS | PASS | 7 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | HIGH_CO2 | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. |
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | HIGH_GAS | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. |

#### Q5
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q5-H-01 | Q5 | SPEC2-Q5/Slides 28 | HIST | HIST_BASE | Ancre thermique historique | TTL/TCA/alpha/corr sont estimes hors surplus. | Q5_summary non vide avec ttl_obs et tca_q95 | HIGH | nan | PASS | share_fini=100.00% | >=80% lignes ttl/tca finies | L'ancre thermique est quantifiable sur la majorite des pays. |
| Q5-H-02 | Q5 | SPEC2-Q5 | HIST | HIST_BASE | Sensibilites analytiques | dTCA/dCO2 et dTCA/dGas sont positives. | dTCA_dCO2 > 0 et dTCA_dGas > 0 | CRITICAL | nan | PASS | share_positive=100.00% | 100% lignes >0 | Sensibilites analytiques globalement coherentes. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | HIGH_CO2 | PASS | 7 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | HIGH_GAS | PASS | 7 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | HIGH_BOTH | PASS | 7 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_CO2 | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_GAS | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_BOTH | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. |

### 4.2 Checks et warnings consolides
| run_id | question_id | status | code | message | scope | scenario_id | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260212_FIX4 | Q1 | INFO | Q1_CAPTURE_ONLY_SIGNAL | BE 2020: capture-only sans low-price ni stress physique. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | Q1_CAPTURE_ONLY_SIGNAL | BE 2022: capture-only sans low-price ni stress physique. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | Q1_CAPTURE_ONLY_SIGNAL | DE 2018: capture-only sans low-price ni stress physique. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | Q1_CAPTURE_ONLY_SIGNAL | DE 2021: capture-only sans low-price ni stress physique. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | Q1_CAPTURE_ONLY_SIGNAL | DE 2022: capture-only sans low-price ni stress physique. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | Q1_CAPTURE_ONLY_SIGNAL | FR 2022: capture-only sans low-price ni stress physique. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | Q1_CAPTURE_ONLY_SIGNAL | NL 2020: capture-only sans low-price ni stress physique. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | Q1_CAPTURE_ONLY_SIGNAL | NL 2021: capture-only sans low-price ni stress physique. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | Q1_CAPTURE_ONLY_SIGNAL | NL 2022: capture-only sans low-price ni stress physique. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_Q1_001 | Toutes les lignes stage2 ont au moins un signal low-price (h_negative/h_below_5/days_spread_gt50). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | Q1_MUSTRUN_SCOPE_HIGH_COVERAGE | BE: coverage max=61.72% (>60%), possible surestimation must-run. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | Q1_MUSTRUN_SCOPE_HIGH_COVERAGE | CZ: coverage max=84.76% (>60%), possible surestimation must-run. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | Q1_MUSTRUN_SCOPE_HIGH_COVERAGE | FR: coverage max=87.11% (>60%), possible surestimation must-run. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | BE-2018: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | BE-2018: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | BE-2018: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | BE-2018: 0.0% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | BE-2018: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=963.0, p50=1143.1, p90=1639.7; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | BE-2019: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | BE-2019: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | BE-2019: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | BE-2019: 26.8% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | BE-2019: 26.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-1098.4, p50=442.5, p90=1330.8; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | BE-2020: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | BE-2020: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | BE-2020: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | BE-2020: 61.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-1170.1, p50=-331.5, p90=935.4; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | BE-2021: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | BE-2021: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | BE-2021: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | BE-2022: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | BE-2022: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | BE-2022: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | BE-2023: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | BE-2023: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | BE-2023: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | BE-2024: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | BE-2024: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | BE-2024: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | BE-2024: 65.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-1890.1, p50=-475.8, p90=1240.2; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | CZ-2018: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | CZ-2018: coverage price/load ok (99.99%/99.91%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | CZ-2018: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_IR_GT_1 | CZ-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=6181.66, p10_load_mw=5946.48. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | CZ-2018: must_run_share=79.3% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | CZ-2018: 0.0% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | CZ-2018: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=740.2, p50=973.9, p90=1568.4; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_D_NOT_ABOVE_C | CZ-2018: median(price|D) <= median(price|C). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | CZ-2019: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | CZ-2019: coverage price/load ok (99.99%/99.94%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | CZ-2019: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | CZ-2019: must_run_share=78.2% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | CZ-2019: 36.2% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | CZ-2019: 36.2% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-603.6, p50=411.4, p90=754.4; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | CZ-2020: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | CZ-2020: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | CZ-2020: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | CZ-2020: must_run_share=76.3% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | CZ-2020: 28.6% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | CZ-2020: 28.6% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-768.9, p50=241.3, p90=1210.1; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | CZ-2021: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | CZ-2021: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | CZ-2021: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | CZ-2021: must_run_share=76.1% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | CZ-2021: 0.0% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | CZ-2021: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=418.7, p50=1039.2, p90=1706.2; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | CZ-2022: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | CZ-2022: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | CZ-2022: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_IR_GT_1 | CZ-2022: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=5874.35, p10_load_mw=5645.40. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2022: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | CZ-2022: must_run_share=79.6% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | CZ-2023: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | CZ-2023: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | CZ-2023: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | CZ-2023: must_run_share=79.6% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | CZ-2023: 46.3% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | CZ-2023: 46.3% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-751.1, p50=119.7, p90=1134.0; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_D_NOT_ABOVE_C | CZ-2023: median(price|D) <= median(price|C). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | CZ-2024: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | CZ-2024: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | CZ-2024: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | CZ-2024: must_run_share=78.6% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | CZ-2024: 20.6% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | CZ-2024: 20.6% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-466.3, p50=418.8, p90=1353.6; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | DE-2018: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | DE-2018: coverage price/load ok (100.00%/99.89%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | DE-2018: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | DE-2018: 33.8% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | DE-2018: 33.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-3039.5, p50=2341.7, p90=8765.7; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | DE-2019: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | DE-2019: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | DE-2019: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | DE-2019: 44.1% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | DE-2019: 44.1% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-4050.2, p50=580.8, p90=5229.3; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | DE-2020: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | DE-2020: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | DE-2020: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | DE-2020: 36.9% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | DE-2020: 36.9% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-3662.8, p50=1184.0, p90=5399.3; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | DE-2021: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | DE-2021: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | DE-2021: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | DE-2021: 41.0% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | DE-2021: 41.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-4056.4, p50=598.4, p90=5182.9; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | DE-2022: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | DE-2022: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | DE-2022: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | DE-2023: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | DE-2023: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | DE-2023: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | DE-2024: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | DE-2024: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | DE-2024: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | ES-2018: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | ES-2018: coverage price/load ok (99.99%/99.97%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | ES-2018: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | ES-2019: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | ES-2019: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | ES-2019: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | ES-2020: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | ES-2020: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | ES-2020: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | ES-2021: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | ES-2021: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | ES-2021: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | ES-2022: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | ES-2022: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | ES-2022: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | ES-2023: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | ES-2023: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | ES-2023: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | ES-2024: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | ES-2024: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | ES-2024: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | FR-2018: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | FR-2018: coverage price/load ok (99.99%/99.79%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | FR-2018: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_IR_GT_1 | FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | FR-2018: must_run_share=82.4% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | FR-2018: 27.3% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | FR-2018: 27.3% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-7350.0, p50=375.0, p90=2173.0; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | FR-2019: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | FR-2019: coverage price/load ok (99.99%/99.90%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | FR-2019: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_IR_GT_1 | FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | FR-2019: must_run_share=80.7% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | FR-2020: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | FR-2020: coverage price/load ok (99.99%/99.97%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | FR-2020: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | FR-2020: must_run_share=77.9% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | FR-2020: 52.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-5301.0, p50=-216.0, p90=2362.8; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | FR-2021: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | FR-2021: coverage price/load ok (99.99%/99.89%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | FR-2021: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_IR_GT_1 | FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2021: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | FR-2021: must_run_share=79.4% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | FR-2022: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | FR-2022: coverage price/load ok (99.99%/99.75%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | FR-2022: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | FR-2022: must_run_share=73.5% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | FR-2023: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | FR-2023: coverage price/load ok (99.99%/99.93%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | FR-2023: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | FR-2023: must_run_share=75.9% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | FR-2024: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | FR-2024: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | FR-2024: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_IR_GT_1 | FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2024: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | FR-2024: must_run_share=79.2% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | IT_NORD-2018: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | IT_NORD-2018: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | IT_NORD-2018: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | IT_NORD-2019: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | IT_NORD-2019: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | IT_NORD-2019: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | IT_NORD-2020: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | IT_NORD-2020: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | IT_NORD-2020: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | IT_NORD-2021: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | IT_NORD-2021: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | IT_NORD-2021: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | IT_NORD-2022: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | IT_NORD-2022: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | IT_NORD-2022: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | IT_NORD-2023: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | IT_NORD-2023: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | IT_NORD-2023: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | IT_NORD-2024: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | IT_NORD-2024: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | IT_NORD-2024: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | NL-2018: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | NL-2018: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | NL-2018: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | NL-2018: must_run_share=0.0% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | NL-2019: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | NL-2019: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | NL-2019: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | NL-2019: must_run_share=0.0% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | NL-2019: 0.0% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | NL-2019: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=8995.7, p50=9175.7, p90=9192.9; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | NL-2020: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | NL-2020: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | NL-2020: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | NL-2020: must_run_share=0.1% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | NL-2020: 0.0% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | NL-2020: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6769.6, p50=7430.8, p90=8315.3; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | NL-2021: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | NL-2021: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | NL-2021: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | NL-2021: must_run_share=0.1% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | NL-2021: 0.0% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | NL-2021: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6325.9, p50=7246.4, p90=8079.5; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | NL-2022: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | NL-2022: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | NL-2022: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | NL-2022: must_run_share=0.1% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | NL-2022: 0.0% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | NL-2022: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=5037.0, p50=5902.3, p90=7074.9; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | NL-2023: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | NL-2023: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | NL-2023: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | NL-2023: must_run_share=0.2% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | NL-2023: 0.0% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | NL-2023: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6180.9, p50=8241.0, p90=10256.6; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | NL-2024: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | NL-2024: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | NL-2024: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | NL-2024: must_run_share=0.2% hors plage plausible [5%,60%]. | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | INFO | RC_NEG_NOT_IN_AB | NL-2024: 0.0% des heures negatives en regime A/B (check legacy). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL | NL-2024: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6637.0, p50=9062.7, p90=11059.5; causes=price_or_regime_mapping). | HIST |  | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | TEST_Q1_001 | Aucune ligne stage2 observee; test non applicable. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | Q1_MUSTRUN_SCOPE_HIGH_COVERAGE | BE: coverage max=80.22% (>60%), possible surestimation must-run. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | Q1_MUSTRUN_SCOPE_HIGH_COVERAGE | CZ: coverage max=89.16% (>60%), possible surestimation must-run. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | BE-2025: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | BE-2025: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | BE-2025: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | BE-2026: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | BE-2026: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | BE-2026: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | WARN | RC_MR_SHARE_IMPLAUSIBLE | BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_001 | BE-2027: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_002 | BE-2027: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |
| FULL_20260212_FIX4 | Q1 | PASS | TEST_DATA_003 | BE-2027: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX4\Q1\summary.json |

### 4.3 Tracabilite tests -> sources
| run_id | question_id | test_id | source_ref | mode | scenario_id | status | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260212_FIX4 | Q1 | Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv |
| FULL_20260212_FIX4 | Q1 | Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv |
| FULL_20260212_FIX4 | Q1 | Q1-H-03 | SPEC2-Q1 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv |
| FULL_20260212_FIX4 | Q1 | Q1-H-04 | Slides 4-6 | HIST | nan | WARN | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv |
| FULL_20260212_FIX4 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv |
| FULL_20260212_FIX4 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv |
| FULL_20260212_FIX4 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | NON_TESTABLE | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv |
| FULL_20260212_FIX4 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | NON_TESTABLE | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv |
| FULL_20260212_FIX4 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv |
| FULL_20260212_FIX4 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv |
| FULL_20260212_FIX4 | Q2 | Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv |
| FULL_20260212_FIX4 | Q2 | Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv |
| FULL_20260212_FIX4 | Q2 | Q2-H-03 | Slides 10-13 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv |
| FULL_20260212_FIX4 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv |
| FULL_20260212_FIX4 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv |
| FULL_20260212_FIX4 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv |
| FULL_20260212_FIX4 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv |
| FULL_20260212_FIX4 | Q3 | Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX4\Q3\test_ledger.csv |
| FULL_20260212_FIX4 | Q3 | Q3-H-02 | SPEC2-Q3 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX4\Q3\test_ledger.csv |
| FULL_20260212_FIX4 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260212_FIX4\Q3\test_ledger.csv |
| FULL_20260212_FIX4 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260212_FIX4\Q3\test_ledger.csv |
| FULL_20260212_FIX4 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | WARN | outputs\combined\FULL_20260212_FIX4\Q3\test_ledger.csv |
| FULL_20260212_FIX4 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | WARN | outputs\combined\FULL_20260212_FIX4\Q3\test_ledger.csv |
| FULL_20260212_FIX4 | Q4 | Q4-H-01 | SPEC2-Q4/Slides 22 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX4\Q4\test_ledger.csv |
| FULL_20260212_FIX4 | Q4 | Q4-H-02 | SPEC2-Q4 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX4\Q4\test_ledger.csv |
| FULL_20260212_FIX4 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260212_FIX4\Q4\test_ledger.csv |
| FULL_20260212_FIX4 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260212_FIX4\Q4\test_ledger.csv |
| FULL_20260212_FIX4 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260212_FIX4\Q4\test_ledger.csv |
| FULL_20260212_FIX4 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260212_FIX4\Q4\test_ledger.csv |
| FULL_20260212_FIX4 | Q5 | Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv |
| FULL_20260212_FIX4 | Q5 | Q5-H-02 | SPEC2-Q5 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv |
| FULL_20260212_FIX4 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv |
| FULL_20260212_FIX4 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv |
| FULL_20260212_FIX4 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv |
| FULL_20260212_FIX4 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv |
| FULL_20260212_FIX4 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv |
| FULL_20260212_FIX4 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv |

### 4.4 Couverture Slides/SPECS -> preuves
_Aucune ligne._

### 4.5 Catalogue de preuves
| run_id | question_id | test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260212_FIX4 | Q1 | Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | nan | PASS | 1.2244897959183674 | score present | Le score de bascule marche est exploitable. | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv#test_id=Q1-H-01 |
| FULL_20260212_FIX4 | Q1 | Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | nan | PASS | far_energy,ir_p10,sr_energy | SR/FAR/IR presents | Le stress physique est calculable. | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv#test_id=Q1-H-02 |
| FULL_20260212_FIX4 | Q1 | Q1-H-03 | SPEC2-Q1 | HIST | nan | PASS | strict=14.29%; concordant_ou_explique=100.00%; n=7; explained=7; reasons=physical_not_reached_but_explained:3;physical_already_phase2_window_start:2;both_not_reached_in_window:1;strict_equal_year:1 | concordant_ou_explique >= 80% | Concordance satisfaisante en comptant les divergences expliquees. | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv#test_id=Q1-H-03 |
| FULL_20260212_FIX4 | Q1 | Q1-H-04 | Slides 4-6 | HIST | nan | WARN | 0.486 | confidence moyenne >=0.60 | Proxy de robustesse du diagnostic de bascule. | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv#test_id=Q1-H-04 |
| FULL_20260212_FIX4 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260212_FIX4 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260212_FIX4 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | NON_TESTABLE | nan | delta vs BASE disponible | Impossible d'evaluer la sensibilite sans BASE et scenario courant. | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260212_FIX4 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | NON_TESTABLE | nan | delta vs BASE disponible | Impossible d'evaluer la sensibilite sans BASE et scenario courant. | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260212_FIX4 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260212_FIX4 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | LOW_RIGIDITY | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260212_FIX4\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260212_FIX4 | Q2 | Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | nan | PASS | 14 | >0 lignes | Les pentes historiques sont calculees. | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv#test_id=Q2-H-01 |
| FULL_20260212_FIX4 | Q2 | Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | nan | PASS | n,p_value,r2 | r2,p_value,n disponibles | La robustesse statistique est lisible. | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv#test_id=Q2-H-02 |
| FULL_20260212_FIX4 | Q2 | Q2-H-03 | Slides 10-13 | HIST | nan | PASS | 4 | >0 lignes | Les drivers de pente sont disponibles. | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv#test_id=Q2-H-03 |
| FULL_20260212_FIX4 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | 14 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260212_FIX4 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | 14 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260212_FIX4 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | finite=14.29%; robust=14.29%; reason_known=100.00% | finite_share >= 20% | Delta de pente partiellement exploitable; beaucoup de valeurs non finies. | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260212_FIX4 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | finite=14.29%; robust=14.29%; reason_known=100.00% | finite_share >= 20% | Delta de pente partiellement exploitable; beaucoup de valeurs non finies. | outputs\combined\FULL_20260212_FIX4\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260212_FIX4 | Q3 | Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | nan | PASS | 7 | >0 lignes | Les tendances historiques sont calculees. | outputs\combined\FULL_20260212_FIX4\Q3\test_ledger.csv#test_id=Q3-H-01 |
| FULL_20260212_FIX4 | Q3 | Q3-H-02 | SPEC2-Q3 | HIST | nan | PASS | 2 | status valides | Les statuts business sont renseignes. | outputs\combined\FULL_20260212_FIX4\Q3\test_ledger.csv#test_id=Q3-H-02 |
| FULL_20260212_FIX4 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. | outputs\combined\FULL_20260212_FIX4\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260212_FIX4 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. | outputs\combined\FULL_20260212_FIX4\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260212_FIX4 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | WARN | hors_scope=42.86% | hors_scope < 40% | Lecture partiellement informative: forte part de cas hors scope Stage 2. | outputs\combined\FULL_20260212_FIX4\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260212_FIX4 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | WARN | hors_scope=42.86% | hors_scope < 40% | Lecture partiellement informative: forte part de cas hors scope Stage 2. | outputs\combined\FULL_20260212_FIX4\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260212_FIX4 | Q4 | Q4-H-01 | SPEC2-Q4/Slides 22 | HIST | nan | PASS | HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED | 3 modes executes | Les trois modes Q4 sont disponibles. | outputs\combined\FULL_20260212_FIX4\Q4\test_ledger.csv#test_id=Q4-H-01 |
| FULL_20260212_FIX4 | Q4 | Q4-H-02 | SPEC2-Q4 | HIST | nan | PASS | WARN | aucun FAIL physique | Les invariants physiques batterie sont respectes. Des avertissements non-physiques peuvent subsister (objectif/scenario). | outputs\combined\FULL_20260212_FIX4\Q4\test_ledger.csv#test_id=Q4-H-02 |
| FULL_20260212_FIX4 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | 7 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260212_FIX4\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260212_FIX4 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | 7 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260212_FIX4\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260212_FIX4 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. | outputs\combined\FULL_20260212_FIX4\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260212_FIX4 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. | outputs\combined\FULL_20260212_FIX4\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260212_FIX4 | Q5 | Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | nan | PASS | share_fini=100.00% | >=80% lignes ttl/tca finies | L'ancre thermique est quantifiable sur la majorite des pays. | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv#test_id=Q5-H-01 |
| FULL_20260212_FIX4 | Q5 | Q5-H-02 | SPEC2-Q5 | HIST | nan | PASS | share_positive=100.00% | 100% lignes >0 | Sensibilites analytiques globalement coherentes. | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv#test_id=Q5-H-02 |
| FULL_20260212_FIX4 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | 7 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260212_FIX4 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | 7 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260212_FIX4 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | 7 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260212_FIX4 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260212_FIX4 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260212_FIX4 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. | outputs\combined\FULL_20260212_FIX4\Q5\test_ledger.csv#test_id=Q5-S-02 |

## 5. Ecarts restants (obligatoire)

- Logic issue: {'question_id': 'GLOBAL', 'issue': "aucun docx de slides fourni n'existe sur disque", 'slides_docx_provided_count': 2}
