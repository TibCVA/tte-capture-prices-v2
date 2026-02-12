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
    "ES",
    "FR",
    "NL",
    "BE",
    "CZ",
    "IT_NORD"
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
BASE,BE,2025,83.52865,9.281,historical_mean_2018_2024,2.66535,3.4558,0.5091,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2026,85.11968,9.4578,historical_mean_2018_2024,2.7117,3.49282,0.51836,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2027,86.71071,9.6346,historical_mean_2018_2024,2.75805,3.52984,0.52762,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2028,88.30174000000001,9.8114,historical_mean_2018_2024,2.8044,3.56686,0.53688,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2029,89.89277,9.9882,historical_mean_2018_2024,2.85075,3.60388,0.54614,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2030,91.4838,10.165,historical_mean_2018_2024,2.8971,3.6409,0.5554,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,BE,2031,93.07483,10.3418,historical_mean_2018_2024,2.94345,3.67792,0.56466,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2032,94.66586,10.5186,historical_mean_2018_2024,2.9898,3.71494,0.57392,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2033,96.25689,10.6954,historical_mean_2018_2024,3.03615,3.75196,0.58318,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2034,97.84792,10.8722,historical_mean_2018_2024,3.0825,3.78898,0.59244,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2035,99.43895,11.049,historical_mean_2018_2024,3.12885,3.826,0.6017,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2036,101.02998,11.2258,historical_mean_2018_2024,3.1752,3.86302,0.6109600000000001,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2037,102.62101,11.4026,historical_mean_2018_2024,3.22155,3.90004,0.62022,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2038,104.21204,11.5794,historical_mean_2018_2024,3.2679,3.93706,0.62948,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2039,105.80307,11.7562,historical_mean_2018_2024,3.31425,3.97408,0.63874,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,BE,2040,107.3941,11.933,historical_mean_2018_2024,3.3606,4.0111,0.648,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,CZ,2025,62.744400000000006,6.9725,historical_mean_2018_2024,1.15,1.12,0.1649999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2026,63.93954000000001,7.105200000000001,historical_mean_2018_2024,1.17,1.132,0.1679999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2027,65.13468,7.237900000000001,historical_mean_2018_2024,1.19,1.144,0.1709999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2028,66.32982,7.3706,historical_mean_2018_2024,1.21,1.156,0.174,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2029,67.52496000000001,7.5033,historical_mean_2018_2024,1.23,1.168,0.177,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2030,68.7201,7.636,historical_mean_2018_2024,1.25,1.18,0.18,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,CZ,2031,69.91524,7.7687,historical_mean_2018_2024,1.27,1.192,0.183,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2032,71.11038,7.9014,historical_mean_2018_2024,1.29,1.204,0.186,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2033,72.30552,8.0341,historical_mean_2018_2024,1.31,1.216,0.189,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2034,73.50066,8.1668,historical_mean_2018_2024,1.33,1.228,0.192,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2035,74.69579999999999,8.2995,historical_mean_2018_2024,1.35,1.24,0.195,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2036,75.89094,8.4322,historical_mean_2018_2024,1.37,1.252,0.1979999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2037,77.08608,8.5649,historical_mean_2018_2024,1.39,1.264,0.2009999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2038,78.28121999999999,8.6976,historical_mean_2018_2024,1.41,1.276,0.204,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2039,79.47636,8.8303,historical_mean_2018_2024,1.43,1.288,0.207,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,CZ,2040,80.6715,8.963,historical_mean_2018_2024,1.45,1.3,0.21,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
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
BASE,IT_NORD,2025,162.49095,18.0545,historical_mean_2018_2024,3.6597500000000007,1.12,0.1649999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2026,165.58602,18.3984,historical_mean_2018_2024,3.7234,1.132,0.1679999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2027,168.68108999999998,18.7423,historical_mean_2018_2024,3.78705,1.144,0.1709999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2028,171.77615999999998,19.0862,historical_mean_2018_2024,3.8507,1.156,0.174,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2029,174.87123,19.4301,historical_mean_2018_2024,3.91435,1.168,0.177,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2030,177.9663,19.774,historical_mean_2018_2024,3.978,1.18,0.18,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,IT_NORD,2031,181.06137,20.1179,historical_mean_2018_2024,4.04165,1.192,0.183,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2032,184.15644,20.4618,historical_mean_2018_2024,4.1053,1.204,0.186,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2033,187.25151,20.8057,historical_mean_2018_2024,4.16895,1.216,0.189,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2034,190.34658,21.1496,historical_mean_2018_2024,4.2326,1.228,0.192,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2035,193.44165,21.4935,historical_mean_2018_2024,4.29625,1.24,0.195,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2036,196.53672,21.8374,historical_mean_2018_2024,4.3599,1.252,0.1979999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2037,199.63179,22.1813,historical_mean_2018_2024,4.42355,1.264,0.2009999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2038,202.72686,22.5252,historical_mean_2018_2024,4.4872,1.276,0.204,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2039,205.82193,22.8691,historical_mean_2018_2024,4.55085,1.288,0.207,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,IT_NORD,2040,208.917,23.213,historical_mean_2018_2024,4.6145,1.3,0.21,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,NL,2025,120.78525,13.421,historical_mean_2018_2024,1.15,6.098049999999999,0.8983,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2026,123.08592,13.6766,historical_mean_2018_2024,1.17,6.163379999999999,0.91464,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2027,125.38659,13.9322,historical_mean_2018_2024,1.19,6.22871,0.93098,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2028,127.68726,14.1878,historical_mean_2018_2024,1.21,6.29404,0.94732,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2029,129.98793,14.4434,historical_mean_2018_2024,1.23,6.359369999999999,0.96366,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2030,132.2886,14.699,historical_mean_2018_2024,1.25,6.4247,0.98,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
BASE,NL,2031,134.58927,14.9546,historical_mean_2018_2024,1.27,6.49003,0.99634,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2032,136.88994,15.2102,historical_mean_2018_2024,1.29,6.555359999999999,1.01268,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2033,139.19061,15.4658,historical_mean_2018_2024,1.31,6.62069,1.02902,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2034,141.49128,15.7214,historical_mean_2018_2024,1.33,6.68602,1.04536,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2035,143.79195,15.977,historical_mean_2018_2024,1.35,6.75135,1.0617,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2036,146.09262,16.232599999999998,historical_mean_2018_2024,1.37,6.81668,1.07804,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2037,148.39329,16.4882,historical_mean_2018_2024,1.39,6.88201,1.09438,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2038,150.69396,16.7438,historical_mean_2018_2024,1.41,6.9473400000000005,1.11072,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2039,152.99463,16.999399999999998,historical_mean_2018_2024,1.43,7.01267,1.12706,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
BASE,NL,2040,155.2953,17.255,historical_mean_2018_2024,1.45,7.078,1.1434,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,BE,2025,91.88155,10.2085,historical_mean_2018_2024,2.66535,3.4558,0.5091,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2026,93.63168,10.403,historical_mean_2018_2024,2.7117,3.49282,0.51836,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2027,95.38181,10.597499999999998,historical_mean_2018_2024,2.75805,3.52984,0.52762,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2028,97.13194,10.792,historical_mean_2018_2024,2.8044,3.56686,0.53688,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2029,98.88207,10.9865,historical_mean_2018_2024,2.85075,3.60388,0.54614,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2030,100.6322,11.181,historical_mean_2018_2024,2.8971,3.6409,0.5554,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,BE,2031,102.38233,11.3755,historical_mean_2018_2024,2.94345,3.67792,0.56466,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2032,104.13246,11.57,historical_mean_2018_2024,2.9898,3.71494,0.57392,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2033,105.88259,11.7645,historical_mean_2018_2024,3.03615,3.75196,0.58318,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2034,107.63272,11.959,historical_mean_2018_2024,3.0825,3.78898,0.59244,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2035,109.38285,12.1535,historical_mean_2018_2024,3.12885,3.826,0.6017,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2036,111.13298,12.348,historical_mean_2018_2024,3.1752,3.86302,0.6109600000000001,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2037,112.88311,12.5425,historical_mean_2018_2024,3.22155,3.90004,0.62022,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2038,114.63324,12.737,historical_mean_2018_2024,3.2679,3.93706,0.62948,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2039,116.38337,12.9315,historical_mean_2018_2024,3.31425,3.97408,0.63874,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,BE,2040,118.1335,13.126,historical_mean_2018_2024,3.3606,4.0111,0.648,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,CZ,2025,69.01885,7.668499999999999,historical_mean_2018_2024,1.15,1.12,0.1649999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2026,70.3335,7.814599999999999,historical_mean_2018_2024,1.17,1.132,0.1679999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2027,71.64815,7.960699999999999,historical_mean_2018_2024,1.19,1.144,0.1709999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2028,72.9628,8.1068,historical_mean_2018_2024,1.21,1.156,0.174,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2029,74.27745,8.252899999999999,historical_mean_2018_2024,1.23,1.168,0.177,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2030,75.5921,8.399,historical_mean_2018_2024,1.25,1.18,0.18,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,CZ,2031,76.90675,8.5451,historical_mean_2018_2024,1.27,1.192,0.183,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2032,78.2214,8.691199999999998,historical_mean_2018_2024,1.29,1.204,0.186,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2033,79.53605,8.837299999999999,historical_mean_2018_2024,1.31,1.216,0.189,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2034,80.8507,8.9834,historical_mean_2018_2024,1.33,1.228,0.192,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2035,82.16535,9.1295,historical_mean_2018_2024,1.35,1.24,0.195,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2036,83.48,9.2756,historical_mean_2018_2024,1.37,1.252,0.1979999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2037,84.79465,9.4217,historical_mean_2018_2024,1.39,1.264,0.2009999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2038,86.1093,9.5678,historical_mean_2018_2024,1.41,1.276,0.204,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2039,87.42395,9.7139,historical_mean_2018_2024,1.43,1.288,0.207,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,CZ,2040,88.7386,9.86,historical_mean_2018_2024,1.45,1.3,0.21,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
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
DEMAND_UP,IT_NORD,2025,178.74,19.859500000000004,historical_mean_2018_2024,3.6597500000000007,1.12,0.1649999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2026,182.14458,20.237800000000004,historical_mean_2018_2024,3.7234,1.132,0.1679999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2027,185.54916,20.616100000000003,historical_mean_2018_2024,3.78705,1.144,0.1709999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2028,188.95374,20.9944,historical_mean_2018_2024,3.8507,1.156,0.174,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2029,192.35832,21.3727,historical_mean_2018_2024,3.91435,1.168,0.177,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2030,195.7629,21.751,historical_mean_2018_2024,3.978,1.18,0.18,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,IT_NORD,2031,199.16748,22.1293,historical_mean_2018_2024,4.04165,1.192,0.183,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2032,202.57206,22.5076,historical_mean_2018_2024,4.1053,1.204,0.186,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2033,205.97664,22.8859,historical_mean_2018_2024,4.16895,1.216,0.189,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2034,209.38122,23.2642,historical_mean_2018_2024,4.2326,1.228,0.192,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2035,212.7858,23.6425,historical_mean_2018_2024,4.29625,1.24,0.195,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2036,216.19038,24.0208,historical_mean_2018_2024,4.3599,1.252,0.1979999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2037,219.59496,24.3991,historical_mean_2018_2024,4.42355,1.264,0.2009999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2038,222.99954,24.7774,historical_mean_2018_2024,4.4872,1.276,0.204,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2039,226.40412,25.1557,historical_mean_2018_2024,4.55085,1.288,0.207,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,IT_NORD,2040,229.8087,25.534,historical_mean_2018_2024,4.6145,1.3,0.21,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,NL,2025,132.86385,14.763,historical_mean_2018_2024,1.15,6.098049999999999,0.8983,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2026,135.39458000000002,15.0442,historical_mean_2018_2024,1.17,6.163379999999999,0.91464,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2027,137.92531000000002,15.3254,historical_mean_2018_2024,1.19,6.22871,0.93098,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2028,140.45604,15.6066,historical_mean_2018_2024,1.21,6.29404,0.94732,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2029,142.98677,15.8878,historical_mean_2018_2024,1.23,6.359369999999999,0.96366,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2030,145.5175,16.169,historical_mean_2018_2024,1.25,6.4247,0.98,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
DEMAND_UP,NL,2031,148.04823000000002,16.450200000000002,historical_mean_2018_2024,1.27,6.49003,0.99634,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2032,150.57896000000002,16.7314,historical_mean_2018_2024,1.29,6.555359999999999,1.01268,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2033,153.10969,17.0126,historical_mean_2018_2024,1.31,6.62069,1.02902,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2034,155.64042,17.2938,historical_mean_2018_2024,1.33,6.68602,1.04536,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2035,158.17115,17.575000000000003,historical_mean_2018_2024,1.35,6.75135,1.0617,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2036,160.70188000000002,17.8562,historical_mean_2018_2024,1.37,6.81668,1.07804,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2037,163.23261000000002,18.1374,historical_mean_2018_2024,1.39,6.88201,1.09438,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2038,165.76334000000003,18.4186,historical_mean_2018_2024,1.41,6.9473400000000005,1.11072,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2039,168.29407,18.699800000000003,historical_mean_2018_2024,1.43,7.01267,1.12706,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
DEMAND_UP,NL,2040,170.8248,18.981,historical_mean_2018_2024,1.45,7.078,1.1434,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,BE,2025,83.52865,9.281,historical_mean_2018_2024,2.66535,3.4558,0.5091,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,120.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2026,85.11968,9.4578,historical_mean_2018_2024,2.7117,3.49282,0.51836,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,123.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2027,86.71071,9.6346,historical_mean_2018_2024,2.75805,3.52984,0.52762,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,126.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2028,88.30174000000001,9.8114,historical_mean_2018_2024,2.8044,3.56686,0.53688,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,129.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2029,89.89277,9.9882,historical_mean_2018_2024,2.85075,3.60388,0.54614,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,132.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2030,91.4838,10.165,historical_mean_2018_2024,2.8971,3.6409,0.5554,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,135.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,BE,2031,93.07483,10.3418,historical_mean_2018_2024,2.94345,3.67792,0.56466,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,138.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2032,94.66586,10.5186,historical_mean_2018_2024,2.9898,3.71494,0.57392,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,141.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2033,96.25689,10.6954,historical_mean_2018_2024,3.03615,3.75196,0.58318,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,144.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2034,97.84792,10.8722,historical_mean_2018_2024,3.0825,3.78898,0.59244,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,147.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2035,99.43895,11.049,historical_mean_2018_2024,3.12885,3.826,0.6017,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,150.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2036,101.02998,11.2258,historical_mean_2018_2024,3.1752,3.86302,0.6109600000000001,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,153.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2037,102.62101,11.4026,historical_mean_2018_2024,3.22155,3.90004,0.62022,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,156.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2038,104.21204,11.5794,historical_mean_2018_2024,3.2679,3.93706,0.62948,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,159.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2039,105.80307,11.7562,historical_mean_2018_2024,3.31425,3.97408,0.63874,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,162.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,BE,2040,107.3941,11.933,historical_mean_2018_2024,3.3606,4.0111,0.648,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,165.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,CZ,2025,62.744400000000006,6.9725,historical_mean_2018_2024,1.15,1.12,0.1649999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,120.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2026,63.93954000000001,7.105200000000001,historical_mean_2018_2024,1.17,1.132,0.1679999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,123.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2027,65.13468,7.237900000000001,historical_mean_2018_2024,1.19,1.144,0.1709999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,126.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2028,66.32982,7.3706,historical_mean_2018_2024,1.21,1.156,0.174,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,129.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2029,67.52496000000001,7.5033,historical_mean_2018_2024,1.23,1.168,0.177,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,132.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2030,68.7201,7.636,historical_mean_2018_2024,1.25,1.18,0.18,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,135.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,CZ,2031,69.91524,7.7687,historical_mean_2018_2024,1.27,1.192,0.183,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,138.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2032,71.11038,7.9014,historical_mean_2018_2024,1.29,1.204,0.186,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,141.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2033,72.30552,8.0341,historical_mean_2018_2024,1.31,1.216,0.189,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,144.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2034,73.50066,8.1668,historical_mean_2018_2024,1.33,1.228,0.192,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,147.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2035,74.69579999999999,8.2995,historical_mean_2018_2024,1.35,1.24,0.195,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,150.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2036,75.89094,8.4322,historical_mean_2018_2024,1.37,1.252,0.1979999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,153.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2037,77.08608,8.5649,historical_mean_2018_2024,1.39,1.264,0.2009999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,156.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2038,78.28121999999999,8.6976,historical_mean_2018_2024,1.41,1.276,0.204,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,159.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2039,79.47636,8.8303,historical_mean_2018_2024,1.43,1.288,0.207,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,162.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,CZ,2040,80.6715,8.963,historical_mean_2018_2024,1.45,1.3,0.21,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,165.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
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
HIGH_CO2,IT_NORD,2025,162.49095,18.0545,historical_mean_2018_2024,3.6597500000000007,1.12,0.1649999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,120.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2026,165.58602,18.3984,historical_mean_2018_2024,3.7234,1.132,0.1679999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,123.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2027,168.68108999999998,18.7423,historical_mean_2018_2024,3.78705,1.144,0.1709999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,126.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2028,171.77615999999998,19.0862,historical_mean_2018_2024,3.8507,1.156,0.174,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,129.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2029,174.87123,19.4301,historical_mean_2018_2024,3.91435,1.168,0.177,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,132.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2030,177.9663,19.774,historical_mean_2018_2024,3.978,1.18,0.18,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,135.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,IT_NORD,2031,181.06137,20.1179,historical_mean_2018_2024,4.04165,1.192,0.183,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,138.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2032,184.15644,20.4618,historical_mean_2018_2024,4.1053,1.204,0.186,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,141.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2033,187.25151,20.8057,historical_mean_2018_2024,4.16895,1.216,0.189,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,144.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2034,190.34658,21.1496,historical_mean_2018_2024,4.2326,1.228,0.192,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,147.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2035,193.44165,21.4935,historical_mean_2018_2024,4.29625,1.24,0.195,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,150.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2036,196.53672,21.8374,historical_mean_2018_2024,4.3599,1.252,0.1979999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,153.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2037,199.63179,22.1813,historical_mean_2018_2024,4.42355,1.264,0.2009999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,156.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2038,202.72686,22.5252,historical_mean_2018_2024,4.4872,1.276,0.204,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,159.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2039,205.82193,22.8691,historical_mean_2018_2024,4.55085,1.288,0.207,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,162.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,IT_NORD,2040,208.917,23.213,historical_mean_2018_2024,4.6145,1.3,0.21,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,165.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,NL,2025,120.78525,13.421,historical_mean_2018_2024,1.15,6.098049999999999,0.8983,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,120.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2026,123.08592,13.6766,historical_mean_2018_2024,1.17,6.163379999999999,0.91464,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,123.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2027,125.38659,13.9322,historical_mean_2018_2024,1.19,6.22871,0.93098,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,126.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2028,127.68726,14.1878,historical_mean_2018_2024,1.21,6.29404,0.94732,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,129.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2029,129.98793,14.4434,historical_mean_2018_2024,1.23,6.359369999999999,0.96366,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,132.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2030,132.2886,14.699,historical_mean_2018_2024,1.25,6.4247,0.98,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,135.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_CO2,NL,2031,134.58927,14.9546,historical_mean_2018_2024,1.27,6.49003,0.99634,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,138.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2032,136.88994,15.2102,historical_mean_2018_2024,1.29,6.555359999999999,1.01268,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,141.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2033,139.19061,15.4658,historical_mean_2018_2024,1.31,6.62069,1.02902,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,144.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2034,141.49128,15.7214,historical_mean_2018_2024,1.33,6.68602,1.04536,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,147.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2035,143.79195,15.977,historical_mean_2018_2024,1.35,6.75135,1.0617,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,150.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2036,146.09262,16.232599999999998,historical_mean_2018_2024,1.37,6.81668,1.07804,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,153.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2037,148.39329,16.4882,historical_mean_2018_2024,1.39,6.88201,1.09438,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,156.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2038,150.69396,16.7438,historical_mean_2018_2024,1.41,6.9473400000000005,1.11072,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,159.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2039,152.99463,16.999399999999998,historical_mean_2018_2024,1.43,7.01267,1.12706,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,162.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_CO2,NL,2040,155.2953,17.255,historical_mean_2018_2024,1.45,7.078,1.1434,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,165.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,BE,2025,83.52865,9.281,historical_mean_2018_2024,2.66535,3.4558,0.5091,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,58.5,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2026,85.11968,9.4578,historical_mean_2018_2024,2.7117,3.49282,0.51836,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,59.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2027,86.71071,9.6346,historical_mean_2018_2024,2.75805,3.52984,0.52762,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,60.3,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2028,88.30174000000001,9.8114,historical_mean_2018_2024,2.8044,3.56686,0.53688,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,61.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2029,89.89277,9.9882,historical_mean_2018_2024,2.85075,3.60388,0.54614,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,62.1,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2030,91.4838,10.165,historical_mean_2018_2024,2.8971,3.6409,0.5554,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,63.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,BE,2031,93.07483,10.3418,historical_mean_2018_2024,2.94345,3.67792,0.56466,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,63.9,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2032,94.66586,10.5186,historical_mean_2018_2024,2.9898,3.71494,0.57392,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,64.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2033,96.25689,10.6954,historical_mean_2018_2024,3.03615,3.75196,0.58318,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,65.7,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2034,97.84792,10.8722,historical_mean_2018_2024,3.0825,3.78898,0.59244,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,66.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2035,99.43895,11.049,historical_mean_2018_2024,3.12885,3.826,0.6017,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,67.5,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2036,101.02998,11.2258,historical_mean_2018_2024,3.1752,3.86302,0.6109600000000001,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,68.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2037,102.62101,11.4026,historical_mean_2018_2024,3.22155,3.90004,0.62022,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,69.3,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2038,104.21204,11.5794,historical_mean_2018_2024,3.2679,3.93706,0.62948,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,70.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2039,105.80307,11.7562,historical_mean_2018_2024,3.31425,3.97408,0.63874,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,71.1,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,BE,2040,107.3941,11.933,historical_mean_2018_2024,3.3606,4.0111,0.648,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,72.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,CZ,2025,62.744400000000006,6.9725,historical_mean_2018_2024,1.15,1.12,0.1649999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,58.5,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2026,63.93954000000001,7.105200000000001,historical_mean_2018_2024,1.17,1.132,0.1679999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,59.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2027,65.13468,7.237900000000001,historical_mean_2018_2024,1.19,1.144,0.1709999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,60.3,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2028,66.32982,7.3706,historical_mean_2018_2024,1.21,1.156,0.174,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,61.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2029,67.52496000000001,7.5033,historical_mean_2018_2024,1.23,1.168,0.177,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,62.1,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2030,68.7201,7.636,historical_mean_2018_2024,1.25,1.18,0.18,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,63.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,CZ,2031,69.91524,7.7687,historical_mean_2018_2024,1.27,1.192,0.183,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,63.9,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2032,71.11038,7.9014,historical_mean_2018_2024,1.29,1.204,0.186,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,64.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2033,72.30552,8.0341,historical_mean_2018_2024,1.31,1.216,0.189,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,65.7,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2034,73.50066,8.1668,historical_mean_2018_2024,1.33,1.228,0.192,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,66.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2035,74.69579999999999,8.2995,historical_mean_2018_2024,1.35,1.24,0.195,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,67.5,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2036,75.89094,8.4322,historical_mean_2018_2024,1.37,1.252,0.1979999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,68.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2037,77.08608,8.5649,historical_mean_2018_2024,1.39,1.264,0.2009999999999999,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,69.3,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2038,78.28121999999999,8.6976,historical_mean_2018_2024,1.41,1.276,0.204,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,70.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2039,79.47636,8.8303,historical_mean_2018_2024,1.43,1.288,0.207,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,71.1,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,CZ,2040,80.6715,8.963,historical_mean_2018_2024,1.45,1.3,0.21,6.0,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,72.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
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
HIGH_GAS,IT_NORD,2025,162.49095,18.0545,historical_mean_2018_2024,3.6597500000000007,1.12,0.1649999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,58.5,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2026,165.58602,18.3984,historical_mean_2018_2024,3.7234,1.132,0.1679999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,59.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2027,168.68108999999998,18.7423,historical_mean_2018_2024,3.78705,1.144,0.1709999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,60.3,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2028,171.77615999999998,19.0862,historical_mean_2018_2024,3.8507,1.156,0.174,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,61.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2029,174.87123,19.4301,historical_mean_2018_2024,3.91435,1.168,0.177,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,62.1,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2030,177.9663,19.774,historical_mean_2018_2024,3.978,1.18,0.18,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,63.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,IT_NORD,2031,181.06137,20.1179,historical_mean_2018_2024,4.04165,1.192,0.183,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,63.9,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2032,184.15644,20.4618,historical_mean_2018_2024,4.1053,1.204,0.186,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,64.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2033,187.25151,20.8057,historical_mean_2018_2024,4.16895,1.216,0.189,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,65.7,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2034,190.34658,21.1496,historical_mean_2018_2024,4.2326,1.228,0.192,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,66.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2035,193.44165,21.4935,historical_mean_2018_2024,4.29625,1.24,0.195,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,67.5,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2036,196.53672,21.8374,historical_mean_2018_2024,4.3599,1.252,0.1979999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,68.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2037,199.63179,22.1813,historical_mean_2018_2024,4.42355,1.264,0.2009999999999999,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,69.3,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2038,202.72686,22.5252,historical_mean_2018_2024,4.4872,1.276,0.204,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,70.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2039,205.82193,22.8691,historical_mean_2018_2024,4.55085,1.288,0.207,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,71.1,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,IT_NORD,2040,208.917,23.213,historical_mean_2018_2024,4.6145,1.3,0.21,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,72.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,NL,2025,120.78525,13.421,historical_mean_2018_2024,1.15,6.098049999999999,0.8983,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.5,0.5,0.88,80.0,58.5,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2026,123.08592,13.6766,historical_mean_2018_2024,1.17,6.163379999999999,0.91464,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.6,1.0,0.88,82.0,59.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2027,125.38659,13.9322,historical_mean_2018_2024,1.19,6.22871,0.93098,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.7,1.5,0.88,84.0,60.3,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2028,127.68726,14.1878,historical_mean_2018_2024,1.21,6.29404,0.94732,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.8,2.0,0.88,86.0,61.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2029,129.98793,14.4434,historical_mean_2018_2024,1.23,6.359369999999999,0.96366,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,0.9,2.5,0.88,88.0,62.1,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2030,132.2886,14.699,historical_mean_2018_2024,1.25,6.4247,0.98,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.0,3.0,0.88,90.0,63.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
HIGH_GAS,NL,2031,134.58927,14.9546,historical_mean_2018_2024,1.27,6.49003,0.99634,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.1,3.5,0.88,92.0,63.9,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2032,136.88994,15.2102,historical_mean_2018_2024,1.29,6.555359999999999,1.01268,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.2,4.0,0.88,94.0,64.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2033,139.19061,15.4658,historical_mean_2018_2024,1.31,6.62069,1.02902,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.3,4.5,0.88,96.0,65.7,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2034,141.49128,15.7214,historical_mean_2018_2024,1.33,6.68602,1.04536,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.4,5.0,0.88,98.0,66.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2035,143.79195,15.977,historical_mean_2018_2024,1.35,6.75135,1.0617,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.5,5.5,0.88,100.0,67.5,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2036,146.09262,16.232599999999998,historical_mean_2018_2024,1.37,6.81668,1.07804,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.6,6.0,0.88,102.0,68.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2037,148.39329,16.4882,historical_mean_2018_2024,1.39,6.88201,1.09438,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.7,6.5,0.88,104.0,69.3,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2038,150.69396,16.7438,historical_mean_2018_2024,1.41,6.9473400000000005,1.11072,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.8,7.0,0.88,106.0,70.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2039,152.99463,16.999399999999998,historical_mean_2018_2024,1.43,7.01267,1.12706,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,1.9,7.5,0.88,108.0,71.1,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
HIGH_GAS,NL,2040,155.2953,17.255,historical_mean_2018_2024,1.45,7.078,1.1434,1.5,1.0,1.2,1.0,0.55,3.0,0.45,1.0,2.0,8.0,0.88,110.0,72.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,BE,2025,83.52865,9.281,historical_mean_2018_2024,2.66535,3.4558,0.5091,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2026,85.11968,9.4578,historical_mean_2018_2024,2.7117,3.49282,0.51836,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2027,86.71071,9.6346,historical_mean_2018_2024,2.75805,3.52984,0.52762,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2028,88.30174000000001,9.8114,historical_mean_2018_2024,2.8044,3.56686,0.53688,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2029,89.89277,9.9882,historical_mean_2018_2024,2.85075,3.60388,0.54614,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2030,91.4838,10.165,historical_mean_2018_2024,2.8971,3.6409,0.5554,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,BE,2031,93.07483,10.3418,historical_mean_2018_2024,2.94345,3.67792,0.56466,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2032,94.66586,10.5186,historical_mean_2018_2024,2.9898,3.71494,0.57392,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2033,96.25689,10.6954,historical_mean_2018_2024,3.03615,3.75196,0.58318,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2034,97.84792,10.8722,historical_mean_2018_2024,3.0825,3.78898,0.59244,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2035,99.43895,11.049,historical_mean_2018_2024,3.12885,3.826,0.6017,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2036,101.02998,11.2258,historical_mean_2018_2024,3.1752,3.86302,0.6109600000000001,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2037,102.62101,11.4026,historical_mean_2018_2024,3.22155,3.90004,0.62022,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2038,104.21204,11.5794,historical_mean_2018_2024,3.2679,3.93706,0.62948,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2039,105.80307,11.7562,historical_mean_2018_2024,3.31425,3.97408,0.63874,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,BE,2040,107.3941,11.933,historical_mean_2018_2024,3.3606,4.0111,0.648,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,CZ,2025,62.744400000000006,6.9725,historical_mean_2018_2024,1.15,1.12,0.1649999999999999,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2026,63.93954000000001,7.105200000000001,historical_mean_2018_2024,1.17,1.132,0.1679999999999999,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2027,65.13468,7.237900000000001,historical_mean_2018_2024,1.19,1.144,0.1709999999999999,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2028,66.32982,7.3706,historical_mean_2018_2024,1.21,1.156,0.174,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2029,67.52496000000001,7.5033,historical_mean_2018_2024,1.23,1.168,0.177,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2030,68.7201,7.636,historical_mean_2018_2024,1.25,1.18,0.18,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,CZ,2031,69.91524,7.7687,historical_mean_2018_2024,1.27,1.192,0.183,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2032,71.11038,7.9014,historical_mean_2018_2024,1.29,1.204,0.186,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2033,72.30552,8.0341,historical_mean_2018_2024,1.31,1.216,0.189,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2034,73.50066,8.1668,historical_mean_2018_2024,1.33,1.228,0.192,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2035,74.69579999999999,8.2995,historical_mean_2018_2024,1.35,1.24,0.195,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2036,75.89094,8.4322,historical_mean_2018_2024,1.37,1.252,0.1979999999999999,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2037,77.08608,8.5649,historical_mean_2018_2024,1.39,1.264,0.2009999999999999,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2038,78.28121999999999,8.6976,historical_mean_2018_2024,1.41,1.276,0.204,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2039,79.47636,8.8303,historical_mean_2018_2024,1.43,1.288,0.207,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,CZ,2040,80.6715,8.963,historical_mean_2018_2024,1.45,1.3,0.21,6.0,1.0,1.2,1.0,0.42,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,coal,0.38,0.341,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
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
LOW_RIGIDITY,IT_NORD,2025,162.49095,18.0545,historical_mean_2018_2024,3.6597500000000007,1.12,0.1649999999999999,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2026,165.58602,18.3984,historical_mean_2018_2024,3.7234,1.132,0.1679999999999999,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2027,168.68108999999998,18.7423,historical_mean_2018_2024,3.78705,1.144,0.1709999999999999,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2028,171.77615999999998,19.0862,historical_mean_2018_2024,3.8507,1.156,0.174,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2029,174.87123,19.4301,historical_mean_2018_2024,3.91435,1.168,0.177,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2030,177.9663,19.774,historical_mean_2018_2024,3.978,1.18,0.18,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,IT_NORD,2031,181.06137,20.1179,historical_mean_2018_2024,4.04165,1.192,0.183,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2032,184.15644,20.4618,historical_mean_2018_2024,4.1053,1.204,0.186,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2033,187.25151,20.8057,historical_mean_2018_2024,4.16895,1.216,0.189,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2034,190.34658,21.1496,historical_mean_2018_2024,4.2326,1.228,0.192,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2035,193.44165,21.4935,historical_mean_2018_2024,4.29625,1.24,0.195,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2036,196.53672,21.8374,historical_mean_2018_2024,4.3599,1.252,0.1979999999999999,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2037,199.63179,22.1813,historical_mean_2018_2024,4.42355,1.264,0.2009999999999999,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2038,202.72686,22.5252,historical_mean_2018_2024,4.4872,1.276,0.204,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2039,205.82193,22.8691,historical_mean_2018_2024,4.55085,1.288,0.207,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,IT_NORD,2040,208.917,23.213,historical_mean_2018_2024,4.6145,1.3,0.21,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,NL,2025,120.78525,13.421,historical_mean_2018_2024,1.15,6.098049999999999,0.8983,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.5,0.5,0.88,80.0,39.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2026,123.08592,13.6766,historical_mean_2018_2024,1.17,6.163379999999999,0.91464,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.6,1.0,0.88,82.0,39.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2027,125.38659,13.9322,historical_mean_2018_2024,1.19,6.22871,0.93098,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.7,1.5,0.88,84.0,40.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2028,127.68726,14.1878,historical_mean_2018_2024,1.21,6.29404,0.94732,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.8,2.0,0.88,86.0,40.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2029,129.98793,14.4434,historical_mean_2018_2024,1.23,6.359369999999999,0.96366,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,0.9,2.5,0.88,88.0,41.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2030,132.2886,14.699,historical_mean_2018_2024,1.25,6.4247,0.98,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.0,3.0,0.88,90.0,42.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
LOW_RIGIDITY,NL,2031,134.58927,14.9546,historical_mean_2018_2024,1.27,6.49003,0.99634,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.1,3.5,0.88,92.0,42.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2032,136.88994,15.2102,historical_mean_2018_2024,1.29,6.555359999999999,1.01268,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.2,4.0,0.88,94.0,43.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2033,139.19061,15.4658,historical_mean_2018_2024,1.31,6.62069,1.02902,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.3,4.5,0.88,96.0,43.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2034,141.49128,15.7214,historical_mean_2018_2024,1.33,6.68602,1.04536,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.4,5.0,0.88,98.0,44.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2035,143.79195,15.977,historical_mean_2018_2024,1.35,6.75135,1.0617,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.5,5.5,0.88,100.0,45.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2036,146.09262,16.232599999999998,historical_mean_2018_2024,1.37,6.81668,1.07804,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.6,6.0,0.88,102.0,45.6,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2037,148.39329,16.4882,historical_mean_2018_2024,1.39,6.88201,1.09438,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.7,6.5,0.88,104.0,46.2,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2038,150.69396,16.7438,historical_mean_2018_2024,1.41,6.9473400000000005,1.11072,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.8,7.0,0.88,106.0,46.8,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2039,152.99463,16.999399999999998,historical_mean_2018_2024,1.43,7.01267,1.12706,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,1.9,7.5,0.88,108.0,47.4,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption_interpolated_2025_2039_from_2030_2040,Auto-generated baseline for phase2 engine | generated annual trajectory row
LOW_RIGIDITY,NL,2040,155.2953,17.255,historical_mean_2018_2024,1.45,7.078,1.1434,1.5,1.0,1.2,1.0,0.42,3.0,0.45,1.0,2.0,8.0,0.88,110.0,48.0,gas_ccgt,0.55,0.202,0.35,support_suspension,6.0,0.65,internal_assumption,Auto-generated baseline for phase2 engine
```

## RUN OUTPUTS

### A.1 annual_metrics_phase1
```csv
country,year,scenario_id,n_hours,timezone,coverage_price,coverage_load_total,coverage_psh_pumping,coverage_pv,coverage_wind,coverage_net_position,coverage_nuclear,coverage_biomass,coverage_ror,load_total_mw_avg,psh_pumping_mw_avg,load_mw_avg,must_run_mw_avg,must_run_nuclear_mw_avg,must_run_biomass_mw_avg,must_run_ror_mw_avg,nrl_mw_avg,nrl_p10_mw,nrl_p50_mw,nrl_p90_mw,surplus_mwh_total,sr_energy,sr_hours,far_energy,far_hours,sink_breakdown_json,ir_p10,baseload_price_eur_mwh,ttl_observed_eur_mwh,capture_price_pv_eur_mwh,capture_ratio_pv,capture_ratio_pv_vs_ttl_observed,capture_price_wind_eur_mwh,capture_ratio_wind,capture_ratio_wind_vs_ttl_observed,h_negative_obs,h_below_5_obs,days_spread_gt50,regime_coherence,nrl_price_corr,load_identity_abs_max_mw,load_identity_rel_err,load_identity_ok,data_quality_flags,quality_flag,quality_notes
BE,2018,HIST,8760,Europe/Brussels,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.2503632091191176,55.27868135631921,88.98300000000002,54.66041229590068,0.9888154159026832,0.6142792701516094,53.69438524907516,0.9713398353873188,0.6034229599932026,9,29,71,0.9998858317159494,0.7100576282926241,NaN,NaN,NaN,NaN,OK,NaN
BE,2019,HIST,8760,Europe/Brussels,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,108234.9125,0.0012484999966865,0.0230593607305936,1.0,NaN,NaN,0.5281338030873663,39.34488411919168,62.53999999999999,36.23116249255138,0.9208608260934872,0.5793278300695777,35.815679371150146,0.9103007969892568,0.5726843519531524,71,98,17,0.9964607831944284,0.6403103200269119,NaN,NaN,NaN,NaN,OK,NaN
BE,2020,HIST,8784,Europe/Brussels,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,105047.18249999991,0.0012849414218001,0.0203779599271402,1.0,NaN,NaN,0.4000857097802364,31.88140612546966,56.575499999999984,24.610657431609187,0.7719439141032126,0.4350055665722653,29.712746290762997,0.9319772839951952,0.5251875156342056,136,293,35,0.9974951611066832,0.7257373062890532,NaN,NaN,NaN,NaN,OK,NaN
BE,2021,HIST,8760,Europe/Brussels,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,878654.435,0.0094973833438082,0.1162100456621004,0.9999430663546356,NaN,NaN,0.6343503096335895,104.1341602922708,274.3134999999999,76.77596224342913,0.7372793138000433,0.2798840095125801,94.2549888953612,0.9051303494532248,0.3436031726304437,159,234,215,0.8990752368991894,0.4292874069974498,NaN,NaN,NaN,NaN,OK,NaN
BE,2022,HIST,8760,Europe/Brussels,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,654248.18,0.0073800773057295,0.0974885844748858,0.9988975819542976,NaN,NaN,0.5370723356597397,244.54961182783427,507.6275,225.0164499373449,0.9201259746662735,0.4432708037632809,188.50025770414453,0.7708057939460189,0.3713357879629148,113,160,361,0.9205388743007192,0.5860011505492821,NaN,NaN,NaN,NaN,OK,NaN
BE,2023,HIST,8760,Europe/Brussels,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,570207.9375,0.0073947875541729,0.0825342465753424,0.9695440665450225,NaN,NaN,0.3987854729972554,97.27812079004453,172.62599999999998,76.20741584522564,0.7833972863199546,0.4414596633486592,82.59429024630141,0.8490531023370071,0.4784579973254401,221,425,322,0.9611827834227652,0.7338178601563417,NaN,NaN,NaN,NaN,OK,NaN
BE,2024,HIST,8784,Europe/Brussels,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,424662.740667,0.0059439588031177,0.0539617486338797,0.9878408393166542,NaN,NaN,0.3943858333535832,70.32324035067745,131.856,39.10758174005171,0.5561117710878487,0.2965931147619502,60.26850267245005,0.8570211266135074,0.4570781964601539,404,738,303,0.990891494933394,0.7503403445852997,NaN,NaN,NaN,NaN,OK,NaN
CZ,2018,HIST,8760,Europe/Prague,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,3895559.64,0.0480998492331919,0.5091324200913242,0.3911743320145908,NaN,NaN,1.039550315178267,46.02857517981504,77.481,46.0569027951704,1.0006154354169057,0.5944283475325615,42.8589958908694,0.9311388789124284,0.5531549139901318,41,109,26,0.5096472200022834,0.2117967616085455,NaN,NaN,NaN,NaN,OK,NaN
CZ,2019,HIST,8760,Europe/Prague,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2554934.88,0.0320847190381809,0.447945205479452,0.8310527664016236,NaN,NaN,0.919915368716706,40.21401187350155,66.6,39.31259251238819,0.9775844458406964,0.5902791668526756,38.32583994610904,0.9530469147586664,0.5754630622538894,58,117,14,0.6426532709213381,0.4061618775850201,NaN,NaN,NaN,NaN,OK,NaN
CZ,2020,HIST,8784,Europe/Prague,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1359602.46,0.0181684751643834,0.2684426229508196,0.7728950490424974,NaN,NaN,0.8862924746997435,33.62335079130138,62.0075,28.878135133671726,0.8588714228072333,0.4657200360226057,32.49670601682515,0.96649219224255,0.5240770232121139,119,273,27,0.8095183877946032,0.2727229345621983,NaN,NaN,NaN,NaN,OK,NaN
CZ,2021,HIST,8760,Europe/Prague,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2043713.4500000002,0.0261723139208055,0.3047945205479452,0.9761426877138768,NaN,NaN,0.889195928147045,100.66678502112111,262.8125000000002,85.5711430580411,0.8500434680623526,0.3255976905894546,96.05033541767251,0.9541412830212068,0.3654709552158761,33,81,168,0.6677702934124901,-0.158811374960401,NaN,NaN,NaN,NaN,OK,NaN
CZ,2022,HIST,8760,Europe/Prague,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,3761019.58,0.0481388255227085,0.521689497716895,0.9999985961253623,NaN,NaN,1.0405540506932722,247.45665829432585,543.3065,237.30027823464425,0.9589569335911684,0.4367705489160248,197.11270341462549,0.7965544543165168,0.3628020342378114,8,58,363,0.4708300034250485,0.0448069114123201,NaN,NaN,NaN,NaN,OK,NaN
CZ,2023,HIST,8760,Europe/Prague,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2800387.37,0.0397238612692903,0.4434931506849315,0.9985400198401838,NaN,NaN,0.8909228000546017,100.7923198995319,181.31800000000004,80.22758006101299,0.795969178415404,0.4424689223409312,92.95481605659027,0.9222410611170184,0.5126618209807645,134,286,339,0.5708414202534536,0.1357804983469138,NaN,NaN,NaN,NaN,OK,NaN
CZ,2024,HIST,8784,Europe/Prague,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1990936.99,0.0293615584260879,0.3532559198542805,0.988700571583634,NaN,NaN,0.8497260413655197,85.10606854150062,170.0,53.46276957278948,0.6281898634140197,0.3144868798399381,79.46611022346208,0.9337302449203336,0.4674477071968357,315,531,320,0.6402140498690653,0.0879073378096901,NaN,NaN,NaN,NaN,OK,NaN
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
FR,2018,HIST,8760,Europe/Paris,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,26408823.0,0.0496520420270981,0.5723744292237443,0.9963003462895716,NaN,NaN,1.0521863248472143,50.20345359059253,85.55399999999993,51.22355835504443,1.020319414133753,0.5987278017982148,48.156834291105,0.9592334958431816,0.5628823233408728,11,56,28,0.5311108574038133,0.633364276131352,NaN,NaN,NaN,NaN,OK,NaN
FR,2019,HIST,8760,Europe/Paris,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,24110598.0,0.0461849869384012,0.5726027397260274,0.9893073286693262,NaN,NaN,1.027953453073615,39.44868249800206,70.31899999999999,37.75672972032813,0.9571100307910252,0.5369349638124565,37.31526142278841,0.9459190791651484,0.5306568839543853,27,81,9,0.6122845073638543,0.7570328459312552,NaN,NaN,NaN,NaN,OK,NaN
FR,2020,HIST,8784,Europe/Paris,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,14681307.0,0.030206233256013,0.4229280510018215,0.9937234947814932,NaN,NaN,0.8761151770927934,32.203028577934646,62.0665,29.859627395869648,0.9272304101338256,0.4810908847102648,30.14428687116799,0.9360699351061256,0.485677247326142,102,268,20,0.905613116247296,0.7498910249081551,NaN,NaN,NaN,NaN,OK,NaN
FR,2021,HIST,8760,Europe/Paris,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,23693657.0,0.0466692261905737,0.5075342465753425,0.8587565693214856,NaN,NaN,1.050096731493738,109.17437721201048,340.0,94.28927727889214,0.863657569539304,0.2773214037614475,102.52994263081202,0.939139249053875,0.3015586547965059,64,156,203,0.5111314076949424,0.5226537232532609,NaN,NaN,NaN,NaN,OK,NaN
FR,2022,HIST,8760,Europe/Paris,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1773457.0,0.0041442212851996,0.0776255707762557,0.9005983229365021,NaN,NaN,0.7147623702216469,275.8996323781253,564.3724999999994,291.49703235009645,1.0565328769651807,0.516497583333874,234.12950121641344,0.8486038897490622,0.4148492373678974,4,44,361,0.9228222399817332,0.5973274640247075,NaN,NaN,NaN,NaN,OK,NaN
FR,2023,HIST,8760,Europe/Paris,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,27558082.0,0.0581805500968788,0.6019406392694064,0.800669582157423,NaN,NaN,0.9605239758914184,96.86486813563192,193.012,83.59736517208924,0.8630308055035466,0.4331200400601477,86.0267300054073,0.888110742947083,0.4457066400296733,147,393,318,0.451078890284279,0.7070793930879798,NaN,NaN,NaN,NaN,OK,NaN
FR,2024,HIST,8784,Europe/Paris,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,55121278.57,0.1066722478632517,0.8502959927140255,0.858105007486948,NaN,NaN,1.063233556199511,58.01313787999545,158.54399999999998,39.24796162782507,0.6765357479716481,0.247552487813005,52.35986555431945,0.9025518609703508,0.3302544754410098,352,1026,284,0.2848684959581009,0.504660100561502,NaN,NaN,NaN,NaN,OK,NaN
IT_NORD,2018,HIST,8760,Europe/Rome,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.1020454822582611,60.7147208585455,87.01,60.82018624414457,1.001737064489595,0.6990022554205789,59.851523932093045,0.985782740754692,0.6878694854854964,0,0,32,0.9639228222399816,0.5613874545392398,NaN,NaN,NaN,NaN,OK,NaN
IT_NORD,2019,HIST,8760,Europe/Rome,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.1066922956221559,51.24951935152414,73.0,50.53720256383189,0.9861010054980922,0.6922904460798889,50.39543705281682,0.9833348232429436,0.6903484527783126,0,9,7,0.9974882977508848,0.7820712478964447,NaN,NaN,NaN,NaN,OK,NaN
IT_NORD,2020,HIST,8784,Europe/Rome,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.1571861997226075,37.79019583285893,63.09699999999999,33.351673404255465,0.8825483083434003,0.5285777993288979,36.0215089205279,0.9531972017251854,0.5708909919731193,0,39,10,0.9994307184333372,0.7845463853744407,NaN,NaN,NaN,NaN,OK,NaN
IT_NORD,2021,HIST,8760,Europe/Rome,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.1352550925060736,125.214559881265,296.23,106.18666146453138,0.8480376528514187,0.3584601879098382,131.95015170403667,1.0537924010527109,0.4454314272829783,0,4,134,0.9603836054344104,0.4045175273548155,NaN,NaN,NaN,NaN,OK,NaN
IT_NORD,2022,HIST,8760,Europe/Rome,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.0831310870867084,307.82841420253453,583.0,315.8243730250482,1.025975376065358,0.5417227667668065,282.8125557909755,0.9187344076849906,0.485098723483663,0,0,362,0.9633519808197284,0.2554660312015852,NaN,NaN,NaN,NaN,OK,NaN
IT_NORD,2023,HIST,8760,Europe/Rome,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.080019079574986,127.77134376070327,195.0,109.19917192457466,0.8546452491654817,0.5599957534593573,131.39439520999272,1.028355743491865,0.673817411333296,0,6,303,0.9948624272177188,0.6874701305832952,NaN,NaN,NaN,NaN,OK,NaN
IT_NORD,2024,HIST,8784,Europe/Rome,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1811.0,1.541671316084026e-05,0.0005692167577413,0.3147432357813363,NaN,NaN,0.1505694351399487,107.4095867015826,157.07949999999997,96.09890313752672,0.8946957724036264,0.611785135154662,105.4720019763206,0.9819607840904816,0.6714561860479606,0,16,275,0.9709666401001936,0.5038066097075028,NaN,NaN,NaN,NaN,OK,NaN
NL,2018,HIST,8760,Europe/Amsterdam,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.0,52.53533394223085,78.78400000000002,61.52181640152318,1.1710559690964195,0.7808922674848087,51.665421682951525,0.9834413870817704,0.6557857138879913,0,4,59,0.9670053659093504,0.5477142573908239,NaN,NaN,NaN,NaN,OK,NaN
NL,2019,HIST,8760,Europe/Amsterdam,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.0,41.19406096586368,60.2,38.786544885788345,0.9415567190117436,0.6442947655446568,40.12074010475579,0.9739447668925546,0.6664574768231858,3,16,9,0.9979449708870876,0.7375176512143253,NaN,NaN,NaN,NaN,OK,NaN
NL,2020,HIST,8784,Europe/Amsterdam,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.0007199508865821,32.24011841056586,55.90599999999999,25.41087852947092,0.788175719638274,0.4545286468262963,30.85764618032428,0.9571195051880296,0.5519558934698294,97,258,33,0.997039735853353,0.7225441407731813,NaN,NaN,NaN,NaN,OK,NaN
NL,2021,HIST,8760,Europe/Amsterdam,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.0008078249825603,102.98233245804316,250.1,78.99143623893805,0.7670387177443332,0.3158394091920753,99.24303029104162,0.9636898672058628,0.3968133958058441,70,151,213,0.9573010617650416,0.4392254105389844,NaN,NaN,NaN,NaN,OK,NaN
NL,2022,HIST,8760,Europe/Amsterdam,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.0,241.93680214636376,495.0,224.02024864076668,0.9259453156913344,0.4525661588702357,198.85504160196317,0.8219296933653872,0.4017273567716427,86,159,363,0.9797922137230276,0.5225736969377416,NaN,NaN,NaN,NaN,OK,NaN
NL,2023,HIST,8760,Europe/Amsterdam,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.0,95.82472428359402,166.561,70.9192164556589,0.7400930916928383,0.4257852465802852,83.77752192717547,0.8742787683816886,0.5029840234339099,315,538,343,0.987098983902272,0.5538583925069821,NaN,NaN,NaN,NaN,OK,NaN
NL,2024,HIST,8784,Europe/Amsterdam,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,0.0,0.0,0.0,NaN,NaN,NaN,0.0006673674536929,77.2893271091882,138.97799999999998,46.5701146150674,0.6025426324294019,0.3350898315925355,68.3161141440014,0.8839010080588466,0.491560636532411,458,781,315,0.9871342365934191,0.5520460299918933,NaN,NaN,NaN,NaN,OK,NaN
```

### A.2 q1_transition_summary
```csv
country,transition_year,stage,stage2_score,non_capture_flags_count,reason_codes,persistence_window_years,confidence_level
BE,2021,2,2.0,1,VALUE:capture_ratio_pv<=0.80 (0.737); PHYSICAL:sr_hours>=0.10 (0.116),2.0,0.8
CZ,2023,2,2.0,2,VALUE:capture_ratio_pv<=0.80 (0.796); PHYSICAL:sr_energy>=0.010 (0.040); PHYSICAL:sr_hours>=0.10 (0.443); UNEXPLAINED_NEGATIVE_PRICES:share>0.35 (0.537),2.0,1.0
DE,2019,2,2.0,1,LOW_PRICE:h_negative_obs>=200.0 (211.0); VALUE:capture_ratio_wind<=0.90 (0.870); UNEXPLAINED_NEGATIVE_PRICES:share>0.35 (0.559),2.0,0.8
ES,2023,2,3.0,4,LOW_PRICE:h_below_5_obs>=500.0 (558.0); LOW_PRICE:low_price_hours_share>=0.057 (0.064); VALUE:capture_ratio_wind<=0.90 (0.876); PHYSICAL:sr_energy>=0.010 (0.012); PHYSICAL:sr_hours>=0.10 (0.132),2.0,1.0
FR,2023,2,2.0,2,VALUE:capture_ratio_wind<=0.90 (0.888); PHYSICAL:sr_energy>=0.010 (0.058); PHYSICAL:sr_hours>=0.10 (0.602); PHYSICAL:far_observed<0.95 (0.801),2.0,0.8
IT_NORD,NaN,1,0.0,0,NaN,2.0,0.0
NL,2023,2,2.0,3,LOW_PRICE:h_negative_obs>=200.0 (315.0); LOW_PRICE:h_below_5_obs>=500.0 (538.0); LOW_PRICE:low_price_hours_share>=0.057 (0.061); VALUE:capture_ratio_pv<=0.80 (0.740); VALUE:capture_ratio_wind<=0.90 (0.874); UNEXPLAINED_NEGATIVE_PRICES:share>0.35 (1.000),2.0,0.8
```

### A.3 q2_slope_summary
```csv
country,tech,x_var_used,y_var_used,n_points,years_used,slope,intercept,r2,p_value,driver_stats_phase2,slope_quality_flag,slope_quality_notes
BE,PV,pv_penetration_share_load,capture_ratio_PV,3,"2021,2023,2024",NaN,NaN,NaN,NaN,"{""sr_energy_mean"": 0.0076120432336996, ""far_energy_mean"": 0.9857759907387708, ""ir_p10_mean"": 0.4758405386614761, ""ttl_mean"": 192.9318333333333, ""corr_vre_load_mean"": -0.951167128647036}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
BE,WIND,wind_penetration_share_load,capture_ratio_WIND,3,"2021,2023,2024",NaN,NaN,NaN,NaN,"{""sr_energy_mean"": 0.0076120432336996, ""far_energy_mean"": 0.9857759907387708, ""ir_p10_mean"": 0.4758405386614761, ""ttl_mean"": 192.9318333333333, ""corr_vre_load_mean"": -0.951167128647036}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
CZ,PV,pv_penetration_share_load,capture_ratio_PV,2,"2023,2024",NaN,NaN,NaN,NaN,"{""sr_energy_mean"": 0.0345427098476891, ""far_energy_mean"": 0.9936202957119088, ""ir_p10_mean"": 0.8703244207100607, ""ttl_mean"": 175.65900000000002, ""corr_vre_load_mean"": 1.0}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
CZ,WIND,wind_penetration_share_load,capture_ratio_WIND,2,"2023,2024",NaN,NaN,NaN,NaN,"{""sr_energy_mean"": 0.0345427098476891, ""far_energy_mean"": 0.9936202957119088, ""ir_p10_mean"": 0.8703244207100607, ""ttl_mean"": 175.65900000000002, ""corr_vre_load_mean"": 1.0}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
DE,PV,pv_penetration_share_load,capture_ratio_PV,4,"2019,2020,2023,2024",-5.534260520793036,1.367722666204194,0.8849617532735934,0.0592759420140285,"{""sr_energy_mean"": 0.0034716406677736, ""far_energy_mean"": 0.9969124061841632, ""ir_p10_mean"": 0.2484130319847082, ""ttl_mean"": 106.94787499999998, ""corr_vre_load_mean"": -0.969405517813395}",WARN,N_LT_6|PVALUE_GT_0_05|LOO_NOT_AVAILABLE
DE,WIND,wind_penetration_share_load,capture_ratio_WIND,4,"2019,2020,2023,2024",-0.3683517153592101,0.9470901671181964,0.3157002068487917,0.4381279444136844,"{""sr_energy_mean"": 0.0034716406677736, ""far_energy_mean"": 0.9969124061841632, ""ir_p10_mean"": 0.2484130319847082, ""ttl_mean"": 106.94787499999998, ""corr_vre_load_mean"": -0.969405517813395}",WARN,N_LT_6|PVALUE_GT_0_05|LOO_NOT_AVAILABLE
ES,PV,pv_penetration_share_load,capture_ratio_PV,2,"2023,2024",NaN,NaN,NaN,NaN,"{""sr_energy_mean"": 0.0131211164140113, ""far_energy_mean"": 0.9994805384070118, ""ir_p10_mean"": 0.2951420547224846, ""ttl_mean"": 144.664, ""corr_vre_load_mean"": 1.0}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
ES,WIND,wind_penetration_share_load,capture_ratio_WIND,2,"2023,2024",NaN,NaN,NaN,NaN,"{""sr_energy_mean"": 0.0131211164140113, ""far_energy_mean"": 0.9994805384070118, ""ir_p10_mean"": 0.2951420547224846, ""ttl_mean"": 144.664, ""corr_vre_load_mean"": 1.0}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
FR,PV,pv_penetration_share_load,capture_ratio_PV,2,"2023,2024",NaN,NaN,NaN,NaN,"{""sr_energy_mean"": 0.0824263989800653, ""far_energy_mean"": 0.8293872948221854, ""ir_p10_mean"": 1.011878766045465, ""ttl_mean"": 175.778, ""corr_vre_load_mean"": -1.0}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
FR,WIND,wind_penetration_share_load,capture_ratio_WIND,2,"2023,2024",NaN,NaN,NaN,NaN,"{""sr_energy_mean"": 0.0824263989800653, ""far_energy_mean"": 0.8293872948221854, ""ir_p10_mean"": 1.011878766045465, ""ttl_mean"": 175.778, ""corr_vre_load_mean"": -1.0}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
IT_NORD,PV,none,capture_ratio_PV,0,nan,NaN,NaN,NaN,NaN,"{""sr_energy_mean"": NaN, ""far_energy_mean"": NaN, ""ir_p10_mean"": NaN, ""ttl_mean"": NaN, ""corr_vre_load_mean"": NaN}",WARN,INSUFFICIENT_POINTS
IT_NORD,WIND,none,capture_ratio_WIND,0,nan,NaN,NaN,NaN,NaN,"{""sr_energy_mean"": NaN, ""far_energy_mean"": NaN, ""ir_p10_mean"": NaN, ""ttl_mean"": NaN, ""corr_vre_load_mean"": NaN}",WARN,INSUFFICIENT_POINTS
NL,PV,pv_penetration_share_load,capture_ratio_PV,2,"2023,2024",NaN,NaN,NaN,NaN,"{""sr_energy_mean"": 0.0, ""far_energy_mean"": NaN, ""ir_p10_mean"": 0.0003336837268464, ""ttl_mean"": 152.7695, ""corr_vre_load_mean"": 1.0}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
NL,WIND,wind_penetration_share_load,capture_ratio_WIND,2,"2023,2024",NaN,NaN,NaN,NaN,"{""sr_energy_mean"": 0.0, ""far_energy_mean"": NaN, ""ir_p10_mean"": 0.0003336837268464, ""ttl_mean"": 152.7695, ""corr_vre_load_mean"": 1.0}",WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE
```

### A.4 q3_inversion_requirements
```csv
country,scenario_id,year,lever,required_uplift,within_bounds,target_sr,target_h_negative,predicted_sr_after,predicted_h_negative_after,predicted_h_negative_metric,applicability_flag,status,reason
BE,HIST,2024,demand_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
BE,HIST,2024,export_uplift,NaN,False,0.05,200.0,0.0009107468123861,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
BE,HIST,2024,flex_uplift,NaN,False,0.05,200.0,0.0014799635701275,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
CZ,HIST,2024,demand_uplift,NaN,False,0.05,200.0,0.000455373406193,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
CZ,HIST,2024,export_uplift,NaN,False,0.05,200.0,0.0026183970856102,894.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
CZ,HIST,2024,flex_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
DE,HIST,2024,demand_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
DE,HIST,2024,export_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
DE,HIST,2024,flex_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
ES,HIST,2024,demand_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
ES,HIST,2024,export_uplift,NaN,False,0.05,200.0,0.0001138433515482,883.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
ES,HIST,2024,flex_uplift,NaN,False,0.05,200.0,0.0,883.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
FR,HIST,2024,demand_uplift,NaN,False,0.05,200.0,0.0001138433515482,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
FR,HIST,2024,export_uplift,NaN,False,0.05,200.0,0.0753642987249544,1530.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
FR,HIST,2024,flex_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
IT_NORD,HIST,2024,demand_uplift,NaN,False,0.05,200.0,NaN,NaN,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,q1_no_bascule
IT_NORD,HIST,2024,export_uplift,NaN,False,0.05,200.0,NaN,NaN,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,q1_no_bascule
IT_NORD,HIST,2024,flex_uplift,NaN,False,0.05,200.0,NaN,NaN,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,q1_no_bascule
NL,HIST,2024,demand_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
NL,HIST,2024,export_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
NL,HIST,2024,flex_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
```

### A.5 q4_bess_sizing_curve
```csv
country,scenario_id,year,bess_power_gw,bess_energy_gwh,cycles_realized_per_day,eta_roundtrip,far_energy_after,surplus_unabsorbed_twh_after,h_negative_proxy_after,h_negative_reducible_upper_bound,monotonicity_check_flag,physics_check_flag,on_efficient_frontier,notes
BE,HIGH_CO2,2035,NaN,NaN,0.0,0.88,0.7399553379352513,0.0138700778428006,52,0,PASS,PASS,True,dispatch_mode=; objective=
BE,HIGH_GAS,2035,NaN,NaN,0.0,0.88,0.7399553379352513,0.0138700778428006,39,0,PASS,PASS,True,dispatch_mode=; objective=
BE,HIST,2024,NaN,NaN,0.0,0.88,0.9878408393166542,0.0051635425,404,0,PASS,PASS,True,dispatch_mode=; objective=
CZ,HIGH_CO2,2035,NaN,NaN,0.0,0.88,0.9745675121650192,0.0009200504363572,0,0,PASS,PASS,True,dispatch_mode=; objective=
CZ,HIGH_GAS,2035,NaN,NaN,0.0,0.88,0.9745675121650192,0.0009200504363572,0,0,PASS,PASS,True,dispatch_mode=; objective=
CZ,HIST,2024,NaN,NaN,0.0,0.88,0.988700571583634,0.0224964499999999,315,0,PASS,PASS,True,dispatch_mode=; objective=
DE,HIGH_CO2,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
DE,HIGH_GAS,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
DE,HIST,2024,NaN,NaN,0.0,0.88,1.0,0.0,457,0,PASS,PASS,True,dispatch_mode=; objective=
ES,HIGH_CO2,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
ES,HIGH_GAS,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
ES,HIST,2024,NaN,NaN,0.0,0.88,0.9994023008613372,0.002132,247,0,PASS,PASS,True,dispatch_mode=; objective=
FR,HIGH_CO2,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
FR,HIGH_GAS,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
FR,HIST,2024,NaN,NaN,0.0,0.88,0.858105007486948,7.82143341,352,0,PASS,PASS,True,dispatch_mode=; objective=
IT_NORD,HIGH_CO2,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
IT_NORD,HIGH_GAS,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
IT_NORD,HIST,2024,NaN,NaN,0.0,0.88,0.3147432357813363,0.001241,0,0,PASS,PASS,True,dispatch_mode=; objective=
NL,HIGH_CO2,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
NL,HIGH_GAS,2035,NaN,NaN,0.0,0.88,1.0,0.0,0,0,PASS,PASS,True,dispatch_mode=; objective=
NL,HIST,2024,NaN,NaN,0.0,0.88,1.0,0.0,458,0,PASS,PASS,True,dispatch_mode=; objective=
```

### A.6 q5_anchor_sensitivity
```csv
country,scenario_id,year,gas_eur_per_mwh_th,co2_eur_per_t,tca_ccgt_eur_mwh,tca_coal_eur_mwh,ttl_observed_eur_mwh,ttl_model_eur_mwh,delta_tca_vs_base,delta_ttl_model_vs_base,coherence_flag
BE,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,154.96095511700383,180.8181818181818,NaN,NaN,WARN
BE,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,161.38822784427657,139.9090909090909,NaN,NaN,WARN
BE,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,169.2791369351857,162.45454545454544,NaN,NaN,WARN
BE,HIST,2024,46.9,70.69,114.23523636363636,135.31655263157896,131.856,131.856,0.0,0.0,PASS
CZ,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,183.09276473004675,236.30263157894737,NaN,NaN,WARN
CZ,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,198.79671209846785,203.7368421052632,NaN,NaN,WARN
CZ,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,203.8164489405731,191.43421052631575,NaN,NaN,WARN
CZ,HIST,2024,47.02,70.93,114.54156363636363,135.7056052631579,170.0,170.0,0.0,0.0,PASS
DE,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,212.65801522615288,236.30263157894737,NaN,NaN,WARN
DE,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,228.36196259457392,203.7368421052632,NaN,NaN,WARN
DE,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,233.3816994366792,191.43421052631575,NaN,NaN,WARN
DE,HIST,2024,46.9,70.83,114.28665454545454,135.4421842105263,146.069,146.069,0.0,0.0,PASS
ES,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,167.7630993635321,180.8181818181818,NaN,NaN,WARN
ES,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,174.19037209080483,139.9090909090909,NaN,NaN,WARN
ES,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,182.0812811817139,162.45454545454544,NaN,NaN,WARN
ES,HIST,2024,47.02,70.69,114.45341818181817,135.49023684210528,140.0,140.0,0.0,0.0,PASS
FR,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,189.1588026891639,180.8181818181818,NaN,NaN,WARN
FR,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,195.58607541643664,139.9090909090909,NaN,NaN,WARN
FR,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,203.4769845073457,162.45454545454544,NaN,NaN,WARN
FR,HIST,2024,47.73,68.25,114.8481818181818,134.3282894736842,158.54399999999998,158.54399999999998,0.0,0.0,PASS
IT_NORD,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,153.02801347759168,180.8181818181818,NaN,NaN,WARN
IT_NORD,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,159.45528620486442,139.9090909090909,NaN,NaN,WARN
IT_NORD,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,167.3461952957735,162.45454545454544,NaN,NaN,WARN
IT_NORD,HIST,2024,46.8,70.83,114.10483636363637,135.29744736842105,157.07949999999997,157.07949999999997,0.0,0.0,PASS
NL,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,157.04824742415067,180.8181818181818,NaN,NaN,WARN
NL,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,163.47552015142338,139.9090909090909,NaN,NaN,WARN
NL,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,171.3664292423325,162.45454545454544,NaN,NaN,WARN
NL,HIST,2024,46.8,70.83,114.10483636363637,135.29744736842105,138.97799999999998,138.97799999999998,0.0,0.0,PASS
```

## TEST LEDGER

```csv
test_id,scope,country,year,scenario_id,status,metric_name,observed_value,expected_rule,message
BUNDLE_INFORMATIVENESS,Q1,NaN,NaN,NaN,WARN,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=80.00% ; share_compare_informatifs=0.00%
BUNDLE_LEDGER_STATUS,Q1,NaN,NaN,NaN,PASS,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=0"
Q1-H-01,Q1,NaN,NaN,nan,PASS,Score marche de bascule,1.2244897959183674,stage2_market_score present et non vide,Le score de bascule marche est exploitable.
Q1-H-02,Q1,NaN,NaN,nan,PASS,Stress physique SR/FAR/IR,"far_energy,ir_p10,sr_energy",sr_energy/far_energy/ir_p10 presentes,Le stress physique est calculable.
Q1-H-03,Q1,NaN,NaN,nan,PASS,Concordance marche vs physique,strict=14.29%; concordant_ou_explique=85.71%; n=7; explained=6; reasons=physical_not_reached_but_explained:3;both_not_reached_in_window:1;market_physical_gap_flag:1;strict_equal_year:1;year_gap_unexplained:1,bascule_year_market et bascule_year_physical comparables,Concordance satisfaisante en comptant les divergences expliquees.
Q1-H-04,Q1,NaN,NaN,nan,PASS,Robustesse seuils,0.743,delta bascules sous choc de seuil <= 50%,Proxy de robustesse du diagnostic de bascule.
Q1-S-01,Q1,NaN,NaN,DEMAND_UP,PASS,Bascule projetee par scenario,7,Q1_country_summary non vide en SCEN,La bascule projetee est produite.
Q1-S-01,Q1,NaN,NaN,LOW_RIGIDITY,PASS,Bascule projetee par scenario,7,Q1_country_summary non vide en SCEN,La bascule projetee est produite.
Q1-S-02,Q1,NaN,NaN,DEMAND_UP,NON_TESTABLE,Effets DEMAND_UP/LOW_RIGIDITY,nan,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),Impossible d'evaluer la sensibilite sans BASE et scenario courant.
Q1-S-02,Q1,NaN,NaN,LOW_RIGIDITY,NON_TESTABLE,Effets DEMAND_UP/LOW_RIGIDITY,nan,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),Impossible d'evaluer la sensibilite sans BASE et scenario courant.
Q1-S-03,Q1,NaN,NaN,DEMAND_UP,PASS,Qualite de causalite,100.00%,part regime_coherence >= seuil min,La coherence scenario est lisible.
Q1-S-03,Q1,NaN,NaN,LOW_RIGIDITY,PASS,Qualite de causalite,100.00%,part regime_coherence >= seuil min,La coherence scenario est lisible.
Q1_CAPTURE_ONLY_SIGNAL,Q1,BE,2020,NaN,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,BE 2020: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,BE,2022,NaN,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,BE 2022: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2018,NaN,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,DE 2018: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2021,NaN,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,DE 2021: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,DE,2022,NaN,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,DE 2022: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,FR,2022,NaN,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,FR 2022: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,NL,2020,NaN,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,NL 2020: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,NL,2021,NaN,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,NL 2021: capture-only sans low-price ni stress physique.
Q1_CAPTURE_ONLY_SIGNAL,Q1,NL,2022,NaN,INFO,Q1_CAPTURE_ONLY_SIGNAL,NaN,NaN,NL 2022: capture-only sans low-price ni stress physique.
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,NaN,NaN,DEMAND_UP,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,NaN,NaN,"BE: coverage max=80.22% (>60%), possible surestimation must-run."
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,NaN,NaN,DEMAND_UP,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,NaN,NaN,"CZ: coverage max=89.16% (>60%), possible surestimation must-run."
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,NaN,NaN,LOW_RIGIDITY,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,NaN,NaN,"BE: coverage max=75.59% (>60%), possible surestimation must-run."
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,NaN,NaN,LOW_RIGIDITY,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,NaN,NaN,"CZ: coverage max=68.01% (>60%), possible surestimation must-run."
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,NaN,NaN,NaN,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,NaN,NaN,"BE: coverage max=61.72% (>60%), possible surestimation must-run."
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,NaN,NaN,NaN,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,NaN,NaN,"CZ: coverage max=84.76% (>60%), possible surestimation must-run."
Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,Q1,NaN,NaN,NaN,WARN,Q1_MUSTRUN_SCOPE_HIGH_COVERAGE,NaN,NaN,"FR: coverage max=87.11% (>60%), possible surestimation must-run."
Q1_S02_NO_SENSITIVITY,Q1,NaN,NaN,NaN,WARN,Q1_S02_NO_SENSITIVITY,NaN,NaN,Q1-S-02: aucune sensibilite scenario non-BASE clairement observable vs BASE.
RC_D_NOT_ABOVE_C,Q1,CZ,2018,NaN,WARN,RC_D_NOT_ABOVE_C,NaN,NaN,CZ-2018: median(price|D) <= median(price|C).
RC_D_NOT_ABOVE_C,Q1,CZ,2023,NaN,WARN,RC_D_NOT_ABOVE_C,NaN,NaN,CZ-2023: median(price|D) <= median(price|C).
RC_IR_GT_1,Q1,CZ,2018,NaN,WARN,RC_IR_GT_1,NaN,NaN,"CZ-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=6181.66, p10_load_mw=5946.48."
RC_IR_GT_1,Q1,CZ,2022,NaN,WARN,RC_IR_GT_1,NaN,NaN,"CZ-2022: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=5874.35, p10_load_mw=5645.40."
RC_IR_GT_1,Q1,FR,2018,NaN,WARN,RC_IR_GT_1,NaN,NaN,"FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40."
RC_IR_GT_1,Q1,FR,2019,NaN,WARN,RC_IR_GT_1,NaN,NaN,"FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00."
RC_IR_GT_1,Q1,FR,2021,NaN,WARN,RC_IR_GT_1,NaN,NaN,"FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00."
RC_IR_GT_1,Q1,FR,2024,NaN,WARN,RC_IR_GT_1,NaN,NaN,"FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60."
RC_LOW_REGIME_COHERENCE,Q1,CZ,2018,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,CZ-2018: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q1,CZ,2022,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,CZ-2022: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q1,FR,2018,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,FR-2018: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q1,FR,2021,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,FR-2021: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q1,FR,2023,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,FR-2023: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q1,FR,2024,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,FR-2024: regime_coherence < 0.55.
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2025,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2025,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2025: must_run_share=68.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2026,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2026,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2026: must_run_share=67.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2027,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2027,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2027: must_run_share=67.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2028,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2028,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2028: must_run_share=67.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2029,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2029,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2029: must_run_share=67.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2030,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2030,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2030: must_run_share=67.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2031,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2031,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2031: must_run_share=67.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2032,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2032,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2032: must_run_share=67.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2033,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2033,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2033: must_run_share=67.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2034,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2034,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2034: must_run_share=67.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2035,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,BE,2035,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2035: must_run_share=66.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2018,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2018: must_run_share=79.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2019,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2019: must_run_share=78.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2020,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2020: must_run_share=76.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2021,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2021: must_run_share=76.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2022,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2022: must_run_share=79.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2023,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2023: must_run_share=79.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2024,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2024: must_run_share=78.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2025,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2025,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2025: must_run_share=62.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2026,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2026,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2026: must_run_share=62.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2027,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2027,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2027: must_run_share=62.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2028,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2028,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2028: must_run_share=62.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2029,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2029,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2029: must_run_share=62.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2030,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2030,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2030: must_run_share=62.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2031,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2031,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2031: must_run_share=62.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2032,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2032,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2032: must_run_share=62.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2033,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2033,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2033: must_run_share=62.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2034,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2034,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2034: must_run_share=62.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2035,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,CZ,2035,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2035: must_run_share=62.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2018,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2018: must_run_share=82.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2019,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2019: must_run_share=80.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2020,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2020: must_run_share=77.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2021,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2021: must_run_share=79.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2022,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2022: must_run_share=73.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2023,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2023: must_run_share=75.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,FR,2024,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2024: must_run_share=79.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2018,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2018: must_run_share=0.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2019,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2019: must_run_share=0.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2020,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2020: must_run_share=0.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2021,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2021: must_run_share=0.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2022,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2022: must_run_share=0.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2023,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2023: must_run_share=0.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2024,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2024: must_run_share=0.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2025,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2025,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2025: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2026,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2026,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2026: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2027,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2027,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2027: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2028,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2028,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2028: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2029,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2029,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2029: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2030,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2030,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2030: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2031,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2031,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2031: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2032,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2032,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2032: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2033,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2033,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2033: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2034,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2034,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2034: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2035,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q1,NL,2035,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2035: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_NEG_NOT_IN_AB,Q1,BE,2018,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,BE-2018: 0.0% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,BE,2019,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,BE-2019: 26.8% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,CZ,2018,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,CZ-2018: 0.0% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,CZ,2019,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,CZ-2019: 36.2% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,CZ,2020,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,CZ-2020: 28.6% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,CZ,2021,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,CZ-2021: 0.0% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,CZ,2023,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,CZ-2023: 46.3% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,CZ,2024,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,CZ-2024: 20.6% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,DE,2018,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,DE-2018: 33.8% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,DE,2019,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,DE-2019: 44.1% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,DE,2020,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,DE-2020: 36.9% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,DE,2021,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,DE-2021: 41.0% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,FR,2018,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,FR-2018: 27.3% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,NL,2019,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,NL-2019: 0.0% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,NL,2020,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,NL-2020: 0.0% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,NL,2021,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,NL-2021: 0.0% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,NL,2022,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,NL-2022: 0.0% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,NL,2023,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,NL-2023: 0.0% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB,Q1,NL,2024,NaN,INFO,RC_NEG_NOT_IN_AB,NaN,NaN,NL-2024: 0.0% des heures negatives en regime A/B (check legacy).
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,BE,2018,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"BE-2018: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=963.0, p50=1143.1, p90=1639.7; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,BE,2019,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"BE-2019: 26.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-1098.4, p50=442.5, p90=1330.8; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,BE,2020,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"BE-2020: 61.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-1170.1, p50=-331.5, p90=935.4; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,BE,2024,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"BE-2024: 65.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-1890.1, p50=-475.8, p90=1240.2; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,CZ,2018,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"CZ-2018: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=740.2, p50=973.9, p90=1568.4; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,CZ,2019,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"CZ-2019: 36.2% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-603.6, p50=411.4, p90=754.4; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,CZ,2020,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"CZ-2020: 28.6% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-768.9, p50=241.3, p90=1210.1; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,CZ,2021,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"CZ-2021: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=418.7, p50=1039.2, p90=1706.2; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,CZ,2023,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"CZ-2023: 46.3% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-751.1, p50=119.7, p90=1134.0; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,CZ,2024,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"CZ-2024: 20.6% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-466.3, p50=418.8, p90=1353.6; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,DE,2018,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"DE-2018: 33.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-3039.5, p50=2341.7, p90=8765.7; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,DE,2019,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"DE-2019: 44.1% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-4050.2, p50=580.8, p90=5229.3; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,DE,2020,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"DE-2020: 36.9% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-3662.8, p50=1184.0, p90=5399.3; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,DE,2021,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"DE-2021: 41.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-4056.4, p50=598.4, p90=5182.9; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,FR,2018,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"FR-2018: 27.3% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-7350.0, p50=375.0, p90=2173.0; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,FR,2020,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"FR-2020: 52.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-5301.0, p50=-216.0, p90=2362.8; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,NL,2019,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"NL-2019: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=8995.7, p50=9175.7, p90=9192.9; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,NL,2020,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"NL-2020: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6769.6, p50=7430.8, p90=8315.3; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,NL,2021,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"NL-2021: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6325.9, p50=7246.4, p90=8079.5; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,NL,2022,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"NL-2022: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=5037.0, p50=5902.3, p90=7074.9; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,NL,2023,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"NL-2023: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6180.9, p50=8241.0, p90=10256.6; causes=price_or_regime_mapping)."
RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,Q1,NL,2024,NaN,WARN,RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL,NaN,NaN,"NL-2024: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6637.0, p50=9062.7, p90=11059.5; causes=price_or_regime_mapping)."
TEST_DATA_001,Q1,BE,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,BE,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,BE,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,BE,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,BE,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,BE,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,BE,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,BE,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,CZ,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,CZ,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,CZ,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,CZ,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,CZ,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,CZ,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,CZ,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2035: n_hours=8760 coherent.
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
TEST_DATA_001,Q1,FR,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,FR,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,FR,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,FR,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,FR,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,FR,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,FR,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,FR,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,IT_NORD,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,IT_NORD,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,IT_NORD,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,IT_NORD,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,IT_NORD,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,IT_NORD,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,IT_NORD,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2018: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2019: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2020: n_hours=8784 coherent.
TEST_DATA_001,Q1,NL,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2021: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2022: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2023: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2024: n_hours=8784 coherent.
TEST_DATA_001,Q1,NL,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2025: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2026: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2027: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,NL,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2028: n_hours=8784 coherent.
TEST_DATA_001,Q1,NL,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2029: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2030: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2031: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,NL,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2032: n_hours=8784 coherent.
TEST_DATA_001,Q1,NL,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2033: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2034: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2035: n_hours=8760 coherent.
TEST_DATA_001,Q1,NL,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2035: n_hours=8760 coherent.
TEST_DATA_002,Q1,BE,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2018: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,BE,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,BE,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,BE,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,BE,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,BE,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,BE,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,BE,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,BE,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2018: coverage price/load ok (99.99%/99.91%).
TEST_DATA_002,Q1,CZ,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2019: coverage price/load ok (99.99%/99.94%).
TEST_DATA_002,Q1,CZ,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,CZ,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,CZ,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,CZ,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,CZ,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,CZ,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,CZ,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2035: coverage price/load ok (100.00%/100.00%).
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
TEST_DATA_002,Q1,FR,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2018: coverage price/load ok (99.99%/99.79%).
TEST_DATA_002,Q1,FR,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2019: coverage price/load ok (99.99%/99.90%).
TEST_DATA_002,Q1,FR,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2020: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q1,FR,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2021: coverage price/load ok (99.99%/99.89%).
TEST_DATA_002,Q1,FR,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2022: coverage price/load ok (99.99%/99.75%).
TEST_DATA_002,Q1,FR,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2023: coverage price/load ok (99.99%/99.93%).
TEST_DATA_002,Q1,FR,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,FR,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,FR,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2018: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,IT_NORD,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,IT_NORD,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,IT_NORD,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,IT_NORD,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,IT_NORD,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,IT_NORD,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,IT_NORD,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,IT_NORD,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2018: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,NL,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,NL,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,NL,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,NL,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,NL,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,NL,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q1,NL,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q1,NL,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_003,Q1,BE,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,BE,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,CZ,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2035: prix dans plage large attendue.
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
TEST_DATA_003,Q1,FR,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,FR,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,IT_NORD,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2018: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2019: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2020: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2021: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2022: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2023: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2024: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2025: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2026: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2027: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2028: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2029: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2030: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2031: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2032: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2033: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2034: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2035: prix dans plage large attendue.
TEST_DATA_003,Q1,NL,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2035: prix dans plage large attendue.
TEST_Q1_001,Q1,NaN,NaN,DEMAND_UP,WARN,TEST_Q1_001,NaN,NaN,Aucune ligne stage2 observee; test non applicable.
TEST_Q1_001,Q1,NaN,NaN,LOW_RIGIDITY,WARN,TEST_Q1_001,NaN,NaN,Aucune ligne stage2 observee; test non applicable.
TEST_Q1_001,Q1,NaN,NaN,NaN,PASS,TEST_Q1_001,NaN,NaN,Toutes les lignes stage2 ont au moins un signal low-price (h_negative/h_below_5/days_spread_gt50).
UNEXPLAINED_NEGATIVE_PRICES,Q1,BE,2018,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,BE-2018: share_neg_hours_unexplained=100.0% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,BE,2019,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,BE-2019: share_neg_hours_unexplained=73.2% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,BE,2020,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,BE-2020: share_neg_hours_unexplained=38.2% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,CZ,2018,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,CZ-2018: share_neg_hours_unexplained=100.0% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,CZ,2019,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,CZ-2019: share_neg_hours_unexplained=63.8% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,CZ,2020,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,CZ-2020: share_neg_hours_unexplained=71.4% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,CZ,2021,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,CZ-2021: share_neg_hours_unexplained=100.0% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,CZ,2023,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,CZ-2023: share_neg_hours_unexplained=53.7% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,CZ,2024,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,CZ-2024: share_neg_hours_unexplained=79.4% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,DE,2018,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,DE-2018: share_neg_hours_unexplained=66.2% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,DE,2019,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,DE-2019: share_neg_hours_unexplained=55.9% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,DE,2020,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,DE-2020: share_neg_hours_unexplained=63.1% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,DE,2021,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,DE-2021: share_neg_hours_unexplained=59.0% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,FR,2018,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,FR-2018: share_neg_hours_unexplained=72.7% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,FR,2020,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,FR-2020: share_neg_hours_unexplained=48.0% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,NL,2019,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,NL-2019: share_neg_hours_unexplained=100.0% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,NL,2020,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,NL-2020: share_neg_hours_unexplained=100.0% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,NL,2021,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,NL-2021: share_neg_hours_unexplained=100.0% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,NL,2022,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,NL-2022: share_neg_hours_unexplained=100.0% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,NL,2023,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,NL-2023: share_neg_hours_unexplained=100.0% > 35%.
UNEXPLAINED_NEGATIVE_PRICES,Q1,NL,2024,NaN,WARN,UNEXPLAINED_NEGATIVE_PRICES,NaN,NaN,NL-2024: share_neg_hours_unexplained=100.0% > 35%.
BUNDLE_INFORMATIVENESS,Q2,NaN,NaN,NaN,WARN,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=100.00% ; share_compare_informatifs=0.00%
BUNDLE_LEDGER_STATUS,Q2,NaN,NaN,NaN,WARN,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=2"
Q2-H-01,Q2,NaN,NaN,nan,PASS,Pentes OLS post-bascule,14,Q2_country_slopes non vide,Les pentes historiques sont calculees.
Q2-H-02,Q2,NaN,NaN,nan,PASS,Robustesse statistique,"n,p_value,r2","colonnes r2,p_value,n presentes",La robustesse statistique est lisible.
Q2-H-03,Q2,NaN,NaN,nan,PASS,Drivers physiques,4,driver correlations non vides,Les drivers de pente sont disponibles.
Q2-S-01,Q2,NaN,NaN,HIGH_CO2,PASS,Pentes projetees,14,Q2_country_slopes non vide en SCEN,Pentes prospectives calculees.
Q2-S-01,Q2,NaN,NaN,HIGH_GAS,PASS,Pentes projetees,14,Q2_country_slopes non vide en SCEN,Pentes prospectives calculees.
Q2-S-02,Q2,NaN,NaN,HIGH_CO2,WARN,Delta pente vs BASE,finite=14.29%; robust=0.00%; reason_known=100.00%,delta slope par pays/tech vs BASE,Delta de pente partiellement exploitable; beaucoup de valeurs non finies.
Q2-S-02,Q2,NaN,NaN,HIGH_GAS,WARN,Delta pente vs BASE,finite=14.29%; robust=0.00%; reason_known=100.00%,delta slope par pays/tech vs BASE,Delta de pente partiellement exploitable; beaucoup de valeurs non finies.
RC_IR_GT_1,Q2,CZ,2018,NaN,WARN,RC_IR_GT_1,NaN,NaN,"CZ-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=6181.66, p10_load_mw=5946.48."
RC_IR_GT_1,Q2,CZ,2022,NaN,WARN,RC_IR_GT_1,NaN,NaN,"CZ-2022: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=5874.35, p10_load_mw=5645.40."
RC_IR_GT_1,Q2,FR,2018,NaN,WARN,RC_IR_GT_1,NaN,NaN,"FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40."
RC_IR_GT_1,Q2,FR,2019,NaN,WARN,RC_IR_GT_1,NaN,NaN,"FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00."
RC_IR_GT_1,Q2,FR,2021,NaN,WARN,RC_IR_GT_1,NaN,NaN,"FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00."
RC_IR_GT_1,Q2,FR,2024,NaN,WARN,RC_IR_GT_1,NaN,NaN,"FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60."
RC_LOW_REGIME_COHERENCE,Q2,CZ,2018,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,CZ-2018: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q2,CZ,2022,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,CZ-2022: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q2,FR,2018,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,FR-2018: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q2,FR,2021,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,FR-2021: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q2,FR,2023,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,FR-2023: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q2,FR,2024,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,FR-2024: regime_coherence < 0.55.
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2025,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2025,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2026,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2026,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2027,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2027,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2028,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2028,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2029,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2029,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2030,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2030,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2031,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2031,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2032,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2032,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2033,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2033,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2034,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2034,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2035,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,BE,2035,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2018,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2018: must_run_share=79.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2019,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2019: must_run_share=78.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2020,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2020: must_run_share=76.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2021,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2021: must_run_share=76.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2022,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2022: must_run_share=79.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2023,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2023: must_run_share=79.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2024,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2024: must_run_share=78.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2025,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2025,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2026,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2026,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2027,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2027,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2028,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2028,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2029,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2029,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2030,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2030,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2031,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2031,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2032,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2032,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2033,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2033,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2034,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2034,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2035,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,CZ,2035,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2018,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2018: must_run_share=82.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2019,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2019: must_run_share=80.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2020,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2020: must_run_share=77.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2021,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2021: must_run_share=79.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2022,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2022: must_run_share=73.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2023,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2023: must_run_share=75.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,FR,2024,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2024: must_run_share=79.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2018,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2018: must_run_share=0.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2019,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2019: must_run_share=0.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2020,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2020: must_run_share=0.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2021,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2021: must_run_share=0.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2022,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2022: must_run_share=0.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2023,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2023: must_run_share=0.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2024,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2024: must_run_share=0.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2025,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2025,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2026,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2026,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2027,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2027,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2028,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2028,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2029,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2029,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2030,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2030,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2031,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2031,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2032,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2032,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2033,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2033,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2034,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2034,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2035,HIGH_CO2,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q2,NL,2035,HIGH_GAS,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
TEST_DATA_001,Q2,BE,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q2,BE,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2023: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2024: n_hours=8784 coherent.
TEST_DATA_001,Q2,BE,2025,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,BE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2025,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,BE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2026,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,BE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2026,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,BE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2027,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,BE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2027,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,BE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2028,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,BE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,BE,2028,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,BE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,BE,2029,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,BE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2029,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,BE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2030,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,BE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2030,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,BE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2031,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,BE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2031,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,BE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2032,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,BE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,BE,2032,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,BE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,BE,2033,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,BE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2033,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,BE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2034,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,BE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2034,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,BE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2035,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,BE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,BE,2035,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,BE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2018: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2019: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2020: n_hours=8784 coherent.
TEST_DATA_001,Q2,CZ,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2021: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2022: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2023: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2024: n_hours=8784 coherent.
TEST_DATA_001,Q2,CZ,2025,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,CZ-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2025,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,CZ-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2026,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,CZ-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2026,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,CZ-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2027,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,CZ-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2027,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,CZ-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2028,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,CZ-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,CZ,2028,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,CZ-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,CZ,2029,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,CZ-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2029,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,CZ-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2030,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,CZ-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2030,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,CZ-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2031,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,CZ-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2031,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,CZ-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2032,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,CZ-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,CZ,2032,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,CZ-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,CZ,2033,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,CZ-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2033,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,CZ-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2034,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,CZ-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2034,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,CZ-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2035,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,CZ-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,CZ,2035,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,CZ-2035: n_hours=8760 coherent.
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
TEST_DATA_001,Q2,FR,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2018: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2019: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2020: n_hours=8784 coherent.
TEST_DATA_001,Q2,FR,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2021: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2022: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2023: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2024: n_hours=8784 coherent.
TEST_DATA_001,Q2,FR,2025,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,FR-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2025,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,FR-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2026,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,FR-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2026,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,FR-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2027,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,FR-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2027,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,FR-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2028,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,FR-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,FR,2028,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,FR-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,FR,2029,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,FR-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2029,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,FR-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2030,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,FR-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2030,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,FR-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2031,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,FR-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2031,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,FR-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2032,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,FR-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,FR,2032,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,FR-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,FR,2033,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,FR-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2033,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,FR-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2034,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,FR-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2034,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,FR-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2035,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,FR-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,FR,2035,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,FR-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2018: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2019: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2020: n_hours=8784 coherent.
TEST_DATA_001,Q2,IT_NORD,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2021: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2022: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2023: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2024: n_hours=8784 coherent.
TEST_DATA_001,Q2,IT_NORD,2025,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2025,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2026,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2026,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2027,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2027,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2028,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,IT_NORD,2028,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,IT_NORD,2029,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2029,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2030,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2030,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2031,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2031,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2032,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,IT_NORD,2032,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,IT_NORD,2033,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2033,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2034,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2034,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2035,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,IT_NORD,2035,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2018: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2019: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2020: n_hours=8784 coherent.
TEST_DATA_001,Q2,NL,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2021: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2022: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2023: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2024: n_hours=8784 coherent.
TEST_DATA_001,Q2,NL,2025,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,NL-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2025,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,NL-2025: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2026,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,NL-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2026,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,NL-2026: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2027,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,NL-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2027,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,NL-2027: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2028,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,NL-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,NL,2028,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,NL-2028: n_hours=8784 coherent.
TEST_DATA_001,Q2,NL,2029,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,NL-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2029,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,NL-2029: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2030,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,NL-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2030,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,NL-2030: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2031,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,NL-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2031,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,NL-2031: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2032,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,NL-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,NL,2032,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,NL-2032: n_hours=8784 coherent.
TEST_DATA_001,Q2,NL,2033,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,NL-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2033,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,NL-2033: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2034,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,NL-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2034,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,NL-2034: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2035,HIGH_CO2,PASS,TEST_DATA_001,NaN,NaN,NL-2035: n_hours=8760 coherent.
TEST_DATA_001,Q2,NL,2035,HIGH_GAS,PASS,TEST_DATA_001,NaN,NaN,NL-2035: n_hours=8760 coherent.
TEST_DATA_002,Q2,BE,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2018: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,BE,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,BE,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,BE,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,BE,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,BE,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,BE,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,BE,2025,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,BE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2025,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,BE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2026,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,BE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2026,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,BE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2027,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,BE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2027,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,BE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2028,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,BE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2028,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,BE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2029,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,BE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2029,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,BE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2030,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,BE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2030,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,BE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2031,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,BE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2031,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,BE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2032,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,BE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2032,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,BE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2033,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,BE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2033,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,BE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2034,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,BE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2034,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,BE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2035,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,BE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,BE,2035,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,BE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2018: coverage price/load ok (99.99%/99.91%).
TEST_DATA_002,Q2,CZ,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2019: coverage price/load ok (99.99%/99.94%).
TEST_DATA_002,Q2,CZ,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,CZ,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,CZ,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,CZ,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,CZ,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,CZ,2025,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,CZ-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2025,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,CZ-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2026,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,CZ-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2026,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,CZ-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2027,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,CZ-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2027,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,CZ-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2028,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,CZ-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2028,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,CZ-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2029,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,CZ-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2029,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,CZ-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2030,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,CZ-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2030,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,CZ-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2031,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,CZ-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2031,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,CZ-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2032,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,CZ-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2032,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,CZ-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2033,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,CZ-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2033,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,CZ-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2034,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,CZ-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2034,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,CZ-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2035,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,CZ-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,CZ,2035,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,CZ-2035: coverage price/load ok (100.00%/100.00%).
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
TEST_DATA_002,Q2,FR,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2018: coverage price/load ok (99.99%/99.79%).
TEST_DATA_002,Q2,FR,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2019: coverage price/load ok (99.99%/99.90%).
TEST_DATA_002,Q2,FR,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2020: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q2,FR,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2021: coverage price/load ok (99.99%/99.89%).
TEST_DATA_002,Q2,FR,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2022: coverage price/load ok (99.99%/99.75%).
TEST_DATA_002,Q2,FR,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2023: coverage price/load ok (99.99%/99.93%).
TEST_DATA_002,Q2,FR,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,FR,2025,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,FR-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2025,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,FR-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2026,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,FR-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2026,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,FR-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2027,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,FR-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2027,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,FR-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2028,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,FR-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2028,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,FR-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2029,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,FR-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2029,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,FR-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2030,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,FR-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2030,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,FR-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2031,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,FR-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2031,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,FR-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2032,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,FR-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2032,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,FR-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2033,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,FR-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2033,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,FR-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2034,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,FR-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2034,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,FR-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2035,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,FR-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,FR,2035,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,FR-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2018: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,IT_NORD,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,IT_NORD,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,IT_NORD,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,IT_NORD,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,IT_NORD,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,IT_NORD,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,IT_NORD,2025,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2025,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2026,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2026,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2027,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2027,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2028,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2028,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2029,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2029,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2030,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2030,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2031,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2031,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2032,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2032,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2033,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2033,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2034,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2034,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2035,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,IT_NORD,2035,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2018: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,NL,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,NL,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,NL,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,NL,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,NL,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,NL,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q2,NL,2025,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,NL-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2025,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,NL-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2026,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,NL-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2026,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,NL-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2027,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,NL-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2027,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,NL-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2028,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,NL-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2028,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,NL-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2029,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,NL-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2029,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,NL-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2030,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,NL-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2030,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,NL-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2031,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,NL-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2031,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,NL-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2032,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,NL-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2032,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,NL-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2033,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,NL-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2033,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,NL-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2034,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,NL-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2034,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,NL-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2035,HIGH_CO2,PASS,TEST_DATA_002,NaN,NaN,NL-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q2,NL,2035,HIGH_GAS,PASS,TEST_DATA_002,NaN,NaN,NL-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_003,Q2,BE,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2018: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2019: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2020: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2021: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2022: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2023: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2024: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2025,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,BE-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2025,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,BE-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2026,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,BE-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2026,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,BE-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2027,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,BE-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2027,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,BE-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2028,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,BE-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2028,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,BE-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2029,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,BE-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2029,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,BE-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2030,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,BE-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2030,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,BE-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2031,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,BE-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2031,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,BE-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2032,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,BE-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2032,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,BE-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2033,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,BE-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2033,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,BE-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2034,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,BE-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2034,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,BE-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2035,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,BE-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,BE,2035,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,BE-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2018: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2019: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2020: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2021: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2022: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2023: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2024: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2025,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,CZ-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2025,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,CZ-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2026,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,CZ-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2026,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,CZ-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2027,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,CZ-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2027,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,CZ-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2028,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,CZ-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2028,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,CZ-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2029,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,CZ-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2029,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,CZ-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2030,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,CZ-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2030,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,CZ-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2031,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,CZ-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2031,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,CZ-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2032,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,CZ-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2032,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,CZ-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2033,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,CZ-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2033,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,CZ-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2034,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,CZ-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2034,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,CZ-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2035,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,CZ-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,CZ,2035,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,CZ-2035: prix dans plage large attendue.
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
TEST_DATA_003,Q2,FR,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2018: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2019: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2020: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2021: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2022: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2023: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2024: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2025,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,FR-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2025,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,FR-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2026,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,FR-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2026,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,FR-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2027,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,FR-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2027,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,FR-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2028,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,FR-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2028,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,FR-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2029,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,FR-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2029,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,FR-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2030,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,FR-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2030,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,FR-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2031,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,FR-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2031,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,FR-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2032,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,FR-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2032,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,FR-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2033,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,FR-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2033,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,FR-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2034,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,FR-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2034,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,FR-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2035,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,FR-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,FR,2035,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,FR-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2018: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2019: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2020: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2021: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2022: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2023: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2024: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2025,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2025,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2026,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2026,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2027,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2027,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2028,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2028,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2029,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2029,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2030,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2030,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2031,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2031,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2032,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2032,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2033,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2033,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2034,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2034,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2035,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,IT_NORD,2035,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2018: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2019: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2020: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2021: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2022: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2023: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2024: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2025,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,NL-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2025,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,NL-2025: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2026,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,NL-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2026,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,NL-2026: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2027,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,NL-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2027,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,NL-2027: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2028,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,NL-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2028,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,NL-2028: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2029,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,NL-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2029,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,NL-2029: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2030,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,NL-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2030,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,NL-2030: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2031,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,NL-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2031,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,NL-2031: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2032,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,NL-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2032,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,NL-2032: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2033,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,NL-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2033,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,NL-2033: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2034,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,NL-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2034,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,NL-2034: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2035,HIGH_CO2,PASS,TEST_DATA_003,NaN,NaN,NL-2035: prix dans plage large attendue.
TEST_DATA_003,Q2,NL,2035,HIGH_GAS,PASS,TEST_DATA_003,NaN,NaN,NL-2035: prix dans plage large attendue.
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
Q3-H-01,Q3,NaN,NaN,nan,PASS,Tendances glissantes,7,Q3_status non vide,Les tendances historiques sont calculees.
Q3-H-02,Q3,NaN,NaN,nan,PASS,Statuts sortie phase 2,2,status dans ensemble attendu,Les statuts business sont renseignes.
Q3-S-01,Q3,NaN,NaN,DEMAND_UP,PASS,Conditions minimales d'inversion,hors_scope=100.00%; inversion=0,"inversion_k, inversion_r et additional_absorbed presentes",Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites.
Q3-S-01,Q3,NaN,NaN,LOW_RIGIDITY,PASS,Conditions minimales d'inversion,hors_scope=100.00%; inversion=0,"inversion_k, inversion_r et additional_absorbed presentes",Scenario deja de-stresse: conditions minimales d'inversion deja satisfaites.
Q3-S-02,Q3,NaN,NaN,DEMAND_UP,PASS,Validation entree phase 3,hors_scope=100.00%; inversion=0,status non vide en SCEN,Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise.
Q3-S-02,Q3,NaN,NaN,LOW_RIGIDITY,PASS,Validation entree phase 3,hors_scope=100.00%; inversion=0,status non vide en SCEN,Scenario de-stresse: la transition Phase 3 est interpretable comme deja acquise.
RC_IR_GT_1,Q3,CZ,2018,NaN,WARN,RC_IR_GT_1,NaN,NaN,"CZ-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=6181.66, p10_load_mw=5946.48."
RC_IR_GT_1,Q3,CZ,2022,NaN,WARN,RC_IR_GT_1,NaN,NaN,"CZ-2022: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=5874.35, p10_load_mw=5645.40."
RC_IR_GT_1,Q3,FR,2018,NaN,WARN,RC_IR_GT_1,NaN,NaN,"FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40."
RC_IR_GT_1,Q3,FR,2019,NaN,WARN,RC_IR_GT_1,NaN,NaN,"FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00."
RC_IR_GT_1,Q3,FR,2021,NaN,WARN,RC_IR_GT_1,NaN,NaN,"FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00."
RC_IR_GT_1,Q3,FR,2024,NaN,WARN,RC_IR_GT_1,NaN,NaN,"FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60."
RC_LOW_REGIME_COHERENCE,Q3,CZ,2018,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,CZ-2018: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q3,CZ,2022,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,CZ-2022: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q3,FR,2018,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,FR-2018: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q3,FR,2021,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,FR-2021: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q3,FR,2023,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,FR-2023: regime_coherence < 0.55.
RC_LOW_REGIME_COHERENCE,Q3,FR,2024,NaN,WARN,RC_LOW_REGIME_COHERENCE,NaN,NaN,FR-2024: regime_coherence < 0.55.
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2025,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2025,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2025: must_run_share=68.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2026,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2026,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2026: must_run_share=67.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2027,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2027,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2027: must_run_share=67.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2028,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2028,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2028: must_run_share=67.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2029,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2029,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2029: must_run_share=67.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2030,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2030,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2030: must_run_share=67.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2031,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2031,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2031: must_run_share=67.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2032,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2032,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2032: must_run_share=67.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2033,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2033,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2033: must_run_share=67.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2034,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2034,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2034: must_run_share=67.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2035,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,BE,2035,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"BE-2035: must_run_share=66.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2018,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2018: must_run_share=79.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2019,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2019: must_run_share=78.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2020,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2020: must_run_share=76.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2021,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2021: must_run_share=76.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2022,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2022: must_run_share=79.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2023,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2023: must_run_share=79.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2024,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2024: must_run_share=78.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2025,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2025,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2025: must_run_share=62.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2026,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2026,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2026: must_run_share=62.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2027,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2027,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2027: must_run_share=62.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2028,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2028,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2028: must_run_share=62.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2029,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2029,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2029: must_run_share=62.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2030,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2030,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2030: must_run_share=62.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2031,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2031,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2031: must_run_share=62.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2032,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2032,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2032: must_run_share=62.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2033,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2033,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2033: must_run_share=62.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2034,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2034,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2034: must_run_share=62.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2035,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,CZ,2035,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"CZ-2035: must_run_share=62.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2018,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2018: must_run_share=82.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2019,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2019: must_run_share=80.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2020,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2020: must_run_share=77.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2021,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2021: must_run_share=79.4% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2022,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2022: must_run_share=73.5% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2023,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2023: must_run_share=75.9% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,FR,2024,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"FR-2024: must_run_share=79.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2018,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2018: must_run_share=0.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2019,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2019: must_run_share=0.0% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2020,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2020: must_run_share=0.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2021,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2021: must_run_share=0.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2022,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2022: must_run_share=0.1% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2023,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2023: must_run_share=0.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2024,NaN,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2024: must_run_share=0.2% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2025,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2025,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2025: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2026,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2026,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2026: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2027,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2027,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2027: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2028,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2028,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2028: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2029,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2029,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2029: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2030,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2030,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2030: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2031,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2031,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2031: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2032,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2032,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2032: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2033,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2033,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2033: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2034,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2034,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2034: must_run_share=0.6% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2035,DEMAND_UP,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
RC_MR_SHARE_IMPLAUSIBLE,Q3,NL,2035,LOW_RIGIDITY,WARN,RC_MR_SHARE_IMPLAUSIBLE,NaN,NaN,"NL-2035: must_run_share=0.6% hors plage plausible [5%,60%]."
TEST_DATA_001,Q3,BE,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2018: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2019: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2020: n_hours=8784 coherent.
TEST_DATA_001,Q3,BE,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2021: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2022: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2023: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,BE-2024: n_hours=8784 coherent.
TEST_DATA_001,Q3,BE,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,BE,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,BE,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,BE,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,BE,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,BE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,BE,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,BE-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2018: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2019: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2020: n_hours=8784 coherent.
TEST_DATA_001,Q3,CZ,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2021: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2022: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2023: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,CZ-2024: n_hours=8784 coherent.
TEST_DATA_001,Q3,CZ,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,CZ,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,CZ,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,CZ,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,CZ,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,CZ-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,CZ,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,CZ-2035: n_hours=8760 coherent.
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
TEST_DATA_001,Q3,FR,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2018: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2019: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2020: n_hours=8784 coherent.
TEST_DATA_001,Q3,FR,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2021: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2022: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2023: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,FR-2024: n_hours=8784 coherent.
TEST_DATA_001,Q3,FR,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,FR,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,FR,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,FR,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,FR,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,FR-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,FR,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,FR-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2018: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2019: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2020: n_hours=8784 coherent.
TEST_DATA_001,Q3,IT_NORD,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2021: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2022: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2023: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2024: n_hours=8784 coherent.
TEST_DATA_001,Q3,IT_NORD,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,IT_NORD,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,IT_NORD,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,IT_NORD,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,IT_NORD,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,IT_NORD,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,IT_NORD-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2018,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2018: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2019,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2019: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2020,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2020: n_hours=8784 coherent.
TEST_DATA_001,Q3,NL,2021,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2021: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2022,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2022: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2023,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2023: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2024,NaN,PASS,TEST_DATA_001,NaN,NaN,NL-2024: n_hours=8784 coherent.
TEST_DATA_001,Q3,NL,2025,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2025,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2025: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2026,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2026,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2026: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2027,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2027,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2027: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2028,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,NL,2028,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2028: n_hours=8784 coherent.
TEST_DATA_001,Q3,NL,2029,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2029,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2029: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2030,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2030,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2030: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2031,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2031,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2031: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2032,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,NL,2032,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2032: n_hours=8784 coherent.
TEST_DATA_001,Q3,NL,2033,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2033,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2033: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2034,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2034,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2034: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2035,DEMAND_UP,PASS,TEST_DATA_001,NaN,NaN,NL-2035: n_hours=8760 coherent.
TEST_DATA_001,Q3,NL,2035,LOW_RIGIDITY,PASS,TEST_DATA_001,NaN,NaN,NL-2035: n_hours=8760 coherent.
TEST_DATA_002,Q3,BE,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2018: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,BE,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,BE,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,BE,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,BE,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,BE,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,BE,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,BE-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,BE,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,BE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,BE,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,BE-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2018: coverage price/load ok (99.99%/99.91%).
TEST_DATA_002,Q3,CZ,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2019: coverage price/load ok (99.99%/99.94%).
TEST_DATA_002,Q3,CZ,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,CZ,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,CZ,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,CZ,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,CZ,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,CZ-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,CZ,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,CZ-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,CZ,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,CZ-2035: coverage price/load ok (100.00%/100.00%).
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
TEST_DATA_002,Q3,FR,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2018: coverage price/load ok (99.99%/99.79%).
TEST_DATA_002,Q3,FR,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2019: coverage price/load ok (99.99%/99.90%).
TEST_DATA_002,Q3,FR,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2020: coverage price/load ok (99.99%/99.97%).
TEST_DATA_002,Q3,FR,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2021: coverage price/load ok (99.99%/99.89%).
TEST_DATA_002,Q3,FR,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2022: coverage price/load ok (99.99%/99.75%).
TEST_DATA_002,Q3,FR,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2023: coverage price/load ok (99.99%/99.93%).
TEST_DATA_002,Q3,FR,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,FR-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,FR,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,FR-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,FR,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,FR-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2018: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,IT_NORD,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,IT_NORD,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,IT_NORD,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,IT_NORD,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,IT_NORD,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,IT_NORD,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,IT_NORD,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,IT_NORD,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,IT_NORD-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2018,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2018: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,NL,2019,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2019: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,NL,2020,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2020: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,NL,2021,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2021: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,NL,2022,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2022: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,NL,2023,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2023: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,NL,2024,NaN,PASS,TEST_DATA_002,NaN,NaN,NL-2024: coverage price/load ok (99.99%/99.99%).
TEST_DATA_002,Q3,NL,2025,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2025,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2025: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2026,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2026,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2026: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2027,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2027,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2027: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2028,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2028,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2028: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2029,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2029,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2029: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2030,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2030,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2030: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2031,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2031,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2031: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2032,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2032,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2032: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2033,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2033,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2033: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2034,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2034,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2034: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2035,DEMAND_UP,PASS,TEST_DATA_002,NaN,NaN,NL-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_002,Q3,NL,2035,LOW_RIGIDITY,PASS,TEST_DATA_002,NaN,NaN,NL-2035: coverage price/load ok (100.00%/100.00%).
TEST_DATA_003,Q3,BE,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2018: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2019: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2020: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2021: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2022: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2023: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,BE-2024: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,BE-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,BE,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,BE-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2018: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2019: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2020: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2021: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2022: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2023: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,CZ-2024: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,CZ-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,CZ,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,CZ-2035: prix dans plage large attendue.
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
TEST_DATA_003,Q3,FR,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2018: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2019: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2020: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2021: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2022: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2023: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,FR-2024: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,FR-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,FR,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,FR-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2018: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2019: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2020: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2021: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2022: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2023: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2024: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,IT_NORD,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,IT_NORD-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2018,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2018: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2019,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2019: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2020,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2020: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2021,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2021: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2022,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2022: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2023,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2023: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2024,NaN,PASS,TEST_DATA_003,NaN,NaN,NL-2024: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2025,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2025,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2025: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2026,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2026,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2026: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2027,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2027,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2027: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2028,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2028,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2028: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2029,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2029,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2029: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2030,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2030,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2030: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2031,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2031,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2031: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2032,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2032,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2032: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2033,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2033,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2033: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2034,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2034,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2034: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2035,DEMAND_UP,PASS,TEST_DATA_003,NaN,NaN,NL-2035: prix dans plage large attendue.
TEST_DATA_003,Q3,NL,2035,LOW_RIGIDITY,PASS,TEST_DATA_003,NaN,NaN,NL-2035: prix dans plage large attendue.
TEST_Q3_001,Q3,NaN,NaN,DEMAND_UP,PASS,TEST_Q3_001,NaN,NaN,Toutes les lignes within_bounds=true respectent target_sr et target_h_negative.
TEST_Q3_001,Q3,NaN,NaN,LOW_RIGIDITY,PASS,TEST_Q3_001,NaN,NaN,Toutes les lignes within_bounds=true respectent target_sr et target_h_negative.
TEST_Q3_001,Q3,NaN,NaN,NaN,PASS,TEST_Q3_001,NaN,NaN,Toutes les lignes within_bounds=true respectent target_sr et target_h_negative.
BUNDLE_INFORMATIVENESS,Q4,NaN,NaN,NaN,PASS,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=100.00% ; share_compare_informatifs=75.00%
BUNDLE_LEDGER_STATUS,Q4,NaN,NaN,NaN,PASS,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=0"
Q4-H-01,Q4,NaN,NaN,nan,PASS,Simulation BESS 3 modes,"HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED",3 modes executes avec sorties non vides,Les trois modes Q4 sont disponibles.
Q4-H-02,Q4,NaN,NaN,nan,PASS,Invariants physiques BESS,WARN,aucun FAIL physique/structurel pertinent,Les invariants physiques batterie sont respectes. Des avertissements non-physiques peuvent subsister (objectif/scenario).
Q4-S-01,Q4,NaN,NaN,HIGH_CO2,PASS,Comparaison effet batteries par scenario,7,Q4 summary non vide pour >=1 scenario,Resultats Q4 prospectifs disponibles.
Q4-S-01,Q4,NaN,NaN,HIGH_GAS,PASS,Comparaison effet batteries par scenario,7,Q4 summary non vide pour >=1 scenario,Resultats Q4 prospectifs disponibles.
Q4-S-02,Q4,NaN,NaN,HIGH_CO2,PASS,Sensibilite valeur commodites,share_finite=100.00%,delta pv_capture ou revenus vs BASE,Sensibilite valeur exploitable sur le panel.
Q4-S-02,Q4,NaN,NaN,HIGH_GAS,PASS,Sensibilite valeur commodites,share_finite=100.00%,delta pv_capture ou revenus vs BASE,Sensibilite valeur exploitable sur le panel.
Q4_BESS_INEFFECTIVE,Q4,NaN,NaN,HIGH_CO2,WARN,Q4_BESS_INEFFECTIVE,NaN,NaN,h_negative>0 mais aucun point de frontier ne reduit h_negative.
Q4_BESS_INEFFECTIVE,Q4,NaN,NaN,HIGH_GAS,WARN,Q4_BESS_INEFFECTIVE,NaN,NaN,h_negative>0 mais aucun point de frontier ne reduit h_negative.
Q4_BESS_INEFFECTIVE,Q4,NaN,NaN,NaN,WARN,Q4_BESS_INEFFECTIVE,NaN,NaN,h_negative>0 mais aucun point de frontier ne reduit h_negative.
Q4_BESS_INEFFECTIVE,Q4,NaN,NaN,NaN,WARN,Q4_BESS_INEFFECTIVE,NaN,NaN,h_negative>0 mais aucun point de frontier ne reduit h_negative.
Q4_BESS_INEFFECTIVE,Q4,NaN,NaN,NaN,WARN,Q4_BESS_INEFFECTIVE,NaN,NaN,h_negative>0 mais aucun point de frontier ne reduit h_negative.
Q4_BESS_INEFFECTIVE,Q4,NaN,NaN,NaN,WARN,Q4_BESS_INEFFECTIVE,NaN,NaN,h_negative>0 mais aucun point de frontier ne reduit h_negative.
Q4_BESS_INEFFECTIVE,Q4,NaN,NaN,NaN,WARN,Q4_BESS_INEFFECTIVE,NaN,NaN,h_negative>0 mais aucun point de frontier ne reduit h_negative.
Q4_BESS_INEFFECTIVE,Q4,NaN,NaN,NaN,WARN,Q4_BESS_INEFFECTIVE,NaN,NaN,h_negative>0 mais aucun point de frontier ne reduit h_negative.
TEST_Q4_001,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,NaN,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,NaN,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,NaN,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,NaN,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,NaN,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,NaN,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_001,Q4,NaN,NaN,NaN,PASS,TEST_Q4_001,NaN,NaN,"Invariants physiques batterie (SOC, puissance, energie) valides."
TEST_Q4_002,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_CO2,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,HIGH_GAS,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,NaN,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,NaN,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,NaN,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,NaN,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,NaN,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,NaN,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
TEST_Q4_002,Q4,NaN,NaN,NaN,PASS,TEST_Q4_002,NaN,NaN,Monotonicite respectee (augmentation bess_power/energy ne degrade pas le surplus).
BUNDLE_INFORMATIVENESS,Q5,NaN,NaN,NaN,PASS,BUNDLE_INFORMATIVENESS,NaN,NaN,share_tests_informatifs=100.00% ; share_compare_informatifs=100.00%
BUNDLE_LEDGER_STATUS,Q5,NaN,NaN,NaN,PASS,BUNDLE_LEDGER_STATUS,NaN,NaN,"ledger: FAIL=0, WARN=0"
Q5-H-01,Q5,NaN,NaN,nan,PASS,Ancre thermique historique,share_fini=100.00%,Q5_summary non vide avec ttl_obs et tca_q95,L'ancre thermique est quantifiable sur la majorite des pays.
Q5-H-02,Q5,NaN,NaN,nan,PASS,Sensibilites analytiques,share_positive=100.00%,dTCA_dCO2 > 0 et dTCA_dGas > 0,Sensibilites analytiques globalement coherentes.
Q5-S-01,Q5,NaN,NaN,HIGH_BOTH,PASS,Sensibilites scenarisees,7,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-01,Q5,NaN,NaN,HIGH_CO2,PASS,Sensibilites scenarisees,7,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-01,Q5,NaN,NaN,HIGH_GAS,PASS,Sensibilites scenarisees,7,Q5_summary non vide sur scenarios selectionnes,Sensibilites scenario calculees.
Q5-S-02,Q5,NaN,NaN,HIGH_BOTH,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5-S-02,Q5,NaN,NaN,HIGH_CO2,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5-S-02,Q5,NaN,NaN,HIGH_GAS,PASS,CO2 requis pour TTL cible,share_finite=100.00%,co2_required_* non NaN,CO2 requis interpretable sur le panel.
Q5_ALPHA_NEGATIVE,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,NaN,NaN,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,NaN,NaN,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,NaN,NaN,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,NaN,NaN,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,NaN,NaN,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_ALPHA_NEGATIVE,NaN,NaN,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_ALPHA_NEGATIVE,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_ALPHA_NEGATIVE,NaN,NaN,Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=36.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=71.7 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=62.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=45.3 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=21.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=42.5 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=50.9 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=10.9 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=25.2 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=40.5 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=33.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=33.8 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=15.5 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=28.0 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=10.9 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=20.8 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=41.2 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=34.1 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=22.9 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=16.6 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=29.0 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,NaN,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=13.6 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,NaN,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=26.8 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,NaN,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=8.0 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,NaN,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=21.5 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,NaN,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=36.4 EUR/MWh (acceptable).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,NaN,WARN,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=39.2 EUR/MWh (a revoir).
Q5_DISTRIBUTIONAL_FIT,Q5,NaN,NaN,NaN,INFO,Q5_DISTRIBUTIONAL_FIT,NaN,NaN,Erreur distributionnelle p90/p95=20.5 EUR/MWh (acceptable).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_LOW_CORR_CD,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_LOW_CORR_CD,NaN,NaN,Corr horaire faible mais non bloquante (fit distributionnel prioritaire).
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_BOTH,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_CO2,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
Q5_TARGET_ALREADY_MET,Q5,NaN,NaN,HIGH_GAS,INFO,Q5_TARGET_ALREADY_MET,NaN,NaN,ttl_target <= ttl_anchor_formula: deltas requis fixes a 0.
TEST_Q5_001,Q5,NaN,NaN,NaN,WARN,TEST_Q5_001,NaN,NaN,Comparaison BASE/HIGH_CO2/HIGH_GAS indisponible (table Q5_summary manquante).
TEST_Q5_002,Q5,NaN,NaN,NaN,WARN,TEST_Q5_002,NaN,NaN,Impossible d'evaluer la coherence delta_ttl_vs_base vs delta_tca_vs_base (donnees manquantes).
```
