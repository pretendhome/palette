package main

import (
	"flag"
	"fmt"
	"os"
	"time"
)

const version = "1.0.0"

type Config struct {
	// Target
	Remote    string
	Container string

	// Endpoints
	AdapterURL  string
	HealthPath  string
	RoutePath   string
	TunnelPort  int
	BridgePort  int
	ServicePort int

	// Thresholds
	LatencyWarn time.Duration
	LatencyCrit time.Duration

	// Watch mode
	Interval time.Duration

	// Output
	JSONOut bool   // emit HandoffPackets as NDJSON to stderr on alert
	TraceID string // shared across all packets in this monitoring session

	// Behaviour
	Verbose bool
}

func defaultConfig() Config {
	return Config{
		Container:   "openclaw-fcup-openclaw-1",
		AdapterURL:  "http://localhost:8787",
		HealthPath:  "/health",
		RoutePath:   "/v1/chat/completions",
		TunnelPort:  18889,
		BridgePort:  19000,
		ServicePort: 18789,
		LatencyWarn: 3 * time.Second,
		LatencyCrit: 8 * time.Second,
		Interval:    30 * time.Second,
	}
}

func buildFlags(cfg *Config) *flag.FlagSet {
	fs := flag.NewFlagSet("para", flag.ContinueOnError)
	fs.StringVar(&cfg.Remote, "remote", cfg.Remote,
		"SSH target for remote docker checks (e.g. root@72.60.171.27)")
	fs.StringVar(&cfg.Container, "container", cfg.Container,
		"Docker container name to monitor")
	fs.StringVar(&cfg.AdapterURL, "adapter-url", cfg.AdapterURL,
		"Local adapter base URL")
	fs.StringVar(&cfg.HealthPath, "health-path", cfg.HealthPath,
		"Adapter health endpoint path")
	fs.IntVar(&cfg.TunnelPort, "tunnel-port", cfg.TunnelPort,
		"SSH tunnel local port")
	fs.IntVar(&cfg.BridgePort, "bridge-port", cfg.BridgePort,
		"socat bridge port on container bridge network")
	fs.IntVar(&cfg.ServicePort, "service-port", cfg.ServicePort,
		"Service port inside container")
	fs.DurationVar(&cfg.LatencyWarn, "latency-warn", cfg.LatencyWarn,
		"Adapter latency warning threshold")
	fs.DurationVar(&cfg.LatencyCrit, "latency-crit", cfg.LatencyCrit,
		"Adapter latency critical threshold")
	fs.DurationVar(&cfg.Interval, "interval", cfg.Interval,
		"Monitoring interval for watch mode")
	fs.BoolVar(&cfg.JSONOut, "json", cfg.JSONOut,
		"Emit HandoffPackets as NDJSON to stderr on any alert")
	fs.StringVar(&cfg.TraceID, "trace-id", cfg.TraceID,
		"Trace ID shared across all packets in this session (auto-generated if empty)")
	fs.BoolVar(&cfg.Verbose, "verbose", cfg.Verbose,
		"Show passing metrics in addition to alerts")
	return fs
}

func usage() {
	fmt.Fprintf(os.Stderr, `
PARA v%s — Palette Signal Monitor (Parasaurolophus)
Continuous metric monitoring for containerized AI services.
Emits signals only — never diagnoses, never fixes.

USAGE:
  para <subcommand> [flags]

SUBCOMMANDS:
  watch    Continuous loop; runs all metrics every --interval (default: 30s)
  check    Single-pass check; exits 0=all normal, 1=any alert
  list     Print all configured metrics and their baselines
  report   Single-pass check; emit alerts as JSON HandoffPackets

KEY FLAGS:
  --remote user@host     SSH target for remote docker checks
  --container NAME       Docker container name (default: openclaw-fcup-openclaw-1)
  --adapter-url URL      Local adapter base URL (default: http://localhost:8787)
  --tunnel-port PORT     SSH tunnel local port  (default: 18889)
  --bridge-port PORT     socat bridge port      (default: 19000)
  --interval DURATION    Watch cycle interval   (default: 30s)
  --latency-warn DUR     Latency warning level  (default: 3s)
  --latency-crit DUR     Latency critical level (default: 8s)
  --json                 Emit HandoffPackets as NDJSON to stderr on alert
  --verbose              Show passing metrics too

EXAMPLES:
  para watch --remote root@72.60.171.27 --json
  para check --remote root@72.60.171.27
  para check --verbose
  para list
  para report --json

`, version)
}
