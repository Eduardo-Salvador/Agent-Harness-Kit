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

At session start, apply the `AGENTS.md` first-run/status gate. For resume or status, read project context, pending-work authority, and task graph in that order before any broad scan. Missing or unapproved `harness-state/PROJECT-CONTEXT.md` means discovery precedes implementation planning. Skills contain routing instructions, not canonical project memory.

Apply [bounded review rounds](../docs/REVIEW-ROUNDS.md) to the root agent and every delegated agent. The orchestrator may dispatch one initial independent review and at most one focused re-review; an exhausted budget requires escalation, decomposition, rewrite, or human decision, never a third unchanged loop.

For every root or delegated agent, apply [status and completion communication](../docs/STATUS-AND-COMPLETION.md). `PENDING.md` owns human decisions/actions and macro project gaps; `TASK-GRAPH.md` owns technical order, dependencies, and execution. Passing tasks are marked `completed` and unlock the next node immediately; assurance review is automatic, non-blocking, and never a renewed human approval request.

Discovery records platform tools, skills, MCP/connectors, scripts, hooks, and integrations in the capability manifest. Filename presence is not proof of runtime availability or authorization. Do not write user-specific configuration, credentials, hooks, network access, or broad permissions.

For mature repositories, keep existing Codex guidance and `.agents/` content authoritative during namespaced coexistence. Bind or merge only through the migration manifest, provenance backlinks, human semantic-equivalence review, and separate cutover approval.

## Capability-tier mapping

The neutral policy lives in [capability-based model routing](../docs/MODEL-ROUTING.md). At dispatch, map `economical`, `balanced`, and `frontier` to models actually exposed by the active Codex host. Prefer the host's low-cost model for deterministic mechanical work, its balanced coding model for normal bounded delivery, and its strongest reasoning/coding model for frontier triggers. Record the resolved model as execution evidence, not durable policy.

If the requested tier is not available, use another exposed model at the same tier or block visibly. Do not hardcode a model ID in the neutral contract, silently downgrade, or treat model selection as permission.
