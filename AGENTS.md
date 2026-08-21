# Agent Harness Kit — operational map

Codex loads this file before work. Claude Code imports it from `CLAUDE.md`. This is the shared, platform-neutral policy map; load details progressively and do not preload the repository.

## First-run gate

Before planning implementation, inspect `harness-state/PROJECT-CONTEXT.md`. Context is initialized only when it contains `schema: harness.project-context/v1` and `status: approved`. If it is absent, draft, stale, or conflicts with current evidence, use the platform's `first-run-discovery` skill and follow [first run](harness/playbooks/first-run.md). Discovery identifies greenfield versus existing-project state, inventories rules and capabilities, records decisions for confirmation, selects `delivery` or `delivery+learning`, obtains approval, and only then creates the initial graph.

If mature harness material exists, do not overwrite `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, `.mcp.json`, or another authority. Follow [mature adoption](harness/playbooks/mature-harness-adoption.md): use a namespaced staged installation, classify every material item with provenance and backlinks, validate snapshot freshness, and preserve originals until human semantic review and separate cutover authorization.

## Session-start, resume, and status gate

On the first request in a new context window, any request to continue/resume, or any project-status request, follow [status and resume](harness/playbooks/status-resume.md) before broad inspection:

1. Read `harness-state/PROJECT-CONTEXT.md`.
2. Read the pending-work authority named by approved context/decisions; otherwise use `harness-state/PENDING.md` when present.
3. Read `harness-state/TASK-GRAPH.md`.
4. Only then load the active task, direct graph neighborhood, relevant decisions/rules/capabilities/model routing, and latest handoff/review.

Do not substitute repository-wide scanning, dependency inventory, Git-history traversal, or conversational recall for this order. If an artifact is missing, stale, or contradictory, report that exact condition and enter the applicable discovery/recovery playbook. Broader inspection is allowed only for a concrete gap exposed by these artifacts, a required recovery step, or an explicit user audit request; announce its reason and scope first.

## Operational loading order

1. Load the assigned [role](harness/roles/README.md), task brief, pinned context revision, relevant decisions, graph neighborhood, scoped rules, capability manifest, and approved model-routing revision named by the task.
2. Follow the applicable [playbook](harness/playbooks/README.md); use [templates](harness/templates/README.md) for durable state. Files carry state; messages announce changes.
3. Use only approved capabilities. Never assume tools, MCP/connectors, skills, commands, hooks, integrations, authentication, secrets, network, or permissions.
4. Write only within the exclusive ownership lease. The orchestrator alone changes graph topology/status and leases. Implementers never self-accept; reviewers remain independent.
5. Run `python tools/validate.py` before review when Python 3 is available, otherwise follow [the validation contract](docs/VALIDATION.md).
6. Route work by [capability tier](docs/MODEL-ROUTING.md), not prestige: balanced is the normal default; economical requires deterministic low-risk acceptance; frontier is reserved for consequential judgment and escalation triggers. Routing changes no authority.
7. Apply the [bounded review policy](docs/REVIEW-ROUNDS.md): one initial independent review and, only when blockers remain, at most one focused re-review. Never start a third unchanged review loop; escalate, decompose, rewrite, or request a human decision.

## Native routing

- **Codex:** load only the relevant skill under `.agents/skills/` and [Codex adapter](adapters/codex.md). Repository skills route into the same neutral roles, playbooks, contracts, and `harness-state/` used by every platform.
- **Claude Code:** `CLAUDE.md` imports this map, then routes to `.claude/skills/`, `.claude/agents/`, and [Claude adapter](adapters/claude.md). Claude-native files translate execution only; they do not own core state.

Installing `core-learning` or `full` makes project-learning support available but never activates observation, consent, retention, or publication. Operational agents must not load `learning-pack/` unless the user explicitly asks to study harness engineering.

Unresolved choices remain in [OPEN-DECISIONS.md](OPEN-DECISIONS.md). An unchecked item grants no permission.
