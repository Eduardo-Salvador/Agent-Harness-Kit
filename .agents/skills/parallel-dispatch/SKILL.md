---
name: parallel-dispatch
description: Automatically use when two or more graph nodes may be ready for implementation and the host may support parallel subagents or tasks. Select a safe batch, dispatch it without waiting between launches, keep capacity filled, and fan in only through declared dependencies/integration nodes.
---

# Parallel dispatch

Follow `../../../harness/playbooks/parallel-execution.md`. Activate automatically after graph reconciliation whenever at least two nodes are `ready`; the user does not need to name this skill.

1. Read the host-evidenced numeric implementation capacity and the current graph revision. If parallel contexts are unavailable, record `sequential-fallback`; do not claim parallel execution.
2. Run `agent-harness schedule harness-state/TASK-GRAPH.md --capacity <host-capacity>` (or the equivalent packaged CLI) and use only its selected IDs. The scheduler rechecks completed dependencies, accepted assurance, active capacity, and normalized write collisions.
3. For the whole selected batch, pin task specs, reserve distinct leases/isolations/model-dispatch routes under the expected graph revision, and create `harness.parallel-dispatch/v1` as `reserving`. Never dispatch from conversational memory.
4. Invoke the actual Codex subagent/task operation once for every selected node without waiting for earlier children to complete. Use separate calls/references, explicit model/reasoning overrides, and the smallest declared context packet. Calls may return sequentially; the children must remain running concurrently.
5. Persist each returned agent/task reference and adapter evidence, transition only confirmed children to `active`, and report the active worker count.
6. Wait for the first child completion or attention event and refill free capacity. At 60–90 seconds without observable progress, warn/request a checkpoint; on the second consecutive occurrence, interrupt, preserve state, and reassign or serialize within budget.
7. Dependents become ready only after all declared dependencies and assurance gates pass. Cross-area results meet in an explicit integration node; never let parallel children edit shared integration/generated outputs concurrently.

Automatic fan-out, refill, and fan-in are normal execution and require no repeated human approval. Human input is requested only for a genuine authority/product/risk decision.
