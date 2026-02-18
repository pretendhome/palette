package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"
)

// ─── Probe types ──────────────────────────────────────────────────────────────

type ProbeStatus int

const (
	ProbePass ProbeStatus = iota
	ProbeFail
)

// ProbeResult is the output of a single probe layer.
type ProbeResult struct {
	Name      string
	Status    ProbeStatus
	Detail    string
	RootCause bool   // true when this probe identified the definitive root cause
	FixMode   string // "bridge" | "tunnel" | "env" | "restart" | "external" | "manual"
}

func pass(name, detail string) ProbeResult {
	return ProbeResult{Name: name, Status: ProbePass, Detail: detail}
}

func fail(name, detail, fixMode string) ProbeResult {
	return ProbeResult{Name: name, Status: ProbeFail, Detail: detail, FixMode: fixMode}
}

func root(name, detail, fixMode string) ProbeResult {
	return ProbeResult{Name: name, Status: ProbeFail, Detail: detail, RootCause: true, FixMode: fixMode}
}

// ProbeFunc is the signature all probe implementations must satisfy.
// Accepting Runner makes probes location-agnostic: the same probe works
// whether the container is local or on a remote VPS.
type ProbeFunc func(run Runner, cfg Config) ProbeResult

// ─── Probe implementations ────────────────────────────────────────────────────
// Probes that check the LOCAL adapter (AdapterHealth, AdapterRoute, UpstreamURL)
// make direct HTTP calls — Runner is not needed and is ignored.
//
// Probes that check the CONTAINER (ContainerRunning, ServicePortOpen,
// BindAddress, BridgePort) delegate to Runner so they work both locally
// and over SSH without any branching inside the probe itself.

func probeAdapterHealth(run Runner, cfg Config) ProbeResult {
	url := strings.TrimRight(cfg.AdapterURL, "/") + cfg.HealthPath
	code, body, err := httpGET(url, "", 5*time.Second)
	if err != nil {
		return fail("AdapterHealth", "not reachable: "+shortErr(err), "restart")
	}
	if code != 200 {
		return fail("AdapterHealth", fmt.Sprintf("HTTP %d", code), "restart")
	}
	var m map[string]interface{}
	_ = json.Unmarshal(body, &m)
	if s, ok := m["status"].(string); ok && s == "ok" {
		return pass("AdapterHealth", "ok")
	}
	return fail("AdapterHealth", clampStr(body, 80), "restart")
}

func probeAdapterRoute(run Runner, cfg Config) ProbeResult {
	url := strings.TrimRight(cfg.AdapterURL, "/") + cfg.RoutePath
	code, body, err := httpPOST(url, "", []byte(cfg.RoutePayload), 30*time.Second)
	if err != nil {
		return fail("AdapterRoute", "request failed: "+shortErr(err), "")
	}
	if code != 200 {
		return fail("AdapterRoute", fmt.Sprintf("HTTP %d", code), "")
	}
	var m map[string]interface{}
	_ = json.Unmarshal(body, &m)
	source, _ := m["source"].(string)
	if source == "local_fallback" || source == "" {
		return fail("AdapterRoute", "source=local_fallback — upstream not reached", "")
	}
	return pass("AdapterRoute", "source="+source+" ✓")
}

// probeUpstreamURL checks whether the configured upstream URL is reachable
// by TCP-connecting and then POSTing to the API path.
// Any JSON response (200, 400, 401, 422) means the API endpoint is live.
func probeUpstreamURL(run Runner, cfg Config) ProbeResult {
	if cfg.UpstreamURL == "" {
		return fail("UpstreamURL", "upstream URL not configured", "env")
	}

	u, err := url.Parse(cfg.UpstreamURL)
	if err != nil {
		return fail("UpstreamURL", "invalid URL: "+err.Error(), "env")
	}
	host := u.Hostname()
	port := 80
	if p := u.Port(); p != "" {
		fmt.Sscanf(p, "%d", &port)
	} else if u.Scheme == "https" {
		port = 443
	}

	// TCP check from local machine — the upstream URL is what the local adapter uses.
	if !NewLocalRunner(false).TCPCheck(host, port) {
		return fail("UpstreamURL", fmt.Sprintf("TCP connect failed to %s:%d", host, port), "tunnel")
	}

	// API probe — accept any JSON response as "reachable"
	apiURL := strings.TrimRight(cfg.UpstreamURL, "/") + cfg.APIPath
	code, body, err := httpPOST(apiURL, cfg.UpstreamToken, probePayload(cfg), 15*time.Second)
	if err != nil {
		return fail("UpstreamURL", "TCP ok but HTTP failed: "+shortErr(err), "")
	}
	if isJSONResponse(code, body) {
		return pass("UpstreamURL", fmt.Sprintf("API reachable — HTTP %d", code))
	}
	return fail("UpstreamURL",
		fmt.Sprintf("HTTP %d but response is not JSON (got HTML?) — wrong API path or port", code), "")
}

func probeContainerRunning(run Runner, cfg Config) ProbeResult {
	status, err := run.DockerInspect(cfg.Container, "{{.State.Status}}")
	if err != nil || status != "running" {
		return fail("ContainerRunning",
			fmt.Sprintf("%s not running on %s (status=%q)", cfg.Container, run.Target(), status),
			"external")
	}
	return pass("ContainerRunning", fmt.Sprintf("running on %s", run.Target()))
}

// probeServicePortOpen checks if the service port is open inside the container.
// Uses bash /dev/tcp — a TCP check that needs no extra tools inside the container.
func probeServicePortOpen(run Runner, cfg Config) ProbeResult {
	cmd := fmt.Sprintf(
		"(echo > /dev/tcp/127.0.0.1/%d) 2>/dev/null && echo open || echo closed",
		cfg.ServicePort)
	out, err := run.DockerExec(cfg.Container, cmd)
	if err != nil {
		return fail("ServicePortOpen", "docker exec failed: "+shortErr(err), "external")
	}
	if strings.TrimSpace(out) != "open" {
		return fail("ServicePortOpen",
			fmt.Sprintf("port %d not open inside container", cfg.ServicePort), "external")
	}
	return pass("ServicePortOpen", fmt.Sprintf("port %d open inside container", cfg.ServicePort))
}

// probeBindAddress is the root-cause probe for the Docker loopback binding problem.
// It checks whether the service bound to 127.0.0.1 (unreachable via bridge)
// or 0.0.0.0 (reachable). Uses ss inside the container first; falls back to logs.
func probeBindAddress(run Runner, cfg Config) ProbeResult {
	ssCmd := fmt.Sprintf("ss -tlnp 2>/dev/null | grep ':%d' || true", cfg.ServicePort)
	ssOut, _ := run.DockerExec(cfg.Container, ssCmd)

	if strings.Contains(ssOut, "127.0.0.1") {
		return root("BindAddress",
			fmt.Sprintf("service bound to 127.0.0.1:%d — container loopback only, Docker bridge cannot reach this",
				cfg.ServicePort),
			"bridge")
	}
	if strings.Contains(ssOut, "0.0.0.0") || strings.Contains(ssOut, "*:") {
		return pass("BindAddress", "bound to 0.0.0.0 — Docker bridge can reach this")
	}

	// ss gave no useful output — fall back to log inspection
	logs, _ := run.DockerLogs(cfg.Container, 100)
	loopSig := fmt.Sprintf("127.0.0.1:%d", cfg.ServicePort)
	pubSig := fmt.Sprintf("0.0.0.0:%d", cfg.ServicePort)

	if strings.Contains(logs, loopSig) {
		return root("BindAddress",
			fmt.Sprintf("logs confirm 127.0.0.1:%d binding — Docker bridge unreachable", cfg.ServicePort),
			"bridge")
	}
	if strings.Contains(logs, pubSig) {
		return pass("BindAddress", "logs show 0.0.0.0 binding — Docker bridge accessible")
	}
	return fail("BindAddress", "cannot determine bind address — check ss and logs manually", "manual")
}

// probeBridgePort checks whether the socat bridge is already active.
// It gets the container's bridge IP via docker inspect, then tests TCP
// connectivity to BridgePort from whatever host the Runner targets.
func probeBridgePort(run Runner, cfg Config) ProbeResult {
	ip, err := run.DockerInspect(cfg.Container,
		"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}")
	if err != nil || ip == "" {
		return fail("BridgePort", "cannot get container bridge IP: "+shortErr(err), "")
	}
	if run.TCPCheck(ip, cfg.BridgePort) {
		return pass("BridgePort", fmt.Sprintf("socat bridge reachable at %s:%d", ip, cfg.BridgePort))
	}
	return fail("BridgePort",
		fmt.Sprintf("bridge not reachable at %s:%d — not created yet", ip, cfg.BridgePort),
		"bridge")
}

// ─── Probe chain ──────────────────────────────────────────────────────────────
// The chain is a plain slice. To add a new probe: append it here.
// Order matters — the engine descends until it finds the root cause.

var probeChain = []ProbeFunc{
	probeAdapterHealth,    // 1. Is the local adapter alive?
	probeAdapterRoute,     // 2. Does a route call succeed? (pass = no problem)
	probeUpstreamURL,      // 3. Is the upstream URL reachable? (pass = env/config issue)
	probeContainerRunning, // 4. Is the container running?
	probeServicePortOpen,  // 5. Is the service port open inside the container?
	probeBindAddress,      // 6. Is the service bound to loopback? (root cause here for Hostinger)
	probeBridgePort,       // 7. Is the socat bridge already active?
}

// ─── Diagnosis engine ─────────────────────────────────────────────────────────

type Diagnosis struct {
	Results   []ProbeResult
	RootCause string
	FixMode   string
	FixReady  bool
}

// diagnose runs the probe chain in order. Each probe either:
//   - passes and the chain continues (normal gate)
//   - passes and the chain stops (AdapterRoute/UpstreamURL — different issue class)
//   - fails and the chain stops (root cause or fix boundary reached)
//
// The chain rules are expressed here rather than inside each ProbeFunc, keeping
// probes themselves stateless and reusable in isolation.
func diagnose(run Runner, cfg Config) Diagnosis {
	d := Diagnosis{}
	emit := func(r ProbeResult) ProbeResult {
		d.Results = append(d.Results, r)
		return r
	}

	for i, probe := range probeChain {
		r := emit(probe(run, cfg))

		switch i {
		case 0: // AdapterHealth — fail = stop
			if r.Status == ProbeFail {
				d.RootCause = "Adapter not running. Start: node --env-file=.env.production server.mjs"
				d.FixMode = "restart"
				return d
			}

		case 1: // AdapterRoute — pass = already working, stop
			if r.Status == ProbePass {
				d.RootCause = "no problem — upstream reachable and routing correctly"
				return d
			}

		case 2: // UpstreamURL — pass = URL works but adapter not using it
			if r.Status == ProbePass {
				d.RootCause = "Upstream URL is reachable but adapter returned local_fallback. " +
					"Check OPENCLAW_UPSTREAM_MODE and restart adapter."
				d.FixMode = "env"
				return d
			}

		case 3, 4: // ContainerRunning, ServicePortOpen — fail = stop, external issue
			if r.Status == ProbeFail {
				d.RootCause = r.Detail
				d.FixMode = r.FixMode
				return d
			}

		case 5: // BindAddress — root cause probe
			if r.RootCause {
				d.RootCause = r.Detail
				d.FixMode = "bridge"
				d.FixReady = true
				return d
			}

		case 6: // BridgePort — fail = bridge needed, pass = env mismatch
			if r.Status == ProbeFail {
				d.RootCause = r.Detail
				d.FixMode = "bridge"
				d.FixReady = true
				return d
			}
			// Bridge exists but adapter not using it
			ip, _ := run.DockerInspect(cfg.Container,
				"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}")
			d.RootCause = fmt.Sprintf(
				"Bridge active at %s:%d but upstream URL not pointing to it. "+
					"Update OPENCLAW_BASE_URL=http://127.0.0.1:%d/ and restart adapter.",
				ip, cfg.BridgePort, cfg.TunnelPort)
			d.FixMode = "env"
			return d
		}
	}
	return d
}

// ─── HTTP helpers (used by probes) ───────────────────────────────────────────

func httpGET(url, token string, timeout time.Duration) (int, []byte, error) {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()
	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return 0, nil, err
	}
	if token != "" {
		req.Header.Set("Authorization", "Bearer "+token)
	}
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return 0, nil, err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return resp.StatusCode, body, nil
}

func httpPOST(url, token string, payload []byte, timeout time.Duration) (int, []byte, error) {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()
	req, err := http.NewRequestWithContext(ctx, "POST", url, bytes.NewReader(payload))
	if err != nil {
		return 0, nil, err
	}
	req.Header.Set("Content-Type", "application/json")
	if token != "" {
		req.Header.Set("Authorization", "Bearer "+token)
	}
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return 0, nil, err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return resp.StatusCode, body, nil
}

// isJSONResponse returns true when the response looks like an API JSON payload.
// 200, 400, 401, 422 all indicate a live API endpoint even if credentials fail.
func isJSONResponse(code int, body []byte) bool {
	switch code {
	case 200, 400, 401, 422:
		s := strings.TrimSpace(string(body))
		return strings.HasPrefix(s, "{") || strings.HasPrefix(s, "[")
	}
	return false
}
