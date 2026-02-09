from __future__ import annotations

import pandas as pd

from src.data_fetcher import _normalize_index_and_frequency
from src.time_utils import annual_utc_index


def test_index_is_utc_hourly() -> None:
    idx = annual_utc_index(2024)
    assert idx.tz is not None
    assert len(idx) == 8784


def test_resample_15min_to_hour_mean() -> None:
    idx = pd.date_range("2024-01-01", periods=8, freq="15min", tz="UTC")
    s = pd.Series([0, 2, 4, 6, 8, 10, 12, 14], index=idx)
    norm, stats = _normalize_index_and_frequency(s, pd.date_range("2024-01-01", periods=2, freq="h", tz="UTC"))
    assert abs(float(norm.iloc[0]) - 3.0) < 1e-9
    assert stats["resampling_applied"] is True


def test_no_interpolation_keeps_nan() -> None:
    idx = pd.date_range("2024-01-01", periods=2, freq="h", tz="UTC")
    s = pd.Series([1.0, float("nan")], index=idx)
    norm, _ = _normalize_index_and_frequency(s, idx)
    assert norm.isna().sum() == 1
