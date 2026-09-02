---
name: request-router
description: Automatically classify every request before Harness ceremony into direct-trivial, vibe, graph-only, or full-harness using deterministic rules first and AI only for genuine ambiguity.
---

# Request router

1. Before mutating work or Harness ceremony, read `../../../harness/playbooks/request-routing.md` and `../../../docs/ADAPTIVE-EXECUTION.md`. Read-only audit/diagnosis does not trigger first-run.
2. Explicit full wins. Otherwise use full for two or more real agents, a human loop, required audit, insufficient model capability, or unresolved consequential ambiguity. Actual security/privacy/authorization/destructive changes require full audit; API/dependency keywords alone are not triggers.
3. Classify deterministically first. Use an available economical AI classifier only when ambiguity remains and classification is cheaper than the work. Do not call a separate provider, invent credentials, hardcode a model ID, or claim a silent model switch.
4. Route to exactly one lane and independently assign `assurance: none|light|full`. Unresolved consequential ambiguity selects `full-harness`; ordinary uncertainty may be resolved by bounded inspection.
5. For `vibe`, permit a small local behavior change in one workstream with no Harness artifacts or mandatory RED, but require a focused deterministic check.
6. Re-evaluate scope before further edits. Failed verification starts bounded in-scope recovery; promote only when a full-Harness condition is discovered.
