# Contract: Task brief

A concise, immutable assignment baseline. Progress fields may advance; changing the goal, scope, paths, dependencies, or acceptance criteria requires orchestrator revision and sometimes human approval.

```yaml
---
schema: harness.task/v1
id: TASK-001
graph: graph-main@7
revision: 1
status: active
assigned_to: agent:builder-1
reviewer: agent:reviewer-1
workstream: backend
agent_role: role:backend-specialist
execution_context: isolated
thread_policy: create-per-task
thread_ref: adapter:task-001
ownership_lease: lease-001
isolation: worktree:task-001
updated_at: 2026-08-20T14:12:00Z
capability_manifest: capability-manifest@1
rules_map: rules-map@1
model_tier: balanced
model_reason: Bounded implementation with deterministic checks and no frontier trigger.
review_profile: standard
max_review_rounds: 2
assurance_gate: none
---
```

```markdown
# TASK-001 — Add contract validator

## Outcome
Reject invalid IDs, graph cycles, and overlapping active ownership.

## Context to load
- `project-context@3` at `state/PROJECT-CONTEXT.md` (illustrative runtime path)
- `graph-main@7` at `state/TASK-GRAPH.md` (illustrative runtime path)
- `DEC-002@1` at `state/decisions/DEC-002.md` (illustrative runtime path)

## Owned paths
- `src/contracts/**`
- `tests/contracts/**`

## Constraints
- No network access. Do not edit graph state.

## Rules to load
- `RULE-SEC-001` and path rules intersecting `src/contracts/**`.

## Required capabilities
- `CAP-FILES-001: available`; `CAP-NETWORK: unavailable`.

## Acceptance criteria
- Invalid fixtures fail with a precise invariant name.
- Valid fixtures pass on supported platforms.

## Verification
- `example-test-command tests/contracts`

## Exit
Write a handoff; do not self-accept the task.
```

## Invariants

- Outcome, bounded owned paths, scoped durable rules, capability states, constraints, acceptance criteria, verification, and exit rule are explicit.
- Dependencies and graph/context references are pinned to revisions.
- Assignee and reviewer are distinct identities.
- Every new task declares a workstream, bounded agent role, execution-context type, thread policy, and adapter-owned reference. Different workstreams do not share one context except an explicit bounded integration task.
- A visible chat, internal subagent, or manual context is adapter execution evidence, never canonical project memory or additional authority.
- Owned paths match the graph lease and do not overlap another active task.
- The task requires no context outside its declared references unless a discovery is recorded in the handoff.
- The implementer cannot mutate graph completion or change baseline scope; it writes a `completed` handoff and the orchestrator performs the graph transition after checking evidence.
- Temporary task context cannot become a durable rule; consequential capability/rule changes require human approval and validation.
- `model_tier` is `economical`, `balanced`, or `frontier`; `model_reason` names task-specific evidence and any trigger considered.
- Routing never changes the task's ownership, capability, review, verification, or human-approval boundaries.
- `review_profile` is `light`, `standard`, or `critical`; `max_review_rounds` is normally `2` and cannot exceed `2` in automatic execution.
- `assurance_gate` is `none` or `affected-actions`. Critical work uses `affected-actions`; graph nodes that integrate, release, deploy, or otherwise consume its risk-sensitive result list that task in `assurance_requires` and cannot become `ready` until its assurance is `accepted`.
- Review budget means one initial independent assurance review plus at most one focused remediation review. Exhaustion blocks/escalates the remediation or affected integration path; it does not reopen completion or create a third loop.
