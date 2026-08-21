---
schema: harness.coexistence/v1
id: coexistence-main
revision: 1
status: active
updated_at: 2000-01-01T00:00:00Z
approved_by: human:owner
---

# Existing-harness coexistence and precedence

## Existing authorities

- Root instructions: replace with paths and authority.
- Roles and path rules: replace.
- Decisions, knowledge, and pending work: replace.

## Namespaced kit placement

- Kit files: `.agent-harness-kit/`.
- Adoption state: `harness-adoption/` and `harness-state/`.

## Precedence and conflicts

- Existing authority remains in force during coexistence.
- Path-scoped rules win inside their scope.
- Conflicts block affected work and require a decision.

## Exclusions and sensitive paths

- Generated worktrees/build outputs: inventory and exclude from ownership/context.
- Secret-bearing files: record path/identity only; never migrate values.

## Cutover gate

- No original or coexistence duplicate may be deleted before human semantic-equivalence review and separate cutover authorization.

## Source references

- Migration manifest: `MIGRATION-MANIFEST.md`.
