# Contract: Review result

An immutable independent assurance verdict for one completed task/handoff revision and one bounded review round. It does not require human approval or hold the completed node.

```yaml
---
schema: harness.review/v1
id: REVIEW-TASK-001-01
task: TASK-001@1
handoff: HANDOFF-TASK-001-01
spec_authority: TASK-001@1
review_packet: REVIEW-PACKET-TASK-001-01
review_context: isolated-fresh
review_context_ref: adapter:review-42
prompt_source: task-spec-only
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
findings: [REV-001]
evidence: [run:contracts-tests-018]
commands: [example-test-command tests/contracts]
duration_ms: 42000
tokens: host-reported:1840
created_at: 2026-08-21T12:00:00Z
---
```

```markdown
# Review — TASK-001

## Independence
- Reviewer differs from implementer: yes.
- Fresh context has no implementer conversation history: yes.

## Spec authority
- Operative SPEC: `TASK-001@1`.
- Original prompt, conversation memory, implementation reasoning, and proposed verdict were excluded.

## Fresh-context evidence
- Review packet: `REVIEW-PACKET-TASK-001-01`.
- Context reference: `adapter:review-42`.
- Packet contains only the pinned SPEC and its named authorities, relevant diff/paths, handoff, verification/TDD evidence, scoped rules, and read/impact sets.

## Independent reconstruction
- Expected behavior and acceptance matrix derived from the SPEC before implementation inspection.

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
- Round 1 and any focused round 2 run in a newly created reviewer context with no implementer conversation history. Same-context review is invalid.
- The review pins exact task and handoff revisions.
- `spec_authority` equals the task revision under review, `prompt_source` is `task-spec-only`, and the review records an immutable packet ID plus adapter-owned context reference.
- The packet excludes the original prompt, conversation transcript, implementation reasoning, suspected findings, and proposed verdict. Only the SPEC and authorities it explicitly references may define expected behavior.
- The reviewer derives the acceptance matrix from the SPEC before inspecting the implementation and independently verifies code and evidence. A SPEC conflict becomes a spec-revision finding; memory never resolves it.
- Round 1 uses `scope: initial`; round 2 uses `scope: focused-rereview` and pins `prior_review`.
- Round 2 also pins non-empty `blocking_findings`, `correction_delta`, and `regression_scope`; these are the auditable boundary of the re-review.
- `changes-requested` requires at least one evidence-backed blocking finding.
- `verdict` is exactly `accept`, `changes-requested`, `rejected`, or `needs-replan`; every final review also normalizes `findings`, `evidence`, `commands`, `duration_ms`, and `tokens` in frontmatter so metrics never need to parse prose. Use empty lists and `unavailable`, never omit fields.
- Non-blocking findings cannot prevent `accept` and become follow-up candidates.
- Round 2 reopens only prior blocking findings, their correction delta, proportional regression risk, and new blockers introduced in that delta.
- No automatic round 3 exists. A second rejection forces task/contract rewrite, decomposition, or a genuine human product/risk decision under [bounded review rounds](../REVIEW-ROUNDS.md).
- `changes-requested` creates linked remediation and may gate affected integration/release work; it never reopens historical completion or blocks unrelated ready nodes.
