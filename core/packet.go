// Package core defines the shared types for structured inter-agent
// communication in the Palette multi-agent system.
//
// Wire contract (V2.2):
//
//   Packet  →  Agent  →  Result
//
//   Packet: id, from, to, task, riu_ids, payload, trace_id
//   Result: packet_id, from, status, output, blockers, artifacts, next_agent
//
//   The protocol is 7 fields in, 7 fields out, linked by one ID.
//   Everything domain-specific lives in payload and output.
//   Everything runtime-specific is transport.
package core

// AgentID is a typed string identifying a Palette agent.
type AgentID string

const (
	AgentOrchestrator AgentID = "orchestrator"
	AgentResolver     AgentID = "resolver"
	AgentArchitect    AgentID = "architect"
	AgentResearcher   AgentID = "researcher"
	AgentBuilder      AgentID = "builder"
	AgentValidator    AgentID = "validator"
	AgentMonitor      AgentID = "monitor"
	AgentDebugger     AgentID = "debugger"
	AgentNarrator     AgentID = "narrator"
	AgentHuman        AgentID = "human"
)

// HandoffStatus is the completion status returned by an agent.
// Closed enum: success | failure | blocked. Nothing else.
type HandoffStatus string

const (
	StatusSuccess HandoffStatus = "success" // agent finished the task
	StatusFailure HandoffStatus = "failure" // agent could not complete; blockers explain why
	StatusBlocked HandoffStatus = "blocked" // cannot proceed; external dependency or human needed
)

// HandoffPacket is the structured message passed between Palette agents.
//
// Wire contract: 7 fields. Everything domain-specific lives in Payload.
type HandoffPacket struct {
	ID      string         `json:"id"`       // Unique packet identifier (UUID)
	From    AgentID        `json:"from"`     // Sending agent
	To      AgentID        `json:"to"`       // Receiving agent
	Task    string         `json:"task"`     // Single bounded objective
	RIUs    []string       `json:"riu_ids"`  // Relevant RIU identifiers
	Payload map[string]any `json:"payload"`  // Agent-specific structured data (extension point)
	TraceID string         `json:"trace_id"` // Groups packets in one session/task chain
}

// HandoffResult is the response produced by an agent after processing
// a HandoffPacket.
//
// Wire contract: 7 fields. Everything domain-specific lives in Output.
//
// Invariants:
//   1. PacketID == the Packet.ID this answers. No orphan results.
//   2. Status is a closed enum: success, failure, blocked.
//   3. If Status != success, Blockers explains why. Glass-box.
type HandoffResult struct {
	PacketID  string         `json:"packet_id"`            // ID of the packet this answers
	From      AgentID        `json:"from"`                 // Agent that produced this result
	Status    HandoffStatus  `json:"status"`               // success | failure | blocked
	Output    map[string]any `json:"output"`               // Structured agent output (extension point)
	Blockers  []string       `json:"blockers,omitempty"`   // What prevented completion
	Artifacts []string       `json:"artifacts,omitempty"`  // Files or resources produced
	NextAgent AgentID        `json:"next_agent,omitempty"` // Suggested next routing target
}
