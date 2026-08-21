---
schema: harness.project-context/v1
id: project-context
revision: 1
status: approved
mode: delivery
updated_at: 2026-08-20T10:00:00Z
approved_by: human:example-owner
supersedes: none
discovery_snapshot: example-greenfield-001
source_references: none
capability_manifest: none
rules_map: none
pending_authority: state/PENDING.md
---

# Project context

## Project state

- Kind: greenfield.
- Evidence: First-run inspection found no application source; the owner confirmed a new example project.

## Intent

- Problem: Example configuration files lack deterministic validation.
- Users: Maintainers of the example project.
- Outcome: Invalid configuration is rejected before integration.

## Scope

- In: Add a local configuration check.
- Out: CI and external services.

## Success measures

- Valid and invalid local fixtures produce deterministic results.

## Constraints

- Standard runtime only; repository-scoped writes; no network.

## Rules and capabilities

- No external capabilities or durable rule map are required by this small greenfield example.

## Assumptions and unknowns

- A-001 (assumption, owner: human:example-owner): Python 3 is the reference runtime.

## Verification environment

- Required: `python tools/validate.py`.

## References

- Decisions: `DEC-001@1`.
- Pending authority: `state/PENDING.md`.
