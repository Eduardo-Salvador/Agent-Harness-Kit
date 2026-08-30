---
schema: harness.task/v1
id: TASK-001
graph: graph-main@1
revision: 1
status: active
planning_mode: inline-simple
implementation_plan: none
plan_step: inline
target_minutes: 5
test_strategy: verification-only
tdd_exception: Test-only fixture task; no production behavior changes.
assigned_to: agent:specialist
reviewer: agent:reviewer
ownership_lease: lease:TASK-001
isolation: generic:exclusive-directory:TASK-001
updated_at: 2026-08-20T10:10:00Z
capability_manifest: none
rules_map: none
model_tier: balanced
model_reason: Bounded validator work with deterministic fixtures and no frontier trigger.
model_dispatch: model-dispatch-TASK-001@1
review_profile: light
max_review_rounds: 2
assurance_gate: none
---

# TASK-001 — Add deterministic configuration validation

## Outcome

Invalid example configuration is rejected with a precise rule name.

## Executable spec

- Exact change: Add the two deterministic configuration fixtures and their validation assertions.
- Planning provenance: inline-simple.

## Context to load

- `project-context@1`, `DEC-001@1`, and `graph-main@1`.

## Owned paths

- `src/config/**`
- `tests/config/**`

## Constraints

- No network or third-party package; do not edit graph state.

## Non-goals

- No production runtime or dependency changes.

## Rules to load

- Task constraints only; no durable project rules are defined.

## Required capabilities

- Repository file access and the local standard-runtime validator; network unavailable.

## Acceptance criteria

- A valid fixture passes.
- An invalid fixture names the violated rule.

## Test-first cycle

- Strategy: verification-only; this task adds test fixtures without production behavior.
- Check: run the focused validator against valid and invalid fixtures.

## Verification

- Run the repository-local dependency-free validator.

## Stop and replan

- Return `needs-replan` if validation requires a new dependency, additional owned paths, or an undefined configuration behavior.

## Exit

Write a handoff; do not self-accept.
