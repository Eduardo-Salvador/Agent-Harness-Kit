# Agent loops and stopping conditions

An agent loop is a bounded cycle inside one task: inspect relevant state, act within authority, run checks, update evidence, and decide whether to continue. A productive loop has an objective exit, not “keep trying until confident.”

This harness uses three exits for an implementer:

- `ready-for-review`: acceptance evidence is present for every criterion;
- `blocked`: a named decision, dependency, capability, or external condition prevents progress;
- `failed`: the bounded attempt ended with recorded evidence.

None means “accepted.” A different reviewer writes a verdict, and the orchestrator changes graph state. This separates local reasoning from system-level completion.

Study the [generic specialist role](../harness/roles/generic-specialist.md), [task template](../harness/templates/TASK.md), and [handoff template](../harness/templates/HANDOFF.md). In the [development-only example](../examples/development-only/README.md), follow the task, handoff, review, and graph revisions in order.
