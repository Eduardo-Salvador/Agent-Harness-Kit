# Playbook: Session start, resume, and status

Use this playbook for the first request in a new context window, any request to continue/resume work, and any project-status request.

1. Read `harness-state/PROJECT-CONTEXT.md` first. Verify schema, approval status, revision, mode, source references, and whether current evidence conflicts with it.
2. Read the pending-work authority second and read it in full. Use the path pinned by project context or approved decisions; when no other path is declared and `harness-state/PENDING.md` exists, use it. The graph is never a substitute for this source.
3. Read `harness-state/TASK-GRAPH.md` third. Verify its pinned project-context revision, active/ready/blocked nodes, dependencies, leases, and transition log.
4. Only after those three sources, load the active task brief, its direct graph neighborhood, applicable decisions/rules/capabilities/model routing, and latest handoff/review evidence.
5. Answer status from durable artifacts using [status and completion communication](../../docs/STATUS-AND-COMPLETION.md) and the executable [`harness.status/v1`](../../docs/contracts/STATUS.md) shape. This applies to every user-facing progress/step update, not only explicit status requests. Always label current stage, progress, work continuing without user action, human pending items, macro gaps, active/ready/blocked graph nodes, per-area technical pending/context, blockers, next action, and repository-relative inspectable paths; use `None` explicitly for empty sections. For “my pending items”, “what do you need from me?”, approval, or decision requests, list open `human:*` items first with the exact action/decision and delivery effect. Then join the pending authority's area rows to graph workstreams and show human pending, technical pending, active agent/context, blockers, and next action for each relevant area. Never lead with or limit the answer to graph nodes, and never send a prose-only step update.
6. If a required source is absent, stale, or contradictory, state that specific condition and enter the applicable first-run, recovery, or reconciliation playbook.

Do not begin with a repository-wide file scan, dependency inventory, Git-history walk, or speculative architecture reconstruction. A broader inspection is allowed only when the ordered sources expose a concrete gap/conflict, the applicable recovery/discovery playbook requires it, or the user explicitly asks for an audit. State the reason and scope before scanning.

Conversation memory and directory recency never override the canonical artifact order.

A human-owned pending item or incomplete project area remains reportable even when it is not represented in the task graph. If the pending authority and graph conflict, surface the conflict and reconcile it; never silently discard the pending item or macro gap.
