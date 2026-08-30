---
schema: harness.model-dispatch/v1
id: model-dispatch-TASK-001
revision: 1
task: TASK-001@1
status: resolved
tier: balanced
tier_reason: Bounded implementation with deterministic acceptance.
adapter: replace-adapter
capability_evidence: capability-manifest@1
available_models: adapter-catalog@replace-timestamp
selected_model: replace-model-id
reasoning_effort: replace-supported-effort
dispatch_surface: replace-override-surface
override_requested: true
override_confirmed: true
execution_context_ref: adapter:replace-context
dispatch_evidence: adapter-response:replace-operation
created_at: 2000-01-01T00:00:00Z
created_by: role:orchestrator
---

# Model dispatch — TASK-001

## Resolution

- Tier and reason: Replace with the pinned task tier and task-specific reason.
- Catalog evidence: Replace with the host capability/model catalog inspected immediately before dispatch.
- Selected model and reasoning: Replace with the exact runtime values.

## Dispatch evidence

- Surface: Replace with the actual override-capable adapter operation.
- Override result: Replace with the returned confirmation and context reference.
- Evidence: Replace with an inspectable adapter response or run identity; never use agent confidence.

## Degradation and recovery

- None, or record `manual-required`/`blocked`, the unavailable capability, same-tier retry, and exact next action. Never silently use the host default or claim a same-context mid-turn switch.
