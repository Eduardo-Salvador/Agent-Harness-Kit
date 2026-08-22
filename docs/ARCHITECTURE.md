# Architecture

Agent Harness Kit keeps product policy and state platform-neutral; native platform entrypoints translate activation and capabilities without becoming the architecture. Every distribution ships both: Codex reads root `AGENTS.md`, while Claude Code reads root `CLAUDE.md`, which imports `@AGENTS.md`. They converge on one authority and one state model without runtime guessing or profile switching.

## System model

The harness has four platform-neutral layers and thin platform adapters:

1. **Intent and policy:** discovery, approved decisions, project constraints, permissions, and mode selection.
2. **Coordination:** the PO/orchestrator owns graph transitions, readiness, assignments, checkpoints, and acceptance.
3. **Execution:** specialized agents run bounded loops inside isolated task nodes with exclusive file ownership.
4. **Evidence and state:** handoffs, review results, verification evidence, decisions, and durable memory.
5. **Adapters:** translate neutral capabilities to Codex, Claude, source control, sandboxes, hooks, and optional note destinations.

The optional project-specific learning layer is outside the delivery control path. Its exact boundary is defined in [Core vs. learning](CORE-VS-LEARNING.md). The separate Harness Engineering Learning Pack (`learning-pack/README.md` in `full`) is static study content outside every runtime layer and operational context.

## First-run gate

At session start, the core checks for approved `harness-state/PROJECT-CONTEXT.md`. Absence, non-approved status, or material conflict triggers the [first-run playbook](../harness/playbooks/first-run.md) before implementation planning. Discovery identifies greenfield versus existing state, fills gaps, records decisions, and selects `delivery` or `delivery+learning`. Only approved context seeds a graph. Adapters may surface this through available facilities or a session-start check; they cannot weaken it.

For a resumed or status-only session with approved context, the [status/resume playbook](../harness/playbooks/status-resume.md) imposes a strict read order: project context, pending-work authority, then task graph. The pending authority owns human decisions/actions and macro incomplete project areas; the graph owns technical order, dependencies, and execution. Task-local evidence follows.

### Mature existing harnesses

Existing root instructions, role systems, path rules, knowledge, decisions, pending work, and verification sources remain authoritative during namespaced coexistence. A [migration manifest](contracts/MIGRATION-MANIFEST.md) records selector expansion, identities, classification, destinations, backlinks, and semantic status; the [coexistence contract](contracts/COEXISTENCE.md) records precedence. Structural coverage cannot authorize cutover. Human semantic-equivalence review and separate cutover authorization are required before deleting originals or transition duplicates.

## Runtime flow

1. First-run/resume detection pins approved context or invokes discovery. Discovery updates a draft [project context](contracts/PROJECT-CONTEXT.md), avoiding questions already answered by evidence.
2. Consequential choices pause at a human checkpoint and become [decision artifacts](contracts/DECISION.md).
3. Approval freezes a context revision and creates the initial [task graph](contracts/TASK-GRAPH.md).
4. The orchestrator finds nodes whose dependencies are satisfied, proposed paths do not overlap active ownership, and required capabilities are available.
5. It follows [capability-based model routing](MODEL-ROUTING.md), records the least costly safe tier and task-specific reason, then assigns one [task brief](contracts/TASK.md), an exclusive ownership set, and an isolation boundary.
   It also applies [context routing](CONTEXT-ROUTING.md): each task receives a workstream, agent role, execution-context policy, and adapter-owned thread reference. Different workstreams use different contexts unless an explicit integration node owns the crossing.
6. A specialized agent loops inside that node: inspect → act → check → update its task artifact. It cannot mutate graph topology.
7. The agent emits a [handoff](contracts/HANDOFF.md) with changes, evidence, and a plain-language closeout. When checks pass, the orchestrator marks the node completed, reports the outcome, releases ownership, and unlocks dependents.
8. A reviewer other than the implementer automatically evaluates the completed work as non-blocking assurance using a `light`, `standard`, or `critical` profile. One initial review and at most one focused remediation review are allowed.
9. A blocking finding creates a linked remediation node and may gate affected integration/release work; it does not reopen historical completion or stop unrelated ready nodes. Integration follows the [coherent change policy](CHANGE-INTEGRATION.md) and separate action authorities.
10. Versioned files allow recovery. If project learning is enabled, its observer reads consented artifacts and updates learning-owned state separately.

## Graph above loops

Graph engineering coordinates work **between** nodes: dependencies, readiness, ownership, isolation, priorities, completion, and remediation. Agent-loop engineering controls work **inside** a node: its prompt, tools, context, iteration, and exit conditions. An agent may propose graph changes in its handoff; only the orchestrator, and a human when consequential, may approve them.

## Artifact-based communication

- Canonical state lives in small, versioned Markdown files with a YAML header.
- Every artifact has an identifier, schema version, lifecycle status, and update timestamp or revision reference where relevant.
- References use stable artifact IDs plus repository-relative paths; information is linked instead of duplicated.
- Every user-facing progress/step message follows `harness.status/v1`: stage, progress, automatic work, human/macro pending items, active/ready/blocked graph nodes, blockers, next action, and inspectable paths are explicit; outcome, changes, verification, and lifecycle remain in closeout evidence.
- Large logs remain external or generated; artifacts retain the command, result summary, and durable evidence pointer.

The Phase 2 [review template](../harness/templates/REVIEW.md) defines the independent immutable result referenced by graph state. It is distinct from the implementer's handoff and cannot be authored by the implementer.

## Progressive context

Context is loaded from least to most specific:

1. harness principles and active policies;
2. approved project context and relevant decisions;
3. the capability manifest, approved model-routing revision, plus only approved durable rules whose scope intersects the role/task/paths;
4. graph neighborhood: the task, dependencies, dependents, and ownership map;
5. task-local files, temporary context, checks, and prior handoff/review evidence;
6. platform instructions exposed by the selected adapter;
7. project-learning profile only for project-learning roles, never delivery agents by default.

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

These native files activate guidance inside capable installed tools; they are not an external autonomous runtime. No entrypoint enables hooks, MCP, network, secrets, settings, or destructive permissions. Mature hosts preserve colliding platform files through namespaced coexistence and human-approved cutover.

For contained installation, a generated profile may live under host `agent-harness-kit/` while minimal managed blocks in root `AGENTS.md` and `CLAUDE.md` route to it. Host-owned operational state remains in root `harness-state/`, outside the replaceable distribution. Nested native-extension discovery is capability evidence, not an assumption; degraded hosts follow neutral playbooks by explicit path. See [embedded installation](EMBEDDED-INSTALLATION.md).

## Failure and recovery

- State transitions are appendable/auditable and use expected revisions to prevent stale writes.
- Discovery approval rechecks selector expansion and source identities; drift invalidates the snapshot and forces refresh.
- A lost message is harmless because the receiver scans canonical artifact state.
- A failed or missing capability produces an explicit degraded plan or a blocked task, never fabricated evidence.
- Orphaned ownership leases expire or require orchestrator recovery before reassignment.
- Failed checks remain recorded; retries link to prior attempts instead of overwriting them.

## Source and distribution boundary

There is one canonical source tree and project version. [Generated profiles](DISTRIBUTION.md) select Development Core, Core plus project learning, or the full source including the separable Learning Pack. Profiles are packaging views, never long-lived branches or duplicated harness implementations.
