---
name: parallel-dispatch
description: Automatically use when two or more graph nodes may be ready and the Claude host exposes parallel subagents or tasks. Select a collision-safe batch, launch every child, keep capacity filled, and join through declared dependencies.
---

# Parallel dispatch

Follow `../../../harness/playbooks/parallel-execution.md` and the same neutral `harness.parallel-dispatch/v1` contract used by Codex. Activate automatically when at least two nodes are ready.

Use proven numeric capacity greater than one and schedule only collision-free ready nodes. Launch the selected batch, persist references before confirming nodes active, and report the actual active worker count. Refill after the first completion/attention event. At 60–90 seconds without observable progress, warn/request a checkpoint; on the second consecutive occurrence, interrupt, preserve state, and reassign or serialize within budget. If the host lacks parallel subagents, record `sequential-fallback`.
