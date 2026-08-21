---
schema: harness.review/v1
id: REVIEW-TASK-001-01
task: TASK-001@1
handoff: HANDOFF-TASK-001-01
revision: 1
round: 1
scope: initial
prior_review: none
status: final
reviewer: agent:independent-reviewer
verdict: changes-requested
created_at: 2000-01-01T00:00:00Z
---

# Review — TASK-001

## Independence

- Reviewer is distinct from implementer: yes.

## Review profile and scope

- Profile: light/standard/critical from the task brief.
- Round: 1 of 2.
- Scope: initial full review, or focused re-review of named blocking findings and correction delta.

## Criterion verdicts

| Criterion | Verdict | Evidence |
| --- | --- | --- |
| Replace | pass/fail | Durable path or run identifier |

## Findings

| ID | Blocking | Category | Evidence | Required action or follow-up |
| --- | --- | --- | --- | --- |
| REV-001 | yes/no | acceptance/security/data/contract/runtime/regression/non-blocking | Durable evidence | Required correction or optional follow-up |

## Integration recommendation

- `accept`, `changes-requested`, or `blocked`; include ordering/conflict and linked-remediation notes. Do not reopen historical completion or block unrelated work.

## Verification

- Checks rerun or inspected: Replace.

## Next review boundary

- On round 1 `changes-requested`, name the linked remediation task, blocking findings, expected correction delta, and proportional regression checks for round 2.
- On round 2 `changes-requested`, stop and recommend escalation/decomposition of the remediation or affected integration path. Request a human decision only for a genuine product/risk conflict; do not request round 3.
