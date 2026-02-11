from __future__ import annotations

import pandas as pd

from app import llm_batch


def _annual_hist_fixture() -> pd.DataFrame:
    rows = []
    for country in ["FR", "DE"]:
        for year in range(2018, 2025):
            rows.append({"country": country, "year": year})
    return pd.DataFrame(rows)


def _phase2_fixture() -> pd.DataFrame:
    scenarios = ["BASE", "DEMAND_UP", "FLEX_UP", "LOW_RIGIDITY", "HIGH_CO2", "HIGH_GAS", "HIGH_BOTH"]
    rows = []
    for scenario_id in scenarios:
        for country in ["FR", "DE"]:
            for year in [2025, 2030, 2035]:
                rows.append({"scenario_id": scenario_id, "country": country, "year": year})
    return pd.DataFrame(rows)


def test_build_default_selection_contract_q1_to_q5() -> None:
    annual_hist = _annual_hist_fixture()
    assumptions_phase2 = _phase2_fixture()
    countries_cfg = {
        "countries": {
            "FR": {"thermal": {"marginal_tech": "COAL"}},
            "DE": {"thermal": {"marginal_tech": "CCGT"}},
        }
    }

    q1 = llm_batch.build_default_selection("Q1", annual_hist, assumptions_phase2, countries_cfg)
    assert q1["countries"] == ["DE", "FR"]
    assert q1["years"] == list(range(2018, 2025))
    assert q1["scenario_ids"] == ["BASE", "DEMAND_UP", "FLEX_UP", "LOW_RIGIDITY"]
    assert q1["scenario_years"] == [2025, 2030, 2035]

    q2 = llm_batch.build_default_selection("Q2", annual_hist, assumptions_phase2, countries_cfg)
    assert q2["years"] == list(range(2018, 2025))
    assert q2["scenario_ids"] == ["BASE", "HIGH_CO2", "HIGH_GAS"]

    q3 = llm_batch.build_default_selection("Q3", annual_hist, assumptions_phase2, countries_cfg)
    assert q3["scenario_ids"] == ["BASE", "DEMAND_UP", "FLEX_UP", "LOW_RIGIDITY"]

    q4 = llm_batch.build_default_selection("Q4", annual_hist, assumptions_phase2, countries_cfg)
    assert q4["country"] == "FR"
    assert q4["countries"] == ["FR"]
    assert q4["year"] == 2024
    assert q4["years"] == [2024]
    assert q4["objective"] == "FAR_TARGET"
    assert q4["scenario_ids"] == ["BASE", "FLEX_UP", "HIGH_CO2", "HIGH_GAS"]
    assert q4["scenario_years"] == [2035]

    q5 = llm_batch.build_default_selection("Q5", annual_hist, assumptions_phase2, countries_cfg)
    assert q5["countries"] == ["FR"]
    assert q5["years"] == list(range(2021, 2025))
    assert q5["scenario_ids"] == ["BASE", "HIGH_CO2", "HIGH_GAS", "HIGH_BOTH"]
    assert q5["scenario_years"] == [2025, 2030, 2035]
    assert q5["marginal_tech"] == "CCGT"
    assert q5["marginal_tech_by_country"] == {"FR": "COAL"}
    assert q5["ttl_target_eur_mwh"] == 120.0


def test_run_parallel_llm_generation_handles_partial_failures(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(llm_batch, "LLM_REPORTS_DIR", tmp_path)

    called: list[str] = []

    def _fake_run(question_id: str, bundle_hash: str, bundle_data: dict, api_key_override: str | None = None) -> dict:
        called.append(question_id)
        if question_id == "Q1":
            (tmp_path / f"{question_id}_{bundle_hash}.json").write_text("{}", encoding="utf-8")
            return {"tokens_input": 11, "tokens_output": 22}
        if question_id == "Q2":
            return {"error": "api boom"}
        raise RuntimeError("unexpected question")

    monkeypatch.setattr(llm_batch, "run_llm_analysis", _fake_run)

    prepared_items = [
        {"question_id": "Q1", "bundle_hash": "hash_q1", "bundle_data": {"x": 1}},
        {"question_id": "Q2", "bundle_hash": "hash_q2", "bundle_data": {"x": 2}},
        {"question_id": "Q3", "status": "FAILED_PREP", "bundle_hash": "", "error": "prep failed"},
    ]

    rows = llm_batch.run_parallel_llm_generation(prepared_items=prepared_items, api_key="dummy", max_workers=2)
    by_q = {row["question_id"]: row for row in rows}

    assert by_q["Q1"]["status"] == "OK"
    assert by_q["Q1"]["tokens_input"] == 11
    assert by_q["Q1"]["tokens_output"] == 22
    assert by_q["Q1"]["report_file"] is not None

    assert by_q["Q2"]["status"] == "FAILED_LLM"
    assert "api boom" in by_q["Q2"]["error"]

    assert by_q["Q3"]["status"] == "FAILED_PREP"
    assert "prep failed" in by_q["Q3"]["error"]
    assert set(called) == {"Q1", "Q2"}
