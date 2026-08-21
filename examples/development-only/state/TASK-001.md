---
schema: harness.task/v1
id: TASK-001
graph: graph-main@1
revision: 1
status: active
assigned_to: agent:specialist
reviewer: agent:reviewer
ownership_lease: lease:TASK-001
isolation: generic:exclusive-directory:TASK-001
updated_at: 2026-08-20T10:10:00Z
capability_manifest: none
rules_map: none
model_tier: balanced
model_reason: Bounded validator work with deterministic fixtures and no frontier trigger.
review_profile: light
max_review_rounds: 2
assurance_gate: none
---

# TASK-001 — Add deterministic configuration validation

## Outcome

Invalid example configuration is rejected with a precise rule name.

## Context to load

- `project-context@1`, `DEC-001@1`, and `graph-main@1`.

## Owned paths

- `src/config/**`
- `tests/config/**`

## Constraints

- No network or third-party package; do not edit graph state.

## Rules to load

- Task constraints only; no durable project rules are defined.

## Required capabilities

- Repository file access and the local standard-runtime validator; network unavailable.

## Acceptance criteria

- A valid fixture passes.
- An invalid fixture names the violated rule.

## Verification

- Run the repository-local dependency-free validator.

## Exit

Write a handoff; do not self-accept.
