# Agent Harness Kit example: Development Core

This small trace uses `mode: delivery` and no learning artifacts. The same core transitions are used by the learning example.

On first run, no approved host-project context existed. Discovery classified the project as greenfield, selected Development Core with the user, and obtained context approval before the initial graph was written.

The same copied profile can start through either native entrypoint: Codex reads root `AGENTS.md`; Claude Code reads root `CLAUDE.md`, which imports `@AGENTS.md`. Both reach this same trace and neutral state without a platform profile switch. If the repository is later opened with the other tool, it resumes from the approved context and graph rather than creating a competing harness.

| Step | Canonical change | Notification |
| --- | --- | --- |
| 1 | [Project context](state/PROJECT-CONTEXT.md) and [decision](state/DEC-001.md) become approved | Approved revision is available |
| 2 | [Initial graph](state/TASK-GRAPH.initial.md) exposes `TASK-001` as ready | Task is ready |
| 3 | Orchestrator grants lease/isolation in [task brief](state/TASK-001.md) | Assignment path is announced |
| 4 | Specialist writes a passing [completed handoff](state/HANDOFF-TASK-001-01.md) | Outcome, checks, next action, and human action are reported |
| 5 | Orchestrator writes the [completed graph](state/TASK-GRAPH.completed.md), updates [pending overview](state/PENDING.md), releases ownership, and advances | Task is completed without human approval |
| 6 | Independent reviewer writes automatic [assurance](state/REVIEW-TASK-001-01.md) | Non-blocking verdict is recorded |

The messages in the last column are insufficient without their referenced files. Native instruction discovery is mapped, while optional runtime capabilities remain evidence-based rather than assumed.
