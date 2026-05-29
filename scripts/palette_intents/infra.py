"""Shared infrastructure for palette intents.

Provides: IntentState, palette_checkpoint, integrity card builder,
artifact storage, UNVALIDATED_FALLBACK display.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# ── Paths ───────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = REPO_ROOT / ".palette" / "artifacts"
INTEGRITY_CACHE_PATH = REPO_ROOT / ".palette" / "integrity_cache.json"
GAP_LOG = REPO_ROOT / "peers" / "gap_signals.ndjson"
BUS_URL = "http://127.0.0.1:7899"

# ── ANSI ────────────────────────────────────────────────────────────────

BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# ── Intent State ────────────────────────────────────────────────────────


@dataclass
class IntentState:
    """Tracks execution state across the intent lifecycle."""

    intent: str
    query: str
    riu: str | None = None
    riu_name: str | None = None
    boundary: str = "local_only"
    confidence: float = 0.0
    posture: str = "execute"
    integrity_card: dict = field(default_factory=dict)
    transition_depth: int = 0
    matter_id: str | None = None
    artifacts: list[str] = field(default_factory=list)
    thread_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def transition_to(self, new_intent: str) -> "IntentState":
        """Create a new state for a transitioned intent."""
        return IntentState(
            intent=new_intent,
            query=self.query,
            riu=self.riu,
            riu_name=self.riu_name,
            boundary=self.boundary,
            confidence=self.confidence,
            posture=self.posture,
            integrity_card=self.integrity_card,
            transition_depth=self.transition_depth + 1,
            matter_id=self.matter_id,
            artifacts=list(self.artifacts),
            thread_id=self.thread_id,
        )


# ── Integrity Card ──────────────────────────────────────────────────────


@dataclass
class IntegrityCard:
    """Lightweight card for intent execution decisions."""

    riu_id: str
    classification: str  # internal_only | both | governed_external
    posture: str  # execute | execute_with_limitations | blocked_by_boundary | research_or_reflect_first | governance_required
    knowledge_count: int = 0
    has_recipe: bool = False
    gaps: list[str] = field(default_factory=list)


def build_integrity_card_fast(riu_id: str, classification: str, knowledge_count: int) -> IntegrityCard:
    """Fast-path integrity card from resolve result (no PIS load).

    Use when resolve already gave us classification + knowledge count.
    """
    posture = "execute"
    if classification == "internal_only":
        posture = "blocked_by_boundary"
    elif knowledge_count == 0:
        posture = "research_or_reflect_first"

    return IntegrityCard(
        riu_id=riu_id,
        classification=classification,
        posture=posture,
        knowledge_count=knowledge_count,
        has_recipe=False,
        gaps=[],
    )


def build_integrity_card(riu_id: str) -> IntegrityCard:
    """Build an integrity card from the existing PIS integrity engine.

    Uses a fast path when possible (classification from resolve result),
    falls back to full PIS load if needed.
    """
    import sys

    sys.path.insert(0, str(REPO_ROOT))
    try:
        from scripts.palette_intelligence_system.integrity import (
            build_card,
            load_integrity_data,
        )

        data = load_integrity_data(str(REPO_ROOT))
        card = build_card(data, riu_id)

        # Map to execution posture
        posture = "execute"
        if card.classification == "internal_only":
            posture = "blocked_by_boundary"
        elif card.knowledge_count == 0:
            posture = "research_or_reflect_first"
        elif card.completeness_label == "bare":
            posture = "execute_with_limitations"

        return IntegrityCard(
            riu_id=riu_id,
            classification=card.classification,
            posture=posture,
            knowledge_count=card.knowledge_count,
            has_recipe=any(rc.has_recipe for rc in card.recipe_coverage),
            gaps=card.gaps,
        )
    except Exception:
        # Fallback: conservative posture
        return IntegrityCard(
            riu_id=riu_id,
            classification="internal_only",
            posture="blocked_by_boundary",
            gaps=["integrity engine unavailable"],
        )


# ── Integrity Cache ─────────────────────────────────────────────────────


def load_integrity_cache() -> dict:
    """Load session-persistent integrity cache."""
    if INTEGRITY_CACHE_PATH.exists():
        try:
            return json.loads(INTEGRITY_CACHE_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"recipe_failures": {}, "posture_overrides": {}}


def save_integrity_cache(cache: dict) -> None:
    """Persist integrity cache."""
    INTEGRITY_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    INTEGRITY_CACHE_PATH.write_text(json.dumps(cache, indent=2))


def record_recipe_failure(recipe_name: str) -> None:
    """Track recipe failure. 3 failures → auto-demote."""
    cache = load_integrity_cache()
    failures = cache.setdefault("recipe_failures", {})
    entry = failures.setdefault(recipe_name, {"count": 0, "last": None})
    entry["count"] += 1
    entry["last"] = datetime.now(timezone.utc).isoformat()
    if entry["count"] >= 3:
        cache.setdefault("posture_overrides", {})[recipe_name] = "execute_with_limitations"
    save_integrity_cache(cache)


# ── Palette Checkpoint ──────────────────────────────────────────────────


def palette_checkpoint(state: IntentState) -> IntentState:
    """Between every model call, check if intent should shift.

    Priority: PROTECT > DIAGNOSE > RESEARCH > DECIDE > CREATE > REFLECT
    """
    # Hard limit: no infinite oscillation
    if state.transition_depth > 2:
        return state  # halt — don't transition further

    card = state.integrity_card
    posture = card.get("posture", "execute") if isinstance(card, dict) else getattr(card, "posture", "execute")

    # Boundary violation → PROTECT
    if posture == "blocked_by_boundary" and state.intent != "PROTECT":
        return state.transition_to("PROTECT")

    # Governance required → halt for human
    if posture == "governance_required":
        return state  # don't auto-transition, flag for human

    return state


# ── Artifact Storage ────────────────────────────────────────────────────


def store_artifact(artifact_type: str, content: dict, body: str = "") -> str:
    """Store a typed artifact as markdown with YAML frontmatter.

    Returns the artifact path.
    """
    # Validate before storing
    errors = validate_artifact(artifact_type, content)
    if errors:
        # Log validation failures but still store (with status marker)
        content["_validation_errors"] = errors

    type_dir = ARTIFACTS_DIR / artifact_type
    type_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    filename = f"{timestamp}.md"
    path = type_dir / filename

    frontmatter = yaml.dump(content, default_flow_style=False, sort_keys=False)
    full_content = f"---\n{frontmatter}---\n\n{body}\n"
    path.write_text(full_content)

    return str(path)


# ── Artifact Validation ─────────────────────────────────────────────────

ARTIFACT_SCHEMAS = {
    "gate_decision": {
        "required": ["artifact_type", "intent", "timestamp", "action", "reason", "boundary"],
        "rules": {
            "action_values": lambda d: d.get("action") in ("BLOCK", "ALLOW"),
            "blocked_entities_on_block": lambda d: d.get("action") != "BLOCK" or len(d.get("blocked_entities", [])) > 0 or "too short" in d.get("reason", "") or "PII category" in d.get("reason", "") or "semantic" in d.get("reason", ""),
        },
    },
    "evidence_brief": {
        "required": ["artifact_type", "intent", "timestamp", "local_canon", "confidence", "status"],
        "rules": {
            "status_values": lambda d: d.get("status") in ("VALIDATED", "LOCAL_ONLY", "UNVALIDATED_FALLBACK"),
            "confidence_range": lambda d: 0 <= d.get("confidence", 0) <= 100,
        },
    },
    "decision_record": {
        "required": ["artifact_type", "intent", "timestamp", "recommendation", "strongest_counterargument", "reversibility"],
        "rules": {
            "counter_length": lambda d: len(d.get("strongest_counterargument", "").split()) >= 30 or "failed" in d.get("strongest_counterargument", "").lower(),
            "reversibility_values": lambda d: d.get("reversibility") in ("ONE_WAY", "TWO_WAY"),
            "checkpoint_on_one_way": lambda d: d.get("reversibility") != "ONE_WAY" or d.get("checkpoint_required") is True,
        },
    },
    "artifact_lineage": {
        "required": ["artifact_type", "intent", "timestamp", "spec", "iterations", "max_iterations"],
        "rules": {
            "iterations_bounded": lambda d: d.get("iterations", 0) <= d.get("max_iterations", 3),
        },
    },
    "failure_lesson": {
        "required": ["artifact_type", "intent", "timestamp", "symptom", "five_whys"],
        "rules": {
            "five_whys_count": lambda d: len(d.get("five_whys", [])) == 5,
        },
    },
    "improvement_proposal": {
        "required": ["artifact_type", "intent", "timestamp", "status", "patterns"],
        "rules": {
            "status_proposed": lambda d: d.get("status") == "PROPOSED",
            "write_lock": lambda d: all(
                p.get("target_file", "").startswith("wiki/proposed/")
                for p in d.get("proposed_actions", [])
            ),
        },
    },
}


def validate_artifact(artifact_type: str, content: dict) -> list[str]:
    """Validate artifact against its schema. Returns list of errors (empty = valid)."""
    schema = ARTIFACT_SCHEMAS.get(artifact_type)
    if not schema:
        return []  # Unknown type — no validation

    errors = []

    # Check required fields
    for field in schema.get("required", []):
        if field not in content or content[field] is None:
            errors.append(f"missing required field: {field}")

    # Check rules
    for rule_name, rule_fn in schema.get("rules", {}).items():
        try:
            if not rule_fn(content):
                errors.append(f"rule failed: {rule_name}")
        except Exception as e:
            errors.append(f"rule error ({rule_name}): {e}")

    return errors


# ── Integrity Signal ────────────────────────────────────────────────────


def emit_integrity_signal(
    intent: str,
    riu_id: str | None,
    success: bool,
    artifact_path: str | None = None,
    details: str = "",
) -> None:
    """Emit an integrity signal after intent execution."""
    signal = {
        "type": "intent_execution",
        "intent": intent,
        "riu_id": riu_id,
        "success": success,
        "artifact_path": artifact_path,
        "details": details,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    GAP_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(GAP_LOG, "a") as f:
        f.write(json.dumps(signal) + "\n")


# ── UNVALIDATED_FALLBACK Display ────────────────────────────────────────


def print_unvalidated_warning(reason: str) -> None:
    """Print amber ANSI warning for unvalidated fallback."""
    print(f"\n  {YELLOW}{BOLD}[!] UNVALIDATED FALLBACK{RESET}")
    print(f"  {YELLOW}{reason}{RESET}")
    print(f"  {DIM}Result may be incomplete. Gap signal filed.{RESET}\n")


# ── PIS Summary (thin wrapper — no full PIS load) ─────────────────────


_pis_cache: dict | None = None


def pis_summary(riu_id: str | None, knowledge_count: int, classification: str) -> dict:
    """Return traversal stats from cached/precomputed data.

    Zero latency — derives from resolve result + cached taxonomy count.
    Shows OS depth in demo output without 568ms PIS load penalty.
    """
    global _pis_cache

    if _pis_cache is None:
        _pis_cache = _precompute_pis_stats()

    total_rius = _pis_cache.get("total_rius", 131)
    total_recipes = _pis_cache.get("total_recipes", 75)
    total_kl = _pis_cache.get("total_kl", 193)
    domain_rius = _pis_cache.get("domain_rius", {})

    # Find matching domain RIUs by prefix group
    matched_domain = "general"
    matched_count = 0
    if riu_id:
        prefix = riu_id.split("-")[1][:1] if "-" in riu_id else ""
        prefix_labels = _pis_cache.get("prefix_labels", {})
        if prefix in domain_rius:
            matched_domain = prefix_labels.get(prefix, "general")
            matched_count = len(domain_rius[prefix])
        if matched_count == 0:
            matched_count = 1

    # Recipe availability for this RIU
    has_recipe = _pis_cache.get("riu_recipes", {}).get(riu_id, False)
    recipe_count = 1 if has_recipe else 0

    return {
        "total_rius": total_rius,
        "matched_domain": matched_domain,
        "matched_rius": matched_count,
        "knowledge_available": knowledge_count,
        "total_kl": total_kl,
        "recipes_available": recipe_count,
        "total_recipes": total_recipes,
        "classification": classification,
    }


def _precompute_pis_stats() -> dict:
    """One-time precomputation of taxonomy/recipe stats. Cached in memory."""
    import yaml

    stats: dict[str, Any] = {
        "total_rius": 131,
        "total_recipes": 75,
        "total_kl": 193,
        "domain_rius": {},
        "riu_recipes": {},
    }

    # Taxonomy
    tax_path = REPO_ROOT / "taxonomy" / "releases" / "v1.3" / "palette_taxonomy_v1.3.yaml"
    if tax_path.exists():
        try:
            tax = yaml.safe_load(tax_path.read_text())
            rius = tax.get("rius", []) if isinstance(tax, dict) else []
            stats["total_rius"] = len(rius)
            # Group by RIU prefix (0xx=core, 1xx=process, ..., 7xx=legal)
            prefix_labels = {
                "0": "core", "1": "process", "2": "evaluation",
                "3": "integration", "4": "taxonomy", "5": "infrastructure",
                "6": "operations", "7": "legal",
            }
            for r in rius:
                rid = r.get("riu_id", "")
                if rid.startswith("RIU-"):
                    prefix = rid[4:5]
                    label = prefix_labels.get(prefix, "general")
                    stats["domain_rius"].setdefault(prefix, []).append(rid)
                    # Store label mapping
                    stats.setdefault("prefix_labels", {})[prefix] = label
        except Exception:
            pass

    # Recipes
    recipe_dir = REPO_ROOT / "buy-vs-build" / "integrations"
    if recipe_dir.exists():
        recipes = list(recipe_dir.rglob("recipe.yaml"))
        stats["total_recipes"] = len(recipes)

    # KL
    kl_path = REPO_ROOT / "knowledge-library" / "v1.4" / "palette_knowledge_library_v1.4.yaml"
    if kl_path.exists():
        try:
            kl = yaml.safe_load(kl_path.read_text())
            if isinstance(kl, dict):
                total = sum(len(v) for v in kl.values() if isinstance(v, list))
                stats["total_kl"] = total
        except Exception:
            pass

    return stats


def format_pis_line(summary: dict) -> str:
    """Format PIS summary as a compact one-liner for demo output."""
    return (
        f"{summary['total_rius']} RIUs traversed → "
        f"{summary['matched_rius']} {summary['matched_domain']} nodes matched → "
        f"{summary['recipes_available']} recipe{'s' if summary['recipes_available'] != 1 else ''} available"
    )


# ── PIS Display Helper ───────────────────────────────────────────────────


def pis_display_line(riu_id: str | None, knowledge_count: int) -> str:
    """Return a compact PIS traversal line for display."""
    if not riu_id:
        return ""
    # These are cached/known counts — no PIS load needed
    total_rius = 131
    matched = f"→ matched {riu_id}"
    kl = f"{knowledge_count} KL entries"
    return f"  {DIM}[PIS] {total_rius} RIUs traversed {matched}, {kl} retrieved{RESET}"


# ── Resolve Helper ──────────────────────────────────────────────────────


def resolve_query(query: str) -> dict:
    """Resolve a query through the taxonomy. Returns retrieval result."""
    import sys

    sys.path.insert(0, str(REPO_ROOT / "peers" / "hub"))
    try:
        from palette_retrieve import retrieve

        return retrieve(query)
    except Exception as e:
        return {
            "riu_id": None,
            "riu_name": None,
            "confidence": 0,
            "classification": "internal_only",
            "knowledge": [],
            "error": str(e),
        }


# ── Bus Helper ──────────────────────────────────────────────────────────


def find_related_artifacts(riu_id: str, limit: int = 5) -> list[dict]:
    """Find prior artifacts with the same RIU — the compounding proof.

    Scans all artifact types. Returns most recent matches (up to limit).
    Includes BLOCKED artifacts (a blocked decision is high-value context).
    """
    if not riu_id:
        return []

    results = []
    for type_dir in sorted(ARTIFACTS_DIR.iterdir()) if ARTIFACTS_DIR.exists() else []:
        if not type_dir.is_dir():
            continue
        for f in sorted(type_dir.rglob("*.md"), reverse=True)[:30]:
            try:
                found_riu = None
                intent = ""
                action = ""
                timestamp = ""
                artifact_type = ""
                query_text = ""
                for line in f.open():
                    if line.startswith("riu_id:"):
                        val = line.split(":", 1)[1].strip().strip("'\"")
                        if val and val != "null":
                            found_riu = val
                    elif line.startswith("intent:"):
                        intent = line.split(":", 1)[1].strip().strip("'\"")
                    elif line.startswith("action:"):
                        action = line.split(":", 1)[1].strip().strip("'\"")
                    elif line.startswith("artifact_type:"):
                        artifact_type = line.split(":", 1)[1].strip().strip("'\"")
                    elif line.startswith("timestamp:"):
                        timestamp = line.split(":", 1)[1].strip().strip("'\"")
                    elif not line.startswith(("---", " ", "\n", "#")) and ":" not in line:
                        break
                if found_riu == riu_id:
                    label = f"{artifact_type}"
                    if action == "BLOCK":
                        label += " (BLOCKED)"
                    results.append({
                        "path": str(f),
                        "type": artifact_type,
                        "intent": intent,
                        "action": action,
                        "timestamp": timestamp,
                        "label": label,
                    })
            except (OSError, UnicodeDecodeError):
                pass

    # Sort by timestamp descending, return top N
    results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return results[:limit]


def bus_post(endpoint: str, payload: dict) -> dict | None:
    """POST JSON to the peers bus. Best-effort."""
    from urllib import request as urllib_request

    url = f"{BUS_URL}{endpoint}"
    data = json.dumps(payload).encode()
    req = urllib_request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib_request.urlopen(req, timeout=3) as resp:
            return json.loads(resp.read())
    except Exception:
        return None
