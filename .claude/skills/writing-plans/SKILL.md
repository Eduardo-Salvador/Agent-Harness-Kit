---
name: writing-plans
description: Automatically use when non-trivial implementation work needs executable, spec-driven units. Do not activate for a direct-trivial presentational or static-content edit; narrowly simple engineering work still receives a compact inline spec.
---

# Writing plans

1. Read `../../../harness/playbooks/writing-plans.md` before creating implementation nodes or task briefs.
2. First apply the `direct-trivial` gate in the playbook. If it passes, edit directly without loading planning artifacts, creating a SPEC/TASK, graphing, TDD, handoff, or review. Otherwise activate automatically after approved first-run discovery, approved feature discovery, or any later request that introduces non-trivial implementation work. The user may invoke this skill explicitly but does not need to.
3. For work that is not `direct-trivial`, classify it using the simple-task gate. A simple task gets one compact inline spec; every other implementation outcome requires `../../../harness-state/plans/PLAN-<id>.md` from `../../../harness/templates/IMPLEMENTATION-PLAN.md`.
4. Decompose planned work into ordered, independently checkable units targeting roughly two to five minutes of active agent work each. Tool wait time and independent review are outside that target. Split a unit again when its change, paths, acceptance, or verification cannot be stated precisely.
5. Generate one self-contained `TASK.md` spec per executable unit. It pins the plan revision and step, exact outcome/change, owned paths, scoped context, non-goals, acceptance criteria, verification, stop/replan triggers, and `test_strategy`. Behavior changes and bug fixes specify a focused RED test, expected failure, minimum GREEN behavior, and proportional regression; keep RED/GREEN in the same unit. The implementer loads the task spec, not the whole plan, unless it reports a contradiction.
6. Do not dispatch a non-simple task without an approved/ready plan and complete spec. Do not let the implementer choose product behavior, broaden scope, add dependencies, or improvise around missing decisions; it must stop, persist evidence, and request spec revision.
7. Optimize planning context: use approved context/feature briefs and scoped source evidence, avoid broad rescans, do not duplicate prose across plan and task, and do not create a separate plan file for simple work.
