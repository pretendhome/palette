# OpenAI Takehome Handoff

Date: 2026-03-11
Purpose: Fast recovery note for the next Codex session after restart.

## Immediate Situation

The user is in an OpenAI interview process for the `AI Deployment Manager - San Francisco` role and expects an upcoming skills-based assessment / take-home.

The active objective is:
- use Palette to turn the prompt into a high-quality submission under deadline pressure
- avoid overbuilding process
- optimize for a serious Technical Success operator artifact, not "impressive" candidate theater

## Start Here Next Session

1. Re-read this file.
2. Re-read `/home/mical/fde/.codex/MESSAGE_TO_FUTURE_CODEX.md`
3. Open these Palette/OpenAI artifacts:
   - `/home/mical/fde/implementations/talent/talent-openai-deployment-mgr/OPENAI_TEST_FACTORY_SYSTEM_2026-03-10.md`
   - `/home/mical/fde/palette/workflows/openai_takehome_factory.yaml`
   - `/home/mical/fde/palette/skills/talent/openai-takehome-execution.md`
   - `/home/mical/fde/palette/lenses/releases/v0/LENS-INT-002_openai_takehome_grader.yaml`

## What Was Built

Reusable Palette assets created:
- workflow: `WF-INT-001` at `/home/mical/fde/palette/workflows/openai_takehome_factory.yaml`
- skill: `SKILL-INT-001` at `/home/mical/fde/palette/skills/talent/openai-takehome-execution.md`
- lens: `LENS-INT-002` at `/home/mical/fde/palette/lenses/releases/v0/LENS-INT-002_openai_takehome_grader.yaml`

Role-specific operating brief:
- `/home/mical/fde/implementations/talent/talent-openai-deployment-mgr/OPENAI_TEST_FACTORY_SYSTEM_2026-03-10.md`

## Key Decisions Already Made

- Do NOT redesign Palette around coding-benchmark architectures.
- Only import useful HYDRA ideas:
  - evaluator-first thinking
  - prompt classification
  - adversarial reviewer questions
  - rubber-duck explanation
- Keep the system lightweight enough for real take-home deadlines.
- Use standard mode by default, compressed mode when deadline/format demands it.

## Important Context

- `PERPLEXITY_API_KEY` is set in the environment.
- Palette `researcher.py` was successfully run against live Perplexity after network escalation.
- `ANTHROPIC_API_KEY` was not set during the prior session, so researcher synthesis used raw Perplexity output rather than Claude post-synthesis.
- Official baseline source confirmed: `https://openai.com/interview-guide/`
- Official role page confirmed: `https://openai.com/careers/ai-deployment-manager-san-francisco/`
- Codex voice-related flags are enabled in `/home/mical/.codex/config.toml`:
  - `features.voice_transcription = true`
  - `features.realtime_conversation = true`
- Native push-to-talk transcription is the default voice path to test first.
- `/realtime` is a separate mode and may require API key auth; do not rely on it for the take-home workflow unless explicitly verified in-session.

## Voice Workflow

Use voice when it increases speed or clarity:
- ideation
- mock interview rehearsal
- outlining responses
- first-pass take-home framing

Do not force voice when precision matters more than speed:
- final artifact editing
- exact file/path changes
- structured YAML/JSON edits
- final answer polish

Practical sequence:
1. Start Codex.
2. Test native push-to-talk in the composer first.
3. Use voice for framing, tradeoff narration, and rehearsal.
4. Switch to typing for exact implementation, patching, and final submission shaping.

## How To Resume When The Test Arrives

1. Paste the exact prompt into the session.
2. Create/update a convergence brief immediately.
3. Use the workflow classifier in `openai_takehome_factory.yaml` to choose `standard` or `compressed`.
4. Run the workflow in order:
   - convergence
   - research
   - architecture
   - build
   - narrative
   - validation
   - remediation if needed
   - monitor
   - defense
   - final human review

## Guardrails

- Requirement coverage beats cleverness.
- If the process starts becoming larger than the deliverable, switch to compressed mode.
- The thesis must name the core tension.
- The first 60 seconds of reviewer experience matter.
- Every major claim must survive follow-up discussion.

## Do Not Forget

The user explicitly wants execution quality and speed once the take-home lands. Do not restart broad research unless the prompt creates a real unknown.
