"""Bundle result contract for unified HIST+SCEN question runs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

import numpy as np
import pandas as pd

from src.modules.result import ModuleResult


@dataclass
class QuestionBundleResult:
    question_id: str
    run_id: str
    selection: dict[str, Any]
    hist_result: ModuleResult
    scen_results: dict[str, ModuleResult]
    test_ledger: pd.DataFrame
    comparison_table: pd.DataFrame
    checks: list[dict[str, Any]]
    warnings: list[str]
    narrative_md: str

    def to_summary(self) -> dict[str, Any]:
        return {
            "question_id": self.question_id,
            "run_id": self.run_id,
            "selection": self.selection,
            "hist_module_id": self.hist_result.module_id,
            "scenarios": sorted(self.scen_results.keys()),
            "n_checks": len(self.checks),
            "n_warnings": len(self.warnings),
            "n_test_rows": int(len(self.test_ledger)),
            "n_compare_rows": int(len(self.comparison_table)),
            "checks": self.checks,
            "warnings": self.warnings,
        }


def _export_module_into_dir(module_result: ModuleResult, out_dir: Path) -> None:
    tables_dir = out_dir / "tables"
    figures_dir = out_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    for name, df in module_result.tables.items():
        out_df = df.replace("", np.nan)
        out_df.to_csv(tables_dir / f"{name}.csv", index=False, na_rep="NaN")

    (out_dir / "narrative.md").write_text(module_result.narrative_md, encoding="utf-8")
    with (out_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(module_result.to_summary(), f, ensure_ascii=False, indent=2, default=str)


def export_question_bundle(result: QuestionBundleResult, base_dir: str = "outputs/combined") -> Path:
    root = Path(base_dir) / result.run_id / result.question_id.upper()
    root.mkdir(parents=True, exist_ok=True)

    _export_module_into_dir(result.hist_result, root / "hist")
    for scenario_id, scen_result in result.scen_results.items():
        _export_module_into_dir(scen_result, root / "scen" / str(scenario_id))

    result.test_ledger.replace("", np.nan).to_csv(root / "test_ledger.csv", index=False, na_rep="NaN")
    result.comparison_table.replace("", np.nan).to_csv(
        root / "comparison_hist_vs_scen.csv",
        index=False,
        na_rep="NaN",
    )
    (root / "narrative.md").write_text(result.narrative_md, encoding="utf-8")

    with (root / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(result.to_summary(), f, ensure_ascii=False, indent=2, default=str)

    return root
