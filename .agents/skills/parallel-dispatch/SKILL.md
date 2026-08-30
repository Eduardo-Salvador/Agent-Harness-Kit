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
5. Persist each returned agent/task reference and adapter evidence, then transition only confirmed children to `active`. A failed launch becomes a durable blocked/failed dispatch entry, releases its reservation, and cannot be silently replaced by work in the orchestrator context.
6. Wait for the first child completion or attention event, not for the entire batch. Reconcile its handoff and graph transition, release its slot/lease when appropriate, recompute the ready batch, and immediately refill free capacity. Repeat until no safe node is ready or capacity is full.
7. Dependents become ready only after all declared dependencies and assurance gates pass. Cross-area results meet in an explicit integration node; never let parallel children edit shared integration/generated outputs concurrently.

Automatic fan-out, refill, and fan-in are normal execution and require no repeated human approval. Human input is requested only for a genuine authority/product/risk decision.
