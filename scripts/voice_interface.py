#!/usr/bin/env python3
"""Unified Voice Interface for Multi-Agent Communication.

This script provides a single local interface for sending one message to multiple
configured agent endpoints. It can attempt MCP-style delivery, keep local
conversation history, and report whether a run was a dry run, a delivery attempt,
or a live-response success.

What this script can prove:
  - one input can be prepared for multiple agent endpoints
  - delivery attempts are made consistently
  - conversation history is persisted locally
  - unavailable endpoints fail gracefully

What this script cannot prove by itself:
  - that remote agents are live
  - that MCP interoperability is complete end-to-end
  - that a message was actually received unless a live endpoint responds
"""

import argparse
import asyncio
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import httpx
import yaml

# Configuration
CONFIG_DIR = Path.home() / ".palette" / "voice"
CONFIG_FILE = CONFIG_DIR / "agents.yaml"
CONVERSATION_HISTORY_FILE = CONFIG_DIR / "conversation_history.yaml"

# Peers Bus (the real communication infrastructure)
PEERS_BUS_URL = "http://127.0.0.1:7899"
VOICE_IDENTITY = "voice.interface"

DEFAULT_TIMEOUT = 30.0


class AgentConfig:
    """Configuration for a single agent endpoint.
    
    Attributes:
        name (str): Unique identifier for the agent
        endpoint (str): URL endpoint for MCP communication
        protocol (str): Communication protocol (default: 'mcp')
        priority (int): Processing priority (1 = highest)
        enabled (bool): Whether the agent is active
    """
    
    def __init__(self, name: str, endpoint: str, protocol: str = "mcp", 
                 priority: int = 1, enabled: bool = True):
        """Initialize agent configuration.
        
        Args:
            name: Unique agent identifier
            endpoint: URL endpoint for MCP communication
            protocol: Communication protocol (default: 'mcp')
            priority: Processing priority (1 = highest)
            enabled: Whether the agent is active
            
        Raises:
            ValueError: If name or endpoint is empty
        """
        if not name or not name.strip():
            raise ValueError("Agent name cannot be empty")
        if not endpoint or not endpoint.strip():
            raise ValueError("Agent endpoint cannot be empty")
            
        self.name = name.strip()
        self.endpoint = endpoint.strip()
        self.protocol = protocol
        self.priority = priority
        self.enabled = enabled
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "endpoint": self.endpoint,
            "protocol": self.protocol,
            "priority": self.priority,
            "enabled": self.enabled
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AgentConfig':
        return cls(
            name=data["name"],
            endpoint=data["endpoint"],
            protocol=data.get("protocol", "mcp"),
            priority=data.get("priority", 1),
            enabled=data.get("enabled", True)
        )


class VoiceInterface:
    """Main unified voice interface for multi-agent communication."""
    
    def __init__(self):
        self.agents: List[AgentConfig] = []
        self.conversation_history: List[Dict] = []
        self.session_id: str = str(uuid.uuid4())
        self._whisper_model = None
        self.metrics = {
            'total_messages': 0,
            'successful_broadcasts': 0,
            'failed_attempts': 0,
            'dry_runs': 0,
            'start_time': time.time()
        }
        self._setup_logging()
        self.load_configuration()
        self.load_conversation_history()
        self._load_metrics()
        # Preserve start_time from saved metrics if it exists
        if not self.metrics.get('_started'):
            self.metrics['start_time'] = time.time()
            self.metrics['_started'] = True
            self._save_metrics()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger('voice_interface')
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh = logging.FileHandler(CONFIG_DIR / 'voice_interface.log')
            fh.setFormatter(fmt)
            self.logger.addHandler(fh)
    
    def load_configuration(self):
        """Load agent configuration from YAML file with robust error handling."""
        if not CONFIG_FILE.exists():
            self.logger.info(f"Configuration file not found, creating default: {CONFIG_FILE}")
            self.create_default_configuration()
            return
        
        try:
            with open(CONFIG_FILE, 'r') as f:
                config_data = yaml.safe_load(f) or {}
                
            # Validate config structure
            if not isinstance(config_data, dict):
                raise ValueError("Configuration file must contain a dictionary")
                
            agents_data = config_data.get("agents", [])
            if not isinstance(agents_data, list):
                raise ValueError("Configuration 'agents' must be a list")
            
            self.agents = []
            for i, agent_data in enumerate(agents_data):
                try:
                    if not isinstance(agent_data, dict):
                        self.logger.warning(f"Skipping invalid agent at index {i}: not a dictionary")
                        continue
                    agent = AgentConfig.from_dict(agent_data)
                    self.agents.append(agent)
                except Exception as e:
                    self.logger.warning(f"Skipping invalid agent at index {i}: {e}")
                    continue
                    
        except yaml.YAMLError as e:
            self.logger.error(f"YAML parsing error in configuration file: {e}")
            self.agents = []
            print(f"❌ Configuration file error: {e}")
            print(f"   File: {CONFIG_FILE}")
            print("   The file may be corrupted. Consider backing it up and letting the system recreate it.")
        except Exception as e:
            self.logger.error(f"Unexpected error loading configuration: {e}")
            self.agents = []
            print(f"❌ Unexpected configuration error: {e}")
    
    def create_default_configuration(self):
        """Create a default agent configuration matching the real peers bus roster."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        default_agents = [
            AgentConfig(name="claude.analysis", endpoint=PEERS_BUS_URL, protocol="peers-bus", priority=1, enabled=True),
            AgentConfig(name="kiro.design", endpoint=PEERS_BUS_URL, protocol="peers-bus", priority=2, enabled=True),
            AgentConfig(name="codex.implementation", endpoint=PEERS_BUS_URL, protocol="peers-bus", priority=3, enabled=True),
            AgentConfig(name="gemini.specialist", endpoint=PEERS_BUS_URL, protocol="peers-bus", priority=4, enabled=False),
            AgentConfig(name="mistral-vibe.builder", endpoint=PEERS_BUS_URL, protocol="peers-bus", priority=5, enabled=False),
        ]
        
        config_data = {"agents": [agent.to_dict() for agent in default_agents]}
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(config_data, f)
        
        self.agents = default_agents
    
    def save_configuration(self):
        """Save current agent configuration to file."""
        try:
            config_data = {"agents": [agent.to_dict() for agent in self.agents]}
            with open(CONFIG_FILE, 'w') as f:
                yaml.dump(config_data, f)
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def load_conversation_history(self):
        """Load conversation history from file."""
        if CONVERSATION_HISTORY_FILE.exists():
            try:
                with open(CONVERSATION_HISTORY_FILE, 'r') as f:
                    self.conversation_history = yaml.safe_load(f) or []
            except Exception as e:
                print(f"Error loading conversation history: {e}")
                self.conversation_history = []
        else:
            self.conversation_history = []
    
    def save_conversation_history(self):
        """Save conversation history to file."""
        try:
            with open(CONVERSATION_HISTORY_FILE, 'w') as f:
                yaml.dump(self.conversation_history, f)
        except Exception as e:
            print(f"Error saving conversation history: {e}")
    
    def _load_metrics(self):
        """Load metrics from file."""
        metrics_file = CONFIG_DIR / "metrics.yaml"
        if metrics_file.exists():
            try:
                with open(metrics_file, 'r') as f:
                    loaded_metrics = yaml.safe_load(f) or {}
                    self.metrics.update(loaded_metrics)
            except Exception as e:
                self.logger.warning(f"Error loading metrics: {e}")
    
    def _save_metrics(self):
        """Save metrics to file."""
        try:
            metrics_file = CONFIG_DIR / "metrics.yaml"
            with open(metrics_file, 'w') as f:
                yaml.dump(self.metrics, f)
        except Exception as e:
            self.logger.warning(f"Error saving metrics: {e}")
    
    def add_to_conversation_history(self, role: str, content: str, agent: Optional[str] = None):
        """Add a message to the conversation history."""
        entry = {
            "timestamp": time.time(),
            "session_id": self.session_id,
            "role": role,
            "content": content
        }
        if agent:
            entry["agent"] = agent
        
        self.conversation_history.append(entry)
        # Keep history bounded
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
        
        self.save_conversation_history()
    
    async def broadcast_to_agents(self, message: str, history: List[Dict], dry_run: bool = False) -> Dict[str, str]:
        """Broadcast a message to all agents via the Palette peers bus.
        
        Uses the real peers bus at localhost:7899, not direct HTTP to agents.
        """
        responses = {}
        
        if dry_run:
            self.metrics['dry_runs'] += 1
            self._save_metrics()
            responses["peers-bus"] = f"[DRY RUN] Would broadcast to {PEERS_BUS_URL}/send with to_agent: 'all'"
            return responses
        
        self.metrics['total_messages'] += 1
        
        try:
            async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
                # Register once per session (idempotent on broker side)
                if not getattr(self, '_registered', False):
                    await client.post(f"{PEERS_BUS_URL}/register", json={
                        "identity": VOICE_IDENTITY,
                        "agent_name": "voice",
                        "runtime": "voice-interface",
                        "pid": os.getpid(),
                        "capabilities": ["broadcast", "voice"],
                        "trust_tier": "WORKING"
                    })
                    self._registered = True
                
                # Send via wire contract
                from datetime import datetime, timezone
                msg_id = str(uuid.uuid4())
                result = await client.post(f"{PEERS_BUS_URL}/send", json={
                    "protocol_version": "1.0.0",
                    "message_id": msg_id,
                    "thread_id": None,
                    "in_reply_to": None,
                    "from_agent": VOICE_IDENTITY,
                    "to_agent": "all",
                    "message_type": "informational",
                    "intent": message[:200],
                    "risk_level": "none",
                    "requires_ack": False,
                    "payload": {"content": message},
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "ttl_seconds": 3600
                })
                
                data = result.json()
                if data.get("ok"):
                    self.metrics['successful_broadcasts'] += 1
                    responses["peers-bus"] = f"Broadcast sent (message_id: {msg_id})"
                else:
                    self.metrics['failed_attempts'] += 1
                    responses["peers-bus"] = f"Error: {data.get('error', 'unknown')}"
                    
        except Exception as e:
            self.metrics['failed_attempts'] += 1
            responses["peers-bus"] = f"Error: Bus unreachable at {PEERS_BUS_URL} — {e}"
        
        self._save_metrics()
        return responses

    def _broadcast_stats(self, responses: Dict[str, str]) -> Dict[str, int]:
        """Summarize the outcome of a broadcast attempt."""
        total = len(responses)
        dry_run = sum(1 for r in responses.values() if "[DRY RUN]" in r)
        failed = sum(1 for r in responses.values() if r.startswith("Error:"))
        delivered = total - dry_run - failed
        return {
            "total": total,
            "dry_run": dry_run,
            "failed": failed,
            "delivered": delivered,
        }
    
    async def process_voice_input(self, audio_file: Path) -> Dict[str, str]:
        """Process voice input and broadcast to agents."""
        # Step 1: Transcribe audio (using existing palette_voice infrastructure)
        transcription = await self._transcribe_audio(audio_file)
        
        if not transcription:
            return {"error": "No speech detected"}
        
        print(f"Transcribed: {transcription}")
        
        # Step 2: Add to conversation history
        self.add_to_conversation_history("user", transcription)
        
        # Step 3: Broadcast to all agents
        history_for_agents = self._prepare_history_for_agents()
        responses = await self.broadcast_to_agents(transcription, history_for_agents)
        
        # Step 4: Add agent responses to history
        for agent_name, agent_response in responses.items():
            self.add_to_conversation_history("agent", agent_response, agent_name)
        
        return responses
    
    async def _transcribe_audio(self, audio_file: Path) -> str:
        """Transcribe audio using Whisper (from palette_voice)."""
        try:
            import whisper
            if self._whisper_model is None:
                self._whisper_model = whisper.load_model("base")
            result = self._whisper_model.transcribe(str(audio_file), fp16=False)
            return result["text"].strip()
        except ImportError:
            print("Whisper not installed. Install with: pip install openai-whisper")
            return ""
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
    
    def _prepare_history_for_agents(self) -> List[Dict]:
        """Prepare conversation history in MCP format."""
        mcp_history = []
        for entry in self.conversation_history:
            mcp_entry = {
                "role": entry["role"],
                "content": entry["content"],
                "timestamp": entry["timestamp"]
            }
            if "agent" in entry:
                mcp_entry["agent"] = entry["agent"]
            mcp_history.append(mcp_entry)
        
        return mcp_history
    
    def list_agents(self, detailed: bool = False) -> List[Dict]:
        """List all configured agents with their status."""
        if detailed:
            return [{
                "name": agent.name,
                "endpoint": agent.endpoint,
                "protocol": agent.protocol,
                "priority": agent.priority,
                "enabled": agent.enabled
            } for agent in self.agents]
        else:
            return [{
                "name": agent.name,
                "enabled": agent.enabled,
                "priority": agent.priority
            } for agent in self.agents]
    
    def get_enabled_agents_count(self) -> int:
        """Get count of enabled agents."""
        return sum(1 for agent in self.agents if agent.enabled)
    
    def enable_agent(self, agent_name: str, enabled: bool) -> bool:
        """Enable or disable an agent by name."""
        for agent in self.agents:
            if agent.name == agent_name:
                agent.enabled = enabled
                self.save_configuration()
                return True
        return False
    
    def add_agent(self, name: str, endpoint: str = None, protocol: str = "peers-bus", 
                  priority: int = 1, enabled: bool = True) -> Tuple[bool, str]:
        """Add a new agent to the configuration."""
        if endpoint is None:
            endpoint = PEERS_BUS_URL
        
        if not self._validate_url(endpoint):
            return False, f"Invalid URL: {endpoint}"
        
        for agent in self.agents:
            if agent.name == name:
                return False, f"Agent already exists: {name}"
        
        new_agent = AgentConfig(name, endpoint, protocol, priority, enabled)
        self.agents.append(new_agent)
        self.save_configuration()
        return True, "Agent added successfully"
    
    def _validate_url(self, url: str) -> bool:
        """Validate that a string is a proper URL."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
    
    def remove_agent(self, agent_name: str) -> bool:
        """Remove an agent from the configuration."""
        original_count = len(self.agents)
        self.agents = [agent for agent in self.agents if agent.name != agent_name]
        
        if len(self.agents) < original_count:
            self.save_configuration()
            return True
        return False
    
    def _print_responses(self, responses: Dict[str, str]):
        """Print agent responses in a formatted way."""
        if not responses:
            print("No agent results recorded.")
            return

        stats = self._broadcast_stats(responses)

        if stats["dry_run"] == stats["total"]:
            print(f"\nℹ️  Dry run only: {stats['total']} agent targets identified.")
            print("No messages were sent.")
            for agent_name, response in responses.items():
                print(f"  • {agent_name}: {response}")
            return

        if stats["delivered"] == 0 and stats["failed"] > 0:
            print(f"\n⚠️  Broadcast attempted to {stats['total']} agent(s), but no live responses were received.")
            print("This demonstrates broadcast attempt handling, not successful delivery.")
            for agent_name, response in responses.items():
                print(f"  • {agent_name}: {response}")
            print("\nNote: This is expected when configured agent endpoints are offline or unreachable.")
        else:
            print(
                f"\nBroadcast summary: {stats['delivered']} live response(s), "
                f"{stats['failed']} failed delivery attempt(s), {stats['dry_run']} dry-run target(s)."
            )
            print("Only agents with live responses are confirmed to have received and processed the message.")
            for agent_name, response in responses.items():
                print(f"\n{agent_name}:")
                print(f"  {response}")


def main():
    parser = argparse.ArgumentParser(
        description="Unified Voice Interface for Multi-Agent Communication (MCP v1.0)",
        epilog="""
        Examples:
          # List all configured agents
          python3 voice_interface.py --list-agents
          
          # Show detailed agent configuration
          python3 voice_interface.py --detailed-agents
          
          # Test message without sending (dry run)
          python3 voice_interface.py --text-input "test message" --dry-run
          
          # Send message to all enabled agents
          python3 voice_interface.py --text-input "your message here"
          
          # Show system summary and statistics
          python3 voice_interface.py --summary
          
          # Add a new agent endpoint
          python3 voice_interface.py --add-agent agent-name http://endpoint:port/mcp
          
          # Interactive mode
          python3 voice_interface.py
        """
    )
    parser.add_argument("--list-agents", action="store_true", help="List all configured agents")
    parser.add_argument("--enable-agent", help="Enable a specific agent")
    parser.add_argument("--disable-agent", help="Disable a specific agent")
    parser.add_argument("--add-agent", nargs='+', metavar="NAME", 
                       help="Add a new agent (name, optional endpoint — defaults to peers bus)")
    parser.add_argument("--remove-agent", help="Remove an agent")
    parser.add_argument("--detailed-agents", action="store_true", help="Show detailed agent configuration")
    parser.add_argument("--dry-run", action="store_true", help="Test without actually sending to agents")
    parser.add_argument("--summary", action="store_true", help="Show system summary and statistics")
    parser.add_argument("--reset-metrics", action="store_true", help="Reset all metrics to zero")
    parser.add_argument("--audio-file", help="Process a specific audio file")
    parser.add_argument("--text-input", help="Process text input directly")
    
    args = parser.parse_args()
    
    interface = VoiceInterface()
    
    # Handle configuration commands
    if args.list_agents:
        agents = interface.list_agents(detailed=False)
        print("Configured Agents:")
        for agent in agents:
            status = "✓" if agent["enabled"] else "✗"
            print(f"  {status} {agent['name']} (priority: {agent['priority']})")
        return
    
    if args.enable_agent:
        if interface.enable_agent(args.enable_agent, True):
            print(f"Enabled agent: {args.enable_agent}")
        else:
            print(f"Agent not found: {args.enable_agent}")
        return
    
    if args.disable_agent:
        if interface.enable_agent(args.disable_agent, False):
            print(f"Disabled agent: {args.disable_agent}")
        else:
            print(f"Agent not found: {args.disable_agent}")
        return
    
    if args.add_agent:
        name = args.add_agent[0]
        endpoint = args.add_agent[1] if len(args.add_agent) > 1 else None
        success, message = interface.add_agent(name, endpoint)
        if success:
            print(f"✅ Added agent: {name} -> {endpoint or PEERS_BUS_URL}")
        else:
            print(f"❌ {message}")
        return
    
    if args.remove_agent:
        if interface.remove_agent(args.remove_agent):
            print(f"Removed agent: {args.remove_agent}")
        else:
            print(f"Agent not found: {args.remove_agent}")
        return
    
    # Handle configuration display
    if args.detailed_agents:
        agents = interface.list_agents(detailed=True)
        print("Detailed Agent Configuration:")
        for agent in agents:
            status = "✓ ENABLED" if agent["enabled"] else "✗ DISABLED"
            print(f"\n{agent['name']}:")
            print(f"  Status: {status}")
            print(f"  Endpoint: {agent['endpoint']}")
            print(f"  Protocol: {agent['protocol']}")
            print(f"  Priority: {agent['priority']}")
        return
    
    if args.summary:
        enabled_count = interface.get_enabled_agents_count()
        total_count = len(interface.agents)
        history_count = len(interface.conversation_history)
        uptime = time.time() - interface.metrics['start_time']
        
        # Check bus health
        bus_status = "❌ OFFLINE"
        bus_peers = 0
        try:
            import httpx as _hx
            r = _hx.get(f"{PEERS_BUS_URL}/health", timeout=2)
            data = r.json()
            if data.get("status") == "ok":
                bus_peers = data.get("peers", 0)
                bus_status = f"✅ ONLINE ({bus_peers} peers)"
        except Exception:
            pass
        
        print("📊 Voice Interface System Summary")
        print("=" * 50)
        print(f"🚌 Peers Bus: {bus_status}")
        print(f"🤖 Agents: {enabled_count}/{total_count} enabled")
        print(f"💬 Conversation History: {history_count} messages")
        print(f"📊 Metrics: {interface.metrics['total_messages']} total messages")
        print(f"✅ Success: {interface.metrics['successful_broadcasts']} broadcasts")
        print(f"❌ Failed: {interface.metrics['failed_attempts']} attempts")
        print(f"🔍 Dry Runs: {interface.metrics['dry_runs']} tests")
        print(f"⏱️  Uptime: {int(uptime//3600)}h {int((uptime%3600)//60)}m {int(uptime%60)}s")
        print(f"📁 Configuration: {CONFIG_FILE}")
        print(f"💾 History File: {CONVERSATION_HISTORY_FILE}")
        
        if history_count > 0:
            last_message = interface.conversation_history[-1]
            last_time = time.ctime(last_message["timestamp"])
            print(f"🕒 Last Activity: {last_time}")
        
        print("\n🔧 Quick Actions:")
        print("  • List agents: --list-agents")
        print("  • Detailed config: --detailed-agents")
        print("  • Test message: --text-input 'your message' --dry-run")
        print("  • Send message: --text-input 'your message'")
        print("  • Reset metrics: --reset-metrics")
        return
    
    if args.reset_metrics:
        interface.metrics = {
            'total_messages': 0, 'successful_broadcasts': 0,
            'failed_attempts': 0, 'dry_runs': 0,
            'start_time': time.time(), '_started': True
        }
        interface._save_metrics()
        print("✅ Metrics reset.")
        return
    
    # Handle input processing
    if args.audio_file:
        audio_path = Path(args.audio_file)
        if not audio_path.exists():
            print(f"Error: Audio file not found: {args.audio_file}")
            return
        
        print(f"Processing audio file: {args.audio_file}")
        responses = asyncio.run(interface.process_voice_input(audio_path))
        interface._print_responses(responses)
        return
    
    if args.text_input is not None:
        if not args.text_input.strip():
            print("Error: Empty text input. Provide non-empty text or use interactive mode.")
            return

        print(f"Processing text input: {args.text_input}")
        
        interface.add_to_conversation_history("user", args.text_input)
        history = interface._prepare_history_for_agents()
        responses = asyncio.run(interface.broadcast_to_agents(args.text_input, history, args.dry_run))
        
        # Record agent responses in history (matches process_voice_input behavior)
        if not args.dry_run:
            for agent_name, agent_response in responses.items():
                interface.add_to_conversation_history("agent", agent_response, agent_name)
        
        interface._print_responses(responses)
        return
    
    # Interactive mode
    print("Unified Voice Interface - Interactive Mode")
    print("Type 'quit' to exit, or enter text to send to all agents")
    print(f"Configured agents: {[agent.name for agent in interface.agents if agent.enabled]}")
    
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() in ('quit', 'exit', 'q'):
                break
            
            if not user_input.strip():
                continue
                
            print(f"Preparing broadcast: {user_input}")
            
            # Add to history
            interface.add_to_conversation_history("user", user_input)
            
            # Broadcast to agents
            history = interface._prepare_history_for_agents()
            responses = asyncio.run(interface.broadcast_to_agents(user_input, history))
            
            for agent_name, agent_response in responses.items():
                interface.add_to_conversation_history("agent", agent_response, agent_name)
            
            interface._print_responses(responses)
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
