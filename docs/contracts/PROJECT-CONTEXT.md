# Contract: Project context

Canonical approved intent and constraints for a project. Store instances in a future runtime state directory; do not overwrite this template.

```yaml
---
schema: harness.project-context/v1
id: project-context
revision: 3
status: approved                 # draft | awaiting-approval | approved | superseded
mode: delivery                   # delivery | delivery+learning
updated_at: 2026-08-20T14:00:00Z
approved_by: human:owner
supersedes: project-context@2
discovery_snapshot: discovery-003
source_references: migration-main@1
capability_manifest: capability-manifest@1
rules_map: rules-map@1
pending_authority: harness-state/PENDING.md
---
```

```markdown
# Project context

## Project state
- Kind: existing.
- Evidence: Repository contains an application and tests at discovery time.

## Intent
- Problem: Developers lose state and control across agent conversations.
- Users: Software developers adopting agent-assisted delivery.
- Outcome: A task can be reconstructed and verified from files alone.

## Scope
- In: discovery, graph orchestration, contracts, adapters.
- Out: hosted model service and automatic production deployment.

## Success measures
- The interruption-recovery fixture passes on every supported adapter.

## Constraints
- Platform-neutral core; human approval for elevated permissions.

## Rules and capabilities
- Durable project rules: `rules-map@1`; route by scope.
- Host/project capabilities: `capability-manifest@1`; unavailable and approval-required items remain explicit.

## Assumptions and unknowns
- A-01 (assumption, owner: product): Git is available in the reference example.
- U-02 (unknown, owner: security, resolve-before: TASK-008): secret broker policy.

## Verification environment
- Required: Markdown validator and repository-local test runner.

## References
- Decisions: `DEC-001` at `state/decisions/DEC-001.md` (illustrative runtime path)
- Pending authority: `harness-state/PENDING.md`; human decisions/actions and macro incomplete project areas only.
- Provenance: source identities/backlinks in `migration-main@1`.
```

## Invariants

- `id` is stable; `revision` increases on every content change.
- Only one revision may be `approved`; approval identifies a human authority.
- Project state/evidence, problem, users, outcome, scope, success measures, constraints, rules/capabilities, and assumptions/unknowns are present.
- Every unknown has an owner and resolution condition; assumptions are visibly labeled.
- `mode: delivery+learning` requires an approved learning profile; `delivery` must not require one.
- Graphs reference an exact approved revision and cannot silently follow later edits.
- `pending_authority` names the canonical human-action and macro project completion source; technical ordering remains in the task graph.
- Approval is invalid if the discovery snapshot selectors or source identities are stale.
