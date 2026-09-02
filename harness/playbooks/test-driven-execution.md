# Test-driven execution

Use this playbook for every behavior-changing `full-harness` implementation task after its executable spec is dispatched. A request routed to `direct-trivial` or `vibe` by [request routing](request-routing.md) has no executable spec and does not enter this playbook.

## Vibe boundary

An eligible `vibe` request may change small local behavior without a mandatory RED phase when it stays in one working context, has low blast radius, and has a focused deterministic check. Vibe never means unverified. A failed check begins bounded in-scope recovery; promote only when it exposes a full-Harness condition.

## Strategy selection

- `tdd`: required for new or changed observable code behavior and bug fixes.
- `characterization`: behavior-preserving refactor; establish the current contract with passing focused coverage before and after the change. Do not invent a failing test when no behavior delta is intended.
- `verification-only`: non-code/artifact/configuration work where no meaningful automated behavior test applies. The task spec names the exact reason and the reproducible alternative check.

Missing test infrastructure is not a silent exception inside graph/full work. If adding the smallest harness is within approved scope, specify it as the first bounded unit. Otherwise return `needs-replan` with the unavailable capability or scope decision. `inline-simple` graph tasks and hackathon tasks follow the same strategy boundary.

A localized static edit is not a behavior task. Handle it through `direct-trivial` with the smallest useful check. A small local behavior request may use `vibe`; promote only when a full-Harness condition appears.

## RED → GREEN → REFACTOR

1. Read the task spec, focused test path/command, expected failure, production write path, and proportional regression set.
2. **RED:** write the smallest test that expresses one acceptance behavior. Run only the focused command first. Preserve evidence of a meaningful failure caused by the intended missing behavior. Syntax/import/environment failures and unrelated failing tests are not valid RED.
3. If RED unexpectedly passes, the behavior may already exist or the test is ineffective. Stop as `needs-replan`; do not weaken assertions or manufacture a failure.
4. **GREEN:** change the minimum production code necessary for that test. Run the identical focused command and require a pass.
5. **REFACTOR:** clean only within the task's behavior and lease boundary. Rerun the focused test after any refactor.
6. Climb the test ladder only as needed: `focused` → `workspace` → `integration` → `global/checkpoint` → `delivery`. Record the highest rung reached and why it is sufficient; do not repeat global checks at every micro-step.
7. Record RED, GREEN, refactor, and ladder evidence in the graph transition or closeout. Put it in a handoff only when an actual separate consumer needs that handoff.

RED and GREEN are phases inside one task, not separate graph nodes. A task never hands off an intentionally failing shared baseline. When a vertical behavior slice cannot complete RED and GREEN inside the target unit, writing plans must split the behavior more narrowly before dispatch.

## Evidence contract

For TDD, the inline transition/closeout records the following; a consumer-bound handoff carries the same evidence:

- test path and behavior asserted;
- RED command, failing result, and why the failure proves the behavior was absent;
- GREEN command and passing result for the same focused test;
- refactor performed or `none`;
- proportional regression command and result.

Test output may be summarized with a durable run/path reference; do not paste large logs. A completion claim without valid RED and GREEN evidence is rejected by the orchestrator and reviewer.
