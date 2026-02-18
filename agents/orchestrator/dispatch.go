package main

import (
	"crypto/rand"
	"fmt"
	"sync"
	"time"

	core "github.com/pretendhome/palette/core"
)

// ── DispatchPlan ──────────────────────────────────────────────────────────────

// DispatchStep is one unit of work: one agent, one packet.
type DispatchStep struct {
	Seq        int
	Agent      core.AgentID
	Packet     core.HandoffPacket
	Reason     string
	Parallel   bool // true = this step runs concurrently with adjacent Parallel steps
	OneWayDoor bool
}

// DispatchPlan is the full ordered sequence of steps Orch will execute.
type DispatchPlan struct {
	TraceID    string
	Steps      []DispatchStep
	OneWayDoor bool // any step flags an irreversible action
}

// DispatchResult is the collected output after executing a DispatchPlan.
type DispatchResult struct {
	Plan     DispatchPlan
	Results  []InvokeResult
	Blocked  bool
	OWDPause bool // plan was stopped at a ONE-WAY DOOR gate
}

// ── Plan construction ─────────────────────────────────────────────────────────

// buildPlan converts a slice of Tasks + their RouteDecisions into a
// DispatchPlan. Multi-step tasks produce serial chains. Decisions with
// len(Agents)>1 and Parallel=true produce concurrent steps.
func buildPlan(tasks []Task, decisions []RouteDecision, cfg Config) DispatchPlan {
	plan := DispatchPlan{TraceID: tasks[0].TraceID}

	for i, task := range tasks {
		if i >= len(decisions) {
			break
		}
		d := decisions[i]
		if len(d.Agents) == 0 {
			continue
		}

		for j, agentID := range d.Agents {
			pkt := buildPacket(task, agentID, cfg)
			step := DispatchStep{
				Seq:        len(plan.Steps) + 1,
				Agent:      agentID,
				Packet:     pkt,
				Reason:     d.Reason,
				Parallel:   d.Parallel && j > 0,
				OneWayDoor: d.OneWayDoor,
			}
			plan.Steps = append(plan.Steps, step)
		}

		if d.OneWayDoor {
			plan.OneWayDoor = true
		}
	}

	return plan
}

// buildPacket constructs a HandoffPacket for a task routed to a specific agent.
// Config values (remote, container, etc.) are embedded in the payload so the
// receiving agent's CLI builder can extract them.
func buildPacket(task Task, agentID core.AgentID, cfg Config) core.HandoffPacket {
	return core.HandoffPacket{
		ID:      newID(),
		TraceID: task.TraceID,
		From:    core.AgentOrchestrator,
		To:      agentID,
		Task:    task.Description,
		Constraints: []string{
			"stay within your defined scope",
			"report status and blockers in HandoffResult",
			"flag ONE-WAY DOOR actions before executing",
		},
		Payload: map[string]any{
			"remote":      cfg.Remote,
			"container":   cfg.Container,
			"adapter_url": cfg.AdapterURL,
			"tunnel_port": cfg.TunnelPort,
			"bridge_port": cfg.BridgePort,
		},
		Timestamp: time.Now(),
	}
}

// ── Plan execution ────────────────────────────────────────────────────────────

// executePlan runs the dispatch plan.
//
// ONE-WAY DOOR steps pause and require explicit confirmation unless --auto
// is set. Maturity gates on UNVALIDATED agents also require confirmation.
//
// Steps run serially by default. Steps marked Parallel run concurrently
// (future use — v0.1 executes serially even when Parallel is set).
func executePlan(
	plan DispatchPlan,
	roster Roster,
	runner AgentRunner,
	cfg Config,
) DispatchResult {
	result := DispatchResult{Plan: plan}

	for _, step := range plan.Steps {
		manifest, ok := roster[step.Agent]
		if !ok {
			ir := InvokeResult{
				AgentID:  step.Agent,
				Stderr:   fmt.Sprintf("agent %q not in roster", step.Agent),
				ExitCode: 1,
				Result:   blockedResult(step.Packet, "agent not found"),
			}
			result.Results = append(result.Results, ir)
			result.Blocked = true
			break
		}

		// ── ONE-WAY DOOR gate ─────────────────────────────────────────────────
		if step.OneWayDoor && !cfg.AutoConfirm && !runner.IsDry() {
			fmt.Printf("\n⛔  ONE-WAY DOOR DETECTED\n")
			fmt.Printf("   Step %d routes to %s (%s)\n", step.Seq, manifest.Code, manifest.Role)
			fmt.Printf("   Task: %s\n", step.Packet.Task)
			fmt.Printf("\n   This action may be irreversible. Confirm? [y/N] ")
			var ans string
			fmt.Scan(&ans)
			if ans != "y" && ans != "Y" {
				result.OWDPause = true
				fmt.Println("   Stopped at ONE-WAY DOOR. Re-run with --auto to bypass.")
				break
			}
		}

		// ── Maturity gate ─────────────────────────────────────────────────────
		if core.AgentStatus(manifest.Status) == core.StatusUnvalidated &&
			!cfg.AutoConfirm && !runner.IsDry() {
			fmt.Printf("\n⚠  MATURITY GATE\n")
			fmt.Printf("   %s (%s) is UNVALIDATED — tier %d, %d/%d successes\n",
				manifest.Code, manifest.Role,
				manifest.Maturity.Tier,
				manifest.Maturity.Successes,
				manifest.Maturity.PromotesAt,
			)
			fmt.Printf("   Human-in-the-loop is required. Proceed? [y/N] ")
			var ans string
			fmt.Scan(&ans)
			if ans != "y" && ans != "Y" {
				fmt.Println("   Skipped. Use --auto to suppress this gate.")
				continue
			}
		}

		// ── Invoke ────────────────────────────────────────────────────────────
		fmt.Printf("  → %s (%s)\n", manifest.Code, manifest.Role)
		ir := runner.Invoke(step.Packet, manifest, cfg.AgentsDir)
		result.Results = append(result.Results, ir)

		if ir.ExitCode != 0 && !runner.IsDry() {
			result.Blocked = true
			break
		}
	}

	return result
}

// executeParallel runs a set of steps concurrently using goroutines.
// Used when RouteDecision.Parallel=true and len(Agents)>1.
// (Parallel dispatch is available for future use; v0.1 routes single agents.)
func executeParallel(
	steps []DispatchStep,
	roster Roster,
	runner AgentRunner,
	agentsDir string,
) []InvokeResult {
	results := make([]InvokeResult, len(steps))
	var wg sync.WaitGroup

	for i, step := range steps {
		wg.Add(1)
		go func(i int, step DispatchStep) {
			defer wg.Done()
			manifest, ok := roster[step.Agent]
			if !ok {
				results[i] = InvokeResult{
					AgentID:  step.Agent,
					Stderr:   fmt.Sprintf("agent %q not in roster", step.Agent),
					ExitCode: 1,
					Result:   blockedResult(step.Packet, "agent not found"),
				}
				return
			}
			results[i] = runner.Invoke(step.Packet, manifest, agentsDir)
		}(i, step)
	}

	wg.Wait()
	return results
}

// ── Utility ───────────────────────────────────────────────────────────────────

// newID generates a random UUID v4 for packet and task IDs.
func newID() string {
	b := make([]byte, 16)
	_, _ = rand.Read(b)
	b[6] = (b[6] & 0x0f) | 0x40 // version 4
	b[8] = (b[8] & 0x3f) | 0x80 // variant
	return fmt.Sprintf("%08x-%04x-%04x-%04x-%012x",
		b[0:4], b[4:6], b[6:8], b[8:10], b[10:16])
}
