---
schema: harness.execution-budget/v1
id: execution-budget-TASK-001
revision: 1
status: active
updated_at: 2000-01-01T00:00:00Z
updated_by: role:orchestrator
---

# Execution budget — TASK-001

The JSON block is the executable budget state. Counters follow the goal lineage across retries, remediation, model changes, decomposition, and session changes.

```json
{
  "schema": "harness.execution-budget/v1",
  "task": "TASK-001@1",
  "goal_lineage": "goal-lineage-001",
  "previous_goal_lineage": null,
  "counter_scope": "goal-lineage",
  "limits": {
    "max_implementation_attempts": 2,
    "max_consecutive_no_progress_cycles": 2,
    "max_context_expansions": 3
  },
  "previous_usage": null,
  "usage": {
    "implementation_attempts": 0,
    "consecutive_no_progress_cycles": 0,
    "context_expansions": 0
  },
  "decision": "continue",
  "reason": "Initial bounded execution state.",
  "evidence_paths": ["harness-state/tasks/TASK-001.md"],
  "token_measurement": "unavailable"
}
```

## Transition log

- r1: Budget initialized from approved policy before dispatch.
