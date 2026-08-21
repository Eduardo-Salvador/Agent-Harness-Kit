# Open decisions

This ledger contains real unresolved choices. An unchecked item is not permission for an agent to guess. Blocking phase indicates when a decision must be made.

## Product and governance

- [x] **Project identity** — name: Agent Harness Kit; repository/package slug: `agent-harness-kit`.
- [x] **License** — standard MIT License, copyright 2026 Agent Harness Kit contributors.
- [ ] **Governance and contribution policy** — owner: maintainers; block: accepting external contributions.

## Learning and notes

- [ ] **Default learning destination** — owner: user/product; block: learning publication prototype. Decide whether baseline is repository-local Markdown only.
- [ ] **Obsidian conventions** — owner: user/product; block: Obsidian adapter. Decide vault path policy, front matter, links, and attachments.
- [ ] **Notion publication model** — owner: user/product/security; block: Notion adapter. Decide database/page structure, preview, approval granularity, and credential storage.
- [ ] **Retention/redaction policy for learning evidence** — owner: security/product; block: learning pilot with non-public code.

## Platforms, integrations, and security

- [ ] **MCP/integration setup** — owner: platform maintainers; block: first external integration. Define discovery, trust, version pinning, and failure behavior.
- [x] **Phase 2 safe permission baseline** — repository-scoped writes, no network/secrets/destructive action by default, with explicit approval-required/unavailable capability states. Production policy details remain adapter work.
- [ ] **Isolation fallback details** — owner: architecture; block: orchestrator implementation. Specify path normalization, symlink handling, lease expiry, and cleanup/recovery.
- [x] **Native entrypoint baseline** — Codex uses root `AGENTS.md` and repository `.agents/skills/`; Claude Code uses root `CLAUDE.md` importing `@AGENTS.md`, plus `.claude/skills/` and bounded `.claude/agents/`. Both converge on neutral state.
- [ ] **Runtime capability baseline** — owner: platform maintainers; block: claims about automated isolation/delegation/hooks. Run installed-tool simulations and record available, degraded, unavailable, and approval-required capabilities without enabling them.
- [ ] **Versioned non-Git artifact-store support** — owner: architecture; block: claiming non-Git runtime support. Decide whether v1 implements it or documents Git as a temporary prerequisite.

## Contracts and validation examples

- [x] Use `harness-state/` as the neutral default runtime location; adapters may map it only when the canonical path remains discoverable.
- [x] Define the minimal immutable review-result record separately from the implementer's handoff.
- [x] Bound delivery review to one initial round plus at most one focused re-review; after round 2, block and escalate/decompose instead of repeating the unchanged contract.
- [x] Use bounded YAML scalar headers plus JSON for executable task-graph data; avoid a third-party schema dependency in Phase 2.
- [ ] Add valid and invalid fixtures for every contract invariant. Phase 2 covers graph validity, missing dependencies, cycles, and write collisions.
- [x] Validate DAG cycles, missing dependencies, and overlapping normalized paths among concurrently ready/active nodes.
- [ ] Validate invalid lifecycle transitions and stale expected revisions.
- [ ] Demonstrate failed verification, retry lineage, reviewer disagreement, checkpoint blocking, and interruption recovery.
- [ ] Demonstrate learning disabled, paused, destination failure, denied publication, and a graph-change recommendation with no direct effect.
- [ ] Run the two approved interactive pre-commit simulations (plain-language explanation and adaptive project interview) through installed Codex and Claude Code, recording visible capability degradation.
- [x] Add namespaced mature-harness adoption, migration/coexistence/provenance contracts, host-mode validation, and sanitized drift/backlink fixtures.
- [ ] Expand host migration validation beyond content hashes/globs to filesystem-specific symlink/case equivalence after the isolation policy is decided.

## Distribution and release

- [x] Define `core`, `core-learning`, and `full` as generated profiles from one source tree and shared `VERSION`.
- [x] **Initial public version** — `0.1.0`; approved tag: `v0.1.0` from the validated canonical source.
- [ ] **Release automation and GitHub attachments** — owner: maintainers/security; block: automated release. Validate provenance, checksums, and permissions before enabling.
- [x] Keep one canonical, profile-aware README pair; copied-profile validation confirms all remaining relative links resolve without profile-specific rendering.
- [ ] **Overview audio capability-routing refresh** — owner: maintainers/user; block: publication polish. Versioned bilingual scripts now cover native entrypoints, capability-based routing, coherent change units, and separate publication authority. Re-render both tracks from those scripts and obtain user audition approval; preserve the current approved MP3s until an acceptable bilingual pair exists.

## Next implementation gate

Before claims about an external autonomous runtime or automated isolation/delegation, run the native interactive simulations, confirm runtime capability baselines, and finish isolation/path policy. Release automation and external note destinations remain blocked only at their stated publication/integration points.
