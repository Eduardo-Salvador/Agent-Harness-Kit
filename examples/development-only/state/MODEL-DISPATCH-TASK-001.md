---
schema: harness.model-dispatch/v1
id: model-dispatch-TASK-001
revision: 1
task: TASK-001@1
status: resolved
tier: balanced
tier_reason: Bounded validator work with deterministic fixtures.
adapter: example
capability_evidence: example-capabilities@1
available_models: example-catalog@1
selected_model: example-balanced
reasoning_effort: medium
dispatch_surface: create_thread
override_requested: true
override_confirmed: true
execution_context_ref: example:thread-001
dispatch_evidence: example-response:create-thread-001
created_at: 2026-08-20T10:09:00Z
created_by: role:orchestrator
---

# Model dispatch — TASK-001

## Resolution

The balanced tier resolved to `example-balanced` from the evidenced example catalog.

## Dispatch evidence

The example adapter accepted the model and reasoning override while creating `example:thread-001`.

## Degradation and recovery

None.
