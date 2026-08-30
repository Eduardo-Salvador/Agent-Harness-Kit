@AGENTS.md

# Claude Code routing

Claude imports the shared map. Load relevant `.claude/skills/`, `.claude/agents/`, and [the adapter](adapters/claude.md).

Before any Harness workflow, load `.claude/skills/request-router/SKILL.md`. Route deterministically to `direct-trivial`, `vibe`, `graph-only`, or `full-harness`; use economical AI only for ambiguity. Explicit full wins, hard triggers override fast lanes, and unresolved ambiguity falls back to full. Vibe permits one small local behavior change with zero artifacts and no mandatory RED, but requires a focused check and promotes on growth or failure.

For a new capability with open choices, automatically load `.claude/skills/feature-discovery/SKILL.md`; the user need not name it. Resolve failure/recovery before pending or graph changes.

For full-harness work load `writing-plans`; use two-to-five-minute specs and replan instead of improvising. For full-harness behavior/bugs load `test-driven-task`; require meaningful RED, GREEN with the same focused test, proportional regression, and no faking RED.

For `handoff-review`, use a fresh reviewer, [REVIEW-ROUNDS.md](docs/REVIEW-ROUNDS.md), and SPEC authority—not prompt/conversation memory. Assurance is non-blocking.

Graph/full progress reads `PENDING.md` and `TASK-GRAPH.md`, follows [STATUS-AND-COMPLETION.md](docs/STATUS-AND-COMPLETION.md), marks passing tasks completed, and keeps assurance non-blocking. Fast lanes return concise checked closeouts.
