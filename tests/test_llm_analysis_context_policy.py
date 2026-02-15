from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from app import llm_analysis
from app.llm_context_policy import compress_bundle_for_profile, estimate_prompt_tokens_approx


def _bundle_fixture() -> dict:
    hist_rows = [{"country": "DE", "year": 2018 + i, "value": float(i)} for i in range(120)]
    comp_rows = [{"country": "DE", "scenario_id": "DEMAND_UP", "metric": "x", "delta": float(i)} for i in range(120)]
    checks_rows = (
        [{"status": "FAIL", "code": "RC_A", "message": "a"} for _ in range(8)]
        + [{"status": "WARN", "code": "RC_B", "message": "b"} for _ in range(5)]
        + [{"status": "PASS", "code": "RC_C", "message": "c"} for _ in range(20)]
    )
    return {
        "question_id": "Q1",
        "run_id": "RUN_X",
        "business_question": "bq",
        "definitions": ["d1"],
        "selection": {"countries": ["DE", "ES"], "years": list(range(2018, 2025)), "scenario_ids": ["BASE", "DEMAND_UP"]},
        "hist_kpis": {"k": 1.0},
        "hist_tables": {"Q1_country_summary": hist_rows, "Q1_year_panel": hist_rows},
        "scen_tables": {"DEMAND_UP": {"Q1_country_summary": hist_rows}},
        "test_ledger": [{"test_id": f"T{i}", "status": "PASS" if i % 3 else "WARN"} for i in range(150)],
        "test_ledger_summary": {"PASS": 100, "WARN": 50},
        "comparison_hist_vs_scen": comp_rows,
        "checks": checks_rows,
        "warnings": [],
    }


def test_context_policy_compression_is_deterministic_and_profiled() -> None:
    bundle = _bundle_fixture()
    full, full_notes = compress_bundle_for_profile(bundle, "FULL")
    compact, compact_notes = compress_bundle_for_profile(bundle, "COMPACT")
    minimal, minimal_notes = compress_bundle_for_profile(bundle, "MINIMAL")

    assert full["selection"] == bundle["selection"]
    assert full["hist_kpis"] == bundle["hist_kpis"]
    assert int(full["check_counts"]["FAIL"]) == 8
    assert int(full["check_counts"]["WARN"]) == 5
    assert "RC_A (x8)" in full["top_fail_codes"]

    full_hist_rows = len(full["hist_tables"]["Q1_country_summary"]["rows"])
    compact_hist_rows = len(compact["hist_tables"]["Q1_country_summary"]["rows"])
    minimal_hist_rows = len(minimal["hist_tables"]["Q1_country_summary"]["rows"])
    assert full_hist_rows > compact_hist_rows > minimal_hist_rows

    full_comp_rows = len(full["comparison_hist_vs_scen"]["rows"])
    compact_comp_rows = len(compact["comparison_hist_vs_scen"]["rows"])
    minimal_comp_rows = len(minimal["comparison_hist_vs_scen"]["rows"])
    assert full_comp_rows > compact_comp_rows > minimal_comp_rows

    assert any("context_profile=FULL" in note for note in full_notes)
    assert any("context_profile=COMPACT" in note for note in compact_notes)
    assert any("context_profile=MINIMAL" in note for note in minimal_notes)

    est1 = estimate_prompt_tokens_approx("abc", [{"role": "user", "content": "xyz"}])
    est2 = estimate_prompt_tokens_approx("abc", [{"role": "user", "content": "xyz"}])
    assert est1 == est2
    assert est1 > 0


def test_run_llm_analysis_retries_on_context_overflow(monkeypatch, tmp_path: Path) -> None:
    calls = {"n": 0}

    class _FakeResponses:
        def create(self, **kwargs):  # type: ignore[no-untyped-def]
            _ = kwargs
            calls["n"] += 1
            if calls["n"] < 3:
                raise RuntimeError("context_length_exceeded")
            return SimpleNamespace(
                output_text="ok report",
                usage=SimpleNamespace(input_tokens=111, output_tokens=222),
            )

    fake_client = SimpleNamespace(responses=_FakeResponses())
    monkeypatch.setattr(llm_analysis, "get_openai_client", lambda api_key_override=None: fake_client)
    monkeypatch.setattr(llm_analysis, "select_initial_profile", lambda data: "FULL")
    monkeypatch.setattr(llm_analysis, "LLM_REPORTS_DIR", tmp_path)

    report = llm_analysis.run_llm_analysis(
        question_id="Q1",
        bundle_hash="HASH_Q1",
        bundle_data=_bundle_fixture(),
        api_key_override="dummy",
    )
    assert "error" not in report
    assert report["context_profile_used"] == "MINIMAL"
    assert int(report["context_retry_count"]) == 2
    assert int(report["context_estimated_input_tokens"]) > 0
    assert isinstance(report.get("context_compaction_notes"), list)
    assert (tmp_path / "Q1_HASH_Q1.json").exists()


def test_run_llm_analysis_no_retry_for_non_overflow_error(monkeypatch, tmp_path: Path) -> None:
    class _FakeResponses:
        def create(self, **kwargs):  # type: ignore[no-untyped-def]
            _ = kwargs
            raise RuntimeError("network down")

    fake_client = SimpleNamespace(responses=_FakeResponses())
    monkeypatch.setattr(llm_analysis, "get_openai_client", lambda api_key_override=None: fake_client)
    monkeypatch.setattr(llm_analysis, "select_initial_profile", lambda data: "FULL")
    monkeypatch.setattr(llm_analysis, "LLM_REPORTS_DIR", tmp_path)

    report = llm_analysis.run_llm_analysis(
        question_id="Q2",
        bundle_hash="HASH_Q2",
        bundle_data=_bundle_fixture(),
        api_key_override="dummy",
    )
    assert "error" in report
    assert report["context_profile_used"] == "FULL"
    assert int(report["context_retry_count"]) == 0
