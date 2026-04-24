"""
Shared evidence packet creation for remediation loop agents.
"""
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

EVIDENCE_DIR = Path(__file__).parent.parent.parent / "artifacts" / "validation"


def create(task, error, input_payload=None):
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    ev_id = str(uuid.uuid4())[:8]
    path = EVIDENCE_DIR / f"EVIDENCE-{ev_id}.json"
    data = {
        "evidence_id": ev_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "task": task,
        "error": str(error),
        "input_payload": input_payload or {},
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path


def read(path):
    with open(path) as f:
        return json.load(f)


def is_sound(path):
    try:
        data = read(path)
        for key in ("evidence_id", "timestamp", "task", "error"):
            if key not in data:
                return False, f"Missing field: {key}"
        if len(str(data.get("error", ""))) < 20:
            return False, "Too Shallow: error details insufficient"
        return True, None
    except Exception as e:
        return False, str(e)
