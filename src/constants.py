"""Core constants for tte-capture-prices-v2."""

from __future__ import annotations

DEFAULT_COUNTRIES = ["FR", "DE", "ES", "NL", "BE", "CZ", "IT_NORD"]
DEFAULT_YEAR_START = 2018
DEFAULT_YEAR_END = 2024

HOURS_YEAR = 8760
HOURS_LEAP = 8784

# Canonical columns
COL_TIMESTAMP_UTC = "timestamp_utc"
COL_TS_UTC_ALIAS = "ts_utc"
COL_COUNTRY = "country"
COL_YEAR = "year"

COL_PRICE_DA = "price_da_eur_mwh"
COL_LOAD_TOTAL = "load_total_mw"
COL_LOAD_NET = "load_mw"
COL_NET_POSITION = "net_position_mw"
COL_EXPORTS = "exports_mw"

COL_GEN_SOLAR = "gen_solar_mw"
COL_GEN_PV_ALIAS = "gen_pv_mw"
COL_GEN_WIND_ON = "gen_wind_on_mw"
COL_GEN_WIND_OFF = "gen_wind_off_mw"
COL_GEN_NUCLEAR = "gen_nuclear_mw"
COL_GEN_HYDRO_ROR = "gen_hydro_ror_mw"
COL_GEN_HYDRO_RES = "gen_hydro_res_mw"
COL_GEN_HYDRO_PSH_GEN = "gen_hydro_psh_gen_mw"
COL_GEN_BIOMASS = "gen_biomass_mw"
COL_GEN_GAS = "gen_gas_mw"
COL_GEN_COAL = "gen_coal_mw"
COL_GEN_LIGNITE = "gen_lignite_mw"
COL_GEN_OIL = "gen_oil_mw"
COL_GEN_OTHER = "gen_other_mw"

COL_PSH_PUMP = "psh_pump_mw"
COL_PSH_PUMP_ALIAS = "psh_pumping_mw"
COL_PSH_PUMP_COVERAGE = "psh_pumping_coverage_share"
COL_PSH_PUMP_STATUS = "psh_pumping_data_status"

COL_GEN_VRE = "gen_vre_mw"
COL_GEN_TOTAL = "gen_total_mw"
COL_GEN_PRIMARY = "gen_primary_mw"
COL_GEN_MUST_RUN_OBS = "gen_must_run_observed_mw"
COL_GEN_MUST_RUN = "gen_must_run_mw"

COL_NRL = "nrl_mw"
COL_NRL_POS = "nrl_pos_mw"
COL_LOW_RESIDUAL_HOUR = "low_residual_hour"
COL_LOW_RESIDUAL_THRESHOLD = "low_residual_threshold_mw"
COL_SURPLUS = "surplus_mw"
COL_FLEX_EXPORTS = "flex_sink_exports_mw"
COL_FLEX_PSH = "flex_sink_psh_pump_mw"
COL_FLEX_OBS = "flex_sink_observed_mw"
COL_SINK_NON_BESS_ALIAS = "sink_non_bess_mw"
COL_BESS_CHARGE = "bess_charge_mw"
COL_BESS_DISCHARGE = "bess_discharge_mw"
COL_BESS_SOC = "bess_soc_mwh"
COL_FLEX_EFFECTIVE = "flex_effective_mw"
COL_SURPLUS_ABSORBED = "surplus_absorbed_mw"
COL_SURPLUS_UNABS = "surplus_unabsorbed_mw"
COL_SURPLUS_UNABS_ALIAS = "surplus_unabs_mw"

COL_REGIME = "regime"
COL_REGIME_ALIAS = "regime_phys"

COL_Q_MISSING_PRICE = "q_missing_price"
COL_Q_MISSING_LOAD = "q_missing_load"
COL_Q_MISSING_GENERATION = "q_missing_generation"
COL_Q_MISSING_NET_POSITION = "q_missing_net_position"
COL_Q_MISSING_PSH_PUMP = "q_missing_psh_pump"
COL_Q_ANY_CRITICAL_MISSING = "q_any_critical_missing"
COL_Q_BAD_LOAD_NET = "q_bad_load_net"

COL_NRL_THRESHOLD = "nrl_positive_quantile_threshold"
COL_LOAD_NET_MODE = "load_net_mode"
COL_MUST_RUN_MODE = "must_run_mode"
COL_ENTSOE_CODE_USED = "entsoe_code_used"
COL_DATA_VERSION_HASH = "data_version_hash"

COL_REGIME_COHERENCE = "regime_coherence"
COL_NRL_PRICE_CORR = "nrl_price_corr"
COL_COMPLETENESS = "completeness"
COL_QUALITY_FLAG = "quality_flag"

PRICE_LOW_THRESHOLD_DEFAULT = 5.0
PRICE_NEGATIVE_THRESHOLD = 0.0

CANONICAL_ALIAS_COLUMNS = {
    COL_TIMESTAMP_UTC: COL_TS_UTC_ALIAS,
    COL_GEN_SOLAR: COL_GEN_PV_ALIAS,
    COL_PSH_PUMP: COL_PSH_PUMP_ALIAS,
    COL_SURPLUS_UNABS: COL_SURPLUS_UNABS_ALIAS,
    COL_REGIME: COL_REGIME_ALIAS,
    COL_FLEX_OBS: COL_SINK_NON_BESS_ALIAS,
}

GEN_COLUMNS = [
    COL_GEN_SOLAR,
    COL_GEN_WIND_ON,
    COL_GEN_WIND_OFF,
    COL_GEN_NUCLEAR,
    COL_GEN_HYDRO_ROR,
    COL_GEN_HYDRO_RES,
    COL_GEN_HYDRO_PSH_GEN,
    COL_GEN_BIOMASS,
    COL_GEN_GAS,
    COL_GEN_COAL,
    COL_GEN_LIGNITE,
    COL_GEN_OIL,
    COL_GEN_OTHER,
]

REQUIRED_HOURLY_COLUMNS = [
    COL_TIMESTAMP_UTC,
    COL_COUNTRY,
    COL_YEAR,
    COL_PRICE_DA,
    COL_LOAD_TOTAL,
    COL_LOAD_NET,
    COL_NET_POSITION,
    COL_EXPORTS,
    COL_GEN_SOLAR,
    COL_GEN_WIND_ON,
    COL_GEN_WIND_OFF,
    COL_GEN_VRE,
    COL_GEN_MUST_RUN,
    COL_NRL,
    COL_SURPLUS,
    COL_PSH_PUMP,
    COL_FLEX_OBS,
    COL_BESS_CHARGE,
    COL_FLEX_EFFECTIVE,
    COL_SURPLUS_ABSORBED,
    COL_SURPLUS_UNABS,
    COL_REGIME,
]

THERMAL_DEFAULTS = {
    "CCGT": {
        "efficiency": 0.55,
        "emission_factor_t_per_mwh_th": 0.202,
        "vom_eur_mwh": 3.0,
    },
    "COAL": {
        "efficiency": 0.38,
        "emission_factor_t_per_mwh_th": 0.341,
        "vom_eur_mwh": 4.0,
    },
}

