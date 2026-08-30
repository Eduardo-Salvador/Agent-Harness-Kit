# Execution contexts and workstreams

Separate contexts are a default engineering practice for substantial agent work. Frontend, backend, data, infrastructure, integration, and learning have different evidence and tool needs; mixing them in one growing conversation wastes context and increases accidental cross-area edits.

## Neutral contract

Every new implementation task declares:

- `workstream`: a project-defined area such as `frontend`, `backend`, `data`, `infra`, or `integration`;
- `agent_role`: the bounded specialist identity;
- `execution_context`: `isolated`, `shared-integration`, or `sequential-fallback`;
- `thread_policy`: normally `create-per-task`, optionally `reuse-workstream`, `manual`, or `sequential-fallback`;
- `thread_ref`: an adapter-owned reference or `pending` before dispatch.

The neutral core requests an execution context; adapters decide whether it is a visible chat/task, internal subagent, delegated agent, worktree-bound session, manually opened context window, or serialized fresh context. A filename or product claim is not capability evidence.

## Default routing

1. Keep one orchestration context for status, human pending items, decisions, and graph transitions.
2. Create a fresh implementation context per task by default and group it under its workstream.
3. Never reuse one execution context across different workstreams unless the node is explicitly `integration` with `shared-integration` and bounded paths.
4. Keep the independent reviewer in a newly created context and different identity from the implementer. It receives no implementation chat history and derives acceptance from the pinned task SPEC.
5. For implementation, prefer user-visible chats/tasks when `create_thread` and lifecycle operations are available and approved; otherwise use an internal subagent, a fresh manual context, or serialized artifact handoff. For review, prefer a fresh subagent, then a new visible task/chat, then a fresh manual context; same-context review is never a valid fallback.
6. Context creation does not reset the goal-lineage budget or grant new tools, permissions, network, commit, push, deploy, or publication authority.
7. Record numeric implementation capacity, review-reserved capacity, the evidence source, and whether first-event waiting is supported. A boolean `parallel_contexts` claim is insufficient.
8. When at least two safe nodes are ready, automatically use the parallel-dispatch workflow: select to capacity, reserve distinct contexts and leases, launch all selected tasks before waiting, then refill after the first completion or attention event.
9. Complete or archive a task context after its handoff is durable; resume it only when the same task revision or linked remediation requires it.

## Capability vocabulary

Inventory `spawn_subagent`, `create_thread`, `resume_thread`, `message_thread`, `close_thread`, first-event waiting, and numeric parallel capacity independently. Record the actual host evidence, review quota sharing, and safe fallback. A platform may support internal delegation without supporting visible user chats. Without numeric capacity or an actual launch operation, use truthful sequential fallback.

## User-facing status

Status groups the macro state and technical graph by workstream. For every relevant area, show progress, human pending items, technical pending items, active context/agent, blockers, and next action. The view is derived from `PENDING.md` plus `TASK-GRAPH.md`; it does not move technical scheduling into the pending authority.
