# Playbook: Parallel execution and isolation

1. Compute ready nodes from the validated DAG; never use agent availability as readiness.
2. Normalize repository-relative write sets. Reject parent/child, identical, wildcard-prefix, and platform-equivalent collisions.
3. Assign one exclusive lease per write set and an adapter-supported isolation boundary.
4. Assign a workstream, agent role, and distinct execution context per task. Do not reuse a context across workstreams; model cross-area work as an explicit integration node.
5. Prefer a worktree or ephemeral environment. If unavailable, serialize execution in a declared directory/branch fallback.
6. Keep shared/generated outputs outside concurrent ownership or assign an explicit integration node.
7. Renew/release leases and task contexts through the orchestrator. Recover orphaned leases before reassignment.
8. Revalidate graph revision, ownership, and context reference before handoff acceptance.

Never allow concurrent writers merely because their intended edits are “probably different.”
