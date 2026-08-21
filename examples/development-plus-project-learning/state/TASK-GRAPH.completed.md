---
schema: harness.task-graph/v1
id: graph-learning-example
revision: 3
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
      "status": "completed",
      "assignee": "agent:specialist",
      "reviewer": "agent:reviewer",
      "write_set": ["tests/parser/**"],
      "checkpoint": null,
      "assurance_status": "accepted",
      "assurance_requires": [],
      "task_brief": "TASK-101.md"
    }
  ]
}
```

## Transition log

- r1: TASK-101 ready and ownership granted.
- r2: Declared checks passed; node completed, lease released, dependents unlocked, and user closeout emitted.
- r3: Automatic post-completion assurance accepted. Learning queue did not affect delivery.
