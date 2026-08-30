---
schema: harness.model-dispatch/v1
id: model-dispatch-TASK-101
revision: 1
task: TASK-101@1
status: resolved
tier: balanced
tier_reason: Bounded parser-test work with deterministic acceptance.
adapter: example
capability_evidence: example-capabilities@1
available_models: example-catalog@1
selected_model: example-balanced
reasoning_effort: medium
dispatch_surface: spawn_subagent
override_requested: true
override_confirmed: true
execution_context_ref: example:agent-101
dispatch_evidence: example-response:spawn-agent-101
created_at: 2026-08-20T11:09:00Z
created_by: role:orchestrator
---

# Model dispatch — TASK-101

## Resolution

The balanced tier resolved to `example-balanced` from the evidenced example catalog.

## Dispatch evidence

The example adapter accepted the model and reasoning override while spawning `example:agent-101`.

## Degradation and recovery

None.
