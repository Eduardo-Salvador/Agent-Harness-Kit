# Publication readiness audit

This audit applies to the Agent Harness Kit repository, generated profiles, and the public PyPI distribution `agent-harness-kit-cli`.

## Current assessment

Version `0.7.2` is published on PyPI. It adds accompanied delivery with real client milestone pauses, progressive feature scope closure, explicit task completion conditions, criterion-level evidence, and executable scope/product/TDD/affected-flow gates. Routine progress remains concise. Technical completion is distinct from product approval; recorded evidence is structurally checked, not authenticated.

The release was built as wheel and source distribution, checked with Twine, and published through [GitHub Actions Trusted Publishing](https://github.com/Eduardo-Salvador/Agent-Harness-Kit/actions/runs/33711530917). Both local-wheel and public-index smoke tests installed into separate empty Windows hosts. The public test downloaded `agent-harness-kit-cli==0.7.2` from PyPI with cache disabled and verified CLI version, contained core installation, root `AGENTS.md`/`CLAUDE.md` bridges, `doctor`, the embedded validator, and all 20 delivery-gate tests from the installed copy.

Legacy JSON nodes without new declarations retain prior behavior; newly planned nodes declare their scope and completion conditions. Table-only Markdown requires migration to an executable JSON block before ready/active/completed transitions. The Kit is not an unattended daemon and does not independently enforce truthful evidence or control the host conversation.

## Evidence currently available

- Source validation checks required assets, contract templates, Markdown links/fragments/fences, language boundaries, license text, first-run policy, scoped graph fields, dependencies, cycles, write/context collisions, reviewer independence, path traversal, assurance gates, executable goal-lineage ceilings, hostile fixtures, and profile boundaries.
- Each generated directory profile can run its own bundled validator using the generated `PACKAGE-MANIFEST.json`.
- Host-integration validation covers a sanitized namespaced mature-harness fixture plus missing-backlink, silent-omission, stale-snapshot, and premature-cutover failures.
- Graph validation covers focused `read_set`, exclusive `write_set`, related `impact_set`, pinned `context_provenance`, and the boundary that repository indexes such as Graphify enrich rather than replace the operational task graph.
- Packaging uses standard-library Python, fixed ZIP metadata, sorted files, hashes, and the shared source version `0.7.2`.
- Source regression: 130 tests passed; source validator checked 174 Markdown files and 218 required files; all four changed Codex/Claude skills passed validation.
- The `0.7.2` public-index smoke installed 242 profile files plus both root bridges, passed `doctor`, passed its embedded validator with 145 Markdown files and 241 required files, and passed all 20 delivery-gate tests.

## Package usability and boundaries

`core`, `core-learning`, and `full` support intentional root-layout copies and contained installation under `agent-harness-kit/` with minimal root bridges. Each tool reaches the same first-run rule, neutral contracts, and host-owned state. Namespaced native-extension discovery remains capability-dependent and degrades explicitly.

The Kit still requires a capable agent or user session to follow its playbooks. It does not independently call APIs, provision worktrees, dispatch sessions, merge branches, deploy software, or publish notes. Leases are validated contracts rather than operating-system locks. Mature-host semantic equivalence and cutover remain human decisions.

Execution budgets reject contract-valid continuation after two implementation attempts, two consecutive no-progress cycles, or three context expansions in one goal lineage. Review permits one initial round and at most one focused re-review. These are artifact-level and validator-level controls, not host process termination or measured token billing.

The refreshed English and Portuguese overview tracks are hash-bound to their current scripts and marked `candidate-awaiting-audition`. File and script synchronization is validated; final listening quality and semantic fidelity still require human audition.

## Remaining follow-ups

These items limit stronger claims or future automation; they do not block use of the published scaffold:

1. Record repeatable native Codex and Claude Code onboarding simulations instead of relying only on structural fixtures and observed manual sessions.
2. Test packaged installation on additional supported operating systems and record filesystem-specific path, case, symlink, and lease-recovery behavior before stronger concurrency claims.
3. Complete third-party/trademark review and continue auditing native instruction, skill, agent, and connector security boundaries.
4. Add live token/time telemetry only where the host exposes trustworthy measurements; do not claim that graph enrichment alone guarantees lower token usage.

See [open decisions](../OPEN-DECISIONS.md), [distribution](DISTRIBUTION.md), [scoped graph execution](SCOPED-GRAPH-EXECUTION.md), [validation](VALIDATION.md), and [portability](PORTABILITY.md).
