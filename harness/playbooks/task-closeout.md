# Playbook: Task closeout and user communication

Use this playbook whenever implementation, review, acceptance, or a material phase reaches a boundary.

1. Persist the handoff or transition evidence.
2. When declared acceptance checks pass, the orchestrator immediately transitions the node to `completed`, releases its lease, updates the macro project overview when an area changed, and unlocks dependents whose dependencies and predeclared assurance checkpoints pass.
3. Give the user the compact closeout from [status and completion communication](../../docs/STATUS-AND-COMPLETION.md): outcome, material changes, checks, `completed`, next task/action, and human action required.
4. Dispatch the next dependency-ready task without asking for completion approval.
5. Run declared independent review automatically as post-completion assurance. It does not hold the completed node or unrelated ready work. For `assurance_gate: affected-actions`, only graph nodes that explicitly list the completed task in `assurance_requires` remain pending until acceptance. A blocking finding creates a linked remediation task and continues to gate only those affected actions.
6. If authority is genuinely missing for a separate action, consolidate it into one exact request and create or update the human-owned item in the pending-work authority. The completed implementation remains completed.
7. If review or correction cannot proceed, name the blocker and selected escalation/decomposition. Never leave the user with only “waiting for review” or an unexplained approval prompt.

Review remains independent and bounded. Communication does not confer acceptance authority, and lifecycle separation does not justify silence or repeated permission requests.
