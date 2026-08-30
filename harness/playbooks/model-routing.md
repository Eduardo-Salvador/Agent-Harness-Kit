# Playbook: Capability-based model routing

1. Read the approved model-routing artifact. Inspect the active adapter capability evidence for the current model catalog, supported reasoning efforts, and the independent override surfaces `create_thread`, `send_message_to_thread`, and `spawn_subagent`; do not infer one from another.
2. Start from `balanced`; choose `economical` only when the work is narrow, low-risk, deterministic, and cheaply verified.
3. Choose `frontier` for consequential judgment, ambiguity, security/privacy, architecture, product tradeoffs, conflicting integration, harness evolution, high-risk review, or repeated failure.
4. Record `model_tier` and a task-specific `model_reason` before dispatch. A generic statement such as “best model” is invalid.
5. Resolve the tier to one model currently exposed by the host and a reasoning effort supported by that model. Create `harness.model-dispatch/v1` from the template; provider IDs are runtime evidence, not permanent policy.
6. Invoke the actual adapter operation with explicit model/reasoning overrides. Persist its returned context reference and response evidence, then set `override_confirmed: true`. Only a resolved record may activate the task.
7. An active context cannot assert that it changed its own model mid-turn. Prefer a fresh override-capable context; otherwise record `manual-required` with the exact selection needed or `blocked`.
8. Route only the task's pinned context packet. Decompose deterministic children away from a frontier parent when ownership and acceptance remain clear.
9. During execution, stop and escalate when a trigger appears. Resolve a new dispatch record for the replacement context and record the prior tier, trigger, and new route in the handoff.
10. If the model ID is rejected, select another currently exposed model at the same tier and retry within the execution budget, or block visibly. Never silently downgrade or accept the host default.
11. Review verifies tier choice, dispatch confirmation, adapter evidence, authority, and acceptance independently. Model strength is not evidence.

Routing changes cost and judgment capacity. It never changes permissions or lifecycle authority.
