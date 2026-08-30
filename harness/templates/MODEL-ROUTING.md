---
schema: harness.model-routing/v1
id: model-routing
revision: 1
status: draft
default_tier: balanced
updated_at: 2000-01-01T00:00:00Z
approved_by: pending
decision: pending
---

# Model routing

## Tiers

| Tier | Default use | Exclusions |
| --- | --- | --- |
| economical | Narrow mechanical work with deterministic output | Judgment, risk, ambiguity, or unclear checks |
| balanced | Bounded implementation, tests, docs, inspection, and accepted-contract remediation | Frontier triggers below |
| frontier | Architecture, security/privacy, product tradeoffs, difficult integration/review, harness evolution, and repeated failure | Decompose deterministic children when practical |

## Escalation triggers

- Consequential risk or ambiguity.
- Cross-domain or conflicting-contract integration.
- Acceptance cannot be deterministic.
- Two materially similar failed attempts at the current tier.

## Adapter mappings

| Adapter | Economical model / effort | Balanced model / effort | Frontier model / effort | Override surfaces | Evidence/date |
| --- | --- | --- | --- | --- | --- |
| replace | replace / replace | replace / replace | replace / replace | replace | replace |

## Dispatch record

- Every task records `model_tier` and `model_reason`.
- Before activation, every task pins a resolved `harness.model-dispatch/v1` record with selected model, supported effort, override surface, returned context reference, and adapter evidence.
- Every handoff records the tier/model/effort actually used and any route changes.
- A tier annotation without confirmed runtime override remains advisory; never silently accept the host default.

## Context efficiency

- Pass only pinned task, direct dependencies, applicable rules, capability evidence, acceptance criteria, and relevant prior attempts.
- Reconcile graph and pending state at material transitions.

## Authority boundary

- Model routing grants no additional permission and removes no review, verification, isolation, or human gate.
