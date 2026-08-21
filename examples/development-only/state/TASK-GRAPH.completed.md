---
schema: harness.task-graph/v1
id: graph-main
revision: 3
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
      "status": "completed",
      "assignee": "agent:specialist",
      "reviewer": "agent:reviewer",
      "write_set": ["src/config/**", "tests/config/**"],
      "checkpoint": null,
      "assurance_status": "accepted",
      "assurance_requires": [],
      "task_brief": "TASK-001.md"
    }
  ]
}
```

## Transition log

- r1: TASK-001 ready and ownership granted.
- r2: Declared checks passed; node completed, lease released, dependents unlocked, and user closeout emitted.
- r3: Automatic post-completion assurance accepted; evidence `REVIEW-TASK-001-01`.
