# Agent Harness Kit

Agent Harness Kit gives coding agents durable project context, separate human and technical pending views, dependency-aware execution, file ownership leases, bounded review, and inspectable completion.

![Agent Harness Kit](https://raw.githubusercontent.com/Eduardo-Salvador/Agent-Harness-Kit/v0.6.0/docs/assets/agent-harness-kit-banner.svg)

## Install

```bash
uv tool install agent-harness-kit-cli
```

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

The installer creates a contained `agent-harness-kit/` directory and managed root `AGENTS.md` and `CLAUDE.md` bridge blocks without replacing existing project instructions.

## What it coordinates

- approved project context before broad inspection;
- `PENDING.md` for human decisions and macro gaps;
- `TASK-GRAPH.md` for dependencies, leases, progress, and execution;
- automatic feature discovery plus optimized writing plans: non-trivial work becomes small executable task specs, while truly simple work stays inline;
- a `direct-trivial` fast path for localized color, spacing, typo, and static-label edits without SPEC, graph, TDD, or review ceremony;
- a deterministic-first request router with `direct-trivial`, `vibe`, `graph-only`, and `full-harness` lanes; AI classifies only genuine ambiguity;
- a zero-artifact `vibe` path for one low-risk local behavior change, with mandatory focused verification and automatic promotion when scope grows;
- a machine-readable `agent-harness route "request"` preflight that always returns one of the four lanes and safely marks unresolved ambiguity for AI refinement;
- test-driven code tasks with meaningful RED before production changes, minimal GREEN, and proportional regression evidence;
- scoped `read_set`, exclusive `write_set`, related `impact_set`, and source provenance to avoid unnecessary repository rescans;
- isolated workstreams and context-aware frontend/backend/integration routing;
- agent-driven parallel fan-out that fills proven capacity, waits for the first event, refills safely, and joins branches through explicit integration nodes;
- capability-tier model routing that applies confirmed model/reasoning overrides at Codex task or subagent dispatch when explicitly approved;
- executable native Codex agent dispatch with neutral-role selection, minimal context, fresh implementer/reviewer identities, and adapter-owned response evidence;
- automatic fresh-context review against the versioned task SPEC, with at most one focused re-review;
- hackathon mode for compressed discovery and demo-first MVP delivery;
- mandatory status with progress, blockers, next action, and inspectable paths.

The Kit is an artifact-driven scaffold followed by capable agents. It has no unattended background daemon. During an active orchestration session it can launch supported internal subtasks in parallel; it does not lock operating-system files, merge branches, or deploy software on its own.

Documentation, source, audio overview, and examples are available in the [GitHub repository](https://github.com/Eduardo-Salvador/Agent-Harness-Kit).
