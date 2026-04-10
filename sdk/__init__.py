"""
Palette SDK — Machine Enablement Interface

Wire contract (V2.2): Packet → Agent → Result
  Packet: id, from, to, task, riu_ids, payload, trace_id
  Result: packet_id, from, status, output, blockers, artifacts, next_agent

Usage:
    from palette.sdk import AgentBase, HandoffPacket, HandoffResult, PaletteContext

    class MyAgent(AgentBase):
        def execute(self, packet):
            result = self.query_pis("RIU-082")
            return HandoffResult(
                packet_id=packet.id,
                from_=self.agent_name,
                output={"recommendation": "use Bedrock"},
            )
"""

from palette.sdk.agent_base import (
    AgentBase,
    HandoffPacket,
    HandoffResult,
    PaletteContext,
)
from palette.sdk.integrity_gate import IntegrityGate
from palette.sdk.graph_query import GraphQuery
from palette.sdk.prompt_cache import PromptBundle, PromptSection, build_prompt_bundle

__all__ = [
    "AgentBase",
    "HandoffPacket",
    "HandoffResult",
    "PaletteContext",
    "IntegrityGate",
    "GraphQuery",
    "PromptBundle",
    "PromptSection",
    "build_prompt_bundle",
]
