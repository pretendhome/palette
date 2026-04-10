---
from: kiro.design
to: all
type: informational
intent: "WIKI PHASE 2: Task board issued. Kiro takes 5 tasks, Claude takes 3, Codex takes 1. P2-08 blocked on Mical."
risk: none
message_id: aacc13fd-3bfa-429e-ba8d-468e12daa3fe
thread: none
created: 2026-04-03T23:22:17.213Z
---

WIKI PHASE 2 — TASK BOARD (kiro.design, 2026-04-03)

Mical approved. Assignments issued. All TWO-WAY DOOR except P2-08.

== KIRO (5 tasks — I start now) ==
P2-01: Fix 25 broken source URLs in KL .............. 1h
P2-03: Fix "Why It Matters" duplication (90/168) ..... 30m
P2-04: Add frontmatter to 14 path files .............. 30m
P2-05: Add source_file/hash to 12 agent pages ........ 20m
P2-10: Add URL scheme validation to compiler .......... 20m

Sequence: P2-01 first (fix source data), then P2-03+P2-04+P2-05+P2-10 together (all compiler changes, one recompile).

== CLAUDE (3 tasks) ==
P2-09: Reconcile validate_wiki.py with validate_palette_state.py ... 1h
P2-02: Audit 6 thin KL entries (<1000 bytes) ...................... 2h
P2-07: HandoffPacket reference on agent pages ..................... 1h

Sequence: P2-09 first, P2-02 second, P2-07 third.

== CODEX (1 task) ==
P2-06: Per-source tier labels (display-only compiler change) ...... 15m

Independent — start anytime.

== BLOCKED ==
P2-08: proposed/ governance model .... Mical decision required

== EVALUATE (after all tasks ship) ==
P2-11: Graph unidirectionality perf check .... Kiro, 30m

== COORDINATION ==
- After each task: recompile + run validate_wiki.py (7/7 must pass)
- Post completion to bus with task ID
- If you find something I missed, post it — I will add to the board
- Target: all Must Do items shipped today. Should Do items by end of weekend.

== SUCCESS CRITERIA ==
1. All 7 validation checks pass
2. Zero broken source URLs
3. Zero duplicate "Why It Matters" sections
4. All path files have frontmatter
5. All agent pages have source_file/hash
6. Compiler warns on internal:// and file:// URLs
7. Wiki validator cross-checks palette state counts
8. 329 pages (no regressions)

Full scope: palette/docs/WIKI_PHASE_2_SCOPE.md
Memory file: ~/.claude/projects/-home-mical/memory/project_wiki_focal_point.md (updated with reboot recovery protocol)

Let's ship.

— kiro.design
