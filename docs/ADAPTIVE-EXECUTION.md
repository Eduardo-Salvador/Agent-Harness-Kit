# Adaptive execution and assurance

Interaction is also independent: [accompanied delivery](ACCOMPANIED-DELIVERY.md) pauses substantial product builds at client milestones while ordinary technical work stays autonomous. Small decided fixes remain continuous. Product approval is not technical assurance; an explicit continuous-delivery choice cannot waive required safety or authority gates.

[Delivery presets](DELIVERY-MODES.md) choose client participation and pace: accompanied by default, autonomous by explicit choice, or hackathon for a timeboxed demo. Presets do not select a lane/assurance or imply one worker. Autonomous may still require full orchestration for actual parallel agents or required audit.

The Harness makes two independent decisions for each request:

1. **Execution lane**: `direct-trivial`, `vibe`, `graph-only`, or `full-harness`.
2. **Assurance level**: `none`, `light`, or `full`.

The lane controls coordination and durable state. Assurance controls evidence and independent checking. A keyword such as API, dependency, migration, authentication, or integration is evidence to inspect, not by itself a reason to select `full-harness`.

## Execution lanes

- `direct-trivial`: a decided mechanical or static-content edit that can be completed immediately.
- `vibe`: one bounded outcome in one working context, including a small behavior change, with a deterministic check.
- `graph-only`: work that benefits from durable ordering, resumability, or ownership but does not need the complete Harness ceremony.
- `full-harness`: orchestration for a genuinely multi-agent, human-governed, audit-bound, capability-constrained, or unresolved request.

Select `full-harness` automatically only when at least one condition is true:

- the user explicitly requests it;
- execution requires two or more real agents or independently running contexts;
- a human decision or approval loop is part of reaching the outcome;
- an audit trail or independent assurance is required by an approved rule, contract, or the user;
- the available model is too weak or materially uncertain for safe autonomous execution; or
- consequential ambiguity remains after the cheapest bounded clarification or inspection.

Risky subject matter may raise assurance, narrow authority, or require a focused check without changing the lane. With `assurance: auto`, risk may raise assurance; explicit `none` or `light` is otherwise honored with a visible warning unless approved authority mandates more. Actual security, privacy, authorization, or destructive-boundary changes require full audit. Merely mentioning an API or dependency changes neither lane nor assurance.

## Assurance levels

| Level | Evidence and review |
| --- | --- |
| `none` | The executor runs the smallest sufficient check and records the result in its closeout or graph transition. No independent reviewer. |
| `light` | The executor climbs the test ladder as needed and an actual separate reviewer performs a focused acceptance check. |
| `full` | A separate reviewer reconstructs acceptance from approved authority, independently verifies proportional evidence, and may gate only the affected delivery action. |

Independent review remains mandatory whenever effective assurance is `light` or `full`. If no separate reviewer context exists, assurance is blocked; same-context self-review is not a substitute. Do not create a handoff or review packet when no separate consumer exists. A same-context inline node uses an inline spec plus its graph transition or concise closeout.

## Compact and complete full Harness

`full-harness` has two operating shapes:

- **Compact**: use for a bounded, decided outcome that has a full-Harness trigger but needs only a small graph neighborhood. Use the minimum durable state, a compact inline spec when sufficient, and only consumer-driven handoff/review artifacts.
- **Complete**: use when discovery, a human decision loop, multiple coordinated agents/workstreams, material scope uncertainty, or a required full audit needs the complete context → pending → plan → task graph → execution → assurance chain.

Full Harness never means “create every artifact.” It means apply the required controls, choosing compact or complete from the actual coordination and assurance needs.

## Resume and read-only work

Resume begins with a bounded, side-effect-free real-state probe: current working-tree state, active processes or tasks when visible, and the most relevant current check/output. Read durable artifacts only to fill gaps, resolve conflicts, or recover ownership and next actions. Current passing tests and direct runtime evidence outrank stale handoffs; do not load a stale handoff merely because it exists.

A read-only audit, explanation, status inspection, or diagnosis does not initialize a project and does not trigger first-run discovery. Inspect the requested evidence and report it. Enter first-run only before planning or mutating an uninitialized project.

## Planning and test ladder

Before graph/full decomposition, `agent-harness preflight` checks every declared file/path, package script, environment-variable name, executable, validator, browser requirement, and worker capacity. A blocker is reported before task generation, preventing setup failures from becoming implementation/review churn.

Planned implementation units target **15–30 minutes of active agent work**. A unit outside that range must state why atomicity, tool/runtime cost, or risk makes the exception preferable. Do not split work solely to manufacture tiny artifacts.

Verification climbs only as far as the task needs:

1. `focused` — the narrowest test, lint, type, or visual check for the change;
2. `workspace` — the affected package/module suite;
3. `integration` — boundaries between affected components or services;
4. `global/checkpoint` — repository-wide checks or a declared assurance checkpoint;
5. `delivery` — build, package, deploy rehearsal, smoke test, or other release evidence.

Record the highest rung reached and why it was sufficient. A failure triggers bounded technical recovery inside the current scope; it does not automatically require human approval or a lane change.

## Authority, parallelism, and inactivity

Continue technical recovery without approval when it stays within the approved outcome, scope, cost envelope, ownership, and experimental integrity. Ask for a human decision before changing product behavior, scope, material cost/budget, permission or external authority, or the integrity of an experiment or evaluation.

When two or more ready nodes are collision-free and the host proves numeric capacity greater than one, launch the safe batch automatically and report the number of active workers. If an agent produces no observable progress for 60–90 seconds, warn and request a checkpoint. On the second consecutive inactivity occurrence for that agent/task, interrupt it, preserve recoverable state, and reassign or serialize the node within the existing execution budget.
