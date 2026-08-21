# Bounded execution budget

Every dispatched implementation task carries one executable budget state. The budget prevents a capable agent from spending an unbounded number of turns while producing no accepted progress.

## Default ceilings

| Counter | Default | Meaning |
| --- | ---: | --- |
| Implementation attempts | 2 | Completed implementation-and-verification cycles in the same goal lineage |
| Consecutive no-progress cycles | 2 | Cycles that add no durable artifact, acceptance progress, or materially new diagnostic evidence |
| Context expansions | 3 | Loads beyond the pinned task packet and direct graph neighborhood |

Projects may approve lower ceilings. Raising a ceiling is a durable policy change and requires the authority named by the project rules; an agent cannot raise it to finish its own task.

## Counter scope

Counters belong to the `goal_lineage`, not to a model, agent, chat, review round, or task filename. Model escalation, retry, remediation, handoff, session restart, and decomposition do not silently reset usage. A genuinely different outcome may start a new lineage when the orchestrator records why it is distinct.

An implementation attempt ends when verification runs or when the agent stops without being able to run it. A no-progress cycle is counted when the cycle produces neither a durable change nor new evidence that narrows the next action. Reading more than the task packet, direct dependencies, scoped rules, and already-approved evidence counts as a context expansion.

## Ceiling behavior

Before beginning another cycle or expanding context, update the budget state. If any counter has reached its ceiling, `decision` must be `stop-and-replan`. The agent persists evidence, reports the exhausted counter, and returns control to the orchestrator. It must not perform another implementation attempt, broad scan, context expansion, or model escalation inside that lineage.

The orchestrator then chooses one bounded action: rewrite acceptance, decompose the outcome, correct missing context, or request one genuine human product/risk decision. It may continue unrelated ready graph nodes. Budget exhaustion is never an invitation to repeat the same work under a new agent or stronger model.

## Token measurement

Host-reported token or cost data may be recorded as advisory evidence, but the three structural counters remain mandatory because hosts do not expose usage consistently. Never invent token counts. A future autonomous runtime may enforce an additional numerical token or time ceiling without weakening these limits.

See the executable [`harness.execution-budget/v1` contract](contracts/EXECUTION-BUDGET.md) and its reusable [template](../harness/templates/EXECUTION-BUDGET.md).
