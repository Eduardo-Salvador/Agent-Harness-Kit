<!-- agent-harness-kit:begin -->
# STOP: Agent Harness Kit mandatory context-routing gate

Before any scan, proposal, plan, status, or file change:

Also apply this gate before answering a greeting-only first message such as "oi", "hello", or "hi". A greeting is not an exemption from onboarding. If context is approved, greet briefly without repeating the welcome or mode question. Read-only audits/explanations and eligible fast edits retain their existing routing exceptions.

1. Read `agent-harness-kit/AGENTS.md`.
2. Check root `harness-state/PROJECT-CONTEXT.md`.
3. If context uses `schema: harness.project-context/v1` and `status: approved`, do not emit the first-run welcome or start a discovery interview. Follow the Harness status/resume read order and answer the project request from approved durable state; do not continue into the uninitialized branch below.
4. Otherwise, if context is absent, unreadable, conflicting, stale, or not approved, stop. Do not answer the substantive project request, propose a solution, or perform a broad scan. Start the first-run discovery interview automatically.
5. Only in that uninitialized branch, the mandatory first response is restricted to, in the user's language:
   - begin the visible response with a welcome saying Agent Harness Kit is active; do not skip this sentence even if the discovery questions are correct;
   - explain briefly that it organizes project context, pending work, and verifiable execution;
   - offer standard delivery (accompanied, the default), autonomous end-to-end delivery, or the faster hackathon mode for a time-boxed MVP/demo;
   - say discovery comes before proposals or implementation;
   - ask exactly one cohesive kickoff question that asks for the delivery-mode preference and, only if unknown, the project idea/intended outcome. If the user already selected a mode, acknowledge it and ask only the highest-leverage unanswered intent question.
6. Do not include recommendations, product scope, company facts, branding, colors, features, design, architecture, stack, implementation, plan, status, or graph in that response. Facts explicitly supplied in the current user message may be acknowledged only as unapproved inputs.
7. Treat model memory and prior conversations as unverified. They are not project facts unless the current user message or an approved project artifact supplies them.
8. Never claim information was “registered mentally.” Only call it recorded when a draft artifact was written, and cite its path/revision.
9. Before sending, self-check: if the uninitialized response omits the kit-active welcome or the unanswered mode choice, contains a proposal, or contains more than one discovery question, replace it with the restricted handshake above. Welcome, mode choice, and discovery are one response, not separate turns.

Project instructions outside this managed block remain authoritative. Stop for human resolution when authorities conflict.
<!-- agent-harness-kit:end -->
