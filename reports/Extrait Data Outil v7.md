# Extrait Data Outil v7

## AUDIT PAYLOAD

### Inputs

#### run_metadata
```json
{
  "run_id": "FULL_20260213_FIX14_DE_ES",
  "run_dir": "C:\\Users\\cval-tlacour\\OneDrive - CVA corporate value associate GmbH\\Desktop\\automation-stack\\projects\\tte-capture-prices-v2\\outputs\\combined\\FULL_20260213_FIX14_DE_ES",
  "countries": [
    "DE",
    "ES"
  ],
  "hist_years": [
    2018,
    2019,
    2020,
    2021,
    2022,
    2023,
    2024
  ],
  "scenario_years": [
    2025,
    2026,
    2027,
    2028,
    2029,
    2030,
    2031,
    2032,
    2033,
    2034,
    2035
  ],
  "scenarios": [
    "BASE",
    "DEMAND_UP",
    "LOW_RIGIDITY"
  ],
  "method_reference": "AUDIT_METHODS_Q1_Q5.md"
}
```

#### Method Reference
```text
C:\Users\cval-tlacour\OneDrive - CVA corporate value associate GmbH\Desktop\automation-stack\projects\tte-capture-prices-v2\AUDIT_METHODS_Q1_Q5.md
```

#### parameter_catalog
```csv
param_group,param_name,param_value,unit,description,source,last_updated,owner
PHASE_THRESHOLDS,capture_ratio_pv_vs_ttl_crisis_max,0.7,ratio,Seuil crise capture ratio pv/ttl,default,2026-02-09,system
PHASE_THRESHOLDS,capture_ratio_pv_vs_ttl_stage2_max,0.8,ratio,Seuil capture ratio pv/ttl,default,2026-02-09,system
PHASE_THRESHOLDS,capture_ratio_pv_stage2_max,0.8,ratio,Seuil capture ratio PV vs baseload en declenchement phase2,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,capture_ratio_wind_stage2_max,0.9,ratio,Seuil capture ratio Wind vs baseload en declenchement phase2,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,days_spread_gt50_stage2_min,150.0,days,Seuil jours spread>50,default,2026-02-09,system
PHASE_THRESHOLDS,avg_daily_spread_crisis_min,50.0,EUR/MWh,Seuil spread journalier moyen pour tagger une annee de crise,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,h_below_5_stage2_min,500.0,hours,Seuil heures basses,default,2026-02-09,system
PHASE_THRESHOLDS,h_negative_stage2_min,200.0,hours,Seuil heures negatives stage2,default,2026-02-09,system
PHASE_THRESHOLDS,h_negative_stage2_strong,300.0,hours,Seuil fort heures negatives,default,2026-02-09,system
PHASE_THRESHOLDS,stage1_capture_ratio_pv_vs_ttl_min,0.9,ratio,Stage1 min capture ratio pv vs ttl,default,2026-02-10,system
PHASE_THRESHOLDS,stage1_capture_ratio_pv_min,0.85,ratio,Stage1 min capture ratio PV vs baseload,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,stage1_capture_ratio_wind_min,0.9,ratio,Stage1 min capture ratio Wind vs baseload,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,stage1_days_spread_gt50_max,120.0,days,Stage1 max days spread gt50,default,2026-02-10,system
PHASE_THRESHOLDS,stage1_h_below_5_max,500.0,hours,Stage1 max hours below 5 (doit rester sous seuil stage2),spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,stage1_h_negative_max,200.0,hours,Stage1 max negative hours (doit rester sous seuil stage2),spec_alignment,2026-02-11,codex
PHYSICS_THRESHOLDS,far_energy_tension_max,0.95,ratio,Seuil far tension,default,2026-02-09,system
PHYSICS_THRESHOLDS,far_stage2_min,0.95,ratio,Seuil FAR minimal pour eviter stress physique stage2,spec_alignment,2026-02-11,codex
PHYSICS_THRESHOLDS,ir_p10_high_min,1.5,ratio,Seuil inflexibilite haute stage2,spec_alignment,2026-02-11,codex
PHYSICS_THRESHOLDS,ir_p10_stage2_min,1.5,ratio,Alias seuil inflexibilite haute stage2,spec_alignment,2026-02-11,codex
PHYSICS_THRESHOLDS,sr_energy_material_min,0.01,ratio,Seuil surplus ratio materialite,default,2026-02-09,system
PHYSICS_THRESHOLDS,sr_hours_material_min,0.05,share,Seuil part d'heures de surplus materialite,default,2026-02-10,system
PHYSICS_THRESHOLDS,sr_hours_stage2_min,0.1,share,Seuil part d'heures de surplus pour stress physique stage2,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,stage1_sr_hours_max,0.05,share,Stage1 max part d'heures de surplus,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,stage1_far_min,0.95,ratio,Stage1 min FAR,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,stage1_ir_p10_max,1.5,ratio,Stage1 max IR P10,spec_alignment,2026-02-11,codex
Q2,exclude_year_2022,1.0,bool,Exclude 2022 from regressions (1=yes),default,2026-02-10,system
Q2,min_points_regression,3.0,count,Nombre minimal de points regression,default,2026-02-09,system
Q3,demand_k_max,0.3,ratio,Borne max hausse demande,default,2026-02-09,system
Q3,far_target,0.95,ratio,Cible FAR inversion,default,2026-02-09,system
Q3,require_recent_stage2,1.0,bool,Require recent stage2 stress,default,2026-02-10,system
Q3,sr_energy_target,0.01,ratio,Cible SR inversion,default,2026-02-09,system
Q3,stage2_recent_h_negative_min,200.0,hours,Recent stage2 threshold on negative hours,default,2026-02-10,system
Q3,trend_capture_ratio_min,0.0,ratio/year,Improvement threshold for capture trend,default,2026-02-10,system
Q3,trend_h_negative_max,-10.0,hours/year,Improvement threshold for h_negative trend,default,2026-02-10,system
Q3,trend_window_years,3.0,years,Fenetre tendance Q3,default,2026-02-09,system
Q3,h_negative_target,100.0,hours,Target max negative hours for phase3 inversion proxy,default,2026-02-10,system
Q3,h_below_5_target,300.0,hours,Target max hours below 5 EUR/MWh for phase3 inversion proxy,default,2026-02-10,system
Q3,slope_capture_target,0.0,ratio/year,Target minimum capture-ratio slope for phase3 trend status,default,2026-02-10,system
Q4,bess_eta_roundtrip,0.88,ratio,Rendement roundtrip BESS,default,2026-02-09,system
Q4,bess_max_cycles_per_day,1.0,cycles/day,Cycles max journaliers BESS,default,2026-02-09,system
Q4,bess_soc_init_frac,0.5,ratio,SOC initial fraction,default,2026-02-09,system
Q4,target_far,0.95,ratio,Cible FAR pour sizing,default,2026-02-09,system
Q4,target_surplus_unabs_energy_twh,0.0,TWh,Cible surplus non absorbe,default,2026-02-09,system
Q5,ccgt_ef_t_per_mwh_th,0.202,tCO2/MWhth,Facteur emission CCGT,default,2026-02-09,system
Q5,ccgt_efficiency,0.55,ratio,Rendement CCGT,default,2026-02-09,system
Q5,ccgt_vom_eur_mwh,3.0,EUR/MWh,VOM CCGT,default,2026-02-09,system
Q5,coal_ef_t_per_mwh_th,0.341,tCO2/MWhth,Facteur emission charbon,default,2026-02-09,system
Q5,coal_efficiency,0.38,ratio,Rendement charbon,default,2026-02-09,system
Q5,coal_vom_eur_mwh,4.0,EUR/MWh,VOM charbon,default,2026-02-09,system
QUALITY,regime_coherence_min_for_causality,0.55,ratio,Seuil coherence minimale causalite,default,2026-02-09,system
PHASE_THRESHOLDS,q1_require_non_capture_signal,1.0,bool01,"Q1: exiger au moins un signal non-capture (h_negative, h_below_5 ou spread) pour classer phase2.",codex_adjustment,2026-02-10,codex
PHASE_THRESHOLDS,q1_min_non_capture_flags,1.0,count,Q1: nombre minimal de flags non-capture requis pour phase2.,codex_adjustment,2026-02-10,codex
PHASE_THRESHOLDS,q1_persistence_window_years,2.0,years,Q1: nombre d'annees consecutives requises pour valider une bascule,spec_alignment,2026-02-11,codex
PHASE_THRESHOLDS,q1_lever_max_uplift,1.0,ratio,Q1: borne max d'uplift pour solveurs required_demand/flex,spec_alignment,2026-02-11,codex
Q3,stage2_recent_h_negative_min_scen,80.0,h/an,Q3 SCEN: seuil h_negative recent pour qualifier un contexte Stage2 en prospectif.,codex_adjustment,2026-02-10,codex
Q3,stage2_recent_sr_energy_min_scen,0.02,ratio,Q3 SCEN: seuil SR recent pour qualifier un contexte Stage2 meme si h_negative reste faible.,codex_adjustment,2026-02-10,codex
```

#### Phase 2 assumptions
```csv
scenario_id,country,year,demand_total_twh,demand_peak_gw,demand_shape_reference,cap_pv_gw,cap_wind_on_gw,cap_wind_off_gw,cap_must_run_nuclear_gw,cap_must_run_chp_gw,cap_must_run_biomass_gw,cap_must_run_hydro_ror_gw,must_run_min_output_factor,interconnection_export_gw,export_coincidence_factor,psh_pump_gw,bess_power_gw,bess_energy_gwh,bess_eta_roundtrip,co2_eur_per_t,gas_eur_per_mwh_th,marginal_tech,marginal_efficiency,marginal_emission_factor_t_per_mwh,supported_vre_share,negative_price_rule,negative_price_rule_threshold_hours,price_exposure_share,source_label,notes
BASE,DE,2025,480.1727000000001,53.353,historical_mean_2018_2024,19.466700000000003,36.46300000000001,5.3717500000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2026,489.3188400000001,54.36919999999999,historical_mean_2018_2024,19.80526,36.85368,5.46942,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2027,498.4649800000001,55.3854,historical_mean_2018_2024,20.14382,37.24436,5.56709,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2028,507.61112,56.4016,historical_mean_2018_2024,20.482380000000003,37.63504,5.66476,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2029,516.7572600000001,57.4178,historical_mean_2018_2024,20.82094,38.02572000000001,5.76243,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,DE,2031,535.04954,59.4502,historical_mean_2018_2024,21.49806,38.80708,5.95777,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2032,544.19568,60.4664,historical_mean_2018_2024,21.83662,39.19776,6.05544,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2033,553.34182,61.4826,historical_mean_2018_2024,22.17518,39.588440000000006,6.15311,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2034,562.48796,62.4988,historical_mean_2018_2024,22.51374,39.97912,6.25078,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2035,571.6341,63.515,historical_mean_2018_2024,22.8523,40.3698,6.34845,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2036,580.7802399999999,64.5312,historical_mean_2018_2024,23.19086,40.76048,6.4461200000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2037,589.92638,65.5474,historical_mean_2018_2024,23.52942,41.15116,6.54379,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2038,599.0725199999999,66.56360000000001,historical_mean_2018_2024,23.867980000000003,41.54184,6.64146,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2039,608.21866,67.5798,historical_mean_2018_2024,24.20654,41.93252,6.73913,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,ES,2025,234.2802,26.030500000000004,historical_mean_2018_2024,12.5165,13.37405,1.9703,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2026,238.74268,26.5264,historical_mean_2018_2024,12.73418,13.51734,2.00612,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2027,243.20516,27.0223,historical_mean_2018_2024,12.95186,13.66063,2.04194,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2028,247.66764,27.5182,historical_mean_2018_2024,13.16954,13.80392,2.07776,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2029,252.13012,28.014100000000003,historical_mean_2018_2024,13.38722,13.94721,2.11358,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,ES,2031,261.05508,29.0059,historical_mean_2018_2024,13.82258,14.23379,2.18522,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2032,265.51756,29.501800000000003,historical_mean_2018_2024,14.04026,14.37708,2.22104,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2033,269.98004000000003,29.9977,historical_mean_2018_2024,14.25794,14.52037,2.25686,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2034,274.44252,30.4936,historical_mean_2018_2024,14.47562,14.66366,2.29268,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2035,278.905,30.9895,historical_mean_2018_2024,14.6933,14.80695,2.3285,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2036,283.36748,31.4854,historical_mean_2018_2024,14.91098,14.95024,2.36432,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2037,287.82996,31.9813,historical_mean_2018_2024,15.12866,15.09353,2.40014,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2038,292.29244,32.4772,historical_mean_2018_2024,15.34634,15.23682,2.43596,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2039,296.75492,32.9731,historical_mean_2018_2024,15.56402,15.38011,2.47178,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,DE,2025,528.1899,58.6875,historical_mean_2018_2024,19.466700000000003,36.46300000000001,5.3717500000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2026,538.2506599999999,59.8054,historical_mean_2018_2024,19.80526,36.85368,5.46942,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2027,548.31142,60.9233,historical_mean_2018_2024,20.14382,37.24436,5.56709,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2028,558.37218,62.0412,historical_mean_2018_2024,20.482380000000003,37.63504,5.66476,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2029,568.43294,63.1591,historical_mean_2018_2024,20.82094,38.02572000000001,5.76243,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2030,578.4937,64.277,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,DE,2031,588.55446,65.3949,historical_mean_2018_2024,21.49806,38.80708,5.95777,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2032,598.61522,66.5128,historical_mean_2018_2024,21.83662,39.19776,6.05544,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2033,608.67598,67.6307,historical_mean_2018_2024,22.17518,39.588440000000006,6.15311,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2034,618.73674,68.7486,historical_mean_2018_2024,22.51374,39.97912,6.25078,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2035,628.7975,69.8665,historical_mean_2018_2024,22.8523,40.3698,6.34845,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2036,638.85826,70.98440000000001,historical_mean_2018_2024,23.19086,40.76048,6.4461200000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2037,648.91902,72.1023,historical_mean_2018_2024,23.52942,41.15116,6.54379,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2038,658.97978,73.2202,historical_mean_2018_2024,23.867980000000003,41.54184,6.64146,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2039,669.0405400000001,74.3381,historical_mean_2018_2024,24.20654,41.93252,6.73913,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,DE,2040,679.1013,75.456,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,ES,2025,257.70815000000005,28.634,historical_mean_2018_2024,12.5165,13.37405,1.9703,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2026,262.61688000000004,29.1794,historical_mean_2018_2024,12.73418,13.51734,2.00612,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2027,267.52561000000003,29.7248,historical_mean_2018_2024,12.95186,13.66063,2.04194,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2028,272.43434,30.270200000000003,historical_mean_2018_2024,13.16954,13.80392,2.07776,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2029,277.34307,30.8156,historical_mean_2018_2024,13.38722,13.94721,2.11358,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2030,282.2518,31.361,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,ES,2031,287.16053,31.9064,historical_mean_2018_2024,13.82258,14.23379,2.18522,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2032,292.06926,32.4518,historical_mean_2018_2024,14.04026,14.37708,2.22104,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2033,296.97799,32.9972,historical_mean_2018_2024,14.25794,14.52037,2.25686,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2034,301.88672,33.5426,historical_mean_2018_2024,14.47562,14.66366,2.29268,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2035,306.79545,34.088,historical_mean_2018_2024,14.6933,14.80695,2.3285,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2036,311.70418,34.6334,historical_mean_2018_2024,14.91098,14.95024,2.36432,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2037,316.61291,35.178799999999995,historical_mean_2018_2024,15.12866,15.09353,2.40014,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2038,321.52164,35.7242,historical_mean_2018_2024,15.34634,15.23682,2.43596,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2039,326.43037,36.2696,historical_mean_2018_2024,15.56402,15.38011,2.47178,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,ES,2040,331.3391,36.815,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,DE,2025,480.1727000000001,53.353,historical_mean_2018_2024,19.466700000000003,36.46300000000001,5.3717500000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,120.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2026,489.3188400000001,54.36919999999999,historical_mean_2018_2024,19.80526,36.85368,5.46942,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,123.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2027,498.4649800000001,55.3854,historical_mean_2018_2024,20.14382,37.24436,5.56709,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,126.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2028,507.61112,56.4016,historical_mean_2018_2024,20.482380000000003,37.63504,5.66476,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,129.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2029,516.7572600000001,57.4178,historical_mean_2018_2024,20.82094,38.02572000000001,5.76243,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,132.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,135.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,DE,2031,535.04954,59.4502,historical_mean_2018_2024,21.49806,38.80708,5.95777,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,138.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2032,544.19568,60.4664,historical_mean_2018_2024,21.83662,39.19776,6.05544,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,141.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2033,553.34182,61.4826,historical_mean_2018_2024,22.17518,39.588440000000006,6.15311,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,144.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2034,562.48796,62.4988,historical_mean_2018_2024,22.51374,39.97912,6.25078,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,147.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2035,571.6341,63.515,historical_mean_2018_2024,22.8523,40.3698,6.34845,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,150.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2036,580.7802399999999,64.5312,historical_mean_2018_2024,23.19086,40.76048,6.4461200000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,153.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2037,589.92638,65.5474,historical_mean_2018_2024,23.52942,41.15116,6.54379,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,156.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2038,599.0725199999999,66.56360000000001,historical_mean_2018_2024,23.867980000000003,41.54184,6.64146,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,159.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2039,608.21866,67.5798,historical_mean_2018_2024,24.20654,41.93252,6.73913,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,162.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,165.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,ES,2025,234.2802,26.030500000000004,historical_mean_2018_2024,12.5165,13.37405,1.9703,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,120.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2026,238.74268,26.5264,historical_mean_2018_2024,12.73418,13.51734,2.00612,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,123.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2027,243.20516,27.0223,historical_mean_2018_2024,12.95186,13.66063,2.04194,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,126.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2028,247.66764,27.5182,historical_mean_2018_2024,13.16954,13.80392,2.07776,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,129.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2029,252.13012,28.014100000000003,historical_mean_2018_2024,13.38722,13.94721,2.11358,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,132.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,135.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,ES,2031,261.05508,29.0059,historical_mean_2018_2024,13.82258,14.23379,2.18522,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,138.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2032,265.51756,29.501800000000003,historical_mean_2018_2024,14.04026,14.37708,2.22104,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,141.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2033,269.98004000000003,29.9977,historical_mean_2018_2024,14.25794,14.52037,2.25686,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,144.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2034,274.44252,30.4936,historical_mean_2018_2024,14.47562,14.66366,2.29268,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,147.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2035,278.905,30.9895,historical_mean_2018_2024,14.6933,14.80695,2.3285,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,150.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2036,283.36748,31.4854,historical_mean_2018_2024,14.91098,14.95024,2.36432,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,153.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2037,287.82996,31.9813,historical_mean_2018_2024,15.12866,15.09353,2.40014,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,156.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2038,292.29244,32.4772,historical_mean_2018_2024,15.34634,15.23682,2.43596,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,159.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2039,296.75492,32.9731,historical_mean_2018_2024,15.56402,15.38011,2.47178,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,162.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,165.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,DE,2025,480.1727000000001,53.353,historical_mean_2018_2024,19.466700000000003,36.46300000000001,5.3717500000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,58.5,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2026,489.3188400000001,54.36919999999999,historical_mean_2018_2024,19.80526,36.85368,5.46942,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,59.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2027,498.4649800000001,55.3854,historical_mean_2018_2024,20.14382,37.24436,5.56709,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,60.3,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2028,507.61112,56.4016,historical_mean_2018_2024,20.482380000000003,37.63504,5.66476,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,61.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2029,516.7572600000001,57.4178,historical_mean_2018_2024,20.82094,38.02572000000001,5.76243,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,62.1,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,63.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,DE,2031,535.04954,59.4502,historical_mean_2018_2024,21.49806,38.80708,5.95777,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,63.9,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2032,544.19568,60.4664,historical_mean_2018_2024,21.83662,39.19776,6.05544,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,64.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2033,553.34182,61.4826,historical_mean_2018_2024,22.17518,39.588440000000006,6.15311,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,65.7,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2034,562.48796,62.4988,historical_mean_2018_2024,22.51374,39.97912,6.25078,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,66.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2035,571.6341,63.515,historical_mean_2018_2024,22.8523,40.3698,6.34845,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,67.5,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2036,580.7802399999999,64.5312,historical_mean_2018_2024,23.19086,40.76048,6.4461200000000005,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,68.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2037,589.92638,65.5474,historical_mean_2018_2024,23.52942,41.15116,6.54379,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,69.3,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2038,599.0725199999999,66.56360000000001,historical_mean_2018_2024,23.867980000000003,41.54184,6.64146,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,70.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2039,608.21866,67.5798,historical_mean_2018_2024,24.20654,41.93252,6.73913,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,71.1,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,72.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,ES,2025,234.2802,26.030500000000004,historical_mean_2018_2024,12.5165,13.37405,1.9703,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,58.5,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2026,238.74268,26.5264,historical_mean_2018_2024,12.73418,13.51734,2.00612,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,59.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2027,243.20516,27.0223,historical_mean_2018_2024,12.95186,13.66063,2.04194,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,60.3,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2028,247.66764,27.5182,historical_mean_2018_2024,13.16954,13.80392,2.07776,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,61.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2029,252.13012,28.014100000000003,historical_mean_2018_2024,13.38722,13.94721,2.11358,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,62.1,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,63.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,ES,2031,261.05508,29.0059,historical_mean_2018_2024,13.82258,14.23379,2.18522,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,63.9,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2032,265.51756,29.501800000000003,historical_mean_2018_2024,14.04026,14.37708,2.22104,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,64.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2033,269.98004000000003,29.9977,historical_mean_2018_2024,14.25794,14.52037,2.25686,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,65.7,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2034,274.44252,30.4936,historical_mean_2018_2024,14.47562,14.66366,2.29268,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,66.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2035,278.905,30.9895,historical_mean_2018_2024,14.6933,14.80695,2.3285,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,67.5,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2036,283.36748,31.4854,historical_mean_2018_2024,14.91098,14.95024,2.36432,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,68.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2037,287.82996,31.9813,historical_mean_2018_2024,15.12866,15.09353,2.40014,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,69.3,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2038,292.29244,32.4772,historical_mean_2018_2024,15.34634,15.23682,2.43596,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,70.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2039,296.75492,32.9731,historical_mean_2018_2024,15.56402,15.38011,2.47178,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,71.1,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,72.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,DE,2025,480.1727000000001,53.353,historical_mean_2018_2024,19.466700000000003,36.46300000000001,5.3717500000000005,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2026,489.3188400000001,54.36919999999999,historical_mean_2018_2024,19.80526,36.85368,5.46942,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2027,498.4649800000001,55.3854,historical_mean_2018_2024,20.14382,37.24436,5.56709,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2028,507.61112,56.4016,historical_mean_2018_2024,20.482380000000003,37.63504,5.66476,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2029,516.7572600000001,57.4178,historical_mean_2018_2024,20.82094,38.02572000000001,5.76243,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2030,525.9034,58.434,historical_mean_2018_2024,21.1595,38.4164,5.8601,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,DE,2031,535.04954,59.4502,historical_mean_2018_2024,21.49806,38.80708,5.95777,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2032,544.19568,60.4664,historical_mean_2018_2024,21.83662,39.19776,6.05544,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2033,553.34182,61.4826,historical_mean_2018_2024,22.17518,39.588440000000006,6.15311,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2034,562.48796,62.4988,historical_mean_2018_2024,22.51374,39.97912,6.25078,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2035,571.6341,63.515,historical_mean_2018_2024,22.8523,40.3698,6.34845,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2036,580.7802399999999,64.5312,historical_mean_2018_2024,23.19086,40.76048,6.4461200000000005,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2037,589.92638,65.5474,historical_mean_2018_2024,23.52942,41.15116,6.54379,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2038,599.0725199999999,66.56360000000001,historical_mean_2018_2024,23.867980000000003,41.54184,6.64146,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2039,608.21866,67.5798,historical_mean_2018_2024,24.20654,41.93252,6.73913,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,DE,2040,617.3648,68.596,historical_mean_2018_2024,24.5451,42.3232,6.8368,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,ES,2025,234.2802,26.030500000000004,historical_mean_2018_2024,12.5165,13.37405,1.9703,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2026,238.74268,26.5264,historical_mean_2018_2024,12.73418,13.51734,2.00612,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2027,243.20516,27.0223,historical_mean_2018_2024,12.95186,13.66063,2.04194,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2028,247.66764,27.5182,historical_mean_2018_2024,13.16954,13.80392,2.07776,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2029,252.13012,28.014100000000003,historical_mean_2018_2024,13.38722,13.94721,2.11358,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2030,256.5926,28.51,historical_mean_2018_2024,13.6049,14.0905,2.1494,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,ES,2031,261.05508,29.0059,historical_mean_2018_2024,13.82258,14.23379,2.18522,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2032,265.51756,29.501800000000003,historical_mean_2018_2024,14.04026,14.37708,2.22104,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2033,269.98004000000003,29.9977,historical_mean_2018_2024,14.25794,14.52037,2.25686,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2034,274.44252,30.4936,historical_mean_2018_2024,14.47562,14.66366,2.29268,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2035,278.905,30.9895,historical_mean_2018_2024,14.6933,14.80695,2.3285,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2036,283.36748,31.4854,historical_mean_2018_2024,14.91098,14.95024,2.36432,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2037,287.82996,31.9813,historical_mean_2018_2024,15.12866,15.09353,2.40014,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2038,292.29244,32.4772,historical_mean_2018_2024,15.34634,15.23682,2.43596,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2039,296.75492,32.9731,historical_mean_2018_2024,15.56402,15.38011,2.47178,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,ES,2040,301.2174,33.469,historical_mean_2018_2024,15.7817,15.5234,2.5076,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
```

## RUN OUTPUTS

### A.1 annual_metrics_phase1
```csv
country,year,scenario_id,n_hours,timezone,coverage_price,coverage_load_total,coverage_psh_pumping,coverage_pv,coverage_wind,coverage_net_position,coverage_nuclear,coverage_biomass,coverage_ror,load_total_mw_avg,psh_pumping_mw_avg,load_mw_avg,must_run_mw_avg,must_run_nuclear_mw_avg,must_run_biomass_mw_avg,must_run_ror_mw_avg,nrl_mw_avg,nrl_p10_mw,nrl_p50_mw,nrl_p90_mw,surplus_mwh_total,sr_energy,sr_hours,far_energy,far_hours,sink_breakdown_json,ir_p10,baseload_price_eur_mwh,ttl_observed_eur_mwh,capture_price_pv_eur_mwh,capture_ratio_pv,capture_ratio_pv_vs_ttl_observed,capture_price_wind_eur_mwh,capture_ratio_wind,capture_ratio_wind_vs_ttl_observed,h_negative_obs,h_below_5_obs,days_spread_gt50,regime_coherence,nrl_price_corr,load_identity_abs_max_mw,load_identity_rel_err,load_identity_ok,data_quality_flags,quality_flag,quality_notes
DE,2018,HIST,8760,Europe/Berlin,1.0,0.9988584474885844,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,63994.59686742856,1541.775593892694,62453.508855428576,27759.03097311644,8201.364040700992,4745.066601495604,4033.805183525517,16938.98747922857,-551.498874999997,17235.284499999998,33588.71037500001,5519737.58175,0.0095832537934301,0.1077625570776255,0.9796177446239518,1.0,"{""exports_absorption_mwh"": 3196795.7587100747, ""psh_absorption_mwh"": 2210437.1220399253, ""other_flex_absorption_mwh"": 0.0}",0.5876118883619526,44.47275456621005,73.28999999999999,43.77257363689873,0.9842559576949768,0.5972516528434811,38.17753675887097,0.8584477649576012,0.5209105847847043,133,231,38,0.9495433789954338,0.6449471743042571,1.4551915228366852e-11,2.110663587732269e-16,True,CORE_SANITY_WARN;PSH_PUMPING_DATA_INCOMPLETE,OK,must_run_mw exceeds load+exports+psh+curtailment_proxy
DE,2019,HIST,8760,Europe/Berlin,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,57367.15583885148,1252.549263413242,56114.46357403814,22754.9653336758,8109.729086082886,4526.801958271492,1666.1688700194086,14381.751818358258,-2947.540250000001,14621.256749999991,30969.69025,8036728.58925,0.0155843596990231,0.1399543378995433,0.9574900183941784,1.0,"{""exports_absorption_mwh"": 5376010.419977754, ""psh_absorption_mwh"": 2319076.9847722473, ""other_flex_absorption_mwh"": 0.0}",0.5289129868835992,37.669692887315904,59.5035,34.906182773392544,0.926638368882113,0.5866240267109085,32.78952818581776,0.8704485137137555,0.5510520924956979,211,335,31,0.9803630551432811,0.838881970646822,7.275957614183426e-12,1.9704071914278732e-16,True,PSH_PUMPING_DATA_INCOMPLETE,OK,NaN
DE,2020,HIST,8784,Europe/Berlin,0.9998861566484516,0.9998861566484516,0.9998861566484516,0.9998861566484516,0.9998861566484516,0.9998861566484516,0.9998861566484516,0.9998861566484516,0.9998861566484516,55818.5015549926,1436.4994894125682,54381.83851104407,20054.27314250341,6935.646044631675,4580.853405157691,1643.1364718774907,14259.849076198336,-2535.8037000000018,14370.08275,30079.16625,6946557.68125,0.0140639659444124,0.1349043715846994,0.9488478002624086,1.0,"{""exports_absorption_mwh"": 5033533.431879824, ""psh_absorption_mwh"": 1557692.5433701773, ""other_flex_absorption_mwh"": 0.0}",0.4833416912394077,30.47081976545599,56.14599999999999,24.511203174738068,0.8044156134757428,0.4365618775110974,25.24537518940176,0.8285098787536335,0.4496380007373947,298,598,42,0.9902083570533986,0.8387745683776916,1.4551915228366852e-11,2.1263532315828492e-16,True,PSH_PUMPING_DATA_INCOMPLETE,OK,NaN
DE,2021,HIST,8760,Europe/Berlin,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,58191.275416999655,1199.9055559360731,56991.232869905245,22854.617910331053,7466.357412375843,4398.012838223542,1524.5079304144308,15832.695628553483,-1394.2332500000043,15945.804999999997,31951.995749999995,6217942.822500002,0.0123326322192535,0.1160958904109589,0.9787814533654792,1.0,"{""exports_absorption_mwh"": 4298014.642321998, ""psh_absorption_mwh"": 1787992.4704280028, ""other_flex_absorption_mwh"": 0.0}",0.5138110015424295,96.86022947825094,259.9279999999997,75.45790652091513,0.7790391053931841,0.2903031090183251,83.19114655913475,0.8588782724060605,0.3200545788031103,139,247,202,0.9086653727594476,0.5395224675147319,1.4551915228366852e-11,1.9302673882086998e-16,True,PSH_PUMPING_DATA_INCOMPLETE,OK,NaN
DE,2022,HIST,8760,Europe/Berlin,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,55628.55850068501,1551.5929223744292,54076.78843560909,19845.877572431506,3747.1264656353455,4340.933297465464,1290.566084027857,13450.170577463176,-4770.141000000004,13900.228249999996,30339.77565,10144511.945,0.0206641833556319,0.1697488584474885,0.9797943883243168,1.0,"{""exports_absorption_mwh"": 6338635.31904302, ""psh_absorption_mwh"": 3600900.5569569813, ""other_flex_absorption_mwh"": 0.0}",0.477699136446879,235.4667222285649,526.146,222.2697802958073,0.9439541103394328,0.4224488645657429,173.5038161884555,0.7368506876315086,0.3297636325059118,69,159,358,0.867108117364996,0.601272099848366,1.4551915228366852e-11,2.0615622932742944e-16,True,PSH_PUMPING_DATA_INCOMPLETE,OK,NaN
DE,2023,HIST,8760,Europe/Berlin,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,52864.463655097614,1446.741551084475,51417.55693201279,13051.235077796806,769.2974491951137,4277.176212181756,1539.000027400388,15670.27397944971,-4078.560399999999,15745.63775,34517.090249999994,9207172.96175,0.0207147899675382,0.1602739726027397,0.9564096539005692,1.0,"{""exports_absorption_mwh"": 5422374.111257402, ""psh_absorption_mwh"": 3383454.9944925983, ""other_flex_absorption_mwh"": 0.0}",0.3302146638326648,95.1827480305971,170.553,72.18210511017934,0.7583528171195051,0.4232238958574715,79.91071132318326,0.8395503699630048,0.4685388783731934,300,526,340,0.9346957415230048,0.8679345857241685,7.275957614183426e-12,2.031206281194015e-16,True,PSH_PUMPING_DATA_INCOMPLETE,OK,NaN
DE,2024,HIST,8784,Europe/Berlin,0.9998861566484516,0.9998861566484516,0.9998861566484516,0.9998861566484516,0.9998861566484516,0.9998861566484516,0.9998861566484516,0.9998861566484516,0.9998861566484516,53553.149668449616,1485.6590895377958,52067.32142724502,12242.631894068762,0.0,4150.120007969942,1794.6057676761925,16812.627341511212,-3663.95635,17749.224000000002,35063.091499999995,9365357.362127,0.0218565415301092,0.1402550091074681,0.9534226589972932,1.0,"{""exports_absorption_mwh"": 5249553.852168727, ""psh_absorption_mwh"": 3679590.066490274, ""other_flex_absorption_mwh"": 0.0}",0.302364053902495,78.51545827166116,148.70999999999998,46.22796099131209,0.5887752808034911,0.3108598008964568,65.83122843523844,0.838449266989748,0.4426819207534023,457,756,315,0.9658431060002276,0.7912510966551397,7.275957614183426e-12,2.0356514176154892e-16,True,PSH_PUMPING_DATA_INCOMPLETE,OK,NaN
ES,2018,HIST,8760,Europe/Madrid,0.9998858447488584,0.9996575342465752,0.9997716894977168,0.9997716894977168,0.9997716894977168,0.9998858447488584,0.9997716894977168,0.9997716894977168,0.9997716894977168,29064.3270526436,384.40353881278537,28679.791937878268,11120.59515981735,6082.010961406714,336.9155058232473,1223.534596939941,10600.259255452782,3360.4600000000005,10736.1,17463.7,613410.0,0.002492798483948,0.0378995433789954,0.9913824358911656,1.0,"{""exports_absorption_mwh"": 147191.54700329818, ""psh_absorption_mwh"": 460932.3529967017, ""other_flex_absorption_mwh"": 0.0}",0.498409408103965,57.30006279255623,73.997,59.342028861067455,1.0356363670298891,0.8019518204936342,53.09425838495249,0.926600352554062,0.7175190667858493,0,45,5,0.9713437607032768,0.7284831419179216,0.0,0.0,True,CORE_SANITY_WARN;PSH_PUMPING_DATA_INCOMPLETE,OK,must_run_mw exceeds load+exports+psh+curtailment_proxy
ES,2019,HIST,8760,Europe/Madrid,0.9998858447488584,0.9998858447488584,0.9993150684931508,0.9993150684931508,0.9993150684931508,0.9998858447488584,0.9993150684931508,0.9993150684931508,0.9993150684931508,28538.000456673137,367.1673515981735,28170.791186208477,10827.2899086758,6388.269591044094,333.6010966415353,997.2428604066712,9719.49062678388,2679.100000000001,9813.1,16403.899999999998,683082.0999999999,0.0027731012860235,0.0406392694063926,0.9668340013594268,1.0,"{""exports_absorption_mwh"": 261737.44350775093, ""psh_absorption_mwh"": 398689.556492249, ""other_flex_absorption_mwh"": 0.0}",0.4919654861226218,47.67961867793127,64.68299999999998,48.57853958864,1.0188533578001284,0.7510248378807417,45.65081383781028,0.9574492226159512,0.705762160657519,0,68,2,0.9725996118278344,0.6978382597849259,0.0,0.0,True,PSH_PUMPING_DATA_INCOMPLETE,OK,NaN
ES,2020,HIST,8784,Europe/Madrid,0.9998861566484516,0.9998861566484516,0.9997723132969034,0.9997723132969034,0.9997723132969034,0.9998861566484516,0.9997723132969034,0.9997723132969034,0.9997723132969034,27086.93293863145,551.7243852459017,26535.145736081067,9699.049806466304,6354.735140059212,436.342746526987,1150.2279662946935,8503.02988728225,869.7400000000004,8720.7,15835.3,1851233.7999999998,0.0077568856418017,0.0809426229508196,0.9809348230353184,1.0,"{""exports_absorption_mwh"": 852236.5733091922, ""psh_absorption_mwh"": 963703.1266908078, ""other_flex_absorption_mwh"": 0.0}",0.4773860231515868,33.95808038255721,52.269,32.896135604866735,0.9687277736041888,0.6293622530537553,32.37432130900995,0.9533613485890452,0.6193790068493744,0,54,0,0.987703518160082,0.7678864458008594,0.0,0.0,True,PSH_PUMPING_DATA_INCOMPLETE,OK,NaN
ES,2021,HIST,8760,Europe/Madrid,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,27848.911633748143,522.9477168949771,27325.90421280968,9769.263493150684,6187.529398333143,474.34376070327664,973.1736499600412,7924.029432583628,153.7800000000008,8283.2,15076.4,2540644.1999999993,0.0102738803207986,0.096917808219178,0.9795160219601,1.0,"{""exports_absorption_mwh"": 1360264.2787309452, ""psh_absorption_mwh"": 1128337.4212690545, ""other_flex_absorption_mwh"": 0.0}",0.4430891814452746,111.94053088252085,258.883,102.39616733438756,0.9147371959656876,0.3955306734485755,103.78184356536732,0.9271158779324008,0.4008831926598785,0,195,130,0.9005594245918483,0.3187951807835402,0.0,0.0,True,PSH_PUMPING_DATA_INCOMPLETE,OK,NaN
ES,2022,HIST,8760,Europe/Madrid,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9971461187214612,0.9998858447488584,0.9998858447488584,0.9998858447488584,26952.232903299464,710.1865753424657,26241.965247174336,10149.37929223744,6411.29978308026,461.7916428816075,770.7814590706702,5826.612878182441,-2319.5399999999986,5981.299999999999,13358.4,4858457.300000001,0.0185848196425309,0.1673515981735159,0.96481259596539,1.0,"{""exports_absorption_mwh"": 2756666.248179511, ""psh_absorption_mwh"": 1930834.5518204886, ""other_flex_absorption_mwh"": 0.0}",0.5017640864926367,167.52426875214064,275.152,151.07895653475305,0.9018332547284886,0.5490745352923223,160.5904117834413,0.958609835933931,0.5836425386093552,0,113,329,0.8370818586596643,0.4936263220095353,0.0,0.0,True,PSH_PUMPING_DATA_INCOMPLETE,OK,NaN
ES,2023,HIST,8760,Europe/Madrid,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,0.9998858447488584,26158.69893823496,952.2392694063929,25206.350953305173,8746.24200913242,6207.673478707615,353.27548806941434,826.0148418769265,4873.536705103323,-5148.0,5380.0,13916.8,10338152.0,0.0422222222948287,0.2627853881278539,0.9210418361037832,1.0,"{""exports_absorption_mwh"": 5039285.3409092445, ""psh_absorption_mwh"": 4482585.159090756, ""other_flex_absorption_mwh"": 0.0}",0.4507519593306502,87.11351866651445,151.61,73.07910508828432,0.8388951130311212,0.4820203488443,76.31964002657413,0.8760941033588467,0.5033944992188784,0,526,273,0.8292042470601667,0.762858935390759,0.0,0.0,True,PSH_PUMPING_DATA_INCOMPLETE,OK,NaN
ES,2024,HIST,8784,Europe/Madrid,0.9998861566484516,0.9998861566484516,0.9997723132969034,0.9997723132969034,0.9997723132969034,0.9998861566484516,0.9997723132969034,0.9997723132969034,0.9997723132969034,26417.495161106683,1013.306921675774,25404.072868040534,7957.82058287796,5957.368708722387,390.2924163060806,1002.2459576406286,5357.910053512467,-5232.0,5860.0,14987.2,10210340.0,0.0421613920351003,0.2695810564663023,0.945507681428826,1.0,"{""exports_absorption_mwh"": 5186977.4604065055, ""psh_absorption_mwh"": 4466977.439593494, ""other_flex_absorption_mwh"": 0.0}",0.3950264981655116,63.03954912899921,141.5,42.80117347476487,0.6789574809169381,0.3024817913410945,55.60947301426717,0.8821362744913085,0.3929998092881072,247,1642,271,0.9008311510873278,0.717301833704112,0.0,0.0,True,PSH_PUMPING_DATA_INCOMPLETE,OK,NaN
```

### A.2 q1_transition_summary
```csv
country,transition_year,stage,stage2_score,non_capture_flags_count,reason_codes,persistence_window_years,confidence_level
DE,2019,2,3.0,3,LOW_PRICE:h_negative_obs>=200.0 (211.0); VALUE:capture_ratio_wind<=0.90 (0.870); PHYSICAL:sr_energy>=0.010 (0.016); PHYSICAL:sr_hours>=0.10 (0.140),2.0,1.0
ES,2023,2,3.0,4,LOW_PRICE:h_below_5_obs>=500.0 (526.0); LOW_PRICE:low_price_hours_share>=0.057 (0.060); VALUE:capture_ratio_wind<=0.90 (0.876); PHYSICAL:sr_energy>=0.010 (0.042); PHYSICAL:sr_hours>=0.10 (0.263); PHYSICAL:far_observed<0.95 (0.921),2.0,1.0
```

### A.3 q2_slope_summary
```csv
scenario_id,country,tech,x_var_used,y_var_used,n_points,years_used,slope,intercept,r2,p_value,driver_stats_phase2,slope_quality_flag,slope_quality_notes
HIGH_CO2,DE,PV,pv_penetration_share_generation,capture_ratio_PV,11,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",-0.4639311591397298,0.9960978028196452,0.9626965348712196,9.826234352612265e-08,"{""sr_energy_mean"": 0.0, ""far_energy_mean"": 1.0, ""ir_p10_mean"": 0.0476924500670436, ""ttl_mean"": 212.0053332833652, ""corr_vre_load_mean"": 0.1901157879571487}",PASS,OLS_STRICT_PASS
HIGH_CO2,DE,WIND,wind_penetration_share_generation,capture_ratio_WIND,11,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",-0.1212272923370727,0.9918414228947604,0.9635221488359548,8.881696819880572e-08,"{""sr_energy_mean"": 0.0, ""far_energy_mean"": 1.0, ""ir_p10_mean"": 0.0476924500670436, ""ttl_mean"": 212.0053332833652, ""corr_vre_load_mean"": 0.2092241523696177}",PASS,OLS_STRICT_PASS
HIGH_GAS,DE,PV,pv_penetration_share_generation,capture_ratio_PV,11,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",-0.4474048633354546,0.9954301664151248,0.9589418917423228,1.5153096971675979e-07,"{""sr_energy_mean"": 0.0, ""far_energy_mean"": 1.0, ""ir_p10_mean"": 0.0476924500670436, ""ttl_mean"": 217.21388591494411, ""corr_vre_load_mean"": 0.1901157879571487}",PASS,OLS_STRICT_PASS
HIGH_GAS,DE,WIND,wind_penetration_share_generation,capture_ratio_WIND,11,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",-0.113901219692303,0.9906297175655832,0.959437403145118,1.434434859836388e-07,"{""sr_energy_mean"": 0.0, ""far_energy_mean"": 1.0, ""ir_p10_mean"": 0.0476924500670436, ""ttl_mean"": 217.21388591494411, ""corr_vre_load_mean"": 0.2092241523696177}",PASS,OLS_STRICT_PASS
HIST,DE,PV,pv_penetration_share_generation,capture_ratio_PV,5,"2019,2020,2021,2023,2024",-4.739637655041085,1.2804002249057085,0.796651927815217,0.041590622211327,"{""sr_energy_mean"": 0.0169104578720673, ""far_energy_mean"": 0.9589903169839856, ""ir_p10_mean"": 0.4317288794801192, ""ttl_mean"": 138.96809999999996, ""corr_vre_load_mean"": 0.1672592506998106}",WARN,N_LT_6|LOO_NOT_AVAILABLE
HIST,DE,PV,pv_penetration_share_generation,capture_ratio_PV,5,"2019,2020,2021,2023,2024",-4.739637655041085,1.2804002249057085,0.796651927815217,0.041590622211327,"{""sr_energy_mean"": 0.0169104578720673, ""far_energy_mean"": 0.9589903169839856, ""ir_p10_mean"": 0.4317288794801192, ""ttl_mean"": 138.96809999999996, ""corr_vre_load_mean"": 0.1672592506998106}",WARN,N_LT_6|LOO_NOT_AVAILABLE
HIST,DE,WIND,wind_penetration_share_generation,capture_ratio_WIND,5,"2019,2020,2021,2023,2024",-0.3006200607703855,0.9298168940484184,0.4112267622485391,0.2435632965927686,"{""sr_energy_mean"": 0.0169104578720673, ""far_energy_mean"": 0.9589903169839856, ""ir_p10_mean"": 0.4317288794801192, ""ttl_mean"": 138.96809999999996, ""corr_vre_load_mean"": 0.1183862831506812}",WARN,N_LT_6|PVALUE_GT_0_05|LOO_NOT_AVAILABLE
HIST,DE,WIND,wind_penetration_share_generation,capture_ratio_WIND,5,"2019,2020,2021,2023,2024",-0.3006200607703855,0.9298168940484184,0.4112267622485391,0.2435632965927686,"{""sr_energy_mean"": 0.0169104578720673, ""far_energy_mean"": 0.9589903169839856, ""ir_p10_mean"": 0.4317288794801192, ""ttl_mean"": 138.96809999999996, ""corr_vre_load_mean"": 0.1183862831506812}",WARN,N_LT_6|PVALUE_GT_0_05|LOO_NOT_AVAILABLE
HIGH_CO2,ES,PV,pv_penetration_share_generation,capture_ratio_PV,11,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",0.6794271695164195,0.8567612786949044,0.9154234138729596,3.990315154991564e-06,"{""sr_energy_mean"": 0.0, ""far_energy_mean"": 1.0, ""ir_p10_mean"": 0.0824222844630902, ""ttl_mean"": 164.91289390184266, ""corr_vre_load_mean"": 0.2383102353783595}",PASS,OLS_STRICT_PASS
HIGH_CO2,ES,WIND,wind_penetration_share_generation,capture_ratio_WIND,11,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",-0.103368526990708,0.9960995060023642,0.9356289986885578,1.157847835152236e-06,"{""sr_energy_mean"": 0.0, ""far_energy_mean"": 1.0, ""ir_p10_mean"": 0.0824222844630902, ""ttl_mean"": 164.91289390184266, ""corr_vre_load_mean"": 0.0640250710919311}",PASS,OLS_STRICT_PASS
HIGH_GAS,ES,PV,pv_penetration_share_generation,capture_ratio_PV,11,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",0.6434755797349244,0.8626689101546849,0.9126841078577111,4.611338307774519e-06,"{""sr_energy_mean"": 0.0, ""far_energy_mean"": 1.0, ""ir_p10_mean"": 0.0824222844630902, ""ttl_mean"": 172.4919848109336, ""corr_vre_load_mean"": 0.2383102353783595}",PASS,OLS_STRICT_PASS
HIGH_GAS,ES,WIND,wind_penetration_share_generation,capture_ratio_WIND,11,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",-0.1011840461414947,0.9962463206892443,0.9359933083476568,1.1284725310266763e-06,"{""sr_energy_mean"": 0.0, ""far_energy_mean"": 1.0, ""ir_p10_mean"": 0.0824222844630902, ""ttl_mean"": 172.4919848109336, ""corr_vre_load_mean"": 0.0640250710919311}",PASS,OLS_STRICT_PASS
HIST,ES,PV,pv_penetration_share_generation,capture_ratio_PV,2,"2023,2024",-5.57809924164063,1.860268768557785,NaN,NaN,"{""sr_energy_mean"": 0.0421918071649645, ""far_energy_mean"": 0.9332747587663048, ""ir_p10_mean"": 0.4228892287480809, ""ttl_mean"": 146.555, ""corr_vre_load_mean"": 0.0969359919115746}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
HIST,ES,PV,pv_penetration_share_generation,capture_ratio_PV,2,"2023,2024",-5.57809924164063,1.860268768557785,NaN,NaN,"{""sr_energy_mean"": 0.0421918071649645, ""far_energy_mean"": 0.9332747587663048, ""ir_p10_mean"": 0.4228892287480809, ""ttl_mean"": 146.555, ""corr_vre_load_mean"": 0.0969359919115746}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
HIST,ES,WIND,wind_penetration_share_generation,capture_ratio_WIND,2,"2023,2024",-0.4835842544288084,1.0098171935311628,NaN,NaN,"{""sr_energy_mean"": 0.0421918071649645, ""far_energy_mean"": 0.9332747587663048, ""ir_p10_mean"": 0.4228892287480809, ""ttl_mean"": 146.555, ""corr_vre_load_mean"": 0.025985207649981}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
HIST,ES,WIND,wind_penetration_share_generation,capture_ratio_WIND,2,"2023,2024",-0.4835842544288084,1.0098171935311628,NaN,NaN,"{""sr_energy_mean"": 0.0421918071649645, ""far_energy_mean"": 0.9332747587663048, ""ir_p10_mean"": 0.4228892287480809, ""ttl_mean"": 146.555, ""corr_vre_load_mean"": 0.025985207649981}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
```

### A.4 q3_inversion_requirements
```csv
country,scenario_id,year,lever,required_uplift,required_uplift_mw,required_uplift_pct_avg_load,required_uplift_twh_per_year,within_bounds,target_sr,target_h_negative,target_h_below_5,predicted_sr_after,predicted_far_after,predicted_h_negative_after,predicted_h_below_5_after,predicted_h_negative_metric,applicability_flag,status,reason
DE,HIST,2024,demand_uplift,6679.487291494592,6679.487291494592,0.1282855946570635,58.67261636848849,True,0.01,200.0,500.0,0.0063156135807017,0.6520442797070842,199.66112433425928,346.40051641639263,MARKET_PROXY_BUCKET_MODEL_EST,APPLICABLE,ok,ok
DE,HIST,2024,export_uplift,7693.13301841282,7693.13301841282,0.1477535776285828,67.57648043373821,True,0.01,200.0,500.0,0.0056794444031859,0.7169269014217347,199.941059183915,384.0372940783505,MARKET_PROXY_BUCKET_MODEL_EST,APPLICABLE,ok,ok
DE,HIST,2024,flex_uplift,6759.39433899484,6759.39433899484,0.1298202817757758,59.37451987373068,True,0.01,200.0,500.0,0.006837071756548,0.6574779364431292,199.97510414447527,352.35270381245607,MARKET_PROXY_BUCKET_MODEL_EST,APPLICABLE,ok,ok
ES,HIST,2024,demand_uplift,6999.600021516316,6999.600021516316,0.2755306228995323,61.48448658899932,True,0.01,200.0,500.0,0.0021604571923841,0.9397782648401564,31.229497655501326,499.9842594398755,MARKET_PROXY_BUCKET_MODEL_EST,APPLICABLE,ok,ok
ES,HIST,2024,export_uplift,5118.935,5118.935,0.2015005635745853,44.964725040000005,False,0.01,200.0,500.0,0.0077012007551762,0.8225648048938626,77.40486771926348,1076.2103989037491,MARKET_PROXY_BUCKET_MODEL_EST,APPLICABLE,not_achievable,not_achievable
ES,HIST,2024,flex_uplift,10185.300000000008,10185.300000000008,0.4009317739288007,89.46767520000006,False,0.01,200.0,500.0,0.0027923652520094,0.9340849961901369,45.3920817599389,907.3392600502729,MARKET_PROXY_BUCKET_MODEL_EST,APPLICABLE,not_achievable,not_achievable
```

### A.5 q4_bess_sizing_curve
```csv
country,scenario_id,year,bess_power_gw,bess_energy_gwh,cycles_realized_per_day,eta_roundtrip,far_energy_after,surplus_unabsorbed_twh_after,h_negative_proxy_after,h_negative_reducible_upper_bound,monotonicity_check_flag,physics_check_flag,on_efficient_frontier,notes
DE,BASE,2035,NaN,NaN,0.0,0.88,1.0,0.0,0.0,0,PASS,PASS,True,dispatch_mode=; objective=
DE,HIGH_CO2,2035,NaN,NaN,0.0,0.88,1.0,0.0,0.0,0,PASS,PASS,True,dispatch_mode=; objective=
DE,HIGH_GAS,2035,NaN,NaN,0.0,0.88,1.0,0.0,0.0,0,PASS,PASS,True,dispatch_mode=; objective=
DE,HIST,2024,NaN,NaN,0.0,0.88,0.9534226589972932,0.4362134434680002,457.0,0,PASS,PASS,True,dispatch_mode=; objective=
ES,BASE,2035,NaN,NaN,0.0,0.88,1.0,0.0,0.0,0,PASS,PASS,True,dispatch_mode=; objective=
ES,HIGH_CO2,2035,NaN,NaN,0.0,0.88,1.0,0.0,0.0,0,PASS,PASS,True,dispatch_mode=; objective=
ES,HIGH_GAS,2035,NaN,NaN,0.0,0.88,1.0,0.0,0.0,0,PASS,PASS,True,dispatch_mode=; objective=
ES,HIST,2024,NaN,NaN,0.0,0.88,0.945507681428826,0.5563851,247.0,0,PASS,PASS,True,dispatch_mode=; objective=
```

### A.6 q5_anchor_sensitivity
```csv
country,scenario_id,year,gas_eur_per_mwh_th,co2_eur_per_t,tca_ccgt_eur_mwh,tca_coal_eur_mwh,ttl_observed_eur_mwh,ttl_model_eur_mwh,delta_tca_vs_base,delta_ttl_model_vs_base,coherence_flag,ttl_proxy_method,status,reason,base_ref_status,base_ref_reason
DE,BASE,2035,45.0,100.0,121.54545454545452,158.8684210526316,206.09345975464063,206.09345975464063,0.0,0.0,PASS,observed_from_prices,ok,nan,ok,nan
DE,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,206.09345975464063,283.52767028095644,77.43421052631578,77.43421052631578,PASS,observed_from_prices,ok,nan,ok,nan
DE,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,221.7974071230617,250.96188080727225,44.86842105263159,44.86842105263159,PASS,observed_from_prices,ok,nan,ok,nan
DE,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,226.81714396516696,238.65924922832485,32.56578947368419,32.56578947368419,PASS,observed_from_prices,ok,nan,ok,nan
DE,HIST,2024,46.96599999999992,70.83,114.4066545454544,135.53771052631566,148.70999999999998,148.70999999999998,0.0,0.0,PASS,observed_from_prices,ok,nan,ok,nan
ES,BASE,2035,45.0,100.0,121.54545454545452,158.8684210526316,164.71704742933926,164.71704742933926,0.0,0.0,PASS,observed_from_prices,ok,nan,ok,nan
ES,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,164.71704742933926,223.9897747020665,59.27272727272728,59.27272727272728,PASS,observed_from_prices,ok,nan,ok,nan
ES,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,171.144320156612,183.08068379297563,18.36363636363637,18.36363636363637,PASS,observed_from_prices,ok,nan,ok,nan
ES,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,179.03522924752107,205.62613833843017,40.90909090909091,40.90909090909091,PASS,observed_from_prices,ok,nan,ok,nan
ES,HIST,2024,47.02,70.68,114.44974545454544,135.48126315789474,141.5,141.5,0.0,0.0,PASS,observed_from_prices,ok,nan,ok,nan
```

## TEST LEDGER

```csv
test_id,scope,country,year,scenario_id,status,metric_name,observed_value,expected_rule,message
BUNDLE_BASE_FALLBACK_HIST,Q1,NaN,NaN,BASE,WARN,BUNDLE_BASE_FALLBACK_HIST,NaN,NaN,Scenario BASE absent: fallback explicite sur les sorties historiques.
BUNDLE_INFORMATIVENESS,Q1,NaN,NaN,NaN,PASS,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=100.00% ; share_compare_informatifs=100.00%
BUNDLE_LEDGER_STATUS,Q1,NaN,NaN,NaN,WARN,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=3"
BUNDLE_NON_NEGATIVE_FIELD_NEGATIVE,Q1,NaN,NaN,NaN,PASS,BUNDLE_NON_NEGATIVE_FIELD_NEGATIVE,NaN,NaN,Tous les champs *_non_negative restent >= 0.
Q1-H-01,Q1,NaN,NaN,nan,PASS,Score marche de bascule,2.0,stage2_market_score present et non vide,Le score de bascule marche est exploitable.
Q1-H-02,Q1,NaN,NaN,nan,PASS,Stress physique SR/FAR/IR,"far_energy,ir_p10,sr_energy",sr_energy/far_energy/ir_p10 presentes,Le stress physique est calculable.
Q1-H-03,Q1,NaN,NaN,nan,WARN,Concordance marche vs physique,strict=0.00%; concordant_ou_explique=50.00%; n=2; explained=1; reasons=lag_within_1y:1;year_gap_unexplained:1,bascule_year_market et bascule_year_physical comparables,Concordance partielle; divergences a expliquer pays par pays.
Q1-H-04,Q1,NaN,NaN,nan,PASS,Robustesse seuils,1.000,delta bascules sous choc de seuil <= 50%,Proxy de robustesse du diagnostic de bascule.
Q1-S-01,Q1,NaN,NaN,BASE,PASS,Bascule projetee par scenario,2,Q1_country_summary non vide en SCEN,La bascule projetee est produite.
Q1-S-01,Q1,NaN,NaN,DEMAND_UP,PASS,Bascule projetee par scenario,2,Q1_country_summary non vide en SCEN,La bascule projetee est produite.
Q1-S-01,Q1,NaN,NaN,LOW_RIGIDITY,PASS,Bascule projetee par scenario,2,Q1_country_summary non vide en SCEN,La bascule projetee est produite.
Q1-S-02,Q1,NaN,NaN,BASE,PASS,Effets DEMAND_UP/LOW_RIGIDITY,reference_scenario,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),BASE est la reference explicite pour le calcul de sensibilite; pas de delta attendu.
Q1-S-02,Q1,NaN,NaN,DEMAND_UP,WARN,Effets DEMAND_UP/LOW_RIGIDITY,finite_share=100.00%; nonzero_share=0.00%; req_defined=100.00%; n_countries=2,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),Delta vs BASE defini mais nul sur tous les pays.
Q1-S-02,Q1,NaN,NaN,LOW_RIGIDITY,WARN,Effets DEMAND_UP/LOW_RIGIDITY,finite_share=100.00%; nonzero_share=0.00%; req_defined=100.00%; n_countries=2,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),Delta vs BASE defini mais nul sur tous les pays.
Q1-S-03,Q1,NaN,NaN,BASE,PASS,Qualite de causalite,100.00%,part regime_coherence >= seuil min,La coherence scenario est lisible.
Q1-S-03,Q1,NaN,NaN,DEMAND_UP,PASS,Qualite de causalite,100.00%,part regime_coherence >= seuil min,La coherence scenario est lisible.
Q1-S-03,Q1,NaN,NaN,LOW_RIGIDITY,PASS,Qualite de causalite,100.00%,part regime_coherence >= seuil min,La coherence scenario est lisible.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2018,DEMAND_UP,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,DE 2018: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2018,LOW_RIGIDITY,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,DE 2018: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2021,DEMAND_UP,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,DE 2021: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2021,LOW_RIGIDITY,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,DE 2021: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2022,DEMAND_UP,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,DE 2022: capture-only sans low-price ni stress physique.
Q1_S02_NO_SENSITIVITY,Q1,NaN,NaN,NaN,WARN,Q1_S02_NO_SENSITIVITY,NaN,NaN,Q1-S-02: aucune sensibilite scenario non-BASE clairement observable vs BASE.
TEST_DATA_001,Q1,DE,2018,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2018,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2019,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2019,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2020,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2020,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2021,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2021,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2022,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2022,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2023,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2023,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2024,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2024,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2018,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2018,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2019,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2019,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2020,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2020,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2021,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2021,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2022,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2022,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2023,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2023,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2024,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2024,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2035: n_hours=8760 coherent.
TEST_DATA_002,Q1,DE,2018,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2018: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2018,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2018: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2018: coverage price/load ok (100.00%/99.89%).
TEST_DATA_002,Q1,DE,2019,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2019: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,DE,2019,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2019: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,DE,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2020,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2020: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,DE,2020,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2020: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,DE,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2021,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2021: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,DE,2021,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2021: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,DE,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2022,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2022: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,DE,2022,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2022: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,DE,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2023,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2023: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,DE,2023,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2023: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,DE,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2024,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2024: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,DE,2024,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2024: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,DE,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2018,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2018: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2018,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2018: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2018: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q1,ES,2019,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2019: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2019,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2019: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2020,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2020: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2020,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2020: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2021,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2021: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2021,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2021: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2022,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2022: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2022,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2022: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2023,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2023: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2023,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2023: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2024,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2024: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2024,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2024: coverage price/load ok (99.99%/100.00%).
TEST_DATA_002,Q1,ES,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_003,Q1,DE,2018,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2018,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2019,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2019,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2020,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2020,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2021,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2021,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2022,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2022,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2023,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2023,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2024,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2024,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2018,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2018,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2019,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2019,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2020,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2020,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2021,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2021,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2022,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2022,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2023,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2023,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2024,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2024,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2035: prix dans plage large attendue.
TEST_Q1_001,Q1,NaN,NaN,DEMAND_UP,PASS,TEST_Q1_001,NaN,NaN,Toutes les lignes stage2 ont au moins un signal low-price (h_negative/h_below_5).
TEST_Q1_001,Q1,NaN,NaN,LOW_RIGIDITY,PASS,TEST_Q1_001,NaN,NaN,Toutes les lignes stage2 ont au moins un signal low-price (h_negative/h_below_5).
TEST_Q1_001,Q1,NaN,NaN,NaN,PASS,TEST_Q1_001,NaN,NaN,Toutes les lignes stage2 ont au moins un signal low-price (h_negative/h_below_5).
BUNDLE_BASE_FALLBACK_HIST,Q2,NaN,NaN,BASE,WARN,BUNDLE_BASE_FALLBACK_HIST,NaN,NaN,Scenario BASE absent: fallback explicite sur les sorties historiques.
BUNDLE_INFORMATIVENESS,Q2,NaN,NaN,NaN,PASS,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=100.00% ; share_compare_informatifs=66.67%
BUNDLE_LEDGER_STATUS,Q2,NaN,NaN,NaN,PASS,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=0"
BUNDLE_NON_NEGATIVE_FIELD_NEGATIVE,Q2,NaN,NaN,NaN,PASS,BUNDLE_NON_NEGATIVE_FIELD_NEGATIVE,NaN,NaN,Tous les champs *_non_negative restent >= 0.
Q2-H-01,Q2,NaN,NaN,nan,PASS,Pentes OLS post-bascule,4,Q2_country_slopes non vide,Les pentes historiques sont calculees.
Q2-H-02,Q2,NaN,NaN,nan,PASS,Robustesse statistique,"n,p_value,r2","colonnes r2,p_value,n presentes",La robustesse statistique est lisible.
Q2-H-03,Q2,NaN,NaN,nan,PASS,Drivers physiques,4,driver correlations non vides,Les drivers de pente sont disponibles.
Q2-S-01,Q2,NaN,NaN,BASE,PASS,Pentes projetees,4,Q2_country_slopes non vide en SCEN,Pentes prospectives calculees.
Q2-S-01,Q2,NaN,NaN,HIGH_CO2,PASS,Pentes projetees,4,Q2_country_slopes non vide en SCEN,Pentes prospectives calculees.
Q2-S-01,Q2,NaN,NaN,HIGH_GAS,PASS,Pentes projetees,4,Q2_country_slopes non vide en SCEN,Pentes prospectives calculees.
Q2-S-02,Q2,NaN,NaN,BASE,PASS,Delta pente vs BASE,finite=100.00%; robust=0.00%; reason_known=100.00%,delta slope par pays/tech vs BASE,Delta de pente exploitable directionnellement; robustesse statistique a lire a part.
Q2-S-02,Q2,NaN,NaN,HIGH_CO2,PASS,Delta pente vs BASE,finite=100.00%; robust=100.00%; reason_known=100.00%,delta slope par pays/tech vs BASE,Delta de pente exploitable directionnellement; robustesse statistique a lire a part.
Q2-S-02,Q2,NaN,NaN,HIGH_GAS,PASS,Delta pente vs BASE,finite=100.00%; robust=100.00%; reason_known=100.00%,delta slope par pays/tech vs BASE,Delta de pente exploitable directionnellement; robustesse statistique a lire a part.
Q2_POSITIVE_ROBUST_SLOPE,Q2,NaN,NaN,HIGH_CO2,WARN,Q2_POSITIVE_ROBUST_SLOPE,NaN,NaN,ES-PV: pente robuste positive (exception possible meteo/structure).
Q2_POSITIVE_ROBUST_SLOPE,Q2,NaN,NaN,HIGH_GAS,WARN,Q2_POSITIVE_ROBUST_SLOPE,NaN,NaN,ES-PV: pente robuste positive (exception possible meteo/structure).
TEST_DATA_001,Q2,DE,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q2,DE,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2023: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2024: n_hours=8784 coherent.
TEST_DATA_001,Q2,DE,2025,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2025,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2026,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2026,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2027,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2027,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2028,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,DE,2028,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,DE,2029,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2029,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2030,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2030,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2031,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2031,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2032,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,DE,2032,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,DE,2033,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2033,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2034,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2034,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2035,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2035,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2018: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2019: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2020: n_hours=8784 coherent.
TEST_DATA_001,Q2,ES,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2021: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2022: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2023: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2024: n_hours=8784 coherent.
TEST_DATA_001,Q2,ES,2025,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2025,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2026,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2026,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2027,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2027,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2028,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,ES,2028,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,ES,2029,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2029,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2030,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2030,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2031,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2031,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2032,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,ES,2032,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,ES,2033,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2033,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2034,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2034,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2035,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,ES-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2035,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,ES-2035: n_hours=8760 coherent.
TEST_DATA_002,Q2,DE,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2018: coverage price/load ok (100.00%/99.89%).
TEST_DATA_002,Q2,DE,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,DE,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,DE,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,DE,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,DE,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,DE,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,DE,2025,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2025,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2026,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2026,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2027,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2027,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2028,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2028,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2029,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2029,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2030,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2030,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2031,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2031,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2032,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2032,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2033,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2033,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2034,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2034,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2035,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2035,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2018: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q2,ES,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,ES,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,ES,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,ES,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,ES,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,ES,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,ES,2025,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2025,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2026,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2026,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2027,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2027,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2028,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2028,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2029,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2029,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2030,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2030,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2031,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2031,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2032,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2032,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2033,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2033,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2034,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2034,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2035,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2035,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_003,Q2,DE,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2018: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2019: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2020: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2021: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2022: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2023: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2024: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2025,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2025,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2026,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2026,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2027,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2027,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2028,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2028,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2029,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2029,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2030,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2030,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2031,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2031,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2032,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2032,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2033,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2033,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2034,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2034,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2035,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2035,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2018: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2019: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2020: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2021: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2022: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2023: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2024: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2025,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2025,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2026,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2026,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2027,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2027,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2028,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2028,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2029,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2029,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2030,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2030,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2031,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2031,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2032,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2032,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2033,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2033,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2034,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2034,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2035,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,ES-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2035,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,ES-2035: prix dans plage large attendue.
TEST_Q2_001,Q2,NaN,NaN,HIGH_CO2,PASS,TEST_Q2_001,NaN,NaN,r2 present pour les OLS (n>=3) ou justification explicite quand OLS impossible.
TEST_Q2_001,Q2,NaN,NaN,HIGH_GAS,PASS,TEST_Q2_001,NaN,NaN,r2 present pour les OLS (n>=3) ou justification explicite quand OLS impossible.
TEST_Q2_001,Q2,NaN,NaN,NaN,PASS,TEST_Q2_001,NaN,NaN,r2 present pour les OLS (n>=3) ou justification explicite quand OLS impossible.
TEST_Q2_002,Q2,NaN,NaN,HIGH_CO2,PASS,TEST_Q2_002,NaN,NaN,Aucun cas physiquement suspect (slope>0 et corr_vre_load fortement negative).
TEST_Q2_002,Q2,NaN,NaN,HIGH_GAS,PASS,TEST_Q2_002,NaN,NaN,Aucun cas physiquement suspect (slope>0 et corr_vre_load fortement negative).
TEST_Q2_002,Q2,NaN,NaN,NaN,PASS,TEST_Q2_002,NaN,NaN,Aucun cas physiquement suspect (slope>0 et corr_vre_load fortement negative).
TEST_Q2_2022_001,Q2,NaN,NaN,HIGH_CO2,PASS,TEST_Q2_2022_001,NaN,NaN,exclude_year_2022=1 respecte: 2022 absent de tous les years_used.
TEST_Q2_2022_001,Q2,NaN,NaN,HIGH_GAS,PASS,TEST_Q2_2022_001,NaN,NaN,exclude_year_2022=1 respecte: 2022 absent de tous les years_used.
TEST_Q2_2022_001,Q2,NaN,NaN,NaN,PASS,TEST_Q2_2022_001,NaN,NaN,exclude_year_2022=1 respecte: 2022 absent de tous les years_used.
BUNDLE_INFORMATIVENESS,Q3,NaN,NaN,NaN,WARN,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=25.00% ; share_compare_informatifs=0.00%
BUNDLE_LEDGER_STATUS,Q3,NaN,NaN,NaN,PASS,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=0"
BUNDLE_NON_NEGATIVE_FIELD_NEGATIVE,Q3,NaN,NaN,NaN,PASS,BUNDLE_NON_NEGATIVE_FIELD_NEGATIVE,NaN,NaN,Tous les champs *_non_negative restent >= 0.
Q3-H-01,Q3,NaN,NaN,nan,PASS,Tendances glissantes,2,Q3_status non vide,Les tendances historiques sont calculees.
Q3-H-02,Q3,NaN,NaN,nan,PASS,Statuts sortie phase 2,1,status dans ensemble attendu,Les statuts business sont renseignes.
Q3-S-01,Q3,NaN,NaN,BASE,NON_TESTABLE,Conditions minimales d'inversion,hors_scope=100.00%,"inversion_k, inversion_r et additional_absorbed presentes",Scenario majoritairement hors scope Stage 2: test non interpretable.
Q3-S-01,Q3,NaN,NaN,DEMAND_UP,NON_TESTABLE,Conditions minimales d'inversion,hors_scope=100.00%,"inversion_k, inversion_r et additional_absorbed presentes",Scenario majoritairement hors scope Stage 2: test non interpretable.
Q3-S-01,Q3,NaN,NaN,LOW_RIGIDITY,NON_TESTABLE,Conditions minimales d'inversion,hors_scope=100.00%,"inversion_k, inversion_r et additional_absorbed presentes",Scenario majoritairement hors scope Stage 2: test non interpretable.
Q3-S-02,Q3,NaN,NaN,BASE,NON_TESTABLE,Validation entree phase 3,hors_scope=100.00%,status non vide en SCEN,Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3.
Q3-S-02,Q3,NaN,NaN,DEMAND_UP,NON_TESTABLE,Validation entree phase 3,hors_scope=100.00%,status non vide en SCEN,Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3.
Q3-S-02,Q3,NaN,NaN,LOW_RIGIDITY,NON_TESTABLE,Validation entree phase 3,hors_scope=100.00%,status non vide en SCEN,Le scenario ne produit pas assez de stress Stage 2 pour conclure sur l'entree Phase 3.
TEST_DATA_001,Q3,DE,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2023: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2024: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2025,BASE,PASS,TEST_DATA_001,NaN,NaN,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2026,BASE,PASS,TEST_DATA_001,NaN,NaN,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2027,BASE,PASS,TEST_DATA_001,NaN,NaN,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2028,BASE,PASS,TEST_DATA_001,NaN,NaN,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2029,BASE,PASS,TEST_DATA_001,NaN,NaN,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2030,BASE,PASS,TEST_DATA_001,NaN,NaN,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2031,BASE,PASS,TEST_DATA_001,NaN,NaN,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2032,BASE,PASS,TEST_DATA_001,NaN,NaN,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2033,BASE,PASS,TEST_DATA_001,NaN,NaN,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2034,BASE,PASS,TEST_DATA_001,NaN,NaN,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2035,BASE,PASS,TEST_DATA_001,NaN,NaN,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2018: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2019: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2020: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2021: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2022: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2023: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2024: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2025,BASE,PASS,TEST_DATA_001,NaN,NaN,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2026,BASE,PASS,TEST_DATA_001,NaN,NaN,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2027,BASE,PASS,TEST_DATA_001,NaN,NaN,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2028,BASE,PASS,TEST_DATA_001,NaN,NaN,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2029,BASE,PASS,TEST_DATA_001,NaN,NaN,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2030,BASE,PASS,TEST_DATA_001,NaN,NaN,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2031,BASE,PASS,TEST_DATA_001,NaN,NaN,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2032,BASE,PASS,TEST_DATA_001,NaN,NaN,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2033,BASE,PASS,TEST_DATA_001,NaN,NaN,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2034,BASE,PASS,TEST_DATA_001,NaN,NaN,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2035,BASE,PASS,TEST_DATA_001,NaN,NaN,ES-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2035: n_hours=8760 coherent.
TEST_DATA_002,Q3,DE,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2018: coverage price/load ok (100.00%/99.89%).
TEST_DATA_002,Q3,DE,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2025,BASE,PASS,TEST_DATA_002,NaN,NaN,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2026,BASE,PASS,TEST_DATA_002,NaN,NaN,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2027,BASE,PASS,TEST_DATA_002,NaN,NaN,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2028,BASE,PASS,TEST_DATA_002,NaN,NaN,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2029,BASE,PASS,TEST_DATA_002,NaN,NaN,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2030,BASE,PASS,TEST_DATA_002,NaN,NaN,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2031,BASE,PASS,TEST_DATA_002,NaN,NaN,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2032,BASE,PASS,TEST_DATA_002,NaN,NaN,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2033,BASE,PASS,TEST_DATA_002,NaN,NaN,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2034,BASE,PASS,TEST_DATA_002,NaN,NaN,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2035,BASE,PASS,TEST_DATA_002,NaN,NaN,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2018: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q3,ES,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2025,BASE,PASS,TEST_DATA_002,NaN,NaN,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2026,BASE,PASS,TEST_DATA_002,NaN,NaN,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2027,BASE,PASS,TEST_DATA_002,NaN,NaN,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2028,BASE,PASS,TEST_DATA_002,NaN,NaN,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2029,BASE,PASS,TEST_DATA_002,NaN,NaN,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2030,BASE,PASS,TEST_DATA_002,NaN,NaN,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2031,BASE,PASS,TEST_DATA_002,NaN,NaN,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2032,BASE,PASS,TEST_DATA_002,NaN,NaN,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2033,BASE,PASS,TEST_DATA_002,NaN,NaN,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2034,BASE,PASS,TEST_DATA_002,NaN,NaN,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2035,BASE,PASS,TEST_DATA_002,NaN,NaN,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_003,Q3,DE,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2018: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2019: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2020: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2021: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2022: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2023: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2024: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2025,BASE,PASS,TEST_DATA_003,NaN,NaN,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2026,BASE,PASS,TEST_DATA_003,NaN,NaN,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2027,BASE,PASS,TEST_DATA_003,NaN,NaN,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2028,BASE,PASS,TEST_DATA_003,NaN,NaN,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2029,BASE,PASS,TEST_DATA_003,NaN,NaN,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2030,BASE,PASS,TEST_DATA_003,NaN,NaN,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2031,BASE,PASS,TEST_DATA_003,NaN,NaN,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2032,BASE,PASS,TEST_DATA_003,NaN,NaN,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2033,BASE,PASS,TEST_DATA_003,NaN,NaN,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2034,BASE,PASS,TEST_DATA_003,NaN,NaN,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2035,BASE,PASS,TEST_DATA_003,NaN,NaN,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2018: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2019: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2020: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2021: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2022: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2023: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2024: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2025,BASE,PASS,TEST_DATA_003,NaN,NaN,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2026,BASE,PASS,TEST_DATA_003,NaN,NaN,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2027,BASE,PASS,TEST_DATA_003,NaN,NaN,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2028,BASE,PASS,TEST_DATA_003,NaN,NaN,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2029,BASE,PASS,TEST_DATA_003,NaN,NaN,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2030,BASE,PASS,TEST_DATA_003,NaN,NaN,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2031,BASE,PASS,TEST_DATA_003,NaN,NaN,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2032,BASE,PASS,TEST_DATA_003,NaN,NaN,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2033,BASE,PASS,TEST_DATA_003,NaN,NaN,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2034,BASE,PASS,TEST_DATA_003,NaN,NaN,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2035,BASE,PASS,TEST_DATA_003,NaN,NaN,ES-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2035: prix dans plage large attendue.
TEST_Q3_001,Q3,NaN,NaN,BASE,WARN,TEST_Q3_001,NaN,NaN,Colonnes predicted/target non disponibles dans Q3_status; test non applicable.
TEST_Q3_001,Q3,NaN,NaN,DEMAND_UP,WARN,TEST_Q3_001,NaN,NaN,Colonnes predicted/target non disponibles dans Q3_status; test non applicable.
TEST_Q3_001,Q3,NaN,NaN,LOW_RIGIDITY,WARN,TEST_Q3_001,NaN,NaN,Colonnes predicted/target non disponibles dans Q3_status; test non applicable.
TEST_Q3_001,Q3,NaN,NaN,NaN,PASS,TEST_Q3_001,NaN,NaN,Toutes les lignes within_bounds=true respectent target_sr/target_h_negative/target_h_below_5.
BUNDLE_INFORMATIVENESS,Q4,NaN,NaN,NaN,PASS,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=100.00% ; share_compare_informatifs=82.35%
BUNDLE_LEDGER_STATUS,Q4,NaN,NaN,NaN,PASS,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=0"
BUNDLE_NON_NEGATIVE_FIELD_NEGATIVE,Q4,NaN,NaN,NaN,PASS,BUNDLE_NON_NEGATIVE_FIELD_NEGATIVE,NaN,NaN,Tous les champs *_non_negative restent >= 0.
GRID_BOUNDARY_SOLUTION,Q4,NaN,NaN,NaN,WARN,GRID_BOUNDARY_SOLUTION,NaN,NaN,Objectif atteint mais solution situee en bord de grille; affiner/etendre la grille.
GRID_BOUNDARY_SOLUTION,Q4,NaN,NaN,NaN,WARN,GRID_BOUNDARY_SOLUTION,NaN,NaN,Objectif atteint mais solution situee en bord de grille; affiner/etendre la grille.
Q4-H-01,Q4,NaN,NaN,nan,PASS,Simulation BESS 3 modes,"extra_dispatch_modes_executed=2; total_dispatch_modes_executed=3; extras=HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED",3 modes executes avec sorties non vides,Convention explicite: les modes supplementaires sont comptes hors SURPLUS_FIRST.
Q4-H-02,Q4,NaN,NaN,nan,PASS,Invariants physiques BESS,WARN,aucun FAIL physique/structurel pertinent,Les invariants physiques batterie sont respectes. Des avertissements non-physiques peuvent subsister (objectif/scenario).
Q4-S-01,Q4,NaN,NaN,BASE,PASS,Comparaison effet batteries par scenario,2,Q4 summary non vide pour >=1 scenario,Resultats Q4 prospectifs disponibles.
Q4-S-01,Q4,NaN,NaN,HIGH_CO2,PASS,Comparaison effet batteries par scenario,2,Q4 summary non vide pour >=1 scenario,Resultats Q4 prospectifs disponibles.
Q4-S-01,Q4,NaN,NaN,HIGH_GAS,PASS,Comparaison effet batteries par scenario,2,Q4 summary non vide pour >=1 scenario,Resultats Q4 prospectifs disponibles.
Q4-S-02,Q4,NaN,NaN,BASE,PASS,Sensibilite valeur commodites,share_finite=100.00%,delta pv_capture ou revenus vs BASE,Sensibilite valeur exploitable sur le panel.
Q4-S-02,Q4,NaN,NaN,HIGH_CO2,PASS,Sensibilite valeur commodites,share_finite=100.00%,delta pv_capture ou revenus vs BASE,Sensibilite valeur exploitable sur le panel.
Q4-S-02,Q4,NaN,NaN,HIGH_GAS,PASS,Sensibilite valeur commodites,share_finite=100.00%,delta pv_capture ou revenus vs BASE,Sensibilite valeur exploitable sur le panel.
Q4_REPORTING_CONSISTENCY,Q4,NaN,NaN,NaN,PASS,Q4_REPORTING_CONSISTENCY,NaN,NaN,"Comparaison Q4 coherente avec Q4_sizing_summary (meme colonnes, meme valeurs)."
TEST_Q4_001,Q4,NaN,NaN,BASE,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,BASE,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,NaN,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,NaN,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_002,Q4,NaN,NaN,BASE,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,BASE,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,NaN,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,NaN,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
BUNDLE_INFORMATIVENESS,Q5,NaN,NaN,NaN,PASS,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=100.00% ; share_compare_informatifs=100.00%
BUNDLE_LEDGER_STATUS,Q5,NaN,NaN,NaN,PASS,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=0"
BUNDLE_NON_NEGATIVE_FIELD_NEGATIVE,Q5,NaN,NaN,NaN,PASS,BUNDLE_NON_NEGATIVE_FIELD_NEGATIVE,NaN,NaN,Tous les champs *_non_negative restent >= 0.
Q5-H-01,Q5,NaN,NaN,nan,PASS,Ancre thermique historique,share_fini=100.00%,Q5_summary non vide avec ttl_obs et tca_q95,L'ancre thermique est quantifiable sur la majorite des pays.
Q5-H-02,Q5,NaN,NaN,nan,PASS,Sensibilites analytiques,share_positive=100.00%,dTCA_dCO2 > 0 et dTCA_dGas > 0,Sensibilites analytiques globalement coherentes.
Q5-S-01,Q5,NaN,NaN,BASE,PASS,Sensibilites scenarisees,2,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-01,Q5,NaN,NaN,HIGH_BOTH,PASS,Sensibilites scenarisees,2,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-01,Q5,NaN,NaN,HIGH_CO2,PASS,Sensibilites scenarisees,2,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-01,Q5,NaN,NaN,HIGH_GAS,PASS,Sensibilites scenarisees,2,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-02,Q5,NaN,NaN,BASE,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5-S-02,Q5,NaN,NaN,HIGH_BOTH,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5-S-02,Q5,NaN,NaN,HIGH_CO2,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5-S-02,Q5,NaN,NaN,HIGH_GAS,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5_ALPHA_NEGATIVE,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,NaN,NaN,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,NaN,NaN,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_BASE_SCENARIO_MISSING,Q5,NaN,NaN,HIGH_BOTH,PASS,Q5_BASE_SCENARIO_MISSING,NaN,NaN,BASE reference resolved (ok or warn_fallback_from_hist) for all countries.
Q5_BASE_SCENARIO_MISSING,Q5,NaN,NaN,HIGH_CO2,PASS,Q5_BASE_SCENARIO_MISSING,NaN,NaN,BASE reference resolved (ok or warn_fallback_from_hist) for all countries.
Q5_BASE_SCENARIO_MISSING,Q5,NaN,NaN,HIGH_GAS,PASS,Q5_BASE_SCENARIO_MISSING,NaN,NaN,BASE reference resolved (ok or warn_fallback_from_hist) for all countries.
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,BASE,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=35.7 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,BASE,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=28.4 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=65.9 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=44.5 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=37.7 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=29.3 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=38.3 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=30.3 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,NaN,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=8.6 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,NaN,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=23.7 EUR/MWh (acceptable).
Q5_LOW_CORR_CD,Q5,NaN,NaN,BASE,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_REPORTING_TTL_OBS_CONSISTENCY,Q5,NaN,NaN,NaN,PASS,Q5_REPORTING_TTL_OBS_CONSISTENCY,NaN,NaN,ttl_obs comparaison/detail coherent (moyennes alignees).
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
TEST_Q5_001,Q5,NaN,NaN,NaN,PASS,TEST_Q5_001,NaN,NaN,HIGH_CO2/HIGH_GAS: TCA scenario >= BASE sur les paires comparables.
TEST_Q5_002,Q5,NaN,NaN,NaN,PASS,TEST_Q5_002,NaN,NaN,Coherence signe delta_ttl vs delta_tca: 100.0% (4/4).
```
