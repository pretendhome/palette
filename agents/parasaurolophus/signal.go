package main

import (
	"crypto/rand"
	"encoding/json"
	"fmt"
	"os"
	"sync"
	"time"

	core "github.com/pretendhome/palette/core"
)

// runAll executes every metric in metricChain concurrently and returns the
// collected signals. Goroutine-per-metric is the natural Go expression of
// Para's core job: watch everything in parallel, emit signals independently.
func runAll(run MetricRunner, cfg Config) []MetricSignal {
	sigs := make([]MetricSignal, len(metricChain))
	var wg sync.WaitGroup
	for i, m := range metricChain {
		wg.Add(1)
		go func(i int, fn MetricFunc) {
			defer wg.Done()
			sigs[i] = fn(run, cfg)
		}(i, m.Fn)
	}
	wg.Wait()
	return sigs
}

// toPacket converts an alerting MetricSignal into a HandoffPacket.
// Para never decides what to do with the signal — it just packages and routes.
func toPacket(sig MetricSignal, cfg Config) core.HandoffPacket {
	return core.HandoffPacket{
		ID:      newUUID(),
		TraceID: cfg.TraceID,
		From:    core.AgentPara,
		To:      sig.RouteTo,
		Task: fmt.Sprintf("SIGNAL DETECTED [%s] %s — %s",
			sig.Status, sig.Name, sig.Detail),
		Constraints: []string{
			"diagnose root cause only",
			"do not expand scope",
			"report fix mode back to orchestrator",
		},
		Payload: map[string]any{
			"metric":   sig.Name,
			"status":   sig.Status.String(),
			"value":    sig.Value,
			"baseline": sig.Baseline,
			"detail":   sig.Detail,
		},
		Timestamp: time.Now(),
	}
}

// emitPacket writes a HandoffPacket as a single NDJSON line to stderr.
// Stderr keeps machine-readable packets separate from human-readable output.
func emitPacket(pkt core.HandoffPacket) {
	b, _ := json.Marshal(pkt)
	fmt.Fprintln(os.Stderr, string(b))
}

// watchLoop runs a monitoring cycle on every tick until the process is stopped.
// It runs immediately on start, then repeats on cfg.Interval.
func watchLoop(run MetricRunner, cfg Config) {
	fmt.Printf("Watching %d metrics every %s  (trace=%s)\n\n",
		len(metricChain), cfg.Interval, cfg.TraceID)

	runCycle(run, cfg)

	ticker := time.NewTicker(cfg.Interval)
	defer ticker.Stop()
	for range ticker.C {
		runCycle(run, cfg)
	}
}

// runCycle executes one full monitoring pass, prints results, and emits
// HandoffPackets for any non-normal signals when cfg.JSONOut is set.
func runCycle(run MetricRunner, cfg Config) {
	sigs := runAll(run, cfg)

	fmt.Printf("[%s]\n", time.Now().Format("15:04:05"))
	anyAlert := false
	for _, sig := range sigs {
		printSignalLine(sig, cfg.Verbose)
		if sig.Status != SignalNormal {
			anyAlert = true
			if cfg.JSONOut && sig.RouteTo != "" {
				emitPacket(toPacket(sig, cfg))
			}
		}
	}
	if !anyAlert {
		fmt.Println("  ✓ all metrics normal")
	}
	fmt.Println()
}

// printReport emits all alerting signals as indented JSON HandoffPackets.
func printReport(sigs []MetricSignal, cfg Config) {
	reported := 0
	for _, sig := range sigs {
		if sig.Status == SignalNormal {
			continue
		}
		pkt := toPacket(sig, cfg)
		b, _ := json.MarshalIndent(pkt, "", "  ")
		fmt.Println(string(b))
		reported++
	}
	if reported == 0 {
		fmt.Println(`{"note":"all metrics normal — no packets to emit"}`)
	}
}

// newUUID generates a random UUID v4.
func newUUID() string {
	b := make([]byte, 16)
	_, _ = rand.Read(b)
	b[6] = (b[6] & 0x0f) | 0x40 // version 4
	b[8] = (b[8] & 0x3f) | 0x80 // variant
	return fmt.Sprintf("%08x-%04x-%04x-%04x-%012x",
		b[0:4], b[4:6], b[6:8], b[8:10], b[10:16])
}
