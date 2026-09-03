---
schema: harness.project-context/v1
id: project-context
revision: 1
status: draft
mode: delivery
delivery_preset: accompanied
interaction: accompanied
updated_at: 2000-01-01T00:00:00Z
approved_by: pending
supersedes: none
discovery_snapshot: discovery-001
source_references: none
capability_manifest: capability-manifest@1
rules_map: rules-map@1
pending_authority: harness-state/PENDING.md
---

# Project context

## Project state

- Kind: greenfield / existing / uncertain.
- Evidence: Replace with repository or user evidence.

## Intent

- Problem: Replace with the approved problem.
- Users: Replace with intended users.
- Outcome: Replace with a measurable outcome.

## Scope

- In: Replace.
- Out: Replace.

## Success measures

- Replace with an observable measure.

## Architecture and project organization

- Architecture: existing-confirmed / user-specified / agent-recommended-and-approved / unknown.
- Folder organization: existing-confirmed / user-specified / agent-recommended-and-approved / unknown.
- Coding conventions: detected / user-specified / stack-defaults-approved / none.
- Evidence: Replace with approved artifact, repository paths, or human decision references.

## Delivery shape

- Delivery preset: accompanied (default) / autonomous / hackathon; decision reference: replace.
- Interaction: accompanied / continuous, consistent with the selected preset or an explicit recorded override.
- Autonomous envelope: approved scope, completion conditions, limits, and mandatory human gates; replace or not applicable.
- Client milestones: accompanied = first usable slice and material capabilities; autonomous = no optional milestone pauses; hackathon = first demo. Record any explicit override and affected expansion.
- Domain examples: intended customer/niche, included/excluded results, and failure behavior when relevant.
- Pace: standard / hackathon.
- Deadline/timebox: none / replace.
- Primary demo path: none / replace.
- Demo audience/environment: none / replace.
- Acceptable shortcuts: none / replace with visible fixtures, mocks, seed data, flags, or manual setup.
- Post-MVP: none / replace.

## Constraints

- Replace with technical, product, security, or permission constraints.

## Rules and capabilities

- Durable rules: `rules-map@1`; temporary task context is separate.
- Detected/required capabilities: `capability-manifest@1`; unavailable/optional/approval-required states remain explicit.
- Automatic model routing: enabled / disabled / pending; approved artifact: `harness-state/MODEL-ROUTING.md@1`. Pending or disabled routing remains advisory/manual.

## Assumptions and unknowns

- U-001 (unknown, owner: human:owner, resolve-before: TASK-001): Replace.

## Verification environment

- Required: Replace with checks and available runtime capabilities.

## References

- Decisions: none.
- Pending authority: `harness-state/PENDING.md` for human actions and macro project completion only.
- Provenance: migration manifest and authoritative existing sources.
