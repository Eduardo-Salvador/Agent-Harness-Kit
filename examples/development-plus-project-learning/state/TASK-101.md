---
schema: harness.task/v1
id: TASK-101
graph: graph-learning-example@1
revision: 1
status: active
planning_mode: inline-simple
implementation_plan: none
plan_step: inline
target_minutes: 5
test_strategy: verification-only
tdd_exception: Test-only boundary assertions; no production behavior changes.
assigned_to: agent:specialist
reviewer: agent:reviewer
ownership_lease: lease:TASK-101
isolation: generic:exclusive-directory:TASK-101
updated_at: 2026-08-20T11:10:00Z
capability_manifest: none
rules_map: none
model_tier: balanced
model_reason: Bounded parser-test work with deterministic acceptance and no frontier trigger.
model_dispatch: model-dispatch-TASK-101@1
review_profile: light
max_review_rounds: 2
assurance_gate: none
---

# TASK-101 — Add parser boundary tests

## Outcome

Empty and maximum-length inputs have deterministic tests.

## Executable spec

- Exact change: Add assertions for the two already-defined parser boundaries.
- Planning provenance: inline-simple.

## Context to load

- `project-context-learning-example@1` and `graph-learning-example@1`.

## Owned paths

- `tests/parser/**`

## Constraints

- Delivery agent does not load the learning profile or edit learning artifacts.

## Non-goals

- No parser behavior or learning-profile changes.

## Rules to load

- Learning non-interference and parser-test path scope only.

## Required capabilities

- Repository file access and local parser test command; no network or secrets.

## Acceptance criteria

- Empty input behavior is asserted.
- Maximum-length input behavior is asserted.

## Test-first cycle

- Strategy: verification-only; this task adds assertions for existing behavior without production changes.
- Check: run the focused parser boundary tests.

## Verification

- Run the parser's local standard-runtime test command.

## Stop and replan

- Return `needs-replan` if parser behavior is undefined or additional ownership/dependencies are required.

## Exit

Write a handoff; do not self-accept.
