# Rapport Final Detaille V2 - Run 20260210_105935

Generation combine-first: ce rapport lit d'abord les outputs unifies Q1..Q5.
Dernier run combine detecte: `outputs\combined\SMOKE_20260210_105822_Q5`

## Resume executif
Le rapport consolide les tests historiques et prospectifs executes par question, avec separation explicite des statuts PASS/WARN/FAIL/NON_TESTABLE et comparaison historique vs scenario.

## Q1
Analyse complete Q1: historique + prospectif en un seul run. Statut global=WARN. Tests PASS=7, WARN=0, FAIL=0, NON_TESTABLE=0. Les resultats sont separes entre historique et scenarios, puis compares dans une table unique.

### Tests executes
```text
test_id mode scenario_id status                       value                 threshold                                         interpretation          source_ref
Q1-H-01 HIST         NaN   PASS           4.142857142857143             score present            Le score de bascule marche est exploitable. SPEC2-Q1/Slides 2-4
Q1-H-02 HIST         NaN   PASS far_energy,ir_p10,sr_energy        SR/FAR/IR presents                     Le stress physique est calculable. SPEC2-Q1/Slides 3-4
Q1-H-03 HIST         NaN   PASS                     100.00%                     >=50% Concordance mesuree entre bascules marche et physique.            SPEC2-Q1
Q1-H-04 HIST         NaN   PASS                       0.700 confidence moyenne >=0.60          Proxy de robustesse du diagnostic de bascule.          Slides 4-6
Q1-S-01 SCEN        BASE   PASS                           1                 >0 lignes                      La bascule projetee est produite.   SPEC2-Q1/Slides 5
Q1-S-02 SCEN        BASE   PASS                           1               >=1 bascule         Le scenario fournit une variation exploitable.   SPEC2-Q1/Slides 5
Q1-S-03 SCEN        BASE   PASS                     100.00%       >=50% lignes >=0.55                     La coherence scenario est lisible.            SPEC2-Q1
```

### Comparaison historique vs prospectif
```text
country scenario_id              metric  hist_value  scen_value  delta
     FR        BASE bascule_year_market      2018.0      2030.0   12.0
```

## Q2
Analyse complete Q2: historique + prospectif en un seul run. Statut global=WARN. Tests PASS=4, WARN=1, FAIL=0, NON_TESTABLE=0. Les resultats sont separes entre historique et scenarios, puis compares dans une table unique.

### Tests executes
```text
test_id mode scenario_id status        value                threshold                                interpretation            source_ref
Q2-H-01 HIST         NaN   PASS            2                >0 lignes        Les pentes historiques sont calculees.    SPEC2-Q2/Slides 10
Q2-H-02 HIST         NaN   PASS n,p_value,r2 r2,p_value,n disponibles        La robustesse statistique est lisible. SPEC2-Q2/Slides 10-12
Q2-H-03 HIST         NaN   PASS            6                >0 lignes        Les drivers de pente sont disponibles.          Slides 10-13
Q2-S-01 SCEN        BASE   PASS            2                >0 lignes                Pentes prospectives calculees.    SPEC2-Q2/Slides 11
Q2-S-02 SCEN        BASE   WARN        0.00%           >=30% robustes Delta de pente interpretable avec robustesse.              SPEC2-Q2
```

### Comparaison historique vs prospectif
```text
country tech scenario_id metric  hist_value  scen_value  delta
     FR   PV        BASE  slope   -5.463838         NaN    NaN
     FR WIND        BASE  slope   -2.651290         NaN    NaN
```

## Q3
Analyse complete Q3: historique + prospectif en un seul run. Statut global=WARN. Tests PASS=4, WARN=0, FAIL=0, NON_TESTABLE=0. Les resultats sont separes entre historique et scenarios, puis compares dans une table unique.

### Tests executes
```text
test_id mode scenario_id status  value                    threshold                                      interpretation         source_ref
Q3-H-01 HIST         NaN   PASS      1                    >0 lignes           Les tendances historiques sont calculees. SPEC2-Q3/Slides 16
Q3-H-02 HIST         NaN   PASS      1               status valides               Les statuts business sont renseignes.           SPEC2-Q3
Q3-S-01 SCEN        BASE   PASS      1 colonnes inversion presentes Les ordres de grandeur d'inversion sont quantifies. SPEC2-Q3/Slides 17
Q3-S-02 SCEN        BASE   PASS      1            status renseignes      La lecture de transition phase 3 est possible.       Slides 17-19
```

### Comparaison historique vs prospectif
```text
country scenario_id              metric  hist_value  scen_value     delta
     FR        BASE  inversion_k_demand    0.278613         0.0 -0.278613
     FR        BASE inversion_r_mustrun    0.246765         0.0 -0.246765
```

## Q4
Analyse complete Q4: historique + prospectif en un seul run. Statut global=PASS. Tests PASS=4, WARN=0, FAIL=0, NON_TESTABLE=0. Les resultats sont separes entre historique et scenarios, puis compares dans une table unique.

### Tests executes
```text
test_id mode scenario_id status                                         value            threshold                                    interpretation         source_ref
Q4-H-01 HIST         NaN   PASS HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED     3 modes executes              Les trois modes Q4 sont disponibles. SPEC2-Q4/Slides 22
Q4-H-02 HIST         NaN   PASS                                          PASS          pas de FAIL Les invariants physiques batterie sont respectes.           SPEC2-Q4
Q4-S-01 SCEN        BASE   PASS                                             1            >0 lignes             Resultats Q4 prospectifs disponibles. SPEC2-Q4/Slides 23
Q4-S-02 SCEN        BASE   PASS                            1318.7589939342624 capture apres finite                   Sensibilite valeur exploitable.       Slides 23-25
```

### Comparaison historique vs prospectif
```text
country                 scenario_id                     metric  hist_value  scen_value       delta
     FR                        BASE                  far_after    0.811900         NaN         NaN
     FR                        BASE surplus_unabs_energy_after   11.469399    0.000000  -11.469399
     FR                        BASE     pv_capture_price_after   39.247962 1318.758994 1279.511032
     FR HIST_PRICE_ARBITRAGE_SIMPLE                  far_after    0.811900    0.808498   -0.003403
     FR           HIST_PV_COLOCATED                  far_after    0.811900    0.800555   -0.011345
```

## Q5
Analyse complete Q5: historique + prospectif en un seul run. Statut global=WARN. Tests PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Les resultats sont separes entre historique et scenarios, puis compares dans une table unique.

### Tests executes
```text
test_id mode scenario_id status                                             value     threshold                       interpretation         source_ref
Q5-H-01 HIST         NaN   PASS                ttl=419.95, tca=370.83959999999996 ttl/tca finis  L'ancre thermique est quantifiable. SPEC2-Q5/Slides 28
Q5-H-02 HIST         NaN   PASS dCO2=0.36727272727272725, dGas=1.8181818181818181            >0 Sensibilites analytiques coherentes.           SPEC2-Q5
Q5-S-01 SCEN        BASE   PASS                                                 1     >0 lignes     Sensibilites scenario calculees. SPEC2-Q5/Slides 29
Q5-S-01 SCEN    HIGH_CO2   PASS                                                 1     >0 lignes     Sensibilites scenario calculees. SPEC2-Q5/Slides 29
Q5-S-01 SCEN    HIGH_GAS   PASS                                                 1     >0 lignes     Sensibilites scenario calculees. SPEC2-Q5/Slides 29
Q5-S-01 SCEN   HIGH_BOTH   PASS                                                 1     >0 lignes     Sensibilites scenario calculees. SPEC2-Q5/Slides 29
Q5-S-02 SCEN        BASE   PASS                               -10168.862806747053  valeur finie            CO2 requis interpretable. SPEC2-Q5/Slides 31
Q5-S-02 SCEN    HIGH_CO2   PASS                               -10177.062869892936  valeur finie            CO2 requis interpretable. SPEC2-Q5/Slides 31
Q5-S-02 SCEN    HIGH_GAS   PASS                               -10308.637127318678  valeur finie            CO2 requis interpretable. SPEC2-Q5/Slides 31
Q5-S-02 SCEN   HIGH_BOTH   PASS                               -10113.862806747053  valeur finie            CO2 requis interpretable. SPEC2-Q5/Slides 31
```

### Comparaison historique vs prospectif
```text
country scenario_id            metric  hist_value    scen_value        delta
     FR        BASE           ttl_obs  419.950000   3895.145976  3475.195976
     FR        BASE           tca_q95  370.839600    130.672727  -240.166873
     FR        BASE co2_required_base -749.805545 -10168.862807 -9419.057262
     FR    HIGH_CO2           ttl_obs  419.950000   3918.357636  3498.407636
     FR    HIGH_CO2           tca_q95  370.839600    150.872727  -219.966873
     FR    HIGH_CO2 co2_required_base -749.805545 -10177.062870 -9427.257325
     FR    HIGH_GAS           ttl_obs  419.950000   3946.481272  3526.531272
     FR    HIGH_GAS           tca_q95  370.839600    174.309091  -196.530509
     FR    HIGH_GAS co2_required_base -749.805545 -10308.637127 -9558.831583
     FR   HIGH_BOTH           ttl_obs  419.950000   3895.145976  3475.195976
     FR   HIGH_BOTH           tca_q95  370.839600    194.509091  -176.330509
     FR   HIGH_BOTH co2_required_base -749.805545 -10113.862807 -9364.057262
```

## Synthese finale
Les conclusions doivent etre lues avec les limits explicites de chaque question. Chaque assertion est tracee a un test_id et une source_ref (SPEC/Slides).