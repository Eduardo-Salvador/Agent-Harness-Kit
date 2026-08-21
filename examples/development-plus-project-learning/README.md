# Agent Harness Kit example: Development Core plus project-specific learning

This trace runs the same delivery core with `mode: delivery+learning`. Learning observes approved evidence after delivery transitions; it never becomes a dependency or graph writer.

On first run, discovery inspected an existing parser project, filled only missing context, obtained consent for project-specific learning, and approved context before the initial graph was written. The Harness Engineering Learning Pack was not loaded.

The `core-learning` files were available before consent, but availability did not activate observation, retention, or publication; the approved learning profile did.

Codex can enter this copied profile through root `AGENTS.md`, and Claude Code through root `CLAUDE.md` importing `@AGENTS.md`. Both route to the same neutral delivery and learning artifacts; neither platform entrypoint activates learning, and changing tools does not require changing profiles.

| Step | Delivery artifact change | Learning artifact change |
| --- | --- | --- |
| 1 | [Context](state/PROJECT-CONTEXT.md) approved; [graph](state/TASK-GRAPH.initial.md) makes `TASK-101` ready | [Profile](project-learning/LEARNING-PROFILE.md) activates explicit consent |
| 2 | Orchestrator dispatches [task](state/TASK-101.md) with lease/isolation | None |
| 3 | Specialist writes a passing [completed handoff](state/HANDOFF-TASK-101-01.md) | Assessor may read only consented reasoning/evidence |
| 4 | Orchestrator writes [completed graph](state/TASK-GRAPH.completed.md), updates [pending overview](state/PENDING.md), and advances | Delivery does not wait for approval or review |
| 5 | Reviewer writes automatic [assurance](state/REVIEW-TASK-101-01.md) | [Queue](project-learning/LEARNING-QUEUE.md) gains a practice proposal; [debrief](project-learning/DEBRIEF-001.md) remains local |

The graph contains no project-learning node or dependency. Removing `project-learning/` leaves the delivery trace valid.
