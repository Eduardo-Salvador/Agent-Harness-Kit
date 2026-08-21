---
schema: harness.task-graph/v1
id: graph-main
revision: 1
status: active
project_context: project-context@1
updated_at: 2026-08-20T10:05:00Z
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
      "status": "ready",
      "assignee": "agent:specialist",
      "reviewer": "agent:reviewer",
      "write_set": ["src/config/**", "tests/config/**"],
      "checkpoint": null,
      "assurance_status": "pending",
      "assurance_requires": [],
      "task_brief": "TASK-001.md"
    }
  ]
}
```

## Transition log

- r1: Human-approved context activated; TASK-001 is ready.
