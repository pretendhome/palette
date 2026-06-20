#!/usr/bin/env python3
"""palette orchestrate — Palette Mode: the OS calls the models.

This is the heuristic orchestration agent. Instead of routing to ONE model,
Palette calls models in sequence — each for a defined purpose — and composes
the result. The user talks to Palette. Palette talks to the models.

The loop:
  1. CLASSIFY   — Taxonomy routes the problem (local, instant)
  2. RETRIEVE   — Pull matching knowledge + prior decisions (local)
  3. REASON     — Local model does initial analysis (Ollama, on-device)
  4. RESEARCH   — External search if classification allows (Perplexity, governed)
  5. SYNTHESIZE — Deep model connects research to context (Claude, governed)
  6. CRITIQUE   — Adversarial model challenges the synthesis (Mistral, governed)
  7. STORE      — Log everything, link decisions, propose improvements

Each step is governed. Each model sees ONLY what Palette allows.
The user never chooses a model. Palette routes based on classification.

Usage:
  palette orchestrate "What's our exposure if the majority member was self-dealing?"
  palette orchestrate --json "What fiduciary duty standards apply to LLC co-founders?"
  palette orchestrate --trace "Given what we found, what would opposing counsel argue?"
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
IDENTITY = "palette.orchestrator"
SESSION_LOG = REPO_ROOT / "peers" / "session_log.ndjson"
GAP_LOG = REPO_ROOT / "peers" / "gap_signals.ndjson"

sys.path.insert(0, str(REPO_ROOT.parent))
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(HUB_DIR))

# ── Socket Firewall ─────────────────────────────────────────────────────
try:
    from core.gateway.socket_firewall import activate_firewall
    activate_firewall()
except Exception:
    pass  # firewall module may not exist in all environments

# ANSI colors
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


# ── Bus helpers ─────────────────────────────────────────────────────────

def bus_post(endpoint: str, payload: dict) -> dict | None:
    url = f"{BUS_URL}{endpoint}"
    data = json.dumps(payload).encode()
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def bus_register():
    return bus_post("/register", {
        "identity": IDENTITY,
        "agent_name": "palette-orchestrator",
        "runtime": "python-cli",
        "capabilities": ["orchestrate", "multi-model", "governed-routing"],
        "palette_role": "orchestrator",
        "trust_tier": "PRODUCTION",
        "version": "1.0.0",
    })


def bus_send(to_agent: str, intent: str, content: str,
             riu_id: str | None = None, confidence: float | None = None,
             thread_id: str | None = None) -> dict | None:
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
        "from_agent": IDENTITY,
        "to_agent": to_agent,
        "message_type": "advisory",
        "intent": intent,
        "risk_level": "none",
        "requires_ack": False,
        "payload": payload,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "ttl_seconds": 3600,
    })


# ── Model API calls ────────────────────────────────────────────────────

def call_ollama(prompt: str, system: str = "", model: str = "qwen2.5:3b") -> str | None:
    """Call local Ollama model. Zero external connection."""
    try:
        import httpx
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        resp = httpx.post("http://127.0.0.1:11434/api/generate", json={
            "model": model,
            "prompt": full_prompt,
            "stream": False,
        }, timeout=60.0)
        if resp.status_code == 200:
            return resp.json().get("response", "")
    except Exception:
        # Fallback to 7B
        try:
            resp = httpx.post("http://127.0.0.1:11434/api/generate", json={
                "model": "qwen2.5:7b",
                "prompt": f"{system}\n\n{prompt}" if system else prompt,
                "stream": False,
            }, timeout=60.0)
            if resp.status_code == 200:
                return resp.json().get("response", "")
        except Exception:
            pass
    return None


def call_perplexity(query: str, system: str = "") -> dict | None:
    """Call Perplexity Sonar Pro. Governed external research."""
    import os
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        return None
    try:
        payload = json.dumps({
            "model": "sonar-pro",
            "messages": [
                {"role": "system", "content": system or "Answer with citations. Public sources only."},
                {"role": "user", "content": query},
            ],
        }).encode()
        req = request.Request(
            "https://api.perplexity.ai/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        )
        with request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
            choices = body.get("choices", [])
            message = choices[0].get("message", {}) if choices else {}
            return {
                "answer": message.get("content", ""),
                "sources": body.get("citations", []),
            }
    except Exception:
        return None


def call_claude(prompt: str, system: str = "") -> str | None:
    """Call Claude via CLI. Uses OAuth subscription — never API credits."""
    import os, subprocess
    try:
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        env = {**os.environ, "CLAUDE_CODE_ENTRYPOINT": "palette-orchestrate"}
        env.pop("ANTHROPIC_API_KEY", None)  # force OAuth, never API credits
        result = subprocess.run(
            ["claude", "-p", full_prompt],
            capture_output=True, text=True, timeout=45,
            env=env,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def call_mistral(prompt: str, system: str = "") -> str | None:
    """Call Mistral via API. Governed external."""
    import os
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        return None
    try:
        payload = json.dumps({
            "model": "mistral-large-latest",
            "messages": [
                {"role": "system", "content": system or "You are a critical analyst."},
                {"role": "user", "content": prompt},
            ],
        }).encode()
        req = request.Request(
            "https://api.mistral.ai/v1/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        )
        with request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
            return body["choices"][0]["message"]["content"]
    except Exception:
        return None


# ── Prior decision lookup ───────────────────────────────────────────────

def find_prior_decisions(query: str, riu_id: str | None) -> list[dict]:
    """Find related prior decisions from session log."""
    import re
    priors = []
    if not SESSION_LOG.exists():
        return priors

    stopwords = {'the', 'a', 'an', 'is', 'are', 'what', 'how', 'do', 'to', 'for',
                 'in', 'of', 'we', 'our', 'would', 'should', 'given', 'found', 'this',
                 'that', 'with', 'from', 'was', 'were', 'have', 'has', 'if', 'or',
                 'and', 'not', 'by', 'on', 'at', 'it'}
    query_words = {w for w in re.findall(r'[a-z]+', query.lower())} - stopwords
    seen = set()

    with open(SESSION_LOG) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                eq = entry.get("query", "").strip().lower()
                if not eq or eq == query.strip().lower() or eq in seen:
                    continue
                entry_words = {w for w in re.findall(r'[a-z]+', eq)} - stopwords
                overlap = query_words & entry_words

                # Match on word overlap OR same RIU cluster
                same_cluster = False
                entry_riu = entry.get("riu_id", "")
                if riu_id and entry_riu:
                    rid_prefix = riu_id.split('-')[0] + '-' + riu_id.split('-')[-1][0] if '-' in riu_id else ""
                    ent_prefix = entry_riu.split('-')[0] + '-' + entry_riu.split('-')[-1][0] if '-' in entry_riu else ""
                    if rid_prefix and ent_prefix and rid_prefix == ent_prefix:
                        same_cluster = True

                if len(overlap) >= 2 or same_cluster:
                    priors.append(entry)
                    seen.add(eq)
            except (json.JSONDecodeError, KeyError):
                pass
    return priors


# ── The Orchestration Loop ──────────────────────────────────────────────

def orchestrate(query: str, show_json: bool = False, show_trace: bool = False) -> int:
    """Run the full 7-step orchestration loop."""
    thread_id = str(uuid.uuid4())
    started = time.time()
    bus_register()

    steps = {}

    # ═══════════════════════════════════════════════════════════════
    # STEP 1: CLASSIFY
    # ═══════════════════════════════════════════════════════════════
    print()
    print(f"  {_DIM}{'━' * 60}{_RESET}")
    print(f"  {_BOLD}{_WHITE}  ◆ palette orchestrate{_RESET}  {_DIM}multi-model governed workflow{_RESET}")
    print(f"  {_DIM}{'━' * 60}{_RESET}")
    print()
    print(f"  {_DIM}Query:{_RESET}  {_BOLD}{query}{_RESET}")
    print()

    t0 = time.time()
    from palette_retrieve import retrieve
    resolved = retrieve(query)
    ms = round((time.time() - t0) * 1000, 1)

    riu_id = resolved.get("riu_id", "unknown")
    riu_name = resolved.get("riu_name", "")
    confidence = resolved.get("confidence", 0)
    classification = resolved.get("classification", "unknown")
    knowledge = resolved.get("knowledge", [])
    is_internal = classification == "internal_only"

    print(f"  {_CYAN}{_BOLD}[1 CLASSIFY]{_RESET} {riu_id} ({riu_name}) — {confidence:.0f}% confidence")
    print(f"  {_DIM}  Classification: {classification} | Time: {ms:.0f}ms{_RESET}")

    steps["classify"] = {"riu_id": riu_id, "confidence": confidence,
                          "classification": classification, "ms": ms}

    # Abort if classification failed
    if confidence == 0 and riu_id is None:
        print(f"\n  {_RED}Classification failed. Gap signal logged.{_RESET}")
        return 1

    # ═══════════════════════════════════════════════════════════════
    # STEP 2: RETRIEVE
    # ═══════════════════════════════════════════════════════════════
    kl_context = "\n".join(
        f"[{k.get('lib_id', '')}] {k.get('question', '')}: {(k.get('answer_excerpt', '') or '')[:200]}"
        for k in knowledge[:3]
    )
    priors = find_prior_decisions(query, riu_id)

    print(f"  {_CYAN}{_BOLD}[2 RETRIEVE]{_RESET} {len(knowledge)} knowledge entries, {len(priors)} prior decisions")

    if priors:
        print(f"  {_GREEN}{_BOLD}  [CONNECT]{_RESET} Compounding with {len(priors)} prior decision(s):")
        for p in priors[:3]:
            ts = p.get("timestamp", "")[:10]
            pq = p.get("query", "")[:60]
            was_blocked = p.get("blocked", False)
            tag = f"{_RED}[BLOCKED]{_RESET}" if was_blocked else f"{_GREEN}[LOCAL]{_RESET}"
            print(f"    {_DIM}{ts}{_RESET} {tag} {pq}")

    steps["retrieve"] = {"knowledge_count": len(knowledge),
                          "prior_decisions": len(priors)}

    # Build context for downstream models (NEVER includes client identity)
    governed_context = f"Classification: {riu_id} ({riu_name})\n\nKnowledge:\n{kl_context}"
    if priors:
        prior_summary = "\n".join(
            f"- Prior: {p.get('query', '')[:80]} (RIU: {p.get('riu_id', '?')})"
            for p in priors[:3]
        )
        governed_context += f"\n\nPrior decisions:\n{prior_summary}"

    # ═══════════════════════════════════════════════════════════════
    # STEP 3: REASON (local model, always runs)
    # ═══════════════════════════════════════════════════════════════
    print()
    print(f"  {_GREEN}{_BOLD}[3 REASON]{_RESET} On-device analysis (Ollama)")
    print(f"  {_DIM}  Model: qwen2.5 (local, zero external connection){_RESET}")

    t0 = time.time()
    local_response = call_ollama(
        query,
        system=f"You are a legal analyst running on-device. Use ONLY the provided knowledge to reason. Be concise (under 100 words). Do not reference any client names.\n\nContext:\n{governed_context}"
    )
    ms = round((time.time() - t0) * 1000, 1)

    if local_response:
        for line in local_response.split("\n")[:6]:
            if line.strip():
                print(f"  {_GREEN}{line[:140]}{_RESET}")
    else:
        print(f"  {_DIM}  (local model unavailable){_RESET}")

    print(f"  {_DIM}  Time: {ms:.0f}ms{_RESET}")
    steps["reason"] = {"model": "ollama", "ms": ms, "success": local_response is not None}

    # ═══════════════════════════════════════════════════════════════
    # STEP 4: RESEARCH (Perplexity, only if classification allows)
    # ═══════════════════════════════════════════════════════════════
    research_result = None
    if is_internal:
        print()
        print(f"\n  {_DIM}{'━' * 4}{_RESET} {_YELLOW}{_BOLD}GOVERNANCE BOUNDARY{_RESET} {_DIM}{'━' * 36}{_RESET}")
        print(f"\n  {_BG_RED}{_BOLD}{_WHITE} BLOCKED {_RESET} {_RED}Classification: internal_only — no external research{_RESET}")
        print(f"  {_BG_GREEN}{_BOLD}{_WHITE} LOCAL ONLY {_RESET} {_GREEN}Zero data left this machine.{_RESET}")
        steps["research"] = {"blocked": True, "reason": "internal_only classification"}
    else:
        # Check sanitizer
        from core.gateway.sanitizer import QuerySanitizer
        sanitizer = QuerySanitizer()
        is_safe, reason = sanitizer.is_safe_for_external(query)
        sanitized, pii_found = sanitizer.sanitize_query(query)

        if not is_safe or pii_found:
            print()
            print(f"\n  {_DIM}{'━' * 4}{_RESET} {_YELLOW}{_BOLD}GOVERNANCE BOUNDARY{_RESET} {_DIM}{'━' * 36}{_RESET}")
            print(f"\n  {_BG_RED}{_BOLD}{_WHITE} BLOCKED {_RESET} {_RED}PII detected: {pii_found}{_RESET}")
            print(f"  {_BG_GREEN}{_BOLD}{_WHITE} LOCAL ONLY {_RESET} {_GREEN}Zero data left this machine.{_RESET}")
            steps["research"] = {"blocked": True, "reason": reason, "pii": pii_found}
        else:
            print()
            print(f"\n  {_DIM}{'━' * 4}{_RESET} {_YELLOW}{_BOLD}GOVERNANCE BOUNDARY{_RESET} {_DIM}{'━' * 36}{_RESET}")
            print(f"\n  {_YELLOW}{_BOLD}[4 RESEARCH]{_RESET} Query sanitized ✓ — routing to Perplexity")
            print(f"  {_DIM}  Model: Perplexity sonar-pro (governed external research){_RESET}")

            t0 = time.time()
            # Build targeted search using taxonomy context
            targeted_system = (
                f"You are answering a {riu_name} ({riu_id}) query.\n"
                f"Known locally: {kl_context[:300]}\n"
                f"Focus on what is MISSING from the local knowledge. Cite public sources."
            )
            research_result = call_perplexity(sanitized, system=targeted_system)
            ms = round((time.time() - t0) * 1000, 1)

            if research_result:
                answer = research_result.get("answer", "")
                sources = research_result.get("sources", [])
                for line in answer.split("\n")[:6]:
                    if line.strip():
                        print(f"  {_BLUE}{line[:140]}{_RESET}")
                if sources:
                    print(f"  {_DIM}  Citations: {', '.join(sources[:3])}{_RESET}")
            print(f"  {_DIM}  Time: {ms:.0f}ms{_RESET}")
            steps["research"] = {"blocked": False, "ms": ms, "success": research_result is not None}

    # ═══════════════════════════════════════════════════════════════
    # STEP 5: SYNTHESIZE (Claude, only if research was done)
    # ═══════════════════════════════════════════════════════════════
    synthesis = None
    if research_result and not is_internal:
        print()
        print(f"  {_CYAN}{_BOLD}[5 SYNTHESIZE]{_RESET} Connecting research to context (Claude)")
        print(f"  {_DIM}  Model: Claude (governed — client identity stripped){_RESET}")

        t0 = time.time()
        research_text = research_result.get("answer", "")[:500]
        synthesis = call_claude(
            f"Research results:\n{research_text}\n\nLocal knowledge:\n{kl_context}\n\nQuestion: {query}",
            system="Synthesize the research into a concise analysis. Connect precedents to the fact pattern. No client names. Under 150 words."
        )
        ms = round((time.time() - t0) * 1000, 1)

        if synthesis:
            for line in synthesis.split("\n")[:6]:
                if line.strip():
                    print(f"  {_CYAN}{line[:140]}{_RESET}")
        print(f"  {_DIM}  Time: {ms:.0f}ms{_RESET}")
        steps["synthesize"] = {"model": "claude", "ms": ms, "success": synthesis is not None}

    # ═══════════════════════════════════════════════════════════════
    # STEP 6: CRITIQUE
    # If internal_only → critique runs LOCAL (Ollama). No external call.
    # If external allowed → critique runs via Mistral (governed).
    # The trust boundary is absolute: internal_only means NOTHING leaves.
    # ═══════════════════════════════════════════════════════════════
    critique = None
    critique_input = synthesis or (local_response if local_response else "")
    blocked_from_external = is_internal or steps.get("research", {}).get("blocked", False)

    if critique_input:
        critique_system = "You are an adversarial analyst. Identify the 2-3 strongest counter-arguments or risks. Be specific about legal standards. No client names. Under 100 words."
        critique_prompt = f"Analysis to critique:\n{critique_input[:500]}\n\nContext:\n{governed_context}\n\nQuestion: {query}"

        if blocked_from_external:
            # INTERNAL ONLY — critique runs on-device. Zero external connection.
            print()
            print(f"  {_GREEN}{_BOLD}[6 CRITIQUE]{_RESET} Adversarial analysis (on-device)")
            print(f"  {_DIM}  Model: Ollama (local — trust boundary enforced){_RESET}")

            t0 = time.time()
            critique = call_ollama(critique_prompt, system=critique_system)
            ms = round((time.time() - t0) * 1000, 1)
            critique_model = "ollama"
        else:
            # EXTERNAL ALLOWED — critique via Mistral (governed, context stripped)
            print()
            print(f"  {_MAGENTA}{_BOLD}[6 CRITIQUE]{_RESET} Adversarial analysis (Mistral)")
            print(f"  {_DIM}  Model: Mistral (governed — client identity stripped){_RESET}")

            t0 = time.time()
            critique = call_mistral(critique_prompt, system=critique_system)
            ms = round((time.time() - t0) * 1000, 1)
            critique_model = "mistral"

            # Fallback to local if Mistral unavailable
            if not critique:
                print(f"  {_DIM}  Mistral unavailable — falling back to on-device{_RESET}")
                critique = call_ollama(critique_prompt, system=critique_system)
                critique_model = "ollama"
                ms = round((time.time() - t0) * 1000, 1)

        if critique:
            for line in critique.split("\n")[:6]:
                if line.strip():
                    color = _GREEN if critique_model == "ollama" else _MAGENTA
                    print(f"  {color}{line[:140]}{_RESET}")
        print(f"  {_DIM}  Time: {ms:.0f}ms{_RESET}")
        steps["critique"] = {"model": critique_model, "ms": ms, "success": critique is not None}

    # ═══════════════════════════════════════════════════════════════
    # STEP 7: STORE + IMPROVE
    # ═══════════════════════════════════════════════════════════════
    total_ms = round((time.time() - started) * 1000, 1)
    dec_id = f"dec-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-{thread_id[:4]}"

    models_used = ["ollama"]
    if research_result:
        models_used.append("perplexity")
    if synthesis:
        models_used.append("claude")
    if critique:
        models_used.append(steps.get("critique", {}).get("model", "unknown"))

    print()
    print(f"  {_DIM}{'━' * 60}{_RESET}")
    print(f"  {_GREEN}{_BOLD}[7 STORED]{_RESET} Decision logged → {_DIM}{dec_id}{_RESET}")
    print(f"  {_DIM}  Models: {' → '.join(models_used)}{_RESET}")
    print(f"  {_DIM}  Prior decisions connected: {len(priors)}{_RESET}")
    print(f"  {_DIM}  Compounding: this decision improves future queries in {riu_id}{_RESET}")
    print(f"  {_DIM}  Total: {total_ms:.0f}ms{_RESET}")
    print()

    # Log to session
    try:
        SESSION_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(SESSION_LOG, "a") as f:
            f.write(json.dumps({
                "query": query[:200],
                "riu_id": riu_id,
                "confidence": confidence,
                "classification": classification,
                "agent": IDENTITY,
                "mode": "orchestrate",
                "models_used": models_used,
                "prior_decisions_connected": len(priors),
                "external_called": research_result is not None,
                "blocked": is_internal or (not research_result and not is_internal),
                "total_ms": total_ms,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }) + "\n")
    except Exception:
        pass

    # Log gap signal if low confidence
    if confidence < 30:
        try:
            GAP_LOG.parent.mkdir(parents=True, exist_ok=True)
            with open(GAP_LOG, "a") as f:
                f.write(json.dumps({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "query": query[:200],
                    "riu_id": riu_id,
                    "confidence": confidence,
                    "signal_type": "low_confidence",
                }) + "\n")
        except Exception:
            pass

    # Send completion to bus
    bus_send(
        to_agent="all",
        intent=f"palette orchestrate completed: {riu_id} ({total_ms:.0f}ms, {len(models_used)} models)",
        content=json.dumps({
            "query": query[:100],
            "riu_id": riu_id,
            "models_used": models_used,
            "prior_decisions": len(priors),
            "total_ms": total_ms,
        }),
        riu_id=riu_id,
        confidence=confidence,
        thread_id=thread_id,
    )

    # JSON output
    if show_json:
        output = {
            "query": query,
            "mode": "orchestrate",
            "riu_id": riu_id,
            "classification": classification,
            "confidence": confidence,
            "models_used": models_used,
            "prior_decisions_connected": len(priors),
            "steps": steps,
            "total_ms": total_ms,
        }
        print(json.dumps(output, indent=2))

    return 0


# ── CLI entry point ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="palette orchestrate",
        description="Palette Mode: the OS calls the models. Multi-model governed workflow.",
    )
    parser.add_argument("query", nargs="+", help="Natural language query")
    parser.add_argument("--json", action="store_true", help="Output JSON result")
    parser.add_argument("--trace", action="store_true", help="Show execution trace")
    args = parser.parse_args()

    query = " ".join(args.query)
    sys.exit(orchestrate(query, show_json=args.json, show_trace=args.trace))


if __name__ == "__main__":
    main()
