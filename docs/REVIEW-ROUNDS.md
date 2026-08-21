# Bounded review rounds

Every completed implementation task receives automatic independent assurance, but review depth and repetition are proportional to risk. Completion is based on declared acceptance checks and an orchestrator transition; review does not require human approval, does not hold the completed node, and does not stop unrelated ready work. The default budget is two rounds total: one initial review and, only when blocking findings exist, one focused remediation review.

## Profiles

| Profile | Suitable work | Initial review |
| --- | --- | --- |
| `light` | Narrow, low-risk, deterministic change with objective checks | Inspect diff, acceptance evidence, declared checks, ownership, and obvious regression risk |
| `standard` | Normal bounded implementation | Evaluate every acceptance criterion, relevant diff, verification, risks, and integration boundary |
| `critical` | Security/privacy/data, architecture, destructive behavior, release-critical or high-impact integration | Standard scope plus domain-specific risk evidence; it may gate the affected integration/release action but does not add automatic rounds or human approval without a genuine decision boundary |

The task brief records `review_profile` and `max_review_rounds`. The maximum supported automatic budget is `2`.

## Verdicts

- `accept`: assurance found no blocking violation.
- `changes-requested`: at least one blocking finding proves a violation of acceptance, security/privacy/data policy, contract, required runtime behavior, ownership, or a material regression. Create a linked remediation task; do not reopen the historical completed node.
- `blocked`: required evidence, capability, dependency, or decision is unavailable. Resolve the blocker without creating an implementation attempt unless the candidate changes.

Style preferences, optional hardening, speculative improvements, naming taste, and cosmetic suggestions are non-blocking unless an approved rule or acceptance criterion makes them mandatory. Record them as follow-up candidates; do not hold acceptance.

## Focused re-review

Round 2 reviews only:

1. findings that blocked round 1;
2. the delta created to resolve them;
3. regression checks proportionate to that delta;
4. newly introduced blocking defects visible in the changed scope.

Do not repeat a repository-wide audit, reload unrelated context, or reopen criteria that passed unless the correction could materially invalidate them.

## Exhausted budget

If round 2 still returns `changes-requested`, stop the loop. The orchestrator blocks the remediation or affected integration path—not the completed historical node or unrelated execution—and chooses one of these explicit paths:

- rewrite the task/acceptance contract;
- decompose the work into new bounded tasks;
- request a human decision for a genuine product/risk conflict;

A frontier model may assist diagnosis for one of those paths, but model escalation is not a fourth disposition and never authorizes another review round. A new task may be created only as the product of rewrite or decomposition after cause and ownership are understood.

Do not create a third review attempt on the same unchanged task contract. Human authority may approve a new plan, but it does not turn blind repetition into a review strategy.
