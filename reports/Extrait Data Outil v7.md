# Extrait Data Outil v7

## AUDIT PAYLOAD

### Inputs

#### run_metadata
```json
{
  "run_id": "FULL_20260212_FIX4",
  "run_dir": "C:\\Users\\cval-tlacour\\OneDrive - CVA corporate value associate GmbH\\Desktop\\automation-stack\\projects\\tte-capture-prices-v2\\outputs\\combined\\FULL_20260212_FIX4",
  "countries": [
    "DE",
    "ES",
    "FR"
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
BASE,FR,2025,444.7546,49.418000000000006,historical_mean_2018_2024,5.4963,9.26135,1.36435,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2026,453.22612,50.3592,historical_mean_2018_2024,5.59188,9.36058,1.38916,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2027,461.69764,51.3004,historical_mean_2018_2024,5.68746,9.45981,1.41397,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2028,470.16916,52.241600000000005,historical_mean_2018_2024,5.78304,9.55904,1.43878,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2029,478.64068,53.1828,historical_mean_2018_2024,5.87862,9.65827,1.46359,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2030,487.1122,54.124,historical_mean_2018_2024,5.9742,9.7575,1.4884,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,FR,2031,495.58372,55.0652,historical_mean_2018_2024,6.06978,9.85673,1.51321,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2032,504.05524,56.0064,historical_mean_2018_2024,6.16536,9.95596,1.53802,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2033,512.52676,56.9476,historical_mean_2018_2024,6.26094,10.05519,1.56283,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2034,520.99828,57.8888,historical_mean_2018_2024,6.35652,10.15442,1.58764,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2035,529.4698,58.83,historical_mean_2018_2024,6.4521,10.25365,1.61245,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2036,537.94132,59.7712,historical_mean_2018_2024,6.54768,10.35288,1.63726,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2037,546.41284,60.7124,historical_mean_2018_2024,6.64326,10.45211,1.66207,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2038,554.88436,61.6536,historical_mean_2018_2024,6.73884,10.55134,1.68688,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2039,563.3558800000001,62.5948,historical_mean_2018_2024,6.83442,10.65057,1.71169,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,FR,2040,571.8274,63.536,historical_mean_2018_2024,6.93,10.7498,1.7365,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
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
DEMAND_UP,FR,2025,489.2302,54.359,historical_mean_2018_2024,5.4963,9.26135,1.36435,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2026,498.54886,55.394400000000005,historical_mean_2018_2024,5.59188,9.36058,1.38916,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2027,507.86752,56.4298,historical_mean_2018_2024,5.68746,9.45981,1.41397,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2028,517.1861799999999,57.4652,historical_mean_2018_2024,5.78304,9.55904,1.43878,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2029,526.50484,58.5006,historical_mean_2018_2024,5.87862,9.65827,1.46359,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2030,535.8235,59.536,historical_mean_2018_2024,5.9742,9.7575,1.4884,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,FR,2031,545.14216,60.5714,historical_mean_2018_2024,6.06978,9.85673,1.51321,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2032,554.46082,61.6068,historical_mean_2018_2024,6.16536,9.95596,1.53802,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2033,563.7794799999999,62.6422,historical_mean_2018_2024,6.26094,10.05519,1.56283,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2034,573.09814,63.6776,historical_mean_2018_2024,6.35652,10.15442,1.58764,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2035,582.4168,64.713,historical_mean_2018_2024,6.4521,10.25365,1.61245,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2036,591.73546,65.7484,historical_mean_2018_2024,6.54768,10.35288,1.63726,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2037,601.05412,66.7838,historical_mean_2018_2024,6.64326,10.45211,1.66207,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2038,610.3727799999999,67.8192,historical_mean_2018_2024,6.73884,10.55134,1.68688,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2039,619.69144,68.8546,historical_mean_2018_2024,6.83442,10.65057,1.71169,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,FR,2040,629.0101,69.89,historical_mean_2018_2024,6.93,10.7498,1.7365,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
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
HIGH_CO2,FR,2025,444.7546,49.418000000000006,historical_mean_2018_2024,5.4963,9.26135,1.36435,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,120.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2026,453.22612,50.3592,historical_mean_2018_2024,5.59188,9.36058,1.38916,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,123.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2027,461.69764,51.3004,historical_mean_2018_2024,5.68746,9.45981,1.41397,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,126.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2028,470.16916,52.241600000000005,historical_mean_2018_2024,5.78304,9.55904,1.43878,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,129.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2029,478.64068,53.1828,historical_mean_2018_2024,5.87862,9.65827,1.46359,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,132.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2030,487.1122,54.124,historical_mean_2018_2024,5.9742,9.7575,1.4884,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,135.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,FR,2031,495.58372,55.0652,historical_mean_2018_2024,6.06978,9.85673,1.51321,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,138.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2032,504.05524,56.0064,historical_mean_2018_2024,6.16536,9.95596,1.53802,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,141.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2033,512.52676,56.9476,historical_mean_2018_2024,6.26094,10.05519,1.56283,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,144.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2034,520.99828,57.8888,historical_mean_2018_2024,6.35652,10.15442,1.58764,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,147.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2035,529.4698,58.83,historical_mean_2018_2024,6.4521,10.25365,1.61245,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,150.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2036,537.94132,59.7712,historical_mean_2018_2024,6.54768,10.35288,1.63726,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,153.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2037,546.41284,60.7124,historical_mean_2018_2024,6.64326,10.45211,1.66207,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,156.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2038,554.88436,61.6536,historical_mean_2018_2024,6.73884,10.55134,1.68688,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,159.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2039,563.3558800000001,62.5948,historical_mean_2018_2024,6.83442,10.65057,1.71169,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,162.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,FR,2040,571.8274,63.536,historical_mean_2018_2024,6.93,10.7498,1.7365,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,165.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
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
HIGH_GAS,FR,2025,444.7546,49.418000000000006,historical_mean_2018_2024,5.4963,9.26135,1.36435,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,58.5,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2026,453.22612,50.3592,historical_mean_2018_2024,5.59188,9.36058,1.38916,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,59.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2027,461.69764,51.3004,historical_mean_2018_2024,5.68746,9.45981,1.41397,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,60.3,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2028,470.16916,52.241600000000005,historical_mean_2018_2024,5.78304,9.55904,1.43878,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,61.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2029,478.64068,53.1828,historical_mean_2018_2024,5.87862,9.65827,1.46359,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,62.1,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2030,487.1122,54.124,historical_mean_2018_2024,5.9742,9.7575,1.4884,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,63.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,FR,2031,495.58372,55.0652,historical_mean_2018_2024,6.06978,9.85673,1.51321,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,63.9,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2032,504.05524,56.0064,historical_mean_2018_2024,6.16536,9.95596,1.53802,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,64.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2033,512.52676,56.9476,historical_mean_2018_2024,6.26094,10.05519,1.56283,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,65.7,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2034,520.99828,57.8888,historical_mean_2018_2024,6.35652,10.15442,1.58764,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,66.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2035,529.4698,58.83,historical_mean_2018_2024,6.4521,10.25365,1.61245,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,67.5,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2036,537.94132,59.7712,historical_mean_2018_2024,6.54768,10.35288,1.63726,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,68.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2037,546.41284,60.7124,historical_mean_2018_2024,6.64326,10.45211,1.66207,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,69.3,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2038,554.88436,61.6536,historical_mean_2018_2024,6.73884,10.55134,1.68688,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,70.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2039,563.3558800000001,62.5948,historical_mean_2018_2024,6.83442,10.65057,1.71169,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,71.1,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,FR,2040,571.8274,63.536,historical_mean_2018_2024,6.93,10.7498,1.7365,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,72.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
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
LOW_RIGIDITY,FR,2025,444.7546,49.418000000000006,historical_mean_2018_2024,5.4963,9.26135,1.36435,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2026,453.22612,50.3592,historical_mean_2018_2024,5.59188,9.36058,1.38916,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2027,461.69764,51.3004,historical_mean_2018_2024,5.68746,9.45981,1.41397,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2028,470.16916,52.241600000000005,historical_mean_2018_2024,5.78304,9.55904,1.43878,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2029,478.64068,53.1828,historical_mean_2018_2024,5.87862,9.65827,1.46359,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2030,487.1122,54.124,historical_mean_2018_2024,5.9742,9.7575,1.4884,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,FR,2031,495.58372,55.0652,historical_mean_2018_2024,6.06978,9.85673,1.51321,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2032,504.05524,56.0064,historical_mean_2018_2024,6.16536,9.95596,1.53802,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2033,512.52676,56.9476,historical_mean_2018_2024,6.26094,10.05519,1.56283,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2034,520.99828,57.8888,historical_mean_2018_2024,6.35652,10.15442,1.58764,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2035,529.4698,58.83,historical_mean_2018_2024,6.4521,10.25365,1.61245,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2036,537.94132,59.7712,historical_mean_2018_2024,6.54768,10.35288,1.63726,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2037,546.41284,60.7124,historical_mean_2018_2024,6.64326,10.45211,1.66207,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2038,554.88436,61.6536,historical_mean_2018_2024,6.73884,10.55134,1.68688,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2039,563.3558800000001,62.5948,historical_mean_2018_2024,6.83442,10.65057,1.71169,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,FR,2040,571.8274,63.536,historical_mean_2018_2024,6.93,10.7498,1.7365,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
```

## RUN OUTPUTS

### A.1 annual_metrics_phase1
```csv
country,year,n_hours,timezone,coverage_price,coverage_load_total,coverage_net_position,coverage_vre,coverage_must_run,coverage_psh_pumping,load_total_mw_avg,psh_pumping_mw_avg,load_mw_avg,gen_vre_mw_avg,pv_mw_avg,wind_on_mw_avg,wind_off_mw_avg,must_run_mw_avg,must_run_nuclear_mw_avg,must_run_biomass_mw_avg,must_run_ror_mw_avg,nrl_mw_avg,surplus_mwh_total,sr_energy,sr_hours,far_energy,ir_p10,baseload_price_eur_mwh,ttl_eur_mwh,capture_price_pv_eur_mwh,capture_ratio_pv,capture_ratio_pv_vs_ttl,h_negative_obs,h_below_5_obs,days_spread_gt50,regime_coherence,nrl_price_corr,quality_flag,quality_notes
DE,2018,8760,Europe/Berlin,1.0,0.9988584474885844,0.9998858447488586,1.0,1.0,,63921.54367465752,0.0,63921.54367465752,17744.703384703193,4855.6151757990865,10712.666226883563,2176.421982020548,23426.637060216897,,,,22750.20322973743,153891.6974999999,0.0002671835702335,0.008904109589041,1.0,0.3794941270703111,44.47275456621005,72.28749999999995,43.77257363689873,0.9842559576949768,0.6055344788089055,133,232,38,0.988812785388128,0.6964810903936534,OK,
DE,2019,8760,Europe/Berlin,0.9998858447488584,0.9998858447488584,0.9998858447488586,1.0,1.0,,57360.607076769404,0.0,57360.607076769404,18972.982413812784,4775.466457762557,11414.357870719177,2783.15808533105,17918.5548581621,,,,20469.069804794515,285774.3125,0.000554157034082,0.0156392694063926,0.9876496247366532,0.2843253281938316,37.669692887315904,58.38,34.906182773392544,0.926638368882113,0.5979133739875393,211,335,31,0.9990866537275944,0.813246051355149,OK,
DE,2020,8784,Europe/Berlin,0.9998861566484517,0.9998861566484517,0.9998861566484518,1.0,1.0,,55812.146989697176,0.0,55812.146989697176,20063.148670594263,5229.671831739526,11773.075855248178,3060.400983606557,15713.789862818761,,,,20035.208456284156,345342.565,0.0006991788301744,0.0159380692167577,1.0,0.2439759191136415,30.47081976545599,55.338,24.511203174738068,0.8044156134757428,0.4429361952860253,298,598,42,0.9982921553000114,0.7903113754356191,OK,
DE,2021,8760,Europe/Berlin,0.9998858447488584,0.9998858447488584,0.9998858447488586,1.0,1.0,,58184.632577340184,0.0,58184.632577340184,18299.220867865293,5299.3239497716895,10259.04259018265,2740.854327910959,17130.81492836758,,,,22754.596781107313,185328.96,0.0003675803989361,0.0087899543378995,1.0,0.2701548827424477,96.86022947825094,249.9639999999992,75.45790652091513,0.7790391053931841,0.3018750960974995,139,248,202,0.9737412946683413,0.5221576401467792,OK,
DE,2022,8760,Europe/Berlin,0.9998858447488584,0.9998858447488584,0.9998858447488586,1.0,1.0,,55622.20820861872,0.0,55622.20820861872,20776.10254394977,6391.267546232876,11560.216815924658,2824.6181817922375,17448.43154908676,,,,17397.674115582195,904994.6575,0.001843457392513,0.042579908675799,1.0,0.3104147117931071,235.4667222285649,513.6109999999999,222.2697802958073,0.9439541103394328,0.4327589952236369,69,161,358,0.9733987898161892,0.5909121520525994,OK,
DE,2023,8760,Europe/Berlin,0.9998858447488584,0.9998858447488584,0.9998858447488586,1.0,1.0,,52858.4288989726,0.0,52858.4288989726,22691.967134703194,6369.718088470319,13637.681156107306,2684.567890125571,14701.374773401829,,,,15465.086990867574,2556732.2,0.0057522727927743,0.0775114155251141,1.0,0.2390462318859233,95.1827480305971,168.00449999999992,72.18210511017934,0.7583528171195051,0.4296438792423975,300,530,340,0.98675647905012,0.8419341186601034,OK,
DE,2024,8784,Europe/Berlin,0.9998861566484517,0.9998861566484517,0.9998861566484518,1.0,1.0,,53547.052998405394,0.0,53547.052998405394,23008.048679132513,7222.682743624772,12863.946802709472,2921.41913279827,14024.982520207195,,,,16514.021799065686,2948435.059833,0.0068809540140638,0.0757058287795992,1.0,0.2263046487454366,78.51545827166116,146.069,46.22796099131209,0.5887752808034911,0.3164803003464944,457,756,315,0.9939656153933736,0.798724901005636,OK,
ES,2018,8760,Europe/Madrid,0.9998858447488584,0.9996575342465753,0.9998858447488586,1.0,1.0,,29054.373515981733,0.0,29054.373515981733,6955.0926940639265,1372.5731735159818,5582.519520547945,0.0,7640.716210045663,,,,14458.564611872145,1484.0,6.030734663893564e-06,0.0003424657534246,1.0,0.2941978481508908,57.30006279255623,73.82749999999999,59.342028861067455,1.0356363670298891,0.8037930156251731,0,57,5,0.9938349126612628,0.717322385044847,OK,
ES,2019,8760,Europe/Madrid,0.9998858447488584,0.9998858447488584,0.9998858447488586,1.0,1.0,,28534.742694063927,0.0,28534.742694063927,7621.904337899543,1646.27100456621,5975.633333333333,0.0,7713.826484018265,,,,13199.011872146122,3224.0,1.308843921710153e-05,0.0005707762557077,1.0,0.2913581991978373,47.67961867793127,64.217,48.57853958864,1.0188533578001284,0.756474758843297,0,69,2,0.9956616052060736,0.6819177627648636,OK,
ES,2020,8784,Europe/Madrid,0.9998861566484517,0.9998861566484517,0.9998861566484518,1.0,1.0,,27083.84927140255,0.0,27083.84927140255,8331.01320582878,2280.3885473588343,6050.624658469946,0.0,7939.497723132969,,,,10813.338342440802,143823.0,0.0006026351526537,0.0159380692167577,1.0,0.3059516604886905,33.95808038255721,51.97899999999999,32.896135604866735,0.9687277736041888,0.6328735759608061,0,60,0,0.997609017420016,0.7267869347642084,OK,
ES,2021,8760,Europe/Madrid,0.9998858447488584,0.9998858447488584,0.9998858447488586,1.0,1.0,,27845.732534246574,0.0,27845.732534246574,9630.396461187214,2894.338584474886,6736.057876712329,0.0,7634.175228310503,,,,10581.160844748856,318652.0,0.0012885678805332,0.0231735159817351,1.0,0.2859684981487956,111.94053088252085,255.0575,102.39616733438756,0.9147371959656876,0.4014630714030662,0,202,130,0.9588994177417514,0.3751809059748108,OK,
ES,2022,8760,Europe/Madrid,0.9998858447488584,0.9998858447488584,0.9971461187214612,1.0,1.0,,26949.156164383563,0.0,26949.156164383563,10263.642557077625,3549.291278538813,6714.351278538812,0.0,7643.000296803653,,,,9042.513310502287,626367.0,0.0023960111216853,0.0438356164383561,1.0,0.3049924924924925,167.52426875214064,270.003,151.07895653475305,0.9018332547284886,0.5595454736975258,0,114,329,0.950907637858203,0.4786983212559283,OK,
ES,2023,8760,Europe/Madrid,0.9998858447488584,0.9998858447488584,0.9998858447488586,1.0,1.0,,26155.71278538813,0.0,26155.71278538813,11584.251141552511,4614.86301369863,6969.388127853881,0.0,7386.1205479452055,,,,7185.341095890411,2818976.0,0.0115130277941151,0.1315068493150684,0.9995587759526864,0.2950851393188854,87.11351866651445,149.328,73.07910508828432,0.8388951130311212,0.4893864853763817,0,558,273,0.9366366023518666,0.7478810502523656,OK,
ES,2024,8784,Europe/Madrid,0.9998861566484517,0.9998861566484517,0.9998861566484518,1.0,1.0,,26414.487704918032,0.0,26414.487704918032,12086.060109289618,5379.377504553734,6706.682604735884,0.0,7348.233606557378,,,,6980.193989071036,3567012.0,0.0147292050339075,0.1691712204007286,0.9994023008613372,0.2951989701260838,63.03954912899921,140.0,42.80117347476487,0.6789574809169381,0.3057226676768919,247,1690,271,0.9461459637936924,0.693152070717716,OK,
FR,2018,8760,Europe/Paris,0.9998858447488584,0.9979452054794521,0.9998858447488586,1.0,1.0,,53698.82865296803,0.0,53698.82865296803,4169.0600456621005,1109.9909817351597,3059.0690639269405,0.0,50003.560844748856,,,,-473.7922374429254,26408823.0,0.0496520420270981,0.5723744292237443,0.9963003462895716,1.0521863248472143,50.20345359059253,85.55399999999993,51.22355835504443,1.020319414133753,0.5987278017982148,11,56,28,0.5311108574038133,0.633364276131352,OK,
FR,2019,8760,Europe/Paris,0.9998858447488584,0.998972602739726,0.9998858447488586,1.0,1.0,,53326.016324200915,0.0,53326.016324200915,5036.808561643836,1303.7987442922374,3733.009817351598,0.0,48093.161643835614,,,,196.0461187214678,24110598.0,0.0461849869384012,0.5726027397260274,0.9893073286693262,1.027953453073615,39.44868249800206,70.31899999999999,37.75672972032813,0.9571100307910252,0.5369349638124565,27,81,9,0.6122845073638543,0.7570328459312552,OK,
FR,2020,8784,Europe/Paris,0.9998861566484517,0.9996584699453552,0.9998861566484518,1.0,1.0,,50593.765027322406,0.0,50593.765027322406,5783.262750455373,1416.5976775956285,4366.665072859745,0.0,43084.858265027324,,,,1725.6440118397077,14681307.0,0.030206233256013,0.4229280510018215,0.9937234947814932,0.8761151770927934,32.203028577934646,62.0665,29.859627395869648,0.9272304101338256,0.4810908847102648,102,268,20,0.905613116247296,0.7498910249081551,OK,
FR,2021,8760,Europe/Paris,0.9998858447488584,0.9988584474885844,0.9998858447488586,1.0,1.0,,53161.96632420091,0.0,53161.96632420091,5576.373287671233,1560.1488584474887,4016.224429223744,0.0,46024.546575342465,,,,1561.0464611872158,23693657.0,0.0466692261905737,0.5075342465753425,0.8587565693214856,1.050096731493738,109.17437721201048,340.0,94.28927727889214,0.863657569539304,0.2773214037614475,64,156,203,0.5111314076949424,0.5226537232532609,OK,
FR,2022,8760,Europe/Paris,0.9998858447488584,0.9974885844748859,0.9998858447488586,1.0,1.0,,50602.50719178082,0.0,50602.50719178082,6262.418493150685,2050.479794520548,4211.938698630137,0.0,35927.87716894977,,,,8412.211529680368,1773457.0,0.0041442212851996,0.0776255707762557,0.9005983229365021,0.7147623702216469,275.8996323781253,564.3724999999994,291.49703235009645,1.0565328769651807,0.516497583333874,4,44,361,0.9228222399817332,0.5973274640247075,OK,
FR,2023,8760,Europe/Paris,0.9998858447488584,0.9993150684931507,0.9998858447488586,1.0,1.0,,48560.92602739726,0.0,48560.92602739726,7942.965410958904,2458.0335616438356,5358.282420091325,126.64942922374429,41027.36894977169,,,,-409.40833333333285,27558082.0,0.0581805500968788,0.6019406392694064,0.800669582157423,0.9605239758914184,96.86486813563192,193.012,83.59736517208924,0.8630308055035466,0.4331200400601477,147,393,318,0.451078890284279,0.7070793930879798,OK,
FR,2024,8784,Europe/Paris,0.9998861566484517,0.9998861566484517,0.9998861566484518,1.0,1.0,,48910.85202299636,0.0,48910.85202299636,7875.115407559199,2655.0392657103826,4770.07945924408,449.9966826047359,46567.32999089254,,,,-5531.593375455377,55121278.57,0.1066722478632517,0.8502959927140255,0.858105007486948,1.063233556199511,58.01313787999545,158.54399999999998,39.24796162782507,0.6765357479716481,0.247552487813005,352,1026,284,0.2848684959581009,0.504660100561502,OK,
```

### A.2 q1_transition_summary
```csv
country,transition_year,stage,stage2_score,non_capture_flags_count,reason_codes,persistence_window_years,confidence_level
DE,2019,2,2.0,1,LOW_PRICE:h_negative_obs>=200.0 (211.0); VALUE:capture_ratio_wind<=0.90 (0.870),2.0,0.8
ES,2023,2,3.0,4,LOW_PRICE:h_below_5_obs>=500.0 (558.0); LOW_PRICE:low_price_hours_share>=0.057 (0.064); VALUE:capture_ratio_wind<=0.90 (0.876); PHYSICAL:sr_energy>=0.010 (0.012); PHYSICAL:sr_hours>=0.10 (0.132),2.0,1.0
FR,,1,3.0,5,LOW_PRICE:h_negative_obs>=200.0 (352.0); LOW_PRICE:h_below_5_obs>=500.0 (1026.0); LOW_PRICE:low_price_hours_share>=0.057 (0.117); VALUE:capture_ratio_pv<=0.80 (0.677); PHYSICAL:sr_energy>=0.010 (0.107); PHYSICAL:sr_hours>=0.10 (0.850); PHYSICAL:far_observed<0.95 (0.858),2.0,0.0
```

### A.3 q2_slope_summary
```csv
country,tech,x_var_used,y_var_used,n_points,years_used,slope,intercept,r2,p_value,driver_stats_phase2,slope_quality_flag,slope_quality_notes
DE,PV,pv_penetration_share_load,capture_ratio_PV,4,"2019,2020,2023,2024",-5.534260520793036,1.367722666204194,0.8849617532735934,0.0592759420140285,"{""sr_energy_mean"": 0.0034716406677736, ""far_energy_mean"": 0.9969124061841632, ""ir_p10_mean"": 0.2484130319847082, ""ttl_mean"": 106.94787499999998, ""corr_vre_load_mean"": -0.969405517813395}",PASS,ols_ok
DE,WIND,wind_penetration_share_load,capture_ratio_WIND,4,"2019,2020,2023,2024",-0.3683517153592101,0.9470901671181964,0.3157002068487917,0.4381279444136844,"{""sr_energy_mean"": 0.0034716406677736, ""far_energy_mean"": 0.9969124061841632, ""ir_p10_mean"": 0.2484130319847082, ""ttl_mean"": 106.94787499999998, ""corr_vre_load_mean"": -0.969405517813395}",PASS,ols_ok
ES,PV,pv_penetration_share_load,capture_ratio_PV,2,"2023,2024",-5.876929761031239,1.875809152071917,,,"{""sr_energy_mean"": 0.0131211164140113, ""far_energy_mean"": 0.9994805384070118, ""ir_p10_mean"": 0.2951420547224846, ""ttl_mean"": 144.664, ""corr_vre_load_mean"": 1.0}",WARN,ols_not_possible_n_lt_4
ES,WIND,wind_penetration_share_load,capture_ratio_WIND,2,"2023,2024",-0.4812210902486096,1.0043191141153942,,,"{""sr_energy_mean"": 0.0131211164140113, ""far_energy_mean"": 0.9994805384070118, ""ir_p10_mean"": 0.2951420547224846, ""ttl_mean"": 144.664, ""corr_vre_load_mean"": 1.0}",WARN,ols_not_possible_n_lt_4
FR,PV,pv_penetration_share_load,capture_ratio_PV,1,2024,,,,,"{""sr_energy_mean"": 0.1066722478632517, ""far_energy_mean"": 0.858105007486948, ""ir_p10_mean"": 1.063233556199511, ""ttl_mean"": 158.54399999999998, ""corr_vre_load_mean"": NaN}",WARN,insufficient_points
FR,WIND,wind_penetration_share_load,capture_ratio_WIND,1,2024,,,,,"{""sr_energy_mean"": 0.1066722478632517, ""far_energy_mean"": 0.858105007486948, ""ir_p10_mean"": 1.063233556199511, ""ttl_mean"": 158.54399999999998, ""corr_vre_load_mean"": NaN}",WARN,insufficient_points
```

### A.4 q3_inversion_requirements
```csv
country,lever,required_uplift,within_bounds,target_sr,target_h_negative,predicted_sr_after,predicted_h_negative_after,applicability_flag
DE,demand_uplift,0.0,True,0.05,200.0,,,APPLICABLE
DE,export_uplift,,False,0.05,200.0,,,APPLICABLE
DE,flex_uplift,,False,0.05,200.0,,,APPLICABLE
ES,demand_uplift,0.0053734043843405,True,0.05,200.0,,,APPLICABLE
ES,export_uplift,,False,0.05,200.0,,,APPLICABLE
ES,flex_uplift,,False,0.05,200.0,,,APPLICABLE
FR,demand_uplift,,False,0.05,200.0,,,NA
FR,export_uplift,,False,0.05,200.0,,,NA
FR,flex_uplift,,False,0.05,200.0,,,NA
```

### A.5 q4_bess_sizing_curve
```csv
country,scenario_id,year,bess_power_gw,bess_energy_gwh,cycles_assumed_per_day,eta_roundtrip,far_energy_after,surplus_unabsorbed_twh_after,h_negative_after,monotonicity_check_flag,physics_check_flag,notes
DE,HIGH_CO2,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.25,0.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.25,1.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.25,1.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.25,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.5,1.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.5,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.5,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.5,4.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.75,1.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.75,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.75,4.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,0.75,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,1.0,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,1.0,4.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,1.0,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,1.0,8.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,1.5,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,1.5,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,1.5,9.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_CO2,2035,1.5,12.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.25,0.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.25,1.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.25,1.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.25,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.5,1.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.5,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.5,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.5,4.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.75,1.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.75,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.75,4.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,0.75,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,1.0,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,1.0,4.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,1.0,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,1.0,8.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,1.5,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,1.5,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,1.5,9.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIGH_GAS,2035,1.5,12.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.0,0.0,,0.88,1.0,0.0,457,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.0,0.0,,0.88,1.0,0.0,457,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.0,0.0,,0.88,1.0,0.0,457,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.0,0.0,,0.88,1.0,0.0,457,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.25,0.5,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.25,1.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.25,1.5,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.25,2.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.5,1.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.5,2.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.5,3.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.5,4.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.75,1.5,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.75,3.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.75,4.5,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,0.75,6.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,1.0,2.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,1.0,4.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,1.0,6.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,1.0,8.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,1.5,3.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,1.5,6.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,1.5,9.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
DE,HIST,2024,1.5,12.0,0.0,0.88,1.0,0.0,96,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.25,0.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.25,1.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.25,1.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.25,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.5,1.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.5,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.5,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.5,4.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.75,1.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.75,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.75,4.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,0.75,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,1.0,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,1.0,4.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,1.0,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,1.0,8.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,1.5,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,1.5,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,1.5,9.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_CO2,2035,1.5,12.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.25,0.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.25,1.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.25,1.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.25,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.5,1.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.5,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.5,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.5,4.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.75,1.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.75,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.75,4.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,0.75,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,1.0,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,1.0,4.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,1.0,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,1.0,8.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,1.5,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,1.5,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,1.5,9.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIGH_GAS,2035,1.5,12.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.0,0.0,,0.88,0.9994023008613372,0.002132,247,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.0,0.0,,0.88,0.9994023008613372,0.002132,247,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.0,0.0,,0.88,0.9994023008613372,0.002132,247,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.0,0.0,,0.88,0.9994023008613372,0.002132,247,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.25,0.5,0.002570090827300509,0.88,0.9995517261480726,0.0015989982091109,74,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.25,1.0,0.002570090827300509,0.88,0.9997011514348082,0.0010659964182219,73,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.25,1.5,0.0017760730593607305,0.88,0.9997120839514978,0.001027,73,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.25,2.0,0.001332054794520548,0.88,0.9997120839514978,0.001027,73,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.5,1.0,0.002570090827300509,0.88,0.9997011514348082,0.0010659964182219,73,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.5,2.0,0.0023313972602739728,0.88,0.9999444913557902,0.000198,72,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.5,3.0,0.0015542648401826486,0.88,0.9999444913557902,0.000198,72,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.5,4.0,0.0011656986301369864,0.88,0.9999444913557902,0.000198,72,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.75,1.5,0.0025700908273005095,0.88,0.9998505767215438,0.0005329946273329,72,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.75,3.0,0.0017133881278538813,0.88,1.0,0.0,70,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.75,4.5,0.0011422587519025877,0.88,1.0,0.0,70,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.75,6.0,0.0008566940639269406,0.88,1.0,0.0,70,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,1.0,2.0,0.002570082191780822,0.88,1.0,0.0,70,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,1.0,4.0,0.001285041095890411,0.88,1.0,0.0,70,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,1.0,6.0,0.0008566940639269406,0.88,1.0,0.0,70,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,1.0,8.0,0.0006425205479452055,0.88,1.0,0.0,70,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,1.5,3.0,0.0017133881278538813,0.88,1.0,0.0,70,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,1.5,6.0,0.0008566940639269406,0.88,1.0,0.0,70,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,1.5,9.0,0.0005711293759512938,0.88,1.0,0.0,70,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,1.5,12.0,0.0004283470319634703,0.88,1.0,0.0,70,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.25,0.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.25,1.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.25,1.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.25,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.5,1.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.5,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.5,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.5,4.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.75,1.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.75,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.75,4.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,0.75,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,1.0,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,1.0,4.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,1.0,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,1.0,8.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,1.5,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,1.5,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,1.5,9.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_CO2,2035,1.5,12.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.0,0.0,,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.25,0.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.25,1.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.25,1.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.25,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.5,1.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.5,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.5,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.5,4.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.75,1.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.75,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.75,4.5,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,0.75,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,1.0,2.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,1.0,4.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,1.0,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,1.0,8.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,1.5,3.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,1.5,6.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,1.5,9.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIGH_GAS,2035,1.5,12.0,0.0,0.88,1.0,0.0,0,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.0,0.0,,0.88,0.858105007486948,7.82143341,352,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.0,0.0,,0.88,0.858105007486948,7.82143341,352,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.0,0.0,,0.88,0.858105007486948,7.82143341,352,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.0,0.0,,0.88,0.858105007486948,7.82143341,352,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.0,0.0,,0.88,0.858105007486948,7.82143341,352,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.0,0.0,,0.88,0.858105007486948,7.82143341,352,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.25,0.5,0.002570090827300509,0.88,0.8581146771064618,7.820900408209111,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.25,1.0,0.002570090827300509,0.88,0.8581243467259757,7.820367406418222,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.25,1.5,0.0025700908273005095,0.88,0.8581340163454896,7.819834404627334,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.25,2.0,0.0025700908273005095,0.88,0.8581436859650033,7.819301402836444,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.25,3.0,0.002570090827300509,0.88,0.8581630252040311,7.818235399254665,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.25,6.0,0.0025700908273005095,0.88,0.8582210429211142,7.815037388509332,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.5,1.0,0.002570090827300509,0.88,0.8581243467259757,7.820367406418222,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.5,2.0,0.0025700908273005095,0.88,0.8581436859650033,7.819301402836444,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.5,3.0,0.0025700908273005095,0.88,0.8581630252040311,7.818235399254665,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.5,4.0,0.0025700908273005095,0.88,0.8581823644430587,7.817169395672887,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.5,6.0,0.002570090827300509,0.88,0.8582210429211142,7.815037388509332,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.5,12.0,0.0025700908273005095,0.88,0.8583370783552806,7.808641367018663,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.75,1.5,0.0025700908273005095,0.88,0.8581340163454896,7.819834404627334,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.75,3.0,0.0025700908273005095,0.88,0.8581630252040311,7.818235399254665,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.75,4.5,0.002570090827300509,0.88,0.8581920340625727,7.816636393881999,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.75,6.0,0.0025700908273005095,0.88,0.8582210429211142,7.815037388509332,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.75,9.0,0.002570090827300509,0.88,0.8582790606381974,7.811839377763998,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,0.75,18.0,0.002570090827300509,0.88,0.8584531137894467,7.802245345527996,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,1.0,2.0,0.0025700908273005095,0.88,0.8581436859650033,7.819301402836444,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,1.0,4.0,0.0025700908273005095,0.88,0.8581823644430587,7.817169395672887,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,1.0,6.0,0.0025700908273005095,0.88,0.8582210429211142,7.815037388509332,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,1.0,8.0,0.002570090827300509,0.88,0.8582597213991696,7.812905381345776,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,1.0,12.0,0.002570090827300509,0.88,0.8583370783552806,7.808641367018663,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,1.0,24.0,0.0025700908273005095,0.88,0.858569149223613,7.795849324037326,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,1.5,3.0,0.0025700908273005095,0.88,0.8581630252040311,7.818235399254665,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,1.5,6.0,0.0025700908273005095,0.88,0.8582210429211142,7.815037388509332,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,1.5,9.0,0.002570090827300509,0.88,0.8582790606381974,7.811839377763998,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,1.5,12.0,0.0025700908273005095,0.88,0.8583370783552806,7.808641367018663,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,1.5,18.0,0.002570090827300509,0.88,0.8584531137894467,7.802245345527996,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,1.5,36.0,0.002570090827300509,0.88,0.8588012200919455,7.78305728105599,242,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,2.25,4.5,0.0025700908273005095,0.88,0.8581920340625727,7.816636393881999,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,2.25,9.0,0.0025700908273005095,0.88,0.8582790606381974,7.811839377763998,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,2.25,13.5,0.0025700908273005095,0.88,0.8583660872138221,7.807042361645997,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,2.25,18.0,0.0025700908273005095,0.88,0.8584531137894467,7.802245345527996,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,2.25,27.0,0.0025700908273005095,0.88,0.8586271669406961,7.792651313291993,243,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,2.25,54.0,0.002570090827300509,0.88,0.8591493263944442,7.763869216583985,242,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,82.8,165.6,0.0025700908273005095,0.88,0.8613075854699362,7.644903216857554,239,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,82.8,331.2,0.00257009082730051,0.88,0.8645101634529245,7.46837302371511,239,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,82.8,496.8,0.0025700908273005095,0.88,0.8677127414359129,7.291842830572664,239,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,82.8,662.4,0.0025700908273005095,0.88,0.8709153194189011,7.115312637430219,239,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,82.8,993.6,0.0025700908273005086,0.88,0.8773204753848778,6.762252251145327,235,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
FR,HIST,2024,82.8,1987.2,0.0025700908273005095,0.88,0.8965359432828073,5.7030710922906565,203,FAIL,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
```

### A.6 q5_anchor_sensitivity
```csv
country,scenario_id,year,gas_eur_per_mwh_th,co2_eur_per_t,tca_ccgt_eur_mwh,tca_coal_eur_mwh,ttl_eur_mwh,delta_ttl_vs_base,coherence_flag
DE,HIGH_BOTH,2035,67.5,150.0,236.30263157894737,,236.30263157894737,,PASS
DE,HIGH_CO2,2035,45.0,150.0,203.7368421052632,,203.7368421052632,,FAIL
DE,HIGH_GAS,2035,67.5,100.0,191.43421052631575,,191.43421052631575,,FAIL
DE,HIST,2024,46.9,70.83,131.51952631578948,,131.51952631578948,,PASS
ES,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,,180.8181818181818,,PASS
ES,HIGH_CO2,2035,45.0,150.0,139.9090909090909,,139.9090909090909,,FAIL
ES,HIGH_GAS,2035,67.5,100.0,162.45454545454544,,162.45454545454544,,FAIL
ES,HIST,2024,47.02,70.69,113.00854545454544,,113.00854545454544,,PASS
FR,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,,180.8181818181818,,PASS
FR,HIGH_CO2,2035,45.0,150.0,139.9090909090909,,139.9090909090909,,FAIL
FR,HIGH_GAS,2035,67.5,100.0,162.45454545454544,,162.45454545454544,,FAIL
FR,HIST,2024,47.73,68.25,114.58007272727272,,114.58007272727272,,PASS
```

## TEST LEDGER

```csv
test_id,scope,country,year,scenario_id,status,metric_name,observed_value,expected_rule,message
BUNDLE_INFORMATIVENESS,Q1,,,,WARN,BUNDLE_INFORMATIVENESS,,,share_tests_informatifs=80.00% ; share_compare_informatifs=0.00%
BUNDLE_LEDGER_STATUS,Q1,,,,WARN,BUNDLE_LEDGER_STATUS,,,"ledger: FAIL=0, WARN=1"
Q1-H-01,Q1,,,nan,PASS,Score marche de bascule,1.2244897959183674,stage2_market_score present et non vide,Le score de bascule marche est exploitable.
Q1-H-02,Q1,,,nan,PASS,Stress physique SR/FAR/IR,"far_energy,ir_p10,sr_energy",sr_energy/far_energy/ir_p10 presentes,Le stress physique est calculable.
Q1-H-03,Q1,,,nan,PASS,Concordance marche vs physique,strict=14.29%; concordant_ou_explique=100.00%; n=7; explained=7; reasons=physical_not_reached_but_explained:3;physical_already_phase2_window_start:2;both_not_reached_in_window:1;strict_equal_year:1,bascule_year_market et bascule_year_physical comparables,Concordance satisfaisante en comptant les divergences expliquees.
Q1-H-04,Q1,,,nan,WARN,Robustesse seuils,0.486,delta bascules sous choc de seuil <= 50%,Proxy de robustesse du diagnostic de bascule.
Q1-S-01,Q1,,,DEMAND_UP,PASS,Bascule projetee par scenario,7,Q1_country_summary non vide en SCEN,La bascule projetee est produite.
Q1-S-01,Q1,,,LOW_RIGIDITY,PASS,Bascule projetee par scenario,7,Q1_country_summary non vide en SCEN,La bascule projetee est produite.
Q1-S-02,Q1,,,DEMAND_UP,NON_TESTABLE,Effets DEMAND_UP/LOW_RIGIDITY,nan,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),Impossible d'evaluer la sensibilite sans BASE et scenario courant.
Q1-S-02,Q1,,,LOW_RIGIDITY,NON_TESTABLE,Effets DEMAND_UP/LOW_RIGIDITY,nan,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),Impossible d'evaluer la sensibilite sans BASE et scenario courant.
Q1-S-03,Q1,,,DEMAND_UP,PASS,Qualite de causalite,100.00%,part regime_coherence >= seuil min,La coherence scenario est lisible.
Q1-S-03,Q1,,,LOW_RIGIDITY,PASS,Qualite de causalite,100.00%,part regime_coherence >= seuil min,La coherence scenario est lisible.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2018,,INFO,Q1_CAPTURE_ONLY_SIGNAL,,,DE 2018: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2021,,INFO,Q1_CAPTURE_ONLY_SIGNAL,,,DE 2021: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2022,,INFO,Q1_CAPTURE_ONLY_SIGNAL,,,DE 2022: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,FR,2022,,INFO,Q1_CAPTURE_ONLY_SIGNAL,,,FR 2022: capture-only sans low-price ni stress physique.
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,,,,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,,,"BE: coverage max=61.72% (>60%), possible surestimation must-run."
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,,,,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,,,"CZ: coverage max=84.76% (>60%), possible surestimation must-run."
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,,,,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,,,"FR: coverage max=87.11% (>60%), possible surestimation must-run."
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,,,DEMAND_UP,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,,,"BE: coverage max=80.22% (>60%), possible surestimation must-run."
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,,,DEMAND_UP,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,,,"CZ: coverage max=89.16% (>60%), possible surestimation must-run."
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,,,LOW_RIGIDITY,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,,,"BE: coverage max=75.59% (>60%), possible surestimation must-run."
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,,,LOW_RIGIDITY,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,,,"CZ: coverage max=68.01% (>60%), possible surestimation must-run."
Q1_S02_NO_SENSITIVITY,Q1,,,,WARN,Q1_S02_NO_SENSITIVITY,,,Q1-S-02: aucune sensibilite scenario non-BASE clairement observable vs BASE.
RC_IR_GT_1,Q1,FR,2018,,WARN,RC_IR_GT_1,,,"FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40."
RC_IR_GT_1,Q1,FR,2019,,WARN,RC_IR_GT_1,,,"FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00."
RC_IR_GT_1,Q1,FR,2021,,WARN,RC_IR_GT_1,,,"FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00."
RC_IR_GT_1,Q1,FR,2024,,WARN,RC_IR_GT_1,,,"FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60."
RC_LOW_REGIME_COHERENCE,Q1,FR,2018,,WARN,RC_LOW_REGIME_COHERENCE,,,FR-2018: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q1,FR,2021,,WARN,RC_LOW_REGIME_COHERENCE,,,FR-2021: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q1,FR,2023,,WARN,RC_LOW_REGIME_COHERENCE,,,FR-2023: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q1,FR,2024,,WARN,RC_LOW_REGIME_COHERENCE,,,FR-2024: regime_coherence < 0.55.
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2018,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2018: must_run_share=82.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2019,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2019: must_run_share=80.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2020,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2020: must_run_share=77.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2021,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2021: must_run_share=79.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2022,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2022: must_run_share=73.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2023,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2023: must_run_share=75.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2024,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2024: must_run_share=79.2% hors plage plausible [5%,60%]."
RC_NEG_NOT_IN_AB,Q1,DE,2018,,INFO,RC_NEG_NOT_IN_AB,,,DE-2018: 33.8% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,DE,2019,,INFO,RC_NEG_NOT_IN_AB,,,DE-2019: 44.1% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,DE,2020,,INFO,RC_NEG_NOT_IN_AB,,,DE-2020: 36.9% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,DE,2021,,INFO,RC_NEG_NOT_IN_AB,,,DE-2021: 41.0% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,FR,2018,,INFO,RC_NEG_NOT_IN_AB,,,FR-2018: 27.3% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,DE,2018,,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,,,"DE-2018: 33.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-3039.5, p50=2341.7, p90=8765.7; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,DE,2019,,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,,,"DE-2019: 44.1% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-4050.2, p50=580.8, p90=5229.3; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,DE,2020,,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,,,"DE-2020: 36.9% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-3662.8, p50=1184.0, p90=5399.3; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,DE,2021,,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,,,"DE-2021: 41.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-4056.4, p50=598.4, p90=5182.9; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,FR,2018,,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,,,"FR-2018: 27.3% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-7350.0, p50=375.0, p90=2173.0; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,FR,2020,,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,,,"FR-2020: 52.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-5301.0, p50=-216.0, p90=2362.8; causes=price_or_regime_mapping)."
TEST_DATA_001,Q1,DE,2018,,PASS,TEST_DATA_001,,,DE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2019,,PASS,TEST_DATA_001,,,DE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2020,,PASS,TEST_DATA_001,,,DE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2021,,PASS,TEST_DATA_001,,,DE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2022,,PASS,TEST_DATA_001,,,DE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2023,,PASS,TEST_DATA_001,,,DE-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2024,,PASS,TEST_DATA_001,,,DE-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2025,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2026,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2027,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2028,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2029,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2030,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2031,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2032,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,DE,2033,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2034,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2035,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2018,,PASS,TEST_DATA_001,,,ES-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2019,,PASS,TEST_DATA_001,,,ES-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2020,,PASS,TEST_DATA_001,,,ES-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2021,,PASS,TEST_DATA_001,,,ES-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2022,,PASS,TEST_DATA_001,,,ES-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2023,,PASS,TEST_DATA_001,,,ES-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2024,,PASS,TEST_DATA_001,,,ES-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2025,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2026,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2027,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2028,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2029,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2030,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2031,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2032,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,ES,2033,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2034,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2035,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2018,,PASS,TEST_DATA_001,,,FR-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2019,,PASS,TEST_DATA_001,,,FR-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2020,,PASS,TEST_DATA_001,,,FR-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,FR,2021,,PASS,TEST_DATA_001,,,FR-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2022,,PASS,TEST_DATA_001,,,FR-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2023,,PASS,TEST_DATA_001,,,FR-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2024,,PASS,TEST_DATA_001,,,FR-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,FR,2025,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2026,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2027,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2028,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,FR,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,FR,2029,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2030,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2031,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2032,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,FR,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,FR,2033,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2034,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2035,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2035: n_hours=8760 coherent.
TEST_DATA_002,Q1,DE,2018,,PASS,TEST_DATA_002,,,DE-2018: coverage price/load ok (100.00%/99.89%).
TEST_DATA_002,Q1,DE,2019,,PASS,TEST_DATA_002,,,DE-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2020,,PASS,TEST_DATA_002,,,DE-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2021,,PASS,TEST_DATA_002,,,DE-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2022,,PASS,TEST_DATA_002,,,DE-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2023,,PASS,TEST_DATA_002,,,DE-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2024,,PASS,TEST_DATA_002,,,DE-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,DE,2025,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2026,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2027,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2028,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2029,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2030,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2031,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2032,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2033,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2034,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2035,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2018,,PASS,TEST_DATA_002,,,ES-2018: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q1,ES,2019,,PASS,TEST_DATA_002,,,ES-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2020,,PASS,TEST_DATA_002,,,ES-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2021,,PASS,TEST_DATA_002,,,ES-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2022,,PASS,TEST_DATA_002,,,ES-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2023,,PASS,TEST_DATA_002,,,ES-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2024,,PASS,TEST_DATA_002,,,ES-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,ES,2025,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2026,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2027,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2028,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2029,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2030,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2031,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2032,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2033,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2034,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2035,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2018,,PASS,TEST_DATA_002,,,FR-2018: coverage price/load ok (99.99%/99.79%).
TEST_DATA_002,Q1,FR,2019,,PASS,TEST_DATA_002,,,FR-2019: coverage price/load ok (99.99%/99.90%).
TEST_DATA_002,Q1,FR,2020,,PASS,TEST_DATA_002,,,FR-2020: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q1,FR,2021,,PASS,TEST_DATA_002,,,FR-2021: coverage price/load ok (99.99%/99.89%).
TEST_DATA_002,Q1,FR,2022,,PASS,TEST_DATA_002,,,FR-2022: coverage price/load ok (99.99%/99.75%).
TEST_DATA_002,Q1,FR,2023,,PASS,TEST_DATA_002,,,FR-2023: coverage price/load ok (99.99%/99.93%).
TEST_DATA_002,Q1,FR,2024,,PASS,TEST_DATA_002,,,FR-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,FR,2025,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2026,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2027,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2028,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2029,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2030,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2031,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2032,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2033,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2034,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2035,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_003,Q1,DE,2018,,PASS,TEST_DATA_003,,,DE-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2019,,PASS,TEST_DATA_003,,,DE-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2020,,PASS,TEST_DATA_003,,,DE-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2021,,PASS,TEST_DATA_003,,,DE-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2022,,PASS,TEST_DATA_003,,,DE-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2023,,PASS,TEST_DATA_003,,,DE-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2024,,PASS,TEST_DATA_003,,,DE-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2025,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2026,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2027,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2028,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2029,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2030,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2031,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2032,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2033,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2034,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2035,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2018,,PASS,TEST_DATA_003,,,ES-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2019,,PASS,TEST_DATA_003,,,ES-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2020,,PASS,TEST_DATA_003,,,ES-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2021,,PASS,TEST_DATA_003,,,ES-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2022,,PASS,TEST_DATA_003,,,ES-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2023,,PASS,TEST_DATA_003,,,ES-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2024,,PASS,TEST_DATA_003,,,ES-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2025,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2026,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2027,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2028,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2029,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2030,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2031,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2032,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2033,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2034,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2035,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2018,,PASS,TEST_DATA_003,,,FR-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2019,,PASS,TEST_DATA_003,,,FR-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2020,,PASS,TEST_DATA_003,,,FR-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2021,,PASS,TEST_DATA_003,,,FR-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2022,,PASS,TEST_DATA_003,,,FR-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2023,,PASS,TEST_DATA_003,,,FR-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2024,,PASS,TEST_DATA_003,,,FR-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2025,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2026,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2027,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2028,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2029,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2030,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2031,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2032,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2033,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2034,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2035,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2035: prix dans plage large attendue.
TEST_Q1_001,Q1,,,,PASS,TEST_Q1_001,,,Toutes les lignes stage2 ont au moins un signal low-price (h_negative/h_below_5/days_spread_gt50).
TEST_Q1_001,Q1,,,DEMAND_UP,WARN,TEST_Q1_001,,,Aucune ligne stage2 observee; test non applicable.
TEST_Q1_001,Q1,,,LOW_RIGIDITY,WARN,TEST_Q1_001,,,Aucune ligne stage2 observee; test non applicable.
BUNDLE_INFORMATIVENESS,Q2,,,,WARN,BUNDLE_INFORMATIVENESS,,,share_tests_informatifs=100.00% ; share_compare_informatifs=14.29%
BUNDLE_LEDGER_STATUS,Q2,,,,WARN,BUNDLE_LEDGER_STATUS,,,"ledger: FAIL=0, WARN=2"
Q2-H-01,Q2,,,nan,PASS,Pentes OLS post-bascule,14,Q2_country_slopes non vide,Les pentes historiques sont calculees.
Q2-H-02,Q2,,,nan,PASS,Robustesse statistique,"n,p_value,r2","colonnes r2,p_value,n presentes",La robustesse statistique est lisible.
Q2-H-03,Q2,,,nan,PASS,Drivers physiques,4,driver correlations non vides,Les drivers de pente sont disponibles.
Q2-S-01,Q2,,,HIGH_CO2,PASS,Pentes projetees,14,Q2_country_slopes non vide en SCEN,Pentes prospectives calculees.
Q2-S-01,Q2,,,HIGH_GAS,PASS,Pentes projetees,14,Q2_country_slopes non vide en SCEN,Pentes prospectives calculees.
Q2-S-02,Q2,,,HIGH_CO2,WARN,Delta pente vs BASE,finite=14.29%; robust=14.29%; reason_known=100.00%,delta slope par pays/tech vs BASE,Delta de pente partiellement exploitable; beaucoup de valeurs non finies.
Q2-S-02,Q2,,,HIGH_GAS,WARN,Delta pente vs BASE,finite=14.29%; robust=14.29%; reason_known=100.00%,delta slope par pays/tech vs BASE,Delta de pente partiellement exploitable; beaucoup de valeurs non finies.
RC_IR_GT_1,Q2,FR,2018,,WARN,RC_IR_GT_1,,,"FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40."
RC_IR_GT_1,Q2,FR,2019,,WARN,RC_IR_GT_1,,,"FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00."
RC_IR_GT_1,Q2,FR,2021,,WARN,RC_IR_GT_1,,,"FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00."
RC_IR_GT_1,Q2,FR,2024,,WARN,RC_IR_GT_1,,,"FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60."
RC_LOW_REGIME_COHERENCE,Q2,FR,2018,,WARN,RC_LOW_REGIME_COHERENCE,,,FR-2018: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q2,FR,2021,,WARN,RC_LOW_REGIME_COHERENCE,,,FR-2021: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q2,FR,2023,,WARN,RC_LOW_REGIME_COHERENCE,,,FR-2023: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q2,FR,2024,,WARN,RC_LOW_REGIME_COHERENCE,,,FR-2024: regime_coherence < 0.55.
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2018,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2018: must_run_share=82.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2019,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2019: must_run_share=80.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2020,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2020: must_run_share=77.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2021,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2021: must_run_share=79.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2022,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2022: must_run_share=73.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2023,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2023: must_run_share=75.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2024,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2024: must_run_share=79.2% hors plage plausible [5%,60%]."
TEST_DATA_001,Q2,DE,2018,,PASS,TEST_DATA_001,,,DE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2019,,PASS,TEST_DATA_001,,,DE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2020,,PASS,TEST_DATA_001,,,DE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q2,DE,2021,,PASS,TEST_DATA_001,,,DE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2022,,PASS,TEST_DATA_001,,,DE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2023,,PASS,TEST_DATA_001,,,DE-2023: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2024,,PASS,TEST_DATA_001,,,DE-2024: n_hours=8784 coherent.
TEST_DATA_001,Q2,DE,2025,HIGH_CO2,PASS,TEST_DATA_001,,,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2025,HIGH_GAS,PASS,TEST_DATA_001,,,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2026,HIGH_CO2,PASS,TEST_DATA_001,,,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2026,HIGH_GAS,PASS,TEST_DATA_001,,,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2027,HIGH_CO2,PASS,TEST_DATA_001,,,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2027,HIGH_GAS,PASS,TEST_DATA_001,,,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2028,HIGH_CO2,PASS,TEST_DATA_001,,,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,DE,2028,HIGH_GAS,PASS,TEST_DATA_001,,,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,DE,2029,HIGH_CO2,PASS,TEST_DATA_001,,,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2029,HIGH_GAS,PASS,TEST_DATA_001,,,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2030,HIGH_CO2,PASS,TEST_DATA_001,,,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2030,HIGH_GAS,PASS,TEST_DATA_001,,,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2031,HIGH_CO2,PASS,TEST_DATA_001,,,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2031,HIGH_GAS,PASS,TEST_DATA_001,,,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2032,HIGH_CO2,PASS,TEST_DATA_001,,,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,DE,2032,HIGH_GAS,PASS,TEST_DATA_001,,,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,DE,2033,HIGH_CO2,PASS,TEST_DATA_001,,,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2033,HIGH_GAS,PASS,TEST_DATA_001,,,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2034,HIGH_CO2,PASS,TEST_DATA_001,,,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2034,HIGH_GAS,PASS,TEST_DATA_001,,,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2035,HIGH_CO2,PASS,TEST_DATA_001,,,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,DE,2035,HIGH_GAS,PASS,TEST_DATA_001,,,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2018,,PASS,TEST_DATA_001,,,ES-2018: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2019,,PASS,TEST_DATA_001,,,ES-2019: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2020,,PASS,TEST_DATA_001,,,ES-2020: n_hours=8784 coherent.
TEST_DATA_001,Q2,ES,2021,,PASS,TEST_DATA_001,,,ES-2021: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2022,,PASS,TEST_DATA_001,,,ES-2022: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2023,,PASS,TEST_DATA_001,,,ES-2023: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2024,,PASS,TEST_DATA_001,,,ES-2024: n_hours=8784 coherent.
TEST_DATA_001,Q2,ES,2025,HIGH_CO2,PASS,TEST_DATA_001,,,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2025,HIGH_GAS,PASS,TEST_DATA_001,,,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2026,HIGH_CO2,PASS,TEST_DATA_001,,,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2026,HIGH_GAS,PASS,TEST_DATA_001,,,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2027,HIGH_CO2,PASS,TEST_DATA_001,,,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2027,HIGH_GAS,PASS,TEST_DATA_001,,,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2028,HIGH_CO2,PASS,TEST_DATA_001,,,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,ES,2028,HIGH_GAS,PASS,TEST_DATA_001,,,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,ES,2029,HIGH_CO2,PASS,TEST_DATA_001,,,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2029,HIGH_GAS,PASS,TEST_DATA_001,,,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2030,HIGH_CO2,PASS,TEST_DATA_001,,,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2030,HIGH_GAS,PASS,TEST_DATA_001,,,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2031,HIGH_CO2,PASS,TEST_DATA_001,,,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2031,HIGH_GAS,PASS,TEST_DATA_001,,,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2032,HIGH_CO2,PASS,TEST_DATA_001,,,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,ES,2032,HIGH_GAS,PASS,TEST_DATA_001,,,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,ES,2033,HIGH_CO2,PASS,TEST_DATA_001,,,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2033,HIGH_GAS,PASS,TEST_DATA_001,,,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2034,HIGH_CO2,PASS,TEST_DATA_001,,,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2034,HIGH_GAS,PASS,TEST_DATA_001,,,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2035,HIGH_CO2,PASS,TEST_DATA_001,,,ES-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,ES,2035,HIGH_GAS,PASS,TEST_DATA_001,,,ES-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2018,,PASS,TEST_DATA_001,,,FR-2018: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2019,,PASS,TEST_DATA_001,,,FR-2019: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2020,,PASS,TEST_DATA_001,,,FR-2020: n_hours=8784 coherent.
TEST_DATA_001,Q2,FR,2021,,PASS,TEST_DATA_001,,,FR-2021: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2022,,PASS,TEST_DATA_001,,,FR-2022: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2023,,PASS,TEST_DATA_001,,,FR-2023: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2024,,PASS,TEST_DATA_001,,,FR-2024: n_hours=8784 coherent.
TEST_DATA_001,Q2,FR,2025,HIGH_CO2,PASS,TEST_DATA_001,,,FR-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2025,HIGH_GAS,PASS,TEST_DATA_001,,,FR-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2026,HIGH_CO2,PASS,TEST_DATA_001,,,FR-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2026,HIGH_GAS,PASS,TEST_DATA_001,,,FR-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2027,HIGH_CO2,PASS,TEST_DATA_001,,,FR-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2027,HIGH_GAS,PASS,TEST_DATA_001,,,FR-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2028,HIGH_CO2,PASS,TEST_DATA_001,,,FR-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,FR,2028,HIGH_GAS,PASS,TEST_DATA_001,,,FR-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,FR,2029,HIGH_CO2,PASS,TEST_DATA_001,,,FR-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2029,HIGH_GAS,PASS,TEST_DATA_001,,,FR-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2030,HIGH_CO2,PASS,TEST_DATA_001,,,FR-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2030,HIGH_GAS,PASS,TEST_DATA_001,,,FR-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2031,HIGH_CO2,PASS,TEST_DATA_001,,,FR-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2031,HIGH_GAS,PASS,TEST_DATA_001,,,FR-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2032,HIGH_CO2,PASS,TEST_DATA_001,,,FR-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,FR,2032,HIGH_GAS,PASS,TEST_DATA_001,,,FR-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,FR,2033,HIGH_CO2,PASS,TEST_DATA_001,,,FR-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2033,HIGH_GAS,PASS,TEST_DATA_001,,,FR-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2034,HIGH_CO2,PASS,TEST_DATA_001,,,FR-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2034,HIGH_GAS,PASS,TEST_DATA_001,,,FR-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2035,HIGH_CO2,PASS,TEST_DATA_001,,,FR-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2035,HIGH_GAS,PASS,TEST_DATA_001,,,FR-2035: n_hours=8760 coherent.
TEST_DATA_002,Q2,DE,2018,,PASS,TEST_DATA_002,,,DE-2018: coverage price/load ok (100.00%/99.89%).
TEST_DATA_002,Q2,DE,2019,,PASS,TEST_DATA_002,,,DE-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,DE,2020,,PASS,TEST_DATA_002,,,DE-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,DE,2021,,PASS,TEST_DATA_002,,,DE-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,DE,2022,,PASS,TEST_DATA_002,,,DE-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,DE,2023,,PASS,TEST_DATA_002,,,DE-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,DE,2024,,PASS,TEST_DATA_002,,,DE-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,DE,2025,HIGH_CO2,PASS,TEST_DATA_002,,,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2025,HIGH_GAS,PASS,TEST_DATA_002,,,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2026,HIGH_CO2,PASS,TEST_DATA_002,,,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2026,HIGH_GAS,PASS,TEST_DATA_002,,,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2027,HIGH_CO2,PASS,TEST_DATA_002,,,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2027,HIGH_GAS,PASS,TEST_DATA_002,,,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2028,HIGH_CO2,PASS,TEST_DATA_002,,,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2028,HIGH_GAS,PASS,TEST_DATA_002,,,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2029,HIGH_CO2,PASS,TEST_DATA_002,,,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2029,HIGH_GAS,PASS,TEST_DATA_002,,,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2030,HIGH_CO2,PASS,TEST_DATA_002,,,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2030,HIGH_GAS,PASS,TEST_DATA_002,,,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2031,HIGH_CO2,PASS,TEST_DATA_002,,,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2031,HIGH_GAS,PASS,TEST_DATA_002,,,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2032,HIGH_CO2,PASS,TEST_DATA_002,,,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2032,HIGH_GAS,PASS,TEST_DATA_002,,,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2033,HIGH_CO2,PASS,TEST_DATA_002,,,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2033,HIGH_GAS,PASS,TEST_DATA_002,,,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2034,HIGH_CO2,PASS,TEST_DATA_002,,,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2034,HIGH_GAS,PASS,TEST_DATA_002,,,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2035,HIGH_CO2,PASS,TEST_DATA_002,,,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,DE,2035,HIGH_GAS,PASS,TEST_DATA_002,,,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2018,,PASS,TEST_DATA_002,,,ES-2018: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q2,ES,2019,,PASS,TEST_DATA_002,,,ES-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,ES,2020,,PASS,TEST_DATA_002,,,ES-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,ES,2021,,PASS,TEST_DATA_002,,,ES-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,ES,2022,,PASS,TEST_DATA_002,,,ES-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,ES,2023,,PASS,TEST_DATA_002,,,ES-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,ES,2024,,PASS,TEST_DATA_002,,,ES-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,ES,2025,HIGH_CO2,PASS,TEST_DATA_002,,,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2025,HIGH_GAS,PASS,TEST_DATA_002,,,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2026,HIGH_CO2,PASS,TEST_DATA_002,,,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2026,HIGH_GAS,PASS,TEST_DATA_002,,,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2027,HIGH_CO2,PASS,TEST_DATA_002,,,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2027,HIGH_GAS,PASS,TEST_DATA_002,,,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2028,HIGH_CO2,PASS,TEST_DATA_002,,,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2028,HIGH_GAS,PASS,TEST_DATA_002,,,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2029,HIGH_CO2,PASS,TEST_DATA_002,,,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2029,HIGH_GAS,PASS,TEST_DATA_002,,,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2030,HIGH_CO2,PASS,TEST_DATA_002,,,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2030,HIGH_GAS,PASS,TEST_DATA_002,,,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2031,HIGH_CO2,PASS,TEST_DATA_002,,,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2031,HIGH_GAS,PASS,TEST_DATA_002,,,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2032,HIGH_CO2,PASS,TEST_DATA_002,,,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2032,HIGH_GAS,PASS,TEST_DATA_002,,,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2033,HIGH_CO2,PASS,TEST_DATA_002,,,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2033,HIGH_GAS,PASS,TEST_DATA_002,,,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2034,HIGH_CO2,PASS,TEST_DATA_002,,,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2034,HIGH_GAS,PASS,TEST_DATA_002,,,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2035,HIGH_CO2,PASS,TEST_DATA_002,,,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,ES,2035,HIGH_GAS,PASS,TEST_DATA_002,,,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2018,,PASS,TEST_DATA_002,,,FR-2018: coverage price/load ok (99.99%/99.79%).
TEST_DATA_002,Q2,FR,2019,,PASS,TEST_DATA_002,,,FR-2019: coverage price/load ok (99.99%/99.90%).
TEST_DATA_002,Q2,FR,2020,,PASS,TEST_DATA_002,,,FR-2020: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q2,FR,2021,,PASS,TEST_DATA_002,,,FR-2021: coverage price/load ok (99.99%/99.89%).
TEST_DATA_002,Q2,FR,2022,,PASS,TEST_DATA_002,,,FR-2022: coverage price/load ok (99.99%/99.75%).
TEST_DATA_002,Q2,FR,2023,,PASS,TEST_DATA_002,,,FR-2023: coverage price/load ok (99.99%/99.93%).
TEST_DATA_002,Q2,FR,2024,,PASS,TEST_DATA_002,,,FR-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,FR,2025,HIGH_CO2,PASS,TEST_DATA_002,,,FR-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2025,HIGH_GAS,PASS,TEST_DATA_002,,,FR-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2026,HIGH_CO2,PASS,TEST_DATA_002,,,FR-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2026,HIGH_GAS,PASS,TEST_DATA_002,,,FR-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2027,HIGH_CO2,PASS,TEST_DATA_002,,,FR-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2027,HIGH_GAS,PASS,TEST_DATA_002,,,FR-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2028,HIGH_CO2,PASS,TEST_DATA_002,,,FR-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2028,HIGH_GAS,PASS,TEST_DATA_002,,,FR-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2029,HIGH_CO2,PASS,TEST_DATA_002,,,FR-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2029,HIGH_GAS,PASS,TEST_DATA_002,,,FR-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2030,HIGH_CO2,PASS,TEST_DATA_002,,,FR-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2030,HIGH_GAS,PASS,TEST_DATA_002,,,FR-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2031,HIGH_CO2,PASS,TEST_DATA_002,,,FR-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2031,HIGH_GAS,PASS,TEST_DATA_002,,,FR-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2032,HIGH_CO2,PASS,TEST_DATA_002,,,FR-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2032,HIGH_GAS,PASS,TEST_DATA_002,,,FR-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2033,HIGH_CO2,PASS,TEST_DATA_002,,,FR-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2033,HIGH_GAS,PASS,TEST_DATA_002,,,FR-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2034,HIGH_CO2,PASS,TEST_DATA_002,,,FR-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2034,HIGH_GAS,PASS,TEST_DATA_002,,,FR-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2035,HIGH_CO2,PASS,TEST_DATA_002,,,FR-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2035,HIGH_GAS,PASS,TEST_DATA_002,,,FR-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_003,Q2,DE,2018,,PASS,TEST_DATA_003,,,DE-2018: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2019,,PASS,TEST_DATA_003,,,DE-2019: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2020,,PASS,TEST_DATA_003,,,DE-2020: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2021,,PASS,TEST_DATA_003,,,DE-2021: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2022,,PASS,TEST_DATA_003,,,DE-2022: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2023,,PASS,TEST_DATA_003,,,DE-2023: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2024,,PASS,TEST_DATA_003,,,DE-2024: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2025,HIGH_CO2,PASS,TEST_DATA_003,,,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2025,HIGH_GAS,PASS,TEST_DATA_003,,,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2026,HIGH_CO2,PASS,TEST_DATA_003,,,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2026,HIGH_GAS,PASS,TEST_DATA_003,,,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2027,HIGH_CO2,PASS,TEST_DATA_003,,,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2027,HIGH_GAS,PASS,TEST_DATA_003,,,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2028,HIGH_CO2,PASS,TEST_DATA_003,,,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2028,HIGH_GAS,PASS,TEST_DATA_003,,,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2029,HIGH_CO2,PASS,TEST_DATA_003,,,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2029,HIGH_GAS,PASS,TEST_DATA_003,,,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2030,HIGH_CO2,PASS,TEST_DATA_003,,,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2030,HIGH_GAS,PASS,TEST_DATA_003,,,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2031,HIGH_CO2,PASS,TEST_DATA_003,,,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2031,HIGH_GAS,PASS,TEST_DATA_003,,,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2032,HIGH_CO2,PASS,TEST_DATA_003,,,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2032,HIGH_GAS,PASS,TEST_DATA_003,,,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2033,HIGH_CO2,PASS,TEST_DATA_003,,,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2033,HIGH_GAS,PASS,TEST_DATA_003,,,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2034,HIGH_CO2,PASS,TEST_DATA_003,,,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2034,HIGH_GAS,PASS,TEST_DATA_003,,,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2035,HIGH_CO2,PASS,TEST_DATA_003,,,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,DE,2035,HIGH_GAS,PASS,TEST_DATA_003,,,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2018,,PASS,TEST_DATA_003,,,ES-2018: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2019,,PASS,TEST_DATA_003,,,ES-2019: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2020,,PASS,TEST_DATA_003,,,ES-2020: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2021,,PASS,TEST_DATA_003,,,ES-2021: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2022,,PASS,TEST_DATA_003,,,ES-2022: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2023,,PASS,TEST_DATA_003,,,ES-2023: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2024,,PASS,TEST_DATA_003,,,ES-2024: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2025,HIGH_CO2,PASS,TEST_DATA_003,,,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2025,HIGH_GAS,PASS,TEST_DATA_003,,,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2026,HIGH_CO2,PASS,TEST_DATA_003,,,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2026,HIGH_GAS,PASS,TEST_DATA_003,,,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2027,HIGH_CO2,PASS,TEST_DATA_003,,,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2027,HIGH_GAS,PASS,TEST_DATA_003,,,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2028,HIGH_CO2,PASS,TEST_DATA_003,,,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2028,HIGH_GAS,PASS,TEST_DATA_003,,,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2029,HIGH_CO2,PASS,TEST_DATA_003,,,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2029,HIGH_GAS,PASS,TEST_DATA_003,,,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2030,HIGH_CO2,PASS,TEST_DATA_003,,,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2030,HIGH_GAS,PASS,TEST_DATA_003,,,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2031,HIGH_CO2,PASS,TEST_DATA_003,,,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2031,HIGH_GAS,PASS,TEST_DATA_003,,,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2032,HIGH_CO2,PASS,TEST_DATA_003,,,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2032,HIGH_GAS,PASS,TEST_DATA_003,,,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2033,HIGH_CO2,PASS,TEST_DATA_003,,,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2033,HIGH_GAS,PASS,TEST_DATA_003,,,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2034,HIGH_CO2,PASS,TEST_DATA_003,,,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2034,HIGH_GAS,PASS,TEST_DATA_003,,,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2035,HIGH_CO2,PASS,TEST_DATA_003,,,ES-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,ES,2035,HIGH_GAS,PASS,TEST_DATA_003,,,ES-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2018,,PASS,TEST_DATA_003,,,FR-2018: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2019,,PASS,TEST_DATA_003,,,FR-2019: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2020,,PASS,TEST_DATA_003,,,FR-2020: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2021,,PASS,TEST_DATA_003,,,FR-2021: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2022,,PASS,TEST_DATA_003,,,FR-2022: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2023,,PASS,TEST_DATA_003,,,FR-2023: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2024,,PASS,TEST_DATA_003,,,FR-2024: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2025,HIGH_CO2,PASS,TEST_DATA_003,,,FR-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2025,HIGH_GAS,PASS,TEST_DATA_003,,,FR-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2026,HIGH_CO2,PASS,TEST_DATA_003,,,FR-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2026,HIGH_GAS,PASS,TEST_DATA_003,,,FR-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2027,HIGH_CO2,PASS,TEST_DATA_003,,,FR-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2027,HIGH_GAS,PASS,TEST_DATA_003,,,FR-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2028,HIGH_CO2,PASS,TEST_DATA_003,,,FR-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2028,HIGH_GAS,PASS,TEST_DATA_003,,,FR-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2029,HIGH_CO2,PASS,TEST_DATA_003,,,FR-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2029,HIGH_GAS,PASS,TEST_DATA_003,,,FR-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2030,HIGH_CO2,PASS,TEST_DATA_003,,,FR-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2030,HIGH_GAS,PASS,TEST_DATA_003,,,FR-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2031,HIGH_CO2,PASS,TEST_DATA_003,,,FR-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2031,HIGH_GAS,PASS,TEST_DATA_003,,,FR-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2032,HIGH_CO2,PASS,TEST_DATA_003,,,FR-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2032,HIGH_GAS,PASS,TEST_DATA_003,,,FR-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2033,HIGH_CO2,PASS,TEST_DATA_003,,,FR-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2033,HIGH_GAS,PASS,TEST_DATA_003,,,FR-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2034,HIGH_CO2,PASS,TEST_DATA_003,,,FR-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2034,HIGH_GAS,PASS,TEST_DATA_003,,,FR-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2035,HIGH_CO2,PASS,TEST_DATA_003,,,FR-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2035,HIGH_GAS,PASS,TEST_DATA_003,,,FR-2035: prix dans plage large attendue.
TEST_Q2_001,Q2,,,,PASS,TEST_Q2_001,,,r2 present pour les OLS (n>=3) ou justification explicite quand OLS impossible.
TEST_Q2_001,Q2,,,HIGH_CO2,PASS,TEST_Q2_001,,,r2 present pour les OLS (n>=3) ou justification explicite quand OLS impossible.
TEST_Q2_001,Q2,,,HIGH_GAS,PASS,TEST_Q2_001,,,r2 present pour les OLS (n>=3) ou justification explicite quand OLS impossible.
TEST_Q2_002,Q2,,,,PASS,TEST_Q2_002,,,Aucun cas physiquement suspect (slope>0 et corr_vre_load fortement negative).
TEST_Q2_002,Q2,,,HIGH_CO2,PASS,TEST_Q2_002,,,Aucun cas physiquement suspect (slope>0 et corr_vre_load fortement negative).
TEST_Q2_002,Q2,,,HIGH_GAS,PASS,TEST_Q2_002,,,Aucun cas physiquement suspect (slope>0 et corr_vre_load fortement negative).
TEST_Q2_2022_001,Q2,,,,PASS,TEST_Q2_2022_001,,,exclude_year_2022=1 respecte: 2022 absent de tous les years_used.
TEST_Q2_2022_001,Q2,,,HIGH_CO2,PASS,TEST_Q2_2022_001,,,exclude_year_2022=1 respecte: 2022 absent de tous les years_used.
TEST_Q2_2022_001,Q2,,,HIGH_GAS,PASS,TEST_Q2_2022_001,,,exclude_year_2022=1 respecte: 2022 absent de tous les years_used.
BUNDLE_INFORMATIVENESS,Q3,,,,WARN,BUNDLE_INFORMATIVENESS,,,share_tests_informatifs=100.00% ; share_compare_informatifs=14.29%
BUNDLE_LEDGER_STATUS,Q3,,,,WARN,BUNDLE_LEDGER_STATUS,,,"ledger: FAIL=0, WARN=2"
Q3-H-01,Q3,,,nan,PASS,Tendances glissantes,7,Q3_status non vide,Les tendances historiques sont calculees.
Q3-H-02,Q3,,,nan,PASS,Statuts sortie phase 2,2,status dans ensemble attendu,Les statuts business sont renseignes.
Q3-S-01,Q3,,,DEMAND_UP,PASS,Conditions minimales d'inversion,7,"inversion_k, inversion_r et additional_absorbed presentes",Les ordres de grandeur d'inversion sont quantifies.
Q3-S-01,Q3,,,LOW_RIGIDITY,PASS,Conditions minimales d'inversion,7,"inversion_k, inversion_r et additional_absorbed presentes",Les ordres de grandeur d'inversion sont quantifies.
Q3-S-02,Q3,,,DEMAND_UP,WARN,Validation entree phase 3,hors_scope=42.86%,status non vide en SCEN,Lecture partiellement informative: forte part de cas hors scope Stage 2.
Q3-S-02,Q3,,,LOW_RIGIDITY,WARN,Validation entree phase 3,hors_scope=42.86%,status non vide en SCEN,Lecture partiellement informative: forte part de cas hors scope Stage 2.
RC_IR_GT_1,Q3,FR,2018,,WARN,RC_IR_GT_1,,,"FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40."
RC_IR_GT_1,Q3,FR,2019,,WARN,RC_IR_GT_1,,,"FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00."
RC_IR_GT_1,Q3,FR,2021,,WARN,RC_IR_GT_1,,,"FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00."
RC_IR_GT_1,Q3,FR,2024,,WARN,RC_IR_GT_1,,,"FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60."
RC_LOW_REGIME_COHERENCE,Q3,FR,2018,,WARN,RC_LOW_REGIME_COHERENCE,,,FR-2018: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q3,FR,2021,,WARN,RC_LOW_REGIME_COHERENCE,,,FR-2021: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q3,FR,2023,,WARN,RC_LOW_REGIME_COHERENCE,,,FR-2023: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q3,FR,2024,,WARN,RC_LOW_REGIME_COHERENCE,,,FR-2024: regime_coherence < 0.55.
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2018,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2018: must_run_share=82.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2019,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2019: must_run_share=80.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2020,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2020: must_run_share=77.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2021,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2021: must_run_share=79.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2022,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2022: must_run_share=73.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2023,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2023: must_run_share=75.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2024,,WARN,RC_MR_SHARE_IMPLAUSIBLE,,,"FR-2024: must_run_share=79.2% hors plage plausible [5%,60%]."
TEST_DATA_001,Q3,DE,2018,,PASS,TEST_DATA_001,,,DE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2019,,PASS,TEST_DATA_001,,,DE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2020,,PASS,TEST_DATA_001,,,DE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2021,,PASS,TEST_DATA_001,,,DE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2022,,PASS,TEST_DATA_001,,,DE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2023,,PASS,TEST_DATA_001,,,DE-2023: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2024,,PASS,TEST_DATA_001,,,DE-2024: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2025,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2026,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2027,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2028,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2029,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2030,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2031,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2032,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,DE,2033,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2034,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2035,DEMAND_UP,PASS,TEST_DATA_001,,,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,,,DE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2018,,PASS,TEST_DATA_001,,,ES-2018: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2019,,PASS,TEST_DATA_001,,,ES-2019: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2020,,PASS,TEST_DATA_001,,,ES-2020: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2021,,PASS,TEST_DATA_001,,,ES-2021: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2022,,PASS,TEST_DATA_001,,,ES-2022: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2023,,PASS,TEST_DATA_001,,,ES-2023: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2024,,PASS,TEST_DATA_001,,,ES-2024: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2025,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2026,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2027,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2028,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2029,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2030,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2031,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2032,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,ES,2033,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2034,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2035,DEMAND_UP,PASS,TEST_DATA_001,,,ES-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,,,ES-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2018,,PASS,TEST_DATA_001,,,FR-2018: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2019,,PASS,TEST_DATA_001,,,FR-2019: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2020,,PASS,TEST_DATA_001,,,FR-2020: n_hours=8784 coherent.
TEST_DATA_001,Q3,FR,2021,,PASS,TEST_DATA_001,,,FR-2021: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2022,,PASS,TEST_DATA_001,,,FR-2022: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2023,,PASS,TEST_DATA_001,,,FR-2023: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2024,,PASS,TEST_DATA_001,,,FR-2024: n_hours=8784 coherent.
TEST_DATA_001,Q3,FR,2025,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2026,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2027,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2028,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,FR,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,FR,2029,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2030,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2031,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2032,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,FR,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,FR,2033,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2034,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2035,DEMAND_UP,PASS,TEST_DATA_001,,,FR-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,,,FR-2035: n_hours=8760 coherent.
TEST_DATA_002,Q3,DE,2018,,PASS,TEST_DATA_002,,,DE-2018: coverage price/load ok (100.00%/99.89%).
TEST_DATA_002,Q3,DE,2019,,PASS,TEST_DATA_002,,,DE-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2020,,PASS,TEST_DATA_002,,,DE-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2021,,PASS,TEST_DATA_002,,,DE-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2022,,PASS,TEST_DATA_002,,,DE-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2023,,PASS,TEST_DATA_002,,,DE-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2024,,PASS,TEST_DATA_002,,,DE-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,DE,2025,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2026,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2027,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2028,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2029,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2030,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2031,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2032,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2033,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2034,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2035,DEMAND_UP,PASS,TEST_DATA_002,,,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,,,DE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2018,,PASS,TEST_DATA_002,,,ES-2018: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q3,ES,2019,,PASS,TEST_DATA_002,,,ES-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2020,,PASS,TEST_DATA_002,,,ES-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2021,,PASS,TEST_DATA_002,,,ES-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2022,,PASS,TEST_DATA_002,,,ES-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2023,,PASS,TEST_DATA_002,,,ES-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2024,,PASS,TEST_DATA_002,,,ES-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,ES,2025,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2026,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2027,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2028,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2029,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2030,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2031,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2032,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2033,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2034,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2035,DEMAND_UP,PASS,TEST_DATA_002,,,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,,,ES-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2018,,PASS,TEST_DATA_002,,,FR-2018: coverage price/load ok (99.99%/99.79%).
TEST_DATA_002,Q3,FR,2019,,PASS,TEST_DATA_002,,,FR-2019: coverage price/load ok (99.99%/99.90%).
TEST_DATA_002,Q3,FR,2020,,PASS,TEST_DATA_002,,,FR-2020: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q3,FR,2021,,PASS,TEST_DATA_002,,,FR-2021: coverage price/load ok (99.99%/99.89%).
TEST_DATA_002,Q3,FR,2022,,PASS,TEST_DATA_002,,,FR-2022: coverage price/load ok (99.99%/99.75%).
TEST_DATA_002,Q3,FR,2023,,PASS,TEST_DATA_002,,,FR-2023: coverage price/load ok (99.99%/99.93%).
TEST_DATA_002,Q3,FR,2024,,PASS,TEST_DATA_002,,,FR-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,FR,2025,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2026,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2027,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2028,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2029,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2030,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2031,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2032,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2033,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2034,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2035,DEMAND_UP,PASS,TEST_DATA_002,,,FR-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,,,FR-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_003,Q3,DE,2018,,PASS,TEST_DATA_003,,,DE-2018: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2019,,PASS,TEST_DATA_003,,,DE-2019: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2020,,PASS,TEST_DATA_003,,,DE-2020: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2021,,PASS,TEST_DATA_003,,,DE-2021: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2022,,PASS,TEST_DATA_003,,,DE-2022: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2023,,PASS,TEST_DATA_003,,,DE-2023: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2024,,PASS,TEST_DATA_003,,,DE-2024: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2025,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2026,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2027,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2028,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2029,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2030,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2031,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2032,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2033,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2034,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2035,DEMAND_UP,PASS,TEST_DATA_003,,,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,DE,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,,,DE-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2018,,PASS,TEST_DATA_003,,,ES-2018: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2019,,PASS,TEST_DATA_003,,,ES-2019: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2020,,PASS,TEST_DATA_003,,,ES-2020: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2021,,PASS,TEST_DATA_003,,,ES-2021: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2022,,PASS,TEST_DATA_003,,,ES-2022: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2023,,PASS,TEST_DATA_003,,,ES-2023: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2024,,PASS,TEST_DATA_003,,,ES-2024: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2025,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2026,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2027,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2028,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2029,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2030,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2031,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2032,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2033,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2034,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2035,DEMAND_UP,PASS,TEST_DATA_003,,,ES-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,ES,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,,,ES-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2018,,PASS,TEST_DATA_003,,,FR-2018: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2019,,PASS,TEST_DATA_003,,,FR-2019: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2020,,PASS,TEST_DATA_003,,,FR-2020: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2021,,PASS,TEST_DATA_003,,,FR-2021: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2022,,PASS,TEST_DATA_003,,,FR-2022: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2023,,PASS,TEST_DATA_003,,,FR-2023: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2024,,PASS,TEST_DATA_003,,,FR-2024: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2025,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2026,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2027,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2028,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2029,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2030,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2031,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2032,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2033,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2034,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2035,DEMAND_UP,PASS,TEST_DATA_003,,,FR-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,,,FR-2035: prix dans plage large attendue.
TEST_Q3_001,Q3,,,,WARN,TEST_Q3_001,,,Colonnes predicted/target non disponibles dans Q3_status; test non applicable.
TEST_Q3_001,Q3,,,DEMAND_UP,WARN,TEST_Q3_001,,,Colonnes predicted/target non disponibles dans Q3_status; test non applicable.
TEST_Q3_001,Q3,,,LOW_RIGIDITY,WARN,TEST_Q3_001,,,Colonnes predicted/target non disponibles dans Q3_status; test non applicable.
BUNDLE_INFORMATIVENESS,Q4,,,,PASS,BUNDLE_INFORMATIVENESS,,,share_tests_informatifs=100.00% ; share_compare_informatifs=75.00%
BUNDLE_LEDGER_STATUS,Q4,,,,PASS,BUNDLE_LEDGER_STATUS,,,"ledger: FAIL=0, WARN=0"
Q4-H-01,Q4,,,nan,PASS,Simulation BESS 3 modes,"HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED",3 modes executes avec sorties non vides,Les trois modes Q4 sont disponibles.
Q4-H-02,Q4,,,nan,PASS,Invariants physiques BESS,WARN,aucun FAIL physique/structurel pertinent,Les invariants physiques batterie sont respectes. Des avertissements non-physiques peuvent subsister (objectif/scenario).
Q4-S-01,Q4,,,HIGH_CO2,PASS,Comparaison effet batteries par scenario,7,Q4 summary non vide pour >=1 scenario,Resultats Q4 prospectifs disponibles.
Q4-S-01,Q4,,,HIGH_GAS,PASS,Comparaison effet batteries par scenario,7,Q4 summary non vide pour >=1 scenario,Resultats Q4 prospectifs disponibles.
Q4-S-02,Q4,,,HIGH_CO2,PASS,Sensibilite valeur commodites,share_finite=100.00%,delta pv_capture ou revenus vs BASE,Sensibilite valeur exploitable sur le panel.
Q4-S-02,Q4,,,HIGH_GAS,PASS,Sensibilite valeur commodites,share_finite=100.00%,delta pv_capture ou revenus vs BASE,Sensibilite valeur exploitable sur le panel.
Q4_BESS_INEFFECTIVE,Q4,,,,WARN,Q4_BESS_INEFFECTIVE,,,h_negative>0 mais aucun point de frontier ne reduit h_negative.
Q4_CACHE_HIT,Q4,,,,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_CO2,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_CO2,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_CO2,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_CO2,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_CO2,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_CO2,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_CO2,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_GAS,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_GAS,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_GAS,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_GAS,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_GAS,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_GAS,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_CACHE_HIT,Q4,,,HIGH_GAS,INFO,Q4_CACHE_HIT,,,Resultat charge depuis cache persistant Q4.
Q4_OBJECTIVE_NOT_REACHED_GRID,Q4,,,,WARN,Q4_OBJECTIVE_NOT_REACHED_GRID,,,Objectif non atteint sur la grille courante; augmenter les bornes de recherche.
Q4_OBJECTIVE_UNREACHABLE,Q4,,,,WARN,Q4_OBJECTIVE_UNREACHABLE,,,Objectif non atteint sous les contraintes de policy actuelles.
Q4_OBJECTIVE_UNREACHABLE,Q4,,,,WARN,Q4_OBJECTIVE_UNREACHABLE,,,Objectif non atteint sous les contraintes de policy actuelles.
TEST_Q4_001,Q4,,,,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_CO2,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_CO2,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_CO2,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_CO2,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_CO2,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_CO2,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_CO2,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_GAS,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_GAS,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_GAS,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_GAS,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_GAS,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_GAS,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,,,HIGH_GAS,PASS,TEST_Q4_001,,,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_002,Q4,,,,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_CO2,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_CO2,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_CO2,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_CO2,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_CO2,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_CO2,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_CO2,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_GAS,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_GAS,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_GAS,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_GAS,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_GAS,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_GAS,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,,,HIGH_GAS,PASS,TEST_Q4_002,,,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
BUNDLE_INFORMATIVENESS,Q5,,,,PASS,BUNDLE_INFORMATIVENESS,,,share_tests_informatifs=100.00% ; share_compare_informatifs=100.00%
BUNDLE_LEDGER_STATUS,Q5,,,,PASS,BUNDLE_LEDGER_STATUS,,,"ledger: FAIL=0, WARN=0"
Q5-H-01,Q5,,,nan,PASS,Ancre thermique historique,share_fini=100.00%,Q5_summary non vide avec ttl_obs et tca_q95,L'ancre thermique est quantifiable sur la majorite des pays.
Q5-H-02,Q5,,,nan,PASS,Sensibilites analytiques,share_positive=100.00%,dTCA_dCO2 > 0 et dTCA_dGas > 0,Sensibilites analytiques globalement coherentes.
Q5-S-01,Q5,,,HIGH_BOTH,PASS,Sensibilites scenarisees,7,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-01,Q5,,,HIGH_CO2,PASS,Sensibilites scenarisees,7,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-01,Q5,,,HIGH_GAS,PASS,Sensibilites scenarisees,7,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-02,Q5,,,HIGH_BOTH,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5-S-02,Q5,,,HIGH_CO2,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5-S-02,Q5,,,HIGH_GAS,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5_ALPHA_NEGATIVE,Q5,,,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,,,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,,,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,,,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,,,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,,,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,,,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,,,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,,,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,,,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,,,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,,,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,,,HIGH_CO2,INFO,Q5_ALPHA_NEGATIVE,,,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_DISTRIBUTIONAL_FIT,Q5,,,,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=13.6 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=26.8 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=8.0 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=21.5 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=36.4 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,,WARN,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=39.2 EUR/MWh (a revoir).
Q5_DISTRIBUTIONAL_FIT,Q5,,,,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=20.5 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=36.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=71.7 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=62.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=45.3 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=21.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=42.5 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=50.9 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=10.9 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=25.2 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=40.5 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=33.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=33.8 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=15.5 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=28.0 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=10.9 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=20.8 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=41.2 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=34.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=22.9 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=16.6 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,,,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,,,Erreur distributionnelle p90/p95=29.0 EUR/MWh (acceptable).
Q5_LOW_CORR_CD,Q5,,,HIGH_BOTH,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_BOTH,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_BOTH,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_BOTH,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_BOTH,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_CO2,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_CO2,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_CO2,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_CO2,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_CO2,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_GAS,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_GAS,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_GAS,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_GAS,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_GAS,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_GAS,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,,,HIGH_GAS,INFO,Q5_LOW_CORR_CD,,,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_CO2,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_CO2,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,,,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,,,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
TEST_Q5_001,Q5,,,,WARN,TEST_Q5_001,,,Comparaison BASE/HIGH_CO2/HIGH_GAS indisponible (table Q5_summary manquante).
TEST_Q5_002,Q5,,,,WARN,TEST_Q5_002,,,Impossible d'evaluer la coherence delta_ttl_vs_base vs delta_tca_vs_base (donnees manquantes).
```
