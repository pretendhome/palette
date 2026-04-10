"""Tests for palette.sdk.prompt_cache."""

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

from palette.sdk.agent_base import AgentBase, HandoffPacket, PaletteContext
from palette.sdk.prompt_cache import PromptSection, build_prompt_bundle


class TestPromptCache(unittest.TestCase):
    def test_stable_hash_ignores_volatile_changes(self):
        stable = [PromptSection("System Prompt", "You are a careful agent.")]
        bundle_a = build_prompt_bundle(
            stable,
            [PromptSection("Task", "Task A", cacheable=False)],
        )
        bundle_b = build_prompt_bundle(
            stable,
            [PromptSection("Task", "Task B", cacheable=False)],
        )
        self.assertEqual(bundle_a.stable_hash, bundle_b.stable_hash)
        self.assertNotEqual(bundle_a.full_hash, bundle_b.full_hash)

    def test_empty_sections_are_removed(self):
        bundle = build_prompt_bundle(
            [PromptSection("System Prompt", "  ")],
            [PromptSection("Task", "Ship it", cacheable=False)],
        )
        self.assertEqual(bundle.stable_sections, ())
        self.assertIn("Task", bundle.volatile_suffix)

    def test_agent_base_builds_cache_friendly_bundle(self):
        agent = AgentBase(context=PaletteContext())
        packet = HandoffPacket(
            task="Evaluate guardrails",
            riu_ids=["RIU-082"],
            payload={"service": "bedrock"},
            trace_id="trace-123",
        )
        bundle = agent.build_prompt_bundle(
            packet,
            system_prompt="You are a read-only research agent.",
        )
        self.assertIn("Agent", bundle.stable_prefix)
        self.assertIn("System Prompt", bundle.stable_prefix)
        self.assertIn("Task", bundle.volatile_suffix)
        self.assertIn("RIU IDs", bundle.volatile_suffix)
        self.assertIn("Payload", bundle.volatile_suffix)
        self.assertIn("Trace ID", bundle.volatile_suffix)

