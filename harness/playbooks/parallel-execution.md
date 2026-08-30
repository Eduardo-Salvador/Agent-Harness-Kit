# Playbook: Parallel execution and isolation

This is an agent-driven scheduler loop, not a background daemon. While an orchestrator context is active, it automatically fills proven implementation capacity with collision-safe graph nodes.

1. Read the validated DAG and current capability manifest. `parallel_contexts` must include a numeric implementation capacity and current host evidence; otherwise use `sequential-fallback` and never claim concurrency.
2. Run `agent-harness schedule harness-state/TASK-GRAPH.md --capacity <host-capacity>`. The deterministic selector uses stable graph order, subtracts active contexts, rechecks completed dependencies and accepted assurance, and excludes normalized parent/child, identical, wildcard-prefix, and platform-equivalent write collisions.
3. Treat `ready` as dependency/checkpoint/capability eligible but possibly deferred by capacity or an active lease. Only `active` nodes own running contexts; simultaneous active write sets and context references must never overlap.
4. Create `harness.parallel-dispatch/v1` as `reserving` against the expected graph revision. For every selected node reserve a distinct lease, isolation, task SPEC, model-dispatch route, workstream/role, and context slot. A stale revision aborts before launch.
5. Invoke the host's actual subagent/task operation for every selected node without waiting for an earlier child to finish. Each child receives only its task artifact and declared context packet. Persist every returned context and adapter response; only confirmed launches transition to `active`.
6. If one launch fails, mark the batch `partial`/`blocked`, release that reservation, and continue safely launched siblings. Never execute the failed child silently in the orchestrator context or duplicate a returned context.
7. Wait for the first completion or attention event rather than the whole batch. Reconcile its handoff, graph revision, review route, lease, and slot, then rerun the selector immediately to refill capacity. Repeat until no safe node is ready or all slots are occupied.
8. Keep shared/generated outputs outside concurrent ownership. Parallel branches meet only through a dependency-gated integration node with its own write set, context, verification, and review.
9. Renew/release leases and task contexts through the orchestrator. Recover orphaned reservations/contexts from graph, dispatch, model-dispatch, and handoff artifacts before reassignment. Duplicate events are idempotent against task/context/graph identity.
10. Revalidate graph revision, ownership, model/context evidence, and capacity before handoff acceptance.

Automatic fan-out, refill, and fan-in do not create repeated human approval gates. Never allow concurrent writers merely because their intended edits are “probably different.”
