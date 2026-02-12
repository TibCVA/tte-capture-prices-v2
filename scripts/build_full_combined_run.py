from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config_loader import load_countries, load_phase2_assumptions
from src.modules.bundle_result import export_question_bundle
from src.modules.question_bundle_runner import run_question_bundle
from src.modules.test_registry import get_default_scenarios
from src.pipeline import load_assumptions_table
from src.storage import load_hourly, load_scenario_hourly


DEFAULT_COUNTRIES = ["FR", "DE", "ES", "NL", "BE", "CZ", "IT_NORD"]
DEFAULT_SCENARIO_YEARS = list(range(2025, 2036))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a full combined run for Q1..Q5.")
    parser.add_argument("--run-id", default="", help="Optional fixed run id (default: FULL_<utc timestamp>)")
    parser.add_argument("--countries", default=",".join(DEFAULT_COUNTRIES))
    parser.add_argument("--hist-year-start", type=int, default=2018)
    parser.add_argument("--hist-year-end", type=int, default=2024)
    parser.add_argument("--scenario-years", default=",".join([str(y) for y in DEFAULT_SCENARIO_YEARS]))
    parser.add_argument("--q4-countries", default="", help="Comma-separated countries for Q4 (default: all --countries)")
    parser.add_argument("--q5-countries", default="", help="Comma-separated countries for Q5 (default: all --countries)")
    parser.add_argument("--q5-marginal-tech", default="CCGT")
    parser.add_argument("--q5-ttl-target", type=float, default=160.0)
    parser.add_argument("--debug-country", default="", help="Optional country for flex debug export (single country).")
    parser.add_argument("--debug-year", type=int, default=0, help="Optional year for flex debug export.")
    parser.add_argument("--debug-scenario-id", default="HIST", help="Scenario id for debug export (HIST for historical).")
    return parser.parse_args()


def _export_flex_debug(run_id: str, *, country: str, year: int, scenario_id: str = "HIST") -> Path:
    scenario = str(scenario_id or "HIST").upper()
    if scenario == "HIST":
        hourly = load_hourly(country, year)
    else:
        hourly = load_scenario_hourly(scenario, country, year)

    nrl = pd.to_numeric(hourly.get("nrl_mw"), errors="coerce")
    surplus_raw = (
        pd.to_numeric(hourly.get("surplus_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
        if "surplus_mw" in hourly.columns
        else (-nrl).fillna(0.0).clip(lower=0.0)
    )
    export_sink = pd.to_numeric(hourly.get("exports_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
    psh = pd.to_numeric(hourly.get("psh_pump_mw"), errors="coerce").fillna(0.0).clip(lower=0.0)
    sink_non_bess = export_sink + psh
    absorbed_non_bess = np.minimum(surplus_raw, sink_non_bess)
    unabsorbed_surplus = (surplus_raw - absorbed_non_bess).clip(lower=0.0)

    out = pd.DataFrame(
        {
            "timestamp_utc": hourly.index,
            "net_position_mw": pd.to_numeric(hourly.get("net_position_mw"), errors="coerce"),
            "export_sink_mw": export_sink,
            "surplus_raw_mw": surplus_raw,
            "psh_pumping_mw": psh,
            "sink_non_bess_mw": sink_non_bess,
            "unabsorbed_surplus_mw": unabsorbed_surplus,
        }
    )
    debug_dir = Path("outputs/combined") / run_id / "debug"
    debug_dir.mkdir(parents=True, exist_ok=True)
    out_path = debug_dir / f"flex_debug_{country}_{year}_{scenario}.csv"
    out.to_csv(out_path, index=False)
    return out_path


def main() -> None:
    args = _parse_args()
    countries = [c.strip() for c in str(args.countries).split(",") if c.strip()]
    q4_countries = [c.strip() for c in str(args.q4_countries).split(",") if c.strip()] or countries
    q5_countries = [c.strip() for c in str(args.q5_countries).split(",") if c.strip()] or countries
    hist_years = list(range(int(args.hist_year_start), int(args.hist_year_end) + 1))
    scenario_years = [int(y.strip()) for y in str(args.scenario_years).split(",") if y.strip()]

    annual_path = Path("data/metrics/annual_metrics.parquet")
    if not annual_path.exists():
        raise FileNotFoundError(f"Missing historical annual metrics: {annual_path}")
    annual_hist = pd.read_parquet(annual_path)
    validation_findings_path = Path("data/metrics/validation_findings.parquet")
    validation_findings_hist = pd.read_parquet(validation_findings_path) if validation_findings_path.exists() else pd.DataFrame()
    assumptions_phase1 = load_assumptions_table()
    assumptions_phase2 = load_phase2_assumptions()
    countries_cfg = load_countries().get("countries", {})

    hourly_hist_map: dict[tuple[str, int], pd.DataFrame] = {}
    for country in countries:
        for year in hist_years:
            try:
                hourly_hist_map[(country, year)] = load_hourly(country, year)
            except Exception:
                continue

    run_id = args.run_id.strip() or f"FULL_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"

    selections = {
        "Q1": {
            "countries": countries,
            "years": hist_years,
            "scenario_ids": get_default_scenarios("Q1"),
            "scenario_years": scenario_years,
        },
        "Q2": {
            "countries": countries,
            "years": hist_years,
            "scenario_ids": get_default_scenarios("Q2"),
            "scenario_years": scenario_years,
        },
        "Q3": {
            "countries": countries,
            "years": hist_years,
            "scenario_ids": get_default_scenarios("Q3"),
            "scenario_years": scenario_years,
        },
        "Q4": {
            "country": str(q4_countries[0]),
            "countries": q4_countries,
            "year": int(args.hist_year_end),
            "years": [int(args.hist_year_end)],
            "horizon_year": max(scenario_years),
            "objective": "LOW_PRICE_TARGET",
            "force_recompute": True,
            "power_grid": [0.0, 250.0, 500.0, 750.0, 1000.0, 1500.0],
            "duration_grid": [2.0, 4.0, 6.0, 8.0],
            "scenario_ids": get_default_scenarios("Q4"),
            "scenario_years": scenario_years,
        },
        "Q5": {
            "country": str(q5_countries[0]),
            "countries": q5_countries,
            "years": hist_years,
            "marginal_tech": str(args.q5_marginal_tech),
            "marginal_tech_by_country": {
                c: str(countries_cfg.get(c, {}).get("thermal", {}).get("marginal_tech", args.q5_marginal_tech)).upper()
                for c in q5_countries
            },
            "ttl_target_eur_mwh": float(args.q5_ttl_target),
            "scenario_ids": get_default_scenarios("Q5"),
            "scenario_years": scenario_years,
        },
    }

    for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        bundle = run_question_bundle(
            question_id=qid,
            annual_hist=annual_hist,
            hourly_hist_map=hourly_hist_map,
            assumptions_phase1=assumptions_phase1,
            assumptions_phase2=assumptions_phase2,
            selection=selections[qid],
            run_id=run_id,
            validation_findings_hist=validation_findings_hist,
        )
        export_question_bundle(bundle)
        status_counts = bundle.test_ledger["status"].astype(str).value_counts().to_dict() if not bundle.test_ledger.empty else {}
        print(f"{qid}: {status_counts}")

    debug_country = str(args.debug_country).strip().upper()
    debug_year = int(args.debug_year) if int(args.debug_year) > 0 else 0
    if debug_country and debug_year:
        try:
            debug_path = _export_flex_debug(
                run_id=run_id,
                country=debug_country,
                year=debug_year,
                scenario_id=str(args.debug_scenario_id),
            )
            print(f"FLEX_DEBUG {debug_path}")
        except Exception as exc:
            print(f"FLEX_DEBUG_ERROR country={debug_country} year={debug_year}: {exc}")

    print(f"RUN_ID {run_id}")


if __name__ == "__main__":
    main()
