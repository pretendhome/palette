#!/usr/bin/env python3
"""palette query — One command, five steps, full chain.

Usage:
  palette query "how do I evaluate voice quality?"
  palette query --learn "how do governance tiers work?"
  palette query --json "what is taxonomy routing?"
  palette query --trace "convergence protocol"

Steps:
  1. RESOLVE  — classify query via taxonomy (hybrid retrieval)
  2. RETRIEVE — pull grounded knowledge entries
  3. ROUTE    — select best agent + send to bus
  4. RESPOND  — get agent response grounded in knowledge
  5. EXTRACT  — propose learnings for memory (governed)

Every step is logged. Every bus interaction uses the governed envelope.
Routes THROUGH the bus, not around it (Gemini constraint).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib import request

# ── Paths ───────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[1]
HUB_DIR = REPO_ROOT / "peers" / "hub"
BUS_URL = "http://127.0.0.1:7899"
IDENTITY = "palette.cli"

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(HUB_DIR))


# ── Bus helpers ─────────────────────────────────────────────────────────

def bus_post(endpoint: str, payload: dict) -> dict | None:
    """POST JSON to the peers bus. Returns parsed response or None on failure.

    Best-effort: bus is nice-to-have for logging/governance, not blocking.
    The query pipeline works without the bus (retrieval is local).
    """
    url = f"{BUS_URL}{endpoint}"
    data = json.dumps(payload).encode()
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def bus_register():
    """Register palette.cli as a bus peer."""
    return bus_post("/register", {
        "identity": IDENTITY,
        "agent_name": "palette-query-cli",
        "runtime": "python-cli",
        "capabilities": ["query", "resolve", "retrieve"],
        "palette_role": "resolver",
        "trust_tier": "PRODUCTION",
        "version": "1.0.0",
    })


def bus_send(to_agent: str, intent: str, content: str,
             msg_type: str = "informational", risk: str = "none",
             thread_id: str | None = None) -> dict | None:
    """Send a governed message through the bus."""
    msg_id = str(uuid.uuid4())
    return bus_post("/send", {
        "protocol_version": "1.0.0",
        "message_id": msg_id,
        "thread_id": thread_id,
        "in_reply_to": None,
        "from_agent": IDENTITY,
        "to_agent": to_agent,
        "message_type": msg_type,
        "intent": intent,
        "risk_level": risk,
        "requires_ack": False,
        "payload": {"content": content},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "ttl_seconds": 3600,
    })


# ── Trace logger ────────────────────────────────────────────────────────

class TraceLog:
    """Append-only trace of the query pipeline."""

    def __init__(self, query: str):
        self.query = query
        self.thread_id = str(uuid.uuid4())
        self.started = time.time()
        self.steps: list[dict] = []

    def step(self, name: str, data: dict, duration_ms: float | None = None):
        entry = {
            "step": name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "duration_ms": duration_ms,
            **data,
        }
        self.steps.append(entry)

    def total_ms(self) -> float:
        return round((time.time() - self.started) * 1000, 1)

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "thread_id": self.thread_id,
            "total_ms": self.total_ms(),
            "steps": self.steps,
        }


# ── Step 1: RESOLVE ─────────────────────────────────────────────────────

def step_resolve(query: str, learn: bool, trace: TraceLog) -> dict:
    """Classify the query via hybrid retrieval (taxonomy routing)."""
    t0 = time.time()

    from palette_retrieve import retrieve, retrieve_learn
    result = retrieve_learn(query) if learn else retrieve(query)

    ms = round((time.time() - t0) * 1000, 1)
    trace.step("resolve", {
        "riu_id": result.get("riu_id"),
        "riu_name": result.get("riu_name"),
        "classification": result.get("classification"),
        "confidence": result.get("confidence"),
        "retrieval_modes": result.get("retrieval_modes"),
        "top_lib": result.get("lib_id"),
        "mode": result.get("mode"),
    }, ms)

    return result


# ── Step 2: RETRIEVE ────────────────────────────────────────────────────

def step_retrieve(resolved: dict, trace: TraceLog) -> list[dict]:
    """Extract grounded knowledge entries from retrieval results."""
    t0 = time.time()

    knowledge = resolved.get("knowledge", [])

    ms = round((time.time() - t0) * 1000, 1)
    trace.step("retrieve", {
        "entries_found": len(knowledge),
        "lib_ids": [k["lib_id"] for k in knowledge],
        "has_enablement": "enablement" in resolved,
    }, ms)

    return knowledge


# ── Step 3: ROUTE ───────────────────────────────────────────────────────

CLASSIFICATION_TO_AGENT = {
    "internal_only": "claude.analysis",
    "both": "claude.analysis",
    "external_preferred": "perplexity.computer",
    "evaluate": "claude.analysis",
    "unknown": "claude.analysis",
}


def step_route(resolved: dict, trace: TraceLog) -> str:
    """Select the best agent based on classification and send routing message to bus."""
    t0 = time.time()

    classification = resolved.get("classification", "unknown")
    agent = CLASSIFICATION_TO_AGENT.get(classification, "claude.analysis")

    # CQ query-before-acting: check what the system already knows
    try:
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        from query_before_act import check_before_dispatch
        pre_check = check_before_dispatch(resolved.get("query", ""), agent)
        pending_count = pre_check.get("pending", {}).get("pending", 0)
        has_memory = pre_check.get("agent_memory", {}).get("has_memory", False)
        memory_entries = len(pre_check.get("agent_memory", {}).get("entries", []))
        advisory = pre_check.get("advisory", [])
    except Exception:
        pending_count = 0
        has_memory = False
        memory_entries = 0
        advisory = []

    # Log the routing decision to the bus
    bus_send(
        to_agent=agent,
        intent=f"palette query routed: {resolved.get('riu_id', 'unknown')} ({resolved.get('riu_name', '')})",
        content=json.dumps({
            "query": resolved.get("query"),
            "riu_id": resolved.get("riu_id"),
            "classification": classification,
            "knowledge_context": resolved.get("context", "")[:500],
            "pre_dispatch_advisory": advisory,
        }),
        thread_id=trace.thread_id,
    )

    ms = round((time.time() - t0) * 1000, 1)
    trace.step("route", {
        "classification": classification,
        "selected_agent": agent,
        "agent_pending_messages": pending_count,
        "agent_has_memory": has_memory,
        "agent_memory_entries": memory_entries,
        "advisory": advisory,
        "bus_message_sent": True,
    }, ms)

    return agent


# ── Step 4: RESPOND ─────────────────────────────────────────────────────

def step_respond(query: str, resolved: dict, agent: str, learn: bool, trace: TraceLog) -> str:
    """Generate a grounded response using the knowledge context.

    Uses the local retrieval context directly — the bus message in step 3
    logged the routing decision for auditability. The actual LLM call happens
    here using the grounded context from step 1-2.
    """
    t0 = time.time()

    riu_id = resolved.get("riu_id", "unknown")
    riu_name = resolved.get("riu_name", "")

    # Build the grounded response without an LLM call — the CLI is a
    # retrieval + routing tool, not a chat interface. The Voice Hub handles
    # LLM generation. The CLI surfaces what Palette knows and how it routes.
    lines = []
    lines.append(f"## Palette Query: {query}")
    lines.append("")

    if riu_id and riu_id != "unknown":
        lines.append(f"**Classified as**: {riu_id} — {riu_name}")
        lines.append(f"**Classification**: {resolved.get('classification', 'unknown')}")
        lines.append(f"**Routed to**: {agent}")
        lines.append("")

    knowledge = resolved.get("knowledge", [])
    if knowledge:
        lines.append("### Grounded Knowledge")
        for k in knowledge:
            score = k.get("score", 0)
            lines.append(f"\n**[{k['lib_id']}]** (score: {score})")
            lines.append(f"  Q: {k.get('question', '')}")
            excerpt = k.get("answer_excerpt", "")
            if excerpt:
                # Truncate for CLI display
                if len(excerpt) > 300:
                    excerpt = excerpt[:300] + "..."
                lines.append(f"  A: {excerpt}")

    enablement = resolved.get("enablement")
    if enablement and learn:
        lines.append("\n### Learning Module")
        lines.append(f"**{enablement.get('name', '')}** ({enablement.get('difficulty', '')})")
        for obj in enablement.get("objectives", []):
            lines.append(f"  - {obj}")

    response_text = "\n".join(lines)

    ms = round((time.time() - t0) * 1000, 1)
    trace.step("respond", {
        "mode": "grounded_retrieval" if not learn else "learning",
        "knowledge_entries": len(knowledge),
        "has_enablement": enablement is not None,
        "response_length": len(response_text),
    }, ms)

    return response_text


# ── Step 5: EXTRACT ─────────────────────────────────────────────────────

def step_extract(query: str, resolved: dict, trace: TraceLog) -> dict | None:
    """Extract learnings and propose for memory (governed).

    Session reflection: if the query resolved to knowledge with high confidence,
    log the successful retrieval pattern. If it resolved poorly, log the gap.
    """
    t0 = time.time()

    confidence = resolved.get("confidence", 0)
    riu_id = resolved.get("riu_id")
    lib_id = resolved.get("lib_id")
    extraction = None

    if confidence < 30 and riu_id:
        # Low confidence = potential content gap
        extraction = {
            "type": "gap_signal",
            "query": query,
            "riu_id": riu_id,
            "confidence": confidence,
            "signal": f"Query '{query[:80]}' matched {riu_id} at only {confidence:.0f}% confidence. Possible content gap.",
        }
        # Send gap signal to bus for governance pipeline
        bus_send(
            to_agent="group",
            intent=f"Content gap detected: {riu_id} — low confidence retrieval",
            content=json.dumps(extraction),
            thread_id=trace.thread_id,
        )
    elif confidence >= 70 and lib_id:
        # High confidence = successful pattern worth remembering
        extraction = {
            "type": "retrieval_success",
            "query": query,
            "lib_id": lib_id,
            "riu_id": riu_id,
            "confidence": confidence,
        }

    ms = round((time.time() - t0) * 1000, 1)
    trace.step("extract", {
        "extraction_type": extraction["type"] if extraction else "none",
        "confidence": confidence,
        "gap_signal_sent": extraction is not None and extraction["type"] == "gap_signal",
    }, ms)

    return extraction


# ── Main pipeline ───────────────────────────────────────────────────────

def run_query(query: str, learn: bool = False, show_json: bool = False,
              show_trace: bool = False) -> int:
    """Execute the full 5-step pipeline."""

    trace = TraceLog(query)

    # Register on bus (idempotent, best-effort)
    bus_register()

    # Step 1: RESOLVE
    resolved = step_resolve(query, learn, trace)

    # Step 2: RETRIEVE
    knowledge = step_retrieve(resolved, trace)

    # Step 3: ROUTE
    agent = step_route(resolved, trace)

    # Step 4: RESPOND
    response = step_respond(query, resolved, agent, learn, trace)

    # Step 5: EXTRACT
    extraction = step_extract(query, resolved, trace)

    # Output
    if show_json:
        output = {
            "query": query,
            "mode": "learn" if learn else "query",
            "riu_id": resolved.get("riu_id"),
            "riu_name": resolved.get("riu_name"),
            "classification": resolved.get("classification"),
            "confidence": resolved.get("confidence"),
            "retrieval_modes": resolved.get("retrieval_modes"),
            "agent": agent,
            "knowledge": knowledge,
            "extraction": extraction,
        }
        if show_trace:
            output["trace"] = trace.to_dict()
        print(json.dumps(output, indent=2))
    elif show_trace:
        print(response)
        print("\n--- TRACE ---")
        print(json.dumps(trace.to_dict(), indent=2))
    else:
        print(response)

    # Write to session log (NDJSON) for session_reflect.py
    session_log = REPO_ROOT / "peers" / "session_log.ndjson"
    try:
        session_log.parent.mkdir(parents=True, exist_ok=True)
        with open(session_log, "a") as f:
            f.write(json.dumps({
                "query": query[:200],
                "riu_id": resolved.get("riu_id"),
                "lib_id": resolved.get("lib_id"),
                "confidence": resolved.get("confidence"),
                "agent": agent,
                "mode": "learn" if learn else "query",
                "retrieval_modes": resolved.get("retrieval_modes"),
                "total_ms": trace.total_ms(),
                "extraction": extraction.get("type") if extraction else None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }) + "\n")
    except Exception:
        pass

    # Log completion to bus
    bus_send(
        to_agent="group",
        intent=f"palette query completed: {resolved.get('riu_id', 'unknown')} ({trace.total_ms():.0f}ms)",
        content=json.dumps({
            "query": query[:100],
            "riu_id": resolved.get("riu_id"),
            "confidence": resolved.get("confidence"),
            "agent": agent,
            "total_ms": trace.total_ms(),
            "steps": len(trace.steps),
        }),
        thread_id=trace.thread_id,
    )

    return 0


# ── CLI entry point ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="palette query",
        description="One command. Five steps. Resolve → Retrieve → Route → Respond → Extract.",
    )
    parser.add_argument("query", nargs="+", help="Natural language query")
    parser.add_argument("--learn", action="store_true", help="Learning mode: include enablement content")
    parser.add_argument("--json", action="store_true", help="Output full JSON result")
    parser.add_argument("--trace", action="store_true", help="Show execution trace")
    args = parser.parse_args()

    query = " ".join(args.query)
    sys.exit(run_query(query, learn=args.learn, show_json=args.json, show_trace=args.trace))


if __name__ == "__main__":
    main()
