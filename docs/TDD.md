# Test-driven task execution

Behavior-changing code tasks and bug fixes in `full-harness` use a RED → GREEN → REFACTOR cycle inside each small executable task. Before that boundary, the [request router](contracts/REQUEST-ROUTE.md) may select `direct-trivial` for a static/mechanical edit or `vibe` for one decided, small local behavior change in one workstream. Neither fast route creates a SPEC or manufactured RED.

Vibe is not a test exemption: it requires a focused deterministic check after the minimum change. It creates no TDD evidence, handoff, review, or other Harness artifact. A missing, ambiguous, or failed check, broader impact, or any hard full trigger promotes the request before further edits; once promoted, normal RED → GREEN applies.

The task spec declares the focused test, expected RED failure, minimal GREEN behavior, and proportional regression set. The implementer observes a meaningful failure before production code, implements the minimum change, reruns the same test to GREEN, then performs bounded cleanup and regression checks. RED and GREEN remain one graph node so the shared baseline is never intentionally handed off failing.

Behavior-preserving refactors use characterization coverage instead of an artificial failure. Non-code work may use `verification-only` only with an explicit reason and reproducible check. Inside graph/full work, `inline-simple` engineering, a hackathon deadline, or an absent test suite does not automatically waive test-first behavior. Fast-route eligibility comes only from the request router and is revoked on scope growth.

See [the executable playbook](../harness/playbooks/test-driven-execution.md), [task contract](contracts/TASK.md), and [handoff contract](contracts/HANDOFF.md).
