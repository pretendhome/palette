#!/usr/bin/env python3
"""Palette Hybrid Retrieval — FTS5 + Vector + Keyword with RRF reranking.

Three retrieval modes combined via Reciprocal Rank Fusion:
  1. keyword_resolve (existing prefix matching)
  2. FTS5 full-text search (porter stemming, BM25)
  3. Vector similarity (nomic-embed-text via Ollama)

Called by Voice Hub as subprocess:
  python3 palette_retrieve.py "how do I evaluate voice quality?"

Returns JSON with ranked results, RIU classification, and context string.
"""

import json
import re
import sqlite3
import sys
from pathlib import Path

import numpy as np
import yaml

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

from scripts.palette_intelligence_system.loader import load_all
from scripts.palette_intelligence_system.cli import keyword_resolve

EMBEDDINGS_PATH = Path(__file__).parent / "kl_embeddings.json"
FTS_DB_PATH = Path(__file__).parent / "kl_fts.db"
OLLAMA_URL = "http://localhost:11434/api/embed"
LEGAL_DEMO_PACK_PATH = repo_root / "bdb" / "legal_demo_pack.yaml"
RRF_K = 60  # RRF constant

STOP_WORDS = frozenset(
    "how do i the a an is my to for what when should are can does it in of on "
    "with that this be from or and".split()
)


def _load_embeddings():
    """Load pre-computed KL embeddings from JSON."""
    if not EMBEDDINGS_PATH.exists():
        return {}
    with open(EMBEDDINGS_PATH) as f:
        return json.load(f)


def _ensure_fts_db(data):
    """Create/rebuild FTS5 index if missing."""
    if FTS_DB_PATH.exists():
        return sqlite3.connect(str(FTS_DB_PATH))

    conn = sqlite3.connect(str(FTS_DB_PATH))
    conn.execute(
        "CREATE VIRTUAL TABLE kl_fts USING fts5("
        "lib_id UNINDEXED, content, tokenize='porter unicode61')"
    )
    for lib_id, entry in data.knowledge.items():
        q = entry.get("question", "")
        a = str(entry.get("answer", entry.get("summary", "")))
        tags = " ".join(entry.get("tags", []))
        conn.execute("INSERT INTO kl_fts VALUES (?, ?)", (lib_id, f"{q} {a} {tags}"))
    conn.commit()
    return conn


def _fts5_query(query: str) -> str:
    """Convert natural language to FTS5 OR query with stop word removal."""
    words = re.findall(r"[a-zA-Z0-9]+", query.lower())
    keywords = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    return " OR ".join(keywords) if keywords else query


def _embed_query(query: str) -> list[float] | None:
    """Get embedding for query via Ollama."""
    try:
        import httpx
        resp = httpx.post(OLLAMA_URL, json={"model": "nomic-embed-text", "input": query}, timeout=10.0)
        if resp.status_code == 200:
            return resp.json()["embeddings"][0]
    except Exception:
        pass
    return None


def _cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def _load_legal_demo_pack():
    """Load the lightweight legal demo pack used for BDB demo queries."""
    if not LEGAL_DEMO_PACK_PATH.exists():
        return {}
    with open(LEGAL_DEMO_PACK_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _legal_demo_override(query: str) -> dict | None:
    """Route legal queries through the real RIU-700 taxonomy nodes.

    This replaces the old hardcoded LEGAL-001/002/003 pseudo-IDs.
    Now uses the canonical taxonomy for classification and the real
    knowledge library (LIB-200 through LIB-209) for retrieval.
    """
    lowered = query.lower()
    legal_tokens = [
        "delaware", "fiduciary", "settle", "settlement", "self-dealing",
        "opposing counsel", "exposure", "breach of duty", "llc co-founder",
        "related-party", "privilege", "filing deadline", "conflict of interest",
        "contract clause", "indemnification", "regulatory compliance",
    ]
    if not any(token in lowered for token in legal_tokens):
        return None

    pack = _load_legal_demo_pack()
    entries = {entry["id"]: entry for entry in pack.get("entries", [])}
    if not entries:
        return None

    def make_knowledge(entry_ids: list[str]) -> list[dict]:
        knowledge = []
        for entry_id in entry_ids:
            entry = entries.get(entry_id)
            if not entry:
                continue
            knowledge.append({
                "lib_id": entry["id"],
                "score": entry.get("score", 80.0),
                "question": entry.get("question", ""),
                "answer_excerpt": entry.get("answer", ""),
                "tags": entry.get("tags", []),
                "journey_stage": entry.get("journey_stage", "analysis"),
            })
        return knowledge

    # ── Route through canonical RIU-700 taxonomy ──

    # RIU-709: Fiduciary Duty Analysis (internal_only)
    if any(w in lowered for w in ["exposure", "self-dealing", "related-party", "our position", "our case"]):
        knowledge = make_knowledge(["LEGAL-KL-001", "LEGAL-KL-002", "LEGAL-KL-004"])
        return _build_legal_result(query, "RIU-709", "Fiduciary Duty Analysis", "internal_only", 72.0, knowledge)

    # RIU-708: Settlement Analysis (both — adversarial critique)
    if any(w in lowered for w in ["opposing counsel", "argue", "counter-argument", "weakness", "what are we missing"]):
        knowledge = make_knowledge(["LEGAL-KL-001", "LEGAL-KL-002", "LEGAL-KL-004"])
        return _build_legal_result(query, "RIU-708", "Settlement Analysis", "both", 68.0, knowledge)

    # RIU-701: Legal Precedent Research (both — external allowed)
    if any(w in lowered for w in ["llc co-founder", "llc member", "fiduciary duty standard", "fiduciary duty standards", "precedent", "precedents", "case law"]):
        knowledge = make_knowledge(["LEGAL-KL-001", "LEGAL-KL-002", "LEGAL-KL-003"])
        return _build_legal_result(query, "RIU-701", "Legal Precedent Research", "both", 45.0, knowledge)

    # RIU-708: Settlement Analysis (internal_only — settlement strategy)
    if "settle" in lowered or "settlement" in lowered:
        knowledge = make_knowledge(["LEGAL-KL-004", "LEGAL-KL-005"])
        return _build_legal_result(query, "RIU-708", "Settlement Analysis", "internal_only", 34.0, knowledge)

    # RIU-702: Filing Deadline Tracking (internal_only)
    if "deadline" in lowered or "deadlines" in lowered or "filing" in lowered:
        knowledge = make_knowledge(["LEGAL-KL-006", "LEGAL-KL-007", "LEGAL-KL-008"])
        return _build_legal_result(query, "RIU-702", "Filing Deadline Tracking", "internal_only", 74.0, knowledge)

    # RIU-701: Legal Precedent Research (both — general Delaware research)
    if "delaware" in lowered:
        knowledge = make_knowledge(["LEGAL-KL-001", "LEGAL-KL-002", "LEGAL-KL-003"])
        return _build_legal_result(query, "RIU-701", "Legal Precedent Research", "both", 40.0, knowledge)

    # RIU-703: Conflict of Interest Check (internal_only)
    if "conflict" in lowered:
        knowledge = make_knowledge(["LEGAL-KL-004", "LEGAL-KL-005"])
        return _build_legal_result(query, "RIU-703", "Conflict of Interest Check", "internal_only", 65.0, knowledge)

    # RIU-705: Regulatory Compliance Check (both)
    if "regulatory" in lowered or "compliance" in lowered:
        knowledge = make_knowledge(["LEGAL-KL-005", "LEGAL-KL-006"])
        return _build_legal_result(query, "RIU-705", "Regulatory Compliance Check", "both", 55.0, knowledge)

    return None


def _build_legal_result(query: str, riu_id: str, riu_name: str, classification: str, confidence: float, knowledge: list[dict]) -> dict:
    """Build a standardized legal retrieval result using canonical RIU IDs."""
    context = "\n".join(
        [f"Palette classified this as {riu_id} ({riu_name}), classification: {classification}."]
        + [f"\nKnowledge [{k['lib_id']}]: {k['question']}\n{k['answer_excerpt']}" for k in knowledge]
    )
    return {
        "query": query,
        "mode": "hybrid",
        "retrieval_modes": ["legal_knowledge_library"],
        "lib_id": knowledge[0]["lib_id"] if knowledge else None,
        "confidence": confidence,
        "riu_id": riu_id,
        "riu_name": riu_name,
        "classification": classification,
        "knowledge": knowledge,
        "context": context,
    }


def hybrid_retrieve(query: str, data=None, top_k: int = 5) -> list[tuple[str, float]]:
    """Run retrieval modes and combine with RRF.

    Optimization: skips expensive vector search if keyword_resolve is high-confidence (≥60%).
    Returns list of (lib_id, rrf_score) sorted by score descending.
    """
    if data is None:
        data = load_all()

    rankings = []  # list of ranked lists: [[lib_id, ...], ...]

    # Mode 1: keyword_resolve (fast, ~1ms)
    _, kw_conf, kw_top = keyword_resolve(data, query)
    if kw_top:
        rankings.append([lib_id for lib_id, _ in kw_top])

    # Mode 2: FTS5 (fast, ~5ms)
    try:
        conn = _ensure_fts_db(data)
        fts_q = _fts5_query(query)
        rows = conn.execute(
            "SELECT lib_id FROM kl_fts WHERE kl_fts MATCH ? ORDER BY rank LIMIT ?",
            (fts_q, top_k * 2),
        ).fetchall()
        if rows:
            rankings.append([r[0] for r in rows])
    except Exception:
        pass

    # Mode 3: Vector similarity (slow, ~500ms) — skip if keyword is confident
    if kw_conf < 60:
        embeddings = _load_embeddings()
        if embeddings:
            query_emb = _embed_query(query)
            if query_emb:
                sims = []
                for lib_id, obj in embeddings.items():
                    sim = _cosine_similarity(query_emb, obj["embedding"])
                    sims.append((lib_id, sim))
                sims.sort(key=lambda x: -x[1])
                rankings.append([lib_id for lib_id, _ in sims[: top_k * 2]])

    # Reciprocal Rank Fusion
    scores: dict[str, float] = {}
    for ranked_list in rankings:
        for rank, lib_id in enumerate(ranked_list, 1):
            scores[lib_id] = scores.get(lib_id, 0) + 1.0 / (RRF_K + rank)

    # Boost by evidence tier
    for lib_id in scores:
        entry = data.knowledge.get(lib_id, {})
        tier = entry.get("evidence_tier", entry.get("tier", 3))
        if isinstance(tier, str):
            tier = {"1": 1, "2": 2, "3": 3}.get(tier.strip(), 3)
        tier_boost = {1: 1.2, 2: 1.0, 3: 0.9}.get(tier, 1.0)
        scores[lib_id] *= tier_boost

    ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_k]

    # Normalize to 0-100 (relative to theoretical max: 3 lists × rank-1 × max boost)
    max_possible = len(rankings) * (1.0 / (RRF_K + 1)) * 1.2
    if max_possible > 0:
        ranked = [(lib_id, min(100.0, (score / max_possible) * 100)) for lib_id, score in ranked]

    return ranked


def retrieve(query: str) -> dict:
    """Full retrieval pipeline: classify + hybrid retrieve + build context."""
    legal_override = _legal_demo_override(query)
    if legal_override:
        return legal_override

    data = load_all()

    # Hybrid retrieval
    ranked = hybrid_retrieve(query, data, top_k=5)

    # Build result
    result = {
        "query": query,
        "mode": "hybrid",
        "retrieval_modes": [],
        "lib_id": ranked[0][0] if ranked else None,
        "confidence": ranked[0][1] if ranked else 0,
        "riu_id": None,
        "riu_name": None,
        "classification": None,
        "knowledge": [],
        "context": "",
    }

    # Track which modes contributed
    modes = ["keyword"]
    if FTS_DB_PATH.exists():
        modes.append("fts5")
    if EMBEDDINGS_PATH.exists():
        modes.append("vector")
    result["retrieval_modes"] = modes

    # Build knowledge entries
    for lib_id, score in ranked[:3]:
        entry = data.knowledge.get(lib_id, {})
        if entry:
            result["knowledge"].append({
                "lib_id": lib_id,
                "score": round(score, 1),
                "question": str(entry.get("question", ""))[:200],
                "answer_excerpt": str(entry.get("answer", entry.get("content", "")))[:500],
                "tags": entry.get("tags", []),
                "journey_stage": entry.get("journey_stage", ""),
            })

    # Find RIU from top result (fall through if top has no RIU)
    if ranked:
        for lib_id, _ in ranked[:5]:
            top_entry = data.knowledge.get(lib_id, {})
            related_rius = top_entry.get("related_rius", [])
            if related_rius:
                riu_id = related_rius[0] if isinstance(related_rius[0], str) else str(related_rius[0])
                result["riu_id"] = riu_id
                cls_entry = data.classification.get(riu_id, {})
                result["classification"] = cls_entry.get("classification", "unknown")
                result["riu_name"] = cls_entry.get("name", riu_id)
                break

    # Build context string for LLM injection
    ctx_parts = []
    if result["riu_id"]:
        ctx_parts.append(
            f"Palette classified this as {result['riu_id']} ({result['riu_name']}), "
            f"classification: {result['classification']}."
        )
    for ke in result["knowledge"][:3]:
        ctx_parts.append(f"\nKnowledge [{ke['lib_id']}]: {ke['question']}")
        if ke["answer_excerpt"]:
            ctx_parts.append(ke["answer_excerpt"])

    result["context"] = "\n".join(ctx_parts) if ctx_parts else ""
    return result


def find_enablement_module(riu_id: str) -> dict | None:
    """Find enablement curriculum module for a given RIU."""
    enablement_root = repo_root.parent / "enablement" / "curriculum" / "workstreams"
    if not enablement_root.exists():
        return None
    for ws_dir in enablement_root.iterdir():
        if not ws_dir.is_dir():
            continue
        mod_path = ws_dir / riu_id / "module.yaml"
        if mod_path.exists():
            with open(mod_path) as f:
                return yaml.safe_load(f)
    return None


def retrieve_learn(query: str) -> dict:
    """Retrieve in learning mode — includes enablement module content."""
    result = retrieve(query)
    result["mode"] = "learn"

    if result["riu_id"]:
        module = find_enablement_module(result["riu_id"])
        if module:
            result["enablement"] = {
                "riu_id": module.get("riu_id", ""),
                "name": module.get("name", ""),
                "objectives": module.get("learning_objectives", []),
                "difficulty": module.get("difficulty", ""),
                "duration": module.get("estimated_duration", {}),
                "description": module.get("description", ""),
                "prerequisites": module.get("prerequisites", {}),
            }
            obj_text = "\n".join(f"- {o}" for o in module.get("learning_objectives", []))
            result["context"] = (
                f"LEARNING MODE — Teach the user about: {module.get('name', '')}\n"
                f"RIU: {result['riu_id']} | Difficulty: {module.get('difficulty', 'unknown')}\n\n"
                f"Learning Objectives:\n{obj_text}\n\n"
                f"Description: {module.get('description', '')}\n\n"
                f"Grounding knowledge:\n{result['context']}"
            )
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: palette_retrieve.py [--learn] <query>"}))
        sys.exit(1)

    args = sys.argv[1:]
    learn_mode = "--learn" in args
    if learn_mode:
        args.remove("--learn")

    query = " ".join(args)
    result = retrieve_learn(query) if learn_mode else retrieve(query)
    print(json.dumps(result, indent=2))
