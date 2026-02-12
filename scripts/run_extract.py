from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reproduce a full combined run, snapshot previous outputs in before_fix/, then regenerate Extrait Data Outil v7."
    )
    parser.add_argument("--run-id", required=True, help="Combined run id under outputs/combined/<run_id>.")
    parser.add_argument("--countries", default="FR,DE,ES,NL,BE,CZ,IT_NORD")
    parser.add_argument("--hist-year-start", type=int, default=2018)
    parser.add_argument("--hist-year-end", type=int, default=2024)
    parser.add_argument("--scenario-years", default="2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035")
    parser.add_argument("--q4-countries", default="")
    parser.add_argument("--q5-countries", default="")
    parser.add_argument("--q5-marginal-tech", default="CCGT")
    parser.add_argument("--q5-ttl-target", type=float, default=160.0)
    parser.add_argument("--debug-country", default="")
    parser.add_argument("--debug-year", type=int, default=0)
    parser.add_argument("--debug-scenario-id", default="HIST")
    return parser.parse_args()


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    args = _parse_args()
    run_id = str(args.run_id).strip()
    if not run_id:
        raise ValueError("run_id is required and must be non-empty.")

    run_dir = ROOT / "outputs" / "combined" / run_id
    before_fix_root = ROOT / "outputs" / "combined" / "before_fix"
    before_fix_root.mkdir(parents=True, exist_ok=True)

    if run_dir.exists():
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        before_fix_dir = before_fix_root / f"{run_id}_{ts}"
        shutil.copytree(run_dir, before_fix_dir)
        print(f"[before_fix] Snapshot saved: {before_fix_dir}")
    else:
        print(f"[before_fix] No existing run to snapshot for run_id={run_id}")

    build_cmd = [
        sys.executable,
        "scripts/build_full_combined_run.py",
        "--run-id",
        run_id,
        "--countries",
        str(args.countries),
        "--hist-year-start",
        str(args.hist_year_start),
        "--hist-year-end",
        str(args.hist_year_end),
        "--scenario-years",
        str(args.scenario_years),
        "--q5-marginal-tech",
        str(args.q5_marginal_tech),
        "--q5-ttl-target",
        str(args.q5_ttl_target),
    ]
    if str(args.q4_countries).strip():
        build_cmd.extend(["--q4-countries", str(args.q4_countries)])
    if str(args.q5_countries).strip():
        build_cmd.extend(["--q5-countries", str(args.q5_countries)])
    if str(args.debug_country).strip() and int(args.debug_year) > 0:
        build_cmd.extend(
            [
                "--debug-country",
                str(args.debug_country),
                "--debug-year",
                str(int(args.debug_year)),
                "--debug-scenario-id",
                str(args.debug_scenario_id),
            ]
        )

    _run(build_cmd)

    _run(
        [
            sys.executable,
            "scripts/generate_extrait_data_outil_v7.py",
            "--run-id",
            run_id,
            "--countries",
            str(args.countries),
        ]
    )

    print(f"[done] Combined run rebuilt: {run_dir}")
    print(f"[done] Report markdown: {ROOT / 'reports' / 'Extrait Data Outil v7.md'}")
    print(f"[done] Report docx: {ROOT / 'reports' / 'Extrait Data Outil v7.docx'}")


if __name__ == "__main__":
    main()
