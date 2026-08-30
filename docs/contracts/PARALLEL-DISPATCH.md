# Contract: Parallel dispatch

Runtime evidence that one graph revision produced a collision-safe batch and that every selected task was actually launched in a distinct execution context. A list of ready IDs is a plan, not dispatch evidence.

```yaml
---
schema: harness.parallel-dispatch/v1
id: parallel-dispatch-001
revision: 1
graph: graph-main@7
status: completed                 # reserving | completed | partial | blocked
capacity: 3
active_before: 1
capability_evidence: capability-manifest@2
scheduler_plan: scheduler-plan:sha256-example
created_at: 2026-08-30T16:00:00Z
created_by: role:orchestrator
---
```

## Selection

- The scheduler uses a validated graph snapshot and numeric implementation capacity evidenced by the current host.
- It selects stable graph order from `ready` nodes whose dependencies are completed and assurance gates accepted, excluding normalized write collisions with active or already selected tasks.
- `ready` means dependency/checkpoint/capability eligible. Capacity and active leases may temporarily defer it; only `active` tasks own running contexts.

## Reservation transaction

- Before spawning, the orchestrator records the expected graph revision, selected IDs, normalized write sets, distinct lease/isolation reservations, task SPEC revisions, and resolved model-dispatch references.
- The orchestrator is the sole graph writer. A stale revision aborts the batch before launch.
- Reservations prevent duplicate dispatch. A failed launch releases its reservation and becomes durable `partial`/`blocked` evidence.

## Adapter dispatch evidence

For every selected task record:

- task and pinned SPEC revision;
- distinct lease/isolation ID;
- actual subagent/task context reference;
- adapter operation/response evidence;
- resolved `harness.model-dispatch/v1` reference;
- launch outcome and graph transition revision.

`completed` requires one confirmed dispatch per selected task, no duplicate context/lease, and `active_before + dispatched <= capacity`. Pending, self-asserted, or missing references are invalid.

## Refill and fan-in

- Wait for the first completion or attention event, reconcile its handoff, graph state, lease, and review route, then rerun scheduling immediately to fill the freed slot.
- A dependent becomes ready only when every declared dependency and assurance gate passes.
- Parallel branches join through an explicit integration node with its own write set, SPEC, context, verification, and review. Children never merge themselves or share integration outputs concurrently.

## Recovery

- Lost notifications are reconciled from graph, dispatch, model-dispatch, and handoff artifacts.
- Duplicate events are idempotent against the pinned task/context/graph revision.
- If parallel capability disappears, finish or recover active children and record `sequential-fallback`; do not claim concurrency.
