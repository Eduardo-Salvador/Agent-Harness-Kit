# Contract: Rules map

The rules map indexes human-approved durable project rules and preserved existing rules without copying them into every task.

Rule kinds include business rules, security/privacy constraints, architectural invariants, coding conventions, and path-scoped rules. Each entry records ID, kind, authority/source identity, scope/paths, affected roles/tasks, precedence, status, approval, validation, and destination/backlink when migrated.

## Invariants

- Durable rules are human-approved and versioned; temporary task context is labeled task-local and never silently promoted.
- Progressive disclosure routes only applicable rules to an agent/task.
- More-specific approved path rules take precedence in scope; conflicts block work and require a decision.
- Mature adoption preserves existing project/platform rules and provenance until semantic review and authorized cutover.
- Consequential durable-rule changes require explicit human approval and validation evidence.
