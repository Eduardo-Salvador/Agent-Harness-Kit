---
name: governed-review
description: Use for independent acceptance review, objective verification, and governed integration of a completed task.
---

# Governed review

Do not load or run review for a task that validly declares `evidence_profile: graph-only`; its deterministic completion transition is final. If the task no longer satisfies that boundary, promote it to `handoff-review` before closeout.

Follow `../../../harness/playbooks/review-integration.md` and the completed task's `review_profile`/`max_review_rounds`. Assurance is automatic and non-blocking: never request human approval, reopen the historical completed node, or stop unrelated ready work.

Round 1 must run under a different identity in a fresh context with no implementer conversation history. When the capability manifest proves `spawn_subagent`, automatically launch a review subagent; otherwise use a new visible task/chat or manually opened clean context. Never review in the implementer's context or pretend isolation exists. Send only the review packet: pinned executable task SPEC, its explicitly referenced approved authorities, changed paths/diff, immutable handoff, verification/TDD evidence, scoped rules, and read/impact sets. Exclude the original prompt, conversational memory, implementation reasoning, and proposed verdict.

Reconstruct expected behavior from the SPEC before inspecting the implementation. Judge each acceptance criterion against code and independently checked evidence; a prompt/SPEC conflict requires a spec-revision finding, never reinterpretation from memory. Round 1 is proportional to risk; for TDD tasks verify that RED preceded production behavior, failed for the intended reason, GREEN used the identical focused command, and proportional regression passed. Reject fabricated/irrelevant RED or an unjustified non-TDD strategy. Round 2 uses another focused fresh context and pins only the SPEC, linked remediation, prior blocker IDs, correction delta, and proportional regressions. Only evidence-backed acceptance, security/privacy/data, contract, required-runtime, ownership, or material-regression violations create remediation. Record optional improvements as follow-ups. A second rejection forces task/acceptance rewrite, decomposition, or a genuine human product/risk decision. Never request round 3 or expand commit/integration/push/deploy/publication authority.
