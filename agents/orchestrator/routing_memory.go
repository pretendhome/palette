package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"

	core "github.com/pretendhome/palette/core"
)

// ── Routing Memory — Phase 0: Passive Collection ────────────────────────────
//
// Appends one observation per workflow completion. No weight adjustment.
// No behavioral change to routing. Pure data collection.
//
// File: routing_memory_v1.0.json (append-only NDJSON for fast writes)
// Stats: `orch stats` reads and summarizes

const routingMemoryFile = "routing_memory_v1.0.json"

// Observation is one completed workflow outcome record.
type Observation struct {
	ID                   string    `json:"id"`
	Timestamp            string    `json:"timestamp"`
	Generation           int       `json:"generation"`
	TraceID              string    `json:"trace_id"`
	TaskDescription      string    `json:"task_description"`
	MatchedRule          string    `json:"matched_rule"`
	RoutedAgent          string    `json:"routed_agent"`
	ValidatorResult      string    `json:"validator_result"` // pass | fail | skipped
	ExitCode             int       `json:"exit_code"`
	DurationMs           int64     `json:"duration_ms"`
	OneWayDoor           bool      `json:"one_way_door"`
	ConfidenceAtDispatch int       `json:"confidence_at_dispatch"`
	InstanceID           string    `json:"instance_id"` // for future signal aggregation
}

// RoutingStats summarizes accumulated routing memory.
type RoutingStats struct {
	TotalObservations int                      `json:"total_observations"`
	Generation        int                      `json:"generation"`
	PerRule           map[string]*RuleStats     `json:"per_rule"`
	PerAgent          map[string]*AgentStats    `json:"per_agent"`
	ActivationReady   bool                     `json:"activation_ready"`
	ActivationNote    string                   `json:"activation_note"`
}

type RuleStats struct {
	Observations int     `json:"observations"`
	Successes    int     `json:"successes"`
	Failures     int     `json:"failures"`
	Skipped      int     `json:"skipped"`
	SuccessRate  float64 `json:"success_rate"`
	ReadyForGA   bool    `json:"ready_for_ga"`
}

type AgentStats struct {
	Dispatches     int     `json:"dispatches"`
	Successes      int     `json:"successes"`
	Failures       int     `json:"failures"`
	SuccessRate    float64 `json:"success_rate"`
	LastDispatched string  `json:"last_dispatched"`
}

var (
	memoryMu   sync.Mutex
	instanceID string
)

func init() {
	// Stable instance ID from hostname — no crypto needed for phase 0
	host, _ := os.Hostname()
	if host == "" {
		host = "unknown"
	}
	instanceID = host
}

// memoryPath returns the path to the routing memory file.
func memoryPath(agentsDir string) string {
	return filepath.Join(agentsDir, "orchestrator", routingMemoryFile)
}

// recordObservation appends one observation to the routing memory.
// Best-effort: never blocks or fails the workflow.
func recordObservation(
	agentsDir string,
	task Task,
	decision RouteDecision,
	result InvokeResult,
	durationMs int64,
) {
	memoryMu.Lock()
	defer memoryMu.Unlock()

	// Determine validator result from the HandoffResult
	validatorResult := "skipped"
	if result.Result.Status == core.StatusSuccess {
		validatorResult = "pass"
	} else if result.ExitCode != 0 || result.Result.Status == core.StatusBlocked {
		validatorResult = "fail"
	}

	// Extract matched rule from Reason field
	matchedRule := "capability_fallback"
	if len(decision.Reason) > 0 {
		// Reason format: "matched rule \"debug/diagnose/fix\" via keyword \"error\""
		for _, rule := range routeRules {
			if contains(decision.Reason, rule.Name) {
				matchedRule = rule.Name
				break
			}
		}
	}

	agentName := "unknown"
	if len(decision.Agents) > 0 {
		agentName = string(decision.Agents[0])
	}

	obs := Observation{
		ID:                   newID(),
		Timestamp:            time.Now().UTC().Format(time.RFC3339),
		Generation:           0, // Phase 0: always generation 0
		TraceID:              task.TraceID,
		TaskDescription:      truncate(task.Description, 200),
		MatchedRule:          matchedRule,
		RoutedAgent:          agentName,
		ValidatorResult:      validatorResult,
		ExitCode:             result.ExitCode,
		DurationMs:           durationMs,
		OneWayDoor:           decision.OneWayDoor,
		ConfidenceAtDispatch: decision.Confidence,
		InstanceID:           instanceID,
	}

	path := memoryPath(agentsDir)
	f, err := os.OpenFile(path, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Fprintf(os.Stderr, "[routing-memory] write error: %v\n", err)
		return
	}
	defer f.Close()

	data, _ := json.Marshal(obs)
	data = append(data, '\n')
	f.Write(data)
}

// loadObservations reads all observations from the routing memory file.
func loadObservations(agentsDir string) ([]Observation, error) {
	path := memoryPath(agentsDir)
	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, nil
		}
		return nil, err
	}

	var observations []Observation
	for _, line := range splitLines(data) {
		if len(line) == 0 {
			continue
		}
		var obs Observation
		if err := json.Unmarshal(line, &obs); err != nil {
			continue // skip malformed lines
		}
		observations = append(observations, obs)
	}
	return observations, nil
}

// computeStats summarizes routing memory into actionable stats.
func computeStats(observations []Observation) RoutingStats {
	stats := RoutingStats{
		TotalObservations: len(observations),
		PerRule:           make(map[string]*RuleStats),
		PerAgent:          make(map[string]*AgentStats),
	}

	for _, obs := range observations {
		// Per-rule stats
		rs, ok := stats.PerRule[obs.MatchedRule]
		if !ok {
			rs = &RuleStats{}
			stats.PerRule[obs.MatchedRule] = rs
		}
		rs.Observations++
		switch obs.ValidatorResult {
		case "pass":
			rs.Successes++
		case "fail":
			rs.Failures++
		default:
			rs.Skipped++
		}

		// Per-agent stats
		as, ok := stats.PerAgent[obs.RoutedAgent]
		if !ok {
			as = &AgentStats{}
			stats.PerAgent[obs.RoutedAgent] = as
		}
		as.Dispatches++
		if obs.ValidatorResult == "pass" {
			as.Successes++
		} else if obs.ValidatorResult == "fail" {
			as.Failures++
		}
		as.LastDispatched = obs.Timestamp
	}

	// Compute rates and GA readiness
	allReady := true
	for _, rs := range stats.PerRule {
		if rs.Observations > 0 {
			rs.SuccessRate = float64(rs.Successes) / float64(rs.Observations)
		}
		rs.ReadyForGA = rs.Observations >= 50
		if !rs.ReadyForGA {
			allReady = false
		}
	}

	for _, as := range stats.PerAgent {
		if as.Dispatches > 0 {
			as.SuccessRate = float64(as.Successes) / float64(as.Dispatches)
		}
	}

	stats.ActivationReady = len(observations) >= 500 && allReady
	if stats.ActivationReady {
		stats.ActivationNote = "Phase 1 activation threshold met. Evolutionary weight adjustment can be enabled."
	} else if len(observations) < 500 {
		stats.ActivationNote = fmt.Sprintf("Need %d more observations for system-wide threshold (500).", 500-len(observations))
	} else {
		stats.ActivationNote = "System-wide threshold met but some rules have <50 observations."
	}

	return stats
}

// printStats outputs a human-readable routing memory summary.
func printStats(agentsDir string) error {
	observations, err := loadObservations(agentsDir)
	if err != nil {
		return err
	}
	if len(observations) == 0 {
		fmt.Println("\nROUTING MEMORY — No observations yet (Phase 0: passive collection)")
		fmt.Println("  Observations accumulate after each workflow completion.")
		fmt.Println("  Weight adjustment activates after 500 observations.")
		return nil
	}

	stats := computeStats(observations)
	fmt.Println()
	fmt.Println("ROUTING MEMORY — Phase 0 (passive collection)")
	fmt.Println(divider)
	fmt.Printf("  Total observations: %d\n", stats.TotalObservations)
	fmt.Printf("  Activation ready:   %v\n", stats.ActivationReady)
	fmt.Printf("  Note:               %s\n", stats.ActivationNote)
	fmt.Println()

	fmt.Println("  PER-RULE STATS:")
	fmt.Printf("  %-30s  %6s  %6s  %6s  %8s  %s\n", "RULE", "OBS", "PASS", "FAIL", "RATE", "GA-READY")
	fmt.Println(divider)
	for rule, rs := range stats.PerRule {
		ready := "no"
		if rs.ReadyForGA {
			ready = "YES"
		}
		fmt.Printf("  %-30s  %6d  %6d  %6d  %7.1f%%  %s\n",
			rule, rs.Observations, rs.Successes, rs.Failures, rs.SuccessRate*100, ready)
	}
	fmt.Println()

	fmt.Println("  PER-AGENT STATS:")
	fmt.Printf("  %-20s  %6s  %6s  %6s  %8s  %s\n", "AGENT", "DISP", "PASS", "FAIL", "RATE", "LAST")
	fmt.Println(divider)
	for agent, as := range stats.PerAgent {
		last := as.LastDispatched
		if len(last) > 10 {
			last = last[:10]
		}
		fmt.Printf("  %-20s  %6d  %6d  %6d  %7.1f%%  %s\n",
			agent, as.Dispatches, as.Successes, as.Failures, as.SuccessRate*100, last)
	}
	fmt.Println()
	return nil
}

// ── Helpers ─────────────────────────────────────────────────────────────────

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(substr) > 0 && containsStr(s, substr))
}

func containsStr(s, sub string) bool {
	for i := 0; i <= len(s)-len(sub); i++ {
		if s[i:i+len(sub)] == sub {
			return true
		}
	}
	return false
}

func truncate(s string, max int) string {
	if len(s) <= max {
		return s
	}
	return s[:max] + "..."
}

func splitLines(data []byte) [][]byte {
	var lines [][]byte
	start := 0
	for i, b := range data {
		if b == '\n' {
			lines = append(lines, data[start:i])
			start = i + 1
		}
	}
	if start < len(data) {
		lines = append(lines, data[start:])
	}
	return lines
}
