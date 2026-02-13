from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

import scripts.generate_extrait_data_outil_v7 as extrait


def _tiny_df(name: str) -> pd.DataFrame:
    return pd.DataFrame([{f"{name}_col": "x"}])


def test_generate_extrait_markdown_only_mode(tmp_path: Path, monkeypatch) -> None:
    run_id = "RUN_MD_ONLY"
    run_dir = tmp_path / "outputs" / "combined" / run_id / "Q1"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "summary.json").write_text(
        json.dumps(
            {
                "selection": {
                    "years": [2018, 2019, 2020],
                    "scenario_years": [2025, 2026],
                    "scenario_ids": ["BASE", "DEMAND_UP"],
                }
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    assumptions_dir = tmp_path / "data" / "assumptions"
    phase2_dir = assumptions_dir / "phase2"
    phase2_dir.mkdir(parents=True, exist_ok=True)
    (assumptions_dir / "phase1_assumptions.csv").write_text("param_name,param_value\nx,1\n", encoding="utf-8")
    (phase2_dir / "phase2_scenario_country_year.csv").write_text(
        "scenario_id,country,year\nBASE,DE,2025\nBASE,ES,2025\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(extrait, "ROOT", tmp_path)
    monkeypatch.setattr(extrait, "_extract_annual_metrics_phase1", lambda *args, **kwargs: _tiny_df("annual"))
    monkeypatch.setattr(extrait, "_extract_q1_transition_summary", lambda *args, **kwargs: _tiny_df("q1"))
    monkeypatch.setattr(extrait, "_extract_q2_slope_summary", lambda *args, **kwargs: _tiny_df("q2"))
    monkeypatch.setattr(extrait, "_extract_q3_inversion_requirements", lambda *args, **kwargs: _tiny_df("q3"))
    monkeypatch.setattr(extrait, "_extract_q4_bess_sizing_curve", lambda *args, **kwargs: _tiny_df("q4"))
    monkeypatch.setattr(extrait, "_extract_q5_anchor_sensitivity", lambda *args, **kwargs: _tiny_df("q5"))
    monkeypatch.setattr(extrait, "_build_test_ledger", lambda *args, **kwargs: _tiny_df("ledger"))
    monkeypatch.setattr(extrait, "_country_timezones", lambda: {"DE": "Europe/Berlin", "ES": "Europe/Madrid"})

    output_docx = tmp_path / "reports" / "x.docx"
    output_md = tmp_path / "reports" / "x.md"
    result = extrait.generate_extrait(
        run_id=run_id,
        countries=["DE", "ES"],
        output_docx=output_docx,
        output_md=output_md,
        generate_docx=False,
    )

    assert output_md.exists()
    assert not output_docx.exists()
    assert result["docx_generated"] is False
    content = output_md.read_text(encoding="utf-8")
    assert "# Extrait Data Outil v7" in content

