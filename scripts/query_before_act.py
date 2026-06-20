#!/usr/bin/env python3
"""query_before_act.py — CQ-inspired pre-dispatch knowledge check.

Before any agent invocation, check what the system already knows:
  1. Query the knowledge library (hybrid retrieval)
  2. Check the target agent's memory (bus /memory endpoint)
  3. Return context that should inform the invocation

This prevents redundant work and ensures agents start with grounded context.

Usage as module:
    from query_before_act import check_before_dispatch
    context = check_before_dispatch("how do I build a RAG pipeline?", "claude.analysis")

Usage as CLI:
    python3 scripts/query_before_act.py "query" agent_identity
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib import request

BUS_URL = "http://127.0.0.1:7899"
REPO_ROOT = Path(__file__).resolve().parent.parent
HUB_DIR = REPO_ROOT / "peers" / "hub"

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(HUB_DIR))


def _bus_get(endpoint: str, payload: dict) -> dict | None:
    """POST to bus endpoint, return parsed JSON or None."""
    url = f"{BUS_URL}{endpoint}"
    data = json.dumps(payload).encode()
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def check_kl(query: str) -> dict:
    """Check knowledge library for relevant entries via hybrid retrieval."""
    try:
        from palette_retrieve import hybrid_retrieve, load_all
        data = load_all()
        ranked = hybrid_retrieve(query, data, top_k=3)

        if not ranked:
            return {"has_knowledge": False, "entries": [], "confidence": 0}

        top_id, top_score = ranked[0]
        # RRF scores normalized to 0-100 range (confidence %)
        entries = []
        for lib_id, score in ranked:
            entry = data.knowledge.get(lib_id, {})
            entries.append({
                "lib_id": lib_id,
                "score": round(score, 1),
                "question": str(entry.get("question", ""))[:150],
            })

        return {
            "has_knowledge": top_score >= 50,
            "entries": entries,
            "confidence": round(top_score, 1),
            "top_lib": top_id,
        }
    except Exception as e:
        return {"has_knowledge": False, "entries": [], "confidence": 0, "error": str(e)}


def check_agent_memory(agent_identity: str) -> dict:
    """Check target agent's memory for relevant context."""
    result = _bus_get("/memory", {
        "identity": agent_identity,
        "store": "memory",
        "action": "read",
    })

    if not result or "error" in result:
        return {"has_memory": False, "entries": [], "usage": None}

    entries = result.get("entries", [])
    usage = result.get("usage", {})

    return {
        "has_memory": len(entries) > 0,
        "entries": [
            {"entry_id": e["entry_id"], "content": e["content"][:200]}
            for e in entries
        ],
        "usage": usage,
    }


def check_pending_messages(agent_identity: str) -> dict:
    """Check if the target agent has pending messages on the bus."""
    result = _bus_get("/peek", {"identity": agent_identity})
    if not result:
        return {"pending": 0}
    return {"pending": result.get("count", 0)}


def check_before_dispatch(query: str, agent_identity: str) -> dict:
    """Full pre-dispatch check: KL + agent memory + pending messages.

    Returns a context dict that should inform the invocation decision:
    - If KL already has a high-confidence answer, the agent may not need to research
    - If agent memory has relevant context, it should be included in the prompt
    - If the agent has pending messages, dispatch may need to wait
    """
    kl = check_kl(query)
    memory = check_agent_memory(agent_identity)
    pending = check_pending_messages(agent_identity)

    # Build advisory
    advisory = []
    if kl["has_knowledge"]:
        advisory.append(
            f"KL has relevant knowledge ({kl['confidence']:.0f}% confidence): "
            f"{kl['top_lib']}"
        )
    if memory["has_memory"]:
        advisory.append(
            f"Agent {agent_identity} has {len(memory['entries'])} memory entries "
            f"({memory['usage'].get('percent', 0)}% capacity)"
        )
    if pending["pending"] > 0:
        advisory.append(
            f"Agent {agent_identity} has {pending['pending']} pending messages"
        )

    return {
        "query": query,
        "agent": agent_identity,
        "knowledge": kl,
        "agent_memory": memory,
        "pending": pending,
        "advisory": advisory,
        "should_dispatch": True,  # always dispatch, but with context
        "context_for_agent": _build_context(kl, memory),
    }


def _build_context(kl: dict, memory: dict) -> str:
    """Build context string to prepend to agent invocation."""
    parts = []

    if kl["has_knowledge"]:
        parts.append("## Existing Knowledge (from Palette KL)")
        for e in kl["entries"][:3]:
            parts.append(f"- [{e['lib_id']}] ({e['score']:.0f}%): {e['question']}")

    if memory["has_memory"]:
        parts.append(f"\n## Agent Memory ({len(memory['entries'])} entries)")
        for e in memory["entries"][:3]:
            parts.append(f"- [{e['entry_id']}]: {e['content']}")

    return "\n".join(parts) if parts else ""


# ── CLI ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 query_before_act.py <query> [agent_identity]")
        print("  Checks KL + agent memory before dispatching to an agent.")
        sys.exit(1)

    query = sys.argv[1]
    agent = sys.argv[2] if len(sys.argv) > 2 else "claude.analysis"

    result = check_before_dispatch(query, agent)
    print(json.dumps(result, indent=2))
