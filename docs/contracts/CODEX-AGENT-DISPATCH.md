# Contract: Codex agent dispatch

Executable bridge between a neutral task/role and a native Codex subagent. The deterministic planner emits the exact native operation and arguments; the final record exists only after adapter-owned runtime evidence returns.

```yaml
---
schema: harness.codex-agent-dispatch/v1
id: codex-dispatch-TASK-001-implementation-01
revision: 1
status: dispatched
task: TASK-001@1
purpose: implementation
agent_identity: agent:implementer:TASK-001:attempt-1
role: role:generic-specialist
execution_context_ref: codex:agent-001
model_dispatch: model-dispatch-TASK-001@1
adapter_operation: spawn_agent
adapter_response_identity: spawn-op-001
created_at: 2026-08-30T18:00:00Z
created_by: role:orchestrator
---
```

## Role resolution

- The task's `agent_role` is the requested identity. Known neutral roles execute directly; area-specific `role:*-specialist` identities execute through `role:generic-specialist` without losing their specialization label.
- Review always executes as `role:reviewer-integrator`. Its identity and returned context cannot equal the implementer's.

## Minimal context packet

The packet contains only the selected role reference, pinned task SPEC, explicitly approved authority/rule references, scoped `read_set`/`impact_set`, and resolved model-dispatch reference. Conversation history, implementer reasoning, a full implementation plan, unrelated graph nodes, and repository-wide dumps are forbidden.

## Native call

- `agent-harness codex-dispatch <request.json>` returns `harness.codex-agent-dispatch-plan/v1`.
- With proven capability, `native_call.operation` is the host's `spawn_agent`/`spawn_subagent`; arguments include bounded task name, `fork_turns: none`, minimal message, resolved model, and supported reasoning effort.
- The orchestrator invokes that operation exactly once and records the returned agent/context reference. A plan is not proof of launch.

## Dispatch evidence

`agent-harness codex-dispatch <plan.json> --response <response.json>` validates requested versus accepted model/reasoning, sanitizes the response to known identity/status fields, and emits `harness.codex-agent-dispatch/v1`. The record includes agent identity, role, context packet, returned context, adapter operation/response identity, and separation evidence.

## Separation and fallback

- Implementation without subagents is explicit `sequential-fallback`; it may run in the active orchestrator context and cannot claim a child agent.
- Review without subagents is `manual-fresh-context-required`, not same-context sequential review. The user or adapter must provide a genuinely fresh context.
- Visible tasks, commits, merges, pushes, deploys, and permissions remain separately authorized operations.
