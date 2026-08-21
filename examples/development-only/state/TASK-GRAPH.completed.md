---
schema: harness.task-graph/v1
id: graph-main
revision: 2
status: complete
project_context: project-context@1
updated_at: 2026-08-20T10:45:00Z
updated_by: role:orchestrator
discovery_snapshot: example-greenfield-001
source_references: none
---

# Task graph

```json
{
  "nodes": [
    {
      "id": "TASK-001",
      "goal": "Add deterministic configuration validation",
      "depends_on": [],
      "status": "accepted",
      "assignee": "agent:specialist",
      "reviewer": "agent:reviewer",
      "write_set": ["src/config/**", "tests/config/**"],
      "checkpoint": null,
      "task_brief": "TASK-001.md"
    }
  ]
}
```

## Transition log

- r1: TASK-001 ready and ownership granted.
- r2: Independent review accepted; evidence `REVIEW-TASK-001-01`; lease released.
