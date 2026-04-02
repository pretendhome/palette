#!/usr/bin/env python3
"""
resolver_service.py — Palette Resolver as HTTP microservice (model-agnostic)

The universal front door. Takes raw text from ANY surface (Telegram bot,
web URL, voice/Rime, CLI) and returns a grounded prompt + routing metadata.

Pipeline:
  1. LLM classifies input into 1 of 7 problem clusters
  2. Cluster filters knowledge library to relevant RIUs
  3. LLM matches to best RIU with confidence + runner-up
  4. RIU brings the library entry (question, answer, tags)
  5. LLM refines into a grounded prompt + suggested agent

Works with ANY OpenAI-compatible API: Perplexity, Mistral, OpenRouter, Groq, etc.
Configure via environment variables:
  RESOLVER_API_KEY     — API key (falls back to PERPLEXITY_API_KEY)
  RESOLVER_API_URL     — base URL (default: https://api.perplexity.ai)
  RESOLVER_MODEL       — model name (default: sonar)
  RESOLVER_REFINE_MODEL — model for refinement step (default: same as RESOLVER_MODEL)

Endpoint:
  POST /resolve
  Body: { "input": "user text", "session_id": "optional", "context": "optional" }

Usage:
  python3 resolver_service.py                    # starts on port 8788
  RESOLVER_PORT=9000 python3 resolver_service.py
"""
from __future__ import annotations

import json
import os
import sys
import datetime
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional

import httpx
import yaml

# ── Config ──────────────────────────────────────────────────────────────────

PORT = int(os.environ.get("RESOLVER_PORT", os.environ.get("PORT", 8788)))

# LLM provider — any OpenAI-compatible API
API_KEY = (
    os.environ.get("RESOLVER_API_KEY")
    or os.environ.get("PERPLEXITY_API_KEY")
    or os.environ.get("MISTRAL_API_KEY")
    or os.environ.get("ANTHROPIC_API_KEY", "")
)
API_URL = os.environ.get("RESOLVER_API_URL", "https://api.perplexity.ai")
MODEL = os.environ.get("RESOLVER_MODEL", "sonar")
REFINE_MODEL = os.environ.get("RESOLVER_REFINE_MODEL", MODEL)

# Knowledge library path
_HERE = os.path.dirname(os.path.abspath(__file__))
_KL_CANDIDATES = [
    os.path.normpath(os.path.join(_HERE, "..", "knowledge-library", "v1.4",
                                  "palette_knowledge_library_v1.4.yaml")),
    "/root/fde/palette/knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml",
]

CONFIDENCE_THRESHOLD = 75
SECOND_TURN_FLOOR = 55

CLUSTER_NAMES = [
    "Intake_and_Convergence",
    "Human_to_System_Translation",
    "Systems_Integration",
    "Data_Semantics_and_Quality",
    "Reliability_and_Failure_Handling",
    "Operationalization_and_Scaling",
    "Trust_Governance_and_Adoption",
]

CLUSTER_DESCRIPTIONS = (
    "1. Intake_and_Convergence — gathering requirements, aligning stakeholders, "
    "defining goals, forcing convergence on competing definitions\n"
    "2. Human_to_System_Translation — turning human intent into machine-readable "
    "specs, RIU mapping, prompt engineering, intent resolution\n"
    "3. Systems_Integration — connecting systems, APIs, data flows, infrastructure "
    "wiring, service mesh\n"
    "4. Data_Semantics_and_Quality — data consistency, meaning, quality issues, "
    "schema design, data contracts\n"
    "5. Reliability_and_Failure_Handling — uptime, resilience, failure recovery, "
    "debugging, root-cause analysis\n"
    "6. Operationalization_and_Scaling — deployment, CI/CD, monitoring, scaling, "
    "cost optimization, production operations\n"
    "7. Trust_Governance_and_Adoption — security, compliance, user adoption, "
    "change management, organizational risk"
)


# ── Data structures ──────────────────────────────────────────────────────────

class RIUEntry:
    __slots__ = ("id", "question", "answer", "problem_type", "tags")
    def __init__(self, id: str, question: str, answer: str, problem_type: str, tags: list):
        self.id = id
        self.question = question
        self.answer = answer
        self.problem_type = problem_type
        self.tags = tags


# ── Knowledge library ────────────────────────────────────────────────────────

_library: list[RIUEntry] = []


def load_library() -> list[RIUEntry]:
    kl_path = next((p for p in _KL_CANDIDATES if os.path.exists(p)), None)
    if not kl_path:
        _log(f"knowledge library not found in any candidate path")
        return []
    with open(kl_path) as f:
        lib = yaml.safe_load(f)
    entries = []
    for q in lib.get("library_questions", []):
        entries.append(RIUEntry(
            id=q.get("id", ""),
            question=q.get("question", ""),
            answer=q.get("answer", ""),
            problem_type=q.get("problem_type", ""),
            tags=q.get("tags", []),
        ))
    return entries


def _get_library() -> list[RIUEntry]:
    global _library
    if not _library:
        _library = load_library()
        _log(f"loaded {len(_library)} RIUs from knowledge library")
    return _library


def get_cluster_rius(library: list[RIUEntry], cluster: str) -> list[RIUEntry]:
    return [r for r in library if r.problem_type == cluster]


def format_rius_for_prompt(rius: list[RIUEntry]) -> str:
    lines = []
    for r in rius:
        lines.append(f"{r.id}: {r.question}")
        if r.tags:
            lines.append(f"  tags: {', '.join(r.tags)}")
    return "\n".join(lines)


# ── LLM calls (model-agnostic) ──────────────────────────────────────────────

def _llm_call(prompt: str, model: str = "", max_tokens: int = 300) -> str:
    """Call any OpenAI-compatible chat completions API. Returns the text response."""
    model = model or MODEL
    with httpx.Client(timeout=30.0) as client:
        resp = client.post(
            f"{API_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
            },
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


def _parse_json(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        start = 1
        end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
        text = "\n".join(lines[start:end]).strip()
    start_idx = text.find("{")
    if start_idx >= 0:
        depth = 0
        for i, ch in enumerate(text[start_idx:], start_idx):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    text = text[start_idx : i + 1]
                    break
    return json.loads(text)


def classify_cluster(raw_input: str, history_context: str) -> tuple[str, int, str, int]:
    """Classify input into one of the 7 problem-type clusters."""
    context_block = (
        f"\nAdditional context from conversation:\n{history_context}"
        if history_context else ""
    )
    prompt = (
        f"Classify this user request into one of 7 problem categories.\n\n"
        f"User request: {raw_input}{context_block}\n\n"
        f"Categories:\n{CLUSTER_DESCRIPTIONS}\n\n"
        f"Return JSON only, no other text:\n"
        f'{{ "cluster": "category_name", "confidence": 0-100, '
        f'"runner_up": "category_name", "runner_up_confidence": 0-100 }}'
    )
    try:
        result = _parse_json(_llm_call(prompt, max_tokens=200))
        cluster = result.get("cluster", CLUSTER_NAMES[0])
        if cluster not in CLUSTER_NAMES:
            cluster = CLUSTER_NAMES[0]
        return (
            cluster,
            int(result.get("confidence", 50)),
            result.get("runner_up", ""),
            int(result.get("runner_up_confidence", 0)),
        )
    except Exception as e:
        _log(f"cluster classify error: {e}")
        return CLUSTER_NAMES[0], 40, "", 0


def match_riu(
    raw_input: str, history_context: str, cluster_rius: list[RIUEntry]
) -> tuple[str, int, str, int, Optional[str]]:
    """Match input to the most relevant RIU within a cluster."""
    if not cluster_rius:
        return "", 0, "", 0, "which type of challenge you're facing"

    riu_list = format_rius_for_prompt(cluster_rius)
    context_block = (
        f"\nClarifications gathered:\n{history_context}"
        if history_context else ""
    )
    prompt = (
        f"Match this user request to the most relevant RIU (Research Intent Unit).\n\n"
        f"User request: {raw_input}{context_block}\n\n"
        f"Available RIUs:\n{riu_list}\n\n"
        f"Find the best match. If two are close, identify the ONE piece of information "
        f"that would break the tie.\n\n"
        f"Return JSON only:\n"
        f'{{ "top_riu": "LIB-XXX", "confidence": 0-100, '
        f'"runner_up": "LIB-YYY or null", "runner_up_confidence": 0-100, '
        f'"missing_slot": "specific discriminating info needed, or null if confident" }}'
    )
    try:
        result = _parse_json(_llm_call(prompt, max_tokens=250))
        runner_up_id = result.get("runner_up") or ""
        if runner_up_id == "null":
            runner_up_id = ""
        missing_slot = result.get("missing_slot")
        if missing_slot in ("null", ""):
            missing_slot = None
        return (
            result.get("top_riu", ""),
            int(result.get("confidence", 40)),
            runner_up_id,
            int(result.get("runner_up_confidence", 0)),
            missing_slot,
        )
    except Exception as e:
        _log(f"RIU match error: {e}")
        return "", 0, "", 0, "more details about your specific situation"


def refine_prompt(
    raw_input: str, riu: RIUEntry, history_context: str
) -> dict:
    """Produce a clean, refined task description using the matched RIU context."""
    context_block = (
        f"\nClarifications gathered:\n{history_context}"
        if history_context else ""
    )
    prompt = (
        f"You are a helpful assistant responding to a user. "
        f"Write a concise, direct response to their request.\n\n"
        f"User said: {raw_input}{context_block}\n\n"
        f"You know this about the topic: {riu.question}\n"
        f"Key insight: {riu.answer[:500]}\n\n"
        f"Rules:\n"
        f"1. Respond directly to the user in 2-4 sentences\n"
        f"2. Be conversational and helpful, not robotic\n"
        f"3. NEVER mention library IDs (LIB-XXX), RIU numbers, internal system names, "
        f"knowledge entries, or any backend plumbing\n"
        f"4. Use the knowledge to inform your answer, don't describe the knowledge\n"
        f"5. If the user asked for updates/brief, summarize what matters\n\n"
        f"Also choose the best specialist for follow-up:\n"
        f"  architect | builder | validator | researcher | debugger | monitor | narrator\n\n"
        f"Return JSON only:\n"
        f'{{ "refined_task": "your direct response to the user", '
        f'"decision_context": "what this informs", '
        f'"suggested_agent": "agent_name", '
        f'"confidence": 0-100 }}'
    )
    try:
        return _parse_json(_llm_call(prompt, model=REFINE_MODEL, max_tokens=600))
    except Exception as e:
        _log(f"refine error: {e}")
        return {
            "refined_task": raw_input,
            "decision_context": f"matched {riu.id}",
            "suggested_agent": "researcher",
            "confidence": 50,
        }


def generate_question(
    raw_input: str, riu_a: RIUEntry, riu_b: RIUEntry, missing_slot: Optional[str], turn: int
) -> str:
    """Generate ONE clarifying question."""
    discriminator = missing_slot or (
        f"whether you're dealing with '{riu_a.question[:80]}' "
        f"or '{riu_b.question[:80]}'"
    )
    brevity = " Keep it brief — we've already asked once." if turn > 0 else ""
    prompt = (
        f"You need one more piece of information to help this user.\n\n"
        f'The user said: "{raw_input}"\n\n'
        f"You're deciding between:\n"
        f"  Option A: {riu_a.question}\n"
        f"  Option B: {riu_b.question}\n\n"
        f"Key discriminator: {discriminator}\n\n"
        f"Write ONE specific, friendly question. One sentence. Conversational. "
        f"No multiple choice.{brevity}"
    )
    try:
        return _llm_call(prompt, max_tokens=100).strip().strip('"')
    except Exception as e:
        _log(f"question generation error: {e}")
        return missing_slot or "Could you tell me more about what you're trying to achieve?"


# ── Utilities ────────────────────────────────────────────────────────────────

_sessions: dict[str, dict] = {}


def _log(msg: str) -> None:
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[resolver-svc {ts}] {msg}", flush=True)


# ── Core resolve function ──────────────────────────────────────────────────

def resolve(
    raw_input: str,
    session_id: str = "",
    context: str = "",
) -> dict:
    """Run the full Resolver pipeline."""

    library = _get_library()

    # Session state
    session = _sessions.get(session_id, {}) if session_id else {}
    matched_cluster = session.get("cluster", "")
    clarification_history: list[dict] = list(session.get("history", []))
    turn = session.get("turn", 0)

    if session.get("last_question") and turn > 0:
        clarification_history.append({
            "question": session["last_question"],
            "answer": raw_input,
        })

    def history_str() -> str:
        parts = []
        if context:
            parts.append(f"Context: {context}")
        if clarification_history:
            parts.extend(
                f"Q: {t['question']}\nA: {t['answer']}"
                for t in clarification_history
            )
        return "\n".join(parts)

    # Step 1: Classify cluster
    if not matched_cluster:
        _log(f"classifying: {raw_input[:60]}")
        matched_cluster, cluster_conf, runner_up_c, _ = classify_cluster(
            raw_input, history_str()
        )
        _log(f"cluster: {matched_cluster} ({cluster_conf}%)")
    else:
        _log(f"cluster: {matched_cluster} (from session)")

    # Step 2: Match RIU
    cluster_rius = get_cluster_rius(library, matched_cluster)
    _log(f"matching in {matched_cluster} ({len(cluster_rius)} candidates)")

    top_id, confidence, runner_up_id, runner_up_conf, missing_slot = match_riu(
        raw_input, history_str(), cluster_rius
    )
    _log(f"match: {top_id} ({confidence}%)")

    # Step 3: Route on confidence
    threshold = SECOND_TURN_FLOOR if turn >= 1 else CONFIDENCE_THRESHOLD

    if top_id and confidence >= threshold:
        matched_riu = next((r for r in cluster_rius if r.id == top_id), None)
        if matched_riu:
            _log(f"confident → refining")
            refined = refine_prompt(raw_input, matched_riu, history_str())

            if session_id and session_id in _sessions:
                del _sessions[session_id]

            runner_up_riu = next((r for r in cluster_rius if r.id == runner_up_id), None)

            return {
                "status": "resolved",
                "riu_id": top_id,
                "confidence": confidence,
                "cluster": matched_cluster,
                "grounded_prompt": refined.get("refined_task", raw_input),
                "decision_context": refined.get("decision_context", ""),
                "suggested_agent": refined.get("suggested_agent", ""),
                "knowledge": {
                    "id": matched_riu.id,
                    "question": matched_riu.question,
                    "answer": matched_riu.answer[:500],
                    "tags": matched_riu.tags,
                },
                "runner_up": {
                    "riu_id": runner_up_id,
                    "confidence": runner_up_conf,
                    "question": runner_up_riu.question if runner_up_riu else "",
                } if runner_up_id else None,
            }

    # Max turns → out of scope
    if turn >= 3:
        if session_id and session_id in _sessions:
            del _sessions[session_id]
        return {
            "status": "out_of_scope",
            "confidence": confidence,
            "cluster": matched_cluster,
            "message": (
                "This request doesn't clearly match a known capability. "
                "Try rephrasing around a specific challenge or outcome."
            ),
            "best_candidate": {
                "riu_id": top_id,
                "confidence": confidence,
            } if top_id else None,
        }

    # Low confidence → clarify
    if not top_id:
        question = "What specific challenge or outcome are you trying to address?"
    else:
        riu_a = next((r for r in cluster_rius if r.id == top_id), None)
        riu_b = next((r for r in cluster_rius if r.id == runner_up_id), None)

        if riu_a and riu_b:
            _log(f"ambiguous: {top_id} vs {runner_up_id} → asking")
            question = generate_question(raw_input, riu_a, riu_b, missing_slot, turn)
        else:
            question = missing_slot or "Could you tell me more about what you're trying to achieve?"

    if session_id:
        _sessions[session_id] = {
            "cluster": matched_cluster,
            "history": clarification_history,
            "turn": turn + 1,
            "last_question": question,
        }

    return {
        "status": "clarify",
        "confidence": confidence,
        "cluster": matched_cluster,
        "question": question,
        "turn": turn + 1,
        "candidates": {
            "top": {"riu_id": top_id, "confidence": confidence} if top_id else None,
            "runner_up": {"riu_id": runner_up_id, "confidence": runner_up_conf} if runner_up_id else None,
        },
    }


# ── HTTP handler ───────────────────────────────────────────────────────────

class ResolverHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/resolve":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length)) if length else {}
            except (json.JSONDecodeError, ValueError):
                self._json(400, {"error": "Invalid JSON"})
                return

            raw_input = body.get("input", "").strip()
            if not raw_input:
                self._json(400, {"error": "Missing 'input' field"})
                return

            try:
                result = resolve(raw_input, body.get("session_id", ""), body.get("context", ""))
                self._json(200, result)
            except Exception as e:
                _log(f"resolve error: {e}")
                self._json(500, {"error": str(e)})
            return

        self._json(404, {"error": "Not found"})

    def do_GET(self):
        if self.path == "/health":
            lib = _get_library()
            self._json(200, {
                "status": "ok",
                "model": MODEL,
                "api_url": API_URL,
                "library_size": len(lib),
                "sessions_active": len(_sessions),
            })
            return
        self._json(404, {"error": "Not found"})

    def _json(self, status: int, data: dict):
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    if not API_KEY:
        print("[resolver-svc] No API key found. Set RESOLVER_API_KEY, "
              "PERPLEXITY_API_KEY, or MISTRAL_API_KEY.", flush=True)
        sys.exit(1)

    _log(f"provider: {API_URL} | model: {MODEL} | refine: {REFINE_MODEL}")
    _get_library()

    server = HTTPServer(("0.0.0.0", PORT), ResolverHandler)
    _log(f"listening on port {PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _log("stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
