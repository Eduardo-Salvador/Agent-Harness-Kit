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
      "write_set": ["replace/path/**"],
      "checkpoint": null,
      "task_brief": "tasks/TASK-001.md"
    }
  ]
}
```

## Transition log

- r1: Draft graph created from approved project context.
