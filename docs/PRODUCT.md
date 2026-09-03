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

### Direct-trivial fast path

Localized, already-decided presentation or static-content mechanics bypass delivery orchestration entirely when they introduce no product behavior, business rule, state, contract, data, dependency, accessibility behavior, risk, or cross-workstream impact. The agent edits the target directly, performs the smallest meaningful check, and reports concisely. No discovery, feature brief, plan, SPEC/TASK, graph event, TDD, handoff, review, or full status ceremony is created. Any discovered ambiguity or broader impact promotes the work before implementation.

### Standard delivery

The required mode. Discovery creates approved project context and an initial task graph. A PO/orchestrator schedules ready nodes, assigns exclusive ownership and isolation, and completes work when declared objective checks pass. It reports the result and advances immediately. Independent review then launches automatically in a fresh context, preferably a proven subagent, and reconstructs acceptance from the versioned task SPEC rather than prompt or implementer memory. Assurance is non-blocking and bounded to one initial round plus at most one focused remediation review; blockers create linked remediation and may gate only affected integration/release work.

### Standard delivery + learning

An optional observer reads approved delivery artifacts and the user's explicit learning profile. It may create a learning queue, guided practice, reasoning feedback, and debriefs. It cannot add, remove, reprioritize, block, or mark delivery nodes complete. See [Core vs. learning](CORE-VS-LEARNING.md).

### Hackathon delivery

A compressed, demo-first pace for time-boxed MVPs. Discovery uses at most two cohesive questions unless consequential authority or safety is missing. The graph prioritizes one demonstrable vertical slice, early integration, isolated workstreams, and a final demo rehearsal while preserving leases, status, checks, and bounded independent review.

### Hackathon delivery + learning

The same fast delivery graph with the optional learning observer. Learning still requires an explicitly approved destination and cannot block or control delivery.

All four runtime selections use exactly the same delivery core and contracts. Standard versus hackathon changes pace and prioritization; the `+learning` variants add only the consented observer.

### Optional Harness Engineering Learning Pack

The Harness Engineering Learning Pack (`learning-pack/README.md` in the `full` profile) teaches this repository's harness engineering through project-independent modules. It is not a runtime mode, observes no software-project work, and is excluded from operational context unless explicitly requested. Removing it affects neither delivery mode.

## Product boundaries

The harness owns:

- discovery and approval boundaries;
- automatic new-feature discovery that compares viable directions and produces an approved feature brief before decomposition;
- optimized writing plans that decompose approved non-trivial outcomes into small self-contained executable specs while keeping simple work inline;
- test-driven behavior delivery that requires meaningful RED, minimal GREEN, and proportional regression evidence inside each code task;
- layered context and durable artifact contracts;
- dependency-aware orchestration and task lifecycle;
- scoped graph execution through focused read paths, exclusive write leases, bounded impact paths, and source provenance;
- ownership, isolation, review, verification, and handoffs;
- platform capability negotiation;
- optional learning observation and approved publication.
- namespaced, provenance-preserving adoption into mature existing harnesses.

The harness does not own the user's product strategy, source-control provider, model vendor, note system, CI service, or final authority. It records and enforces decisions made through explicit policy and checkpoints.

## Success criteria for the first executable version

1. A developer can run discovery and obtain a complete, approved `PROJECT-CONTEXT` plus a valid initial `TASK-GRAPH`.
2. The orchestrator schedules only dependency-ready tasks and prevents overlapping file ownership.
3. A task runs in a declared isolation mode and produces a concise, traceable handoff.
4. Objective checks make completion admissible; a different reviewer in a fresh context independently verifies code against the pinned SPEC, records non-blocking assurance, and can trigger linked remediation.
5. An interrupted run can reconstruct current state from versioned files without relying on chat history.
6. The same fixture completes through Codex and Claude adapters, with declared degradation where capabilities differ.
7. Disabling learning changes no delivery artifact except an explicit mode/configuration record.
8. A new user can follow the documented example without prior harness-engineering knowledge.
9. A user can install the published CLI, create the contained profile plus root bridges in an empty host, and validate that installation without using the source checkout.
10. A new feature request with unresolved product choices automatically produces a reviewable `FEATURE-BRIEF` before pending state or graph topology changes.
11. Planned implementation uses ready 15–30-minute units with justified exceptions; bounded same-context work may use an inline spec and transition.
12. Behavior-changing code and bug fixes cannot complete without valid RED/GREEN evidence and proportional regression, while non-code exceptions remain explicit and reproducible.
13. Every initial review proves a fresh reviewer context, excludes prompt/conversation memory, and records a criterion-by-criterion verdict derived from the task SPEC before implementation inspection.
14. When the host proves numeric capacity and actual subtask operations, independent ready nodes are launched as one collision-safe batch, the first freed slot is refilled, and dependent branches converge through an explicit integration node.

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

The current source and public-index version is `0.7.3` under `agent-harness-kit-cli`. It adds accompanied (default), autonomous end-to-end, and hackathon delivery presets, a read-only CLI inspector, and greeting-triggered onboarding with a visible welcome and unanswered mode choice. The public package was downloaded without cache and passed core installation, root bridges, doctor, embedded validation, and 26 delivery-mode/gate tests. Two bounded real Claude Code greeting cases verified fresh-project welcome/mode selection and approved-context non-repetition. Host instruction loading and truthful evidence remain required; these observations are not a universal behavior guarantee. Existing scope, product, and completion gates remain intact, as do adaptive lanes/assurance, preflight, proportional testing, ownership, scheduling, events, and metrics. The Kit does not independently provision credentials, integrate branches, deploy, or publish notes. Remaining capability decisions are tracked in [OPEN-DECISIONS.md](../OPEN-DECISIONS.md).
