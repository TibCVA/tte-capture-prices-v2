# Synthese resultats Q1-Q5 - DE - FULL_20260212_FIX13_DE_ES_CLEAN

- Generated_at: `2026-02-13 00:00:04 UTC`
- Source run: `outputs/combined/FULL_20260212_FIX13_DE_ES_CLEAN` (run unique, no reuse of previous run outputs)
- Scope: historique 2018-2024, scenarios 2025-2035

## Garde-fous globaux
- Q1 consolidated checks: PASS=176, WARN=4, FAIL=0, NON_TESTABLE=2
- Q2 consolidated checks: PASS=186, WARN=3, FAIL=0, NON_TESTABLE=0
- Q3 consolidated checks: PASS=246, WARN=1, FAIL=0, NON_TESTABLE=0
- Q4 consolidated checks: PASS=20, WARN=5, FAIL=0, NON_TESTABLE=0
- Q5 consolidated checks: PASS=9, WARN=0, FAIL=0, NON_TESTABLE=0
- non_negative fields < 0 (DE): `0`
- Q1 stage2 without low-price evidence (DE): `0`

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
DE,BASE,bascule_year_market,2019,2019,0,,FRAGILE,delta_quasi_nul_vs_historique
DE,DEMAND_UP,bascule_year_market,2019,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,LOW_RIGIDITY,bascule_year_market,2019,,,,NON_TESTABLE,delta_non_interpretable_nan

### Q1 country summary (hist)
country,bascule_year_market,bascule_year_market_country,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_year_market_observed,bascule_year_physical_observed,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_status_physical,stage1_bascule_year,stage1_detected,bascule_confidence,families_active_at_bascule_pv,families_active_at_bascule_wind,families_active_at_bascule_country,drivers_at_bascule,quality_flag_unexplained_neg_prices,quality_flags,low_price_flags_count_at_bascule,physical_flags_count_at_bascule,capture_flags_count_at_bascule,stage2_market_score_at_bascule,score_breakdown_at_bascule,required_demand_uplift_to_avoid_phase2,required_demand_uplift_status,required_flex_uplift_to_avoid_phase2,required_flex_uplift_status,bascule_rationale,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,capture_ratio_pv_at_bascule,capture_ratio_wind_at_bascule,market_physical_gap_at_bascule,neg_price_explained_by_surplus_ratio_at_bascule,neg_price_unexplained_share_at_bascule,h_negative_at_bascule,notes_quality,end_year,low_price_flags_count_at_end_year,physical_flags_count_at_end_year,capture_flags_count_at_end_year,stage2_market_score_at_end_year,score_breakdown_at_end_year,sr_energy_at_end_year,far_energy_at_end_year,ir_p10_at_end_year,ttl_at_end_year,capture_ratio_pv_vs_ttl_at_end_year,capture_ratio_pv_at_end_year,capture_ratio_wind_at_end_year,market_physical_gap_at_end_year,h_negative_at_end_year,neg_price_explained_by_surplus_ratio_at_end_year,neg_price_unexplained_share_at_end_year
DE,2019,2019,2019,2019,2018,2019,,transition_observed,transition_observed,transition_observed,already_phase2_at_window_start,,False,1,"LOW_PRICE,PHYSICAL","LOW_PRICE,PHYSICAL,VALUE_WIND","LOW_PRICE,PHYSICAL,VALUE_WIND",LOW_PRICE:h_negative_obs>=200.0 (211.0); VALUE:capture_ratio_wind<=0.90 (0.870); PHYSICAL:sr_energy>=0.010 (0.016); PHYSICAL:sr_hours>=0.10 (0.140),False,,1,2,1,3,low=1;value=1;physical=1;crisis=0,0.500061,ok,0.625061,ok,Bascule validee: >=2 familles actives (LOW_PRICE/VALUE/PHYSICAL) sur 2 annees consecutives hors crise.,0.0155844,0.95749,0.528913,59.5035,0.586624,0.926638,0.870449,True,0.995261,0,211,ok,2024,3,2,2,3,low=1;value=1;physical=1;crisis=0,0.0218565,0.953423,0.302364,148.71,0.31086,0.588775,0.838449,False,457,0.964989,0


## Q2
- Test ledger: PASS=9, WARN=0, FAIL=0, NON_TESTABLE=0
- Consolidated checks: PASS=186, WARN=3, FAIL=0, NON_TESTABLE=0
- Consolidated non-PASS (filtered): none
### Comparaison historique vs prospectif
country,tech,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
DE,PV,BASE,slope,-4.73964,-4.73964,0,,FRAGILE,delta_quasi_nul_vs_historique
DE,WIND,BASE,slope,-0.30062,-0.30062,0,,FRAGILE,delta_quasi_nul_vs_historique
DE,PV,HIGH_CO2,slope,-4.73964,-0.463931,4.27571,,INFORMATIVE,delta_interpretable
DE,WIND,HIGH_CO2,slope,-0.30062,-0.121227,0.179393,,INFORMATIVE,delta_interpretable
DE,PV,HIGH_GAS,slope,-4.73964,-0.447405,4.29223,,INFORMATIVE,delta_interpretable
DE,WIND,HIGH_GAS,slope,-0.30062,-0.113901,0.186719,,INFORMATIVE,delta_interpretable

### Q2 slopes (hist)
scenario_id,country,tech,phase2_start_year_for_slope,phase2_start_reason,phase2_end_year,years_used,n_points,x_axis_used,x_axis_default,x_unit,slope,slope_per_1pp,slope_unit,intercept,r2,p_value,loo_slope_rel_var_max,n,slope_method,method,insufficient_points,slope_status,robust_flag,reason_code,outlier_years_count,slope_all_years,slope_excluding_outliers,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2,penetration_share_generation_mean_phase2,penetration_share_load_mean_phase2,slope_quality_flag,slope_quality_notes,corr_vre_load_phase2,cross_country_benchmark_slope,cross_country_benchmark_r2,cross_country_benchmark_p_value,cross_country_benchmark_n,cross_country_benchmark_reason
HIST,DE,PV,2019,q1_bascule_pv,2024,"2019,2020,2021,2023,2024",5,pv_penetration_share_generation,pv_penetration_share_generation,share_of_generation,-4.73964,-0.0473964,capture_ratio_per_share_generation,1.2804,0.796652,0.0415906,,5,ols,ols,False,OK,FRAGILE,ok,0,-4.73964,-4.73964,0.0169105,0.95899,0.431729,138.968,,,0.107383,0.107383,WARN,N_LT_6|LOO_NOT_AVAILABLE,-0.981615,-4.87776,0.829624,0.0115707,7,ok
HIST,DE,WIND,2019,q1_bascule_wind,2024,"2019,2020,2021,2023,2024",5,wind_penetration_share_generation,wind_penetration_share_generation,share_of_generation,-0.30062,-0.0030062,capture_ratio_per_share_generation,0.929817,0.411227,0.243563,,5,ols,ols,False,OK,FRAGILE,ok,0,-0.30062,-0.30062,0.0169105,0.95899,0.431729,138.968,,,0.274931,0.274931,WARN,N_LT_6|PVALUE_GT_0_05|LOO_NOT_AVAILABLE,-0.981615,-0.303283,0.418155,0.165226,7,ok


## Q3
- Test ledger: PASS=5, WARN=3, FAIL=0, NON_TESTABLE=0
- Consolidated checks: PASS=246, WARN=1, FAIL=0, NON_TESTABLE=0
- Consolidated non-PASS (filtered):
status,code,scope,scenario_id,message
WARN,BUNDLE_LEDGER_STATUS,BUNDLE,,"ledger: FAIL=0, WARN=3"

### Comparaison historique vs prospectif
country,scenario_id,metric,hist_value,scen_value,delta,hist_status,scen_status,interpretability_status,interpretability_reason
DE,BASE,inversion_k_demand,6679.49,0,-6679.49,CONTINUES,STOP_CONFIRMED,INFORMATIVE,delta_interpretable
DE,BASE,inversion_r_mustrun,0.703003,0,-0.703003,CONTINUES,STOP_CONFIRMED,INFORMATIVE,delta_interpretable
DE,DEMAND_UP,inversion_k_demand,6679.49,0,-6679.49,CONTINUES,STOP_CONFIRMED,INFORMATIVE,delta_interpretable
DE,DEMAND_UP,inversion_r_mustrun,0.703003,0,-0.703003,CONTINUES,STOP_CONFIRMED,INFORMATIVE,delta_interpretable
DE,LOW_RIGIDITY,inversion_k_demand,6679.49,0,-6679.49,CONTINUES,STOP_CONFIRMED,INFORMATIVE,delta_interpretable
DE,LOW_RIGIDITY,inversion_r_mustrun,0.703003,0,-0.703003,CONTINUES,STOP_CONFIRMED,INFORMATIVE,delta_interpretable

### Q3 inversion requirements (hist)
country,scenario_id,year,lever,required_uplift,required_uplift_mw,required_uplift_pct_avg_load,required_uplift_twh_per_year,within_bounds,target_sr,target_h_negative,target_h_below_5,predicted_sr_after,predicted_far_after,predicted_h_negative_after,predicted_h_below_5_after,predicted_h_negative_metric,h_negative_obs_before,h_below_5_obs_before,h_negative_est_before,h_below_5_est_before,applicability_flag,status,reason,export_coincidence_factor,proxy_quality_status,proxy_quality_reasons,output_schema_version
DE,HIST,2024,demand_uplift,6679.49,6679.49,0.128286,58.6726,True,0.01,200,500,0.00631561,0.652044,199.661,346.401,MARKET_PROXY_BUCKET_MODEL_EST,457,756,457,756.001,APPLICABLE,ok,ok,1,PASS,,2.0.0
DE,HIST,2024,export_uplift,7693.13,7693.13,0.147754,67.5765,True,0.01,200,500,0.00567944,0.716927,199.941,384.037,MARKET_PROXY_BUCKET_MODEL_EST,457,756,457,756.001,APPLICABLE,ok,ok,1,PASS,,2.0.0
DE,HIST,2024,flex_uplift,6759.39,6759.39,0.12982,59.3745,True,0.01,200,500,0.00683707,0.657478,199.975,352.353,MARKET_PROXY_BUCKET_MODEL_EST,457,756,457,756.001,APPLICABLE,ok,ok,1,PASS,,2.0.0


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
DE,BASE,far_after,0.998786,1,0.00121363,,INFORMATIVE,delta_interpretable
DE,BASE,surplus_unabs_energy_after,0.0113661,0,-0.0113661,,INFORMATIVE,delta_interpretable
DE,BASE,pv_capture_price_after,55.0713,126.871,71.7997,,INFORMATIVE,delta_interpretable
DE,BASE,far_before,0.953423,1,0.0465773,,INFORMATIVE,delta_interpretable
DE,BASE,surplus_unabs_energy_before,0.436213,0,-0.436213,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,far_after,0.998786,1,0.00121363,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,surplus_unabs_energy_after,0.0113661,0,-0.0113661,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,pv_capture_price_after,55.0713,138.307,83.2357,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,far_before,0.953423,1,0.0465773,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,surplus_unabs_energy_before,0.436213,0,-0.436213,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,far_after,0.998786,1,0.00121363,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,surplus_unabs_energy_after,0.0113661,0,-0.0113661,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,pv_capture_price_after,55.0713,141.962,86.8911,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,far_before,0.953423,1,0.0465773,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,surplus_unabs_energy_before,0.436213,0,-0.436213,,INFORMATIVE,delta_interpretable
DE,HIST_PRICE_ARBITRAGE_SIMPLE,far_after,0.998786,0.980246,-0.0185402,,INFORMATIVE,delta_interpretable
DE,HIST_PV_COLOCATED,far_after,0.998786,0.953423,-0.0453637,,INFORMATIVE,delta_interpretable

### Q4 sizing summary (hist)
scenario_id,country,year,dispatch_mode,objective,bess_power_mw_test,bess_energy_mwh_test,bess_duration_h_test,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_obs_before,h_negative_est_before,h_negative_est_after,h_negative_before,h_negative_after,h_negative_proxy_before,h_negative_proxy_after,h_negative_proxy_raw_after,h_negative_reducible_upper_bound,h_negative_upper_bound_after,h_below_5_reducible_upper_bound,h_below_5_obs_before,h_below_5_est_before,h_below_5_est_after,h_below_5_before,h_below_5_after,h_below_5_proxy_before,h_below_5_proxy_after,h_below_5_proxy_raw_after,delta_h_negative_est,delta_h_below_5_est,delta_h_negative,delta_h_below_5,h_negative_after_source,h_below_5_after_source,baseload_price_obs_before,baseload_price_est_before,baseload_price_est_after,baseload_price_before,baseload_price_after,capture_ratio_pv_obs_before,capture_ratio_pv_est_before,capture_ratio_pv_est_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_obs_before,capture_ratio_wind_est_before,capture_ratio_wind_est_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_est_pv,delta_capture_ratio_est_wind,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_obs_before,pv_capture_price_est_before,pv_capture_price_est_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_obs_before,wind_capture_price_est_before,wind_capture_price_est_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,charge_hours,discharge_hours,cycles_assumed_per_day,cycles_realized_per_day,simultaneous_charge_discharge_hours,energy_balance_residual,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,charge_vs_surplus_violation_hours,no_dispatch,proxy_quality_status,proxy_quality_reasons,output_schema_version,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh,on_efficient_frontier,objective_met,objective_reason,objective_not_reached,status,reason,objective_target_value,objective_direction,objective_value_after,objective_recommendation,pv_capacity_proxy_mw,power_grid_max_mw,duration_grid_max_h,grid_expansions_used,notes_quality
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,76260.3,152521,2,76260.3,152521,2,0.953423,0.998786,False,False,457,457,157.513,457,157.513,457,157.513,157.513,457,0,756,756,756.001,385.524,756,385.524,756.001,385.524,385.524,-299.487,-370.477,-299.487,-370.477,est_proxy,est_proxy,78.5155,78.5143,79.1348,78.5155,79.1348,0.588775,0.588784,0.695918,0.588784,0.695918,0.838449,0.838598,0.846846,0.838598,0.846846,0.107133,0.00824774,0.107133,0.00824774,0.436213,0.0113661,46.228,46.228,55.0713,46.228,55.0713,65.8312,65.8419,67.015,65.8419,67.015,319,319,112.006,108.233,0.0861794,0.283584,0.140255,0.00808288,0.302315,0.305471,False,False,False,False,False,,0,152521,0,0,0,24346.3,33599.3,8.78447e+06,7.73034e+06,1177,805,1,0.157364,0,9.31323e-10,0.88,0.938083,0.938083,ZERO_END,0,False,PASS,,2.0.0,v2.2.2,17.4918,False,76260.3,2,152521,True,True,met_after_grid_expansion,False,ok,met_after_grid_expansion,200,lower_is_better,157.513,,40714.2,76260.3,24,1,ok


## Q5
- Test ledger: PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0
- Consolidated checks: PASS=9, WARN=0, FAIL=0, NON_TESTABLE=0
- Consolidated non-PASS (filtered):
status,code,scope,scenario_id,message
INFO,Q5_DISTRIBUTIONAL_FIT,HIST,,Erreur distributionnelle p90/p95=8.6 EUR/MWh (acceptable).
INFO,Q5_DISTRIBUTIONAL_FIT,HIST,,Erreur distributionnelle p90/p95=23.7 EUR/MWh (acceptable).

### Comparaison historique vs prospectif
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
DE,BASE,ttl_obs,148.71,206.093,57.3835,,INFORMATIVE,delta_interpretable
DE,BASE,tca_q95,131.52,158.868,27.3489,,INFORMATIVE,delta_interpretable
DE,BASE,co2_required_base_non_negative,98.09,101.261,3.17097,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,ttl_obs,148.71,221.797,73.0874,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,tca_q95,131.52,203.737,72.2173,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,co2_required_base_non_negative,98.09,150,51.91,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,ttl_obs,148.71,226.817,78.1071,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,tca_q95,131.52,191.434,59.9147,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,co2_required_base_non_negative,98.09,100,1.90997,,INFORMATIVE,delta_interpretable
DE,HIGH_BOTH,ttl_obs,148.71,206.093,57.3835,,INFORMATIVE,delta_interpretable
DE,HIGH_BOTH,tca_q95,131.52,236.303,104.783,,INFORMATIVE,delta_interpretable
DE,HIGH_BOTH,co2_required_base_non_negative,98.09,150,51.91,,INFORMATIVE,delta_interpretable

### Q5 summary (hist)
scenario_id,country,year_range_used,ttl_reference_mode,ttl_reference_year,marginal_tech,chosen_anchor_tech,fuel_used,assumed_co2_price_eur_t,assumed_gas_price_eur_mwh_th,assumed_coal_price_eur_mwh_th,assumed_efficiency,assumed_emission_factor_t_per_mwh_th,assumed_vom_eur_mwh,assumed_fuel_multiplier_vs_gas,ttl_obs,ttl_observed_eur_mwh,ttl_obs_price_cd,ttl_annual_metrics_same_year,ttl_anchor,ttl_anchor_formula,ttl_model_eur_mwh,ttl_physical,ttl_regression,ttl_method,tca_q95,alpha,alpha_effective,corr_cd,anchor_confidence,anchor_distribution_error_p90_p95,anchor_error_p90,anchor_error_p95,anchor_status,dTCA_dCO2,dTCA_dFuel,dTCA_dGas,eta_implicit_from_dTCA_dFuel,ef_implicit_t_per_mwh_e,ttl_target,anchor_gap_to_target,required_co2_eur_t,required_gas_eur_mwh_th,required_co2_abs_eur_t,required_gas_abs_eur_mwh_th,delta_co2_vs_scenario,delta_gas_vs_scenario,tca_ccgt_eur_mwh,tca_coal_eur_mwh,tca_current_eur_mwh,pass_through_factor,base_scenario_id,base_year_reference,base_ref_source_year,base_ref_status,base_ref_reason,base_tca_ref_eur_mwh,base_ttl_model_ref_eur_mwh,base_gas_eur_per_mwh_th,base_co2_eur_per_t,ttl_proxy_method,status,reason,delta_tca_vs_base,delta_ttl_model_vs_base,delta_capture_ratio_vs_base,coherence_flag,required_co2_abs_raw_eur_t,required_gas_abs_raw_eur_mwh_th,co2_required_base,co2_required_gas_override,co2_required_base_raw,gas_required_base_raw,co2_required_base_non_negative,gas_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality,output_schema_version
HIST,DE,2018-2024,year_specific,2024,COAL,COAL,coal,70.83,46.966,25.8313,0.38,0.341,4,0.55,148.71,148.71,148.71,148.71,131.52,135.538,148.71,131.52,,anchor_distributional,131.52,17.1905,17.1905,0.307622,0.892094,8.63247,-0.0734737,17.1915,target_above_anchor,0.897368,2.63158,1.44737,0.38,0.897368,160,24.4623,98.09,63.8672,98.09,63.8672,27.26,16.9012,114.407,135.538,135.538,1,BASE,2024,2024,ok,,135.538,148.71,46.966,70.83,observed_from_prices,ok,,0,0,0,PASS,98.09,63.8672,98.09,,98.09,63.8672,98.09,63.8672,,,2.0.0
