# Playbook: Workstream and execution-context routing

1. Classify each outcome into a project-defined `workstream`; use `integration` only when acceptance genuinely crosses areas.
2. Assign a bounded `agent_role`, exclusive write set, and independent reviewer before choosing a context.
3. Inspect the capability manifest for `spawn_subagent`, `create_thread`, `resume_thread`, `message_thread`, `close_thread`, and `parallel_contexts`.
4. Default to `execution_context: isolated` and `thread_policy: create-per-task`. Store only an adapter-owned reference in `thread_ref`; never treat conversational memory as canonical state.
5. Prefer a visible task/chat when creation and lifecycle capabilities are available and approved. Otherwise delegate to an internal subagent; otherwise use a manually opened fresh context; otherwise serialize with `sequential-fallback` and a complete task artifact/handoff.
6. Do not place different workstreams in the same context. The exception is a bounded `integration` node using `shared-integration`, explicit dependencies, and an integration-only write set.
7. Send only the task artifact and declared context packet. The receiving context re-reads canonical files and reports its identity/reference in the handoff.
8. Close or archive the context after durable completion when the host supports it. A failed close is reported but does not undo task completion.
9. Group every project-status response by workstream after reporting human-owned items first.

Context creation is dispatch mechanics, not new authority. It cannot reset execution counters, bypass review independence, or silently enable tools, permissions, network, secrets, commit, push, deploy, or publication.
