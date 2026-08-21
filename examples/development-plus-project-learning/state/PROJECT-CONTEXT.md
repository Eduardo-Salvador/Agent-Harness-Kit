---
schema: harness.project-context/v1
id: project-context-learning-example
revision: 1
status: approved
mode: delivery+learning
updated_at: 2026-08-20T11:00:00Z
approved_by: human:example-owner
supersedes: none
discovery_snapshot: example-existing-001
source_references: none
capability_manifest: none
rules_map: none
pending_authority: state/PENDING.md
---

# Project context

## Project state

- Kind: existing.
- Evidence: First-run inspection found the parser and its current tests.

## Intent

- Problem: A small parser lacks boundary-case tests.
- Users: Maintainers learning evidence-driven task decomposition.
- Outcome: Boundary cases are covered and the user's reasoning receives a separate debrief.

## Scope

- In: Parser tests and consented reasoning assessment.
- Out: External note publication.

## Success measures

- Delivery criteria pass; learning remains removable and non-blocking.

## Constraints

- No network; local artifacts only; learning cannot edit delivery state.

## Rules and capabilities

- Preserve the learning non-interference rule; local file/test capabilities only.

## Assumptions and unknowns

- A-101 (assumption, owner: human:example-owner): The example reasoning contains no sensitive data.

## Verification environment

- Required: `python tools/validate.py`.

## References

- Learning profile: `learning-profile-example@1`.
- Pending authority: `state/PENDING.md`.
