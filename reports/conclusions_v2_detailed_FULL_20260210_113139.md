# Rapport Final V2.3 - Run `FULL_20260210_113139`

## 1. Page de garde
- Date de génération: `2026-02-10 12:43:35 UTC`
- Run combiné source: `outputs\combined\FULL_20260210_113139`
- Périmètre pays déclaré: `non renseigné`
- Fenêtre historique de référence: `2018-2024`
- Horizons prospectifs de référence: `2030/2040`
- Questions couvertes: `Q1, Q2, Q3, Q4, Q5`
- Avertissement méthodologique: ce rapport n'est pas un modèle d'équilibre complet, mais une analyse empirique et scénarisée bornée par les hypothèses explicites.

### Scénarios exécutés par question
- `Q1`: BASE, DEMAND_UP, FLEX_UP, LOW_RIGIDITY
- `Q2`: BASE, HIGH_CO2, HIGH_GAS
- `Q3`: BASE, DEMAND_UP, FLEX_UP, LOW_RIGIDITY
- `Q4`: BASE, FLEX_UP, HIGH_CO2, HIGH_GAS
- `Q5`: BASE, HIGH_BOTH, HIGH_CO2, HIGH_GAS

## 2. Méthode et gouvernance

### 2.1 Conventions et garde-fous (SPEC 0)
- Index interne horaire en UTC, conventions de signe et unités harmonisées.
- Classification physique des régimes sans utilisation du prix (anti-circularité).
- Distinction stricte entre observations historiques et simulations prospectives.

### 2.2 Observé vs simulé
- Historique: données ENTSO-E, métriques et tests empiriques sur années observées.
- Prospectif: mêmes métriques appliquées à des chroniques scénarisées, avec hypothèses explicites.

### 2.3 Qualité des données et limites structurantes
- Un résultat est robuste uniquement s'il ne contredit aucun FAIL et explicite tout WARN.
- Tout NON_TESTABLE est conservé comme zone d'incertitude, jamais masqué.
- Les conclusions sont formulées au niveau des preuves disponibles, sans extrapolation.

## 3. Analyses détaillées par question

## Q1 - Analyse détaillée

### Question business
Identifier de façon auditable la bascule de Phase 1 vers Phase 2, et distinguer explicitement ce qui relève d'un signal marché et ce qui relève d'un signal physique.

### Définitions opérationnelles
- SR (Surplus Ratio) mesure l'intensité du surplus en énergie sur l'année.
- FAR (Flex Absorption Ratio) mesure la part du surplus absorbée par la flexibilité.
- IR (Inflexibility Ratio) mesure la rigidité en creux de charge.
- La bascule marché est détectée via prix/capture ; la bascule physique via SR/FAR/IR.

### Périmètre des tests exécutés
Le périmètre analysé couvre `périmètre du run`. L'analyse s'appuie sur un run combiné unique pour éviter tout mélange inter-runs, et distingue systématiquement historique (observé) et prospectif (scénarisé).
Synthèse des tests exécutés: 16 tests au total, HIST=4, SCEN=12. Répartition statuts: PASS=15, WARN=1, FAIL=0, NON_TESTABLE=0.
Couverture prospective par scénario: BASE:3, DEMAND_UP:3, FLEX_UP:3, LOW_RIGIDITY:3.
Points d'attention prioritaires issus des tests non pleinement conformes: Q1-H-03 (HIST/nan) -> WARN, valeur=42.86%, règle=>=50%, lecture=Concordance mesuree entre bascules marche et physique..

### Résultats historiques et prospectifs (synthèse chiffrée)
Historique Q1 sur 7 pays: la bascule marché est observée entre 2 018.00 et 2 020.00, avec une confiance moyenne de 0.9143. La bascule physique est disponible pour 3 pays.
Le décalage moyen (physique - marché) vaut 1.6667 année(s). Un décalage positif signifie que le marché signale la tension avant la saturation physique mesurée.
Les notes de qualité signalent 2 cas de cohérence faible à traiter prudemment.
Prospectif Q1 par scénario (lecture moyenne):
| scenario_id | countries | mean_bascule_year_market | mean_bascule_confidence |
| --- | --- | --- | --- |
| BASE | 7.0000 | 2 030.00 | 1.0000 |
| DEMAND_UP | 7.0000 | 2 030.00 | 1.0000 |
| FLEX_UP | 7.0000 | 2 030.00 | 1.0000 |
| LOW_RIGIDITY | 7.0000 | 2 030.00 | 1.0000 |

### Comparaison historique vs prospectif
La comparaison historique vs prospectif contient 28 lignes sur 1 métriques et 4 scénarios.
Lecture synthétique des deltas moyens (prospectif - historique):
| metric | scenario_id | count | mean | median |
| --- | --- | --- | --- | --- |
| bascule_year_market | BASE | 7.0000 | 11.5714 | 12.0000 |
| bascule_year_market | DEMAND_UP | 7.0000 | 11.5714 | 12.0000 |
| bascule_year_market | FLEX_UP | 7.0000 | 11.5714 | 12.0000 |
| bascule_year_market | LOW_RIGIDITY | 7.0000 | 11.5714 | 12.0000 |

### Robustesse, fragilité et risques de mauvaise lecture
Checks consolidés: total=42, WARN/FAIL/ERROR=42, INFO=0.
Codes les plus fréquents à traiter: RC_CAPTURE_RANGE:26, RC_LOW_REGIME_COHERENCE:8, RC_IR_GT_1:7, BUNDLE_LEDGER_STATUS:1.
Risque 1: confondre corrélation et causalité. Risque 2: ignorer les WARN/NON_TESTABLE. Risque 3: extrapoler hors périmètre (pays, période, scénario) sans revalidation empirique.

### Réponse conclusive à la question
La conclusion est formulée au niveau des preuves effectivement observées. Une conclusion est considérée robuste uniquement si elle ne contredit aucun FAIL et si les WARN restants sont explicitement interprétés.
En cas de divergence historique/prospectif, la position recommandée n'est pas de choisir un camp, mais de qualifier précisément la cause de divergence: hypothèses scénario, qualité des données, ou limites structurelles du modèle.

### Actions et priorités de décision
1. Prioriser le traitement des incohérences critiques (FAIL ou contradiction forte avec reality checks).
2. Réviser les hypothèses prospectives qui réduisent artificiellement le stress système.
3. Consolider les périmètres avec faible robustesse statistique avant usage stratégique.

### Table de traçabilité test par test
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
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | 7 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 7 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | 7 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 7 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-03 | SPEC2-Q1 | SCEN | BASE | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
| Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
| Q1-S-03 | SPEC2-Q1 | SCEN | FLEX_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |
| Q1-S-03 | SPEC2-Q1 | SCEN | LOW_RIGIDITY | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. |

### Références de preuve obligatoires
[evidence:Q1-H-01] [evidence:Q1-H-02] [evidence:Q1-H-03] [evidence:Q1-H-04] [evidence:Q1-S-01] [evidence:Q1-S-02] [evidence:Q1-S-03]

Lecture complémentaire de preuve `Q1-H-01`: le test vérifie `La signature marche de phase 2 est calculee et exploitable.` selon la règle `stage2_market_score present et non vide`. La valeur observée (`4.1020`) est lue contre le seuil/règle (`score present`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Le score de bascule marche est exploitable. [evidence:Q1-H-01] [source:SPEC2-Q1/Slides 2-4]
Lecture complémentaire de preuve `Q1-H-02`: le test vérifie `La bascule physique est fondee sur SR/FAR/IR.` selon la règle `sr_energy/far_energy/ir_p10 presentes`. La valeur observée (`far_energy,ir_p10,sr_energy`) est lue contre le seuil/règle (`SR/FAR/IR presents`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Le stress physique est calculable. [evidence:Q1-H-02] [source:SPEC2-Q1/Slides 3-4]
Lecture complémentaire de preuve `Q1-H-03`: le test vérifie `La relation entre bascule marche et bascule physique est mesurable.` selon la règle `bascule_year_market et bascule_year_physical comparables`. La valeur observée (`42.86%`) est lue contre le seuil/règle (`>=50%`) avec statut `WARN` (interprétable mais fragile.). D'un point de vue décisionnel, cela signifie: Concordance mesuree entre bascules marche et physique. [evidence:Q1-H-03] [source:SPEC2-Q1]
Lecture complémentaire de preuve `Q1-H-04`: le test vérifie `Le diagnostic reste stable sous variation raisonnable de seuils.` selon la règle `delta bascules sous choc de seuil <= 50%`. La valeur observée (`0.9140`) est lue contre le seuil/règle (`confidence moyenne >=0.60`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Proxy de robustesse du diagnostic de bascule. [evidence:Q1-H-04] [source:Slides 4-6]

## Q2 - Analyse détaillée

### Question business
Mesurer la pente de cannibalisation de valeur, qualifier sa robustesse statistique, et relier cette pente aux drivers physiques et marché sans surinterpréter la causalité.

### Définitions opérationnelles
- La pente est une relation empirique entre pénétration et capture ratio, pas une loi structurelle.
- La robustesse statistique se lit avec n, p-value et R².
- Un driver corrélé n'est pas une preuve causale ; c'est un facteur explicatif plausible à challenger.

### Périmètre des tests exécutés
Le périmètre analysé couvre `périmètre du run`. L'analyse s'appuie sur un run combiné unique pour éviter tout mélange inter-runs, et distingue systématiquement historique (observé) et prospectif (scénarisé).
Synthèse des tests exécutés: 9 tests au total, HIST=3, SCEN=6. Répartition statuts: PASS=6, WARN=3, FAIL=0, NON_TESTABLE=0.
Couverture prospective par scénario: BASE:2, HIGH_CO2:2, HIGH_GAS:2.
Points d'attention prioritaires issus des tests non pleinement conformes: Q2-S-02 (SCEN/BASE) -> WARN, valeur=0.00%, règle=>=30% robustes, lecture=Delta de pente interpretable avec robustesse.; Q2-S-02 (SCEN/HIGH_CO2) -> WARN, valeur=0.00%, règle=>=30% robustes, lecture=Delta de pente interpretable avec robustesse.; Q2-S-02 (SCEN/HIGH_GAS) -> WARN, valeur=0.00%, règle=>=30% robustes, lecture=Delta de pente interpretable avec robustesse..

### Résultats historiques et prospectifs (synthèse chiffrée)
Historique Q2 (pentes observées) par technologie:
| tech | n | mean_slope | median_slope | robust_share | sig_share |
| --- | --- | --- | --- | --- | --- |
| PV | 7.0000 | -9.6775 | -3.0701 | 1.0000 | 0.0000 |
| WIND | 7.0000 | 3.1074 | -0.7863 | 1.0000 | 0.0000 |
Drivers historiques de pente (corrélations):
| driver_name | corr_with_slope_pv | corr_with_slope_wind | n_countries |
| --- | --- | --- | --- |
| mean_sr_energy_phase2 | 0.2731 | -0.0089 | 7.0000 |
| mean_far_energy_phase2 | 0.8728 | -0.2752 | 7.0000 |
| mean_ir_p10_phase2 | 0.4182 | 0.0440 | 7.0000 |
| mean_ttl_phase2 | -0.0632 | 0.5287 | 7.0000 |
| vre_load_corr_phase2 | -0.1086 | 0.5786 | 7.0000 |
| surplus_load_trough_share_phase2 | 0.7605 | 0.6674 | 7.0000 |
Prospectif Q2 (qualité statistique des pentes):
| scenario_id | rows | finite_slope_share | mean_r2 | fragile_share |
| --- | --- | --- | --- | --- |
| BASE | 14.0000 | 0.2857 | 1.0000 | 1.0000 |
| HIGH_CO2 | 14.0000 | 0.2857 | 1.0000 | 1.0000 |
| HIGH_GAS | 14.0000 | 0.2857 | 1.0000 | 1.0000 |

### Comparaison historique vs prospectif
La comparaison historique vs prospectif contient 42 lignes sur 1 métriques et 3 scénarios.
Lecture synthétique des deltas moyens (prospectif - historique):
| metric | scenario_id | count | mean | median |
| --- | --- | --- | --- | --- |
| slope | BASE | 4.0000 | -310.9575 | -14.0478 |
| slope | HIGH_CO2 | 4.0000 | 157.2880 | -13.4458 |
| slope | HIGH_GAS | 4.0000 | 3 257.09 | 2 750.60 |

### Robustesse, fragilité et risques de mauvaise lecture
Checks consolidés: total=86, WARN/FAIL/ERROR=81, INFO=5.
Codes les plus fréquents à traiter: Q2_FRAGILE:42, RC_CAPTURE_RANGE:20, RC_LOW_REGIME_COHERENCE:8, RC_IR_GT_1:7, Q2_POSITIVE_PV_SLOPE:3, BUNDLE_LEDGER_STATUS:1.
Risque 1: confondre corrélation et causalité. Risque 2: ignorer les WARN/NON_TESTABLE. Risque 3: extrapoler hors périmètre (pays, période, scénario) sans revalidation empirique.

### Réponse conclusive à la question
La conclusion est formulée au niveau des preuves effectivement observées. Une conclusion est considérée robuste uniquement si elle ne contredit aucun FAIL et si les WARN restants sont explicitement interprétés.
En cas de divergence historique/prospectif, la position recommandée n'est pas de choisir un camp, mais de qualifier précisément la cause de divergence: hypothèses scénario, qualité des données, ou limites structurelles du modèle.

### Actions et priorités de décision
1. Prioriser le traitement des incohérences critiques (FAIL ou contradiction forte avec reality checks).
2. Réviser les hypothèses prospectives qui réduisent artificiellement le stress système.
3. Consolider les périmètres avec faible robustesse statistique avant usage stratégique.

### Table de traçabilité test par test
| test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | NaN | PASS | 14 | >0 lignes | Les pentes historiques sont calculees. |
| Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | NaN | PASS | n,p_value,r2 | r2,p_value,n disponibles | La robustesse statistique est lisible. |
| Q2-H-03 | Slides 10-13 | HIST | NaN | PASS | 6 | >0 lignes | Les drivers de pente sont disponibles. |
| Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | BASE | PASS | 14 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | 14 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | 14 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-02 | SPEC2-Q2 | SCEN | BASE | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. |
| Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. |
| Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. |

### Références de preuve obligatoires
[evidence:Q2-H-01] [evidence:Q2-H-02] [evidence:Q2-H-03] [evidence:Q2-S-01] [evidence:Q2-S-02]

Lecture complémentaire de preuve `Q2-H-01`: le test vérifie `Les pentes PV/Wind sont estimees en historique.` selon la règle `Q2_country_slopes non vide`. La valeur observée (`14.0000`) est lue contre le seuil/règle (`>0 lignes`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Les pentes historiques sont calculees. [evidence:Q2-H-01] [source:SPEC2-Q2/Slides 10]
Lecture complémentaire de preuve `Q2-H-02`: le test vérifie `R2/p-value/n sont disponibles pour qualifier la robustesse.` selon la règle `colonnes r2,p_value,n presentes`. La valeur observée (`n,p_value,r2`) est lue contre le seuil/règle (`r2,p_value,n disponibles`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: La robustesse statistique est lisible. [evidence:Q2-H-02] [source:SPEC2-Q2/Slides 10-12]
Lecture complémentaire de preuve `Q2-H-03`: le test vérifie `Les drivers SR/FAR/IR/corr VRE-load sont exploites.` selon la règle `driver correlations non vides`. La valeur observée (`6.0000`) est lue contre le seuil/règle (`>0 lignes`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Les drivers de pente sont disponibles. [evidence:Q2-H-03] [source:Slides 10-13]

## Q3 - Analyse détaillée

### Question business
Qualifier la dynamique de sortie de Phase 2 (dégradation, stabilisation, amélioration) et chiffrer les ordres de grandeur des leviers d'inversion (demande, must-run, flex).

### Définitions opérationnelles
- Le statut (dégradation, stabilisation, amélioration) est multi-indicateurs et non monocritère.
- Les contre-factuels demande/must-run/flex sont des ordres de grandeur statiques.
- L'entrée en Phase 3 exige une convergence de signaux physiques et marché.

### Périmètre des tests exécutés
Le périmètre analysé couvre `périmètre du run`. L'analyse s'appuie sur un run combiné unique pour éviter tout mélange inter-runs, et distingue systématiquement historique (observé) et prospectif (scénarisé).
Synthèse des tests exécutés: 10 tests au total, HIST=2, SCEN=8. Répartition statuts: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0.
Couverture prospective par scénario: BASE:2, DEMAND_UP:2, FLEX_UP:2, LOW_RIGIDITY:2.
Aucun test WARN/FAIL/NON_TESTABLE n'est remonté; le diagnostic technique est globalement stable.

### Résultats historiques et prospectifs (synthèse chiffrée)
Historique Q3 - distribution des statuts: degradation:6, hors_scope_stage2:1.
Ordres de grandeur historiques des leviers d'inversion:
| metric | mean | median | max |
| --- | --- | --- | --- |
| inversion_k_demand | 0.0942 | 0.0583 | 0.2786 |
| inversion_r_mustrun | 0.1703 | 0.1264 | 0.5332 |
| additional_absorbed_needed_TWh_year | 1.3860 | 0.0000 | 9.6888 |
Prospectif Q3 - synthèse par scénario:
| scenario_id | rows | status_main | mean_inversion_k | mean_inversion_r |
| --- | --- | --- | --- | --- |
| BASE | 7.0000 | hors_scope_stage2 | 0.0000 | 0.0000 |
| DEMAND_UP | 7.0000 | hors_scope_stage2 | 0.0000 | 0.0000 |
| FLEX_UP | 7.0000 | hors_scope_stage2 | 0.0000 | 0.0000 |
| LOW_RIGIDITY | 7.0000 | hors_scope_stage2 | 0.0000 | 0.0000 |

### Comparaison historique vs prospectif
La comparaison historique vs prospectif contient 56 lignes sur 2 métriques et 4 scénarios.
Lecture synthétique des deltas moyens (prospectif - historique):
| metric | scenario_id | count | mean | median |
| --- | --- | --- | --- | --- |
| inversion_k_demand | BASE | 7.0000 | -0.0942 | -0.0583 |
| inversion_k_demand | DEMAND_UP | 7.0000 | -0.0942 | -0.0583 |
| inversion_k_demand | FLEX_UP | 7.0000 | -0.0942 | -0.0583 |
| inversion_k_demand | LOW_RIGIDITY | 7.0000 | -0.0942 | -0.0583 |
| inversion_r_mustrun | BASE | 7.0000 | -0.1703 | -0.1264 |
| inversion_r_mustrun | DEMAND_UP | 7.0000 | -0.1703 | -0.1264 |
| inversion_r_mustrun | FLEX_UP | 7.0000 | -0.1703 | -0.1264 |
| inversion_r_mustrun | LOW_RIGIDITY | 7.0000 | -0.1703 | -0.1264 |

### Robustesse, fragilité et risques de mauvaise lecture
Checks consolidés: total=51, WARN/FAIL/ERROR=18, INFO=32.
Codes les plus fréquents à traiter: RC_CAPTURE_RANGE:14, Q3_DEMAND_HIGH:1, Q3_MUSTRUN_HIGH:1, RC_IR_GT_1:1, RC_LOW_REGIME_COHERENCE:1.
Risque 1: confondre corrélation et causalité. Risque 2: ignorer les WARN/NON_TESTABLE. Risque 3: extrapoler hors périmètre (pays, période, scénario) sans revalidation empirique.

### Réponse conclusive à la question
La conclusion est formulée au niveau des preuves effectivement observées. Une conclusion est considérée robuste uniquement si elle ne contredit aucun FAIL et si les WARN restants sont explicitement interprétés.
En cas de divergence historique/prospectif, la position recommandée n'est pas de choisir un camp, mais de qualifier précisément la cause de divergence: hypothèses scénario, qualité des données, ou limites structurelles du modèle.

### Actions et priorités de décision
1. Prioriser le traitement des incohérences critiques (FAIL ou contradiction forte avec reality checks).
2. Réviser les hypothèses prospectives qui réduisent artificiellement le stress système.
3. Consolider les périmètres avec faible robustesse statistique avant usage stratégique.

### Table de traçabilité test par test
| test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | NaN | PASS | 7.0000 | >0 lignes | Les tendances historiques sont calculees. |
| Q3-H-02 | SPEC2-Q3 | HIST | NaN | PASS | 2.0000 | status valides | Les statuts business sont renseignes. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | BASE | PASS | 7.0000 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | PASS | 7.0000 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | FLEX_UP | PASS | 7.0000 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | PASS | 7.0000 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. |
| Q3-S-02 | Slides 17-19 | SCEN | BASE | PASS | 1.0000 | status renseignes | La lecture de transition phase 3 est possible. |
| Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | PASS | 1.0000 | status renseignes | La lecture de transition phase 3 est possible. |
| Q3-S-02 | Slides 17-19 | SCEN | FLEX_UP | PASS | 1.0000 | status renseignes | La lecture de transition phase 3 est possible. |
| Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | PASS | 1.0000 | status renseignes | La lecture de transition phase 3 est possible. |

### Références de preuve obligatoires
[evidence:Q3-H-01] [evidence:Q3-H-02] [evidence:Q3-S-01] [evidence:Q3-S-02]

Lecture complémentaire de preuve `Q3-H-01`: le test vérifie `Les tendances h_negative et capture_ratio sont estimees.` selon la règle `Q3_status non vide`. La valeur observée (`7.0000`) est lue contre le seuil/règle (`>0 lignes`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Les tendances historiques sont calculees. [evidence:Q3-H-01] [source:SPEC2-Q3/Slides 16]
Lecture complémentaire de preuve `Q3-H-02`: le test vérifie `Les statuts degradation/stabilisation/amelioration sont attribues.` selon la règle `status dans ensemble attendu`. La valeur observée (`2.0000`) est lue contre le seuil/règle (`status valides`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Les statuts business sont renseignes. [evidence:Q3-H-02] [source:SPEC2-Q3]
Lecture complémentaire de preuve `Q3-S-01`: le test vérifie `Les besoins demande/must-run/flex sont quantifies en scenario.` selon la règle `inversion_k, inversion_r et additional_absorbed presentes`. La valeur observée (`7.0000`) est lue contre le seuil/règle (`colonnes inversion presentes`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Les ordres de grandeur d'inversion sont quantifies. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
Lecture complémentaire de preuve `Q3-S-01`: le test vérifie `Les besoins demande/must-run/flex sont quantifies en scenario.` selon la règle `inversion_k, inversion_r et additional_absorbed presentes`. La valeur observée (`7.0000`) est lue contre le seuil/règle (`colonnes inversion presentes`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Les ordres de grandeur d'inversion sont quantifies. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
Lecture complémentaire de preuve `Q3-S-01`: le test vérifie `Les besoins demande/must-run/flex sont quantifies en scenario.` selon la règle `inversion_k, inversion_r et additional_absorbed presentes`. La valeur observée (`7.0000`) est lue contre le seuil/règle (`colonnes inversion presentes`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Les ordres de grandeur d'inversion sont quantifies. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]
Lecture complémentaire de preuve `Q3-S-01`: le test vérifie `Les besoins demande/must-run/flex sont quantifies en scenario.` selon la règle `inversion_k, inversion_r et additional_absorbed presentes`. La valeur observée (`7.0000`) est lue contre le seuil/règle (`colonnes inversion presentes`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Les ordres de grandeur d'inversion sont quantifies. [evidence:Q3-S-01] [source:SPEC2-Q3/Slides 17]

## Q4 - Analyse détaillée

### Question business
Quantifier l'effet des batteries sous une lecture système et une lecture actif, avec tests d'invariants physiques et comparaison des scénarios de contexte.

### Définitions opérationnelles
- SURPLUS_FIRST porte une lecture système (absorption du surplus).
- PRICE_ARBITRAGE_SIMPLE porte une lecture économique batterie simplifiée.
- PV_COLOCATED porte une lecture valeur actif PV + batterie.

### Périmètre des tests exécutés
Le périmètre analysé couvre `périmètre du run`. L'analyse s'appuie sur un run combiné unique pour éviter tout mélange inter-runs, et distingue systématiquement historique (observé) et prospectif (scénarisé).
Synthèse des tests exécutés: 10 tests au total, HIST=2, SCEN=8. Répartition statuts: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0.
Couverture prospective par scénario: BASE:2, FLEX_UP:2, HIGH_CO2:2, HIGH_GAS:2.
Aucun test WARN/FAIL/NON_TESTABLE n'est remonté; le diagnostic technique est globalement stable.

### Résultats historiques et prospectifs (synthèse chiffrée)
Frontière historique Q4:
| dispatch_mode | objective | required_bess_power_mw | required_bess_energy_mwh | required_bess_duration_h | far_before | far_after | surplus_unabs_energy_before | surplus_unabs_energy_after | pv_capture_price_before | pv_capture_price_after | revenue_bess_price_taker | soc_min | soc_max | charge_max | discharge_max | charge_sum_mwh | discharge_sum_mwh | initial_deliverable_mwh | engine_version | compute_time_sec | cache_hit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SURPLUS_FIRST | FAR_TARGET | 0.0000 | 0.0000 | 1.0000 | 0.7911 | 0.7911 | 12.7375 | 12.7375 | 39.2480 | 39.2480 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 0.0000 | 0.0000 | 2.0000 | 0.7911 | 0.7911 | 12.7375 | 12.7375 | 39.2480 | 39.2480 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 0.0000 | 0.0000 | 4.0000 | 0.7911 | 0.7911 | 12.7375 | 12.7375 | 39.2480 | 39.2480 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 0.0000 | 0.0000 | 6.0000 | 0.7911 | 0.7911 | 12.7375 | 12.7375 | 39.2480 | 39.2480 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 0.0000 | 0.0000 | 8.0000 | 0.7911 | 0.7911 | 12.7375 | 12.7375 | 39.2480 | 39.2480 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 0.0000 | 0.0000 | 10.0000 | 0.7911 | 0.7911 | 12.7375 | 12.7375 | 39.2480 | 39.2480 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 200.0000 | 200.0000 | 1.0000 | 0.7911 | 0.7922 | 12.7375 | 12.6718 | 39.2480 | 39.2480 | 2 653 039.2 | 0.0000 | 200.0000 | 200.0000 | 187.6166 | 65 761.53 | 57 787.95 | 93.8083 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 200.0000 | 400.0000 | 2.0000 | 0.7911 | 0.7932 | 12.7375 | 12.6068 | 39.2480 | 39.2480 | 5 245 639.2 | 0.0000 | 400.0000 | 200.0000 | 200.0000 | 130 773.60 | 115 092.38 | 187.6166 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 200.0000 | 800.0000 | 4.0000 | 0.7911 | 0.7953 | 12.7375 | 12.4801 | 39.2480 | 39.2480 | 9 831 831.2 | 0.0000 | 800.0000 | 200.0000 | 200.0000 | 257 461.60 | 226 765.44 | 375.2333 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 200.0000 | 1 200.00 | 6.0000 | 0.7911 | 0.7973 | 12.7375 | 12.3613 | 39.2480 | 39.2480 | 12 288 985.3 | 0.0000 | 1 200.00 | 200.0000 | 200.0000 | 376 276.65 | 331 510.31 | 562.8499 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 200.0000 | 1 600.00 | 8.0000 | 0.7911 | 0.7991 | 12.7375 | 12.2510 | 39.2480 | 39.2480 | 14 026 056.7 | 0.0000 | 1 600.00 | 200.0000 | 200.0000 | 486 504.35 | 428 698.30 | 750.4665 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 200.0000 | 2 000.00 | 10.0000 | 0.7911 | 0.8007 | 12.7375 | 12.1508 | 39.2480 | 39.2480 | 15 337 124.4 | 0.0000 | 2 000.00 | 200.0000 | 200.0000 | 586 724.43 | 517 079.58 | 938.0832 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 500.0000 | 500.0000 | 1.0000 | 0.7911 | 0.7938 | 12.7375 | 12.5742 | 39.2480 | 39.2480 | 6 655 521.5 | 0.0000 | 500.0000 | 500.0000 | 469.0416 | 163 343.57 | 143 536.86 | 234.5208 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 500.0000 | 1 000.00 | 2.0000 | 0.7911 | 0.7964 | 12.7375 | 12.4122 | 39.2480 | 39.2480 | 13 144 189.9 | 0.0000 | 1 000.00 | 500.0000 | 500.0000 | 325 300.86 | 286 293.80 | 469.0416 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 500.0000 | 2 000.00 | 4.0000 | 0.7911 | 0.8016 | 12.7375 | 12.0966 | 39.2480 | 39.2480 | 24 616 879.4 | 0.0000 | 2 000.00 | 500.0000 | 500.0000 | 640 944.73 | 564 529.45 | 938.0832 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 500.0000 | 3 000.00 | 6.0000 | 0.7911 | 0.8064 | 12.7375 | 11.8042 | 39.2480 | 39.2480 | 30 744 074.2 | 0.0000 | 3 000.00 | 500.0000 | 500.0000 | 933 364.40 | 822 327.80 | 1 407.12 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 500.0000 | 4 000.00 | 8.0000 | 0.7911 | 0.8109 | 12.7375 | 11.5325 | 39.2480 | 39.2480 | 35 044 855.1 | 0.0000 | 4 000.00 | 500.0000 | 500.0000 | 1 204 987.6 | 1 061 825.3 | 1 876.17 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 500.0000 | 5 000.00 | 10.0000 | 0.7911 | 0.8149 | 12.7375 | 11.2879 | 39.2480 | 39.2480 | 38 346 349.8 | 0.0000 | 5 000.00 | 500.0000 | 500.0000 | 1 449 624.6 | 1 277 574.9 | 2 345.21 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 1 000.00 | 1 000.00 | 1.0000 | 0.7911 | 0.7964 | 12.7375 | 12.4136 | 39.2480 | 39.2480 | 13 349 020.3 | 0.0000 | 1 000.00 | 1 000.00 | 938.0832 | 323 930.21 | 284 848.42 | 469.0416 | v2.1.0 | 1.5958 | 1.0000 |
| SURPLUS_FIRST | FAR_TARGET | 1 000.00 | 2 000.00 | 2.0000 | 0.7911 | 0.8017 | 12.7375 | 12.0914 | 39.2480 | 39.2480 | 26 352 082.7 | 0.0000 | 2 000.00 | 1 000.00 | 1 000.00 | 646 113.04 | 568 838.35 | 938.0832 | v2.1.0 | 1.5958 | 1.0000 |
Synthèse historique Q4:
| country | year | dispatch_mode | objective | required_bess_power_mw | required_bess_energy_mwh | required_bess_duration_h | far_before | far_after | surplus_unabs_energy_before | surplus_unabs_energy_after | pv_capture_price_before | pv_capture_price_after | revenue_bess_price_taker | soc_min | soc_max | charge_max | discharge_max | charge_sum_mwh | discharge_sum_mwh | initial_deliverable_mwh | engine_version | compute_time_sec | cache_hit | notes_quality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR | 2 024.00 | SURPLUS_FIRST | FAR_TARGET | 6 000.00 | 48 000.00 | 8.0000 | 0.7911 | 0.9656 | 12.7375 | 2.1003 | 39.2480 | 39.2480 | 355 296 205.8 | 0.0000 | 48 000.00 | 6 000.00 | 6 000.00 | 10 637 245.9 | 9 382 611.2 | 22 514.00 | v2.1.0 | 1.5958 | 1.0000 | ok |
Prospectif Q4 - synthèse:
| scenario_id | rows | far_after_mean | surplus_unabs_after_mean | pv_capture_after_mean |
| --- | --- | --- | --- | --- |
| BASE | 1.0000 | NaN | 0.0000 | 1 318.76 |
| FLEX_UP | 1.0000 | NaN | 0.0000 | 1 317.04 |
| HIGH_CO2 | 1.0000 | NaN | 0.0000 | 1 336.28 |
| HIGH_GAS | 1.0000 | NaN | 0.0000 | 1 356.60 |

### Comparaison historique vs prospectif
La comparaison historique vs prospectif contient 14 lignes sur 3 métriques et 6 scénarios.
Lecture synthétique des deltas moyens (prospectif - historique):
| metric | scenario_id | count | mean | median |
| --- | --- | --- | --- | --- |
| far_after | BASE | 0.0000 | NaN | NaN |
| far_after | FLEX_UP | 0.0000 | NaN | NaN |
| far_after | HIGH_CO2 | 0.0000 | NaN | NaN |
| far_after | HIGH_GAS | 0.0000 | NaN | NaN |
| far_after | HIST_PRICE_ARBITRAGE_SIMPLE | 1.0000 | -0.0349 | -0.0349 |
| far_after | HIST_PV_COLOCATED | 1.0000 | -0.0600 | -0.0600 |
| pv_capture_price_after | BASE | 1.0000 | 1 279.51 | 1 279.51 |
| pv_capture_price_after | FLEX_UP | 1.0000 | 1 277.79 | 1 277.79 |
| pv_capture_price_after | HIGH_CO2 | 1.0000 | 1 297.03 | 1 297.03 |
| pv_capture_price_after | HIGH_GAS | 1.0000 | 1 317.36 | 1 317.36 |
| surplus_unabs_energy_after | BASE | 1.0000 | -2.1003 | -2.1003 |
| surplus_unabs_energy_after | FLEX_UP | 1.0000 | -2.1003 | -2.1003 |
| surplus_unabs_energy_after | HIGH_CO2 | 1.0000 | -2.1003 | -2.1003 |
| surplus_unabs_energy_after | HIGH_GAS | 1.0000 | -2.1003 | -2.1003 |

### Robustesse, fragilité et risques de mauvaise lecture
Checks consolidés: total=6, WARN/FAIL/ERROR=0, INFO=2.
Risque 1: confondre corrélation et causalité. Risque 2: ignorer les WARN/NON_TESTABLE. Risque 3: extrapoler hors périmètre (pays, période, scénario) sans revalidation empirique.

### Réponse conclusive à la question
La conclusion est formulée au niveau des preuves effectivement observées. Une conclusion est considérée robuste uniquement si elle ne contredit aucun FAIL et si les WARN restants sont explicitement interprétés.
En cas de divergence historique/prospectif, la position recommandée n'est pas de choisir un camp, mais de qualifier précisément la cause de divergence: hypothèses scénario, qualité des données, ou limites structurelles du modèle.

### Actions et priorités de décision
1. Prioriser le traitement des incohérences critiques (FAIL ou contradiction forte avec reality checks).
2. Réviser les hypothèses prospectives qui réduisent artificiellement le stress système.
3. Consolider les périmètres avec faible robustesse statistique avant usage stratégique.

### Table de traçabilité test par test
| test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q4-H-01 | SPEC2-Q4/Slides 22 | HIST | NaN | PASS | HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED | 3 modes executes | Les trois modes Q4 sont disponibles. |
| Q4-H-02 | SPEC2-Q4 | HIST | NaN | PASS | PASS | pas de FAIL | Les invariants physiques batterie sont respectes. |
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | BASE | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | FLEX_UP | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. |
| Q4-S-02 | Slides 23-25 | SCEN | BASE | PASS | 1318.7589939342624 | capture apres finite | Sensibilite valeur exploitable. |
| Q4-S-02 | Slides 23-25 | SCEN | FLEX_UP | PASS | 1317.042435494933 | capture apres finite | Sensibilite valeur exploitable. |
| Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | 1336.2811724552707 | capture apres finite | Sensibilite valeur exploitable. |
| Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | 1356.6039238995759 | capture apres finite | Sensibilite valeur exploitable. |

### Références de preuve obligatoires
[evidence:Q4-H-01] [evidence:Q4-H-02] [evidence:Q4-S-01] [evidence:Q4-S-02]

## Q5 - Analyse détaillée

### Question business
Mesurer l'impact du gaz et du CO2 sur l'ancre thermique, puis traduire cet impact en sensibilités opérationnelles et en niveau de CO2 requis sous hypothèses explicites.

### Définitions opérationnelles
- TTL est une statistique de prix hors surplus ; TCA est une ancre coût explicative.
- dTCA/dCO2 et dTCA/dGas mesurent des sensibilités incrémentales.
- Le CO2 requis est un ordre de grandeur conditionnel aux hypothèses de techno marginale et de pass-through.

### Périmètre des tests exécutés
Le périmètre analysé couvre `périmètre du run`. L'analyse s'appuie sur un run combiné unique pour éviter tout mélange inter-runs, et distingue systématiquement historique (observé) et prospectif (scénarisé).
Synthèse des tests exécutés: 10 tests au total, HIST=2, SCEN=8. Répartition statuts: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0.
Couverture prospective par scénario: BASE:2, HIGH_CO2:2, HIGH_GAS:2, HIGH_BOTH:2.
Aucun test WARN/FAIL/NON_TESTABLE n'est remonté; le diagnostic technique est globalement stable.

### Résultats historiques et prospectifs (synthèse chiffrée)
Synthèse historique Q5 (TTL/TCA/sensibilités):
| country | year_range_used | marginal_tech | ttl_obs | tca_q95 | alpha | corr_cd | dTCA_dCO2 | dTCA_dGas | ttl_target | co2_required_base | co2_required_gas_override | warnings_quality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR | 2018-2024 | CCGT | 419.9500 | 370.8396 | 49.1104 | 0.9082 | 0.3673 | 1.8182 | 120.0000 | -749.8055 | NaN | NaN |
Prospectif Q5 - synthèse:
| scenario_id | rows | ttl_obs_mean | tca_q95_mean | co2_required_base_mean |
| --- | --- | --- | --- | --- |
| BASE | 1.0000 | 3 895.15 | 130.6727 | -10 168.86 |
| HIGH_BOTH | 1.0000 | 3 895.15 | 194.5091 | -10 113.86 |
| HIGH_CO2 | 1.0000 | 3 918.36 | 150.8727 | -10 177.06 |
| HIGH_GAS | 1.0000 | 3 946.48 | 174.3091 | -10 308.64 |

### Comparaison historique vs prospectif
La comparaison historique vs prospectif contient 12 lignes sur 3 métriques et 4 scénarios.
Lecture synthétique des deltas moyens (prospectif - historique):
| metric | scenario_id | count | mean | median |
| --- | --- | --- | --- | --- |
| co2_required_base | BASE | 1.0000 | -9 419.06 | -9 419.06 |
| co2_required_base | HIGH_BOTH | 1.0000 | -9 364.06 | -9 364.06 |
| co2_required_base | HIGH_CO2 | 1.0000 | -9 427.26 | -9 427.26 |
| co2_required_base | HIGH_GAS | 1.0000 | -9 558.83 | -9 558.83 |
| tca_q95 | BASE | 1.0000 | -240.1669 | -240.1669 |
| tca_q95 | HIGH_BOTH | 1.0000 | -176.3305 | -176.3305 |
| tca_q95 | HIGH_CO2 | 1.0000 | -219.9669 | -219.9669 |
| tca_q95 | HIGH_GAS | 1.0000 | -196.5305 | -196.5305 |
| ttl_obs | BASE | 1.0000 | 3 475.20 | 3 475.20 |
| ttl_obs | HIGH_BOTH | 1.0000 | 3 475.20 | 3 475.20 |
| ttl_obs | HIGH_CO2 | 1.0000 | 3 498.41 | 3 498.41 |
| ttl_obs | HIGH_GAS | 1.0000 | 3 526.53 | 3 526.53 |

### Robustesse, fragilité et risques de mauvaise lecture
Checks consolidés: total=6, WARN/FAIL/ERROR=4, INFO=0.
Codes les plus fréquents à traiter: Q5_LOW_CORR_CD:4.
Risque 1: confondre corrélation et causalité. Risque 2: ignorer les WARN/NON_TESTABLE. Risque 3: extrapoler hors périmètre (pays, période, scénario) sans revalidation empirique.

### Réponse conclusive à la question
La conclusion est formulée au niveau des preuves effectivement observées. Une conclusion est considérée robuste uniquement si elle ne contredit aucun FAIL et si les WARN restants sont explicitement interprétés.
En cas de divergence historique/prospectif, la position recommandée n'est pas de choisir un camp, mais de qualifier précisément la cause de divergence: hypothèses scénario, qualité des données, ou limites structurelles du modèle.

### Actions et priorités de décision
1. Prioriser le traitement des incohérences critiques (FAIL ou contradiction forte avec reality checks).
2. Réviser les hypothèses prospectives qui réduisent artificiellement le stress système.
3. Consolider les périmètres avec faible robustesse statistique avant usage stratégique.

### Table de traçabilité test par test
| test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | NaN | PASS | ttl=419.95, tca=370.83959999999996 | ttl/tca finis | L'ancre thermique est quantifiable. |
| Q5-H-02 | SPEC2-Q5 | HIST | NaN | PASS | dCO2=0.36727272727272725, dGas=1.8181818181818181 | >0 | Sensibilites analytiques coherentes. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | BASE | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | BASE | PASS | -10168.862806747053 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | -10177.062869892936 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | -10308.637127318678 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | -10113.862806747053 | valeur finie | CO2 requis interpretable. |

### Références de preuve obligatoires
[evidence:Q5-H-01] [evidence:Q5-H-02] [evidence:Q5-S-01] [evidence:Q5-S-02]

Lecture complémentaire de preuve `Q5-H-01`: le test vérifie `TTL/TCA/alpha/corr sont estimes hors surplus.` selon la règle `Q5_summary non vide avec ttl_obs et tca_q95`. La valeur observée (`ttl=419.95, tca=370.83959999999996`) est lue contre le seuil/règle (`ttl/tca finis`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: L'ancre thermique est quantifiable. [evidence:Q5-H-01] [source:SPEC2-Q5/Slides 28]
Lecture complémentaire de preuve `Q5-H-02`: le test vérifie `dTCA/dCO2 et dTCA/dGas sont positives.` selon la règle `dTCA_dCO2 > 0 et dTCA_dGas > 0`. La valeur observée (`dCO2=0.36727272727272725, dGas=1.8181818181818181`) est lue contre le seuil/règle (`>0`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Sensibilites analytiques coherentes. [evidence:Q5-H-02] [source:SPEC2-Q5]
Lecture complémentaire de preuve `Q5-S-01`: le test vérifie `BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.` selon la règle `Q5_summary non vide sur scenarios selectionnes`. La valeur observée (`1.0000`) est lue contre le seuil/règle (`>0 lignes`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Sensibilites scenario calculees. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
Lecture complémentaire de preuve `Q5-S-01`: le test vérifie `BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.` selon la règle `Q5_summary non vide sur scenarios selectionnes`. La valeur observée (`1.0000`) est lue contre le seuil/règle (`>0 lignes`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Sensibilites scenario calculees. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
Lecture complémentaire de preuve `Q5-S-01`: le test vérifie `BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.` selon la règle `Q5_summary non vide sur scenarios selectionnes`. La valeur observée (`1.0000`) est lue contre le seuil/règle (`>0 lignes`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Sensibilites scenario calculees. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]
Lecture complémentaire de preuve `Q5-S-01`: le test vérifie `BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.` selon la règle `Q5_summary non vide sur scenarios selectionnes`. La valeur observée (`1.0000`) est lue contre le seuil/règle (`>0 lignes`) avec statut `PASS` (conforme à la règle.). D'un point de vue décisionnel, cela signifie: Sensibilites scenario calculees. [evidence:Q5-S-01] [source:SPEC2-Q5/Slides 29]


## 4. Annexes de preuve et traçabilité

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
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE calculable | MEDIUM | BASE | PASS | 7 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE calculable | MEDIUM | DEMAND_UP | PASS | 7 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE calculable | MEDIUM | FLEX_UP | PASS | 7 | >=1 bascule | Le scenario fournit une variation exploitable. |
| Q1-S-02 | Q1 | SPEC2-Q1/Slides 5 | SCEN | DEFAULT | Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY | Les leviers scenario modifient la bascule vs BASE. | delta bascule_year_market vs BASE calculable | MEDIUM | LOW_RIGIDITY | PASS | 7 | >=1 bascule | Le scenario fournit une variation exploitable. |
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
| Q2-S-01 | Q2 | SPEC2-Q2/Slides 11 | SCEN | DEFAULT | Pentes projetees | Les pentes sont reproduites en mode scenario. | Q2_country_slopes non vide en SCEN | HIGH | BASE | PASS | 14 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | Q2 | SPEC2-Q2/Slides 11 | SCEN | DEFAULT | Pentes projetees | Les pentes sont reproduites en mode scenario. | Q2_country_slopes non vide en SCEN | HIGH | HIGH_CO2 | PASS | 14 | >0 lignes | Pentes prospectives calculees. |
| Q2-S-01 | Q2 | SPEC2-Q2/Slides 11 | SCEN | DEFAULT | Pentes projetees | Les pentes sont reproduites en mode scenario. | Q2_country_slopes non vide en SCEN | HIGH | HIGH_GAS | PASS | 14 | >0 lignes | Pentes prospectives calculees. |
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
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | BASE | PASS | 1 | status renseignes | La lecture de transition phase 3 est possible. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | DEMAND_UP | PASS | 1 | status renseignes | La lecture de transition phase 3 est possible. |
| Q3-S-02 | Q3 | Slides 17-19 | SCEN | DEFAULT | Validation entree phase 3 | Le statut prospectif est interpretable pour la transition phase 3. | status non vide en SCEN | MEDIUM | FLEX_UP | PASS | 1 | status renseignes | La lecture de transition phase 3 est possible. |
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
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | BASE | PASS | 1318.7589939342624 | capture apres finite | Sensibilite valeur exploitable. |
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | FLEX_UP | PASS | 1317.042435494933 | capture apres finite | Sensibilite valeur exploitable. |
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | HIGH_CO2 | PASS | 1336.2811724552707 | capture apres finite | Sensibilite valeur exploitable. |
| Q4-S-02 | Q4 | Slides 23-25 | SCEN | DEFAULT | Sensibilite valeur commodites | Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur. | delta pv_capture ou revenus vs BASE | MEDIUM | HIGH_GAS | PASS | 1356.6039238995759 | capture apres finite | Sensibilite valeur exploitable. |

#### Q5
| test_id | question_id | source_ref | mode | scenario_group | title | what_is_tested | metric_rule | severity_if_fail | scenario_id | status | value | threshold | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q5-H-01 | Q5 | SPEC2-Q5/Slides 28 | HIST | HIST_BASE | Ancre thermique historique | TTL/TCA/alpha/corr sont estimes hors surplus. | Q5_summary non vide avec ttl_obs et tca_q95 | HIGH | nan | PASS | ttl=419.95, tca=370.83959999999996 | ttl/tca finis | L'ancre thermique est quantifiable. |
| Q5-H-02 | Q5 | SPEC2-Q5 | HIST | HIST_BASE | Sensibilites analytiques | dTCA/dCO2 et dTCA/dGas sont positives. | dTCA_dCO2 > 0 et dTCA_dGas > 0 | CRITICAL | nan | PASS | dCO2=0.36727272727272725, dGas=1.8181818181818181 | >0 | Sensibilites analytiques coherentes. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | BASE | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | HIGH_CO2 | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | HIGH_GAS | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-01 | Q5 | SPEC2-Q5/Slides 29 | SCEN | DEFAULT | Sensibilites scenarisees | BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares. | Q5_summary non vide sur scenarios selectionnes | HIGH | HIGH_BOTH | PASS | 1 | >0 lignes | Sensibilites scenario calculees. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | BASE | PASS | -10168.862806747053 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_CO2 | PASS | -10177.062869892936 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_GAS | PASS | -10308.637127318678 | valeur finie | CO2 requis interpretable. |
| Q5-S-02 | Q5 | SPEC2-Q5/Slides 31 | SCEN | DEFAULT | CO2 requis pour TTL cible | Le CO2 requis est calcule et interpretable. | co2_required_* non NaN | MEDIUM | HIGH_BOTH | PASS | -10113.862806747053 | valeur finie | CO2 requis interpretable. |

### 4.2 Checks et warnings consolidés
| run_id | question_id | status | code | message | scope | scenario_id | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260210_113139 | Q1 | WARN | RC_IR_GT_1 | CZ-2018: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_IR_GT_1 | CZ-2019: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_IR_GT_1 | CZ-2022: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2022: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_IR_GT_1 | FR-2018: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_IR_GT_1 | FR-2019: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2019: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_IR_GT_1 | FR-2021: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2021: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_IR_GT_1 | FR-2024: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_LOW_REGIME_COHERENCE | FR-2024: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | DE-2030: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | DE-2040: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | FR-2030: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | FR-2040: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | IT_NORD-2030: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | IT_NORD-2040: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | DE-2030: capture price PV hors plage attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | DE-2040: capture price PV hors plage attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | ES-2040: capture price PV hors plage attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | FR-2030: capture price PV hors plage attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | FR-2040: capture price PV hors plage attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | IT_NORD-2030: capture price PV hors plage attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | IT_NORD-2040: capture price PV hors plage attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | DE-2030: capture price PV hors plage attendue. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | DE-2040: capture price PV hors plage attendue. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | FR-2030: capture price PV hors plage attendue. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | FR-2040: capture price PV hors plage attendue. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | IT_NORD-2030: capture price PV hors plage attendue. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | IT_NORD-2040: capture price PV hors plage attendue. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | DE-2030: capture price PV hors plage attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | DE-2040: capture price PV hors plage attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | ES-2040: capture price PV hors plage attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | FR-2030: capture price PV hors plage attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | FR-2040: capture price PV hors plage attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | IT_NORD-2030: capture price PV hors plage attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | RC_CAPTURE_RANGE | IT_NORD-2040: capture price PV hors plage attendue. | SCEN | LOW_RIGIDITY | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q1 | WARN | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=1 | BUNDLE |  | outputs\combined\FULL_20260210_113139\Q1\summary.json |
| FULL_20260210_113139 | Q2 | INFO | Q2_LOW_R2 | BE-WIND: R2 faible (0.09). | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | INFO | Q2_LOW_R2 | CZ-WIND: R2 faible (0.03). | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | INFO | Q2_LOW_R2 | DE-WIND: R2 faible (0.00). | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | INFO | Q2_LOW_R2 | IT_NORD-PV: R2 faible (0.01). | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | INFO | Q2_LOW_R2 | IT_NORD-WIND: R2 faible (0.10). | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_IR_GT_1 | CZ-2018: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_IR_GT_1 | CZ-2019: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_IR_GT_1 | CZ-2022: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2022: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | CZ-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_IR_GT_1 | FR-2018: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2018: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_IR_GT_1 | FR-2019: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2019: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_IR_GT_1 | FR-2021: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2021: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2023: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_IR_GT_1 | FR-2024: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_LOW_REGIME_COHERENCE | FR-2024: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | BE-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | BE-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | CZ-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_POSITIVE_PV_SLOPE | CZ: slope PV positive et significative. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | CZ-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | DE-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | DE-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | ES-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | ES-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | FR-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | FR-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | IT_NORD-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | IT_NORD-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | NL-PV: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | NL-WIND: n=2 < 3. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | DE-2030: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | DE-2040: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | FR-2030: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | FR-2040: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | IT_NORD-2030: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | IT_NORD-2040: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | BE-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | BE-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | CZ-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_POSITIVE_PV_SLOPE | CZ: slope PV positive et significative. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | CZ-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | DE-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | DE-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | ES-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | ES-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | FR-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | FR-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | IT_NORD-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | IT_NORD-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | NL-PV: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | NL-WIND: n=2 < 3. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | DE-2030: capture price PV hors plage attendue. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | DE-2040: capture price PV hors plage attendue. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | ES-2040: capture price PV hors plage attendue. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | FR-2030: capture price PV hors plage attendue. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | FR-2040: capture price PV hors plage attendue. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | IT_NORD-2030: capture price PV hors plage attendue. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | IT_NORD-2040: capture price PV hors plage attendue. | SCEN | HIGH_CO2 | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | BE-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | BE-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | CZ-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_POSITIVE_PV_SLOPE | CZ: slope PV positive et significative. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | CZ-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | DE-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | DE-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | ES-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | ES-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | FR-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | FR-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | IT_NORD-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | IT_NORD-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | NL-PV: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | Q2_FRAGILE | NL-WIND: n=2 < 3. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | DE-2030: capture price PV hors plage attendue. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | DE-2040: capture price PV hors plage attendue. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | ES-2040: capture price PV hors plage attendue. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | FR-2030: capture price PV hors plage attendue. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | FR-2040: capture price PV hors plage attendue. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | IT_NORD-2030: capture price PV hors plage attendue. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | RC_CAPTURE_RANGE | IT_NORD-2040: capture price PV hors plage attendue. | SCEN | HIGH_GAS | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q2 | WARN | BUNDLE_LEDGER_STATUS | ledger: FAIL=0, WARN=3 | BUNDLE |  | outputs\combined\FULL_20260210_113139\Q2\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | HIST |  | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | HIST |  | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | WARN | Q3_MUSTRUN_HIGH | ES: inversion_r_mustrun=53.3% (>50%). | HIST |  | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | HIST |  | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | WARN | Q3_DEMAND_HIGH | FR: inversion_k_demand=27.9% (>25%). | HIST |  | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | HIST |  | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | WARN | RC_IR_GT_1 | FR-2024: IR > 1 (must-run tres eleve en creux). | HIST |  | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | WARN | RC_LOW_REGIME_COHERENCE | FR-2024: regime_coherence < 0.55. | HIST |  | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | BE: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | FR: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | IT_NORD: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | WARN | RC_CAPTURE_RANGE | DE-2040: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | WARN | RC_CAPTURE_RANGE | FR-2040: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | WARN | RC_CAPTURE_RANGE | IT_NORD-2040: capture price PV hors plage attendue. | SCEN | BASE | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | BE: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | ES: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | FR: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | IT_NORD: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | NL: FAR cible deja atteinte. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | WARN | RC_CAPTURE_RANGE | DE-2040: capture price PV hors plage attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | WARN | RC_CAPTURE_RANGE | ES-2040: capture price PV hors plage attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | WARN | RC_CAPTURE_RANGE | FR-2040: capture price PV hors plage attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | WARN | RC_CAPTURE_RANGE | IT_NORD-2040: capture price PV hors plage attendue. | SCEN | DEMAND_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | BE: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | CZ: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |
| FULL_20260210_113139 | Q3 | INFO | Q3_FAR_ALREADY_REACHED | DE: FAR cible deja atteinte. | SCEN | FLEX_UP | outputs\combined\FULL_20260210_113139\Q3\summary.json |

### 4.3 Traçabilité tests -> sources
| run_id | question_id | test_id | source_ref | mode | scenario_id | status | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260210_113139 | Q1 | Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | nan | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | nan | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-H-03 | SPEC2-Q1 | HIST | nan | WARN | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-H-04 | Slides 4-6 | HIST | nan | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv |
| FULL_20260210_113139 | Q2 | Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | nan | PASS | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv |
| FULL_20260210_113139 | Q2 | Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | nan | PASS | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv |
| FULL_20260210_113139 | Q2 | Q2-H-03 | Slides 10-13 | HIST | nan | PASS | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv |
| FULL_20260210_113139 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv |
| FULL_20260210_113139 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv |
| FULL_20260210_113139 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv |
| FULL_20260210_113139 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | BASE | WARN | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv |
| FULL_20260210_113139 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv |
| FULL_20260210_113139 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv |
| FULL_20260210_113139 | Q3 | Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | nan | PASS | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv |
| FULL_20260210_113139 | Q3 | Q3-H-02 | SPEC2-Q3 | HIST | nan | PASS | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv |
| FULL_20260210_113139 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv |
| FULL_20260210_113139 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv |
| FULL_20260210_113139 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv |
| FULL_20260210_113139 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv |
| FULL_20260210_113139 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv |
| FULL_20260210_113139 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | PASS | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv |
| FULL_20260210_113139 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv |
| FULL_20260210_113139 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | PASS | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv |
| FULL_20260210_113139 | Q4 | Q4-H-01 | SPEC2-Q4/Slides 22 | HIST | nan | PASS | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv |
| FULL_20260210_113139 | Q4 | Q4-H-02 | SPEC2-Q4 | HIST | nan | PASS | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv |
| FULL_20260210_113139 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv |
| FULL_20260210_113139 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv |
| FULL_20260210_113139 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv |
| FULL_20260210_113139 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv |
| FULL_20260210_113139 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv |
| FULL_20260210_113139 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | FLEX_UP | PASS | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv |
| FULL_20260210_113139 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv |
| FULL_20260210_113139 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv |
| FULL_20260210_113139 | Q5 | Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | nan | PASS | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv |
| FULL_20260210_113139 | Q5 | Q5-H-02 | SPEC2-Q5 | HIST | nan | PASS | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv |
| FULL_20260210_113139 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv |
| FULL_20260210_113139 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv |
| FULL_20260210_113139 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv |
| FULL_20260210_113139 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv |
| FULL_20260210_113139 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | BASE | PASS | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv |
| FULL_20260210_113139 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv |
| FULL_20260210_113139 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv |
| FULL_20260210_113139 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv |

### 4.4 Couverture Slides/SPECS -> preuves
| slide_id | requirement_id | question_id | requirement_text | covered | coverage_method | evidence_ref | test_id | report_section |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SLIDE_01_01 | GLOBAL | Contexte et 5 questions à traiter Nous voulons expliquer la dynamique des capture prices des renouvelables intermittents en restant sur une approche simple, auditable et utile pour la décision | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_02 | GLOBAL | Nous traitons 5 questions, dans l’ordre logique des phases de marché | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_03 | GLOBAL | Bascule phase 1 → phase 2 Quels paramètres font passer un marché d’un régime “confortable” à un régime où les prix et la valeur des actifs deviennent structurellement sous pression | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_04 | GLOBAL | Quels ratios simples expliquent la bascule | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_05 | GLOBAL | Pente en phase 2 À quelle vitesse la valeur captée se dégrade en phase 2 | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_06 | GLOBAL | Quels facteurs expliquent cette vitesse et pourquoi elle diffère selon les pays | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_07 | GLOBAL | Sortie de la phase 2 et entrée en phase 3 À quelles conditions la dynamique cesse de s’aggraver et commence à se stabiliser | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_08 | GLOBAL | Que faudrait-il pour inverser la tendance | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_09 | GLOBAL | Par exemple une hausse durable de la demande | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_10 | GLOBAL | Rôle du stockage batteries couplé au solaire Quel niveau de batteries associé au solaire change réellement la trajectoire | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_11 | GLOBAL | Comment cette condition dépend du coût des batteries, du prix du CO2 et du rôle résiduel du thermique | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_12 | GLOBAL | Impact des commodités et du CO2 Comment le prix du gaz et le prix du CO2 modifient l’ancre des prix et donc les capture prices | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 1 | SLIDE_01_13 | GLOBAL | Quel niveau de CO2 peut relever le haut de la courbe de prix. | yes | global_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | GLOBAL |
| 2 | SLIDE_02_01 | Q1 | Question 1 Définition Question 1 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_02 | Q1 | Quels paramètres expliquent le passage de la phase de marché 1 à la phase de marché 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_03 | Q1 | Définition des phases de marché, en langage simple | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_04 | Q1 | La phase 1 est une situation où l’électricité renouvelable variable ne change pas encore le fonctionnement du marché de façon visible et répétée | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_05 | Q1 | La phase 2 est une situation où la production variable crée régulièrement des heures de prix très bas ou négatifs et où la valeur moyenne captée par ces actifs baisse de façon mesurable | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_06 | Q1 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_07 | Q1 | Le “capture price” d’une filière est le prix moyen reçu pendant les heures où elle produit, pondéré par sa production horaire | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_08 | Q1 | Le “capture ratio” est le capture price divisé par le prix moyen de marché sur la même période | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_09 | Q1 | Un “prix négatif” est un prix day ahead inférieur à zéro | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_10 | Q1 | Un “surplus” est une situation où, sur une heure donnée, la production inflexible plus la production renouvelable variable dépasse ce que le système peut absorber via la demande et les flexibilités disponibles | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_11 | Q1 | Le “ratio d’inflexibilité” est la part de production inflexible par rapport à la demande durant les heures creuses, ce qui mesure la rigidité du système | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_12 | Q1 | Le “ratio de surplus” est la part d’énergie qui apparaît en surplus sur l’année par rapport à l’énergie totale produite | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_13 | Q1 | Le “ratio d’absorption par flexibilité” est la part de ce surplus que le système peut absorber via des leviers identifiables comme exportations, pompage, charge batteries et effacements | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_14 | Q1 | Objet de l’analyse pour Q1 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 2 | SLIDE_02_15 | Q1 | Nous voulons passer d’un constat “il y a des prix négatifs” à une règle simple du type “la bascule se produit quand une combinaison de surplus, rigidité et faible capacité d’absorption devient récurrente et se reflète dans la distribution des prix et dans le capture ratio”. | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 | Q1-H-01 | Q1 |
| 3 | SLIDE_03_01 | Q1 | Question 1 Hypothèses Hypothèse centrale | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_02 | Q1 | La phase 1 se transforme en phase 2 quand les épisodes de surplus deviennent suffisamment fréquents pour modifier la distribution des prix et donc la valeur captée par le solaire et l’éolien | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_03 | Q1 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_04 | Q1 | Un “surplus” est une heure où la demande ne suffit plus à absorber la somme production inflexible plus production variable, compte tenu des capacités d’export et de flexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_05 | Q1 | Le “ratio de surplus” est une mesure annuelle du volume de surplus rapporté à la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_06 | Q1 | Le “ratio d’absorption par flexibilité” est la fraction du surplus absorbée par des leviers physiques identifiables | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_07 | Q1 | Le “ratio d’inflexibilité” mesure la rigidité du parc sur les heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_08 | Q1 | Le “capture ratio” est le prix moyen reçu par une filière rapporté au prix moyen de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_09 | Q1 | Hypothèses minimales à tester, sans usine à gaz | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_10 | Q1 | La bascule est d’abord un phénomène physique | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_11 | Q1 | Elle commence quand la fréquence des heures de surplus dépasse un niveau qui n’est plus marginal | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_12 | Q1 | La bascule arrive plus tôt si le système est rigide | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_13 | Q1 | Un ratio d’inflexibilité élevé réduit l’espace disponible pour absorber la production variable en heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_14 | Q1 | La bascule arrive plus tôt si les capacités d’absorption sont limitées | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_15 | Q1 | Un ratio d’absorption par flexibilité faible signifie que le surplus se transforme en contrainte de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_16 | Q1 | La bascule est plus tardive si la production variable est bien alignée avec la demande | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_17 | Q1 | Une forte corrélation horaire entre production solaire et demande réduit les surplus | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_18 | Q1 | La bascule dépend aussi des règles et incitations | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 3 | SLIDE_03_19 | Q1 | Si des volumes importants sont développés et injectés sans exposition au signal de prix, la phase 2 peut démarrer plus tôt ou durer plus longtemps car l’investissement ne se freine pas naturellement. | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 | Q1-H-01; Q1-H-02 | Q1 |
| 4 | SLIDE_04_01 | Q1 | Question 1 Tests empiriques Objectif des tests | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_02 | Q1 | Construire une règle de bascule vérifiable et réplicable, basée sur des données observées et sur des définitions physiques simples | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_03 | Q1 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_04 | Q1 | Le “surplus” correspond à des heures où production inflexible plus production variable dépasse ce que la demande et les flexibilités peuvent absorber | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_05 | Q1 | Le “ratio de surplus” mesure le volume annuel de surplus rapporté à la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_06 | Q1 | Le “ratio d’absorption par flexibilité” mesure la part de surplus absorbée par exportations, pompage, charge batteries et effacements | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_07 | Q1 | Le “ratio d’inflexibilité” mesure la rigidité du système en heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_08 | Q1 | Le “capture ratio” mesure la valeur captée par une filière | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_09 | Q1 | Jeu de tests simple, en trois blocs | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_10 | Q1 | Bloc A | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_11 | Q1 | Construire les indicateurs physiques par pays et par année | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_12 | Q1 | Nous calculons heure par heure un indicateur de demande résiduelle, qui correspond à la demande moins la production variable moins la production inflexible | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_13 | Q1 | Nous identifions les heures où cette demande résiduelle devient négative, ce qui signale un surplus potentiel | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_14 | Q1 | Nous mesurons le ratio de surplus annuel et le ratio d’inflexibilité sur les heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_15 | Q1 | Bloc B | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_16 | Q1 | Confronter les indicateurs physiques aux signaux de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_17 | Q1 | Nous comptons le nombre d’heures de prix négatifs et le nombre d’heures de prix très bas | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_18 | Q1 | Nous calculons le capture ratio solaire et le capture ratio éolien | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_19 | Q1 | Nous vérifions que la bascule vers la phase 2 se manifeste à la fois dans les prix et dans la valeur captée, et pas uniquement dans un seul indicateur | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_20 | Q1 | Bloc C | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_21 | Q1 | Identifier un seuil robuste | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_22 | Q1 | Nous cherchons un point de rupture statistique, par exemple une accélération du nombre d’heures négatives ou une chute du capture ratio au-delà d’un certain niveau de ratio de surplus | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_23 | Q1 | Nous validons le seuil en comparant plusieurs pays et en vérifiant qu’il se retrouve avec une logique cohérente, même si les valeurs exactes diffèrent | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_24 | Q1 | Critère de réussite | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 4 | SLIDE_04_25 | Q1 | Nous obtenons une règle de bascule qui explique correctement le passage phase 1 à phase 2 sur plusieurs pays, et qui reste stable quand on change légèrement la période historique. | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-01; Q1-H-02; Q1-H-04 | Q1 |
| 5 | SLIDE_05_01 | Q1 | Question 1 Scénarios prospectifs Pourquoi des scénarios sont nécessaires pour Q1 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_02 | Q1 | Le passé ne suffit pas | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_03 | Q1 | Nous devons tester comment un pays bascule quand la pénétration renouvelable continue d’augmenter et quand la demande ou la flexibilité changent | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_04 | Q1 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_05 | Q1 | Le “ratio de surplus” est le volume annuel de surplus rapporté à la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_06 | Q1 | Le “ratio d’absorption par flexibilité” est la part de surplus absorbée par des leviers identifiables comme exportations, pompage, charge batteries et effacements | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_07 | Q1 | Le “ratio d’inflexibilité” mesure la rigidité de la production en heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_08 | Q1 | Le “capture ratio” mesure la valeur captée par une filière | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_09 | Q1 | Principe de scénarisation pragmatique | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_10 | Q1 | Nous ne cherchons pas à simuler un dispatch complet optimisé | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_11 | Q1 | Nous cherchons à projeter des ordres de grandeur crédibles, avec une logique explicable, en faisant varier quelques variables exogènes | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_12 | Q1 | Variables exogènes minimales pour scénarios de bascule | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_13 | Q1 | La trajectoire de demande électrique, avec une hypothèse haute et basse | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_14 | Q1 | La trajectoire de capacités solaires et éoliennes | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_15 | Q1 | La trajectoire de production inflexible, ou au minimum sa rigidité en heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_16 | Q1 | La trajectoire de capacité d’absorption, via export, pompage, batteries et effacements | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_17 | Q1 | Une hypothèse de cadre d’incitation, qui représente la part de nouvelles capacités développées sans exposition forte au prix spot | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_18 | Q1 | Ce que l’on doit obtenir en sortie | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_19 | Q1 | Une année de bascule probable pour chaque pays et chaque trajectoire | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 5 | SLIDE_05_20 | Q1 | Une explication causale sous forme de ratios simples qui changent de valeur avant la bascule. | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 | Q1-H-04; Q1-S-01; Q1-S-02 | Q1 |
| 6 | SLIDE_06_01 | Q1 | Question 1 Limites et points de vigilance Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_02 | Q1 | Le “surplus” est une heure où la production dépasse la capacité d’absorption du système | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_03 | Q1 | Le “ratio d’absorption par flexibilité” mesure ce qui est absorbé par des leviers identifiés | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_04 | Q1 | Le “capture ratio” mesure la valeur captée par une filière | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_05 | Q1 | Limites structurelles si on reste volontairement simple | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_06 | Q1 | Les données ne captent pas toutes les flexibilités réelles | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_07 | Q1 | Certaines flexibilités sont infra horaires ou ne sont pas observables simplement | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_08 | Q1 | La corrélation n’est pas une preuve de causalité | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_09 | Q1 | Une bascule observée peut être accélérée ou freinée par des facteurs non modélisés comme des changements de règles de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_10 | Q1 | Le rôle des incitations peut être déterminant | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_11 | Q1 | Si l’investissement est guidé par des mécanismes politiques et non par le marché, une règle purement physique peut sous estimer la durée de la phase 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_12 | Q1 | Les interconnexions peuvent masquer le problème | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_13 | Q1 | Un pays peut absorber son surplus par export, mais cela dépend de la situation simultanée des voisins | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_14 | Q1 | Les années atypiques peuvent fausser les seuils | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_15 | Q1 | Nous devons isoler les chocs extrêmes et tester la stabilité | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_16 | Q1 | Conséquence de ces limites | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 6 | SLIDE_06_17 | Q1 | La bascule doit être présentée comme une estimation robuste à grosse maille, pas comme une date exacte au mois près. | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 | Q1-H-04 | Q1 |
| 7 | SLIDE_07_01 | Q1 | Question 1 Livrable attendu Livrable principal | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_02 | Q1 | Un jeu de “règles de bascule” auditable qui explique le passage de la phase de marché 1 à la phase de marché 2 | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_03 | Q1 | Définitions nécessaires sur cette slide | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_04 | Q1 | Le “ratio de surplus” mesure le volume annuel de surplus rapporté à la production totale | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_05 | Q1 | Le “ratio d’absorption par flexibilité” mesure la fraction de surplus absorbée par exportations, pompage, charge batteries et effacements | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_06 | Q1 | Le “ratio d’inflexibilité” mesure la rigidité du système en heures creuses | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_07 | Q1 | Le “capture ratio” mesure la valeur captée par une filière | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_08 | Q1 | Contenu concret du livrable | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_09 | Q1 | Nous fournissons une définition claire et unique des phases de marché 1 et 2 | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_10 | Q1 | Nous fournissons une liste courte de ratios et une formule de bascule, compréhensible et calculable | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_11 | Q1 | Nous fournissons une justification empirique par pays, basée sur données historiques | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_12 | Q1 | Nous fournissons une estimation de seuils de bascule, avec une fourchette et un niveau de confiance | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_13 | Q1 | Nous fournissons un diagnostic des leviers les plus efficaces pour retarder la bascule, en distinguant demande, flexibilité et rigidité du parc | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_14 | Q1 | Format de restitution | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_15 | Q1 | Une note courte et structurée | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_16 | Q1 | Un ensemble de graphiques simples et répétables | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 7 | SLIDE_07_17 | Q1 | Un fichier de calcul permettant de recalculer les ratios avec de nouvelles hypothèses. | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02; outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 | Q1-H-01; Q1-H-02; Q1-H-03; Q1-H-04; Q1-S-01 | Q1 |
| 8 | SLIDE_08_01 | Q2 | Question 2 Définition Question 2 | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_02 | Q2 | Quelle est la pente de la phase de marché 2 et quels facteurs la pilotent | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_03 | Q2 | Définition opérationnelle de la “pente” | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_04 | Q2 | La pente mesure la vitesse à laquelle la valeur captée se dégrade quand la pénétration des renouvelables variables augmente dans un marché déjà entré en phase 2 | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_05 | Q2 | Définitions nécessaires sur cette slide | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_06 | Q2 | Le “capture price” est le prix moyen reçu pendant les heures de production d’une filière, pondéré par sa production horaire | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_07 | Q2 | Le “capture ratio” est le capture price divisé par le prix moyen de marché | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_08 | Q2 | La “pénétration” d’une filière est sa part dans la production totale sur une année | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_09 | Q2 | L’“ancre thermique des prix” est un niveau de prix représentatif des heures où le thermique fixe le prix, et il dépend surtout du coût du gaz et du prix du CO2 | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_10 | Q2 | Le “ratio de surplus” mesure le volume annuel de surplus rapporté à la production totale | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_11 | Q2 | Le “ratio d’absorption par flexibilité” mesure la fraction du surplus absorbée par des leviers identifiables | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_12 | Q2 | Mesures possibles de pente, à choisir explicitement | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_13 | Q2 | Nous pouvons mesurer la pente du capture ratio solaire en fonction de la pénétration solaire | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_14 | Q2 | Nous pouvons mesurer la pente du nombre d’heures de prix négatifs en fonction de la pénétration solaire et éolienne | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_15 | Q2 | Nous pouvons mesurer la pente de la profondeur des prix négatifs, si nous voulons aller au delà du comptage d’heures | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_16 | Q2 | Sortie attendue | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 8 | SLIDE_08_17 | Q2 | Une estimation chiffrée de la pente, par pays, avec une explication causale simple des écarts entre pays. | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_01 | Q2 | Question 2 Hypothèses Définitions nécessaires sur cette slide | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_02 | Q2 | Le “capture ratio” est la valeur captée par une filière rapportée au prix moyen de marché | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_03 | Q2 | Le “ratio de surplus” mesure l’énergie en surplus sur l’année rapportée à la production totale | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_04 | Q2 | Le “ratio d’absorption par flexibilité” mesure ce que la flexibilité absorbe sur ce surplus | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_05 | Q2 | Le “ratio d’inflexibilité” mesure la rigidité du parc en heures creuses | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_06 | Q2 | L’“ancre thermique des prix” dépend du coût du gaz et du prix du CO2 | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_07 | Q2 | Hypothèse générale | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_08 | Q2 | En phase 2, la pente est pilotée par deux effets qui se cumulent | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_09 | Q2 | Le premier effet est l’augmentation de la fréquence des heures de prix très bas | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_10 | Q2 | Le second effet est la baisse de la valeur moyenne captée car la production se concentre sur ces heures | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_11 | Q2 | Hypothèses explicatives de la pente, à tester de façon pragmatique | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_12 | Q2 | La pente est plus forte si la production solaire est peu corrélée à la demande | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_13 | Q2 | Une faible corrélation augmente les surplus à midi et donc accélère la chute du capture ratio | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_14 | Q2 | La pente est plus forte si le système est rigide | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_15 | Q2 | Un ratio d’inflexibilité élevé réduit les marges d’absorption en heures creuses et accélère les heures de prix négatifs | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_16 | Q2 | La pente est plus faible si la flexibilité croît vite | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_17 | Q2 | Un ratio d’absorption par flexibilité élevé réduit la fréquence et l’intensité des épisodes de prix extrêmes | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_18 | Q2 | La pente dépend de l’ancre thermique | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_19 | Q2 | Si le coût marginal thermique est élevé, la différence entre heures chères et heures en surplus peut être plus grande, ce qui peut amplifier la cannibalisation en valeur relative | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_20 | Q2 | La pente dépend des règles d’investissement | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 9 | SLIDE_09_21 | Q2 | Si une grande partie des nouvelles capacités est développée avec une protection hors marché, l’investissement peut continuer malgré des signaux spot dégradés, ce qui accentue la pente et prolonge la phase 2. | yes | question_fallback | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03; Q2-S-01; Q2-S-02 | Q2 |
| 10 | SLIDE_10_01 | Q2 | Question 2 Tests empiriques Objectif des tests | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_02 | Q2 | Mesurer la pente de façon robuste et expliquer sa variance entre pays par un petit nombre de drivers testables | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_03 | Q2 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_04 | Q2 | Le “capture ratio” est la valeur captée par une filière rapportée au prix moyen de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_05 | Q2 | La “pénétration” est la part de production annuelle d’une filière dans la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_06 | Q2 | L’“ancre thermique des prix” est un niveau représentatif des heures où le thermique fixe le prix, et elle dépend surtout du coût du gaz et du prix du CO2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_07 | Q2 | Le “ratio de surplus” mesure l’énergie en surplus sur l’année rapportée à la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_08 | Q2 | Le “ratio d’inflexibilité” mesure la rigidité du parc en heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_09 | Q2 | Le “ratio d’absorption par flexibilité” mesure la fraction de surplus absorbée par flexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_10 | Q2 | Test 1 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_11 | Q2 | Estimer la pente en phase 2 de manière simple | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_12 | Q2 | Nous identifions les années où un pays est en phase 2 avec des critères explicites | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_13 | Q2 | Nous régressons le capture ratio solaire sur la pénétration solaire sur ces années | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_14 | Q2 | Nous exprimons la pente en points de capture ratio perdus par point de pénétration ajouté | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_15 | Q2 | Test 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_16 | Q2 | Vérifier que la pente n’est pas un artefact d’ancre thermique | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_17 | Q2 | Nous recalculons la pente en contrôlant l’ancre thermique des prix, qui dépend du gaz et du CO2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_18 | Q2 | Nous distinguons la baisse de valeur due à plus de surplus de la baisse de valeur due à une ancre thermique qui change | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_19 | Q2 | Test 3 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_20 | Q2 | Expliquer la pente par des drivers simples | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_21 | Q2 | Nous testons si la pente est corrélée au ratio de surplus et au ratio d’inflexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_22 | Q2 | Nous testons si la pente est corrélée au ratio d’absorption par flexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_23 | Q2 | Nous testons si la pente est corrélée à un indicateur de corrélation production solaire et demande | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_24 | Q2 | Test 4 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_25 | Q2 | Tests de robustesse | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_26 | Q2 | Nous excluons les années de crise et nous vérifions si la pente reste du même ordre de grandeur | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 10 | SLIDE_10_27 | Q2 | Nous testons la stabilité du résultat si on change la période et si on change le pays de référence. | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-01; Q2-H-02; Q2-H-03 | Q2 |
| 11 | SLIDE_11_01 | Q2 | Question 2 Scénarios prospectifs et leviers Pourquoi faire des scénarios pour la pente | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_02 | Q2 | Même si la pente est mesurée sur l’historique, elle peut changer si la flexibilité se développe ou si les règles d’investissement changent | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_03 | Q2 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_04 | Q2 | La “pente” est la vitesse de dégradation du capture ratio en phase 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_05 | Q2 | Le “ratio d’absorption par flexibilité” est la fraction du surplus absorbée par des leviers physiques identifiables | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_06 | Q2 | L’“ancre thermique des prix” dépend du coût du gaz et du prix du CO2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_07 | Q2 | Le “capture ratio” est la valeur captée par une filière rapportée au prix moyen de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_08 | Q2 | Scénarios simples à construire | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_09 | Q2 | Scénario A | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_10 | Q2 | Demande faible et forte croissance solaire | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_11 | Q2 | La pente doit s’accentuer si la flexibilité ne suit pas | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_12 | Q2 | Scénario B | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_13 | Q2 | Demande dynamique via électrification | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_14 | Q2 | La pente peut se réduire si les heures de surplus diminuent | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_15 | Q2 | Scénario C | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_16 | Q2 | Accélération stockage et effacement | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_17 | Q2 | La pente se réduit si le ratio d’absorption par flexibilité augmente vite | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_18 | Q2 | Scénario D | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_19 | Q2 | Choc gaz et CO2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_20 | Q2 | L’ancre thermique augmente et change la valeur relative, même si le surplus ne change pas | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_21 | Q2 | Scénario E | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_22 | Q2 | Maintien d’incitations hors marché sur de gros volumes | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_23 | Q2 | La pente peut rester forte car l’investissement ne se freine pas naturellement | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_24 | Q2 | Leviers à relier directement aux drivers | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_25 | Q2 | Le levier “flexibilité” agit sur le ratio d’absorption par flexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_26 | Q2 | Le levier “pilotabilité” agit sur le ratio d’inflexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 11 | SLIDE_11_27 | Q2 | Le levier “politique et règles de soutien” agit sur la trajectoire d’investissement et donc sur la vitesse d’augmentation de la pénétration. | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 | Q2-H-02; Q2-H-03; Q2-S-01 | Q2 |
| 12 | SLIDE_12_01 | Q2 | Question 2 Limites et règles d’interprétation Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_02 | Q2 | Le “capture ratio” est la valeur captée par une filière rapportée au prix moyen de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_03 | Q2 | L’“ancre thermique des prix” dépend du coût du gaz et du prix du CO2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_04 | Q2 | Le “ratio de surplus” mesure l’énergie en surplus sur l’année rapportée à la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_05 | Q2 | Limites si on veut rester auditable | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_06 | Q2 | La pente observée sur dix ans peut refléter plusieurs régimes différents | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_07 | Q2 | Le marché peut changer de règles au milieu de la période | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_08 | Q2 | La pente peut dépendre d’effets voisins | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_09 | Q2 | L’absorption par export dépend aussi de la situation simultanée des pays interconnectés | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_10 | Q2 | Les incitations politiques sont difficiles à quantifier sans une variable dédiée | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_11 | Q2 | Si on ne modélise pas ce facteur, on peut mal expliquer la durée de phase 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_12 | Q2 | Une pente statistique n’est pas une loi physique | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_13 | Q2 | Elle doit être interprétée comme un ordre de grandeur conditionnel | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_14 | Q2 | Règles de lecture à imposer | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_15 | Q2 | Nous présentons toujours une pente avec un intervalle d’incertitude | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_16 | Q2 | Nous explicitons les années exclues et la raison | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 12 | SLIDE_12_17 | Q2 | Nous relions chaque pente à des variables explicatives mesurables, sinon elle n’est pas actionnable. | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02; outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-02; Q2-H-03 | Q2 |
| 13 | SLIDE_13_01 | Q2 | Question 2 Livrable attendu Livrable principal | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_02 | Q2 | Un diagnostic chiffré de la pente en phase 2, et une explication simple des facteurs qui la pilotent | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_03 | Q2 | Définitions nécessaires sur cette slide | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_04 | Q2 | Le “capture ratio” est la valeur captée par une filière rapportée au prix moyen de marché | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_05 | Q2 | La “pente” est la variation du capture ratio quand la pénétration augmente en phase 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_06 | Q2 | L’“ancre thermique des prix” dépend du coût du gaz et du prix du CO2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_07 | Q2 | Le “ratio de surplus” mesure l’énergie en surplus sur l’année rapportée à la production totale | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_08 | Q2 | Le “ratio d’absorption par flexibilité” mesure la part de surplus absorbée par flexibilité | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_09 | Q2 | Le “ratio d’inflexibilité” mesure la rigidité du parc en heures creuses | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_10 | Q2 | Contenu concret du livrable | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_11 | Q2 | Nous fournissons, par pays, une pente du capture ratio solaire et une pente du capture ratio éolien en phase 2 | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_12 | Q2 | Nous fournissons une décomposition qualitative et si possible quantitative des drivers, avec un ordre de grandeur par driver | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_13 | Q2 | Nous fournissons une lecture opérationnelle pour TTE, sous forme de règles simples | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_14 | Q2 | Par exemple une pente forte signifie que chaque point de pénétration additionnel détruit rapidement la valeur captée si aucune flexibilité ne suit | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |
| 13 | SLIDE_13_15 | Q2 | Nous fournissons une analyse de sensibilité à l’ancre thermique via gaz et CO2, car cette ancre change le niveau de valeur même si la cannibalisation relative reste identique | yes | direct_slide_match | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 | Q2-H-03 | Q2 |

### 4.5 Dictionnaire de preuves
| run_id | question_id | test_id | source_ref | mode | scenario_id | status | value | threshold | interpretation | evidence_ref |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FULL_20260210_113139 | Q1 | Q1-H-01 | SPEC2-Q1/Slides 2-4 | HIST | nan | PASS | 4.1020408163265305 | score present | Le score de bascule marche est exploitable. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-01 |
| FULL_20260210_113139 | Q1 | Q1-H-02 | SPEC2-Q1/Slides 3-4 | HIST | nan | PASS | far_energy,ir_p10,sr_energy | SR/FAR/IR presents | Le stress physique est calculable. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-02 |
| FULL_20260210_113139 | Q1 | Q1-H-03 | SPEC2-Q1 | HIST | nan | WARN | 42.86% | >=50% | Concordance mesuree entre bascules marche et physique. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-03 |
| FULL_20260210_113139 | Q1 | Q1-H-04 | Slides 4-6 | HIST | nan | PASS | 0.914 | confidence moyenne >=0.60 | Proxy de robustesse du diagnostic de bascule. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-H-04 |
| FULL_20260210_113139 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260210_113139 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260210_113139 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260210_113139 | Q1 | Q1-S-01 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 7 | >0 lignes | La bascule projetee est produite. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-01 |
| FULL_20260210_113139 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | BASE | PASS | 7 | >=1 bascule | Le scenario fournit une variation exploitable. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260210_113139 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | DEMAND_UP | PASS | 7 | >=1 bascule | Le scenario fournit une variation exploitable. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260210_113139 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | FLEX_UP | PASS | 7 | >=1 bascule | Le scenario fournit une variation exploitable. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260210_113139 | Q1 | Q1-S-02 | SPEC2-Q1/Slides 5 | SCEN | LOW_RIGIDITY | PASS | 7 | >=1 bascule | Le scenario fournit une variation exploitable. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-02 |
| FULL_20260210_113139 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | BASE | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260210_113139 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | DEMAND_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260210_113139 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | FLEX_UP | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260210_113139 | Q1 | Q1-S-03 | SPEC2-Q1 | SCEN | LOW_RIGIDITY | PASS | 100.00% | >=50% lignes >=0.55 | La coherence scenario est lisible. | outputs\combined\FULL_20260210_113139\Q1\test_ledger.csv#test_id=Q1-S-03 |
| FULL_20260210_113139 | Q2 | Q2-H-01 | SPEC2-Q2/Slides 10 | HIST | nan | PASS | 14 | >0 lignes | Les pentes historiques sont calculees. | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-01 |
| FULL_20260210_113139 | Q2 | Q2-H-02 | SPEC2-Q2/Slides 10-12 | HIST | nan | PASS | n,p_value,r2 | r2,p_value,n disponibles | La robustesse statistique est lisible. | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-02 |
| FULL_20260210_113139 | Q2 | Q2-H-03 | Slides 10-13 | HIST | nan | PASS | 6 | >0 lignes | Les drivers de pente sont disponibles. | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-H-03 |
| FULL_20260210_113139 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | BASE | PASS | 14 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260210_113139 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_CO2 | PASS | 14 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260210_113139 | Q2 | Q2-S-01 | SPEC2-Q2/Slides 11 | SCEN | HIGH_GAS | PASS | 14 | >0 lignes | Pentes prospectives calculees. | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-01 |
| FULL_20260210_113139 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | BASE | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260210_113139 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_CO2 | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260210_113139 | Q2 | Q2-S-02 | SPEC2-Q2 | SCEN | HIGH_GAS | WARN | 0.00% | >=30% robustes | Delta de pente interpretable avec robustesse. | outputs\combined\FULL_20260210_113139\Q2\test_ledger.csv#test_id=Q2-S-02 |
| FULL_20260210_113139 | Q3 | Q3-H-01 | SPEC2-Q3/Slides 16 | HIST | nan | PASS | 7 | >0 lignes | Les tendances historiques sont calculees. | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv#test_id=Q3-H-01 |
| FULL_20260210_113139 | Q3 | Q3-H-02 | SPEC2-Q3 | HIST | nan | PASS | 2 | status valides | Les statuts business sont renseignes. | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv#test_id=Q3-H-02 |
| FULL_20260210_113139 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | BASE | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260210_113139 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | DEMAND_UP | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260210_113139 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | FLEX_UP | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260210_113139 | Q3 | Q3-S-01 | SPEC2-Q3/Slides 17 | SCEN | LOW_RIGIDITY | PASS | 7 | colonnes inversion presentes | Les ordres de grandeur d'inversion sont quantifies. | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv#test_id=Q3-S-01 |
| FULL_20260210_113139 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | BASE | PASS | 1 | status renseignes | La lecture de transition phase 3 est possible. | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260210_113139 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | DEMAND_UP | PASS | 1 | status renseignes | La lecture de transition phase 3 est possible. | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260210_113139 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | FLEX_UP | PASS | 1 | status renseignes | La lecture de transition phase 3 est possible. | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260210_113139 | Q3 | Q3-S-02 | Slides 17-19 | SCEN | LOW_RIGIDITY | PASS | 1 | status renseignes | La lecture de transition phase 3 est possible. | outputs\combined\FULL_20260210_113139\Q3\test_ledger.csv#test_id=Q3-S-02 |
| FULL_20260210_113139 | Q4 | Q4-H-01 | SPEC2-Q4/Slides 22 | HIST | nan | PASS | HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED | 3 modes executes | Les trois modes Q4 sont disponibles. | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv#test_id=Q4-H-01 |
| FULL_20260210_113139 | Q4 | Q4-H-02 | SPEC2-Q4 | HIST | nan | PASS | PASS | pas de FAIL | Les invariants physiques batterie sont respectes. | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv#test_id=Q4-H-02 |
| FULL_20260210_113139 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | BASE | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260210_113139 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | FLEX_UP | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260210_113139 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_CO2 | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260210_113139 | Q4 | Q4-S-01 | SPEC2-Q4/Slides 23 | SCEN | HIGH_GAS | PASS | 1 | >0 lignes | Resultats Q4 prospectifs disponibles. | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv#test_id=Q4-S-01 |
| FULL_20260210_113139 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | BASE | PASS | 1318.7589939342624 | capture apres finite | Sensibilite valeur exploitable. | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260210_113139 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | FLEX_UP | PASS | 1317.042435494933 | capture apres finite | Sensibilite valeur exploitable. | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260210_113139 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_CO2 | PASS | 1336.2811724552707 | capture apres finite | Sensibilite valeur exploitable. | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260210_113139 | Q4 | Q4-S-02 | Slides 23-25 | SCEN | HIGH_GAS | PASS | 1356.6039238995759 | capture apres finite | Sensibilite valeur exploitable. | outputs\combined\FULL_20260210_113139\Q4\test_ledger.csv#test_id=Q4-S-02 |
| FULL_20260210_113139 | Q5 | Q5-H-01 | SPEC2-Q5/Slides 28 | HIST | nan | PASS | ttl=419.95, tca=370.83959999999996 | ttl/tca finis | L'ancre thermique est quantifiable. | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv#test_id=Q5-H-01 |
| FULL_20260210_113139 | Q5 | Q5-H-02 | SPEC2-Q5 | HIST | nan | PASS | dCO2=0.36727272727272725, dGas=1.8181818181818181 | >0 | Sensibilites analytiques coherentes. | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv#test_id=Q5-H-02 |
| FULL_20260210_113139 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | BASE | PASS | 1 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260210_113139 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_CO2 | PASS | 1 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260210_113139 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_GAS | PASS | 1 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260210_113139 | Q5 | Q5-S-01 | SPEC2-Q5/Slides 29 | SCEN | HIGH_BOTH | PASS | 1 | >0 lignes | Sensibilites scenario calculees. | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv#test_id=Q5-S-01 |
| FULL_20260210_113139 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | BASE | PASS | -10168.862806747053 | valeur finie | CO2 requis interpretable. | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260210_113139 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_CO2 | PASS | -10177.062869892936 | valeur finie | CO2 requis interpretable. | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260210_113139 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_GAS | PASS | -10308.637127318678 | valeur finie | CO2 requis interpretable. | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv#test_id=Q5-S-02 |
| FULL_20260210_113139 | Q5 | Q5-S-02 | SPEC2-Q5/Slides 31 | SCEN | HIGH_BOTH | PASS | -10113.862806747053 | valeur finie | CO2 requis interpretable. | outputs\combined\FULL_20260210_113139\Q5\test_ledger.csv#test_id=Q5-S-02 |

## 5. Écarts restants (obligatoire)

Aucun écart critique détecté par les quality gates.
