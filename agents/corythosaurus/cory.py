#!/usr/bin/env python3
"""
cory.py — Corythosaurus (Cory) Intent Resolver
Palette Workflow Agent v0.1

The front door of Palette. Maps raw user input to the right RIU from the
111-entry knowledge library, asks ONE clarifying question when ambiguous,
and hands a clean, refined HandoffPacket to the Orchestrator.

Cory never executes. Cory never decides. Cory listens until it understands,
then passes the baton with full context attached.

────────────────────────────────────────────────────────────────────────────
Conversation state is stateless per invocation — state carries through
HandoffPacket.payload across multiple turns:

  Turn 0:   raw input → classify cluster → match RIU → complete | clarify
  Turn 1+:  raw input + history → re-match in known cluster → complete |
            clarify | out-of-scope (if turn >= max_turns)

────────────────────────────────────────────────────────────────────────────
Input:  --input "raw user text"  (CLI)  or  HandoffPacket JSON on stdin
Output: HandoffResult JSON to stdout

HandoffPacket.payload fields read:
  raw_input              original user text (preserved across turns)
  matched_cluster        cluster from turn 0 (preserved)
  clarification_history  [{question, answer}, ...]
  turn                   current turn number (0-indexed)
  last_question          question asked in prior turn (for CLI re-invocation)
  max_turns              max clarification rounds before out-of-scope (default: 3)

HandoffResult statuses:
  complete      → output.refined_packet  (clean HandoffPacket for Orch)
  clarify       → output.question, output.turn, output.payload_for_next_turn
  out-of-scope  → output.message, output.guidance
  error         → blockers[]
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Optional


# ── Constants ─────────────────────────────────────────────────────────────────

_HERE = os.path.dirname(os.path.abspath(__file__))

KNOWLEDGE_LIBRARY_PATH = os.path.normpath(os.path.join(
    _HERE, "..", "..", "knowledge-library",
    "v1.2", "palette_knowledge_library_v1.2.yaml",
))
HISTORY_PATH = os.path.join(_HERE, "history.jsonl")

DEFAULT_MAX_TURNS    = 3
CONFIDENCE_THRESHOLD = 75   # below this → ask a question
SECOND_TURN_FLOOR    = 55   # lower bar after at least one clarification

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


# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class RIUEntry:
    id:           str
    question:     str
    answer:       str
    problem_type: str
    tags:         list[str] = field(default_factory=list)


# ── Knowledge library ─────────────────────────────────────────────────────────

def load_library() -> list[RIUEntry]:
    """Load and parse the knowledge library YAML into RIUEntry objects."""
    if not os.path.exists(KNOWLEDGE_LIBRARY_PATH):
        progress(f"knowledge library not found at {KNOWLEDGE_LIBRARY_PATH}")
        return []

    try:
        import yaml
    except ImportError:
        progress("pyyaml not installed — pip install pyyaml")
        return []

    try:
        with open(KNOWLEDGE_LIBRARY_PATH) as f:
            lib = yaml.safe_load(f)
    except Exception as e:
        progress(f"knowledge library read error: {e}")
        return []

    entries = []
    for q in lib.get("library_questions", []):
        entries.append(RIUEntry(
            id           = q.get("id", ""),
            question     = q.get("question", ""),
            answer       = q.get("answer", ""),
            problem_type = q.get("problem_type", ""),
            tags         = q.get("tags", []),
        ))
    return entries


def get_cluster_rius(library: list[RIUEntry], cluster: str) -> list[RIUEntry]:
    return [r for r in library if r.problem_type == cluster]


def format_rius_for_prompt(rius: list[RIUEntry]) -> str:
    lines = []
    for r in rius:
        lines.append(f"{r.id}: {r.question}")
        if r.tags:
            lines.append(f"  tags: {', '.join(r.tags)}")
    return "\n".join(lines)


# ── History store ─────────────────────────────────────────────────────────────

def load_history(riu_id: str, limit: int = 5) -> list[dict]:
    """Load recent successful matches for a specific RIU (for prompt refinement)."""
    if not os.path.exists(HISTORY_PATH):
        return []
    matches = []
    try:
        with open(HISTORY_PATH) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get("riu_id") == riu_id and entry.get("outcome") == "success":
                        matches.append(entry)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return []
    return sorted(matches, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]


def save_history(riu_id: str, raw_input: str, refined_task: str) -> None:
    """Append a successful resolution to the history log."""
    entry = {
        "riu_id":       riu_id,
        "raw_input":    raw_input[:200],
        "refined_task": refined_task[:400],
        "outcome":      "success",
        "timestamp":    _now(),
    }
    try:
        with open(HISTORY_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError as e:
        progress(f"history write error: {e}")


# ── Utilities ─────────────────────────────────────────────────────────────────

def progress(msg: str) -> None:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    print(f"[cory {ts}] {msg}", file=sys.stderr, flush=True)


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_json(text: str) -> dict:
    """
    Parse JSON from Claude responses robustly:
    - strips markdown code fences (```json ... ```)
    - extracts the first complete JSON object regardless of surrounding text
    """
    text = text.strip()
    # Strip markdown code fences
    if text.startswith("```"):
        lines = text.splitlines()
        start = 1
        end   = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
        text  = "\n".join(lines[start:end]).strip()
    # Extract first complete {...} object — ignore any trailing text
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


# ── Claude calls ──────────────────────────────────────────────────────────────

def classify_cluster(
    raw_input:       str,
    history_context: str,
    client,
) -> tuple[str, int, str, int]:
    """
    Classify input into one of the 7 problem-type clusters.
    Returns (cluster, confidence, runner_up, runner_up_confidence).
    Uses Haiku — this runs on every input, must be fast and cheap.
    """
    context_block = (
        f"\nAdditional context from conversation:\n{history_context}"
        if history_context else ""
    )
    prompt = (
        f"Classify this user request into one of 7 problem categories.\n\n"
        f"User request: {raw_input}{context_block}\n\n"
        f"Categories:\n{CLUSTER_DESCRIPTIONS}\n\n"
        f"Return JSON only, no prose:\n"
        f'{{ "cluster": "category_name", "confidence": 0-100, '
        f'"runner_up": "category_name", "runner_up_confidence": 0-100 }}'
    )

    message = client.messages.create(
        model      = "claude-haiku-4-5-20251001",
        max_tokens = 200,
        messages   = [{"role": "user", "content": prompt}],
    )

    try:
        result         = _parse_json(message.content[0].text)
        cluster        = result.get("cluster", CLUSTER_NAMES[0])
        confidence     = int(result.get("confidence", 50))
        runner_up      = result.get("runner_up", "")
        runner_up_conf = int(result.get("runner_up_confidence", 0))
        if cluster not in CLUSTER_NAMES:
            cluster = CLUSTER_NAMES[0]
        return cluster, confidence, runner_up, runner_up_conf
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        progress(f"cluster classify parse error: {e}")
        return CLUSTER_NAMES[0], 40, "", 0


def match_riu(
    raw_input:       str,
    history_context: str,
    cluster_rius:    list[RIUEntry],
    client,
) -> tuple[str, int, str, int, Optional[str]]:
    """
    Match input to the most relevant RIU within a cluster.
    Returns (top_riu_id, confidence, runner_up_id, runner_up_conf, missing_slot).
    missing_slot is the one discriminating piece of info needed, or None.
    Uses Haiku — fast matching against a bounded list.
    """
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

    message = client.messages.create(
        model      = "claude-haiku-4-5-20251001",
        max_tokens = 250,
        messages   = [{"role": "user", "content": prompt}],
    )

    try:
        result         = _parse_json(message.content[0].text)
        top_id         = result.get("top_riu", "")
        confidence     = int(result.get("confidence", 40))
        runner_up_id   = result.get("runner_up") or ""
        if runner_up_id == "null":
            runner_up_id = ""
        runner_up_conf = int(result.get("runner_up_confidence", 0))
        missing_slot   = result.get("missing_slot")
        if missing_slot in ("null", ""):
            missing_slot = None
        return top_id, confidence, runner_up_id, runner_up_conf, missing_slot
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        progress(f"RIU match parse error: {e}")
        return "", 0, "", 0, "more details about your specific situation"


def generate_question(
    raw_input:    str,
    riu_a:        RIUEntry,
    riu_b:        RIUEntry,
    missing_slot: Optional[str],
    turn:         int,
    client,
) -> str:
    """
    Generate the ONE clarifying question that best collapses ambiguity.
    Not "which do you mean?" — the actual specific question.
    Uses Haiku — just generating a sentence.
    """
    discriminator = missing_slot or (
        f"whether you're dealing with '{riu_a.question[:80]}' "
        f"or '{riu_b.question[:80]}'"
    )
    brevity = " Keep it brief — we've already asked once." if turn > 0 else ""
    prompt = (
        f"You are Cory, a friendly and patient intent resolver. You need one more piece of information.\n\n"
        f'The user said: "{raw_input}"\n\n'
        f"You're deciding between:\n"
        f"  Option A: {riu_a.question}\n"
        f"  Option B: {riu_b.question}\n\n"
        f"Key discriminator needed: {discriminator}\n\n"
        f"Write ONE specific, friendly question — not 'which do you mean?' but the "
        f"actual question that gives you the answer. One sentence. Conversational. "
        f"No multiple choice. No options offered to the user.{brevity}"
    )

    message = client.messages.create(
        model      = "claude-haiku-4-5-20251001",
        max_tokens = 100,
        messages   = [{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip().strip('"')


def refine_prompt(
    raw_input:           str,
    riu:                 RIUEntry,
    history_context:     str,
    historical_examples: list[dict],
    client,
) -> dict:
    """
    Produce a clean, refined task description using the matched RIU context.
    Suggests the most appropriate specialist agent.
    Uses Sonnet — quality matters here, this goes straight to the specialist.
    """
    examples_block = ""
    if historical_examples:
        examples = "\n".join(
            f"- {e.get('refined_task', '')}"
            for e in historical_examples[:3]
            if e.get("refined_task")
        )
        if examples:
            examples_block = f"\nHistorical successful prompts for this RIU:\n{examples}"

    context_block = (
        f"\nClarifications gathered:\n{history_context}"
        if history_context else ""
    )

    prompt = (
        f"Refine this user request into a clean, complete task description "
        f"for a Palette specialist agent.\n\n"
        f"Original request: {raw_input}{context_block}\n\n"
        f"Matched RIU: {riu.question}\n"
        f"RIU approach: {riu.answer[:400]}{examples_block}\n\n"
        f"Write a refined task that:\n"
        f"1. Captures the user's actual intent precisely\n"
        f"2. Includes all context needed to act without further clarification\n"
        f"3. Uses clear, professional language appropriate for a specialist agent\n\n"
        f"Choose the best specialist agent:\n"
        f"  rex              → architectural/design decisions or system structure\n"
        f"  therizinosaurus  → implementation, code, or building something\n"
        f"  ankylosaurus     → validation, testing, audit, or risk assessment\n"
        f"  argentavis       → research, investigation, or information gathering\n"
        f"  velociraptor     → debugging, troubleshooting, or diagnosing failures\n"
        f"  parasaurolophus  → monitoring, alerting, or signal watching\n"
        f"  yutyrannus       → narrative, pitch, presentation, or communication\n\n"
        f"Return JSON only:\n"
        f'{{ "refined_task": "...", '
        f'"decision_context": "brief statement of what this informs or enables", '
        f'"suggested_agent": "agent_name", '
        f'"confidence": 0-100 }}'
    )

    message = client.messages.create(
        model      = "claude-sonnet-4-6",
        max_tokens = 600,
        messages   = [{"role": "user", "content": prompt}],
    )

    try:
        return _parse_json(message.content[0].text)
    except (json.JSONDecodeError, KeyError) as e:
        progress(f"refine parse error: {e} — using raw input")
        return {
            "refined_task":     raw_input,
            "decision_context": f"matched {riu.id}",
            "suggested_agent":  "human",
            "confidence":       50,
        }


# ── Result builders ───────────────────────────────────────────────────────────

def build_clarify(
    packet_id:             str,
    trace_id:              str,
    turn:                  int,
    max_turns:             int,
    question:              str,
    matched_cluster:       str,
    raw_input:             str,
    clarification_history: list[dict],
) -> dict:
    return {
        "packet_id": packet_id,
        "from":      "corythosaurus",
        "status":    "clarify",
        "output": {
            "question":        question,
            "turn":            turn + 1,
            "max_turns":       max_turns,
            "matched_cluster": matched_cluster,
            # payload_for_next_turn lets the caller reconstruct state
            "payload_for_next_turn": {
                "raw_input":             raw_input,
                "matched_cluster":       matched_cluster,
                "clarification_history": clarification_history,
                "turn":                  turn + 1,
                "max_turns":             max_turns,
                "last_question":         question,
            },
        },
        "produced_artifacts": [],
        "blockers":           [],
        "timestamp":          _now(),
    }


def build_complete(
    packet_id:             str,
    trace_id:              str,
    raw_input:             str,
    refined:               dict,
    riu_id:                str,
    confidence:            int,
    clarification_history: list[dict],
) -> dict:
    refined_packet = {
        "id":       f"cory-{packet_id}",
        "trace_id": trace_id,
        "from":     "corythosaurus",
        "to":       "orchestrator",
        "riu_ids":  [riu_id],
        "task":     refined.get("refined_task", raw_input),
        "payload": {
            "decision_context":      refined.get("decision_context", ""),
            "original_input":        raw_input,
            "riu_id":                riu_id,
            "suggested_agent":       refined.get("suggested_agent", ""),
            "clarification_history": clarification_history,
            "cory_confidence":       confidence,
        },
        "artifacts":   [],
        "constraints": [],
        "timestamp":   _now(),
    }
    return {
        "packet_id": packet_id,
        "from":      "corythosaurus",
        "status":    "complete",
        "output": {
            "refined_packet":  refined_packet,
            "riu_id":          riu_id,
            "confidence":      confidence,
            "suggested_agent": refined.get("suggested_agent", ""),
        },
        "produced_artifacts": [],
        "blockers":           [],
        "next_agent":         "orchestrator",
        "timestamp":          _now(),
    }


def build_out_of_scope(packet_id: str, reason: str) -> dict:
    return {
        "packet_id": packet_id,
        "from":      "corythosaurus",
        "status":    "out-of-scope",
        "output": {
            "message": reason,
            "guidance": (
                "This request doesn't clearly match any of Palette's 111 RIUs. "
                "Try rephrasing around a specific challenge, decision, or outcome — "
                "e.g. 'I need to align stakeholders on X' or 'our Y integration is failing'."
            ),
        },
        "produced_artifacts": [],
        "blockers":           [],
        "next_agent":         "human",
        "timestamp":          _now(),
    }


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cory — Corythosaurus Intent Resolver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  cory.py --input 'I need help aligning my team'\n"
            "  cory.py --input 'our API integration is failing' --dry-run\n"
            "  echo '{...HandoffPacket...}' | cory.py\n"
        ),
    )
    parser.add_argument("--input",     help="Raw user input (CLI mode)")
    parser.add_argument("--answer",    help="Answer to the last clarifying question (CLI multi-turn)")
    parser.add_argument("--max-turns", type=int, default=DEFAULT_MAX_TURNS)
    parser.add_argument("--dry-run",   action="store_true")
    args = parser.parse_args()

    # ── Load HandoffPacket from stdin or build from CLI ───────────────────────
    packet: dict = {}
    if not sys.stdin.isatty():
        try:
            raw_bytes = sys.stdin.read().strip()
            if raw_bytes:
                packet = json.loads(raw_bytes)
        except json.JSONDecodeError as e:
            progress(f"invalid JSON on stdin: {e}")
            return 1

    payload   = packet.get("payload", {})
    packet_id = packet.get("id",       "cli")
    trace_id  = packet.get("trace_id", "cli")

    # Reconstruct conversation state from payload (multi-turn support)
    raw_input   = args.input or payload.get("raw_input") or packet.get("task", "")
    matched_cluster        = payload.get("matched_cluster", "")
    clarification_history: list[dict] = list(payload.get("clarification_history", []))
    turn      = int(payload.get("turn", 0))
    max_turns = args.max_turns or int(payload.get("max_turns", DEFAULT_MAX_TURNS))

    # CLI multi-turn: --answer appends to history from prior invocation
    if args.answer and payload.get("last_question"):
        clarification_history.append({
            "question": payload["last_question"],
            "answer":   args.answer,
        })
        turn += 1

    if not raw_input:
        progress("no input provided — use --input or pass a HandoffPacket on stdin")
        return 1

    progress(f"corythosaurus v0.1 | turn {turn}/{max_turns}")
    progress(f"input: {raw_input[:80]}")

    # ── Gate: ANTHROPIC_API_KEY required ─────────────────────────────────────
    if not os.environ.get("ANTHROPIC_API_KEY"):
        err = {
            "packet_id": packet_id,
            "from":      "corythosaurus",
            "status":    "error",
            "output":    {},
            "blockers":  [
                "ANTHROPIC_API_KEY not set — Cory requires Claude for intent resolution"
            ],
            "timestamp": _now(),
        }
        json.dump(err, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 1

    # ── Dry-run ───────────────────────────────────────────────────────────────
    if args.dry_run:
        progress(f"[dry-run] input={raw_input[:60]} | turn={turn} | "
                 f"cluster={matched_cluster or 'unclassified'}")
        out = {
            "packet_id": packet_id,
            "from":      "corythosaurus",
            "status":    "dry-run",
            "output": {
                "turn":    turn,
                "cluster": matched_cluster or "unclassified",
                "input":   raw_input[:120],
            },
            "timestamp": _now(),
        }
        json.dump(out, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    # ── Load library ──────────────────────────────────────────────────────────
    library = load_library()
    progress(f"library: {len(library)} RIUs loaded")

    import anthropic
    client = anthropic.Anthropic()

    def history_str() -> str:
        if not clarification_history:
            return ""
        return "\n".join(
            f"Q: {t['question']}\nA: {t['answer']}"
            for t in clarification_history
        )

    # ── Step 1: Classify cluster (skip if carried from prior turn) ────────────
    if not matched_cluster:
        progress("classifying cluster")
        matched_cluster, cluster_conf, runner_up_c, _ = classify_cluster(
            raw_input, history_str(), client
        )
        progress(f"cluster: {matched_cluster} ({cluster_conf}%)"
                 + (f" | runner-up: {runner_up_c}" if runner_up_c else ""))
    else:
        progress(f"cluster: {matched_cluster} (carried from prior turn)")

    # ── Step 2: Match RIU within cluster ─────────────────────────────────────
    cluster_rius = get_cluster_rius(library, matched_cluster)
    progress(f"matching within {matched_cluster} ({len(cluster_rius)} RIUs)")

    top_id, confidence, runner_up_id, runner_up_conf, missing_slot = match_riu(
        raw_input, history_str(), cluster_rius, client
    )
    progress(f"match: {top_id} ({confidence}%)"
             + (f" | runner-up: {runner_up_id} ({runner_up_conf}%)" if runner_up_id else ""))

    # ── Step 3: Route on confidence ───────────────────────────────────────────

    # Confident match (or lowered bar on subsequent turns) → refine and return
    threshold = SECOND_TURN_FLOOR if turn >= 1 else CONFIDENCE_THRESHOLD
    if top_id and confidence >= threshold:
        matched_riu = next((r for r in cluster_rius if r.id == top_id), None)
        if matched_riu:
            progress(f"confident match: {top_id} — refining prompt")
            history_examples = load_history(top_id)
            refined = refine_prompt(
                raw_input, matched_riu, history_str(), history_examples, client
            )
            progress(f"→ {refined.get('suggested_agent', '?')} "
                     f"| confidence={refined.get('confidence', 0)}%")
            save_history(top_id, raw_input, refined.get("refined_task", ""))
            result = build_complete(
                packet_id, trace_id, raw_input, refined,
                top_id, confidence, clarification_history,
            )
            json.dump(result, sys.stdout, indent=2)
            sys.stdout.write("\n")
            return 0

    # Max turns reached → out of scope
    if turn >= max_turns:
        progress(f"max turns ({max_turns}) reached — out of scope")
        msg = (
            f"After {max_turns} clarifying questions, this request still doesn't "
            f"clearly match a known RIU."
        )
        if top_id:
            msg += f" Best candidate was {top_id} ({confidence}% confidence)."
        result = build_out_of_scope(packet_id, msg)
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    # Low confidence + turns remaining → ask ONE question
    if not top_id:
        progress("no RIU match — asking about problem domain")
        question = (
            "What specific challenge or outcome are you trying to address? "
            "(For example: aligning stakeholders, integrating systems, "
            "improving reliability, or managing risk)"
        )
    else:
        riu_a = next((r for r in cluster_rius if r.id == top_id), None)
        riu_b = next((r for r in cluster_rius if r.id == runner_up_id), None)

        if riu_a and riu_b:
            progress(f"ambiguous: {top_id} vs {runner_up_id} — generating question")
            question = generate_question(
                raw_input, riu_a, riu_b, missing_slot, turn, client
            )
        else:
            question = (
                missing_slot
                or "Could you tell me more about the specific outcome you're aiming for?"
            )

    progress(f"asking: {question[:80]}")
    result = build_clarify(
        packet_id, trace_id, turn, max_turns,
        question, matched_cluster, raw_input, clarification_history,
    )
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
