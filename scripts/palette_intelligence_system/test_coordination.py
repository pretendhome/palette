#!/usr/bin/env python3
"""Unit tests for scripts.palette_intelligence_system.coordination — HandoffPacket v2 + replay.

Run with:
  python -m unittest scripts.palette_intelligence_system.test_coordination
(from palette/)

All tests use real PIS data. Resolver step uses keyword_resolve (no LLM).
Each test uses its own temp directory for state isolation.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from scripts.palette_intelligence_system import coordination


class CoordinationBase(unittest.TestCase):
    """Base class: isolate state dir per test."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self._old_env = os.environ.get("PIS_COORDINATION_STATE_DIR")
        os.environ["PIS_COORDINATION_STATE_DIR"] = self.tmp.name

    def tearDown(self):
        if self._old_env is None:
            os.environ.pop("PIS_COORDINATION_STATE_DIR", None)
        else:
            os.environ["PIS_COORDINATION_STATE_DIR"] = self._old_env

    def _task_files(self) -> list[Path]:
        return sorted(Path(self.tmp.name).glob("*.json"))

    def _load_only_packet(self) -> dict:
        files = self._task_files()
        self.assertEqual(len(files), 1, f"Expected 1 packet, found {len(files)}")
        with open(files[0], encoding="utf-8") as f:
            return json.load(f)


# ── Packet Creation ────────────────────────────────────────────────

class TestPacketCreation(CoordinationBase):

    def test_run_creates_valid_packet(self):
        rc = coordination.main(["run", "add guardrails to my llm app"])
        self.assertEqual(rc, 0)
        packet = self._load_only_packet()
        self.assertEqual(packet["schema_version"], "handoffpacket.v2")
        self.assertEqual(packet["status"], "completed")
        self.assertEqual(packet["user_query"], "add guardrails to my llm app")
        self.assertIn("task_id", packet)
        self.assertIn("created_at", packet)
        self.assertIn("updated_at", packet)

    def test_packet_has_all_required_fields(self):
        coordination.main(["run", "add guardrails to my llm app"])
        packet = self._load_only_packet()
        for field in ("task_id", "created_at", "user_query", "status",
                       "resolved_rius", "steps", "outputs", "gaps",
                       "errors", "provenance"):
            self.assertIn(field, packet, f"Missing field: {field}")

    def test_packet_has_all_steps(self):
        coordination.main(["run", "add guardrails to my llm app"])
        packet = self._load_only_packet()
        for step_name in ("resolver", "traversal", "researcher", "final"):
            self.assertIn(step_name, packet["steps"])
            step = packet["steps"][step_name]
            self.assertIn("status", step)
            self.assertIn("attempt", step)


# ── Run → Show → Replay Flow ──────────────────────────────────────

class TestRunShowReplayFlow(CoordinationBase):

    def test_full_happy_path(self):
        rc = coordination.main(["run", "add guardrails to my llm app"])
        self.assertEqual(rc, 0)
        packet = self._load_only_packet()

        # All steps succeeded
        for step_name in ("resolver", "traversal", "researcher", "final"):
            self.assertEqual(packet["steps"][step_name]["status"], "success",
                             f"Step {step_name} not success")
            self.assertGreaterEqual(packet["steps"][step_name]["attempt"], 1)

        # Outputs present
        self.assertIn("resolver", packet["outputs"])
        self.assertIn("traversal", packet["outputs"])
        self.assertIn("researcher", packet["outputs"])
        self.assertIn("final", packet["outputs"])

        # Resolved RIUs present
        self.assertGreater(len(packet["resolved_rius"]), 0)
        self.assertIn("riu_id", packet["resolved_rius"][0])

    def test_show_returns_zero(self):
        coordination.main(["run", "add guardrails to my llm app"])
        packet = self._load_only_packet()
        rc = coordination.main(["show", packet["task_id"]])
        self.assertEqual(rc, 0)

    def test_list_returns_zero(self):
        coordination.main(["run", "add guardrails to my llm app"])
        rc = coordination.main(["list"])
        self.assertEqual(rc, 0)

    def test_show_nonexistent_returns_one(self):
        rc = coordination.main(["show", "nonexistent-task-id"])
        self.assertEqual(rc, 1)


# ── Traversal Output ──────────────────────────────────────────────

class TestTraversalOutput(CoordinationBase):

    def test_guardrails_resolves_to_valid_riu(self):
        coordination.main(["run", "add guardrails to my llm app"])
        packet = self._load_only_packet()
        trav = packet["outputs"]["traversal"]
        # keyword_resolve works against knowledge library, so the exact RIU
        # depends on which LIB entry scores highest. Verify we get a valid
        # traversal regardless.
        self.assertTrue(trav["riu_id"].startswith("RIU-"))
        self.assertIn(trav["classification"], ("both", "internal_only"))
        self.assertIsNotNone(trav.get("completeness"))

    def test_traversal_has_structured_output(self):
        coordination.main(["run", "add guardrails to my llm app"])
        packet = self._load_only_packet()
        trav = packet["outputs"]["traversal"]
        for field in ("riu_id", "riu_name", "classification",
                       "completeness", "recommendation", "gaps"):
            self.assertIn(field, trav, f"Missing traversal field: {field}")

    def test_traversal_full_result_present(self):
        """Full traversal result dict should be stored for debugging."""
        coordination.main(["run", "add guardrails to my llm app"])
        packet = self._load_only_packet()
        trav = packet["outputs"]["traversal"]
        self.assertIn("full_result", trav)
        self.assertIn("query_riu", trav["full_result"])


# ── Failure Injection & Replay ────────────────────────────────────

class TestFailureAndReplay(CoordinationBase):

    def test_resolver_failure_records_error(self):
        rc = coordination.main(["run", "add guardrails", "--fail-step", "resolver"])
        self.assertEqual(rc, 1)
        packet = self._load_only_packet()
        self.assertEqual(packet["status"], "failed")
        self.assertEqual(packet["steps"]["resolver"]["status"], "failed")
        self.assertIn("Injected failure", packet["steps"]["resolver"]["error"])

    def test_traversal_failure_preserves_resolver(self):
        rc = coordination.main(["run", "add guardrails", "--fail-step", "traversal"])
        self.assertEqual(rc, 1)
        packet = self._load_only_packet()
        self.assertEqual(packet["steps"]["resolver"]["status"], "success")
        self.assertEqual(packet["steps"]["traversal"]["status"], "failed")
        self.assertIn("resolver", packet["outputs"])
        self.assertNotIn("traversal", packet["outputs"])

    def test_researcher_failure_preserves_resolver_and_traversal(self):
        rc = coordination.main(["run", "add guardrails", "--fail-step", "researcher"])
        self.assertEqual(rc, 1)
        packet = self._load_only_packet()
        self.assertEqual(packet["steps"]["resolver"]["status"], "success")
        self.assertEqual(packet["steps"]["traversal"]["status"], "success")
        self.assertEqual(packet["steps"]["researcher"]["status"], "failed")
        self.assertIn("resolver", packet["outputs"])
        self.assertIn("traversal", packet["outputs"])
        self.assertNotIn("researcher", packet["outputs"])

    def test_replay_reruns_only_failed_and_downstream(self):
        coordination.main(["run", "add guardrails", "--fail-step", "traversal"])
        packet = self._load_only_packet()
        task_id = packet["task_id"]
        resolver_attempt = packet["steps"]["resolver"]["attempt"]
        resolver_output = json.dumps(packet["outputs"]["resolver"], sort_keys=True)

        # Replay without failure injection
        rc = coordination.main(["replay", task_id])
        self.assertEqual(rc, 0)
        packet = self._load_only_packet()

        # Resolver should NOT be re-executed
        self.assertEqual(packet["steps"]["resolver"]["attempt"], resolver_attempt,
                         "Resolver should not be re-executed on replay")
        self.assertEqual(json.dumps(packet["outputs"]["resolver"], sort_keys=True), resolver_output,
                         "Resolver output should be preserved on replay")

        # Traversal and downstream should be re-executed
        self.assertEqual(packet["steps"]["traversal"]["status"], "success")
        self.assertEqual(packet["steps"]["researcher"]["status"], "success")
        self.assertEqual(packet["steps"]["final"]["status"], "success")
        self.assertEqual(packet["status"], "completed")

    def test_replay_increments_attempt_counter(self):
        coordination.main(["run", "add guardrails", "--fail-step", "traversal"])
        packet = self._load_only_packet()
        task_id = packet["task_id"]
        trav_attempt_before = packet["steps"]["traversal"]["attempt"]

        coordination.main(["replay", task_id])
        packet = self._load_only_packet()
        self.assertGreater(packet["steps"]["traversal"]["attempt"], trav_attempt_before)

    def test_replay_completed_task_is_noop(self):
        coordination.main(["run", "add guardrails to my llm app"])
        packet = self._load_only_packet()
        task_id = packet["task_id"]

        rc = coordination.main(["replay", task_id])
        self.assertEqual(rc, 0)  # No-op, no error


# ── File Integrity ─────────────────────────────────────────────────

class TestFileIntegrity(CoordinationBase):

    def test_packet_remains_valid_json_after_failure(self):
        coordination.main(["run", "add guardrails", "--fail-step", "traversal"])
        for f in self._task_files():
            with open(f, encoding="utf-8") as fh:
                data = json.load(fh)  # Should not raise
            self.assertIn("task_id", data)

    def test_packet_remains_valid_after_replay(self):
        coordination.main(["run", "add guardrails", "--fail-step", "researcher"])
        packet = self._load_only_packet()
        task_id = packet["task_id"]

        # Verify file is valid JSON after failure
        with open(self._task_files()[0], encoding="utf-8") as f:
            json.load(f)

        coordination.main(["replay", task_id])

        # Verify file is valid JSON after replay
        with open(self._task_files()[0], encoding="utf-8") as f:
            packet2 = json.load(f)
        self.assertEqual(packet2["status"], "completed")

    def test_multiple_runs_create_separate_files(self):
        coordination.main(["run", "add guardrails"])
        coordination.main(["run", "observability for my app"])
        files = self._task_files()
        self.assertEqual(len(files), 2)
        ids = set()
        for f in files:
            with open(f, encoding="utf-8") as fh:
                p = json.load(fh)
            ids.add(p["task_id"])
        self.assertEqual(len(ids), 2, "Each run should have a unique task ID")


# ── Different Queries ──────────────────────────────────────────────

class TestDifferentQueries(CoordinationBase):

    def test_observability_query(self):
        rc = coordination.main(["run", "set up observability and monitoring"])
        self.assertEqual(rc, 0)
        packet = self._load_only_packet()
        self.assertEqual(packet["status"], "completed")
        # Should resolve to something observability-related
        trav = packet["outputs"]["traversal"]
        self.assertIsNotNone(trav.get("riu_id"))

    def test_empty_query_still_runs(self):
        """An odd query should still produce a packet, even if confidence is low."""
        rc = coordination.main(["run", "xyznonexistent"])
        # May succeed or fail depending on whether any RIU matches
        packet = self._load_only_packet()
        self.assertIn(packet["status"], ("completed", "failed"))
        self.assertIn("task_id", packet)


if __name__ == "__main__":
    unittest.main()
