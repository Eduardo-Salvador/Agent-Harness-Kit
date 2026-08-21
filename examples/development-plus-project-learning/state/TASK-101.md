---
schema: harness.task/v1
id: TASK-101
graph: graph-learning-example@1
revision: 1
status: active
assigned_to: agent:specialist
reviewer: agent:reviewer
ownership_lease: lease:TASK-101
isolation: generic:exclusive-directory:TASK-101
updated_at: 2026-08-20T11:10:00Z
capability_manifest: none
rules_map: none
model_tier: balanced
model_reason: Bounded parser-test work with deterministic acceptance and no frontier trigger.
review_profile: light
max_review_rounds: 2
assurance_gate: none
---

# TASK-101 — Add parser boundary tests

## Outcome

Empty and maximum-length inputs have deterministic tests.

## Context to load

- `project-context-learning-example@1` and `graph-learning-example@1`.

## Owned paths

- `tests/parser/**`

## Constraints

- Delivery agent does not load the learning profile or edit learning artifacts.

## Rules to load

- Learning non-interference and parser-test path scope only.

## Required capabilities

- Repository file access and local parser test command; no network or secrets.

## Acceptance criteria

- Empty input behavior is asserted.
- Maximum-length input behavior is asserted.

## Verification

- Run the parser's local standard-runtime test command.

## Exit

Write a handoff; do not self-accept.
