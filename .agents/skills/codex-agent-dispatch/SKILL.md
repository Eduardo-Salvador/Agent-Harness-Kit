---
name: codex-agent-dispatch
description: Automatically use for every Codex implementation or independent-review dispatch. Select the neutral role, construct a minimal context packet, invoke a fresh native subagent with resolved model/reasoning, and persist adapter-owned evidence; degrade explicitly when subagents are unavailable.
---

# Codex agent dispatch

Follow `../../../docs/contracts/CODEX-AGENT-DISPATCH.md` and `../../../adapters/codex.md`. This is the executable Codex bridge from neutral role/task artifacts to a live agent context.

1. Build a request from the pinned `TASK.md`, resolved `harness.model-dispatch/v1`, and current capability evidence. Include only the role, task SPEC, approved authority/rule references, `read_set`, and `impact_set`; never include the conversation, full plan, or broad repository context.
2. Run `agent-harness codex-dispatch <request.json>` and inspect the machine-readable plan. For implementation, retain the requested specialist identity and use `role:generic-specialist` when no dedicated neutral executor exists. For review, force `role:reviewer-integrator`, a distinct identity, and `fork_turns: none`.
3. When status is `ready-to-dispatch`, invoke the named native operation using exactly `native_call.arguments`, including model and reasoning effort. Do not claim dispatch before the host returns an agent/context reference.
4. Persist the sanitized host response, then run `agent-harness codex-dispatch <plan.json> --response <response.json>`. Link the resulting `harness.codex-agent-dispatch/v1` record from the task/graph transition before marking the child active.
5. An implementation request with no subagent capability records `sequential-fallback` and runs visibly in the orchestrator context. A review request records `manual-fresh-context-required`; same-context review is forbidden even under fallback.
6. Implementer and reviewer identities, contexts, packets, and dispatch evidence remain distinct. A user-visible Codex task is created only when the user explicitly requests one; the normal route is an internal subagent.
