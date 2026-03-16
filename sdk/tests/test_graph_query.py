"""Tests for palette.sdk.graph_query — GraphQuery SPO queries."""

from __future__ import annotations

import os
import sys
import unittest

_palette_root = os.path.join(os.path.expanduser("~"), "fde", "palette")
_palette_parent = os.path.dirname(_palette_root)
if _palette_root not in sys.path:
    sys.path.insert(0, _palette_root)
if _palette_parent not in sys.path:
    sys.path.insert(0, _palette_parent)

from palette.sdk.graph_query import GraphQuery


# ── Sample quads ──────────────────────────────────────────────────────

SAMPLE_QUADS = [
    {"id": "Q001", "subject": "Architect", "predicate": "handles_riu", "object": "RIU-001"},
    {"id": "Q002", "subject": "Architect", "predicate": "handles_riu", "object": "RIU-014"},
    {"id": "Q003", "subject": "RIU-082", "predicate": "has_service", "object": "Bedrock Guardrails"},
    {"id": "Q004", "subject": "RIU-082", "predicate": "has_knowledge", "object": "LIB-042"},
    {"id": "Q005", "subject": "PERSON-019", "predicate": "recommends", "object": "OpenRouter"},
    {"id": "Q006", "subject": "PERSON-020", "predicate": "recommends", "object": "OpenRouter"},
    {"id": "Q007", "subject": "RIU-082", "predicate": "routed_to", "object": "Validator"},
]


# ── Construction ──────────────────────────────────────────────────────

class TestConstruction(unittest.TestCase):

    def test_empty_graph(self):
        gq = GraphQuery([])
        self.assertEqual(gq.quad_count, 0)
        self.assertEqual(gq.predicates, [])
        self.assertEqual(gq.subjects, [])

    def test_sample_counts(self):
        gq = GraphQuery(SAMPLE_QUADS)
        self.assertEqual(gq.quad_count, 7)
        self.assertIn("handles_riu", gq.predicates)
        self.assertIn("Architect", gq.subjects)


# ── Query tests ───────────────────────────────────────────────────────

class TestQuery(unittest.TestCase):

    def setUp(self):
        self.gq = GraphQuery(SAMPLE_QUADS)

    def test_query_by_subject(self):
        results = self.gq.query(subject="Architect")
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r["subject"] == "Architect" for r in results))

    def test_query_by_predicate(self):
        results = self.gq.query(predicate="recommends")
        self.assertEqual(len(results), 2)

    def test_query_by_object(self):
        results = self.gq.query(object="OpenRouter")
        self.assertEqual(len(results), 2)

    def test_query_by_subject_and_predicate(self):
        results = self.gq.query(subject="RIU-082", predicate="has_service")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["object"], "Bedrock Guardrails")

    def test_query_all(self):
        results = self.gq.query()
        self.assertEqual(len(results), 7)

    def test_query_no_match(self):
        results = self.gq.query(subject="Nonexistent")
        self.assertEqual(results, [])


# ── Shorthand methods ─────────────────────────────────────────────────

class TestShorthands(unittest.TestCase):

    def setUp(self):
        self.gq = GraphQuery(SAMPLE_QUADS)

    def test_objects_for(self):
        objects = self.gq.objects_for("Architect", "handles_riu")
        self.assertIn("RIU-001", objects)
        self.assertIn("RIU-014", objects)
        self.assertEqual(len(objects), 2)

    def test_subjects_for(self):
        subjects = self.gq.subjects_for("recommends", "OpenRouter")
        self.assertIn("PERSON-019", subjects)
        self.assertIn("PERSON-020", subjects)

    def test_objects_for_no_match(self):
        self.assertEqual(self.gq.objects_for("Nobody", "nothing"), [])


# ── Neighbors ─────────────────────────────────────────────────────────

class TestNeighbors(unittest.TestCase):

    def setUp(self):
        self.gq = GraphQuery(SAMPLE_QUADS)

    def test_neighbors_as_subject(self):
        n = self.gq.neighbors("RIU-082")
        self.assertIn("has_service", n)
        self.assertIn("Bedrock Guardrails", n["has_service"])
        self.assertIn("has_knowledge", n)
        self.assertIn("LIB-042", n["has_knowledge"])

    def test_neighbors_as_object(self):
        n = self.gq.neighbors("OpenRouter")
        self.assertIn("<-recommends", n)
        self.assertIn("PERSON-019", n["<-recommends"])

    def test_neighbors_no_match(self):
        n = self.gq.neighbors("Nonexistent")
        self.assertEqual(n, {})


# ── Summary ───────────────────────────────────────────────────────────

class TestSummary(unittest.TestCase):

    def test_summary_structure(self):
        gq = GraphQuery(SAMPLE_QUADS)
        s = gq.summary()
        self.assertEqual(s["total_quads"], 7)
        self.assertIn("predicates", s)
        self.assertEqual(s["predicates"]["handles_riu"], 2)
        self.assertGreater(s["unique_subjects"], 0)
        self.assertGreater(s["unique_objects"], 0)


# ── from_yaml ─────────────────────────────────────────────────────────

class TestFromYAML(unittest.TestCase):

    def test_load_real_graph(self):
        gq = GraphQuery.from_yaml(_palette_root)
        self.assertIsNotNone(gq)
        self.assertGreater(gq.quad_count, 1000)

    def test_load_missing_yaml_returns_none(self):
        gq = GraphQuery.from_yaml("/tmp/nonexistent-palette")
        self.assertIsNone(gq)


if __name__ == "__main__":
    unittest.main()
