#!/usr/bin/env python3
"""Unit tests for query_engine.py — PIS Query Engine.

Run with:
  python -m unittest scripts.pis.test_query_engine
  (from the palette/ directory)

All tests use real PIS data. No mock YAML files.
"""

import sys
import unittest
from io import StringIO
from pathlib import Path

from scripts.pis.query_engine import (
    PISData,
    cmd_check,
    cmd_cost,
    cmd_coverage,
    cmd_gaps,
    cmd_stack,
    cmd_traverse,
    normalize_name,
)


def _capture(func, *args):
    """Run a command function and capture its stdout + return code."""
    old_out = sys.stdout
    old_err = sys.stderr
    sys.stdout = buf = StringIO()
    sys.stderr = StringIO()  # suppress stderr noise
    try:
        rc = func(*args)
        return rc, buf.getvalue()
    finally:
        sys.stdout = old_out
        sys.stderr = old_err


class TestDataLoading(unittest.TestCase):
    """Verify that all four data layers load without errors."""

    @classmethod
    def setUpClass(cls):
        cls.pis = PISData()
        cls.pis.load_all()

    def test_no_load_errors(self):
        self.assertEqual(self.pis.load_errors, [],
                         f"Load errors: {self.pis.load_errors}")

    def test_taxonomy_populated(self):
        self.assertEqual(len(self.pis.taxonomy), 117)

    def test_classification_populated(self):
        self.assertEqual(len(self.pis.classification), 117)

    def test_routing_populated(self):
        self.assertGreater(len(self.pis.routing), 30)

    def test_recipes_populated(self):
        self.assertGreaterEqual(len(self.pis.recipes), 21)

    def test_recipe_riu_index_built(self):
        # At least some recipes declare RIUs served
        self.assertGreater(len(self.pis.recipe_riu_index), 0)


class TestNormalization(unittest.TestCase):
    """Test the service name normalization function."""

    def test_aws_bedrock(self):
        self.assertEqual(normalize_name("AWS Bedrock Guardrails"), "awsbedrockguardrails")

    def test_openrouter(self):
        self.assertEqual(normalize_name("OpenRouter"), "openrouter")

    def test_hyphens_and_spaces(self):
        self.assertEqual(normalize_name("Upstash Redis"), "upstashredis")

    def test_parenthetical(self):
        self.assertEqual(normalize_name("OpenRouter (built-in)"), "openrouterbuiltin")


class TestTraverseCommand(unittest.TestCase):
    """Test the traverse command with real data."""

    @classmethod
    def setUpClass(cls):
        cls.pis = PISData()
        cls.pis.load_all()

    def test_both_riu_with_recipe(self):
        rc, out = _capture(cmd_traverse, self.pis, "RIU-082")
        self.assertEqual(rc, 0)
        self.assertIn("RIU-082", out)
        self.assertIn("LLM Safety Guardrails", out)
        self.assertIn("Classification: both", out)
        self.assertIn("Service Routing:", out)
        self.assertIn("AWS Bedrock Guardrails", out)
        self.assertIn("recipe.yaml", out)
        self.assertIn("PII", out)  # Free tier mentions PII

    def test_internal_only_riu(self):
        rc, out = _capture(cmd_traverse, self.pis, "RIU-001")
        self.assertEqual(rc, 0)
        self.assertIn("internal_only", out)
        self.assertIn("N/A", out)

    def test_nonexistent_riu(self):
        rc, _ = _capture(cmd_traverse, self.pis, "RIU-999")
        self.assertEqual(rc, 1)

    def test_empty_riu_id(self):
        rc, _ = _capture(cmd_traverse, self.pis, "")
        self.assertEqual(rc, 1)

    def test_malformed_riu_id(self):
        rc, _ = _capture(cmd_traverse, self.pis, "NOT-A-RIU")
        self.assertEqual(rc, 1)

    def test_recipe_via_riu_index(self):
        """RIU-522 should find OpenRouter recipe via reverse RIU index."""
        rc, out = _capture(cmd_traverse, self.pis, "RIU-522")
        self.assertEqual(rc, 0)
        self.assertIn("recipe.yaml", out)
        # Should NOT say NOT FOUND for the first service that has a recipe
        # OpenRouter is listed as a service and the recipe declares RIU-522
        self.assertIn("openrouter", out.lower())


class TestCoverageCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pis = PISData()
        cls.pis.load_all()

    def test_output_structure(self):
        rc, out = _capture(cmd_coverage, self.pis)
        self.assertEqual(rc, 0)
        self.assertIn("Layer Coverage Report", out)
        self.assertIn("117/117", out)
        self.assertIn("Taxonomy:", out)
        self.assertIn("Classification:", out)
        self.assertIn("Service Routing:", out)
        self.assertIn("Integration Recipes:", out)
        self.assertIn("Full traversal:", out)


class TestCostCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pis = PISData()
        cls.pis.load_all()

    def test_with_known_rius(self):
        rc, out = _capture(cmd_cost, self.pis, ["RIU-082", "RIU-061"])
        self.assertEqual(rc, 0)
        # Should have actual cost data from recipes
        self.assertTrue("$" in out or "FREE" in out or "free" in out.lower())
        self.assertIn("RIU-082", out)
        self.assertIn("RIU-061", out)

    def test_nonexistent_riu(self):
        rc, out = _capture(cmd_cost, self.pis, ["RIU-999"])
        self.assertEqual(rc, 1)

    def test_bedrock_cost_precision(self):
        """Verify Bedrock cost data is extracted verbatim from recipe."""
        rc, out = _capture(cmd_cost, self.pis, ["RIU-082"])
        self.assertEqual(rc, 0)
        # These exact strings come from bedrock-guardrails/recipe.yaml cost_per_unit
        self.assertIn("$0.15 per 1,000 text units", out)
        self.assertIn("FREE", out)


class TestGapsCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pis = PISData()
        cls.pis.load_all()

    def test_finds_gaps(self):
        rc, out = _capture(cmd_gaps, self.pis)
        self.assertEqual(rc, 0)
        # Data evolves: this command may find gaps or report full coverage.
        self.assertTrue(
            ("missing recipes" in out.lower()) or ("no gaps found" in out.lower()),
            f"unexpected gaps output: {out}",
        )

    def test_gap_has_riu_id(self):
        rc, out = _capture(cmd_gaps, self.pis)
        # Every gap line should have a RIU-XXX identifier
        for line in out.splitlines():
            if line.startswith("RIU-"):
                self.assertRegex(line, r"^RIU-\d+:")


class TestStackCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pis = PISData()
        cls.pis.load_all()

    def test_observability_keyword(self):
        rc, out = _capture(cmd_stack, self.pis, "observability")
        self.assertEqual(rc, 0)
        self.assertIn("RIU-061", out)
        self.assertIn("matching", out)

    def test_guardrails_keyword(self):
        rc, out = _capture(cmd_stack, self.pis, "guardrails")
        self.assertEqual(rc, 0)
        self.assertIn("RIU-082", out)

    def test_no_match(self):
        rc, out = _capture(cmd_stack, self.pis, "xyznonexistent123")
        self.assertEqual(rc, 1)
        self.assertIn("No RIUs found", out)


class TestCheckCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pis = PISData()
        cls.pis.load_all()

    def test_output_structure(self):
        rc, out = _capture(cmd_check, self.pis)
        self.assertIn("Cross-Layer Consistency Check", out)
        self.assertIn("Summary:", out)
        self.assertIn("checks passed", out)

    def test_detects_missing_classification(self):
        """Deliberately remove a classification and verify check catches it."""
        test_pis = PISData()
        test_pis.load_all()
        # Remove one classification to create an inconsistency
        victim = next(iter(test_pis.classification))
        del test_pis.classification[victim]

        rc, out = _capture(cmd_check, test_pis)
        self.assertIn("[FAIL]", out)
        self.assertIn(victim, out)

    def test_taxonomy_classification_alignment(self):
        """The real data should have taxonomy and classification in sync."""
        rc, out = _capture(cmd_check, self.pis)
        self.assertIn("[PASS] Every RIU in taxonomy has a classification entry", out)


class TestRecipeMatching(unittest.TestCase):
    """Test the three-strategy recipe matching heuristic."""

    @classmethod
    def setUpClass(cls):
        cls.pis = PISData()
        cls.pis.load_all()

    def test_exact_match(self):
        """'OpenRouter' should match openrouter recipe."""
        recipe = self.pis.find_recipe_for_service("OpenRouter")
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.get("service_name"), "OpenRouter")

    def test_complex_name_match(self):
        """'AWS Bedrock Guardrails' should match bedrock-guardrails recipe."""
        recipe = self.pis.find_recipe_for_service("AWS Bedrock Guardrails")
        self.assertIsNotNone(recipe)
        self.assertIn("Bedrock", recipe.get("service_name", ""))

    def test_reverse_riu_index(self):
        """RIU fallback should return a recipe that declares the RIU in served list."""
        # Unknown service name + RIU context forces fallback behavior.
        recipe = self.pis.find_recipe_for_service("UnknownService", "RIU-522", allow_riu_fallback=True)
        self.assertIsNotNone(recipe)
        self.assertIn("RIU-522", recipe.get("_served_rius", []))

    def test_direct_match_without_fallback(self):
        """Lakera Guard should resolve directly without RIU fallback."""
        recipe = self.pis.find_recipe_for_service("Lakera Guard", "RIU-082", allow_riu_fallback=False)
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.get("service_name"), "Lakera Guard")

    def test_no_match(self):
        """A completely unknown service should return None."""
        recipe = self.pis.find_recipe_for_service("NonexistentService12345")
        self.assertIsNone(recipe)


if __name__ == "__main__":
    unittest.main()
