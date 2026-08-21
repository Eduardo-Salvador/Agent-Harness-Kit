# Playbook: Task dispatch

1. Orchestrator selects a node whose dependencies are completed and checkpoint/capability requirements pass.
2. Compare its normalized write set with all ready/active leases; serialize or repartition any collision.
3. Select an implementer and distinct reviewer. Negotiate the adapter capability manifest.
4. Follow [capability-based model routing](model-routing.md): choose the least costly safe tier, record `model_tier` and `model_reason`, and resolve the tier through the active adapter.
5. Grant an explicit lease and isolation identifier; update graph and task revisions atomically or stop on stale state.
6. Send a notification pointing to the task artifact. The specialist loads only declared context.
7. On lost notification, reconciliation discovers the active artifact; no canonical state is lost.

Local checks, completion, post-completion review, focused remediation, and graph transitions declared by an approved task are part of its execution authority. Announce material results and continue; do not turn each one into a fresh human approval request. Use [task closeout](task-closeout.md) and dispatch the next ready node after completion.

Dispatch fails closed if permissions, ownership, isolation, model-tier availability, or evidence facilities are ambiguous.
