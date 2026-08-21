# Playbook: Parallel execution and isolation

1. Compute ready nodes from the validated DAG; never use agent availability as readiness.
2. Normalize repository-relative write sets. Reject parent/child, identical, wildcard-prefix, and platform-equivalent collisions.
3. Assign one exclusive lease per write set and an adapter-supported isolation boundary.
4. Prefer a worktree or ephemeral environment. If unavailable, serialize execution in a declared directory/branch fallback.
5. Keep shared/generated outputs outside concurrent ownership or assign an explicit integration node.
6. Renew/release leases through the orchestrator. Recover orphaned leases before reassignment.
7. Revalidate graph revision and ownership before handoff acceptance.

Never allow concurrent writers merely because their intended edits are “probably different.”
