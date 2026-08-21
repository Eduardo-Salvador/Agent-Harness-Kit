# Sandboxes, worktrees, and concurrent environments

Isolation limits the blast radius of one task. A worktree, branch, or ephemeral environment can provide a separate execution boundary, but the invariant is platform-neutral: concurrently executable tasks must not share write ownership.

The orchestrator grants an exclusive lease over normalized repository-relative paths. If strong isolation is unavailable, the safe fallback is serialized work in an explicitly exclusive directory or branch. “Different agents” is not isolation, and intended edits do not prevent collisions.

Ephemeral environments also need evidence and recovery: identify the environment in the task/handoff, record checks before cleanup, and recover orphaned leases before reassignment.

Read the [parallel execution playbook](../harness/playbooks/parallel-execution.md) and [portability degradation table](../docs/PORTABILITY.md#degradation-policy). The invalid collision fixture used by the validator demonstrates why two ready nodes cannot own a parent/child write set.
