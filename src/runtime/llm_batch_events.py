from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json


DEFAULT_LLM_BATCH_EVENTS_PATH = Path("outputs/audit/llm_batch_events.jsonl")


def append_llm_batch_event(event_type: str, payload: dict[str, Any], log_path: Path = DEFAULT_LLM_BATCH_EVENTS_PATH) -> Path:
    record = {
        "event_type": str(event_type),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "payload": payload if isinstance(payload, dict) else {"value": str(payload)},
    }
    target = log_path if log_path.is_absolute() else Path(__file__).resolve().parents[2] / log_path
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return target

