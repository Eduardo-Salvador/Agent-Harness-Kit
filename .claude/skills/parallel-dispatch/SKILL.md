---
name: parallel-dispatch
description: Automatically use when two or more graph nodes may be ready and the Claude host exposes parallel subagents or tasks. Select a collision-safe batch, launch every child, keep capacity filled, and join through declared dependencies.
---

# Parallel dispatch

Follow `../../../harness/playbooks/parallel-execution.md` and the same neutral `harness.parallel-dispatch/v1` contract used by Codex. Activate automatically when at least two nodes are ready.

Use the host-evidenced numeric implementation capacity and `agent-harness schedule harness-state/TASK-GRAPH.md --capacity <host-capacity>`. Reserve distinct write leases and contexts for the selected batch, then invoke the actual Claude subagent/task operation for every selected node without waiting for earlier children to finish. Persist returned references and adapter evidence before confirming nodes active. Wait for the first completion/attention event, reconcile graph and leases, and immediately refill free capacity. If the host lacks parallel subagents, record `sequential-fallback`; never simulate parallelism in one context. Fan-in occurs only through declared dependency/integration nodes.
