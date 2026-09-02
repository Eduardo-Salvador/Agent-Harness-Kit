# Validation contract

Run from the repository root:

```text
python tools/validate.py
```

The validator uses only the Python 3 standard library and does not modify files. It checks:

- required root entrypoints, native Codex skills, native Claude Code skills/subagents, roles, templates, playbooks, adapters, examples, and learning-pack modules;
- required YAML-header keys and Markdown sections in every operational template;
- a request router with four public lanes plus orthogonal `none|light|full` assurance, narrow full-Harness conditions, compact/complete execution, and Codex/Claude parity;
- `direct-trivial` routing for bounded presentation/static-content mechanics and zero-artifact `vibe` routing for small local behavior changes only when a focused deterministic check is available and passes;
- proportional `evidence_profile` routing: only inline-simple verification-only tasks may use `graph-only`, with no reviewer, zero rounds, no assurance gate, and a concise graph transition instead of handoff/review artifacts; hostile tests reject TDD or assurance bypasses;
- test-strategy declarations, meaningful RED/GREEN task specs, explicit non-TDD exceptions, handoff evidence sections, and native Codex/Claude TDD routing;
- model-routing tier/reason fields plus executable `harness.model-dispatch/v1` evidence: selected runtime model, supported reasoning effort, override surface, returned context, and adapter confirmation;
- hostile model-dispatch fixtures that reject recorded-tier-only routing, silent host-default fallback, and impossible same-context mid-turn switch claims;
- native Codex agent-dispatch tests and hostile records that reject context leakage, missing adapter responses, model/reasoning mismatch, and implementer/reviewer identity or context reuse;
- executable goal-lineage budgets in templates, fixtures, and discovered `harness-state/` artifacts, with positive ceilings, stable lineage, monotonic attempt/no-progress/context counters, mandatory stop-and-replan behavior, and safe evidence paths;
- review-profile and bounded-round fields in task templates, including the zero-review graph-only exception, plus fresh-context identity, SPEC-only authority, immutable packet provenance, and auditable prior blockers/correction delta/regression scope for focused round-two reviews;
- JSON task-graph blocks for node shape, unique IDs, existing dependencies, acyclicity, repository-relative write sets, and collisions among active ownership leases;
- built-in valid and invalid graph fixtures, including missing dependencies, cycles, write-set collisions, self-review, and path traversal;
- deterministic scheduler tests for dependency/assurance eligibility, numeric capacity, active-slot accounting, collision deferral, and dependency fan-in;
- prerequisite preflight checks for declared paths, package scripts, environment names, executables, validator, browser state, and worker capacity without exposing secret values;
- compare-and-swap graph transitions, hash-chained/idempotent event ledgers, append-only run metrics, lighter-lane suggestions, and two-stage inactivity handling;
- benchmark isolation that scans the resolved work directory and every ancestor before the first injected call, plus a clean external installed-host smoke;
- hostile parallel-dispatch fixtures that reject over-capacity batches, duplicate contexts, and claims of dispatch without adapter runtime evidence;
- hostile status mutations that remove mandatory fields, omit human-pending provenance, or escape repository-relative inspectable paths;
- hostile review mutations that remove the correction delta or SPEC authority, substitute prompt memory, or reuse the implementer context;
- hostile budget mutations that bypass attempt, no-progress, or context-expansion ceilings, roll counters backward, narrow scope to one task, or escape evidence paths;
- relative Markdown links and fragment targets, balanced fenced-code blocks, and one Mermaid block in each README;
- the language boundary using a documented Portuguese-marker heuristic outside `README.pt-BR.md`;
- root routing: `CLAUDE.md` imports `@AGENTS.md`, both routes invoke the neutral request router before all Harness ceremony, context remains concise, and safe defaults add no live MCP/settings/hooks;
- default frontend-screen routing through the same neutral playbook on Codex and Claude, with explicit checks for design-taste, responsive image direction, image generation, and image-to-code capabilities;
- project-learning activation routing from plain-language study requests, including explicit local/Obsidian/Notion destination discovery and capability-manifest evidence;
- portable workstream/context routing, separate visible-thread versus subagent capabilities, context-collision checks, and per-area status payloads;
- first-run and learning-pack exclusion statements in root entry points;
- overview-audio integrity, language-specific README media links, approved-attachment requirements, versioned script links, and manifest hashes/status so narration drift is visible;
- distribution-profile boundaries (`core`, `core-learning`, `full`) through dependency-free packaging dry runs.
- bounded-review invariants: supported profiles, mandatory clean reviewer context, task-SPEC authority instead of prompt memory, a hard two-round maximum, initial scope for round one, and focused scope with a prior-review reference for round two;
- pending-work schema separation between human actions, macro project gaps, and technical graph execution;
- mandatory user-facing progress/status fields—stage, progress, automatic work, human and macro pending items, active/ready/blocked graph snapshot, blockers, next action, and inspectable paths—with hostile field-removal mutations, automatic completion/next-task routing, and non-blocking assurance references across Codex and Claude entrypoints;
- executable assurance checkpoints: critical results can gate only explicitly affected graph actions while unrelated ready work continues;
- shared graph-local readiness semantics: structural validation and scheduling both reject false `ready`/`active` dependency, assurance, and checkpoint state using already-loaded graph data only;
- embedded installer dry-run, content preservation, marker safety, existing-destination refusal, profile selection, and packaged hash verification;
- embedded-installation documentation and stable managed bridge markers for root `AGENTS.md` and `CLAUDE.md`;
- migration coverage, classifications, selector expansion, source identities, destinations/backlinks, unresolved ownership, semantic reviewers, and cutover authority.

Inside a generated directory bundle, `PACKAGE-MANIFEST.json` selects bundle-aware required files and the validator checks only that profile's packaging boundary. This lets each copied profile validate without requiring intentionally omitted optional content.

All profiles must contain both native platform entrypoints and core workflow extensions. `core` must exclude platform-specific project-learning skills/agents; `core-learning` and `full` include them without activating learning. These checks are structural filesystem conformance, not proof that installed Codex or Claude Code binaries executed a session.

For a namespaced host adoption:

```text
python <kit>/tools/validate.py --host-root <host> --migration-manifest harness-adoption/MIGRATION-MANIFEST.md
```

The sanitized mature-host fixture covers root filename collisions, existing roles/knowledge, unresolved backlog, generated `.claude/worktrees`, a secret-bearing example path, retained narrative decisions, and verification sources. Negative fixtures prove missing-backlink, silent-omission, stale-snapshot, and premature-cutover detection. Structural coverage still requires human semantic review before cutover.

## Scope and limitations

The YAML reader is deliberately bounded: it validates top-level scalar fields used by these templates, not arbitrary YAML. Task graph execution data is JSON inside Markdown so standard-library parsing is deterministic. Path collision checks normalize separators, `.` segments, case, and trailing `/**`; they reject absolute/parent paths and conservatively treat wildcard prefixes as owned directories. Symlink and filesystem-specific equivalence remain an open runtime policy.

Language detection cannot prove that prose is English. The validator rejects a maintained set of unambiguous Portuguese markers outside the allowed README and also checks the removed Portuguese filename. Human review remains necessary for style and semantics.

Audio hash validation proves that the declared scripts and media assets match the manifest. Binary MP3/MP4 hashes are byte-exact; UTF-8 script hashes normalize CRLF and CR line endings to LF so Git checkout policy cannot create false drift. It cannot independently recognize speech. A newly rendered track remains `candidate-awaiting-audition` and may omit a GitHub attachment until a human approves listening quality and semantic fidelity; `approved` requires a valid attachment.

If Python 3 is unavailable, an adapter or human runner must implement these same checks and record durable evidence. Lack of a validator is explicit degradation, never a passing result.
