---
schema: harness.task/v1
id: TASK-001
graph: graph-main@1
revision: 1
status: ready
assigned_to: unassigned
reviewer: unassigned
workstream: replace-area
agent_role: role:generic-specialist
execution_context: isolated
thread_policy: create-per-task
thread_ref: pending
ownership_lease: pending
isolation: pending
updated_at: 2000-01-01T00:00:00Z
capability_manifest: capability-manifest@1
rules_map: rules-map@1
model_tier: balanced
model_reason: Bounded implementation with deterministic acceptance and no frontier trigger.
execution_budget: execution-budget-TASK-001@1
review_profile: standard
max_review_rounds: 2
assurance_gate: none
---

# TASK-001 — Replace with outcome

## Outcome

Replace with one bounded result.

## Context to load

- `project-context@1`
- `graph-main@1` and direct dependency artifacts
- `thread_ref` is routing evidence only; reconstruct state from these artifacts, not prior chat memory.

## Owned paths

- `replace/path/**`

## Constraints

- Do not change graph state or broaden the write set.
- Stop before another attempt or context expansion when the linked execution budget reaches a ceiling.

## Rules to load

- Only approved rules whose scope intersects this task/role/owned paths.

## Required capabilities

- Capability IDs and required states; never assume installation, authentication, secrets, network, or authorization.

## Acceptance criteria

- Replace with an observable criterion.

## Verification

- Replace with a reproducible command/check or a declared manual evidence procedure.

## Exit

Write a handoff with criterion-level evidence; do not self-accept.
