from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.config_loader import load_countries, load_assumptions
from src.pipeline import build_country_year
from src.modules.q1_transition import run_q1
from src.modules.q2_slope import run_q2
from src.modules.q3_exit import run_q3
from src.modules.q4_bess import run_q4
from src.modules.q5_thermal_anchor import run_q5, load_commodity_daily
from src.modules.result import export_module_result
from src.storage import load_hourly


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--countries", nargs="*", default=None)
    parser.add_argument("--years", nargs="*", type=int, default=None)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    cfg = load_countries()
    countries = args.countries or sorted(cfg["countries"].keys())
    years = args.years or list(range(2018, 2025))

    for c in countries:
        for y in years:
            print(f"Building {c} {y} ...")
            try:
                res = build_country_year(c, y, force_refresh=args.refresh, use_cache_only=not args.refresh)
                if res["hard_error_count"] > 0:
                    print(f"WARN {c} {y}: {res['hard_error_count']} hard errors")
            except Exception as exc:
                print(f"ERROR {c} {y}: {exc}")

    annual_path = Path("data/metrics/annual_metrics.parquet")
    if not annual_path.exists():
        print("No annual metrics found.")
        return

    annual = pd.read_parquet(annual_path)
    assumptions = load_assumptions()
    run_id = pd.Timestamp.utcnow().strftime("%Y%m%d_%H%M%S")

    q1 = run_q1(annual, assumptions, {"countries": countries, "years": years}, run_id)
    export_module_result(q1)
    q2 = run_q2(annual, assumptions, {"countries": countries}, run_id)
    export_module_result(q2)

    hourly_map = {}
    for _, row in annual[annual["country"].isin(countries) & annual["year"].isin(years)].iterrows():
        c = row["country"]
        y = int(row["year"])
        try:
            hourly_map[(c, y)] = load_hourly(c, y)
        except Exception:
            continue

    q3 = run_q3(annual, hourly_map, assumptions, {"countries": countries, "years": years}, run_id)
    export_module_result(q3)

    # Q4/Q5 on first available country-year
    if hourly_map:
        (c0, y0), h0 = next(iter(hourly_map.items()))
        q4 = run_q4(h0, assumptions, {"country": c0, "year": y0}, run_id)
        export_module_result(q4)
        q5 = run_q5(h0, assumptions, {"country": c0, "year": y0, "marginal_tech": cfg["countries"][c0]["thermal"]["marginal_tech"]}, run_id, commodity_daily=load_commodity_daily())
        export_module_result(q5)

    print(f"Completed run_id={run_id}")


if __name__ == "__main__":
    main()
