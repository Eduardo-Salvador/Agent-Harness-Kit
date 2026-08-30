# Test-driven task execution

Behavior-changing code tasks and bug fixes use a RED → GREEN → REFACTOR cycle inside each small executable task. A `direct-trivial` presentation/static-content edit—such as one color, spacing value, typo, or static label with no logic, state, rule, contract, data, dependency, accessibility behavior, or risk—is edited directly without a SPEC or manufactured RED.

The task spec declares the focused test, expected RED failure, minimal GREEN behavior, and proportional regression set. The implementer observes a meaningful failure before production code, implements the minimum change, reruns the same test to GREEN, then performs bounded cleanup and regression checks. RED and GREEN remain one graph node so the shared baseline is never intentionally handed off failing.

Behavior-preserving refactors use characterization coverage instead of an artificial failure. Non-code work may use `verification-only` only with an explicit reason and reproducible check. `inline-simple` engineering work, a hackathon deadline, or an absent test suite does not automatically waive test-first behavior; `direct-trivial` is a separate pre-task route and leaves it immediately when real behavior appears.

See [the executable playbook](../harness/playbooks/test-driven-execution.md), [task contract](contracts/TASK.md), and [handoff contract](contracts/HANDOFF.md).
