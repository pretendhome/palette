package main

import (
	"fmt"
	"net"
	"os/exec"
	"strings"
	"time"
)

// MetricRunner abstracts local vs remote execution for metric checks.
// The same MetricFunc works whether Docker is local or on a remote VPS —
// identical to Raptor's Runner pattern applied to monitoring.
type MetricRunner interface {
	DockerInspect(container, format string) (string, error)
	TCPCheck(host string, port int) bool
	IsRemote() bool
	Target() string
}

// ── Local runner ──────────────────────────────────────────────────────────────

type LocalRunner struct{}

func (r LocalRunner) DockerInspect(container, format string) (string, error) {
	out, err := exec.Command("docker", "inspect", "--format", format, container).Output()
	return strings.TrimSpace(string(out)), err
}

func (r LocalRunner) TCPCheck(host string, port int) bool {
	conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", host, port), 3*time.Second)
	if err != nil {
		return false
	}
	conn.Close()
	return true
}

func (r LocalRunner) IsRemote() bool { return false }
func (r LocalRunner) Target() string { return "localhost" }

// ── SSH runner ────────────────────────────────────────────────────────────────

type SSHRunner struct{ remote string }

func (r SSHRunner) DockerInspect(container, format string) (string, error) {
	return r.exec(fmt.Sprintf("docker inspect --format '%s' %s", format, container))
}

// TCPCheck uses bash /dev/tcp on the remote host — no extra tools required.
func (r SSHRunner) TCPCheck(host string, port int) bool {
	cmd := fmt.Sprintf("(echo > /dev/tcp/%s/%d) 2>/dev/null && echo open || echo closed", host, port)
	out, err := r.exec(cmd)
	return err == nil && strings.TrimSpace(out) == "open"
}

func (r SSHRunner) exec(cmd string) (string, error) {
	out, err := exec.Command("ssh",
		"-o", "StrictHostKeyChecking=accept-new",
		"-o", "ConnectTimeout=10",
		"-o", "BatchMode=yes",
		r.remote, cmd,
	).Output()
	return strings.TrimSpace(string(out)), err
}

func (r SSHRunner) IsRemote() bool { return true }
func (r SSHRunner) Target() string { return r.remote }

// ── Factory ───────────────────────────────────────────────────────────────────

func newRunner(cfg Config) MetricRunner {
	if cfg.Remote != "" {
		return SSHRunner{remote: cfg.Remote}
	}
	return LocalRunner{}
}
