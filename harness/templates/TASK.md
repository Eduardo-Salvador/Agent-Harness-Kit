---
schema: harness.task/v1
id: TASK-001
graph: graph-main@1
revision: 1
status: ready
planning_mode: planned
implementation_plan: PLAN-001@1
plan_step: STEP-001
target_minutes: 5
test_strategy: tdd
tdd_exception: none
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
model_dispatch: model-dispatch-TASK-001@1
execution_budget: execution-budget-TASK-001@1
review_profile: standard
max_review_rounds: 2
assurance_gate: none
---

# TASK-001 — Replace with outcome

## Outcome

Replace with one bounded result.

## Executable spec

- Exact change: Replace with the implementation action already decided by the plan.
- Planning provenance: `PLAN-001@1`, `STEP-001`.

## Context to load

- `project-context@1`
- `graph-main@1` and direct dependency artifacts
- `thread_ref` is routing evidence only; reconstruct state from these artifacts, not prior chat memory.

## Owned paths

- `replace/path/**`

## Constraints

- Do not change graph state or broaden the write set.
- Stop before another attempt or context expansion when the linked execution budget reaches a ceiling.

## Non-goals

- Replace with behavior, paths, dependencies, and cleanup intentionally outside this task.

## Rules to load

- Only approved rules whose scope intersects this task/role/owned paths.

## Required capabilities

- Capability IDs and required states; never assume installation, authentication, secrets, network, or authorization.

## Acceptance criteria

- Replace with an observable criterion.

## Test-first cycle

- RED test/path: Replace.
- RED command: Replace with the focused command.
- Expected RED: Replace with the intended missing-behavior failure; syntax/environment/unrelated failures do not count.
- GREEN change: Replace with the minimum production behavior.
- GREEN command: Rerun the identical focused command and require pass.
- Refactor boundary: Replace or state none.
- Proportional regression: Replace with impacted tests; full suite only when risk/impact requires it.

## Verification

- Replace with a reproducible command/check or a declared manual evidence procedure.

## Stop and replan

- Return `needs-replan` instead of improvising when the spec is missing/contradictory, a product choice or undeclared dependency appears, ownership must expand, acceptance cannot be evaluated, or the unit is materially larger than planned.
- For TDD, also replan if RED passes before implementation or fails for syntax, environment, or an unrelated reason.

## Exit

Write a handoff with criterion-level evidence; do not self-accept.
