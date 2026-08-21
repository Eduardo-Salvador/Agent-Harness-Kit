# Harness Engineering Learning Pack

This optional, project-independent pack teaches how this repository's harness works. It is not a runtime mode, contains no project state, and is never loaded by operational agents unless the user explicitly asks to study harness engineering. The directory can be omitted or distributed separately without changing Development Core or Development Core plus project-specific learning.

## Recommended reading order

1. [Harness boundaries](01-HARNESS-BOUNDARIES.md)
2. [Seven components](02-SEVEN-COMPONENTS.md)
3. [Agent loops](03-AGENT-LOOPS.md)
4. [Memory](04-MEMORY.md)
5. [Context engineering](05-CONTEXT-ENGINEERING.md)
6. [Isolation and concurrency](06-ISOLATION.md)
7. [Assurance and checkpoints](07-ASSURANCE.md)
8. [Orchestration and graphs](08-ORCHESTRATION.md)

Each module ends at a concrete repository artifact or playbook. For hands-on study, inspect the [development-only example](../examples/development-only/README.md), then compare the [project-learning example](../examples/development-plus-project-learning/README.md). Project-specific learning is governed by `harness/roles/learning-*`; this pack does not observe or assess the user's software-project work.
