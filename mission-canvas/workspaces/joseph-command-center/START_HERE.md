# Joseph Command Center — START HERE

This package is the focused setup layer for Joseph's broader Palette workspace.

It does **not** replace the existing `oil-investor` workspace. It creates a cleaner command-center path around Joseph himself: his priorities, his source folders, his preferred surfaces, and the artifacts he actually wants to wake up to.

## What This Is

This folder gives Joseph:

- a new configurable workspace: `joseph-command-center`
- a local-only onboarding lens prompt
- a step-by-step setup checklist
- a valid Mission Canvas workspace route he can use immediately

The goal is simple:

**make Palette feel like Joseph's workspace, not just a demo or a single-domain bot**

## Quick Start

### 1. Open the package

Work in this directory:

`palette/mission-canvas/workspaces/joseph-command-center/`

### 2. Run the onboarding lens session

Open Claude Code in this directory and paste:

`palette/lenses/onboarding/ONBOARD_JOSEPH_COMMAND_CENTER.md`

That session should produce:

- `lens.yaml` — local-only full context
- `profile.md` — sanitized workspace summary
- recommended edits to `config.yaml` and `project_state.yaml`

### 3. Follow the setup checklist

Use:

- [SETUP_CHECKLIST.md](./SETUP_CHECKLIST.md)

Do not skip the source-map and front-door decisions. Those are what make this actually customized.

### 4. Open the workspace

If Mission Canvas is already running locally, open:

- `http://127.0.0.1:8787/joseph-command-center`

If you are already inside the Palette Mission Canvas server on another host, use:

- `/<workspace_id>` with `workspace_id = joseph-command-center`

### 5. Keep the existing investor workspace intact

If Joseph already uses:

- `oil-investor`

keep using it for the investment-specific flow until you decide whether to:

- leave it separate
- link it from this workspace
- or slowly migrate parts of it here

That is an explicit setup decision in this package.

## What Must Be True Before This Feels Real

This package is not "done" when the route loads.

It is only done when:

1. Joseph's live priorities are captured.
2. His local document folders are mapped.
3. The primary front door is chosen.
4. Startup artifacts are tuned to his actual workflow.
5. The first monitor loop is turned on without creating noise.

## Package Contents

- [config.yaml](./config.yaml)
- [project_state.yaml](./project_state.yaml)
- [learner_lens.yaml](./learner_lens.yaml)
- [SETUP_CHECKLIST.md](./SETUP_CHECKLIST.md)
- [../../lenses/onboarding/ONBOARD_JOSEPH_COMMAND_CENTER.md](../../lenses/onboarding/ONBOARD_JOSEPH_COMMAND_CENTER.md)

## Recommended Demo Framing

When showing this to Joseph, say:

> This is the broader workspace around you. The old oil workspace can stay exactly where it is. This package is about turning Palette into the system that knows your priorities, your files, your preferred surfaces, and what you want the system to produce first.
