# Platform adapters

Adapters translate native platform conventions into one neutral core. They may describe how a platform loads instructions, skills, agents, tools, or configuration; they cannot change schemas, authority, graph semantics, checkpoints, rules, or learning non-interference.

| Adapter | First-version status |
| --- | --- |
| [Generic](generic.md) | Capability/degradation contract for any capable agent or human runner |
| [Codex](codex.md) | Native root `AGENTS.md` plus on-demand repository skills in `.agents/skills/` |
| [Claude Code](claude.md) | Native root `CLAUDE.md` importing `@AGENTS.md`, plus project skills and bounded subagents |

Every adapter reports each native tool, MCP server/connector, skill, script/command, hook, or external integration as `available`, `degraded`, `unavailable`, `optional`, or `approval-required`, with evidence and reason. It never assumes installation, authentication, secret access, network access, or authorization.

No live `.mcp.json`, `.claude/settings.json`, hook, credential, or global/user configuration ships with the kit. Mature hosts adopt native files through namespaced coexistence rather than blind overwrite.
