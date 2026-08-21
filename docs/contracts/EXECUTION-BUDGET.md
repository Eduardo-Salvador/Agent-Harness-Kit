# Contract: `harness.execution-budget/v1`

An execution-budget artifact is the durable, machine-checkable state for one goal lineage.

## Required payload

The Markdown artifact contains one JSON block with:

- `schema`: exactly `harness.execution-budget/v1`;
- `task`: current task revision;
- `goal_lineage`: stable identifier inherited by retries, remediation, decomposition, model changes, and session changes that pursue the same outcome;
- `previous_goal_lineage`: preceding lineage identifier, or `null` only for the first state;
- `counter_scope`: exactly `goal-lineage`;
- `limits`: positive integers for `max_implementation_attempts`, `max_consecutive_no_progress_cycles`, and `max_context_expansions`;
- `previous_usage`: the preceding non-negative counter values, or `null` only for the first state;
- `usage`: non-negative values for `implementation_attempts`, `consecutive_no_progress_cycles`, and `context_expansions`;
- `decision`: `continue` or `stop-and-replan`;
- `reason`: concise explanation of the decision;
- `evidence_paths`: non-empty repository-relative paths supporting progress or exhaustion;
- `token_measurement`: `unavailable`, `advisory`, or `host-reported`.

## Executable invariants

1. `goal_lineage` matches `previous_goal_lineage` after initialization, and usage never decreases relative to `previous_usage`.
2. `continue` is invalid when any usage counter is greater than or equal to its matching ceiling.
3. Changing model, agent, task ID, review round, or session does not change `goal_lineage` for the same outcome.
4. Only approved durable policy may change limits. An implementer cannot edit limits or its lineage.
5. At a ceiling, the next lifecycle action is bounded replanning; another work cycle in the same lineage is forbidden.
6. Evidence paths remain inside the repository.

The source validator executes a known-good payload plus hostile mutations for ceiling bypass, counter rollback, invalid scope, and unsafe evidence paths. This proves the encoded invariants, not host-level process termination.
