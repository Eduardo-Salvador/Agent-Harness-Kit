# Agent Harness Kit

Agent Harness Kit is a local execution-governance layer for coding agents. It gives Codex and Claude Code durable project context, adaptive workflow selection, dependency-aware execution, ownership leases, proportional verification, and inspectable completion.

![Agent Harness Kit](https://raw.githubusercontent.com/Eduardo-Salvador/Agent-Harness-Kit/v0.7.4/docs/assets/agent-harness-kit-banner.svg)

## Install

```bash
uv tool install agent-harness-kit-cli
```

For an existing installation, run `uv tool upgrade agent-harness-kit-cli` and verify `agent-harness --version`; repeating `uv tool install` does not upgrade an already installed tool.

Or install from the same PyPI release with `pipx` or plain `pip`, including from the integrated terminal in VS Code:

```bash
pipx install agent-harness-kit-cli
python -m pip install agent-harness-kit-cli
```

On Windows, `py -m pip install agent-harness-kit-cli` is also supported. Prefer a virtual environment with plain `pip`.

Open a terminal inside a project and run:

```bash
agent-harness install
```

The recommended `core` profile is installed by default. Use `--dry-run` to preview or `--profile core-learning` to include optional, consented project-learning support.

The installer creates a contained `agent-harness-kit/` directory **plus root `AGENTS.md` and `CLAUDE.md` entrypoints**. Missing root files are created; existing instructions are preserved outside one managed bridge block. Open a new agent context at the project root after installation, then use `agent-harness doctor` to verify the entrypoints.

## Compact distribution in this source checkout

Source version `0.7.4` contains the compact client distribution described below. The currently published PyPI `0.7.3` package does not include it yet.

The default `core` profile installs no more than 80 contained files inside `agent-harness-kit/`. The current manifest accounts for 79 files, including `PACKAGE-MANIFEST.json`. It excludes the repository-only `validation/`, `media/`, `examples/`, `benchmarks/`, and `.github/` trees from the client project. All QA stays in the source repository and in the release gate, so the smaller install does not lower quality.

Canonical runtime templates are packaged in `resources/templates.zip`. Use the compact runtime to validate the installation, discover templates, and scaffold one template on demand:

```bash
agent-harness validate
agent-harness scaffold --list
agent-harness scaffold PROJECT-CONTEXT --output harness-state/PROJECT-CONTEXT.md
```

The `full` profile is opt-in. Export it outside the client installation when an expanded portable package or audit surface is needed:

```bash
agent-harness export <dir> --profile full
```

The `core` and `full` profiles have different payload sizes, not different verification or release standards.

## New in 0.7.4

The default `core` installation is reduced to 79 contained files. Source tests, fixtures, media, benchmarks, examples, and CI remain in the repository and release gates instead of being copied into every client project. Canonical templates are hash-bound in `resources/templates.zip`, and the portable `runtime.pyz` provides validation and on-demand scaffolding.

The release gate inventories all 20 test modules and 59 support files, enforces a floor of 160 tests, validates all distribution profiles, and blocks packaging when coverage or client boundaries regress. Generated source packages verify every declared source hash before deriving compact artifacts or writing into a host project.

## Added in 0.7.3

Choose accompanied (default), autonomous end-to-end, or hackathon delivery. Accompanied waits at product milestones; autonomous executes the agreed scope without optional evaluation pauses; hackathon targets a timeboxed demo and first-demo evaluation. All retain completion evidence and authority limits; autonomous does not mean one worker.

`agent-harness delivery-mode [accompanied|autonomous|hackathon]` previews a preset without changing saved project policy, starting agents, or activating learning. The host agent records the approved selection in project context and preserves it on resume. Existing gates cannot be silently cleared by a mode switch.

## Retained from 0.7.2

Product builds use accompanied delivery: demonstrate the first usable slice and material capabilities, then genuinely wait for client evaluation before dependent expansion. Small fixes remain continuous; continuous product delivery can be explicitly chosen.

Planning is progressive. The initial interview does not authorize unspecified future features. When a functionality or stopping condition remains unclear, the agent asks and helps close it before graph readiness.

Every new spec states “This task is complete only when…” with concrete successful behavior, rejected/failure cases, and evidence per criterion. Scheduling/transitions enforce declared scope, human product-approval, criterion-level completion, and required TDD/affected-flow smoke gates. Routine progress no longer requires a full status form.

Checks validate recorded evidence, not execution authenticity. Legacy JSON nodes without declarations keep their previous behavior; table-only Markdown requires migration to an executable JSON block before dispatch/completion. CLI upgrades do not replace existing project installations.

## What it does

- four execution lanes (`direct-trivial`, `vibe`, `graph-only`, `full-harness`) independent from `none|light|full` assurance;
- evidence-first resume: probe current repository/runtime/check state, then read durable artifacts only to fill gaps;
- adaptive first-run project-shape discovery: reuse approved evidence, resolve architecture and folder organization before planning, and ask about optional coding conventions only when they are not already established;
- executable preflight for declared paths, scripts, environment names, commands, validator, browser/sandbox requirements, and worker capacity;
- `PENDING.md` for human decisions and macro gaps;
- `TASK-GRAPH.md` for dependencies, leases, progress, and execution;
- compact same-context specs and consumer-driven handoff/review artifacts;
- planned units targeting 15–30 active minutes, with justified exceptions;
- focused-first verification that climbs through workspace, integration, checkpoint, and delivery only as needed;
- scoped `read_set`, exclusive `write_set`, related `impact_set`, and source provenance to avoid unnecessary repository rescans;
- maximum-cardinality collision-free scheduling for hosts with proven parallel capacity;
- atomic compare-and-swap graph transitions, hash-chained events, append-only run metrics, and lighter-lane suggestions;
- bounded native Codex dispatch packets and fresh-context review when the host provides those capabilities;
- hackathon mode for compressed discovery and demo-first MVP delivery;
- a validator covering source, packaged profiles, and installed-host behavior.

The CLI performs deterministic installation, inspection, routing, preflight, scheduling, state transitions, metrics, and dispatch-packet operations. Capable agent hosts perform the actual coding and agent creation. The Kit has no unattended background daemon and does not lock operating-system files, merge branches, or deploy software on its own.

Documentation, source, audio overview, and examples are available in the [GitHub repository](https://github.com/Eduardo-Salvador/Agent-Harness-Kit).
