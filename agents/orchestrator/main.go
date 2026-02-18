// orch — Palette Workflow Router (Orchestrator)
//
// Orch is the connective tissue of the Palette multi-agent system.
// It reads a task description, routes it to the right specialist agent(s),
// enforces maturity gates and ONE-WAY DOOR confirmation, dispatches
// HandoffPackets, and aggregates HandoffResults.
//
// Architecture mirrors Raptor and Para:
//
//	AgentRunner interface   →  SubprocessRunner (real) | DryRunner (plan-only)
//	routeRules []rule       →  data-driven routing table, add a route = one line
//	buildPlan()             →  converts Tasks + decisions into DispatchPlan
//	executePlan()           →  runs plan with gates, collects InvokeResults
//
// The Orchestrator never does domain work. It routes. That is all.

package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 ||
		os.Args[1] == "-h" || os.Args[1] == "--help" || os.Args[1] == "help" {
		usage()
		os.Exit(0)
	}

	sub := os.Args[1]
	cfg := defaultConfig()
	fs := buildFlags(&cfg)
	_ = fs.Parse(os.Args[2:])

	if cfg.TraceID == "" {
		cfg.TraceID = newID()
	}

	fmt.Printf("\nORCH v%s — Palette Workflow Router\n", version)

	// Load roster for all subcommands
	roster, errs := loadRoster(cfg.AgentsDir)
	if len(errs) > 0 && cfg.Verbose {
		for _, err := range errs {
			fmt.Fprintf(os.Stderr, "  roster warning: %v\n", err)
		}
	}
	if len(roster) == 0 {
		fmt.Fprintf(os.Stderr,
			"✗ no agents found in %q\n   Set --agents-dir or PALETTE_AGENTS_DIR\n\n",
			cfg.AgentsDir)
		os.Exit(1)
	}

	switch sub {

	// ── status ────────────────────────────────────────────────────────────────
	// Show every agent in the roster with maturity and invocation status.
	case "status", "s":
		printStatus(roster, cfg.AgentsDir)

	// ── manifest ──────────────────────────────────────────────────────────────
	// Dump raw JSON for every loaded agent manifest.
	case "manifest", "m":
		printManifest(roster)

	// ── route ─────────────────────────────────────────────────────────────────
	// Show routing decision only — which agent(s) would handle this task and why.
	// Does not build a plan, does not execute anything.
	case "route", "r":
		input := taskInput(fs.Args())
		tasks := parseInput(input, cfg.TraceID)
		decisions := make([]RouteDecision, len(tasks))
		for i, task := range tasks {
			decisions[i] = route(task, roster)
		}
		printRouteDecision(tasks, decisions, roster)

	// ── plan ──────────────────────────────────────────────────────────────────
	// Route + build full DispatchPlan + show it. Never executes.
	// Equivalent to `orch run --dry-run` but cleaner output focused on the plan.
	case "plan", "p":
		input := taskInput(fs.Args())
		tasks := parseInput(input, cfg.TraceID)
		decisions := make([]RouteDecision, len(tasks))
		for i, task := range tasks {
			decisions[i] = route(task, roster)
		}
		plan := buildPlan(tasks, decisions, cfg)
		printRouteDecision(tasks, decisions, roster)
		printPlan(plan, roster, cfg)

	// ── run ───────────────────────────────────────────────────────────────────
	// Route + build plan + execute. This is the full orchestration path.
	// Maturity gates and ONE-WAY DOOR gates are enforced unless --auto is set.
	// Use --dry-run to see what would happen without invoking any agents.
	case "run", "dispatch", "d":
		input := taskInput(fs.Args())
		tasks := parseInput(input, cfg.TraceID)
		decisions := make([]RouteDecision, len(tasks))
		for i, task := range tasks {
			decisions[i] = route(task, roster)
		}
		plan := buildPlan(tasks, decisions, cfg)

		// Always show the plan first so the operator knows what's coming
		printRouteDecision(tasks, decisions, roster)
		printPlan(plan, roster, cfg)

		if len(plan.Steps) == 0 {
			fmt.Println("✗ No dispatchable agents matched this task.")
			fmt.Println("  Try: orch route \"<task>\" to see the routing decision.")
			os.Exit(1)
		}

		var runner AgentRunner
		if cfg.DryRun {
			runner = DryRunner{verbose: cfg.Verbose}
		} else {
			runner = SubprocessRunner{cfg: cfg}
		}

		result := executePlan(plan, roster, runner, cfg)
		printDispatchResult(result, roster)

		if result.Blocked || result.OWDPause {
			os.Exit(1)
		}

	default:
		fmt.Fprintf(os.Stderr, "unknown subcommand: %s\n\n", sub)
		usage()
		os.Exit(1)
	}
}

// taskInput extracts the task description from remaining args after flag parsing.
// Joins multiple args with a space so quoting is optional.
func taskInput(args []string) string {
	if len(args) == 0 {
		fmt.Fprintln(os.Stderr, "✗ task description required\n  Usage: orch <subcommand> \"<task>\"\n")
		os.Exit(1)
	}
	result := ""
	for i, a := range args {
		if i > 0 {
			result += " "
		}
		result += a
	}
	return result
}
