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

| ID | Workstream | Goal | Depends on | Status | Agent/context | Paths | Checkpoint | Assurance requires |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-001 | backend | Add contract validator | — | active | builder-1 / isolated task context | `src/contracts/**`, `tests/contracts/**` | no | — |
| TASK-002 | integration | Integrate validator with runtime | TASK-001 | pending | unassigned / pending | `src/runtime/**`, `tests/runtime/**` | no | TASK-001 |
| TASK-003 | governance | Select license | — | blocked | human:owner | `LICENSE` | yes: DEC-004 | — |

## Transition log
- r7: TASK-001 ready → active; ownership lease `lease-001` granted.
```

## Invariants

- Node IDs are unique and dependencies reference existing nodes.
- The directed graph is acyclic. A node is `ready` only when all dependencies are completed and its checkpoint, capability, and `assurance_requires` requirements pass.
- Lifecycle is `pending → ready → active → completed`; `blocked` may be entered from any nonterminal state with a reason. Post-completion review records assurance outside the completion gate; a blocker creates a linked remediation node and may gate affected downstream integration/release work.
- Only the orchestrator changes lifecycle or topology, using the expected prior revision.
- Every technical event is a graph transaction: dispatch/start, material progress evidence, dependency discovery, block/unblock, remediation, completion, lease/context change, and newly ready dependents increment the graph revision and enter the transition log before user-facing communication. A `PENDING.md` write never satisfies this requirement.
- Active ownership path sets must not overlap (including parent/child or equivalent normalized paths).
- Every implementation node links to a task brief; completion requires objective acceptance evidence. Independent review remains automatic and bounded. It is non-blocking for ordinary execution; only predeclared consumers of `assurance_gate: affected-actions` wait for accepted assurance.
- Every machine-readable node records `assurance_status` (`not-required`, `pending`, `accepted`, `changes-requested`, or `blocked`) and an `assurance_requires` list. A `ready` or `active` node cannot reference a task whose assurance is not `accepted`.
- New implementation nodes record `workstream`, `agent_role`, `execution_context`, `thread_policy`, and `thread_ref`. Different workstreams cannot reuse one active execution context; cross-area work is an explicit `integration` node.
- Consequential topology/scope changes link to an approved decision.
- Existing-harness nodes link to source material through the migration manifest; an approved context cannot seed a graph from a stale discovery snapshot.
