---
schema: harness.handoff/v1
id: HANDOFF-TASK-001-01
task: TASK-001@1
attempt: 1
status: completed
author: agent:implementer
workstream: replace-area
agent_role: role:generic-specialist
execution_context: isolated
thread_ref: adapter-owned-or-manual
created_at: 2000-01-01T00:00:00Z
model_tier_used: balanced
model_route_changes: none
execution_budget: execution-budget-TASK-001@2
---

# Handoff — TASK-001

## Result

Replace with the bounded result or blocker.

- Execution context: Record the adapter evidence/reference and whether it was closed, retained, or degraded.

## Changes

- `path`: concise purpose.

## Change unit and authority

- Coherent unit: Replace with the shared acceptance/rollback boundary.
- Split boundaries: None, or list meaningful ownership/deployability/risk/dependency/rollback splits.
- Commit/integration/push/deploy/publication authority: Record each as authorized, approval-required, or unavailable.

## Acceptance evidence

| Criterion | Result | Evidence |
| --- | --- | --- |
| Replace | pass/fail/not-run | Durable path or run identifier |

## Verification run

- Command/check: Replace.
- Outcome: Replace.
- Environment/adapter: Replace.

## Execution budget

- Goal lineage: Replace.
- Usage: Replace with implementation attempts, consecutive no-progress cycles, and context expansions.
- Decision: `continue` or `stop-and-replan` with the inspectable budget artifact path.
- Token/cost measurement: `unavailable`, `advisory`, or `host-reported`; never estimate unavailable usage.

## Discoveries and risks

- None known.

## Routing and authority

- Tier used and reason: Replace.
- Escalation/decomposition: None, or record prior tier, trigger, and resulting route.
- Routing granted no additional permissions and removed no review or verification gate.

## Review request

- Focus on the acceptance criteria and declared risks.

## User-facing closeout

- Outcome: Replace with a plain-language result.
- Stage: Replace with the current project or delivery stage.
- Progress: Replace with a measurable value or precise baseline.
- Material changes: Replace with behavior and key paths.
- Verification: Replace with checks and outcomes.
- Lifecycle state: completed / blocked / failed. If blocked, state separately whether the pending owner is human or software.
- Blockers: None, or list exact blockers and owners.
- Next action: Replace with the next ready task; post-completion review runs automatically and non-blockingly.
- Inspectable paths: Replace with repository-relative evidence paths, including the consulted pending authority and graph for project status.
- Human action required: None, or one exact decision/action with reason and effect.
