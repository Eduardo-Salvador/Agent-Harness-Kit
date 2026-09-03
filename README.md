# Agent Harness Kit

![Agent Harness Kit — context, tasks, checks, shipped](docs/assets/agent-harness-kit-banner.svg)

<p align="center">
  <strong>Give coding agents durable context, bounded execution, and a clear path to completion.</strong><br>
  Platform-neutral contracts with native entrypoints for Codex and Claude Code.
</p>

<p align="center">
  <img alt="Version 0.7.3" src="https://img.shields.io/badge/version-0.7.3-4967ff">
  <img alt="Python 3.10 or newer" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&amp;logoColor=white">
  <img alt="Install with uv, pipx, or pip" src="https://img.shields.io/badge/installer-uv%20%7C%20pipx%20%7C%20pip-DE5FE9">
  <img alt="Codex compatible" src="https://img.shields.io/badge/agent-Codex-11131a">
  <img alt="Claude Code compatible" src="https://img.shields.io/badge/agent-Claude_Code-D97757">
  <img alt="MIT License" src="https://img.shields.io/badge/license-MIT-ffb84d">
</p>

<p align="center">
  <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="#start-here">Start here</a> · <a href="#choose-your-delivery-mode">Modes</a> · <a href="docs/ARCHITECTURE.md">Architecture</a>
</p>

**Source version: `0.7.3`.** Choose accompanied delivery (default), autonomous end-to-end execution, or hackathon. All three keep explicit completion conditions, evidence, and scope/authority limits. A new read-only `delivery-mode` command previews their policies; the agent records the approved choice in project context.

> **A harness mature enough to know when to get out of the way.** Four execution lanes stay separate from `none|light|full` assurance. Failed checks trigger bounded recovery; full orchestration is reserved for real coordination, human governance, required audit, model insufficiency, or unresolved consequential ambiguity.

## Start here

Open any terminal, including the integrated terminal in VS Code, and install the CLI once. [`uv`](https://docs.astral.sh/uv/) is the recommended isolated option:

```bash
uv tool install agent-harness-kit-cli
```

Already installed? `uv tool install` does not upgrade an existing tool automatically. Run `uv tool upgrade agent-harness-kit-cli`, then confirm `agent-harness --version` before installing into another project.

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

The installation is immediately discoverable by supported agents. It creates the contained `agent-harness-kit/` directory **and** creates or updates these two files at the project root:

```text
your-project/
├── AGENTS.md          # Codex entrypoint
├── CLAUDE.md          # Claude Code entrypoint
└── agent-harness-kit/ # versioned Kit distribution
```

Existing root instructions are preserved outside a small managed bridge block. Run `agent-harness doctor` to verify all three entrypoints. Then open a **new agent context at the project root** so the host reloads `AGENTS.md` or `CLAUDE.md`; no activation prompt is required on hosts that load root instructions normally.

After installing, a simple **“hi”** in a fresh Codex or Claude Code context at the project root should trigger the welcome and a question about accompanied, autonomous, or hackathon delivery when project context is not yet approved. An initialized project keeps its saved mode and does not repeat onboarding. This depends on the host loading root instructions; `doctor` checks installation, not model obedience.

> Prefer to preview first? Run `agent-harness install --dry-run`. Existing root instructions are preserved through managed blocks and namespaced coexistence.

## What it actually does

Agent Harness Kit is a local execution-governance layer for coding agents. Codex or Claude still writes the software; the Kit determines how the work is scoped, ordered, verified, resumed, and—when the host supports it—dispatched across independent agents.

- `route` selects the lightest safe execution lane and an independent assurance level.
- `preflight` verifies declared files, scripts, environment names, commands, validator, browser/sandbox needs, and worker capacity before decomposition.
- Durable project context and graph state let a fresh conversation resume from current repository/runtime evidence instead of reconstructing work from chat history.
- First-run discovery reuses proven project decisions, resolves architecture and folder organization before planning, and asks about optional coding conventions only when the repository has not already established them. Users may specify a shape, choose from relevant options, or ask the agent to recommend one.
- Ownership leases and `schedule` select a maximum-size collision-free batch from ready graph nodes.
- `transition` advances graph state atomically and records hash-chained events; `metrics` reports ceremony, implementation, gate, review, and remediation signals.
- A proportional test ladder and consumer-driven review keep small work small while preserving independent assurance when it is actually required.

The CLI performs deterministic installation, inspection, routing, preflight, scheduling, state transitions, metrics, and dispatch-packet operations. Agent hosts perform the actual coding, subagent creation, review, merge, and delivery actions using their available capabilities and permissions.

## Build with the client, not past the client

The default for substantial product builds is **accompanied delivery**. The agent explains the next block, demonstrates the first usable slice and later material capabilities, and waits for the client's evaluation before affected expansion. It does not stop after every technical task; unrelated authorized work may continue. Say “use continuous delivery” to explicitly choose fewer optional product pauses.

Initial discovery is not blanket permission to invent future features. Only the next approved block is detailed. If a functionality's rules, exclusions, or stopping condition remain unclear, the agent asks a focused question and helps close them with examples before dispatch.

Every new spec states **“This task is complete only when…”** followed by successfully implemented behavior, expected results, and how each condition is proven. Desired, rejected, and failure cases come from approved intent—not merely from the code's assumptions. Automation/entrypoint changes require a controlled affected-flow smoke, including visible failure behavior.

The scheduler and atomic transitions enforce declared scope, product-approval, and completion-evidence gates. These validate recorded evidence; they do not authenticate a human decision or guarantee an agent's truthful compliance. Legacy JSON nodes without declarations remain compatible; table-only graphs need an executable JSON block before dispatch/completion. See [the contract and examples](docs/ACCOMPANIED-DELIVERY.md).

Upgrading the CLI does not replace a Kit copy already installed in a project. Preview the existing project's update before applying it, preserve host instructions/state, and open a fresh agent context afterward.

## Choose your delivery mode

| Say this | What happens |
| --- | --- |
| “Build this with me” (default) | Accompanied: define features progressively, demonstrate milestones, and wait for client evaluation before dependent expansion |
| “Execute the agreed scope end to end” | Autonomous: implement, test, and correct through the approved envelope without optional milestone pauses |
| “Use hackathon mode” | At most two cohesive discovery questions, a timeboxed demo, and first-demo evaluation |
| “I also want to learn” | Adds guided learning only after you approve the exact Markdown, Obsidian, Notion/MCP, or other note destination |

All three presets keep completion conditions, evidence, and authority limits; autonomous is not a one-worker restriction. Learning remains an independent consented option. Preview a preset with `agent-harness delivery-mode`, `agent-harness delivery-mode autonomous`, or `agent-harness delivery-mode hackathon`. This read-only command does not save the choice or activate execution; the agent records the approved choice in project context. See [delivery modes](docs/DELIVERY-MODES.md).

Hackathon mode keeps state, file leases, checks, and status, but uses light review by default and cuts secondary scope before the primary demo path.

## Prefer to listen?

Listen to a short English explanation of what the project does and how its workflow fits together.

[Play or download the English MP3](media/agent-harness-kit-overview-en.mp3) · [Open the GitHub-compatible MP4](media/agent-harness-kit-overview-en.mp4) · [Read the English script](media/overview-script-en.txt)

## Why it exists

| Without durable coordination | With the Kit |
| --- | --- |
| The agent rescans and guesses context | Approved context is read before broad inspection |
| A long context window becomes slow and expensive | Durable graph state lets a fresh window resume from the active neighborhood instead of chat history |
| Human decisions mix with technical tasks | `PENDING.md` and `TASK-GRAPH.md` have separate authority |
| Reviews repeat indefinitely or echo the implementer | A fresh reviewer context judges the SPEC once, with at most one focused re-review |
| The agent builds the whole system before client feedback | Technical tasks close on evidence; product milestones pause affected expansion |
| Multiple agents collide | Workstreams, ownership leases, and handoffs are explicit |
| Independent work waits in a single-file queue | The active orchestrator fills proven parallel capacity, then refills the first freed slot |
| A tiny CSS/copy edit triggers the whole harness | `direct-trivial` edits go straight to the file, with no interview, SPEC, graph, TDD, or review |
| A small local behavior fix triggers full ceremony | `vibe` changes one low-risk workstream directly, creates zero artifacts, and must pass a focused check |
| Study notes land in arbitrary folders | Learning starts only after the destination is approved |
| New feature ideas jump straight into code | Automatic feature discovery compares directions and records an approved brief first |
| Vague tasks make agents improvise and rescan | Non-trivial work gets one concise writing plan and small executable task specs |
| Tests are added only after implementation | Behavior tasks prove RED first, reach GREEN minimally, then run proportional regression |
| Small graph tasks generate piles of evidence files | Eligible deterministic `graph-only` tasks store just the outcome/check in the graph transition |

## What changes in your project

- `PROJECT-CONTEXT.md` records the approved product, constraints, mode, and important decisions.
- `FEATURE-*.md` closes product behavior gaps; `PLAN-*.md` decomposes approved non-trivial work without becoming another file per task.
- `PENDING.md` answers what still needs a human and what remains unfinished at product level.
- `TASK-GRAPH.md` owns technical order, dependencies, leases, progress, and the next ready work; each `TASK.md` is a self-contained executable spec.
- `CODEX-AGENT-DISPATCH.md` proves which dynamic Codex agent was created, with which role, bounded context, model/reasoning, returned context, and adapter response.
- Root `AGENTS.md` and `CLAUDE.md` route capable agents into the same platform-neutral rules contained in `agent-harness-kit/`.

Frontend, backend, data, infrastructure, integration, and learning use separate contexts when the host supports them. Every active node can declare a focused `read_set`, exclusive `write_set`, related `impact_set`, and source revision, reducing broad rescans without inventing a second graph.

Long conversations naturally become slower and more token-intensive across model families because every turn must process more accumulated material. The Kit treats that as normal: project context, pending state, the graph, specs, and decisions are durable memory. Open a fresh context, follow the resume order, and load only the active graph neighborhood; the new window can see what is complete, active, ready, blocked, and next without replaying the old chat.

## The working loop

Every mutating request uses one of four public lanes: `direct-trivial`, `vibe`, `graph-only`, or `full-harness`. Assurance is separate: `none`, `light`, or `full`. Full Harness is automatic only for two or more real agents, a human decision loop, required audit, insufficient model capability, unresolved consequential ambiguity, or an explicit request. Actual security/privacy/authorization/destructive changes require full audit; API and dependency keywords alone do not force a lane.

Full Harness can be compact for a bounded outcome or complete for discovery, multi-agent coordination, human governance, or full audit. Read-only audits and diagnosis do not trigger first-run. Resume probes current working-tree/runtime/test state first and reads durable artifacts only to fill gaps; current evidence supersedes stale handoffs.

You can inspect the same preflight from the terminal with `agent-harness route "your request"`. Use `--mode vibe` or `--mode full` for an explicit preference, `--workstreams 2` when more than one area is involved, and `--graph-bound --graph-only-eligible` for already specified low-risk graph work. The command always returns one of the four lanes as JSON; ambiguity safely falls back to `full-harness` while signaling that an economical AI classifier may refine it.

1. The agent reads approved context, then human/macro pending work, then the technical graph.
2. A new feature with open product choices automatically enters a focused brainstorm: known context is reused, credible options are compared, and you approve a feature brief before the graph changes.
3. Planned work uses independently checkable units targeting 15–30 active minutes, with exceptions justified by atomicity, runtime cost, or risk.
4. In Codex, the native dispatcher selects the neutral role, builds only the scoped context packet, resolves model/reasoning, and creates a fresh executable subagent with `fork_turns: none`. It records the returned identity/context/response; without subagents, implementation degrades explicitly to sequential execution while review still requires a separate fresh context. The agent then executes its self-contained SPEC without inventing missing behavior. Code follows RED → GREEN → REFACTOR; a contradiction or invalid RED returns to planning.
5. When two or more collision-free nodes are ready and capacity is greater than one, the orchestrator launches the safe batch, reports its active worker count, and refills the first released slot. It warns after 60–90 seconds without observable progress and interrupts/reassigns on the second consecutive occurrence.
6. Verification climbs `focused` → `workspace` → `integration` → `global/checkpoint` → `delivery` only as needed. In-scope technical recovery continues automatically; product, scope, material cost, permission, and experimental-integrity changes require a decision.
7. Same-context nodes use an inline spec and transition. Handoff/review packets exist only for real separate consumers. `assurance: light|full` preserves fresh independent review; `none` closes on executor verification.

For graph-managed work, routine progress updates are concise; explicit status views and milestone closeouts include stage, progress, automatic work, human/technical pending items, blockers, next action, and inspectable paths. `direct-trivial` and `vibe` return only a short edit/check summary; vibe always names its passing focused verification.

## Profiles

| Profile | Includes | Best for |
| --- | --- | --- |
| `core` | Delivery, graph, status, review, validation | Most projects |
| `core-learning` | `core` plus optional project learning | Guided practice and debriefs |
| `full` | `core-learning` plus the separate harness study pack | Studying harness engineering itself |

Learning support is never silently activated. The user chooses the exact Markdown path, Obsidian location, Notion target/MCP, or another destination before any note is created.

## New project or existing harness

In an empty project, discovery comes before stack, architecture, branding, or feature proposals. After product intent is known, the agent asks for architecture and folder organization only when they cannot be recovered from approved context or project evidence; optional coding conventions may be supplied, delegated to normal stack defaults, or omitted. In a mature repository, the Kit preserves the proven project shape and existing instructions; it never silently overwrites or reorganizes `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, or another authority. See the [mature-adoption playbook](harness/playbooks/mature-harness-adoption.md).

## Honest boundaries

- The Kit does not run unattended or open user-visible chats by itself. During an active orchestration session it can launch supported internal subagents/tasks in parallel; merge, deploy, publication, and visible task creation still require their own capability and authority.
- Leases are validated contracts, not OS-level locks.
- Threads, subagents, worktrees, MCPs, network, and model choice depend on the host's real capabilities and authorization. When automatic routing is explicitly approved and the host exposes overrides, dispatch applies the resolved model/reasoning values and records adapter confirmation; otherwise the route is visibly manual or blocked.
- A knowledge graph can reduce broad scans, but only scoped queries and execution budgets prevent waste; no tool guarantees lower token usage. See the [scoped graph execution contract](docs/SCOPED-GRAPH-EXECUTION.md) for the `read_set`, `write_set`, `impact_set`, provenance, and Graphify boundaries.

Need more detail? Read the [step-by-step installation guide](docs/EMBEDDED-INSTALLATION.md), [hackathon mode](docs/HACKATHON-MODE.md), [architecture](docs/ARCHITECTURE.md), [validation contract](docs/VALIDATION.md), [publication readiness audit](docs/PUBLICATION-READINESS.md), and [MIT License](LICENSE).
