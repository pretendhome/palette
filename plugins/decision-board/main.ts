import {
	App,
	debounce,
	ItemView,
	MarkdownPostProcessorContext,
	Modal,
	Notice,
	Platform,
	Plugin,
	PluginSettingTab,
	Setting,
	TFile,
	WorkspaceLeaf
} from "obsidian";

import {
	Decoration,
	DecorationSet,
	EditorView,
	WidgetType
} from "@codemirror/view";

import { EditorState, StateField } from "@codemirror/state";

// ────────────────────────────────────────────
// Constants & Types
// ────────────────────────────────────────────

const VIEW_TYPE = "decision-board";
type Status = "open" | "thinking" | "decided";
const VALID: Status[] = ["open", "thinking", "decided"];

interface DecisionState {
	status: Status;
	next_action: string;
	known: string[];
	missing: string[];
	updated: string;
}

interface Settings {
	enableRibbon: boolean;
	showBadge: boolean;
	showStatusBar: boolean;
	showBanner: boolean;
}

const DEFAULTS: Settings = { enableRibbon: true, showBadge: true, showStatusBar: true, showBanner: true };

// ────────────────────────────────────────────
// Utilities
// ────────────────────────────────────────────

function now(): string { return new Date().toISOString(); }
function label(s: Status): string { return s === "open" ? "Open" : s === "thinking" ? "Thinking" : "Decided"; }

// ────────────────────────────────────────────
// Frontmatter
// ────────────────────────────────────────────

function read(app: App, file: TFile): DecisionState | null {
	const fm = app.metadataCache.getFileCache(file)?.frontmatter;
	if (!fm?.status || !VALID.includes(fm.status)) return null;
	return {
		status: fm.status as Status,
		next_action: typeof fm.next_action === "string" ? fm.next_action : "",
		known: Array.isArray(fm.known) ? fm.known.map(String) : [],
		missing: Array.isArray(fm.missing) ? fm.missing.map(String) : [],
		updated: typeof fm.updated === "string" ? fm.updated : now(),
	};
}

async function write(app: App, file: TFile, s: DecisionState): Promise<void> {
	const cur = app.metadataCache.getFileCache(file)?.frontmatter;
	if (cur?.updated && new Date(cur.updated) > new Date(s.updated)) {
		new Notice("Decision updated elsewhere. Refresh."); return;
	}
	await app.fileManager.processFrontMatter(file, (fm) => {
		fm.status = s.status;
		fm.next_action = s.next_action;
		fm.known = s.known.filter(Boolean);
		fm.missing = s.missing.filter(Boolean);
		fm.updated = now();
	});
}

// ────────────────────────────────────────────
// CM6 Badge
// ────────────────────────────────────────────

class Badge extends WidgetType {
	constructor(readonly status: Status) { super(); }
	toDOM(): HTMLElement {
		const el = document.createElement("span");
		el.className = `db-badge db-badge-${this.status}`;
		el.textContent = label(this.status);
		return el;
	}
	eq(o: Badge): boolean { return this.status === o.status; }
}

function parseStatus(doc: string): Status | null {
	if (!doc.startsWith("---")) return null;
	const end = doc.indexOf("\n---", 3);
	if (end === -1) return null;
	const m = doc.substring(0, end).match(/^status:\s*(\w+)/m);
	return m && VALID.includes(m[1] as Status) ? m[1] as Status : null;
}

// Badge visibility — controlled by settings, toggled via EditorExtension array swap
let badgeEnabled = true;
let editorExtArray: (typeof statusField | typeof decoField)[] = [];

function buildDecos(state: EditorState): DecorationSet {
	if (!badgeEnabled) return Decoration.none;
	const s = state.field(statusField);
	if (!s) return Decoration.none;
	const doc = state.doc.toString();
	const end = doc.indexOf("\n---", 3);
	if (end === -1) return Decoration.none;
	const line = state.doc.lineAt(end + 1);
	return Decoration.set([
		Decoration.widget({ widget: new Badge(s), side: 1, block: true }).range(line.to)
	]);
}

const statusField = StateField.define<Status | null>({
	create(s) { return parseStatus(s.doc.toString()); },
	update(v, tr) { return tr.docChanged ? parseStatus(tr.state.doc.toString()) : v; },
});

const decoField = StateField.define<DecorationSet>({
	create(s) { return buildDecos(s); },
	update(v, tr) { return tr.docChanged ? buildDecos(tr.state) : v; },
	provide(f) { return EditorView.decorations.from(f); }
});

// ────────────────────────────────────────────
// Sidebar
// ────────────────────────────────────────────

class BoardView extends ItemView {
	private plugin: DecisionBoardPlugin;
	constructor(leaf: WorkspaceLeaf, plugin: DecisionBoardPlugin) { super(leaf); this.plugin = plugin; }
	getViewType() { return VIEW_TYPE; }
	getDisplayText() { return "Decision Board"; }
	getIcon() { return "check-circle"; }

	async onOpen() {
		this.registerEvent(this.app.workspace.on("file-open", () => this.render()));
		this.registerEvent(this.app.metadataCache.on("changed", (f) => {
			if (f === this.app.workspace.getActiveFile()) this.render();
		}));
		this.render();
	}

	render() {
		const el = this.containerEl.children[1] as HTMLElement;
		el.empty();
		el.addClass("db-board");

		const file = this.app.workspace.getActiveFile();
		if (!file) { el.createEl("p", { cls: "db-empty", text: "Open a note to begin." }); return; }

		const state = read(this.app, file);
		if (!state) {
			const w = el.createDiv({ cls: "db-empty-state" });
			w.createEl("p", { text: "What is this note trying to decide?" });
			w.createEl("p", { cls: "db-hint", text: "Track what you know, what's unclear, and what happens next." });
			const btn = w.createEl("button", { text: "Start thinking", cls: "mod-cta" });
			btn.addEventListener("click", async () => {
				await write(this.app, file, { status: "open", next_action: "", known: [], missing: [], updated: now() });
			});
			return;
		}

		// Status selector
		const bar = el.createDiv({ cls: "db-status-bar" });
		for (const s of VALID) {
			const seg = bar.createEl("button", { text: label(s), cls: `db-status-seg ${state.status === s ? "is-active" : ""}` });
			seg.dataset.status = s;
			seg.addEventListener("click", async () => {
				if (s === "decided" && state.status !== "decided") {
					new ConfirmModal(this.app, async () => { state.status = "decided"; await write(this.app, file, state); }).open();
				} else { state.status = s; await write(this.app, file, state); }
			});
		}

		// Known list
		this.renderList(el, "What do you know?", state.known, file, state);
		// Missing list
		this.renderList(el, "What's still unclear?", state.missing, file, state);

		// Next action
		const row = el.createDiv({ cls: "db-field" });
		row.createEl("label", { text: "What happens next?" });
		const input = row.createEl("input", { cls: "db-input" }) as HTMLInputElement;
		input.type = "text"; input.value = state.next_action; input.placeholder = "Next step...";
		input.addEventListener("blur", async () => {
			if (input.value !== state.next_action) { state.next_action = input.value; await write(this.app, file, state); }
		});
		input.addEventListener("keydown", (e: KeyboardEvent) => { if (e.key === "Enter") input.blur(); });

		// Timestamp
		el.createEl("div", { cls: "db-timestamp", text: `Updated: ${new Date(state.updated).toLocaleString()}` });
	}

	private renderList(parent: HTMLElement, title: string, items: string[], file: TFile, state: DecisionState) {
		const sec = parent.createDiv({ cls: "db-list-section" });
		const hdr = sec.createDiv({ cls: "db-list-header" });
		hdr.createEl("label", { text: `${title} (${items.length})` });
		const addBtn = hdr.createEl("button", { text: "+", cls: "db-add-btn clickable-icon" });
		addBtn.addEventListener("click", () => { items.push(""); this.render(); });

		const list = sec.createDiv({ cls: "db-list" });
		items.forEach((item, i) => {
			const row = list.createDiv({ cls: "db-list-item" });
			const inp = row.createEl("input", { cls: "db-input" }) as HTMLInputElement;
			inp.type = "text"; inp.value = item; inp.placeholder = "Add item...";
			inp.addEventListener("blur", async () => {
				if (inp.value !== items[i]) { items[i] = inp.value; await write(this.app, file, state); }
			});
			inp.addEventListener("keydown", (e: KeyboardEvent) => { if (e.key === "Enter") inp.blur(); });
			const del = row.createEl("button", { text: "×", cls: "db-del-btn clickable-icon" });
			del.addEventListener("click", async () => { items.splice(i, 1); await write(this.app, file, state); });
		});
	}
}

// ────────────────────────────────────────────
// Modals
// ────────────────────────────────────────────

class ConfirmModal extends Modal {
	private onConfirm: () => Promise<void>;
	constructor(app: App, onConfirm: () => Promise<void>) { super(app); this.onConfirm = onConfirm; }
	onOpen() {
		this.contentEl.createEl("h3", { text: "Mark as Decided" });
		this.contentEl.createEl("p", { text: "This records your decision. Are you sure?" });
		new Setting(this.contentEl)
			.addButton((b) => b.setButtonText("Decide").setCta().onClick(async () => { await this.onConfirm(); this.close(); }))
			.addButton((b) => b.setButtonText("Cancel").onClick(() => this.close()));
	}
}

class OverviewModal extends Modal {
	onOpen() {
		const { contentEl } = this;
		contentEl.addClass("db-overview");
		contentEl.createEl("h2", { text: "All Decisions" });

		const files = this.app.vault.getMarkdownFiles();
		const grouped: Record<Status, { file: TFile; state: DecisionState }[]> = { open: [], thinking: [], decided: [] };
		const sevenDaysAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
		let stale = 0;

		for (const f of files) {
			const s = read(this.app, f);
			if (!s) continue;
			grouped[s.status].push({ file: f, state: s });
			if (s.status !== "decided" && new Date(s.updated).getTime() < sevenDaysAgo) stale++;
		}

		const total = grouped.open.length + grouped.thinking.length + grouped.decided.length;
		const stats = contentEl.createDiv({ cls: "db-overview-stats" });
		stats.createEl("span", { text: `${total} tracked` });
		if (stale > 0) stats.createEl("span", { cls: "db-stale", text: `${stale} stale (>7 days)` });

		for (const status of VALID) {
			const entries = grouped[status];
			if (!entries.length) continue;
			const sec = contentEl.createDiv({ cls: "db-overview-group" });
			sec.createEl("h3", { text: `${label(status)} (${entries.length})` });
			for (const { file, state } of entries) {
				const row = sec.createDiv({ cls: "db-overview-row" });
				const link = row.createEl("a", { text: file.basename, cls: "db-overview-link" });
				link.addEventListener("click", () => { this.app.workspace.openLinkText(file.path, ""); this.close(); });
				if (state.next_action) row.createEl("span", { cls: "db-overview-next", text: state.next_action });
			}
		}

		if (total === 0) contentEl.createEl("p", { cls: "db-empty", text: "No notes with decisions yet." });
	}
}

// ────────────────────────────────────────────
// Settings
// ────────────────────────────────────────────

class SettingsTab extends PluginSettingTab {
	private plugin: DecisionBoardPlugin;
	constructor(app: App, plugin: DecisionBoardPlugin) { super(app, plugin); this.plugin = plugin; }
	display() {
		const { containerEl: c } = this;
		c.empty();
		c.createEl("h2", { text: "Decision Board" });
		new Setting(c).setName("Ribbon icon").setDesc("Show icon to open the board.")
			.addToggle((t) => t.setValue(this.plugin.settings.enableRibbon).onChange(async (v) => { this.plugin.settings.enableRibbon = v; await this.plugin.saveSettings(); this.plugin.updateRibbon(); }));
		new Setting(c).setName("Editor badge").setDesc("Show status badge in the editor.")
			.addToggle((t) => t.setValue(this.plugin.settings.showBadge).onChange(async (v) => {
				this.plugin.settings.showBadge = v;
				badgeEnabled = v;
				editorExtArray.length = 0;
				if (v) editorExtArray.push(statusField, decoField);
				this.plugin.app.workspace.updateOptions();
				await this.plugin.saveSettings();
			}));
		new Setting(c).setName("Status bar").setDesc("Show decision status in the status bar.")
			.addToggle((t) => t.setValue(this.plugin.settings.showStatusBar).onChange(async (v) => { this.plugin.settings.showStatusBar = v; await this.plugin.saveSettings(); this.plugin.renderStatusBar(); }));
		new Setting(c).setName("Reading view banner").setDesc("Show status banner at the top of notes in reading view.")
			.addToggle((t) => t.setValue(this.plugin.settings.showBanner).onChange(async (v) => { this.plugin.settings.showBanner = v; await this.plugin.saveSettings(); }));
	}
}

// ────────────────────────────────────────────
// Main Plugin
// ────────────────────────────────────────────

export default class DecisionBoardPlugin extends Plugin {
	settings: Settings = DEFAULTS;
	private ribbonEl: HTMLElement | null = null;
	private statusBarEl: HTMLElement | null = null;

	async onload() {
		await this.loadSettings();
		badgeEnabled = this.settings.showBadge;
		this.registerView(VIEW_TYPE, (leaf) => new BoardView(leaf, this));
		this.updateRibbon();

		// Status bar
		this.statusBarEl = this.addStatusBarItem();
		this.statusBarEl.addClass("db-statusbar");
		const upd = debounce(() => this.renderStatusBar(), 200, true);
		this.registerEvent(this.app.workspace.on("file-open", () => upd()));
		this.registerEvent(this.app.metadataCache.on("changed", () => upd()));

		// CM6 — use mutable array so badge toggle triggers live reconfiguration
		editorExtArray = this.settings.showBadge ? [statusField, decoField] : [];
		this.registerEditorExtension(editorExtArray);

		// Reading view banner
		this.registerMarkdownPostProcessor((el, ctx) => {
			if (!this.settings.showBanner) return;
			const info = ctx.getSectionInfo(el);
			if (!info || info.lineStart !== 0) return;
			const file = this.app.vault.getAbstractFileByPath(ctx.sourcePath);
			if (!(file instanceof TFile)) return;
			const state = read(this.app, file);
			if (!state) return;
			const banner = document.createElement("div");
			banner.className = `db-banner db-badge-${state.status}`;
			banner.textContent = [label(state.status), state.missing.length > 0 ? `${state.missing.length} unclear` : null, state.next_action || null].filter(Boolean).join(" · ");
			banner.addEventListener("click", () => this.activateView());
			el.prepend(banner);
		});

		// Code block processor
		this.registerMarkdownCodeBlockProcessor("decision", (source, el) => {
			el.addClass("db-card");
			for (const line of source.trim().split("\n")) {
				const m = line.match(/^(\w[\w_]*):\s*(.*)$/);
				if (m) {
					const row = el.createDiv({ cls: "db-card-row" });
					row.createEl("strong", { text: m[1] + ": " });
					row.createEl("span", { text: m[2] });
				}
				const li = line.match(/^\s*-\s+(.+)$/);
				if (li) el.createDiv({ cls: "db-card-item", text: `  • ${li[1]}` });
			}
		});

		// Commands
		this.addCommand({ id: "open-board", name: "Open Decision Board", callback: () => this.activateView() });
		this.addCommand({ id: "vault-overview", name: "All Decisions", callback: () => new OverviewModal(this.app).open() });
		this.addCommand({
			id: "cycle-status", name: "Cycle status",
			callback: async () => {
				const file = this.app.workspace.getActiveFile();
				if (!file) { new Notice("Open a note first."); return; }
				const state = read(this.app, file);
				if (!state) { new Notice("No decision on this note."); return; }
				const next = VALID[(VALID.indexOf(state.status) + 1) % VALID.length];
				if (next === "decided") {
					new ConfirmModal(this.app, async () => { state.status = "decided"; await write(this.app, file, state); new Notice("Decided."); }).open();
				} else { state.status = next; await write(this.app, file, state); new Notice(label(next)); }
			}
		});
		this.addCommand({
			id: "mark-decided", name: "Mark as Decided",
			callback: () => {
				const file = this.app.workspace.getActiveFile();
				if (!file) { new Notice("Open a note first."); return; }
				new ConfirmModal(this.app, async () => {
					const s = read(this.app, file) ?? { status: "open" as Status, next_action: "", known: [], missing: [], updated: now() };
					s.status = "decided"; await write(this.app, file, s); new Notice("Decided.");
				}).open();
			}
		});

		this.addSettingTab(new SettingsTab(this.app, this));
	}

	async onunload() { this.app.workspace.detachLeavesOfType(VIEW_TYPE); }

	updateRibbon() {
		if (this.ribbonEl) { this.ribbonEl.remove(); this.ribbonEl = null; }
		if (this.settings.enableRibbon) this.ribbonEl = this.addRibbonIcon("check-circle", "Decision Board", () => this.activateView());
	}

	async activateView() {
		const existing = this.app.workspace.getLeavesOfType(VIEW_TYPE);
		if (existing.length) { this.app.workspace.revealLeaf(existing[0]); return; }
		const leaf = Platform.isMobile ? this.app.workspace.getLeaf(true) : this.app.workspace.getRightLeaf(false);
		if (!leaf) return;
		await leaf.setViewState({ type: VIEW_TYPE, active: true });
		this.app.workspace.revealLeaf(leaf);
	}

	renderStatusBar() {
		if (!this.statusBarEl) return;
		this.statusBarEl.empty();
		if (!this.settings.showStatusBar) return;
		const file = this.app.workspace.getActiveFile();
		if (!file) return;
		const state = read(this.app, file);
		if (!state) return;
		this.statusBarEl.createSpan({ cls: `db-statusbar-badge db-badge-${state.status}`, text: label(state.status) });
	}

	async loadSettings() { this.settings = Object.assign({}, DEFAULTS, await this.loadData()); }
	async saveSettings() { await this.saveData(this.settings); }
}
