(function () {
  const CONFIG = {
    apiBase: (window.MISSIONCANVAS_CONFIG && window.MISSIONCANVAS_CONFIG.apiBase) || "",
    routePath: "/v1/missioncanvas/route",
    streamPath: "/v1/missioncanvas/talk-stream",
    confirmPath: "/v1/missioncanvas/confirm-one-way-door",
    logAppendPath: "/v1/missioncanvas/log-append",
    commitPath: "/v1/missioncanvas/commit",
    uncommitPath: "/v1/missioncanvas/uncommit",
    workspaceId: window.WORKSPACE_ID || null
  };

  const STATE = {
    transcript: "",
    structured: {
      objective: "",
      context: "",
      desired_outcome: "",
      constraints: ""
    },
    lastResponse: null,
    lastRequestId: null,
    lastOneWayItems: [],
    lastBrief: "",
    lastDecisionLogPayload: "",
    activePersona: null,
    currentMode: "explore",
    convergenceScore: 0,
    committedRoute: null,
    workspaceWelcome: null
  };

  // ── Legacy client-side project state (non-workspace flow only) ──
  const PROJECT_STATE_KEY = "missioncanvas_project_state";
  const SESSION_KEY = CONFIG.workspaceId
    ? `missioncanvas_session_${CONFIG.workspaceId}`
    : "missioncanvas_session_default";

  function loadProjectState() {
    if (CONFIG.workspaceId) return null;
    try {
      const raw = localStorage.getItem(PROJECT_STATE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch { return null; }
  }

  function saveProjectState(update) {
    if (CONFIG.workspaceId) return null;
    const existing = loadProjectState() || {
      id: "session-" + Date.now(),
      created_at: new Date().toISOString(),
      known_facts: [],
      route_history: [],
      decisions_made: [],
      convergence_high_water: 0
    };
    // Merge update into existing
    if (update.known_fact && !existing.known_facts.includes(update.known_fact)) {
      existing.known_facts.push(update.known_fact);
    }
    if (update.route) {
      existing.route_history.push({
        riu_id: update.route.riu_id,
        name: update.route.name,
        mode: update.mode,
        score: update.convergence_score,
        timestamp: new Date().toISOString()
      });
      // Cap at 50 entries
      if (existing.route_history.length > 50) existing.route_history.shift();
    }
    if (update.decision) {
      existing.decisions_made.push({
        ...update.decision,
        timestamp: new Date().toISOString()
      });
    }
    if (update.convergence_score > existing.convergence_high_water) {
      existing.convergence_high_water = update.convergence_score;
    }
    existing.last_mode = update.mode || existing.last_mode;
    existing.last_updated = new Date().toISOString();
    existing.persona = STATE.activePersona || existing.persona;
    localStorage.setItem(PROJECT_STATE_KEY, JSON.stringify(existing));
    return existing;
  }

  function getProjectSummary() {
    if (CONFIG.workspaceId) return null;
    const ps = loadProjectState();
    if (!ps) return null;
    return {
      routes_explored: ps.route_history.length,
      facts_known: ps.known_facts.length,
      decisions_made: ps.decisions_made.length,
      high_water_score: ps.convergence_high_water,
      last_mode: ps.last_mode,
      last_updated: ps.last_updated,
      persona: ps.persona
    };
  }

  function clearProjectState() {
    if (CONFIG.workspaceId) return;
    localStorage.removeItem(PROJECT_STATE_KEY);
  }

  function getSessionId() {
    try {
      var existing = sessionStorage.getItem(SESSION_KEY);
      if (existing) return existing;
      var sessionId = (crypto.randomUUID ? crypto.randomUUID() : String(Date.now())) +
        (CONFIG.workspaceId ? `-${CONFIG.workspaceId}` : "");
      sessionStorage.setItem(SESSION_KEY, sessionId);
      return sessionId;
    } catch (_err) {
      return CONFIG.workspaceId ? `workspace-session-${CONFIG.workspaceId}` : "missioncanvas-web-session";
    }
  }

  function prefillWorkspaceQuery(query) {
    if (refs.queryInput) refs.queryInput.value = query;
  }

  const $ = (id) => document.getElementById(id);

  const refs = {
    btnHealth: $("btnHealth"),
    systemStatus: $("systemStatus"),
    btnVoiceStart: $("btnVoiceStart"),
    btnVoiceStop: $("btnVoiceStop"),
    voiceState: $("voiceState"),
    transcriptInput: $("transcriptInput"),
    btnTranslate: $("btnTranslate"),
    translateConfidence: $("translateConfidence"),
    tObjective: $("tObjective"),
    tContext: $("tContext"),
    tOutcome: $("tOutcome"),
    tConstraints: $("tConstraints"),
    tRiskPosture: $("tRiskPosture"),
    tUserRole: $("tUserRole"),
    btnRoute: $("btnRoute"),
    btnStream: $("btnStream"),
    manualInput: $("manualInput"),
    btnManualTranslate: $("btnManualTranslate"),
    resultStatus: $("resultStatus"),
    rSource: $("rSource"),
    rStatus: $("rStatus"),
    rRiu: $("rRiu"),
    rAgent: $("rAgent"),
    rArtifact: $("rArtifact"),
    rAction: $("rAction"),
    briefOutput: $("briefOutput"),
    btnSpeak: $("btnSpeak"),
    btnCopy: $("btnCopy"),
    btnConfirmOwd: $("btnConfirmOwd"),
    btnAppendLog: $("btnAppendLog"),
    autoLog: $("autoLog"),
    followupInput: $("followupInput"),
    btnRefine: $("btnRefine"),
    personaChips: Array.from(document.querySelectorAll(".persona-chip")),
    personaHint: $("personaHint"),
    personaChecklist: $("personaChecklist"),
    translationNotes: $("translationNotes"),
    qualityChecks: $("qualityChecks"),
    presetChips: Array.from(document.querySelectorAll(".preset-chip")),
    streamBox: $("streamBox"),
    streamOutput: $("streamOutput"),
    modeBadge: $("modeBadge"),
    modeContent: $("modeContent"),
    projectCheckin: $("projectCheckin"),
    liveMeter: $("liveMeterFill"),
    liveScore: $("liveScore"),
    liveHint: $("liveHint"),
    queryPanel: $("queryPanel"),
    queryInput: $("queryInput"),
    btnQuery: $("btnQuery"),
    btnCommit: $("btnCommit"),
    btnUncommit: $("btnUncommit"),
    commitBanner: $("commitBanner")
  };

  const PERSONAS = {
    mythfall: {
      name: "Game Builder",
      hint: "Prioritize scope clarity, build sequencing, and fast test loops.",
      checklist: [
        "Name the core game loop and target player.",
        "Set a 2-week playable milestone.",
        "Constrain features to MVP."
      ],
      defaults: {
        context: "Indie game project with limited team capacity.",
        constraints: "Time-constrained, budget-sensitive, MVP-first."
      }
    },
    rossi: {
      name: "Business Owner",
      hint: "Prioritize revenue, operations, and execution constraints.",
      checklist: [
        "Define revenue target and timeline.",
        "Include budget and staffing constraints.",
        "Identify first operating artifact to build."
      ],
      defaults: {
        context: "Owner-operator business environment with active customers.",
        constraints: "Limited budget, small team, 30-90 day horizon."
      }
    },
    scuola: {
      name: "Education",
      hint: "Prioritize student outcomes, educator workflow, and policy constraints.",
      checklist: [
        "State learner/teacher outcome clearly.",
        "Include implementation and training constraints.",
        "Include compliance or governance needs."
      ],
      defaults: {
        context: "Education setting with multiple stakeholders and approval gates.",
        constraints: "Policy-sensitive, adoption-risk managed."
      }
    },
    job: {
      name: "Job Seeker",
      hint: "Prioritize positioning, proof, and targeted outreach.",
      checklist: [
        "Define target role and timeline.",
        "Specify strengths and evidence to highlight.",
        "Set weekly cadence for applications/networking."
      ],
      defaults: {
        context: "Active career transition with existing resume/work history.",
        constraints: "Time-boxed outreach and interview prep."
      }
    },
    exec: {
      name: "Enterprise AI Operator",
      hint: "Prioritize reversible decisions, ROI, and stakeholder alignment.",
      checklist: [
        "State pilot objective and success metric.",
        "Define risk tolerance and one-way-door conditions.",
        "Name the first decision artifact."
      ],
      defaults: {
        context: "Cross-functional initiative requiring decision quality and speed.",
        constraints: "High-visibility outcomes, governance expectations."
      }
    }
  };

  function setSystemStatus(message, level = "warn") {
    if (!refs.systemStatus) return;
    refs.systemStatus.textContent = `System status: ${message}`;
    refs.systemStatus.classList.remove("ok", "warn", "error");
    refs.systemStatus.classList.add(level);
  }

  function renderList(el, items) {
    if (!el) return;
    el.textContent = "";
    items.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      el.appendChild(li);
    });
  }

  function applyPersona(personaId) {
    const persona = PERSONAS[personaId];
    if (!persona) return;

    STATE.activePersona = personaId;
    refs.personaChips.forEach((chip) => {
      chip.classList.toggle("active", chip.getAttribute("data-persona") === personaId);
    });

    refs.personaHint.textContent = `${persona.name}: ${persona.hint}`;
    renderList(refs.personaChecklist, persona.checklist);

    if (!refs.tContext.value.trim() && persona.defaults.context) refs.tContext.value = persona.defaults.context;
    if (!refs.tConstraints.value.trim() && persona.defaults.constraints) refs.tConstraints.value = persona.defaults.constraints;
    setSystemStatus(`persona selected: ${persona.name}`, "ok");
    updateLiveConvergence();
  }

  // ── Client-side convergence scoring (mirrors server computeConvergenceScore) ──
  function computeConvergenceLocal(structured) {
    let score = 0;
    const fieldScores = {};

    if (structured.objective && structured.objective.trim()) {
      score += 40;
      fieldScores.objective = 40;
    } else {
      fieldScores.objective = 0;
    }
    if (structured.desired_outcome && structured.desired_outcome.trim()) {
      score += 30;
      fieldScores.desired_outcome = 30;
    } else {
      fieldScores.desired_outcome = 0;
    }
    if (structured.context && structured.context.trim()) {
      score += 15;
      fieldScores.context = 15;
    } else {
      fieldScores.context = 0;
    }
    if (structured.constraints && structured.constraints.trim()) {
      score += 10;
      fieldScores.constraints = 10;
    } else {
      fieldScores.constraints = 0;
    }
    if (STATE.activePersona) {
      score += 5;
      fieldScores.persona = 5;
    } else {
      fieldScores.persona = 0;
    }

    const mode = score < 50 ? "explore" : "converge";
    return { score, mode, fieldScores };
  }

  function updateLiveConvergence() {
    const structured = readStructuredPrompt();
    const { score, mode, fieldScores } = computeConvergenceLocal(structured);

    STATE.currentMode = mode;
    STATE.convergenceScore = score;

    // Update the live meter
    if (refs.liveMeter) {
      refs.liveMeter.style.width = score + "%";
      refs.liveMeter.className = "live-meter-fill mode-" + mode;
    }
    if (refs.liveScore) {
      refs.liveScore.textContent = mode.toUpperCase() + " " + score + "/100";
      refs.liveScore.className = "live-score mode-" + mode;
    }

    // Update field-level hints
    var hints = [];
    if (!fieldScores.objective) hints.push("Objective (+40)");
    if (!fieldScores.desired_outcome) hints.push("Desired outcome (+30)");
    if (!fieldScores.context) hints.push("Context (+15)");
    if (!fieldScores.constraints) hints.push("Constraints (+10)");
    if (!fieldScores.persona) hints.push("Persona (+5)");

    if (refs.liveHint) {
      if (hints.length === 0) {
        refs.liveHint.textContent = "Ready to route. All fields filled.";
      } else if (mode === "explore") {
        refs.liveHint.textContent = "Add " + hints[0] + " to move toward CONVERGE";
      } else {
        refs.liveHint.textContent = "Remaining: " + hints.join(", ");
      }
    }
  }

  function evaluatePromptQuality(structured) {
    const checks = [];
    if (structured.objective) checks.push("Objective is clear.");
    else checks.push("Add a clear objective.");

    if (structured.context) checks.push("Context is present.");
    else checks.push("Add current context.");

    if (structured.desired_outcome) checks.push("Desired outcome is specified.");
    else checks.push("Add a measurable desired outcome.");

    if (structured.constraints) checks.push("Constraints are specified.");
    else checks.push("Add at least one key constraint (time, budget, risk).");

    if (STATE.activePersona) {
      checks.push(`Persona in use: ${PERSONAS[STATE.activePersona].name}.`);
    } else {
      checks.push("Select a persona for better routing defaults.");
    }
    return checks;
  }

  async function checkConnection() {
    const url = `${CONFIG.apiBase}/v1/missioncanvas/health`;
    try {
      const res = await fetch(url, { method: "GET" });
      if (res.ok) {
        setSystemStatus("health endpoint reachable", "ok");
      } else if (res.status === 404) {
        setSystemStatus("server reachable (no /health endpoint)", "ok");
      } else {
        setSystemStatus(`health check returned ${res.status}`, "warn");
      }
    } catch (_err) {
      setSystemStatus("health endpoint unreachable", "error");
    }
  }

  function splitSentences(text) {
    return String(text || "")
      .split(/(?<=[.!?])\s+|\n+/)
      .map((s) => s.trim())
      .filter(Boolean);
  }

  function firstNonEmpty(arr) {
    for (const item of arr) {
      if (item && String(item).trim()) return String(item).trim();
    }
    return "";
  }

  function findSentence(sentences, patterns) {
    for (const s of sentences) {
      const lower = s.toLowerCase();
      if (patterns.some((p) => lower.includes(p))) return s;
    }
    return "";
  }

  function mergeUnique(parts) {
    return [...new Set(parts.filter(Boolean).map((x) => x.trim()))].join(" ");
  }

  // Translation layer: convert natural speech into structured mission prompt.
  function translateNaturalInput(rawText, prior = null) {
    const text = String(rawText || "").trim();
    const sentences = splitSentences(text);

    const objective = firstNonEmpty([
      findSentence(sentences, ["i need", "i want", "help me", "build", "create", "plan", "figure out"]),
      sentences[0],
      prior?.objective
    ]);

    const context = firstNonEmpty([
      findSentence(sentences, ["currently", "today", "right now", "already", "we have", "so far", "existing"]),
      prior?.context
    ]);

    const desiredOutcome = firstNonEmpty([
      findSentence(sentences, ["so that", "goal", "outcome", "by", "within", "end state", "in "]),
      prior?.desired_outcome
    ]);

    const constraints = mergeUnique([
      findSentence(sentences, ["budget", "deadline", "time", "limited", "cannot", "can't", "risk", "team", "constraint"]),
      prior?.constraints
    ]);

    let confidence = 40;
    if (objective) confidence += 25;
    if (context) confidence += 10;
    if (desiredOutcome) confidence += 15;
    if (constraints) confidence += 10;

    const notes = [];
    if (!objective) notes.push("objective_missing");
    if (!context) notes.push("context_missing");
    if (!desiredOutcome) notes.push("outcome_missing");
    if (!constraints) notes.push("constraints_missing");
    if (STATE.activePersona) notes.push(`persona_${STATE.activePersona}`);

    return {
      objective,
      context,
      desired_outcome: desiredOutcome,
      constraints,
      confidence: Math.min(100, confidence),
      notes: notes.length ? notes.join(", ") : "complete"
    };
  }

  function renderStructuredPrompt(data) {
    refs.tObjective.value = data.objective || "";
    refs.tContext.value = data.context || "";
    refs.tOutcome.value = data.desired_outcome || "";
    refs.tConstraints.value = data.constraints || "";
    refs.translateConfidence.textContent = `Confidence: ${data.confidence || 0}%`;
    refs.translationNotes.textContent = `Translator notes: ${data.notes || "No notes."}`;

    STATE.structured = {
      objective: data.objective || "",
      context: data.context || "",
      desired_outcome: data.desired_outcome || "",
      constraints: data.constraints || ""
    };

    renderList(refs.qualityChecks, evaluatePromptQuality(STATE.structured));
    updateLiveConvergence();
  }

  function readStructuredPrompt() {
    return {
      objective: String(refs.tObjective.value || "").trim(),
      context: String(refs.tContext.value || "").trim(),
      desired_outcome: String(refs.tOutcome.value || "").trim(),
      constraints: String(refs.tConstraints.value || "").trim(),
      risk_posture: String(refs.tRiskPosture?.value || "medium").trim(),
      user_role: String(refs.tUserRole?.value || "operator").trim()
    };
  }

  function localFallbackRoute(structured) {
    const objective = structured.objective || "UNKNOWN";
    const requestId = crypto.randomUUID ? crypto.randomUUID() : String(Date.now());
    const route = /grant|fund/i.test(objective)
      ? { id: "RIU-039", name: "Funding & Grants", agent: "Argy + Theri", artifact: "Funding Pipeline" }
      : /plan|business|strategy/i.test(objective)
        ? { id: "RIU-014", name: "Business Planning & Positioning", agent: "Rex + Yuty", artifact: "Operating Plan v1" }
        : { id: "RIU-001", name: "Convergence & Scope Clarification", agent: "Yuty -> Rex", artifact: "Convergence Brief" };

    const brief = [
      "# MissionCanvas Action Brief",
      "",
      `Route: ${route.id} - ${route.name}`,
      `Primary Agent: ${route.agent}`,
      "",
      "## Input",
      `Objective: ${structured.objective || "N/A"}`,
      `Context: ${structured.context || "N/A"}`,
      `Desired Outcome: ${structured.desired_outcome || "N/A"}`,
      `Constraints: ${structured.constraints || "N/A"}`,
      "",
      "## Immediate Action",
      `Build ${route.artifact} and execute first 30-day priority set.`
    ].join("\n");

    return {
      request_id: requestId,
      source: "local_fallback",
      status: "ok",
      routing: {
        selected_rius: [{ riu_id: route.id, name: route.name, why_now: "Fallback route chosen by local translator." }],
        agent_map: [{ agent: route.agent, task: `Build ${route.artifact} and define first execution sequence.` }]
      },
      artifacts: { to_create: [route.artifact] },
      action_brief_markdown: brief,
      decision_log_payload: `Route=${route.id}; Agent=${route.agent}; OWD=false`,
      one_way_door: { detected: false, items: [] }
    };
  }

  // The standalone flow still injects local project state. Workspace mode uses server state only.
  function buildProjectStatePayload() {
    var ps = loadProjectState();
    if (!ps || !ps.known_facts.length) return null;
    return {
      known_facts: ps.known_facts,
      // Pull structured missing/decisions/blocked from bootstrap data if available
      missing_evidence: ps.missing_evidence || [],
      open_decisions: ps.open_decisions || [],
      blocked_actions: ps.blocked_actions || []
    };
  }

  async function fetchRoute(structured) {
    const endpoint = `${CONFIG.apiBase}${CONFIG.routePath}`;
    const body = {
      request_id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()),
      timestamp: new Date().toISOString(),
      session_id: getSessionId(),
      workspace_id: CONFIG.workspaceId,
      persona_id: STATE.activePersona || null,
      user: { id: "web-user", role: structured.user_role || "operator" },
      input: {
        objective: structured.objective,
        context: structured.context,
        desired_outcome: structured.desired_outcome,
        constraints: structured.constraints,
        risk_posture: structured.risk_posture || "medium"
      },
      policy: {
        enforce_convergence: true,
        enforce_one_way_gate: true,
        max_selected_rius: 5,
        require_validation_checks: true
      },
      runtime: {
        mode: "planning",
        allow_execution: false,
        tool_whitelist: ["research", "planning"],
        log_target: "implementation"
      }
    };
    if (!CONFIG.workspaceId) {
      body.project_state = buildProjectStatePayload();
    }

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setSystemStatus("proxy route success", "ok");
      return data;
    } catch (_err) {
      setSystemStatus("proxy unavailable, using local fallback", "warn");
      return localFallbackRoute(structured);
    }
  }

  async function fetchStream(structured) {
    refs.streamBox.classList.remove("hidden");
    refs.streamOutput.textContent = "";

    const endpoint = `${CONFIG.apiBase}${CONFIG.streamPath}`;
    const body = {
      request_id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()),
      timestamp: new Date().toISOString(),
      session_id: getSessionId(),
      workspace_id: CONFIG.workspaceId,
      user: { id: "web-user", role: structured.user_role || "operator" },
      input: {
        objective: structured.objective,
        context: structured.context,
        desired_outcome: structured.desired_outcome,
        constraints: structured.constraints,
        risk_posture: structured.risk_posture || "medium"
      },
      policy: {
        enforce_convergence: true,
        enforce_one_way_gate: true,
        max_selected_rius: 5,
        require_validation_checks: true
      },
      runtime: {
        mode: "planning",
        allow_execution: false,
        tool_whitelist: ["research", "planning"],
        log_target: "implementation"
      }
    };

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });

      if (!res.ok || !res.body) throw new Error("Stream unavailable");
      setSystemStatus("stream connected", "ok");

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let finalResponse = null;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.trim()) continue;
          let evt;
          try {
            evt = JSON.parse(line);
          } catch (_err) {
            continue;
          }

          if (evt.type === "chunk") {
            refs.streamOutput.textContent += evt.text;
          } else if (evt.type === "final") {
            finalResponse = evt.response;
          }
        }
      }

      if (finalResponse) renderResponse(finalResponse);
    } catch (_err) {
      setSystemStatus("stream unavailable", "warn");
      refs.streamOutput.textContent = "Streaming unavailable. Use standard route.";
    }
  }

  function renderResponse(response) {
    const selected = response?.routing?.selected_rius?.[0] || null;
    const agentMap = response?.routing?.agent_map?.[0] || null;
    const artifact = response?.artifacts?.to_create?.[0] || "-";
    const mode = response?.mode || "explore";
    const score = response?.convergence_score || 0;

    STATE.currentMode = mode;
    STATE.convergenceScore = score;

    // Update mode badge
    if (refs.modeBadge) {
      refs.modeBadge.textContent = `${mode.toUpperCase()} (${score}/100)`;
      refs.modeBadge.className = "mode-badge mode-" + mode;
    }

    refs.resultStatus.textContent = "Route complete.";
    refs.rSource.textContent = response?.source || "unknown";
    refs.rStatus.textContent = response?.status || "unknown";
    refs.rRiu.textContent = selected ? `${selected.riu_id} - ${selected.name}` : "-";
    refs.rAgent.textContent = agentMap?.agent || "-";
    refs.rArtifact.textContent = artifact;
    refs.rAction.textContent = agentMap?.task || "-";
    refs.briefOutput.value = response?.action_brief_markdown || "No brief returned.";

    STATE.lastResponse = response;
    STATE.lastRequestId = response?.request_id || null;
    STATE.lastOneWayItems = response?.one_way_door?.items || [];
    STATE.lastBrief = response?.action_brief_markdown || "";
    STATE.lastDecisionLogPayload = response?.decision_log_payload || "";

    if (window.WorkspaceUI && CONFIG.workspaceId) {
      if (response?.coaching) {
        window.WorkspaceUI.renderCoaching(response);
      } else if (response?.convergence_chain) {
        window.WorkspaceUI.renderChain(response);
      } else if (STATE.workspaceWelcome) {
        window.WorkspaceUI.renderWelcome(STATE.workspaceWelcome);
      }
    }

    // Render mode-specific content
    renderModeContent(response);
    checkExploreNudge(response);

    if (response?.status === "needs_confirmation" && STATE.lastOneWayItems.length) {
      refs.btnConfirmOwd.classList.remove("hidden");
    } else {
      refs.btnConfirmOwd.classList.add("hidden");
    }

    // Show/hide commit button based on mode
    if (refs.btnCommit) {
      // Show commit only in converge mode with score >= 70, and not already committed
      if (mode === "converge" && score >= 70 && !STATE.committedRoute) {
        refs.btnCommit.classList.remove("hidden");
      } else {
        refs.btnCommit.classList.add("hidden");
      }
    }

    // Update committed state from server response
    if (response?.session?.committed_route) {
      STATE.committedRoute = response.session.committed_route;
      renderCommitBanner();
    }

    // Save to client-side project state
    if (!CONFIG.workspaceId) {
      saveProjectState({
        mode: mode,
        convergence_score: score,
        route: selected ? { riu_id: selected.riu_id, name: selected.name } : null,
        known_fact: selected ? `Routed to ${selected.riu_id} (${selected.name})` : null
      });
    }
  }

  async function commitRoute() {
    var selected = STATE.lastResponse?.routing?.selected_rius?.[0];
    if (!selected) {
      setSystemStatus("Route first, then commit.", "warn");
      return;
    }

    var endpoint = CONFIG.apiBase + CONFIG.commitPath;
    try {
      var res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: getSessionId(),
          riu_id: selected.riu_id,
          riu_name: selected.name
        })
      });
      var data = await res.json();
      if (data.status === "committed") {
        STATE.committedRoute = data.committed_route;
        STATE.currentMode = "commit";
        renderCommitBanner();
        if (refs.btnCommit) refs.btnCommit.classList.add("hidden");
        if (refs.modeBadge) {
          refs.modeBadge.textContent = "COMMIT (locked)";
          refs.modeBadge.className = "mode-badge mode-commit";
        }
        setSystemStatus("Committed to " + selected.riu_id, "ok");
        // Record in project state
        if (!CONFIG.workspaceId) {
          saveProjectState({
            decision: { type: "commit", riu_id: selected.riu_id, name: selected.name, status: "committed" },
            mode: "commit",
            convergence_score: STATE.convergenceScore
          });
        }
      } else {
        setSystemStatus(data.message || "Cannot commit yet.", "warn");
      }
    } catch (_err) {
      setSystemStatus("Commit failed.", "error");
    }
  }

  async function uncommitRoute() {
    var endpoint = CONFIG.apiBase + CONFIG.uncommitPath;
    try {
      var res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: getSessionId() })
      });
      var data = await res.json();
      if (data.status === "uncommitted") {
        STATE.committedRoute = null;
        STATE.currentMode = "converge";
        if (refs.commitBanner) refs.commitBanner.classList.add("hidden");
        if (refs.btnUncommit) refs.btnUncommit.classList.add("hidden");
        updateLiveConvergence();
        setSystemStatus("Back to converge mode.", "ok");
      }
    } catch (_err) {
      setSystemStatus("Uncommit failed.", "error");
    }
  }

  function renderCommitBanner() {
    if (!refs.commitBanner || !STATE.committedRoute) return;
    refs.commitBanner.classList.remove("hidden");
    refs.commitBanner.textContent = "";

    var icon = document.createElement("span");
    icon.className = "commit-icon";
    icon.textContent = "COMMITTED";
    refs.commitBanner.appendChild(icon);

    var text = document.createElement("span");
    text.textContent = STATE.committedRoute.riu_id + " — " + STATE.committedRoute.name +
      " | Locked at " + (STATE.committedRoute.committed_at || "").slice(0, 16);
    refs.commitBanner.appendChild(text);

    if (refs.btnUncommit) refs.btnUncommit.classList.remove("hidden");
  }

  function renderModeContent(response) {
    const mode = response?.mode || "explore";
    const modePanel = refs.modeContent;
    if (!modePanel) return;

    modePanel.textContent = "";
    modePanel.className = "mode-content mode-" + mode;

    if (mode === "explore") {
      // Show suggested questions
      const questions = response?.suggested_questions || [];
      if (questions.length) {
        const qh = document.createElement("h4");
        qh.textContent = "To narrow down, consider:";
        modePanel.appendChild(qh);
        const ul = document.createElement("ul");
        ul.className = "mode-questions";
        for (const q of questions) {
          const li = document.createElement("li");
          li.textContent = q;
          li.className = "mode-question-item";
          li.addEventListener("click", function () {
            refs.followupInput.value = q;
            refs.followupInput.focus();
          });
          ul.appendChild(li);
        }
        modePanel.appendChild(ul);
      }

      // Show route options as selectable cards
      const options = response?.route_options || [];
      if (options.length > 1) {
        const oh = document.createElement("h4");
        oh.textContent = "Route options (" + options.length + "):";
        modePanel.appendChild(oh);
        for (const opt of options) {
          const card = document.createElement("div");
          card.className = "route-option-card";
          card.innerHTML = "";
          const title = document.createElement("strong");
          title.textContent = opt.riu_id + " " + opt.name + " [" + opt.strength + "]";
          card.appendChild(title);
          const desc = document.createElement("p");
          desc.textContent = opt.mini_brief;
          card.appendChild(desc);
          card.addEventListener("click", function () {
            refs.tObjective.value = "I want to focus on: " + opt.name;
            refs.tContext.value = refs.tContext.value || "";
            setSystemStatus("Selected " + opt.riu_id + " — refine and reroute", "ok");
          });
          modePanel.appendChild(card);
        }
      }
    }

    if (mode === "converge") {
      // Show convergence gaps as actionable checklist
      const gaps = response?.convergence_gaps || [];
      if (gaps.length) {
        const gh = document.createElement("h4");
        gh.textContent = "Fill these gaps to strengthen your mission:";
        modePanel.appendChild(gh);
        const ul = document.createElement("ul");
        ul.className = "mode-gaps";
        for (const gap of gaps) {
          const li = document.createElement("li");
          li.textContent = gap;
          li.className = "mode-gap-item";
          ul.appendChild(li);
        }
        modePanel.appendChild(ul);
      }

      // Show knowledge gaps if any
      const kGaps = response?.knowledge_gap;
      if (kGaps?.detected) {
        const kh = document.createElement("h4");
        kh.textContent = "Knowledge gaps detected:";
        modePanel.appendChild(kh);
        const ul = document.createElement("ul");
        for (const g of kGaps.what_is_missing || []) {
          const li = document.createElement("li");
          li.textContent = g;
          ul.appendChild(li);
        }
        modePanel.appendChild(ul);
      }
    }
  }

  async function appendDecisionLog() {
    if (!STATE.lastRequestId || !STATE.lastDecisionLogPayload) {
      refs.rAction.textContent = "No decision payload to append yet.";
      return;
    }

    const endpoint = `${CONFIG.apiBase}${CONFIG.logAppendPath}`;
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          request_id: STATE.lastRequestId,
          decision_log_payload: STATE.lastDecisionLogPayload,
          action_brief_markdown: STATE.lastBrief
        })
      });
      const data = await res.json();
      refs.rAction.textContent = data?.message || "Decision log appended.";
    } catch (_err) {
      refs.rAction.textContent = "Decision log append failed.";
    }
  }

  async function confirmOneWayDoor() {
    if (!STATE.lastRequestId || !STATE.lastOneWayItems.length) return;

    const endpoint = `${CONFIG.apiBase}${CONFIG.confirmPath}`;
    const payload = {
      request_id: STATE.lastRequestId,
      confirmation_id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()),
      approvals: STATE.lastOneWayItems.map((item) => ({
        decision_id: item.decision_id,
        approved: true,
        approved_by: "web-user",
        timestamp: new Date().toISOString(),
        notes: "Confirmed via MissionCanvas voice-first UI"
      }))
    };

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      refs.rStatus.textContent = `${data.status || "approved"} (confirmed)`;
      refs.btnConfirmOwd.classList.add("hidden");
      // Record OWD decision in project state
      if (!CONFIG.workspaceId) {
        saveProjectState({
          decision: { type: "owd", status: data.status, request_id: STATE.lastRequestId },
          mode: STATE.currentMode,
          convergence_score: STATE.convergenceScore
        });
      }
    } catch (_err) {
      refs.rStatus.textContent = "confirmation_failed";
    }
  }

  async function fetchWorkspaceWelcome() {
    if (!CONFIG.workspaceId) return null;
    const endpoint = `${CONFIG.apiBase}/v1/missioncanvas/workspace-welcome`;
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ workspace_id: CONFIG.workspaceId })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  async function refreshWorkspaceView() {
    if (!CONFIG.workspaceId) return;
    const activeQuery = String(refs.queryInput?.value || "").trim();
    if (activeQuery) {
      await renderProjectStateQuery(activeQuery);
      return;
    }
    const welcome = await fetchWorkspaceWelcome();
    renderWorkspaceWelcome(welcome);
  }

  function renderWorkspaceWelcome(welcome) {
    if (!welcome || !refs.projectCheckin) return;

    STATE.workspaceWelcome = welcome;
    refs.projectCheckin.classList.remove("hidden");
    refs.projectCheckin.textContent = "";

    var header = document.createElement("h3");
    header.textContent = welcome.workspace_name || "Workspace";
    header.className = "checkin-header";
    refs.projectCheckin.appendChild(header);

    var intro = document.createElement("p");
    intro.className = "checkin-context";
    intro.textContent = welcome.welcome_message || "Workspace ready.";
    refs.projectCheckin.appendChild(intro);

    var stats = document.createElement("div");
    stats.className = "checkin-stats";
    var statItems = [
      { label: "User", value: welcome.user_name || "Unknown" },
      { label: "Role", value: (welcome.user_role || "operator").toUpperCase() },
      { label: "Health", value: welcome.health_score != null ? `${welcome.health_score}/${welcome.target_score || 100}` : "n/a" },
      { label: "Status", value: welcome.health_label || "n/a" }
    ];
    for (var i = 0; i < statItems.length; i++) {
      var stat = document.createElement("span");
      stat.className = "checkin-stat";
      var lbl = document.createElement("span");
      lbl.className = "checkin-stat-label";
      lbl.textContent = statItems[i].label;
      var val = document.createElement("span");
      val.className = "checkin-stat-value";
      val.textContent = statItems[i].value;
      stat.appendChild(lbl);
      stat.appendChild(val);
      stats.appendChild(stat);
    }
    refs.projectCheckin.appendChild(stats);

    if (welcome.objective) {
      var objective = document.createElement("p");
      objective.className = "checkin-context";
      objective.textContent = "Objective: " + welcome.objective;
      refs.projectCheckin.appendChild(objective);
    }

    if (Array.isArray(welcome.nudges) && welcome.nudges.length > 0) {
      var nudgeHeader = document.createElement("h4");
      nudgeHeader.textContent = "Start here";
      refs.projectCheckin.appendChild(nudgeHeader);

      var nudgeList = document.createElement("ul");
      nudgeList.className = "mode-gaps";
      for (var n = 0; n < welcome.nudges.length; n++) {
        var item = document.createElement("li");
        var nudge = welcome.nudges[n];
        item.className = "mode-gap-item";
        item.textContent = nudge.summary || nudge.what || "Follow up on a stale blocker.";
        nudgeList.appendChild(item);
      }
      refs.projectCheckin.appendChild(nudgeList);
    }

    if (Array.isArray(welcome.suggested_queries) && welcome.suggested_queries.length > 0) {
      var actionRow = document.createElement("div");
      actionRow.className = "row";
      welcome.suggested_queries.slice(0, 3).forEach(function (query, index) {
        var btn = document.createElement("button");
        btn.className = index === 0 ? "btn btn-primary" : "btn";
        btn.textContent = query;
        btn.addEventListener("click", function () {
          if (refs.queryInput) refs.queryInput.value = query;
          renderProjectStateQuery(query);
        });
        actionRow.appendChild(btn);
      });
      refs.projectCheckin.appendChild(actionRow);
    }

    if (refs.queryInput) {
      refs.queryInput.placeholder = welcome.suggested_queries?.[0] || "Ask about status, blockers, or next actions";
    }
    if (refs.tUserRole && welcome.user_role) refs.tUserRole.value = welcome.user_role;
    if (window.WorkspaceUI && CONFIG.workspaceId) {
      window.WorkspaceUI.setWorkspace(CONFIG.workspaceId);
      window.WorkspaceUI.renderWelcome(welcome);
    }
  }

  function formatWorkspaceQueryOutput(response, welcome) {
    if (response?.coaching) return response.action_brief_markdown;
    if (response?.convergence_chain?.narration) return response.convergence_chain.narration;
    if (response?.action_brief_markdown) return response.action_brief_markdown;
    if (welcome) {
      return [
        welcome.workspace_name || "Workspace",
        welcome.welcome_message || "",
        welcome.objective ? `Objective: ${welcome.objective}` : "",
        Array.isArray(welcome.nudges) && welcome.nudges.length
          ? `Top nudges:\n- ${welcome.nudges.map(function (n) { return n.summary || n.what || "Follow up"; }).join("\n- ")}`
          : ""
      ].filter(Boolean).join("\n\n");
    }
    if (!response) return "No response returned.";
    return "No workspace summary available.";
  }

  function speakBrief() {
    if (!STATE.lastBrief || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(STATE.lastBrief.slice(0, 1200));
    utter.rate = 1.0;
    utter.pitch = 1.0;
    window.speechSynthesis.speak(utter);
  }

  async function copyBrief() {
    if (!STATE.lastBrief) return;
    try {
      await navigator.clipboard.writeText(STATE.lastBrief);
      refs.btnCopy.textContent = "Copied";
      setTimeout(() => {
        refs.btnCopy.textContent = "Copy Brief";
      }, 1000);
    } catch (_err) {
      refs.btnCopy.textContent = "Copy Failed";
    }
  }

  function initVoiceRecognition() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      refs.voiceState.textContent = "Voice unsupported in this browser";
      refs.btnVoiceStart.disabled = true;
      refs.btnVoiceStop.disabled = true;
      setSystemStatus("voice unsupported in this browser", "warn");
      return;
    }

    const recognition = new SR();
    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = true;

    let finalText = "";

    recognition.onstart = function () {
      refs.voiceState.textContent = "Listening...";
      setSystemStatus("voice listening", "ok");
    };

    recognition.onresult = function (event) {
      let interim = "";
      for (let i = event.resultIndex; i < event.results.length; i += 1) {
        const t = event.results[i][0].transcript;
        if (event.results[i].isFinal) finalText += `${t} `;
        else interim += t;
      }
      refs.transcriptInput.value = `${finalText}${interim}`.trim();
      STATE.transcript = refs.transcriptInput.value;
    };

    recognition.onerror = function () {
      refs.voiceState.textContent = "Voice error";
      setSystemStatus("voice capture error", "error");
    };

    recognition.onend = function () {
      refs.voiceState.textContent = "Voice idle";
      setSystemStatus("voice capture complete", "ok");
      const translated = translateNaturalInput(refs.transcriptInput.value, STATE.structured);
      renderStructuredPrompt(translated);
    };

    refs.btnVoiceStart.addEventListener("click", function () {
      try {
        finalText = refs.transcriptInput.value ? `${refs.transcriptInput.value} ` : "";
        recognition.start();
      } catch (_err) {
        refs.voiceState.textContent = "Voice unavailable";
        setSystemStatus("microphone unavailable", "error");
      }
    });

    refs.btnVoiceStop.addEventListener("click", function () {
      recognition.stop();
      refs.voiceState.textContent = "Stopping...";
    });
  }

  function initEvents() {
    refs.personaChips.forEach((chip) => {
      chip.addEventListener("click", function () {
        applyPersona(chip.getAttribute("data-persona"));
      });
    });

    refs.btnHealth.addEventListener("click", checkConnection);

    // Live convergence updates as user types in structured fields
    var convergenceFields = [refs.tObjective, refs.tContext, refs.tOutcome, refs.tConstraints];
    convergenceFields.forEach(function (field) {
      if (field) field.addEventListener("input", updateLiveConvergence);
    });

    refs.presetChips.forEach((chip) => {
      chip.addEventListener("click", function () {
        const text = chip.getAttribute("data-preset") || "";
        refs.transcriptInput.value = text;
        const translated = translateNaturalInput(text, STATE.structured);
        renderStructuredPrompt(translated);
        setSystemStatus("preset loaded", "ok");
      });
    });

    refs.btnTranslate.addEventListener("click", function () {
      const translated = translateNaturalInput(refs.transcriptInput.value, STATE.structured);
      renderStructuredPrompt(translated);
      setSystemStatus("translation generated", "ok");
    });

    refs.btnManualTranslate.addEventListener("click", function () {
      refs.transcriptInput.value = String(refs.manualInput.value || "").trim();
      const translated = translateNaturalInput(refs.transcriptInput.value, STATE.structured);
      renderStructuredPrompt(translated);
      setSystemStatus("manual text translated", "ok");
    });

    refs.btnRoute.addEventListener("click", async function () {
      const structured = readStructuredPrompt();
      renderList(refs.qualityChecks, evaluatePromptQuality(structured));
      if (!structured.objective) {
        refs.resultStatus.textContent = "Add objective first (voice or text).";
        setSystemStatus("missing objective", "warn");
        return;
      }
      const response = await fetchRoute(structured);
      renderResponse(response);
      if (refs.autoLog.checked) await appendDecisionLog();
    });

    refs.btnStream.addEventListener("click", async function () {
      const structured = readStructuredPrompt();
      renderList(refs.qualityChecks, evaluatePromptQuality(structured));
      if (!structured.objective) return;
      await fetchStream(structured);
    });

    refs.btnRefine.addEventListener("click", async function () {
      const followup = String(refs.followupInput.value || "").trim();
      if (!followup) return;
      const combined = `${refs.transcriptInput.value || ""}\n${followup}`.trim();
      refs.transcriptInput.value = combined;
      const translated = translateNaturalInput(combined, readStructuredPrompt());
      renderStructuredPrompt(translated);
      const response = await fetchRoute(readStructuredPrompt());
      renderResponse(response);
      setSystemStatus("self-refinement reroute complete", "ok");
    });

    refs.btnSpeak.addEventListener("click", speakBrief);
    refs.btnCopy.addEventListener("click", copyBrief);
    refs.btnAppendLog.addEventListener("click", appendDecisionLog);
    refs.btnConfirmOwd.addEventListener("click", confirmOneWayDoor);
    if (refs.btnCommit) refs.btnCommit.addEventListener("click", commitRoute);
    if (refs.btnUncommit) refs.btnUncommit.addEventListener("click", uncommitRoute);
  }

  // ── Project state check-in on page load ──
  async function checkProjectState() {
    if (CONFIG.workspaceId) {
      if (!refs.projectCheckin) return;
      try {
        const welcome = await fetchWorkspaceWelcome();
        renderWorkspaceWelcome(welcome);
        setSystemStatus(`workspace ready: ${welcome.workspace_name}`, "ok");
        if (refs.queryPanel) {
          refs.queryPanel.classList.remove("hidden");
          var output = refs.queryPanel.querySelector(".query-output");
          if (output) output.textContent = formatWorkspaceQueryOutput(null, welcome);
        }
      } catch (_err) {
        setSystemStatus("workspace welcome unavailable", "warn");
      }
      return;
    }

    const ps = loadProjectState();
    if (!ps || !refs.projectCheckin) return;

    const summary = getProjectSummary();
    if (!summary || summary.routes_explored === 0) return;

    const lastDate = new Date(summary.last_updated);
    const ago = Math.round((Date.now() - lastDate.getTime()) / 60000);
    var agoText;
    if (ago < 1) agoText = "just now";
    else if (ago < 60) agoText = ago + " minutes ago";
    else if (ago < 1440) agoText = Math.round(ago / 60) + " hours ago";
    else agoText = Math.round(ago / 1440) + " days ago";

    refs.projectCheckin.classList.remove("hidden");
    refs.projectCheckin.textContent = "";

    // Header
    var header = document.createElement("h3");
    header.textContent = "Welcome back";
    header.className = "checkin-header";
    refs.projectCheckin.appendChild(header);

    // Summary stats
    var stats = document.createElement("div");
    stats.className = "checkin-stats";
    stats.innerHTML = "";
    var statItems = [
      { label: "Last active", value: agoText },
      { label: "Routes explored", value: String(summary.routes_explored) },
      { label: "Convergence high", value: summary.high_water_score + "/100" },
      { label: "Last mode", value: (summary.last_mode || "explore").toUpperCase() }
    ];
    if (summary.persona) {
      statItems.push({ label: "Persona", value: PERSONAS[summary.persona]?.name || summary.persona });
    }
    for (var i = 0; i < statItems.length; i++) {
      var stat = document.createElement("span");
      stat.className = "checkin-stat";
      var lbl = document.createElement("span");
      lbl.className = "checkin-stat-label";
      lbl.textContent = statItems[i].label;
      var val = document.createElement("span");
      val.className = "checkin-stat-value";
      val.textContent = statItems[i].value;
      stat.appendChild(lbl);
      stat.appendChild(val);
      stats.appendChild(stat);
    }
    refs.projectCheckin.appendChild(stats);

    // Last route context
    var lastRoute = ps.route_history[ps.route_history.length - 1];
    if (lastRoute) {
      var ctx = document.createElement("p");
      ctx.className = "checkin-context";
      ctx.textContent = "Last route: " + lastRoute.riu_id + " " + lastRoute.name +
        " (score " + lastRoute.score + ", " + lastRoute.mode + ")";
      refs.projectCheckin.appendChild(ctx);
    }

    // Buttons
    var btnResume = document.createElement("button");
    btnResume.className = "btn btn-primary";
    btnResume.textContent = "Continue where I left off";
    btnResume.addEventListener("click", function () {
      if (summary.persona && PERSONAS[summary.persona]) {
        applyPersona(summary.persona);
      }
      refs.projectCheckin.classList.add("hidden");
      setSystemStatus("Session resumed from " + agoText, "ok");
    });

    var btnNew = document.createElement("button");
    btnNew.className = "btn";
    btnNew.textContent = "Start fresh";
    btnNew.addEventListener("click", function () {
      clearProjectState();
      refs.projectCheckin.classList.add("hidden");
      setSystemStatus("Fresh start", "ok");
    });

    var row = document.createElement("div");
    row.className = "row";
    row.appendChild(btnResume);
    row.appendChild(btnNew);
    refs.projectCheckin.appendChild(row);
  }

  // ── Explore-mode nudge (after 5+ routes without converging) ──
  var exploreRouteCount = 0;

  function checkExploreNudge(response) {
    if (response?.mode === "explore") {
      exploreRouteCount++;
      if (exploreRouteCount >= 5 && refs.modeContent) {
        var nudge = document.createElement("div");
        nudge.className = "explore-nudge";
        nudge.textContent = "You've explored " + exploreRouteCount +
          " routes. Would narrowing to a specific outcome help? Try adding a desired outcome above.";
        refs.modeContent.prepend(nudge);
      }
    } else {
      exploreRouteCount = 0;
    }
  }

  // ── Anonymous feedback opt-in ──
  var FEEDBACK_KEY = "missioncanvas_feedback_offered";
  var FEEDBACK_ENDPOINT = "/v1/missioncanvas/anonymous-feedback";

  function checkFeedbackOffer() {
    if (CONFIG.workspaceId) return;
    // Only offer after meaningful usage (5+ routes, score hit 60+)
    var ps = loadProjectState();
    if (!ps) return;
    var summary = getProjectSummary();
    if (!summary || summary.routes_explored < 5 || summary.high_water_score < 60) return;

    // Only offer once per session
    if (sessionStorage.getItem(FEEDBACK_KEY)) return;
    sessionStorage.setItem(FEEDBACK_KEY, "offered");

    // Don't show if they've opted out permanently
    if (localStorage.getItem(FEEDBACK_KEY) === "never") return;

    if (!refs.projectCheckin) return;

    var panel = document.createElement("div");
    panel.className = "feedback-offer";

    var msg = document.createElement("p");
    msg.textContent = "You've been making progress! Would you like to share anonymous usage data to help us improve MissionCanvas?";
    panel.appendChild(msg);

    var detail = document.createElement("p");
    detail.className = "feedback-detail";
    detail.textContent = "We collect: routes explored, convergence scores, persona used, and gaps filled. No personal data, text input, or identifying information.";
    panel.appendChild(detail);

    var btnSend = document.createElement("button");
    btnSend.className = "btn btn-primary";
    btnSend.textContent = "Share anonymous feedback";
    btnSend.addEventListener("click", function () {
      sendAnonymousFeedback();
      panel.remove();
    });

    var btnLater = document.createElement("button");
    btnLater.className = "btn";
    btnLater.textContent = "Not now";
    btnLater.addEventListener("click", function () {
      panel.remove();
    });

    var btnNever = document.createElement("button");
    btnNever.className = "btn";
    btnNever.textContent = "Don't ask again";
    btnNever.addEventListener("click", function () {
      localStorage.setItem(FEEDBACK_KEY, "never");
      panel.remove();
    });

    var row = document.createElement("div");
    row.className = "row";
    row.appendChild(btnSend);
    row.appendChild(btnLater);
    row.appendChild(btnNever);
    panel.appendChild(row);

    // Insert after check-in or at top of result panel
    var target = refs.projectCheckin.parentElement || document.querySelector(".result-panel");
    if (target) target.insertBefore(panel, target.firstChild);
  }

  function sendAnonymousFeedback() {
    if (CONFIG.workspaceId) return;
    var ps = loadProjectState();
    if (!ps) return;

    var feedback = {
      timestamp: new Date().toISOString(),
      routes_explored: ps.route_history.length,
      convergence_high_water: ps.convergence_high_water,
      persona: ps.persona || null,
      decisions_made: ps.decisions_made.length,
      modes_used: ps.route_history.reduce(function (acc, r) {
        acc[r.mode] = (acc[r.mode] || 0) + 1;
        return acc;
      }, {}),
      avg_score: ps.route_history.length > 0
        ? Math.round(ps.route_history.reduce(function (sum, r) { return sum + (r.score || 0); }, 0) / ps.route_history.length)
        : 0,
      session_duration_routes: ps.route_history.length,
      rius_explored: [...new Set(ps.route_history.map(function (r) { return r.riu_id; }))].length
    };

    // Best-effort POST — don't block on failure
    fetch(CONFIG.apiBase + FEEDBACK_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(feedback)
    }).then(function () {
      setSystemStatus("Anonymous feedback sent. Thank you!", "ok");
    }).catch(function () {
      // Silently fail — feedback is opt-in and best-effort
    });
  }

  // ── Queryable project state UI ──
  async function renderProjectStateQuery(question) {
    var panel = refs.queryPanel;
    if (!panel) return;

    panel.classList.remove("hidden");
    var output = panel.querySelector(".query-output");
    if (!output) return;

    if (CONFIG.workspaceId) {
      var q = String(question || "").trim();
      try {
        if (!q || q.toLowerCase() === "summary") {
          const welcome = STATE.workspaceWelcome || await fetchWorkspaceWelcome();
          if (welcome) {
            STATE.workspaceWelcome = welcome;
            output.textContent = formatWorkspaceQueryOutput(null, welcome);
          }
          return;
        }

        output.textContent = "Loading workspace answer...";
        const response = await fetchRoute({
          objective: q,
          context: "",
          desired_outcome: "",
          constraints: "",
          risk_posture: String(refs.tRiskPosture?.value || "medium").trim(),
          user_role: String(refs.tUserRole?.value || "operator").trim()
        });
        renderResponse(response);
        output.textContent = formatWorkspaceQueryOutput(response, STATE.workspaceWelcome);
      } catch (_err) {
        output.textContent = "Workspace query failed. Try again.";
      }
      return;
    }

    var ps = loadProjectState();
    if (!ps || !ps.route_history.length) {
      output.textContent = "No project data yet. Route a mission to start building state.";
      return;
    }

    var q = (question || "").toLowerCase();
    var lines = [];

    if (!q || q === "summary" || q.includes("progress") || q.includes("status") || q.includes("how")) {
      var summary = getProjectSummary();
      lines.push("PROJECT STATUS");
      lines.push("Routes explored: " + summary.routes_explored);
      lines.push("Unique RIUs: " + [...new Set(ps.route_history.map(function(r){ return r.riu_id; }))].length);
      lines.push("Convergence high: " + summary.high_water_score + "/100");
      lines.push("Current mode: " + (summary.last_mode || "explore").toUpperCase());
      lines.push("Decisions made: " + summary.decisions_made);
      lines.push("Persona: " + (summary.persona ? PERSONAS[summary.persona]?.name || summary.persona : "none"));
      lines.push("Last active: " + (summary.last_updated || "never"));

      if (ps.convergence_high_water < 50) {
        lines.push("");
        lines.push("SUGGESTION: You're still in explore territory. Try adding a desired outcome to push toward convergence.");
      } else if (ps.convergence_high_water < 95) {
        lines.push("");
        lines.push("SUGGESTION: You're converging. Fill remaining gaps (constraints, context) to strengthen your mission.");
      } else {
        lines.push("");
        lines.push("READY: Convergence is high. You can commit to a route when ready.");
      }
    } else if (q.includes("block") || q.includes("stuck") || q.includes("gap")) {
      lines.push("CONVERGENCE GAPS");
      var gaps = STATE.lastResponse?.convergence_gaps || [];
      if (gaps.length) {
        for (var g = 0; g < gaps.length; g++) lines.push("- " + gaps[g]);
      } else {
        lines.push("No gaps detected from last route.");
      }
      var kGaps = STATE.lastResponse?.knowledge_gap;
      if (kGaps?.detected) {
        lines.push("");
        lines.push("KNOWLEDGE GAPS");
        var missing = kGaps.what_is_missing || [];
        for (var k = 0; k < missing.length; k++) lines.push("- " + missing[k]);
      }
    } else if (q.includes("decision") || q.includes("owd")) {
      lines.push("DECISIONS");
      if (ps.decisions_made.length === 0) {
        lines.push("No decisions recorded yet.");
      } else {
        for (var d = 0; d < ps.decisions_made.length; d++) {
          var dec = ps.decisions_made[d];
          lines.push("- [" + (dec.timestamp || "?").slice(0, 16) + "] " + dec.type + ": " + dec.status);
        }
      }
    } else if (q.includes("history") || q.includes("route")) {
      lines.push("ROUTE HISTORY");
      for (var r = 0; r < ps.route_history.length; r++) {
        var route = ps.route_history[r];
        lines.push((r + 1) + ". " + (route.timestamp || "").slice(0, 16) + " | " +
          route.riu_id + " " + route.name + " (" + route.mode + ", " + route.score + "/100)");
      }
    } else if (q.includes("fact") || q.includes("know")) {
      lines.push("KNOWN FACTS");
      if (ps.known_facts.length === 0) {
        lines.push("No facts recorded yet.");
      } else {
        for (var f = 0; f < ps.known_facts.length; f++) {
          lines.push("- " + ps.known_facts[f]);
        }
      }
    } else {
      lines.push("QUERY HELP");
      lines.push("Try asking about:");
      lines.push("  progress / status — overall project state");
      lines.push("  gaps / blocks — what's missing");
      lines.push("  decisions — OWD confirmations and choices");
      lines.push("  routes / history — where you've been");
      lines.push("  facts / know — what's been confirmed");
    }

    output.textContent = lines.join("\n");
  }

  // Keep console API too
  window.queryProjectState = async function (question) {
    if (CONFIG.workspaceId) {
      var panel = refs.queryPanel;
      if (panel) {
        await renderProjectStateQuery(question);
        return "Result shown in UI.";
      }
      const response = await fetchRoute({
        objective: String(question || "How are we doing?"),
        context: "",
        desired_outcome: "",
        constraints: "",
        risk_posture: String(refs.tRiskPosture?.value || "medium").trim(),
        user_role: String(refs.tUserRole?.value || "operator").trim()
      });
      return formatWorkspaceQueryOutput(response, STATE.workspaceWelcome);
    }

    var ps = loadProjectState();
    if (!ps) return "No project state saved yet.";
    var panel = refs.queryPanel;
    if (panel) {
      renderProjectStateQuery(question);
      return "Result shown in UI.";
    }
    // Fallback for console-only usage
    var q = (question || "").toLowerCase();
    if (q.includes("block") || q.includes("stuck")) {
      return "Convergence gaps from last route:\n" +
        (STATE.lastResponse?.convergence_gaps || ["None detected"]).join("\n");
    }
    if (q.includes("decision") || q.includes("pending")) {
      return "Decisions made: " + ps.decisions_made.length;
    }
    if (q.includes("progress") || q.includes("status") || q.includes("how")) {
      var summary = getProjectSummary();
      return "Routes explored: " + summary.routes_explored +
        "\nConvergence high water: " + summary.high_water_score + "/100" +
        "\nLast mode: " + (summary.last_mode || "none");
    }
    if (q.includes("history") || q.includes("route")) {
      return ps.route_history.map(function (r) {
        return r.timestamp?.slice(0, 16) + " | " + r.riu_id + " " + r.name;
      }).join("\n") || "No routes yet.";
    }
    return "Ask about: progress, routes, decisions, or blocks.";
  };

  if (window.WorkspaceUI) {
    window.WorkspaceUI.init({
      apiBase: CONFIG.apiBase,
      workspaceId: CONFIG.workspaceId,
      runQuery: function (query) {
        prefillWorkspaceQuery(query);
        return renderProjectStateQuery(query);
      },
      prefillQuery: function (query) {
        prefillWorkspaceQuery(query);
        if (refs.queryInput) refs.queryInput.focus();
      },
      refreshWorkspace: function () {
        return refreshWorkspaceView();
      },
      setStatus: function (message, level) {
        setSystemStatus(message, level || "ok");
      }
    });
  }

  initVoiceRecognition();
  initEvents();
  checkProjectState();

  // Wire query panel button and input
  if (refs.btnQuery) {
    refs.btnQuery.addEventListener("click", function () {
      renderProjectStateQuery(refs.queryInput ? refs.queryInput.value : "summary");
    });
  }
  if (refs.queryInput) {
    refs.queryInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        renderProjectStateQuery(refs.queryInput.value);
      }
    });
  }

  // Check for explore nudge after route
  var originalRenderResponse = renderResponse;
  // (explore nudge is wired inside renderResponse via renderModeContent, but also check feedback)
  // Offer anonymous feedback after each route if criteria met
  var routeCountThisSession = 0;

  // Patch btnRoute to track route count for feedback timing
  var origRouteClick = refs.btnRoute.onclick;
  refs.btnRoute.addEventListener("click", function () {
    routeCountThisSession++;
    if (routeCountThisSession === 5) {
      setTimeout(checkFeedbackOffer, 1000);
    }
  });

  setSystemStatus("ready", "ok");
})();
