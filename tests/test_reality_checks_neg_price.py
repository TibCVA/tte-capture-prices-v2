from __future__ import annotations

import pandas as pd

from src.modules.reality_checks import build_common_checks


def test_neg_price_principal_check_uses_ab_or_low_residual():
    annual = pd.DataFrame(
        [
            {
                "country": "FR",
                "year": 2024,
                "sr_energy": 0.02,
                "far_energy": 0.90,
                "ir_p10": 1.2,
                "regime_coherence": 0.8,
                "h_regime_c": 3000,
                "h_regime_d": 1000,
                "share_neg_price_hours_in_AB": 0.30,
                "share_neg_price_hours_in_AB_OR_LOW_RESIDUAL": 0.65,
                "load_total_twh": 100.0,
                "load_net_twh": 99.5,
                "psh_pumping_twh": 0.5,
                "gen_must_run_twh": 20.0,
                "gen_primary_twh": 80.0,
            }
        ]
    )
    checks = build_common_checks(annual)
    codes = {str(c.get("code")): str(c.get("status")) for c in checks}
    assert codes.get("RC_NEG_NOT_IN_AB") == "INFO"
    assert codes.get("RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL") == "WARN"

