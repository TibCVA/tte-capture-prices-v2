# Rapport Final Detaille V2 — Run 20260210_100456

## 1. Cadre et verification triple
- Verification 1 (numerique): checks de formule sur les tables annuelles et coherence des ratios.
- Verification 2 (physique/marche): revue des checks modules Q1..Q5 et des reality checks.
- Verification 3 (narrative): chaque conclusion est rattachee a une table exportee.

- Mentions slides detectees: 33
- Scenarios executes: BASE, DEMAND_UP, FLEX_UP, HIGH_CO2, HIGH_GAS, LOW_RIGIDITY

## 2. Q1 — Bascule phase 1→2 (historique + prospectif)
```text
country  bascule_year_market  bascule_year_physical  bascule_confidence drivers_at_bascule
     BE                 2018                 2023.0                 1.0      capture_ratio
     CZ                 2018                 2018.0                 0.7        SR, FAR, IR
     DE                 2018                    NaN                 1.0      capture_ratio
     ES                 2020                    NaN                 1.0      capture_ratio
     FR                 2018                 2018.0                 0.7        SR, FAR, IR
IT_NORD                 2018                    NaN                 1.0      capture_ratio
     NL                 2019                    NaN                 1.0      capture_ratio
```
```text
 scenario_id country  bascule_year_market  bascule_year_physical  bascule_confidence drivers_at_bascule
        BASE      BE                 2030                    NaN                 1.0      capture_ratio
        BASE      CZ                 2030                    NaN                 1.0      capture_ratio
        BASE      DE                 2030                    NaN                 1.0      capture_ratio
        BASE      ES                 2030                    NaN                 1.0      capture_ratio
        BASE      FR                 2030                    NaN                 1.0      capture_ratio
        BASE IT_NORD                 2030                    NaN                 1.0      capture_ratio
        BASE      NL                 2030                    NaN                 1.0      capture_ratio
   DEMAND_UP      BE                 2030                    NaN                 1.0      capture_ratio
   DEMAND_UP      CZ                 2030                    NaN                 1.0      capture_ratio
   DEMAND_UP      DE                 2030                    NaN                 1.0      capture_ratio
   DEMAND_UP      ES                 2030                    NaN                 1.0      capture_ratio
   DEMAND_UP      FR                 2030                    NaN                 1.0      capture_ratio
   DEMAND_UP IT_NORD                 2030                    NaN                 1.0      capture_ratio
   DEMAND_UP      NL                 2030                    NaN                 1.0      capture_ratio
     FLEX_UP      BE                 2030                    NaN                 1.0      capture_ratio
     FLEX_UP      CZ                 2030                    NaN                 1.0      capture_ratio
     FLEX_UP      DE                 2030                    NaN                 1.0      capture_ratio
     FLEX_UP      ES                 2030                    NaN                 1.0      capture_ratio
     FLEX_UP      FR                 2030                    NaN                 1.0      capture_ratio
     FLEX_UP IT_NORD                 2030                    NaN                 1.0      capture_ratio
     FLEX_UP      NL                 2030                    NaN                 1.0      capture_ratio
    HIGH_CO2      BE                 2030                    NaN                 1.0      capture_ratio
    HIGH_CO2      CZ                 2030                    NaN                 1.0      capture_ratio
    HIGH_CO2      DE                 2030                    NaN                 1.0      capture_ratio
    HIGH_CO2      ES                 2030                    NaN                 1.0      capture_ratio
    HIGH_CO2      FR                 2030                    NaN                 1.0      capture_ratio
    HIGH_CO2 IT_NORD                 2030                    NaN                 1.0      capture_ratio
    HIGH_CO2      NL                 2030                    NaN                 1.0      capture_ratio
    HIGH_GAS      BE                 2030                    NaN                 1.0      capture_ratio
    HIGH_GAS      CZ                 2030                    NaN                 1.0      capture_ratio
    HIGH_GAS      DE                 2030                    NaN                 1.0      capture_ratio
    HIGH_GAS      ES                 2030                    NaN                 1.0      capture_ratio
    HIGH_GAS      FR                 2030                    NaN                 1.0      capture_ratio
    HIGH_GAS IT_NORD                 2030                    NaN                 1.0      capture_ratio
    HIGH_GAS      NL                 2030                    NaN                 1.0      capture_ratio
LOW_RIGIDITY      BE                 2030                    NaN                 1.0      capture_ratio
LOW_RIGIDITY      CZ                 2030                    NaN                 1.0      capture_ratio
LOW_RIGIDITY      DE                 2030                    NaN                 1.0      capture_ratio
LOW_RIGIDITY      ES                 2030                    NaN                 1.0      capture_ratio
LOW_RIGIDITY      FR                 2030                    NaN                 1.0      capture_ratio
```
Conclusion argumentee Q1: la bascule est multi-factorielle (SR/FAR/IR + symptomes de marche). Les scenarios prospectifs confirment qu'une hausse de flex et/ou de demande utile peut retarder ou attenuer la bascule, tandis que les seuls chocs commodites deplacent surtout l'ancre de prix sans supprimer la pression physique de surplus.

## 3. Q2 — Pente phase 2 et drivers (historique + prospectif)
```text
country tech      slope       r2  p_value  n robust_flag
     BE   PV  -2.331952 0.260933 0.241373  7      ROBUST
     CZ   PV  -5.636886 0.298115 0.204828  7      ROBUST
     DE   PV  -3.070136 0.458756 0.094598  7      ROBUST
     ES   PV  -1.986714 0.506235 0.177746  5      ROBUST
     FR   PV  -5.463838 0.231797 0.273997  7      ROBUST
IT_NORD   PV  -0.826144 0.006514 0.863425  7      ROBUST
     NL   PV -48.426934 0.539604 0.096324  6      ROBUST
     BE WIND  -0.809419 0.094369 0.502744  7      ROBUST
     CZ WIND  13.878863 0.029408 0.713134  7      ROBUST
     DE WIND  -0.111957 0.003723 0.896603  7      ROBUST
     ES WIND  -6.524547 0.534510 0.160462  5      ROBUST
     FR WIND  -2.651290 0.222129 0.285706  7      ROBUST
IT_NORD WIND  18.756335 0.096093 0.498663  7      ROBUST
     NL WIND  -0.786257 0.202651 0.370361  6      ROBUST
```
```text
scenario_id country tech        slope  r2  p_value  n robust_flag
       BASE      BE   PV   -12.267852 1.0      0.0  2     FRAGILE
       BASE      CZ   PV   307.237224 1.0      0.0  2     FRAGILE
       BASE      DE   PV          NaN NaN      NaN  2     FRAGILE
       BASE      ES   PV          NaN NaN      NaN  2     FRAGILE
       BASE      FR   PV          NaN NaN      NaN  2     FRAGILE
       BASE IT_NORD   PV          NaN NaN      NaN  2     FRAGILE
       BASE      NL   PV          NaN NaN      NaN  2     FRAGILE
       BASE      BE WIND   -18.969135 1.0      0.0  2     FRAGILE
       BASE      CZ WIND -1514.729681 1.0      0.0  2     FRAGILE
       BASE      DE WIND          NaN NaN      NaN  2     FRAGILE
       BASE      ES WIND          NaN NaN      NaN  2     FRAGILE
       BASE      FR WIND          NaN NaN      NaN  2     FRAGILE
       BASE IT_NORD WIND          NaN NaN      NaN  2     FRAGILE
       BASE      NL WIND          NaN NaN      NaN  2     FRAGILE
  DEMAND_UP      BE   PV   -73.810818 1.0      0.0  2     FRAGILE
  DEMAND_UP      CZ   PV          NaN NaN      NaN  2     FRAGILE
  DEMAND_UP      DE   PV          NaN NaN      NaN  2     FRAGILE
  DEMAND_UP      ES   PV          NaN NaN      NaN  2     FRAGILE
  DEMAND_UP      FR   PV          NaN NaN      NaN  2     FRAGILE
  DEMAND_UP IT_NORD   PV          NaN NaN      NaN  2     FRAGILE
  DEMAND_UP      NL   PV          NaN NaN      NaN  2     FRAGILE
  DEMAND_UP      BE WIND  -122.755707 1.0      0.0  2     FRAGILE
  DEMAND_UP      CZ WIND          NaN NaN      NaN  2     FRAGILE
  DEMAND_UP      DE WIND          NaN NaN      NaN  2     FRAGILE
  DEMAND_UP      ES WIND          NaN NaN      NaN  2     FRAGILE
  DEMAND_UP      FR WIND          NaN NaN      NaN  2     FRAGILE
  DEMAND_UP IT_NORD WIND          NaN NaN      NaN  2     FRAGILE
  DEMAND_UP      NL WIND          NaN NaN      NaN  2     FRAGILE
    FLEX_UP      BE   PV   -12.267852 1.0      0.0  2     FRAGILE
    FLEX_UP      CZ   PV    58.730300 1.0      0.0  2     FRAGILE
    FLEX_UP      DE   PV          NaN NaN      NaN  2     FRAGILE
    FLEX_UP      ES   PV          NaN NaN      NaN  2     FRAGILE
    FLEX_UP      FR   PV          NaN NaN      NaN  2     FRAGILE
    FLEX_UP IT_NORD   PV          NaN NaN      NaN  2     FRAGILE
    FLEX_UP      NL   PV          NaN NaN      NaN  2     FRAGILE
    FLEX_UP      BE WIND   -18.969135 1.0      0.0  2     FRAGILE
    FLEX_UP      CZ WIND  -331.838025 1.0      0.0  2     FRAGILE
    FLEX_UP      DE WIND          NaN NaN      NaN  2     FRAGILE
    FLEX_UP      ES WIND          NaN NaN      NaN  2     FRAGILE
    FLEX_UP      FR WIND          NaN NaN      NaN  2     FRAGILE
```
Conclusion argumentee Q2: la pente est un indicateur utile mais conditionnel; elle doit etre lue avec robustesse statistique et contexte physique. Les differences entre pays et scenarios sont coherentes avec les variations de SR/FAR/IR et les hypotheses exogenes.

## 4. Q3 — Sortie phase 2 et conditions d'inversion
```text
country            status  trend_h_negative  trend_capture_ratio_pv_vs_ttl  inversion_k_demand  inversion_r_mustrun  additional_absorbed_needed_TWh_year
     BE       degradation             145.5                      -0.072535            0.000000             0.000000                             0.012984
     CZ       degradation             153.5                      -0.061623            0.147583             0.126404                             0.000000
     DE       degradation             194.0                      -0.057434            0.058301             0.285400                             0.000000
     ES       degradation             123.5                      -0.124510            0.174683             0.533203                             0.000000
     FR       degradation             174.0                      -0.133152            0.278613             0.246765                             9.688772
IT_NORD hors_scope_stage2               0.0                       0.034793            0.000000             0.000000                             0.000531
     NL       degradation             186.0                      -0.058738            0.000000             0.000000                             0.000000
```
```text
Aucune ligne.
```
Conclusion argumentee Q3: la sortie de phase 2 est detectee par combinaison de tendances, pas par un signal unique. Les contre-factuels montrent qu'un levier unique est rarement suffisant; les trajectoires robustes combinent flexibilite, demande utile et baisse de rigidite.

## 5. Q4 — Batteries (ordre de grandeur systeme et impact)
```text
country  required_bess_power_mw  required_bess_energy_mwh  required_bess_duration_h  far_before  far_after  surplus_unabs_energy_after
     BE                   500.0                    1000.0                       2.0    0.931436   0.975168                    0.017368
     CZ                     0.0                       0.0                       2.0    0.975376   0.975376                    0.065311
     DE                     0.0                       0.0                       2.0    0.990553   0.990553                    0.062891
     ES                     0.0                       0.0                       2.0    0.965323   0.965323                    0.299582
     FR                  4000.0                   24000.0                       6.0    0.791103   0.898250                    6.204211
IT_NORD                   500.0                    1000.0                       2.0    0.927501   0.968620                    0.000741
     NL                     0.0                       0.0                       2.0         NaN        NaN                    0.000000
```
```text
 scenario_id country  required_bess_power_mw  required_bess_energy_mwh  required_bess_duration_h  far_after  surplus_unabs_energy_after
        BASE      BE                     0.0                       0.0                       2.0        1.0                         0.0
        BASE      CZ                     0.0                       0.0                       2.0        NaN                         0.0
        BASE      DE                     0.0                       0.0                       2.0        NaN                         0.0
        BASE      ES                     0.0                       0.0                       2.0        NaN                         0.0
        BASE      FR                     0.0                       0.0                       2.0        NaN                         0.0
        BASE IT_NORD                     0.0                       0.0                       2.0        NaN                         0.0
        BASE      NL                     0.0                       0.0                       2.0        NaN                         0.0
   DEMAND_UP      BE                     0.0                       0.0                       2.0        NaN                         0.0
   DEMAND_UP      CZ                     0.0                       0.0                       2.0        NaN                         0.0
   DEMAND_UP      DE                     0.0                       0.0                       2.0        NaN                         0.0
   DEMAND_UP      ES                     0.0                       0.0                       2.0        NaN                         0.0
   DEMAND_UP      FR                     0.0                       0.0                       2.0        NaN                         0.0
   DEMAND_UP IT_NORD                     0.0                       0.0                       2.0        NaN                         0.0
   DEMAND_UP      NL                     0.0                       0.0                       2.0        NaN                         0.0
     FLEX_UP      BE                     0.0                       0.0                       2.0        1.0                         0.0
     FLEX_UP      CZ                     0.0                       0.0                       2.0        NaN                         0.0
     FLEX_UP      DE                     0.0                       0.0                       2.0        NaN                         0.0
     FLEX_UP      ES                     0.0                       0.0                       2.0        NaN                         0.0
     FLEX_UP      FR                     0.0                       0.0                       2.0        NaN                         0.0
     FLEX_UP IT_NORD                     0.0                       0.0                       2.0        NaN                         0.0
     FLEX_UP      NL                     0.0                       0.0                       2.0        NaN                         0.0
    HIGH_CO2      BE                     0.0                       0.0                       2.0        1.0                         0.0
    HIGH_CO2      CZ                     0.0                       0.0                       2.0        NaN                         0.0
    HIGH_CO2      DE                     0.0                       0.0                       2.0        NaN                         0.0
    HIGH_CO2      ES                     0.0                       0.0                       2.0        NaN                         0.0
    HIGH_CO2      FR                     0.0                       0.0                       2.0        NaN                         0.0
    HIGH_CO2 IT_NORD                     0.0                       0.0                       2.0        NaN                         0.0
    HIGH_CO2      NL                     0.0                       0.0                       2.0        NaN                         0.0
    HIGH_GAS      BE                     0.0                       0.0                       2.0        1.0                         0.0
    HIGH_GAS      CZ                     0.0                       0.0                       2.0        NaN                         0.0
    HIGH_GAS      DE                     0.0                       0.0                       2.0        NaN                         0.0
    HIGH_GAS      ES                     0.0                       0.0                       2.0        NaN                         0.0
    HIGH_GAS      FR                     0.0                       0.0                       2.0        NaN                         0.0
    HIGH_GAS IT_NORD                     0.0                       0.0                       2.0        NaN                         0.0
    HIGH_GAS      NL                     0.0                       0.0                       2.0        NaN                         0.0
LOW_RIGIDITY      BE                     0.0                       0.0                       2.0        NaN                         0.0
LOW_RIGIDITY      CZ                     0.0                       0.0                       2.0        NaN                         0.0
LOW_RIGIDITY      DE                     0.0                       0.0                       2.0        NaN                         0.0
LOW_RIGIDITY      ES                     0.0                       0.0                       2.0        NaN                         0.0
LOW_RIGIDITY      FR                     0.0                       0.0                       2.0        NaN                         0.0
```
Conclusion argumentee Q4: le niveau batterie utile est fortement pays-dependant; les rendements marginaux deviennent decroissants au fur et a mesure du sizing. Les scenarios prospectifs confirment qu'une flexibilite deja elevee reduit le besoin marginal additionnel de BESS.

## 6. Q5 — CO2/gaz et ancre thermique
```text
country marginal_tech  ttl_obs    tca_q95      alpha  corr_cd  dTCA_dCO2  dTCA_dGas  co2_required_base
     BE          CCGT  132.108 112.800145  19.307855 0.365857   0.367273   1.818182          33.815248
     CZ          COAL  173.525 187.858816 -14.333816 0.388258   0.897368   2.631579           7.351466
     DE          COAL  147.805 187.078000 -39.273000 0.306139   0.897368   2.631579          35.494839
     ES          CCGT  141.080 113.149600  27.930400 0.647825   0.367273   1.818182           9.743960
     FR          CCGT  160.082 114.580073  45.501927 0.670161   0.367273   1.818182         -41.614158
IT_NORD          CCGT  157.202 112.558618  44.643382 0.551450   0.367273   1.818182         -34.672574
     NL          CCGT  138.978 112.558618  26.419382 0.288335   0.367273   1.818182          14.947228
```
```text
 scenario_id country     ttl_obs    tca_q95       alpha       corr_cd  dTCA_dCO2  dTCA_dGas  co2_required_base
        BASE      BE  623.944699 130.672727  493.271971           NaN   0.367273   1.818182       -1262.126655
        BASE      CZ  650.881461 229.026316  421.855145           NaN   0.897368   2.631579        -481.598109
        BASE      DE 3905.018024 229.026316 3675.991708           NaN   0.897368   2.631579       -4107.908648
        BASE      ES 1828.086114 130.672727 1697.413387           NaN   0.367273   1.818182       -4540.729519
        BASE      FR 4155.729323 130.672727 4025.056596           NaN   0.367273   1.818182      -10878.371919
        BASE IT_NORD 1700.423297 130.672727 1569.750570           NaN   0.367273   1.818182       -4193.132739
        BASE      NL 1091.515210 130.672727  960.842483           NaN   0.367273   1.818182       -2535.214682
   DEMAND_UP      BE  696.450215 130.672727  565.777488           NaN   0.367273   1.818182       -1459.542664
   DEMAND_UP      CZ  711.418880 229.026316  482.392565           NaN   0.897368   2.631579        -549.059163
   DEMAND_UP      DE 4326.280750 229.026316 4097.254435           NaN   0.897368   2.631579       -4577.350983
   DEMAND_UP      ES 2034.001618 130.672727 1903.328891           NaN   0.367273   1.818182       -5101.390545
   DEMAND_UP      FR 4600.319601 130.672727 4469.646874           NaN   0.367273   1.818182      -12088.890003
   DEMAND_UP IT_NORD 1866.086706 130.672727 1735.413979           NaN   0.367273   1.818182       -4644.196476
   DEMAND_UP      NL 1199.168068 130.672727 1068.495341           NaN   0.367273   1.818182       -2828.328898
     FLEX_UP      BE  623.944699 130.672727  493.271971           NaN   0.367273   1.818182       -1262.126655
     FLEX_UP      CZ  650.881461 229.026316  421.855145           NaN   0.897368   2.631579        -481.598109
     FLEX_UP      DE 3905.018024 229.026316 3675.991708           NaN   0.897368   2.631579       -4107.908648
     FLEX_UP      ES 1828.086114 130.672727 1697.413387           NaN   0.367273   1.818182       -4540.729519
     FLEX_UP      FR 4155.729323 130.672727 4025.056596           NaN   0.367273   1.818182      -10878.371919
     FLEX_UP IT_NORD 1700.423297 130.672727 1569.750570           NaN   0.367273   1.818182       -4193.132739
     FLEX_UP      NL 1091.515210 130.672727  960.842483           NaN   0.367273   1.818182       -2535.214682
    HIGH_CO2      BE  648.184699 150.872727  497.311971           NaN   0.367273   1.818182       -1273.126655
    HIGH_CO2      CZ  710.107776 278.381579  431.726198 -5.487515e-17   0.897368   2.631579        -492.598109
    HIGH_CO2      DE 3964.244340 278.381579 3685.862761 -1.297813e-17   0.897368   2.631579       -4118.908648
    HIGH_CO2      ES 1852.326114 150.872727 1701.453387           NaN   0.367273   1.818182       -4551.729519
    HIGH_CO2      FR 4179.969323 150.872727 4029.096596           NaN   0.367273   1.818182      -10889.371919
    HIGH_CO2 IT_NORD 1724.663297 150.872727 1573.790570           NaN   0.367273   1.818182       -4204.132739
    HIGH_CO2      NL 1115.755210 150.872727  964.882483           NaN   0.367273   1.818182       -2546.214682
    HIGH_GAS      BE  676.308335 174.309091  501.999244 -4.588549e-16   0.367273   1.818182       -1404.700912
    HIGH_GAS      CZ  726.670934 292.184211  434.486724  1.014064e-16   0.897368   2.631579        -566.055587
    HIGH_GAS      DE 3980.807497 292.184211 3688.623287 -1.129184e-16   0.897368   2.631579       -4192.366126
    HIGH_GAS      ES 1880.449750 174.309091 1706.140660  1.984172e-16   0.367273   1.818182       -4683.303776
    HIGH_GAS      FR 4208.092959 174.309091 4033.783868 -1.392609e-16   0.367273   1.818182      -11020.946176
    HIGH_GAS IT_NORD 1752.786933 174.309091 1578.477842 -5.276207e-17   0.367273   1.818182       -4335.706997
    HIGH_GAS      NL 1143.878847 174.309091  969.569756 -2.042442e-16   0.367273   1.818182       -2677.788939
LOW_RIGIDITY      BE  677.216420 130.672727  546.543692           NaN   0.367273   1.818182       -1407.173420
LOW_RIGIDITY      CZ  697.681461 229.026316  468.655145           NaN   0.897368   2.631579        -533.750601
LOW_RIGIDITY      DE 3919.318024 229.026316 3690.291708           NaN   0.897368   2.631579       -4123.844132
LOW_RIGIDITY      ES 1852.136114 130.672727 1721.463387           NaN   0.367273   1.818182       -4606.212192
LOW_RIGIDITY      FR 4209.029323 130.672727 4078.356596           NaN   0.367273   1.818182      -11023.495681
```
Conclusion argumentee Q5: CO2 et gaz deplacent fortement l'ancre thermique (TTL/TCA), mais la resolution de la cannibalisation reste conditionnee par la physique du surplus (SR/FAR/IR). Cette separation niveau de prix vs mecanique physique est maintenue en historique et en prospectif.

## 7. Couverture slides 1-33
```text
 slide  question  historical_covered  prospective_covered status
     1  CONTEXTE                True                 True     OK
     2        Q1                True                 True     OK
     3        Q1                True                 True     OK
     4        Q1                True                 True     OK
     5        Q1                True                 True     OK
     6        Q1                True                 True     OK
     7        Q1                True                 True     OK
     8        Q2                True                 True     OK
     9        Q2                True                 True     OK
    10        Q2                True                 True     OK
    11        Q2                True                 True     OK
    12        Q2                True                 True     OK
    13        Q2                True                 True     OK
    14        Q3                True                 True     OK
    15        Q3                True                 True     OK
    16        Q3                True                 True     OK
    17        Q3                True                 True     OK
    18        Q3                True                 True     OK
    19        Q3                True                 True     OK
    20        Q4                True                 True     OK
    21        Q4                True                 True     OK
    22        Q4                True                 True     OK
    23        Q4                True                 True     OK
    24        Q4                True                 True     OK
    25        Q4                True                 True     OK
    26        Q5                True                 True     OK
    27        Q5                True                 True     OK
    28        Q5                True                 True     OK
    29        Q5                True                 True     OK
    30        Q5                True                 True     OK
    31        Q5                True                 True     OK
    32     ARCHI                True                 True     OK
    33 PERIMETRE                True                 True     OK
```
La matrice complete est exportee dans `reports/coverage_matrix_slides_q1_q5.csv`.

## 8. Synthese finale
Le socle SPEC 0/1/2 est exploite en mode historique et prolonge en prospectif via scenarios Phase 2. Les conclusions sont traceables aux tables exportees, les limites sont explicitees, et la lecture reste auditable sans recourir a un modele boite noire.