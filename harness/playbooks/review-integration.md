# Playbook: Review and integration

1. The task declares `review_profile: light|standard|critical` and `max_review_rounds: 2`. A lower or larger automatic budget is invalid unless the project adopts a stricter one-review policy.
2. Implementer writes an immutable handoff for the attempt and announces its path.
3. Orchestrator transitions the node to `review` and assigns the predeclared independent reviewer.
4. In round 1, reviewer pins task/handoff revisions and follows the profile in [bounded review rounds](../../docs/REVIEW-ROUNDS.md). `changes-requested` requires an evidence-backed blocking finding; non-blocking notes become follow-ups.
5. Orchestrator checks reviewer independence, evidence, current graph revision, lease validity, routing/escalation records, coherent change boundaries, and integration conflicts.
6. On `accept`, follow the [coherent change and integration policy](../../docs/CHANGE-INTEGRATION.md). Perform only the separately authorized adapter action, record evidence, transition to `accepted`, and release the lease.
7. On round 1 `changes-requested`, create one linked correction attempt. Round 2 is a focused re-review limited to prior blockers, the correction delta, proportional regression checks, and new blocking defects introduced by that delta.
8. On round 2 `changes-requested`, stop. Mark the task blocked and escalate to frontier diagnosis/integration, decompose or rewrite the task, request a human decision, or create a new bounded task. Never dispatch round 3 on the unchanged task contract.
9. A `blocked` review resolves its missing evidence/capability/decision without consuming another implementation attempt unless the candidate changes.

The reviewer recommends; the orchestrator transitions. Neither may silently combine those authorities. Technical acceptance does not itself authorize commit, integration, push, deployment, or publication. Review depth is proportional; repetition is bounded.
