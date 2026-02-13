# Synthese resultats Q1-Q5 - ES - FULL_20260212_FIX13_DE_ES_CLEAN

- Generated_at: `2026-02-13 00:00:05 UTC`
- Source run: `outputs/combined/FULL_20260212_FIX13_DE_ES_CLEAN` (run unique, no reuse of previous run outputs)
- Scope: historique 2018-2024, scenarios 2025-2035

## Garde-fous globaux
- Q1 consolidated checks: PASS=176, WARN=4, FAIL=0, NON_TESTABLE=2
- Q2 consolidated checks: PASS=186, WARN=3, FAIL=0, NON_TESTABLE=0
- Q3 consolidated checks: PASS=246, WARN=1, FAIL=0, NON_TESTABLE=0
- Q4 consolidated checks: PASS=20, WARN=5, FAIL=0, NON_TESTABLE=0
- Q5 consolidated checks: PASS=9, WARN=0, FAIL=0, NON_TESTABLE=0
- non_negative fields < 0 (ES): `0`
- Q1 stage2 without low-price evidence (ES): `0`

## Q1
- Test ledger: PASS=10, WARN=1, FAIL=0, NON_TESTABLE=2
- Consolidated checks: PASS=176, WARN=4, FAIL=0, NON_TESTABLE=2
- Consolidated non-PASS (filtered):
status,code,scope,scenario_id,message
WARN,BUNDLE_LEDGER_STATUS,BUNDLE,,"ledger: FAIL=0, WARN=1"
WARN,BUNDLE_INFORMATIVENESS,BUNDLE,,share_tests_informatifs=84.62% ; share_compare_informatifs=0.00%
WARN,Q1_S02_NO_SENSITIVITY,BUNDLE,,Q1-S-02: aucune sensibilite scenario non-BASE clairement observable vs BASE.

### Comparaison historique vs prospectif
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
ES,BASE,bascule_year_market,2023,2023,0,,FRAGILE,delta_quasi_nul_vs_historique
ES,DEMAND_UP,bascule_year_market,2023,,,,NON_TESTABLE,delta_non_interpretable_nan
ES,LOW_RIGIDITY,bascule_year_market,2023,,,,NON_TESTABLE,delta_non_interpretable_nan

### Q1 country summary (hist)
country,bascule_year_market,bascule_year_market_country,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_year_market_observed,bascule_year_physical_observed,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_status_physical,stage1_bascule_year,stage1_detected,bascule_confidence,families_active_at_bascule_pv,families_active_at_bascule_wind,families_active_at_bascule_country,drivers_at_bascule,quality_flag_unexplained_neg_prices,quality_flags,low_price_flags_count_at_bascule,physical_flags_count_at_bascule,capture_flags_count_at_bascule,stage2_market_score_at_bascule,score_breakdown_at_bascule,required_demand_uplift_to_avoid_phase2,required_demand_uplift_status,required_flex_uplift_to_avoid_phase2,required_flex_uplift_status,bascule_rationale,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,capture_ratio_pv_at_bascule,capture_ratio_wind_at_bascule,market_physical_gap_at_bascule,neg_price_explained_by_surplus_ratio_at_bascule,neg_price_unexplained_share_at_bascule,h_negative_at_bascule,notes_quality,end_year,low_price_flags_count_at_end_year,physical_flags_count_at_end_year,capture_flags_count_at_end_year,stage2_market_score_at_end_year,score_breakdown_at_end_year,sr_energy_at_end_year,far_energy_at_end_year,ir_p10_at_end_year,ttl_at_end_year,capture_ratio_pv_vs_ttl_at_end_year,capture_ratio_pv_at_end_year,capture_ratio_wind_at_end_year,market_physical_gap_at_end_year,h_negative_at_end_year,neg_price_explained_by_surplus_ratio_at_end_year,neg_price_unexplained_share_at_end_year
ES,2023,2023,2023,2023,2021,2023,2021,transition_observed,transition_observed,transition_observed,transition_observed,2018,True,1,"LOW_PRICE,PHYSICAL","LOW_PRICE,PHYSICAL,VALUE_WIND","LOW_PRICE,PHYSICAL,VALUE_WIND",LOW_PRICE:h_below_5_obs>=500.0 (526.0); LOW_PRICE:low_price_hours_share>=0.057 (0.060); VALUE:capture_ratio_wind<=0.90 (0.876); PHYSICAL:sr_energy>=0.010 (0.042); PHYSICAL:sr_hours>=0.10 (0.263); PHYSICAL:far_observed<0.95 (0.921),False,,2,2,1,3,low=1;value=1;physical=1;crisis=0,0.052002,ok,0.0650024,ok,Bascule validee: >=2 familles actives (LOW_PRICE/VALUE/PHYSICAL) sur 2 annees consecutives hors crise.,0.0422222,0.921042,0.450752,151.61,0.48202,0.838895,0.876094,False,,,0,ok,2024,3,2,2,3,low=1;value=1;physical=1;crisis=0,0.0421614,0.945508,0.395026,141.5,0.302482,0.678957,0.882136,False,247,0.951417,0.00809717


## Q2
- Test ledger: PASS=9, WARN=0, FAIL=0, NON_TESTABLE=0
- Consolidated checks: PASS=186, WARN=3, FAIL=0, NON_TESTABLE=0
- Consolidated non-PASS (filtered):
status,code,scope,scenario_id,message
WARN,Q2_POSITIVE_ROBUST_SLOPE,SCEN,HIGH_CO2,ES-PV: pente robuste positive (exception possible meteo/structure).
WARN,Q2_POSITIVE_ROBUST_SLOPE,SCEN,HIGH_GAS,ES-PV: pente robuste positive (exception possible meteo/structure).

### Comparaison historique vs prospectif
country,tech,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
ES,PV,BASE,slope,-5.5781,-5.5781,0,,FRAGILE,delta_quasi_nul_vs_historique
ES,WIND,BASE,slope,-0.483584,-0.483584,0,,FRAGILE,delta_quasi_nul_vs_historique
ES,PV,HIGH_CO2,slope,-5.5781,0.679427,6.25753,,INFORMATIVE,delta_interpretable
ES,WIND,HIGH_CO2,slope,-0.483584,-0.103369,0.380216,,INFORMATIVE,delta_interpretable
ES,PV,HIGH_GAS,slope,-5.5781,0.643476,6.22157,,INFORMATIVE,delta_interpretable
ES,WIND,HIGH_GAS,slope,-0.483584,-0.101184,0.3824,,INFORMATIVE,delta_interpretable

### Q2 slopes (hist)
scenario_id,country,tech,phase2_start_year_for_slope,phase2_start_reason,phase2_end_year,years_used,n_points,x_axis_used,x_axis_default,x_unit,slope,slope_per_1pp,slope_unit,intercept,r2,p_value,loo_slope_rel_var_max,n,slope_method,method,insufficient_points,slope_status,robust_flag,reason_code,outlier_years_count,slope_all_years,slope_excluding_outliers,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2,penetration_share_generation_mean_phase2,penetration_share_load_mean_phase2,slope_quality_flag,slope_quality_notes,corr_vre_load_phase2,cross_country_benchmark_slope,cross_country_benchmark_r2,cross_country_benchmark_p_value,cross_country_benchmark_n,cross_country_benchmark_reason
HIST,ES,PV,2023,q1_bascule_pv,2024,"2023,2024",2,pv_penetration_share_generation,pv_penetration_share_generation,share_of_generation,-5.5781,-0.055781,capture_ratio_per_share_generation,1.86027,,,,2,endpoint_delta,endpoint_delta,True,FRAGILE,FRAGILE,insufficient_points,0,-5.5781,-5.5781,0.0421918,0.933275,0.422889,146.555,,,0.19744,0.19744,WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE,1,-4.87776,0.829624,0.0115707,7,ok
HIST,ES,WIND,2023,q1_bascule_wind,2024,"2023,2024",2,wind_penetration_share_generation,wind_penetration_share_generation,share_of_generation,-0.483584,-0.00483584,capture_ratio_per_share_generation,1.00982,,,,2,endpoint_delta,endpoint_delta,True,FRAGILE,FRAGILE,insufficient_points,0,-0.483584,-0.483584,0.0421918,0.933275,0.422889,146.555,,,0.270278,0.270278,WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE,1,-0.303283,0.418155,0.165226,7,ok


## Q3
- Test ledger: PASS=5, WARN=3, FAIL=0, NON_TESTABLE=0
- Consolidated checks: PASS=246, WARN=1, FAIL=0, NON_TESTABLE=0
- Consolidated non-PASS (filtered):
status,code,scope,scenario_id,message
WARN,BUNDLE_LEDGER_STATUS,BUNDLE,,"ledger: FAIL=0, WARN=3"

### Comparaison historique vs prospectif
country,scenario_id,metric,hist_value,scen_value,delta,hist_status,scen_status,interpretability_status,interpretability_reason
ES,BASE,inversion_k_demand,,,,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,NON_TESTABLE,scenario_hors_scope_phase2
ES,BASE,inversion_r_mustrun,,,,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,NON_TESTABLE,scenario_hors_scope_phase2
ES,DEMAND_UP,inversion_k_demand,,,,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,NON_TESTABLE,scenario_hors_scope_phase2
ES,DEMAND_UP,inversion_r_mustrun,,,,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,NON_TESTABLE,scenario_hors_scope_phase2
ES,LOW_RIGIDITY,inversion_k_demand,,,,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,NON_TESTABLE,scenario_hors_scope_phase2
ES,LOW_RIGIDITY,inversion_r_mustrun,,,,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,NON_TESTABLE,scenario_hors_scope_phase2

### Q3 inversion requirements (hist)
country,scenario_id,year,lever,required_uplift,required_uplift_mw,required_uplift_pct_avg_load,required_uplift_twh_per_year,within_bounds,target_sr,target_h_negative,target_h_below_5,predicted_sr_after,predicted_far_after,predicted_h_negative_after,predicted_h_below_5_after,predicted_h_negative_metric,h_negative_obs_before,h_below_5_obs_before,h_negative_est_before,h_below_5_est_before,applicability_flag,status,reason,export_coincidence_factor,proxy_quality_status,proxy_quality_reasons,output_schema_version
ES,HIST,2024,demand_uplift,,,,,False,0.01,200,500,,,,,MARKET_PROXY_BUCKET_MODEL_EST,,,,,HORS_SCOPE_PHASE2,hors_scope_phase2,no_stage2_detected,,,,
ES,HIST,2024,export_uplift,,,,,False,0.01,200,500,,,,,MARKET_PROXY_BUCKET_MODEL_EST,,,,,HORS_SCOPE_PHASE2,hors_scope_phase2,no_stage2_detected,,,,
ES,HIST,2024,flex_uplift,,,,,False,0.01,200,500,,,,,MARKET_PROXY_BUCKET_MODEL_EST,,,,,HORS_SCOPE_PHASE2,hors_scope_phase2,no_stage2_detected,,,,


## Q4
- Test ledger: PASS=8, WARN=0, FAIL=0, NON_TESTABLE=0
- Consolidated checks: PASS=20, WARN=5, FAIL=0, NON_TESTABLE=0
- Consolidated non-PASS (filtered):
status,code,scope,scenario_id,message
WARN,Q4_SURPLUS_NON_MONOTONIC_DOMINANCE,HIST,,"Surplus non absorbe non monotone en dominance (P,E)."
WARN,Q4_FAR_NON_MONOTONIC_DOMINANCE,HIST,,"FAR non monotone en dominance (P,E)."
WARN,Q4_SURPLUS_NON_MONOTONIC_DOMINANCE,HIST,,"Surplus non absorbe non monotone en dominance (P,E)."
WARN,Q4_FAR_NON_MONOTONIC_DOMINANCE,HIST,,"FAR non monotone en dominance (P,E)."
WARN,Q4_OBJECTIVE_NOT_REACHED_GRID,HIST,,Objectif non atteint sur la grille courante; augmenter les bornes de recherche.

### Comparaison historique vs prospectif
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
ES,BASE,far_after,1,1,0,,FRAGILE,delta_quasi_nul_vs_historique
ES,BASE,surplus_unabs_energy_after,0,0,0,,FRAGILE,delta_quasi_nul_vs_historique
ES,BASE,pv_capture_price_after,54.8253,97.4638,42.6385,,INFORMATIVE,delta_interpretable
ES,BASE,far_before,0.945508,1,0.0544923,,INFORMATIVE,delta_interpretable
ES,BASE,surplus_unabs_energy_before,0.556385,0,-0.556385,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,far_after,1,1,0,,FRAGILE,delta_quasi_nul_vs_historique
ES,HIGH_CO2,surplus_unabs_energy_after,0,0,0,,FRAGILE,delta_quasi_nul_vs_historique
ES,HIGH_CO2,pv_capture_price_after,54.8253,102.092,47.2672,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,far_before,0.945508,1,0.0544923,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,surplus_unabs_energy_before,0.556385,0,-0.556385,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,far_after,1,1,0,,FRAGILE,delta_quasi_nul_vs_historique
ES,HIGH_GAS,surplus_unabs_energy_after,0,0,0,,FRAGILE,delta_quasi_nul_vs_historique
ES,HIGH_GAS,pv_capture_price_after,54.8253,107.775,52.9499,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,far_before,0.945508,1,0.0544923,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,surplus_unabs_energy_before,0.556385,0,-0.556385,,INFORMATIVE,delta_interpretable
ES,HIST_PRICE_ARBITRAGE_SIMPLE,far_after,1,0.962424,-0.0375758,,INFORMATIVE,delta_interpretable
ES,HIST_PV_COLOCATED,far_after,1,0.946089,-0.053911,,INFORMATIVE,delta_interpretable

### Q4 sizing summary (hist)
scenario_id,country,year,dispatch_mode,objective,bess_power_mw_test,bess_energy_mwh_test,bess_duration_h_test,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_obs_before,h_negative_est_before,h_negative_est_after,h_negative_before,h_negative_after,h_negative_proxy_before,h_negative_proxy_after,h_negative_proxy_raw_after,h_negative_reducible_upper_bound,h_negative_upper_bound_after,h_below_5_reducible_upper_bound,h_below_5_obs_before,h_below_5_est_before,h_below_5_est_after,h_below_5_before,h_below_5_after,h_below_5_proxy_before,h_below_5_proxy_after,h_below_5_proxy_raw_after,delta_h_negative_est,delta_h_below_5_est,delta_h_negative,delta_h_below_5,h_negative_after_source,h_below_5_after_source,baseload_price_obs_before,baseload_price_est_before,baseload_price_est_after,baseload_price_before,baseload_price_after,capture_ratio_pv_obs_before,capture_ratio_pv_est_before,capture_ratio_pv_est_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_obs_before,capture_ratio_wind_est_before,capture_ratio_wind_est_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_est_pv,delta_capture_ratio_est_wind,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_obs_before,pv_capture_price_est_before,pv_capture_price_est_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_obs_before,wind_capture_price_est_before,wind_capture_price_est_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,charge_hours,discharge_hours,cycles_assumed_per_day,cycles_realized_per_day,simultaneous_charge_discharge_hours,energy_balance_residual,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,charge_vs_surplus_violation_hours,no_dispatch,proxy_quality_status,proxy_quality_reasons,output_schema_version,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh,on_efficient_frontier,objective_met,objective_reason,objective_not_reached,status,reason,objective_target_value,objective_direction,objective_value_after,objective_recommendation,pv_capacity_proxy_mw,power_grid_max_mw,duration_grid_max_h,grid_expansions_used,notes_quality
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,38128,305024,8,38128,305024,8,0.945508,1,False,False,247,247,154.861,247,154.861,247,154.861,154.861,247,0,1642,1642,1642,1545.27,1642,1545.27,1642,1545.27,1545.27,-92.1386,-96.731,-92.1386,-96.731,est_proxy,est_proxy,63.0395,63.0461,61.6951,63.0395,61.6951,0.678957,0.678888,0.888649,0.678888,0.888649,0.882136,0.882071,0.853951,0.882071,0.853951,0.20976,-0.0281198,0.20976,-0.0281198,0.556385,0,42.8012,42.8013,54.8253,42.8013,54.8253,55.6095,55.6111,52.6847,55.6111,52.6847,272,272,71.5241,71.463,0.073429,0.473019,0.269581,0,0.39501,0.407742,False,False,True,False,True,,0,257898,0,0,0,12416,18308,1.02103e+07,8.9851e+06,2368,1523,1,0.0914587,0,-1.86265e-09,0.88,0.938083,0.938083,ZERO_END,0,False,PASS,,2.0.0,v2.2.2,14.8218,False,38128,8,305024,True,True,grid_too_small,False,ok,grid_too_small,200,lower_is_better,154.861,expand_grid_to_power_mw>=57192.0;duration_h>=36.0,20284,38128,24,1,ok


## Q5
- Test ledger: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0
- Consolidated checks: PASS=9, WARN=0, FAIL=0, NON_TESTABLE=0
- Consolidated non-PASS (filtered):
status,code,scope,scenario_id,message
INFO,Q5_DISTRIBUTIONAL_FIT,HIST,,Erreur distributionnelle p90/p95=8.6 EUR/MWh (acceptable).
INFO,Q5_DISTRIBUTIONAL_FIT,HIST,,Erreur distributionnelle p90/p95=23.7 EUR/MWh (acceptable).

### Comparaison historique vs prospectif
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
ES,BASE,ttl_obs,141.5,164.717,23.217,,INFORMATIVE,delta_interpretable
ES,BASE,tca_q95,113.15,121.545,8.39585,,INFORMATIVE,delta_interpretable
ES,BASE,co2_required_base_non_negative,194.703,204.703,10,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,ttl_obs,141.5,171.144,29.6443,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,tca_q95,113.15,139.909,26.7595,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,co2_required_base_non_negative,194.703,204.703,10,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,ttl_obs,141.5,179.035,37.5352,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,tca_q95,113.15,162.455,49.3049,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,co2_required_base_non_negative,194.703,100,-94.703,,INFORMATIVE,delta_interpretable
ES,HIGH_BOTH,ttl_obs,141.5,164.717,23.217,,INFORMATIVE,delta_interpretable
ES,HIGH_BOTH,tca_q95,113.15,180.818,67.6686,,INFORMATIVE,delta_interpretable
ES,HIGH_BOTH,co2_required_base_non_negative,194.703,150,-44.703,,INFORMATIVE,delta_interpretable

### Q5 summary (hist)
scenario_id,country,year_range_used,ttl_reference_mode,ttl_reference_year,marginal_tech,chosen_anchor_tech,fuel_used,assumed_co2_price_eur_t,assumed_gas_price_eur_mwh_th,assumed_coal_price_eur_mwh_th,assumed_efficiency,assumed_emission_factor_t_per_mwh_th,assumed_vom_eur_mwh,assumed_fuel_multiplier_vs_gas,ttl_obs,ttl_observed_eur_mwh,ttl_obs_price_cd,ttl_annual_metrics_same_year,ttl_anchor,ttl_anchor_formula,ttl_model_eur_mwh,ttl_physical,ttl_regression,ttl_method,tca_q95,alpha,alpha_effective,corr_cd,anchor_confidence,anchor_distribution_error_p90_p95,anchor_error_p90,anchor_error_p95,anchor_status,dTCA_dCO2,dTCA_dFuel,dTCA_dGas,eta_implicit_from_dTCA_dFuel,ef_implicit_t_per_mwh_e,ttl_target,anchor_gap_to_target,required_co2_eur_t,required_gas_eur_mwh_th,required_co2_abs_eur_t,required_gas_abs_eur_mwh_th,delta_co2_vs_scenario,delta_gas_vs_scenario,tca_ccgt_eur_mwh,tca_coal_eur_mwh,tca_current_eur_mwh,pass_through_factor,base_scenario_id,base_year_reference,base_ref_source_year,base_ref_status,base_ref_reason,base_tca_ref_eur_mwh,base_ttl_model_ref_eur_mwh,base_gas_eur_per_mwh_th,base_co2_eur_per_t,ttl_proxy_method,status,reason,delta_tca_vs_base,delta_ttl_model_vs_base,delta_capture_ratio_vs_base,coherence_flag,required_co2_abs_raw_eur_t,required_gas_abs_raw_eur_mwh_th,co2_required_base,co2_required_gas_override,co2_required_base_raw,gas_required_base_raw,co2_required_base_non_negative,gas_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality,output_schema_version
HIST,ES,2018-2024,year_specific,2024,CCGT,CCGT,gas,70.68,47.02,,0.55,0.202,3,1,141.5,141.5,141.5,141.5,113.15,114.45,141.5,113.15,,anchor_distributional,113.15,28.3504,28.3504,0.65024,0.703278,23.7378,19.1251,28.3504,target_above_anchor,0.367273,1.81818,1.81818,0.55,0.367273,160,45.5503,194.703,72.0726,194.703,72.0726,124.023,25.0526,114.45,135.481,114.45,1,BASE,2024,2024,ok,,114.45,141.5,47.02,70.68,observed_from_prices,ok,,0,0,0,PASS,194.703,72.0726,194.703,,194.703,72.0726,194.703,72.0726,,,2.0.0
