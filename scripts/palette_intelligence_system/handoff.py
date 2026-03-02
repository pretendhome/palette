"""DEPRECATED: legacy HandoffPacket model.

Active coordination state and replay semantics now live in:
  scripts/palette_intelligence_system/coordination.py

This module remains only as a compatibility shim for older references and
should not be used for new code.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class StepRecord:
    """Single step in a task execution."""
    
    def __init__(self, name: str):
        self.name = name
        self.status = "pending"  # pending|running|success|failed|skipped
        self.started_at: Optional[str] = None
        self.ended_at: Optional[str] = None
        self.attempt = 0
        self.error: Optional[str] = None
        self.output: Any = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "attempt": self.attempt,
            "error": self.error,
            "output": self.output
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StepRecord":
        step = cls(data["name"])
        step.status = data.get("status", "pending")
        step.started_at = data.get("started_at")
        step.ended_at = data.get("ended_at")
        step.attempt = data.get("attempt", 0)
        step.error = data.get("error")
        step.output = data.get("output")
        return step


class HandoffPacket:
    """HandoffPacket v2 — Task state for multi-agent coordination."""
    
    SCHEMA_VERSION = "handoffpacket.v2"
    
    def __init__(self, task_id: str, user_query: str):
        self.task_id = task_id
        self.schema_version = self.SCHEMA_VERSION
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.user_query = user_query
        self.status = "pending"  # pending|running|success|failed
        self.resolved_rius: List[Dict[str, Any]] = []
        self.steps: Dict[str, StepRecord] = {
            "resolver": StepRecord("resolver"),
            "traversal": StepRecord("traversal"),
            "researcher": StepRecord("researcher"),
            "final": StepRecord("final")
        }
        self.outputs: Dict[str, Any] = {}
        self.gaps: List[str] = []
        self.errors: List[str] = []
        self.provenance: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "schema_version": self.schema_version,
            "created_at": self.created_at,
            "user_query": self.user_query,
            "status": self.status,
            "resolved_rius": self.resolved_rius,
            "steps": {name: step.to_dict() for name, step in self.steps.items()},
            "outputs": self.outputs,
            "gaps": self.gaps,
            "errors": self.errors,
            "provenance": self.provenance
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HandoffPacket":
        packet = cls(data["task_id"], data["user_query"])
        packet.schema_version = data.get("schema_version", cls.SCHEMA_VERSION)
        packet.created_at = data.get("created_at", packet.created_at)
        packet.status = data.get("status", "pending")
        packet.resolved_rius = data.get("resolved_rius", [])
        packet.steps = {
            name: StepRecord.from_dict(step_data)
            for name, step_data in data.get("steps", {}).items()
        }
        packet.outputs = data.get("outputs", {})
        packet.gaps = data.get("gaps", [])
        packet.errors = data.get("errors", [])
        packet.provenance = data.get("provenance", {})
        return packet
    
    def save(self, state_dir: Path):
        """Save packet to JSON file."""
        state_dir.mkdir(parents=True, exist_ok=True)
        path = state_dir / f"{self.task_id}.json"
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, task_id: str, state_dir: Path) -> "HandoffPacket":
        """Load packet from JSON file."""
        path = state_dir / f"{task_id}.json"
        with open(path) as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def get_first_failed_step(self) -> Optional[str]:
        """Return name of first failed step, or None if all succeeded."""
        step_order = ["resolver", "traversal", "researcher", "final"]
        for step_name in step_order:
            step = self.steps.get(step_name)
            if step and step.status == "failed":
                return step_name
        return None
    
    def get_steps_to_replay(self, from_step: Optional[str] = None) -> List[str]:
        """Get list of steps to replay.
        
        If from_step is provided, replay from that step onwards.
        Otherwise, replay from first failed step onwards.
        """
        step_order = ["resolver", "traversal", "researcher", "final"]
        
        if from_step:
            start_idx = step_order.index(from_step)
        else:
            first_failed = self.get_first_failed_step()
            if not first_failed:
                return []
            start_idx = step_order.index(first_failed)
        
        return step_order[start_idx:]
