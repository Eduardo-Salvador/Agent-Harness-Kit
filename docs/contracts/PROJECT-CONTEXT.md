# Contract: Project context

Canonical approved intent and constraints for a project. Store instances in a future runtime state directory; do not overwrite this template.

```yaml
---
schema: harness.project-context/v1
id: project-context
revision: 3
status: approved                 # draft | awaiting-approval | approved | superseded
mode: delivery                   # delivery | delivery+learning | hackathon | hackathon+learning
delivery_preset: accompanied      # accompanied | autonomous | hackathon
interaction: accompanied          # accompanied | continuous
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

## Architecture and project organization
- Architecture: existing-confirmed; artifact-driven, platform-neutral core with native adapters.
- Folder organization: existing-confirmed; neutral contracts/playbooks under `harness/`, native routing under `.agents/` and `.claude/`, runtime state under `harness-state/`.
- Coding conventions: detected; repository formatter, validator, and language-specific rules.
- Evidence: repository layout, approved architecture decisions, and scoped rules map.

## Delivery shape
- Pace: standard.
- Deadline/timebox: none.
- Primary demo path: not applicable.
- Demo audience/environment: not applicable.
- Acceptable shortcuts: none.
- Post-MVP: none.

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

## Delivery preset compatibility

Follow [delivery modes](../DELIVERY-MODES.md). New contexts record the preset, interaction, and decision reference. Accompanied and autonomous use existing `delivery` mode; hackathon uses `hackathon`. Preserve approved learning suffixes and explicit interaction overrides without activating new consent. Existing contexts without these fields keep their approved behavior; missing interaction defaults visibly at the next product block. The CLI inspector is not a context write or approval.

## Invariants

- `id` is stable; `revision` increases on every content change.
- Only one revision may be `approved`; approval identifies a human authority.
- Project state/evidence, problem, users, outcome, scope, success measures, architecture, folder organization, coding-convention disposition, constraints, rules/capabilities, and assumptions/unknowns are present.
- Architecture and folder organization are approved before planning. Existing evidence is preserved by default; absent or ambiguous choices may be user-specified, selected from bounded options, or agent-recommended and approved. Coding conventions are optional and may explicitly use detected stack defaults or none.
- Every unknown has an owner and resolution condition; assumptions are visibly labeled.
- `delivery+learning` and `hackathon+learning` require an approved learning profile; `delivery` and `hackathon` must not require one.
- `hackathon` modes record a deadline/timebox, one primary demo path, audience/environment, acceptable shortcuts, and post-MVP exclusions. They use the same graph, ownership, status, verification, and review authorities as standard delivery.
- Graphs reference an exact approved revision and cannot silently follow later edits.
- `pending_authority` names the canonical human-action and macro project completion source; technical ordering remains in the task graph.
- Approval is invalid if the discovery snapshot selectors or source identities are stale.
