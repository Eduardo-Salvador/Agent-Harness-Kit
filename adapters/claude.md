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

Apply [bounded review rounds](../docs/REVIEW-ROUNDS.md) to the main context and every delegated subagent. The orchestrator may dispatch one initial independent review and at most one focused re-review; a second rejection forces task/acceptance rewrite, decomposition, or a genuine human product/risk decision. A stronger model may diagnose those paths but never creates a third loop.

For every main agent or subagent, apply [status and completion communication](../docs/STATUS-AND-COMPLETION.md) and [`harness.status/v1`](../docs/contracts/STATUS.md). `PENDING.md` owns human decisions/actions and macro project gaps; `TASK-GRAPH.md` owns technical order, dependencies, and execution. Every user-facing progress/step update reports current stage, progress, work continuing without user action, human/macro pending items, active/ready/blocked graph nodes, blockers, next action, and inspectable paths; prose-only updates are invalid. Passing tasks are marked `completed` and unlock the next node immediately; assurance review is automatic, non-blocking, and never a renewed human approval request.

Before that update, persist every technical transition or material progress event in a new `TASK-GRAPH.md` revision. Never use a `PENDING.md` update as its substitute; pending changes only when human/macro state also changes.

Discovery records actual tools, skills, agents, MCP/connectors, scripts, hooks, and integrations. Presence does not establish installation, authentication, secret access, network access, or authorization.

Claude subagents provide separate execution context only when runtime evidence confirms them; they do not automatically create user-visible chats. Map visible thread lifecycle operations separately, follow [context routing](../docs/CONTEXT-ROUTING.md), and keep different workstreams out of one implementation context except an explicit integration node.

For mature repositories, preserve existing `CLAUDE.md`, `.claude/`, `.mcp.json`, and generated `.claude/worktrees/` according to the migration classifications. Generated worktree material is evidence or an exclusion, never silently promoted to canonical state. Cutover or deletion requires human semantic-equivalence review and separate authorization.

## Capability-tier mapping

The neutral policy lives in [capability-based model routing](../docs/MODEL-ROUTING.md). At dispatch, map `economical`, `balanced`, and `frontier` to the low-cost, balanced, and highest-capability Claude families actually available in the current host. Use current aliases or approved full identifiers and record the resolved model as execution evidence, not durable policy.

If the required tier is unavailable, use another available model at the same tier or block visibly. Never silently downgrade or infer additional tool, file, network, secret, integration, or publication authority from model choice.
