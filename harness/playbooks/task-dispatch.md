# Playbook: Task dispatch

1. Orchestrator selects a node whose dependencies are completed and checkpoint/capability requirements pass.
2. Compare its normalized write set with all ready/active leases; serialize or repartition any collision.
3. Select an implementer and distinct reviewer. Classify the workstream and follow [execution-context routing](context-routing.md); negotiate the adapter capability manifest before creating a chat, task, subagent, or manual context.
4. Initialize or inherit the executable goal-lineage budget before dispatch. The same outcome keeps cumulative counters across model, agent, task, remediation, decomposition, review, and session changes.
5. Follow [capability-based model routing](model-routing.md): choose the least costly safe tier, record `model_tier` and `model_reason`, and resolve the tier through the active adapter.
6. Grant an explicit lease and isolation identifier; update graph and task revisions atomically or stop on stale state. Record the ready → active transition, lease, context, and evidence in `TASK-GRAPH.md` before announcing dispatch.
7. Create/resume the declared context through the adapter, persist its reference, and send a notification pointing to the task artifact. The specialist loads only declared context. Different workstreams cannot share one context except a bounded integration node.
8. On lost notification, reconciliation discovers the active artifact; no canonical state is lost.

Before each new implementation cycle or context expansion, reconcile the linked [`harness.execution-budget/v1`](../../docs/contracts/EXECUTION-BUDGET.md) state. At any ceiling, stop that lineage and replan; do not hide a retry behind a stronger model or a new task ID.

Local checks, completion, post-completion review, focused remediation, and graph transitions declared by an approved task are part of its execution authority. Announce material results and continue; do not turn each one into a fresh human approval request. Use [task closeout](task-closeout.md) and dispatch the next ready node after completion.

Dispatch fails closed if permissions, ownership, isolation, model-tier availability, or evidence facilities are ambiguous.

After dispatch, every material technical event updates `TASK-GRAPH.md` in the same operational step: progress evidence, dependency discovery, block/unblock, context or lease change, remediation, completion, and newly ready dependents. `PENDING.md` is not a technical event log and cannot substitute for this write. Change it alongside the graph only when human action or the macro completion overview changed.
