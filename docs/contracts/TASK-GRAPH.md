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

| ID | Goal | Depends on | Status | Owner | Paths | Checkpoint |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-001 | Add contract validator | — | active | agent:builder-1 | `src/contracts/**`, `tests/contracts/**` | no |
| TASK-002 | Integrate validator with runtime | TASK-001 | pending | — | `src/runtime/**`, `tests/runtime/**` | no |
| TASK-003 | Select license | — | blocked | human:owner | `LICENSE` | yes: DEC-004 |

## Transition log
- r7: TASK-001 ready → active; ownership lease `lease-001` granted.
```

## Invariants

- Node IDs are unique and dependencies reference existing nodes.
- The directed graph is acyclic. A node is `ready` only when all dependencies are accepted and its checkpoint/capability requirements pass.
- Lifecycle is `pending → ready → active → review → accepted`; `blocked` may be entered from any nonterminal state with a reason. Retry/follow-up work is a linked node or recorded attempt, never erased history.
- Only the orchestrator changes lifecycle or topology, using the expected prior revision.
- Active ownership path sets must not overlap (including parent/child or equivalent normalized paths).
- Every implementation node links to a task brief; acceptance requires independent review and objective evidence.
- Consequential topology/scope changes link to an approved decision.
- Existing-harness nodes link to source material through the migration manifest; an approved context cannot seed a graph from a stale discovery snapshot.
