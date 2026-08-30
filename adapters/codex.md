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
| Model dispatch | Current model catalog plus model/reasoning override on each task or subagent operation | Human-selected fresh context or blocked route; never an unreported host default |
| Parallel dispatch | Internal subagent creation plus first-completion/attention waiting and numeric child-slot evidence | `sequential-fallback`; never simulate concurrency in the root context |
| Native agent dispatch | `agent-harness codex-dispatch` plus the host's returned `spawn_agent`/`spawn_subagent` evidence | Sequential implementation or fresh manual review context; never a fabricated child |

At session start, apply the `AGENTS.md` first-run/status gate. For resume or status, read project context, pending-work authority, and task graph in that order before any broad scan. Missing or unapproved `harness-state/PROJECT-CONTEXT.md` means discovery precedes implementation planning. Skills contain routing instructions, not canonical project memory.

Apply the `AGENTS.md` `direct-trivial` gate before first-run or task routing. A qualified local presentation/static-content edit is made directly with the smallest useful check and no discovery, SPEC, graph, TDD, review, or full status artifact. Promote it immediately if behavior, ambiguity, risk, or broader impact appears.

With approved project context, automatically load `.agents/skills/feature-discovery/SKILL.md` for unresolved new feature, workflow, integration, or user-facing capability requests. Do not require explicit skill invocation, and do not route routine fixes or already-approved implementation through feature discovery.

Before creating or dispatching non-simple implementation tasks, automatically load `.agents/skills/writing-plans/SKILL.md`. Dispatch only self-contained executable task specs; a specialist returns `needs-replan` rather than improvising beyond the spec.

For code behavior and bug fixes, automatically load `.agents/skills/test-driven-task/SKILL.md`. Require meaningful RED before production edits, GREEN with the identical focused command, and proportional regression evidence in the handoff.

Apply [bounded review rounds](../docs/REVIEW-ROUNDS.md) to the root agent and every delegated agent. After verification, automatically launch round 1 in a fresh reviewer context with no implementer history: use an internal subagent when `spawn_subagent` is proven, otherwise a new visible task/chat or clean manual context. Same-context review is invalid. Pass the pinned SPEC-led review packet, not the original prompt or conversation. The reviewer derives acceptance from the SPEC before inspecting code. Allow at most one focused fresh re-review; a second rejection forces task/acceptance rewrite, decomposition, or a genuine human product/risk decision, never a third loop.

For every root or delegated agent, apply [status and completion communication](../docs/STATUS-AND-COMPLETION.md) and [`harness.status/v1`](../docs/contracts/STATUS.md). `PENDING.md` owns human decisions/actions and macro project gaps; `TASK-GRAPH.md` owns technical order, dependencies, and execution. Every user-facing progress/step update reports current stage, progress, work continuing without user action, human/macro pending items, active/ready/blocked graph nodes, blockers, next action, and inspectable paths; prose-only updates are invalid. Passing tasks are marked `completed` and unlock the next node immediately; assurance review is automatic, non-blocking, and never a renewed human approval request.

Before that update, persist every technical transition or material progress event in a new `TASK-GRAPH.md` revision. Never use a `PENDING.md` update as its substitute; pending changes only when human/macro state also changes.

Discovery records platform tools, skills, MCP/connectors, scripts, hooks, and integrations in the capability manifest. Filename presence is not proof of runtime availability or authorization. Do not write user-specific configuration, credentials, hooks, network access, or broad permissions.

Map `create_thread`, `resume_thread`, `message_thread`, and `close_thread` only when the current Codex host exposes those operations. Internal subagent spawning is a separate capability and does not imply a sidebar-visible task. A review subagent is the preferred assurance route when proven; store its adapter reference in the immutable review result, not as conversational memory. Follow [context routing](../docs/CONTEXT-ROUTING.md) and keep workstreams isolated.

## Effective Codex App agent dispatch

Every implementation and review launch automatically loads `.agents/skills/codex-agent-dispatch/SKILL.md`. Materialize the bounded request from the task SPEC, selected neutral role, scoped approved references, and resolved model dispatch; then run `agent-harness codex-dispatch <request.json>`. Invoke the returned `native_call.operation` with exactly its arguments. Because `fork_turns` is `none`, the child receives only the generated packet rather than the orchestrator conversation.

After the host returns, record its agent/context and operation identity with `agent-harness codex-dispatch <plan.json> --response <response.json>`. Only the resulting [`harness.codex-agent-dispatch/v1`](../docs/contracts/CODEX-AGENT-DISPATCH.md) proves a live agent. Review dispatch forces `role:reviewer-integrator` and rejects the implementer identity/context. Without subagents, implementation is an explicit sequential fallback; review needs a fresh manual context.

## Effective Codex App parallel dispatch

When at least two graph nodes are ready, automatically load `.agents/skills/parallel-dispatch/SKILL.md`. Evidence the current number of available child-agent slots after reserving the orchestrator context, then run `agent-harness schedule harness-state/TASK-GRAPH.md --capacity <child-capacity>`.

For each selected node, reserve a distinct lease/isolation and resolve its model dispatch. Then invoke the host's internal subagent creation operation (`spawn_agent`, `spawn_subagent`, or the currently exposed equivalent) once per node without waiting for an earlier child to finish. Pass only the pinned task SPEC/context packet and the resolved model/reasoning values. The calls may return references one at a time, but all confirmed children remain concurrently running. Do not create user-visible Codex tasks unless the user explicitly asked for visible separate tasks.

Write `harness.parallel-dispatch/v1` with the selected batch, returned agent references, leases, model-dispatch records, and adapter evidence. Wait through the host's first-completion/attention operation (`wait_agent`, `wait_threads`, or equivalent), reconcile the first returned child, and immediately rerun scheduling to fill the freed slot. Do not wait for the whole batch before refilling. A failed spawn releases only its reservation; safely launched siblings continue.

If the host exposes no numeric capacity, internal subagent operation, or attention wait, record `sequential-fallback`. Multiple ready nodes, multiple prompts in the same context, or context references without live adapter responses are not parallel execution.

## Effective Codex App model dispatch

Automatic overrides require an explicitly human-approved model-routing artifact; approval of a tier policy/mapping is the authority to apply it to later task dispatches. Without that approval, record routing as advisory and keep model selection manual.

Immediately before every approved dispatch:

1. Inspect the models and reasoning efforts actually exposed by the active Codex host, plus override support on visible task creation, follow-up messaging, and internal subagent creation. Record this evidence in the capability manifest; do not reuse a stale catalog.
2. Resolve the task's `economical`, `balanced`, or `frontier` tier to one currently exposed model and a supported reasoning effort. Do not permanently hardcode provider model IDs in neutral policy.
3. For a new visible Codex task, call the host's `create_thread` operation with explicit `model` and `thinking` values. For an existing destination task, use `send_message_to_thread` with those overrides when the host exposes it. For an internal implementation/review context, call `spawn_subagent` with its model/reasoning override when supported.
4. Persist the returned thread/agent reference and adapter response in [`harness.model-dispatch/v1`](../docs/contracts/MODEL-DISPATCH.md), link it from the task, and only then transition the task to `active`.
5. If the operation rejects the model/effort combination, refresh the catalog and try another model in the same tier within the execution budget. If no valid route remains, record `manual-required` or `blocked`; never omit the override and call that successful routing.

The currently running Codex turn cannot claim that it changed its own model after starting. When its tier differs from the required tier, dispatch a fresh task/subagent with the approved override or ask for an explicit manual selection. A UI selection, task tier, or implementer self-report is not confirmation; the dispatch record must carry adapter-owned evidence.

For mature repositories, keep existing Codex guidance and `.agents/` content authoritative during namespaced coexistence. Bind or merge only through the migration manifest, provenance backlinks, human semantic-equivalence review, and separate cutover approval.

## Capability-tier mapping

The neutral policy lives in [capability-based model routing](../docs/MODEL-ROUTING.md). At dispatch, map `economical`, `balanced`, and `frontier` to models actually exposed by the active Codex host. Prefer the host's low-cost model for deterministic mechanical work, its balanced coding model for normal bounded delivery, and its strongest reasoning/coding model for frontier triggers. Apply the resolved model through the real task/subagent operation and record its confirmation as execution evidence, not durable policy.

If the requested tier is not available, use another exposed model at the same tier or block visibly. Do not hardcode a model ID in the neutral contract, silently downgrade, or treat model selection as permission.
