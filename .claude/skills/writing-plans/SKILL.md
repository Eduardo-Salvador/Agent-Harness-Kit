---
name: writing-plans
description: Automatically use when non-trivial implementation work needs executable, spec-driven units. Do not activate for a direct-trivial presentational or static-content edit; narrowly simple engineering work still receives a compact inline spec.
---

# Writing plans

1. Read `../../../harness/playbooks/writing-plans.md` before creating implementation nodes or task briefs. Run its mandatory `agent-harness preflight` before decomposition and stop on missing declared prerequisites.
2. First apply the `direct-trivial` gate in the playbook. If it passes, edit directly without loading planning artifacts, creating a SPEC/TASK, graphing, TDD, handoff, or review. Otherwise activate automatically after approved first-run discovery, approved feature discovery, or any later request that introduces non-trivial implementation work. The user may invoke this skill explicitly but does not need to.
3. Use a compact inline spec for bounded same-context work and a plan for larger work. Assign `assurance: none|light|full` independently. Create TASK/handoff/review packets only for actual separate consumers.
4. Decompose planned work into ordered, independently checkable units targeting 15–30 minutes of active agent work each. Tool wait time and independent review are outside that target. Justify units outside the range by atomicity, runtime cost, or risk.
5. Generate a self-contained `TASK.md` when a separate executor will consume it; a same-context inline node uses a compact inline spec and graph transition. Pin plan revision/step, outcome, owned paths, scoped context, non-goals, acceptance, verification, assurance, stop/replan triggers, and `test_strategy`. Behavior changes and bug fixes keep focused RED/GREEN in the same unit.
6. Do not dispatch a non-simple task without an approved/ready plan and complete spec. Do not let the implementer choose product behavior, broaden scope, add dependencies, or improvise around missing decisions; it must stop, persist evidence, and request spec revision.
7. Optimize planning context: use approved context/feature briefs and scoped source evidence, avoid broad rescans, do not duplicate prose across plan and task, and do not create a separate plan file for simple work.
