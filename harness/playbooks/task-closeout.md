# Playbook: Task closeout and user communication

Use this playbook whenever implementation, review, acceptance, or a material phase reaches a boundary.

1. Persist the handoff or transition evidence.
2. Reconcile the linked execution budget. Record attempt, consecutive no-progress, and context-expansion counters without decreasing or resetting the goal lineage.
3. When declared acceptance checks pass, first revise `TASK-GRAPH.md`: transition the node to `completed`, release its lease, record acceptance evidence in the transition log, and unlock dependents whose dependencies and predeclared assurance checkpoints pass. This graph write is mandatory and precedes communication.
4. Update `PENDING.md` only when a human item or macro project outcome changed; point affected macro rows to the new graph revision. Never use a pending update as a substitute for step 3.
5. Give the user the compact closeout from [status and completion communication](../../docs/STATUS-AND-COMPLETION.md): outcome, current stage/progress, work continuing without user action, human/macro pending work from `PENDING.md`, active/ready/blocked technical graph state from the just-persisted `TASK-GRAPH.md` revision, material changes, checks, `completed`, blockers, next task/action, and inspectable paths.
6. Dispatch the next dependency-ready task without asking for completion approval.
7. Run declared independent review automatically as post-completion assurance. It does not hold the completed node or unrelated ready work. For `assurance_gate: affected-actions`, only graph nodes that explicitly list the completed task in `assurance_requires` remain pending until acceptance. A blocking finding creates a linked remediation task and continues to gate only those affected actions.
8. If a budget ceiling is reached before acceptance, persist evidence and return `stop-and-replan`. Rewrite, decompose, repair missing context, or request one genuine human product/risk decision; never repeat the same lineage under a new model, agent, or task ID.
9. If authority is genuinely missing for a separate action, consolidate it into one exact request and create or update the human-owned item in the pending-work authority. The completed implementation remains completed.
10. If review or correction cannot proceed, name the blocker and selected escalation/decomposition. Never leave the user with only “waiting for review” or an unexplained approval prompt.

Review remains independent and bounded. Communication does not confer acceptance authority, and lifecycle separation does not justify silence or repeated permission requests.
