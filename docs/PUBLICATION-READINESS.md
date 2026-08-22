# Publication readiness audit

This audit applies to Agent Harness Kit and the repository/package slug `agent-harness-kit`.

## Current assessment

The source is suitable for public review as a native Codex/Claude Code operating scaffold, not as a standalone autonomous runtime. Every profile contains both documented platform entrypoints and small native extensions, while all durable policy/state stays neutral. It contains no configured external service, live MCP file, hook, credential, or automatic permission expansion.

## Evidence currently available

- Source validation checks required assets, contract templates, Markdown links/fragments/fences, both Mermaid blocks, language boundary, license text, first-run policy, graph dependencies/cycles/write collisions, reviewer independence, executable goal-lineage budget ceilings, fixtures, and profile boundaries.
- Each generated directory profile can run its own bundled validator using the generated `PACKAGE-MANIFEST.json`.
- Host-integration mode validates a sanitized namespaced mature-harness fixture plus missing-backlink, silent-omission, stale-snapshot, and premature-cutover failures.
- The examples demonstrate greenfield Development Core and existing-project Core plus project learning, but remain artifact traces rather than a live orchestrator test.
- Packaging uses standard-library Python, fixed ZIP metadata, sorted files, hashes, and the shared project version `0.4.0`.

## Package usability

`core`, `core-learning`, and `full` support intentional root-layout copies and contained installation under `agent-harness-kit/` with minimal root bridges. Each tool reaches the same first-run rule, neutral contracts, and host-owned state. Namespaced native-extension discovery remains capability-dependent and must degrade explicitly. Actions still require the capable agent/user session to follow the playbooks; the kit is not a separate program that independently calls APIs, provisions worktrees, dispatches sessions, merges branches, or publishes notes.

Current automated evidence is structural and fixture-based; installed Codex and Claude Code binaries have not yet been run through the planned interactive simulations. Mature-host semantic equivalence and cutover remain human decisions.

The execution budget now prevents contract-valid continuation after two implementation attempts, two consecutive no-progress cycles, or three context expansions in one goal lineage. The validator also checks discovered budget artifacts under direct-root or embedded-host `harness-state/`. This is artifact-level enforcement, not host-level process termination or measured token billing.

Controlled mature-host adoption is structurally testable, but semantic equivalence and cutover remain human decisions. Package selection never activates project learning.

## Remaining blockers before a public release

1. Run and record the planned interactive native onboarding simulations in installed Codex and Claude Code.
2. Complete filesystem-specific path/symlink/lease recovery policy before concurrent execution claims.
3. Review third-party/trademark notices and the native instruction/skill/agent security boundaries.
4. Run the validator and clean-build all profiles from the exact release source; inspect archive inventories/checksums and test on supported operating systems.
5. Decide release provenance/automation and GitHub attachment workflow before publishing artifacts.

See [open decisions](../OPEN-DECISIONS.md), [distribution](DISTRIBUTION.md), [validation](VALIDATION.md), and [portability](PORTABILITY.md).
