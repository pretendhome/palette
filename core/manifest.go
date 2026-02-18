package core

// AgentManifest mirrors the agent.json schema.
// The Orchestrator loads manifests at startup to build its routing table:
// which agents exist, what they accept, what tier they are, and how to
// invoke them.
type AgentManifest struct {
	Name         string            `json:"name"`
	Version      string            `json:"version"`
	ArkType      string            `json:"ark_type"`
	Code         string            `json:"code"`
	Role         string            `json:"role"`
	Description  string            `json:"description"`
	Status       AgentStatus       `json:"status"`
	Maturity     AgentMaturity     `json:"maturity"`
	EntryPoint   *string           `json:"entry_point"` // nil for DESIGN-ONLY agents
	Runtime      AgentRuntime      `json:"runtime"`
	Capabilities []string          `json:"capabilities"`
	Constraints  map[string]bool   `json:"constraints"`
	AcceptsFrom  []AgentID         `json:"accepts_from"`
	RoutesTo     []AgentID         `json:"routes_to"`
	Invocation   AgentInvocation   `json:"invocation"`
	Logging      AgentLogging      `json:"logging"`
}

// AgentStatus reflects the Palette maturity model tier labels.
type AgentStatus string

const (
	StatusUnvalidated AgentStatus = "UNVALIDATED"  // Tier 1: human-in-the-loop required
	StatusWorking     AgentStatus = "WORKING"       // Tier 2: autonomous with review
	StatusProduction  AgentStatus = "PRODUCTION"    // Tier 3: fully autonomous
	StatusDesignOnly  AgentStatus = "DESIGN-ONLY"   // Tier 0: spec only, no runtime
)

// AgentRuntime is the execution environment for the agent's entry point.
type AgentRuntime string

const (
	RuntimeGo     AgentRuntime = "go"
	RuntimePython AgentRuntime = "python"
	RuntimeNone   AgentRuntime = "none" // DESIGN-ONLY agents
)

// AgentMaturity tracks the promotion path counters defined in palette-core.md.
type AgentMaturity struct {
	Tier       int `json:"tier"`        // 0=design-only, 1=unvalidated, 2=working, 3=production
	Successes  int `json:"successes"`
	Failures   int `json:"failures"`
	PromotesAt int `json:"promotes_at"` // successes needed to reach next tier
}

// AgentInvocation describes how to invoke the agent.
type AgentInvocation struct {
	Command string   `json:"command"`
	Aliases []string `json:"aliases"`
}

// AgentLogging describes where the agent logs maturity events.
type AgentLogging struct {
	Ledger        string `json:"ledger"`
	TrackMaturity bool   `json:"track_maturity"`
	LogQueries    bool   `json:"log_queries,omitempty"`
}
