# Feature discovery

Use this playbook after project context is approved and before technical decomposition when a request introduces a new product capability with unresolved consequential choices.

## Trigger boundary

Activate automatically when the user asks to brainstorm, ideate, explore, shape, or add a new feature, workflow, integration, or user-facing capability and no approved feature brief or equivalent acceptance contract resolves the product choices.

Do not activate for bug fixes, maintenance, refactors, dependency upgrades, implementation with approved scope/acceptance, or a `direct-trivial` copy/style/static-content edit. The fast path precedes project discovery and creates no feature artifact; otherwise missing/stale project context routes to first-run discovery.

## Flow

Discovery is progressive, not a one-time interview. Also activate when planning or expanding a graph exposes an unresolved feature boundary or completion condition, even without a new user feature request. An approved initial "build a system" brief does not authorize the agent to decide every later functionality. Explain the gap, ask one highest-leverage question, offer concrete examples/options and a recommendation, and obtain approval of the bounded functionality and its "complete only when" conditions before implementation. Reuse already approved details; do not restart onboarding or question every technical task.

Keep future outcomes at roadmap/macro level while only the next approved block receives executable task specs. A planned placeholder already in the graph remains pending/blocked with `scope_status: needs-discovery`; it must not be scheduled or activated. Record the exact human decision needed in `PENDING.md` when an existing node is blocked, but do not add new unapproved scope. After approval, pin the feature/decision revision, set `scope_status: approved`, and reconcile readiness under all other gates. Initial plan approval never counts as later client demonstration approval.

1. Read approved project context, relevant decisions, the pending authority, and only the graph neighborhood or source evidence needed to avoid repeating known facts.
2. State briefly that feature discovery is active before implementation. Reflect what is already known and ask one highest-leverage unanswered question at a time.
3. Run the feature-completeness analysis below. Resolve only consequential gaps, but do not omit a relevant branch merely because the user did not mention it.
4. When the problem is clear, present two to four credible directions. For each, name the user value, main tradeoff, important risk, and approximate scope. Recommend one direction and explain why it fits the approved project context.
5. Ask the user to select, revise, or reject the direction. Do not treat silence, enthusiasm, or permission to continue brainstorming as approval.
6. Write or revise `harness-state/features/FEATURE-<id>.md` from the feature brief template. Keep the artifact `draft` until the selected direction and acceptance boundary are explicitly approved.
7. On approval, mark the feature brief `approved` with its authority and exact project-context revision. If the user asked only to brainstorm, stop with the approved brief and a concise result; do not manufacture implementation work.
8. If planning or implementation was requested, reflect any new macro project outcome in `PENDING.md`, then run `writing-plans` before discovery-to-graph creates technical nodes linked to the approved feature brief. Preserve the pending/graph authority split.

## Feature-completeness analysis

Build a small decision map for the feature and ask about unresolved branches one high-leverage question at a time:

- **People and access:** intended users, excluded users, roles, eligibility, permissions, ownership, and approval boundaries.
- **Entry and identity:** how a user reaches or activates the feature; onboarding, authentication, verification, account linking, and session behavior when relevant.
- **Journeys:** trigger, happy path, alternate valid paths, cancellation or abandonment, empty state, repeat use, and completion.
- **Failure and recovery:** invalid input, unavailable dependency/provider, timeout, conflict or duplicate state, retry/idempotency, forgotten credentials, and support/manual recovery when relevant.
- **Data and integrations:** required inputs, source of truth, validation, storage, retention/deletion, synchronization, notifications, and external capability/authentication.
- **Quality and risk:** privacy, security, abuse, accessibility, compatibility, performance or volume, observability, rollout/rollback, and consequential business rules.
- **Closure:** explicit scope and non-goals, measurable success, testable acceptance outcomes, and intentionally deferred cases.

This is a relevance filter, not a questionnaire to recite. For a login feature, the decision map might expose email/password versus Google, verification, forgotten-password recovery, duplicate identities, provider outage, session expiry/logout, and role access. For a simple export feature, most identity branches may already be inherited and need no new question.

The feature remains `draft` if a consequential branch has no chosen behavior, named owner, or explicit deferral. An intentional deferral belongs in non-goals or risks with its impact visible; it must not disappear when the graph is created.

## Efficient questioning

- Never replay the first-run welcome or ask the user to repeat approved product facts.
- Prefer repository evidence and a confirmation over an open-ended question when evidence is strong.
- If the request already supplies every material decision, summarize the proposed brief and ask one approval question instead of running an interview.
- A question may group tightly related choices, but do not send a questionnaire dump.
- In hackathon mode, ask at most two cohesive feature questions, propose a primary demo path, and cut secondary scope before graph creation.

## Routing after approval

A feature brief is product authority, not a technical plan. UI direction may next route through `frontend-screen`; architecture and integration choices use their applicable decision gates; graph execution begins only from approved acceptance boundaries. New evidence that materially changes the feature returns the brief to `draft` or creates a superseding revision.
