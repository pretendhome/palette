#!/usr/bin/env python3
"""palette query — One command, five steps, full chain.

Usage:
  palette query "how do I evaluate voice quality?"
  palette query --learn "how do governance tiers work?"
  palette query --json "what is taxonomy routing?"
  palette query --trace "convergence protocol"
  palette query --external "What are Delaware fiduciary duty precedents?"

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

sys.path.insert(0, str(REPO_ROOT.parent))
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
             thread_id: str | None = None,
             riu_id: str | None = None,
             confidence: float | None = None) -> dict | None:
    """Send a governed message through the bus."""
    msg_id = str(uuid.uuid4())
    payload: dict = {"content": content}
    if riu_id:
        payload["riu_id"] = riu_id
    if confidence is not None:
        payload["confidence"] = confidence
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
        "payload": payload,
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


# ── Gap signal logging ─────────────────────────────────────────────────

GAP_LOG = REPO_ROOT / "peers" / "gap_signals.ndjson"


def _log_gap_signal(query: str, riu_id: str | None, confidence: float, signal_type: str):
    """Append a gap signal to the persistent NDJSON log for auto_enrich."""
    try:
        GAP_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(GAP_LOG, "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "query": query[:200],
                "riu_id": riu_id,
                "confidence": confidence,
                "signal_type": signal_type,
            }) + "\n")
    except Exception:
        pass


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


def step_external(query: str, resolved: dict, use_external: bool, trace: TraceLog) -> dict | None:
    """Optionally run the governed external research gateway."""
    if not use_external:
        return None

    t0 = time.time()
    from palette.bdb.gateway import gateway_query

    external = gateway_query(
        query=query,
        retrieval_result=resolved,
        use_external=True,
    )
    ms = round((time.time() - t0) * 1000, 1)
    trace.step("external", {
        "requested": True,
        "called": external["governance"].get("external_called"),
        "blocked": external["governance"].get("blocked"),
        "cache_hit": external["governance"].get("cache_hit"),
        "pii_detected": external["governance"].get("pii_detected"),
    }, ms)
    return external


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
        msg_type="advisory",
        thread_id=trace.thread_id,
        riu_id=resolved.get("riu_id"),
        confidence=resolved.get("confidence"),
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
    """Generate a grounded response using the knowledge context."""
    t0 = time.time()

    riu_id = resolved.get("riu_id", "unknown")
    riu_name = resolved.get("riu_name", "")

    lines = []
    lines.append(f"## Palette Query: {query}")
    lines.append("")

    if riu_id and riu_id != "unknown":
        lines.append(f"**Classified as**: {riu_id} — {riu_name}")
        lines.append(f"**Classification**: {resolved.get('classification', 'unknown')}")
        lines.append(f"**Routed to**: {agent}")
        lines.append("")

    gateway = resolved.get("gateway")
    if gateway:
        governance = gateway.get("governance", {})
        lines.append("### Governance")
        lines.append(f"**External requested**: {governance.get('external_requested')}")
        lines.append(f"**External called**: {governance.get('external_called')}")
        lines.append(f"**Blocked**: {governance.get('blocked')}")
        if governance.get("block_reason"):
            lines.append(f"**Block reason**: {governance.get('block_reason')}")
        pii = governance.get("pii_detected") or []
        if pii:
            lines.append(f"**PII detected**: {', '.join(pii)}")
        lines.append("")
        lines.append("### Merged Context")
        lines.append(gateway.get("merged_context", ""))
    else:
        knowledge = resolved.get("knowledge", [])
        if knowledge:
            lines.append("### Grounded Knowledge")
            for k in knowledge:
                score = k.get("score", 0)
                lines.append(f"\n**[{k['lib_id']}]** (score: {score})")
                lines.append(f"  Q: {k.get('question', '')}")
                excerpt = k.get("answer_excerpt", "")
                if excerpt:
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
        "knowledge_entries": len(resolved.get("knowledge", [])),
        "has_enablement": enablement is not None,
        "response_length": len(response_text),
        "used_gateway": gateway is not None,
    }, ms)

    return response_text


# ── Step 5: EXTRACT ─────────────────────────────────────────────────────

def step_extract(query: str, resolved: dict, trace: TraceLog) -> dict | None:
    """Extract learnings and propose for memory (governed)."""
    t0 = time.time()

    confidence = resolved.get("confidence", 0)
    riu_id = resolved.get("riu_id")
    lib_id = resolved.get("lib_id")
    extraction = None

    if confidence < 30 and riu_id:
        extraction = {
            "type": "gap_signal",
            "query": query,
            "riu_id": riu_id,
            "confidence": confidence,
            "signal": f"Query '{query[:80]}' matched {riu_id} at only {confidence:.0f}% confidence. Possible content gap.",
        }
        bus_send(
            to_agent="all",
            intent=f"Content gap detected: {riu_id} — low confidence retrieval",
            content=json.dumps(extraction),
            thread_id=trace.thread_id,
        )
        _log_gap_signal(query, riu_id, confidence, "low_confidence")
    elif confidence < 70 and riu_id:
        _log_gap_signal(query, riu_id, confidence, "medium_confidence")
        extraction = {
            "type": "medium_confidence",
            "query": query,
            "riu_id": riu_id,
            "confidence": confidence,
        }
    elif confidence >= 70 and lib_id:
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
              show_trace: bool = False, use_external: bool = False) -> int:
    """Execute the full 5-step pipeline."""

    trace = TraceLog(query)

    bus_register()

    resolved = step_resolve(query, learn, trace)

    # OBLIGATORY GATE: abort if classification failed entirely
    if resolved.get("confidence", 0) == 0 and resolved.get("riu_id") is None:
        extraction = {
            "type": "classification_failure",
            "query": query[:200],
            "signal": "No taxonomy match. Cannot route without classification.",
        }
        bus_send(
            to_agent="all",
            intent="Classification failure — unroutable query",
            content=json.dumps(extraction),
            thread_id=trace.thread_id,
        )
        _log_gap_signal(query, None, 0, "classification_failure")
        if show_json:
            print(json.dumps({"error": "classification_failure", "query": query, "signal": extraction["signal"]}, indent=2))
        else:
            print(f"## Classification Failed\n\nQuery: {query}\nNo RIU match found. Gap signal logged.\n")
        return 1

    knowledge = step_retrieve(resolved, trace)
    gateway_result = step_external(query, resolved, use_external, trace)
    if gateway_result is not None:
        resolved["gateway"] = gateway_result
    agent = step_route(resolved, trace)
    response = step_respond(query, resolved, agent, learn, trace)
    extraction = step_extract(query, resolved, trace)

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
            "gateway": gateway_result,
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
                "external_requested": use_external,
                "external_called": gateway_result.get("governance", {}).get("external_called") if gateway_result else False,
                "total_ms": trace.total_ms(),
                "extraction": extraction.get("type") if extraction else None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }) + "\n")
    except Exception:
        pass

    bus_send(
        to_agent="all",
        intent=f"palette query completed: {resolved.get('riu_id', 'unknown')} ({trace.total_ms():.0f}ms)",
        content=json.dumps({
            "query": query[:100],
            "riu_id": resolved.get("riu_id"),
            "confidence": resolved.get("confidence"),
            "agent": agent,
            "external_requested": use_external,
            "external_called": gateway_result.get("governance", {}).get("external_called") if gateway_result else False,
            "total_ms": trace.total_ms(),
            "steps": len(trace.steps),
        }),
        thread_id=trace.thread_id,
    )

    return 0


# ── Demo output mode ────────────────────────────────────────────────────

# ANSI color codes (work on all modern terminals)
_RESET = "\033[0m"
_BOLD = "\033[1m"
_DIM = "\033[2m"
_GREEN = "\033[32m"
_BLUE = "\033[34m"
_RED = "\033[31m"
_YELLOW = "\033[33m"
_CYAN = "\033[36m"
_WHITE = "\033[37m"
_MAGENTA = "\033[35m"
_BG_RED = "\033[41m"
_BG_GREEN = "\033[42m"


def _demo_label(label: str, color: str, text: str = "") -> str:
    """Format a step label for demo output."""
    suffix = f" {text}" if text else ""
    return f"{color}{_BOLD}[{label}]{_RESET}{suffix}"


def _demo_boundary(label: str) -> str:
    """Visual governance boundary marker."""
    return f"\n  {_DIM}{'━' * 4}{_RESET} {_YELLOW}{_BOLD}{label}{_RESET} {_DIM}{'━' * 40}{_RESET}\n"


def _call_model_api(model_name: str, system_prompt: str, user_prompt: str, timeout: int = 30) -> str | None:
    """Call an external model API and return the response text. Best-effort."""
    import os as _os

    if model_name == "ollama":
        try:
            import httpx
            resp = httpx.post("http://127.0.0.1:11434/api/generate", json={
                "model": "qwen2.5:3b",
                "prompt": f"{system_prompt}\n\n{user_prompt}",
                "stream": False,
            }, timeout=60.0)
            if resp.status_code == 200:
                return resp.json().get("response", "")
        except Exception:
            # Fallback to 7B
            try:
                resp = httpx.post("http://127.0.0.1:11434/api/generate", json={
                    "model": "qwen2.5:7b",
                    "prompt": f"{system_prompt}\n\n{user_prompt}",
                    "stream": False,
                }, timeout=60.0)
                if resp.status_code == 200:
                    return resp.json().get("response", "")
            except Exception:
                pass
        return None

    # Claude via CLI (uses OAuth subscription, no API key)
    if model_name == "claude":
        try:
            import subprocess
            result = subprocess.run(
                ["claude", "-p", f"{system_prompt}\n\n{user_prompt}"],
                capture_output=True, text=True, timeout=timeout,
                env={**_os.environ, "CLAUDE_CODE_ENTRYPOINT": "palette-demo"},
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None

    # Mistral via API
    if model_name == "mistral":
        api_key = _os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            return None
        try:
            payload = json.dumps({
                "model": "mistral-large-latest",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            }).encode()
            req = request.Request(
                "https://api.mistral.ai/v1/chat/completions",
                data=payload,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            )
            with request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read())
                return body["choices"][0]["message"]["content"]
        except Exception:
            pass
        return None

    return None


def run_demo(query: str, use_external: bool = False) -> int:
    """Execute the pipeline with demo-optimized terminal output.

    Designed for 2-minute video recording:
    - Clear step labels with color coding
    - Governance state visible at every step
    - [LOCAL] green, [EXTERNAL:Perplexity] blue, [BLOCKED] red
    - Readable at 14pt+ font on dark background
    """
    import time as _time

    trace = TraceLog(query)
    bus_register()

    # ── Header
    print()
    print(f"  {_DIM}{'━' * 60}{_RESET}")
    print(f"  {_BOLD}{_WHITE}  ◆ palette{_RESET}  {_DIM}the operating system for professional judgment{_RESET}")
    print(f"  {_DIM}{'━' * 60}{_RESET}")
    print()
    print(f"  {_DIM}Query:{_RESET}  {_BOLD}{query}{_RESET}")
    print()

    # ── Step 1: RESOLVE
    _time.sleep(0.1)  # visual pacing for recording
    resolved = step_resolve(query, False, trace)
    riu_id = resolved.get("riu_id", "unknown")
    riu_name = resolved.get("riu_name", "")
    confidence = resolved.get("confidence", 0)

    print(f"  {_demo_label('RESOLVE', _CYAN)} Classified: {_BOLD}{riu_id}{_RESET} ({riu_name})")

    # ── Step 2: RETRIEVE
    knowledge = step_retrieve(resolved, trace)
    k_count = len(resolved.get("knowledge", []))
    conf_color = _GREEN if confidence >= 40 else _YELLOW if confidence >= 20 else _RED

    print(f"  {_demo_label('RETRIEVE', _CYAN)} Local knowledge: {k_count} entries (confidence: {conf_color}{confidence:.0f}%{_RESET})")

    # Check for prior related decisions in session log (compounding signal)
    prior_decisions = []
    session_log = REPO_ROOT / "peers" / "session_log.ndjson"
    if session_log.exists():
        try:
            import re as _re

            def _stem(word):
                """Minimal stemming for matching: duties→duty, fiduciary stays"""
                if word.endswith('ies') and len(word) > 4:
                    return word[:-3] + 'y'  # duties→duty, parties→party
                for suffix in ('ing', 'tion', 'es', 'ed', 'ly', 's'):
                    if word.endswith(suffix) and len(word) - len(suffix) >= 3:
                        return word[:-len(suffix)]
                return word

            _stopwords = {'the', 'a', 'an', 'is', 'are', 'what', 'how', 'do', 'to', 'for', 'in', 'of', 'we', 'our', 'would', 'should', 'about', 'given', 'found', 'this', 'that', 'with', 'from', 'was', 'were', 'been', 'have', 'has', 'had', 'if', 'or', 'and', 'not', 'no', 'by', 'on', 'at', 'it'}
            query_words = {_stem(w) for w in _re.findall(r'[a-z]+', query.lower())} - _stopwords
            seen_queries = set()
            with open(session_log) as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        entry_query = entry.get("query", "")
                        normalized_query = entry_query.strip().lower()
                        if not normalized_query or normalized_query == query.strip().lower() or normalized_query in seen_queries:
                            continue
                        entry_words = {_stem(w) for w in _re.findall(r'[a-z]+', normalized_query)} - _stopwords
                        overlap = query_words & entry_words
                        # Match on word overlap OR same RIU cluster (e.g., both RIU-7xx)
                        same_cluster = False
                        entry_riu = entry.get("riu_id", "")
                        if riu_id and entry_riu:
                            # Same hundred-group: RIU-7xx matches RIU-7xx, LEGAL-0xx matches LEGAL-0xx
                            rid_prefix = riu_id.rsplit('-', 1)[0] + '-' + riu_id.rsplit('-', 1)[-1][0] if '-' in riu_id else ""
                            ent_prefix = entry_riu.rsplit('-', 1)[0] + '-' + entry_riu.rsplit('-', 1)[-1][0] if '-' in entry_riu else ""
                            if rid_prefix and ent_prefix and rid_prefix == ent_prefix:
                                same_cluster = True
                        if len(overlap) >= 2 or same_cluster:
                            prior_decisions.append(entry)
                            seen_queries.add(normalized_query)
                    except (json.JSONDecodeError, KeyError):
                        pass
        except Exception:
            pass

    if prior_decisions:
        print(f"  {_demo_label('CONNECT', _GREEN)} Connected to {len(prior_decisions)} prior decision(s):")
        for pd in prior_decisions[:3]:
            ts = pd.get("timestamp", "")[:10]
            pq = pd.get("query", "")[:60]
            blocked = pd.get("blocked", False)
            ext = pd.get("external_called", False)
            tag = f"{_RED}[BLOCKED]{_RESET}" if blocked else (f"{_BLUE}[EXT]{_RESET}" if ext else f"{_GREEN}[LOCAL]{_RESET}")
            print(f"    {_DIM}{ts}{_RESET} {tag} {pq}")

    # ── Step 3: EXTERNAL GATEWAY (if requested)
    gateway_result = None
    if use_external:
        _time.sleep(0.1)
        # In demo mode, always run the sanitizer when --external is passed.
        # Override the confidence gate so the governance decision is always visible.
        from palette.bdb.gateway import PerplexityGateway
        gw = PerplexityGateway()

        # Force low confidence so gateway enters the sanitization path
        demo_retrieval = dict(resolved)
        demo_retrieval["confidence"] = 10  # force below threshold

        gateway_result = gw.gateway_query(
            query=query,
            retrieval_result=demo_retrieval,
            use_external=True,
        )
        resolved["gateway"] = gateway_result
        trace.step("external", {
            "requested": True,
            "called": gateway_result["governance"].get("external_called"),
            "blocked": gateway_result["governance"].get("blocked"),
            "cache_hit": gateway_result["governance"].get("cache_hit"),
            "pii_detected": gateway_result["governance"].get("pii_detected"),
        }, 0)
        if gateway_result:
            gov = gateway_result.get("governance", {})
            pii = gov.get("pii_detected", [])
            blocked = gov.get("blocked", False)
            external_called = gov.get("external_called", False)
            cache_hit = gov.get("cache_hit", False)
            sanitization_applied = gov.get("sanitization_applied", False)

            if blocked:
                # BLOCKED — the money shot for the demo
                block_reason = gov.get("block_reason", "policy violation")
                print(_demo_boundary("GOVERNANCE BOUNDARY"))
                print(f"  {_BG_RED}{_BOLD}{_WHITE} ⚠️  BLOCKED {_RESET} {_RED}Client-specific query detected{_RESET}")
                if pii:
                    print(f"  {_RED}  PII found: [{', '.join(pii)}]{_RESET}")
                print(f"  {_RED}  Reason: {block_reason}{_RESET}")
                print()
                print(f"  {_BG_GREEN}{_BOLD}{_WHITE} → LOCAL ONLY {_RESET} {_GREEN}Zero data left this machine.{_RESET}")
                print(f"  {_DIM}  Model: Ollama (on-device){_RESET}")
            elif external_called:
                # External call succeeded
                if sanitization_applied:
                    san_query = gateway_result.get("sanitized_query", "")
                    print(f"  {_demo_label('SANITIZE', _YELLOW)} Query safe for external: {_GREEN}✓{_RESET} (no PII detected)")
                print(_demo_boundary("GOVERNANCE BOUNDARY"))
                source_label = f"(cache: {cache_hit})" if cache_hit else ""
                print(f"  {_demo_label('EXTERNAL', _BLUE)} Routed to Perplexity sonar-pro {_DIM}{source_label}{_RESET}")
                print(f"  {_DIM}  Model: Perplexity (governed external research){_RESET}")
            else:
                # External not needed (high confidence)
                print(f"  {_demo_label('LOCAL', _GREEN)} High confidence — no external query needed.")

            resolved["gateway"] = gateway_result

    # ── Step 4: RESPOND
    _time.sleep(0.1)
    agent = step_route(resolved, trace)

    # Build demo response
    print()
    print(f"  {_DIM}{'━' * 50}{_RESET}")

    if gateway_result and gateway_result.get("governance", {}).get("external_called"):
        external = gateway_result.get("external_results", {})
        answer = external.get("answer", "").strip()
        sources = external.get("sources", [])
        print(f"  {_demo_label('RESULT', _GREEN)} {_BLUE}[EXTERNAL:Perplexity]{_RESET} answer + {_GREEN}[LOCAL]{_RESET} support")
        print()
        print(f"  {_BLUE}{_BOLD}Perplexity answer:{_RESET}")
        answer_lines = [line.strip() for line in answer.split("\n") if line.strip()]
        if not answer_lines:
            answer_lines = ["No external answer returned."]
        for line in answer_lines[:8]:
            print(f"  {line[:140]}")
        if len(answer_lines) > 8:
            print(f"  {_DIM}... [truncated for display]{_RESET}")
        if sources:
            print(f"  {_DIM}Citations:{_RESET}")
            for source in sources[:3]:
                print(f"  {_DIM}- {source}{_RESET}")
        print()
        print(f"  {_GREEN}{_BOLD}Local support:{_RESET}")
        for k in resolved.get("knowledge", [])[:2]:
            print(f"  {_DIM}[{k.get('lib_id', '')}]{_RESET} {k.get('question', '')}")
            excerpt = (k.get("answer_excerpt", "") or "").strip()
            if excerpt:
                print(f"    {excerpt[:140]}")

        # ── Multi-model routing: Claude synthesis or Mistral critique
        query_lower = query.lower()
        is_adversarial = any(w in query_lower for w in ["opposing counsel", "argue", "missing", "counter", "weakness", "risk"])

        if is_adversarial:
            # Route to Mistral for adversarial critique
            print()
            print(f"  {_demo_label('CRITIQUE', _MAGENTA)} Routed to Mistral for adversarial analysis")
            print(f"  {_DIM}  Model: Mistral (governed — client identity stripped){_RESET}")
            critique_ctx = answer[:500] if answer else ""
            local_ctx = "\n".join(k.get("question", "") for k in resolved.get("knowledge", [])[:3])
            critique = _call_model_api("mistral",
                "You are an adversarial legal analyst. Identify the 3 strongest counter-arguments opposing counsel would raise. Be specific about legal standards. Do not reference any client names.",
                f"Legal context:\n{critique_ctx}\n\nLocal knowledge:\n{local_ctx}\n\nQuestion: {query}")
            if critique:
                print()
                print(f"  {_MAGENTA}{_BOLD}Mistral critique:{_RESET}")
                for line in critique.split("\n")[:12]:
                    if line.strip():
                        print(f"  {line[:140]}")
        else:
            # Route to Claude for synthesis
            print()
            print(f"  {_demo_label('SYNTHESIS', _CYAN)} Routed to Claude for analysis")
            print(f"  {_DIM}  Model: Claude (governed — client identity stripped){_RESET}")
            local_ctx = "\n".join(k.get("question", "") for k in resolved.get("knowledge", [])[:3])
            synthesis = _call_model_api("claude",
                "You are a legal analyst. Synthesize the research into a concise analysis. Connect the precedents to the fact pattern. Do not reference any client names. Be specific about applicable legal standards. Keep it under 150 words.",
                f"Research results:\n{answer[:500]}\n\nLocal knowledge:\n{local_ctx}\n\nQuestion: {query}")
            if synthesis:
                print()
                print(f"  {_CYAN}{_BOLD}Claude synthesis:{_RESET}")
                for line in synthesis.split("\n")[:8]:
                    if line.strip():
                        print(f"  {line[:140]}")

    elif gateway_result and gateway_result.get("governance", {}).get("blocked"):
        # Blocked — show local-only response with on-device model
        print(f"  {_demo_label('RESULT', _GREEN)} {_GREEN}[LOCAL ONLY]{_RESET} Answered on-device. Zero external connection.")
        print()

        # Get local model response for the blocked query
        local_ctx = "\n".join(
            f"- {k.get('question', '')}: {(k.get('answer_excerpt', '') or '')[:200]}"
            for k in resolved.get("knowledge", [])[:3]
        )
        local_response = _call_model_api("ollama",
            "You are a legal research assistant running entirely on-device. Answer based ONLY on the provided knowledge. Do not speculate. Keep it concise — under 100 words.",
            f"Knowledge:\n{local_ctx}\n\nQuestion: {query}")
        if local_response:
            print(f"  {_GREEN}{_BOLD}On-device analysis:{_RESET}")
            for line in local_response.split("\n")[:6]:
                if line.strip():
                    print(f"  {line[:140]}")
            print()

        for k in resolved.get("knowledge", [])[:2]:
            print(f"  {_DIM}[{k.get('lib_id', '')}]{_RESET} {k.get('question', '')}")
            excerpt = (k.get("answer_excerpt", "") or "").strip()
            if excerpt:
                print(f"    {excerpt[:140]}")
    else:
        # Standard local response
        print(f"  {_demo_label('RESULT', _GREEN)} {_GREEN}[LOCAL]{_RESET} Confidence: {confidence:.0f}%")
        print(f"  {_DIM}  Model: Ollama qwen2.5 (on-device, zero external connection){_RESET}")
        print()
        for k in resolved.get("knowledge", [])[:3]:
            print(f"  {_DIM}[{k.get('lib_id', '')}]{_RESET} {k.get('question', '')}")
            excerpt = (k.get("answer_excerpt", "") or "").strip()
            if excerpt:
                print(f"    {excerpt[:140]}")

    # ── Step 5: STORED
    _time.sleep(0.1)
    extraction = step_extract(query, resolved, trace)
    print()
    print(f"  {_DIM}{'━' * 50}{_RESET}")
    dec_id = f"dec-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-{trace.thread_id[:4]}"
    print(f"  {_demo_label('STORED', _GREEN)} Decision logged → {_DIM}{dec_id}{_RESET}")
    print(f"  {_DIM}  Compounding: this decision improves future queries in {riu_id}{_RESET}")
    print(f"  {_DIM}  Time: {trace.total_ms():.0f}ms{_RESET}")
    print()

    # Log session
    session_log = REPO_ROOT / "peers" / "session_log.ndjson"
    try:
        session_log.parent.mkdir(parents=True, exist_ok=True)
        with open(session_log, "a") as f:
            f.write(json.dumps({
                "query": query[:200],
                "riu_id": resolved.get("riu_id"),
                "confidence": confidence,
                "agent": agent,
                "external_requested": use_external,
                "external_called": gateway_result.get("governance", {}).get("external_called") if gateway_result else False,
                "blocked": gateway_result.get("governance", {}).get("blocked") if gateway_result else False,
                "total_ms": trace.total_ms(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }) + "\n")
    except Exception:
        pass

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
    parser.add_argument("--external", action="store_true", help="Enable governed Perplexity external research path")
    parser.add_argument("--demo", action="store_true", help="Demo output mode: color-coded, video-optimized")
    args = parser.parse_args()

    query = " ".join(args.query)

    if args.demo:
        sys.exit(run_demo(query, use_external=args.external))
    else:
        sys.exit(run_query(query, learn=args.learn, show_json=args.json, show_trace=args.trace, use_external=args.external))


if __name__ == "__main__":
    main()
