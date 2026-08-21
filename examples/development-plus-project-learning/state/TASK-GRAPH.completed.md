---
schema: harness.task-graph/v1
id: graph-learning-example
revision: 2
status: complete
project_context: project-context-learning-example@1
updated_at: 2026-08-20T11:45:00Z
updated_by: role:orchestrator
discovery_snapshot: example-existing-001
source_references: none
---

# Task graph

```json
{
  "nodes": [
    {
      "id": "TASK-101",
      "goal": "Add parser boundary tests",
      "depends_on": [],
      "status": "accepted",
      "assignee": "agent:specialist",
      "reviewer": "agent:reviewer",
      "write_set": ["tests/parser/**"],
      "checkpoint": null,
      "task_brief": "TASK-101.md"
    }
  ]
}
```

## Transition log

- r1: TASK-101 ready and ownership granted.
- r2: Review accepted; lease released. Learning queue did not affect transition.
