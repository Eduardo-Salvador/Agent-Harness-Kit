# Playbook: First run

This neutral policy is evaluated whenever the harness is added to or resumed in a host project. Codex reaches it through root `AGENTS.md`; Claude Code reaches the same rule through root `CLAUDE.md` importing `@AGENTS.md`. Both entrypoints may coexist and share neutral state, so no runtime platform guess or manual profile switch is required.

In a mature host, do not copy over an existing entrypoint or native extension directory. Use namespaced coexistence and migration classification before proposing a merge or cutover.

## Initialization test

1. Look for `harness-state/PROJECT-CONTEXT.md` in the host-project root. Templates and examples do not count.
2. Treat the project as uninitialized when the file is absent, unreadable, not `harness.project-context/v1`, not `approved`, or contradicted by material repository evidence.
3. If initialized, pin its revision and continue to graph reconciliation. If not, do not plan or dispatch implementation.

## Adaptive initialization

At the user's request, briefly explain in plain language what the harness is, why discovery runs before planning, what artifacts/checkpoints will be created, and what the user will approve. This optional explanation may happen before or during discovery, never blocks delivery, and grants no project-learning consent/observation/retention/publication or Learning Pack activation.

### First-response handshake

When the project is uninitialized, the first user-facing response must make activation visible and begin discovery in the same message:

1. Give a brief, natural welcome that says Agent Harness Kit is active for this project and explains what it does in one short sentence: it organizes project context, pending work, and verifiable execution.
2. State that a short discovery will establish the project context before implementation planning.
3. Reflect any useful facts already present in the user's request or repository so the user does not repeat them.
4. Ask the highest-leverage unanswered discovery question immediately.

This is a first-response firewall, not a preference. Until the handshake is sent, do not answer the substantive project request, recommend anything, perform a broad repository scan, or emit a proposal, plan, status, or graph. Restrict the response to the welcome/explanation, the discovery-before-proposals statement, and exactly one discovery question. Before sending, self-check that it contains no recommendation and no second question; if it does, replace it with the restricted handshake.

Treat model memory, summaries, and prior conversations as unverified inputs. They do not establish company facts, brand direction, product scope, technical choices, or approval unless the current user message states them or an approved project artifact records them. Facts in the current message may be acknowledged as unapproved inputs, not silently promoted to decisions.

If an initial briefing exists, pre-fill `harness-state/PROJECT-CONTEXT.md` as a draft before saying the briefing was recorded, then cite its path and revision. Never say information was “registered mentally” or otherwise imply durable storage when no artifact write occurred. The draft is not approval and grants no implementation authority.

For an empty or effectively empty greenfield directory, do not propose a product, company description, brand or color direction, feature list, design, architecture, stack, implementation plan, or task graph before the user supplies intent. Start with one compact question covering the product/idea, intended user, problem or value, and first success outcome. Ask delivery versus guided-learning mode in a later turn unless the user already answered the primary discovery question. A detailed initial brief is evidence to pre-fill, not a reason to skip the handshake or repeat answered facts.

Keep the welcome to at most two short sentences before the question. Do not turn it into marketing copy, a long harness explanation, or an approval gate.

Localize the wording to the user's language. A suitable opening is: “Welcome — Agent Harness Kit is active. It organizes project context, pending work, and verifiable execution; before implementation, I will run a short discovery.” Follow it immediately with the first discovery question; do not repeat this fixed wording after initialization.

1. Discovery interviewer inventories files and classifies the host as `greenfield`, `existing`, or `uncertain`, with evidence.
2. If existing harness material is mature, switch to the [mature adoption playbook](mature-harness-adoption.md), record a discovery snapshot, and preserve originals.
3. Pre-fill known context; ask only questions that close consequential gaps or conflicts.
4. Record product, architecture, scope, permission, and publication choices as decision proposals for human confirmation.
5. Ask the user to select exactly one runtime mode. A plain-language request to study, learn through the project, receive guided practice, or keep learning notes selects configuration of `delivery+learning`; do not require the internal label:
   - `delivery` — Development Core only;
   - `delivery+learning` — the same core plus consented project-specific learning.
6. If `delivery+learning` is selected, follow `harness/playbooks/learning-capture-publication.md` when the extension is installed: ask only for missing goals, observation boundaries, and the exact note destination; verify local/Obsidian filesystem access or ask which Notion/other connector/MCP and target to use; then create and approve the learning profile. Never create notes or assume `docs/` or another fallback before that destination is confirmed. Installing `core-learning` never performs this activation. The Harness Engineering Learning Pack is a separate study resource and is never a mode.
7. Revalidate discovery snapshot identities and selector expansion immediately before approval.
8. Obtain explicit approval of project context and consequential decisions.
9. Create `harness-state/PENDING.md` from the approved context: human decisions/actions plus a macro project completion overview. Do not put technical order or dependencies there.
10. Only then decompose work into `harness-state/TASK-GRAPH.md`, validate the initial graph, and create briefs for ready nodes.

## Resume behavior

An existing approved context avoids a repeated interview. Reopen only conflicting or newly consequential fields, explain why, and create a new revision. Messages announce the resulting artifact changes.
