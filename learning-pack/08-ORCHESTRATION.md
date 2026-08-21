# Orchestration and graph engineering

Orchestration coordinates task nodes above their agent loops. A dependency edge means one node cannot become ready until the prerequisite reaches the required accepted state. A **ready node** has satisfied dependencies, checkpoints, capabilities, and ownership constraints.

Parallelism is a graph property before it is an agent-count choice. Two ready nodes may run together only when their normalized exclusive write sets do not collide and the platform can provide safe isolation. Parent/child paths, wildcard prefixes, shared generated files, and platform-equivalent paths can collide.

Stale context creates another race: an agent dispatched from an old graph revision may act after priorities, dependencies, or ownership changed. Expected-revision writes and pre-acceptance revalidation prevent the old view from silently winning.

Study the [task-graph template](../harness/templates/TASK-GRAPH.md), [dispatch playbook](../harness/playbooks/task-dispatch.md), and validator fixtures. Then sketch two independent nodes and choose write sets that are provably disjoint; add an integration node for any shared output.
