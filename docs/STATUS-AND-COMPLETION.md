# Status and completion communication

The harness distinguishes the project-level completion overview and actions that require a human from technical execution state. A task graph is not a substitute for the pending-work authority, and an internal handoff is not a substitute for telling the user what happened.

## Fast-route exception

A request classified by [request routing](../harness/playbooks/request-routing.md) as `direct-trivial` or `vibe` never becomes a task or graph event. Do not emit an intermediate status update or render `harness.status/v1` unless the edit becomes blocked or must be promoted. Make the edit and return a concise closeout naming what changed and the smallest check run. `direct-trivial` may report `not run` when no meaningful check exists for a purely static edit; `vibe` must always report a passing focused deterministic check.

Fast routes cannot hide human pending items or bypass an explicit status/resume question. Failed verification begins bounded in-scope recovery; promotion occurs only when recovery reveals a full-Harness condition.

## Graph-only closeout

A graph node remains a real task, but lane and assurance are independent. Same-context work records its outcome and highest sufficient test-ladder rung in one transition and creates no handoff. Create a handoff/review packet only for an actual separate consumer. `assurance: light|full` preserves fresh independent review; `none` closes on executor verification.

## Mandatory step update

Use brief updates at task start, concrete progress, a blocker, and phase completion. State the result/evidence, any human action, and what follows. Routine updates do not require a full status form or artifact reread. Explicit status/pending questions and milestone closeouts use the complete view below; never hide a human blocker in a short progress message.

Each complete status view explicitly labels: **Current stage**, **Progress**, **Continuing without your action**, **Human pending and macro gaps (`PENDING.md`)**, **Technical graph (`TASK-GRAPH.md`)**, **Blockers**, **Next action**, and **Inspectable paths**. Localize those labels to the user's language (for example, **Etapa atual** and **Continua sem sua ação**) without dropping or merging sections. “Continuing without your action” names automatic work already authorized or says `None`. The pending section lists human actions plus incomplete macro areas, even when empty. The graph section summarizes active, ready, and blocked nodes plus relevant dependencies; it never substitutes for `PENDING.md`.

Persist before speaking: when the update reports dispatch/start, material progress, dependency changes, block/unblock, remediation, completion, lease/context changes, or newly ready work, revise `TASK-GRAPH.md` and append its transition log first. Generate status from that new revision. `PENDING.md` changes in the same step only for human/macro state; a pending-only technical update is invalid.

## Pending-work precedence

For “my pending items”, “what do you need from me?”, approval, or decision queries:

1. Read the approved pending-work authority in full before the graph.
2. Return open items owned by `human:*` first. Include the exact request or decision, why it matters, whether it blocks delivery, and its source.
3. State “No human action is currently recorded” when that set is empty.
4. Read the project completion overview in the same authority for the macro view of what remains, such as unfinished backend or authentication work.
5. Only then, when useful or requested, use the task graph for technical order, dependencies, and execution detail.

For general project status, present: human action required, project completion overview, then a workstream view that joins each area to its technical graph nodes, active agent/context, blockers, and next action. Never omit a human-owned pending item or macro project gap merely because it is not a graph node. Reconcile contradictions visibly; do not silently choose the graph.

Render explicit status views and milestone closeouts through [`harness.status/v1`](contracts/STATUS.md): stage, progress, automatic actions, human action, macro pending work, graph snapshot, per-workstream pending/progress/context, blockers, next action, and repository-relative inspectable paths are mandatory. Pin the consulted project-context, pending-authority, and graph revisions. Status is a derived view, never a competing authority.

## No silent finish

When implementation or a material phase finishes, tell the user before starting another potentially lengthy phase. The update must name:

- the outcome in plain language;
- the current stage and measurable progress (or a precise qualitative baseline);
- material files or behavior changed;
- checks run and their result;
- the precise lifecycle state (`completed`, `blocked`, or `failed`), with `human-owned` stated separately when a blocked item requires a person;
- blockers, explicitly “none” when empty;
- the next action;
- repository-relative inspectable evidence paths; and
- any human action actually required, or “none”.

Do not expose only an internal artifact path or say that review is pending without describing the completed work.

## Continue within granted authority

Follow [accompanied delivery](ACCOMPANIED-DELIVERY.md). Meaningful product checkpoints are required pauses, not ceremonial technical completion approval. Persist one transition per actual state change, not per message/tool call; update rules only when durable rules change.

Local validation, bounded technical recovery, completion transitions, and next-task dispatch inside approved scope/cost/ownership are normal execution steps. Independent assurance and proportional remediation are also automatic when declared. Perform them without asking again.

Do not request approval merely to:

- run the task's declared local checks;
- dispatch a predeclared independent reviewer for `assurance: light|full`;
- record an evidence-backed graph transition;
- apply corrections inside the existing outcome, lease, paths, capabilities, and review budget; or
- report completion.

## Approval request quality

Ask at planned client milestones under [accompanied delivery](ACCOMPANIED-DELIVERY.md), or once as late as safely possible when the next action changes product behavior, approved scope, material cost/budget, permission or external authority, experimental/evaluation integrity, or a separately gated destructive/delivery action. In-scope technical diagnosis, correction, reruns, and proportional regression continue automatically; a failed check alone is not an approval gate.

Before asking, consolidate related approvals and state the exact proposed action, why it is needed now, affected target, material effect/risk, safe default, and what work can continue without it. Never repeat an approval that the durable state already records as granted.

## Terminal behavior

- Completed: only after every declared completion condition has passing observed evidence, close the technical task, release its lease, and report completion. Dispatch only work whose dependencies, product approvals, and declared assurance gates pass. At a client milestone, demonstrate the result and actually wait before affected expansion; unrelated authorized work may continue. Initial plan approval and technical completion are not client acceptance.
- Post-completion review: run automatically and non-blockingly for `assurance: light|full`; `none` has no review step. A critical checkpoint keeps only affected actions pending.
- Human-blocked: record one actionable human pending item and ask the concrete decision once.
- Review budget exhausted: report blockers and escalation/decomposition on the remediation/integration path; do not keep the project in an unnamed review loop.
