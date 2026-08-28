# Agent Harness Kit

Agent Harness Kit gives coding agents durable project context, separate human and technical pending views, dependency-aware execution, file ownership leases, bounded review, and inspectable completion.

![Agent Harness Kit](https://raw.githubusercontent.com/Eduardo-Salvador/Agent-Harness-Kit/v0.5.3/docs/assets/agent-harness-kit-banner.svg)

## Install

```bash
uv tool install agent-harness-kit-cli
```

Open a terminal inside a project and run:

```bash
agent-harness install
```

The recommended `core` profile is installed by default. Use `--dry-run` to preview or `--profile core-learning` to include optional, consented project-learning support.

The installer creates a contained `agent-harness-kit/` directory and managed root `AGENTS.md` and `CLAUDE.md` bridge blocks without replacing existing project instructions.

## What it coordinates

- approved project context before broad inspection;
- `PENDING.md` for human decisions and macro gaps;
- `TASK-GRAPH.md` for dependencies, leases, progress, and execution;
- isolated workstreams and context-aware frontend/backend/integration routing;
- one independent review and at most one focused re-review;
- hackathon mode for compressed discovery and demo-first MVP delivery;
- mandatory status with progress, blockers, next action, and inspectable paths.

The Kit is an artifact-driven scaffold followed by capable agents. It is not a daemon that autonomously opens sessions, locks operating-system files, merges branches, or deploys software.

Documentation, source, audio overview, and examples are available in the [GitHub repository](https://github.com/Eduardo-Salvador/Agent-Harness-Kit).
