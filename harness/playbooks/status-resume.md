# Playbook: Session start, resume, and status

Use this playbook for the first request in a new context window, any request to continue/resume work, and any project-status request.

1. Read `harness-state/PROJECT-CONTEXT.md` first. Verify schema, approval status, revision, mode, source references, and whether current evidence conflicts with it.
2. Read the pending-work authority second. Use the path pinned by project context or approved decisions; when no other path is declared and `harness-state/PENDING.md` exists, use it.
3. Read `harness-state/TASK-GRAPH.md` third. Verify its pinned project-context revision, active/ready/blocked nodes, dependencies, leases, and transition log.
4. Only after those three sources, load the active task brief, its direct graph neighborhood, applicable decisions/rules/capabilities/model routing, and latest handoff/review evidence.
5. Answer status from durable artifacts. Name their revisions and distinguish accepted, active, ready, blocked, pending-human, stale, and merely observed work.
6. If a required source is absent, stale, or contradictory, state that specific condition and enter the applicable first-run, recovery, or reconciliation playbook.

Do not begin with a repository-wide file scan, dependency inventory, Git-history walk, or speculative architecture reconstruction. A broader inspection is allowed only when the ordered sources expose a concrete gap/conflict, the applicable recovery/discovery playbook requires it, or the user explicitly asks for an audit. State the reason and scope before scanning.

Conversation memory and directory recency never override the canonical artifact order.
