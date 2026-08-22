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
4. Keep the independent reviewer in a different context and identity from the implementer.
5. Prefer user-visible chats/tasks when `create_thread` and lifecycle operations are available and approved. Otherwise use an internal subagent; otherwise request/open a fresh context window; otherwise serialize with an artifact-only handoff.
6. Context creation does not reset the goal-lineage budget or grant new tools, permissions, network, commit, push, deploy, or publication authority.
7. Complete or archive a task context after its handoff is durable; resume it only when the same task revision or linked remediation requires it.

## Capability vocabulary

Inventory `spawn_subagent`, `create_thread`, `resume_thread`, `message_thread`, `close_thread`, and `parallel_contexts` independently. Record the actual host evidence and safe fallback. A platform may support internal delegation without supporting visible user chats.

## User-facing status

Status groups the macro state and technical graph by workstream. For every relevant area, show progress, human pending items, technical pending items, active context/agent, blockers, and next action. The view is derived from `PENDING.md` plus `TASK-GRAPH.md`; it does not move technical scheduling into the pending authority.
