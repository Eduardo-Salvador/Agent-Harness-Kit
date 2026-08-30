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

The JSON block is the executable graph view. `write_set` contains exclusively leased paths. `read_set` narrows the source context to load, while `impact_set` bounds related regression analysis; neither grants write ownership. All sets use repository-relative paths or directory globs ending in `/**`. `context_provenance` records how those hints were established and the source revision used.
This artifact owns technical order, dependencies, readiness, leases, remediation, and execution. Human decisions/actions and the macro view of unfinished project areas belong in `harness-state/PENDING.md`, not here.
Revise this artifact in the same operational step as every technical event and before announcing it. The transition log records dispatch/start, material progress evidence, dependency changes, block/unblock, remediation, completion, lease/context changes, and newly ready nodes.
Ready nodes do not own files or contexts. When more than one is eligible, use the parallel scheduler to defer write collisions, reserve a safe batch up to proven numeric capacity, and link the resulting `harness.parallel-dispatch/v1` artifact in the transition log. Parallel branches converge through an explicit integration node.

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
      "read_set": ["replace/path/entrypoint.ext", "replace/shared/**"],
      "write_set": ["replace/path/**"],
      "impact_set": ["replace/tests/**", "replace/consumer/**"],
      "context_provenance": "source-inspection@replace-revision",
      "planning_mode": "planned",
      "implementation_plan": "plans/PLAN-001.md@1",
      "plan_step": "STEP-001",
      "target_minutes": 5,
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
