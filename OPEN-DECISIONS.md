# Open decisions

This ledger contains real unresolved choices. An unchecked item is not permission for an agent to guess. Blocking phase indicates when a decision must be made.

## Product and governance

- [x] **Project identity** — name: Agent Harness Kit; repository/package slug: `agent-harness-kit`.
- [x] **License** — standard MIT License, copyright 2026 Agent Harness Kit contributors.
- [x] **Governance and contribution policy** — maintainers retain final acceptance and release authority; contribution, conduct, security-reporting, and support boundaries are defined under `.github/`.

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
- [x] Define an executable goal-lineage budget with default ceilings of two implementation attempts, two consecutive no-progress cycles, and three context expansions; hostile fixtures reject ceiling bypass, counter rollback, task-only reset scope, and unsafe evidence paths.
- [x] Run delivery review automatically as non-blocking post-completion assurance, limited to one initial round plus at most one focused remediation review; after a second rejection, force task/acceptance rewrite, decomposition, or a genuine human product/risk decision without reopening completion or repeating the loop.
- [x] Define contained installation under `agent-harness-kit/` with minimal managed root bridges, host-owned `harness-state/`, preserved existing authority, and explicit native-extension degradation.
- [x] Use bounded YAML scalar headers plus JSON for executable task-graph data; avoid a third-party schema dependency in Phase 2.
- [ ] Add valid and invalid fixtures for every contract invariant. Current coverage includes graph validity, missing dependencies, cycles, write collisions, reviewer independence, path traversal, mandatory status/provenance fields, focused re-review evidence, assurance gates, and mature-host migration failures.
- [x] Validate DAG cycles, missing dependencies, and overlapping normalized paths among concurrently ready/active nodes.
- [ ] Validate invalid lifecycle transitions and stale expected revisions.
- [ ] Demonstrate failed verification, retry lineage, reviewer disagreement, checkpoint blocking, and interruption recovery.
- [ ] Add live host token/time telemetry and optional numerical cost ceilings after Codex/Claude capability simulations establish which measurements are actually exposed.
- [ ] Demonstrate learning disabled, paused, destination failure, denied publication, and a graph-change recommendation with no direct effect.
- [ ] Run the two approved interactive pre-commit simulations (plain-language explanation and adaptive project interview) through installed Codex and Claude Code, recording visible capability degradation.
- [x] Add namespaced mature-harness adoption, migration/coexistence/provenance contracts, host-mode validation, and sanitized drift/backlink fixtures.
- [ ] Expand host migration validation beyond content hashes/globs to filesystem-specific symlink/case equivalence after the isolation policy is decided.

## Distribution and release

- [x] Define `core`, `core-learning`, and `full` as generated profiles from one source tree and shared `VERSION`.
- [x] **Initial public version** — `0.1.0`; approved tag: `v0.1.0` from the validated canonical source.
- [x] **Contained installation and continuous delivery release** — `0.2.0`; approved tag: `v0.2.0` from the validated canonical source.
- [ ] **Release automation and GitHub attachments** — owner: maintainers/security; block: automated release. Validate provenance, checksums, and permissions before enabling.
- [x] Keep one canonical, profile-aware README pair; copied-profile validation confirms all remaining relative links resolve without profile-specific rendering.
- [x] **Overview audio 0.3.0 refresh** — bilingual tracks were re-rendered with the current scripts, including executable goal-lineage budgets, approved by the user, published as GitHub attachments, and bound by manifest hashes.

## Next implementation gate

Before claims about an external autonomous runtime or automated isolation/delegation, run the native interactive simulations, confirm runtime capability baselines, and finish isolation/path policy. Release automation and external note destinations remain blocked only at their stated publication/integration points.
