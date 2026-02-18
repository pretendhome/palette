// raptor — Palette Debug Agent (Velociraptor v2.1)
//
// Auto-recursive connectivity diagnosis and repair for containerized AI services.
// Implements the Palette velociraptor archetype: isolate → diagnose → fix → verify.

package main

import (
	"fmt"
	"os"
	"time"
)

const version = "2.1.0"

func usage() {
	fmt.Fprintf(os.Stderr, `
RAPTOR v%s — Palette Debug Agent (Velociraptor)
Auto-recursive connectivity diagnosis for containerized AI services.

USAGE:
  raptor <subcommand> [flags]

SUBCOMMANDS:
  diagnose   Non-destructive probe of all connectivity layers
  fix        Diagnose + apply nsenter+socat bridge
  tunnel     Kill old SSH tunnel, start correct one
  persist    Install systemd unit (bridge survives reboots)
  verify     End-to-end route test
  runbook    Print manual VPS commands
  report     Print Palette decisions.md log entry

KEY FLAGS:
  --remote user@host   SSH target for remote execution  (e.g. root@72.60.171.27)
  --container NAME     Docker container name             (default: openclaw-fcup-openclaw-1)
  --service-port PORT  Port service binds inside container (default: 18789)
  --bridge-port PORT   Port socat exposes on bridge net  (default: 19000)
  --tunnel-port PORT   Local SSH tunnel port             (default: 18889)
  --adapter-url URL    Local adapter base URL            (default: http://localhost:8787)
  --upstream-url URL   Upstream base URL  (reads OPENCLAW_BASE_URL if unset)
  --token TOKEN        Upstream API token (reads OPENCLAW_API_KEY if unset)
  --api-path PATH      API endpoint to probe             (default: /v1/chat/completions)
  --api-model MODEL    Model name for probe payload      (default: openclaw:main)
  --dry-run            Print commands without executing
  --verbose            Show SSH commands as they run

EXAMPLES:
  raptor fix --remote root@72.60.171.27   # full automated fix
  raptor diagnose --remote root@72.60.171.27
  raptor tunnel --remote root@72.60.171.27 --bridge-ip 172.18.0.2
  raptor persist --remote root@72.60.171.27
  raptor verify
  raptor runbook --remote root@72.60.171.27

`, version)
}

func main() {
	if len(os.Args) < 2 || os.Args[1] == "-h" || os.Args[1] == "--help" || os.Args[1] == "help" {
		usage()
		os.Exit(0)
	}

	sub := os.Args[1]
	cfg := defaultConfig()
	fs := buildFlags(&cfg)
	bridgeIP := fs.String("bridge-ip", "", "container bridge IP (used by tunnel subcommand)")
	_ = fs.Parse(os.Args[2:])

	run := newRunner(cfg)

	fmt.Printf("\nRAPTOR v%s — Palette Debug Agent (Velociraptor)\n", version)
	fmt.Printf("Target: %s\n\n", run.Target())

	switch sub {

	case "diagnose", "diag", "d":
		d := diagnose(run, cfg)
		printDiagnosis(d)

	case "fix", "f":
		if cfg.DryRun {
			printRunbook(cfg)
			return
		}
		fmt.Println("Running probe chain...")
		d := diagnose(run, cfg)
		printDiagnosis(d)

		if !d.FixReady || d.FixMode != "bridge" {
			fmt.Printf("⚠️  No auto-fix for mode '%s'. See diagnosis above.\n\n", d.FixMode)
			os.Exit(1)
		}

		fmt.Printf("🔧 Applying bridge fix (container=%s, %d→%d)...\n\n",
			cfg.Container, cfg.BridgePort, cfg.ServicePort)
		fr := applyBridgeFix(run, cfg)
		printFixResult(fr, cfg)
		if !fr.Applied {
			os.Exit(1)
		}

		// After a remote fix, automatically start the local tunnel.
		if run.IsRemote() {
			fmt.Println("🔌 Starting local SSH tunnel...")
			tr := manageTunnel(cfg, fr.BridgeIP)
			printTunnelResult(tr)
			if tr.Active {
				fmt.Println("Running verify...")
				r := probeAdapterRoute(run, cfg)
				fmt.Printf("  [%s] %s\n\n", icon(r.Status), r.Detail)
			}
		}

	case "tunnel", "t":
		ip := *bridgeIP
		if ip == "" && cfg.Remote != "" {
			fmt.Printf("Detecting bridge IP from %s...\n", cfg.Remote)
			var err error
			ip, err = run.DockerInspect(cfg.Container,
				"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}")
			if err != nil || ip == "" {
				fmt.Printf("✗ Cannot get bridge IP: %v\n", err)
				fmt.Println("  Provide it with: raptor tunnel --bridge-ip 172.18.0.2")
				os.Exit(1)
			}
			fmt.Printf("  Bridge IP: %s\n\n", ip)
		}
		if ip == "" {
			fmt.Println("✗ Need --bridge-ip or --remote to detect it.")
			os.Exit(1)
		}
		tr := manageTunnel(cfg, ip)
		printTunnelResult(tr)
		if !tr.Active {
			os.Exit(1)
		}

	case "persist", "p":
		if cfg.DryRun {
			fmt.Println(systemdUnit(cfg))
			return
		}
		fmt.Printf("📌 Installing systemd bridge unit on %s...\n\n", run.Target())
		if err := applyPersistence(run, cfg); err != nil {
			fmt.Printf("✗ %v\n\n", err)
			os.Exit(1)
		}
		fmt.Printf("\n✓ Bridge will restart automatically after container or host restarts.\n\n")

	case "verify", "v":
		fmt.Println("End-to-end verification...")
		r := probeAdapterRoute(run, cfg)
		fmt.Printf("\n  [%s] %s\n\n", icon(r.Status), r.Detail)
		if r.Status != ProbePass {
			os.Exit(1)
		}

	case "runbook", "rb":
		printRunbook(cfg)

	case "report", "r":
		d := diagnose(run, cfg)
		ts := time.Now().Format(time.RFC3339)
		fmt.Printf("---\n### Agent Execution: Velociraptor\n\n")
		fmt.Printf("**Timestamp**: %s\n", ts)
		fmt.Printf("**Agent**: raptor v%s\n", version)
		fmt.Printf("**Target**: %s\n", run.Target())
		fmt.Printf("**Container**: %s / port %d\n\n", cfg.Container, cfg.ServicePort)
		fmt.Printf("**Root Cause**: %s\n", d.RootCause)
		fmt.Printf("**Fix Mode**: %s  |  Fix Ready: %v\n\n", d.FixMode, d.FixReady)
		fmt.Printf("**Probe Chain**:\n")
		for i, r := range d.Results {
			marker := ""
			if r.RootCause {
				marker = " ← ROOT CAUSE"
			}
			fmt.Printf("  %d. [%s] %s: %s%s\n", i+1, icon(r.Status), r.Name, r.Detail, marker)
		}
		fmt.Println()

	default:
		fmt.Fprintf(os.Stderr, "unknown subcommand: %s\n", sub)
		usage()
		os.Exit(1)
	}
}

