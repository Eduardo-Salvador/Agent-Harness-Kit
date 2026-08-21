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

Every rendered status and machine payload must contain:

- stage;
- measurable progress or a precise qualitative baseline;
- human actions from the pending authority;
- blockers, explicitly `None` when empty;
- one next action; and
- repository-relative inspectable paths, including the consulted pending authority and task graph.

The executable payload shape is `stage`, `progress`, `blockers[]`, `next_action`, `inspectable_paths[]`, and `human_pending[]`. Every human-pending item includes `action` and `source`. Absolute paths and `..` traversal are invalid.

See `validation/status-fixtures/`: the validator starts from a valid payload, applies hostile field-removal/path mutations, and proves that the contract rejects them.
