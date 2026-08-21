# Capability-based model routing

Model routing chooses the least costly capability tier that can safely satisfy a task. It is a dispatch decision, not a permission decision and not a ranking of people or providers.

## Tiers

| Tier | Use by default for | Do not use when |
| --- | --- | --- |
| `economical` | Narrow mechanical transformations with deterministic expected output and cheap verification | Judgment, ambiguity, security impact, product tradeoffs, or unclear acceptance is present |
| `balanced` | Bounded implementation, tests, fixtures, documentation, repository inspection, and remediation against accepted contracts | Cross-domain ambiguity, consequential risk, conflicting contracts, or repeated failure is present |
| `frontier` | Architecture, security/privacy judgment, brainstorming, difficult integration, high-risk review, harness evolution, and recovery after repeated failure | The work can be decomposed into a smaller judgment-heavy parent and deterministic children |

Balanced is the normal default. Economical is an optimization for work that is both narrow and objectively checkable. Frontier is reserved for the smallest context that genuinely needs deeper judgment.

## Escalation triggers

Escalate before continuing when any of these becomes true:

- risk, ambiguity, or cross-domain coupling grows beyond the task contract;
- acceptance cannot be made deterministic;
- security, privacy, data-loss, architecture, or product tradeoffs become consequential;
- source contracts conflict or integration requires semantic reconciliation;
- two bounded attempts at the current tier fail for materially similar reasons.

After decomposition, deterministic child tasks may return to balanced or economical. Never silently route below a required tier because a named model is unavailable.

## Provider boundary

Canonical artifacts store tiers and reasons, not model names. Each adapter maps tiers to models actually available in the current host. A mapping is evidence about availability, latency, cost, and capability at that time; it is not permanent product policy.

## Dispatch and handoff

Every task records `model_tier` and `model_reason`. The handoff records `model_tier_used` and `model_route_changes`, including why an escalation or decomposition occurred. Reviewers check that a lower tier did not bypass a trigger.

## Context efficiency

Route the smallest sufficient context with the selected model: pinned task, direct dependencies, applicable rules, required capability evidence, acceptance criteria, and relevant prior attempts. Do not reload the full repository or entire graph into every child. Reconcile graph and pending state at material lifecycle transitions rather than every commentary event.

## Authority boundary

Model selection never grants file, secret, network, commit, integration, push, deployment, publication, or product authority. It does not remove isolation, independent review, verification, or human checkpoints.

This policy was promoted from the Dioli Confeitaria pilot after the project demonstrated that strong control and review can coexist with cheaper default execution when escalation boundaries are explicit.
