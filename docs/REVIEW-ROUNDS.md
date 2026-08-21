# Bounded review rounds

Every implementation task receives independent review, but review depth and repetition are proportional to risk. The default budget is two rounds total: one initial review and, only when blocking findings exist, one focused re-review.

## Profiles

| Profile | Suitable work | Initial review |
| --- | --- | --- |
| `light` | Narrow, low-risk, deterministic change with objective checks | Inspect diff, acceptance evidence, declared checks, ownership, and obvious regression risk |
| `standard` | Normal bounded implementation | Evaluate every acceptance criterion, relevant diff, verification, risks, and integration boundary |
| `critical` | Security/privacy/data, architecture, destructive behavior, release-critical or high-impact integration | Standard scope plus domain-specific risk evidence and required human checkpoints; it does not add automatic reviewer rounds |

The task brief records `review_profile` and `max_review_rounds`. The maximum supported automatic budget is `2`.

## Verdicts

- `accept`: all acceptance criteria pass and no blocking finding remains.
- `changes-requested`: at least one blocking finding proves a violation of acceptance, security/privacy/data policy, contract, required runtime behavior, ownership, or a material regression.
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

If round 2 still returns `changes-requested`, stop the loop. The orchestrator marks the task blocked and chooses one of these explicit paths:

- escalate to the frontier model tier for diagnosis/integration;
- decompose or rewrite the task/acceptance contract;
- request a human decision for a genuine product/risk conflict;
- create a new bounded task after the cause and ownership are understood.

Do not create a third review attempt on the same unchanged task contract. Human authority may approve a new plan, but it does not turn blind repetition into a review strategy.
