# Playbook: First run

This neutral policy is evaluated whenever the harness is added to or resumed in a host project. Codex reaches it through root `AGENTS.md`; Claude Code reaches the same rule through root `CLAUDE.md` importing `@AGENTS.md`. Both entrypoints may coexist and share neutral state, so no runtime platform guess or manual profile switch is required.

In a mature host, do not copy over an existing entrypoint or native extension directory. Use namespaced coexistence and migration classification before proposing a merge or cutover.

## Initialization test

1. Look for `harness-state/PROJECT-CONTEXT.md` in the host-project root. Templates and examples do not count.
2. Treat the project as uninitialized when the file is absent, unreadable, not `harness.project-context/v1`, not `approved`, or contradicted by material repository evidence.
3. If initialized, pin its revision and continue to graph reconciliation. If not, do not plan or dispatch implementation.

## Adaptive initialization

At the user's request, briefly explain in plain language what the harness is, why discovery runs before planning, what artifacts/checkpoints will be created, and what the user will approve. This optional explanation may happen before or during discovery, never blocks delivery, and grants no project-learning consent/observation/retention/publication or Learning Pack activation.

1. Discovery interviewer inventories files and classifies the host as `greenfield`, `existing`, or `uncertain`, with evidence.
2. If existing harness material is mature, switch to the [mature adoption playbook](mature-harness-adoption.md), record a discovery snapshot, and preserve originals.
3. Pre-fill known context; ask only questions that close consequential gaps or conflicts.
4. Record product, architecture, scope, permission, and publication choices as decision proposals for human confirmation.
5. Ask the user to select exactly one runtime mode:
   - `delivery` — Development Core only;
   - `delivery+learning` — the same core plus consented project-specific learning.
6. If `delivery+learning` is selected, create/approve the learning profile. Installing `core-learning` never performs this activation. The Harness Engineering Learning Pack is a separate study resource and is never a mode.
7. Revalidate discovery snapshot identities and selector expansion immediately before approval.
8. Obtain explicit approval of project context and consequential decisions.
9. Only then decompose work, validate the initial graph, and create briefs for ready nodes.

## Resume behavior

An existing approved context avoids a repeated interview. Reopen only conflicting or newly consequential fields, explain why, and create a new revision. Messages announce the resulting artifact changes.
