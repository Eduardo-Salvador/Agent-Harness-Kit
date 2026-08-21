# Contract: Decision

An auditable choice, especially for human checkpoints. Keep one decision per instance.

```yaml
---
schema: harness.decision/v1
id: DEC-004
revision: 1
status: approved                  # proposed | awaiting-approval | approved | rejected | superseded
consequence: high                 # low | medium | high
decided_by: human:owner
decided_at: 2026-08-20T15:00:00Z
supersedes: null
source_references: migration-main@1
---
```

```markdown
# DEC-004 — Choose repository license

## Context
Distribution terms must be explicit before public release.

## Decision
Use the Apache-2.0 license.

## Options considered
- MIT — simpler; fewer explicit patent terms.
- Apache-2.0 — selected for explicit patent grant.
- No license — rejected; prevents intended reuse.

## Consequences
- Add `LICENSE`; review third-party compatibility before release.

## Affected artifacts
- `project-context@4`
- `TASK-003`

## Provenance
- Existing narrative decision: `legacy/DECISIONS.md`, identity/backlink in `migration-main@1`.
```

## Invariants

- Context, decision, considered alternatives, rationale/consequences, and affected artifacts are present.
- High-consequence product, architecture, scope, security, permission, verification-override, and publication decisions require a human decider.
- Approval is explicit; silence and agent inference are not approval.
- A changed decision creates a new revision or successor and links what it supersedes; history is not rewritten.
- Referenced artifacts apply only the approved revision.
- Narrative sources may remain authoritative references; migration requires provenance and human semantic review rather than lossy automatic splitting.
