# Analyse detaillee Q1-Q5 (DE/ES)

- Run ID: `FULL_20260212_ALLQ`
- Pays: `DE, ES`
- Genere le: 2026-02-12 08:42:08 UTC

## Synthese des checks
- Q1: INFO=28, PASS=611, WARN=155
- Q2: PASS=618, WARN=101
- Q3: PASS=613, WARN=100
- Q4: PASS=44, WARN=8
- Q5: INFO=67, PASS=2, WARN=3

## Q1 - Transition Phase 1/2
### Q1 historique - synthese pays
```csv
country,bascule_year_market,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_confidence,drivers_at_bascule,stage2_market_score_at_bascule,required_demand_uplift_to_avoid_phase2
DE,2019.0,2023.0,2019.0,NaN,transition_observed,transition_observed,transition_observed,0.8,LOW_PRICE:h_negative_obs>=200.0 (211.0); VALUE:capture_ratio_wind<=0.90 (0.870); UNEXPLAINED_NEGATIVE_PRICES:share>0.35 (0.559),2.0,0.60455322265625
ES,2023.0,2023.0,2023.0,2023.0,transition_observed,transition_observed,transition_observed,1.0,LOW_PRICE:h_below_5_obs>=500.0 (558.0); LOW_PRICE:low_price_hours_share>=0.057 (0.064); VALUE:capture_ratio_wind<=0.90 (0.876); PHYSICAL:sr_energy>=0.010 (0.012); PHYSICAL:sr_hours>=0.10 (0.132),3.0,NaN
```

### Q1 historique - diagnostics annuels
```csv
country,year,stage_label,family_count_overall,score_price,score_value,score_physical,low_price_family,value_family_pv,value_family_wind,physical_family,reason_codes,bascule_year_market,bascule_year_market_pv,bascule_year_market_wind,bascule_confidence
DE,2018,ambiguous,1,0,1,0,False,False,True,False,VALUE:capture_ratio_wind<=0.90 (0.858); UNEXPLAINED_NEGATIVE_PRICES:share>0.35 (0.662),2019.0,2023.0,2019.0,0.8
DE,2019,Phase2,2,1,1,0,True,False,True,False,LOW_PRICE:h_negative_obs>=200.0 (211.0); VALUE:capture_ratio_wind<=0.90 (0.870); UNEXPLAINED_NEGATIVE_PRICES:share>0.35 (0.559),2019.0,2023.0,2019.0,0.8
DE,2020,Phase2,2,3,1,0,True,False,True,False,LOW_PRICE:h_negative_obs>=200.0 (298.0); LOW_PRICE:h_below_5_obs>=500.0 (598.0); LOW_PRICE:low_price_hours_share>=0.057 (0.068); VALUE:capture_ratio_wind<=0.90 (0.829); UNEXPLAINED_NEGATIVE_PRICES:share>0.35 (0.631),2019.0,2023.0,2019.0,0.8
DE,2021,ambiguous,1,0,2,0,False,True,True,False,VALUE:capture_ratio_pv<=0.80 (0.779); VALUE:capture_ratio_wind<=0.90 (0.859); UNEXPLAINED_NEGATIVE_PRICES:share>0.35 (0.590),2019.0,2023.0,2019.0,0.8
DE,2022,ambiguous,1,0,1,0,False,False,True,False,VALUE:capture_ratio_wind<=0.90 (0.737),2019.0,2023.0,2019.0,0.8
DE,2023,Phase2,2,3,2,0,True,True,True,False,LOW_PRICE:h_negative_obs>=200.0 (300.0); LOW_PRICE:h_below_5_obs>=500.0 (530.0); LOW_PRICE:low_price_hours_share>=0.057 (0.061); VALUE:capture_ratio_pv<=0.80 (0.758); VALUE:capture_ratio_wind<=0.90 (0.840),2019.0,2023.0,2019.0,0.8
DE,2024,Phase2,2,3,2,0,True,True,True,False,LOW_PRICE:h_negative_obs>=200.0 (457.0); LOW_PRICE:h_below_5_obs>=500.0 (756.0); LOW_PRICE:low_price_hours_share>=0.057 (0.086); VALUE:capture_ratio_pv<=0.80 (0.589); VALUE:capture_ratio_wind<=0.90 (0.838),2019.0,2023.0,2019.0,0.8
ES,2018,Phase1,0,0,0,0,False,False,False,False,NaN,2023.0,2023.0,2023.0,1.0
ES,2019,Phase1,0,0,0,0,False,False,False,False,NaN,2023.0,2023.0,2023.0,1.0
ES,2020,Phase1,0,0,0,0,False,False,False,False,NaN,2023.0,2023.0,2023.0,1.0
ES,2021,Phase1,0,0,0,0,False,False,False,False,NaN,2023.0,2023.0,2023.0,1.0
ES,2022,ambiguous,0,0,0,0,False,False,False,False,NaN,2023.0,2023.0,2023.0,1.0
ES,2023,Phase2,3,2,1,2,True,False,True,True,LOW_PRICE:h_below_5_obs>=500.0 (558.0); LOW_PRICE:low_price_hours_share>=0.057 (0.064); VALUE:capture_ratio_wind<=0.90 (0.876); PHYSICAL:sr_energy>=0.010 (0.012); PHYSICAL:sr_hours>=0.10 (0.132),2023.0,2023.0,2023.0,1.0
ES,2024,Phase2,3,3,2,2,True,True,True,True,LOW_PRICE:h_negative_obs>=200.0 (247.0); LOW_PRICE:h_below_5_obs>=500.0 (1690.0); LOW_PRICE:low_price_hours_share>=0.057 (0.192); VALUE:capture_ratio_pv<=0.80 (0.679); VALUE:capture_ratio_wind<=0.90 (0.882); PHYSICAL:sr_energy>=0.010 (0.015); PHYSICAL:sr_hours>=0.10 (0.169),2023.0,2023.0,2023.0,1.0
```

### Q1 historique - explainability prix negatifs
```csv
country,year,negative_hours,share_neg_hours_in_regime_A,share_neg_hours_in_regime_B,share_neg_hours_in_low_residual_bucket,share_neg_hours_explained_union,share_neg_hours_unexplained,flag_unexplained_negative_prices
DE,2018,133.0,0.0,0.3383458646616541,0.0,0.3383458646616541,0.6616541353383458,True
DE,2019,211.0,0.0284360189573459,0.4123222748815165,0.0,0.4407582938388625,0.5592417061611374,True
DE,2020,298.0,0.0,0.3691275167785235,0.0,0.3691275167785235,0.6308724832214765,True
DE,2021,139.0,0.0,0.4100719424460431,0.0,0.4100719424460431,0.5899280575539568,True
DE,2022,69.0,0.0,0.7391304347826086,0.0,0.7391304347826086,0.2608695652173913,False
DE,2023,300.0,0.0,0.8633333333333333,0.0,0.8633333333333333,0.1366666666666667,False
DE,2024,457.0,0.0,0.7899343544857768,0.0,0.7899343544857768,0.2100656455142232,False
ES,2018,0.0,NaN,NaN,NaN,NaN,NaN,False
ES,2019,0.0,NaN,NaN,NaN,NaN,NaN,False
ES,2020,0.0,NaN,NaN,NaN,NaN,NaN,False
ES,2021,0.0,NaN,NaN,NaN,NaN,NaN,False
ES,2022,0.0,NaN,NaN,NaN,NaN,NaN,False
ES,2023,0.0,NaN,NaN,NaN,NaN,NaN,False
ES,2024,247.0,0.0161943319838056,0.7004048582995951,0.0,0.7165991902834008,0.2834008097165992,False
```

### Q1 scenario `DEMAND_UP` - synthese pays
```csv
country,bascule_year_market,bascule_year_market_pv,bascule_year_market_wind,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_confidence,drivers_at_bascule,stage2_market_score_at_bascule
DE,NaN,NaN,NaN,not_reached_in_window,not_reached_in_window,not_reached_in_window,0.0,NaN,0.0
ES,NaN,NaN,NaN,not_reached_in_window,not_reached_in_window,not_reached_in_window,0.0,NaN,0.0
```

### Q1 scenario `LOW_RIGIDITY` - synthese pays
```csv
country,bascule_year_market,bascule_year_market_pv,bascule_year_market_wind,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_confidence,drivers_at_bascule,stage2_market_score_at_bascule
DE,NaN,NaN,NaN,not_reached_in_window,not_reached_in_window,not_reached_in_window,0.0,NaN,0.0
ES,NaN,NaN,NaN,not_reached_in_window,not_reached_in_window,not_reached_in_window,0.0,NaN,0.0
```

## Q2 - Pentes de Phase 2
### Q2 historique
```csv
country,tech,phase2_start_year_for_slope,phase2_end_year,years_used,n_points,x_axis_used,slope,slope_per_1pp,slope_unit,r2,p_value,loo_slope_rel_var_max,slope_quality_flag,slope_quality_notes,reason_code
DE,PV,2019.0,2024.0,"2019,2020,2023,2024",4,pv_penetration_share_load,-5.534260520793036,-0.0553426052079303,capture_ratio_per_share_load,0.8849617532735934,0.0592759420140285,NaN,WARN,N_LT_6|PVALUE_GT_0_05|LOO_NOT_AVAILABLE,ok
DE,WIND,2019.0,2024.0,"2019,2020,2023,2024",4,wind_penetration_share_load,-0.3683517153592101,-0.0036835171535921,capture_ratio_per_share_load,0.3157002068487917,0.4381279444136844,NaN,WARN,N_LT_6|PVALUE_GT_0_05|LOO_NOT_AVAILABLE,ok
ES,PV,2023.0,2024.0,"2023,2024",2,pv_penetration_share_load,NaN,NaN,capture_ratio_per_share_load,NaN,NaN,NaN,WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE,INSUFFICIENT_POINTS
ES,WIND,2023.0,2024.0,"2023,2024",2,wind_penetration_share_load,NaN,NaN,capture_ratio_per_share_load,NaN,NaN,NaN,WARN,INSUFFICIENT_POINTS|N_LT_6|METHOD_NOT_OLS|PVALUE_MISSING|LOO_NOT_AVAILABLE,INSUFFICIENT_POINTS
```

### Q2 HIGH_CO2
```csv
country,tech,phase2_start_year_for_slope,phase2_end_year,years_used,n_points,x_axis_used,slope,slope_per_1pp,slope_unit,r2,p_value,loo_slope_rel_var_max,slope_quality_flag,slope_quality_notes,reason_code
DE,PV,NaN,NaN,NaN,0,none,NaN,NaN,capture_ratio_per_share_load,NaN,NaN,NaN,WARN,INSUFFICIENT_POINTS,q1_no_phase2_market_year
DE,WIND,NaN,NaN,NaN,0,none,NaN,NaN,capture_ratio_per_share_load,NaN,NaN,NaN,WARN,INSUFFICIENT_POINTS,q1_no_phase2_market_year
ES,PV,NaN,NaN,NaN,0,none,NaN,NaN,capture_ratio_per_share_load,NaN,NaN,NaN,WARN,INSUFFICIENT_POINTS,q1_no_phase2_market_year
ES,WIND,NaN,NaN,NaN,0,none,NaN,NaN,capture_ratio_per_share_load,NaN,NaN,NaN,WARN,INSUFFICIENT_POINTS,q1_no_phase2_market_year
```

### Q2 HIGH_GAS
```csv
country,tech,phase2_start_year_for_slope,phase2_end_year,years_used,n_points,x_axis_used,slope,slope_per_1pp,slope_unit,r2,p_value,loo_slope_rel_var_max,slope_quality_flag,slope_quality_notes,reason_code
DE,PV,NaN,NaN,NaN,0,none,NaN,NaN,capture_ratio_per_share_load,NaN,NaN,NaN,WARN,INSUFFICIENT_POINTS,q1_no_phase2_market_year
DE,WIND,NaN,NaN,NaN,0,none,NaN,NaN,capture_ratio_per_share_load,NaN,NaN,NaN,WARN,INSUFFICIENT_POINTS,q1_no_phase2_market_year
ES,PV,NaN,NaN,NaN,0,none,NaN,NaN,capture_ratio_per_share_load,NaN,NaN,NaN,WARN,INSUFFICIENT_POINTS,q1_no_phase2_market_year
ES,WIND,NaN,NaN,NaN,0,none,NaN,NaN,capture_ratio_per_share_load,NaN,NaN,NaN,WARN,INSUFFICIENT_POINTS,q1_no_phase2_market_year
```

## Q3 - Inversion / sortie de Phase 2
### Q3 historique
```csv
country,scenario_id,year,lever,required_uplift,within_bounds,target_sr,target_h_negative,predicted_sr_after,predicted_h_negative_after,predicted_h_negative_metric,applicability_flag,status,reason
DE,HIST,2024,demand_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
DE,HIST,2024,export_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
DE,HIST,2024,flex_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
ES,HIST,2024,demand_uplift,NaN,False,0.05,200.0,0.0,879.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
ES,HIST,2024,export_uplift,NaN,False,0.05,200.0,0.0001138433515482,883.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
ES,HIST,2024,flex_uplift,NaN,False,0.05,200.0,0.0,883.0,PROXY_SURPLUS_OR_LOW_NRL,APPLICABLE,NOT_CALCULABLE,not_calculable
```

### Q3 DEMAND_UP
```csv
country,scenario_id,year,lever,required_uplift,within_bounds,target_sr,target_h_negative,predicted_sr_after,predicted_h_negative_after,predicted_h_negative_metric,applicability_flag,status,reason
DE,DEMAND_UP,2035,demand_uplift,NaN,False,0.05,200.0,0.0,876.0,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,not_calculable
DE,DEMAND_UP,2035,export_uplift,NaN,False,0.05,200.0,0.0,876.0,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,not_calculable
DE,DEMAND_UP,2035,flex_uplift,NaN,False,0.05,200.0,0.0,876.0,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,not_calculable
ES,DEMAND_UP,2035,demand_uplift,NaN,False,0.05,200.0,0.0,876.0,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,not_calculable
ES,DEMAND_UP,2035,export_uplift,NaN,False,0.05,200.0,0.0,876.0,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,not_calculable
ES,DEMAND_UP,2035,flex_uplift,NaN,False,0.05,200.0,0.0,876.0,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,not_calculable
```

### Q3 LOW_RIGIDITY
```csv
country,scenario_id,year,lever,required_uplift,within_bounds,target_sr,target_h_negative,predicted_sr_after,predicted_h_negative_after,predicted_h_negative_metric,applicability_flag,status,reason
DE,LOW_RIGIDITY,2035,demand_uplift,NaN,False,0.05,200.0,0.0,876.0,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,not_calculable
DE,LOW_RIGIDITY,2035,export_uplift,NaN,False,0.05,200.0,0.0,876.0,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,not_calculable
DE,LOW_RIGIDITY,2035,flex_uplift,NaN,False,0.05,200.0,0.0,876.0,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,not_calculable
ES,LOW_RIGIDITY,2035,demand_uplift,NaN,False,0.05,200.0,0.0,876.0,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,not_calculable
ES,LOW_RIGIDITY,2035,export_uplift,NaN,False,0.05,200.0,0.0,876.0,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,not_calculable
ES,LOW_RIGIDITY,2035,flex_uplift,NaN,False,0.05,200.0,0.0,876.0,PROXY_SURPLUS_OR_LOW_NRL,HORS_SCOPE_PHASE2,HORS_SCOPE_PHASE2,not_calculable
```

## Q4 - Sizing BESS
### Q4 historique - synthese sizing
```csv
country,scenario_id,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,h_negative_before,h_negative_proxy_after,h_negative_reducible_upper_bound,h_negative_upper_bound_after,h_below_5_before,h_below_5_proxy_after
DE,HIST,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,250.0,500.0,2.0,1.0,1.0,457,457,0,457,756,457
ES,HIST,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,250.0,500.0,2.0,0.9994023008613372,0.9995517261480726,247,247,1,246,1642,247
```

### Q4 HIGH_CO2 - synthese sizing
```csv
country,scenario_id,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,h_negative_before,h_negative_proxy_after,h_negative_reducible_upper_bound,h_negative_upper_bound_after,h_below_5_before,h_below_5_proxy_after
DE,HIGH_CO2,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0.0,0.0,0.0,1.0,1.0,0,0,0,0,0,0
ES,HIGH_CO2,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0.0,0.0,0.0,1.0,1.0,0,0,0,0,0,0
```

### Q4 HIGH_GAS - synthese sizing
```csv
country,scenario_id,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,h_negative_before,h_negative_proxy_after,h_negative_reducible_upper_bound,h_negative_upper_bound_after,h_below_5_before,h_below_5_proxy_after
DE,HIGH_GAS,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0.0,0.0,0.0,1.0,1.0,0,0,0,0,0,0
ES,HIGH_GAS,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0.0,0.0,0.0,1.0,1.0,0,0,0,0,0,0
```

### Q4 historique - points sur frontiere efficiente (DE/ES)
```csv
country,scenario_id,year,bess_power_gw,bess_energy_gwh,cycles_assumed_per_day,cycles_realized_per_day,far_energy_after,surplus_unabsorbed_twh_after,h_negative_proxy_after,h_negative_reducible_upper_bound,on_efficient_frontier,monotonicity_check_flag,physics_check_flag,notes
DE,HIST,2024,0.0,0.0,1.0,0.0,1.0,0.0,457,0,True,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.0,0.0,1.0,0.0,0.9994023008613372,0.002132,247,0,True,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.25,0.5,1.0,0.0025630687212149,0.9995517261480726,0.0015989982091109,247,1,True,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.25,1.0,1.0,0.0025630687212149,0.9997011514348082,0.0010659964182219,247,1,True,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.25,1.5,1.0,0.0017712204007285,0.9997120839514978,0.001027,247,1,True,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.5,2.0,1.0,0.0023250273224043,0.9999444913557902,0.000198,247,2,True,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.75,1.5,1.0,0.0025630687212149,0.9998505767215438,0.0005329946273329,247,3,True,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,0.75,3.0,1.0,0.0017087067395264,1.0,0.0,247,4,True,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
ES,HIST,2024,1.0,2.0,1.0,0.0025630601092896,1.0,0.0,247,4,True,PASS,PASS,dispatch_mode=SURPLUS_FIRST; objective=LOW_PRICE_TARGET
```

## Q5 - Ancre thermique / sensibilite commodites
### Q5 historique
```csv
country,scenario_id,year,gas_eur_per_mwh_th,co2_eur_per_t,tca_ccgt_eur_mwh,tca_coal_eur_mwh,ttl_observed_eur_mwh,ttl_model_eur_mwh,delta_tca_vs_base,delta_ttl_model_vs_base,coherence_flag
DE,HIST,2024,46.9,70.83,114.28665454545454,135.4421842105263,146.069,146.069,0.0,0.0,PASS
ES,HIST,2024,47.02,70.69,114.45341818181817,135.49023684210528,140.0,140.0,0.0,0.0,PASS
```

### Q5 HIGH_CO2
```csv
country,scenario_id,year,gas_eur_per_mwh_th,co2_eur_per_t,tca_ccgt_eur_mwh,tca_coal_eur_mwh,ttl_observed_eur_mwh,ttl_model_eur_mwh,delta_tca_vs_base,delta_ttl_model_vs_base,coherence_flag
DE,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,228.36196259457392,203.7368421052632,NaN,NaN,WARN
ES,HIGH_CO2,2035,45.0,150.0,139.9090909090909,203.7368421052632,174.19037209080483,139.9090909090909,NaN,NaN,WARN
```

### Q5 HIGH_GAS
```csv
country,scenario_id,year,gas_eur_per_mwh_th,co2_eur_per_t,tca_ccgt_eur_mwh,tca_coal_eur_mwh,ttl_observed_eur_mwh,ttl_model_eur_mwh,delta_tca_vs_base,delta_ttl_model_vs_base,coherence_flag
DE,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,233.3816994366792,191.43421052631575,NaN,NaN,WARN
ES,HIGH_GAS,2035,67.5,100.0,162.45454545454544,191.43421052631575,182.0812811817139,162.45454545454544,NaN,NaN,WARN
```

### Q5 HIGH_BOTH
```csv
country,scenario_id,year,gas_eur_per_mwh_th,co2_eur_per_t,tca_ccgt_eur_mwh,tca_coal_eur_mwh,ttl_observed_eur_mwh,ttl_model_eur_mwh,delta_tca_vs_base,delta_ttl_model_vs_base,coherence_flag
DE,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,212.65801522615288,236.30263157894737,NaN,NaN,WARN
ES,HIGH_BOTH,2035,67.5,150.0,180.8181818181818,236.30263157894737,167.7630993635321,180.8181818181818,NaN,NaN,WARN
```
