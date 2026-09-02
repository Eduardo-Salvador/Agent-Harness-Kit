# Request routing

Run this playbook before mutating work or entering Harness ceremony. Read-only audits, explanations, status inspections, and diagnosis do not trigger first-run; route them directly to bounded inspection. Its purpose is to spend less effort classifying a request than completing it. After selecting a lane, independently choose `assurance: none|light|full` using [adaptive execution](../../docs/ADAPTIVE-EXECUTION.md).

## Route in order

1. Read the request and only the nearest scoped instruction needed to classify it. Do not preload project context, pending state, the graph, or repository-wide evidence.
2. Apply user precedence: explicit full always wins. Otherwise honor the requested lane unless a real full-Harness condition is present.
3. Choose `direct-trivial`, `vibe`, `graph-only`, or `full-harness` deterministically. Automatically select full only for two or more real agents/independent contexts, a human decision loop, a required audit, a model too weak or uncertain for the work, unresolved consequential ambiguity, or explicit full. With assurance auto, actual security/privacy/authorization/destructive changes default to full assurance; honor explicit none/light with a warning unless approved authority mandates audit. API/dependency words alone decide neither lane nor assurance.
4. Only when two or more lanes remain plausible, use an available economical AI classifier. Give it the request, lane definitions, full-Harness conditions, and nearest scoped evidence only. It advises classification; it does not change model, authority, or execution context.
5. If AI classification would cost as much as the work, inspect the target directly. Use `full-harness` only if consequential ambiguity remains.
6. Select assurance independently: `none` for executor verification, `light` for focused independent acceptance, or `full` for required audit/deep assurance.

## Execute the lane

### Direct-trivial

Inspect the target and nearest rules, make the mechanical edit, run the smallest useful check when one exists, and return a concise closeout. Create no Harness artifacts or intermediate status ceremony.

### Vibe

Confirm one working context, a decided result, low blast radius, and a focused deterministic check. Vibe may change small local behavior without mandatory RED, but never skips verification. Failed verification begins bounded recovery and does not alone change the lane.

Create no feature brief, implementation plan, TASK/SPEC, task graph node, lease artifact, TDD evidence, handoff, review, request-route record, or full status artifact. Report the changed behavior and focused check concisely. A check that is missing, ambiguous, or failing promotes the work; it is never treated as success.

### Graph-only

Enter the normal approved-context and graph workflow. Use this lane only when scheduling/ownership coordination is useful and the task satisfies the graph-only evidence profile. Run its declared deterministic verification and record the concise result in the graph transition.

### Full-harness

Choose the compact shape for a bounded decided outcome: minimum durable state, a small graph neighborhood, and a compact inline spec where sufficient. Choose the complete shape when discovery, a human decision loop, multiple coordinated agents/workstreams, material uncertainty, or required full audit needs the complete state chain. Full Harness does not require every artifact.

## Continuous promotion check

After target inspection, re-evaluate coordination and assurance. Failed verification begins bounded technical recovery within current scope. Promote if recovery exposes unresolved consequential ambiguity, a human loop, required audit, insufficient model capability, multiple real agents, or an actual security/privacy/authorization/destructive boundary. Never use an API or dependency keyword as a proxy for those facts.
