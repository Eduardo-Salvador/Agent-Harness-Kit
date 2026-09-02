---
name: test-driven-task
description: Automatically use for full-harness code behavior changes and bug fixes after task dispatch. Do not activate for eligible direct-trivial or vibe routes; otherwise enforce RED, minimum GREEN, and proportional regression.
---

# Test-driven task

Do not load this skill for `direct-trivial` or `vibe`. Vibe requires a focused deterministic check. Failed verification begins bounded in-scope recovery; promote only when a full-Harness condition is exposed.

1. Read `../../../harness/playbooks/test-driven-execution.md` and the task's `Test-first cycle` section before editing code.
2. For `test_strategy: tdd`, do not change production code before observing RED: add or select the focused test from the spec, run it, and confirm it fails for the intended missing behavior rather than syntax, environment, or an unrelated defect.
3. If the test passes before implementation or fails for the wrong reason, stop and return `needs-replan`; do not fake RED, weaken the assertion, or edit production code until the spec/test is corrected.
4. Implement only the minimum behavior required for GREEN. Run the same focused test and record its passing result. Refactor only after GREEN, without broadening behavior, then run the focused test plus the spec's proportional regression set.
5. Keep RED and GREEN inside the same small task and lease. Do not create a separate graph node that intentionally leaves the shared baseline failing.
6. Record RED, GREEN, refactor, and the highest sufficient ladder rung (`focused` → `workspace` → `integration` → `global/checkpoint` → `delivery`) in the transition/closeout. Create a handoff only for an actual separate consumer.
7. `characterization` is allowed only for a behavior-preserving refactor with no desired behavior delta. `verification-only` is allowed only for non-code/artifact work or when no meaningful automated behavior test applies; the task spec must state the exact exception. Once work enters `full-harness`, simplicity, deadline, hackathon mode, or lack of an existing test is not by itself an exception.
