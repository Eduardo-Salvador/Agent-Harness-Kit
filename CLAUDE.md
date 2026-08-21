@AGENTS.md

# Claude Code routing

Claude Code loads this file and imports the shared operational map above. For a task, load only the relevant `.claude/skills/*/SKILL.md`, an explicitly delegated `.claude/agents/*.md` role when useful, and [the Claude adapter](adapters/claude.md). All project context, graph, decisions, rules, capability evidence, and handoffs remain in the shared neutral paths defined by `AGENTS.md`.

Every Claude main agent and subagent follows the imported [bounded review policy](docs/REVIEW-ROUNDS.md): one initial review, at most one focused re-review, and no third unchanged review loop.

Do not assume or enable hooks, MCP servers, settings, network, secrets, destructive permissions, or integrations. Propose consequential capability changes through discovery and obtain explicit human approval. Existing Claude/Codex/custom instructions use the mature-adoption process; never overwrite them blindly.
