# Request route contract

`harness.request-route/v1` is the neutral classification contract applied before first-run discovery, resume/status loading, feature discovery, planning, graph creation, TDD, review, or full status ceremony.

## Fields

```yaml
schema: harness.request-route/v1
route: direct-trivial | vibe | graph-only | full-harness
classification: deterministic | ai-ambiguity | fallback
user_override: none | direct-trivial | vibe | graph-only | full-harness
hard_triggers: []
reason: <short decision>
verification: <smallest meaningful check or planned harness verification>
promotion_trigger: <condition that requires reclassification before further edits>
```

The record is conceptual for `direct-trivial` and `vibe`: those routes create no durable route file. The template exists for adapters, tests, and integrations that need to exchange a route decision; full Harness workflows may persist the decision in their normal task authority instead of creating a second artifact.

## Decision precedence

1. A user request for `full-harness` always wins.
2. A hard full trigger always selects `full-harness`, even when the user asks for `vibe`, `direct-trivial`, or `graph-only`.
3. Otherwise, honor an explicit user lane override when that lane's eligibility rules pass.
4. Otherwise, apply deterministic rules first. Use an available economical classifier only when the request remains genuinely ambiguous and classification costs less than doing the work.
5. If ambiguity remains unresolved or the classifier is unavailable, select `full-harness`.

`fallback` means the deterministic preflight exposed ambiguity but no economical classifier resolved it on that surface; `full-harness` is therefore the safe lane. It is never a fifth route.

No route may invent credentials, call a separate AI provider, hardcode a model ID, or claim a silent model switch in an already-running context.

## Lanes

- `direct-trivial`: one decided, localized presentation/static-content or equally mechanical value edit; no product behavior, interaction/state, contract, data, dependency, accessibility behavior, risk, or cross-workstream impact. It creates no Harness artifacts and runs the smallest useful check when one exists.
- `vibe`: one decided, small local change, including limited observable behavior, within one workstream and ownership area. It has a clear target, low blast radius, no hard trigger, and a focused deterministic check. It creates no feature brief, plan, task, graph, TDD evidence, handoff, review, route, or full status artifact.
- `graph-only`: deterministic, low-risk technical work that needs graph scheduling or ownership coordination and satisfies the existing `evidence_profile: graph-only` contract. It is a real graph task and records only its checked transition.
- `full-harness`: all consequential, ambiguous, multi-workstream, assurance-relevant, or otherwise ineligible work. It follows approved context, discovery, planning, TDD, graph, review, status, and budget rules as applicable.

## Hard full triggers

Authentication/authorization; security or privacy; data/schema/API contracts; dependencies; migrations; permissions; accessibility behavior; external side effects; integrations or external systems; multiple workstreams or ownership areas; destructive or hard-to-recover actions; consequential product or architecture choices; unresolved ambiguity; conflicting leases; unavailable or non-deterministic verification; failed focused verification; and any material scope growth force `full-harness`.

## Promotion

Before every additional edit, compare discovered scope with the chosen lane. Stop fast-route edits and promote to `full-harness` when a hard trigger, broader impact, ownership conflict, ambiguity, or failed check appears. Preserve the current working tree and report what was discovered; do not manufacture fast-route evidence or silently continue.
