# Test-driven execution

Use this playbook for every behavior-changing implementation task after its executable spec is dispatched. A request that passes the `direct-trivial` gate in [writing plans](writing-plans.md) has no executable spec and does not enter this playbook.

## Strategy selection

- `tdd`: required for new or changed observable code behavior and bug fixes.
- `characterization`: behavior-preserving refactor; establish the current contract with passing focused coverage before and after the change. Do not invent a failing test when no behavior delta is intended.
- `verification-only`: non-code/artifact/configuration work where no meaningful automated behavior test applies. The task spec names the exact reason and the reproducible alternative check.

Missing test infrastructure is not a silent exception. If adding the smallest harness is within approved scope, specify it as the first bounded unit. Otherwise return `needs-replan` with the unavailable capability or scope decision. `inline-simple` engineering tasks and hackathon tasks follow the same strategy boundary.

A localized presentation/static-content edit such as a color, spacing value, typo, static label, or asset reference is not a behavior task when it adds no logic, interaction/state, accessibility behavior, rule, contract, data flow, dependency, or risk. Handle it through `direct-trivial` with the smallest useful check and no manufactured RED. If inspection reveals any of those concerns, promote it before editing.

## RED → GREEN → REFACTOR

1. Read the task spec, focused test path/command, expected failure, production write path, and proportional regression set.
2. **RED:** write the smallest test that expresses one acceptance behavior. Run only the focused command first. Preserve evidence of a meaningful failure caused by the intended missing behavior. Syntax/import/environment failures and unrelated failing tests are not valid RED.
3. If RED unexpectedly passes, the behavior may already exist or the test is ineffective. Stop as `needs-replan`; do not weaken assertions or manufacture a failure.
4. **GREEN:** change the minimum production code necessary for that test. Run the identical focused command and require a pass.
5. **REFACTOR:** clean only within the task's behavior and lease boundary. Rerun the focused test after any refactor.
6. Run the declared proportional regression set once after GREEN/refactor. Run the full suite only when the task's impact/risk contract requires it; do not repeat it at every micro-step.
7. Write RED, GREEN, refactor, and regression evidence into the handoff before completion.

RED and GREEN are phases inside one task, not separate graph nodes. A task never hands off an intentionally failing shared baseline. When a vertical behavior slice cannot complete RED and GREEN inside the target unit, writing plans must split the behavior more narrowly before dispatch.

## Evidence contract

For TDD, the handoff records:

- test path and behavior asserted;
- RED command, failing result, and why the failure proves the behavior was absent;
- GREEN command and passing result for the same focused test;
- refactor performed or `none`;
- proportional regression command and result.

Test output may be summarized with a durable run/path reference; do not paste large logs. A completion claim without valid RED and GREEN evidence is rejected by the orchestrator and reviewer.
