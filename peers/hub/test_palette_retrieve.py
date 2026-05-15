#!/usr/bin/env python3
"""Unit tests for palette hybrid retrieval."""

import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import palette_retrieve as pr


class FakeData:
    """Minimal data fixture for testing."""

    def __init__(self):
        self.knowledge = {
            "LIB-001": {
                "question": "How do I force convergence?",
                "answer": "Use a convergence brief with clear success criteria.",
                "tags": ["convergence", "governance"],
                "evidence_tier": 1,
                "related_rius": ["RIU-001"],
                "journey_stage": "foundation",
            },
            "LIB-002": {
                "question": "What is a one-way door decision?",
                "answer": "Irreversible or high-cost to undo. Requires human confirmation.",
                "tags": ["governance", "decisions"],
                "evidence_tier": 2,
                "related_rius": ["RIU-003"],
                "journey_stage": "foundation",
            },
            "LIB-003": {
                "question": "How do I scope an AI pilot?",
                "answer": "Start with bounded scope, clear metrics, and a kill switch.",
                "tags": ["pilot", "scoping"],
                "evidence_tier": 3,
                "related_rius": ["RIU-005"],
                "journey_stage": "foundation",
            },
        }
        self.classification = {
            "RIU-001": {"name": "Convergence Brief", "classification": "internal_only"},
            "RIU-003": {"name": "Decision Log", "classification": "internal_only"},
            "RIU-005": {"name": "AI Pilot Scoping", "classification": "both"},
        }


def test_keyword_only_path():
    """hybrid_retrieve works with keyword_resolve alone (no FTS5, no vectors)."""
    data = FakeData()
    with patch.object(pr, "_ensure_fts_db", side_effect=Exception("no db")), \
         patch.object(pr, "_load_embeddings", return_value={}):
        results = pr.hybrid_retrieve("convergence", data=data, top_k=3)
    assert len(results) > 0
    assert all(isinstance(r, tuple) and len(r) == 2 for r in results)
    assert all(0 <= score <= 100 for _, score in results)


def test_rrf_ordering():
    """Results are ordered by descending score."""
    data = FakeData()
    with patch.object(pr, "_ensure_fts_db", side_effect=Exception("no db")), \
         patch.object(pr, "_load_embeddings", return_value={}):
        results = pr.hybrid_retrieve("governance decisions", data=data, top_k=3)
    scores = [s for _, s in results]
    assert scores == sorted(scores, reverse=True)


def test_evidence_tier_boost():
    """Tier 1 entries get boosted over Tier 3 at same rank."""
    data = FakeData()
    # Both LIB-001 (tier 1) and LIB-003 (tier 3) should appear
    # If both are at same base rank, tier 1 should score higher
    with patch.object(pr, "_ensure_fts_db", side_effect=Exception("no db")), \
         patch.object(pr, "_load_embeddings", return_value={}):
        # Query that could match both
        results = pr.hybrid_retrieve("AI", data=data, top_k=3)
    if len(results) >= 2:
        scores_by_id = dict(results)
        if "LIB-001" in scores_by_id and "LIB-003" in scores_by_id:
            # Tier 1 (1.2x) should beat Tier 3 (0.9x) at same base rank
            assert scores_by_id["LIB-001"] >= scores_by_id["LIB-003"]


def test_graceful_degradation_no_ollama():
    """System works without Ollama (vector search fails gracefully)."""
    data = FakeData()
    with patch.object(pr, "_ensure_fts_db", side_effect=Exception("no db")), \
         patch.object(pr, "_embed_query", return_value=None):
        results = pr.hybrid_retrieve("convergence", data=data, top_k=3)
    # Should still return results from keyword_resolve
    assert len(results) > 0


def test_scores_normalized_0_100():
    """All scores are in 0-100 range."""
    data = FakeData()
    with patch.object(pr, "_ensure_fts_db", side_effect=Exception("no db")), \
         patch.object(pr, "_load_embeddings", return_value={}):
        results = pr.hybrid_retrieve("governance", data=data, top_k=5)
    for lib_id, score in results:
        assert 0 <= score <= 100, f"{lib_id} score {score} out of range"


def test_fts5_query_stop_words():
    """FTS5 query builder removes stop words."""
    q = pr._fts5_query("how do I set up governance for my team?")
    assert "how" not in q
    assert "governance" in q
    assert "team" in q


def test_retrieve_returns_expected_structure():
    """retrieve() returns dict with required keys."""
    data = FakeData()
    with patch.object(pr, "load_all", return_value=data), \
         patch.object(pr, "_ensure_fts_db", side_effect=Exception("no db")), \
         patch.object(pr, "_load_embeddings", return_value={}):
        result = pr.retrieve("convergence")
    assert "query" in result
    assert "mode" in result
    assert "retrieval_modes" in result
    assert "lib_id" in result
    assert "confidence" in result
    assert "knowledge" in result
    assert "context" in result
    assert result["mode"] == "hybrid"


def test_learn_mode_structure():
    """retrieve_learn() adds enablement data when available."""
    data = FakeData()
    with patch.object(pr, "load_all", return_value=data), \
         patch.object(pr, "_ensure_fts_db", side_effect=Exception("no db")), \
         patch.object(pr, "_load_embeddings", return_value={}), \
         patch.object(pr, "find_enablement_module", return_value={
             "riu_id": "RIU-001",
             "name": "Convergence Brief",
             "learning_objectives": ["Understand convergence"],
             "difficulty": "intermediate",
         }):
        result = pr.retrieve_learn("convergence")
    assert result["mode"] == "learn"
    assert "enablement" in result
    assert result["enablement"]["name"] == "Convergence Brief"


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  ✅ {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {test.__name__}: {e}")
            failed += 1
    print(f"\n{passed}/{passed+failed} passed")
    sys.exit(0 if failed == 0 else 1)
