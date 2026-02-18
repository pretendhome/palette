package main

import (
	"encoding/json"
	"fmt"
	"sort"
	"strings"

	core "github.com/pretendhome/palette/core"
)

const divider = "  ─────────────────────────────────────────────────────────────────"

// ── Roster / status ───────────────────────────────────────────────────────────

func printStatus(roster Roster, agentsDir string) {
	fmt.Println()
	fmt.Println("ORCH — Palette Agent Roster")
	fmt.Println(divider)
	fmt.Printf("  %-20s  %-18s  %-10s  %s\n", "AGENT", "ROLE", "RUNTIME", "STATUS")
	fmt.Println(divider)

	// Sort alphabetically
	names := make([]string, 0, len(roster))
	for id := range roster {
		names = append(names, string(id))
	}
	sort.Strings(names)

	for _, name := range names {
		m := roster[core.AgentID(name)]
		self := ""
		if name == "orchestrator" {
			self = "  ← you are here"
		}
		dispatchable := ""
		if !isDispatchable(m) {
			dispatchable = "  [not dispatchable]"
		}
		fmt.Printf("  %-20s  %-18s  %-10s  %s%s%s\n",
			name, m.Role, m.Runtime, maturityBadge(m), self, dispatchable)
	}

	fmt.Println(divider)
	dispatchable := 0
	for _, m := range roster {
		if isDispatchable(m) {
			dispatchable++
		}
	}
	fmt.Printf("  Dispatchable: %d / %d agents  |  agents-dir: %s\n\n",
		dispatchable, len(roster), agentsDir)
}

func printManifest(roster Roster) {
	names := make([]string, 0, len(roster))
	for id := range roster {
		names = append(names, string(id))
	}
	sort.Strings(names)

	for _, name := range names {
		m := roster[core.AgentID(name)]
		b, _ := json.MarshalIndent(m, "  ", "  ")
		fmt.Printf("\n── %s ──\n  %s\n", name, string(b))
	}
	fmt.Println()
}

// ── Routing decision ──────────────────────────────────────────────────────────

func printRouteDecision(tasks []Task, decisions []RouteDecision, roster Roster) {
	fmt.Println()
	fmt.Println("ORCH — Routing Decision")
	fmt.Println(divider)

	if len(tasks) > 1 {
		fmt.Printf("  Multi-step task (%d steps detected)\n\n", len(tasks))
	}

	for i, task := range tasks {
		if i >= len(decisions) {
			break
		}
		d := decisions[i]
		stepLabel := ""
		if len(tasks) > 1 {
			stepLabel = fmt.Sprintf("Step %d: ", i+1)
		}
		fmt.Printf("  %sTask: %q\n", stepLabel, task.Description)

		if len(d.Agents) == 0 {
			fmt.Printf("  Route:  ✗ no agent found (confidence: %d%%)\n", d.Confidence)
			fmt.Printf("          %s\n", d.Reason)
		} else {
			for _, agentID := range d.Agents {
				m, ok := roster[agentID]
				if !ok {
					fmt.Printf("  Route:  ? %s (not in roster)\n", agentID)
					continue
				}
				owdLabel := ""
				if d.OneWayDoor {
					owdLabel = "  ⛔ ONE-WAY DOOR"
				}
				fmt.Printf("  Route:  %s (%s — %s)%s\n",
					m.Code, m.Name, m.Role, owdLabel)
				fmt.Printf("          %s\n", d.Reason)
				fmt.Printf("  Confidence: %d%%  |  Maturity: %s\n",
					d.Confidence, maturityBadge(m))
			}
		}
		if i < len(tasks)-1 {
			fmt.Println()
		}
	}
	fmt.Println(divider)
	fmt.Println()
}

// ── Dispatch plan ─────────────────────────────────────────────────────────────

func printPlan(plan DispatchPlan, roster Roster, cfg Config) {
	fmt.Println()
	fmt.Println("ORCH — Dispatch Plan")
	fmt.Println(divider)
	fmt.Printf("  Trace:      %s\n", plan.TraceID)
	fmt.Printf("  Steps:      %d\n", len(plan.Steps))
	if plan.OneWayDoor {
		fmt.Printf("  ONE-WAY DOOR: ⛔ detected — will require confirmation\n")
	}
	fmt.Println(divider)

	for _, step := range plan.Steps {
		m, ok := roster[step.Agent]
		owdFlag := ""
		if step.OneWayDoor {
			owdFlag = "  ⛔ ONE-WAY DOOR"
		}
		fmt.Printf("\n  Step %d — %s", step.Seq, step.Agent)
		if ok {
			fmt.Printf(" (%s — %s)", m.Code, m.Role)
		}
		fmt.Printf("%s\n", owdFlag)
		fmt.Printf("    Task:   %s\n", step.Packet.Task)
		fmt.Printf("    Reason: %s\n", step.Reason)

		if ok && isDispatchable(m) {
			binary, err := resolveBinary(m, cfg.AgentsDir)
			if err == nil {
				args := buildGoArgs(step.Packet, m, cfg)
				invocation := binary
				if args != nil {
					invocation += " " + strings.Join(args, " ")
				}
				fmt.Printf("    Invoke: %s\n", invocation)
			}
		}

		// Print the HandoffPacket
		pktJSON, _ := json.MarshalIndent(step.Packet, "    ", "  ")
		fmt.Printf("    Packet:\n    %s\n", string(pktJSON))
	}

	fmt.Println()
	fmt.Println(divider)
	if cfg.DryRun {
		fmt.Println("  [dry-run] No agents will be invoked.")
	} else {
		fmt.Println("  Run with: orch run \"<task>\" [flags]")
	}
	fmt.Println()
}

// ── Dispatch result ───────────────────────────────────────────────────────────

func printDispatchResult(result DispatchResult, roster Roster) {
	fmt.Println()
	fmt.Println("ORCH — Dispatch Result")
	fmt.Println(divider)
	fmt.Printf("  Trace: %s\n", result.Plan.TraceID)
	fmt.Printf("  Steps: %d executed / %d planned\n",
		len(result.Results), len(result.Plan.Steps))
	fmt.Println(divider)

	for i, ir := range result.Results {
		m, ok := roster[ir.AgentID]
		label := string(ir.AgentID)
		if ok {
			label = fmt.Sprintf("%s (%s)", m.Code, m.Role)
		}
		statusIcon := "✓"
		if ir.ExitCode != 0 {
			statusIcon = "✗"
		}
		fmt.Printf("\n  Step %d — [%s] %s  (exit %d)\n", i+1, statusIcon, label, ir.ExitCode)

		if ir.Output != "" {
			lines := strings.Split(strings.TrimRight(ir.Output, "\n"), "\n")
			for _, line := range lines {
				fmt.Printf("  │ %s\n", line)
			}
		}
		if ir.Stderr != "" && ir.Stderr != ir.Output {
			lines := strings.Split(strings.TrimRight(ir.Stderr, "\n"), "\n")
			for _, line := range lines {
				if strings.TrimSpace(line) != "" {
					fmt.Printf("  ⚠ %s\n", line)
				}
			}
		}
	}

	fmt.Println()
	fmt.Println(divider)
	if result.OWDPause {
		fmt.Println("  ⛔ Stopped at ONE-WAY DOOR gate.")
	} else if result.Blocked {
		fmt.Println("  ✗ Dispatch blocked — one or more agents reported failure.")
	} else {
		fmt.Printf("  ✓ All %d step(s) complete.  Trace: %s\n",
			len(result.Results), result.Plan.TraceID)
	}
	fmt.Println()
}
