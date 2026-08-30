# Claude Code native adapter

Claude Code natively loads root `CLAUDE.md`. This kit uses the documented `@AGENTS.md` import so Claude and Codex converge on one neutral policy map, then adds only Claude-specific routing to `.claude/skills/` and `.claude/agents/`.

## Native mapping

| Neutral operation | Claude Code surface | Safe fallback |
| --- | --- | --- |
| Session guidance | `CLAUDE.md` importing root `AGENTS.md` | Load the shared map explicitly |
| Essential workflow | Relevant `.claude/skills/*/SKILL.md` | Follow the linked neutral playbook directly |
| Bounded delegation | Explicit `.claude/agents/*.md` definitions | Run sequentially in the main context while preserving reviewer independence |
| Task/chat lifecycle | Thread/session operations actually exposed by the Claude host | Bounded subagent, user-opened fresh context, or sequential artifact handoff |
| Tool execution | Tools allowed by the selected agent and current permission system | Mark unavailable or approval-required |
| Hooks and MCP | Existing, reviewed project configuration | Do not create `.claude/settings.json` or `.mcp.json` automatically |

At session start, apply the imported first-run/status gate. For resume or status, read project context, pending-work authority, and task graph in that order before any broad scan. Missing or unapproved `harness-state/PROJECT-CONTEXT.md` means discovery precedes implementation planning. Native skills and agents translate execution; canonical context, graph, decisions, rules, capability evidence, and handoffs remain in neutral paths.

Apply the imported `direct-trivial` gate before first-run or task routing. A qualified local presentation/static-content edit is made directly with the smallest useful check and no discovery, SPEC, graph, TDD, review, or full status artifact. Promote it immediately if behavior, ambiguity, risk, or broader impact appears.

With approved project context, automatically load `.claude/skills/feature-discovery/SKILL.md` for unresolved new feature, workflow, integration, or user-facing capability requests. Do not require explicit skill invocation, and do not route routine fixes or already-approved implementation through feature discovery.

Before creating or dispatching non-simple implementation tasks, automatically load `.claude/skills/writing-plans/SKILL.md`. Dispatch only self-contained executable task specs; a specialist returns `needs-replan` rather than improvising beyond the spec.

For code behavior and bug fixes, automatically load `.claude/skills/test-driven-task/SKILL.md`. Require meaningful RED before production edits, GREEN with the identical focused command, and proportional regression evidence in the handoff.

Apply [bounded review rounds](../docs/REVIEW-ROUNDS.md) to the main context and every delegated subagent. After verification, automatically launch `.claude/agents/independent-reviewer.md` in a fresh subagent when capability evidence allows it; otherwise use a new visible task/chat or clean manual context. Same-context review is invalid. Pass the pinned SPEC-led review packet, not the original prompt or conversation. The reviewer derives acceptance from the SPEC before inspecting code. Allow at most one focused fresh re-review; a second rejection forces task/acceptance rewrite, decomposition, or a genuine human product/risk decision, never a third loop.

For every main agent or subagent, apply [status and completion communication](../docs/STATUS-AND-COMPLETION.md) and [`harness.status/v1`](../docs/contracts/STATUS.md). `PENDING.md` owns human decisions/actions and macro project gaps; `TASK-GRAPH.md` owns technical order, dependencies, and execution. Every user-facing progress/step update reports current stage, progress, work continuing without user action, human/macro pending items, active/ready/blocked graph nodes, blockers, next action, and inspectable paths; prose-only updates are invalid. Passing tasks are marked `completed` and unlock the next node immediately; assurance review is automatic, non-blocking, and never a renewed human approval request.

Before that update, persist every technical transition or material progress event in a new `TASK-GRAPH.md` revision. Never use a `PENDING.md` update as its substitute; pending changes only when human/macro state also changes.

Discovery records actual tools, skills, agents, MCP/connectors, scripts, hooks, and integrations. Presence does not establish installation, authentication, secret access, network access, or authorization.

Claude subagents provide separate execution context only when runtime evidence confirms them; they do not automatically create user-visible chats. A proven subagent is the preferred fresh-review route and its adapter reference belongs in the immutable result. Map visible thread lifecycle separately, follow [context routing](../docs/CONTEXT-ROUTING.md), and keep different workstreams out of one implementation context except an explicit integration node.

When two or more nodes are ready and the Claude host proves numeric child capacity plus a completion/attention wait surface, automatically load `.claude/skills/parallel-dispatch/SKILL.md`, consume the deterministic `agent-harness schedule` batch, and invoke one real subagent operation per selected node before waiting. Persist distinct contexts/leases and `harness.parallel-dispatch/v1`, reconcile the first child event, and refill capacity. Otherwise record `sequential-fallback`; agent definitions alone do not prove concurrency.

For mature repositories, preserve existing `CLAUDE.md`, `.claude/`, `.mcp.json`, and generated `.claude/worktrees/` according to the migration classifications. Generated worktree material is evidence or an exclusion, never silently promoted to canonical state. Cutover or deletion requires human semantic-equivalence review and separate authorization.

## Capability-tier mapping

The neutral policy lives in [capability-based model routing](../docs/MODEL-ROUTING.md). At dispatch, map `economical`, `balanced`, and `frontier` to the low-cost, balanced, and highest-capability Claude families actually available in the current host. Use current aliases or approved full identifiers. When the active host exposes a model override for the delegated context, apply it in the real operation and persist `harness.model-dispatch/v1`; otherwise record `manual-required` or `blocked`. A tier label or host default is not confirmed routing.

If the required tier is unavailable, use another available model at the same tier or block visibly. Never silently downgrade or infer additional tool, file, network, secret, integration, or publication authority from model choice.
