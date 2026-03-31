// Mission Canvas — Workspace Setup Wizard
// Client-side logic for the 4-step onboarding flow

(function () {
  'use strict';

  // ── State ──
  let currentStep = 1;
  let createdWorkspace = null; // response from create-workspace API
  let selectedSubs = ['claude'];
  let apiKeys = {};
  const startTime = Date.now();

  // ── DOM refs ──
  const $wsName = document.getElementById('wsName');
  const $userName = document.getElementById('userName');
  const $objective = document.getElementById('objective');
  const $slugPreview = document.getElementById('slugPreview');
  const $btnCreate = document.getElementById('btnCreate');
  const $step1Msg = document.getElementById('step1Msg');

  // ── Slug generation ──
  function toSlug(str) {
    return str.toLowerCase().trim()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .substring(0, 40);
  }

  $wsName.addEventListener('input', () => {
    const slug = toSlug($wsName.value);
    $slugPreview.textContent = slug ? `workspace-id: ${slug}` : '';
    validateStep1();
  });
  $userName.addEventListener('input', validateStep1);
  $objective.addEventListener('input', validateStep1);

  function validateStep1() {
    const valid = $wsName.value.trim() && $userName.value.trim() && $objective.value.trim();
    $btnCreate.disabled = !valid;
  }

  // ── Step navigation ──
  function goToStep(n) {
    currentStep = n;
    document.querySelectorAll('.step-panel').forEach((p, i) => {
      p.classList.toggle('active', i + 1 === n);
    });
    document.querySelectorAll('.step-dot').forEach((d, i) => {
      d.classList.remove('active', 'done');
      if (i + 1 === n) d.classList.add('active');
      else if (i + 1 < n) d.classList.add('done');
    });
  }

  // ── Step 1: Create workspace ──
  $btnCreate.addEventListener('click', async () => {
    $btnCreate.disabled = true;
    $btnCreate.textContent = 'Creating...';
    $step1Msg.className = 'msg';
    $step1Msg.style.display = 'none';

    const body = {
      workspace_id: toSlug($wsName.value),
      name: $wsName.value.trim(),
      user_name: $userName.value.trim(),
      user_role: document.getElementById('userRole').value,
      domain: document.getElementById('domain').value,
      objective: $objective.value.trim(),
      risk_posture: document.getElementById('riskPosture').value,
      greeting_style: 'executive'
    };

    try {
      const resp = await fetch('/v1/missioncanvas/create-workspace', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await resp.json();

      if (!resp.ok) {
        $step1Msg.className = 'msg error';
        $step1Msg.textContent = data.error || 'Failed to create workspace';
        $step1Msg.style.display = 'block';
        $btnCreate.disabled = false;
        $btnCreate.textContent = 'Create Workspace';
        return;
      }

      createdWorkspace = data;
      goToStep(2);
    } catch (err) {
      $step1Msg.className = 'msg error';
      $step1Msg.textContent = 'Connection error — is the server running?';
      $step1Msg.style.display = 'block';
      $btnCreate.disabled = false;
      $btnCreate.textContent = 'Create Workspace';
    }
  });

  // ── Step 2: Subscriptions ──
  const $subGrid = document.getElementById('subGrid');
  $subGrid.addEventListener('change', (e) => {
    if (e.target.type === 'checkbox') {
      const item = e.target.closest('.sub-item');
      item.classList.toggle('checked', e.target.checked);

      selectedSubs = Array.from($subGrid.querySelectorAll('input:checked')).map(i => i.value);
    }
  });

  // Initialize the checked state
  $subGrid.querySelectorAll('input:checked').forEach(i => i.closest('.sub-item').classList.add('checked'));

  // Key toggle
  document.getElementById('keyToggle').addEventListener('click', () => {
    document.getElementById('keyFields').classList.toggle('visible');
  });

  function collectKeys() {
    apiKeys = {};
    document.querySelectorAll('#keyFields input[data-key]').forEach(input => {
      if (input.value.trim()) {
        apiKeys[input.dataset.key] = input.value.trim();
      }
    });
  }

  document.getElementById('btnSubs').addEventListener('click', () => {
    collectKeys();
    renderConfig();
    goToStep(3);
  });

  document.getElementById('btnSkipSubs').addEventListener('click', () => {
    apiKeys = {};
    renderConfig();
    goToStep(3);
  });

  // Back buttons
  document.getElementById('btnBackToCreate').addEventListener('click', () => goToStep(1));
  document.getElementById('btnBackToSubs').addEventListener('click', () => goToStep(2));

  // ── Step 3: Config rendering ──
  let activeTab = 'claude-desktop';

  document.querySelectorAll('.config-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      activeTab = tab.dataset.target;
      document.querySelectorAll('.config-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      renderConfig();
    });
  });

  function buildConfig(target) {
    if (!createdWorkspace) return '{}';
    const wsId = createdWorkspace.workspace_id;
    const env = { MC_WORKSPACE: wsId, ...apiKeys };

    if (target === 'claude-desktop') {
      return JSON.stringify({
        mcpServers: {
          'mission-canvas': {
            command: 'node',
            args: [createdWorkspace.mcp_config.mcpServers['mission-canvas'].args[0]],
            env
          }
        }
      }, null, 2);
    }

    if (target === 'claude-code') {
      return JSON.stringify({
        mcpServers: {
          'mission-canvas': {
            command: 'node',
            args: ['mcp_server.mjs'],
            cwd: createdWorkspace.mcp_config_claude_code.mcpServers['mission-canvas'].cwd,
            env
          }
        }
      }, null, 2);
    }

    // Cursor / generic
    return JSON.stringify({
      mcpServers: {
        'mission-canvas': {
          command: 'node',
          args: [createdWorkspace.mcp_config.mcpServers['mission-canvas'].args[0]],
          env
        }
      }
    }, null, 2);
  }

  function getInstructions(target) {
    if (target === 'claude-desktop') {
      return `<strong>Claude Desktop:</strong> Open Settings → Developer → Edit Config. Paste the JSON above into your <code>claude_desktop_config.json</code> file. If you already have other MCP servers, merge the <code>mcpServers</code> object. Restart Claude Desktop. You'll see the mission-canvas tools in the tool picker.`;
    }
    if (target === 'claude-code') {
      return `<strong>Claude Code:</strong> Save the JSON above as <code>.mcp.json</code> in your project root, or run <code>claude mcp add mission-canvas node mcp_server.mjs</code> from the missioncanvas-site directory. The tools will be available in your next Claude Code session.`;
    }
    return `<strong>Cursor / Other MCP clients:</strong> Open your MCP settings and add the server config above. The <code>command</code> launches the server, and <code>env.MC_WORKSPACE</code> tells it which workspace to use. Restart your client after adding.`;
  }

  function renderConfig() {
    document.getElementById('configCode').textContent = buildConfig(activeTab);
    document.getElementById('configInstructions').innerHTML = getInstructions(activeTab);
  }

  // Copy button
  document.getElementById('btnCopy').addEventListener('click', async () => {
    const btn = document.getElementById('btnCopy');
    const text = buildConfig(activeTab);
    try {
      await navigator.clipboard.writeText(text);
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
    } catch {
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
    }
  });

  // ── Step 3 → 4 ──
  document.getElementById('btnToLaunch').addEventListener('click', () => {
    renderSummary();
    goToStep(4);
  });

  // ── Step 4: Launch ──
  function renderSummary() {
    if (!createdWorkspace) return;
    const wsId = createdWorkspace.workspace_id;
    const wsUrl = createdWorkspace.workspace_url;

    document.getElementById('summaryGrid').innerHTML = `
      <div class="summary-item">
        <div class="summary-label">Workspace</div>
        <div class="summary-value">${$wsName.value.trim()}</div>
      </div>
      <div class="summary-item">
        <div class="summary-label">Health Score</div>
        <div class="summary-value health">50 / 100 — STARTING</div>
      </div>
      <div class="summary-item">
        <div class="summary-label">Subscriptions</div>
        <div class="summary-value">${selectedSubs.length} connected</div>
      </div>
      <div class="summary-item">
        <div class="summary-label">Setup time</div>
        <div class="summary-value">${Math.round((Date.now() - startTime) / 60000)} min</div>
      </div>
    `;

    document.getElementById('btnOpenWeb').href = wsUrl;

    // Wire chip links to the web UI
    const base = wsUrl;
    document.getElementById('chipBrief').href = base;
    document.getElementById('chipGaps').href = base;
    document.getElementById('chipDecisions').href = base;
  }

  // ── Timer ──
  setInterval(() => {
    const elapsed = Math.round((Date.now() - startTime) / 1000);
    const min = Math.floor(elapsed / 60);
    const sec = String(elapsed % 60).padStart(2, '0');
    document.getElementById('timer').textContent = `${min}:${sec}`;
  }, 1000);

})();
