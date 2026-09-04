# Discovery interview

## Goal

Turn an initial idea into an approved [project context](contracts/PROJECT-CONTEXT.md), explicit [decisions](contracts/DECISION.md), an optimized [implementation plan](contracts/IMPLEMENTATION-PLAN.md) when work is non-trivial, and a valid initial [task graph](contracts/TASK-GRAPH.md)—without making the user repeat facts already present in the repository or prior approved artifacts.

This interview is the mandatory first-run behavior when `harness-state/PROJECT-CONTEXT.md` is absent or not approved. Codex reaches it through root `AGENTS.md`; Claude Code reaches the same rule through root `CLAUDE.md` importing `@AGENTS.md`. Both may be present, and both use the same neutral context and graph without runtime guessing or profile switching. The interview identifies whether the host project is greenfield, existing, or uncertain; selects standard delivery (accompanied by default), autonomous delivery, or the compressed hackathon variant, with optional learning when requested; and completes before implementation planning. See the executable [first-run playbook](../harness/playbooks/first-run.md).

## Delivery choice

Offer [accompanied, autonomous, and hackathon](DELIVERY-MODES.md) as three simple presets. Accompanied is the default; autonomous completes an upfront-approved envelope without optional intermediate client evaluations; hackathon prioritizes a timeboxed demo and first-demo evaluation. Ask any unanswered mode preference in the first cohesive kickoff question alongside missing product intent; include the result in consolidated context approval rather than a separate questionnaire. A greeting-only first message also triggers this welcome and question when context is uninitialized. Preserve existing choices and learning consent on resume. No preset skips verification or grants unspecified scope.

## Operating loop

1. **Inspect first:** read available project files, existing decisions, constraints, and capability declarations.
2. **Build an evidence map:** classify each required field as known, inferred, conflicting, or unknown and retain its source.
3. **Snapshot evidence:** record selector expansion, source identities, revision, and time before interpreting a mature existing harness.
4. **Ask the highest-leverage question:** prefer one cohesive question at a time; bundle only tightly related low-risk facts.
5. **Reflect and update:** briefly state the interpreted answer, update the draft artifact, and identify what uncertainty it resolved.
6. **Adapt:** skip answered branches; deepen only where risk, ambiguity, or inconsistency remains.
7. **Checkpoint:** revalidate the snapshot, then pause for explicit approval at consequential choices.
8. **Close:** show a concise summary and unresolved non-blockers before context approval. Then apply writing plans and present only consequential plan/topology choices; ordinary spec-driven decomposition does not add ceremonial approval.

Questions should use the user's vocabulary and offer concrete tradeoffs when useful. The interview must not force a fixed questionnaire or ask the user to reconfirm unchanged approved facts.

### Hackathon compression

When the user asks for a hackathon, time-boxed MVP, or demo-first build, follow [hackathon mode](HACKATHON-MODE.md). Ask at most two cohesive discovery questions before presenting the draft context and demo-first graph unless consequential safety or authority is missing. Establish the audience, deadline, single visible outcome, must-have path, supplied assets, hard constraints, demo runtime, smallest credible checks, acceptable labeled shortcuts, and explicit post-MVP scope. Record non-blocking unknowns as assumptions instead of extending the interview.

## First-response handshake

For an uninitialized project, the first response identifies that Agent Harness Kit is active, explains briefly that it organizes project context, pending work, and verifiable execution, says discovery establishes context before implementation planning, mentions that the user may choose standard delivery (accompanied by default), autonomous end-to-end delivery, or the faster hackathon mode for a time-boxed MVP/demo, and asks the highest-leverage unanswered question immediately. The welcome is localized to the user's language, at most two short sentences, and is not marketing copy or a separate approval checkpoint.

For an empty or effectively empty greenfield directory, the first question asks what the user wants to create, for whom, what problem/value it addresses, and what the first successful outcome is. The same kickoff question asks the delivery-mode preference when unanswered; if the mode is already explicit, acknowledge it instead. The visible kit-active welcome must precede the question. The agent does not first invent or recommend product scope, features, visual direction, architecture, stack, implementation steps, or a task graph. When the initial user request already answers some of those fields, reflect and pre-fill them, then ask only for the consequential gap.

The handshake is a first-response firewall. Before it is sent, the agent does not answer the substantive request, scan broadly, recommend, or output a proposal, plan, status, or graph. It contains exactly one discovery question. A pre-send check replaces any draft that includes a recommendation or a second question. Model memory, summaries, and prior conversations are unverified and cannot establish company facts, brand direction, product scope, technical decisions, or approval; only the current user message and approved project artifacts can do so.

## Architecture, folders, and coding conventions

After intent is known, the interviewer resolves the project's technical shape adaptively rather than presenting a generic questionnaire:

1. Read approved context and inspect existing structure, manifests, framework markers, formatter/linter configuration, tests, and scoped rules.
2. If architecture and folder organization are already approved and current evidence agrees, reuse them without another question.
3. If an existing repository clearly expresses them, preserve that shape by default, record the inference and evidence, and ask only for correction or consolidated approval.
4. If either is missing or ambiguous, let the user describe it, select from two or three relevant directions with tradeoffs, or ask the agent to recommend one. A recommendation is recorded as proposed until explicitly approved.
5. Coding conventions are optional. Existing rules win; when none exist, the user may state preferences, approve normal stack defaults, or choose no additional convention.

Architecture and folder organization must be resolved before project-context approval. The three fields reopen only for conflicting evidence or an explicit user change. Hackathon mode may bundle them into one cohesive project-shape question within its two-question limit.

“Recorded” means persisted in a draft artifact with an inspectable path and revision. The interviewer never says it registered a briefing mentally. When a briefing is already available, it writes or updates the draft `harness-state/PROJECT-CONTEXT.md`, cites that draft, and keeps its status unapproved until the human checkpoint.

## Optional onboarding explanation

The user may request a plain-language explanation before or during discovery. Explain the harness purpose, why approved context precedes implementation planning, the artifacts/checkpoints that will be created, and the expected next steps. This is an optional onboarding aid, not a prerequisite or delivery node. It cannot block delivery and does not activate `delivery+learning`, learning consent, observation, retention, publication, or the separate Harness Engineering Learning Pack.

The explanation should mention the active native entrypoint in plain language while making clear that both platform files can coexist and route to one core. It must not imply that entrypoint detection installs or authorizes tools, MCP, hooks, network, secrets, or other capabilities.

## Coverage model

Use [accompanied delivery](ACCOMPANIED-DELIVERY.md) for product builds: establish meaningful client evaluation milestones in the consolidated context, unless continuous delivery is explicitly chosen. Include relevant customer/niche, concrete desired and undesired results, and failure/recovery examples; a list of features alone is not an acceptance oracle. Reuse prior answers and preserve the hackathon question limit.

Discovery should establish, to the degree relevant:

- intended users, problem, value, and measurable outcomes;
- host-project state: greenfield, existing, or uncertain, with repository evidence;
- in-scope and out-of-scope behavior;
- functional slices and priority;
- architecture constraints, existing systems, and data boundaries;
- approved architecture, intended folder organization, and their repository or human evidence;
- quality attributes, security/privacy needs, and permission limits;
- delivery environment, verification commands, and definition of done;
- platform capabilities and acceptable degradation;
- native platform tools, MCP servers/connectors, skills, scripts/commands, hooks, and external integrations, including evidence and `available`/`degraded`/`unavailable`/`optional`/`approval-required` state; never assume installation, authentication, secrets, network, or authorization;
- user-defined business rules, security/privacy constraints, architectural invariants, coding conventions, and path-scoped rules, indexed in a rules map materialized through the [runtime template catalog](../harness/TEMPLATES.md), with authority, scope, precedence, approval, and validation;
- optional coding conventions, recorded as detected, user-specified, stack-defaults-approved, or none rather than silently invented;
- project-specific domains and whether existing roles suffice; when they do not, proposed specialist responsibilities, least tool access, progressive context packet, ownership boundary, independent reviewer, and verification criteria;
- known risks, assumptions, dependencies, and open questions;
- whether automatic model routing is enabled, disabled, or pending, with the current host catalog/override evidence stored in `harness-state/MODEL-ROUTING.md`; include it in consolidated context approval rather than adding a ceremonial question;
- delivery mode and, when the user requests study/learning in plain language, learning goals, observation consent, and an exact note destination with format, capability state, retention, and write/publication policy.
- for hackathon delivery: timebox, demo audience/environment, primary visible path, acceptable labeled shortcuts, and post-MVP exclusions.

Role customization is governed discovery output, never silent agent self-modification. Consequential authority/tool expansion requires a human decision, and customization cannot remove orchestrator/reviewer independence, least capability, exclusive ownership, verification, checkpoints, or learning non-interference.

Durable rules are human-approved/versioned and routed only to relevant roles/tasks through progressive disclosure. Temporary task context stays task-local. Mature adoption preserves existing project/platform rules and provenance. Consequential changes to tools, permissions, secrets, network, destructive actions, hooks, integrations, or durable rules require explicit human approval and validation.

Unknown facts are acceptable when marked with an owner and resolution condition. Hidden assumptions are not.

## Non-repetition rules

- Do not ask when a current approved artifact supplies the answer.
- When repository evidence is strong but unapproved, present it as an inference and ask only for correction/approval.
- When sources conflict, cite the conflict and ask a discriminating question.
- Track asked questions and resolved fields in the working session so rephrasing does not create duplicates.
- Reopen an answer only when new evidence conflicts, the user changes it, or a dependent decision requires more precision; explain why.

## Human checkpoints

Create a [decision](contracts/DECISION.md) and require explicit approval before:

- committing to product goals, users, or success measures;
- choosing or materially changing architecture, public APIs, data ownership, or security posture;
- adding/removing major scope, moving deadlines/budgets, or accepting significant risk;
- requesting elevated credentials or irreversible/destructive operations;
- overriding failed verification or independent review;
- enabling the learning layer's observation scope or publishing learning content externally.

Low-risk wording, decomposition, and reversible implementation details may proceed under recorded policy.

## Stopping criteria

Stop asking discovery questions when all are true:

1. every required project-context field is approved or explicitly marked `unknown` with owner and resolution plan;
2. no unresolved conflict blocks the first delivery slice;
3. success criteria are testable enough to create acceptance criteria;
4. architecture and folder organization are approved, and optional coding conventions have an explicit disposition;
5. platform and permission constraints are known enough to choose safe isolation and verification;
6. non-simple implementation has a ready writing plan; every graph node has a complete executable task spec and targets a bounded unit;
7. the initial graph is acyclic, traceable to outcomes, and has at least one ready node;
8. consequential decisions have explicit human dispositions;
9. the user approves the context revision and only consequential graph/topology choices;
10. the discovery snapshot still matches every expanded selector and source identity; drift forces refresh before approval.

More questions are not inherently better. Stop when additional answers would not change safe initial execution.

## Exact outputs

Discovery produces:

1. one approved `PROJECT-CONTEXT.md` instance with provenance, assumptions, unknowns, constraints, outcomes, and mode;
2. one `DECISION.md` instance for each consequential choice, including rejected alternatives;
3. one ready `IMPLEMENTATION-PLAN.md` for non-simple work; simple work records its classification only in the task spec;
4. one initial `TASK-GRAPH.md` instance with dependencies, ownership proposals, acceptance summaries, and checkpoint nodes;
5. one complete executable `TASK.md` spec for every node that is initially `ready`;
6. when project-specific roles are needed, bounded role proposals/bindings with responsibilities, capabilities, context, ownership, reviewer, criteria, and approval status;
7. one capability manifest and one rules map (or approved references to existing equivalents), with unavailable/optional/approval-required states and scoped routing;
8. when learning is enabled, one consented `LEARNING-PROFILE.md` instance; otherwise none;
9. a short discovery closeout message that points to those files and announces approval/state changes only.

The interview does not generate platform-specific agents or silently configure integrations.
