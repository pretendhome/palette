package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
)

const version = "0.1.0"

// Config holds all runtime configuration for the Orchestrator.
type Config struct {
	// Agent discovery
	AgentsDir string // path to palette/agents/ — auto-detected from binary location

	// Target — passed through to invoked agents
	Remote      string
	Container   string
	AdapterURL  string
	TunnelPort  int
	BridgePort  int
	ServicePort int

	// Orch behaviour
	DryRun      bool   // build plan, never execute
	AutoConfirm bool   // skip maturity and ONE-WAY DOOR gates (use carefully)
	JSONOut     bool   // emit HandoffPackets as NDJSON on stderr
	TraceID     string // shared across all packets in this session
	Verbose     bool
}

func defaultConfig() Config {
	return Config{
		AgentsDir:   defaultAgentsDir(),
		Container:   "openclaw-fcup-openclaw-1",
		AdapterURL:  "http://localhost:8787",
		TunnelPort:  18889,
		BridgePort:  19000,
		ServicePort: 18789,
	}
}

// defaultAgentsDir resolves palette/agents/ relative to the orch binary.
// Falls back to PALETTE_AGENTS_DIR env var, then "../" as a last resort.
func defaultAgentsDir() string {
	if dir := os.Getenv("PALETTE_AGENTS_DIR"); dir != "" {
		return dir
	}
	exe, err := os.Executable()
	if err != nil {
		return ".."
	}
	// Binary at palette/agents/orchestrator/orch
	// filepath.Dir twice → palette/agents/
	return filepath.Dir(filepath.Dir(exe))
}

func buildFlags(cfg *Config) *flag.FlagSet {
	fs := flag.NewFlagSet("orch", flag.ContinueOnError)
	fs.StringVar(&cfg.AgentsDir, "agents-dir", cfg.AgentsDir,
		"Path to palette/agents/ directory (auto-detected from binary if unset)")
	fs.StringVar(&cfg.Remote, "remote", cfg.Remote,
		"SSH target forwarded to invoked agents (e.g. root@72.60.171.27)")
	fs.StringVar(&cfg.Container, "container", cfg.Container,
		"Docker container name forwarded to invoked agents")
	fs.StringVar(&cfg.AdapterURL, "adapter-url", cfg.AdapterURL,
		"Adapter base URL forwarded to invoked agents")
	fs.IntVar(&cfg.TunnelPort, "tunnel-port", cfg.TunnelPort,
		"SSH tunnel port forwarded to invoked agents")
	fs.IntVar(&cfg.BridgePort, "bridge-port", cfg.BridgePort,
		"socat bridge port forwarded to invoked agents")
	fs.BoolVar(&cfg.DryRun, "dry-run", cfg.DryRun,
		"Build plan and print HandoffPackets; do not execute")
	fs.BoolVar(&cfg.AutoConfirm, "auto", cfg.AutoConfirm,
		"Skip maturity and ONE-WAY DOOR confirmation gates")
	fs.BoolVar(&cfg.JSONOut, "json", cfg.JSONOut,
		"Emit HandoffPackets as NDJSON to stderr")
	fs.StringVar(&cfg.TraceID, "trace-id", cfg.TraceID,
		"Trace ID shared across all packets (auto-generated if empty)")
	fs.BoolVar(&cfg.Verbose, "verbose", cfg.Verbose,
		"Show passing metrics and full packet details")
	return fs
}

func usage() {
	fmt.Fprintf(os.Stderr, `
ORCH v%s — Palette Workflow Router (Orchestrator)
Reads task descriptions, routes them to specialist agents,
enforces maturity gates and ONE-WAY DOOR confirmation.

USAGE:
  orch <subcommand> [flags] "<task description>"

SUBCOMMANDS:
  status              Show roster: all agents, maturity, and invocation status
  route   "<task>"    Show routing decision — which agent handles this and why
  plan    "<task>"    Show full dispatch plan (dry-run; never executes)
  run     "<task>"    Execute the dispatch plan (with maturity gates)
  manifest            Show raw agent.json manifests for all agents

KEY FLAGS:
  --agents-dir PATH    Path to palette/agents/  (auto-detected from binary)
  --remote user@host   SSH target forwarded to invoked agents
  --container NAME     Container name forwarded to invoked agents
  --dry-run            Plan only; never invoke an agent
  --auto               Skip maturity + ONE-WAY DOOR confirmation gates
  --json               Emit HandoffPackets as NDJSON to stderr
  --trace-id ID        Shared trace ID for this session (auto-generated if empty)
  --verbose            Show full output from invoked agents

EXAMPLES:
  orch status
  orch route "debug openclaw connection"
  orch plan  "research WebSocket options then design the implementation"
  orch run   "debug openclaw" --remote root@72.60.171.27 --auto
  orch run   "check all metrics" --remote root@72.60.171.27

ENVIRONMENT:
  PALETTE_AGENTS_DIR   Override default agents directory

`, version)
}
