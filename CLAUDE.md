@AGENTS.md

# Claude Code routing

Claude imports the shared map. Load only relevant `.claude/skills/*/SKILL.md`, delegated `.claude/agents/*.md`, and [the adapter](adapters/claude.md); shared files remain authoritative.

Before any harness workflow, apply the imported `direct-trivial` gate. A localized color, spacing, typo, or static-label edit with no behavior/rule/state/contract/data/risk is edited directly: no interview, SPEC, graph, TDD, review, or full status ceremony.

For a new capability with open choices, automatically load `.claude/skills/feature-discovery/SKILL.md`; the user need not name it. Resolve actors, access/authentication, failure/recovery, data, risks, and acceptance before pending or graph changes.

For non-trivial implementation load `writing-plans`; for behavior/bugs load `test-driven-task`. Dispatch two-to-five-minute specs; require meaningful RED, GREEN with the same focused test, and proportional regression. Replan instead of improvising or faking RED.

Follow [REVIEW-ROUNDS.md](docs/REVIEW-ROUNDS.md). After verification, launch `independent-reviewer` in a fresh supported context. It reviews the SPEC—not prompt or memory—before code; assurance is non-blocking with one initial plus one focused re-review.

Except direct-trivial closeout, progress follows [STATUS-AND-COMPLETION.md](docs/STATUS-AND-COMPLETION.md), joining `PENDING.md` with `TASK-GRAPH.md`. Passing tasks are marked completed and advance. Never assume hooks, MCP, network, secrets, destructive permissions, or integrations.
