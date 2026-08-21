# Playbook: Review and integration

1. The task declares `review_profile: light|standard|critical` and `max_review_rounds: 2`. A lower or larger automatic budget is invalid unless the project adopts a stricter one-review policy.
2. Implementer writes an immutable `completed` handoff with acceptance evidence.
3. When declared checks pass, the orchestrator transitions the node to `completed`, releases the lease, reports the result, and dispatches the next ready task. Nodes with an `assurance_requires` checkpoint remain pending until the referenced assurance is accepted; unrelated nodes continue. The orchestrator then assigns the predeclared independent reviewer automatically; no human completion or review approval is requested.
4. In round 1, reviewer pins task/handoff revisions and follows the profile in [bounded review rounds](../../docs/REVIEW-ROUNDS.md). `changes-requested` requires an evidence-backed blocking finding; non-blocking notes become follow-ups.
5. Orchestrator checks reviewer independence, evidence, current graph revision, lease validity, routing/escalation records, coherent change boundaries, and integration conflicts.
6. On `accept`, record the assurance result and follow the [coherent change and integration policy](../../docs/CHANGE-INTEGRATION.md) for separately authorized actions. The completed node needs no further lifecycle transition.
7. On round 1 `changes-requested`, create one linked remediation task. Do not reopen the historical completed node or stop unrelated ready work. Round 2 is a focused review of the remediation, prior blockers, correction delta, proportional regressions, and new blocking defects introduced by that delta.
8. On round 2 `changes-requested`, stop the review loop. Block the remediation or affected integration path—not the completed historical node or unrelated work—and choose task/acceptance rewrite, decomposition, or a human decision for a genuine product/risk conflict. A stronger model may assist diagnosis but cannot authorize round 3.
9. A `blocked` review resolves its missing evidence/capability/decision without consuming another implementation attempt unless the candidate changes.

The reviewer recommends assurance/remediation; the orchestrator owns graph transitions. Neither may silently combine those authorities. Task completion does not itself authorize separately gated commit, integration, push, deployment, or publication. Review depth is proportional, repetition is bounded, and normal project execution is non-blocking.

Follow [task closeout](task-closeout.md) at each implementation/review boundary. An internal handoff or review artifact never replaces the user-facing explanation.
