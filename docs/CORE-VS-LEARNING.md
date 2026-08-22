# Shared core, project learning, and harness study

## One core, two modes

There is one delivery graph, one orchestrator, one set of task contracts, and one verification path. `delivery+learning` activates project-specific observers around that same core; it is not a fork, alternate prompt stack, or duplicate harness.

The Harness Engineering Learning Pack (`learning-pack/README.md` in the `full` profile) is static, project-independent study material. It is not a runtime mode, owns no project state, and is excluded from operational context unless explicitly requested.

## Boundary

| Shared delivery core (required) | Project-specific learning layer (optional) |
| --- | --- |
| Discovery of project intent and constraints | Explicit knowledge/self-assessment |
| Approved project context and decisions | Learning goals and calibrated profile |
| Dependency graph and scheduling | Learning queue derived from real work |
| Ownership, isolation, implementation | Guided practice outside critical delivery work |
| Independent review and verification | Feedback on reasoning and demonstrated seniority |
| Handoffs and durable operational state | Debriefs and destination adapters |

Delivery review judges the software and acceptance evidence. Learning review discusses the user's reasoning and growth. The two verdicts are never conflated.

## Activation rules

Learning is active only when all are true:

1. the user explicitly selects `delivery+learning`;
2. a [learning profile](contracts/LEARNING-PROFILE.md) exists with consent and visibility settings;
3. the selected learning activities do not require an unavailable or unapproved capability;
4. any external publication destination has separate human approval.

Distribution is not activation: installing `core-learning` or `full` creates no consent, observation scope, retention policy, or publication permission. Until a user approves an active learning profile, project learning remains off.

An explicit request to study or learn through the current project is the trigger to configure that profile, even when the user does not say `delivery+learning`. The agent asks only for missing goals, observation boundaries, and the note destination. That destination may be repository Markdown, a user-approved local path, an Obsidian vault/folder, a Notion page/database, or another named system. Exact location, format, capability evidence, retention, and write/publication policy become durable project-learning context; credentials do not.

If any condition stops being true, learning pauses while delivery continues. The user can disable it at any time; disabling requires no migration of delivery state.

## Allowed inputs and outputs

The learning observer may read approved project context, task briefs, user-authored reasoning, handoffs, reviews, and verification summaries within its consent boundary. It may write only learning-owned artifacts: profile, queue items, exercises, reasoning feedback, and debrief drafts.

It may recommend a delivery-graph change by creating a proposal addressed to the orchestrator. That proposal has no effect until processed under ordinary graph and checkpoint rules.

## Non-interference guarantees

1. Learning roles have no direct write authority over `TASK-GRAPH`, task status, ownership, acceptance criteria, verification results, or delivery decisions.
2. A learning failure, unavailable note adapter, or unanswered exercise cannot block a delivery node.
3. Learning priorities cannot reorder delivery priorities or consume delivery budget without explicit approval.
4. Learning context is not injected into delivery agents unless the task explicitly requires it and the user approves disclosure.
5. Learning completion never counts as delivery verification; delivery completion never fabricates learning progress.
6. Private notes may be written under the exact destination policy approved in the active profile. Public sharing, a new destination, broader visibility, or consequential retention changes require fresh approval.
7. With learning disabled, delivery reads no learning artifacts. Removing the learning directory/adapter leaves all core contracts valid.

These guarantees should become automated conformance tests in Phase 2.

## Learning cycle

1. **Assess:** record confidence and evidence, not just self-ratings.
2. **Observe:** identify reasoning patterns from current work.
3. **Practice:** offer a bounded task or question, preferably off the delivery critical path.
4. **Review:** compare the user's reasoning with evidence and calibrate demonstrated level by skill area, never as a global label.
5. **Queue:** prioritize gaps by relevance, prerequisites, and user intent.
6. **Debrief:** summarize what changed, remaining uncertainty, and a next practice step.
7. **Retain or publish:** write private notes under the approved destination policy; use separate approval for public sharing or a changed destination/visibility boundary.

## Privacy and control

The profile declares what can be observed, retained, and exported. Sensitive project content should be referenced minimally or redacted from learning outputs. Destination credentials belong to adapters and secure platform storage, never contract files.
