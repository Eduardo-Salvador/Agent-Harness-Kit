# Portability

## Generic guarantees

The platform-neutral core guarantees stable artifact schemas and lifecycle semantics, dependency and ownership rules, explicit approvals, evidence-based completion, reconstructable state, and learning non-interference. A platform adapter may change how a capability is performed, not what these guarantees mean.

No canonical state may exist only in a vendor directory, proprietary conversation, or platform-only database. Vendor directories may contain thin configuration that points back to neutral contracts.

In a mature host, existing vendor/root instructions may remain authoritative. Adapters bind them through [provenance](contracts/ADAPTER-BINDING.md) and [coexistence](contracts/COEXISTENCE.md); they do not overwrite them. Generated worktrees/build outputs are inventory/exclusion candidates, and secret-bearing paths are recorded without copying values.

## Capability negotiation

At startup, an adapter reports a versioned manifest for capabilities such as:

- repository read/write and path scoping;
- branch/worktree creation or ephemeral environment provisioning;
- command execution and timeout/cancellation;
- independent agent/session invocation;
- lifecycle hooks/events;
- approval requests and secure secret access;
- durable artifact storage and source-control metadata.

The orchestrator compares task requirements with this manifest before assignment. Capability state is `available`, `degraded`, `unavailable`, `optional`, or `approval-required`, with a human-readable reason. Inventory includes native platform tools, MCP servers/connectors, skills, scripts/commands, hooks, and external integrations; discovery never assumes installation, authentication, secrets, network, or authorization.

## Degradation policy

Degradation must be explicit and preserve safety:

| Preferred capability | Acceptable declared fallback | Never acceptable |
| --- | --- | --- |
| Worktree or ephemeral environment | Serialized branch/directory execution with exclusive ownership | Concurrent writers in the same paths |
| Native lifecycle hook | Core event log plus periodic reconciliation | Losing canonical state transitions |
| Separate reviewer session | Serialized fresh-context reviewer with distinct role identity | Implementer self-approval |
| Secure secret broker | Human-mediated, scoped environment injection | Secret in Markdown artifacts |
| Push/event notification | Receiver scans versioned artifact status | State only in chat message |

If no safe fallback exists, the task becomes explicitly blocked and names the missing capability. Adapters must not emulate evidence they cannot produce.

## Adapter contract

Every platform adapter must:

1. detect and report capabilities without side effects;
2. translate neutral operations and lifecycle events;
3. enforce declared path, command, network, and permission scopes;
4. return structured outcomes and durable evidence references;
5. expose degradation before scheduling;
6. avoid embedding core orchestration policy;
7. pass shared contract and end-to-end fixtures.
8. preserve existing authority/provenance and surface snapshot drift during namespaced adoption.

## Codex adapter responsibilities

Codex natively reads root `AGENTS.md` before work and discovers repository skills under `.agents/skills/`. The shipped entrypoint applies the shared first-run gate and loads only the relevant workflow skill. Actual isolation, delegation, approvals, tool execution, MCP, and lifecycle capabilities are still discovered and recorded; the adapter never assumes them. Project context, graph state, tasks, decisions, rules, capability evidence, and handoffs remain in neutral paths.

## Claude adapter responsibilities

Claude Code natively reads root `CLAUDE.md`; the shipped file imports `@AGENTS.md` and adds only Claude-specific routing to `.claude/skills/` and bounded `.claude/agents/`. It uses the same first-run gate and neutral state as Codex. Hooks, settings, MCP, isolation, network, and other capabilities are discovered rather than enabled. Claude-specific files remain thin and cannot become the canonical task graph or memory store.

Both entrypoints coexist in every profile. No runtime detection selects between them: each installed tool reads its own documented entrypoint. Opening the same repository with Codex and Claude Code at different times therefore preserves one authority and one state model, subject to mature-host coexistence rules.

## Source control and non-Git environments

Versioned Git files are the preferred durable implementation. The contracts also allow a versioned artifact store with atomic revisions when Git is unavailable. The store must preserve history, stable IDs, expected-revision writes, and auditable authorship; otherwise the first executable version should stop as unsupported.

## Destination and integration adapters

Markdown is the baseline learning export. Obsidian is a filesystem convention over Markdown. Notion, MCP servers, CI systems, and other services are optional adapters with explicit credentials and approval boundaries. Integration failure cannot corrupt or block the delivery graph unless the delivery task explicitly depends on that integration.

## Cross-platform conformance

Codex and Claude adapters must run the same fixtures for graph readiness, overlapping ownership rejection, stale revision rejection, checkpoint blocking, verification admission, recovery after interruption, visible degradation, and learning non-interference. Platform-specific tests may be added but cannot replace shared conformance.

Structural validation verifies both native entrypoint trees, their convergence on the neutral core, safe capability defaults, profile inclusion, and mature-host collision policy. It does not claim an installed Codex or Claude Code binary was exercised. The [generic adapter](../adapters/generic.md) remains the capability envelope, and unsupported runtime operations degrade explicitly.
