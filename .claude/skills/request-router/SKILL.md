---
name: request-router
description: Automatically classify every request before Harness ceremony into direct-trivial, vibe, graph-only, or full-harness using deterministic rules first and AI only for genuine ambiguity.
---

# Request router

1. Before first-run, resume/status loading, discovery, planning, graph, TDD, review, or full status ceremony, read `../../../harness/playbooks/request-routing.md` and apply `../../../docs/contracts/REQUEST-ROUTE.md`.
2. Respect precedence: explicit full always wins; hard full triggers override every fast-lane request; otherwise honor a valid explicit lane override.
3. Classify deterministically first. Use an available economical AI classifier only when ambiguity remains and classification is cheaper than the work. Do not call a separate provider, invent credentials, hardcode a model ID, or claim a silent model switch.
4. Route to exactly one lane: `direct-trivial`, `vibe`, `graph-only`, or `full-harness`. Unresolved ambiguity falls back to `full-harness`.
5. For `vibe`, permit a small local behavior change in one workstream with no Harness artifacts or mandatory RED, but require a focused deterministic check.
6. Re-evaluate scope before further edits. Failed verification, broader impact, or any hard trigger stops the fast route and promotes to `full-harness`.
