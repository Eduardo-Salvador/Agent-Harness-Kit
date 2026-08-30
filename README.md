# Agent Harness Kit

![Agent Harness Kit — context, tasks, checks, shipped](docs/assets/agent-harness-kit-banner.svg)

<p align="center">
  <strong>Give coding agents durable context, bounded execution, and a clear path to completion.</strong><br>
  Platform-neutral contracts with native entrypoints for Codex and Claude Code.
</p>

<p align="center">
  <img alt="Version 0.6.0" src="https://img.shields.io/badge/version-0.6.0-4967ff">
  <img alt="Python 3.10 or newer" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&amp;logoColor=white">
  <img alt="Install with uv, pipx, or pip" src="https://img.shields.io/badge/installer-uv%20%7C%20pipx%20%7C%20pip-DE5FE9">
  <img alt="Codex compatible" src="https://img.shields.io/badge/agent-Codex-11131a">
  <img alt="Claude Code compatible" src="https://img.shields.io/badge/agent-Claude_Code-D97757">
  <img alt="MIT License" src="https://img.shields.io/badge/license-MIT-ffb84d">
</p>

<p align="center">
  <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="#start-here">Start here</a> · <a href="#choose-your-pace">Modes</a> · <a href="docs/ARCHITECTURE.md">Architecture</a>
</p>

**Source version: `0.6.0`.** The Kit is an executable, artifact-driven scaffold. It has no unattended background daemon and does not lock the operating system. While an orchestrator agent is active, it can safely launch independent ready subtasks in parallel when the host proves that capability.

## Start here

Open any terminal, including the integrated terminal in VS Code, and install the CLI once. [`uv`](https://docs.astral.sh/uv/) is the recommended isolated option:

```bash
uv tool install agent-harness-kit-cli
```

You can also use `pipx` or install directly from PyPI with `pip`:

```bash
pipx install agent-harness-kit-cli
python -m pip install agent-harness-kit-cli
```

On Windows, `py -m pip install agent-harness-kit-cli` is also supported. Prefer a virtual environment when using plain `pip`; `uv` and `pipx` isolate the CLI automatically.

Then open the project you want to organize and run:

```bash
agent-harness install
```

Open a **new agent context at the project root**. The Kit will introduce itself, inspect only the initial state it needs, and begin a short discovery before proposing implementation.

> Prefer to preview first? Run `agent-harness install --dry-run`. Existing root instructions are preserved through managed blocks and namespaced coexistence.

## Choose your pace

| Say this | What happens |
| --- | --- |
| “Use standard delivery” | Full discovery where needed, bounded implementation, checks, and independent assurance |
| “Use hackathon mode” | At most two cohesive discovery questions, then a demo-first graph aimed at a testable MVP |
| “I also want to learn” | Adds guided learning only after you approve the exact Markdown, Obsidian, Notion/MCP, or other note destination |

Hackathon mode keeps state, file leases, checks, and status, but uses light review by default and cuts secondary scope before the primary demo path.

## Prefer to listen?

Listen to a short English explanation of what the project does and how its workflow fits together.

https://github.com/user-attachments/assets/1affd407-4d32-4f66-8386-0bdc3666df2e

[Download the English MP3](media/agent-harness-kit-overview-en.mp3) · [Read the English script](media/overview-script-en.txt)

## Why it exists

| Without durable coordination | With the Kit |
| --- | --- |
| The agent rescans and guesses context | Approved context is read before broad inspection |
| Human decisions mix with technical tasks | `PENDING.md` and `TASK-GRAPH.md` have separate authority |
| Reviews repeat indefinitely or echo the implementer | A fresh reviewer context judges the SPEC once, with at most one focused re-review |
| Completion waits for ceremonial approval | Passing work is completed, reported, and advances |
| Multiple agents collide | Workstreams, ownership leases, and handoffs are explicit |
| Independent work waits in a single-file queue | The active orchestrator fills proven parallel capacity, then refills the first freed slot |
| A tiny CSS/copy edit triggers the whole harness | `direct-trivial` edits go straight to the file, with no interview, SPEC, graph, TDD, or review |
| Study notes land in arbitrary folders | Learning starts only after the destination is approved |
| New feature ideas jump straight into code | Automatic feature discovery compares directions and records an approved brief first |
| Vague tasks make agents improvise and rescan | Non-trivial work gets one concise writing plan and small executable task specs |
| Tests are added only after implementation | Behavior tasks prove RED first, reach GREEN minimally, then run proportional regression |

## What changes in your project

- `PROJECT-CONTEXT.md` records the approved product, constraints, mode, and important decisions.
- `FEATURE-*.md` closes product behavior gaps; `PLAN-*.md` decomposes approved non-trivial work without becoming another file per task.
- `PENDING.md` answers what still needs a human and what remains unfinished at product level.
- `TASK-GRAPH.md` owns technical order, dependencies, leases, progress, and the next ready work; each `TASK.md` is a self-contained executable spec.
- `CODEX-AGENT-DISPATCH.md` proves which dynamic Codex agent was created, with which role, bounded context, model/reasoning, returned context, and adapter response.
- Root `AGENTS.md` and `CLAUDE.md` route capable agents into the same platform-neutral rules contained in `agent-harness-kit/`.

Frontend, backend, data, infrastructure, integration, and learning use separate contexts when the host supports them. Every active node can declare a focused `read_set`, exclusive `write_set`, related `impact_set`, and source revision, reducing broad rescans without inventing a second graph.

## The working loop

Not every change enters the loop. A clearly localized presentation or static-content edit—such as changing one button color, spacing value, typo, or label—uses the `direct-trivial` fast path when it has no logic, state, rule, contract, data, dependency, accessibility behavior, or risk. The agent edits it directly, runs the smallest useful check, and reports briefly. If inspection reveals real behavior or broader impact, it promotes the work before changing code.

1. The agent reads approved context, then human/macro pending work, then the technical graph.
2. A new feature with open product choices automatically enters a focused brainstorm: known context is reused, credible options are compared, and you approve a feature brief before the graph changes.
3. Approved non-trivial work becomes one writing plan with independently checkable units targeting roughly two to five minutes; truly simple work keeps only a compact inline spec.
4. In Codex, the native dispatcher selects the neutral role, builds only the scoped context packet, resolves model/reasoning, and creates a fresh executable subagent with `fork_turns: none`. It records the returned identity/context/response; without subagents, implementation degrades explicitly to sequential execution while review still requires a separate fresh context. The agent then executes its self-contained SPEC without inventing missing behavior. Code follows RED → GREEN → REFACTOR; a contradiction or invalid RED returns to planning.
5. When two or more collision-free nodes are ready and the host reports numeric capacity, the orchestrator reserves distinct leases and contexts, launches the whole safe batch without waiting between launches, then refills a slot after the first completion or attention event. Dependent branches join through an explicit integration node.
6. Passing work is completed and reported immediately; the next ready task can start without ceremonial approval.
7. After verification, the orchestrator launches an independent reviewer in a fresh context—preferably a subagent when supported. It receives the versioned SPEC, relevant diff, handoff, and test evidence, reconstructs acceptance before reading the code, and never relies on the original prompt or implementer memory. Assurance stays non-blocking: one proportional review and, only for a real blocker, at most one focused re-review. There is no third loop.

For graph-managed work, every progress update includes stage, progress, work continuing automatically, human and technical pending items, blockers, next action, and inspectable paths. `direct-trivial` returns only a short edit/check summary.

## Profiles

| Profile | Includes | Best for |
| --- | --- | --- |
| `core` | Delivery, graph, status, review, validation | Most projects |
| `core-learning` | `core` plus optional project learning | Guided practice and debriefs |
| `full` | `core-learning` plus the separate harness study pack | Studying harness engineering itself |

Learning support is never silently activated. The user chooses the exact Markdown path, Obsidian location, Notion target/MCP, or another destination before any note is created.

## New project or existing harness

In an empty project, discovery comes before stack, architecture, branding, or feature proposals. In a mature repository, the Kit preserves existing instructions and uses namespaced coexistence; it never silently overwrites `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, or another authority. See the [mature-adoption playbook](harness/playbooks/mature-harness-adoption.md).

## Honest boundaries

- The Kit does not run unattended or open user-visible chats by itself. During an active orchestration session it can launch supported internal subagents/tasks in parallel; merge, deploy, publication, and visible task creation still require their own capability and authority.
- Leases are validated contracts, not OS-level locks.
- Threads, subagents, worktrees, MCPs, network, and model choice depend on the host's real capabilities and authorization. When automatic routing is explicitly approved and the host exposes overrides, dispatch applies the resolved model/reasoning values and records adapter confirmation; otherwise the route is visibly manual or blocked.
- A knowledge graph can reduce broad scans, but only scoped queries and execution budgets prevent waste; no tool guarantees lower token usage. See the [scoped graph execution contract](docs/SCOPED-GRAPH-EXECUTION.md) for the `read_set`, `write_set`, `impact_set`, provenance, and Graphify boundaries.

Need more detail? Read the [step-by-step installation guide](docs/EMBEDDED-INSTALLATION.md), [hackathon mode](docs/HACKATHON-MODE.md), [architecture](docs/ARCHITECTURE.md), [validation contract](docs/VALIDATION.md), [publication readiness audit](docs/PUBLICATION-READINESS.md), and [MIT License](LICENSE).
