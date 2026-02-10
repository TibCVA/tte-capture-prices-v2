from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.scenario.trajectory import expand_phase2_trajectory


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Expand phase2 assumptions to explicit annual trajectory rows.")
    parser.add_argument(
        "--input",
        default="data/assumptions/phase2/phase2_scenario_country_year.csv",
        help="Input phase2 assumptions CSV.",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Output CSV path. Defaults to --input (in-place).",
    )
    parser.add_argument("--start-year", type=int, default=2025)
    parser.add_argument("--end-year", type=int, default=2039)
    parser.add_argument("--anchor-start-year", type=int, default=2030)
    parser.add_argument("--anchor-end-year", type=int, default=2040)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    output_path = Path(args.output) if str(args.output).strip() else input_path

    df = pd.read_csv(input_path)
    expanded = expand_phase2_trajectory(
        df,
        start_year=int(args.start_year),
        end_year=int(args.end_year),
        anchor_start_year=int(args.anchor_start_year),
        anchor_end_year=int(args.anchor_end_year),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    expanded.to_csv(output_path, index=False)

    n_in = int(len(df))
    n_out = int(len(expanded))
    years = sorted(pd.to_numeric(expanded.get("year"), errors="coerce").dropna().astype(int).unique().tolist())
    print(f"phase2_trajectory_expanded input_rows={n_in} output_rows={n_out} years={years[:3]}...{years[-3:] if years else []}")
    print(str(output_path))


if __name__ == "__main__":
    main()
