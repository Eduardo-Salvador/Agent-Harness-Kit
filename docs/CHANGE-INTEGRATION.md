# Coherent change and integration policy

The harness organizes changes by coherent delivery unit, not by elapsed time or number of microcorrections.

## Change unit

Related changes in one owned area that share acceptance and rollback boundaries should be validated and proposed as one coherent, reversible change. Obvious mechanical checks and review corrections should run before the first candidate commit whenever practical.

Split changes when a boundary is meaningful for ownership, independent deployment, dependency order, risk isolation, review scope, or rollback. Never combine unrelated areas merely to reduce commit count.

## Authority separation

A change plan does not authorize a commit. A commit does not authorize integration, push, deployment, or publication. Each action follows the project's approved capability and human-checkpoint policy. Force-push and history rewriting require separate explicit authority.

## Review behavior

Reviewers judge the complete delivery unit. A real defect found after a candidate commit may remain a separate corrective commit rather than rewriting shared or published history. Cosmetic microfixes that can safely be folded into the uncommitted candidate should not create artificial commit noise.

## Handoff record

The handoff names the coherent change unit, proposed split boundaries, and the current authority state for commit, integration, push, deployment, and publication. This makes technical completeness visible without implying publication permission.

This policy was promoted from the Dioli Confeitaria pilot, where one-commit-per-microfix behavior produced noise without improving review or rollback.
