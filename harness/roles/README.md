# Roles

Roles constrain authority; they are not personality prompts. These files are editable templates: discovery may adapt a role or propose a new project-specific specialist when the domain, verification surface, or ownership boundary requires it. Load exactly one primary role per task, plus project/task context.

Customization must define the specialist's purpose, responsibilities, permitted tools/capability states, progressive context packet, exclusive write set, acceptance/review criteria, escalation path, and exit conditions. Tools/capabilities include native platform tools, MCP servers/connectors, skills, scripts/commands, hooks, and external integrations. It is a proposal until approved under project policy. Consequential authority, permission, secret, network, destructive-action, hook, integration, or durable-rule expansion requires explicit human approval and validation; an agent cannot grant it to itself.

Project rules live in or are referenced by the rules map: business rules, security/privacy constraints, architectural invariants, coding conventions, and path-scoped rules. Route only applicable approved rules through progressive disclosure. Preserve existing project/platform rules during mature adoption and never promote temporary task context to a durable rule without human approval.

Every built-in or customized role must:

- treat versioned artifacts as canonical and messages as notifications;
- stay inside declared permissions, owned paths, and isolation;
- record uncertainty, blockers, and evidence;
- request a human decision at the checkpoints in [discovery](../../docs/DISCOVERY-INTERVIEW.md);
- never claim a capability or verification result it cannot prove.

The following invariants are not customizable away: orchestrator authority over graph state, implementer/reviewer independence, least capability, exclusive path ownership, objective verification, human checkpoints, and project-learning non-interference.

| Role | Owns | Must not own |
| --- | --- | --- |
| [Discovery interviewer](discovery-interviewer.md) | Evidence-led interview drafts | Approved decisions or delivery execution |
| [Orchestrator/PO](orchestrator-po.md) | Graph state, readiness, leases | Product approval or implementation verdicts |
| [Task decomposer](task-decomposer.md) | Proposed graph/task decomposition | Graph activation |
| [Generic specialist](generic-specialist.md) | Assigned implementation and handoff | Scope, graph status, self-acceptance |
| [Reviewer/integrator](reviewer-integrator.md) | Independent verdict and safe integration recommendation | Implementer identity or failed-check overrides |
| Learning assessor (`learning-assessor.md`, `core-learning`/`full`) | Consented evidence assessment and queue proposals | Delivery graph or global seniority labels |
| Learning debriefer/publisher (`learning-debriefer-publisher.md`, `core-learning`/`full`) | Debrief drafts and approved export | Delivery status or unapproved publication |
