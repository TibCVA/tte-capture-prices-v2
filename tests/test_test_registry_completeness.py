from __future__ import annotations

from src.modules.test_registry import all_tests, get_default_scenarios


def test_registry_has_unique_test_ids() -> None:
    tests = all_tests()
    ids = [t.test_id for t in tests]
    assert len(ids) == len(set(ids))


def test_registry_covers_hist_and_scen_for_each_question() -> None:
    tests = all_tests()
    by_q = {}
    for t in tests:
        by_q.setdefault(t.question_id, set()).add(t.mode)
    for q in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        assert q in by_q
        assert "HIST" in by_q[q]
        assert "SCEN" in by_q[q]


def test_default_scenarios_defined_for_each_question() -> None:
    for q in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        scenarios = get_default_scenarios(q)
        assert isinstance(scenarios, list)
        assert len(scenarios) >= 1
