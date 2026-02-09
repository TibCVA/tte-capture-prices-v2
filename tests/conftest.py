from __future__ import annotations

import pandas as pd
import pytest

from src.config_loader import load_countries, load_thresholds


@pytest.fixture
def countries_cfg() -> dict:
    return load_countries()


@pytest.fixture
def thresholds_cfg() -> dict:
    return load_thresholds()


@pytest.fixture
def make_raw_panel():
    def _make(n: int = 72, year: int = 2024, price: float = 60.0, net: float = 0.0) -> pd.DataFrame:
        idx = pd.date_range(f"{year}-01-01", periods=n, freq="h", tz="UTC")
        df = pd.DataFrame(index=idx)
        df.index.name = "timestamp_utc"
        df["load_total_mw"] = 50000.0
        df["price_da_eur_mwh"] = price
        df["net_position_mw"] = net
        df["gen_solar_mw"] = 8000.0
        df["gen_wind_on_mw"] = 7000.0
        df["gen_wind_off_mw"] = 1000.0
        df["gen_nuclear_mw"] = 18000.0
        df["gen_hydro_ror_mw"] = 2000.0
        df["gen_hydro_res_mw"] = 1000.0
        df["gen_hydro_psh_gen_mw"] = 0.0
        df["gen_biomass_mw"] = 1500.0
        df["gen_gas_mw"] = 4000.0
        df["gen_coal_mw"] = 500.0
        df["gen_lignite_mw"] = 500.0
        df["gen_oil_mw"] = 0.0
        df["gen_other_mw"] = 300.0
        df["psh_pump_mw"] = 500.0
        return df

    return _make

@pytest.fixture
def annual_panel_fixture() -> pd.DataFrame:
    data = []
    for country in ["FR", "DE"]:
        for year in [2021, 2022, 2023, 2024]:
            base = {
                "country": country,
                "year": year,
                "quality_flag": "OK",
                "completeness": 0.99,
                "sr_energy": 0.005 + 0.005 * (year - 2021),
                "sr_hours": 0.05 + 0.03 * (year - 2021),
                "far_energy": 0.98 - 0.05 * (year - 2021),
                "ir_p10": 0.6 + 0.05 * (year - 2021),
                "ttl_eur_mwh": 90 + 5 * (year - 2021),
                "capture_ratio_pv_vs_ttl": 0.95 - 0.1 * (year - 2021),
                "capture_ratio_wind_vs_ttl": 0.98 - 0.05 * (year - 2021),
                "h_negative_obs": 50 + 120 * (year - 2021),
                "h_below_5_obs": 200 + 150 * (year - 2021),
                "days_spread_gt50": 100 + 30 * (year - 2021),
                "pv_penetration_pct_gen": 0.1 + 0.02 * (year - 2021),
                "wind_penetration_pct_gen": 0.15 + 0.01 * (year - 2021),
                "vre_penetration_proxy": 0.2 + 0.03 * (year - 2021),
                "nrl_price_corr": 0.4,
                "regime_coherence": 0.7,
            }
            data.append(base)
    return pd.DataFrame(data)
