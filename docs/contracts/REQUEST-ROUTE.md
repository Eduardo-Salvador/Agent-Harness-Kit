# Request route contract

`harness.request-route/v1` is the neutral classification contract applied before first-run discovery, resume/status loading, feature discovery, planning, graph creation, TDD, review, or full status ceremony.

## Fields

```yaml
schema: harness.request-route/v1
route: direct-trivial | vibe | graph-only | full-harness
assurance: none | light | full
harness_shape: none | compact | complete
classification: deterministic | ai-ambiguity | fallback
user_override: none | direct-trivial | vibe | graph-only | full-harness
risk_signals: []
coordination_signals: []
warnings: []
reason: <short decision>
verification: <smallest meaningful check or planned harness verification>
promotion_trigger: <condition that requires reclassification before further edits>
```

The record is conceptual for `direct-trivial` and `vibe`: those routes create no durable route file. The template exists for adapters, tests, and integrations that need to exchange a route decision; full Harness workflows may persist the decision in their normal task authority instead of creating a second artifact.

## Decision precedence

1. A user request for `full-harness` always wins.
2. Two or more real execution agents/contexts, a human decision or approval loop, required audit, a model too weak/materially uncertain for the work, unresolved consequential ambiguity, or explicit full selects `full-harness`.
3. Otherwise, honor an explicit user lane override when that lane's eligibility rules pass.
4. Otherwise, apply deterministic rules first. Use an available economical classifier only when the request remains genuinely ambiguous and classification costs less than doing the work.
5. If consequential ambiguity remains unresolved or the classifier is unavailable, select `full-harness` because a human decision loop is now required.

`fallback` means the deterministic preflight exposed ambiguity but no economical classifier resolved it on that surface; `full-harness` is therefore the safe lane. It is never a fifth route.

No route may invent credentials, call a separate AI provider, hardcode a model ID, or claim a silent model switch in an already-running context.

## Lanes

- `direct-trivial`: one decided, localized presentation/static-content or equally mechanical value edit; no product behavior, interaction/state, contract, data, dependency, accessibility behavior, risk, or cross-workstream impact. It creates no Harness artifacts and runs the smallest useful check when one exists.
- `vibe`: one decided, small local change, including limited observable behavior, within one workstream and ownership area. It has a clear target, low blast radius, and a focused deterministic check. It creates no feature brief, plan, task, graph, TDD evidence, handoff, review, route, or full status artifact.
- `graph-only`: deterministic, low-risk technical work that needs graph scheduling or ownership coordination and satisfies the existing `evidence_profile: graph-only` contract. It is a real graph task and records only its checked transition.
- `full-harness`: work that needs real multi-context coordination, a human loop, required audit, model-risk compensation, or resolution of consequential ambiguity. `compact` keeps only essential shared state; `complete` adds transfer/review artifacts only for their real consumers.

## Orthogonal assurance

Risk does not automatically inflate the lane. With `assurance: auto`, contract, schema, dependency, migration, integration, accessibility, and external-effect signals recommend or select stronger assurance while retaining the appropriate lane. An explicit `none|light|full` is honored with a visible warning when below the recommendation, except where an approved project/user rule requires an audit. Actual authentication/authorization, security/privacy, and destructive boundaries require full audit.

## Promotion

Before every additional edit, compare discovered scope with the chosen lane, assurance, and shape. Reclassify when a full-Harness condition appears; otherwise raise only the assurance or shape actually needed. Preserve the current working tree and report what was discovered.
