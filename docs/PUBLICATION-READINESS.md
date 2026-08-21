# Publication readiness audit

This audit applies to Agent Harness Kit and the repository/package slug `agent-harness-kit`.

## Current assessment

The source is suitable for public review as a native Codex/Claude Code operating scaffold, not as a standalone autonomous runtime. Every profile contains both documented platform entrypoints and small native extensions, while all durable policy/state stays neutral. It contains no configured external service, live MCP file, hook, credential, or automatic permission expansion.

## Evidence currently available

- Source validation checks required assets, contract templates, Markdown links/fragments/fences, both Mermaid blocks, language boundary, license text, first-run policy, graph dependencies/cycles/write collisions, reviewer independence, fixtures, and profile boundaries.
- Each generated directory profile can run its own bundled validator using the generated `PACKAGE-MANIFEST.json`.
- Host-integration mode validates a sanitized namespaced mature-harness fixture plus missing-backlink, silent-omission, stale-snapshot, and premature-cutover failures.
- The examples demonstrate greenfield Development Core and existing-project Core plus project learning, but remain artifact traces rather than a live orchestrator test.
- Packaging uses standard-library Python, fixed ZIP metadata, sorted files, hashes, and the shared project version `0.1.0`.

## Package usability

`core`, `core-learning`, and `full` are usable as copied with Codex or Claude Code: each tool reads its native root file and reaches the same first-run rule, neutral contracts, and state. Skills and bounded Claude subagents provide progressive workflow routing. Actions still require the capable agent/user session to follow the playbooks; the kit is not a separate program that independently calls APIs, provisions worktrees, dispatches sessions, merges branches, or publishes notes.

Current automated evidence is structural and fixture-based; installed Codex and Claude Code binaries have not yet been run through the planned interactive simulations. Mature-host semantic equivalence and cutover remain human decisions.

Controlled mature-host adoption is structurally testable, but semantic equivalence and cutover remain human decisions. Package selection never activates project learning.

## Remaining blockers before a public release

1. Decide contribution governance and add the corresponding contributor/security/support documents.
2. Run and record the planned interactive native onboarding simulations in installed Codex and Claude Code.
3. Complete filesystem-specific path/symlink/lease recovery policy before concurrent execution claims.
4. Review third-party/trademark notices and the native instruction/skill/agent security boundaries.
5. Run the validator and clean-build all profiles from the exact release source; inspect archive inventories/checksums and test on supported operating systems.
6. Decide release provenance/automation and GitHub attachment workflow before publishing artifacts.
7. Re-render and audition both overview audios with the minimal dual-native-entrypoint sentence; the current approved MP3s predate that sentence and remain intentionally preserved.

See [open decisions](../OPEN-DECISIONS.md), [distribution](DISTRIBUTION.md), [validation](VALIDATION.md), and [portability](PORTABILITY.md).
