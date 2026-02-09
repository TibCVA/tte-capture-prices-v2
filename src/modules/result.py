"""Standard module output contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

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

    def to_summary(self) -> dict[str, Any]:
        return {
            "module_id": self.module_id,
            "run_id": self.run_id,
            "selection": self.selection,
            "assumptions_used": self.assumptions_used,
            "kpis": self.kpis,
            "checks": self.checks,
            "warnings": self.warnings,
        }


def export_module_result(result: ModuleResult, base_dir: str = "outputs/phase1") -> Path:
    out_dir = Path(base_dir) / result.run_id / result.module_id
    tables_dir = out_dir / "tables"
    figs_dir = out_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figs_dir.mkdir(parents=True, exist_ok=True)

    for name, df in result.tables.items():
        df.to_csv(tables_dir / f"{name}.csv", index=False)

    (out_dir / "narrative.md").write_text(result.narrative_md, encoding="utf-8")

    import json

    with (out_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(result.to_summary(), f, ensure_ascii=False, indent=2, default=str)

    return out_dir

