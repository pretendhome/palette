package main

import (
	"fmt"
	"sort"
	"strings"

	core "github.com/pretendhome/palette/core"
)

// ── Task ──────────────────────────────────────────────────────────────────────

// Task is a parsed unit of work derived from the user's input.
// Multi-step inputs ("research X then design Y") produce multiple Tasks
// that are chained together in a DispatchPlan.
type Task struct {
	ID          string
	TraceID     string
	Description string // this step's description
	FullInput   string // the original unmodified input
}

// ── RouteDecision ─────────────────────────────────────────────────────────────

// RouteDecision is what the routing engine produces for a single Task.
type RouteDecision struct {
	Agents     []core.AgentID // in order; len>1 + Parallel=true = concurrent dispatch
	Parallel   bool
	OneWayDoor bool
	Reason     string
	Confidence int // 0–100
}

// ── Route rules ───────────────────────────────────────────────────────────────
// routeRules is the ordered routing table.
// First rule whose keywords match the task description wins.
// To route a new task type: add one entry here. Nothing else changes.

var routeRules = []struct {
	Name     string
	Keywords []string
	Agent    core.AgentID
	Reason   string
}{
	{
		Name: "debug/diagnose/fix",
		Keywords: []string{
			"debug", "fix", "broken", "error", "crash", "fail", "diagnose",
			"connectivity", "not working", "issue", "problem", "bridge",
			"tunnel", "connection", "not reachable", "empty reply",
		},
		Agent:  core.AgentRaptor,
		Reason: "failure/connectivity keywords → Raptor (root-cause specialist)",
	},
	{
		Name: "monitor/signal/watch",
		Keywords: []string{
			"monitor", "watch", "alert", "metric", "signal",
			"latency", "uptime", "status check", "health check",
		},
		Agent:  core.AgentPara,
		Reason: "monitoring keywords → Para (signal monitor)",
	},
	{
		Name: "research/investigate",
		Keywords: []string{
			"research", "investigate", "look up", "what is", "how does",
			"compare", "find out", "search for", "learn about", "explore",
		},
		Agent:  core.AgentArgy,
		Reason: "research keywords → Argy (resource gatherer)",
	},
	{
		Name: "architecture/design",
		Keywords: []string{
			"design", "architect", "tradeoff", "approach", "structure",
			"pattern", "options for", "how should we", "what approach",
			"evaluate", "choose between",
		},
		Agent:  core.AgentRex,
		Reason: "design/tradeoff keywords → Rex (architect)",
	},
	{
		Name: "build/implement",
		Keywords: []string{
			"build", "implement", "create", "write code", "develop",
			"make", "add feature", "code this", "scaffold", "generate",
		},
		Agent:  core.AgentTheri,
		Reason: "build keywords → Theri (builder)",
	},
	{
		Name: "validate/review",
		Keywords: []string{
			"validate", "review", "assess", "audit", "go/no-go",
			"check this", "is this ready", "verify this", "approve",
		},
		Agent:  core.AgentAnky,
		Reason: "validation keywords → Anky (validator)",
	},
	{
		Name: "pitch/narrate/GTM",
		Keywords: []string{
			"pitch", "demo", "narrate", "customer", "presentation",
			"explain to", "business value", "talking points", "gtm",
			"sell", "narrative", "story",
		},
		Agent:  core.AgentYuty,
		Reason: "narrative/GTM keywords → Yuty (narrator)",
	},
	{
		// Cory catches conversational, exploratory, or vague inputs that don't
		// map cleanly to a specialist. She resolves intent first, then hands
		// a refined packet back to Orch for final routing.
		Name: "intent/clarify",
		Keywords: []string{
			"help me", "i need", "i want", "i have a", "how do i",
			"what should", "not sure", "can you", "i'm trying to",
			"we need to", "we should", "looking for", "wondering if",
			"any advice", "where do i start", "not sure where",
		},
		Agent:  core.AgentCory,
		Reason: "conversational/ambiguous input → Cory (intent resolver)",
	},
}

// ── ONE-WAY DOOR detection ────────────────────────────────────────────────────
// Any task matching these keywords is flagged as irreversible and requires
// explicit human confirmation before Orch will execute it.

var oneWayDoorKeywords = []string{
	"delete", "drop database", "drop table", "destroy", "remove all",
	"push to production", "deploy to prod", "release to production",
	"migrate schema", "alter table", "change database schema",
	"force push", "git reset --hard", "git push --force",
	"revoke", "deprovision", "terminate all", "wipe",
}

func detectOneWayDoor(desc string) bool {
	lower := strings.ToLower(desc)
	for _, kw := range oneWayDoorKeywords {
		if strings.Contains(lower, kw) {
			return true
		}
	}
	return false
}

// ── Multi-step parsing ────────────────────────────────────────────────────────
// Detects conjunction keywords in the user input and splits into subtasks.
// "research X then design Y" → two Tasks routed to Argy then Rex.

var conjunctions = []string{
	" then ", " and then ", " after that ", " followed by ", " next, ",
}

func parseInput(input, traceID string) []Task {
	lower := strings.ToLower(input)
	for _, conj := range conjunctions {
		idx := strings.Index(lower, conj)
		if idx > 0 {
			step1 := strings.TrimSpace(input[:idx])
			step2 := strings.TrimSpace(input[idx+len(conj):])
			if step1 != "" && step2 != "" {
				return []Task{
					{ID: newID(), TraceID: traceID, Description: step1, FullInput: input},
					{ID: newID(), TraceID: traceID, Description: step2, FullInput: input},
				}
			}
		}
	}
	return []Task{
		{ID: newID(), TraceID: traceID, Description: input, FullInput: input},
	}
}

// ── Routing engine ────────────────────────────────────────────────────────────

// route determines which agent(s) should handle a task.
// It runs routeRules in order (first keyword match wins), then falls back
// to capability scoring. DESIGN-ONLY agents are never selected.
func route(task Task, roster Roster) RouteDecision {
	descLower := strings.ToLower(task.Description)

	for _, rule := range routeRules {
		for _, kw := range rule.Keywords {
			if strings.Contains(descLower, strings.ToLower(kw)) {
				m, ok := roster[rule.Agent]
				if !ok || !isDispatchable(m) {
					break // agent not available — try next rule
				}
				return RouteDecision{
					Agents:     []core.AgentID{rule.Agent},
					OneWayDoor: detectOneWayDoor(descLower),
					Reason: fmt.Sprintf(
						"matched rule %q via keyword %q\n     %s",
						rule.Name, kw, rule.Reason,
					),
					Confidence: 80,
				}
			}
		}
	}

	return routeByCapability(task, roster)
}

// routeByCapability scores each agent by keyword overlap between the task
// description and the agent's capability list. Used as fallback when no
// explicit rule matches.
func routeByCapability(task Task, roster Roster) RouteDecision {
	type scored struct {
		id    core.AgentID
		score int
	}
	var candidates []scored
	lower := strings.ToLower(task.Description)

	for id, m := range roster {
		if !isDispatchable(m) {
			continue
		}
		score := 0
		for _, cap := range m.Capabilities {
			words := strings.Fields(strings.ReplaceAll(cap, "_", " "))
			for _, w := range words {
				if strings.Contains(lower, w) {
					score++
				}
			}
		}
		if score > 0 {
			candidates = append(candidates, scored{id, score})
		}
	}

	if len(candidates) == 0 {
		// Before giving up, try Cory — she can resolve intent from any input
		if cory, ok := roster[core.AgentCory]; ok && isDispatchable(cory) {
			return RouteDecision{
				Agents:     []core.AgentID{core.AgentCory},
				Reason:     "no routing rule and no capability overlap → Cory (intent resolver)",
				Confidence: 40,
			}
		}
		return RouteDecision{
			Reason:     "no routing rule and no capability overlap — route to human",
			Confidence: 0,
		}
	}

	sort.Slice(candidates, func(i, j int) bool {
		return candidates[i].score > candidates[j].score
	})

	best := candidates[0]
	conf := min(50+best.score*5, 85)
	return RouteDecision{
		Agents:     []core.AgentID{best.id},
		OneWayDoor: detectOneWayDoor(lower),
		Reason: fmt.Sprintf(
			"capability scoring: %s scored %d overlap point(s)",
			best.id, best.score,
		),
		Confidence: conf,
	}
}
