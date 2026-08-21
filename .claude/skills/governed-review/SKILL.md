---
name: governed-review
description: Perform independent acceptance review and governed integration using objective evidence.
---

# Governed review

Follow `../../../harness/playbooks/review-integration.md` and the task's `review_profile`/`max_review_rounds`. Round 1 is proportional to risk; round 2 is focused on prior blockers, the correction delta, and proportional regressions. Only evidence-backed acceptance, security/privacy/data, contract, required-runtime, ownership, or material-regression violations may block. Record optional improvements as follow-ups. Never request round 3 on the unchanged task contract. Use an independent context, verify routing and coherent change boundaries, and never silently expand authority.
