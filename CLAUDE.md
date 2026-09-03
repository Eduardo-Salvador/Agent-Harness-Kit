@AGENTS.md

# Claude Code routing

On an uninitialized project's first response, including a greeting-only "oi"/"hello", begin visibly with the localized Kit-active welcome, then ask the delivery-mode preference (accompanied by default, autonomous, or hackathon) in the same cohesive kickoff question as any missing product intent. Asking correct discovery questions does not replace the welcome. Never repeat the welcome or mode question when context is approved or the choice is already explicit. See the [first-run gate](harness/playbooks/first-run.md); read-only audits and eligible fast edits remain exempt.

Claude imports the shared map. Load relevant `.claude/skills/`, `.claude/agents/`, and [the adapter](adapters/claude.md).

Before mutating work or Harness ceremony, load `.claude/skills/request-router/SKILL.md`. Keep the four public lanes and separately assign assurance `none|light|full`. Full Harness is automatic only for two or more real agents, a human loop, required audit, insufficient model capability, unresolved consequential ambiguity, or explicit full; actual security/privacy/authorization/destructive changes require full audit, while API/dependency keywords alone do not. Read-only audits and diagnosis do not trigger first-run.

When graph expansion exposes an unresolved functionality or completion condition, ask through feature discovery before readiness; use `scope_status: needs-discovery` for existing unresolved nodes. Initial context approval never grants blanket authority over later scope.

For a new capability with open choices, automatically load `.claude/skills/feature-discovery/SKILL.md`; the user need not name it. Resolve failure/recovery before pending or graph changes.

Follow [accompanied delivery](docs/ACCOMPANIED-DELIVERY.md): product builds pause at the first usable slice and material capabilities for actual client evaluation; affected work waits on `product_requires`, while unrelated authorized work may continue. Every new spec states explicit completion conditions, mirrored in `acceptance_criteria` with current observed verification evidence. Technical completion is not client approval. Small fixes remain continuous.

Use [delivery modes](docs/DELIVERY-MODES.md): default accompanied, explicit autonomous end-to-end inside approved scope, or timeboxed hackathon with first-demo evaluation. Persist the choice in project context and preserve it on resume. No mode bypasses evidence or existing gates, restricts worker count by itself, or activates learning.

For planned work load `writing-plans`; target 15–30 active minutes per unit and justify exceptions. Full Harness may be compact or complete. Same-context inline nodes use an inline spec/transition; create handoff/review packets only for actual separate consumers. For full-Harness behavior/bugs load `test-driven-task` and climb the test ladder only as needed.

For `assurance: light|full`, use a fresh reviewer, [REVIEW-ROUNDS.md](docs/REVIEW-ROUNDS.md), and SPEC authority—not prompt/conversation memory. `none` closes on executor verification.

Graph/full progress reads `PENDING.md` and `TASK-GRAPH.md`, follows [STATUS-AND-COMPLETION.md](docs/STATUS-AND-COMPLETION.md), marks passing tasks completed, and keeps assurance non-blocking. Fast lanes return concise checked closeouts.
