# Playbook: Task closeout and user communication

Use this playbook whenever implementation, review, acceptance, or a material phase reaches a boundary.

`direct-trivial` edits do not create tasks, handoffs, graph transitions, or review. Close them with one concise statement of the edit and smallest useful check; use the steps below only if the work was promoted into a task.

Artifact footprint follows the actual continuation path. A same-context node records the concise outcome, highest test-ladder rung, and check result in its completion transition; it creates no handoff. Create a handoff/review packet only when an actual separate consumer will continue or independently review the work. Lane and `assurance: none|light|full` are independent.

1. Persist a concise graph transition for same-context work. Persist a handoff only for a real receiving context. For TDD, record meaningful RED, GREEN from the identical focused command, refactor status, and the highest sufficient ladder rung in whichever artifact the continuation path actually uses.
2. Reconcile the linked execution budget. Record attempt, consecutive no-progress, and context-expansion counters without decreasing or resetting the goal lineage.
3. When declared acceptance checks pass, first revise `TASK-GRAPH.md`: transition the node to `completed`, release its lease, record acceptance evidence in the transition log, and unlock dependents only when dependencies, predeclared assurance checkpoints, and product approvals pass. Declared completion conditions need current observed evidence; required TDD/smoke evidence must also pass. This graph write is mandatory and precedes communication.
4. Update `PENDING.md` only when a human item or macro project outcome changed; point affected macro rows to the new graph revision. Never use a pending update as a substitute for step 3.
5. Give the user the compact closeout from [status and completion communication](../../docs/STATUS-AND-COMPLETION.md): outcome, current stage/progress, work continuing without user action, human/macro pending work from `PENDING.md`, active/ready/blocked technical graph state from the just-persisted `TASK-GRAPH.md` revision, material changes, checks, `completed`, blockers, next task/action, and inspectable paths.
6. Follow [accompanied delivery](../../docs/ACCOMPANIED-DELIVERY.md): at a client milestone show the result and request evaluation, then stop affected expansion until explicit current approval. Dispatch unrelated ready work whose gates pass without ceremonial completion approval. Technical completion does not imply product acceptance.
7. For `assurance: light|full`, launch independent review automatically in a fresh reviewer context using the consumer-bound packet. Review does not hold the completed node or unrelated ready work. `assurance: none` has no review step, regardless of lane.
8. If a budget ceiling is reached before acceptance, persist evidence and return `stop-and-replan`. Rewrite, decompose, repair missing context, or request one genuine human product/risk decision; never repeat the same lineage under a new model, agent, or task ID.
9. If authority is genuinely missing for a separate action, consolidate it into one exact request and create or update the human-owned item in the pending-work authority. The completed implementation remains completed.
10. If review or correction cannot proceed, name the blocker and selected escalation/decomposition. Never leave the user with only “waiting for review” or an unexplained approval prompt.

Review remains independent and bounded. Communication does not confer acceptance authority, and lifecycle separation does not justify silence or repeated permission requests.
