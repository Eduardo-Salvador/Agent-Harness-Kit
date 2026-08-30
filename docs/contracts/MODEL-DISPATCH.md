# Contract: Model dispatch

Runtime evidence that a capability tier was resolved to a model exposed by the active host and actually applied at task dispatch. Recording only `economical`, `balanced`, or `frontier` is not successful routing.

```yaml
---
schema: harness.model-dispatch/v1
id: model-dispatch-TASK-001
revision: 1
task: TASK-001@1
status: resolved                 # resolved | manual-required | blocked
tier: balanced
tier_reason: Bounded implementation with deterministic acceptance.
adapter: codex-app
capability_evidence: capability-manifest@2
available_models: adapter-catalog@2026-08-30T15:00:00Z
selected_model: adapter-model-id
reasoning_effort: medium
dispatch_surface: create_thread  # create_thread | send_message_to_thread | spawn_subagent | manual-selection
override_requested: true
override_confirmed: true
execution_context_ref: adapter:thread-001
dispatch_evidence: adapter-response:create-thread-001
created_at: 2026-08-30T15:00:01Z
created_by: role:orchestrator
---
```

## Resolution

- The adapter inventories the current host model catalog and model/reasoning override surfaces immediately before dispatch.
- The orchestrator maps the approved tier to one model in that catalog. Provider model IDs are runtime evidence, not permanent neutral policy.
- A task cannot transition to `active` with `selected_model`, `dispatch_evidence`, or the relevant capability still `pending`, `unknown`, `host-default`, or `unavailable`.

## Dispatch evidence

- For Codex App, pass the resolved model and supported reasoning effort in the actual `create_thread`, `send_message_to_thread`, or internal `spawn_subagent` operation.
- Persist the returned task/thread/agent reference and adapter response identity, then mark `override_confirmed: true` only when the operation accepted the override.
- The implementer handoff repeats the dispatch reference, model ID, reasoning effort, and any route change. Self-report without adapter evidence is insufficient.

## Degradation and recovery

- An already-running context cannot claim that it changed its own model mid-turn. Prefer a fresh task/subagent with an explicit override.
- If no override-capable fresh-context surface exists, use `manual-required` and name the exact user selection needed, or `blocked` when the required tier is unavailable.
- A rejected model ID may be retried with another currently exposed model in the same tier. Never silently accept the host default or downgrade tiers.

## Invariants

- `tier` and `tier_reason` match the pinned task.
- `resolved` requires a non-placeholder `selected_model` present in current catalog evidence, an override-capable dispatch surface, confirmed override, context reference, and adapter evidence.
- Model routing changes no authority, lease, acceptance, verification, review, or execution-budget boundary.
