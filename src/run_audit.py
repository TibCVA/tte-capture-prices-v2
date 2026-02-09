"""Run audit context and manifest management."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from src.hash_utils import hash_object, sha256_file


@dataclass
class RunContext:
    run_id: str
    run_dir: Path


def create_run_context(config_snapshot: dict[str, Any], base_dir: str = "outputs/runs") -> RunContext:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    cfg_hash = hash_object(config_snapshot)[:12]
    run_id = f"{ts}_{cfg_hash}"
    run_dir = Path(base_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    pd.Series(config_snapshot, dtype=object).to_json(
        run_dir / "run_config_snapshot.json", orient="index", indent=2, force_ascii=False
    )
    return RunContext(run_id=run_id, run_dir=run_dir)


def write_data_manifest(run_ctx: RunContext, entries: list[dict[str, Any]]) -> Path:
    rows = []
    for e in entries:
        item = dict(e)
        file_path = item.get("file_path")
        if file_path and Path(file_path).exists():
            item["checksum_sha256"] = sha256_file(file_path)
        rows.append(item)
    df = pd.DataFrame(rows)
    path = run_ctx.run_dir / "data_manifest.csv"
    df.to_csv(path, index=False)
    return path

