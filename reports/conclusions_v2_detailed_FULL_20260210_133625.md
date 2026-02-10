# Rapport Final V2.3 - Run `FULL_20260210_133625`

## 1. Page de garde
- Date de generation: `2026-02-10 13:39:19 UTC`
- Run combine source: `outputs\combined\FULL_20260210_133625`
- Perimetre pays declare: `non renseigne`
- Fenetre historique de reference: `2018-2024`
- Horizons prospectifs de reference: `2030/2040`
- Questions couvertes: `Q1, Q2, Q3, Q4, Q5`
- Avertissement methodologique: cette analyse est empirique et scenarisee; ce n'est pas un modele d'equilibre complet.

### Scenarios executes par question
- `Q1`: BASE, DEMAND_UP, FLEX_UP, LOW_RIGIDITY
- `Q2`: BASE, HIGH_CO2, HIGH_GAS
- `Q3`: BASE, DEMAND_UP, FLEX_UP, LOW_RIGIDITY
- `Q4`: BASE, FLEX_UP, HIGH_CO2, HIGH_GAS
- `Q5`: BASE, HIGH_BOTH, HIGH_CO2, HIGH_GAS

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
16 tests ont ete executes, dont HIST=4 et SCEN=12. Repartition des statuts: PASS=15, WARN=1, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 12 ligne(s) de test scenario.

### Resultats historiques test par test
- **Q1-H-01** (HIST/nan) - Score marche de bascule. Ce test verifie: La signature marche de phase 2 est calculee et exploitable.. Regle: `stage2_market_score present et non vide`. Valeur observee: `4.1020` ; seuil/regle de comparaison: `score present` ; statut: `PASS`. Interpretation metier: Le score de bascule marche est exploitable.. Resultat conforme a la regle definie. [evidence:Q1-H-01] [source:SPEC2-Q1/Slides 2-4]
- **Q1-H-02** (HIST/nan) - Stress physique SR/FAR/IR. Ce test verifie: La bascule physique est fondee sur SR/FAR/IR.. Regle: `sr_energy/far_energy/ir_p10 presentes`. Valeur observee: `far_energy,ir_p10,sr_energy` ; seuil/regle de comparaison: `SR/FAR/IR presents` ; statut: `PASS`. Interpretation metier: Le stress physique est calculable.. Resultat conforme a la regle definie. [evidence:Q1-H-02] [source:SPEC2-Q1/Slides 3-4]
- **Q1-H-03** (HIST/nan) - Concordance marche vs physique. Ce test verifie: La relation entre bascule marche et bascule physique est mesurable.. Regle: `bascule_year_market et bascule_year_physical comparables`. Valeur observee: `42.86%` ; seuil/regle de comparaison: `>=50%` ; statut: `WARN`. Interpretation metier: Concordance mesuree entre bascules marche et physique.. Resultat exploitable avec prudence et justification explicite. [evidence:Q1-H-03] [source:SPEC2-Q1]
- **Q1-H-04** (HIST/nan) - Robustesse seuils. Ce test verifie: Le diagnostic reste stable sous variation raisonnable de seuils.. Regle: `delta bascules sous choc de seuil <= 50%`. Valeur observee: `0.9140` ; seuil/regle de comparaison: `confidence moyenne >=0.60` ; statut: `PASS`. Interpretation metier: Proxy de robustesse du diagnostic de bascule.. Resultat conforme a la regle definie. [evidence:Q1-H-04] [source:Slides 4-6]

### Resultats prospectifs test par test (par scenario)
#### Scenario `BASE`
- **Q1-S-01** (SCEN/BASE) - Bascule projetee par scenario. Ce test verifie: Chaque scenario fournit un diagnostic de bascule projetee.. Regle: `Q1_country_summary non vide en SCEN`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: La bascule projetee est produite.. Resultat conforme a la regle definie. [evidence:Q1-S-01] [source:SPEC2-Q1/Slides 5]
- **Q1-S-02** (SCEN/BASE) - Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY. Ce test verifie: Les leviers scenario modifient la bascule vs BASE.. Regle: `delta bascule_year_market vs BASE calculable`. Valeur observee: `4.0000` ; seuil/regle de comparaison: `>=1 bascule` ; statut: `PASS`. Interpretation metier: Le scenario fournit une variation exploitable.. Resultat conforme a la regle definie. [evidence:Q1-S-02] [source:SPEC2-Q1/Slides 5]
- **Q1-S-03** (SCEN/BASE) - Qualite de causalite. Ce test verifie: Le regime_coherence respecte le seuil d'interpretation.. Regle: `part regime_coherence >= seuil min`. Valeur observee: `100.00%` ; seuil/regle de comparaison: `>=50% lignes >=0.55` ; statut: `PASS`. Interpretation metier: La coherence scenario est lisible.. Resultat conforme a la regle definie. [evidence:Q1-S-03] [source:SPEC2-Q1]
#### Scenario `DEMAND_UP`
- **Q1-S-01** (SCEN/DEMAND_UP) - Bascule projetee par scenario. Ce test verifie: Chaque scenario fournit un diagnostic de bascule projetee.. Regle: `Q1_country_summary non vide en SCEN`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: La bascule projetee est produite.. Resultat conforme a la regle definie. [evidence:Q1-S-01] [source:SPEC2-Q1/Slides 5]
- **Q1-S-02** (SCEN/DEMAND_UP) - Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY. Ce test verifie: Les leviers scenario modifient la bascule vs BASE.. Regle: `delta bascule_year_market vs BASE calculable`. Valeur observee: `4.0000` ; seuil/regle de comparaison: `>=1 bascule` ; statut: `PASS`. Interpretation metier: Le scenario fournit une variation exploitable.. Resultat conforme a la regle definie. [evidence:Q1-S-02] [source:SPEC2-Q1/Slides 5]
- **Q1-S-03** (SCEN/DEMAND_UP) - Qualite de causalite. Ce test verifie: Le regime_coherence respecte le seuil d'interpretation.. Regle: `part regime_coherence >= seuil min`. Valeur observee: `100.00%` ; seuil/regle de comparaison: `>=50% lignes >=0.55` ; statut: `PASS`. Interpretation metier: La coherence scenario est lisible.. Resultat conforme a la regle definie. [evidence:Q1-S-03] [source:SPEC2-Q1]
#### Scenario `FLEX_UP`
- **Q1-S-01** (SCEN/FLEX_UP) - Bascule projetee par scenario. Ce test verifie: Chaque scenario fournit un diagnostic de bascule projetee.. Regle: `Q1_country_summary non vide en SCEN`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: La bascule projetee est produite.. Resultat conforme a la regle definie. [evidence:Q1-S-01] [source:SPEC2-Q1/Slides 5]
- **Q1-S-02** (SCEN/FLEX_UP) - Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY. Ce test verifie: Les leviers scenario modifient la bascule vs BASE.. Regle: `delta bascule_year_market vs BASE calculable`. Valeur observee: `4.0000` ; seuil/regle de comparaison: `>=1 bascule` ; statut: `PASS`. Interpretation metier: Le scenario fournit une variation exploitable.. Resultat conforme a la regle definie. [evidence:Q1-S-02] [source:SPEC2-Q1/Slides 5]
- **Q1-S-03** (SCEN/FLEX_UP) - Qualite de causalite. Ce test verifie: Le regime_coherence respecte le seuil d'interpretation.. Regle: `part regime_coherence >= seuil min`. Valeur observee: `100.00%` ; seuil/regle de comparaison: `>=50% lignes >=0.55` ; statut: `PASS`. Interpretation metier: La coherence scenario est lisible.. Resultat conforme a la regle definie. [evidence:Q1-S-03] [source:SPEC2-Q1]
#### Scenario `LOW_RIGIDITY`
- **Q1-S-01** (SCEN/LOW_RIGIDITY) - Bascule projetee par scenario. Ce test verifie: Chaque scenario fournit un diagnostic de bascule projetee.. Regle: `Q1_country_summary non vide en SCEN`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: La bascule projetee est produite.. Resultat conforme a la regle definie. [evidence:Q1-S-01] [source:SPEC2-Q1/Slides 5]
- **Q1-S-02** (SCEN/LOW_RIGIDITY) - Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY. Ce test verifie: Les leviers scenario modifient la bascule vs BASE.. Regle: `delta bascule_year_market vs BASE calculable`. Valeur observee: `4.0000` ; seuil/regle de comparaison: `>=1 bascule` ; statut: `PASS`. Interpretation metier: Le scenario fournit une variation exploitable.. Resultat conforme a la regle definie. [evidence:Q1-S-02] [source:SPEC2-Q1/Slides 5]
- **Q1-S-03** (SCEN/LOW_RIGIDITY) - Qualite de causalite. Ce test verifie: Le regime_coherence respecte le seuil d'interpretation.. Regle: `part regime_coherence >= seuil min`. Valeur observee: `100.00%` ; seuil/regle de comparaison: `>=50% lignes >=0.55` ; statut: `PASS`. Interpretation metier: La coherence scenario est lisible.. Resultat conforme a la regle definie. [evidence:Q1-S-03] [source:SPEC2-Q1]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 28 ligne(s), 1 metrique(s) et 4 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| bascule_year_market | BASE | 4.0000 | 11.2500 | 11.5000 | 10.0000 | 12.0000 |
| bascule_year_market | DEMAND_UP | 4.0000 | 11.2500 | 11.5000 | 10.0000 | 12.0000 |
| bascule_year_market | FLEX_UP | 4.0000 | 11.2500 | 11.5000 | 10.0000 | 12.0000 |
| bascule_year_market | LOW_RIGIDITY | 4.0000 | 11.2500 | 11.5000 | 10.0000 | 12.0000 |

Historique Q1: 7 pays avec bascule analysee; confiance moyenne=0.9143.
Synthese scenario Q1:
| scenario_id | countries | mean_bascule_year_market | mean_bascule_confidence |
| --- | --- | --- | --- |
| BASE | 7.0000 | 2 030.00 | 0.5714 |
| DEMAND_UP | 7.0000 | 2 030.00 | 0.5714 |
| FLEX_UP | 7.0000 | 2 030.00 | 0.5714 |
| LOW_RIGIDITY | 7.0000 | 2 030.00 | 0.5714 |

### Robustesse / fragilite
Statuts ledger: PASS=15, WARN=1, FAIL=0, NON_TESTABLE=0. Checks severes: 16 sur 20.
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
| Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | NaN | PASS | 4.1020408163265305 | score present | Le score de bascule marche est exploitable. |
| Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | NaN | PASS | far_energy,ir_p10,sr_energy | SR/FAR/IR presents | Le stress physique est calculable. |
| Q1-H-03 | SPEC2-Q1 | HIST | NaN | WARN | 42.86% | >=50% | Concordance mesuree entre bascules marche et physique. |
| Q1-H-04 | Slides 4-6 | HIST | NaN | PASS | 0.914 | confidence moyenne >=0.60 | Proxy de robustesse du diagnostic de bascule. |
| Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | 7 | >0 lignes | La bascule projetee est produite. |
| Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. |
| Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. |
| Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 7 | >0 lignes | La bascule projetee est produite. |
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-03 | SPEC2-Q1 | SCEN | BASE | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
| Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
| Q1-S-03 | SPEC2-Q1 | SCEN | FLEX_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
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
9 tests ont ete executes, dont HIST=3 et SCEN=6. Repartition des statuts: PASS=6, WARN=3, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 6 ligne(s) de test scenario.

### Resultats historiques test par test
- **Q2-H-01** (HIST/nan) - Pentes OLS post-bascule. Ce test verifie: Les pentes PV/Wind sont estimees en historique.. Regle: `Q2_country_slopes non vide`. Valeur observee: `14.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Les pentes historiques sont calculees.. Resultat conforme a la regle definie. [evidence:Q2-H-01] [source:SPEC2-Q2/Slides 10]
- **Q2-H-02** (HIST/nan) - Robustesse statistique. Ce test verifie: R2/p-value/n sont disponibles pour qualifier la robustesse.. Regle: `colonnes r2,p_value,n presentes`. Valeur observee: `n,p_value,r2` ; seuil/regle de comparaison: `r2,p_value,n disponibles` ; statut: `PASS`. Interpretation metier: La robustesse statistique est lisible.. Resultat conforme a la regle definie. [evidence:Q2-H-02] [source:SPEC2-Q2/Slides 10-12]
- **Q2-H-03** (HIST/nan) - Drivers physiques. Ce test verifie: Les drivers SR/FAR/IR/corr VRE-load sont exploites.. Regle: `driver correlations non vides`. Valeur observee: `6.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Les drivers de pente sont disponibles.. Resultat conforme a la regle definie. [evidence:Q2-H-03] [source:Slides 10-13]

### Resultats prospectifs test par test (par scenario)
#### Scenario `BASE`
- **Q2-S-01** (SCEN/BASE) - Pentes projetees. Ce test verifie: Les pentes sont reproduites en mode scenario.. Regle: `Q2_country_slopes non vide en SCEN`. Valeur observee: `8.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Pentes prospectives calculees.. Resultat conforme a la regle definie. [evidence:Q2-S-01] [source:SPEC2-Q2/Slides 11]
- **Q2-S-02** (SCEN/BASE) - Delta pente vs BASE. Ce test verifie: Les differences de pente vs BASE sont calculables.. Regle: `delta slope par pays/tech vs BASE`. Valeur observee: `0.00%` ; seuil/regle de comparaison: `>=30% robustes` ; statut: `WARN`. Interpretation metier: Delta de pente interpretable avec robustesse.. Resultat exploitable avec prudence et justification explicite. [evidence:Q2-S-02] [source:SPEC2-Q2]
#### Scenario `HIGH_CO2`
- **Q2-S-01** (SCEN/HIGH_CO2) - Pentes projetees. Ce test verifie: Les pentes sont reproduites en mode scenario.. Regle: `Q2_country_slopes non vide en SCEN`. Valeur observee: `8.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Pentes prospectives calculees.. Resultat conforme a la regle definie. [evidence:Q2-S-01] [source:SPEC2-Q2/Slides 11]
- **Q2-S-02** (SCEN/HIGH_CO2) - Delta pente vs BASE. Ce test verifie: Les differences de pente vs BASE sont calculables.. Regle: `delta slope par pays/tech vs BASE`. Valeur observee: `0.00%` ; seuil/regle de comparaison: `>=30% robustes` ; statut: `WARN`. Interpretation metier: Delta de pente interpretable avec robustesse.. Resultat exploitable avec prudence et justification explicite. [evidence:Q2-S-02] [source:SPEC2-Q2]
#### Scenario `HIGH_GAS`
- **Q2-S-01** (SCEN/HIGH_GAS) - Pentes projetees. Ce test verifie: Les pentes sont reproduites en mode scenario.. Regle: `Q2_country_slopes non vide en SCEN`. Valeur observee: `8.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Pentes prospectives calculees.. Resultat conforme a la regle definie. [evidence:Q2-S-01] [source:SPEC2-Q2/Slides 11]
- **Q2-S-02** (SCEN/HIGH_GAS) - Delta pente vs BASE. Ce test verifie: Les differences de pente vs BASE sont calculables.. Regle: `delta slope par pays/tech vs BASE`. Valeur observee: `0.00%` ; seuil/regle de comparaison: `>=30% robustes` ; statut: `WARN`. Interpretation metier: Delta de pente interpretable avec robustesse.. Resultat exploitable avec prudence et justification explicite. [evidence:Q2-S-02] [source:SPEC2-Q2]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 24 ligne(s), 1 metrique(s) et 3 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| slope | BASE | 2.0000 | -11.6568 | -11.6568 | -17.2080 | -6.1055 |
| slope | HIGH_CO2 | 2.0000 | -11.8080 | -11.8080 | -17.3414 | -6.2745 |
| slope | HIGH_GAS | 2.0000 | -11.6396 | -11.6396 | -17.1415 | -6.1377 |

Distribution des pentes historiques par techno:
| tech | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- |
| PV | 7.0000 | -9.6775 | -3.0701 | -48.4269 | -0.8261 |
| WIND | 7.0000 | 3.1074 | -0.7863 | -6.5245 | 18.7563 |

### Robustesse / fragilite
Statuts ledger: PASS=6, WARN=3, FAIL=0, NON_TESTABLE=0. Checks severes: 40 sur 48.
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
| Q2-H-03 | Slides 10-13 | HIST | NaN | PASS | 6 | >0 lignes | Les drivers de pente sont disponibles. |
| Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | BASE | PASS | 8 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | 8 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | 8 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-02 | SPEC2-Q2 | SCEN | BASE | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. |
| Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. |
| Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. |

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
10 tests ont ete executes, dont HIST=2 et SCEN=8. Repartition des statuts: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 8 ligne(s) de test scenario.

### Resultats historiques test par test
- **Q3-H-01** (HIST/nan) - Tendances glissantes. Ce test verifie: Les tendances h_negative et capture_ratio sont estimees.. Regle: `Q3_status non vide`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Les tendances historiques sont calculees.. Resultat conforme a la regle definie. [evidence:Q3-H-01] [source:SPEC2-Q3/Slides 16]
- **Q3-H-02** (HIST/nan) - Statuts sortie phase 2. Ce test verifie: Les statuts degradation/stabilisation/amelioration sont attribues.. Regle: `status dans ensemble attendu`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `status valides` ; statut: `PASS`. Interpretation metier: Les statuts business sont renseignes.. Resultat conforme a la regle definie. [evidence:Q3-H-02] [source:SPEC2-Q3]

### Resultats prospectifs test par test (par scenario)
#### Scenario `BASE`
- **Q3-S-01** (SCEN/BASE) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `colonnes inversion presentes` ; statut: `PASS`. Interpretation metier: Les ordres de grandeur d'inversion sont quantifies.. Resultat conforme a la regle definie. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/BASE) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `status renseignes` ; statut: `PASS`. Interpretation metier: La lecture de transition phase 3 est possible.. Resultat conforme a la regle definie. [evidence:Q3-S-02] [source:Slides 17-19]
#### Scenario `DEMAND_UP`
- **Q3-S-01** (SCEN/DEMAND_UP) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `colonnes inversion presentes` ; statut: `PASS`. Interpretation metier: Les ordres de grandeur d'inversion sont quantifies.. Resultat conforme a la regle definie. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/DEMAND_UP) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `status renseignes` ; statut: `PASS`. Interpretation metier: La lecture de transition phase 3 est possible.. Resultat conforme a la regle definie. [evidence:Q3-S-02] [source:Slides 17-19]
#### Scenario `FLEX_UP`
- **Q3-S-01** (SCEN/FLEX_UP) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `colonnes inversion presentes` ; statut: `PASS`. Interpretation metier: Les ordres de grandeur d'inversion sont quantifies.. Resultat conforme a la regle definie. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/FLEX_UP) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `status renseignes` ; statut: `PASS`. Interpretation metier: La lecture de transition phase 3 est possible.. Resultat conforme a la regle definie. [evidence:Q3-S-02] [source:Slides 17-19]
#### Scenario `LOW_RIGIDITY`
- **Q3-S-01** (SCEN/LOW_RIGIDITY) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `colonnes inversion presentes` ; statut: `PASS`. Interpretation metier: Les ordres de grandeur d'inversion sont quantifies.. Resultat conforme a la regle definie. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/LOW_RIGIDITY) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `status renseignes` ; statut: `PASS`. Interpretation metier: La lecture de transition phase 3 est possible.. Resultat conforme a la regle definie. [evidence:Q3-S-02] [source:Slides 17-19]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 56 ligne(s), 2 metrique(s) et 4 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| inversion_k_demand | BASE | 7.0000 | -0.0942 | -0.0583 | -0.2786 | 0.0000 |
| inversion_k_demand | DEMAND_UP | 7.0000 | -0.0942 | -0.0583 | -0.2786 | 0.0000 |
| inversion_k_demand | FLEX_UP | 7.0000 | -0.0942 | -0.0583 | -0.2786 | 0.0000 |
| inversion_k_demand | LOW_RIGIDITY | 7.0000 | -0.0942 | -0.0583 | -0.2786 | 0.0000 |
| inversion_r_mustrun | BASE | 7.0000 | -0.1703 | -0.1264 | -0.5332 | 0.0000 |
| inversion_r_mustrun | DEMAND_UP | 7.0000 | -0.1703 | -0.1264 | -0.5332 | 0.0000 |
| inversion_r_mustrun | FLEX_UP | 7.0000 | -0.1703 | -0.1264 | -0.5332 | 0.0000 |
| inversion_r_mustrun | LOW_RIGIDITY | 7.0000 | -0.1703 | -0.1264 | -0.5332 | 0.0000 |

Distribution des statuts historiques Q3:
| status | n |
| --- | --- |
| degradation | 6.0000 |
| hors_scope_stage2 | 1.0000 |

### Robustesse / fragilite
Statuts ledger: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Checks severes: 4 sur 40.
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
| Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | NaN | PASS | 7.0000 | >0 lignes | Les tendances historiques sont calculees. |
| Q3-H-02 | SPEC2-Q3 | HIST | NaN | PASS | 2.0000 | status valides | Les statuts business sont renseignes. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | BASE | PASS | 7.0000 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | PASS | 7.0000 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | FLEX_UP | PASS | 7.0000 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | PASS | 7.0000 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-02 | Slides 17-19 | SCEN | BASE | PASS | 2.0000 | status renseignes | La lecture de transition phase 3 est possible. |
| Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | PASS | 1.0000 | status renseignes | La lecture de transition phase 3 est possible. |
| Q3-S-02 | Slides 17-19 | SCEN | FLEX_UP | PASS | 2.0000 | status renseignes | La lecture de transition phase 3 est possible. |
| Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | PASS | 1.0000 | status renseignes | La lecture de transition phase 3 est possible. |

### References de preuve
[evidence:Q3-H-01] [evidence:Q3-H-02] [evidence:Q3-S-01] [evidence:Q3-S-02]

## Q4 - Analyse detaillee

### Question business
Quantifier l'effet des batteries sous angle systeme et sous angle actif PV, avec verification stricte des invariants physiques.

### Definitions operationnelles
- SURPLUS_FIRST cible d'abord l'absorption du surplus systeme.
- PRICE_ARBITRAGE_SIMPLE fournit une lecture economique simplifiee de l'actif batterie.
- PV_COLOCATED mesure le gain de valeur d'un couple PV + batterie.

### Perimetre des tests executes
Le perimetre couvre `perimetre du run` et un run combine unique. Les resultats historiques et prospectifs sont presentes separement puis compares.
10 tests ont ete executes, dont HIST=2 et SCEN=8. Repartition des statuts: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 8 ligne(s) de test scenario.

### Resultats historiques test par test
- **Q4-H-01** (HIST/nan) - Simulation BESS 3 modes. Ce test verifie: SURPLUS_FIRST, PRICE_ARBITRAGE_SIMPLE et PV_COLOCATED sont executes.. Regle: `3 modes executes avec sorties non vides`. Valeur observee: `HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED` ; seuil/regle de comparaison: `3 modes executes` ; statut: `PASS`. Interpretation metier: Les trois modes Q4 sont disponibles.. Resultat conforme a la regle definie. [evidence:Q4-H-01] [source:SPEC2-Q4/Slides 22]
- **Q4-H-02** (HIST/nan) - Invariants physiques BESS. Ce test verifie: Bornes SOC/puissance/energie respectees.. Regle: `aucun check FAIL Q4`. Valeur observee: `PASS` ; seuil/regle de comparaison: `pas de FAIL` ; statut: `PASS`. Interpretation metier: Les invariants physiques batterie sont respectes.. Resultat conforme a la regle definie. [evidence:Q4-H-02] [source:SPEC2-Q4]

### Resultats prospectifs test par test (par scenario)
#### Scenario `BASE`
- **Q4-S-01** (SCEN/BASE) - Comparaison effet batteries par scenario. Ce test verifie: Impact FAR/surplus/capture compare entre scenarios utiles.. Regle: `Q4 summary non vide pour >=1 scenario`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Resultats Q4 prospectifs disponibles.. Resultat conforme a la regle definie. [evidence:Q4-S-01] [source:SPEC2-Q4/Slides 23]
- **Q4-S-02** (SCEN/BASE) - Sensibilite valeur commodites. Ce test verifie: Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.. Regle: `delta pv_capture ou revenus vs BASE`. Valeur observee: `141.4176` ; seuil/regle de comparaison: `capture apres finite` ; statut: `PASS`. Interpretation metier: Sensibilite valeur exploitable.. Resultat conforme a la regle definie. [evidence:Q4-S-02] [source:Slides 23-25]
#### Scenario `FLEX_UP`
- **Q4-S-01** (SCEN/FLEX_UP) - Comparaison effet batteries par scenario. Ce test verifie: Impact FAR/surplus/capture compare entre scenarios utiles.. Regle: `Q4 summary non vide pour >=1 scenario`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Resultats Q4 prospectifs disponibles.. Resultat conforme a la regle definie. [evidence:Q4-S-01] [source:SPEC2-Q4/Slides 23]
- **Q4-S-02** (SCEN/FLEX_UP) - Sensibilite valeur commodites. Ce test verifie: Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.. Regle: `delta pv_capture ou revenus vs BASE`. Valeur observee: `141.3928` ; seuil/regle de comparaison: `capture apres finite` ; statut: `PASS`. Interpretation metier: Sensibilite valeur exploitable.. Resultat conforme a la regle definie. [evidence:Q4-S-02] [source:Slides 23-25]
#### Scenario `HIGH_CO2`
- **Q4-S-01** (SCEN/HIGH_CO2) - Comparaison effet batteries par scenario. Ce test verifie: Impact FAR/surplus/capture compare entre scenarios utiles.. Regle: `Q4 summary non vide pour >=1 scenario`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Resultats Q4 prospectifs disponibles.. Resultat conforme a la regle definie. [evidence:Q4-S-01] [source:SPEC2-Q4/Slides 23]
- **Q4-S-02** (SCEN/HIGH_CO2) - Sensibilite valeur commodites. Ce test verifie: Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.. Regle: `delta pv_capture ou revenus vs BASE`. Valeur observee: `146.5826` ; seuil/regle de comparaison: `capture apres finite` ; statut: `PASS`. Interpretation metier: Sensibilite valeur exploitable.. Resultat conforme a la regle definie. [evidence:Q4-S-02] [source:Slides 23-25]
#### Scenario `HIGH_GAS`
- **Q4-S-01** (SCEN/HIGH_GAS) - Comparaison effet batteries par scenario. Ce test verifie: Impact FAR/surplus/capture compare entre scenarios utiles.. Regle: `Q4 summary non vide pour >=1 scenario`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Resultats Q4 prospectifs disponibles.. Resultat conforme a la regle definie. [evidence:Q4-S-01] [source:SPEC2-Q4/Slides 23]
- **Q4-S-02** (SCEN/HIGH_GAS) - Sensibilite valeur commodites. Ce test verifie: Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.. Regle: `delta pv_capture ou revenus vs BASE`. Valeur observee: `152.5750` ; seuil/regle de comparaison: `capture apres finite` ; statut: `PASS`. Interpretation metier: Sensibilite valeur exploitable.. Resultat conforme a la regle definie. [evidence:Q4-S-02] [source:Slides 23-25]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 14 ligne(s), 3 metrique(s) et 6 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| far_after | BASE | 0.0000 | NaN | NaN | NaN | NaN |
| far_after | FLEX_UP | 0.0000 | NaN | NaN | NaN | NaN |
| far_after | HIGH_CO2 | 0.0000 | NaN | NaN | NaN | NaN |
| far_after | HIGH_GAS | 0.0000 | NaN | NaN | NaN | NaN |
| far_after | HIST_PRICE_ARBITRAGE_SIMPLE | 1.0000 | -0.0349 | -0.0349 | -0.0349 | -0.0349 |
| far_after | HIST_PV_COLOCATED | 1.0000 | -0.0600 | -0.0600 | -0.0600 | -0.0600 |
| pv_capture_price_after | BASE | 1.0000 | 102.1697 | 102.1697 | 102.1697 | 102.1697 |
| pv_capture_price_after | FLEX_UP | 1.0000 | 102.1448 | 102.1448 | 102.1448 | 102.1448 |
| pv_capture_price_after | HIGH_CO2 | 1.0000 | 107.3346 | 107.3346 | 107.3346 | 107.3346 |
| pv_capture_price_after | HIGH_GAS | 1.0000 | 113.3270 | 113.3270 | 113.3270 | 113.3270 |
| surplus_unabs_energy_after | BASE | 1.0000 | -2.1003 | -2.1003 | -2.1003 | -2.1003 |
| surplus_unabs_energy_after | FLEX_UP | 1.0000 | -2.1003 | -2.1003 | -2.1003 | -2.1003 |
| surplus_unabs_energy_after | HIGH_CO2 | 1.0000 | -2.1003 | -2.1003 | -2.1003 | -2.1003 |
| surplus_unabs_energy_after | HIGH_GAS | 1.0000 | -2.1003 | -2.1003 | -2.1003 | -2.1003 |

Synthese sizing historique Q4:
| country | year | dispatch_mode | objective | required_bess_power_mw | required_bess_energy_mwh | required_bess_duration_h | far_before | far_after | surplus_unabs_energy_before | surplus_unabs_energy_after | pv_capture_price_before | pv_capture_price_after | revenue_bess_price_taker | soc_min | soc_max | charge_max | discharge_max | charge_sum_mwh | discharge_sum_mwh | initial_deliverable_mwh | engine_version | compute_time_sec | cache_hit | notes_quality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR | 2 024.00 | SURPLUS_FIRST | FAR_TARGET | 6 000.00 | 48 000.00 | 8.0000 | 0.7911 | 0.9656 | 12.7375 | 2.1003 | 39.2480 | 39.2480 | 355 296 205.8 | 0.0000 | 48 000.00 | 6 000.00 | 6 000.00 | 10 637 245.9 | 9 382 611.2 | 22 514.00 | v2.1.0 | 1.5958 | 1.0000 | ok |
Apercu frontiere historique Q4:
| dispatch_mode | required_bess_power_mw | required_bess_duration_h | far_after | surplus_unabs_energy_after | pv_capture_price_after |
| --- | --- | --- | --- | --- | --- |
| SURPLUS_FIRST | 0.0000 | 1.0000 | 0.7911 | 12.7375 | 39.2480 |
| SURPLUS_FIRST | 0.0000 | 2.0000 | 0.7911 | 12.7375 | 39.2480 |
| SURPLUS_FIRST | 0.0000 | 4.0000 | 0.7911 | 12.7375 | 39.2480 |
| SURPLUS_FIRST | 0.0000 | 6.0000 | 0.7911 | 12.7375 | 39.2480 |
| SURPLUS_FIRST | 0.0000 | 8.0000 | 0.7911 | 12.7375 | 39.2480 |
| SURPLUS_FIRST | 0.0000 | 10.0000 | 0.7911 | 12.7375 | 39.2480 |
| SURPLUS_FIRST | 200.0000 | 1.0000 | 0.7922 | 12.6718 | 39.2480 |
| SURPLUS_FIRST | 200.0000 | 2.0000 | 0.7932 | 12.6068 | 39.2480 |
| SURPLUS_FIRST | 200.0000 | 4.0000 | 0.7953 | 12.4801 | 39.2480 |
| SURPLUS_FIRST | 200.0000 | 6.0000 | 0.7973 | 12.3613 | 39.2480 |
| SURPLUS_FIRST | 200.0000 | 8.0000 | 0.7991 | 12.2510 | 39.2480 |
| SURPLUS_FIRST | 200.0000 | 10.0000 | 0.8007 | 12.1508 | 39.2480 |
| SURPLUS_FIRST | 500.0000 | 1.0000 | 0.7938 | 12.5742 | 39.2480 |
| SURPLUS_FIRST | 500.0000 | 2.0000 | 0.7964 | 12.4122 | 39.2480 |
| SURPLUS_FIRST | 500.0000 | 4.0000 | 0.8016 | 12.0966 | 39.2480 |
| SURPLUS_FIRST | 500.0000 | 6.0000 | 0.8064 | 11.8042 | 39.2480 |
| SURPLUS_FIRST | 500.0000 | 8.0000 | 0.8109 | 11.5325 | 39.2480 |
| SURPLUS_FIRST | 500.0000 | 10.0000 | 0.8149 | 11.2879 | 39.2480 |
| SURPLUS_FIRST | 1 000.00 | 1.0000 | 0.7964 | 12.4136 | 39.2480 |
| SURPLUS_FIRST | 1 000.00 | 2.0000 | 0.8017 | 12.0914 | 39.2480 |
| SURPLUS_FIRST | 1 000.00 | 4.0000 | 0.8119 | 11.4694 | 39.2480 |
| SURPLUS_FIRST | 1 000.00 | 6.0000 | 0.8213 | 10.8950 | 39.2480 |
| SURPLUS_FIRST | 1 000.00 | 8.0000 | 0.8299 | 10.3711 | 39.2480 |
| SURPLUS_FIRST | 1 000.00 | 10.0000 | 0.8376 | 9.9053 | 39.2480 |
| SURPLUS_FIRST | 2 000.00 | 1.0000 | 0.8016 | 12.0964 | 39.2480 |
| SURPLUS_FIRST | 2 000.00 | 2.0000 | 0.8119 | 11.4688 | 39.2480 |
| SURPLUS_FIRST | 2 000.00 | 4.0000 | 0.8318 | 10.2550 | 39.2480 |
| SURPLUS_FIRST | 2 000.00 | 6.0000 | 0.8496 | 9.1702 | 39.2480 |
| SURPLUS_FIRST | 2 000.00 | 8.0000 | 0.8654 | 8.2063 | 39.2480 |
| SURPLUS_FIRST | 2 000.00 | 10.0000 | 0.8794 | 7.3511 | 39.2480 |

### Robustesse / fragilite
Statuts ledger: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Checks severes: 0 sur 6.
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
| Q4-H-02 | SPEC2-Q4 | HIST | NaN | PASS | PASS | pas de FAIL | Les invariants physiques batterie sont respectes. |
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | BASE | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | FLEX_UP | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-02 | Slides 23-25 | SCEN | BASE | PASS | 141.4176326086802 | capture apres finite | Sensibilite valeur exploitable. |
| Q4-S-02 | Slides 23-25 | SCEN | FLEX_UP | PASS | 141.39276677627964 | capture apres finite | Sensibilite valeur exploitable. |
| Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | 146.5825566444785 | capture apres finite | Sensibilite valeur exploitable. |
| Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | 152.5749842611698 | capture apres finite | Sensibilite valeur exploitable. |

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
10 tests ont ete executes, dont HIST=2 et SCEN=8. Repartition des statuts: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 8 ligne(s) de test scenario.

### Resultats historiques test par test
- **Q5-H-01** (HIST/nan) - Ancre thermique historique. Ce test verifie: TTL/TCA/alpha/corr sont estimes hors surplus.. Regle: `Q5_summary non vide avec ttl_obs et tca_q95`. Valeur observee: `ttl=419.95, tca=370.83959999999996` ; seuil/regle de comparaison: `ttl/tca finis` ; statut: `PASS`. Interpretation metier: L'ancre thermique est quantifiable.. Resultat conforme a la regle definie. [evidence:Q5-H-01] [source:SPEC2-Q5/Slides 28]
- **Q5-H-02** (HIST/nan) - Sensibilites analytiques. Ce test verifie: dTCA/dCO2 et dTCA/dGas sont positives.. Regle: `dTCA_dCO2 > 0 et dTCA_dGas > 0`. Valeur observee: `dCO2=0.36727272727272725, dGas=1.8181818181818181` ; seuil/regle de comparaison: `>0` ; statut: `PASS`. Interpretation metier: Sensibilites analytiques coherentes.. Resultat conforme a la regle definie. [evidence:Q5-H-02] [source:SPEC2-Q5]

### Resultats prospectifs test par test (par scenario)
#### Scenario `BASE`
- **Q5-S-01** (SCEN/BASE) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/BASE) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `138.0055` ; seuil/regle de comparaison: `valeur finie` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]
#### Scenario `HIGH_BOTH`
- **Q5-S-01** (SCEN/HIGH_BOTH) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/HIGH_BOTH) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `193.0055` ; seuil/regle de comparaison: `valeur finie` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]
#### Scenario `HIGH_CO2`
- **Q5-S-01** (SCEN/HIGH_CO2) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/HIGH_CO2) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `174.1047` ; seuil/regle de comparaison: `valeur finie` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]
#### Scenario `HIGH_GAS`
- **Q5-S-01** (SCEN/HIGH_GAS) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/HIGH_GAS) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `96.9935` ; seuil/regle de comparaison: `valeur finie` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 12 ligne(s), 3 metrique(s) et 4 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| co2_required_base | BASE | 1.0000 | 669.9892 | 669.9892 | 669.9892 | 669.9892 |
| co2_required_base | HIGH_BOTH | 1.0000 | 724.9892 | 724.9892 | 724.9892 | 724.9892 |
| co2_required_base | HIGH_CO2 | 1.0000 | 706.0884 | 706.0884 | 706.0884 | 706.0884 |
| co2_required_base | HIGH_GAS | 1.0000 | 628.9773 | 628.9773 | 628.9773 | 628.9773 |
| tca_q95 | BASE | 1.0000 | -240.1669 | -240.1669 | -240.1669 | -240.1669 |
| tca_q95 | HIGH_BOTH | 1.0000 | -176.3305 | -176.3305 | -176.3305 | -176.3305 |
| tca_q95 | HIGH_CO2 | 1.0000 | -219.9669 | -219.9669 | -219.9669 | -219.9669 |
| tca_q95 | HIGH_GAS | 1.0000 | -196.5305 | -196.5305 | -196.5305 | -196.5305 |
| ttl_obs | BASE | 1.0000 | -230.2356 | -230.2356 | -230.2356 | -230.2356 |
| ttl_obs | HIGH_BOTH | 1.0000 | -230.2356 | -230.2356 | -230.2356 | -230.2356 |
| ttl_obs | HIGH_CO2 | 1.0000 | -223.2939 | -223.2939 | -223.2939 | -223.2939 |
| ttl_obs | HIGH_GAS | 1.0000 | -215.1731 | -215.1731 | -215.1731 | -215.1731 |

Synthese historique Q5:
| country | year_range_used | marginal_tech | ttl_obs | tca_q95 | alpha | corr_cd | dTCA_dCO2 | dTCA_dGas | ttl_target | co2_required_base | co2_required_gas_override | warnings_quality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR | 2018-2024 | CCGT | 419.9500 | 370.8396 | 49.1104 | 0.9082 | 0.3673 | 1.8182 | 200.0000 | -531.9838 | NaN | NaN |

### Robustesse / fragilite
Statuts ledger: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Checks severes: 0 sur 6.
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
| Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | NaN | PASS | ttl=419.95, tca=370.83959999999996 | ttl/tca finis | L'ancre thermique est quantifiable. |
| Q5-H-02 | SPEC2-Q5 | HIST | NaN | PASS | dCO2=0.36727272727272725, dGas=1.8181818181818181 | >0 | Sensibilites analytiques coherentes. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | BASE | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | BASE | PASS | 138.00545463253732 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | 174.10466846065344 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | 96.9935307065473 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | 193.00545463253732 | valeur finie | CO2 requis interpretable. |

### References de preuve
[evidence:Q5-H-01] [evidence:Q5-H-02] [evidence:Q5-S-01] [evidence:Q5-S-02]


## 4. Annexes de preuve et tracabilite

### 4.1 Ledger complet des tests
#### Q1
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1-H-01 | Q1 | SPEC2-Q1/Slides 2-4 | HIST | HIST_BASE | Score marche de bascule | La signature marche de phase 2 est calculee et exploitable. | stage2_market_score present et non vide | HIGH | nan | PASS | 4.1020408163265305 | score present | Le score de bascule marche est exploitable. |
| Q1-H-02 | Q1 | SPEC2-Q1/Slides 3-4 | HIST | HIST_BASE | Stress physique SR/FAR/IR | La bascule physique est fondee sur SR/FAR/IR. | sr_energy/far_energy/ir_p10 presentes | CRITICAL | nan | PASS | far_energy,ir_p10,sr_energy | SR/FAR/IR presents | Le stress physique est calculable. |
| Q1-H-03 | Q1 | SPEC2-Q1 | HIST | HIST_BASE | Concordance marche vs physique | La relation entre bascule marche et bascule physique est mesurable. | bascule_year_market et bascule_year_physical comparables | MEDIUM | nan | WARN | 42.86% | >=50% | Concordance mesuree entre bascules marche et physique. |
| Q1-H-04 | Q1 | Slides 4-6 | HIST | HIST_BASE | Robustesse seuils | Le diagnostic reste stable sous variation raisonnable de seuils. | delta bascules sous choc de seuil <= 50% | MEDIUM | nan | PASS | 0.914 | confidence moyenne >=0.60 | Proxy de robustesse du diagnostic de bascule. |
| Q1-S-01 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Bascule projetee par scenario | Chaque scenario fournit un diagnostic de bascule projetee. | Q1_country_summary non vide en SCEN | HIGH | BASE | PASS | 7 | >0 lignes | La bascule projetee est produite. |
| Q1-S-01 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Bascule projetee par scenario | Chaque scenario fournit un diagnostic de bascule projetee. | Q1_country_summary non vide en SCEN | HIGH | DEMAND_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. |
| Q1-S-01 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Bascule projetee par scenario | Chaque scenario fournit un diagnostic de bascule projetee. | Q1_country_summary non vide en SCEN | HIGH | FLEX_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. |
| Q1-S-01 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Bascule projetee par scenario | Chaque scenario fournit un diagnostic de bascule projetee. | Q1_country_summary non vide en SCEN | HIGH | LOW_RIGIDITY | PASS | 7 | >0 lignes | La bascule projetee est produite. |
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE calculable | MEDIUM | BASE | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE calculable | MEDIUM | DEMAND_UP | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE calculable | MEDIUM | FLEX_UP | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE calculable | MEDIUM | LOW_RIGIDITY | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-03 | Q1 | SPEC2-Q1 | SCEN | DEFAULT | Qualite de causalite | Le regime_coherence respecte le seuil d'interpretation. | part regime_coherence >= seuil min | MEDIUM | BASE | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
| Q1-S-03 | Q1 | SPEC2-Q1 | SCEN | DEFAULT | Qualite de causalite | Le regime_coherence respecte le seuil d'interpretation. | part regime_coherence >= seuil min | MEDIUM | DEMAND_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
| Q1-S-03 | Q1 | SPEC2-Q1 | SCEN | DEFAULT | Qualite de causalite | Le regime_coherence respecte le seuil d'interpretation. | part regime_coherence >= seuil min | MEDIUM | FLEX_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
| Q1-S-03 | Q1 | SPEC2-Q1 | SCEN | DEFAULT | Qualite de causalite | Le regime_coherence respecte le seuil d'interpretation. | part regime_coherence >= seuil min | MEDIUM | LOW_RIGIDITY | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |

#### Q2
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q2-H-01 | Q2 | SPEC2-Q2/Slides 10 | HIST | HIST_BASE | Pentes OLS post-bascule | Les pentes PV/Wind sont estimees en historique. | Q2_country_slopes non vide | HIGH | nan | PASS | 14 | >0 lignes | Les pentes historiques sont calculees. |
| Q2-H-02 | Q2 | SPEC2-Q2/Slides 10-12 | HIST | HIST_BASE | Robustesse statistique | R2/p-value/n sont disponibles pour qualifier la robustesse. | colonnes r2,p_value,n presentes | MEDIUM | nan | PASS | n,p_value,r2 | r2,p_value,n disponibles | La robustesse statistique est lisible. |
| Q2-H-03 | Q2 | Slides 10-13 | HIST | HIST_BASE | Drivers physiques | Les drivers SR/FAR/IR/corr VRE-load sont exploites. | driver correlations non vides | MEDIUM | nan | PASS | 6 | >0 lignes | Les drivers de pente sont disponibles. |
| Q2-S-01 | Q2 | SPEC2-Q2/Slides 11 | SCEN | DEFAULT | Pentes projetees | Les pentes sont reproduites en mode scenario. | Q2_country_slopes non vide en SCEN | HIGH | BASE | PASS | 8 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | Q2 | SPEC2-Q2/Slides 11 | SCEN | DEFAULT | Pentes projetees | Les pentes sont reproduites en mode scenario. | Q2_country_slopes non vide en SCEN | HIGH | HIGH_CO2 | PASS | 8 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | Q2 | SPEC2-Q2/Slides 11 | SCEN | DEFAULT | Pentes projetees | Les pentes sont reproduites en mode scenario. | Q2_country_slopes non vide en SCEN | HIGH | HIGH_GAS | PASS | 8 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-02 | Q2 | SPEC2-Q2 | SCEN | DEFAULT | Delta pente vs BASE | Les differences de pente vs BASE sont calculables. | delta slope par pays/tech vs BASE | MEDIUM | BASE | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. |
| Q2-S-02 | Q2 | SPEC2-Q2 | SCEN | DEFAULT | Delta pente vs BASE | Les differences de pente vs BASE sont calculables. | delta slope par pays/tech vs BASE | MEDIUM | HIGH_CO2 | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. |
| Q2-S-02 | Q2 | SPEC2-Q2 | SCEN | DEFAULT | Delta pente vs BASE | Les differences de pente vs BASE sont calculables. | delta slope par pays/tech vs BASE | MEDIUM | HIGH_GAS | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. |

#### Q3
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q3-H-01 | Q3 | SPEC2-Q3/Slides 16 | HIST | HIST_BASE | Tendances glissantes | Les tendances h_negative et capture_ratio sont estimees. | Q3_status non vide | HIGH | nan | PASS | 7 | >0 lignes | Les tendances historiques sont calculees. |
| Q3-H-02 | Q3 | SPEC2-Q3 | HIST | HIST_BASE | Statuts sortie phase 2 | Les statuts degradation/stabilisation/amelioration sont attribues. | status dans ensemble attendu | MEDIUM | nan | PASS | 2 | status valides | Les statuts business sont renseignes. |
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | BASE | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | DEMAND_UP | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | FLEX_UP | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | LOW_RIGIDITY | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | BASE | PASS | 2 | status renseignes | La lecture de transition phase 3 est possible. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | DEMAND_UP | PASS | 1 | status renseignes | La lecture de transition phase 3 est possible. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | FLEX_UP | PASS | 2 | status renseignes | La lecture de transition phase 3 est possible. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | LOW_RIGIDITY | PASS | 1 | status renseignes | La lecture de transition phase 3 est possible. |

#### Q4
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q4-H-01 | Q4 | SPEC2-Q4/Slides 22 | HIST | HIST_BASE | Simulation BESS 3 modes | SURPLUS_FIRST, PRICE_ARBITRAGE_SIMPLE et PV_COLOCATED sont executes. | 3 modes executes avec sorties non vides | CRITICAL | nan | PASS | HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED | 3 modes executes | Les trois modes Q4 sont disponibles. |
| Q4-H-02 | Q4 | SPEC2-Q4 | HIST | HIST_BASE | Invariants physiques BESS | Bornes SOC/puissance/energie respectees. | aucun check FAIL Q4 | CRITICAL | nan | PASS | PASS | pas de FAIL | Les invariants physiques batterie sont respectes. |
| Q4-S-01 | Q4 | SPEC2-Q4/Slides 23 | SCEN | DEFAULT | Comparaison effet batteries par scenario | Impact FAR/surplus/capture compare entre scenarios utiles. | Q4 summary non vide pour >=1 scenario | HIGH | BASE | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | Q4 | SPEC2-Q4/Slides 23 | SCEN | DEFAULT | Comparaison effet batteries par scenario | Impact FAR/surplus/capture compare entre scenarios utiles. | Q4 summary non vide pour >=1 scenario | HIGH | FLEX_UP | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | Q4 | SPEC2-Q4/Slides 23 | SCEN | DEFAULT | Comparaison effet batteries par scenario | Impact FAR/surplus/capture compare entre scenarios utiles. | Q4 summary non vide pour >=1 scenario | HIGH | HIGH_CO2 | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | Q4 | SPEC2-Q4/Slides 23 | SCEN | DEFAULT | Comparaison effet batteries par scenario | Impact FAR/surplus/capture compare entre scenarios utiles. | Q4 summary non vide pour >=1 scenario | HIGH | HIGH_GAS | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | BASE | PASS | 141.4176326086802 | capture apres finite | Sensibilite valeur exploitable. |
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | FLEX_UP | PASS | 141.39276677627964 | capture apres finite | Sensibilite valeur exploitable. |
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | HIGH_CO2 | PASS | 146.5825566444785 | capture apres finite | Sensibilite valeur exploitable. |
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | HIGH_GAS | PASS | 152.5749842611698 | capture apres finite | Sensibilite valeur exploitable. |

#### Q5
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q5-H-01 | Q5 | SPEC2-Q5/Slides 28 | HIST | HIST_BASE | Ancre thermique historique | TTL/TCA/alpha/corr sont estimes hors surplus. | Q5_summary non vide avec ttl_obs et tca_q95 | HIGH | nan | PASS | ttl=419.95, tca=370.83959999999996 | ttl/tca finis | L'ancre thermique est quantifiable. |
| Q5-H-02 | Q5 | SPEC2-Q5 | HIST | HIST_BASE | Sensibilites analytiques | dTCA/dCO2 et dTCA/dGas sont positives. | dTCA_dCO2 > 0 et dTCA_dGas > 0 | CRITICAL | nan | PASS | dCO2=0.36727272727272725, dGas=1.8181818181818181 | >0 | Sensibilites analytiques coherentes. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | BASE | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | HIGH_CO2 | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | HIGH_GAS | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | HIGH_BOTH | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | BASE | PASS | 138.00545463253732 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_CO2 | PASS | 174.10466846065344 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_GAS | PASS | 96.9935307065473 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_BOTH | PASS | 193.00545463253732 | valeur finie | CO2 requis interpretable. |

### 4.2 Checks et warnings consolides
| run_id | question_id | status | code | message | scope | scenario_id | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260210_133625 | Q1 | WARN | RC_IR_GT_1 | CZ-2018: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_IR_GT_1 | CZ-2019: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_IR_GT_1 | CZ-2022: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2022: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_IR_GT_1 | FR-2018: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_IR_GT_1 | FR-2019: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2019: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_IR_GT_1 | FR-2021: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2021: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_IR_GT_1 | FR-2024: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2024: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q1 | WARN | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=1 | BUNDLE |  | outputs\combined\FULL_20260210_133625\Q1\summary.json |
| FULL_20260210_133625 | Q2 | INFO | Q2_LOW_R2 | BE-WIND: R2 faible (0.09). | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | INFO | Q2_LOW_R2 | CZ-WIND: R2 faible (0.03). | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | INFO | Q2_LOW_R2 | DE-WIND: R2 faible (0.00). | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | INFO | Q2_LOW_R2 | IT_NORD-PV: R2 faible (0.01). | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | INFO | Q2_LOW_R2 | IT_NORD-WIND: R2 faible (0.10). | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_IR_GT_1 | CZ-2018: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_IR_GT_1 | CZ-2019: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_IR_GT_1 | CZ-2022: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2022: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_IR_GT_1 | FR-2018: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_IR_GT_1 | FR-2019: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2019: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_IR_GT_1 | FR-2021: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2021: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_IR_GT_1 | FR-2024: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2024: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | BE-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | BE-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | DE-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | DE-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | ES-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | ES-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | NL-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | NL-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | BE-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | BE-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | DE-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | DE-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | ES-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | ES-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | NL-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | NL-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | BE-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | BE-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | DE-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | DE-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | ES-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | ES-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | NL-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | Q2_FRAGILE | NL-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q2 | WARN | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=3 | BUNDLE |  | outputs\combined\FULL_20260210_133625\Q2\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | HIST |  | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | HIST |  | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | WARN | Q3_MUSTRUN_HIGH | ES: inversion_r_mustrun=53.3% (>50%). | HIST |  | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | HIST |  | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | WARN | Q3_DEMAND_HIGH | FR: inversion_k_demand=27.9% (>25%). | HIST |  | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | HIST |  | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | WARN | RC_IR_GT_1 | FR-2024: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | WARN | RC_LOW_REGIME_COHERENCE | FR-2024: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | FR: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | IT_NORD: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | BE: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | FR: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | IT_NORD: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | BE: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | FR: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | IT_NORD: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | BE: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | FR: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | IT_NORD: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q3 | PASS | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=0 | BUNDLE |  | outputs\combined\FULL_20260210_133625\Q3\summary.json |
| FULL_20260210_133625 | Q4 | INFO | Q4_CACHE_HIT | Resultat charge depuis cache persistant Q4. | HIST |  | outputs\combined\FULL_20260210_133625\Q4\summary.json |
| FULL_20260210_133625 | Q4 | PASS | Q4_PASS | Q4 invariants et checks passes. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q4\summary.json |
| FULL_20260210_133625 | Q4 | PASS | Q4_PASS | Q4 invariants et checks passes. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_133625\Q4\summary.json |
| FULL_20260210_133625 | Q4 | PASS | Q4_PASS | Q4 invariants et checks passes. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_133625\Q4\summary.json |
| FULL_20260210_133625 | Q4 | PASS | Q4_PASS | Q4 invariants et checks passes. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_133625\Q4\summary.json |
| FULL_20260210_133625 | Q4 | PASS | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=0 | BUNDLE |  | outputs\combined\FULL_20260210_133625\Q4\summary.json |
| FULL_20260210_133625 | Q5 | PASS | Q5_PASS | Q5 checks passes. | HIST |  | outputs\combined\FULL_20260210_133625\Q5\summary.json |
| FULL_20260210_133625 | Q5 | PASS | Q5_PASS | Q5 checks passes. | SCEN | BASE | outputs\combined\FULL_20260210_133625\Q5\summary.json |
| FULL_20260210_133625 | Q5 | PASS | Q5_PASS | Q5 checks passes. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_133625\Q5\summary.json |
| FULL_20260210_133625 | Q5 | PASS | Q5_PASS | Q5 checks passes. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_133625\Q5\summary.json |
| FULL_20260210_133625 | Q5 | PASS | Q5_PASS | Q5 checks passes. | SCEN | HIGH_BOTH | outputs\combined\FULL_20260210_133625\Q5\summary.json |
| FULL_20260210_133625 | Q5 | PASS | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=0 | BUNDLE |  | outputs\combined\FULL_20260210_133625\Q5\summary.json |

### 4.3 Tracabilite tests -> sources
| run_id | question_id | test_id | source_ref | mode | scenario_id | status | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260210_133625 | Q1 | Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | nan | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | nan | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-H-03 | SPEC2-Q1 | HIST | nan | WARN | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-H-04 | Slides 4-6 | HIST | nan | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv |
| FULL_20260210_133625 | Q2 | Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | nan | PASS | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv |
| FULL_20260210_133625 | Q2 | Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | nan | PASS | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv |
| FULL_20260210_133625 | Q2 | Q2-H-03 | Slides 10-13 | HIST | nan | PASS | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv |
| FULL_20260210_133625 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv |
| FULL_20260210_133625 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv |
| FULL_20260210_133625 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv |
| FULL_20260210_133625 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | BASE | WARN | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv |
| FULL_20260210_133625 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv |
| FULL_20260210_133625 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv |
| FULL_20260210_133625 | Q3 | Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | nan | PASS | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv |
| FULL_20260210_133625 | Q3 | Q3-H-02 | SPEC2-Q3 | HIST | nan | PASS | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv |
| FULL_20260210_133625 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv |
| FULL_20260210_133625 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv |
| FULL_20260210_133625 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv |
| FULL_20260210_133625 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv |
| FULL_20260210_133625 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv |
| FULL_20260210_133625 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv |
| FULL_20260210_133625 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv |
| FULL_20260210_133625 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv |
| FULL_20260210_133625 | Q4 | Q4-H-01 | SPEC2-Q4/Slides 22 | HIST | nan | PASS | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv |
| FULL_20260210_133625 | Q4 | Q4-H-02 | SPEC2-Q4 | HIST | nan | PASS | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv |
| FULL_20260210_133625 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv |
| FULL_20260210_133625 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv |
| FULL_20260210_133625 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv |
| FULL_20260210_133625 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv |
| FULL_20260210_133625 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv |
| FULL_20260210_133625 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv |
| FULL_20260210_133625 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv |
| FULL_20260210_133625 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv |
| FULL_20260210_133625 | Q5 | Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | nan | PASS | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv |
| FULL_20260210_133625 | Q5 | Q5-H-02 | SPEC2-Q5 | HIST | nan | PASS | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv |
| FULL_20260210_133625 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv |
| FULL_20260210_133625 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv |
| FULL_20260210_133625 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv |
| FULL_20260210_133625 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv |
| FULL_20260210_133625 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv |
| FULL_20260210_133625 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv |
| FULL_20260210_133625 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv |
| FULL_20260210_133625 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv |

### 4.4 Couverture Slides/SPECS -> preuves
_Aucune ligne._

### 4.5 Catalogue de preuves
| run_id | question_id | test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260210_133625 | Q1 | Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | nan | PASS | 4.1020408163265305 | score present | Le score de bascule marche est exploitable. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-H-01 |
| FULL_20260210_133625 | Q1 | Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | nan | PASS | far_energy,ir_p10,sr_energy | SR/FAR/IR presents | Le stress physique est calculable. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-H-02 |
| FULL_20260210_133625 | Q1 | Q1-H-03 | SPEC2-Q1 | HIST | nan | WARN | 42.86% | >=50% | Concordance mesuree entre bascules marche et physique. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-H-03 |
| FULL_20260210_133625 | Q1 | Q1-H-04 | Slides 4-6 | HIST | nan | PASS | 0.914 | confidence moyenne >=0.60 | Proxy de robustesse du diagnostic de bascule. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-H-04 |
| FULL_20260210_133625 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260210_133625 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260210_133625 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260210_133625 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260210_133625 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260210_133625 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260210_133625 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260210_133625 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260210_133625 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | BASE | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260210_133625 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260210_133625 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | FLEX_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260210_133625 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | LOW_RIGIDITY | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260210_133625\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260210_133625 | Q2 | Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | nan | PASS | 14 | >0 lignes | Les pentes historiques sont calculees. | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv#test_id=Q2-H-01 |
| FULL_20260210_133625 | Q2 | Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | nan | PASS | n,p_value,r2 | r2,p_value,n disponibles | La robustesse statistique est lisible. | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv#test_id=Q2-H-02 |
| FULL_20260210_133625 | Q2 | Q2-H-03 | Slides 10-13 | HIST | nan | PASS | 6 | >0 lignes | Les drivers de pente sont disponibles. | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv#test_id=Q2-H-03 |
| FULL_20260210_133625 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | BASE | PASS | 8 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260210_133625 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | 8 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260210_133625 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | 8 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260210_133625 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | BASE | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260210_133625 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260210_133625 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. | outputs\combined\FULL_20260210_133625\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260210_133625 | Q3 | Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | nan | PASS | 7 | >0 lignes | Les tendances historiques sont calculees. | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv#test_id=Q3-H-01 |
| FULL_20260210_133625 | Q3 | Q3-H-02 | SPEC2-Q3 | HIST | nan | PASS | 2 | status valides | Les statuts business sont renseignes. | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv#test_id=Q3-H-02 |
| FULL_20260210_133625 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | BASE | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260210_133625 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260210_133625 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | FLEX_UP | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260210_133625 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260210_133625 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | BASE | PASS | 2 | status renseignes | La lecture de transition phase 3 est possible. | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260210_133625 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | PASS | 1 | status renseignes | La lecture de transition phase 3 est possible. | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260210_133625 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | FLEX_UP | PASS | 2 | status renseignes | La lecture de transition phase 3 est possible. | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260210_133625 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | PASS | 1 | status renseignes | La lecture de transition phase 3 est possible. | outputs\combined\FULL_20260210_133625\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260210_133625 | Q4 | Q4-H-01 | SPEC2-Q4/Slides 22 | HIST | nan | PASS | HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED | 3 modes executes | Les trois modes Q4 sont disponibles. | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv#test_id=Q4-H-01 |
| FULL_20260210_133625 | Q4 | Q4-H-02 | SPEC2-Q4 | HIST | nan | PASS | PASS | pas de FAIL | Les invariants physiques batterie sont respectes. | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv#test_id=Q4-H-02 |
| FULL_20260210_133625 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | BASE | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260210_133625 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | FLEX_UP | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260210_133625 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260210_133625 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260210_133625 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | BASE | PASS | 141.4176326086802 | capture apres finite | Sensibilite valeur exploitable. | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260210_133625 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | FLEX_UP | PASS | 141.39276677627964 | capture apres finite | Sensibilite valeur exploitable. | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260210_133625 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | 146.5825566444785 | capture apres finite | Sensibilite valeur exploitable. | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260210_133625 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | 152.5749842611698 | capture apres finite | Sensibilite valeur exploitable. | outputs\combined\FULL_20260210_133625\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260210_133625 | Q5 | Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | nan | PASS | ttl=419.95, tca=370.83959999999996 | ttl/tca finis | L'ancre thermique est quantifiable. | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv#test_id=Q5-H-01 |
| FULL_20260210_133625 | Q5 | Q5-H-02 | SPEC2-Q5 | HIST | nan | PASS | dCO2=0.36727272727272725, dGas=1.8181818181818181 | >0 | Sensibilites analytiques coherentes. | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv#test_id=Q5-H-02 |
| FULL_20260210_133625 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | BASE | PASS | 1 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260210_133625 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | 1 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260210_133625 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | 1 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260210_133625 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | 1 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260210_133625 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | BASE | PASS | 138.00545463253732 | valeur finie | CO2 requis interpretable. | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260210_133625 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | 174.10466846065344 | valeur finie | CO2 requis interpretable. | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260210_133625 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | 96.9935307065473 | valeur finie | CO2 requis interpretable. | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260210_133625 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | 193.00545463253732 | valeur finie | CO2 requis interpretable. | outputs\combined\FULL_20260210_133625\Q5\test_ledger.csv#test_id=Q5-S-02 |

## 5. Ecarts restants (obligatoire)

Aucun ecart critique detecte par les quality gates.
