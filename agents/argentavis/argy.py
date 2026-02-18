#!/usr/bin/env python3
"""
argy.py — Argentavis (Argy) Research Agent
Palette Workflow Agent v2.0

Input:  HandoffPacket JSON via stdin  OR  --task / --context flags
Output: HandoffResult JSON to stdout  (machine-readable for Orch)
Stderr: Human-readable progress log

HandoffPacket.payload fields read:
  decision_context   REQUIRED — what decision does this research inform?
  depth              fast | standard | deep  (default: standard)
  query_type_hint    factual | synthesis | academic | current_events (optional)
  decisions_path     path to decisions.md for maturity logging (optional)

HandoffResult.output fields produced:
  findings[]   {claim, evidence, source, confidence}
  gaps[]       things we could not find or resolve — FIRST-CLASS, min 1
  sources[]    {url, title, retrieved_at, reliability}
  confidence   0-100 overall confidence in the findings
  query_type   classification used for backend routing
  depth_used   which backend(s) did the work
  cache_hit    whether knowledge library answered it
  next_agent   routing suggestion (rex | therizinosaurus | ankylosaurus | human)

Backend selection by query type:
  factual        → Tavily → Perplexity → Exa
  current_events → Perplexity → Tavily
  academic       → Exa → Perplexity
  synthesis      → Perplexity → Tavily → Exa
Claude always runs synthesis over raw results when ANTHROPIC_API_KEY is set.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Optional


# ── Query types ───────────────────────────────────────────────────────────────

class QueryType(str, Enum):
    FACTUAL        = "factual"         # concrete facts, comparisons, costs → Tavily
    SYNTHESIS      = "synthesis"       # design, strategy, tradeoffs → Perplexity + Claude
    ACADEMIC       = "academic"        # papers, theory, algorithms → Exa
    CURRENT_EVENTS = "current_events"  # latest news, releases → Perplexity
    UNKNOWN        = "unknown"         # fallback — try all


# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class Finding:
    claim:      str
    evidence:   str
    source:     str
    confidence: int  # 0-100


@dataclass
class Source:
    url:          str
    title:        str
    retrieved_at: str
    reliability:  str  # high | medium | low


@dataclass
class SearchResult:
    findings:   list[Finding] = field(default_factory=list)
    gaps:       list[str]     = field(default_factory=list)
    sources:    list[Source]  = field(default_factory=list)
    confidence: int           = 0
    depth_used: str           = "none"
    cache_hit:  bool          = False
    next_agent: str           = "human"  # filled by Claude synthesis


# ── Backend registry ──────────────────────────────────────────────────────────

class BackendRegistry:
    """Checks which API keys are present at startup."""

    def __init__(self) -> None:
        self.anthropic  = bool(os.environ.get("ANTHROPIC_API_KEY"))
        self.perplexity = bool(os.environ.get("PERPLEXITY_API_KEY"))
        self.tavily     = bool(os.environ.get("TAVILY_API_KEY"))
        self.exa        = bool(os.environ.get("EXA_API_KEY"))

    def available(self) -> list[str]:
        out = []
        if self.anthropic:  out.append("claude")
        if self.perplexity: out.append("perplexity")
        if self.tavily:     out.append("tavily")
        if self.exa:        out.append("exa")
        return out

    def report(self) -> str:
        a = self.available()
        return "backends: " + ", ".join(a) if a else "no backends — set API keys"


# ── Knowledge library ─────────────────────────────────────────────────────────

_HERE = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_LIBRARY_PATH = os.path.normpath(os.path.join(
    _HERE, "..", "..", "knowledge-library",
    "v1.2", "palette_knowledge_library_v1.2.yaml",
))


def check_knowledge_library(task: str) -> Optional[SearchResult]:
    """
    Check the local knowledge library BEFORE any external API call.
    Returns a SearchResult with matched entries, or None if no hits.
    """
    if not os.path.exists(KNOWLEDGE_LIBRARY_PATH):
        progress(f"knowledge library not found at {KNOWLEDGE_LIBRARY_PATH}")
        return None

    try:
        import yaml
    except ImportError:
        progress("pyyaml not installed — pip install pyyaml to enable knowledge library")
        return None

    try:
        with open(KNOWLEDGE_LIBRARY_PATH) as f:
            lib = yaml.safe_load(f)
    except Exception as e:
        progress(f"knowledge library read error: {e}")
        return None

    questions = lib.get("library_questions", [])
    task_lower = task.lower()
    task_words = set(w for w in task_lower.split() if len(w) > 4)

    scored: list[tuple[int, dict]] = []
    for q in questions:
        q_text  = q.get("question", "").lower()
        q_words = set(w for w in q_text.split() if len(w) > 4)
        overlap = len(task_words & q_words)
        if overlap >= 2:
            scored.append((overlap, q))

    if not scored:
        return None

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:3]

    result = SearchResult(cache_hit=True, depth_used="knowledge-library:v1.2")
    now    = datetime.datetime.utcnow().isoformat() + "Z"

    for _, q in top:
        answer = q.get("answer", "")
        if not answer:
            continue
        lib_id  = q.get("id", "LIB-???")
        preview = answer[:500] + ("..." if len(answer) > 500 else "")
        result.findings.append(Finding(
            claim      = q.get("question", ""),
            evidence   = preview,
            source     = f"Palette Knowledge Library {lib_id}",
            confidence = 82,
        ))
        result.sources.append(Source(
            url          = f"file://{KNOWLEDGE_LIBRARY_PATH}#{lib_id}",
            title        = f"Knowledge Library: {lib_id}",
            retrieved_at = now,
            reliability  = "high",
        ))

    if result.findings:
        result.confidence = 68  # good signal, but may be stale
        result.gaps.append(
            "Knowledge library answers may be stale — external validation recommended"
        )
        return result

    return None


# ── Query classifier ──────────────────────────────────────────────────────────

_FACTUAL_SIGNALS        = ["what is", "how does", "define", "explain", "describe",
                           "vs", "versus", "compare", "difference between",
                           "cost", "pricing", "latency", "benchmark", "list"]
_SYNTHESIS_SIGNALS      = ["best approach", "should i", "trade-off", "tradeoff",
                           "design", "architecture", "pattern", "strategy",
                           "recommend", "evaluate", "assess", "how should"]
_ACADEMIC_SIGNALS       = ["research", "study", "paper", "published", "academic",
                           "theory", "algorithm", "formal", "proof", "survey"]
_CURRENT_EVENTS_SIGNALS = ["latest", "recent", "2025", "2026", "current",
                           "new release", "just announced", "breaking", "today",
                           "changelog", "update"]


def classify_query(task: str, hint: Optional[str] = None) -> QueryType:
    """Classify query type from task text and optional override hint."""
    if hint:
        try:
            return QueryType(hint)
        except ValueError:
            pass

    t = task.lower()
    scores = {
        QueryType.FACTUAL:        sum(1 for s in _FACTUAL_SIGNALS        if s in t),
        QueryType.SYNTHESIS:      sum(1 for s in _SYNTHESIS_SIGNALS      if s in t),
        QueryType.ACADEMIC:       sum(1 for s in _ACADEMIC_SIGNALS       if s in t),
        QueryType.CURRENT_EVENTS: sum(1 for s in _CURRENT_EVENTS_SIGNALS if s in t),
    }
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return QueryType.SYNTHESIS  # default for undifferentiated research tasks
    return best


# ── Progress output ───────────────────────────────────────────────────────────

def progress(msg: str) -> None:
    """Write human-readable progress to stderr (never pollutes stdout/JSON)."""
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    print(f"[argy {ts}] {msg}", file=sys.stderr, flush=True)


def _parse_json(text: str) -> dict:
    """
    Parse JSON from Claude responses robustly:
    - strips markdown code fences (```json ... ```)
    - extracts the first complete JSON object regardless of surrounding text
    """
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        start = 1
        end   = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
        text  = "\n".join(lines[start:end]).strip()
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


# ── Perplexity backend ────────────────────────────────────────────────────────

def search_perplexity(task: str, context: str, model: str = "sonar-pro") -> SearchResult:
    """Call Perplexity Sonar API — best for synthesis and current-events queries."""
    import httpx

    api_key = os.environ["PERPLEXITY_API_KEY"]
    progress(f"querying perplexity:{model}")

    prompt = (
        f"Research task: {task}\n\n"
        f"Decision context: {context}\n\n"
        "Provide:\n"
        "1. Key findings with evidence and explicit source citations\n"
        "2. Tradeoffs and technical considerations\n"
        "3. What is NOT known or unclear — gaps matter as much as findings\n\n"
        "Be factual. Cite sources. Flag uncertainty honestly."
    )

    payload = {
        "model":   model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a precise research assistant. "
                    "Cite sources explicitly. Flag uncertainty. Never hallucinate."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "return_citations":         True,
        "return_related_questions": False,
    }

    with httpx.Client(timeout=30.0) as client:
        resp = client.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type":  "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()

    content   = data["choices"][0]["message"]["content"]
    citations = data.get("citations", [])
    now       = datetime.datetime.utcnow().isoformat() + "Z"

    sources = [
        Source(url=url, title=f"Source {i+1}", retrieved_at=now, reliability="medium")
        for i, url in enumerate(citations[:10])
    ]

    result = SearchResult(depth_used=f"perplexity:{model}", cache_hit=False)
    result.findings.append(Finding(
        claim      = content[:300] + ("..." if len(content) > 300 else ""),
        evidence   = content,
        source     = f"perplexity:{model}",
        confidence = 72,
    ))
    result.sources    = sources
    result.confidence = 72
    result.gaps.append(
        "Perplexity synthesis — verify key claims against primary sources"
    )
    return result


# ── Tavily backend ────────────────────────────────────────────────────────────

def search_tavily(task: str, context: str, depth: str = "standard") -> SearchResult:
    """Call Tavily Search API — best for factual, fast queries."""
    import httpx

    api_key      = os.environ["TAVILY_API_KEY"]
    search_depth = "advanced" if depth == "deep" else "basic"
    progress(f"querying tavily:{search_depth}")

    query   = f"{task} ({context})" if context else task
    payload = {
        "api_key":        api_key,
        "query":          query,
        "search_depth":   search_depth,
        "include_answer": True,
        "max_results":    8,
    }

    with httpx.Client(timeout=20.0) as client:
        resp = client.post("https://api.tavily.com/search", json=payload)
        resp.raise_for_status()
        data = resp.json()

    now    = datetime.datetime.utcnow().isoformat() + "Z"
    result = SearchResult(depth_used=f"tavily:{search_depth}", cache_hit=False)

    answer = data.get("answer", "")
    if answer:
        result.findings.append(Finding(
            claim      = answer[:300] + ("..." if len(answer) > 300 else ""),
            evidence   = answer,
            source     = "tavily:aggregated",
            confidence = 68,
        ))

    for item in data.get("results", [])[:6]:
        result.findings.append(Finding(
            claim      = item.get("title", ""),
            evidence   = item.get("content", "")[:400],
            source     = item.get("url", ""),
            confidence = 62,
        ))
        result.sources.append(Source(
            url          = item.get("url", ""),
            title        = item.get("title", ""),
            retrieved_at = now,
            reliability  = "medium",
        ))

    result.confidence = 64
    if not result.findings:
        result.gaps.append("Tavily returned no results for this query")
    else:
        result.gaps.append(
            "Tavily results are raw web data — synthesis and cross-validation needed"
        )
    return result


# ── Exa backend ───────────────────────────────────────────────────────────────

def search_exa(task: str, context: str) -> SearchResult:
    """Call Exa neural search — best for academic and semantic queries."""
    import httpx

    api_key = os.environ["EXA_API_KEY"]
    progress("querying exa:neural")

    payload = {
        "query":         task,
        "numResults":    8,
        "useAutoprompt": True,
        "contents": {"text": {"maxCharacters": 800}},
    }

    with httpx.Client(timeout=25.0) as client:
        resp = client.post(
            "https://api.exa.ai/search",
            headers={"x-api-key": api_key, "Content-Type": "application/json"},
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()

    now    = datetime.datetime.utcnow().isoformat() + "Z"
    result = SearchResult(depth_used="exa:neural", cache_hit=False)

    for item in data.get("results", [])[:6]:
        text = item.get("text", "") or item.get("excerpt", "")
        result.findings.append(Finding(
            claim      = item.get("title", ""),
            evidence   = text[:400],
            source     = item.get("url", ""),
            confidence = 78,
        ))
        result.sources.append(Source(
            url          = item.get("url", ""),
            title        = item.get("title", ""),
            retrieved_at = now,
            reliability  = "high",
        ))

    result.confidence = 76
    if not result.findings:
        result.gaps.append("Exa found no relevant academic or technical sources")
    else:
        result.gaps.append(
            "Academic sources found — check publication dates for recency"
        )
    return result


# ── Claude synthesis layer ────────────────────────────────────────────────────

def synthesize_with_claude(
    task:       str,
    context:    str,
    raw_result: SearchResult,
) -> SearchResult:
    """
    Transform raw backend results into structured findings using Claude.
    Claude is always the final synthesis layer — regardless of which search
    backend did the retrieval. Synthesis is not the same as search.
    """
    import anthropic

    progress("synthesizing with claude:opus-4-6")

    raw_findings = "\n".join(
        f"- [{f.source}] {f.claim}: {f.evidence[:250]}"
        for f in raw_result.findings
    )

    prompt = f"""You are a research synthesizer. Transform raw search findings into structured analysis.

Research task: {task}
Decision context: {context}

Raw findings:
{raw_findings}

Produce a JSON object with EXACTLY this structure:
{{
  "findings": [
    {{
      "claim":      "precise, verifiable factual claim",
      "evidence":   "supporting evidence directly from the sources",
      "source":     "URL or source identifier",
      "confidence": 0-100
    }}
  ],
  "gaps": [
    "specific unanswered question",
    "area where sources conflict or are missing",
    "claim that needs primary-source validation"
  ],
  "confidence": 0-100,
  "next_agent": "rex|therizinosaurus|ankylosaurus|human"
}}

Rules:
- findings: 3-7 items, each a distinct verifiable claim with evidence
- gaps: MINIMUM 2 items — empty gaps means stopped looking too soon
- confidence: honest score for how well this answers the decision question
- next_agent routing:
    rex              → architectural decisions or system design needed
    therizinosaurus  → implementation or code changes needed
    ankylosaurus     → validation, testing, or risk assessment needed
    human            → judgment call beyond technical facts

Return ONLY the JSON object. No markdown, no prose."""

    client  = anthropic.Anthropic()
    message = client.messages.create(
        model      = "claude-opus-4-6",
        max_tokens = 2000,
        messages   = [{"role": "user", "content": prompt}],
    )

    try:
        synthesis = _parse_json(message.content[0].text)
    except (json.JSONDecodeError, IndexError, KeyError) as e:
        progress(f"claude synthesis parse error: {e} — using raw results")
        return raw_result

    result = SearchResult(
        depth_used = raw_result.depth_used + "+claude:opus-4-6",
        cache_hit  = raw_result.cache_hit,
        sources    = raw_result.sources,
    )
    for f in synthesis.get("findings", []):
        result.findings.append(Finding(
            claim      = f.get("claim", ""),
            evidence   = f.get("evidence", ""),
            source     = f.get("source", ""),
            confidence = int(f.get("confidence", 60)),
        ))

    raw_gaps          = synthesis.get("gaps", [])
    result.gaps       = raw_gaps if raw_gaps else ["synthesis complete — review findings for edge cases"]
    result.confidence = int(synthesis.get("confidence", 60))
    result.next_agent = synthesis.get("next_agent", "human")
    return result


# ── Main research flow ────────────────────────────────────────────────────────

def run_research(
    task:       str,
    context:    str,
    depth:      str,
    query_type: QueryType,
    registry:   BackendRegistry,
) -> SearchResult:
    """
    Execute research using the best available backends for the query type.
    Always ends with Claude synthesis if the anthropic key is available.
    """
    raw: Optional[SearchResult] = None

    # Step 1: Knowledge library FIRST — always, before any API call
    progress("checking knowledge library")
    lib_result = check_knowledge_library(task)

    if lib_result:
        n = len(lib_result.findings)
        progress(f"knowledge library: {n} matching entries")
        if depth == "fast" and lib_result.confidence >= 68:
            progress("knowledge library sufficient for fast depth — skipping external search")
            if registry.anthropic:
                return synthesize_with_claude(task, context, lib_result)
            return lib_result
    else:
        progress("knowledge library: no matches")

    # Step 2: External search — route by query type
    progress(f"routing by query type: {query_type.value}")

    try:
        if query_type == QueryType.FACTUAL:
            if registry.tavily:
                raw = search_tavily(task, context, depth)
            elif registry.perplexity:
                raw = search_perplexity(task, context)
            elif registry.exa:
                raw = search_exa(task, context)

        elif query_type == QueryType.CURRENT_EVENTS:
            if registry.perplexity:
                raw = search_perplexity(task, context)
            elif registry.tavily:
                raw = search_tavily(task, context, depth)

        elif query_type == QueryType.ACADEMIC:
            if registry.exa:
                raw = search_exa(task, context)
            elif registry.perplexity:
                raw = search_perplexity(task, context)

        else:  # SYNTHESIS or UNKNOWN — Perplexity first
            if registry.perplexity:
                model = "sonar-reasoning" if depth == "deep" else "sonar-pro"
                raw   = search_perplexity(task, context, model=model)
            elif registry.tavily:
                raw = search_tavily(task, context, depth)
            elif registry.exa:
                raw = search_exa(task, context)

    except Exception as e:
        progress(f"primary backend failed: {e}")
        raw = None

    # Step 3: Merge library hits with external results when both exist
    if lib_result and raw:
        raw.findings = lib_result.findings + raw.findings
        raw.sources  = lib_result.sources  + raw.sources
        raw.gaps.append(
            "merged knowledge library + external results — check for consistency"
        )
    elif lib_result and raw is None:
        raw = lib_result
    elif raw is None:
        return SearchResult(
            findings   = [],
            gaps       = [
                "No search backends available — set PERPLEXITY_API_KEY, TAVILY_API_KEY, or EXA_API_KEY",
                "Knowledge library had no matches for this task",
            ],
            confidence = 0,
            depth_used = "none",
            next_agent = "human",
        )

    # Step 4: Claude synthesis (always when key is available)
    if registry.anthropic:
        return synthesize_with_claude(task, context, raw)

    progress("ANTHROPIC_API_KEY not set — returning raw results without synthesis")
    if not raw.gaps:
        raw.gaps.append(
            "Claude synthesis unavailable — set ANTHROPIC_API_KEY for structured findings"
        )
    return raw


# ── Maturity logging ──────────────────────────────────────────────────────────

def log_execution(
    task:           str,
    context:        str,
    result:         SearchResult,
    packet_id:      str,
    trace_id:       str,
    decisions_path: str,
) -> None:
    """Append execution record to decisions.md for maturity tracking."""
    if not decisions_path:
        return

    ddir = os.path.dirname(decisions_path)
    if ddir and not os.path.exists(ddir):
        return

    outcome    = "SUCCESS" if result.confidence >= 50 else "FAILURE"
    lib_status = "HIT" if result.cache_hit else "MISS"
    ts         = datetime.datetime.utcnow().isoformat()

    entry = (
        f"\n---\n"
        f"### Agent Execution: Argentavis\n\n"
        f"**Timestamp**: {ts}\n"
        f"**Trace**: {trace_id}\n"
        f"**Packet**: {packet_id}\n"
        f"**Agent**: argentavis v2.0\n"
        f"**Status**: WORKING\n"
        f"**Request**: {task[:120]}\n"
        f"**Decision Context**: {context[:120]}\n"
        f"**Outcome**: {outcome}\n"
        f"**Confidence**: {result.confidence}%\n"
        f"**Knowledge Library**: {lib_status}\n"
        f"**Sources Found**: {len(result.sources)}\n"
        f"**Depth Used**: {result.depth_used}\n"
        f"**Gaps**: {len(result.gaps)}\n"
    )

    try:
        with open(decisions_path, "a") as f:
            f.write(entry)
        progress(f"logged to {decisions_path}")
    except OSError as e:
        progress(f"could not write to decisions.md: {e}")


# ── HandoffResult builder ─────────────────────────────────────────────────────

def build_handoff_result(
    packet_id:  str,
    result:     SearchResult,
    query_type: QueryType,
    status:     str = "complete",
) -> dict:
    return {
        "packet_id": packet_id,
        "from":      "argentavis",
        "status":    status,
        "output": {
            "findings":   [asdict(f) for f in result.findings],
            "gaps":       result.gaps if result.gaps else ["no gaps recorded — review findings manually"],
            "sources":    [asdict(s) for s in result.sources],
            "confidence": result.confidence,
            "query_type": query_type.value,
            "depth_used": result.depth_used,
            "cache_hit":  result.cache_hit,
            "next_agent": result.next_agent,
        },
        "produced_artifacts": [],
        "blockers":           [],
        "next_agent":         result.next_agent,
        "timestamp":          datetime.datetime.utcnow().isoformat() + "Z",
    }


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Argy — Argentavis Research Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  argy.py --task 'compare Redis vs DynamoDB' --context 'choosing session store'\n"
            "  echo '{...HandoffPacket JSON...}' | argy.py\n"
            "  argy.py --task 'latest Go concurrency patterns' --depth deep --dry-run\n"
        ),
    )
    parser.add_argument("--task",    help="Research task description (CLI mode)")
    parser.add_argument("--context", default="", help="Decision context (CLI mode)")
    parser.add_argument("--depth",   choices=["fast", "standard", "deep"], default="standard")
    parser.add_argument(
        "--query-type", dest="query_type_hint",
        choices=[t.value for t in QueryType if t != QueryType.UNKNOWN],
        help="Override automatic query type classification",
    )
    parser.add_argument("--decisions", default="", help="Path to decisions.md for maturity logging")
    parser.add_argument("--dry-run",   action="store_true", help="Classify without calling any APIs")
    args = parser.parse_args()

    # ── Load input ────────────────────────────────────────────────────────────
    packet: dict = {}
    if not sys.stdin.isatty():
        try:
            raw_input = sys.stdin.read().strip()
            if raw_input:
                packet = json.loads(raw_input)
        except json.JSONDecodeError as e:
            progress(f"invalid JSON on stdin: {e}")
            return 1

    payload = packet.get("payload", {})

    task            = args.task             or packet.get("task", "")
    context         = args.context          or payload.get("decision_context", "")
    depth           = args.depth            or payload.get("depth", "standard")
    query_type_hint = args.query_type_hint  or payload.get("query_type_hint")
    packet_id       = packet.get("id",       "cli")
    trace_id        = packet.get("trace_id", "cli")
    decisions_path  = args.decisions        or payload.get("decisions_path", "")

    if not task:
        progress("no task provided — use --task or pass a HandoffPacket on stdin")
        return 1

    # ── Gate: decision_context required ──────────────────────────────────────
    if not context:
        clarify = {
            "packet_id": packet_id,
            "from":      "argentavis",
            "status":    "clarify",
            "output": {
                "question": (
                    "What decision does this research inform? "
                    "(required to focus the search and calibrate depth)"
                ),
                "findings": [],
                "gaps":     [
                    "decision_context missing — cannot determine relevance or search depth"
                ],
            },
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        }
        json.dump(clarify, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    # ── Registry ──────────────────────────────────────────────────────────────
    registry = BackendRegistry()
    progress(f"argentavis v2.0 | {registry.report()}")
    progress(f"task:    {task[:80]}")
    progress(f"context: {context[:80]}")
    progress(f"depth:   {depth}")

    # ── Dry-run ───────────────────────────────────────────────────────────────
    if args.dry_run:
        qt = classify_query(task, query_type_hint)
        progress(f"[dry-run] query_type={qt.value} | available: {registry.available()}")
        out = build_handoff_result(
            packet_id  = packet_id,
            result     = SearchResult(
                gaps       = ["dry-run mode — no search performed"],
                depth_used = "none",
                confidence = 0,
            ),
            query_type = qt,
            status     = "dry-run",
        )
        json.dump(out, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    # ── Classify ──────────────────────────────────────────────────────────────
    query_type = classify_query(task, query_type_hint)
    progress(f"query type: {query_type.value}")

    # ── Research ──────────────────────────────────────────────────────────────
    t0 = time.time()
    try:
        search_result = run_research(task, context, depth, query_type, registry)
    except Exception as e:
        progress(f"research failed: {e}")
        err_out = {
            "packet_id": packet_id,
            "from":      "argentavis",
            "status":    "error",
            "output": {
                "findings":   [],
                "gaps":       [f"search error: {e}"],
                "sources":    [],
                "confidence": 0,
                "query_type": query_type.value,
                "depth_used": "error",
                "cache_hit":  False,
                "next_agent": "human",
            },
            "blockers":  [str(e)],
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        }
        json.dump(err_out, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 1

    elapsed = time.time() - t0
    progress(
        f"done in {elapsed:.1f}s | "
        f"confidence={search_result.confidence}% | "
        f"findings={len(search_result.findings)} | "
        f"gaps={len(search_result.gaps)} | "
        f"sources={len(search_result.sources)}"
    )

    # ── Log maturity ──────────────────────────────────────────────────────────
    if decisions_path:
        log_execution(task, context, search_result, packet_id, trace_id, decisions_path)

    # ── Emit HandoffResult ────────────────────────────────────────────────────
    handoff = build_handoff_result(packet_id, search_result, query_type)
    json.dump(handoff, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
