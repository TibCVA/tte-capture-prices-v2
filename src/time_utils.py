"""Time helpers."""

from __future__ import annotations

import calendar

import pandas as pd


def to_utc_index(idx: pd.DatetimeIndex) -> pd.DatetimeIndex:
    if not isinstance(idx, pd.DatetimeIndex):
        raise TypeError("Expected DatetimeIndex")
    if idx.tz is None:
        return idx.tz_localize("UTC")
    return idx.tz_convert("UTC")


def expected_hours(year: int) -> int:
    return 8784 if calendar.isleap(year) else 8760


def annual_utc_index(year: int) -> pd.DatetimeIndex:
    start = pd.Timestamp(f"{year}-01-01 00:00:00", tz="UTC")
    end = pd.Timestamp(f"{year+1}-01-01 00:00:00", tz="UTC")
    return pd.date_range(start, end, freq="h", inclusive="left")


def local_peak_mask(index_utc: pd.DatetimeIndex, timezone: str) -> pd.Series:
    idx = to_utc_index(index_utc).tz_convert(timezone)
    mask = (idx.weekday < 5) & (idx.hour >= 8) & (idx.hour < 20)
    return pd.Series(mask, index=to_utc_index(index_utc))

