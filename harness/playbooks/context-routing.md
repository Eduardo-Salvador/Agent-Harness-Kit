# Playbook: Workstream and execution-context routing

1. Classify each outcome into a project-defined `workstream`; use `integration` only when acceptance genuinely crosses areas.
2. Assign a bounded `agent_role`, exclusive write set, and independent reviewer before choosing a context.
3. Inspect the capability manifest for `spawn_subagent`, `create_thread`, `resume_thread`, `message_thread`, `close_thread`, and `parallel_contexts`. Parallel capability records a numeric implementation capacity and whether implementation/review share a quota; a boolean claim is insufficient for automatic fan-out.
4. Default to `execution_context: isolated` and `thread_policy: create-per-task`. Store only an adapter-owned reference in `thread_ref`; never treat conversational memory as canonical state.
5. Prefer a visible task/chat when creation and lifecycle capabilities are available and approved. Otherwise delegate implementation to an internal subagent; otherwise use a manually opened fresh context; otherwise serialize implementation with `sequential-fallback` and a complete task artifact/handoff.
6. Do not place different workstreams in the same context. The exception is a bounded `integration` node using `shared-integration`, explicit dependencies, and an integration-only write set.
7. Send only the task artifact and declared context packet. The receiving context re-reads canonical files and reports its identity/reference in the handoff.
8. Close or archive the context after durable completion when the host supports it. A failed close is reported but does not undo task completion.
9. Group every project-status response by workstream after reporting human-owned items first.
10. When two or more nodes are ready, load the native `parallel-dispatch` skill, launch every scheduler-selected child without waiting between launches, and refill capacity after the first completion/attention event.

Independent review is stricter than implementation fallback: round 1 always uses a new context and identity with no implementer history. Prefer a review subagent when `spawn_subagent` is proven, then a new visible task/chat, then a manually opened clean context. Same-context sequential review is invalid; record blocked assurance when no fresh-context route exists. Send only the SPEC-led review packet defined by [review and integration](review-integration.md).

Context creation is dispatch mechanics, not new authority. It cannot reset execution counters, bypass review independence, or silently enable tools, permissions, network, secrets, commit, push, deploy, or publication.
