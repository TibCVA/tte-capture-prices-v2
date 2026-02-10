from __future__ import annotations

from datetime import datetime, timezone
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config_loader import load_phase2_assumptions
from src.modules.bundle_result import export_question_bundle
from src.modules.question_bundle_runner import run_question_bundle
from src.modules.test_registry import get_default_scenarios
from src.pipeline import load_assumptions_table
from src.storage import load_hourly


def main() -> None:
    countries = ["FR", "DE", "ES", "NL", "BE", "CZ", "IT_NORD"]
    years = list(range(2018, 2025))
    scenario_years = [2030, 2040]

    annual_hist = pd.read_parquet("data/metrics/annual_metrics.parquet")
    assumptions_phase1 = load_assumptions_table()
    assumptions_phase2 = load_phase2_assumptions()

    hourly_map: dict[tuple[str, int], pd.DataFrame] = {}
    for c in countries:
        for y in years:
            try:
                hourly_map[(c, y)] = load_hourly(c, y)
            except Exception:
                continue

    run_id = "FULL_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    selections = {
        "Q1": {
            "countries": countries,
            "years": years,
            "scenario_ids": get_default_scenarios("Q1"),
            "scenario_years": scenario_years,
        },
        "Q2": {
            "countries": countries,
            "years": years,
            "scenario_ids": get_default_scenarios("Q2"),
            "scenario_years": scenario_years,
        },
        "Q3": {
            "countries": countries,
            "years": years,
            "scenario_ids": get_default_scenarios("Q3"),
            "scenario_years": scenario_years,
        },
        "Q4": {
            "country": "FR",
            "year": 2024,
            "countries": countries,
            "years": [2024],
            "scenario_ids": get_default_scenarios("Q4"),
            "scenario_years": [2040],
            "horizon_year": 2040,
            "objective": "FAR_TARGET",
        },
        "Q5": {
            "country": "FR",
            "countries": countries,
            "years": years,
            "scenario_ids": get_default_scenarios("Q5"),
            "scenario_years": scenario_years,
            "marginal_tech": "CCGT",
            "ttl_target_eur_mwh": 120.0,
        },
    }

    for q in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        print(f"RUN {q}")
        result = run_question_bundle(
            question_id=q,
            annual_hist=annual_hist,
            hourly_hist_map=hourly_map,
            assumptions_phase1=assumptions_phase1,
            assumptions_phase2=assumptions_phase2,
            selection=selections[q],
            run_id=run_id,
        )
        out_dir = export_question_bundle(result)
        print(f"EXPORTED {out_dir}")

    print(f"RUN_ID {run_id}")


if __name__ == "__main__":
    main()
