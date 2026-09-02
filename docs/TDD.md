# Test-driven task execution

Behavior-changing code tasks and bug fixes in `full-harness` use a RED → GREEN → REFACTOR cycle inside each small executable task. Before that boundary, the [request router](contracts/REQUEST-ROUTE.md) may select `direct-trivial` for a static/mechanical edit or `vibe` for one decided, small local behavior change in one workstream. Neither fast route creates a SPEC or manufactured RED.

Vibe is not a test exemption: it requires a focused deterministic check after the minimum change. A failed check starts bounded recovery inside the approved scope and promotes only when it reveals a full-Harness condition.

The task spec declares the focused test, expected RED failure, minimal GREEN behavior, and proportional regression set. The implementer observes a meaningful failure before production code, implements the minimum change, and reruns the same test to GREEN. Verification then climbs only as needed through `focused` → `workspace` → `integration` → `global/checkpoint` → `delivery`, recording the highest sufficient rung. RED and GREEN remain one graph node.

Behavior-preserving refactors use characterization coverage instead of an artificial failure. Non-code work may use `verification-only` only with an explicit reason and reproducible check. Inside graph/full work, `inline-simple` engineering, a hackathon deadline, or an absent test suite does not automatically waive test-first behavior. Fast-route eligibility comes only from the request router and is revoked on scope growth.

Record TDD evidence in the same-context transition/closeout. Create a [handoff](contracts/HANDOFF.md) only when an actual separate consumer needs it. See [the executable playbook](../harness/playbooks/test-driven-execution.md) and [task contract](contracts/TASK.md).
