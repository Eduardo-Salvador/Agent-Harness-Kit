---
schema: harness.parallel-dispatch/v1
id: parallel-dispatch-001
revision: 1
graph: graph-main@1
status: reserving
capacity: 2
active_before: 0
capability_evidence: capability-manifest@1
scheduler_plan: scheduler-plan:replace
created_at: 2000-01-01T00:00:00Z
created_by: role:orchestrator
---

# Parallel dispatch — batch 001

## Selection

- Selected tasks and normalized write sets: Replace from the deterministic scheduler output.
- Deferred tasks and exact reasons: Replace.

## Reservation transaction

- Expected graph revision: Replace.
- Task SPEC / lease / isolation / model-dispatch reservation per selected task: Replace.

## Adapter dispatch evidence

| Task | Context | Lease/isolation | Model dispatch | Adapter evidence | Outcome / graph revision |
| --- | --- | --- | --- | --- | --- |
| replace | replace | replace | replace | replace | replace |

## Refill and fan-in

- First completion/attention event: Replace.
- Released/refilled slot: Replace.
- Newly ready dependents or integration node: Replace.

## Recovery

- None, or record failed launch, released reservation, lost notification reconciliation, capacity degradation, or sequential fallback.
