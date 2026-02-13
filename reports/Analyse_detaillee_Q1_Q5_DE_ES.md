# Rapport Final V2.3 - Run `FULL_20260212_FIX10_DE_ES`

## 1. Page de garde
- Date de generation: `2026-02-12 21:17:03 UTC`
- Run combine source: `outputs\combined\FULL_20260212_FIX10_DE_ES`
- Perimetre pays declare: `DE, ES`
- Fenetre historique de reference: `2018-2024`
- Horizons prospectifs de reference: `2030/2040`
- Questions couvertes: `Q1, Q2, Q3, Q4, Q5`
- Avertissement methodologique: cette analyse est empirique et scenarisee; ce n'est pas un modele d'equilibre complet.

### Scenarios executes par question
- `Q1`: BASE, DEMAND_UP, LOW_RIGIDITY
- `Q2`: BASE, HIGH_CO2, HIGH_GAS
- `Q3`: BASE, DEMAND_UP, LOW_RIGIDITY
- `Q4`: BASE, HIGH_CO2, HIGH_GAS
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
Le perimetre couvre `DE, ES` et un run combine unique. Les resultats historiques et prospectifs sont presentes separement puis compares.
13 tests ont ete executes, dont HIST=4 et SCEN=9. Repartition des statuts: PASS=12, WARN=1, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 9 ligne(s) de test scenario.

### Audit block
- Definitions: negative price = `price < 0`, low-price hours = `price < 5`.
- Definitions: `load_mw = load_total_mw - psh_pumping_mw`; PSH pumping is counted as a flexibility sink and not double-counted in load.
- Thresholds: h_negative>=200.0000, h_below_5>=500.0000, low_price_share>=0.0571, capture_ratio_pv<=0.8000, capture_ratio_wind<=0.9000, sr_energy>=0.0100, sr_hours>=0.1000, ir_p10>=1.5000.
- Years used: [2018, 2019, 2020, 2021, 2022, 2023, 2024].
- Quality flags: {'OK': 14}.

### Resultats historiques test par test
- **Q1-H-01** (HIST/nan) - Score marche de bascule. Ce test verifie: La signature marche de phase 2 est calculee et exploitable.. Regle: `stage2_market_score present et non vide`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `score present` ; statut: `PASS`. Interpretation metier: Le score de bascule marche est exploitable.. Resultat conforme a la regle definie. [evidence:Q1-H-01] [source:SPEC2-Q1/Slides 2-4]
- **Q1-H-02** (HIST/nan) - Stress physique SR/FAR/IR. Ce test verifie: La bascule physique est fondee sur SR/FAR/IR.. Regle: `sr_energy/far_energy/ir_p10 presentes`. Valeur observee: `far_energy,ir_p10,sr_energy` ; seuil/regle de comparaison: `SR/FAR/IR presents` ; statut: `PASS`. Interpretation metier: Le stress physique est calculable.. Resultat conforme a la regle definie. [evidence:Q1-H-02] [source:SPEC2-Q1/Slides 3-4]
- **Q1-H-03** (HIST/nan) - Concordance marche vs physique. Ce test verifie: La relation entre bascule marche et bascule physique est mesurable.. Regle: `bascule_year_market et bascule_year_physical comparables`. Valeur observee: `strict=50.00%; concordant_ou_explique=50.00%; n=2; explained=1; reasons=strict_equal_year:1;year_gap_unexplained:1` ; seuil/regle de comparaison: `concordant_ou_explique >= 80%` ; statut: `WARN`. Interpretation metier: Concordance partielle; divergences a expliquer pays par pays.. Resultat exploitable avec prudence et justification explicite. [evidence:Q1-H-03] [source:SPEC2-Q1]
- **Q1-H-04** (HIST/nan) - Robustesse seuils. Ce test verifie: Le diagnostic reste stable sous variation raisonnable de seuils.. Regle: `delta bascules sous choc de seuil <= 50%`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `confidence moyenne >=0.60` ; statut: `PASS`. Interpretation metier: Proxy de robustesse du diagnostic de bascule.. Resultat conforme a la regle definie. [evidence:Q1-H-04] [source:Slides 4-6]

### Resultats prospectifs test par test (par scenario)
#### Scenario `BASE`
- **Q1-S-01** (SCEN/BASE) - Bascule projetee par scenario. Ce test verifie: Chaque scenario fournit un diagnostic de bascule projetee.. Regle: `Q1_country_summary non vide en SCEN`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: La bascule projetee est produite.. Resultat conforme a la regle definie. [evidence:Q1-S-01] [source:SPEC2-Q1/Slides 5]
- **Q1-S-02** (SCEN/BASE) - Effets DEMAND_UP/LOW_RIGIDITY. Ce test verifie: Les leviers scenario modifient la bascule vs BASE.. Regle: `delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share)`. Valeur observee: `reference_scenario` ; seuil/regle de comparaison: `scenario de reference` ; statut: `PASS`. Interpretation metier: BASE est la reference explicite pour le calcul de sensibilite; pas de delta attendu.. Resultat conforme a la regle definie. [evidence:Q1-S-02] [source:SPEC2-Q1/Slides 5]
- **Q1-S-03** (SCEN/BASE) - Qualite de causalite. Ce test verifie: Le regime_coherence respecte le seuil d'interpretation.. Regle: `part regime_coherence >= seuil min`. Valeur observee: `100.00%` ; seuil/regle de comparaison: `>=50% lignes >=0.55` ; statut: `PASS`. Interpretation metier: La coherence scenario est lisible.. Resultat conforme a la regle definie. [evidence:Q1-S-03] [source:SPEC2-Q1]
#### Scenario `DEMAND_UP`
- **Q1-S-01** (SCEN/DEMAND_UP) - Bascule projetee par scenario. Ce test verifie: Chaque scenario fournit un diagnostic de bascule projetee.. Regle: `Q1_country_summary non vide en SCEN`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: La bascule projetee est produite.. Resultat conforme a la regle definie. [evidence:Q1-S-01] [source:SPEC2-Q1/Slides 5]
- **Q1-S-02** (SCEN/DEMAND_UP) - Effets DEMAND_UP/LOW_RIGIDITY. Ce test verifie: Les leviers scenario modifient la bascule vs BASE.. Regle: `delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share)`. Valeur observee: `finite_share=0.00%; nonzero_share=0.00%; req_defined=100.00%; n_countries=2` ; seuil/regle de comparaison: `nonzero_share >= 20% (scenarios non-BASE)` ; statut: `PASS`. Interpretation metier: Delta vs BASE nul/non defini, mais solveur required_lever disponible et interpretable.. Resultat conforme a la regle definie. [evidence:Q1-S-02] [source:SPEC2-Q1/Slides 5]
- **Q1-S-03** (SCEN/DEMAND_UP) - Qualite de causalite. Ce test verifie: Le regime_coherence respecte le seuil d'interpretation.. Regle: `part regime_coherence >= seuil min`. Valeur observee: `100.00%` ; seuil/regle de comparaison: `>=50% lignes >=0.55` ; statut: `PASS`. Interpretation metier: La coherence scenario est lisible.. Resultat conforme a la regle definie. [evidence:Q1-S-03] [source:SPEC2-Q1]
#### Scenario `LOW_RIGIDITY`
- **Q1-S-01** (SCEN/LOW_RIGIDITY) - Bascule projetee par scenario. Ce test verifie: Chaque scenario fournit un diagnostic de bascule projetee.. Regle: `Q1_country_summary non vide en SCEN`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: La bascule projetee est produite.. Resultat conforme a la regle definie. [evidence:Q1-S-01] [source:SPEC2-Q1/Slides 5]
- **Q1-S-02** (SCEN/LOW_RIGIDITY) - Effets DEMAND_UP/LOW_RIGIDITY. Ce test verifie: Les leviers scenario modifient la bascule vs BASE.. Regle: `delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share)`. Valeur observee: `finite_share=0.00%; nonzero_share=0.00%; req_defined=100.00%; n_countries=2` ; seuil/regle de comparaison: `nonzero_share >= 20% (scenarios non-BASE)` ; statut: `PASS`. Interpretation metier: Delta vs BASE nul/non defini, mais solveur required_lever disponible et interpretable.. Resultat conforme a la regle definie. [evidence:Q1-S-02] [source:SPEC2-Q1/Slides 5]
- **Q1-S-03** (SCEN/LOW_RIGIDITY) - Qualite de causalite. Ce test verifie: Le regime_coherence respecte le seuil d'interpretation.. Regle: `part regime_coherence >= seuil min`. Valeur observee: `100.00%` ; seuil/regle de comparaison: `>=50% lignes >=0.55` ; statut: `PASS`. Interpretation metier: La coherence scenario est lisible.. Resultat conforme a la regle definie. [evidence:Q1-S-03] [source:SPEC2-Q1]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 6 ligne(s), 1 metrique(s) et 3 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| bascule_year_market | BASE | 0.0000 | NaN | NaN | NaN | NaN |
| bascule_year_market | DEMAND_UP | 0.0000 | NaN | NaN | NaN | NaN |
| bascule_year_market | LOW_RIGIDITY | 0.0000 | NaN | NaN | NaN | NaN |

Historique Q1: 2 pays avec bascule analysee; confiance moyenne=1.0000.
Synthese scenario Q1:
| scenario_id | countries | mean_bascule_year_market | mean_bascule_confidence |
| --- | --- | --- | --- |
| BASE | 2.0000 | NaN | 0.0000 |
| DEMAND_UP | 2.0000 | NaN | 0.0000 |
| LOW_RIGIDITY | 2.0000 | NaN | 0.0000 |

### Robustesse / fragilite
Statuts ledger: PASS=12, WARN=1, FAIL=0, NON_TESTABLE=0. Checks severes: 6 sur 247.
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
| Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | NaN | PASS | 2.0 | score present | Le score de bascule marche est exploitable. |
| Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | NaN | PASS | far_energy,ir_p10,sr_energy | SR/FAR/IR presents | Le stress physique est calculable. |
| Q1-H-03 | SPEC2-Q1 | HIST | NaN | WARN | strict=50.00%; concordant_ou_explique=50.00%; n=2; explained=1; reasons=strict_equal_year:1;year_gap_unexplained:1 | concordant_ou_explique >= 80% | Concordance partielle; divergences a expliquer pays par pays. |
| Q1-H-04 | Slides 4-6 | HIST | NaN | PASS | 1.000 | confidence moyenne >=0.60 | Proxy de robustesse du diagnostic de bascule. |
| Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | 2 | >0 lignes | La bascule projetee est produite. |
| Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 2 | >0 lignes | La bascule projetee est produite. |
| Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 2 | >0 lignes | La bascule projetee est produite. |
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | reference_scenario | scenario de reference | BASE est la reference explicite pour le calcul de sensibilite; pas de delta attendu. |
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | finite_share=0.00%; nonzero_share=0.00%; req_defined=100.00%; n_countries=2 | nonzero_share >= 20% (scenarios non-BASE) | Delta vs BASE nul/non defini, mais solveur required_lever disponible et interpretable. |
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | finite_share=0.00%; nonzero_share=0.00%; req_defined=100.00%; n_countries=2 | nonzero_share >= 20% (scenarios non-BASE) | Delta vs BASE nul/non defini, mais solveur required_lever disponible et interpretable. |
| Q1-S-03 | SPEC2-Q1 | SCEN | BASE | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
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
Le perimetre couvre `DE, ES` et un run combine unique. Les resultats historiques et prospectifs sont presentes separement puis compares.
9 tests ont ete executes, dont HIST=3 et SCEN=6. Repartition des statuts: PASS=6, WARN=3, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 6 ligne(s) de test scenario.

### Audit block
- Definitions: negative price = `price < 0`, low-price hours = `price < 5`.
- Definitions: `load_mw = load_total_mw - psh_pumping_mw`; PSH pumping is counted as a flexibility sink and not double-counted in load.
- Years used for regressions: [2018, 2019, 2020, 2021, 2023, 2024].
- Regression x-axis: ['pv_penetration_share_generation', 'wind_penetration_share_generation'].
- Robustness flags: {'FRAGILE': 2, 'NON_TESTABLE': 2}.

### Resultats historiques test par test
- **Q2-H-01** (HIST/nan) - Pentes OLS post-bascule. Ce test verifie: Les pentes PV/Wind sont estimees en historique.. Regle: `Q2_country_slopes non vide`. Valeur observee: `4.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Les pentes historiques sont calculees.. Resultat conforme a la regle definie. [evidence:Q2-H-01] [source:SPEC2-Q2/Slides 10]
- **Q2-H-02** (HIST/nan) - Robustesse statistique. Ce test verifie: R2/p-value/n sont disponibles pour qualifier la robustesse.. Regle: `colonnes r2,p_value,n presentes`. Valeur observee: `n,p_value,r2` ; seuil/regle de comparaison: `r2,p_value,n disponibles` ; statut: `PASS`. Interpretation metier: La robustesse statistique est lisible.. Resultat conforme a la regle definie. [evidence:Q2-H-02] [source:SPEC2-Q2/Slides 10-12]
- **Q2-H-03** (HIST/nan) - Drivers physiques. Ce test verifie: Les drivers SR/FAR/IR/corr VRE-load sont exploites.. Regle: `driver correlations non vides`. Valeur observee: `4.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Les drivers de pente sont disponibles.. Resultat conforme a la regle definie. [evidence:Q2-H-03] [source:Slides 10-13]

### Resultats prospectifs test par test (par scenario)
#### Scenario `BASE`
- **Q2-S-01** (SCEN/BASE) - Pentes projetees. Ce test verifie: Les pentes sont reproduites en mode scenario.. Regle: `Q2_country_slopes non vide en SCEN`. Valeur observee: `4.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Pentes prospectives calculees.. Resultat conforme a la regle definie. [evidence:Q2-S-01] [source:SPEC2-Q2/Slides 11]
- **Q2-S-02** (SCEN/BASE) - Delta pente vs BASE. Ce test verifie: Les differences de pente vs BASE sont calculables.. Regle: `delta slope par pays/tech vs BASE`. Valeur observee: `finite=0.00%; robust=0.00%; reason_known=100.00%` ; seuil/regle de comparaison: `finite_share >= 20%` ; statut: `WARN`. Interpretation metier: Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable.. Resultat exploitable avec prudence et justification explicite. [evidence:Q2-S-02] [source:SPEC2-Q2]
#### Scenario `HIGH_CO2`
- **Q2-S-01** (SCEN/HIGH_CO2) - Pentes projetees. Ce test verifie: Les pentes sont reproduites en mode scenario.. Regle: `Q2_country_slopes non vide en SCEN`. Valeur observee: `4.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Pentes prospectives calculees.. Resultat conforme a la regle definie. [evidence:Q2-S-01] [source:SPEC2-Q2/Slides 11]
- **Q2-S-02** (SCEN/HIGH_CO2) - Delta pente vs BASE. Ce test verifie: Les differences de pente vs BASE sont calculables.. Regle: `delta slope par pays/tech vs BASE`. Valeur observee: `finite=0.00%; robust=0.00%; reason_known=100.00%` ; seuil/regle de comparaison: `finite_share >= 20%` ; statut: `WARN`. Interpretation metier: Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable.. Resultat exploitable avec prudence et justification explicite. [evidence:Q2-S-02] [source:SPEC2-Q2]
#### Scenario `HIGH_GAS`
- **Q2-S-01** (SCEN/HIGH_GAS) - Pentes projetees. Ce test verifie: Les pentes sont reproduites en mode scenario.. Regle: `Q2_country_slopes non vide en SCEN`. Valeur observee: `4.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Pentes prospectives calculees.. Resultat conforme a la regle definie. [evidence:Q2-S-01] [source:SPEC2-Q2/Slides 11]
- **Q2-S-02** (SCEN/HIGH_GAS) - Delta pente vs BASE. Ce test verifie: Les differences de pente vs BASE sont calculables.. Regle: `delta slope par pays/tech vs BASE`. Valeur observee: `finite=0.00%; robust=0.00%; reason_known=100.00%` ; seuil/regle de comparaison: `finite_share >= 20%` ; statut: `WARN`. Interpretation metier: Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable.. Resultat exploitable avec prudence et justification explicite. [evidence:Q2-S-02] [source:SPEC2-Q2]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 12 ligne(s), 1 metrique(s) et 3 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| slope | BASE | 0.0000 | NaN | NaN | NaN | NaN |
| slope | HIGH_CO2 | 0.0000 | NaN | NaN | NaN | NaN |
| slope | HIGH_GAS | 0.0000 | NaN | NaN | NaN | NaN |

Distribution des pentes historiques par techno:
| tech | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- |
| PV | 2.0000 | -5.1589 | -5.1589 | -5.5781 | -4.7396 |
| WIND | 2.0000 | -0.3634 | -0.3634 | -0.4836 | -0.2432 |

### Robustesse / fragilite
Statuts ledger: PASS=6, WARN=3, FAIL=0, NON_TESTABLE=0. Checks severes: 2 sur 254.
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
| Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | NaN | PASS | 4 | >0 lignes | Les pentes historiques sont calculees. |
| Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | NaN | PASS | n,p_value,r2 | r2,p_value,n disponibles | La robustesse statistique est lisible. |
| Q2-H-03 | Slides 10-13 | HIST | NaN | PASS | 4 | >0 lignes | Les drivers de pente sont disponibles. |
| Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | BASE | PASS | 4 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | 4 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | 4 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-02 | SPEC2-Q2 | SCEN | BASE | WARN | finite=0.00%; robust=0.00%; reason_known=100.00% | finite_share >= 20% | Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable. |
| Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | finite=0.00%; robust=0.00%; reason_known=100.00% | finite_share >= 20% | Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable. |
| Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | finite=0.00%; robust=0.00%; reason_known=100.00% | finite_share >= 20% | Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable. |

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
Le perimetre couvre `DE, ES` et un run combine unique. Les resultats historiques et prospectifs sont presentes separement puis compares.
8 tests ont ete executes, dont HIST=2 et SCEN=6. Repartition des statuts: PASS=8, WARN=0, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 6 ligne(s) de test scenario.

### Audit block
- Definitions: negative price = `price < 0`, low-price hours = `price < 5`.
- Definitions: `load_mw = load_total_mw - psh_pumping_mw`; PSH pumping is counted as a flexibility sink and not double-counted in load.
- Years used: [2024].
- Quality flags: {'nan': 2}.
- Scenario assumptions present in rows: scenario_id, assumed_demand_multiplier, assumed_must_run_reduction_factor, assumed_flex_multiplier.

### Resultats historiques test par test
- **Q3-H-01** (HIST/nan) - Tendances glissantes. Ce test verifie: Les tendances h_negative et capture_ratio sont estimees.. Regle: `Q3_status non vide`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Les tendances historiques sont calculees.. Resultat conforme a la regle definie. [evidence:Q3-H-01] [source:SPEC2-Q3/Slides 16]
- **Q3-H-02** (HIST/nan) - Statuts sortie phase 2. Ce test verifie: Les statuts degradation/stabilisation/amelioration sont attribues.. Regle: `status dans ensemble attendu`. Valeur observee: `1.0000` ; seuil/regle de comparaison: `status valides` ; statut: `PASS`. Interpretation metier: Les statuts business sont renseignes.. Resultat conforme a la regle definie. [evidence:Q3-H-02] [source:SPEC2-Q3]

### Resultats prospectifs test par test (par scenario)
#### Scenario `BASE`
- **Q3-S-01** (SCEN/BASE) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `hors_scope=100.00%; inversion=0` ; seuil/regle de comparaison: `hors_scope < 80% ou inversion deja atteinte` ; statut: `PASS`. Interpretation metier: Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites.. Resultat conforme a la regle definie. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/BASE) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `hors_scope=100.00%; inversion=0` ; seuil/regle de comparaison: `hors_scope < 80% ou inversion deja atteinte` ; statut: `PASS`. Interpretation metier: Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise.. Resultat conforme a la regle definie. [evidence:Q3-S-02] [source:Slides 17-19]
#### Scenario `DEMAND_UP`
- **Q3-S-01** (SCEN/DEMAND_UP) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `hors_scope=100.00%; inversion=0` ; seuil/regle de comparaison: `hors_scope < 80% ou inversion deja atteinte` ; statut: `PASS`. Interpretation metier: Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites.. Resultat conforme a la regle definie. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/DEMAND_UP) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `hors_scope=100.00%; inversion=0` ; seuil/regle de comparaison: `hors_scope < 80% ou inversion deja atteinte` ; statut: `PASS`. Interpretation metier: Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise.. Resultat conforme a la regle definie. [evidence:Q3-S-02] [source:Slides 17-19]
#### Scenario `LOW_RIGIDITY`
- **Q3-S-01** (SCEN/LOW_RIGIDITY) - Conditions minimales d'inversion. Ce test verifie: Les besoins demande/must-run/flex sont quantifies en scenario.. Regle: `inversion_k, inversion_r et additional_absorbed presentes`. Valeur observee: `hors_scope=100.00%; inversion=0` ; seuil/regle de comparaison: `hors_scope < 80% ou inversion deja atteinte` ; statut: `PASS`. Interpretation metier: Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites.. Resultat conforme a la regle definie. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
- **Q3-S-02** (SCEN/LOW_RIGIDITY) - Validation entree phase 3. Ce test verifie: Le statut prospectif est interpretable pour la transition phase 3.. Regle: `status non vide en SCEN`. Valeur observee: `hors_scope=100.00%; inversion=0` ; seuil/regle de comparaison: `hors_scope < 80% ou inversion deja atteinte` ; statut: `PASS`. Interpretation metier: Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise.. Resultat conforme a la regle definie. [evidence:Q3-S-02] [source:Slides 17-19]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 12 ligne(s), 2 metrique(s) et 3 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| inversion_k_demand | BASE | 2.0000 | -6 839.54 | -6 839.54 | -6 999.60 | -6 679.49 |
| inversion_k_demand | DEMAND_UP | 2.0000 | -6 839.54 | -6 839.54 | -6 999.60 | -6 679.49 |
| inversion_k_demand | LOW_RIGIDITY | 2.0000 | -6 839.54 | -6 839.54 | -6 999.60 | -6 679.49 |
| inversion_r_mustrun | BASE | 2.0000 | -0.8483 | -0.8483 | -0.9936 | -0.7030 |
| inversion_r_mustrun | DEMAND_UP | 2.0000 | -0.8483 | -0.8483 | -0.9936 | -0.7030 |
| inversion_r_mustrun | LOW_RIGIDITY | 2.0000 | -0.8483 | -0.8483 | -0.9936 | -0.7030 |

Distribution des statuts historiques Q3:
| status | n |
| --- | --- |
| CONTINUES | 2.0000 |

### Robustesse / fragilite
Statuts ledger: PASS=8, WARN=0, FAIL=0, NON_TESTABLE=0. Checks severes: 1 sur 246.
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
| Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | NaN | PASS | 2 | >0 lignes | Les tendances historiques sont calculees. |
| Q3-H-02 | SPEC2-Q3 | HIST | NaN | PASS | 1 | status valides | Les statuts business sont renseignes. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | BASE | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites. |
| Q3-S-02 | Slides 17-19 | SCEN | BASE | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise. |
| Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise. |
| Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise. |

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
Le perimetre couvre `DE, ES` et un run combine unique. Les resultats historiques et prospectifs sont presentes separement puis compares.
8 tests ont ete executes, dont HIST=2 et SCEN=6. Repartition des statuts: PASS=8, WARN=0, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 6 ligne(s) de test scenario.

### Audit block
- Definitions: negative price = `price < 0`, low-price hours = `price < 5`.
- Definitions: `load_mw = load_total_mw - psh_pumping_mw`; PSH pumping is counted as a flexibility sink and not double-counted in load.
- Years used: [2024].
- Dispatch modes: ['SURPLUS_FIRST'].
- Grid columns: `bess_power_mw_test`, `bess_energy_mwh_test`, `bess_duration_h_test`.
- Quality/status flags: {'met_after_grid_expansion': 1, 'grid_too_small': 1}.

### Resultats historiques test par test
- **Q4-H-01** (HIST/nan) - Simulation BESS 3 modes. Ce test verifie: SURPLUS_FIRST, PRICE_ARBITRAGE_SIMPLE et PV_COLOCATED sont executes.. Regle: `3 modes executes avec sorties non vides`. Valeur observee: `HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED` ; seuil/regle de comparaison: `3 modes executes` ; statut: `PASS`. Interpretation metier: Les trois modes Q4 sont disponibles.. Resultat conforme a la regle definie. [evidence:Q4-H-01] [source:SPEC2-Q4/Slides 22]
- **Q4-H-02** (HIST/nan) - Invariants physiques BESS. Ce test verifie: Bornes SOC/puissance/energie respectees (mode physique de reference) avec garde-fous structurels sur modes alternatifs.. Regle: `aucun FAIL physique/structurel pertinent`. Valeur observee: `WARN` ; seuil/regle de comparaison: `aucun FAIL physique` ; statut: `PASS`. Interpretation metier: Les invariants physiques batterie sont respectes. Des avertissements non-physiques peuvent subsister (objectif/scenario).. Resultat conforme a la regle definie. [evidence:Q4-H-02] [source:SPEC2-Q4]

### Resultats prospectifs test par test (par scenario)
#### Scenario `BASE`
- **Q4-S-01** (SCEN/BASE) - Comparaison effet batteries par scenario. Ce test verifie: Impact FAR/surplus/capture compare entre scenarios utiles.. Regle: `Q4 summary non vide pour >=1 scenario`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Resultats Q4 prospectifs disponibles.. Resultat conforme a la regle definie. [evidence:Q4-S-01] [source:SPEC2-Q4/Slides 23]
- **Q4-S-02** (SCEN/BASE) - Sensibilite valeur commodites. Ce test verifie: Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.. Regle: `delta pv_capture ou revenus vs BASE`. Valeur observee: `share_finite=100.00%` ; seuil/regle de comparaison: `>=80% valeurs finies` ; statut: `PASS`. Interpretation metier: Sensibilite valeur exploitable sur le panel.. Resultat conforme a la regle definie. [evidence:Q4-S-02] [source:Slides 23-25]
#### Scenario `HIGH_CO2`
- **Q4-S-01** (SCEN/HIGH_CO2) - Comparaison effet batteries par scenario. Ce test verifie: Impact FAR/surplus/capture compare entre scenarios utiles.. Regle: `Q4 summary non vide pour >=1 scenario`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Resultats Q4 prospectifs disponibles.. Resultat conforme a la regle definie. [evidence:Q4-S-01] [source:SPEC2-Q4/Slides 23]
- **Q4-S-02** (SCEN/HIGH_CO2) - Sensibilite valeur commodites. Ce test verifie: Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.. Regle: `delta pv_capture ou revenus vs BASE`. Valeur observee: `share_finite=100.00%` ; seuil/regle de comparaison: `>=80% valeurs finies` ; statut: `PASS`. Interpretation metier: Sensibilite valeur exploitable sur le panel.. Resultat conforme a la regle definie. [evidence:Q4-S-02] [source:Slides 23-25]
#### Scenario `HIGH_GAS`
- **Q4-S-01** (SCEN/HIGH_GAS) - Comparaison effet batteries par scenario. Ce test verifie: Impact FAR/surplus/capture compare entre scenarios utiles.. Regle: `Q4 summary non vide pour >=1 scenario`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Resultats Q4 prospectifs disponibles.. Resultat conforme a la regle definie. [evidence:Q4-S-01] [source:SPEC2-Q4/Slides 23]
- **Q4-S-02** (SCEN/HIGH_GAS) - Sensibilite valeur commodites. Ce test verifie: Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.. Regle: `delta pv_capture ou revenus vs BASE`. Valeur observee: `share_finite=100.00%` ; seuil/regle de comparaison: `>=80% valeurs finies` ; statut: `PASS`. Interpretation metier: Sensibilite valeur exploitable sur le panel.. Resultat conforme a la regle definie. [evidence:Q4-S-02] [source:Slides 23-25]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 22 ligne(s), 3 metrique(s) et 5 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| far_after | BASE | 2.0000 | 0.0006 | 0.0006 | 0.0000 | 0.0012 |
| far_after | HIGH_CO2 | 2.0000 | 0.0006 | 0.0006 | 0.0000 | 0.0012 |
| far_after | HIGH_GAS | 2.0000 | 0.0006 | 0.0006 | 0.0000 | 0.0012 |
| far_after | HIST_PRICE_ARBITRAGE_SIMPLE | 2.0000 | -0.0281 | -0.0281 | -0.0376 | -0.0185 |
| far_after | HIST_PV_COLOCATED | 2.0000 | -0.0496 | -0.0496 | -0.0539 | -0.0454 |
| pv_capture_price_after | BASE | 2.0000 | 57.2191 | 57.2191 | 42.6385 | 71.7997 |
| pv_capture_price_after | HIGH_CO2 | 2.0000 | 65.2514 | 65.2514 | 47.2672 | 83.2357 |
| pv_capture_price_after | HIGH_GAS | 2.0000 | 69.9205 | 69.9205 | 52.9499 | 86.8911 |
| surplus_unabs_energy_after | BASE | 2.0000 | -0.0057 | -0.0057 | -0.0114 | 0.0000 |
| surplus_unabs_energy_after | HIGH_CO2 | 2.0000 | -0.0057 | -0.0057 | -0.0114 | 0.0000 |
| surplus_unabs_energy_after | HIGH_GAS | 2.0000 | -0.0057 | -0.0057 | -0.0114 | 0.0000 |

Synthese sizing historique Q4:
| scenario_id | country | year | dispatch_mode | objective | bess_power_mw_test | bess_energy_mwh_test | bess_duration_h_test | required_bess_power_mw | required_bess_energy_mwh | required_bess_duration_h | far_before | far_after | far_before_trivial | far_after_trivial | h_negative_obs_before | h_negative_est_before | h_negative_est_after | h_negative_before | h_negative_after | h_negative_proxy_before | h_negative_proxy_after | h_negative_proxy_raw_after | h_negative_reducible_upper_bound | h_negative_upper_bound_after | h_below_5_reducible_upper_bound | h_below_5_obs_before | h_below_5_est_before | h_below_5_est_after | h_below_5_before | h_below_5_after | h_below_5_proxy_before | h_below_5_proxy_after | h_below_5_proxy_raw_after | delta_h_negative_est | delta_h_below_5_est | delta_h_negative | delta_h_below_5 | h_negative_after_source | h_below_5_after_source | baseload_price_obs_before | baseload_price_est_before | baseload_price_est_after | baseload_price_before | baseload_price_after | capture_ratio_pv_obs_before | capture_ratio_pv_est_before | capture_ratio_pv_est_after | capture_ratio_pv_before | capture_ratio_pv_after | capture_ratio_wind_obs_before | capture_ratio_wind_est_before | capture_ratio_wind_est_after | capture_ratio_wind_before | capture_ratio_wind_after | delta_capture_ratio_est_pv | delta_capture_ratio_est_wind | delta_capture_ratio_pv | delta_capture_ratio_wind | surplus_unabs_energy_before | surplus_unabs_energy_after | pv_capture_price_obs_before | pv_capture_price_est_before | pv_capture_price_est_after | pv_capture_price_before | pv_capture_price_after | wind_capture_price_obs_before | wind_capture_price_est_before | wind_capture_price_est_after | wind_capture_price_before | wind_capture_price_after | days_spread_gt50_before | days_spread_gt50_after | avg_daily_spread_before | avg_daily_spread_after | low_residual_share_before | low_residual_share_after | sr_hours_share_before | sr_hours_share_after | ir_p10_before | ir_p10_after | turned_off_family_low_price | turned_off_family_physical | turned_off_family_value_pv | turned_off_family_value_wind | turned_off_family_any | revenue_bess_price_taker | soc_min | soc_max | soc_start_mwh | soc_end_mwh | soc_end_target_mwh | charge_max | discharge_max | charge_sum_mwh | discharge_sum_mwh | charge_hours | discharge_hours | cycles_assumed_per_day | cycles_realized_per_day | simultaneous_charge_discharge_hours | energy_balance_residual | eta_roundtrip | eta_charge | eta_discharge | soc_boundary_mode | charge_vs_surplus_violation_hours | no_dispatch | proxy_quality_status | proxy_quality_reasons | output_schema_version | engine_version | compute_time_sec | cache_hit | bess_power_mw | duration_h | bess_energy_mwh | on_efficient_frontier | objective_met | objective_reason | objective_not_reached | status | reason | objective_target_value | objective_direction | objective_value_after | objective_recommendation | pv_capacity_proxy_mw | power_grid_max_mw | duration_grid_max_h | grid_expansions_used | notes_quality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HIST | DE | 2 024.00 | SURPLUS_FIRST | LOW_PRICE_TARGET | 76 260.27 | 152 520.54 | 2.0000 | 76 260.27 | 152 520.54 | 2.0000 | 0.9534 | 0.9988 | 0.0000 | 0.0000 | 457.0000 | 457.0000 | 157.5129 | 457.0000 | 157.5129 | 457.0000 | 157.5129 | 157.5129 | 457.0000 | 0.0000 | 756.0000 | 756.0000 | 756.0014 | 385.5243 | 756.0000 | 385.5243 | 756.0014 | 385.5243 | 385.5243 | -299.4871 | -370.4771 | -299.4871 | -370.4771 | est_proxy | est_proxy | 78.5155 | 78.5143 | 79.1348 | 78.5155 | 79.1348 | 0.5888 | 0.5888 | 0.6959 | 0.5888 | 0.6959 | 0.8384 | 0.8386 | 0.8468 | 0.8386 | 0.8468 | 0.1071 | 0.0082 | 0.1071 | 0.0082 | 0.4362 | 0.0114 | 46.2280 | 46.2280 | 55.0713 | 46.2280 | 55.0713 | 65.8312 | 65.8419 | 67.0150 | 65.8419 | 67.0150 | 319.0000 | 319.0000 | 112.0063 | 108.2327 | 0.0862 | 0.2836 | 0.1403 | 0.0081 | 0.3023 | 0.3055 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NaN | 0.0000 | 152 520.54 | 0.0000 | 0.0000 | 0.0000 | 24 346.34 | 33 599.28 | 8 784 474.0 | 7 730 337.2 | 1 177.00 | 805.0000 | 1.0000 | 0.1574 | 0.0000 | 0.0000 | 0.8800 | 0.9381 | 0.9381 | ZERO_END | 0.0000 | 0.0000 | PASS | NaN | 2.0.0 | v2.2.2 | 7.3906 | 0.0000 | 76 260.27 | 2.0000 | 152 520.54 | 1.0000 | 1.0000 | met_after_grid_expansion | 0.0000 | ok | met_after_grid_expansion | 200.0000 | lower_is_better | 157.5129 | NaN | 40 714.24 | 76 260.27 | 24.0000 | 1.0000 | ok |
| HIST | ES | 2 024.00 | SURPLUS_FIRST | LOW_PRICE_TARGET | 38 128.00 | 305 024.00 | 8.0000 | 38 128.00 | 305 024.00 | 8.0000 | 0.9455 | 1.0000 | 0.0000 | 0.0000 | 247.0000 | 247.0000 | 154.8614 | 247.0000 | 154.8614 | 247.0000 | 154.8614 | 154.8614 | 247.0000 | 0.0000 | 1 642.00 | 1 642.00 | 1 642.00 | 1 545.27 | 1 642.00 | 1 545.27 | 1 642.00 | 1 545.27 | 1 545.27 | -92.1386 | -96.7310 | -92.1386 | -96.7310 | est_proxy | est_proxy | 63.0395 | 63.0461 | 61.6951 | 63.0395 | 61.6951 | 0.6790 | 0.6789 | 0.8886 | 0.6789 | 0.8886 | 0.8821 | 0.8821 | 0.8540 | 0.8821 | 0.8540 | 0.2098 | -0.0281 | 0.2098 | -0.0281 | 0.5564 | 0.0000 | 42.8012 | 42.8013 | 54.8253 | 42.8013 | 54.8253 | 55.6095 | 55.6111 | 52.6847 | 55.6111 | 52.6847 | 272.0000 | 272.0000 | 71.5241 | 71.4630 | 0.0734 | 0.4730 | 0.2696 | 0.0000 | 0.3950 | 0.4077 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | NaN | 0.0000 | 257 898.16 | 0.0000 | 0.0000 | 0.0000 | 12 416.00 | 18 308.00 | 10 210 340.0 | 8 985 099.2 | 2 368.00 | 1 523.00 | 1.0000 | 0.0915 | 0.0000 | -0.0000 | 0.8800 | 0.9381 | 0.9381 | ZERO_END | 0.0000 | 0.0000 | PASS | NaN | 2.0.0 | v2.2.2 | 7.3542 | 0.0000 | 38 128.00 | 8.0000 | 305 024.00 | 1.0000 | 1.0000 | grid_too_small | 0.0000 | ok | grid_too_small | 200.0000 | lower_is_better | 154.8614 | expand_grid_to_power_mw>=57192.0;duration_h>=36.0 | 20 284.00 | 38 128.00 | 24.0000 | 1.0000 | ok |
Apercu frontiere historique Q4:
| dispatch_mode | bess_power_mw_test | bess_duration_h_test | far_after | surplus_unabs_energy_after | pv_capture_price_after |
| --- | --- | --- | --- | --- | --- |
| SURPLUS_FIRST | 0.0000 | 0.0000 | 0.9534 | 0.4362 | 46.2280 |
| SURPLUS_FIRST | 250.0000 | 2.0000 | 0.9542 | 0.4288 | 46.2558 |
| SURPLUS_FIRST | 250.0000 | 4.0000 | 0.9563 | 0.4095 | 46.2613 |
| SURPLUS_FIRST | 250.0000 | 6.0000 | 0.9582 | 0.3914 | 46.3101 |
| SURPLUS_FIRST | 250.0000 | 8.0000 | 0.9593 | 0.3809 | 46.3238 |
| SURPLUS_FIRST | 250.0000 | 12.0000 | 0.9598 | 0.3764 | 46.3441 |
| SURPLUS_FIRST | 250.0000 | 24.0000 | 0.9602 | 0.3729 | 46.3497 |
| SURPLUS_FIRST | 500.0000 | 2.0000 | 0.9549 | 0.4223 | 46.2974 |
| SURPLUS_FIRST | 500.0000 | 4.0000 | 0.9589 | 0.3854 | 46.3395 |
| SURPLUS_FIRST | 500.0000 | 6.0000 | 0.9625 | 0.3509 | 46.4303 |
| SURPLUS_FIRST | 500.0000 | 8.0000 | 0.9647 | 0.3310 | 46.4871 |
| SURPLUS_FIRST | 500.0000 | 12.0000 | 0.9655 | 0.3229 | 46.5236 |
| SURPLUS_FIRST | 500.0000 | 24.0000 | 0.9662 | 0.3168 | 46.5412 |
| SURPLUS_FIRST | 750.0000 | 2.0000 | 0.9556 | 0.4160 | 46.4191 |
| SURPLUS_FIRST | 750.0000 | 4.0000 | 0.9612 | 0.3636 | 46.5119 |
| SURPLUS_FIRST | 750.0000 | 6.0000 | 0.9664 | 0.3143 | 46.6318 |
| SURPLUS_FIRST | 750.0000 | 8.0000 | 0.9694 | 0.2867 | 46.7070 |
| SURPLUS_FIRST | 750.0000 | 12.0000 | 0.9706 | 0.2756 | 46.7670 |
| SURPLUS_FIRST | 750.0000 | 24.0000 | 0.9715 | 0.2671 | 46.7835 |
| SURPLUS_FIRST | 1 000.00 | 2.0000 | 0.9561 | 0.4108 | 46.4856 |
| SURPLUS_FIRST | 1 000.00 | 4.0000 | 0.9632 | 0.3447 | 46.6269 |
| SURPLUS_FIRST | 1 000.00 | 6.0000 | 0.9699 | 0.2816 | 46.7632 |
| SURPLUS_FIRST | 1 000.00 | 8.0000 | 0.9736 | 0.2474 | 46.8713 |
| SURPLUS_FIRST | 1 000.00 | 12.0000 | 0.9751 | 0.2334 | 46.9228 |
| SURPLUS_FIRST | 1 000.00 | 24.0000 | 0.9762 | 0.2229 | 46.9391 |
| SURPLUS_FIRST | 1 500.00 | 2.0000 | 0.9572 | 0.4008 | 46.6228 |
| SURPLUS_FIRST | 1 500.00 | 4.0000 | 0.9666 | 0.3124 | 46.8062 |
| SURPLUS_FIRST | 1 500.00 | 6.0000 | 0.9755 | 0.2292 | 47.0268 |
| SURPLUS_FIRST | 1 500.00 | 8.0000 | 0.9802 | 0.1855 | 47.1664 |
| SURPLUS_FIRST | 1 500.00 | 12.0000 | 0.9822 | 0.1666 | 47.2519 |

### Robustesse / fragilite
Statuts ledger: PASS=8, WARN=0, FAIL=0, NON_TESTABLE=0. Checks severes: 5 sur 23.
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
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | BASE | PASS | 2 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | 2 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | 2 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-02 | Slides 23-25 | SCEN | BASE | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. |
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
Le perimetre couvre `DE, ES` et un run combine unique. Les resultats historiques et prospectifs sont presentes separement puis compares.
10 tests ont ete executes, dont HIST=2 et SCEN=8. Repartition des statuts: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Le perimetre prospectif couvre 8 ligne(s) de test scenario.

### Audit block
- Definitions: negative price = `price < 0`, low-price hours = `price < 5`.
- Definitions: `load_mw = load_total_mw - psh_pumping_mw`; PSH pumping is counted as a flexibility sink and not double-counted in load.
- Years used: [2024].
- Anchor assumptions columns: `scenario_id`, `assumed_co2_price_eur_t`, `assumed_gas_price_eur_mwh_th`, `assumed_efficiency`, `assumed_emission_factor_t_per_mwh_th`, `chosen_anchor_tech`.
- Quality flags: {'target_above_anchor': 2}.

### Resultats historiques test par test
- **Q5-H-01** (HIST/nan) - Ancre thermique historique. Ce test verifie: TTL/TCA/alpha/corr sont estimes hors surplus.. Regle: `Q5_summary non vide avec ttl_obs et tca_q95`. Valeur observee: `share_fini=100.00%` ; seuil/regle de comparaison: `>=80% lignes ttl/tca finies` ; statut: `PASS`. Interpretation metier: L'ancre thermique est quantifiable sur la majorite des pays.. Resultat conforme a la regle definie. [evidence:Q5-H-01] [source:SPEC2-Q5/Slides 28]
- **Q5-H-02** (HIST/nan) - Sensibilites analytiques. Ce test verifie: dTCA/dCO2 et dTCA/dGas sont positives.. Regle: `dTCA_dCO2 > 0 et dTCA_dGas > 0`. Valeur observee: `share_positive=100.00%` ; seuil/regle de comparaison: `100% lignes >0` ; statut: `PASS`. Interpretation metier: Sensibilites analytiques globalement coherentes.. Resultat conforme a la regle definie. [evidence:Q5-H-02] [source:SPEC2-Q5]

### Resultats prospectifs test par test (par scenario)
#### Scenario `BASE`
- **Q5-S-01** (SCEN/BASE) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/BASE) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `share_finite=100.00%` ; seuil/regle de comparaison: `>=80% valeurs finies` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable sur le panel.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]
#### Scenario `HIGH_BOTH`
- **Q5-S-01** (SCEN/HIGH_BOTH) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/HIGH_BOTH) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `share_finite=100.00%` ; seuil/regle de comparaison: `>=80% valeurs finies` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable sur le panel.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]
#### Scenario `HIGH_CO2`
- **Q5-S-01** (SCEN/HIGH_CO2) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/HIGH_CO2) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `share_finite=100.00%` ; seuil/regle de comparaison: `>=80% valeurs finies` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable sur le panel.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]
#### Scenario `HIGH_GAS`
- **Q5-S-01** (SCEN/HIGH_GAS) - Sensibilites scenarisees. Ce test verifie: BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.. Regle: `Q5_summary non vide sur scenarios selectionnes`. Valeur observee: `2.0000` ; seuil/regle de comparaison: `>0 lignes` ; statut: `PASS`. Interpretation metier: Sensibilites scenario calculees.. Resultat conforme a la regle definie. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
- **Q5-S-02** (SCEN/HIGH_GAS) - CO2 requis pour TTL cible. Ce test verifie: Le CO2 requis est calcule et interpretable.. Regle: `co2_required_* non NaN`. Valeur observee: `share_finite=100.00%` ; seuil/regle de comparaison: `>=80% valeurs finies` ; statut: `PASS`. Interpretation metier: CO2 requis interpretable sur le panel.. Resultat conforme a la regle definie. [evidence:Q5-S-02] [source:SPEC2-Q5/Slides 31]

### Comparaison historique vs prospectif
La comparaison historique/prospectif contient 24 ligne(s), 3 metrique(s) et 4 scenario(s).
| metric | scenario_id | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| co2_required_base_non_negative | BASE | 2.0000 | 6.5855 | 6.5855 | 3.1710 | 10.0000 |
| co2_required_base_non_negative | HIGH_BOTH | 2.0000 | 3.6035 | 3.6035 | -44.7030 | 51.9100 |
| co2_required_base_non_negative | HIGH_CO2 | 2.0000 | 30.9550 | 30.9550 | 10.0000 | 51.9100 |
| co2_required_base_non_negative | HIGH_GAS | 2.0000 | -46.3965 | -46.3965 | -94.7030 | 1.9100 |
| tca_q95 | BASE | 2.0000 | 17.8724 | 17.8724 | 8.3959 | 27.3489 |
| tca_q95 | HIGH_BOTH | 2.0000 | 86.2258 | 86.2258 | 67.6686 | 104.7831 |
| tca_q95 | HIGH_CO2 | 2.0000 | 49.4884 | 49.4884 | 26.7595 | 72.2173 |
| tca_q95 | HIGH_GAS | 2.0000 | 54.6098 | 54.6098 | 49.3049 | 59.9147 |
| ttl_obs | BASE | 2.0000 | 40.3003 | 40.3003 | 23.2170 | 57.3835 |
| ttl_obs | HIGH_BOTH | 2.0000 | 40.3003 | 40.3003 | 23.2170 | 57.3835 |
| ttl_obs | HIGH_CO2 | 2.0000 | 51.3659 | 51.3659 | 29.6443 | 73.0874 |
| ttl_obs | HIGH_GAS | 2.0000 | 57.8212 | 57.8212 | 37.5352 | 78.1071 |

Synthese historique Q5:
| scenario_id | country | year_range_used | ttl_reference_mode | ttl_reference_year | marginal_tech | chosen_anchor_tech | fuel_used | assumed_co2_price_eur_t | assumed_gas_price_eur_mwh_th | assumed_coal_price_eur_mwh_th | assumed_efficiency | assumed_emission_factor_t_per_mwh_th | assumed_vom_eur_mwh | assumed_fuel_multiplier_vs_gas | ttl_obs | ttl_observed_eur_mwh | ttl_obs_price_cd | ttl_annual_metrics_same_year | ttl_anchor | ttl_anchor_formula | ttl_model_eur_mwh | ttl_physical | ttl_regression | ttl_method | tca_q95 | alpha | alpha_effective | corr_cd | anchor_confidence | anchor_distribution_error_p90_p95 | anchor_error_p90 | anchor_error_p95 | anchor_status | dTCA_dCO2 | dTCA_dFuel | dTCA_dGas | eta_implicit_from_dTCA_dFuel | ef_implicit_t_per_mwh_e | ttl_target | anchor_gap_to_target | required_co2_eur_t | required_gas_eur_mwh_th | required_co2_abs_eur_t | required_gas_abs_eur_mwh_th | delta_co2_vs_scenario | delta_gas_vs_scenario | tca_ccgt_eur_mwh | tca_coal_eur_mwh | tca_current_eur_mwh | pass_through_factor | base_scenario_id | base_year_reference | base_ref_source_year | base_ref_status | base_ref_reason | base_tca_ref_eur_mwh | base_ttl_model_ref_eur_mwh | base_gas_eur_per_mwh_th | base_co2_eur_per_t | ttl_proxy_method | status | reason | delta_tca_vs_base | delta_ttl_model_vs_base | delta_capture_ratio_vs_base | coherence_flag | required_co2_abs_raw_eur_t | required_gas_abs_raw_eur_mwh_th | co2_required_base | co2_required_gas_override | co2_required_base_non_negative | co2_required_gas_override_non_negative | warnings_quality | output_schema_version |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HIST | DE | 2018-2024 | year_specific | 2 024.00 | COAL | COAL | coal | 70.8300 | 46.9660 | 25.8313 | 0.3800 | 0.3410 | 4.0000 | 0.5500 | 148.7100 | 148.7100 | 148.7100 | 148.7100 | 131.5195 | 135.5377 | 148.7100 | 131.5195 | NaN | anchor_distributional | 131.5195 | 17.1905 | 17.1905 | 0.3076 | 0.8921 | 8.6325 | -0.0735 | 17.1915 | target_above_anchor | 0.8974 | 2.6316 | 1.4474 | 0.3800 | 0.8974 | 160.0000 | 24.4623 | 98.0900 | 63.8672 | 98.0900 | 63.8672 | 27.2600 | 16.9012 | 114.4067 | 135.5377 | 135.5377 | 1.0000 | BASE | 2 024.00 | 2 024.00 | ok | NaN | 135.5377 | 148.7100 | 46.9660 | 70.8300 | observed_from_prices | ok | NaN | 0.0000 | 0.0000 | 0.0000 | PASS | 98.0900 | 63.8672 | 98.0900 | NaN | 98.0900 | NaN | NaN | 2.0.0 |
| HIST | ES | 2018-2024 | year_specific | 2 024.00 | CCGT | CCGT | gas | 70.6800 | 47.0200 | NaN | 0.5500 | 0.2020 | 3.0000 | 1.0000 | 141.5000 | 141.5000 | 141.5000 | 141.5000 | 113.1496 | 114.4497 | 141.5000 | 113.1496 | NaN | anchor_distributional | 113.1496 | 28.3504 | 28.3504 | 0.6502 | 0.7033 | 23.7378 | 19.1251 | 28.3504 | target_above_anchor | 0.3673 | 1.8182 | 1.8182 | 0.5500 | 0.3673 | 160.0000 | 45.5503 | 194.7030 | 72.0726 | 194.7030 | 72.0726 | 124.0230 | 25.0526 | 114.4497 | 135.4813 | 114.4497 | 1.0000 | BASE | 2 024.00 | 2 024.00 | ok | NaN | 114.4497 | 141.5000 | 47.0200 | 70.6800 | observed_from_prices | ok | NaN | 0.0000 | 0.0000 | 0.0000 | PASS | 194.7030 | 72.0726 | 194.7030 | NaN | 194.7030 | NaN | NaN | 2.0.0 |

### Robustesse / fragilite
Statuts ledger: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Checks severes: 0 sur 30.
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
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | BASE | PASS | 2 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | 2 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | 2 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | 2 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | BASE | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. |
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
| Q1-H-01 | Q1 | SPEC2-Q1/Slides 2-4 | HIST | HIST_BASE | Score marche de bascule | La signature marche de phase 2 est calculee et exploitable. | stage2_market_score present et non vide | HIGH | nan | PASS | 2.0 | score present | Le score de bascule marche est exploitable. |
| Q1-H-02 | Q1 | SPEC2-Q1/Slides 3-4 | HIST | HIST_BASE | Stress physique SR/FAR/IR | La bascule physique est fondee sur SR/FAR/IR. | sr_energy/far_energy/ir_p10 presentes | CRITICAL | nan | PASS | far_energy,ir_p10,sr_energy | SR/FAR/IR presents | Le stress physique est calculable. |
| Q1-H-03 | Q1 | SPEC2-Q1 | HIST | HIST_BASE | Concordance marche vs physique | La relation entre bascule marche et bascule physique est mesurable. | bascule_year_market et bascule_year_physical comparables | MEDIUM | nan | WARN | strict=50.00%; concordant_ou_explique=50.00%; n=2; explained=1; reasons=strict_equal_year:1;year_gap_unexplained:1 | concordant_ou_explique >= 80% | Concordance partielle; divergences a expliquer pays par pays. |
| Q1-H-04 | Q1 | Slides 4-6 | HIST | HIST_BASE | Robustesse seuils | Le diagnostic reste stable sous variation raisonnable de seuils. | delta bascules sous choc de seuil <= 50% | MEDIUM | nan | PASS | 1.000 | confidence moyenne >=0.60 | Proxy de robustesse du diagnostic de bascule. |
| Q1-S-01 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Bascule projetee par scenario | Chaque scenario fournit un diagnostic de bascule projetee. | Q1_country_summary non vide en SCEN | HIGH | BASE | PASS | 2 | >0 lignes | La bascule projetee est produite. |
| Q1-S-01 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Bascule projetee par scenario | Chaque scenario fournit un diagnostic de bascule projetee. | Q1_country_summary non vide en SCEN | HIGH | DEMAND_UP | PASS | 2 | >0 lignes | La bascule projetee est produite. |
| Q1-S-01 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Bascule projetee par scenario | Chaque scenario fournit un diagnostic de bascule projetee. | Q1_country_summary non vide en SCEN | HIGH | LOW_RIGIDITY | PASS | 2 | >0 lignes | La bascule projetee est produite. |
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share) | MEDIUM | BASE | PASS | reference_scenario | scenario de reference | BASE est la reference explicite pour le calcul de sensibilite; pas de delta attendu. |
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share) | MEDIUM | DEMAND_UP | PASS | finite_share=0.00%; nonzero_share=0.00%; req_defined=100.00%; n_countries=2 | nonzero_share >= 20% (scenarios non-BASE) | Delta vs BASE nul/non defini, mais solveur required_lever disponible et interpretable. |
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share) | MEDIUM | LOW_RIGIDITY | PASS | finite_share=0.00%; nonzero_share=0.00%; req_defined=100.00%; n_countries=2 | nonzero_share >= 20% (scenarios non-BASE) | Delta vs BASE nul/non defini, mais solveur required_lever disponible et interpretable. |
| Q1-S-03 | Q1 | SPEC2-Q1 | SCEN | DEFAULT | Qualite de causalite | Le regime_coherence respecte le seuil d'interpretation. | part regime_coherence >= seuil min | MEDIUM | BASE | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
| Q1-S-03 | Q1 | SPEC2-Q1 | SCEN | DEFAULT | Qualite de causalite | Le regime_coherence respecte le seuil d'interpretation. | part regime_coherence >= seuil min | MEDIUM | DEMAND_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
| Q1-S-03 | Q1 | SPEC2-Q1 | SCEN | DEFAULT | Qualite de causalite | Le regime_coherence respecte le seuil d'interpretation. | part regime_coherence >= seuil min | MEDIUM | LOW_RIGIDITY | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |

#### Q2
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q2-H-01 | Q2 | SPEC2-Q2/Slides 10 | HIST | HIST_BASE | Pentes OLS post-bascule | Les pentes PV/Wind sont estimees en historique. | Q2_country_slopes non vide | HIGH | nan | PASS | 4 | >0 lignes | Les pentes historiques sont calculees. |
| Q2-H-02 | Q2 | SPEC2-Q2/Slides 10-12 | HIST | HIST_BASE | Robustesse statistique | R2/p-value/n sont disponibles pour qualifier la robustesse. | colonnes r2,p_value,n presentes | MEDIUM | nan | PASS | n,p_value,r2 | r2,p_value,n disponibles | La robustesse statistique est lisible. |
| Q2-H-03 | Q2 | Slides 10-13 | HIST | HIST_BASE | Drivers physiques | Les drivers SR/FAR/IR/corr VRE-load sont exploites. | driver correlations non vides | MEDIUM | nan | PASS | 4 | >0 lignes | Les drivers de pente sont disponibles. |
| Q2-S-01 | Q2 | SPEC2-Q2/Slides 11 | SCEN | DEFAULT | Pentes projetees | Les pentes sont reproduites en mode scenario. | Q2_country_slopes non vide en SCEN | HIGH | BASE | PASS | 4 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | Q2 | SPEC2-Q2/Slides 11 | SCEN | DEFAULT | Pentes projetees | Les pentes sont reproduites en mode scenario. | Q2_country_slopes non vide en SCEN | HIGH | HIGH_CO2 | PASS | 4 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | Q2 | SPEC2-Q2/Slides 11 | SCEN | DEFAULT | Pentes projetees | Les pentes sont reproduites en mode scenario. | Q2_country_slopes non vide en SCEN | HIGH | HIGH_GAS | PASS | 4 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-02 | Q2 | SPEC2-Q2 | SCEN | DEFAULT | Delta pente vs BASE | Les differences de pente vs BASE sont calculables. | delta slope par pays/tech vs BASE | MEDIUM | BASE | WARN | finite=0.00%; robust=0.00%; reason_known=100.00% | finite_share >= 20% | Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable. |
| Q2-S-02 | Q2 | SPEC2-Q2 | SCEN | DEFAULT | Delta pente vs BASE | Les differences de pente vs BASE sont calculables. | delta slope par pays/tech vs BASE | MEDIUM | HIGH_CO2 | WARN | finite=0.00%; robust=0.00%; reason_known=100.00% | finite_share >= 20% | Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable. |
| Q2-S-02 | Q2 | SPEC2-Q2 | SCEN | DEFAULT | Delta pente vs BASE | Les differences de pente vs BASE sont calculables. | delta slope par pays/tech vs BASE | MEDIUM | HIGH_GAS | WARN | finite=0.00%; robust=0.00%; reason_known=100.00% | finite_share >= 20% | Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable. |

#### Q3
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q3-H-01 | Q3 | SPEC2-Q3/Slides 16 | HIST | HIST_BASE | Tendances glissantes | Les tendances h_negative et capture_ratio sont estimees. | Q3_status non vide | HIGH | nan | PASS | 2 | >0 lignes | Les tendances historiques sont calculees. |
| Q3-H-02 | Q3 | SPEC2-Q3 | HIST | HIST_BASE | Statuts sortie phase 2 | Les statuts degradation/stabilisation/amelioration sont attribues. | status dans ensemble attendu | MEDIUM | nan | PASS | 1 | status valides | Les statuts business sont renseignes. |
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | BASE | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites. |
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | DEMAND_UP | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites. |
| Q3-S-01 | Q3 | SPEC2-Q3/Slides 17 | SCEN | DEFAULT | Conditions minimales d'inversion | Les besoins demande/must-run/flex sont quantifies en scenario. | inversion_k, inversion_r et additional_absorbed presentes | HIGH | LOW_RIGIDITY | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | BASE | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | DEMAND_UP | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | LOW_RIGIDITY | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise. |

#### Q4
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q4-H-01 | Q4 | SPEC2-Q4/Slides 22 | HIST | HIST_BASE | Simulation BESS 3 modes | SURPLUS_FIRST, PRICE_ARBITRAGE_SIMPLE et PV_COLOCATED sont executes. | 3 modes executes avec sorties non vides | CRITICAL | nan | PASS | HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED | 3 modes executes | Les trois modes Q4 sont disponibles. |
| Q4-H-02 | Q4 | SPEC2-Q4 | HIST | HIST_BASE | Invariants physiques BESS | Bornes SOC/puissance/energie respectees (mode physique de reference) avec garde-fous structurels sur modes alternatifs. | aucun FAIL physique/structurel pertinent | CRITICAL | nan | PASS | WARN | aucun FAIL physique | Les invariants physiques batterie sont respectes. Des avertissements non-physiques peuvent subsister (objectif/scenario). |
| Q4-S-01 | Q4 | SPEC2-Q4/Slides 23 | SCEN | DEFAULT | Comparaison effet batteries par scenario | Impact FAR/surplus/capture compare entre scenarios utiles. | Q4 summary non vide pour >=1 scenario | HIGH | BASE | PASS | 2 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | Q4 | SPEC2-Q4/Slides 23 | SCEN | DEFAULT | Comparaison effet batteries par scenario | Impact FAR/surplus/capture compare entre scenarios utiles. | Q4 summary non vide pour >=1 scenario | HIGH | HIGH_CO2 | PASS | 2 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | Q4 | SPEC2-Q4/Slides 23 | SCEN | DEFAULT | Comparaison effet batteries par scenario | Impact FAR/surplus/capture compare entre scenarios utiles. | Q4 summary non vide pour >=1 scenario | HIGH | HIGH_GAS | PASS | 2 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | BASE | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. |
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | HIGH_CO2 | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. |
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | HIGH_GAS | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. |

#### Q5
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q5-H-01 | Q5 | SPEC2-Q5/Slides 28 | HIST | HIST_BASE | Ancre thermique historique | TTL/TCA/alpha/corr sont estimes hors surplus. | Q5_summary non vide avec ttl_obs et tca_q95 | HIGH | nan | PASS | share_fini=100.00% | >=80% lignes ttl/tca finies | L'ancre thermique est quantifiable sur la majorite des pays. |
| Q5-H-02 | Q5 | SPEC2-Q5 | HIST | HIST_BASE | Sensibilites analytiques | dTCA/dCO2 et dTCA/dGas sont positives. | dTCA_dCO2 > 0 et dTCA_dGas > 0 | CRITICAL | nan | PASS | share_positive=100.00% | 100% lignes >0 | Sensibilites analytiques globalement coherentes. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | BASE | PASS | 2 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | HIGH_CO2 | PASS | 2 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | HIGH_GAS | PASS | 2 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | HIGH_BOTH | PASS | 2 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | BASE | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_CO2 | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_GAS | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_BOTH | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. |

### 4.2 Checks et warnings consolides
| run_id | question_id | status | code | message | scope | scenario_id | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260212_FIX10_DE_ES | Q1 | FAIL | TEST_Q1_001 | DE-2018: stage2 sans evidence low-price (h_negative=133.0, h_below_5=231.0). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2018: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2018: coverage price/load ok (100.00%/99.89%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2018: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2019: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2019: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2019: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2020: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2020: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2020: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2021: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2021: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2021: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2022: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2022: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2022: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2023: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2023: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2023: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2024: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2024: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2024: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2018: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2018: coverage price/load ok (99.99%/99.97%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2018: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2019: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2019: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2019: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2020: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2020: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2020: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2021: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2021: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2021: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2022: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2022: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2022: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2023: n_hours=8760 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2023: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2023: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2024: n_hours=8784 coherent. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2024: coverage price/load ok (99.99%/99.99%). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2024: prix dans plage large attendue. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | WARN | TEST_Q1_001 | Aucune ligne stage2 observee; test non applicable. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2025: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2025: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2025: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2026: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2026: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2026: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2027: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2027: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2027: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2028: n_hours=8784 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2028: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2028: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2029: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2029: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2029: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2030: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2030: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2030: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2031: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2031: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2031: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2032: n_hours=8784 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2032: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2032: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2033: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2033: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2033: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2034: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2034: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2034: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2035: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2035: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2035: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2025: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2025: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2025: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2026: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2026: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2026: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2027: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2027: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2027: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2028: n_hours=8784 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2028: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2028: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2029: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2029: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2029: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2030: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2030: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2030: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2031: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2031: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2031: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2032: n_hours=8784 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2032: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2032: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2033: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2033: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2033: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2034: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2034: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2034: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2035: n_hours=8760 coherent. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2035: coverage price/load ok (100.00%/100.00%). | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2035: prix dans plage large attendue. | SCEN | BASE | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | WARN | TEST_Q1_001 | Aucune ligne stage2 observee; test non applicable. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2025: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2025: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2025: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2026: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2026: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2026: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2027: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2027: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2027: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2028: n_hours=8784 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2028: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2028: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2029: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2029: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2029: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2030: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2030: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2030: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2031: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2031: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2031: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2032: n_hours=8784 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2032: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2032: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2033: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2033: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2033: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2034: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2034: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2034: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2035: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2035: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2035: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2025: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2025: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2025: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2026: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2026: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2026: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2027: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2027: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2027: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2028: n_hours=8784 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2028: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2028: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2029: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2029: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2029: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2030: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2030: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2030: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2031: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2031: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2031: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2032: n_hours=8784 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2032: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2032: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2033: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2033: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2033: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2034: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2034: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2034: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2035: n_hours=8760 coherent. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2035: coverage price/load ok (100.00%/100.00%). | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2035: prix dans plage large attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | WARN | TEST_Q1_001 | Aucune ligne stage2 observee; test non applicable. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2025: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2025: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2025: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2026: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2026: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2026: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2027: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2027: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2027: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2028: n_hours=8784 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2028: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2028: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2029: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2029: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2029: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2030: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2030: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2030: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2031: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2031: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2031: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2032: n_hours=8784 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2032: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2032: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2033: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2033: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2033: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2034: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2034: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2034: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | DE-2035: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | DE-2035: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | DE-2035: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2025: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2025: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2025: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2026: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2026: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2026: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2027: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2027: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2027: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2028: n_hours=8784 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2028: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2028: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2029: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2029: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2029: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2030: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2030: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2030: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2031: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2031: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2031: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2032: n_hours=8784 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2032: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2032: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2033: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2033: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2033: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2034: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2034: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2034: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_001 | ES-2035: n_hours=8760 coherent. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_002 | ES-2035: coverage price/load ok (100.00%/100.00%). | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | TEST_DATA_003 | ES-2035: prix dans plage large attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | WARN | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=1 | BUNDLE |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | WARN | BUNDLE_INFORMATIVENESS | share_tests_informatifs=100.00% ; share_compare_informatifs=0.00% | BUNDLE |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q1 | PASS | Q1_S02_NO_SENSITIVITY | Q1-S-02: au moins un scenario non-BASE montre une sensibilite observable. | BUNDLE |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\summary.json |
| FULL_20260212_FIX10_DE_ES | Q2 | PASS | TEST_Q2_2022_001 | exclude_year_2022=1 respecte: 2022 absent de tous les years_used. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\summary.json |
| FULL_20260212_FIX10_DE_ES | Q2 | PASS | TEST_Q2_001 | r2 present pour les OLS (n>=3) ou justification explicite quand OLS impossible. | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\summary.json |
| FULL_20260212_FIX10_DE_ES | Q2 | PASS | TEST_Q2_002 | Aucun cas physiquement suspect (slope>0 et corr_vre_load fortement negative). | HIST |  | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\summary.json |

### 4.3 Tracabilite tests -> sources
| run_id | question_id | test_id | source_ref | mode | scenario_id | status | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-H-03 | SPEC2-Q1 | HIST | nan | WARN | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-H-04 | Slides 4-6 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | BASE | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-H-03 | Slides 10-13 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | BASE | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | BASE | WARN | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-H-02 | SPEC2-Q3 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | BASE | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-S-02 | Slides 17-19 | SCEN | BASE | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-H-01 | SPEC2-Q4/Slides 22 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-H-02 | SPEC2-Q4 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | BASE | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-S-02 | Slides 23-25 | SCEN | BASE | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-H-02 | SPEC2-Q5 | HIST | nan | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | BASE | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | BASE | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv |

### 4.4 Couverture Slides/SPECS -> preuves
_Aucune ligne._

### 4.5 Catalogue de preuves
| run_id | question_id | test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | nan | PASS | 2.0 | score present | Le score de bascule marche est exploitable. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-H-01 |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | nan | PASS | far_energy,ir_p10,sr_energy | SR/FAR/IR presents | Le stress physique est calculable. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-H-02 |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-H-03 | SPEC2-Q1 | HIST | nan | WARN | strict=50.00%; concordant_ou_explique=50.00%; n=2; explained=1; reasons=strict_equal_year:1;year_gap_unexplained:1 | concordant_ou_explique >= 80% | Concordance partielle; divergences a expliquer pays par pays. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-H-03 |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-H-04 | Slides 4-6 | HIST | nan | PASS | 1.000 | confidence moyenne >=0.60 | Proxy de robustesse du diagnostic de bascule. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-H-04 |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | 2 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 2 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 2 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | reference_scenario | scenario de reference | BASE est la reference explicite pour le calcul de sensibilite; pas de delta attendu. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | finite_share=0.00%; nonzero_share=0.00%; req_defined=100.00%; n_countries=2 | nonzero_share >= 20% (scenarios non-BASE) | Delta vs BASE nul/non defini, mais solveur required_lever disponible et interpretable. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | finite_share=0.00%; nonzero_share=0.00%; req_defined=100.00%; n_countries=2 | nonzero_share >= 20% (scenarios non-BASE) | Delta vs BASE nul/non defini, mais solveur required_lever disponible et interpretable. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | BASE | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260212_FIX10_DE_ES | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | LOW_RIGIDITY | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | nan | PASS | 4 | >0 lignes | Les pentes historiques sont calculees. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv#test_id=Q2-H-01 |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | nan | PASS | n,p_value,r2 | r2,p_value,n disponibles | La robustesse statistique est lisible. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv#test_id=Q2-H-02 |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-H-03 | Slides 10-13 | HIST | nan | PASS | 4 | >0 lignes | Les drivers de pente sont disponibles. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv#test_id=Q2-H-03 |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | BASE | PASS | 4 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | 4 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | 4 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | BASE | WARN | finite=0.00%; robust=0.00%; reason_known=100.00% | finite_share >= 20% | Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | finite=0.00%; robust=0.00%; reason_known=100.00% | finite_share >= 20% | Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260212_FIX10_DE_ES | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | finite=0.00%; robust=0.00%; reason_known=100.00% | finite_share >= 20% | Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | nan | PASS | 2 | >0 lignes | Les tendances historiques sont calculees. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv#test_id=Q3-H-01 |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-H-02 | SPEC2-Q3 | HIST | nan | PASS | 1 | status valides | Les statuts business sont renseignes. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv#test_id=Q3-H-02 |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | BASE | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-S-02 | Slides 17-19 | SCEN | BASE | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260212_FIX10_DE_ES | Q3 | Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | PASS | hors_scope=100.00%; inversion=0 | hors_scope < 80% ou inversion deja atteinte | Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-H-01 | SPEC2-Q4/Slides 22 | HIST | nan | PASS | HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED | 3 modes executes | Les trois modes Q4 sont disponibles. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv#test_id=Q4-H-01 |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-H-02 | SPEC2-Q4 | HIST | nan | PASS | WARN | aucun FAIL physique | Les invariants physiques batterie sont respectes. Des avertissements non-physiques peuvent subsister (objectif/scenario). | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv#test_id=Q4-H-02 |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | BASE | PASS | 2 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | 2 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | 2 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-S-02 | Slides 23-25 | SCEN | BASE | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260212_FIX10_DE_ES | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | share_finite=100.00% | >=80% valeurs finies | Sensibilite valeur exploitable sur le panel. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | nan | PASS | share_fini=100.00% | >=80% lignes ttl/tca finies | L'ancre thermique est quantifiable sur la majorite des pays. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv#test_id=Q5-H-01 |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-H-02 | SPEC2-Q5 | HIST | nan | PASS | share_positive=100.00% | 100% lignes >0 | Sensibilites analytiques globalement coherentes. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv#test_id=Q5-H-02 |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | BASE | PASS | 2 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | 2 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | 2 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | 2 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | BASE | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260212_FIX10_DE_ES | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | share_finite=100.00% | >=80% valeurs finies | CO2 requis interpretable sur le panel. | outputs\combined\FULL_20260212_FIX10_DE_ES\Q5\test_ledger.csv#test_id=Q5-S-02 |

## 5. Ecarts restants (obligatoire)

- Logic issue: {'question_id': 'GLOBAL', 'issue': "aucun docx de slides fourni n'existe sur disque", 'slides_docx_provided_count': 2}
