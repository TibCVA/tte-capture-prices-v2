from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def test_generate_extrait_writes_structured_xlsx(monkeypatch, tmp_path: Path) -> None:
    from scripts import generate_extrait_data_outil_v7 as mod

    run_id = "RUN_EXTRACT_XLSX"
    run_q1 = tmp_path / "outputs" / "combined" / run_id / "Q1"
    run_q1.mkdir(parents=True, exist_ok=True)
    (run_q1 / "summary.json").write_text(
        json.dumps(
            {
                "selection": {"years": [2024], "scenario_years": [2030], "scenario_ids": ["BASE"]},
                "checks": [],
            }
        ),
        encoding="utf-8",
    )

    sample_two_rows = pd.DataFrame([{"country": "DE", "year": 2024}, {"country": "ES", "year": 2024}])
    sample_test_ledger = pd.DataFrame([{"test_id": "Q1-H-01", "status": "PASS"}])

    monkeypatch.setattr(mod, "_country_timezones", lambda: {"DE": "Europe/Berlin", "ES": "Europe/Madrid"})
    monkeypatch.setattr(mod, "_extract_annual_metrics_phase1", lambda *args, **kwargs: sample_two_rows)
    monkeypatch.setattr(mod, "_extract_q1_transition_summary", lambda *args, **kwargs: sample_two_rows)
    monkeypatch.setattr(mod, "_extract_q2_slope_summary", lambda *args, **kwargs: sample_two_rows)
    monkeypatch.setattr(mod, "_extract_q3_inversion_requirements", lambda *args, **kwargs: sample_two_rows)
    monkeypatch.setattr(mod, "_extract_q4_bess_sizing_curve", lambda *args, **kwargs: sample_two_rows)
    monkeypatch.setattr(mod, "_extract_q5_anchor_sensitivity", lambda *args, **kwargs: sample_two_rows)
    monkeypatch.setattr(mod, "_build_test_ledger", lambda *args, **kwargs: sample_test_ledger)

    def fake_read_csv(path: Path, label: str) -> pd.DataFrame:  # noqa: ARG001
        if label == "phase1_assumptions":
            return pd.DataFrame([{"param_name": "q1_persistence_window_years", "param_value": 3}])
        if label == "phase2_scenario_country_year":
            return pd.DataFrame([{"country": "DE", "scenario_id": "BASE", "year": 2030}])
        return pd.DataFrame()

    monkeypatch.setattr(mod, "_read_csv", fake_read_csv)

    output_md = tmp_path / "reports" / "extrait.md"
    output_docx = tmp_path / "reports" / "extrait.docx"
    output_xlsx = tmp_path / "reports" / "results.xlsx"
    result = mod.generate_extrait(
        run_id=run_id,
        countries=["DE", "ES"],
        output_docx=output_docx,
        output_md=output_md,
        output_xlsx=output_xlsx,
        generate_docx=False,
        combined_base_dir=tmp_path / "outputs" / "combined",
    )

    assert output_xlsx.exists()
    workbook = pd.ExcelFile(output_xlsx)
    expected = {
        "A1_annual_metrics",
        "Q1_transition",
        "Q2_slope",
        "Q3_inversion",
        "Q4_bess",
        "Q5_anchor",
        "test_ledger",
    }
    assert expected.issubset(set(workbook.sheet_names))
    assert result["output_xlsx"] == str(output_xlsx)

