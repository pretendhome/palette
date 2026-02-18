package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	core "github.com/pretendhome/palette/core"
)

// Roster is the loaded set of all agent manifests, keyed by agent name.
// Built at startup by scanning palette/agents/*/agent.json.
// Adding a new agent requires only dropping an agent.json in its directory.
type Roster map[core.AgentID]core.AgentManifest

// loadRoster scans agentsDir for subdirectories containing agent.json files
// and unmarshals each into an AgentManifest. Agents without a manifest are
// silently skipped — they are not part of the Palette system yet.
func loadRoster(agentsDir string) (Roster, []error) {
	roster := make(Roster)
	var errs []error

	entries, err := os.ReadDir(agentsDir)
	if err != nil {
		return nil, []error{fmt.Errorf("cannot read agents dir %q: %w", agentsDir, err)}
	}

	for _, e := range entries {
		if !e.IsDir() {
			continue
		}
		manifestPath := filepath.Join(agentsDir, e.Name(), "agent.json")
		data, err := os.ReadFile(manifestPath)
		if err != nil {
			continue // no manifest — skip silently
		}
		var m core.AgentManifest
		if err := json.Unmarshal(data, &m); err != nil {
			errs = append(errs, fmt.Errorf("agent %q: invalid agent.json: %w", e.Name(), err))
			continue
		}
		roster[core.AgentID(m.Name)] = m
	}

	return roster, errs
}

// isDispatchable returns true when the Orchestrator can actually invoke the agent:
// not DESIGN-ONLY, has an entry_point, and is not "orchestrator" itself.
func isDispatchable(m core.AgentManifest) bool {
	return m.Status != core.StatusDesignOnly &&
		m.EntryPoint != nil &&
		*m.EntryPoint != "" &&
		m.Name != "orchestrator"
}

// resolveBinary finds the agent's executable binary or script.
// Search order:
//  1. <agentsDir>/<agentname>/<entry_point>   (development: built in-place)
//  2. PATH                                     (installed: built and added to PATH)
func resolveBinary(m core.AgentManifest, agentsDir string) (string, error) {
	if m.EntryPoint == nil || *m.EntryPoint == "" {
		return "", fmt.Errorf("agent %q has no entry_point", m.Name)
	}
	ep := *m.EntryPoint

	// Try the agent's own directory first (normal development workflow)
	candidate := filepath.Join(agentsDir, m.Name, ep)
	if _, err := os.Stat(candidate); err == nil {
		return candidate, nil
	}

	// Fall back to PATH (installed workflow)
	// Use os.LookPath manually to stay dependency-free
	pathDirs := filepath.SplitList(os.Getenv("PATH"))
	for _, dir := range pathDirs {
		full := filepath.Join(dir, ep)
		if info, err := os.Stat(full); err == nil && !info.IsDir() {
			return full, nil
		}
	}

	return "", fmt.Errorf(
		"binary %q not found — build it first:\n  cd %s && go build -o %s .",
		ep,
		filepath.Join(agentsDir, m.Name),
		ep,
	)
}

// maturityBadge returns a short human-readable status string for the agent.
func maturityBadge(m core.AgentManifest) string {
	switch core.AgentStatus(m.Status) {
	case core.StatusWorking:
		return fmt.Sprintf("WORKING     tier %d  %d successes", m.Maturity.Tier, m.Maturity.Successes)
	case core.StatusProduction:
		return fmt.Sprintf("PRODUCTION  tier %d  %d successes", m.Maturity.Tier, m.Maturity.Successes)
	case core.StatusDesignOnly:
		return "DESIGN-ONLY  (no runtime)"
	default:
		return fmt.Sprintf("UNVALIDATED tier %d  %d/%d successes",
			m.Maturity.Tier, m.Maturity.Successes, m.Maturity.PromotesAt)
	}
}
