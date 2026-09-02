# Playbook: Session start, resume, and status

Use this playbook for an explicit continue/resume request or a project-status request. A new context alone does not activate it for a read-only audit, explanation, or diagnosis, and those requests do not trigger first-run.

When project context is approved, the first user-visible response in a fresh window is a resume/substantive response, never the first-run welcome. Do not load or replay the first-run handshake unless the initialization test actually fails.

1. Run a bounded, side-effect-free real-state probe first: current working-tree changes, visible active tasks/processes, and the most relevant recent test, build, or runtime output. Do not begin with a repository-wide scan.
2. For explicit status or human-pending questions, read the approved pending-work authority in full and the graph sections needed to answer. For resume, read `PROJECT-CONTEXT.md`, `PENDING.md`, and `TASK-GRAPH.md` only where the probe leaves a gap in authority, ownership, active/ready work, or next action.
3. Load only the active task brief and direct graph neighborhood needed to continue. Current source/runtime evidence and passing checks outrank stale narrative artifacts.
4. Load a handoff or review only when its revision is current and an actual receiving context needs it. Skip stale handoffs when current tests, source, and graph transitions fully establish state.
5. Answer status from durable artifacts using [status and completion communication](../../docs/STATUS-AND-COMPLETION.md) and the executable [`harness.status/v1`](../../docs/contracts/STATUS.md) shape. This applies to every user-facing progress/step update, not only explicit status requests. Always label current stage, progress, work continuing without user action, human pending items, macro gaps, active/ready/blocked graph nodes, per-area technical pending/context, blockers, next action, and repository-relative inspectable paths; use `None` explicitly for empty sections. For “my pending items”, “what do you need from me?”, approval, or decision requests, list open `human:*` items first with the exact action/decision and delivery effect. Then join the pending authority's area rows to graph workstreams and show human pending, technical pending, active agent/context, blockers, and next action for each relevant area. Never lead with or limit the answer to graph nodes, and never send a prose-only step update.
6. If a required source is absent, stale, or contradictory, state that specific condition and enter the applicable first-run, recovery, or reconciliation playbook.

Do not begin with a repository-wide file scan, dependency inventory, Git-history walk, or speculative architecture reconstruction. A broader inspection is allowed only when the ordered sources expose a concrete gap/conflict, the applicable recovery/discovery playbook requires it, or the user explicitly asks for an audit. State the reason and scope before scanning.

Conversation memory never overrides current source/runtime evidence or canonical authority. Durable artifacts fill gaps and resolve ownership; they are not ceremony to replay when the bounded probe already proves current state.

A human-owned pending item or incomplete project area remains reportable even when it is not represented in the task graph. If the pending authority and graph conflict, surface the conflict and reconcile it; never silently discard the pending item or macro gap.
