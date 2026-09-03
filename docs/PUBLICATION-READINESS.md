# Publication readiness audit

This audit applies to the Agent Harness Kit repository, generated profiles, and the public PyPI distribution `agent-harness-kit-cli`.

## Current assessment

Version `0.7.3` is published on PyPI. It adds explicit accompanied (default), autonomous end-to-end, and hackathon presets; a read-only `delivery-mode` inspector; and greeting-triggered onboarding with a visible welcome and unanswered mode choice. All presets preserve completion evidence, approved scope, existing gates, learning consent, and host-capability parallelism.

Wheel and source distribution passed metadata checks. [GitHub Actions Trusted Publishing](https://github.com/Eduardo-Salvador/Agent-Harness-Kit/actions/runs/33768257711) completed successfully. Separate clean Windows environments verified the local wheel and the public-index distribution. The public smoke downloaded `agent-harness-kit-cli==0.7.3` without cache and passed version inspection, core installation, both root bridges, doctor, embedded validation, and 26 delivery-mode/gate tests from the installed copy.

Two real Claude Code 2.1.197 print-mode smoke cases used only the prompt `oi`, an isolated installed host, Read/Glob tools, no session persistence, project-only settings, strict MCP configuration, and a US$1 cap per case. With no approved context, the result visibly welcomed the user, said the Kit was active, and asked the project intent plus accompanied/autonomous/hackathon preference. In a fresh session with approved autonomous context, the response preserved that mode and did not repeat onboarding or ask for mode selection. Both completed without permission denials. These are observed cases, not a universal model-obedience guarantee; Codex behavior is covered by shared-contract/installation checks here, not a new real Codex session trial.

The existing 0.7.2 scope/product/completion gates remain in force. Legacy JSON nodes without declarations retain their earlier behavior; table-only Markdown requires migration before ready/active/completed transitions. The Kit is not an unattended daemon. Project instruction loading remains a host requirement.

## Evidence currently available

- Source validation checks required assets, contract templates, Markdown links/fragments/fences, language boundaries, license text, first-run policy, scoped graph fields, dependencies, cycles, write/context collisions, reviewer independence, path traversal, assurance gates, executable goal-lineage ceilings, hostile fixtures, and profile boundaries.
- Each generated directory profile can run its own bundled validator using the generated `PACKAGE-MANIFEST.json`.
- Host-integration validation covers a sanitized namespaced mature-harness fixture plus missing-backlink, silent-omission, stale-snapshot, and premature-cutover failures.
- Graph validation covers focused `read_set`, exclusive `write_set`, related `impact_set`, pinned `context_provenance`, and the boundary that repository indexes such as Graphify enrich rather than replace the operational task graph.
- Packaging uses standard-library Python, fixed ZIP metadata, sorted files, hashes, and the shared source version `0.7.3`.
- Source regression: 136 tests passed; source validator checked 175 Markdown files and 219 required files; both changed native first-run skills passed UTF-8 validation.
- The `0.7.3` public-index smoke installed 245 profile files plus both root bridges, passed doctor, passed its embedded validator with 146 Markdown files and 244 required files, and passed all 26 delivery-mode/gate tests.

## Package usability and boundaries

`core`, `core-learning`, and `full` support intentional root-layout copies and contained installation under `agent-harness-kit/` with minimal root bridges. Each tool reaches the same first-run rule, neutral contracts, and host-owned state. Namespaced native-extension discovery remains capability-dependent and degrades explicitly.

The Kit still requires a capable agent or user session to follow its playbooks. It does not independently call APIs, provision worktrees, dispatch sessions, merge branches, deploy software, or publish notes. Leases are validated contracts rather than operating-system locks. Mature-host semantic equivalence and cutover remain human decisions.

Execution budgets reject contract-valid continuation after two implementation attempts, two consecutive no-progress cycles, or three context expansions in one goal lineage. Review permits one initial round and at most one focused re-review. These are artifact-level and validator-level controls, not host process termination or measured token billing.

The refreshed English and Portuguese overview tracks are hash-bound to their current scripts and marked `candidate-awaiting-audition`. File and script synchronization is validated; final listening quality and semantic fidelity still require human audition.

## Remaining follow-ups

These items limit stronger claims or future automation; they do not block use of the published scaffold:

1. Expand the two bounded real Claude onboarding cases into repeatable multi-host/native Codex coverage; do not generalize two successful greetings into guaranteed adherence.
2. Test packaged installation on additional supported operating systems and record filesystem-specific path, case, symlink, and lease-recovery behavior before stronger concurrency claims.
3. Complete third-party/trademark review and continue auditing native instruction, skill, agent, and connector security boundaries.
4. Add live token/time telemetry only where the host exposes trustworthy measurements; do not claim that graph enrichment alone guarantees lower token usage.

See [open decisions](../OPEN-DECISIONS.md), [distribution](DISTRIBUTION.md), [scoped graph execution](SCOPED-GRAPH-EXECUTION.md), [validation](VALIDATION.md), and [portability](PORTABILITY.md).
