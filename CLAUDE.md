@AGENTS.md

# Claude Code routing

Claude imports the shared map. Load only relevant `.claude/skills/`, `.claude/agents/`, and [the adapter](adapters/claude.md).

Before any harness workflow, apply `direct-trivial`. A localized static/presentation edit with no behavior, contract, data, or risk has no interview, SPEC, graph, TDD, review, or full status ceremony.

For a new capability with open choices, automatically load `.claude/skills/feature-discovery/SKILL.md`; the user need not name it. Resolve failure/recovery before pending or graph changes.

For non-trivial work load `writing-plans`; use two-to-five-minute specs and replan instead of improvising. For behavior/bugs load `test-driven-task`; require meaningful RED, GREEN with the same focused test, proportional regression, and no faking RED.

Long windows naturally slow all models. Resume fresh from durable context, `PENDING.md`, and the active `TASK-GRAPH.md` neighborhood. Eligible `graph-only` work stores only its checked graph transition.

For `handoff-review`, launch a fresh independent reviewer after verification. It follows [REVIEW-ROUNDS.md](docs/REVIEW-ROUNDS.md) from the SPEC and rejects the original prompt or conversation memory as authority. Assurance is non-blocking.

Progress follows [STATUS-AND-COMPLETION.md](docs/STATUS-AND-COMPLETION.md). Join pending with graph state, mark passing tasks completed, and never assume capabilities or authority.
