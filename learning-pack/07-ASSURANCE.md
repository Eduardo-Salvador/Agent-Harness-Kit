# Guardrails, verification, and human checkpoints

These mechanisms solve different problems:

- **Guardrails** constrain actions before or during execution: path scopes, denied network access, permission boundaries, and role authority.
- **Verification** tests claims against observable criteria: commands, fixtures, inspection evidence, and independent review.
- **Human checkpoints** reserve consequential judgment: product intent, architecture, scope, risky permissions, failed-check overrides, and external publication.

A guardrail cannot prove correctness. A passing check cannot grant permission. A human approval should not replace reproducible evidence when a check is available.

See the [generic adapter defaults](../adapters/generic.md), [review and integration playbook](../harness/playbooks/review-integration.md), and [decision template](../harness/templates/DECISION.md). The project-learning publication playbook shows all three: consent limits inputs, debrief evidence supports claims, and a human approves external publication.
