"""Run audit context and manifest management."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Any

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

    (run_dir / "run_config_snapshot.json").write_text(
        json.dumps(config_snapshot, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
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
    path = run_ctx.run_dir / "data_manifest.csv"
    if not rows:
        path.write_text("dataset_name,country,year,file_path,source,download_timestamp_utc,checksum_sha256\n", encoding="utf-8")
        return path
    import pandas as pd
    pd.DataFrame(rows).to_csv(path, index=False)
    return path

