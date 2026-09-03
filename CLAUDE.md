@AGENTS.md

# Claude Code routing

Claude imports the shared map. Load relevant `.claude/skills/`, `.claude/agents/`, and [the adapter](adapters/claude.md).

Before mutating work or Harness ceremony, load `.claude/skills/request-router/SKILL.md`. Keep the four public lanes and separately assign assurance `none|light|full`. Full Harness is automatic only for two or more real agents, a human loop, required audit, insufficient model capability, unresolved consequential ambiguity, or explicit full; actual security/privacy/authorization/destructive changes require full audit, while API/dependency keywords alone do not. Read-only audits and diagnosis do not trigger first-run.

When graph expansion exposes an unresolved functionality or completion condition, ask through feature discovery before readiness; use `scope_status: needs-discovery` for existing unresolved nodes. Initial context approval never grants blanket authority over later scope.

For a new capability with open choices, automatically load `.claude/skills/feature-discovery/SKILL.md`; the user need not name it. Resolve failure/recovery before pending or graph changes.

Follow [accompanied delivery](docs/ACCOMPANIED-DELIVERY.md): product builds pause at the first usable slice and material capabilities for actual client evaluation; affected work waits on `product_requires`, while unrelated authorized work may continue. Every new spec states explicit completion conditions, mirrored in `acceptance_criteria` with current observed verification evidence. Technical completion is not client approval. Small fixes remain continuous.

For planned work load `writing-plans`; target 15–30 active minutes per unit and justify exceptions. Full Harness may be compact or complete. Same-context inline nodes use an inline spec/transition; create handoff/review packets only for actual separate consumers. For full-Harness behavior/bugs load `test-driven-task` and climb the test ladder only as needed.

For `assurance: light|full`, use a fresh reviewer, [REVIEW-ROUNDS.md](docs/REVIEW-ROUNDS.md), and SPEC authority—not prompt/conversation memory. `none` closes on executor verification.

Graph/full progress reads `PENDING.md` and `TASK-GRAPH.md`, follows [STATUS-AND-COMPLETION.md](docs/STATUS-AND-COMPLETION.md), marks passing tasks completed, and keeps assurance non-blocking. Fast lanes return concise checked closeouts.
