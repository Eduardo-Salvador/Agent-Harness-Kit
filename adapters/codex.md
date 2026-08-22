# Codex native adapter

Codex natively discovers root `AGENTS.md` and repository skills under `.agents/skills/`. This adapter translates those filesystem conventions into the neutral harness; it does not create a second policy or state store.

## Native mapping

| Neutral operation | Codex-native surface | Safe fallback |
| --- | --- | --- |
| Session guidance | Root `AGENTS.md`, plus layered path guidance already present in the host | Load the shared root map only |
| Essential workflow | Relevant `.agents/skills/*/SKILL.md` | Follow the linked neutral playbook directly |
| Tool execution | Tools actually exposed by the current Codex session | Mark unavailable or approval-required |
| MCP | User/project configuration that already exists and is approved | Do not install, authenticate, or edit global config |
| Isolation/delegation | Capabilities evidenced in the current host | Serialize work and preserve distinct implementer/reviewer contexts |
| Task/chat lifecycle | Visible task/thread operations actually exposed by the Codex host | Internal subagent, user-opened fresh context, or sequential artifact handoff |

At session start, apply the `AGENTS.md` first-run/status gate. For resume or status, read project context, pending-work authority, and task graph in that order before any broad scan. Missing or unapproved `harness-state/PROJECT-CONTEXT.md` means discovery precedes implementation planning. Skills contain routing instructions, not canonical project memory.

Apply [bounded review rounds](../docs/REVIEW-ROUNDS.md) to the root agent and every delegated agent. The orchestrator may dispatch one initial independent review and at most one focused re-review; a second rejection forces task/acceptance rewrite, decomposition, or a genuine human product/risk decision. A stronger model may diagnose those paths but never creates a third loop.

For every root or delegated agent, apply [status and completion communication](../docs/STATUS-AND-COMPLETION.md) and [`harness.status/v1`](../docs/contracts/STATUS.md). `PENDING.md` owns human decisions/actions and macro project gaps; `TASK-GRAPH.md` owns technical order, dependencies, and execution. Every user-facing progress/step update reports current stage, progress, work continuing without user action, human/macro pending items, active/ready/blocked graph nodes, blockers, next action, and inspectable paths; prose-only updates are invalid. Passing tasks are marked `completed` and unlock the next node immediately; assurance review is automatic, non-blocking, and never a renewed human approval request.

Before that update, persist every technical transition or material progress event in a new `TASK-GRAPH.md` revision. Never use a `PENDING.md` update as its substitute; pending changes only when human/macro state also changes.

Discovery records platform tools, skills, MCP/connectors, scripts, hooks, and integrations in the capability manifest. Filename presence is not proof of runtime availability or authorization. Do not write user-specific configuration, credentials, hooks, network access, or broad permissions.

Map `create_thread`, `resume_thread`, `message_thread`, and `close_thread` only when the current Codex host exposes those operations. Internal subagent spawning is a separate capability and does not imply a sidebar-visible task. Follow [context routing](../docs/CONTEXT-ROUTING.md), keep workstreams isolated, and store only the returned adapter reference in task state.

For mature repositories, keep existing Codex guidance and `.agents/` content authoritative during namespaced coexistence. Bind or merge only through the migration manifest, provenance backlinks, human semantic-equivalence review, and separate cutover approval.

## Capability-tier mapping

The neutral policy lives in [capability-based model routing](../docs/MODEL-ROUTING.md). At dispatch, map `economical`, `balanced`, and `frontier` to models actually exposed by the active Codex host. Prefer the host's low-cost model for deterministic mechanical work, its balanced coding model for normal bounded delivery, and its strongest reasoning/coding model for frontier triggers. Record the resolved model as execution evidence, not durable policy.

If the requested tier is not available, use another exposed model at the same tier or block visibly. Do not hardcode a model ID in the neutral contract, silently downgrade, or treat model selection as permission.
