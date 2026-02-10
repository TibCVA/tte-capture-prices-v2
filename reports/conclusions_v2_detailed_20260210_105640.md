# Rapport Final Detaille V2 - Run 20260210_105640

Source principale: `outputs\combined\Q1_BOOT_20260210_105623`
Generation combine-first: ce rapport lit d'abord les outputs unifies Q1..Q5.

## Resume executif
Le rapport consolide les tests historiques et prospectifs executes par question, avec separation explicite des statuts PASS/WARN/FAIL/NON_TESTABLE et comparaison historique vs scenario.

## Q1
Analyse complete Q1: historique + prospectif en un seul run. Statut global=WARN. Tests PASS=7, WARN=0, FAIL=0, NON_TESTABLE=0. Les resultats sont separes entre historique et scenarios, puis compares dans une table unique.

### Tests executes
```text
test_id mode scenario_id status                       value                 threshold                                         interpretation          source_ref
Q1-H-01 HIST         NaN   PASS           4.642857142857143             score present            Le score de bascule marche est exploitable. SPEC2-Q1/Slides 2-4
Q1-H-02 HIST         NaN   PASS far_energy,ir_p10,sr_energy        SR/FAR/IR presents                     Le stress physique est calculable. SPEC2-Q1/Slides 3-4
Q1-H-03 HIST         NaN   PASS                      50.00%                     >=50% Concordance mesuree entre bascules marche et physique.            SPEC2-Q1
Q1-H-04 HIST         NaN   PASS                       0.850 confidence moyenne >=0.60          Proxy de robustesse du diagnostic de bascule.          Slides 4-6
Q1-S-01 SCEN        BASE   PASS                           2                 >0 lignes                      La bascule projetee est produite.   SPEC2-Q1/Slides 5
Q1-S-02 SCEN        BASE   PASS                           2               >=1 bascule         Le scenario fournit une variation exploitable.   SPEC2-Q1/Slides 5
Q1-S-03 SCEN        BASE   PASS                     100.00%       >=50% lignes >=0.55                     La coherence scenario est lisible.            SPEC2-Q1
```

### Comparaison historique vs prospectif
```text
country scenario_id              metric  hist_value  scen_value  delta
     DE        BASE bascule_year_market      2018.0      2030.0   12.0
     FR        BASE bascule_year_market      2018.0      2030.0   12.0
```

## Q2
Aucun resultat combine disponible.

## Q3
Aucun resultat combine disponible.

## Q4
Aucun resultat combine disponible.

## Q5
Aucun resultat combine disponible.

## Synthese finale
Les conclusions doivent etre lues avec les limits explicites de chaque question. Chaque assertion est tracee a un test_id et une source_ref (SPEC/Slides).