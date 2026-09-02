# Publication readiness audit

This audit applies to the Agent Harness Kit repository, generated profiles, and the public PyPI distribution `agent-harness-kit-cli`.

## Current assessment

Source version `0.7.0` is validated and suitable for use as a native Codex/Claude Code operating scaffold. It adds adaptive routing/assurance, compact and complete execution shapes, real-state-first resume, preflight, consumer-driven transfer artifacts, proportional test escalation, maximum-cardinality scheduling, runtime state/event/metric primitives, scoped validation, and clean external-host smoke coverage. The latest previously verified PyPI publication remains `0.5.3` until `0.7.0` is published and smoke-tested from the public index. It is not an unattended standalone daemon. No profile silently enables an external service, MCP, hook, credential, network permission, or destructive permission.

The previously published `0.5.3` package was built as wheel and source distribution, uploaded to PyPI, downloaded through the public index, installed into an empty Windows host, and validated from the installed copy. The local `0.7.0` release candidate has now passed the equivalent pre-publication path: build wheel and source distribution, install the wheel in a clean Python environment, create a contained profile in an empty Windows host, verify both root bridges with `doctor`, and run the embedded validator. A successful install creates the contained `agent-harness-kit/` directory and managed root `AGENTS.md` and `CLAUDE.md` bridges.

## Evidence currently available

- Source validation checks required assets, contract templates, Markdown links/fragments/fences, language boundaries, license text, first-run policy, scoped graph fields, dependencies, cycles, write/context collisions, reviewer independence, path traversal, assurance gates, executable goal-lineage ceilings, hostile fixtures, and profile boundaries.
- Each generated directory profile can run its own bundled validator using the generated `PACKAGE-MANIFEST.json`.
- Host-integration validation covers a sanitized namespaced mature-harness fixture plus missing-backlink, silent-omission, stale-snapshot, and premature-cutover failures.
- Graph validation covers focused `read_set`, exclusive `write_set`, related `impact_set`, pinned `context_provenance`, and the boundary that repository indexes such as Graphify enrich rather than replace the operational task graph.
- Packaging uses standard-library Python, fixed ZIP metadata, sorted files, hashes, and the shared source version `0.7.0`.
- The `0.7.0` clean-wheel smoke installed 239 profile files plus both root bridges; its embedded validator passed 144 Markdown files and 238 required files. Only a post-publication public-index smoke may close the new release evidence.

## Package usability and boundaries

`core`, `core-learning`, and `full` support intentional root-layout copies and contained installation under `agent-harness-kit/` with minimal root bridges. Each tool reaches the same first-run rule, neutral contracts, and host-owned state. Namespaced native-extension discovery remains capability-dependent and degrades explicitly.

The Kit still requires a capable agent or user session to follow its playbooks. It does not independently call APIs, provision worktrees, dispatch sessions, merge branches, deploy software, or publish notes. Leases are validated contracts rather than operating-system locks. Mature-host semantic equivalence and cutover remain human decisions.

Execution budgets reject contract-valid continuation after two implementation attempts, two consecutive no-progress cycles, or three context expansions in one goal lineage. Review permits one initial round and at most one focused re-review. These are artifact-level and validator-level controls, not host process termination or measured token billing.

The refreshed English and Portuguese overview tracks are hash-bound to their current scripts and marked `candidate-awaiting-audition`. File and script synchronization is validated; final listening quality and semantic fidelity still require human audition.

## Remaining follow-ups

These items limit stronger claims or future automation; they do not block use of the published scaffold:

1. Configure PyPI Trusted Publishing and release automation so future releases do not depend on a broad manual API token.
2. Record repeatable native Codex and Claude Code onboarding simulations instead of relying only on structural fixtures and observed manual sessions.
3. Test packaged installation on additional supported operating systems and record filesystem-specific path, case, symlink, and lease-recovery behavior before stronger concurrency claims.
4. Complete third-party/trademark review and continue auditing native instruction, skill, agent, and connector security boundaries.
5. Add live token/time telemetry only where the host exposes trustworthy measurements; do not claim that graph enrichment alone guarantees lower token usage.

See [open decisions](../OPEN-DECISIONS.md), [distribution](DISTRIBUTION.md), [scoped graph execution](SCOPED-GRAPH-EXECUTION.md), [validation](VALIDATION.md), and [portability](PORTABILITY.md).
