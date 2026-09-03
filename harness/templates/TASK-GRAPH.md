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
For a same-context node with `assurance: none`, the completion transition stores the concise outcome and highest sufficient test-ladder rung. It is the complete durable closeout: do not create a handoff, review packet, copied log, or separate evidence file. Create transfer/review artifacts only when `light|full` assurance or a human handoff supplies an actual separate consumer.
Ready nodes do not own files or contexts. When more than one is eligible, use the parallel scheduler to defer write collisions, reserve a safe batch up to proven numeric capacity, and link the resulting `harness.parallel-dispatch/v1` artifact in the transition log. Parallel branches converge through an explicit integration node.

```json
{
  "nodes": [
    {
      "id": "TASK-001",
      "goal": "Replace with a bounded outcome",
      "depends_on": [],
      "product_requires": [],
      "scope_status": "approved",
      "acceptance_revision": 1,
      "acceptance_criteria": [{"id": "AC-001", "condition": "Replace with the exact implemented behavior and observable successful result"}],
      "test_strategy": "tdd",
      "runtime_smoke_required": false,
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
      "target_minutes": 20,
      "evidence_profile": "handoff-review",
      "assurance": "full",
      "artifact_policy": "transfer",
      "handoff_consumer": "reviewer",
      "test_ladder": "focused-unit",
      "checkpoint": null,
      "assurance_status": "pending",
      "assurance_requires": [],
      "task_brief": "tasks/TASK-001.md"
    }
  ]
}
```

## Transition log

For substantial product builds, declare milestone `product_review` and link affected dependents through `product_requires` as described in [accompanied delivery](../../docs/ACCOMPANIED-DELIVERY.md). Record revision-pinned `verification` inline before completion. Empty `product_requires` is for genuinely independent work, not permission to omit a planned client milestone.

- r1: Draft graph created from approved project context.
