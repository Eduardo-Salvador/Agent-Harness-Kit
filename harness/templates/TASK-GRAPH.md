---
schema: harness.task-graph/v1
id: graph-main
revision: 1
status: draft
project_context: project-context@1
updated_at: 2000-01-01T00:00:00Z
updated_by: role:orchestrator
discovery_snapshot: discovery-001
source_references: none
---

# Task graph

The JSON block is the executable graph view. `write_set` contains repository-relative paths or directory globs ending in `/**`.
This artifact owns technical order, dependencies, readiness, leases, remediation, and execution. Human decisions/actions and the macro view of unfinished project areas belong in `harness-state/PENDING.md`, not here.
Revise this artifact in the same operational step as every technical event and before announcing it. The transition log records dispatch/start, material progress evidence, dependency changes, block/unblock, remediation, completion, lease/context changes, and newly ready nodes.

```json
{
  "nodes": [
    {
      "id": "TASK-001",
      "goal": "Replace with a bounded outcome",
      "depends_on": [],
      "status": "ready",
      "assignee": "unassigned",
      "reviewer": "unassigned",
      "workstream": "replace-area",
      "agent_role": "role:generic-specialist",
      "execution_context": "isolated",
      "thread_policy": "create-per-task",
      "thread_ref": "pending",
      "write_set": ["replace/path/**"],
      "checkpoint": null,
      "assurance_status": "pending",
      "assurance_requires": [],
      "task_brief": "tasks/TASK-001.md"
    }
  ]
}
```

## Transition log

- r1: Draft graph created from approved project context.
