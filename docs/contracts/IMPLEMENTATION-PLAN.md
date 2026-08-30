# Contract: Implementation plan

`harness.implementation-plan/v1` converts approved product authority into small executable units before graph creation. Store instances under `harness-state/plans/`.

## Invariants

- Non-trivial implementation has one plan; a narrowly classified simple task may use only its compact inline task spec.
- Every unit targets two to five minutes of active agent work and has one observable result, exact change, dependencies, scoped paths, non-goals, acceptance, test strategy, verification, and replan triggers.
- Behavior-changing and bug-fix units keep RED and GREEN inside the same task and specify the focused failing test, intended failure reason, minimum passing implementation, and proportional regression set.
- Time spent waiting for tools, CI, downloads, or independent review is not active implementation time.
- Every planned graph node pins the exact plan revision and step through its task brief.
- The task brief is the executable spec. It is self-contained so the implementer does not reload the entire plan during normal execution.
- Missing product behavior returns to discovery. Missing or contradictory implementation detail returns to planning. The implementer does not improvise either.
- Ordinary local coding choices are allowed only when they do not change behavior, contracts, scope, dependencies, permissions, or risk.
- A plan can become `ready` without ceremonial approval when it introduces no consequential decision. Consequential scope, architecture, risk, permission, or budget choices still require their named authority.
- Replanning preserves execution-budget lineage and graph history.

Use [the canonical template](../../harness/templates/IMPLEMENTATION-PLAN.md) and [writing-plans playbook](../../harness/playbooks/writing-plans.md).
