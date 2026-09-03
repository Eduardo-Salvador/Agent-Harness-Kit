---
schema: harness.task/v1
id: TASK-001
graph: graph-main@1
revision: 1
status: ready
planning_mode: planned
implementation_plan: PLAN-001@1
plan_step: STEP-001
target_minutes: 20
test_strategy: tdd
tdd_exception: none
evidence_profile: handoff-review
assurance: full
artifact_policy: transfer
handoff_consumer: reviewer
test_ladder: focused-unit
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

- Positive case: concrete input, actor/customer, and expected observable result from approved intent.
- Negative/boundary case: concrete input that must be excluded or rejected, with expected reason.
- Failure/recovery case: how the affected flow exposes failure and can safely recover.
- Product checkpoint: none / milestone ID, demonstration, affected downstream work, and current approval reference.

## Completion conditions — this task is complete only when

- AC-001: The specified behavior is implemented successfully in the affected execution path; replace this sentence with the exact input/action and required observable result.
- AC-002: The specified rejected/boundary and failure/recovery cases behave as required; replace with concrete conditions.
- Every required condition above has a recorded observed result and evidence reference; code written, a file created, or tests merely executed is not success.
- Required focused tests, affected-flow smoke, and proportional regression pass. No unresolved defect contradicts these conditions. Unavailable verification is a blocker, not a pass.
- Mirror the concrete conditions as `acceptance_criteria` in the graph and record one passing `verification.acceptance` result per ID. Pin the same acceptance revision; do not weaken conditions after implementation to obtain a pass.
- Technical completion does not imply client approval: if this is a product milestone, affected expansion waits for its explicit `product_review`.

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
- Pin the graph node's `acceptance_revision`, `test_strategy`, and `runtime_smoke_required` before execution; record current `verification` according to [executable acceptance](../../docs/ACCOMPANIED-DELIVERY.md).
- For automation, entrypoint, configuration-consumer, or integration changes: run a controlled affected-flow smoke including visible failure behavior. Record command, expected/observed results, exit code, and original evidence reference. A build alone is insufficient; reuse a qualifying integration run rather than duplicate it.

## Stop and replan

- Return `needs-replan` instead of improvising when the spec is missing/contradictory, a product choice or undeclared dependency appears, ownership must expand, acceptance cannot be evaluated, or the unit is materially larger than planned.
- For TDD, also replan if RED passes before implementation or fails for syntax, environment, or an unrelated reason.

## Exit

For a real reviewer/human consumer, write a handoff with criterion-level evidence. For a closed single-context task, create no handoff or separate review packet: return the concise outcome and verification result for the atomic graph transition/event. Do not self-accept when assurance requires independent acceptance.
