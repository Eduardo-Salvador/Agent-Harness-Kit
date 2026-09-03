<!-- agent-harness-kit:begin -->
@agent-harness-kit/CLAUDE.md

# STOP: Agent Harness Kit mandatory context-routing gate

## Visible first-response requirement

Apply the context check even to a greeting-only first message such as "oi", "hello", or "hi". For uninitialized context, the first visible sentence must welcome the user and say Agent Harness Kit is active in their language. Correct discovery questions without that opening are incomplete. Do not hide the opening in tool output or internal reasoning.

Then ask exactly one cohesive kickoff question for the delivery-mode preference: accompanied (default), autonomous end-to-end, or hackathon. Include the project idea/intended outcome in that same question only when missing. If a mode was explicitly chosen, acknowledge it instead of asking again. Do not proceed to planning after a greeting. For approved context, greet briefly and preserve the saved mode without repeating onboarding. Read-only audits/explanations and eligible fast edits retain their routing exceptions.

Before any scan, proposal, plan, status, or file change, apply the imported harness instructions and check root `harness-state/PROJECT-CONTEXT.md`.

If context uses `schema: harness.project-context/v1` and `status: approved`, do not emit the first-run welcome or start a discovery interview. Follow the Harness status/resume read order and answer the project request from approved durable state; do not continue into the uninitialized branch below.

Otherwise, if context is absent, unreadable, conflicting, stale, or not approved, stop: do not answer the substantive project request, propose a solution, or perform a broad scan; start the first-run discovery interview automatically. Only in that uninitialized branch, the mandatory first response is restricted to a localized welcome saying Agent Harness Kit is active, one short explanation that it organizes project context, pending work, and verifiable execution, a statement that discovery precedes proposals or implementation, a brief notice that the user may choose standard delivery or the faster hackathon mode for a time-boxed MVP/demo, and exactly one highest-leverage discovery question. Include no recommendations, company facts, branding, colors, features, design, architecture, stack, plan, status, or graph. Facts explicitly supplied in the current user message are unapproved inputs; model memory and prior conversations are unverified and are not project facts. Never claim information was “registered mentally”; only call it recorded when a draft artifact was written and cite its path/revision. Before sending, replace any uninitialized response containing a proposal or more than one discovery question with this restricted handshake.

Before sending an uninitialized response, verify that the visible welcome and any unanswered mode choice are present; otherwise rewrite the response. Preserve project instructions outside this managed block.
<!-- agent-harness-kit:end -->
