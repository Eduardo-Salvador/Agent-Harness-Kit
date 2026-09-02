# Architecture

Agent Harness Kit keeps product policy and state platform-neutral; native platform entrypoints translate activation and capabilities without becoming the architecture. Every distribution ships both: Codex reads root `AGENTS.md`, while Claude Code reads root `CLAUDE.md`, which imports `@AGENTS.md`. They converge on one authority and one state model without runtime guessing or profile switching.

## System model

The harness has four platform-neutral layers and thin platform adapters:

1. **Intent and policy:** discovery, approved decisions, project constraints, permissions, and mode selection.
2. **Coordination:** the PO/orchestrator owns graph transitions, readiness, assignments, checkpoints, acceptance, and scoped code-context hints.
3. **Execution:** specialized agents run bounded loops inside isolated task nodes with exclusive file ownership.
4. **Evidence and state:** handoffs, review results, verification evidence, decisions, and durable memory.
5. **Adapters:** translate neutral capabilities to Codex, Claude, source control, sandboxes, hooks, and optional note destinations.

The optional project-specific learning layer is outside the delivery control path. Its exact boundary is defined in [Core vs. learning](CORE-VS-LEARNING.md). The separate Harness Engineering Learning Pack (`learning-pack/README.md` in `full`) is static study content outside every runtime layer and operational context.

## First-run gate

First-run gates planning or mutation in an uninitialized project, not read-only audit, explanation, status inspection, or diagnosis. Resume begins with a bounded real-state probe and consults durable context/pending/graph artifacts only to fill gaps. Current tests/runtime evidence supersede stale handoffs.

For a resumed or status-only session with approved context, the [status/resume playbook](../harness/playbooks/status-resume.md) imposes a strict read order: project context, pending-work authority, then task graph. The pending authority owns human decisions/actions and macro incomplete project areas; the graph owns technical order, dependencies, and execution. Task-local evidence follows.

After project context is approved, an unresolved new capability request invokes [feature discovery](../harness/playbooks/feature-discovery.md) automatically. It reuses project evidence, compares credible directions, and stores `harness.feature-brief/v1` under `harness-state/features/`. The brief must be approved before macro pending state or technical graph topology changes; routine fixes and already-approved implementation do not pass through this gate.

Approved implementation then invokes [writing plans](../harness/playbooks/writing-plans.md). Non-trivial work is captured once under `harness-state/plans/` and decomposed into small executable units; each graph node receives a self-contained task spec so the implementer does not reload the full plan. A strict simple-task gate avoids the separate plan for localized, already-decided work. Missing decisions return to discovery, while contradictory or underspecified execution returns `needs-replan` instead of being improvised.

Every code-behavior or bug-fix unit then follows [test-driven execution](TDD.md). RED and GREEN are evidence phases inside one graph node: the focused test must fail for the intended missing behavior before production edits, pass with the minimum change, and remain passing through bounded refactor and proportional regression. This preserves small task isolation without handing off a deliberately failing baseline.

### Mature existing harnesses

Existing root instructions, role systems, path rules, knowledge, decisions, pending work, and verification sources remain authoritative during namespaced coexistence. A [migration manifest](contracts/MIGRATION-MANIFEST.md) records selector expansion, identities, classification, destinations, backlinks, and semantic status; the [coexistence contract](contracts/COEXISTENCE.md) records precedence. Structural coverage cannot authorize cutover. Human semantic-equivalence review and separate cutover authorization are required before deleting originals or transition duplicates.

## Runtime flow

Before this flow, the `direct-trivial` gate handles atomic presentation/static-content edits outside the runtime graph. It reads only the target and nearest scoped rules, changes it directly, runs a minimal check, and creates no durable harness artifact. Discovery of logic, state, contracts, data, dependencies, accessibility behavior, risk, ownership conflict, or wider impact promotes the request into the normal flow before editing.

1. First-run/resume detection pins approved context or invokes discovery. Discovery updates a draft [project context](contracts/PROJECT-CONTEXT.md), avoiding questions already answered by evidence.
2. Consequential choices pause at a human checkpoint and become [decision artifacts](contracts/DECISION.md). New capabilities with unresolved product choices first produce an approved [feature brief](contracts/FEATURE-BRIEF.md).
3. Approval freezes a context or feature-brief revision; [writing plans](../harness/playbooks/writing-plans.md) creates complete task specs and then creates or updates the [task graph](contracts/TASK-GRAPH.md).
4. The orchestrator finds specified nodes whose dependencies are satisfied, proposed paths do not overlap active ownership, and required capabilities are available. A shared graph-local, in-memory readiness gate rejects false `ready`/`active` dependency, assurance, or checkpoint state without AI or repository scanning. With two or more safe ready nodes, it runs the deterministic `agent-harness schedule` selector against proven numeric capacity, atomically reserves the batch, and records `harness.parallel-dispatch/v1`.
5. It follows [capability-based model routing](MODEL-ROUTING.md), records the least costly safe tier and task-specific reason, and resolves that tier against the current host catalog. On Codex, the executable [native agent dispatch](contracts/CODEX-AGENT-DISPATCH.md) selects the neutral role, constructs a minimal packet from the task SPEC/scoped references, and emits the exact `spawn_agent`/`spawn_subagent` call with resolved model/reasoning and `fork_turns: none`. [`harness.model-dispatch/v1`](contracts/MODEL-DISPATCH.md) stores routing authority; `harness.codex-agent-dispatch/v1` stores the returned identity, context, and adapter response before activation. It then assigns one [task brief](contracts/TASK.md), an exclusive ownership set, and an isolation boundary. Each node may carry a focused `read_set`, exclusive `write_set`, related `impact_set`, and pinned `context_provenance` under [scoped graph execution](SCOPED-GRAPH-EXECUTION.md).
   It also applies [context routing](CONTEXT-ROUTING.md): each task receives a workstream, agent role, execution-context policy, and adapter-owned thread reference. Different workstreams use different contexts unless an explicit integration node owns the crossing.
6. The adapter launches every selected task/subagent without waiting between calls. Each receives a distinct context, lease/isolation reference, task SPEC, and confirmed model-dispatch record. The orchestrator waits for the first completion or attention event, reconciles it, and immediately schedules a refill. A specialized agent loops inside its node: inspect → act → check → update its task artifact. It cannot mutate graph topology.
7. The agent emits a [handoff](contracts/HANDOFF.md) with changes, evidence, and a plain-language closeout. When checks pass, the orchestrator marks the node completed, reports the outcome, releases ownership, and unlocks dependents.
8. A reviewer other than the implementer is launched automatically in a fresh context—preferably a subagent when capability evidence permits it. A minimal packet supplies the pinned SPEC, its referenced authorities, relevant diff, handoff, and verification/TDD evidence while excluding prompt and conversation history. The reviewer derives its criterion matrix from the SPEC before inspecting code, then evaluates the completed work as non-blocking `light`, `standard`, or `critical` assurance. One initial review and at most one fresh focused remediation review are allowed.
9. A blocking finding creates a linked remediation node and may gate affected integration/release work; it does not reopen historical completion or stop unrelated ready nodes. Integration follows the [coherent change policy](CHANGE-INTEGRATION.md) and separate action authorities.
10. Parallel branches converge only through an explicit integration node after all declared dependencies pass. Versioned files allow recovery. If project learning is enabled, its observer reads consented artifacts and updates learning-owned state separately.

## Graph above loops

Graph engineering coordinates work **between** nodes: dependencies, readiness, ownership, isolation, priorities, completion, and remediation. Agent-loop engineering controls work **inside** a node: its prompt, tools, context, iteration, and exit conditions. An agent may propose graph changes in its handoff; only the orchestrator, and a human when consequential, may approve them.

A fresh, approved repository index such as Graphify may enrich navigation and regression hints, but it is not a second operational graph. Generated relationships are verified in source, pinned through `context_provenance`, and never grant write authority or mutate lifecycle state automatically.

## Artifact-based communication

- Canonical state lives in small, versioned Markdown files with a YAML header.
- Every artifact has an identifier, schema version, lifecycle status, and update timestamp or revision reference where relevant.
- References use stable artifact IDs plus repository-relative paths; information is linked instead of duplicated.
- Every user-facing progress/step message follows `harness.status/v1`: stage, progress, automatic work, human/macro pending items, active/ready/blocked graph nodes, blockers, next action, and inspectable paths are explicit; outcome, changes, verification, and lifecycle remain in closeout evidence.
- Large logs remain external or generated; artifacts retain the command, result summary, and durable evidence pointer.

The Phase 2 [review template](../harness/templates/REVIEW.md) defines the independent immutable result referenced by graph state. It is distinct from the implementer's handoff, records the fresh-context reference and packet identity, and cannot be authored in the implementer's context.

## Progressive context

Context is loaded from least to most specific:

1. harness principles and active policies;
2. approved project context and relevant decisions;
3. the capability manifest, approved model-routing revision, resolved model-dispatch evidence, plus only approved durable rules whose scope intersects the role/task/paths;
4. graph neighborhood: the task, dependencies, dependents, and ownership map;
5. the node's `read_set`, followed only when necessary by evidence-backed context expansion; its `impact_set` bounds proportional regression checks while `write_set` remains the sole ownership lease;
6. task-local temporary context, checks, and prior handoff/review evidence;
7. platform instructions exposed by the selected adapter;
8. project-learning profile only for project-learning roles, never delivery agents by default.

The Harness Engineering Learning Pack is outside this sequence and is loaded only for an explicit study request.

Each task brief declares required references. Agents fetch more context only when needed and record material discoveries as artifacts rather than relying on conversational recall.

Temporary task context is not a durable rule. Durable business, security/privacy, architecture, coding, or path-scoped rules require human approval/versioning in the rules map; consequential rule/capability changes require validation before dispatch.

## Seven harness components

| Component | Neutral responsibility | Primary artifact/boundary |
| --- | --- | --- |
| System prompt | Stable role, authority, loop, and exit rules | [Bounded roles](../harness/roles/README.md); task brief supplies instance context |
| Tools | Capability-scoped operations | Adapter capability manifest and task permission set |
| Context management | Progressive, relevant, reconstructable input | Project context, decisions, task/graph neighborhood |
| Verification | Executable acceptance evidence and independent verdict | Task acceptance criteria and handoff evidence |
| Memory | Durable facts and decisions, not chat recall | Versioned contracts and repository history |
| Sandboxes | Isolation, ownership, and safe concurrency | Worktree/branch/ephemeral environment assignment |
| Hooks | Observable lifecycle events and policy gates | Neutral events translated by adapters |

These components shape each node's loop. The task graph coordinates those loops; it is not an eighth kind of prompt.

## State ownership

| State | Sole authority | Who may propose |
| --- | --- | --- |
| Approved product/architecture/scope decision | Human checkpoint | Any role |
| Graph topology and task lifecycle | PO/orchestrator | Agents, reviewer, human |
| File ownership lease | PO/orchestrator | Implementer request |
| Task-local progress | Assigned implementer | Assigned implementer |
| Review verdict | Independent reviewer | Reviewer only |
| Verification evidence | Verification runner/adapter | Implementer or reviewer may invoke |
| Project-learning profile and queue | Project-learning subsystem + user approval policy | Project-learning roles and user |
| External project-learning publication | User | Project-learning subsystem may draft |

The orchestrator rejects ambiguous authority, concurrent ownership overlap, stale revisions, and completion without evidence.

## Adapter boundaries

Core code speaks in capabilities such as `isolate`, `read`, `write`, `execute_check`, `emit_event`, and `request_approval`. Adapters report availability and implement translation. They do not redefine lifecycle states, contract schemas, approval policy, graph semantics, or learning safeguards. See [Portability](PORTABILITY.md).

The first-version adapter layer provides a [generic contract](../adapters/generic.md), native [Codex](../adapters/codex.md) routing through `.agents/skills/`, and native [Claude Code](../adapters/claude.md) routing through `.claude/skills/` and bounded `.claude/agents/`. Both read and write the same neutral `harness-state/`, contracts, rules, capability manifest, and playbooks. A repository may be used with Codex and Claude Code at different times without changing profiles or creating competing state.

These native files activate guidance inside capable installed tools; they are not an unattended external daemon. An active orchestrator may invoke the host's supported subagent/task operations and refill parallel capacity, but no entrypoint enables hooks, MCP, network, secrets, settings, or destructive permissions. Mature hosts preserve colliding platform files through namespaced coexistence and human-approved cutover.

For contained installation, a generated profile may live under host `agent-harness-kit/` while minimal managed blocks in root `AGENTS.md` and `CLAUDE.md` route to it. Host-owned operational state remains in root `harness-state/`, outside the replaceable distribution. Nested native-extension discovery is capability evidence, not an assumption; degraded hosts follow neutral playbooks by explicit path. See [embedded installation](EMBEDDED-INSTALLATION.md).

## Failure and recovery

- State transitions are appendable/auditable and use expected revisions to prevent stale writes.
- Discovery approval rechecks selector expansion and source identities; drift invalidates the snapshot and forces refresh.
- A lost message is harmless because the receiver scans canonical artifact state.
- A failed or missing capability produces an explicit degraded plan or a blocked task, never fabricated evidence.
- Orphaned ownership leases expire or require orchestrator recovery before reassignment.
- Failed checks remain recorded; retries link to prior attempts instead of overwriting them.

## Source and distribution boundary

There is one canonical source tree and project version. [Generated profiles](DISTRIBUTION.md) select Development Core, Core plus project learning, or the full source including the separable Learning Pack. Profiles are packaging views, never long-lived branches or duplicated harness implementations. The public `agent-harness-kit-cli` distribution installs those views; it does not add an autonomous runtime or a competing state store.
