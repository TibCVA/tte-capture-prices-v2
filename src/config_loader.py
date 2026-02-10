"""Configuration helpers."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

COUNTRY_CODE_PERIODS_KEY = "country_code_periods"


def load_yaml(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Missing config file: {p}")
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML root object: {p}")
    return data


def load_countries(path: str = "config/countries.yaml") -> dict[str, Any]:
    data = load_yaml(path)
    countries = data.get("countries")
    if not isinstance(countries, dict) or not countries:
        raise ValueError("config/countries.yaml must contain 'countries' dict")
    return data


def load_thresholds(path: str = "config/thresholds.yaml") -> dict[str, Any]:
    return load_yaml(path)


def load_assumptions(path: str = "data/assumptions/phase1_assumptions.csv") -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Missing assumptions file: {p}")
    df = pd.read_csv(p)
    required = {
        "param_group",
        "param_name",
        "param_value",
        "unit",
        "description",
        "source",
        "last_updated",
        "owner",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Assumptions file missing columns: {sorted(missing)}")
    return df


def load_phase2_assumptions(path: str = "data/assumptions/phase2/phase2_scenario_country_year.csv") -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Missing phase2 assumptions file: {p}")
    df = pd.read_csv(p)
    required = {
        "scenario_id",
        "country",
        "year",
        "demand_total_twh",
        "cap_pv_gw",
        "cap_wind_on_gw",
        "interconnection_export_gw",
        "export_coincidence_factor",
        "bess_power_gw",
        "bess_energy_gwh",
        "co2_eur_per_t",
        "gas_eur_per_mwh_th",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Phase2 assumptions missing columns: {sorted(missing)}")
    return df


def assumptions_to_dict(df: pd.DataFrame) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for _, row in df.iterrows():
        key = str(row["param_name"])
        value = row["param_value"]
        try:
            if isinstance(value, str) and value.strip().lower() in {"true", "false"}:
                out[key] = value.strip().lower() == "true"
            else:
                out[key] = float(value)
                if out[key].is_integer():
                    out[key] = int(out[key])
        except Exception:
            out[key] = value
    return out


def resolve_entsoe_segments(country_key: str, year: int, countries_cfg: dict[str, Any]) -> list[dict[str, Any]]:
    countries = countries_cfg["countries"]
    if country_key not in countries:
        raise KeyError(f"Unknown country: {country_key}")

    start_year = dt.datetime(year, 1, 1)
    end_year = dt.datetime(year + 1, 1, 1)

    periods = countries_cfg.get(COUNTRY_CODE_PERIODS_KEY, {})
    if country_key not in periods:
        return [{"code": countries[country_key]["entsoe_code"], "start": start_year, "end": end_year}]

    segments: list[dict[str, Any]] = []
    for item in periods[country_key]:
        p_start = dt.datetime.fromisoformat(item["start"])
        p_end = dt.datetime.fromisoformat(item["end"]) + dt.timedelta(days=1)
        seg_start = max(start_year, p_start)
        seg_end = min(end_year, p_end)
        if seg_start < seg_end:
            segments.append({"code": item["code"], "start": seg_start, "end": seg_end})

    if not segments:
        segments = [{"code": countries[country_key]["entsoe_code"], "start": start_year, "end": end_year}]

    segments = sorted(segments, key=lambda x: x["start"])
    return segments

