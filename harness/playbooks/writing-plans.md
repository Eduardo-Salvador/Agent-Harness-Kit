# Writing plans

Use this playbook after the relevant product context or feature brief is approved and before graph creation or dispatch. Its result is an execution packet: a plan for non-trivial work plus one concise task spec per executable unit.

## Direct-trivial gate — no SDD

Before creating any durable harness artifact, classify a request as `direct-trivial` only when every condition is true:

- the user has already decided one atomic result and its target is clear;
- the edit is presentational, static content, or an equally mechanical local value—for example one color, spacing value, typo, static label, or asset reference;
- it adds no product behavior, business rule, interaction/state flow, data/schema/API contract, dependency, authentication/authorization, security/privacy/accessibility behavior, migration, permission, or cross-workstream coordination;
- it touches one local ownership area, does not conflict with an active lease, and has no plausible material blast radius; and
- targeted inspection plus edit should take only a few minutes.

Execute this class directly: read the target and nearest scoped rules, make the smallest edit, run the cheapest meaningful syntax/build/visual check when available, and return a concise result. Do not create a feature brief, plan, inline SPEC/TASK, graph node, lease artifact, TDD cycle, handoff, independent review, or full status artifact/update. It is valid to report `not run` when no meaningful check exists for a purely visual/static edit; never invent one.

If any condition is uncertain or inspection reveals logic, state, ambiguity, broader impact, risk, or a conflicting owner, leave `direct-trivial` immediately and promote the work to the simple-task or planned route. Classification should be cheaper than the edit itself.

## Simple-task gate

For engineering work that does not qualify as `direct-trivial`, a task is `inline-simple` only when every condition is true:

- it has one directly requested, already-decided outcome;
- it stays within one local ownership area and requires no cross-workstream coordination;
- it introduces no product behavior choice, dependency, schema/API contract, migration, authentication/authorization, security/privacy boundary, or risky permission;
- one deterministic check can prove completion; and
- active agent work is reasonably expected to fit within five minutes.

If uncertain, classify it as `planned`. An `inline-simple` task skips the separate plan file but still receives a compact task spec containing exact change, paths, non-goals, acceptance, verification, and replan triggers. It is intentionally different from `direct-trivial`, which creates no spec. Do not spend more context proving simplicity than planning the work would cost.

### Graph-only evidence profile

After a task passes the `inline-simple` gate, it may use `evidence_profile: graph-only` only when verification is deterministic and the task changes no product behavior, security/privacy/authentication boundary, data/schema/API contract, dependency, migration, external side effect, integration boundary, cross-workstream ownership, or assurance-gated outcome. It must use `test_strategy: verification-only`, `review_profile: none`, `max_review_rounds: 0`, `reviewer: not-required`, and `assurance_gate: none`.

The agent still runs the declared verification. On success, the orchestrator records a concise result and check outcome in the graph transition, completes the node, releases the lease, and unlocks dependents. It creates no handoff, review packet, review artifact, copied log, or separate evidence file. Any ambiguous/failed check, behavior/TDD work, consequential risk, remediation, or discovered broader impact promotes the task to `evidence_profile: handoff-review` before completion. Graph-only reduces durable artifacts; it never turns an unverified claim into completion.

## Non-trivial planning flow

1. Pin the approved project context and feature brief/decision when applicable. Load only scoped source evidence required to identify paths and dependencies.
2. Write `harness-state/plans/PLAN-<id>.md` from the implementation-plan template. Keep product choices out of the plan; unresolved consequential behavior returns to discovery.
3. Decompose the outcome into ordered units targeting two to five minutes of active agent work. Tool runtime, dependency download, CI wait, and independent assurance are not implementation time.
4. Each unit declares one observable result, exact change, dependencies, `read_set`, exclusive `write_set`, `impact_set`, non-goals, acceptance criteria, verification, test strategy, and stop/replan triggers. Behavior changes and bug fixes declare a focused RED test/expected failure, minimum GREEN implementation, and proportional regression command. If these cannot remain concise, split the unit without separating RED from GREEN.
5. Map each unit to a graph node and generate a self-contained `TASK.md`. The task pins `planning_mode`, plan revision, plan step, target minutes, and `evidence_profile`. Planned units always use `handoff-review`. Copy only executable facts into the task spec; do not make the implementer reread the full plan.
6. Validate dependency order, path leases, capability availability, acceptance, and integration coverage. Mark the plan `ready`; no ceremonial human approval is required unless planning exposes a consequential product, architecture, risk, permission, budget, or scope decision.
7. Dispatch only a node with a complete spec. The implementer executes the stated change and checks; it does not redesign the plan while coding.

For test strategy and evidence, follow [test-driven execution](test-driven-execution.md). An `inline-simple` engineering task is exempt from the separate plan, not from TDD when it changes behavior. A `direct-trivial` presentation/static-content edit never enters TDD. Hackathon pace narrows the test and regression scope but does not permit implementation before meaningful RED.

## No-improvisation boundary

An implementer stops and reports `needs-replan` when the spec is missing or contradictory, an undeclared dependency or product choice appears, the required write path is outside the lease, acceptance cannot be evaluated, or the unit is materially larger than planned. It may make ordinary local coding choices that do not change observable behavior, contracts, scope, dependencies, or risk.

The orchestrator revises the plan/spec, graph, and budget evidence in one operational step. Replanning is not a hidden implementation retry and does not reset the goal lineage.

## Optimization rules

- One plan may contain many small units; do not create a plan file per unit.
- One task brief is the unit's executable spec. Do not create a second spec document.
- The implementer loads its task brief and pinned source paths first; it does not need to load the whole implementation plan during normal execution. The plan is provenance and is opened only for a reported contradiction or replan.
- Prefer the smallest coherent number of units. Two-to-five minutes is a decomposition target, not a reason to split a single atomic edit into ceremony.
- Evidence and review remain proportional: eligible inline-simple work may close through one graph transition; all planned, behavior, risky, ambiguous, or assurance-relevant work uses `handoff-review`. Do not add approval gates between correctly specified units.
