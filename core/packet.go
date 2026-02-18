// Package core defines the shared types for structured inter-agent
// communication in the Palette multi-agent system.
//
// All agents — whether Go binaries or Python scripts — speak the same
// protocol: HandoffPacket in, HandoffResult out. Python agents validate
// against the companion JSON schemas in schema/.
package core

import "time"

// AgentID is a typed string identifying a Palette agent.
type AgentID string

const (
	AgentOrchestrator AgentID = "orchestrator"
	AgentCory         AgentID = "corythosaurus"
	AgentRex          AgentID = "rex"
	AgentArgy         AgentID = "argentavis"
	AgentTheri        AgentID = "therizinosaurus"
	AgentAnky         AgentID = "ankylosaurus"
	AgentPara         AgentID = "parasaurolophus"
	AgentRaptor       AgentID = "velociraptor"
	AgentYuty         AgentID = "yutyrannus"
	AgentHuman        AgentID = "human"
)

// HandoffStatus is the completion status returned by an agent.
type HandoffStatus string

const (
	StatusComplete   HandoffStatus = "complete"    // agent finished the task
	StatusBlocked    HandoffStatus = "blocked"     // cannot proceed; blockers listed
	StatusEscalate   HandoffStatus = "escalate"    // needs a different agent or human
	StatusOneWayDoor HandoffStatus = "one_way_door" // stop; human confirmation required
)

// OneWayDoor describes a decision that cannot be easily reversed.
// When Detected is true the Orchestrator must pause and surface Details
// to the human before routing further.
type OneWayDoor struct {
	Detected bool     `json:"detected"`
	Details  []string `json:"details,omitempty"`
}

// HandoffPacket is the structured message passed between Palette agents.
// Every inter-agent communication uses this envelope — nothing travels
// as free-form text.
//
// Minimum required fields: ID, TraceID, From, To, Task, Timestamp.
// All other fields default to their zero values.
type HandoffPacket struct {
	ID          string         `json:"id"`           // Unique packet identifier (UUID)
	TraceID     string         `json:"trace_id"`     // Groups packets in one session/task chain
	From        AgentID        `json:"from"`         // Sending agent
	To          AgentID        `json:"to"`           // Receiving agent
	RIUs        []string       `json:"riu_ids"`      // Relevant RIU identifiers (e.g. "RIU-006")
	Task        string         `json:"task"`         // Single bounded objective
	Artifacts   []string       `json:"artifacts"`    // Input file paths the agent needs
	Constraints []string       `json:"constraints"`  // Behavioral constraints for this task
	OneWayDoor  OneWayDoor     `json:"one_way_door"` // Gate flag; stops routing until human confirms
	Payload     map[string]any `json:"payload"`      // Agent-specific structured data
	Timestamp   time.Time      `json:"timestamp"`
}

// HandoffResult is the response produced by an agent after processing
// a HandoffPacket.  The Orchestrator reads Status first to decide the
// next routing step.
type HandoffResult struct {
	PacketID          string         `json:"packet_id"`           // ID of the packet this answers
	From              AgentID        `json:"from"`                // Agent that produced this result
	Status            HandoffStatus  `json:"status"`
	Output            map[string]any `json:"output"`              // Structured agent output
	ProducedArtifacts []string       `json:"produced_artifacts"`  // Files created or modified
	Blockers          []string       `json:"blockers,omitempty"`  // What is blocking completion
	NextAgent         AgentID        `json:"next_agent,omitempty"` // Suggested next routing target
	Timestamp         time.Time      `json:"timestamp"`
}
