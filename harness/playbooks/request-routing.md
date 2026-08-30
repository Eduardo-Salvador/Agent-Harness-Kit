# Request routing

Run this playbook before every Harness workflow, including the session-start/status gate. Its purpose is to spend less effort classifying a request than completing it while keeping consequential work inside the full Harness.

## Route in order

1. Read the request and only the nearest scoped instruction needed to classify it. Do not preload project context, pending state, the graph, or repository-wide evidence.
2. Apply user precedence: explicit full always wins; explicit fast-lane requests are honored only when no hard full trigger applies.
3. Apply deterministic rules from the [request-route contract](../../docs/contracts/REQUEST-ROUTE.md). Choose `direct-trivial`, `vibe`, `graph-only`, or `full-harness` when the evidence is clear.
4. Only when two or more lanes remain plausible, use an available economical AI classifier. Give it the request, lane definitions, hard triggers, and nearest scoped evidence only. It advises classification; it does not change model, authority, or execution context.
5. If AI classification would cost as much as the work, is unavailable, or leaves ambiguity, use `full-harness`.

## Execute the lane

### Direct-trivial

Inspect the target and nearest rules, make the mechanical edit, run the smallest useful check when one exists, and return a concise closeout. Create no Harness artifacts or intermediate status ceremony.

### Vibe

Confirm one workstream, one local ownership area, a decided result, low blast radius, no hard trigger, and a focused deterministic check. Make the smallest implementation directly. Vibe may change small local behavior without a mandatory RED phase, but it never skips focused verification.

Create no feature brief, implementation plan, TASK/SPEC, task graph node, lease artifact, TDD evidence, handoff, review, request-route record, or full status artifact. Report the changed behavior and focused check concisely. A check that is missing, ambiguous, or failing promotes the work; it is never treated as success.

### Graph-only

Enter the normal approved-context and graph workflow. Use this lane only when scheduling/ownership coordination is useful and the task satisfies the graph-only evidence profile. Run its declared deterministic verification and record the concise result in the graph transition.

### Full-harness

Enter the existing first-run/status/discovery/planning/graph/TDD/review flow at the applicable gate. `full-harness` is the safe fallback, not an error.

## Continuous promotion check

After target inspection and before each further edit, re-evaluate hard triggers. If scope grows beyond the chosen fast lane, stop editing, preserve current changes, state the promotion reason, and continue only through `full-harness`. Never demote a running full-harness task merely because one implementation step looks small.
