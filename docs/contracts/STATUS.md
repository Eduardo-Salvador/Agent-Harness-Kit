# Contract: Status update

A status update is a derived, user-facing view. It never replaces `PENDING.md` or `TASK-GRAPH.md`; it proves which revisions were consulted and makes the answer inspectable.

```yaml
---
schema: harness.status/v1
id: STATUS-CURRENT
revision: 1
generated_at: 2026-08-21T12:00:00Z
generated_by: agent:orchestrator
project_context: project-context@1
pending_authority: pending-main@1
task_graph: graph-main@1
---
```

Every rendered status or user-facing progress/step update and machine payload must contain:

Rendered labels may be localized to the user's language, but the sections and payload fields remain mandatory and separate.

- stage;
- measurable progress or a precise qualitative baseline;
- work that continues automatically under existing authority, explicitly `None` when empty;
- human actions from the pending authority;
- incomplete macro project areas from the pending authority;
- a graph snapshot with active, ready, and blocked nodes from the task graph;
- a workstream view with progress, human pending items, technical pending items, active agent/context, blockers, and next action for each relevant area;
- blockers, explicitly `None` when empty;
- one next action; and
- repository-relative inspectable paths, including the consulted pending authority and task graph.

The executable payload shape is `stage`, `progress`, `automatic_actions[]`, `human_pending[]`, `macro_pending[]`, `state_revisions`, `technical_transition`, `graph_snapshot`, `workstreams[]`, `blockers[]`, `next_action`, and `inspectable_paths[]`. `state_revisions` contains the exact `pending` and `task_graph` revisions consulted. `technical_transition` contains `occurred`, `graph_updated`, `graph_revision`, and `node_changes[]`; when a transition occurred, the graph must be updated, its revision must match `state_revisions.task_graph`, and node changes cannot be empty. `graph_snapshot` contains `active_nodes[]`, `ready_nodes[]`, and `blocked_nodes[]`. Every human-pending item includes `action` and `source`. Every workstream item includes `area`, `progress`, `human_pending[]`, `technical_pending[]`, `active_context`, `blockers[]`, and `next_action`. Absolute paths and `..` traversal are invalid.

See `validation/status-fixtures/`: the validator starts from a valid payload, applies hostile field-removal/path mutations, and proves that the contract rejects them.
