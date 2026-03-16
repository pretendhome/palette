"""
Palette SDK — Machine Enablement Interface

The parallel to the human enablement coach: teaches any agent how to navigate,
query, verify against, and extend the Palette Intelligence System through
structured interfaces to the same underlying knowledge.

Usage:
    from palette.sdk import AgentBase, PaletteContext

    class MyAgent(AgentBase):
        def execute(self, packet):
            # Query the system
            result = self.query_pis("RIU-082")

            # Check what's connected
            quads = self.query_graph(subject="Architect", predicate="handles_riu")

            # Validate before emitting
            warnings = self.validate_output(my_result)

            return my_result
"""

from palette.sdk.agent_base import AgentBase, PaletteContext
from palette.sdk.integrity_gate import IntegrityGate
from palette.sdk.graph_query import GraphQuery

__all__ = ["AgentBase", "PaletteContext", "IntegrityGate", "GraphQuery"]
