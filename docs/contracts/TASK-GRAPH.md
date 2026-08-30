# Contract: Task graph

Canonical coordination state. Only the PO/orchestrator changes graph topology or node lifecycle.

```yaml
---
schema: harness.task-graph/v1
id: graph-main
revision: 7
status: active                    # draft | awaiting-approval | active | complete | blocked
project_context: project-context@3
updated_at: 2026-08-20T14:10:00Z
updated_by: role:orchestrator
discovery_snapshot: discovery-003
source_references: migration-main@1
---
```

```markdown
# Task graph

| ID | Workstream | Goal | Depends on | Status | Agent/context | Read / write / impact paths | Checkpoint | Assurance requires |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-001 | backend | Add contract validator | — | active | builder-1 / isolated task context | read `src/contracts/schema.ts`; write `src/contracts/**`; impact `tests/contracts/**` | no | — |
| TASK-002 | integration | Integrate validator with runtime | TASK-001 | pending | unassigned / pending | read `src/contracts/**`; write `src/runtime/**`; impact `tests/runtime/**` | no | TASK-001 |
| TASK-003 | governance | Select license | — | blocked | human:owner | write `LICENSE` | yes: DEC-004 | — |

## Transition log
- r7: TASK-001 ready → active; ownership lease `lease-001` granted.
```

## Invariants

- Node IDs are unique and dependencies reference existing nodes.
- The directed graph is acyclic. A node is `ready` only when all dependencies are completed and its checkpoint, capability, and `assurance_requires` requirements pass.
- Lifecycle is `pending → ready → active → completed`; `blocked` may be entered from any nonterminal state with a reason. Post-completion review records assurance outside the completion gate; a blocker creates a linked remediation node and may gate affected downstream integration/release work.
- Only the orchestrator changes lifecycle or topology, using the expected prior revision.
- Every technical event is a graph transaction: dispatch/start, material progress evidence, dependency discovery, block/unblock, remediation, completion, lease/context change, and newly ready dependents increment the graph revision and enter the transition log before user-facing communication. A `PENDING.md` write never satisfies this requirement.
- Active ownership path sets must not overlap (including parent/child or equivalent normalized paths). Ready nodes may overlap each other because they own nothing yet; the scheduler defers colliding candidates before reservation and activation.
- `write_set` alone grants an exclusive ownership lease. Optional `read_set` identifies the smallest source context to load; optional `impact_set` identifies related consumers/tests for regression analysis. Their paths are safe and repository-relative, but overlap is allowed because they grant no write authority.
- When `read_set` or `impact_set` is derived from repository analysis, `context_provenance` names the evidence method and pinned source revision, such as `source-inspection@git:<sha>` or `graphify@git:<sha>`. Generated relationships are navigation hints until verified in the actual source.
- A repository graph tool enriches nodes in this task graph; it never creates a second operational authority, infers lifecycle transitions, or changes dependencies automatically. If unavailable or stale, use scoped source search and record that provenance.
- Every implementation node links to a task brief and declares an evidence profile. `handoff-review` completion requires objective handoff evidence and automatic bounded independent review. Eligible `graph-only` completion stores only a concise outcome/check result in the transition log and uses no handoff or review artifact. Only predeclared consumers of `assurance_gate: affected-actions` wait for accepted assurance.
- New nodes also record `planning_mode`, `implementation_plan`, `plan_step`, and `target_minutes`. Planned nodes pin a ready plan revision and a two-to-five-minute unit; `inline-simple` nodes use `none`, `inline`, and at most five minutes while still linking a compact executable task spec.
- New nodes record `evidence_profile: handoff-review | graph-only`. Graph-only is valid only for inline-simple verification-only work with `assurance_status: not-required`; all other work uses handoff-review.
- Every machine-readable node records `assurance_status` (`not-required`, `pending`, `accepted`, `changes-requested`, or `blocked`) and an `assurance_requires` list. A `ready` or `active` node cannot reference a task whose assurance is not `accepted`.
- New implementation nodes record `workstream`, `agent_role`, `execution_context`, `thread_policy`, and `thread_ref`. Different workstreams cannot reuse one active execution context; cross-area work is an explicit `integration` node.
- When multiple safe nodes are ready, the orchestrator selects up to proven numeric capacity, reserves distinct leases/contexts, and records actual launches in `harness.parallel-dispatch/v1`. It waits for the first completion or attention event and refills the released slot; dependencies converge only through an explicit integration node.
- Consequential topology/scope changes link to an approved decision.
- Existing-harness nodes link to source material through the migration manifest; an approved context cannot seed a graph from a stale discovery snapshot.
