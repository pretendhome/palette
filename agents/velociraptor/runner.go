package main

import (
	"fmt"
	"net"
	"os/exec"
	"strings"
	"time"
)

// Runner executes shell commands either locally or on a remote host via SSH.
// All probes accept a Runner so they stay location-agnostic — the same probe
// code works whether the container is local or on a remote VPS.
type Runner interface {
	// Exec runs a shell command and returns trimmed stdout.
	Exec(cmd string) (string, error)

	// DockerExec runs a shell command inside a named container.
	DockerExec(container, cmd string) (string, error)

	// DockerInspect runs docker inspect with a Go template format string.
	DockerInspect(container, format string) (string, error)

	// DockerLogs returns the last N lines of a container's combined logs.
	DockerLogs(container string, lines int) (string, error)

	// TCPCheck tests whether host:port accepts a TCP connection.
	// Uses Go's net.Dial locally; bash /dev/tcp remotely (no extra tools needed).
	TCPCheck(host string, port int) bool

	// IsRemote returns true when commands execute on a remote host.
	IsRemote() bool

	// Target returns a human-readable label ("local" or "user@host").
	Target() string
}

// ─── LocalRunner ──────────────────────────────────────────────────────────────

type LocalRunner struct{ verbose bool }

func NewLocalRunner(verbose bool) Runner { return &LocalRunner{verbose: verbose} }

func (r *LocalRunner) Exec(cmd string) (string, error) {
	if r.verbose {
		fmt.Printf("    [local] %s\n", cmd)
	}
	out, err := exec.Command("bash", "-c", cmd).Output()
	if err != nil {
		if ee, ok := err.(*exec.ExitError); ok {
			return strings.TrimSpace(string(out)),
				fmt.Errorf("exit %d: %s", ee.ExitCode(), strings.TrimSpace(string(ee.Stderr)))
		}
		return strings.TrimSpace(string(out)), err
	}
	return strings.TrimSpace(string(out)), nil
}

func (r *LocalRunner) DockerExec(container, cmd string) (string, error) {
	return r.Exec(fmt.Sprintf("docker exec %s bash -c %q", container, cmd))
}

func (r *LocalRunner) DockerInspect(container, format string) (string, error) {
	out, err := exec.Command("docker", "inspect", "--format", format, container).Output()
	if err != nil {
		return "", fmt.Errorf("docker inspect: %w", err)
	}
	return strings.TrimSpace(string(out)), nil
}

func (r *LocalRunner) DockerLogs(container string, lines int) (string, error) {
	out, err := exec.Command("docker", "logs", "--tail", fmt.Sprint(lines), container).CombinedOutput()
	return string(out), err
}

func (r *LocalRunner) TCPCheck(host string, port int) bool {
	conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", host, port), 3*time.Second)
	if err != nil {
		return false
	}
	conn.Close()
	return true
}

func (r *LocalRunner) IsRemote() bool { return false }
func (r *LocalRunner) Target() string { return "local" }

// ─── SSHRunner ────────────────────────────────────────────────────────────────

type SSHRunner struct {
	remote  string // user@host
	verbose bool
}

func NewSSHRunner(remote string, verbose bool) Runner {
	return &SSHRunner{remote: remote, verbose: verbose}
}

func (r *SSHRunner) Exec(cmd string) (string, error) {
	if r.verbose {
		fmt.Printf("    [ssh %s] %s\n", r.remote, cmd)
	}
	args := []string{
		"-o", "StrictHostKeyChecking=accept-new",
		"-o", "ConnectTimeout=10",
		r.remote, cmd,
	}
	out, err := exec.Command("ssh", args...).Output()
	result := strings.TrimSpace(string(out))
	if err != nil {
		if ee, ok := err.(*exec.ExitError); ok {
			return result, fmt.Errorf("ssh exit %d: %s", ee.ExitCode(), strings.TrimSpace(string(ee.Stderr)))
		}
		return result, err
	}
	return result, nil
}

func (r *SSHRunner) DockerExec(container, cmd string) (string, error) {
	// Use printf to avoid quoting issues with nested quotes in cmd.
	return r.Exec(fmt.Sprintf("docker exec %s bash -c %q", container, cmd))
}

func (r *SSHRunner) DockerInspect(container, format string) (string, error) {
	// Single-quote the format to protect {{ }} from remote shell expansion.
	cmd := fmt.Sprintf("docker inspect --format '%s' %s", format, container)
	out, err := r.Exec(cmd)
	if err != nil {
		return "", fmt.Errorf("docker inspect on %s: %w", r.remote, err)
	}
	return out, nil
}

func (r *SSHRunner) DockerLogs(container string, lines int) (string, error) {
	return r.Exec(fmt.Sprintf("docker logs --tail %d %s 2>&1", lines, container))
}

func (r *SSHRunner) TCPCheck(host string, port int) bool {
	// bash /dev/tcp is available on all Linux systems without extra tools.
	out, _ := r.Exec(fmt.Sprintf(
		"bash -c '(echo > /dev/tcp/%s/%d) 2>/dev/null && echo open || echo closed'",
		host, port))
	return strings.TrimSpace(out) == "open"
}

func (r *SSHRunner) IsRemote() bool { return true }
func (r *SSHRunner) Target() string { return r.remote }

// ─── Runner factory ───────────────────────────────────────────────────────────

// newRunner returns the appropriate Runner based on Config.
// If Remote is set, returns an SSHRunner; otherwise a LocalRunner.
func newRunner(cfg Config) Runner {
	if cfg.Remote != "" {
		return NewSSHRunner(cfg.Remote, cfg.Verbose)
	}
	return NewLocalRunner(cfg.Verbose)
}
