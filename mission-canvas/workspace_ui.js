(function () {
  function $(id) {
    return document.getElementById(id);
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function clear(node) {
    if (node) node.textContent = "";
  }

  function badge(label, cssClass) {
    var span = document.createElement("span");
    span.className = cssClass;
    span.textContent = label;
    return span;
  }

  function createStat(label, value, extraClass) {
    var wrap = document.createElement("div");
    wrap.className = extraClass ? "workspace-stat " + extraClass : "workspace-stat";
    var lbl = document.createElement("span");
    lbl.className = "workspace-stat-label";
    lbl.textContent = label;
    var val = document.createElement("span");
    val.className = "workspace-stat-value";
    val.textContent = value;
    wrap.appendChild(lbl);
    wrap.appendChild(val);
    return wrap;
  }

  function formatSectionDetail(detail) {
    if (Array.isArray(detail)) {
      return detail.map(function (item) {
        if (typeof item === "string") return item;
        return item.id ? item.id + ": " + (item.what || item.action || item.decision || item.fact || "") : JSON.stringify(item);
      });
    }

    if (!detail || typeof detail !== "object") return [];

    var lines = [];
    Object.keys(detail).forEach(function (key) {
      var value = detail[key];
      if (!Array.isArray(value) || !value.length) return;
      lines.push(key.replace(/_/g, " ").toUpperCase());
      value.forEach(function (item) {
        if (typeof item === "string") {
          lines.push("- " + item);
          return;
        }
        var summary = item.what || item.action || item.decision || item.fact || item.id || "Item";
        lines.push("- " + summary);
      });
    });
    return lines;
  }

  function getBriefAccentClass(sectionId) {
    if (sectionId === "health_snapshot") return "workspace-brief-health";
    if (sectionId === "top_blockers") return "workspace-brief-critical";
    if (sectionId === "open_decisions") return "workspace-brief-decisions";
    if (sectionId === "recently_resolved") return "workspace-brief-resolved";
    return "workspace-brief-neutral";
  }

  function renderDailyBrief(target, dailyBrief) {
    if (!target || !dailyBrief || !normalizeList(dailyBrief.sections).length) return;

    var panel = document.createElement("section");
    panel.className = "workspace-card workspace-brief";

    var head = document.createElement("div");
    head.className = "workspace-panel-head";
    var title = document.createElement("h3");
    title.textContent = "Daily Brief";
    head.appendChild(title);

    if (dailyBrief.generated_at) {
      var stamp = document.createElement("span");
      stamp.className = "workspace-kicker";
      stamp.textContent = dailyBrief.generated_at;
      head.appendChild(stamp);
    }
    panel.appendChild(head);

    normalizeList(dailyBrief.sections).forEach(function (section) {
      var block = document.createElement("details");
      block.className = "workspace-brief-section " + getBriefAccentClass(section.id);
      block.open = section.id === "health_snapshot" || section.id === "top_blockers";

      var summary = document.createElement("summary");
      summary.className = "workspace-brief-summary";

      var sectionTitle = document.createElement("h4");
      sectionTitle.textContent = section.title || section.id || "Section";
      summary.appendChild(sectionTitle);

      if (section.id) {
        var accent = document.createElement("span");
        accent.className = "workspace-kicker";
        accent.textContent = section.id.replace(/_/g, " ");
        summary.appendChild(accent);
      }
      block.appendChild(summary);

      var content = document.createElement("div");
      content.className = "workspace-brief-body";

      if (section.voice) {
        var voice = document.createElement("p");
        voice.className = "workspace-copy";
        voice.textContent = section.voice;
        content.appendChild(voice);
      }

      var detailLines = formatSectionDetail(section.detail);
      if (detailLines.length) {
        content.appendChild(createList(detailLines));
      }

      block.appendChild(content);
      panel.appendChild(block);
    });

    if (dailyBrief.closing && normalizeList(dailyBrief.closing.choices).length) {
      var closing = document.createElement("div");
      closing.className = "workspace-brief-closing";

      if (dailyBrief.closing.voice) {
        var closingCopy = document.createElement("p");
        closingCopy.className = "workspace-copy";
        closingCopy.textContent = dailyBrief.closing.voice;
        closing.appendChild(closingCopy);
      }

      var actions = document.createElement("div");
      actions.className = "workspace-chip-row";
      dailyBrief.closing.choices.forEach(function (choice) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "workspace-chip workspace-chip-solid";
        btn.textContent = choice;
        btn.addEventListener("click", function () {
          if (state.prefillQuery) state.prefillQuery(choice);
          if (state.runQuery) state.runQuery(choice);
        });
        actions.appendChild(btn);
      });
      closing.appendChild(actions);
      panel.appendChild(closing);
    }

    target.appendChild(panel);
  }

  function normalizeList(value) {
    return Array.isArray(value) ? value : [];
  }

  function parseNarration(narration) {
    var lines = String(narration || "").split("\n");
    var sections = [];
    var current = null;
    var bottomLine = "";

    lines.forEach(function (rawLine) {
      var line = rawLine.trim();
      if (!line) return;

      if (line.indexOf("## ") === 0) {
        current = { heading: line.slice(3), items: [] };
        sections.push(current);
        return;
      }

      if (line.indexOf("### ") === 0) {
        current = { heading: line.slice(4), items: [] };
        sections.push(current);
        return;
      }

      if (line.indexOf("**Bottom line**:") === 0) {
        bottomLine = line.replace(/^\*\*Bottom line\*\*:\s*/, "");
        return;
      }

      if (!current) {
        current = { heading: "", items: [] };
        sections.push(current);
      }
      current.items.push(line);
    });

    return { sections: sections, bottomLine: bottomLine };
  }

  function createList(items) {
    var list = document.createElement("ul");
    list.className = "workspace-list";
    items.forEach(function (item) {
      var li = document.createElement("li");
      li.innerHTML = escapeHtml(item)
        .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
        .replace(/^- /, "");
      list.appendChild(li);
    });
    return list;
  }

  function createNarrationBlock(chain) {
    var card = document.createElement("section");
    card.className = "workspace-card";

    var head = document.createElement("div");
    head.className = "workspace-card-head";
    var title = document.createElement("h3");
    title.textContent = chain.title || "Workspace View";
    head.appendChild(title);

    if (chain.query_type) {
      var kicker = document.createElement("span");
      kicker.className = "workspace-kicker";
      kicker.textContent = chain.query_type.replace(/_/g, " ");
      head.appendChild(kicker);
    }
    card.appendChild(head);

    var parsed = parseNarration(chain.narration);
    parsed.sections.forEach(function (section) {
      var block = document.createElement("div");
      block.className = "workspace-section";
      if (section.heading) {
        var heading = document.createElement("h4");
        heading.textContent = section.heading;
        block.appendChild(heading);
      }

      var bullets = [];
      var copy = [];
      section.items.forEach(function (item) {
        if (item.indexOf("- ") === 0 || item.indexOf("1.") === 0 || item.indexOf("2.") === 0 || item.indexOf("3.") === 0) {
          bullets.push(item);
        } else {
          copy.push(item);
        }
      });

      if (copy.length > 0) {
        var p = document.createElement("p");
        p.className = "workspace-copy";
        p.innerHTML = escapeHtml(copy.join(" ")).replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
        block.appendChild(p);
      }

      if (bullets.length > 0) {
        block.appendChild(createList(bullets));
      }
      card.appendChild(block);
    });

    if (parsed.bottomLine) {
      var bottom = document.createElement("div");
      bottom.className = "workspace-bottom-line";
      bottom.textContent = parsed.bottomLine;
      card.appendChild(bottom);
    }

    return card;
  }

  function createTreeNode(node) {
    var details = document.createElement("details");
    details.open = true;

    var summary = document.createElement("summary");
    var summaryText = document.createElement("span");
    summaryText.textContent = node.summary || node.node_id || "Dependency";
    summary.appendChild(summaryText);
    details.appendChild(summary);

    var meta = document.createElement("div");
    meta.className = "workspace-tree-meta";
    if (node.priority) meta.appendChild(badge(node.priority, "priority-badge priority-" + node.priority));
    if (node.age_string) meta.appendChild(badge(node.age_string, "urgency-badge urgency-moderate"));
    if (node.who_resolves) meta.appendChild(badge(node.who_resolves, "urgency-badge urgency-low"));
    details.appendChild(meta);

    var resolveControls = createResolveControls(node);
    if (resolveControls) details.appendChild(resolveControls);

    if (normalizeList(node.unblocks).length > 0) {
      node.unblocks.forEach(function (child) {
        details.appendChild(createTreeNode(child));
      });
    }

    return details;
  }

  function renderTree(target, chains) {
    if (!target) return;
    clear(target);
    if (!normalizeList(chains).length) return;

    var panel = document.createElement("section");
    panel.className = "workspace-tree";
    var head = document.createElement("div");
    head.className = "workspace-panel-head";
    var title = document.createElement("h3");
    title.textContent = "Dependency Tree";
    head.appendChild(title);
    panel.appendChild(head);

    chains.forEach(function (chain) {
      panel.appendChild(createTreeNode(chain));
    });
    target.appendChild(panel);
  }

  function renderNudges(target, nudges, hooks) {
    if (!target) return;
    clear(target);
    if (!normalizeList(nudges).length) return;

    var panel = document.createElement("section");
    panel.className = "workspace-nudges";
    var head = document.createElement("div");
    head.className = "workspace-panel-head";
    var title = document.createElement("h3");
    title.textContent = "Nudges";
    head.appendChild(title);
    panel.appendChild(head);

    var list = document.createElement("div");
    list.className = "workspace-nudge-list";

    nudges.forEach(function (nudge) {
      var item = document.createElement("div");
      item.className = "workspace-nudge";

      var top = document.createElement("div");
      top.className = "workspace-nudge-top";

      var name = document.createElement("div");
      name.className = "workspace-nudge-title";
      name.textContent = nudge.summary || nudge.what || nudge.id || "Nudge";
      top.appendChild(name);
      top.appendChild(badge(nudge.urgency || nudge.priority || "low", "urgency-badge urgency-" + (nudge.urgency || "low")));
      item.appendChild(top);

      var meta = document.createElement("div");
      meta.className = "workspace-nudge-meta";
      meta.textContent = [
        nudge.age_string || "",
        nudge.is_yours ? "on you" : (nudge.who_resolves || ""),
        nudge.unblocks_count ? "unblocks " + nudge.unblocks_count : ""
      ].filter(Boolean).join(" · ");
      item.appendChild(meta);

      var row = document.createElement("div");
      row.className = "workspace-chip-row";
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "workspace-chip";
      btn.textContent = "Ask about this";
      btn.addEventListener("click", function () {
        if (hooks && hooks.prefillQuery) hooks.prefillQuery("What's blocking us?");
      });
      row.appendChild(btn);
      item.appendChild(row);

      list.appendChild(item);
    });

    panel.appendChild(list);
    target.appendChild(panel);
  }

  function renderSuggestedQueries(target, queries, hooks) {
    if (!target) return;
    clear(target);
    if (!normalizeList(queries).length) return;

    var panel = document.createElement("section");
    panel.className = "workspace-suggested";
    var head = document.createElement("div");
    head.className = "workspace-panel-head";
    var title = document.createElement("h3");
    title.textContent = "Suggested Queries";
    head.appendChild(title);
    panel.appendChild(head);

    var row = document.createElement("div");
    row.className = "workspace-chip-row";
    queries.forEach(function (query) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "workspace-chip";
      btn.textContent = query;
      btn.addEventListener("click", function () {
        if (hooks && hooks.runQuery) hooks.runQuery(query);
      });
      row.appendChild(btn);
    });
    panel.appendChild(row);
    target.appendChild(panel);
  }

  function renderCoachingPanel(target, response) {
    if (!target || !response || !response.coaching) return;

    var coaching = response.coaching;
    var panel = document.createElement("section");
    panel.className = "workspace-card workspace-coaching";

    var head = document.createElement("div");
    head.className = "workspace-card-head";
    var title = document.createElement("h3");
    title.textContent = "Coaching";
    head.appendChild(title);

    if (coaching.stage) {
      head.appendChild(badge(coaching.stage, "workspace-health-badge workspace-coaching-stage"));
    }
    panel.appendChild(head);

    var concept = document.createElement("p");
    concept.className = "workspace-copy";
    concept.innerHTML = "<strong>Concept:</strong> " + escapeHtml(coaching.concept_label || coaching.concept_id || "Concept");
    panel.appendChild(concept);

    if (coaching.answer) {
      var answer = document.createElement("p");
      answer.className = "workspace-copy";
      answer.textContent = coaching.answer;
      panel.appendChild(answer);
    }

    if (coaching.why_it_matters) {
      var why = document.createElement("div");
      why.className = "workspace-section";
      var whyTitle = document.createElement("h4");
      whyTitle.textContent = "Why It Matters Here";
      why.appendChild(whyTitle);
      var whyCopy = document.createElement("p");
      whyCopy.className = "workspace-copy";
      whyCopy.textContent = coaching.why_it_matters;
      why.appendChild(whyCopy);
      panel.appendChild(why);
    }

    if (coaching.verification_prompt) {
      var check = document.createElement("div");
      check.className = "workspace-section";
      var checkTitle = document.createElement("h4");
      checkTitle.textContent = "Check Your Understanding";
      check.appendChild(checkTitle);
      var checkCopy = document.createElement("p");
      checkCopy.className = "workspace-copy";
      checkCopy.textContent = coaching.verification_prompt;
      check.appendChild(checkCopy);
      panel.appendChild(check);

      renderVerificationForm(panel, coaching);
    }

    if (normalizeList(coaching.sources).length) {
      var sources = document.createElement("div");
      sources.className = "workspace-section";
      var sourcesTitle = document.createElement("h4");
      sourcesTitle.textContent = "Sources";
      sources.appendChild(sourcesTitle);
      var sourceList = document.createElement("ul");
      sourceList.className = "workspace-list";
      coaching.sources.forEach(function (source) {
        var item = document.createElement("li");
        item.textContent = source.url ? source.title + " — " + source.url : source.title;
        sourceList.appendChild(item);
      });
      sources.appendChild(sourceList);
      panel.appendChild(sources);
    }

    target.appendChild(panel);
  }

  function renderWelcomeSummary(target, welcome) {
    if (!target || !welcome) return;
    clear(target);

    var card = document.createElement("section");
    card.className = "workspace-card";
    var head = document.createElement("div");
    head.className = "workspace-card-head";
    var title = document.createElement("h3");
    title.textContent = welcome.workspace_name || "Workspace";
    head.appendChild(title);

    var kicker = document.createElement("span");
    kicker.className = "workspace-kicker";
    kicker.textContent = welcome.domain || "workspace";
    head.appendChild(kicker);
    card.appendChild(head);

    var intro = document.createElement("p");
    intro.className = "workspace-copy";
    intro.textContent = welcome.welcome_message || "Workspace ready.";
    card.appendChild(intro);

    var stats = document.createElement("div");
    stats.className = "workspace-summary";
    stats.appendChild(createStat("User", welcome.user_name || "Unknown"));
    stats.appendChild(createStat("Role", (welcome.user_role || "operator").toUpperCase()));
    stats.appendChild(createStat(
      "Health",
      welcome.health_score != null ? String(welcome.health_score) : "n/a",
      welcome.health_label ? "workspace-stat-health workspace-health-" + String(welcome.health_label).toLowerCase().replace(/\s+/g, "-") : "workspace-stat-health"
    ));
    stats.appendChild(createStat("Target", welcome.target_score != null ? String(welcome.target_score) : "n/a"));
    card.appendChild(stats);

    if (welcome.health_label) {
      var healthBadgeRow = document.createElement("div");
      healthBadgeRow.className = "workspace-health-row";
      healthBadgeRow.appendChild(badge(welcome.health_label, "workspace-health-badge workspace-health-" + String(welcome.health_label).toLowerCase().replace(/\s+/g, "-")));
      card.appendChild(healthBadgeRow);
    }

    if (welcome.objective) {
      var objective = document.createElement("div");
      objective.className = "workspace-section";
      var heading = document.createElement("h4");
      heading.textContent = "Objective";
      objective.appendChild(heading);
      var copy = document.createElement("p");
      copy.className = "workspace-copy";
      copy.textContent = welcome.objective;
      objective.appendChild(copy);
      card.appendChild(objective);
    }

    target.appendChild(card);
    renderDailyBrief(target, welcome.daily_brief);
    renderLearnerSummary(target, welcome.learner_summary);
  }

  function renderVerificationForm(target, coaching) {
    var formWrap = document.createElement("div");
    formWrap.className = "workspace-inline-wrap";

    var form = createInlineMutationForm({
      primaryPlaceholder: "Your answer...",
      secondaryPlaceholder: null,
      submitLabel: "Verify Mastery",
      emptyMessage: "Please provide an answer first.",
      onSubmit: function (answer) {
        return postJson("/v1/missioncanvas/verify-mastery", {
          workspace_id: state.workspaceId,
          concept_id: coaching.concept_id,
          answer: answer
        }).then(function(res) {
          setStatus(res.message || "Concept verified.", "ok");
          return state.refreshWorkspace ? state.refreshWorkspace() : null;
        });
      }
    });

    formWrap.appendChild(form.element);
    target.appendChild(formWrap);
    form.show();
  }

  function renderLearnerSummary(target, learnerSummary) {
    if (!target || !learnerSummary) return;

    var taught = normalizeList(learnerSummary.taught_concepts);
    var progress = normalizeList(learnerSummary.concept_progress);
    if (!taught.length && !progress.length && !learnerSummary.last_taught_concept) return;

    var panel = document.createElement("section");
    panel.className = "workspace-card workspace-learner";

    var head = document.createElement("div");
    head.className = "workspace-card-head";
    var title = document.createElement("h3");
    title.textContent = "Learning State";
    head.appendChild(title);

    if (learnerSummary.teaching_moments != null) {
      head.appendChild(badge(String(learnerSummary.teaching_moments) + " moments", "workspace-health-badge workspace-learner-badge"));
    }
    panel.appendChild(head);

    var stats = document.createElement("div");
    stats.className = "workspace-summary";
    stats.appendChild(createStat("Taught", String(taught.length || 0)));
    stats.appendChild(createStat("Verified", String(normalizeList(learnerSummary.verified_concepts).length || 0)));
    stats.appendChild(createStat("Orient", String((learnerSummary.stage_counts && learnerSummary.stage_counts.orient) || 0)));
    stats.appendChild(createStat("Retain", String((learnerSummary.stage_counts && learnerSummary.stage_counts.retain) || 0)));
    panel.appendChild(stats);

    if (learnerSummary.last_taught_concept) {
      var last = document.createElement("p");
      last.className = "workspace-copy";
      last.innerHTML = "<strong>Last concept:</strong> " + escapeHtml(learnerSummary.last_taught_concept);
      panel.appendChild(last);
    }

    if (progress.length) {
      var list = document.createElement("div");
      list.className = "workspace-section";
      var heading = document.createElement("h4");
      heading.textContent = "Concept Progress";
      list.appendChild(heading);
      var rows = document.createElement("ul");
      rows.className = "workspace-list";
      progress
        .slice()
        .sort(function (a, b) {
          return String(b.last_taught_at || "").localeCompare(String(a.last_taught_at || ""));
        })
        .slice(0, 4)
        .forEach(function (item) {
          var isVerified = normalizeList(learnerSummary.verified_concepts).indexOf(item.concept_id) !== -1;
          var row = document.createElement("li");
          if (isVerified) row.className = "concept-verified";
          row.textContent = (isVerified ? "✓ " : "") + (item.concept_label || item.concept_id || "Concept") +
            " · " + String(item.stage || "orient").toUpperCase() +
            " · taught " + String(item.times_taught || 1) + "x";
          rows.appendChild(row);
        });
      list.appendChild(rows);
      panel.appendChild(list);
    }

    target.appendChild(panel);
  }

  function setStatus(message, level) {
    if (state.setStatus) state.setStatus(message, level || "ok");
  }

  function createInputField(placeholder) {
    var input = document.createElement("input");
    input.type = "text";
    input.className = "workspace-inline-input";
    input.placeholder = placeholder;
    return input;
  }

  function createInlineMutationForm(options) {
    var form = document.createElement("form");
    form.className = "workspace-inline-form hidden";

    var primaryInput = createInputField(options.primaryPlaceholder);
    form.appendChild(primaryInput);

    var secondaryInput = null;
    if (options.secondaryPlaceholder) {
      secondaryInput = createInputField(options.secondaryPlaceholder);
      form.appendChild(secondaryInput);
    }

    var actions = document.createElement("div");
    actions.className = "workspace-inline-actions";

    var submit = document.createElement("button");
    submit.type = "submit";
    submit.className = "workspace-chip workspace-chip-solid";
    submit.textContent = options.submitLabel;
    actions.appendChild(submit);

    var cancel = document.createElement("button");
    cancel.type = "button";
    cancel.className = "workspace-chip";
    cancel.textContent = "Cancel";
    actions.appendChild(cancel);

    form.appendChild(actions);

    cancel.addEventListener("click", function () {
      form.classList.add("hidden");
      form.reset();
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var primaryValue = primaryInput.value.trim();
      var secondaryValue = secondaryInput ? secondaryInput.value.trim() : "";
      if (!primaryValue) {
        setStatus(options.emptyMessage, "warn");
        primaryInput.focus();
        return;
      }
      submit.disabled = true;
      cancel.disabled = true;
      Promise.resolve(options.onSubmit(primaryValue, secondaryValue))
        .then(function () {
          form.classList.add("hidden");
          form.reset();
        })
        .finally(function () {
          submit.disabled = false;
          cancel.disabled = false;
        });
    });

    return {
      element: form,
      show: function () {
        form.classList.remove("hidden");
        primaryInput.focus();
      }
    };
  }

  function postJson(path, payload) {
    return fetch((state.apiBase || "") + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (res) {
      return res.json().then(function (data) {
        if (!res.ok || data.status === "error") {
          var message = (data && (data.message || (data.error && data.error.message))) || "Request failed";
          throw new Error(message);
        }
        return data;
      });
    });
  }

  function mutateWorkspace(path, payload, successMessage) {
    return postJson(path, payload)
      .then(function () {
        setStatus(successMessage, "ok");
        return state.refreshWorkspace ? state.refreshWorkspace() : null;
      })
      .catch(function (error) {
        setStatus(error.message || "Workspace update failed", "error");
        throw error;
      });
  }

  function createResolveControls(node) {
    if (node.node_type !== "missing_evidence" || !node.node_id || !state.workspaceId) return null;

    var wrap = document.createElement("div");
    wrap.className = "workspace-inline-wrap";

    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "workspace-chip";
    toggle.textContent = "Resolve";
    wrap.appendChild(toggle);

    var form = createInlineMutationForm({
      primaryPlaceholder: "Resolution note",
      secondaryPlaceholder: "Artifact path (optional)",
      submitLabel: "Resolve",
      emptyMessage: "Add a short resolution note first.",
      onSubmit: function (resolution, artifactPath) {
        return mutateWorkspace("/v1/missioncanvas/resolve-evidence", {
          workspace_id: state.workspaceId,
          evidence_id: node.node_id,
          resolution: resolution,
          artifact_path: artifactPath || undefined
        }, "Evidence resolved.");
      }
    });
    wrap.appendChild(form.element);

    toggle.addEventListener("click", function () {
      form.show();
    });

    return wrap;
  }

  function createAddFactPanel() {
    if (!state.workspaceId) return null;

    var panel = document.createElement("section");
    panel.className = "workspace-card workspace-add-fact";

    var head = document.createElement("div");
    head.className = "workspace-panel-head";
    var title = document.createElement("h3");
    title.textContent = "Add Fact";
    head.appendChild(title);
    panel.appendChild(head);

    var intro = document.createElement("p");
    intro.className = "workspace-copy";
    intro.textContent = "Record a confirmed fact and refresh the workspace state.";
    panel.appendChild(intro);

    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "workspace-chip";
    toggle.textContent = "Add Fact";
    panel.appendChild(toggle);

    var form = createInlineMutationForm({
      primaryPlaceholder: "Fact",
      secondaryPlaceholder: "Source",
      submitLabel: "Add Fact",
      emptyMessage: "Add the fact text first.",
      onSubmit: function (fact, source) {
        return mutateWorkspace("/v1/missioncanvas/add-fact", {
          workspace_id: state.workspaceId,
          fact: fact,
          source: source || undefined
        }, "Fact added.");
      }
    });
    panel.appendChild(form.element);

    toggle.addEventListener("click", function () {
      form.show();
    });

    return panel;
  }

  var state = {
    apiBase: "",
    workspaceId: null,
    runQuery: null,
    prefillQuery: null,
    refreshWorkspace: null,
    setStatus: null,
    root: null,
    selectorMount: null
  };

  function renderWorkspaceSelector(currentWorkspaceId) {
    if (!state.selectorMount || !currentWorkspaceId) return;
    clear(state.selectorMount);

    var wrap = document.createElement("div");
    wrap.className = "workspace-toolbar";
    var label = document.createElement("label");
    label.textContent = "Workspace";
    label.setAttribute("for", "workspaceSelector");
    wrap.appendChild(label);

    var select = document.createElement("select");
    select.id = "workspaceSelector";
    wrap.appendChild(select);
    state.selectorMount.appendChild(wrap);

    fetch((state.apiBase || "") + "/v1/missioncanvas/workspaces")
      .then(function (res) { return res.json(); })
      .then(function (data) {
        normalizeList(data.workspaces).forEach(function (workspace) {
          var option = document.createElement("option");
          option.value = workspace.id;
          option.textContent = workspace.name || workspace.id;
          option.selected = workspace.id === currentWorkspaceId;
          select.appendChild(option);
        });
      })
      .catch(function () {
        var option = document.createElement("option");
        option.value = currentWorkspaceId;
        option.textContent = currentWorkspaceId;
        option.selected = true;
        select.appendChild(option);
      });

    select.addEventListener("change", function () {
      if (!select.value || select.value === currentWorkspaceId) return;
      window.location.href = "/" + select.value;
    });
  }

  window.WorkspaceUI = {
    init: function (config) {
      state.apiBase = config.apiBase || "";
      state.workspaceId = config.workspaceId || null;
      state.runQuery = config.runQuery || null;
      state.prefillQuery = config.prefillQuery || null;
      state.refreshWorkspace = config.refreshWorkspace || null;
      state.setStatus = config.setStatus || null;
      state.root = $("workspaceUiRoot");
      state.selectorMount = $("workspaceSelectorMount");
      if (!state.workspaceId || !state.root) return;
      renderWorkspaceSelector(state.workspaceId);
    },

    setWorkspace: function (workspaceId) {
      state.workspaceId = workspaceId || null;
      renderWorkspaceSelector(state.workspaceId);
    },

    renderWelcome: function (welcome) {
      if (!state.root || !state.workspaceId || !welcome) return;
      state.root.classList.remove("hidden");
      clear(state.root);
      renderWelcomeSummary(state.root, welcome);
      state.root.appendChild(createAddFactPanel());
      renderNudges(state.root, welcome.nudges, { prefillQuery: state.prefillQuery });
      renderSuggestedQueries(state.root, welcome.suggested_queries, { runQuery: state.runQuery });
    },

    renderNudges: function (nudges) {
      if (!state.root || !state.workspaceId) return;
      renderNudges(state.root, nudges, { prefillQuery: state.prefillQuery });
    },

    renderSuggestedQueries: function (queries) {
      if (!state.root || !state.workspaceId) return;
      renderSuggestedQueries(state.root, queries, { runQuery: state.runQuery });
    },

    renderChain: function (response) {
      if (!state.root || !state.workspaceId) return;
      if (!response || !response.convergence_chain) return;

      state.root.classList.remove("hidden");
      clear(state.root);
      state.root.appendChild(createNarrationBlock(response.convergence_chain));
      renderTree(state.root, response.convergence_chain.data && response.convergence_chain.data.chains);
      state.root.appendChild(createAddFactPanel());
      renderNudges(state.root, response.convergence_chain.nudges, { prefillQuery: state.prefillQuery });
      renderSuggestedQueries(state.root, response.suggested_questions, { runQuery: state.runQuery });
    },

    renderCoaching: function (response) {
      if (!state.root || !state.workspaceId || !response || !response.coaching) return;
      state.root.classList.remove("hidden");
      clear(state.root);
      renderCoachingPanel(state.root, response);
      state.root.appendChild(createAddFactPanel());
      renderSuggestedQueries(state.root, response.suggested_questions, { runQuery: state.runQuery });
    }
  };
})();
