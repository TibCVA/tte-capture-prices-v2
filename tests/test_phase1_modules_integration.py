from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.modules.q1_transition import run_q1
from src.modules.q2_slope import run_q2
from src.modules.q3_exit import run_q3
from src.modules.q4_bess import run_q4
from src.modules.q5_thermal_anchor import run_q5
from src.modules.result import export_module_result
from src.processing import build_hourly_table


def _assert_export_pack(base: Path, run_id: str, module_id: str) -> None:
    module_dir = base / run_id / module_id
    assert (module_dir / "summary.json").exists()
    assert (module_dir / "narrative.md").exists()
    assert (module_dir / "tables").exists()
    assert any((module_dir / "tables").glob("*.csv"))


def test_phase1_modules_integration(annual_panel_fixture, make_raw_panel, countries_cfg, thresholds_cfg, tmp_path):
    assumptions = pd.read_csv("data/assumptions/phase1_assumptions.csv")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    q1 = run_q1(annual_panel_fixture, assumptions, {"countries": ["FR", "DE"], "years": [2021, 2022, 2023, 2024]}, run_id)
    assert q1.module_id == "Q1"
    export_module_result(q1, base_dir=str(tmp_path))

    q2 = run_q2(annual_panel_fixture, assumptions, {"countries": ["FR", "DE"]}, run_id)
    assert q2.module_id == "Q2"
    export_module_result(q2, base_dir=str(tmp_path))

    raw = make_raw_panel(n=240)
    hourly = build_hourly_table(raw, "FR", 2024, countries_cfg["countries"]["FR"], thresholds_cfg, "FR")
    hourly_map = {("FR", 2024): hourly}

    panel = annual_panel_fixture.copy()
    q3 = run_q3(panel, hourly_map, assumptions, {"countries": ["FR"], "years": [2021, 2022, 2023, 2024]}, run_id)
    assert q3.module_id == "Q3"
    export_module_result(q3, base_dir=str(tmp_path))

    q4 = run_q4(hourly, assumptions, {"country": "FR", "year": 2024, "objective": "FAR_TARGET"}, run_id)
    assert q4.module_id == "Q4"
    export_module_result(q4, base_dir=str(tmp_path))

    commodity = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "gas_price_eur_mwh_th": 35.0,
            "co2_price_eur_t": 80.0,
        }
    )
    q5 = run_q5(hourly, assumptions, {"country": "FR", "year": 2024, "marginal_tech": "CCGT"}, run_id, commodity_daily=commodity)
    assert q5.module_id == "Q5"
    export_module_result(q5, base_dir=str(tmp_path))

    for module_id in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        _assert_export_pack(tmp_path, run_id, module_id)

    for module in [q1, q2, q3, q4, q5]:
        assert isinstance(module.checks, list)
        assert module.tables
