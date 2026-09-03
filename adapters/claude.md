# Claude Code native adapter

Claude Code natively loads root `CLAUDE.md`. This kit uses the documented `@AGENTS.md` import so Claude and Codex converge on one neutral policy map, then adds only Claude-specific routing to `.claude/skills/` and `.claude/agents/`.

## Visible greeting and activation

Root `CLAUDE.md` carries the welcome requirement directly as well as importing the shared map. A greeting-only "oi"/"hello" starts onboarding when approved context is missing. The visible first response starts with the localized Kit-active welcome and asks one combined question for unanswered mode preference and missing product intent. Merely asking discovery questions is insufficient. Approved context preserves the existing choice and skips the welcome. Start a new context at the host-project root after installation; disabled project-instruction loading requires the explicit activation fallback, not a claim of automatic enforcement.

## Native mapping

| Neutral operation | Claude Code surface | Safe fallback |
| --- | --- | --- |
| Session guidance | `CLAUDE.md` importing root `AGENTS.md` | Load the shared map explicitly |
| Essential workflow | Relevant `.claude/skills/*/SKILL.md` | Follow the linked neutral playbook directly |
| Bounded delegation | Explicit `.claude/agents/*.md` definitions | Run sequentially in the main context while preserving reviewer independence |
| Task/chat lifecycle | Thread/session operations actually exposed by the Claude host | Bounded subagent, user-opened fresh context, or sequential artifact handoff |
| Tool execution | Tools allowed by the selected agent and current permission system | Mark unavailable or approval-required |
| Hooks and MCP | Existing, reviewed project configuration | Do not create `.claude/settings.json` or `.mcp.json` automatically |

For resume, run a bounded real-state probe first, then read `harness-state/PROJECT-CONTEXT.md`, the pending authority, and `harness-state/TASK-GRAPH.md` only to fill gaps; skip stale handoffs when current tests/runtime evidence cover state. Read-only audits and diagnosis do not trigger first-run. Missing project context gates planning or mutation, not inspection.

Apply the imported `direct-trivial` gate before first-run or task routing. A qualified local presentation/static-content edit is made directly with the smallest useful check and no discovery, SPEC, graph, TDD, review, or full status artifact. Promote it immediately if behavior, ambiguity, risk, or broader impact appears.

With approved project context, automatically load `.claude/skills/feature-discovery/SKILL.md` for unresolved new feature, workflow, integration, or user-facing capability requests. Do not require explicit skill invocation, and do not route routine fixes or already-approved implementation through feature discovery.

Before planned implementation, load `.claude/skills/writing-plans/SKILL.md`; target 15–30 active minutes per unit and justify exceptions. Use compact full Harness for bounded work and complete full Harness only when coordination/discovery/audit requires it.

For code behavior and bug fixes, load `.claude/skills/test-driven-task/SKILL.md`. Require meaningful RED/GREEN and climb `focused` → `workspace` → `integration` → `global/checkpoint` → `delivery` only as needed. Record evidence in the inline transition unless a real consumer needs a handoff.

Apply [bounded review rounds](../docs/REVIEW-ROUNDS.md) for `assurance: light|full`; `none` closes on executor verification. Required review stays independent and fresh. Create a handoff/review packet only for that actual reviewer consumer, and allow at most one focused re-review.

The review packet excludes the original prompt and implementer conversation; neither is review authority.

For every main agent or subagent, apply [status and completion communication](../docs/STATUS-AND-COMPLETION.md) and [`harness.status/v1`](../docs/contracts/STATUS.md). `PENDING.md` owns human decisions/actions and macro project gaps; `TASK-GRAPH.md` owns technical order, dependencies, and execution. Explicit status views and milestone closeouts report current stage, progress, work continuing without user action, human/macro pending items, active/ready/blocked graph nodes, blockers, next action, and inspectable paths; routine progress may use concise result/evidence, human action, and next-action text. Passing tasks are marked `completed` and unlock only nodes whose product and technical gates pass; assurance review is automatic, non-blocking, and never a renewed human approval request.

Before that update, persist every technical transition or material progress event in a new `TASK-GRAPH.md` revision. Never use a `PENDING.md` update as its substitute; pending changes only when human/macro state also changes.

Discovery records actual tools, skills, agents, MCP/connectors, scripts, hooks, and integrations. Presence does not establish installation, authentication, secret access, network access, or authorization.

Claude subagents provide separate execution context only when runtime evidence confirms them; they do not automatically create user-visible chats. A proven subagent is the preferred fresh-review route and its adapter reference belongs in the immutable result. Map visible thread lifecycle separately, follow [context routing](../docs/CONTEXT-ROUTING.md), and keep different workstreams out of one implementation context except an explicit integration node.

When two or more collision-free nodes are ready and the Claude host proves numeric capacity greater than one, automatically launch the safe batch and report the active worker count. Refill on the first child event. Warn after 60–90 seconds without observable progress; on the second consecutive occurrence interrupt and reassign/serialize within budget. Otherwise record `sequential-fallback`.

For mature repositories, preserve existing `CLAUDE.md`, `.claude/`, `.mcp.json`, and generated `.claude/worktrees/` according to the migration classifications. Generated worktree material is evidence or an exclusion, never silently promoted to canonical state. Cutover or deletion requires human semantic-equivalence review and separate authorization.

## Capability-tier mapping

The neutral policy lives in [capability-based model routing](../docs/MODEL-ROUTING.md). At dispatch, map `economical`, `balanced`, and `frontier` to the low-cost, balanced, and highest-capability Claude families actually available in the current host. Use current aliases or approved full identifiers. When the active host exposes a model override for the delegated context, apply it in the real operation and persist `harness.model-dispatch/v1`; otherwise record `manual-required` or `blocked`. A tier label or host default is not confirmed routing.

If the required tier is unavailable, use another available model at the same tier or block visibly. Never silently downgrade or infer additional tool, file, network, secret, integration, or publication authority from model choice.
