# Extrait Data Outil v7

## AUDIT PAYLOAD

### Inputs

#### run_metadata
```json
{
  "run_id": "FULL_20260212_ALLQ",
  "run_dir": "C:\\Users\\cval-tlacour\\OneDrive - CVA corporate value associate GmbH\\Desktop\\automation-stack\\projects\\tte-capture-prices-v2\\outputs\\combined\\FULL_20260212_ALLQ",
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
DE,2018,HIST,8760,Europe/Berlin,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,153891.6974999999,0.0002671835702335,0.008904109589041,1.0,NaN,NaN,0.3794941270703111,44.47275456621005,72.28749999999995,43.77257363689873,0.9842559576949768,0.6055344788089055,38.17753675887097,0.8584477649576012,0.5281346949178073,133,232,38,0.988812785388128,0.6964810903936534,NaN,NaN,NaN,NaN,OK,NaN
DE,2019,HIST,8760,Europe/Berlin,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,285774.3125,0.000554157034082,0.0156392694063926,0.9876496247366532,NaN,NaN,0.2843253281938316,37.669692887315904,58.38,34.906182773392544,0.926638368882113,0.5979133739875393,32.78952818581776,0.8704485137137555,0.5616568719735827,211,335,31,0.9990866537275944,0.813246051355149,NaN,NaN,NaN,NaN,OK,NaN
DE,2020,HIST,8784,Europe/Berlin,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,345342.565,0.0006991788301744,0.0159380692167577,1.0,NaN,NaN,0.2439759191136415,30.47081976545599,55.338,24.511203174738068,0.8044156134757428,0.4429361952860253,25.24537518940176,0.8285098787536335,0.4562032453178966,298,598,42,0.9982921553000114,0.7903113754356191,NaN,NaN,NaN,NaN,OK,NaN
DE,2021,HIST,8760,Europe/Berlin,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,185328.96,0.0003675803989361,0.0087899543378995,1.0,NaN,NaN,0.2701548827424477,96.86022947825094,249.9639999999992,75.45790652091513,0.7790391053931841,0.3018750960974995,83.19114655913475,0.8588782724060605,0.3328125112381583,139,248,202,0.9737412946683413,0.5221576401467792,NaN,NaN,NaN,NaN,OK,NaN
DE,2022,HIST,8760,Europe/Berlin,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,904994.6575,0.001843457392513,0.042579908675799,1.0,NaN,NaN,0.3104147117931071,235.4667222285649,513.6109999999999,222.2697802958073,0.9439541103394328,0.4327589952236369,173.5038161884555,0.7368506876315086,0.3378117216890906,69,161,358,0.9733987898161892,0.5909121520525994,NaN,NaN,NaN,NaN,OK,NaN
DE,2023,HIST,8760,Europe/Berlin,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2556732.2,0.0057522727927743,0.0775114155251141,1.0,NaN,NaN,0.2390462318859233,95.1827480305971,168.00449999999992,72.18210511017934,0.7583528171195051,0.4296438792423975,79.91071132318326,0.8395503699630048,0.4756462554466297,300,530,340,0.98675647905012,0.8419341186601034,NaN,NaN,NaN,NaN,OK,NaN
DE,2024,HIST,8784,Europe/Berlin,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2948435.059833,0.0068809540140638,0.0757058287795992,1.0,NaN,NaN,0.2263046487454366,78.51545827166116,146.069,46.22796099131209,0.5887752808034911,0.3164803003464944,65.83122843523844,0.838449266989748,0.4506858295410966,457,756,315,0.9939656153933736,0.798724901005636,NaN,NaN,NaN,NaN,OK,NaN
ES,2018,HIST,8760,Europe/Madrid,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1484.0,6.030734663893564e-06,0.0003424657534246,1.0,NaN,NaN,0.2941978481508908,57.30006279255623,73.82749999999999,59.342028861067455,1.0356363670298891,0.8037930156251731,53.09425838495249,0.926600352554062,0.7191664133954488,0,57,5,0.9938349126612628,0.717322385044847,NaN,NaN,NaN,NaN,OK,NaN
ES,2019,HIST,8760,Europe/Madrid,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,3224.0,1.308843921710153e-05,0.0005707762557077,1.0,NaN,NaN,0.2913581991978373,47.67961867793127,64.217,48.57853958864,1.0188533578001284,0.756474758843297,45.65081383781028,0.9574492226159512,0.7108836264199555,0,69,2,0.9956616052060736,0.6819177627648636,NaN,NaN,NaN,NaN,OK,NaN
ES,2020,HIST,8784,Europe/Madrid,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,143823.0,0.0006026351526537,0.0159380692167577,1.0,NaN,NaN,0.3059516604886905,33.95808038255721,51.97899999999999,32.896135604866735,0.9687277736041888,0.6328735759608061,32.37432130900995,0.9533613485890452,0.6228346314667453,0,60,0,0.997609017420016,0.7267869347642084,NaN,NaN,NaN,NaN,OK,NaN
ES,2021,HIST,8760,Europe/Madrid,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,318652.0,0.0012885678805332,0.0231735159817351,1.0,NaN,NaN,0.2859684981487956,111.94053088252085,255.0575,102.39616733438756,0.9147371959656876,0.4014630714030662,103.78184356536732,0.9271158779324008,0.4068958707952807,0,202,130,0.9588994177417514,0.3751809059748108,NaN,NaN,NaN,NaN,OK,NaN
ES,2022,HIST,8760,Europe/Madrid,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,626367.0,0.0023960111216853,0.0438356164383561,1.0,NaN,NaN,0.3049924924924925,167.52426875214064,270.003,151.07895653475305,0.9018332547284886,0.5595454736975258,160.5904117834413,0.958609835933931,0.5947726943161421,0,114,329,0.950907637858203,0.4786983212559283,NaN,NaN,NaN,NaN,OK,NaN
ES,2023,HIST,8760,Europe/Madrid,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2818976.0,0.0115130277941151,0.1315068493150684,0.9995587759526864,NaN,NaN,0.2950851393188854,87.11351866651445,149.328,73.07910508828432,0.8388951130311212,0.4893864853763817,76.31964002657413,0.8760941033588467,0.5110872711519215,0,558,273,0.9366366023518666,0.7478810502523656,NaN,NaN,NaN,NaN,OK,NaN
ES,2024,HIST,8784,Europe/Madrid,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,3567012.0,0.0147292050339075,0.1691712204007286,0.9994023008613372,NaN,NaN,0.2951989701260838,63.03954912899921,140.0,42.80117347476487,0.6789574809169381,0.3057226676768919,55.60947301426717,0.8821362744913085,0.3972105215304798,247,1690,271,0.9461459637936924,0.693152070717716,NaN,NaN,NaN,NaN,OK,NaN
```

### A.2 q1_transition_summary
```csv
country,transition_year,stage,stage2_score,non_capture_flags_count,reason_codes,persistence_window_years,confidence_level
DE,2019,2,2.0,1,LOW_PRICE:h_negative_obs>=200.0 (211.0); VALUE:capture_ratio_wind<=0.90 (0.870),2.0,0.8
ES,2023,2,3.0,4,LOW_PRICE:h_below_5_obs>=500.0 (558.0); LOW_PRICE:low_price_hours_share>=0.057 (0.064); VALUE:capture_ratio_wind<=0.90 (0.876); PHYSICAL:sr_energy>=0.010 (0.012); PHYSICAL:sr_hours>=0.10 (0.132),2.0,1.0
```

### A.3 q2_slope_summary
```csv
scenario_id,country,tech,x_var_used,y_var_used,n_points,years_used,slope,intercept,r2,p_value,driver_stats_phase2,slope_quality_flag,slope_quality_notes
HIGH_CO2,DE,PV,none,capture_ratio_PV,0,nan,NaN,NaN,NaN,NaN,"{""sr_energy_mean"": NaN, ""far_energy_mean"": NaN, ""ir_p10_mean"": NaN, ""ttl_mean"": NaN, ""corr_vre_load_mean"": NaN}",WARN,INSUFFICIENT_POINTS
HIGH_CO2,DE,WIND,none,capture_ratio_WIND,0,nan,NaN,NaN,NaN,NaN,"{""sr_energy_mean"": NaN, ""far_energy_mean"": NaN, ""ir_p10_mean"": NaN, ""ttl_mean"": NaN, ""corr_vre_load_mean"": NaN}",WARN,INSUFFICIENT_POINTS
HIGH_GAS,DE,PV,none,capture_ratio_PV,0,nan,NaN,NaN,NaN,NaN,"{""sr_energy_mean"": NaN, ""far_energy_mean"": NaN, ""ir_p10_mean"": NaN, ""ttl_mean"": NaN, ""corr_vre_load_mean"": NaN}",WARN,INSUFFICIENT_POINTS
HIGH_GAS,DE,WIND,none,capture_ratio_WIND,0,nan,NaN,NaN,NaN,NaN,"{""sr_energy_mean"": NaN, ""far_energy_mean"": NaN, ""ir_p10_mean"": NaN, ""ttl_mean"": NaN, ""corr_vre_load_mean"": NaN}",WARN,INSUFFICIENT_POINTS
HIST,DE,PV,pv_penetration_share_load,capture_ratio_PV,2,"2023,2024",-11.79297599718819,2.179468315458616,NaN,NaN,"{""sr_energy_mean"": 0.006316613403419, ""far_energy_mean"": 1.0, ""ir_p10_mean"": 0.23267544031568, ""ttl_mean"": 157.03674999999996, ""corr_vre_load_mean"": 1.0}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
HIST,DE,WIND,wind_penetration_share_load,capture_ratio_WIND,5,"2019,2020,2021,2023,2024",-0.313292745567829,0.931148477635842,0.4051476994742447,0.2482232666527261,"{""sr_energy_mean"": 0.0028508286140061, ""far_energy_mean"": 0.9975299249473306, ""ir_p10_mean"": 0.2527614021362562, ""ttl_mean"": 135.55109999999982, ""corr_vre_load_mean"": -0.9805629427510812}",WARN,N_LT_6|PVALUE_GT_0_05|LOO_NOT_AVAILABLE
HIGH_CO2,ES,PV,none,capture_ratio_PV,0,nan,NaN,NaN,NaN,NaN,"{""sr_energy_mean"": NaN, ""far_energy_mean"": NaN, ""ir_p10_mean"": NaN, ""ttl_mean"": NaN, ""corr_vre_load_mean"": NaN}",WARN,INSUFFICIENT_POINTS
HIGH_CO2,ES,WIND,none,capture_ratio_WIND,0,nan,NaN,NaN,NaN,NaN,"{""sr_energy_mean"": NaN, ""far_energy_mean"": NaN, ""ir_p10_mean"": NaN, ""ttl_mean"": NaN, ""corr_vre_load_mean"": NaN}",WARN,INSUFFICIENT_POINTS
HIGH_GAS,ES,PV,none,capture_ratio_PV,0,nan,NaN,NaN,NaN,NaN,"{""sr_energy_mean"": NaN, ""far_energy_mean"": NaN, ""ir_p10_mean"": NaN, ""ttl_mean"": NaN, ""corr_vre_load_mean"": NaN}",WARN,INSUFFICIENT_POINTS
HIGH_GAS,ES,WIND,none,capture_ratio_WIND,0,nan,NaN,NaN,NaN,NaN,"{""sr_energy_mean"": NaN, ""far_energy_mean"": NaN, ""ir_p10_mean"": NaN, ""ttl_mean"": NaN, ""corr_vre_load_mean"": NaN}",WARN,INSUFFICIENT_POINTS
HIST,ES,PV,pv_penetration_share_load,capture_ratio_PV,2,"2023,2024",-5.876929761031239,1.875809152071917,NaN,NaN,"{""sr_energy_mean"": 0.0131211164140113, ""far_energy_mean"": 0.9994805384070118, ""ir_p10_mean"": 0.2951420547224846, ""ttl_mean"": 144.664, ""corr_vre_load_mean"": 1.0}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
HIST,ES,WIND,wind_penetration_share_load,capture_ratio_WIND,2,"2023,2024",-0.4812210902486096,1.0043191141153942,NaN,NaN,"{""sr_energy_mean"": 0.0131211164140113, ""far_energy_mean"": 0.9994805384070118, ""ir_p10_mean"": 0.2951420547224846, ""ttl_mean"": 144.664, ""corr_vre_load_mean"": 1.0}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
```

### A.4 q3_inversion_requirements
```csv
country,scenario_id,year,lever,required_uplift,required_uplift_mw,required_uplift_pct_avg_load,required_uplift_twh_per_year,within_bounds,target_sr,target_h_negative,target_h_below_5,predicted_sr_after,predicted_far_after,predicted_h_negative_after,predicted_h_below_5_after,predicted_h_negative_metric,applicability_flag,status,reason
DE,HIST,2024,demand_uplift,8304.697261361387,8304.697261361387,0.1594992220401763,72.94846074379842,True,0.01,200.0,500.0,0.0,1.0,200.0,200.0,MARKET_PROXY_NRL_LOOKUP,APPLICABLE,ok,ok
DE,HIST,2024,export_uplift,NaN,NaN,NaN,NaN,False,0.01,200.0,500.0,0.0,1.0,802.0,802.0,MARKET_PROXY_NRL_LOOKUP,APPLICABLE,not_achievable,not_achievable
DE,HIST,2024,flex_uplift,NaN,NaN,NaN,NaN,False,0.01,200.0,500.0,0.0,1.0,802.0,802.0,MARKET_PROXY_NRL_LOOKUP,APPLICABLE,not_achievable,not_achievable
ES,HIST,2024,demand_uplift,0.0,0.0,0.0,0.0,True,0.01,200.0,500.0,0.0013426692672896,0.9653226280664032,0.0,0.0,MARKET_PROXY_NRL_LOOKUP,APPLICABLE,already_ok,already_ok
ES,HIST,2024,export_uplift,0.0,0.0,0.0,0.0,True,0.01,200.0,500.0,0.0013426692672896,0.9653226280664032,0.0,0.0,MARKET_PROXY_NRL_LOOKUP,APPLICABLE,already_ok,already_ok
ES,HIST,2024,flex_uplift,0.0,0.0,0.0,0.0,True,0.01,200.0,500.0,0.0013426692672896,0.9653226280664032,0.0,0.0,MARKET_PROXY_NRL_LOOKUP,APPLICABLE,already_ok,already_ok
```

### A.5 q4_bess_sizing_curve
```csv
country,scenario_id,year,bess_power_gw,bess_energy_gwh,cycles_realized_per_day,eta_roundtrip,far_energy_after,surplus_unabsorbed_twh_after,h_negative_proxy_after,h_negative_reducible_upper_bound,monotonicity_check_flag,physics_check_flag,on_efficient_frontier,notes
DE,HIGH_CO2,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
DE,HIGH_GAS,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
DE,HIST,2024,NaN,NaN,0.0,0.88,1.0,0.0,457,0,PASS,PASS,True,dispatch_mode=; objective=
ES,HIGH_CO2,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
ES,HIGH_GAS,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
ES,HIST,2024,NaN,NaN,0.0,0.88,0.9994023008613372,0.002132,247,0,PASS,PASS,True,dispatch_mode=; objective=
```

### A.6 q5_anchor_sensitivity
```csv
country,scenario_id,year,gas_eur_per_mwh_th,co2_eur_per_t,tca_ccgt_eur_mwh,tca_coal_eur_mwh,ttl_observed_eur_mwh,ttl_model_eur_mwh,delta_tca_vs_base,delta_ttl_model_vs_base,coherence_flag,ttl_proxy_method,status,reason,base_ref_status,base_ref_reason
DE,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,212.65801522615288,236.30263157894737,NaN,NaN,MISSING_BASE,observed_from_prices,missing_base,base_reference_not_provided,missing_base,base_reference_not_provided
DE,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,228.36196259457392,203.7368421052632,NaN,NaN,MISSING_BASE,observed_from_prices,missing_base,base_reference_not_provided,missing_base,base_reference_not_provided
DE,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,233.3816994366792,191.43421052631575,NaN,NaN,MISSING_BASE,observed_from_prices,missing_base,base_reference_not_provided,missing_base,base_reference_not_provided
DE,HIST,2024,46.9,70.83,114.28665454545454,135.4421842105263,146.069,146.069,0.0,0.0,PASS,observed_from_prices,ok,nan,ok,nan
ES,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,167.7630993635321,180.8181818181818,NaN,NaN,MISSING_BASE,observed_from_prices,missing_base,base_reference_not_provided,missing_base,base_reference_not_provided
ES,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,174.19037209080483,139.9090909090909,NaN,NaN,MISSING_BASE,observed_from_prices,missing_base,base_reference_not_provided,missing_base,base_reference_not_provided
ES,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,182.0812811817139,162.45454545454544,NaN,NaN,MISSING_BASE,observed_from_prices,missing_base,base_reference_not_provided,missing_base,base_reference_not_provided
ES,HIST,2024,47.02,70.69,114.45341818181817,135.49023684210528,140.0,140.0,0.0,0.0,PASS,observed_from_prices,ok,nan,ok,nan
```

## TEST LEDGER

```csv
test_id,scope,country,year,scenario_id,status,metric_name,observed_value,expected_rule,message
BUNDLE_INFORMATIVENESS,Q1,NaN,NaN,NaN,WARN,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=80.00% ; share_compare_informatifs=0.00%
BUNDLE_LEDGER_STATUS,Q1,NaN,NaN,NaN,PASS,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=0"
Q1-H-01,Q1,NaN,NaN,nan,PASS,Score marche de bascule,1.3571428571428572,stage2_market_score present et non vide,Le score de bascule marche est exploitable.
Q1-H-02,Q1,NaN,NaN,nan,PASS,Stress physique SR/FAR/IR,"far_energy,ir_p10,sr_energy",sr_energy/far_energy/ir_p10 presentes,Le stress physique est calculable.
Q1-H-03,Q1,NaN,NaN,nan,PASS,Concordance marche vs physique,strict=50.00%; concordant_ou_explique=100.00%; n=2; explained=2; reasons=physical_not_reached_but_explained:1;strict_equal_year:1,bascule_year_market et bascule_year_physical comparables,Concordance satisfaisante en comptant les divergences expliquees.
Q1-H-04,Q1,NaN,NaN,nan,PASS,Robustesse seuils,0.900,delta bascules sous choc de seuil <= 50%,Proxy de robustesse du diagnostic de bascule.
Q1-S-01,Q1,NaN,NaN,DEMAND_UP,PASS,Bascule projetee par scenario,2,Q1_country_summary non vide en SCEN,La bascule projetee est produite.
Q1-S-01,Q1,NaN,NaN,LOW_RIGIDITY,PASS,Bascule projetee par scenario,2,Q1_country_summary non vide en SCEN,La bascule projetee est produite.
Q1-S-02,Q1,NaN,NaN,DEMAND_UP,NON_TESTABLE,Effets DEMAND_UP/LOW_RIGIDITY,nan,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),Impossible d'evaluer la sensibilite sans BASE et scenario courant.
Q1-S-02,Q1,NaN,NaN,LOW_RIGIDITY,NON_TESTABLE,Effets DEMAND_UP/LOW_RIGIDITY,nan,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),Impossible d'evaluer la sensibilite sans BASE et scenario courant.
Q1-S-03,Q1,NaN,NaN,DEMAND_UP,PASS,Qualite de causalite,100.00%,part regime_coherence >= seuil min,La coherence scenario est lisible.
Q1-S-03,Q1,NaN,NaN,LOW_RIGIDITY,PASS,Qualite de causalite,100.00%,part regime_coherence >= seuil min,La coherence scenario est lisible.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2018,NaN,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,DE 2018: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2021,NaN,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,DE 2021: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2022,NaN,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,DE 2022: capture-only sans low-price ni stress physique.
Q1_S02_NO_SENSITIVITY,Q1,NaN,NaN,NaN,WARN,Q1_S02_NO_SENSITIVITY,NaN,NaN,Q1-S-02: aucune sensibilite scenario non-BASE clairement observable vs BASE.
RC_NEG_NOT_IN_AB,Q1,DE,2018,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,DE-2018: 33.8% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,DE,2019,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,DE-2019: 44.1% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,DE,2020,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,DE-2020: 36.9% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,DE,2021,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,DE-2021: 41.0% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,DE,2018,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"DE-2018: 33.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-3039.5, p50=2341.7, p90=8765.7; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,DE,2019,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"DE-2019: 44.1% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-4050.2, p50=580.8, p90=5229.3; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,DE,2020,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"DE-2020: 36.9% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-3662.8, p50=1184.0, p90=5399.3; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,DE,2021,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"DE-2021: 41.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-4056.4, p50=598.4, p90=5182.9; causes=price_or_regime_mapping)."
TEST_DATA_001,Q1,DE,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2023: n_hours=8760 coherent.
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
TEST_DATA_001,Q1,ES,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2023: n_hours=8760 coherent.
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
TEST_DATA_002,Q1,DE,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2018: coverage price/load ok (100.00%/99.89%).
TEST_DATA_002,Q1,DE,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2023: coverage price/load ok (99.99%/99.99%).
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
TEST_DATA_002,Q1,ES,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2018: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q1,ES,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2023: coverage price/load ok (99.99%/99.99%).
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
TEST_DATA_003,Q1,DE,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2023: prix dans plage large attendue.
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
TEST_DATA_003,Q1,ES,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2023: prix dans plage large attendue.
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
TEST_Q1_001,Q1,NaN,NaN,DEMAND_UP,WARN,TEST_Q1_001,NaN,NaN,Aucune ligne stage2 observee; test non applicable.
TEST_Q1_001,Q1,NaN,NaN,LOW_RIGIDITY,WARN,TEST_Q1_001,NaN,NaN,Aucune ligne stage2 observee; test non applicable.
TEST_Q1_001,Q1,NaN,NaN,NaN,PASS,TEST_Q1_001,NaN,NaN,Toutes les lignes stage2 ont au moins un signal low-price (h_negative/h_below_5/days_spread_gt50).
BUNDLE_INFORMATIVENESS,Q2,NaN,NaN,NaN,WARN,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=100.00% ; share_compare_informatifs=0.00%
BUNDLE_LEDGER_STATUS,Q2,NaN,NaN,NaN,WARN,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=2"
Q2-H-01,Q2,NaN,NaN,nan,PASS,Pentes OLS post-bascule,4,Q2_country_slopes non vide,Les pentes historiques sont calculees.
Q2-H-02,Q2,NaN,NaN,nan,PASS,Robustesse statistique,"n,p_value,r2","colonnes r2,p_value,n presentes",La robustesse statistique est lisible.
Q2-H-03,Q2,NaN,NaN,nan,PASS,Drivers physiques,4,driver correlations non vides,Les drivers de pente sont disponibles.
Q2-S-01,Q2,NaN,NaN,HIGH_CO2,PASS,Pentes projetees,4,Q2_country_slopes non vide en SCEN,Pentes prospectives calculees.
Q2-S-01,Q2,NaN,NaN,HIGH_GAS,PASS,Pentes projetees,4,Q2_country_slopes non vide en SCEN,Pentes prospectives calculees.
Q2-S-02,Q2,NaN,NaN,HIGH_CO2,WARN,Delta pente vs BASE,finite=0.00%; robust=0.00%; reason_known=100.00%,delta slope par pays/tech vs BASE,Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable.
Q2-S-02,Q2,NaN,NaN,HIGH_GAS,WARN,Delta pente vs BASE,finite=0.00%; robust=0.00%; reason_known=100.00%,delta slope par pays/tech vs BASE,Pentes non finies mais raisons explicites (insufficient_points/q1_no_bascule); limitation interpretable.
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
BUNDLE_INFORMATIVENESS,Q3,NaN,NaN,NaN,WARN,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=100.00% ; share_compare_informatifs=0.00%
BUNDLE_LEDGER_STATUS,Q3,NaN,NaN,NaN,PASS,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=0"
Q3-H-01,Q3,NaN,NaN,nan,PASS,Tendances glissantes,2,Q3_status non vide,Les tendances historiques sont calculees.
Q3-H-02,Q3,NaN,NaN,nan,PASS,Statuts sortie phase 2,2,status dans ensemble attendu,Les statuts business sont renseignes.
Q3-S-01,Q3,NaN,NaN,DEMAND_UP,PASS,Conditions minimales d'inversion,hors_scope=100.00%; inversion=0,"inversion_k, inversion_r et additional_absorbed presentes",Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites.
Q3-S-01,Q3,NaN,NaN,LOW_RIGIDITY,PASS,Conditions minimales d'inversion,hors_scope=100.00%; inversion=0,"inversion_k, inversion_r et additional_absorbed presentes",Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites.
Q3-S-02,Q3,NaN,NaN,DEMAND_UP,PASS,Validation entree phase 3,hors_scope=100.00%; inversion=0,status non vide en SCEN,Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise.
Q3-S-02,Q3,NaN,NaN,LOW_RIGIDITY,PASS,Validation entree phase 3,hors_scope=100.00%; inversion=0,status non vide en SCEN,Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise.
TEST_DATA_001,Q3,DE,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2023: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,DE-2024: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2018: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2019: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2020: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2021: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2022: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2023: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,ES-2024: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,ES-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,ES-2035: n_hours=8760 coherent.
TEST_DATA_002,Q3,DE,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2018: coverage price/load ok (100.00%/99.89%).
TEST_DATA_002,Q3,DE,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,DE-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2018: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q3,ES,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,ES-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_003,Q3,DE,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2018: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2019: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2020: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2021: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2022: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2023: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,DE-2024: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2018: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2019: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2020: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2021: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2022: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2023: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,ES-2024: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,ES-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,ES-2035: prix dans plage large attendue.
TEST_Q3_001,Q3,NaN,NaN,DEMAND_UP,PASS,TEST_Q3_001,NaN,NaN,Toutes les lignes within_bounds=true respectent target_sr/target_h_negative/target_h_below_5.
TEST_Q3_001,Q3,NaN,NaN,LOW_RIGIDITY,PASS,TEST_Q3_001,NaN,NaN,Toutes les lignes within_bounds=true respectent target_sr/target_h_negative/target_h_below_5.
TEST_Q3_001,Q3,NaN,NaN,NaN,PASS,TEST_Q3_001,NaN,NaN,Toutes les lignes within_bounds=true respectent target_sr/target_h_negative/target_h_below_5.
BUNDLE_INFORMATIVENESS,Q4,NaN,NaN,NaN,PASS,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=100.00% ; share_compare_informatifs=62.50%
BUNDLE_LEDGER_STATUS,Q4,NaN,NaN,NaN,PASS,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=0"
Q4-H-01,Q4,NaN,NaN,nan,PASS,Simulation BESS 3 modes,"HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED",3 modes executes avec sorties non vides,Les trois modes Q4 sont disponibles.
Q4-H-02,Q4,NaN,NaN,nan,PASS,Invariants physiques BESS,PASS,aucun FAIL physique/structurel pertinent,Les invariants physiques batterie sont respectes.
Q4-S-01,Q4,NaN,NaN,HIGH_CO2,PASS,Comparaison effet batteries par scenario,2,Q4 summary non vide pour >=1 scenario,Resultats Q4 prospectifs disponibles.
Q4-S-01,Q4,NaN,NaN,HIGH_GAS,PASS,Comparaison effet batteries par scenario,2,Q4 summary non vide pour >=1 scenario,Resultats Q4 prospectifs disponibles.
Q4-S-02,Q4,NaN,NaN,HIGH_CO2,PASS,Sensibilite valeur commodites,share_finite=100.00%,delta pv_capture ou revenus vs BASE,Sensibilite valeur exploitable sur le panel.
Q4-S-02,Q4,NaN,NaN,HIGH_GAS,PASS,Sensibilite valeur commodites,share_finite=100.00%,delta pv_capture ou revenus vs BASE,Sensibilite valeur exploitable sur le panel.
TEST_Q4_001,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,NaN,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,NaN,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_002,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,NaN,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,NaN,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
BUNDLE_INFORMATIVENESS,Q5,NaN,NaN,NaN,PASS,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=100.00% ; share_compare_informatifs=100.00%
BUNDLE_LEDGER_STATUS,Q5,NaN,NaN,NaN,PASS,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=0"
Q5-H-01,Q5,NaN,NaN,nan,PASS,Ancre thermique historique,share_fini=100.00%,Q5_summary non vide avec ttl_obs et tca_q95,L'ancre thermique est quantifiable sur la majorite des pays.
Q5-H-02,Q5,NaN,NaN,nan,PASS,Sensibilites analytiques,share_positive=100.00%,dTCA_dCO2 > 0 et dTCA_dGas > 0,Sensibilites analytiques globalement coherentes.
Q5-S-01,Q5,NaN,NaN,HIGH_BOTH,PASS,Sensibilites scenarisees,2,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-01,Q5,NaN,NaN,HIGH_CO2,PASS,Sensibilites scenarisees,2,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-01,Q5,NaN,NaN,HIGH_GAS,PASS,Sensibilites scenarisees,2,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-02,Q5,NaN,NaN,HIGH_BOTH,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5-S-02,Q5,NaN,NaN,HIGH_CO2,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5-S-02,Q5,NaN,NaN,HIGH_GAS,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5_ALPHA_NEGATIVE,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,NaN,NaN,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,NaN,NaN,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=62.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=45.3 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=40.5 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=33.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=41.2 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=34.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,NaN,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=8.0 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,NaN,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=21.5 EUR/MWh (acceptable).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
TEST_Q5_001,Q5,NaN,NaN,NaN,WARN,TEST_Q5_001,NaN,NaN,Comparaison BASE/HIGH_CO2/HIGH_GAS indisponible (table Q5_summary manquante).
TEST_Q5_002,Q5,NaN,NaN,NaN,WARN,TEST_Q5_002,NaN,NaN,Impossible d'evaluer la coherence delta_ttl_vs_base vs delta_tca_vs_base (donnees manquantes).
```
