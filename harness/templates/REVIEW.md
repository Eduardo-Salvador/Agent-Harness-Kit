---
schema: harness.review/v1
id: REVIEW-TASK-001-01
task: TASK-001@1
handoff: HANDOFF-TASK-001-01
spec_authority: TASK-001@1
review_packet: REVIEW-PACKET-TASK-001-01
review_context: isolated-fresh
review_context_ref: adapter:replace
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
evidence: [run:replace]
commands: [replace-focused-command]
duration_ms: 0
tokens: unavailable
created_at: 2000-01-01T00:00:00Z
---

# Review — TASK-001

## Independence

- Reviewer is distinct from implementer: yes.
- Fresh context has no implementer conversation history: yes.
- Route: review subagent/new task or chat/manual clean context.

## Spec authority

- Operative SPEC: `TASK-001@1`.
- Pinned authorities referenced by the SPEC: Replace, or `none`.
- Original prompt, conversation memory, implementation reasoning, and proposed verdict were excluded.

## Fresh-context evidence

- Review packet: `REVIEW-PACKET-TASK-001-01`.
- Context reference: adapter-owned reference; never paste private conversation state.
- Packet contents: SPEC, declared authority references, diff/changed paths, handoff, verification/TDD evidence, scoped rules, `read_set`, and `impact_set`.

## Independent reconstruction

- State the expected behavior and criterion matrix derived before implementation inspection.

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
- On round 2, the frontmatter must pin the prior blocking finding IDs, the correction delta, and related regression scope.
- On round 2 `changes-requested`, stop. Rewrite the task/acceptance contract, decompose the work, or request a human decision for a genuine product/risk conflict. A stronger model may diagnose those paths but cannot create round 3.
