# Contract: Handoff

The implementer's concise completion/failure artifact. It points to state and evidence rather than pasting logs.

```yaml
---
schema: harness.handoff/v1
id: HANDOFF-TASK-001-01
task: TASK-001@1
attempt: 1
status: completed                 # completed | blocked | failed
author: agent:builder-1
workstream: backend
agent_role: role:backend-specialist
execution_context: isolated
thread_ref: adapter:task-001
created_at: 2026-08-20T14:45:00Z
model_tier_used: balanced
model_route_changes: none
---
```

```markdown
# Handoff — TASK-001

## Result
Implemented graph-cycle and ownership-overlap validation.

- Execution context: `adapter:task-001`; closed after durable handoff.

## Changes
- `src/contracts/graph-validator.*`: validation rules.
- `tests/contracts/*`: valid and invalid fixtures.

## Change unit and authority
- Coherent unit: validator behavior plus its fixtures share one acceptance and rollback boundary.
- Split boundaries: none.
- Commit: approval-required; integration: approval-required; push/deploy/publication: unavailable.

## Acceptance evidence
| Criterion | Result | Evidence |
| --- | --- | --- |
| Invalid fixtures name the invariant | pass | `artifacts/TASK-001/test-summary.txt` |
| Valid fixtures pass | pass | check `contracts-tests`, run `run-018` |

## Verification run
- Command/check: `example-test-command tests/contracts`
- Outcome: pass (12 checks)
- Environment: `worktree:task-001`, adapter `example@1`

## Discoveries and risks
- Symlink-normalized paths need an explicit Phase 2 policy.

## Routing and authority
- Tier used and reason: balanced; bounded implementation with deterministic fixtures.
- Escalation/decomposition: none.
- Routing changed no capability or lifecycle authority.

## Review request
- Focus on normalization and false-positive overlap.

## User-facing closeout
- Outcome: Configuration validation is implemented.
- Stage: Implementation.
- Progress: 1 of 3 graph-validation tasks completed.
- Material changes: Validator behavior and deterministic fixtures.
- Verification: 12 contract checks passed.
- Lifecycle state: completed.
- Blockers: None.
- Next action: Dispatch the next ready task and run assurance review non-blockingly.
- Inspectable paths: `harness-state/PENDING.md`, `harness-state/TASK-GRAPH.md`, and `artifacts/TASK-001/test-summary.txt`.
- Human action required: None.
```

## Invariants

- The handoff pins a task revision and attempt; later attempts create new artifacts.
- Every acceptance criterion has a result and durable evidence pointer, including failures/not-run reasons.
- Changed paths stay within ownership or link to an approved lease change.
- Claims summarize reproducible checks; they do not treat agent confidence as verification.
- `completed` means declared implementation checks passed and the orchestrator may unlock dependents. Independent assurance remains separate and may create remediation without reopening historical completion.
- Blockers name the missing decision, capability, dependency, or external condition.
- The actual model tier and route changes are recorded; a stronger model is never presented as evidence.
- The coherent change unit and commit/integration/push/deploy/publication authority states are explicit and independent.
- The user-facing closeout explains outcome, stage, progress, work continuing without user action, human/macro pending items, active/ready/blocked graph nodes, material changes, verification, lifecycle state, blockers, next action, and inspectable paths before a review or approval boundary.
