package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os/exec"
	"strings"
	"time"

	core "github.com/pretendhome/palette/core"
)

// ── InvokeResult ──────────────────────────────────────────────────────────────

// InvokeResult is the raw output from running an agent.
type InvokeResult struct {
	AgentID  core.AgentID
	Output   string             // stdout
	Stderr   string             // stderr (Para emits NDJSON HandoffPackets here)
	ExitCode int
	Result   core.HandoffResult // best-effort parsed or inferred
}

// ── AgentRunner interface ─────────────────────────────────────────────────────

// AgentRunner abstracts how the Orchestrator invokes an agent.
// SubprocessRunner runs real binaries/scripts.
// DryRunner prints what would happen without executing.
// This is the same Runner pattern Raptor and Para use — applied to agent invocation.
type AgentRunner interface {
	Invoke(pkt core.HandoffPacket, manifest core.AgentManifest, agentsDir string) InvokeResult
	IsDry() bool
}

// ── SubprocessRunner ──────────────────────────────────────────────────────────

// SubprocessRunner invokes agents as subprocesses.
//
//   - Go agents (runtime=go):  builds CLI args from HandoffPacket.Payload,
//     runs the binary, captures stdout/stderr.
//   - Python agents (runtime=python): encodes packet as JSON on stdin,
//     reads HandoffResult JSON from stdout.
//   - DESIGN-ONLY agents: returns an error immediately.
type SubprocessRunner struct{ cfg Config }

func (r SubprocessRunner) IsDry() bool { return false }

func (r SubprocessRunner) Invoke(
	pkt core.HandoffPacket,
	manifest core.AgentManifest,
	agentsDir string,
) InvokeResult {
	binary, err := resolveBinary(manifest, agentsDir)
	if err != nil {
		return InvokeResult{
			AgentID:  pkt.To,
			Stderr:   err.Error(),
			ExitCode: 1,
			Result:   blockedResult(pkt, err.Error()),
		}
	}

	var cmd *exec.Cmd
	switch core.AgentRuntime(manifest.Runtime) {
	case core.RuntimeGo:
		args := buildGoArgs(pkt, manifest, r.cfg)
		cmd = exec.Command(binary, args...)

	case core.RuntimePython:
		// Python agents: receive HandoffPacket as JSON on stdin,
		// emit HandoffResult JSON on stdout.
		packetJSON, _ := json.Marshal(pkt)
		cmd = exec.Command("python3", binary)
		cmd.Stdin = bytes.NewReader(packetJSON)

	default:
		return InvokeResult{
			AgentID:  pkt.To,
			Stderr:   fmt.Sprintf("agent %q runtime=%q is not dispatchable", manifest.Name, manifest.Runtime),
			ExitCode: 1,
			Result:   blockedResult(pkt, "not dispatchable"),
		}
	}

	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	exitCode := 0
	if err := cmd.Run(); err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			exitCode = exitErr.ExitCode()
		} else {
			exitCode = 1
		}
	}

	out := stdout.String()
	serr := stderr.String()

	// Attempt to parse HandoffResult from stdout (Python agents emit JSON).
	// For Go agents we infer from exit code.
	result := tryParseResult(out, pkt)
	if result.PacketID == "" {
		result = inferResult(pkt, exitCode)
	}

	return InvokeResult{
		AgentID:  pkt.To,
		Output:   out,
		Stderr:   serr,
		ExitCode: exitCode,
		Result:   result,
	}
}

// buildGoArgs maps a HandoffPacket to CLI arguments for a known Go agent.
// Each Go agent in the Palette system has its own flag conventions; the
// Orchestrator knows how to translate the shared payload fields into them.
func buildGoArgs(pkt core.HandoffPacket, manifest core.AgentManifest, cfg Config) []string {
	switch manifest.Name {

	case "velociraptor":
		args := []string{"diagnose"}
		if remote, _ := pkt.Payload["remote"].(string); remote != "" {
			args = append(args, "--remote", remote)
		} else if cfg.Remote != "" {
			args = append(args, "--remote", cfg.Remote)
		}
		if container, _ := pkt.Payload["container"].(string); container != "" {
			args = append(args, "--container", container)
		} else if cfg.Container != "" {
			args = append(args, "--container", cfg.Container)
		}
		if cfg.Verbose {
			args = append(args, "--verbose")
		}
		return args

	case "parasaurolophus":
		args := []string{"check"}
		if remote, _ := pkt.Payload["remote"].(string); remote != "" {
			args = append(args, "--remote", remote)
		} else if cfg.Remote != "" {
			args = append(args, "--remote", cfg.Remote)
		}
		if container, _ := pkt.Payload["container"].(string); container != "" {
			args = append(args, "--container", container)
		} else if cfg.Container != "" {
			args = append(args, "--container", cfg.Container)
		}
		args = append(args, "--verbose") // always verbose when invoked by orch
		return args

	default:
		return nil
	}
}

// ── DryRunner ─────────────────────────────────────────────────────────────────

// DryRunner prints what would be executed without running anything.
// Used by `orch plan` and `orch run --dry-run`.
type DryRunner struct{ verbose bool }

func (r DryRunner) IsDry() bool { return true }

func (r DryRunner) Invoke(
	pkt core.HandoffPacket,
	manifest core.AgentManifest,
	agentsDir string,
) InvokeResult {
	binary, err := resolveBinary(manifest, agentsDir)
	if err != nil {
		binary = fmt.Sprintf("[binary not built: %s]", err.Error())
	}

	args := buildGoArgs(pkt, manifest, Config{})
	invocation := binary
	if args != nil {
		invocation += " " + strings.Join(args, " ")
	} else if core.AgentRuntime(manifest.Runtime) == core.RuntimePython {
		packetPreview, _ := json.MarshalIndent(pkt, "    ", "  ")
		invocation = fmt.Sprintf("python3 %s <<PACKET\n    %s\nPACKET", binary, string(packetPreview))
	}

	return InvokeResult{
		AgentID:  pkt.To,
		Output:   fmt.Sprintf("[dry-run] would invoke:\n  %s", invocation),
		ExitCode: 0,
		Result: core.HandoffResult{
			PacketID:  pkt.ID,
			From:      pkt.To,
			Status:    core.StatusComplete,
			Timestamp: time.Now(),
		},
	}
}

// ── Helpers ───────────────────────────────────────────────────────────────────

func inferResult(pkt core.HandoffPacket, exitCode int) core.HandoffResult {
	status := core.StatusComplete
	if exitCode != 0 {
		status = core.StatusBlocked
	}
	return core.HandoffResult{
		PacketID:  pkt.ID,
		From:      pkt.To,
		Status:    status,
		Timestamp: time.Now(),
	}
}

func blockedResult(pkt core.HandoffPacket, reason string) core.HandoffResult {
	return core.HandoffResult{
		PacketID:  pkt.ID,
		From:      pkt.To,
		Status:    core.StatusBlocked,
		Blockers:  []string{reason},
		Timestamp: time.Now(),
	}
}

func tryParseResult(out string, pkt core.HandoffPacket) core.HandoffResult {
	// Look for a JSON object on a single line in stdout
	for _, line := range strings.Split(out, "\n") {
		line = strings.TrimSpace(line)
		if strings.HasPrefix(line, "{") {
			var r core.HandoffResult
			if err := json.Unmarshal([]byte(line), &r); err == nil && r.PacketID != "" {
				return r
			}
		}
	}
	return core.HandoffResult{}
}
