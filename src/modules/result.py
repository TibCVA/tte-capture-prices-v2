"""Standard module output contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class ModuleResult:
    module_id: str
    run_id: str
    selection: dict[str, Any]
    assumptions_used: list[dict[str, Any]]
    kpis: dict[str, Any]
    tables: dict[str, pd.DataFrame]
    figures: list[str]
    narrative_md: str
    checks: list[dict[str, Any]]
    warnings: list[str]
    mode: str = "HIST"
    scenario_id: str | None = None
    horizon_year: int | None = None

    def to_summary(self) -> dict[str, Any]:
        return {
            "module_id": self.module_id,
            "run_id": self.run_id,
            "selection": self.selection,
            "assumptions_used": self.assumptions_used,
            "kpis": self.kpis,
            "checks": self.checks,
            "warnings": self.warnings,
            "mode": self.mode,
            "scenario_id": self.scenario_id,
            "horizon_year": self.horizon_year,
        }


def export_module_result(result: ModuleResult, base_dir: str | None = None) -> Path:
    if base_dir is None:
        base_dir = "outputs/phase2" if str(result.mode).upper() == "SCEN" else "outputs/phase1"
    out_dir = Path(base_dir) / result.run_id / result.module_id
    tables_dir = out_dir / "tables"
    figs_dir = out_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figs_dir.mkdir(parents=True, exist_ok=True)

    for name, df in result.tables.items():
        out_df = df.replace("", np.nan)
        out_df.to_csv(tables_dir / f"{name}.csv", index=False, na_rep="NaN")

    (out_dir / "narrative.md").write_text(result.narrative_md, encoding="utf-8")

    import json

    with (out_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(result.to_summary(), f, ensure_ascii=False, indent=2, default=str)

    return out_dir

