---
name: governed-review
description: Use for independent acceptance review, objective verification, and governed integration of a completed task.
---

# Governed review

Follow `../../../harness/playbooks/review-integration.md` and the completed task's `review_profile`/`max_review_rounds`. Assurance is automatic and non-blocking: never request human approval, reopen the historical completed node, or stop unrelated ready work. Round 1 is proportional to risk; round 2 focuses on linked remediation, prior blockers, the correction delta, and proportional regressions. Only evidence-backed acceptance, security/privacy/data, contract, required-runtime, ownership, or material-regression violations create remediation. Record optional improvements as follow-ups. Never request round 3. Review independently and do not expand commit/integration/push/deploy/publication authority.
