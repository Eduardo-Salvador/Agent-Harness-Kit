# Embedded installation

The recommended contained layout installs one generated profile under `agent-harness-kit/` in the host repository. The host's root entrypoints contain only small managed bridges. This keeps Kit files replaceable without treating the Kit as the owner of the host repository.

```text
host-project/
├── AGENTS.md
├── CLAUDE.md
├── agent-harness-kit/
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── harness/
│   ├── adapters/
│   └── tools/
└── harness-state/
```

`agent-harness-kit/` contains the selected, versioned distribution. `harness-state/` contains host-owned context, decisions, pending work, graph state, tasks, handoffs, and reviews. Keeping state outside the installed distribution prevents a Kit update from replacing project history.

## Installation

Downloading or cloning the Kit does not modify a host project. Run the bundled installer to create the contained directory and bridges:

```text
python tools/install.py --profile core --host <host-project> --dry-run
python tools/install.py --profile core --host <host-project>
```

Substitute `core-learning` or `full` when needed. From a generated profile, the selected profile must match that package. The installer preflights the complete operation, refuses an existing `agent-harness-kit/`, rejects malformed or duplicated bridge markers, verifies packaged hashes, preserves root entrypoint content and line endings, stages the distribution before making it visible, and rolls back bridge writes if installation fails. It never creates `harness-state/`, installs hooks, touches root extension directories, or enables services.

After installation:

1. Inspect root `AGENTS.md` and `CLAUDE.md`; existing content remains outside one managed block.
2. Ask the active agent to read the root entrypoint. The bridge routes it to the embedded Kit, which applies first-run or status/resume behavior.
3. Run the embedded validator from the host root with `python agent-harness-kit/tools/validate.py`.

Manual installation remains available: copy the complete generated profile to `agent-harness-kit/`, then add exactly one block from the [AGENTS bridge template](../harness/templates/ROOT-AGENTS-BRIDGE.md) and [Claude bridge template](../harness/templates/ROOT-CLAUDE-BRIDGE.md), preserving all surrounding content.

If a root entrypoint does not exist, create it with only the applicable bridge block. If it already exists, add one block without rewriting surrounding project instructions. Do not duplicate the block on later updates.

## Authority and coexistence

The bridge does not silently grant the embedded Kit precedence over existing project instructions. Existing authorities remain in force until the project records precedence and, for a mature harness, completes semantic review and separate cutover authorization.

Use `harness-adoption/` for migration evidence when the host already has material harness behavior. Follow the [mature adoption playbook](../harness/playbooks/mature-harness-adoption.md) rather than using the bridge as an automatic conversion.

## Native capability boundary

Some hosts discover native extensions only from root `.agents/` or `.claude/` directories. The bridge makes the embedded policy and neutral playbooks readable, but it does not prove that nested skills or subagents are automatically registered.

Discovery must record each native extension as `available`, `degraded`, `unavailable`, or `approval-required`. When automatic discovery is unavailable, the agent follows the neutral playbooks by explicit path. Promoting selected native extensions to root remains a separate, reviewed migration step; the embedded installation never overwrites root extension directories.

## Updates

1. Record the installed Kit version and current bridge path.
2. Preserve `harness-state/`, `harness-adoption/`, and all existing root instructions.
3. Replace only `agent-harness-kit/` with the reviewed new profile.
4. Update a root bridge only when its managed path or contract changes.
5. Re-run validation and review migration notes before operational cutover to a breaking version.

The embedded layout does not install hooks, MCP servers, credentials, settings, network access, or external integrations.
