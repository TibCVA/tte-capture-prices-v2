# Rapport Final V2.3 - Run `FULL_20260210_150232`

## 1. Page de garde
- Date de generation: `2026-02-10 15:03:19 UTC`
- Run combine source: `outputs\combined\FULL_20260210_150232`
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
Statuts ledger: PASS=15, WARN=1, FAIL=0, NON_TESTABLE=0. Checks severes: 16 sur 21.
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
Statuts ledger: PASS=6, WARN=3, FAIL=0, NON_TESTABLE=0. Checks severes: 41 sur 49.
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
10 tests ont ete executes, dont HIST=2 et SCEN=8. Repartition des statuts: PASS=2, WARN=0, FAIL=0, NON_TESTABLE=8. Le perimetre prospectif couvre 8 ligne(s) de test scenario.

### Resultats historiques test par test
- **Q3-H-01** (HIST/nan) - Tendances glissantes. Ce test verifie: Les tendances h_negative et capture_ratio sont estimees.. Regle: `Q3_status non vide`. Valeur observee: `7.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Les tendances historiques sont calculees.. Resultat conforme a la regle definie. [evidence:Q3-H-01] [source:SPEC2-Q3/Slides 16]
- **Q3-H-02** (HIST/nan) - Statuts sortie phase 2. Ce test verifie: Les statuts degradation/stabilisation/amelioration sont attribues.. Regle: `status dans ensemble attendu`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `status valides` ; statut: `PASS`. Interpretation metier: Les statuts business sont renseignes.. Resultat conforme a la regle definie. [evidence:Q3-H-02] [source:SPEC2-Q3]

### Resultats prospectifs test par test (par scenario)
#### Scenario `BASE`
- **Q3-S-01** (SCEN/BASE) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `hors_scope=85.71%` ; seuil/regle de comparaison: `hors_scope < 80%` ; statut: `NON_TESTABLE`. Interpretation metier: Le scenario reste majoritairement hors scope Stage 2; inversion peu informative.. Resultat non testable faute de donnees ou de perimetre suffisant. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/BASE) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `hors_scope=85.71%` ; seuil/regle de comparaison: `hors_scope < 80%` ; statut: `NON_TESTABLE`. Interpretation metier: Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3.. Resultat non testable faute de donnees ou de perimetre suffisant. [evidence:Q3-S-02] [source:Slides 17-19]
#### Scenario `DEMAND_UP`
- **Q3-S-01** (SCEN/DEMAND_UP) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `hors_scope=100.00%` ; seuil/regle de comparaison: `hors_scope < 80%` ; statut: `NON_TESTABLE`. Interpretation metier: Le scenario reste majoritairement hors scope Stage 2; inversion peu informative.. Resultat non testable faute de donnees ou de perimetre suffisant. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/DEMAND_UP) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `hors_scope=100.00%` ; seuil/regle de comparaison: `hors_scope < 80%` ; statut: `NON_TESTABLE`. Interpretation metier: Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3.. Resultat non testable faute de donnees ou de perimetre suffisant. [evidence:Q3-S-02] [source:Slides 17-19]
#### Scenario `FLEX_UP`
- **Q3-S-01** (SCEN/FLEX_UP) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `hors_scope=85.71%` ; seuil/regle de comparaison: `hors_scope < 80%` ; statut: `NON_TESTABLE`. Interpretation metier: Le scenario reste majoritairement hors scope Stage 2; inversion peu informative.. Resultat non testable faute de donnees ou de perimetre suffisant. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/FLEX_UP) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `hors_scope=85.71%` ; seuil/regle de comparaison: `hors_scope < 80%` ; statut: `NON_TESTABLE`. Interpretation metier: Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3.. Resultat non testable faute de donnees ou de perimetre suffisant. [evidence:Q3-S-02] [source:Slides 17-19]
#### Scenario `LOW_RIGIDITY`
- **Q3-S-01** (SCEN/LOW_RIGIDITY) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `hors_scope=100.00%` ; seuil/regle de comparaison: `hors_scope < 80%` ; statut: `NON_TESTABLE`. Interpretation metier: Le scenario reste majoritairement hors scope Stage 2; inversion peu informative.. Resultat non testable faute de donnees ou de perimetre suffisant. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/LOW_RIGIDITY) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `hors_scope=100.00%` ; seuil/regle de comparaison: `hors_scope < 80%` ; statut: `NON_TESTABLE`. Interpretation metier: Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3.. Resultat non testable faute de donnees ou de perimetre suffisant. [evidence:Q3-S-02] [source:Slides 17-19]

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
Statuts ledger: PASS=2, WARN=0, FAIL=0, NON_TESTABLE=8. Checks severes: 5 sur 41.
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
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | BASE | NON_TESTABLE | hors_scope=85.71% | hors_scope < 80% | Le scenario reste majoritairement hors scope Stage 2; inversion peu informative. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | NON_TESTABLE | hors_scope=100.00% | hors_scope < 80% | Le scenario reste majoritairement hors scope Stage 2; inversion peu informative. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | FLEX_UP | NON_TESTABLE | hors_scope=85.71% | hors_scope < 80% | Le scenario reste majoritairement hors scope Stage 2; inversion peu informative. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | NON_TESTABLE | hors_scope=100.00% | hors_scope < 80% | Le scenario reste majoritairement hors scope Stage 2; inversion peu informative. |
| Q3-S-02 | Slides 17-19 | SCEN | BASE | NON_TESTABLE | hors_scope=85.71% | hors_scope < 80% | Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3. |
| Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | NON_TESTABLE | hors_scope=100.00% | hors_scope < 80% | Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3. |
| Q3-S-02 | Slides 17-19 | SCEN | FLEX_UP | NON_TESTABLE | hors_scope=85.71% | hors_scope < 80% | Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3. |
| Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | NON_TESTABLE | hors_scope=100.00% | hors_scope < 80% | Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3. |

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
| far_after | HIST_PRICE_ARBITRAGE_SIMPLE | 1.0000 | -0.0085 | -0.0085 | -0.0085 | -0.0085 |
| far_after | HIST_PV_COLOCATED | 1.0000 | -0.0208 | -0.0208 | -0.0208 | -0.0208 |
| pv_capture_price_after | BASE | 1.0000 | 102.1697 | 102.1697 | 102.1697 | 102.1697 |
| pv_capture_price_after | FLEX_UP | 1.0000 | 102.1448 | 102.1448 | 102.1448 | 102.1448 |
| pv_capture_price_after | HIGH_CO2 | 1.0000 | 107.3346 | 107.3346 | 107.3346 | 107.3346 |
| pv_capture_price_after | HIGH_GAS | 1.0000 | 113.3270 | 113.3270 | 113.3270 | 113.3270 |
| surplus_unabs_energy_after | BASE | 1.0000 | -9.2595 | -9.2595 | -9.2595 | -9.2595 |
| surplus_unabs_energy_after | FLEX_UP | 1.0000 | -9.2595 | -9.2595 | -9.2595 | -9.2595 |
| surplus_unabs_energy_after | HIGH_CO2 | 1.0000 | -9.2595 | -9.2595 | -9.2595 | -9.2595 |
| surplus_unabs_energy_after | HIGH_GAS | 1.0000 | -9.2595 | -9.2595 | -9.2595 | -9.2595 |

Synthese sizing historique Q4:
| country | year | dispatch_mode | objective | required_bess_power_mw | required_bess_energy_mwh | required_bess_duration_h | far_before | far_after | surplus_unabs_energy_before | surplus_unabs_energy_after | pv_capture_price_before | pv_capture_price_after | revenue_bess_price_taker | soc_min | soc_max | charge_max | discharge_max | charge_sum_mwh | discharge_sum_mwh | initial_deliverable_mwh | engine_version | compute_time_sec | cache_hit | notes_quality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR | 2 024.00 | SURPLUS_FIRST | FAR_TARGET | 1 500.00 | 12 000.00 | 8.0000 | 0.7911 | 0.8481 | 12.7375 | 9.2595 | 39.2480 | 39.2480 | 104 695 652.8 | 0.0000 | 12 000.00 | 1 500.00 | 1 500.00 | 3 478 020.3 | 3 065 607.2 | 5 628.50 | v2.1.0 | 0.8222 | 0.0000 | ok |
Apercu frontiere historique Q4:
| dispatch_mode | required_bess_power_mw | required_bess_duration_h | far_after | surplus_unabs_energy_after | pv_capture_price_after |
| --- | --- | --- | --- | --- | --- |
| SURPLUS_FIRST | 0.0000 | 2.0000 | 0.7911 | 12.7375 | 39.2480 |
| SURPLUS_FIRST | 0.0000 | 4.0000 | 0.7911 | 12.7375 | 39.2480 |
| SURPLUS_FIRST | 0.0000 | 6.0000 | 0.7911 | 12.7375 | 39.2480 |
| SURPLUS_FIRST | 0.0000 | 8.0000 | 0.7911 | 12.7375 | 39.2480 |
| SURPLUS_FIRST | 250.0000 | 2.0000 | 0.7938 | 12.5742 | 39.2480 |
| SURPLUS_FIRST | 250.0000 | 4.0000 | 0.7964 | 12.4159 | 39.2480 |
| SURPLUS_FIRST | 250.0000 | 6.0000 | 0.7988 | 12.2678 | 39.2480 |
| SURPLUS_FIRST | 250.0000 | 8.0000 | 0.8011 | 12.1303 | 39.2480 |
| SURPLUS_FIRST | 500.0000 | 2.0000 | 0.7964 | 12.4122 | 39.2480 |
| SURPLUS_FIRST | 500.0000 | 4.0000 | 0.8016 | 12.0966 | 39.2480 |
| SURPLUS_FIRST | 500.0000 | 6.0000 | 0.8064 | 11.8042 | 39.2480 |
| SURPLUS_FIRST | 500.0000 | 8.0000 | 0.8109 | 11.5325 | 39.2480 |
| SURPLUS_FIRST | 750.0000 | 2.0000 | 0.7991 | 12.2512 | 39.2480 |
| SURPLUS_FIRST | 750.0000 | 4.0000 | 0.8068 | 11.7808 | 39.2480 |
| SURPLUS_FIRST | 750.0000 | 6.0000 | 0.8139 | 11.3461 | 39.2480 |
| SURPLUS_FIRST | 750.0000 | 8.0000 | 0.8205 | 10.9453 | 39.2480 |
| SURPLUS_FIRST | 1 000.00 | 2.0000 | 0.8017 | 12.0914 | 39.2480 |
| SURPLUS_FIRST | 1 000.00 | 4.0000 | 0.8119 | 11.4694 | 39.2480 |
| SURPLUS_FIRST | 1 000.00 | 6.0000 | 0.8213 | 10.8950 | 39.2480 |
| SURPLUS_FIRST | 1 000.00 | 8.0000 | 0.8299 | 10.3711 | 39.2480 |
| SURPLUS_FIRST | 1 500.00 | 2.0000 | 0.8069 | 11.7763 | 39.2480 |
| SURPLUS_FIRST | 1 500.00 | 4.0000 | 0.8220 | 10.8561 | 39.2480 |
| SURPLUS_FIRST | 1 500.00 | 6.0000 | 0.8358 | 10.0138 | 39.2480 |
| SURPLUS_FIRST | 1 500.00 | 8.0000 | 0.8481 | 9.2595 | 39.2480 |

### Robustesse / fragilite
Statuts ledger: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Checks severes: 0 sur 7.
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
- **Q5-S-02** (SCEN/BASE) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `29.0946` ; seuil/regle de comparaison: `valeur finie` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]
#### Scenario `HIGH_BOTH`
- **Q5-S-01** (SCEN/HIGH_BOTH) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/HIGH_BOTH) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `84.0946` ; seuil/regle de comparaison: `valeur finie` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]
#### Scenario `HIGH_CO2`
- **Q5-S-01** (SCEN/HIGH_CO2) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/HIGH_CO2) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `65.1938` ; seuil/regle de comparaison: `valeur finie` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]
#### Scenario `HIGH_GAS`
- **Q5-S-01** (SCEN/HIGH_GAS) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/HIGH_GAS) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `-11.9174` ; seuil/regle de comparaison: `valeur finie` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]

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
| FR | 2018-2024 | CCGT | 419.9500 | 370.8396 | 49.1104 | 0.9082 | 0.3673 | 1.8182 | 160.0000 | -640.8947 | NaN | NaN |

### Robustesse / fragilite
Statuts ledger: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Checks severes: 0 sur 7.
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
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | BASE | PASS | 29.094563543428396 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | 65.19377737154454 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | -11.917360382561618 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | 84.09456354342841 | valeur finie | CO2 requis interpretable. |

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
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | BASE | NON_TESTABLE | hors_scope=85.71% | hors_scope < 80% | Le scenario reste majoritairement hors scope Stage 2; inversion peu informative. |
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | DEMAND_UP | NON_TESTABLE | hors_scope=100.00% | hors_scope < 80% | Le scenario reste majoritairement hors scope Stage 2; inversion peu informative. |
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | FLEX_UP | NON_TESTABLE | hors_scope=85.71% | hors_scope < 80% | Le scenario reste majoritairement hors scope Stage 2; inversion peu informative. |
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | LOW_RIGIDITY | NON_TESTABLE | hors_scope=100.00% | hors_scope < 80% | Le scenario reste majoritairement hors scope Stage 2; inversion peu informative. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | BASE | NON_TESTABLE | hors_scope=85.71% | hors_scope < 80% | Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | DEMAND_UP | NON_TESTABLE | hors_scope=100.00% | hors_scope < 80% | Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | FLEX_UP | NON_TESTABLE | hors_scope=85.71% | hors_scope < 80% | Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | LOW_RIGIDITY | NON_TESTABLE | hors_scope=100.00% | hors_scope < 80% | Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3. |

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
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | BASE | PASS | 29.094563543428396 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_CO2 | PASS | 65.19377737154454 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_GAS | PASS | -11.917360382561618 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_BOTH | PASS | 84.09456354342841 | valeur finie | CO2 requis interpretable. |

### 4.2 Checks et warnings consolides
| run_id | question_id | status | code | message | scope | scenario_id | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260210_150232 | Q1 | WARN | RC_IR_GT_1 | CZ-2018: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_IR_GT_1 | CZ-2019: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_IR_GT_1 | CZ-2022: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2022: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_IR_GT_1 | FR-2018: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_IR_GT_1 | FR-2019: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2019: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_IR_GT_1 | FR-2021: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2021: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_IR_GT_1 | FR-2024: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2024: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | WARN | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=1 | BUNDLE |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q1 | PASS | BUNDLE_INFORMATIVENESS | share_tests_informatifs=100.00% ; share_compare_informatifs=57.14% | BUNDLE |  | outputs\combined\FULL_20260210_150232\Q1\summary.json |
| FULL_20260210_150232 | Q2 | INFO | Q2_LOW_R2 | BE-WIND: R2 faible (0.09). | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | INFO | Q2_LOW_R2 | CZ-WIND: R2 faible (0.03). | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | INFO | Q2_LOW_R2 | DE-WIND: R2 faible (0.00). | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | INFO | Q2_LOW_R2 | IT_NORD-PV: R2 faible (0.01). | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | INFO | Q2_LOW_R2 | IT_NORD-WIND: R2 faible (0.10). | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_IR_GT_1 | CZ-2018: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_IR_GT_1 | CZ-2019: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_IR_GT_1 | CZ-2022: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2022: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_IR_GT_1 | FR-2018: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_IR_GT_1 | FR-2019: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2019: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_IR_GT_1 | FR-2021: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2021: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_IR_GT_1 | FR-2024: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2024: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | BE-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | BE-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | DE-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | DE-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | ES-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | ES-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | NL-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | NL-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | BE-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | BE-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | DE-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | DE-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | ES-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | ES-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | NL-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | NL-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | BE-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | BE-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | DE-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | DE-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | ES-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | ES-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | NL-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | Q2_FRAGILE | NL-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=3 | BUNDLE |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q2 | WARN | BUNDLE_INFORMATIVENESS | share_tests_informatifs=100.00% ; share_compare_informatifs=25.00% | BUNDLE |  | outputs\combined\FULL_20260210_150232\Q2\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | HIST |  | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | HIST |  | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | WARN | Q3_MUSTRUN_HIGH | ES: inversion_r_mustrun=53.3% (>50%). | HIST |  | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | HIST |  | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | WARN | Q3_DEMAND_HIGH | FR: inversion_k_demand=27.9% (>25%). | HIST |  | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | HIST |  | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | WARN | RC_IR_GT_1 | FR-2024: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | WARN | RC_LOW_REGIME_COHERENCE | FR-2024: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | FR: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | IT_NORD: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | BE: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | FR: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | IT_NORD: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | BE: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | FR: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | IT_NORD: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | BE: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | FR: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | IT_NORD: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | PASS | RC_COMMON_PASS | Checks communs RC-1..RC-4 OK. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | PASS | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=0 | BUNDLE |  | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q3 | WARN | BUNDLE_INFORMATIVENESS | share_tests_informatifs=20.00% ; share_compare_informatifs=0.00% | BUNDLE |  | outputs\combined\FULL_20260210_150232\Q3\summary.json |
| FULL_20260210_150232 | Q4 | PASS | Q4_PASS | Q4 invariants et checks passes. | HIST |  | outputs\combined\FULL_20260210_150232\Q4\summary.json |
| FULL_20260210_150232 | Q4 | PASS | Q4_PASS | Q4 invariants et checks passes. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q4\summary.json |
| FULL_20260210_150232 | Q4 | PASS | Q4_PASS | Q4 invariants et checks passes. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_150232\Q4\summary.json |
| FULL_20260210_150232 | Q4 | PASS | Q4_PASS | Q4 invariants et checks passes. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_150232\Q4\summary.json |
| FULL_20260210_150232 | Q4 | PASS | Q4_PASS | Q4 invariants et checks passes. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_150232\Q4\summary.json |
| FULL_20260210_150232 | Q4 | PASS | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=0 | BUNDLE |  | outputs\combined\FULL_20260210_150232\Q4\summary.json |
| FULL_20260210_150232 | Q4 | PASS | BUNDLE_INFORMATIVENESS | share_tests_informatifs=100.00% ; share_compare_informatifs=71.43% | BUNDLE |  | outputs\combined\FULL_20260210_150232\Q4\summary.json |
| FULL_20260210_150232 | Q5 | PASS | Q5_PASS | Q5 checks passes. | HIST |  | outputs\combined\FULL_20260210_150232\Q5\summary.json |
| FULL_20260210_150232 | Q5 | PASS | Q5_PASS | Q5 checks passes. | SCEN | BASE | outputs\combined\FULL_20260210_150232\Q5\summary.json |
| FULL_20260210_150232 | Q5 | PASS | Q5_PASS | Q5 checks passes. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_150232\Q5\summary.json |
| FULL_20260210_150232 | Q5 | PASS | Q5_PASS | Q5 checks passes. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_150232\Q5\summary.json |
| FULL_20260210_150232 | Q5 | PASS | Q5_PASS | Q5 checks passes. | SCEN | HIGH_BOTH | outputs\combined\FULL_20260210_150232\Q5\summary.json |
| FULL_20260210_150232 | Q5 | PASS | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=0 | BUNDLE |  | outputs\combined\FULL_20260210_150232\Q5\summary.json |
| FULL_20260210_150232 | Q5 | PASS | BUNDLE_INFORMATIVENESS | share_tests_informatifs=100.00% ; share_compare_informatifs=100.00% | BUNDLE |  | outputs\combined\FULL_20260210_150232\Q5\summary.json |

### 4.3 Tracabilite tests -> sources
| run_id | question_id | test_id | source_ref | mode | scenario_id | status | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260210_150232 | Q1 | Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | nan | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | nan | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-H-03 | SPEC2-Q1 | HIST | nan | WARN | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-H-04 | Slides 4-6 | HIST | nan | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv |
| FULL_20260210_150232 | Q2 | Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | nan | PASS | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv |
| FULL_20260210_150232 | Q2 | Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | nan | PASS | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv |
| FULL_20260210_150232 | Q2 | Q2-H-03 | Slides 10-13 | HIST | nan | PASS | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv |
| FULL_20260210_150232 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv |
| FULL_20260210_150232 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv |
| FULL_20260210_150232 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv |
| FULL_20260210_150232 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | BASE | WARN | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv |
| FULL_20260210_150232 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv |
| FULL_20260210_150232 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv |
| FULL_20260210_150232 | Q3 | Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | nan | PASS | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv |
| FULL_20260210_150232 | Q3 | Q3-H-02 | SPEC2-Q3 | HIST | nan | PASS | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv |
| FULL_20260210_150232 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | BASE | NON_TESTABLE | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv |
| FULL_20260210_150232 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | NON_TESTABLE | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv |
| FULL_20260210_150232 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | FLEX_UP | NON_TESTABLE | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv |
| FULL_20260210_150232 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | NON_TESTABLE | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv |
| FULL_20260210_150232 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | BASE | NON_TESTABLE | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv |
| FULL_20260210_150232 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | NON_TESTABLE | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv |
| FULL_20260210_150232 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | FLEX_UP | NON_TESTABLE | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv |
| FULL_20260210_150232 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | NON_TESTABLE | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv |
| FULL_20260210_150232 | Q4 | Q4-H-01 | SPEC2-Q4/Slides 22 | HIST | nan | PASS | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv |
| FULL_20260210_150232 | Q4 | Q4-H-02 | SPEC2-Q4 | HIST | nan | PASS | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv |
| FULL_20260210_150232 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv |
| FULL_20260210_150232 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv |
| FULL_20260210_150232 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv |
| FULL_20260210_150232 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv |
| FULL_20260210_150232 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv |
| FULL_20260210_150232 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv |
| FULL_20260210_150232 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv |
| FULL_20260210_150232 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv |
| FULL_20260210_150232 | Q5 | Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | nan | PASS | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv |
| FULL_20260210_150232 | Q5 | Q5-H-02 | SPEC2-Q5 | HIST | nan | PASS | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv |
| FULL_20260210_150232 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv |
| FULL_20260210_150232 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv |
| FULL_20260210_150232 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv |
| FULL_20260210_150232 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv |
| FULL_20260210_150232 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv |
| FULL_20260210_150232 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv |
| FULL_20260210_150232 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv |
| FULL_20260210_150232 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv |

### 4.4 Couverture Slides/SPECS -> preuves
| slide_id | requirement_id | question_id | requirement_text | covered | coverage_method | evidence_ref | test_id | report_section |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SLIDE_01_01 | GLOBAL | Contexte et 5 questions à traiter Nous voulons expliquer la dynamique des capture prices des renouvelables intermittents en restant sur une approche simple, auditable et utile pour la décision | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_02 | GLOBAL | Nous traitons 5 questions, dans l’ordre logique des phases de marché | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_03 | GLOBAL | Bascule phase 1 → phase 2 Quels paramètres font passer un marché d’un régime “confortable” à un régime où les prix et la valeur des actifs deviennent structurellement sous pression | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_04 | GLOBAL | Quels ratios simples expliquent la bascule | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_05 | GLOBAL | Pente en phase 2 À quelle vitesse la valeur captée se dégrade en phase 2 | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_06 | GLOBAL | Quels facteurs expliquent cette vitesse et pourquoi elle diffère selon les pays | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_07 | GLOBAL | Sortie de la phase 2 et entrée en phase 3 À quelles conditions la dynamique cesse de s’aggraver et commence à se stabiliser | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_08 | GLOBAL | Que faudrait-il pour inverser la tendance | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_09 | GLOBAL | Par exemple une hausse durable de la demande | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_10 | GLOBAL | Rôle du stockage batteries couplé au solaire Quel niveau de batteries associé au solaire change réellement la trajectoire | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_11 | GLOBAL | Comment cette condition dépend du coût des batteries, du prix du CO2 et du rôle résiduel du thermique | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_12 | GLOBAL | Impact des commodités et du CO2 Comment le prix du gaz et le prix du CO2 modifient l’ancre des prix et donc les capture prices | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_13 | GLOBAL | Quel niveau de CO2 peut relever le haut de la courbe de prix. | yes | global_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 2 | SLIDE_02_01 | Q1 | Question 1 Définition Question 1 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_02 | Q1 | Quels paramètres expliquent le passage de la phase de marché 1 à la phase de marché 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_03 | Q1 | Définition des phases de marché, en langage simple | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_04 | Q1 | La phase 1 est une situation où l’électricité renouvelable variable ne change pas encore le fonctionnement du marché de façon visible et répétée | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_05 | Q1 | La phase 2 est une situation où la production variable crée régulièrement des heures de prix très bas ou négatifs et où la valeur moyenne captée par ces actifs baisse de façon mesurable | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_06 | Q1 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_07 | Q1 | Le “capture price” d’une filière est le prix moyen reçu pendant les heures où elle produit, pondéré par sa production horaire | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_08 | Q1 | Le “capture ratio” est le capture price divisé par le prix moyen de marché sur la même période | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_09 | Q1 | Un “prix négatif” est un prix day ahead inférieur à zéro | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_10 | Q1 | Un “surplus” est une situation où, sur une heure donnée, la production inflexible plus la production renouvelable variable dépasse ce que le système peut absorber via la demande et les flexibilités disponibles | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_11 | Q1 | Le “ratio d’inflexibilité” est la part de production inflexible par rapport à la demande durant les heures creuses, ce qui mesure la rigidité du système | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_12 | Q1 | Le “ratio de surplus” est la part d’énergie qui apparaît en surplus sur l’année par rapport à l’énergie totale produite | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_13 | Q1 | Le “ratio d’absorption par flexibilité” est la part de ce surplus que le système peut absorber via des leviers identifiables comme exportations, pompage, charge batteries et effacements | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_14 | Q1 | Objet de l’analyse pour Q1 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_15 | Q1 | Nous voulons passer d’un constat “il y a des prix négatifs” à une règle simple du type “la bascule se produit quand une combinaison de surplus, rigidité et faible capacité d’absorption devient récurrente et se reflète dans la distribution des prix et dans le capture ratio”. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 3 | SLIDE_03_01 | Q1 | Question 1 Hypothèses Hypothèse centrale | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_02 | Q1 | La phase 1 se transforme en phase 2 quand les épisodes de surplus deviennent suffisamment fréquents pour modifier la distribution des prix et donc la valeur captée par le solaire et l’éolien | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_03 | Q1 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_04 | Q1 | Un “surplus” est une heure où la demande ne suffit plus à absorber la somme production inflexible plus production variable, compte tenu des capacités d’export et de flexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_05 | Q1 | Le “ratio de surplus” est une mesure annuelle du volume de surplus rapporté à la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_06 | Q1 | Le “ratio d’absorption par flexibilité” est la fraction du surplus absorbée par des leviers physiques identifiables | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_07 | Q1 | Le “ratio d’inflexibilité” mesure la rigidité du parc sur les heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_08 | Q1 | Le “capture ratio” est le prix moyen reçu par une filière rapporté au prix moyen de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_09 | Q1 | Hypothèses minimales à tester, sans usine à gaz | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_10 | Q1 | La bascule est d’abord un phénomène physique | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_11 | Q1 | Elle commence quand la fréquence des heures de surplus dépasse un niveau qui n’est plus marginal | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_12 | Q1 | La bascule arrive plus tôt si le système est rigide | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_13 | Q1 | Un ratio d’inflexibilité élevé réduit l’espace disponible pour absorber la production variable en heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_14 | Q1 | La bascule arrive plus tôt si les capacités d’absorption sont limitées | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_15 | Q1 | Un ratio d’absorption par flexibilité faible signifie que le surplus se transforme en contrainte de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_16 | Q1 | La bascule est plus tardive si la production variable est bien alignée avec la demande | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_17 | Q1 | Une forte corrélation horaire entre production solaire et demande réduit les surplus | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_18 | Q1 | La bascule dépend aussi des règles et incitations | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_19 | Q1 | Si des volumes importants sont développés et injectés sans exposition au signal de prix, la phase 2 peut démarrer plus tôt ou durer plus longtemps car l’investissement ne se freine pas naturellement. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 4 | SLIDE_04_01 | Q1 | Question 1 Tests empiriques Objectif des tests | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_02 | Q1 | Construire une règle de bascule vérifiable et réplicable, basée sur des données observées et sur des définitions physiques simples | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_03 | Q1 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_04 | Q1 | Le “surplus” correspond à des heures où production inflexible plus production variable dépasse ce que la demande et les flexibilités peuvent absorber | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_05 | Q1 | Le “ratio de surplus” mesure le volume annuel de surplus rapporté à la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_06 | Q1 | Le “ratio d’absorption par flexibilité” mesure la part de surplus absorbée par exportations, pompage, charge batteries et effacements | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_07 | Q1 | Le “ratio d’inflexibilité” mesure la rigidité du système en heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_08 | Q1 | Le “capture ratio” mesure la valeur captée par une filière | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_09 | Q1 | Jeu de tests simple, en trois blocs | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_10 | Q1 | Bloc A | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_11 | Q1 | Construire les indicateurs physiques par pays et par année | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_12 | Q1 | Nous calculons heure par heure un indicateur de demande résiduelle, qui correspond à la demande moins la production variable moins la production inflexible | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_13 | Q1 | Nous identifions les heures où cette demande résiduelle devient négative, ce qui signale un surplus potentiel | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_14 | Q1 | Nous mesurons le ratio de surplus annuel et le ratio d’inflexibilité sur les heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_15 | Q1 | Bloc B | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_16 | Q1 | Confronter les indicateurs physiques aux signaux de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_17 | Q1 | Nous comptons le nombre d’heures de prix négatifs et le nombre d’heures de prix très bas | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_18 | Q1 | Nous calculons le capture ratio solaire et le capture ratio éolien | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_19 | Q1 | Nous vérifions que la bascule vers la phase 2 se manifeste à la fois dans les prix et dans la valeur captée, et pas uniquement dans un seul indicateur | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_20 | Q1 | Bloc C | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_21 | Q1 | Identifier un seuil robuste | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_22 | Q1 | Nous cherchons un point de rupture statistique, par exemple une accélération du nombre d’heures négatives ou une chute du capture ratio au-delà d’un certain niveau de ratio de surplus | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_23 | Q1 | Nous validons le seuil en comparant plusieurs pays et en vérifiant qu’il se retrouve avec une logique cohérente, même si les valeurs exactes diffèrent | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_24 | Q1 | Critère de réussite | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_25 | Q1 | Nous obtenons une règle de bascule qui explique correctement le passage phase 1 à phase 2 sur plusieurs pays, et qui reste stable quand on change légèrement la période historique. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 5 | SLIDE_05_01 | Q1 | Question 1 Scénarios prospectifs Pourquoi des scénarios sont nécessaires pour Q1 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_02 | Q1 | Le passé ne suffit pas | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_03 | Q1 | Nous devons tester comment un pays bascule quand la pénétration renouvelable continue d’augmenter et quand la demande ou la flexibilité changent | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_04 | Q1 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_05 | Q1 | Le “ratio de surplus” est le volume annuel de surplus rapporté à la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_06 | Q1 | Le “ratio d’absorption par flexibilité” est la part de surplus absorbée par des leviers identifiables comme exportations, pompage, charge batteries et effacements | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_07 | Q1 | Le “ratio d’inflexibilité” mesure la rigidité de la production en heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_08 | Q1 | Le “capture ratio” mesure la valeur captée par une filière | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_09 | Q1 | Principe de scénarisation pragmatique | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_10 | Q1 | Nous ne cherchons pas à simuler un dispatch complet optimisé | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_11 | Q1 | Nous cherchons à projeter des ordres de grandeur crédibles, avec une logique explicable, en faisant varier quelques variables exogènes | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_12 | Q1 | Variables exogènes minimales pour scénarios de bascule | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_13 | Q1 | La trajectoire de demande électrique, avec une hypothèse haute et basse | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_14 | Q1 | La trajectoire de capacités solaires et éoliennes | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_15 | Q1 | La trajectoire de production inflexible, ou au minimum sa rigidité en heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_16 | Q1 | La trajectoire de capacité d’absorption, via export, pompage, batteries et effacements | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_17 | Q1 | Une hypothèse de cadre d’incitation, qui représente la part de nouvelles capacités développées sans exposition forte au prix spot | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_18 | Q1 | Ce que l’on doit obtenir en sortie | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_19 | Q1 | Une année de bascule probable pour chaque pays et chaque trajectoire | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_20 | Q1 | Une explication causale sous forme de ratios simples qui changent de valeur avant la bascule. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 6 | SLIDE_06_01 | Q1 | Question 1 Limites et points de vigilance Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_02 | Q1 | Le “surplus” est une heure où la production dépasse la capacité d’absorption du système | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_03 | Q1 | Le “ratio d’absorption par flexibilité” mesure ce qui est absorbé par des leviers identifiés | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_04 | Q1 | Le “capture ratio” mesure la valeur captée par une filière | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_05 | Q1 | Limites structurelles si on reste volontairement simple | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_06 | Q1 | Les données ne captent pas toutes les flexibilités réelles | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_07 | Q1 | Certaines flexibilités sont infra horaires ou ne sont pas observables simplement | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_08 | Q1 | La corrélation n’est pas une preuve de causalité | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_09 | Q1 | Une bascule observée peut être accélérée ou freinée par des facteurs non modélisés comme des changements de règles de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_10 | Q1 | Le rôle des incitations peut être déterminant | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_11 | Q1 | Si l’investissement est guidé par des mécanismes politiques et non par le marché, une règle purement physique peut sous estimer la durée de la phase 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_12 | Q1 | Les interconnexions peuvent masquer le problème | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_13 | Q1 | Un pays peut absorber son surplus par export, mais cela dépend de la situation simultanée des voisins | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_14 | Q1 | Les années atypiques peuvent fausser les seuils | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_15 | Q1 | Nous devons isoler les chocs extrêmes et tester la stabilité | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_16 | Q1 | Conséquence de ces limites | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_17 | Q1 | La bascule doit être présentée comme une estimation robuste à grosse maille, pas comme une date exacte au mois près. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 7 | SLIDE_07_01 | Q1 | Question 1 Livrable attendu Livrable principal | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_02 | Q1 | Un jeu de “règles de bascule” auditable qui explique le passage de la phase de marché 1 à la phase de marché 2 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_03 | Q1 | Définitions nécessaires sur cette slide | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_04 | Q1 | Le “ratio de surplus” mesure le volume annuel de surplus rapporté à la production totale | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_05 | Q1 | Le “ratio d’absorption par flexibilité” mesure la fraction de surplus absorbée par exportations, pompage, charge batteries et effacements | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_06 | Q1 | Le “ratio d’inflexibilité” mesure la rigidité du système en heures creuses | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_07 | Q1 | Le “capture ratio” mesure la valeur captée par une filière | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_08 | Q1 | Contenu concret du livrable | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_09 | Q1 | Nous fournissons une définition claire et unique des phases de marché 1 et 2 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_10 | Q1 | Nous fournissons une liste courte de ratios et une formule de bascule, compréhensible et calculable | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_11 | Q1 | Nous fournissons une justification empirique par pays, basée sur données historiques | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_12 | Q1 | Nous fournissons une estimation de seuils de bascule, avec une fourchette et un niveau de confiance | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_13 | Q1 | Nous fournissons un diagnostic des leviers les plus efficaces pour retarder la bascule, en distinguant demande, flexibilité et rigidité du parc | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_14 | Q1 | Format de restitution | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_15 | Q1 | Une note courte et structurée | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_16 | Q1 | Un ensemble de graphiques simples et répétables | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_17 | Q1 | Un fichier de calcul permettant de recalculer les ratios avec de nouvelles hypothèses. | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 8 | SLIDE_08_01 | Q2 | Question 2 Définition Question 2 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_02 | Q2 | Quelle est la pente de la phase de marché 2 et quels facteurs la pilotent | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_03 | Q2 | Définition opérationnelle de la “pente” | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_04 | Q2 | La pente mesure la vitesse à laquelle la valeur captée se dégrade quand la pénétration des renouvelables variables augmente dans un marché déjà entré en phase 2 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_05 | Q2 | Définitions nécessaires sur cette slide | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_06 | Q2 | Le “capture price” est le prix moyen reçu pendant les heures de production d’une filière, pondéré par sa production horaire | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_07 | Q2 | Le “capture ratio” est le capture price divisé par le prix moyen de marché | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_08 | Q2 | La “pénétration” d’une filière est sa part dans la production totale sur une année | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_09 | Q2 | L’“ancre thermique des prix” est un niveau de prix représentatif des heures où le thermique fixe le prix, et il dépend surtout du coût du gaz et du prix du CO2 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_10 | Q2 | Le “ratio de surplus” mesure le volume annuel de surplus rapporté à la production totale | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_11 | Q2 | Le “ratio d’absorption par flexibilité” mesure la fraction du surplus absorbée par des leviers identifiables | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_12 | Q2 | Mesures possibles de pente, à choisir explicitement | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_13 | Q2 | Nous pouvons mesurer la pente du capture ratio solaire en fonction de la pénétration solaire | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_14 | Q2 | Nous pouvons mesurer la pente du nombre d’heures de prix négatifs en fonction de la pénétration solaire et éolienne | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_15 | Q2 | Nous pouvons mesurer la pente de la profondeur des prix négatifs, si nous voulons aller au delà du comptage d’heures | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_16 | Q2 | Sortie attendue | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_17 | Q2 | Une estimation chiffrée de la pente, par pays, avec une explication causale simple des écarts entre pays. | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_01 | Q2 | Question 2 Hypothèses Définitions nécessaires sur cette slide | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_02 | Q2 | Le “capture ratio” est la valeur captée par une filière rapportée au prix moyen de marché | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_03 | Q2 | Le “ratio de surplus” mesure l’énergie en surplus sur l’année rapportée à la production totale | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_04 | Q2 | Le “ratio d’absorption par flexibilité” mesure ce que la flexibilité absorbe sur ce surplus | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_05 | Q2 | Le “ratio d’inflexibilité” mesure la rigidité du parc en heures creuses | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_06 | Q2 | L’“ancre thermique des prix” dépend du coût du gaz et du prix du CO2 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_07 | Q2 | Hypothèse générale | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_08 | Q2 | En phase 2, la pente est pilotée par deux effets qui se cumulent | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_09 | Q2 | Le premier effet est l’augmentation de la fréquence des heures de prix très bas | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_10 | Q2 | Le second effet est la baisse de la valeur moyenne captée car la production se concentre sur ces heures | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_11 | Q2 | Hypothèses explicatives de la pente, à tester de façon pragmatique | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_12 | Q2 | La pente est plus forte si la production solaire est peu corrélée à la demande | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_13 | Q2 | Une faible corrélation augmente les surplus à midi et donc accélère la chute du capture ratio | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_14 | Q2 | La pente est plus forte si le système est rigide | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_15 | Q2 | Un ratio d’inflexibilité élevé réduit les marges d’absorption en heures creuses et accélère les heures de prix négatifs | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_16 | Q2 | La pente est plus faible si la flexibilité croît vite | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_17 | Q2 | Un ratio d’absorption par flexibilité élevé réduit la fréquence et l’intensité des épisodes de prix extrêmes | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_18 | Q2 | La pente dépend de l’ancre thermique | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_19 | Q2 | Si le coût marginal thermique est élevé, la différence entre heures chères et heures en surplus peut être plus grande, ce qui peut amplifier la cannibalisation en valeur relative | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_20 | Q2 | La pente dépend des règles d’investissement | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_21 | Q2 | Si une grande partie des nouvelles capacités est développée avec une protection hors marché, l’investissement peut continuer malgré des signaux spot dégradés, ce qui accentue la pente et prolonge la phase 2. | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 10 | SLIDE_10_01 | Q2 | Question 2 Tests empiriques Objectif des tests | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_02 | Q2 | Mesurer la pente de façon robuste et expliquer sa variance entre pays par un petit nombre de drivers testables | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_03 | Q2 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_04 | Q2 | Le “capture ratio” est la valeur captée par une filière rapportée au prix moyen de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_05 | Q2 | La “pénétration” est la part de production annuelle d’une filière dans la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_06 | Q2 | L’“ancre thermique des prix” est un niveau représentatif des heures où le thermique fixe le prix, et elle dépend surtout du coût du gaz et du prix du CO2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_07 | Q2 | Le “ratio de surplus” mesure l’énergie en surplus sur l’année rapportée à la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_08 | Q2 | Le “ratio d’inflexibilité” mesure la rigidité du parc en heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_09 | Q2 | Le “ratio d’absorption par flexibilité” mesure la fraction de surplus absorbée par flexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_10 | Q2 | Test 1 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_11 | Q2 | Estimer la pente en phase 2 de manière simple | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_12 | Q2 | Nous identifions les années où un pays est en phase 2 avec des critères explicites | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_13 | Q2 | Nous régressons le capture ratio solaire sur la pénétration solaire sur ces années | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_14 | Q2 | Nous exprimons la pente en points de capture ratio perdus par point de pénétration ajouté | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_15 | Q2 | Test 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_16 | Q2 | Vérifier que la pente n’est pas un artefact d’ancre thermique | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_17 | Q2 | Nous recalculons la pente en contrôlant l’ancre thermique des prix, qui dépend du gaz et du CO2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_18 | Q2 | Nous distinguons la baisse de valeur due à plus de surplus de la baisse de valeur due à une ancre thermique qui change | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_19 | Q2 | Test 3 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_20 | Q2 | Expliquer la pente par des drivers simples | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_21 | Q2 | Nous testons si la pente est corrélée au ratio de surplus et au ratio d’inflexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_22 | Q2 | Nous testons si la pente est corrélée au ratio d’absorption par flexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_23 | Q2 | Nous testons si la pente est corrélée à un indicateur de corrélation production solaire et demande | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_24 | Q2 | Test 4 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_25 | Q2 | Tests de robustesse | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_26 | Q2 | Nous excluons les années de crise et nous vérifions si la pente reste du même ordre de grandeur | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_27 | Q2 | Nous testons la stabilité du résultat si on change la période et si on change le pays de référence. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 11 | SLIDE_11_01 | Q2 | Question 2 Scénarios prospectifs et leviers Pourquoi faire des scénarios pour la pente | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_02 | Q2 | Même si la pente est mesurée sur l’historique, elle peut changer si la flexibilité se développe ou si les règles d’investissement changent | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_03 | Q2 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_04 | Q2 | La “pente” est la vitesse de dégradation du capture ratio en phase 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_05 | Q2 | Le “ratio d’absorption par flexibilité” est la fraction du surplus absorbée par des leviers physiques identifiables | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_06 | Q2 | L’“ancre thermique des prix” dépend du coût du gaz et du prix du CO2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_07 | Q2 | Le “capture ratio” est la valeur captée par une filière rapportée au prix moyen de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_08 | Q2 | Scénarios simples à construire | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_09 | Q2 | Scénario A | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_10 | Q2 | Demande faible et forte croissance solaire | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_11 | Q2 | La pente doit s’accentuer si la flexibilité ne suit pas | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_12 | Q2 | Scénario B | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_13 | Q2 | Demande dynamique via électrification | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_14 | Q2 | La pente peut se réduire si les heures de surplus diminuent | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_15 | Q2 | Scénario C | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_16 | Q2 | Accélération stockage et effacement | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_17 | Q2 | La pente se réduit si le ratio d’absorption par flexibilité augmente vite | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_18 | Q2 | Scénario D | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_19 | Q2 | Choc gaz et CO2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_20 | Q2 | L’ancre thermique augmente et change la valeur relative, même si le surplus ne change pas | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_21 | Q2 | Scénario E | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_22 | Q2 | Maintien d’incitations hors marché sur de gros volumes | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_23 | Q2 | La pente peut rester forte car l’investissement ne se freine pas naturellement | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_24 | Q2 | Leviers à relier directement aux drivers | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_25 | Q2 | Le levier “flexibilité” agit sur le ratio d’absorption par flexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_26 | Q2 | Le levier “pilotabilité” agit sur le ratio d’inflexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_27 | Q2 | Le levier “politique et règles de soutien” agit sur la trajectoire d’investissement et donc sur la vitesse d’augmentation de la pénétration. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 12 | SLIDE_12_01 | Q2 | Question 2 Limites et règles d’interprétation Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_02 | Q2 | Le “capture ratio” est la valeur captée par une filière rapportée au prix moyen de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_03 | Q2 | L’“ancre thermique des prix” dépend du coût du gaz et du prix du CO2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_04 | Q2 | Le “ratio de surplus” mesure l’énergie en surplus sur l’année rapportée à la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_05 | Q2 | Limites si on veut rester auditable | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_06 | Q2 | La pente observée sur dix ans peut refléter plusieurs régimes différents | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_07 | Q2 | Le marché peut changer de règles au milieu de la période | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_08 | Q2 | La pente peut dépendre d’effets voisins | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_09 | Q2 | L’absorption par export dépend aussi de la situation simultanée des pays interconnectés | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_10 | Q2 | Les incitations politiques sont difficiles à quantifier sans une variable dédiée | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_11 | Q2 | Si on ne modélise pas ce facteur, on peut mal expliquer la durée de phase 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_12 | Q2 | Une pente statistique n’est pas une loi physique | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_13 | Q2 | Elle doit être interprétée comme un ordre de grandeur conditionnel | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_14 | Q2 | Règles de lecture à imposer | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_15 | Q2 | Nous présentons toujours une pente avec un intervalle d’incertitude | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_16 | Q2 | Nous explicitons les années exclues et la raison | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_17 | Q2 | Nous relions chaque pente à des variables explicatives mesurables, sinon elle n’est pas actionnable. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 13 | SLIDE_13_01 | Q2 | Question 2 Livrable attendu Livrable principal | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_02 | Q2 | Un diagnostic chiffré de la pente en phase 2, et une explication simple des facteurs qui la pilotent | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_03 | Q2 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_04 | Q2 | Le “capture ratio” est la valeur captée par une filière rapportée au prix moyen de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_05 | Q2 | La “pente” est la variation du capture ratio quand la pénétration augmente en phase 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_06 | Q2 | L’“ancre thermique des prix” dépend du coût du gaz et du prix du CO2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_07 | Q2 | Le “ratio de surplus” mesure l’énergie en surplus sur l’année rapportée à la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_08 | Q2 | Le “ratio d’absorption par flexibilité” mesure la part de surplus absorbée par flexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_09 | Q2 | Le “ratio d’inflexibilité” mesure la rigidité du parc en heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_10 | Q2 | Contenu concret du livrable | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_11 | Q2 | Nous fournissons, par pays, une pente du capture ratio solaire et une pente du capture ratio éolien en phase 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_12 | Q2 | Nous fournissons une décomposition qualitative et si possible quantitative des drivers, avec un ordre de grandeur par driver | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_13 | Q2 | Nous fournissons une lecture opérationnelle pour TTE, sous forme de règles simples | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_14 | Q2 | Par exemple une pente forte signifie que chaque point de pénétration additionnel détruit rapidement la valeur captée si aucune flexibilité ne suit | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_15 | Q2 | Nous fournissons une analyse de sensibilité à l’ancre thermique via gaz et CO2, car cette ancre change le niveau de valeur même si la cannibalisation relative reste identique | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_16 | Q2 | Nous fournissons un ensemble de scénarios standards pour projeter la pente sur 5 à 10 ans, sans faire un modèle d’équilibre complexe | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_17 | Q2 | Format de restitution | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_18 | Q2 | Une note structurée | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_19 | Q2 | Un set de graphiques répétés à l’identique pour chaque pays | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_20 | Q2 | Un fichier de calcul pour recalculer les pentes et tester des hypothèses. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 14 | SLIDE_14_01 | Q3 | Question 3 (Phase 2 → Phase 3) — Définition précise du problème La question vise à définir quand et pourquoi un marché sort de la Phase 2 (dégradation active de la valeur captée par le PV et montée des prix très bas et négatifs) pour entrer en Phase 3 , où le système “s’auto-adapte” et où certains signaux de stress cessent d’empirer, voire commencent à se stabiliser | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 14 | SLIDE_14_02 | Q3 | Définitions clés à rappeler systématiquement | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 14 | SLIDE_14_03 | Q3 | Le capture price PV est le prix moyen pondéré par la production PV | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 14 | SLIDE_14_04 | Q3 | Le capture ratio PV est le capture price PV divisé par le prix moyen “baseload” sur la même période | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 14 | SLIDE_14_05 | Q3 | Un ratio inférieur à 1 signifie que le PV produit plus souvent quand les prix sont bas | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 14 | SLIDE_14_06 | Q3 | Le Surplus Ratio (SR) mesure la fréquence et l’ampleur des heures où la production non pilotable excède la demande instantanée | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 14 | SLIDE_14_07 | Q3 | Le Flex Absorption Ratio (FAR) mesure la part de ce surplus qui est absorbée par des “puits” de flexibilité (stockage, export, effacements) | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 14 | SLIDE_14_08 | Q3 | L’ Inflexibility Ratio (IR) mesure la rigidité de la production non pilotable en heures creuses par rapport à la demande creuse | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 14 | SLIDE_14_09 | Q3 | Le Thermal Tail Level (TTL) représente un niveau de prix élevé typique des heures “thermiques” qui sert d’ancre économique hors surplus | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 14 | SLIDE_14_10 | Q3 | Définition opérationnelle de la bascule Phase 2 → Phase 3 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 14 | SLIDE_14_11 | Q3 | La bascule n’est pas un jugement qualitatif | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 14 | SLIDE_14_12 | Q3 | C’est un ensemble de critères observables et testables qui montrent qu’un ou plusieurs mécanismes d’adaptation prennent le dessus sur l’augmentation mécanique du surplus. | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_01 | Q3 | Question 3 — Hypothèses structurantes (simples, auditables, et falsifiables) Hypothèse H3.1 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_02 | Q3 | La Phase 3 commence quand la croissance de la flexibilité utile dépasse durablement la croissance du surplus | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_03 | Q3 | Dans un langage simple, “le système ajoute plus de capacité à absorber que de capacité à surproduire” | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_04 | Q3 | Hypothèse H3.2 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_05 | Q3 | Le meilleur signal “pédestre” n’est pas un niveau de prix, mais une combinaison de tendance | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_06 | Q3 | La Phase 3 est crédible si la tendance des heures à prix très bas ou négatifs s’infléchit, tout en observant que la pénétration VRE continue de croître | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_07 | Q3 | Hypothèse H3.3 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_08 | Q3 | Le mécanisme d’adaptation peut venir de plusieurs leviers, et il faut les séparer pour ne pas confondre les causes | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_09 | Q3 | Le levier peut être une hausse de la demande utile aux bonnes heures, une hausse de flexibilité, une réduction de rigidité, un recours plus systématique au curtailment, ou une amélioration des interconnexions | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_10 | Q3 | Hypothèse H3.4 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_11 | Q3 | Si l’IR est élevé, la Phase 3 est plus difficile à atteindre car une partie du surplus est “structurelle” et non liée au PV | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_12 | Q3 | Cela implique que l’adaptation ne peut pas reposer uniquement sur des batteries couplées au PV | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_13 | Q3 | Définitions rappelées | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_14 | Q3 | SR mesure le surplus brut | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_15 | Q3 | FAR mesure l’absorption de ce surplus | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_16 | Q3 | IR mesure la rigidité en creux | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_17 | Q3 | TTL mesure un niveau haut de prix sur heures non-surplus | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 15 | SLIDE_15_18 | Q3 | Le capture ratio PV mesure la valeur relative captée par le PV. | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 | Q3-H-01; Q3-H-02; Q3-S-01; Q3-S-02 | Q3 |
| 16 | SLIDE_16_01 | Q3 | Question 3 — Tests empiriques (preuve historique multi-pays, sans usine à gaz) Test T3.1 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_02 | Q3 | Détection d’un retournement de tendance | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_03 | Q3 | On calcule, par pays et par année, le nombre d’heures à prix négatifs et le nombre d’heures sous un seuil très bas | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_04 | Q3 | On teste si la pente sur 3 ans devient négative alors que la pénétration VRE continue de monter | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_05 | Q3 | Test T3.2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_06 | Q3 | Test de cohérence économique | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_07 | Q3 | On vérifie que la baisse des heures négatives n’est pas due à un choc exogène temporaire | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_08 | Q3 | On exclut les années “anormales” ou on les traite à part | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_09 | Q3 | On exige un signal sur plusieurs années consécutives | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_10 | Q3 | Test T3.3 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_11 | Q3 | Décomposition par leviers | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_12 | Q3 | On relie le retournement à des variables explicatives simples | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_13 | Q3 | On compare l’évolution de SR, FAR, IR et des capacités plausibles de flexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_14 | Q3 | Si le retournement est observé alors que SR continue d’augmenter et que FAR n’augmente pas, l’hypothèse “flex” est fragile | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_15 | Q3 | Test T3.4 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_16 | Q3 | Test “capture ratio” | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_17 | Q3 | On observe si la pente de dégradation du capture ratio PV cesse de s’aggraver quand les signaux de surplus se stabilisent | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_18 | Q3 | La Phase 3 est crédible si la dégradation ralentit parce que la distribution des prix en heures PV se redresse | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_19 | Q3 | Définitions rappelées | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_20 | Q3 | FAR est la part du surplus absorbée | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_21 | Q3 | SR est la part de surplus brut | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_22 | Q3 | IR caractérise la place occupée par la production rigide en creux | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 16 | SLIDE_16_23 | Q3 | TTL décrit l’ancre “thermique” sur heures non-surplus. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 | Q3-H-01 | Q3 |
| 17 | SLIDE_17_01 | Q3 | Question 3 — Scénarios prospectifs (pragmatiques, cohérents, et limités en nombre) Objectif des scénarios | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_02 | Q3 | Les scénarios ne cherchent pas à “prévoir le spot” | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_03 | Q3 | Ils servent à tester des conditions de bascule | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_04 | Q3 | On construit une petite grille de scénarios cohérents et lisibles | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_05 | Q3 | Scénario S3.A “Demande utile” | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_06 | Q3 | On augmente la demande annuelle et surtout la demande sur les heures de surplus PV | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_07 | Q3 | On observe l’effet sur SR et sur le capture ratio PV | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_08 | Q3 | Scénario S3.B “Flex” | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_09 | Q3 | On augmente les puits de flexibilité (batteries, pompage, effacement) et on mesure l’impact sur FAR, sur la fréquence des heures négatives, et sur le capture ratio PV | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_10 | Q3 | Scénario S3.C “Moins de rigidité” | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_11 | Q3 | On réduit le must-run effectif en creux ou on augmente sa modulation, ce qui diminue IR | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_12 | Q3 | On mesure l’impact sur SR et sur la probabilité de prix négatifs | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_13 | Q3 | Scénario S3.D “Interconnexions et export” | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_14 | Q3 | On teste une capacité d’export additionnelle, en restant prudent sur la synchronisation des surplus entre pays | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_15 | Q3 | Définitions rappelées | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_16 | Q3 | SR et FAR décrivent la mécanique physique surplus-absorption | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_17 | Q3 | IR décrit une contrainte structurelle | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 17 | SLIDE_17_18 | Q3 | TTL définit le niveau de prix “haut” qui conditionne les spreads et donc l’intérêt économique des flexibilités. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01; outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-01; Q3-S-02 | Q3 |
| 18 | SLIDE_18_01 | Q3 | Question 3 — Limites, points d’attention, et règles de prudence Limite L3.1 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_02 | Q3 | Endogénéité | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_03 | Q3 | En réalité, la montée de la flex est souvent une réponse au stress | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_04 | Q3 | Un simple lien statistique ne prouve pas le mécanisme causal | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_05 | Q3 | Il faut trianguler avec des événements concrets et des ordres de grandeur | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_06 | Q3 | Limite L3.2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_07 | Q3 | Confusion entre adaptation et choc temporaire | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_08 | Q3 | Un retournement peut venir d’une météo atypique, d’une crise combustible, ou d’un événement système | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_09 | Q3 | Il faut donc exiger un signal sur plusieurs années et sur plusieurs indicateurs | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_10 | Q3 | Limite L3.3 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_11 | Q3 | Mesure imparfaite de la flexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_12 | Q3 | Certaines flexibilités sont peu visibles dans les données publiques | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_13 | Q3 | Cela peut biaiser l’estimation du FAR | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_14 | Q3 | Limite L3.4 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_15 | Q3 | Synchronisation régionale | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_16 | Q3 | Les interconnexions ne sont une soupape que si les surplus ne sont pas simultanés | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_17 | Q3 | C’est une hypothèse à tester pays par pays | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_18 | Q3 | Définitions rappelées | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_19 | Q3 | FAR peut être “surestimé” si on compte des puits qui ne sont pas disponibles aux bonnes heures | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_20 | Q3 | IR peut masquer que le surplus n’est pas d’origine PV | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 18 | SLIDE_18_21 | Q3 | TTL peut bouger fortement avec le gaz et le CO2, ce qui change la lecture économique sans changer la physique du surplus. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_01 | Q3 | Question 3 — Livrable attendu (clair, auditable, directement utilisable par un CEO) Livrable principal | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_02 | Q3 | Une fiche “règles de bascule Phase 2 → Phase 3” par pays, avec des critères simples, chiffrés, et une logique d’attribution des causes | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_03 | Q3 | Contenu minimal de la fiche | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_04 | Q3 | La fiche explicite un seuil de FAR durable, une condition sur la tendance des heures négatives, et une lecture conjointe SR-IR pour distinguer “surplus PV” et “surplus structurel” | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_05 | Q3 | Livrable “inversion” | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_06 | Q3 | Un mini-calculateur qui répond à “Que faudrait-il pour inverser la trajectoire” | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_07 | Q3 | Il donne des ordres de grandeur | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_08 | Q3 | Il traduit une hausse de demande ciblée, une baisse de rigidité, ou un ajout de flexibilité en impact sur SR, FAR et capture ratio PV | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_09 | Q3 | Définitions rappelées | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_10 | Q3 | Le capture ratio PV est la valeur relative captée par le PV | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_11 | Q3 | SR quantifie la taille du problème | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_12 | Q3 | FAR quantifie la réponse du système | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_13 | Q3 | IR explique la contrainte structurelle | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 19 | SLIDE_19_14 | Q3 | TTL sert de repère économique pour l’intérêt des flexibilités. | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 | Q3-S-02 | Q3 |
| 20 | SLIDE_20_01 | Q4 | Question 4 (Batteries) — Définition précise du problème La question vise à quantifier combien de batteries il faut pour “neutraliser” la dégradation de valeur liée au surplus, et comment ce besoin dépend du coût des batteries, du CO2, et du rôle résiduel du thermique | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_02 | Q4 | L’enjeu est de trouver un langage simple | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_03 | Q4 | On exprime le besoin de batteries comme une combinaison de puissance et d’énergie | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_04 | Q4 | Définitions clés | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_05 | Q4 | Une batterie se caractérise par une puissance (GW) et une énergie (GWh) | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_06 | Q4 | La durée équivalente est l’énergie divisée par la puissance | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_07 | Q4 | Le rendement aller-retour réduit l’énergie utile restituée | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_08 | Q4 | Le FAR mesure la part du surplus absorbée par des puits, dont la batterie | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_09 | Q4 | Le SR mesure l’ampleur du surplus à absorber | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_10 | Q4 | L’ IR reflète la rigidité qui peut créer un surplus même sans PV | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_11 | Q4 | Le TTL est un repère de prix élevé sur heures “thermiques” qui conditionne le spread et donc la valeur économique du stockage | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_12 | Q4 | Définition opérationnelle du “bon niveau” | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_13 | Q4 | Le bon niveau de batteries n’est pas “zéro heure négative” | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 20 | SLIDE_20_14 | Q4 | C’est un compromis défini par un critère business explicite, par exemple stabiliser le capture ratio PV au-dessus d’un seuil, ou réduire les heures négatives sous un certain niveau. | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_01 | Q4 | Question 4 — Hypothèses structurantes (ce qui doit être vrai pour que la logique tienne) Hypothèse H4.1 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_02 | Q4 | Les batteries améliorent le capture ratio PV si elles chargent majoritairement pendant les heures PV à bas prix et déchargent pendant les heures non-PV à prix plus élevé | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_03 | Q4 | Hypothèse H4.2 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_04 | Q4 | Les batteries réduisent les heures négatives si elles agissent comme un puits pendant les heures où SR est matérialisé en prix négatif | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_05 | Q4 | Cette efficacité dépend de la concordance horaire entre surplus PV et disponibilité de charge | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_06 | Q4 | Hypothèse H4.3 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_07 | Q4 | Rendements décroissants | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_08 | Q4 | Au-delà d’un certain niveau, ajouter des batteries réduit peu les heures négatives car le surplus restant est soit trop long, soit trop simultané à l’échelle régionale, soit d’origine structurelle liée à un IR élevé | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_09 | Q4 | Hypothèse H4.4 | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_10 | Q4 | Le CO2 et le gaz modifient surtout l’intérêt économique des batteries via les spreads, plus que la physique du surplus | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_11 | Q4 | Le SR et l’IR ne changent pas parce que le CO2 change | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_12 | Q4 | Définitions rappelées | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_13 | Q4 | SR mesure la taille du surplus | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_14 | Q4 | FAR mesure la part absorbée | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_15 | Q4 | IR mesure la rigidité | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 21 | SLIDE_21_16 | Q4 | TTL sert de repère de prix haut pour évaluer les spreads et la valeur du stockage. | yes | question_fallback | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02; outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 | Q4-H-01; Q4-H-02; Q4-S-01; Q4-S-02 | Q4 |
| 22 | SLIDE_22_01 | Q4 | Question 4 — Tests empiriques et calculs “pédestres” (adéquation puis plausibilité économique) Test T4.1 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01 | Q4-H-01 | Q4 |
| 22 | SLIDE_22_02 | Q4 | Adéquation physique simple | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01 | Q4-H-01 | Q4 |
| 22 | SLIDE_22_03 | Q4 | On simule un comportement de batterie volontairement simple et transparent | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01 | Q4-H-01 | Q4 |
| 22 | SLIDE_22_04 | Q4 | La batterie charge pendant les heures de surplus PV, sous contrainte de puissance et d’état de charge | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01 | Q4-H-01 | Q4 |
| 22 | SLIDE_22_05 | Q4 | Elle décharge pendant des heures non-surplus, avec une règle fixe et explicable | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01 | Q4-H-01 | Q4 |
| 22 | SLIDE_22_06 | Q4 | On mesure l’effet sur FAR, sur le nombre d’heures négatives, et sur le capture ratio PV | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01 | Q4-H-01 | Q4 |
| 22 | SLIDE_22_07 | Q4 | Test T4.2 | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01 | Q4-H-01 | Q4 |
| 22 | SLIDE_22_08 | Q4 | Courbe de rendement décroissant | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01 | Q4-H-01 | Q4 |
| 22 | SLIDE_22_09 | Q4 | On répète le test pour plusieurs tailles de batteries | yes | direct_slide_match | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01 | Q4-H-01 | Q4 |

### 4.5 Catalogue de preuves
| run_id | question_id | test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260210_150232 | Q1 | Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | nan | PASS | 4.1020408163265305 | score present | Le score de bascule marche est exploitable. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-01 |
| FULL_20260210_150232 | Q1 | Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | nan | PASS | far_energy,ir_p10,sr_energy | SR/FAR/IR presents | Le stress physique est calculable. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-02 |
| FULL_20260210_150232 | Q1 | Q1-H-03 | SPEC2-Q1 | HIST | nan | WARN | 42.86% | >=50% | Concordance mesuree entre bascules marche et physique. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-03 |
| FULL_20260210_150232 | Q1 | Q1-H-04 | Slides 4-6 | HIST | nan | PASS | 0.914 | confidence moyenne >=0.60 | Proxy de robustesse du diagnostic de bascule. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-H-04 |
| FULL_20260210_150232 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260210_150232 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260210_150232 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260210_150232 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260210_150232 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260210_150232 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260210_150232 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260210_150232 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 4 | >=1 bascule | Le scenario fournit une variation exploitable. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260210_150232 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | BASE | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260210_150232 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260210_150232 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | FLEX_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260210_150232 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | LOW_RIGIDITY | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260210_150232\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260210_150232 | Q2 | Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | nan | PASS | 14 | >0 lignes | Les pentes historiques sont calculees. | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-01 |
| FULL_20260210_150232 | Q2 | Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | nan | PASS | n,p_value,r2 | r2,p_value,n disponibles | La robustesse statistique est lisible. | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-02 |
| FULL_20260210_150232 | Q2 | Q2-H-03 | Slides 10-13 | HIST | nan | PASS | 6 | >0 lignes | Les drivers de pente sont disponibles. | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-H-03 |
| FULL_20260210_150232 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | BASE | PASS | 8 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260210_150232 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | 8 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260210_150232 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | 8 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260210_150232 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | BASE | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260210_150232 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260210_150232 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. | outputs\combined\FULL_20260210_150232\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260210_150232 | Q3 | Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | nan | PASS | 7 | >0 lignes | Les tendances historiques sont calculees. | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-01 |
| FULL_20260210_150232 | Q3 | Q3-H-02 | SPEC2-Q3 | HIST | nan | PASS | 2 | status valides | Les statuts business sont renseignes. | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-H-02 |
| FULL_20260210_150232 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | BASE | NON_TESTABLE | hors_scope=85.71% | hors_scope < 80% | Le scenario reste majoritairement hors scope Stage 2; inversion peu informative. | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260210_150232 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | NON_TESTABLE | hors_scope=100.00% | hors_scope < 80% | Le scenario reste majoritairement hors scope Stage 2; inversion peu informative. | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260210_150232 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | FLEX_UP | NON_TESTABLE | hors_scope=85.71% | hors_scope < 80% | Le scenario reste majoritairement hors scope Stage 2; inversion peu informative. | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260210_150232 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | NON_TESTABLE | hors_scope=100.00% | hors_scope < 80% | Le scenario reste majoritairement hors scope Stage 2; inversion peu informative. | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260210_150232 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | BASE | NON_TESTABLE | hors_scope=85.71% | hors_scope < 80% | Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3. | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260210_150232 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | NON_TESTABLE | hors_scope=100.00% | hors_scope < 80% | Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3. | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260210_150232 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | FLEX_UP | NON_TESTABLE | hors_scope=85.71% | hors_scope < 80% | Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3. | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260210_150232 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | NON_TESTABLE | hors_scope=100.00% | hors_scope < 80% | Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3. | outputs\combined\FULL_20260210_150232\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260210_150232 | Q4 | Q4-H-01 | SPEC2-Q4/Slides 22 | HIST | nan | PASS | HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED | 3 modes executes | Les trois modes Q4 sont disponibles. | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-01 |
| FULL_20260210_150232 | Q4 | Q4-H-02 | SPEC2-Q4 | HIST | nan | PASS | PASS | pas de FAIL | Les invariants physiques batterie sont respectes. | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-H-02 |
| FULL_20260210_150232 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | BASE | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260210_150232 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | FLEX_UP | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260210_150232 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260210_150232 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260210_150232 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | BASE | PASS | 141.4176326086802 | capture apres finite | Sensibilite valeur exploitable. | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260210_150232 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | FLEX_UP | PASS | 141.39276677627964 | capture apres finite | Sensibilite valeur exploitable. | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260210_150232 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | 146.5825566444785 | capture apres finite | Sensibilite valeur exploitable. | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260210_150232 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | 152.5749842611698 | capture apres finite | Sensibilite valeur exploitable. | outputs\combined\FULL_20260210_150232\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260210_150232 | Q5 | Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | nan | PASS | ttl=419.95, tca=370.83959999999996 | ttl/tca finis | L'ancre thermique est quantifiable. | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv#test_id=Q5-H-01 |
| FULL_20260210_150232 | Q5 | Q5-H-02 | SPEC2-Q5 | HIST | nan | PASS | dCO2=0.36727272727272725, dGas=1.8181818181818181 | >0 | Sensibilites analytiques coherentes. | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv#test_id=Q5-H-02 |
| FULL_20260210_150232 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | BASE | PASS | 1 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260210_150232 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | 1 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260210_150232 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | 1 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260210_150232 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | 1 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260210_150232 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | BASE | PASS | 29.094563543428396 | valeur finie | CO2 requis interpretable. | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260210_150232 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | 65.19377737154454 | valeur finie | CO2 requis interpretable. | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260210_150232 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | -11.917360382561618 | valeur finie | CO2 requis interpretable. | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260210_150232 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | 84.09456354342841 | valeur finie | CO2 requis interpretable. | outputs\combined\FULL_20260210_150232\Q5\test_ledger.csv#test_id=Q5-S-02 |

## 5. Ecarts restants (obligatoire)

Aucun ecart critique detecte par les quality gates.
