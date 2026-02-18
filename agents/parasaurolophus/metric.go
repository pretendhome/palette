package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"

	core "github.com/pretendhome/palette/core"
)

// ── Signal types ──────────────────────────────────────────────────────────────

type SignalStatus int

const (
	SignalNormal SignalStatus = iota
	SignalWarn
	SignalAlert
	SignalError
)

func (s SignalStatus) String() string {
	switch s {
	case SignalNormal:
		return "NORMAL"
	case SignalWarn:
		return "WARN"
	case SignalAlert:
		return "ALERT"
	case SignalError:
		return "ERROR"
	}
	return "UNKNOWN"
}

// MetricSignal is the output of a single metric check.
// Para never interprets these — it emits them and routes them.
type MetricSignal struct {
	Name     string
	Status   SignalStatus
	Value    string       // current observed value (human-readable)
	Baseline string       // expected normal value
	Detail   string       // what changed, nothing more
	RouteTo  core.AgentID // agent to route HandoffPacket to when not normal
}

// MetricFunc is the signature all metric implementations must satisfy.
// Accepting MetricRunner makes checks location-agnostic: same function works
// locally or over SSH, identical to Raptor's ProbeFunc pattern.
type MetricFunc func(run MetricRunner, cfg Config) MetricSignal

// metricChain is the ordered list of all metrics Para monitors.
// Adding a new metric = one entry here.
var metricChain = []struct {
	Name     string
	Baseline string
	Fn       MetricFunc
}{
	{"AdapterHealth", `HTTP 200, {"status":"ok"}`, checkAdapterHealth},
	{"TunnelPort", "TCP listening on tunnel port (localhost)", checkTunnelPort},
	{"AdapterLatency", "response < warn threshold", checkAdapterLatency},
	{"ContainerStatus", "State.Status = running", checkContainerRunning},
	{"BridgePort", "TCP reachable at container_bridge_ip:bridge_port", checkBridgePort},
	{"UpstreamRoute", `response.source != "local_fallback"`, checkUpstreamRoute},
}

// ── Constructors ──────────────────────────────────────────────────────────────

func normal(name, value, baseline string) MetricSignal {
	return MetricSignal{
		Name:     name,
		Status:   SignalNormal,
		Value:    value,
		Baseline: baseline,
		Detail:   value + " — within normal range",
	}
}

func sigwarn(name, value, baseline, detail string) MetricSignal {
	return MetricSignal{
		Name:     name,
		Status:   SignalWarn,
		Value:    value,
		Baseline: baseline,
		Detail:   detail,
		RouteTo:  core.AgentRaptor,
	}
}

func sigalert(name, value, baseline, detail string) MetricSignal {
	return MetricSignal{
		Name:     name,
		Status:   SignalAlert,
		Value:    value,
		Baseline: baseline,
		Detail:   detail,
		RouteTo:  core.AgentRaptor,
	}
}

func sigerr(name, detail string) MetricSignal {
	return MetricSignal{
		Name:     name,
		Status:   SignalError,
		Value:    "error",
		Baseline: "reachable",
		Detail:   detail,
		RouteTo:  core.AgentRaptor,
	}
}

// ── Metric implementations ────────────────────────────────────────────────────

// checkAdapterHealth probes the local adapter's /health endpoint.
// Expects HTTP 200 with {"status":"ok"}.
func checkAdapterHealth(_ MetricRunner, cfg Config) MetricSignal {
	url := strings.TrimRight(cfg.AdapterURL, "/") + cfg.HealthPath
	start := time.Now()
	resp, err := httpGET(url, 5*time.Second)
	if err != nil {
		return sigerr("AdapterHealth", "not reachable: "+shortErr(err))
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	elapsed := time.Since(start).Round(time.Millisecond)

	if resp.StatusCode != 200 {
		return sigalert("AdapterHealth",
			fmt.Sprintf("HTTP %d", resp.StatusCode),
			"HTTP 200",
			fmt.Sprintf("health returned HTTP %d: %s", resp.StatusCode, shortBody(body)))
	}
	var m map[string]any
	_ = json.Unmarshal(body, &m)
	if s, _ := m["status"].(string); s != "ok" {
		return sigalert("AdapterHealth",
			fmt.Sprintf("status=%q", s),
			`status="ok"`,
			fmt.Sprintf("health check status=%q (took %s)", s, elapsed))
	}
	return normal("AdapterHealth", fmt.Sprintf("HTTP 200 (%s)", elapsed), "HTTP 200")
}

// checkTunnelPort checks whether the SSH tunnel is listening locally.
// Always checks localhost regardless of MetricRunner — the tunnel is
// always on the local machine, even when --remote is set.
func checkTunnelPort(_ MetricRunner, cfg Config) MetricSignal {
	local := LocalRunner{}
	baseline := fmt.Sprintf("localhost:%d listening", cfg.TunnelPort)
	if local.TCPCheck("127.0.0.1", cfg.TunnelPort) {
		return normal("TunnelPort",
			fmt.Sprintf("localhost:%d open", cfg.TunnelPort),
			baseline)
	}
	return sigalert("TunnelPort",
		fmt.Sprintf("localhost:%d closed", cfg.TunnelPort),
		baseline,
		fmt.Sprintf("SSH tunnel not listening on port %d — run: raptor tunnel --remote %s",
			cfg.TunnelPort, cfg.Remote))
}

// checkAdapterLatency times a GET to the health endpoint.
// Warn if > LatencyWarn, alert if > LatencyCrit.
func checkAdapterLatency(_ MetricRunner, cfg Config) MetricSignal {
	url := strings.TrimRight(cfg.AdapterURL, "/") + cfg.HealthPath
	start := time.Now()
	resp, err := httpGET(url, cfg.LatencyCrit+2*time.Second)
	elapsed := time.Since(start).Round(time.Millisecond)
	if err != nil {
		return sigerr("AdapterLatency", "request failed: "+shortErr(err))
	}
	resp.Body.Close()

	baseline := fmt.Sprintf("< %s", cfg.LatencyWarn)
	value := elapsed.String()
	if elapsed > cfg.LatencyCrit {
		return sigalert("AdapterLatency", value, baseline,
			fmt.Sprintf("response took %s — exceeded critical threshold %s", value, cfg.LatencyCrit))
	}
	if elapsed > cfg.LatencyWarn {
		return sigwarn("AdapterLatency", value, baseline,
			fmt.Sprintf("response took %s — exceeded warning threshold %s", value, cfg.LatencyWarn))
	}
	return normal("AdapterLatency", value, baseline)
}

// checkContainerRunning checks that the Docker container is in "running" state.
// Uses MetricRunner so it works both locally and over SSH.
func checkContainerRunning(run MetricRunner, cfg Config) MetricSignal {
	status, err := run.DockerInspect(cfg.Container, "{{.State.Status}}")
	if err != nil {
		return sigerr("ContainerStatus",
			fmt.Sprintf("docker inspect failed for %s on %s: %s",
				cfg.Container, run.Target(), shortErr(err)))
	}
	if status != "running" {
		return sigalert("ContainerStatus",
			fmt.Sprintf("status=%s", status),
			"status=running",
			fmt.Sprintf("container %s is %q on %s", cfg.Container, status, run.Target()))
	}
	return normal("ContainerStatus", "running", "running")
}

// checkBridgePort fetches the container's bridge IP then TCP-checks BridgePort.
// Uses MetricRunner so it works both locally and over SSH.
func checkBridgePort(run MetricRunner, cfg Config) MetricSignal {
	ip, err := run.DockerInspect(cfg.Container,
		"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}")
	if err != nil || ip == "" {
		return sigerr("BridgePort",
			"cannot get container bridge IP: "+shortErr(err))
	}
	baseline := fmt.Sprintf("%s:%d reachable", ip, cfg.BridgePort)
	if run.TCPCheck(ip, cfg.BridgePort) {
		return normal("BridgePort", baseline, baseline)
	}
	return sigalert("BridgePort",
		fmt.Sprintf("%s:%d unreachable", ip, cfg.BridgePort),
		baseline,
		fmt.Sprintf("socat bridge not running at %s:%d — run: raptor fix --remote %s",
			ip, cfg.BridgePort, cfg.Remote))
}

// checkUpstreamRoute sends a minimal POST to the adapter's completions endpoint
// and inspects the "source" field. source=local_fallback means upstream is down.
// Uses max_tokens:1 to minimise cost.
func checkUpstreamRoute(_ MetricRunner, cfg Config) MetricSignal {
	url := strings.TrimRight(cfg.AdapterURL, "/") + cfg.RoutePath
	payload := []byte(`{"model":"openclaw:main","messages":[{"role":"user","content":"ping"}],"max_tokens":1}`)

	resp, err := httpPOST(url, payload, 20*time.Second)
	if err != nil {
		return sigerr("UpstreamRoute", "request failed: "+shortErr(err))
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)

	if resp.StatusCode != 200 {
		return sigalert("UpstreamRoute",
			fmt.Sprintf("HTTP %d", resp.StatusCode),
			"HTTP 200",
			fmt.Sprintf("adapter returned HTTP %d: %s", resp.StatusCode, shortBody(body)))
	}
	var m map[string]any
	_ = json.Unmarshal(body, &m)
	source, _ := m["source"].(string)
	if source == "local_fallback" || source == "" {
		return sigalert("UpstreamRoute",
			"source=local_fallback",
			"source=openclaw_*",
			"adapter is not reaching upstream — run: raptor diagnose")
	}
	return normal("UpstreamRoute", "source="+source, "source=openclaw_*")
}

// ── HTTP helpers ──────────────────────────────────────────────────────────────

func httpGET(url string, timeout time.Duration) (*http.Response, error) {
	client := &http.Client{Timeout: timeout}
	return client.Get(url)
}

func httpPOST(url string, body []byte, timeout time.Duration) (*http.Response, error) {
	client := &http.Client{Timeout: timeout}
	return client.Post(url, "application/json", bytes.NewReader(body))
}

func shortErr(err error) string {
	if err == nil {
		return ""
	}
	s := err.Error()
	if len(s) > 80 {
		return s[:80] + "..."
	}
	return s
}

func shortBody(b []byte) string {
	if len(b) > 60 {
		return string(b[:60]) + "..."
	}
	return string(b)
}
