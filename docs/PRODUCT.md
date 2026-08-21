# Product definition

## Purpose

Agent Harness Kit helps developers deliver real software through a disciplined multi-agent process while making harness engineering understandable. It is a reusable project substrate, not a hosted agent product.

## Users and problems

| User | Need | Failure addressed |
| --- | --- | --- |
| Developer new to agent harnesses | A safe path from intent to verified work | Prompting without durable context or clear checkpoints |
| Experienced developer | Repeatable parallel execution with control | Conflicts, hidden assumptions, and unverifiable handoffs |
| Team or maintainer | Auditable decisions and portable workflows | Platform lock-in and state trapped in chat history |
| Learner-practitioner | Feedback on reasoning during real work | Tutorials detached from delivery and unapproved note publication |

## Modes

### Delivery

The required mode. Discovery creates approved project context and an initial task graph. A PO/orchestrator schedules ready nodes, assigns exclusive ownership and isolation, and completes work when declared objective checks pass. It reports the result and advances immediately. Independent review runs automatically as non-blocking assurance, bounded to one initial round plus at most one focused remediation review; blockers create linked remediation and may gate only affected integration/release work.

### Delivery + learning

An optional observer reads approved delivery artifacts and the user's explicit learning profile. It may create a learning queue, guided practice, reasoning feedback, and debriefs. It cannot add, remove, reprioritize, block, or mark delivery nodes complete. See [Core vs. learning](CORE-VS-LEARNING.md).

Both modes use exactly the same delivery core and contracts.

### Optional Harness Engineering Learning Pack

The Harness Engineering Learning Pack (`learning-pack/README.md` in the `full` profile) teaches this repository's harness engineering through project-independent modules. It is not a runtime mode, observes no software-project work, and is excluded from operational context unless explicitly requested. Removing it affects neither delivery mode.

## Product boundaries

The harness owns:

- discovery and approval boundaries;
- layered context and durable artifact contracts;
- dependency-aware orchestration and task lifecycle;
- ownership, isolation, review, verification, and handoffs;
- platform capability negotiation;
- optional learning observation and approved publication.
- namespaced, provenance-preserving adoption into mature existing harnesses.

The harness does not own the user's product strategy, source-control provider, model vendor, note system, CI service, or final authority. It records and enforces decisions made through explicit policy and checkpoints.

## Success criteria for the first executable version

1. A developer can run discovery and obtain a complete, approved `PROJECT-CONTEXT` plus a valid initial `TASK-GRAPH`.
2. The orchestrator schedules only dependency-ready tasks and prevents overlapping file ownership.
3. A task runs in a declared isolation mode and produces a concise, traceable handoff.
4. Objective checks make completion admissible; a different reviewer records non-blocking assurance and can trigger linked remediation.
5. An interrupted run can reconstruct current state from versioned files without relying on chat history.
6. The same fixture completes through Codex and Claude adapters, with declared degradation where capabilities differ.
7. Disabling learning changes no delivery artifact except an explicit mode/configuration record.
8. A new user can follow the documented example without prior harness-engineering knowledge.

## Human checkpoints

Human approval is mandatory for consequential product intent, architecture direction, scope/budget changes, risky permissions, destructive actions, overrides of failed verification, and publication of learning material to an external destination. Checkpoints produce a [decision artifact](contracts/DECISION.md).

## Non-goals

- Building a universal autonomous coding agent or replacing developer judgment.
- Encoding vendor-specific autonomous prompts or unsupported APIs.
- Requiring Codex, Claude, GitHub, MCP, Obsidian, Notion, or any single vendor.
- Treating chat transcripts as canonical memory.
- Automatically granting credentials, escalating permissions, merging, deploying, or publishing notes.
- Loading harness-engineering study material into operational context by default.
- Maximizing agent count or parallelism at the expense of safe ownership.

## Status and scope gate

The first public scope includes native activation for both Codex and Claude Code through documented root entrypoints and small progressive extensions. A profile may be copied into an intentionally empty root or installed under `agent-harness-kit/` with minimal root bridges. It does not include a separate autonomous runtime that independently calls APIs, dispatches sessions, provisions isolation, integrates branches, or publishes notes. Remaining gates are tracked in [OPEN-DECISIONS.md](../OPEN-DECISIONS.md).
