# The seven harness components

The components describe a task node's operating environment:

| Component | Question it answers | Repository example |
| --- | --- | --- |
| System prompt | What role, authority, loop, and exit apply? | [Bounded roles](../harness/roles/README.md) |
| Tools | What operations are actually available? | [Generic adapter manifest](../adapters/generic.md) |
| Context management | What must be loaded now, and what stays out? | Task `Context to load` plus [progressive context](../docs/ARCHITECTURE.md#progressive-context) |
| Verification | What objective evidence admits completion? | Task criteria, handoff evidence, and [review playbook](../harness/playbooks/review-integration.md) |
| Memory | What durable facts survive the session? | Versioned context, decisions, graph, tasks, and handoffs |
| Sandboxes | Where can work happen without collisions? | Lease/isolation fields and [parallel playbook](../harness/playbooks/parallel-execution.md) |
| Hooks | How are lifecycle changes surfaced? | Adapter event capability plus file reconciliation fallback |

These components operate inside nodes. The dependency graph coordinates nodes above them; it does not replace the components.
