from __future__ import annotations

import pandas as pd

from app.page_utils import to_plot_frame


def test_to_plot_frame_handles_timestamp_in_index_and_column() -> None:
    idx = pd.date_range("2024-01-01", periods=3, freq="h", tz="UTC", name="timestamp_utc")
    df = pd.DataFrame({"timestamp_utc": idx, "price_da_eur_mwh": [10.0, 20.0, 30.0]}, index=idx)

    out = to_plot_frame(df)

    assert "timestamp_utc" in out.columns
    assert len(out) == 3
    assert out.columns.tolist().count("timestamp_utc") == 1


def test_to_plot_frame_builds_timestamp_from_datetime_index() -> None:
    idx = pd.date_range("2024-01-01", periods=2, freq="h", tz="UTC", name="ts")
    df = pd.DataFrame({"x": [1, 2]}, index=idx)

    out = to_plot_frame(df)

    assert "timestamp_utc" in out.columns
    assert len(out) == 2
