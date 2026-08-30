# Contract: Feature brief

`harness.feature-brief/v1` records an approved product direction between project context and technical decomposition. Store instances under `harness-state/features/`.

## Lifecycle

- `draft`: exploration is active; no technical graph mutation is authorized by the brief.
- `approved`: the named human approved the selected direction and acceptance boundary.
- `superseded`: a later revision replaces this one while preserving its provenance.

## Invariants

- The brief pins an approved project-context revision.
- Known project facts are referenced, not rediscovered through a second first-run interview.
- Options and tradeoffs are visible before selection; the recommendation is not approval.
- Intended/excluded actors, access and permission boundaries, scope, non-goals, outcome, success signal, happy/alternate/failure/recovery journeys, data lifecycle, constraints, risks, deferred cases, and testable acceptance criteria are explicit when relevant.
- The completeness analysis is relevance-based, not an exhaustive questionnaire. A relevant unresolved branch keeps the brief in `draft`; an intentional deferral names its impact.
- Open questions have owners and resolution boundaries; no consequential unresolved question survives approval.
- `PENDING.md` and `TASK-GRAPH.md` remain unchanged until approval. After approval, pending owns macro product outcomes and the graph owns technical execution.
- Graph nodes link to the exact approved feature-brief revision.

Use [the canonical template](../../harness/templates/FEATURE-BRIEF.md) and [feature-discovery playbook](../../harness/playbooks/feature-discovery.md).
