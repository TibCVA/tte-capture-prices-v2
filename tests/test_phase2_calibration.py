from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.scenario.calibration import calibrate_country_bundle


def test_calibrate_country_bundle_returns_expected_keys_and_ranges(tmp_path: Path) -> None:
    idx = pd.date_range("2024-01-01", periods=240, freq="h", tz="UTC")
    ref = pd.DataFrame(index=idx)
    ref["gen_must_run_mw"] = 15000.0
    ref["price_da_eur_mwh"] = 60.0
    ref["surplus_mw"] = 0.0
    ref["nrl_mw"] = 3000.0
    ref["regime"] = "C"

    # Inject enough regime B points for calibration fit.
    ref.loc[idx[:140], "regime"] = "B"
    ref.loc[idx[:140], "surplus_mw"] = 500.0
    ref.loc[idx[:140], "price_da_eur_mwh"] = 25.0

    annual_hist = pd.DataFrame(
        [
            {
                "country": "FR",
                "year": 2024,
                "far_energy": 0.82,
            }
        ]
    )

    interco = pd.DataFrame(
        [
            {
                "country": "FR",
                "interconnection_export_gw_proxy": 6.0,
            }
        ]
    )
    interco_path = tmp_path / "interco.csv"
    interco.to_csv(interco_path, index=False)

    coincidence = pd.DataFrame(
        [
            {
                "country": "FR",
                "neighbor_country": "BE",
                "export_coincidence_factor": 0.52,
            }
        ]
    )
    coincidence_path = tmp_path / "coincidence.csv"
    coincidence.to_csv(coincidence_path, index=False)

    scenario_row = pd.Series(
        {
            "scenario_id": "BASE",
            "export_coincidence_factor": 0.40,
            "interconnection_export_gw": 5.0,
        }
    )

    calib = calibrate_country_bundle(
        country="FR",
        ref_hourly=ref,
        annual_hist=annual_hist,
        scenario_row=scenario_row,
        interconnection_proxy_path=interco_path,
        coincidence_matrix_path=coincidence_path,
    )

    expected = {
        "mr_p10_mw",
        "mr_mean_mw",
        "flex_realization_factor",
        "export_realization_factor",
        "psh_realization_factor",
        "stress_penalty",
        "export_cap_eff_gw",
        "export_coincidence_used",
        "price_b_floor",
        "price_b_intercept",
        "price_b_slope_surplus_norm",
        "price_c_level",
        "price_d_level",
    }
    assert expected.issubset(set(calib.keys()))

    assert 0.30 <= float(calib["flex_realization_factor"]) <= 0.95
    assert 0.30 <= float(calib["export_realization_factor"]) <= 0.95
    assert 0.0 <= float(calib["export_coincidence_used"]) <= 0.95
    assert float(calib["price_b_slope_surplus_norm"]) < 0.0

    # Coincidence used should not be below empirical value when both exist.
    assert float(calib["export_coincidence_used"]) >= 0.52
