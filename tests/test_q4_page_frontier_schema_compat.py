from __future__ import annotations

from pathlib import Path
import runpy

import pandas as pd


def _load_resolver():
    namespace = runpy.run_path(
        str(
            Path(__file__).resolve().parents[1]
            / "app"
            / "pages"
            / "04_Q4_BESS_OrderOfMagnitude.py"
        )
    )
    return namespace["_resolve_frontier_plot_columns"]


def test_resolve_frontier_new_schema_only() -> None:
    resolve = _load_resolver()
    frontier = pd.DataFrame(
        {
            "bess_power_mw_test": ["200", "400"],
            "bess_energy_mwh_test": ["800", "1600"],
            "bess_duration_h_test": ["4", "4"],
            "far_after": ["0.65", "0.70"],
            "surplus_unabs_energy_after": ["1200", "900"],
        }
    )
    normalized, resolved, issues = resolve(frontier)

    assert issues == []
    assert resolved["power"] == "bess_power_mw_test"
    assert resolved["energy"] == "bess_energy_mwh_test"
    assert resolved["duration"] == "bess_duration_h_test"
    assert normalized["bess_power_mw_test"].dtype.kind in "fi"
    assert normalized["bess_energy_mwh_test"].dtype.kind in "fi"
    assert normalized["bess_duration_h_test"].dtype.kind in "fi"


def test_resolve_frontier_legacy_schema_only() -> None:
    resolve = _load_resolver()
    frontier = pd.DataFrame(
        {
            "required_bess_power_mw": [100.0, 300.0],
            "required_bess_energy_mwh": [200.0, 900.0],
            "required_bess_duration_h": [2.0, 3.0],
            "far_after": [0.5, 0.6],
            "surplus_unabs_energy_after": [1500.0, 1100.0],
        }
    )
    _, resolved, issues = resolve(frontier)

    assert issues == []
    assert resolved["power"] == "required_bess_power_mw"
    assert resolved["energy"] == "required_bess_energy_mwh"
    assert resolved["duration"] == "required_bess_duration_h"


def test_resolve_frontier_partial_schema_reports_missing_without_exception() -> None:
    resolve = _load_resolver()
    frontier = pd.DataFrame(
        {
            "bess_power_mw_test": [250.0],
            "bess_energy_mwh_test": [1000.0],
            "far_after": [0.62],
            "surplus_unabs_energy_after": [980.0],
        }
    )
    _, resolved, issues = resolve(frontier)

    assert resolved["power"] == "bess_power_mw_test"
    assert resolved["energy"] == "bess_energy_mwh_test"
    assert "duration" not in resolved
    assert any(item.startswith("duration: colonne manquante") for item in issues)

