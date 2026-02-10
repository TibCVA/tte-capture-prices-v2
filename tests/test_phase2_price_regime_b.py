from __future__ import annotations

import pandas as pd

from src.constants import COL_NRL, COL_PRICE_DA, COL_REGIME, COL_SURPLUS, COL_SURPLUS_UNABS
from src.scenario.phase2_engine import _inject_synthetic_price


def test_regime_b_price_is_calibrated_and_surplus_sensitive() -> None:
    idx = pd.date_range("2030-01-01", periods=5, freq="h", tz="UTC")
    hourly = pd.DataFrame(index=idx)
    hourly[COL_NRL] = [-100.0, -300.0, -600.0, -900.0, -1200.0]
    hourly[COL_SURPLUS] = [100.0, 300.0, 600.0, 900.0, 1200.0]
    hourly[COL_SURPLUS_UNABS] = 0.0
    hourly[COL_REGIME] = "B"

    row = pd.Series(
        {
            "marginal_tech": "gas_ccgt",
            "marginal_efficiency": 0.55,
            "marginal_emission_factor_t_per_mwh": 0.202,
            "gas_eur_per_mwh_th": 40.0,
            "co2_eur_per_t": 80.0,
        }
    )

    calib = {
        "price_anchor_ref": 90.0,
        "price_b_floor": -20.0,
        "price_b_cap": 80.0,
        "price_b_intercept": 30.0,
        "price_b_slope_surplus_norm": -18.0,
        "price_b_tca_pass": 0.40,
        "surplus_p95": 1200.0,
        "nrl_p90": 1000.0,
        "nrl_p99": 3000.0,
        "price_c_level": 70.0,
        "price_d_level": 120.0,
    }

    out = _inject_synthetic_price(hourly.copy(), row=row, calib=calib)
    prices = out[COL_PRICE_DA].to_numpy(dtype=float)

    # Prices in B should be finite and within calibrated floor/cap.
    assert (prices >= -20.0 - 1e-9).all()
    assert (prices <= 80.0 + 1e-9).all()

    # With negative slope on surplus, higher surplus should not increase B price.
    assert prices[0] >= prices[-1]


def test_regime_b_price_responds_to_tca_delta_via_pass_through() -> None:
    idx = pd.date_range("2030-01-01", periods=2, freq="h", tz="UTC")
    hourly = pd.DataFrame(index=idx)
    hourly[COL_NRL] = [-200.0, -200.0]
    hourly[COL_SURPLUS] = [200.0, 200.0]
    hourly[COL_SURPLUS_UNABS] = 0.0
    hourly[COL_REGIME] = "B"

    base_row = pd.Series(
        {
            "marginal_tech": "gas_ccgt",
            "marginal_efficiency": 0.55,
            "marginal_emission_factor_t_per_mwh": 0.202,
            "gas_eur_per_mwh_th": 30.0,
            "co2_eur_per_t": 60.0,
        }
    )
    high_row = base_row.copy()
    high_row["gas_eur_per_mwh_th"] = 80.0

    calib = {
        "price_anchor_ref": 70.0,
        "price_b_floor": -30.0,
        "price_b_cap": 120.0,
        "price_b_intercept": 15.0,
        "price_b_slope_surplus_norm": -5.0,
        "price_b_tca_pass": 0.50,
        "surplus_p95": 500.0,
        "nrl_p90": 1000.0,
        "nrl_p99": 3000.0,
        "price_c_level": 65.0,
        "price_d_level": 115.0,
    }

    p_base = _inject_synthetic_price(hourly.copy(), base_row, calib)[COL_PRICE_DA].mean()
    p_high = _inject_synthetic_price(hourly.copy(), high_row, calib)[COL_PRICE_DA].mean()

    assert float(p_high) > float(p_base)
