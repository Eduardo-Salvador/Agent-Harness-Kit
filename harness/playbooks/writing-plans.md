# Writing plans

Use this playbook only after [request routing](request-routing.md) selects `graph-only` or `full-harness` and the relevant product context or feature brief is approved. `direct-trivial` and `vibe` stop before planning. The result is an execution packet: a plan for non-trivial work plus one concise task spec per executable unit.

Before decomposition, run `agent-harness preflight` with every prerequisite named by the approved request/context: paths, package scripts, environment-variable names, native commands, validator, browser requirement, and proven worker capacity. Stop on blockers and record exact capability degradation; do not create a speculative graph first.

## Fast-route boundary

The request router owns pre-Harness classification. `vibe` permits one decided, small local behavior change in one working context with low blast radius and a focused check. Failed verification starts bounded in-scope recovery; promote only when a full-Harness condition appears.

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

For graph/full engineering work that was not routed to `direct-trivial` or `vibe`, a task is `inline-simple` only when every condition is true:

- it has one directly requested, already-decided outcome;
- it stays within one local ownership area and requires no cross-workstream coordination;
- it introduces no product behavior choice, dependency, schema/API contract, migration, authentication/authorization, security/privacy boundary, or risky permission;
- one deterministic check can prove completion; and
- active agent work is reasonably expected to fit within five minutes.

If uncertain, classify it as `planned`. An `inline-simple` task skips the separate plan file but still receives a compact task spec containing exact change, paths, non-goals, acceptance, verification, and replan triggers. It is intentionally different from `direct-trivial`, which creates no spec. Do not spend more context proving simplicity than planning the work would cost.

### Graph-only evidence profile

After a task passes the `inline-simple` gate, it may use `evidence_profile: graph-only` only when verification is deterministic and the task changes no product behavior, security/privacy/authentication boundary, data/schema/API contract, dependency, migration, external side effect, integration boundary, cross-workstream ownership, or assurance-gated outcome. It must use `test_strategy: verification-only`, `review_profile: none`, `max_review_rounds: 0`, `reviewer: not-required`, and `assurance_gate: none`.

The agent runs declared verification and records the highest sufficient test-ladder rung. A same-context node closes in its graph transition. If `assurance: light|full` requires an independent reviewer, create the consumer-bound packet; otherwise do not create handoff ceremony. Failed checks begin bounded in-scope recovery.

## Non-trivial planning flow

1. Pin the approved project context and feature brief/decision when applicable. Load only scoped source evidence required to identify paths and dependencies.
2. Write `harness-state/plans/PLAN-<id>.md` from the implementation-plan template. Keep product choices out of the plan; unresolved consequential behavior returns to discovery.
3. Decompose the outcome into ordered units targeting 15–30 minutes of active agent work. Tool runtime, dependency download, CI wait, and independent assurance are not implementation time. A smaller or larger unit states why atomicity, runtime cost, or risk makes the exception preferable.
4. Each unit declares one observable result, exact change, dependencies, `read_set`, exclusive `write_set`, `impact_set`, non-goals, acceptance criteria, verification, test strategy, and stop/replan triggers. Behavior changes and bug fixes declare a focused RED test/expected failure, minimum GREEN implementation, and proportional regression command. If these cannot remain concise, split the unit without separating RED from GREEN.
5. Map each unit to a graph node and generate a self-contained `TASK.md` when a separate implementer will consume it. A same-context inline node uses a compact inline spec plus its graph transition. Pin planning mode, plan revision/step, target minutes, evidence profile, and orthogonal assurance; do not create a handoff merely to transfer work to the same context.
6. Validate dependency order, path leases, capability availability, acceptance, and integration coverage. Mark the plan `ready`; no ceremonial human approval is required unless planning exposes a consequential product, architecture, risk, permission, budget, or scope decision.
7. Dispatch only a node with a complete spec. The implementer executes the stated change and checks; it does not redesign the plan while coding.

For test strategy and evidence, follow [test-driven execution](test-driven-execution.md). An `inline-simple` graph/full task is exempt from the separate plan, not from TDD when it changes behavior. A `direct-trivial` edit never enters TDD; an eligible `vibe` behavior change also stays outside TDD but still requires focused verification. Hackathon pace narrows the test and regression scope but does not permit implementation before meaningful RED inside `full-harness`.

## No-improvisation boundary

An implementer stops and reports `needs-replan` when the spec is missing or contradictory, an undeclared dependency or product choice appears, the required write path is outside the lease, acceptance cannot be evaluated, or the unit is materially larger than planned. It may make ordinary local coding choices that do not change observable behavior, contracts, scope, dependencies, or risk.

The orchestrator revises the plan/spec, graph, and budget evidence in one operational step. Replanning is not a hidden implementation retry and does not reset the goal lineage.

## Optimization rules

- One plan may contain many small units; do not create a plan file per unit.
- One task brief is the unit's executable spec. Do not create a second spec document.
- The implementer loads its task brief and pinned source paths first; it does not need to load the whole implementation plan during normal execution. The plan is provenance and is opened only for a reported contradiction or replan.
- Prefer the smallest coherent number of units. Fifteen-to-thirty minutes is a planning target, not a reason to split an atomic edit or pad a small change.
- Evidence and review follow `assurance: none|light|full`, independently from lane. Create a handoff and review packet only for an actual separate consumer; preserve fresh independent review whenever `light` or `full` assurance requires it.
- A separate executor always receives a self-contained task in a separate context; an inline executor uses the compact graph spec.
