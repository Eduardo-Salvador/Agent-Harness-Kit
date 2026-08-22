# Contract: Pending-work authority

The canonical cross-cutting list of open human actions and the macro project completion overview. Graph nodes remain authoritative for technical execution topology, but cannot erase decisions, approvals, external actions, or project areas that remain incomplete.

```yaml
---
schema: harness.pending/v1
id: pending-main
revision: 1
status: active
updated_at: 2026-08-21T12:00:00Z
updated_by: role:orchestrator
---
```

```markdown
# Pending work

## Human action required
| ID | Area | Owner | Request or decision | Why / delivery effect | Needed by | Status | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HUMAN-001 | authentication | human:product-owner | Choose option A or B | Blocks TASK-003 | Before TASK-003 | open | `DEC-003@1` |

## Project completion overview
| Area | Current state | What remains | Human dependency | Technical source |
| --- | --- | --- | --- | --- |
| Backend | partial | Complete account endpoints | none | `graph-main@4` |
| Authentication | not-started | Implement sign-in and session flow | HUMAN-001 | `graph-main@4` |

## Recently resolved
| ID | Resolution | Resolved by | Evidence |
| --- | --- | --- | --- |
| HUMAN-000 | Option A approved | human:product-owner | `DEC-002@2` |
```

## Invariants

- Every open item has one explicit owner, actionable wording, status, and durable source.
- Every human item and macro completion row names its project area so status can group pending work by workstream without moving technical scheduling into this artifact.
- Human-owned items live under `Human action required`; technical tasks cannot be presented as the user's to-do list.
- A human item names the requested decision/action and delivery effect, not only “approval required”.
- `Project completion overview` describes product areas and outcomes still missing, not task ordering or agent dispatch details.
- Technical order, dependencies, leases, and execution state remain exclusively in `TASK-GRAPH.md`.
- Technical progress cannot be recorded only here. When technical state changes, `TASK-GRAPH.md` is revised first/in the same operational transaction; this artifact changes only for a related human item or macro outcome and then backlinks the new graph revision.
- Resolved items leave the open sections and retain evidence under `Recently resolved`.
- The task graph and pending authority backlink when an item blocks a node, but non-graph human items remain visible.
- Status answers read this authority before the graph and visibly report stale or contradictory state.
