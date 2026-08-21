# Contract: Capability manifest

The capability manifest records what a host/project actually exposes. “Tools/capabilities” includes platform-native tools, MCP servers/connectors, skills, scripts/commands, hooks, and external integrations.

Each entry records ID, kind, purpose, provider/source, state (`available`, `degraded`, `unavailable`, `optional`, or `approval-required`), scopes, authentication/secret/network needs, side effects, evidence, fallback, and approving authority. Discovery never treats presence in documentation as installation, authentication, access, or authorization.

## Invariants

- Default to unavailable or approval-required when evidence is missing.
- Never store secrets; record only the secret boundary/provider.
- Consequential tool, permission, secret, network, destructive-action, hook, or integration changes require explicit human approval and validation.
- Task briefs request capabilities by ID and state; adapters recheck them before dispatch.
