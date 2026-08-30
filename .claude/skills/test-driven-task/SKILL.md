---
name: test-driven-task
description: Automatically use for full-harness code behavior changes and bug fixes after task dispatch. Do not activate for eligible direct-trivial or vibe routes; otherwise enforce RED, minimum GREEN, and proportional regression.
---

# Test-driven task

Do not load this skill for a request routed by `request-router` to `direct-trivial` or `vibe`. Direct-trivial covers static/mechanical edits. Vibe may cover one small local behavior change without mandatory RED, but only with a focused deterministic check, no hard full trigger, and zero artifacts. If inspection exposes broader impact or verification fails, leave the fast path before further editing and promote to `full-harness`.

1. Read `../../../harness/playbooks/test-driven-execution.md` and the task's `Test-first cycle` section before editing code.
2. For `test_strategy: tdd`, do not change production code before observing RED: add or select the focused test from the spec, run it, and confirm it fails for the intended missing behavior rather than syntax, environment, or an unrelated defect.
3. If the test passes before implementation or fails for the wrong reason, stop and return `needs-replan`; do not fake RED, weaken the assertion, or edit production code until the spec/test is corrected.
4. Implement only the minimum behavior required for GREEN. Run the same focused test and record its passing result. Refactor only after GREEN, without broadening behavior, then run the focused test plus the spec's proportional regression set.
5. Keep RED and GREEN inside the same small task and lease. Do not create a separate graph node that intentionally leaves the shared baseline failing.
6. Record RED command/outcome/reason, GREEN command/outcome, refactor status, and regression outcome in the handoff. Completion is invalid without this evidence for a TDD task.
7. `characterization` is allowed only for a behavior-preserving refactor with no desired behavior delta. `verification-only` is allowed only for non-code/artifact work or when no meaningful automated behavior test applies; the task spec must state the exact exception. Once work enters `full-harness`, simplicity, deadline, hackathon mode, or lack of an existing test is not by itself an exception.
