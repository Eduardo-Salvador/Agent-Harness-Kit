# Claude Code native adapter

Claude Code natively loads root `CLAUDE.md`. This kit uses the documented `@AGENTS.md` import so Claude and Codex converge on one neutral policy map, then adds only Claude-specific routing to `.claude/skills/` and `.claude/agents/`.

## Native mapping

| Neutral operation | Claude Code surface | Safe fallback |
| --- | --- | --- |
| Session guidance | `CLAUDE.md` importing root `AGENTS.md` | Load the shared map explicitly |
| Essential workflow | Relevant `.claude/skills/*/SKILL.md` | Follow the linked neutral playbook directly |
| Bounded delegation | Explicit `.claude/agents/*.md` definitions | Run sequentially in the main context while preserving reviewer independence |
| Tool execution | Tools allowed by the selected agent and current permission system | Mark unavailable or approval-required |
| Hooks and MCP | Existing, reviewed project configuration | Do not create `.claude/settings.json` or `.mcp.json` automatically |

At session start, apply the imported first-run/status gate. For resume or status, read project context, pending-work authority, and task graph in that order before any broad scan. Missing or unapproved `harness-state/PROJECT-CONTEXT.md` means discovery precedes implementation planning. Native skills and agents translate execution; canonical context, graph, decisions, rules, capability evidence, and handoffs remain in neutral paths.

Apply [bounded review rounds](../docs/REVIEW-ROUNDS.md) to the main context and every delegated subagent. The orchestrator may dispatch one initial independent review and at most one focused re-review; an exhausted budget requires escalation, decomposition, rewrite, or human decision, never a third unchanged loop.

Discovery records actual tools, skills, agents, MCP/connectors, scripts, hooks, and integrations. Presence does not establish installation, authentication, secret access, network access, or authorization.

For mature repositories, preserve existing `CLAUDE.md`, `.claude/`, `.mcp.json`, and generated `.claude/worktrees/` according to the migration classifications. Generated worktree material is evidence or an exclusion, never silently promoted to canonical state. Cutover or deletion requires human semantic-equivalence review and separate authorization.

## Capability-tier mapping

The neutral policy lives in [capability-based model routing](../docs/MODEL-ROUTING.md). At dispatch, map `economical`, `balanced`, and `frontier` to the low-cost, balanced, and highest-capability Claude families actually available in the current host. Use current aliases or approved full identifiers and record the resolved model as execution evidence, not durable policy.

If the required tier is unavailable, use another available model at the same tier or block visibly. Never silently downgrade or infer additional tool, file, network, secret, integration, or publication authority from model choice.
