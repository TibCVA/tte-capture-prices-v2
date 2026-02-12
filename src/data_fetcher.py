"""ENTSO-E ingestion and raw cache writer (freeze-first)."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from dotenv import dotenv_values
from entsoe import EntsoePandasClient

from src.config_loader import resolve_entsoe_segments
from src.constants import (
    COL_GEN_BIOMASS,
    COL_GEN_COAL,
    COL_GEN_GAS,
    COL_GEN_HYDRO_PSH_GEN,
    COL_GEN_HYDRO_RES,
    COL_GEN_HYDRO_ROR,
    COL_GEN_LIGNITE,
    COL_GEN_NUCLEAR,
    COL_GEN_OIL,
    COL_GEN_OTHER,
    COL_GEN_SOLAR,
    COL_GEN_WIND_OFF,
    COL_GEN_WIND_ON,
    COL_LOAD_TOTAL,
    COL_NET_POSITION,
    COL_PRICE_DA,
    COL_PSH_PUMP,
)
from src.hash_utils import sha256_file
from src.time_utils import annual_utc_index, expected_hours, to_utc_index

RAW_BASE = Path("data/raw/entsoe")
PSR_MAPPING_PATH = Path("data/static/entsoe_psr_mapping.csv")


@dataclass
class FetchResult:
    country: str
    year: int
    entsoe_codes_used: list[str]
    datasets: dict[str, pd.DataFrame]
    meta_entries: list[dict[str, Any]]


def _resolve_api_key() -> str:
    key = os.getenv("ENTSOE_API_KEY")
    if key:
        return key
    env_file_key = dotenv_values(".env").get("ENTSOE_API_KEY")
    if env_file_key:
        return str(env_file_key)
    raise RuntimeError("ENTSOE_API_KEY is required")


def _api_call_with_retry(fn, *args, **kwargs):
    delays = [3, 8, 15]
    attempt = 0
    while True:
        try:
            return fn(*args, **kwargs)
        except Exception:
            if attempt >= len(delays):
                raise
            time.sleep(delays[attempt])
            attempt += 1


def _segment_to_local_ts(segment: dict[str, Any], timezone: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    start = pd.Timestamp(segment["start"]).tz_localize(timezone)
    end = pd.Timestamp(segment["end"]).tz_localize(timezone)
    return start, end


def _raw_path(dataset: str, country: str, year: int) -> Path:
    return RAW_BASE / dataset / country / f"{year}.parquet"


def _meta_path(dataset: str, country: str, year: int) -> Path:
    return RAW_BASE / dataset / country / f"{year}.meta.json"


def _cached_manifest_entries(country: str, year: int) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for dataset in ["load_total", "generation_by_type", "prices_da", "net_position", "psh_pump"]:
        raw_path = _raw_path(dataset, country, year)
        meta_path = _meta_path(dataset, country, year)
        meta: dict[str, Any] = {}
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except Exception:
                meta = {}
        entsoe_codes_used = meta.get("entsoe_codes_used", "")
        if isinstance(entsoe_codes_used, list):
            entsoe_codes_used = ",".join(str(x) for x in entsoe_codes_used)
        entries.append(
            {
                "dataset_name": dataset,
                "country": country,
                "year": year,
                "file_path": str(raw_path),
                "meta_path": str(meta_path),
                "source": meta.get("source", "ENTSO-E API"),
                "download_timestamp_utc": meta.get("download_timestamp_utc", ""),
                "entsoe_codes_used": entsoe_codes_used,
            }
        )
    return entries


def _normalize_index_and_frequency(series_or_df: pd.Series | pd.DataFrame, index_utc: pd.DatetimeIndex) -> tuple[pd.Series | pd.DataFrame, dict[str, Any]]:
    if isinstance(series_or_df, pd.Series):
        s = series_or_df.copy()
        s.index = to_utc_index(pd.DatetimeIndex(s.index))
        duplicate_count = int(s.index.duplicated().sum())
        if duplicate_count:
            s = s.groupby(level=0).mean()
        try:
            freq = pd.infer_freq(s.index)
        except ValueError:
            freq = None
        source_freq = str(freq) if freq is not None else "unknown"
        resampling_applied = False
        method = "none"
        if source_freq in {"15T", "30T", "15min", "30min"}:
            s = s.resample("h").mean()
            resampling_applied = True
            method = "mean_to_hour"
        s = s.reindex(index_utc)
        stats = {
            "source_frequency_detected": source_freq,
            "resampling_applied": resampling_applied,
            "resampling_method": method,
            "duplicate_count": duplicate_count,
            "missing_count": int(s.isna().sum()),
            "missing_share": float(s.isna().mean()),
            "n_rows_after_normalization": int(len(s)),
        }
        return s, stats

    df = series_or_df.copy()
    df.index = to_utc_index(pd.DatetimeIndex(df.index))
    duplicate_count = int(df.index.duplicated().sum())
    if duplicate_count:
        df = df.groupby(level=0).mean()
    try:
        freq = pd.infer_freq(df.index)
    except ValueError:
        freq = None
    source_freq = str(freq) if freq is not None else "unknown"
    resampling_applied = False
    method = "none"
    if source_freq in {"15T", "30T", "15min", "30min"}:
        df = df.resample("h").mean()
        resampling_applied = True
        method = "mean_to_hour"
    df = df.reindex(index_utc)
    stats = {
        "source_frequency_detected": source_freq,
        "resampling_applied": resampling_applied,
        "resampling_method": method,
        "duplicate_count": duplicate_count,
        "missing_count": int(df.isna().any(axis=1).sum()),
        "missing_share": float(df.isna().any(axis=1).mean()),
        "n_rows_after_normalization": int(len(df)),
    }
    return df, stats


def _load_psr_mapping() -> dict[str, str]:
    mapping_df = pd.read_csv(PSR_MAPPING_PATH)
    out = {}
    for _, row in mapping_df.iterrows():
        out[str(row["entsoe_label"]).strip()] = str(row["canonical_column"]).strip()
    return out


def _extract_generation(raw_gen: pd.DataFrame) -> pd.DataFrame:
    mapping = _load_psr_mapping()
    cols = [
        COL_GEN_SOLAR,
        COL_GEN_WIND_ON,
        COL_GEN_WIND_OFF,
        COL_GEN_NUCLEAR,
        COL_GEN_HYDRO_ROR,
        COL_GEN_HYDRO_RES,
        COL_GEN_HYDRO_PSH_GEN,
        COL_PSH_PUMP,
        COL_GEN_BIOMASS,
        COL_GEN_GAS,
        COL_GEN_COAL,
        COL_GEN_LIGNITE,
        COL_GEN_OIL,
        COL_GEN_OTHER,
    ]
    out = pd.DataFrame(index=raw_gen.index)
    for c in cols:
        out[c] = 0.0

    if isinstance(raw_gen.columns, pd.MultiIndex):
        for gen_label, flow_label in raw_gen.columns:
            label = str(gen_label).strip()
            flow = str(flow_label)
            mapped = mapping.get(label)
            if mapped is None:
                mapped = COL_GEN_OTHER

            values = pd.to_numeric(raw_gen[(gen_label, flow_label)], errors="coerce")
            if mapped == "_psh_dispatch":
                flow_l = flow.lower()
                label_l = label.lower()
                # Preferred path: explicit ENTSO-E pumped-storage consumption flow.
                if ("consumption" in flow_l) or ("consumption" in label_l):
                    out[COL_PSH_PUMP] = out[COL_PSH_PUMP].add(values.abs(), fill_value=0.0)
                else:
                    # Fallback path: some zones expose pumping as negative PSH generation.
                    psh_from_negative = (-values.clip(upper=0.0)).fillna(0.0)
                    psh_generation = values.clip(lower=0.0).fillna(0.0)
                    out[COL_PSH_PUMP] = out[COL_PSH_PUMP].add(psh_from_negative, fill_value=0.0)
                    out[COL_GEN_HYDRO_PSH_GEN] = out[COL_GEN_HYDRO_PSH_GEN].add(psh_generation, fill_value=0.0)
                continue

            if "Actual Aggregated" in flow or flow == "Actual":
                out[mapped] = out[mapped].add(values, fill_value=0.0)
    else:
        for c in raw_gen.columns:
            label = str(c)
            mapped = mapping.get(label, COL_GEN_OTHER)
            values = pd.to_numeric(raw_gen[c], errors="coerce")
            if mapped == "_psh_dispatch":
                label_l = label.lower()
                if "consumption" in label_l:
                    out[COL_PSH_PUMP] = out[COL_PSH_PUMP].add(values.abs(), fill_value=0.0)
                else:
                    psh_from_negative = (-values.clip(upper=0.0)).fillna(0.0)
                    psh_generation = values.clip(lower=0.0).fillna(0.0)
                    out[COL_PSH_PUMP] = out[COL_PSH_PUMP].add(psh_from_negative, fill_value=0.0)
                    out[COL_GEN_HYDRO_PSH_GEN] = out[COL_GEN_HYDRO_PSH_GEN].add(psh_generation, fill_value=0.0)
            else:
                out[mapped] = out[mapped].add(values, fill_value=0.0)

    # cleanup negatives
    for c in out.columns:
        s = pd.to_numeric(out[c], errors="coerce")
        s = s.where(~(s < -0.1), np.nan)
        s = s.where(~((s >= -0.1) & (s < 0.0)), 0.0)
        if c == COL_PSH_PUMP:
            s = s.clip(lower=0.0)
        out[c] = s

    return out


def _query_with_segments(client: EntsoePandasClient, method_name: str, segments: list[dict[str, Any]], timezone: str, **kwargs):
    parts = []
    for seg in segments:
        start, end = _segment_to_local_ts(seg, timezone)
        method = getattr(client, method_name)
        data = _api_call_with_retry(method, seg["code"], start=start, end=end, **kwargs)
        if data is None:
            continue
        parts.append(data)
    if not parts:
        return None
    if isinstance(parts[0], pd.Series):
        return pd.concat(parts).sort_index()
    return pd.concat(parts).sort_index()


def _write_dataset(dataset: str, country: str, year: int, data: pd.Series | pd.DataFrame, meta: dict[str, Any]) -> dict[str, Any]:
    path = _raw_path(dataset, country, year)
    meta_path = _meta_path(dataset, country, year)
    path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(data, pd.Series):
        df = data.to_frame(name=data.name or "value")
    else:
        df = data.copy()

    df.to_parquet(path, index=True)
    meta = dict(meta)
    meta["sha256_of_parquet_file"] = sha256_file(path)
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2, default=str)

    return {
        "dataset_name": dataset,
        "country": country,
        "year": year,
        "file_path": str(path),
        "meta_path": str(meta_path),
        "source": "ENTSO-E API",
        "download_timestamp_utc": meta["download_timestamp_utc"],
        "entsoe_codes_used": ",".join(meta["entsoe_codes_used"]),
    }


def fetch_country_year(country: str, year: int, countries_cfg: dict[str, Any], force_refresh: bool = False) -> FetchResult:
    country_cfg = countries_cfg["countries"][country]
    timezone = country_cfg["timezone"]
    segments = resolve_entsoe_segments(country, year, countries_cfg)
    entsoe_codes = sorted({s["code"] for s in segments})

    key = _resolve_api_key()
    client = EntsoePandasClient(api_key=key)
    idx_utc = annual_utc_index(year)

    datasets: dict[str, pd.DataFrame] = {}
    manifest_entries: list[dict[str, Any]] = []

    # load
    load_raw = _query_with_segments(client, "query_load", segments, timezone)
    if isinstance(load_raw, pd.DataFrame):
        candidates = [c for c in load_raw.columns if "Actual Load" in str(c)]
        load_raw = load_raw[candidates[0]] if candidates else load_raw.iloc[:, 0]
    load_norm, load_stats = _normalize_index_and_frequency(load_raw, idx_utc)
    load_norm = pd.to_numeric(load_norm, errors="coerce")
    load_norm = load_norm.where(load_norm >= 0, np.nan)
    load_meta = {
        "dataset_name": "load_total",
        "country": country,
        "year": year,
        "entsoe_codes_used": entsoe_codes,
        "start_utc": str(idx_utc.min()),
        "end_utc": str(idx_utc.max()),
        "download_timestamp_utc": pd.Timestamp.utcnow().isoformat(),
        "n_rows_raw": int(len(load_raw)),
        **load_stats,
    }
    manifest_entries.append(_write_dataset("load_total", country, year, load_norm.rename(COL_LOAD_TOTAL), load_meta))
    datasets["load_total"] = load_norm.to_frame(COL_LOAD_TOTAL)

    # generation
    gen_raw = _query_with_segments(client, "query_generation", segments, timezone, psr_type=None)
    gen_extracted = _extract_generation(gen_raw)
    gen_norm, gen_stats = _normalize_index_and_frequency(gen_extracted, idx_utc)
    gen_meta = {
        "dataset_name": "generation_by_type",
        "country": country,
        "year": year,
        "entsoe_codes_used": entsoe_codes,
        "start_utc": str(idx_utc.min()),
        "end_utc": str(idx_utc.max()),
        "download_timestamp_utc": pd.Timestamp.utcnow().isoformat(),
        "n_rows_raw": int(len(gen_extracted)),
        **gen_stats,
    }
    manifest_entries.append(_write_dataset("generation_by_type", country, year, gen_norm, gen_meta))
    datasets["generation_by_type"] = gen_norm

    # prices
    price_raw = None
    try:
        price_raw = _query_with_segments(client, "query_day_ahead_prices", segments, timezone)
    except Exception:
        if hasattr(client, "query_day_ahead_prices_local"):
            price_raw = _query_with_segments(client, "query_day_ahead_prices_local", segments, timezone)
        else:
            raise

    price_norm, price_stats = _normalize_index_and_frequency(price_raw, idx_utc)
    price_norm = pd.to_numeric(price_norm, errors="coerce")
    price_meta = {
        "dataset_name": "prices_da",
        "country": country,
        "year": year,
        "entsoe_codes_used": entsoe_codes,
        "start_utc": str(idx_utc.min()),
        "end_utc": str(idx_utc.max()),
        "download_timestamp_utc": pd.Timestamp.utcnow().isoformat(),
        "n_rows_raw": int(len(price_raw)),
        **price_stats,
    }
    manifest_entries.append(_write_dataset("prices_da", country, year, price_norm.rename(COL_PRICE_DA), price_meta))
    datasets["prices_da"] = price_norm.to_frame(COL_PRICE_DA)

    # net position (optional)
    net_raw = None
    try:
        net_raw = _query_with_segments(client, "query_net_position", segments, timezone)
    except Exception:
        net_raw = None

    if net_raw is not None and len(net_raw) > 0:
        net_norm, net_stats = _normalize_index_and_frequency(net_raw, idx_utc)
        net_norm = pd.to_numeric(net_norm, errors="coerce")
    else:
        net_norm = pd.Series(np.nan, index=idx_utc)
        net_stats = {
            "source_frequency_detected": "none",
            "resampling_applied": False,
            "resampling_method": "none",
            "duplicate_count": 0,
            "missing_count": int(len(idx_utc)),
            "missing_share": 1.0,
            "n_rows_after_normalization": int(len(idx_utc)),
        }
    net_meta = {
        "dataset_name": "net_position",
        "country": country,
        "year": year,
        "entsoe_codes_used": entsoe_codes,
        "start_utc": str(idx_utc.min()),
        "end_utc": str(idx_utc.max()),
        "download_timestamp_utc": pd.Timestamp.utcnow().isoformat(),
        "n_rows_raw": int(0 if net_raw is None else len(net_raw)),
        **net_stats,
    }
    manifest_entries.append(_write_dataset("net_position", country, year, net_norm.rename(COL_NET_POSITION), net_meta))
    datasets["net_position"] = net_norm.to_frame(COL_NET_POSITION)

    # psh pump (optional extract from generation)
    psh = gen_norm[COL_PSH_PUMP] if COL_PSH_PUMP in gen_norm.columns else pd.Series(np.nan, index=idx_utc)
    psh_meta = {
        "dataset_name": "psh_pump",
        "country": country,
        "year": year,
        "entsoe_codes_used": entsoe_codes,
        "start_utc": str(idx_utc.min()),
        "end_utc": str(idx_utc.max()),
        "download_timestamp_utc": pd.Timestamp.utcnow().isoformat(),
        "n_rows_raw": int(len(psh)),
        "source_frequency_detected": "derived_from_generation",
        "resampling_applied": False,
        "resampling_method": "none",
        "duplicate_count": 0,
        "missing_count": int(psh.isna().sum()),
        "missing_share": float(psh.isna().mean()),
        "n_rows_after_normalization": int(len(psh)),
    }
    manifest_entries.append(_write_dataset("psh_pump", country, year, psh.rename(COL_PSH_PUMP), psh_meta))
    datasets["psh_pump"] = psh.to_frame(COL_PSH_PUMP)

    return FetchResult(
        country=country,
        year=year,
        entsoe_codes_used=entsoe_codes,
        datasets=datasets,
        meta_entries=manifest_entries,
    )


def load_frozen_raw(country: str, year: int) -> dict[str, pd.DataFrame]:
    out = {}
    for dataset in ["load_total", "generation_by_type", "prices_da", "net_position", "psh_pump"]:
        p = _raw_path(dataset, country, year)
        if not p.exists():
            raise FileNotFoundError(f"Missing frozen raw dataset: {p}")
        out[dataset] = pd.read_parquet(p)
    return out


def build_raw_panel(country: str, year: int, use_cache_only: bool = True, countries_cfg: dict[str, Any] | None = None) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    """Return merged raw panel and manifest entries for one country-year."""
    if use_cache_only:
        raw = load_frozen_raw(country, year)
        manifest = _cached_manifest_entries(country, year)
    else:
        if countries_cfg is None:
            raise ValueError("countries_cfg required when use_cache_only=False")
        fetched = fetch_country_year(country, year, countries_cfg)
        raw = fetched.datasets
        manifest = fetched.meta_entries

    idx = annual_utc_index(year)
    panel = pd.DataFrame(index=idx)
    panel.index.name = "timestamp_utc"

    panel = panel.join(raw["load_total"], how="left")
    panel = panel.join(raw["generation_by_type"], how="left")
    panel = panel.join(raw["prices_da"], how="left")
    panel = panel.join(raw["net_position"], how="left")
    if "psh_pump_mw" not in panel.columns:
        panel = panel.join(raw["psh_pump"], how="left")

    # Ensure expected generation columns exist
    for col in [
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
        COL_PSH_PUMP,
    ]:
        if col not in panel.columns:
            panel[col] = np.nan

    panel = panel.sort_index()
    if len(panel) != expected_hours(year):
        # still allowed if index already expected but defensive
        panel = panel.reindex(idx)

    return panel, manifest

