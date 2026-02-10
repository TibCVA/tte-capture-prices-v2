"""End-to-end pipeline for one country-year."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.config_loader import load_assumptions, load_countries, load_thresholds
from src.data_fetcher import build_raw_panel, fetch_country_year
from src.hash_utils import hash_object
from src.metrics import compute_annual_metrics, compute_daily_metrics
from src.processing import build_hourly_table
from src.run_audit import create_run_context, write_data_manifest
from src.storage import save_annual_metrics_row, save_daily_metrics, save_hourly, save_validation_findings
from src.validation_report import build_validation_report


def build_country_year(
    country: str,
    year: int,
    force_refresh: bool = False,
    use_cache_only: bool = True,
) -> dict[str, Any]:
    countries_cfg = load_countries()
    thresholds_cfg = load_thresholds()
    use_cache_effective = bool(use_cache_only and not force_refresh)
    config_snapshot = {
        "country": country,
        "year": year,
        "force_refresh": bool(force_refresh),
        "use_cache_only": use_cache_effective,
        "country_config": countries_cfg.get("countries", {}).get(country, {}),
        "thresholds": thresholds_cfg,
        "assumptions_phase1_path": "data/assumptions/phase1_assumptions.csv",
    }
    run_ctx = create_run_context(config_snapshot)

    if force_refresh:
        fetch_country_year(country, year, countries_cfg, force_refresh=True)

    raw_panel, manifest_entries = build_raw_panel(
        country=country,
        year=year,
        use_cache_only=use_cache_effective,
        countries_cfg=None if use_cache_effective else countries_cfg,
    )

    entsoe_codes = countries_cfg.get("country_code_periods", {}).get(country)
    if entsoe_codes:
        entsoe_code_used = ",".join(sorted({x["code"] for x in entsoe_codes}))
    else:
        entsoe_code_used = countries_cfg["countries"][country]["entsoe_code"]

    hourly = build_hourly_table(
        raw_panel=raw_panel,
        country=country,
        year=year,
        country_cfg=countries_cfg["countries"][country],
        thresholds_cfg=thresholds_cfg,
        entsoe_code_used=entsoe_code_used,
    )

    data_version_hash = hash_object({"country": country, "year": year, "rows": int(len(hourly)), "manifest_entries": manifest_entries})
    annual = compute_annual_metrics(hourly, countries_cfg["countries"][country], data_version_hash=data_version_hash)
    daily = compute_daily_metrics(hourly, timezone=countries_cfg["countries"][country]["timezone"])

    findings = build_validation_report(hourly, annual)
    findings_df = pd.DataFrame(findings)
    findings_df["country"] = country
    findings_df["year"] = year

    hourly_path = save_hourly(hourly, country, year)
    annual_path = save_annual_metrics_row(annual)
    daily_path = save_daily_metrics(daily)
    findings_path = save_validation_findings(findings_df)

    hard_errors = findings_df[findings_df["severity"] == "ERROR"]
    now_iso = pd.Timestamp.utcnow().isoformat()
    manifest_entries_extended = list(manifest_entries) + [
        {
            "dataset_name": "processed_hourly",
            "country": country,
            "year": year,
            "file_path": str(hourly_path),
            "source": "internal_pipeline",
            "download_timestamp_utc": now_iso,
        },
        {
            "dataset_name": "annual_metrics",
            "country": country,
            "year": year,
            "file_path": str(annual_path),
            "source": "internal_pipeline",
            "download_timestamp_utc": now_iso,
        },
        {
            "dataset_name": "daily_metrics",
            "country": country,
            "year": year,
            "file_path": str(daily_path),
            "source": "internal_pipeline",
            "download_timestamp_utc": now_iso,
        },
        {
            "dataset_name": "validation_findings",
            "country": country,
            "year": year,
            "file_path": str(findings_path),
            "source": "internal_pipeline",
            "download_timestamp_utc": now_iso,
        },
    ]
    manifest_path = write_data_manifest(run_ctx, manifest_entries_extended)

    return {
        "country": country,
        "year": year,
        "run_id": run_ctx.run_id,
        "run_dir": str(run_ctx.run_dir),
        "run_config_snapshot_path": str(run_ctx.run_dir / "run_config_snapshot.json"),
        "data_manifest_path": str(manifest_path),
        "hourly_path": str(hourly_path),
        "annual_path": str(annual_path),
        "daily_path": str(daily_path),
        "findings_path": str(findings_path),
        "hard_error_count": int(len(hard_errors)),
        "manifest_entries": manifest_entries_extended,
        "annual_row": annual,
    }


def load_assumptions_table() -> pd.DataFrame:
    return load_assumptions()

