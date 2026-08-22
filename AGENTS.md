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

For “my pending items”, “what do you need from me?”, approvals, or decisions, read the pending authority in full and report open human-owned items first, including items outside the graph. State explicitly when there is no recorded human action. Never answer these requests from the graph alone.

## State authority split

- `harness-state/PENDING.md` owns human decisions/actions and the macro project completion overview: product areas or outcomes still missing, such as unfinished backend or authentication. It does not schedule technical tasks.
- `harness-state/TASK-GRAPH.md` owns technical order, dependencies, readiness, leases, dispatch, remediation, and execution state. It does not replace the human/macro pending view.
- Every technical event—dispatch/start, material progress, new dependency, block/unblock, remediation, completion, lease/context change, or next-task readiness—must update `TASK-GRAPH.md` and its transition log in the same operational step, before the user-facing update. Never record technical movement only in `PENDING.md`. Update `PENDING.md` in that step only when a human item or macro project outcome also changed, and backlink its technical source to the new graph revision.
- Status and resume reads both in the required order. “My pending items” is answered from human-owned `PENDING.md` entries first; technical detail is added from the graph only when useful or requested.

## Operational loading order

1. Load the assigned [role](harness/roles/README.md), task brief, pinned context revision, relevant decisions, graph neighborhood, scoped rules, capability manifest, and approved model-routing revision named by the task.
2. Follow the applicable [playbook](harness/playbooks/README.md); use [templates](harness/templates/README.md) for durable state. Files carry state; messages announce changes.
3. Use only approved capabilities. Never assume tools, MCP/connectors, skills, commands, hooks, integrations, authentication, secrets, network, or permissions.
4. Write only within the exclusive ownership lease. The orchestrator alone changes graph topology/status and leases. Implementers never self-accept; reviewers remain independent.
5. Run `python tools/validate.py` before review when Python 3 is available, otherwise follow [the validation contract](docs/VALIDATION.md).
6. Route work by [capability tier](docs/MODEL-ROUTING.md), not prestige: balanced is the normal default; economical requires deterministic low-risk acceptance; frontier is reserved for consequential judgment and escalation triggers. Routing changes no authority.
7. Apply the [bounded review policy](docs/REVIEW-ROUNDS.md): one initial independent review and, only when blockers remain, at most one focused re-review. A second rejection forces task/acceptance rewrite, decomposition, or a genuine human product/risk decision. Never start a third loop; model escalation may diagnose but is not another disposition or round.
8. Follow [status and completion communication](docs/STATUS-AND-COMPLETION.md) and [`harness.status/v1`](docs/contracts/STATUS.md). Every user-facing progress/step update—not only an explicit status answer—uses the compact status shape after reading `PENDING.md` with `TASK-GRAPH.md`: current stage, progress, what continues without user action, human pending items and macro gaps from `PENDING.md`, active/ready/blocked graph nodes and technical pending work from `TASK-GRAPH.md`, blockers, next action, and inspectable paths. Never send a prose-only progress update that omits those sections. When declared checks pass, mark the task completed, explain the result, release ownership, and dispatch the next ready node. Post-completion review runs automatically and non-blockingly; ask once only for concrete authority that is genuinely missing.
9. Enforce the [bounded execution budget](docs/EXECUTION-BUDGET.md) and [`harness.execution-budget/v1`](docs/contracts/EXECUTION-BUDGET.md). Default ceilings are two implementation attempts, two consecutive no-progress cycles, and three context expansions per goal lineage. Reconcile counters before more work; model/agent/task/session changes never reset them. At a ceiling, persist evidence and `stop-and-replan` instead of continuing to consume context.
10. For a requested frontend screen, page, landing page, portfolio surface, responsive section, material visual redesign, or implementation from approved screenshots, route through the native `frontend-screen` skill and the shared [frontend screen playbook](harness/playbooks/frontend-screen.md). With approved screens, `image-to-code` is the primary coding skill for screenshot interpretation, proportions, components, and responsive implementation; `frontend-screen` checks desktop/mobile coverage and fidelity; `imagegen` creates only temporary photographs/raster assets, never code. Without approved screens, the router may coordinate design direction and responsive proposals while checking every named capability instead of assuming it exists.
11. Treat an explicit request to study, learn through the current project, enable study mode, receive guided practice, or keep learning notes as a request to configure `delivery+learning`; do not wait for the user to know that internal name. Load the native `project-learning` skill when present and follow `harness/playbooks/learning-capture-publication.md`. Before activation, ask only for missing learning goals, observation consent, and the note destination (repository Markdown, another local path, Obsidian vault/folder, Notion page/database, or another named system). Destination selection is a hard gate: until the user confirms the exact path or external target and required connector/MCP, do not activate learning, create a learning profile as active, create note files or folders, or silently fall back to `docs/`, the repository, or any other location. Record the approved choice in `harness-state/LEARNING-PROFILE.md`, including exact location, format, capability/authentication state, retention, and write/publication policy—never credentials. If the installed profile lacks project-learning support or the destination capability is unavailable, say so and offer the bounded profile/integration change; never silently pretend activation succeeded. Distinguish this from an explicit request to study the harness itself, which loads `learning-pack/` only when available.
12. Follow [execution-context routing](harness/playbooks/context-routing.md). Every new task names a workstream, agent role, isolated/shared/fallback context, thread policy, and adapter-owned reference. Prefer a fresh context per task and keep frontend, backend, data, infrastructure, integration, and learning separated. Create visible chats/tasks or internal subagents only when the capability manifest proves the host can do so; otherwise request a fresh manual context or serialize with a complete handoff. Status must group human and technical pending work, active context, blockers, and next action by area.

## Native routing

- **Codex:** load only the relevant skill under `.agents/skills/` and [Codex adapter](adapters/codex.md). Repository skills route into the same neutral roles, playbooks, contracts, and `harness-state/` used by every platform.
- **Claude Code:** `CLAUDE.md` imports this map, then routes to `.claude/skills/`, `.claude/agents/`, and [Claude adapter](adapters/claude.md). Claude-native files translate execution only; they do not own core state.

Installing `core-learning` or `full` makes project-learning support available but never activates observation, consent, retention, or publication. Operational agents must not load `learning-pack/` unless the user explicitly asks to study harness engineering.

Unresolved choices remain in [OPEN-DECISIONS.md](OPEN-DECISIONS.md). An unchecked item grants no permission.
