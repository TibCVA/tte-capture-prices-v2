from __future__ import annotations

import numpy as np
import pandas as pd

from src.core.market_proxy import fit_market_proxy, predict_event_counts, predict_prices


def test_market_proxy_counts_respect_ordering():
    nrl = np.linspace(-1000.0, 1000.0, 200)
    price = (nrl * 0.03) + 5.0
    df = pd.DataFrame({"nrl_mw": nrl, "price_da_eur_mwh": price})
    mapping = fit_market_proxy(df, n_bins=10)
    pred = predict_prices(mapping, pd.Series(nrl))
    counts = predict_event_counts(pred)
    assert float(counts["h_below5_pred"]) >= float(counts["h_negative_pred"])


def test_market_proxy_positive_ttl_shift_raises_upper_tail():
    nrl = np.linspace(-2000.0, 2000.0, 500)
    price = (nrl * 0.02) + 20.0
    df = pd.DataFrame({"nrl_mw": nrl, "price_da_eur_mwh": price})
    mapping = fit_market_proxy(df, n_bins=20)
    pred_base = predict_prices(mapping, pd.Series(nrl), ttl_shift_eur_mwh=0.0, shift_top_nrl_quantile=0.90)
    pred_up = predict_prices(mapping, pd.Series(nrl), ttl_shift_eur_mwh=15.0, shift_top_nrl_quantile=0.90)
    assert float(np.nanquantile(pred_up, 0.95)) > float(np.nanquantile(pred_base, 0.95))

