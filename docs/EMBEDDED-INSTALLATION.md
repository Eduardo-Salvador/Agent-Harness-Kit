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

### Recommended: one command

Open a terminal inside the host project. This may be the integrated terminal in VS Code. Install the CLI with [`uv`](https://docs.astral.sh/uv/), then run the installer:

```text
uv tool install agent-harness-kit-cli
agent-harness install
```

The same PyPI package can be installed with `pipx` or plain `pip`:

```text
pipx install agent-harness-kit-cli
# or, preferably inside a virtual environment
python -m pip install agent-harness-kit-cli
agent-harness install
```

On Windows, `py -m pip install agent-harness-kit-cli` is equivalent. `uv` and `pipx` are preferred for a CLI because they isolate it from project dependencies automatically.

The current directory and `core` profile are defaults. Add `--dry-run` to preview, `--profile core-learning` for optional project-learning support, or pass another project path after `install`. The command still performs the same contained, preflighted installation described below; it only removes the clone-and-path ceremony. `agent-harness doctor` checks the expected entrypoints after installation, and `agent-harness prompt` prints the fallback activation prompt.

The distribution name is `agent-harness-kit-cli` because the shorter `agent-harness-kit` name is owned by an unrelated PyPI project. The installed commands are still `agent-harness` and `ahk`. To run directly from GitHub without a persistent tool installation, use `uvx --from git+https://github.com/Eduardo-Salvador/Agent-Harness-Kit.git agent-harness install`.

### Clone, fork, ZIP, or offline installation

Downloading or cloning the Kit does not modify a host project. Run the bundled installer to create the contained directory and bridges:

```text
workspace/
├── Agent-Harness-Kit/   source repository or fork
└── host-project/        destination; never the Kit source directory
```

From `host-project/` on Windows PowerShell:

```powershell
python ..\Agent-Harness-Kit\tools\install.py --profile core --host . --dry-run
python ..\Agent-Harness-Kit\tools\install.py --profile core --host .
```

From another directory layout, replace `..\Agent-Harness-Kit` with the actual source/fork path. On macOS or Linux use `/` separators and `python3`. The source/fork and host must remain different directories.

Alternatively, from the Kit source directory:

```text
python tools/install.py --profile core --host <host-project> --dry-run
python tools/install.py --profile core --host <host-project>
```

Substitute `core-learning` or `full` when needed. From a generated profile, the selected profile must match that package. The installer preflights the complete operation, refuses an existing `agent-harness-kit/`, rejects malformed or duplicated bridge markers, verifies packaged hashes, preserves root entrypoint content and line endings, stages the distribution before making it visible, and rolls back bridge writes if installation fails. It never creates `harness-state/`, installs hooks, touches root extension directories, or enables services.

After installation:

1. Inspect root `AGENTS.md` and `CLAUDE.md`; existing content remains outside one managed block.
2. Open a new agent context at the host-project root so the host reloads the root entrypoint. The bridge routes it to the embedded Kit, which applies first-run or status/resume behavior.
3. Run the embedded validator from the host root with `python agent-harness-kit/tools/validate.py`.

If the host does not load root instructions automatically, paste the same activation prompt printed by the installer:

```text
Agent Harness Kit is installed in this project. Before scanning, proposing, planning, reporting status, or changing files, read the applicable root AGENTS.md or CLAUDE.md, then follow the referenced instructions under agent-harness-kit/. Check harness-state/PROJECT-CONTEXT.md first: approved context resumes without a first-run welcome; only missing or unapproved context starts first-run discovery.
```

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
