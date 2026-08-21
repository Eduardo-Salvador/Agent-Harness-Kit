# Contract: Review result

An immutable independent assurance verdict for one completed task/handoff revision and one bounded review round. It does not require human approval or hold the completed node.

```yaml
---
schema: harness.review/v1
id: REVIEW-TASK-001-01
task: TASK-001@1
handoff: HANDOFF-TASK-001-01
revision: 1
round: 1
scope: initial
prior_review: none
blocking_findings: none
correction_delta: none
regression_scope: none
status: final
reviewer: agent:independent-reviewer
verdict: changes-requested
created_at: 2026-08-21T12:00:00Z
---
```

```markdown
# Review — TASK-001

## Independence
- Reviewer differs from implementer: yes.

## Review profile and scope
- Profile: standard.
- Round: 1 of 2.
- Scope: all acceptance criteria, relevant diff, verification, risks, routing, and integration boundaries.

## Criterion verdicts
| Criterion | Verdict | Evidence |
| --- | --- | --- |
| Invalid fixtures name the invariant | pass | run `contracts-tests-018` |

## Findings
| ID | Blocking | Category | Evidence | Required action or follow-up |
| --- | --- | --- | --- | --- |
| REV-001 | yes | contract | `path:line` | Correct the declared response shape |
| REV-002 | no | maintainability | `path:line` | Optional follow-up candidate |

## Integration recommendation
- `accept`, `changes-requested`, or `blocked`, with ordering/conflict notes.

## Verification
- Checks rerun or inspected, environment, and outcome.

## Next review boundary
- If changes are requested, name only the failed findings, expected correction delta, and proportional regression checks for round 2.
```

## Invariants

- Reviewer identity differs from implementer identity.
- The review pins exact task and handoff revisions.
- Round 1 uses `scope: initial`; round 2 uses `scope: focused-rereview` and pins `prior_review`.
- Round 2 also pins non-empty `blocking_findings`, `correction_delta`, and `regression_scope`; these are the auditable boundary of the re-review.
- `changes-requested` requires at least one evidence-backed blocking finding.
- Non-blocking findings cannot prevent `accept` and become follow-up candidates.
- Round 2 reopens only prior blocking findings, their correction delta, proportional regression risk, and new blockers introduced in that delta.
- No automatic round 3 exists. A second rejection forces task/contract rewrite, decomposition, or a genuine human product/risk decision under [bounded review rounds](../REVIEW-ROUNDS.md).
- `changes-requested` creates linked remediation and may gate affected integration/release work; it never reopens historical completion or blocks unrelated ready nodes.
