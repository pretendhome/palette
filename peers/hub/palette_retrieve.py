#!/usr/bin/env python3
"""Palette retrieval for Voice Hub — classify query, retrieve knowledge.

Called by the Hub server as a subprocess:
  python3 palette_retrieve.py "how do I evaluate voice quality?"

Returns JSON:
  {
    "riu_id": "RIU-082",
    "riu_name": "Guardrails & Safety Evaluation",
    "confidence": 72.5,
    "classification": "both",
    "knowledge": [
      {"lib_id": "LIB-042", "question": "...", "answer_excerpt": "..."},
      ...
    ],
    "context": "Based on RIU-082 (Guardrails & Safety Evaluation):\n..."
  }
"""

import json
import sys
from pathlib import Path

# Add repo root to path so we can import PIS modules
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

from scripts.palette_intelligence_system.loader import load_all
from scripts.palette_intelligence_system.cli import keyword_resolve


def retrieve(query: str) -> dict:
    """Classify query and retrieve relevant knowledge."""
    data = load_all()  # uses PALETTE_ROOT env or ~/fde/palette default

    # Step 1: Resolve query to knowledge entry
    lib_id, confidence, top_3 = keyword_resolve(data, query)

    result = {
        "query": query,
        "lib_id": lib_id,
        "confidence": confidence,
        "top_candidates": [{"lib_id": c[0], "score": c[1]} for c in top_3],
        "riu_id": None,
        "riu_name": None,
        "classification": None,
        "knowledge": [],
        "context": "",
    }

    # Step 2: Get knowledge entry content
    knowledge_entries = []
    for candidate_id, score in top_3:
        entry = data.knowledge.get(candidate_id, {})
        if entry:
            knowledge_entries.append({
                "lib_id": candidate_id,
                "score": score,
                "question": str(entry.get("question", ""))[:200],
                "answer_excerpt": str(entry.get("answer", entry.get("content", "")))[:500],
                "tags": entry.get("tags", []),
                "journey_stage": entry.get("journey_stage", ""),
            })

    result["knowledge"] = knowledge_entries

    # Step 3: If we resolved to a lib_id, find its RIU
    if lib_id:
        entry = data.knowledge.get(lib_id, {})
        related_rius = entry.get("related_rius", [])
        if related_rius:
            riu_id = related_rius[0] if isinstance(related_rius[0], str) else str(related_rius[0])
            result["riu_id"] = riu_id

            # Get classification
            cls_entry = data.classification.get(riu_id, {})
            result["classification"] = cls_entry.get("classification", "unknown")
            result["riu_name"] = cls_entry.get("name", riu_id)

    # Step 4: Build context string for LLM injection
    ctx_parts = []
    if result["riu_id"]:
        ctx_parts.append(f"Palette classified this as {result['riu_id']} ({result['riu_name']}), classification: {result['classification']}.")

    for ke in knowledge_entries[:3]:
        ctx_parts.append(f"\nKnowledge [{ke['lib_id']}]: {ke['question']}")
        if ke["answer_excerpt"]:
            ctx_parts.append(ke["answer_excerpt"])

    result["context"] = "\n".join(ctx_parts) if ctx_parts else ""

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: palette_retrieve.py <query>"}))
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    result = retrieve(query)
    print(json.dumps(result))
