# Validation contract

Run from the repository root:

```text
python tools/validate.py
```

The validator uses only the Python 3 standard library and does not modify files. It checks:

- required root entrypoints, native Codex skills, native Claude Code skills/subagents, roles, templates, playbooks, adapters, examples, and learning-pack modules;
- required YAML-header keys and Markdown sections in every operational template;
- model-routing tier/reason fields in task and handoff templates, plus the provider-neutral routing template;
- executable goal-lineage budgets in templates, fixtures, and discovered `harness-state/` artifacts, with positive ceilings, stable lineage, monotonic attempt/no-progress/context counters, mandatory stop-and-replan behavior, and safe evidence paths;
- review-profile and two-round-budget fields in task templates, plus auditable prior blockers, correction delta, and regression scope for focused round-two reviews;
- JSON task-graph blocks for node shape, unique IDs, existing dependencies, acyclicity, repository-relative write sets, and collisions among ready/active nodes;
- built-in valid and invalid graph fixtures, including missing dependencies, cycles, write-set collisions, self-review, and path traversal;
- hostile status mutations that remove mandatory fields, omit human-pending provenance, or escape repository-relative inspectable paths;
- hostile review mutation that removes the correction delta from a focused second-round payload;
- hostile budget mutations that bypass attempt, no-progress, or context-expansion ceilings, roll counters backward, narrow scope to one task, or escape evidence paths;
- relative Markdown links and fragment targets, balanced fenced-code blocks, and one Mermaid block in each README;
- the language boundary using a documented Portuguese-marker heuristic outside `README.pt-BR.md`;
- root routing: `CLAUDE.md` imports `@AGENTS.md`, both routes converge on neutral state, context remains concise, and safe defaults add no live MCP/settings/hooks;
- default frontend-screen routing through the same neutral playbook on Codex and Claude, with explicit checks for design-taste, responsive image direction, image generation, and image-to-code capabilities;
- project-learning activation routing from plain-language study requests, including explicit local/Obsidian/Notion destination discovery and capability-manifest evidence;
- portable workstream/context routing, separate visible-thread versus subagent capabilities, context-collision checks, and per-area status payloads;
- first-run and learning-pack exclusion statements in root entry points;
- overview-audio integrity, inline bilingual README players, versioned script links, and manifest hashes/status so narration drift is visible;
- distribution-profile boundaries (`core`, `core-learning`, `full`) through dependency-free packaging dry runs.
- bounded-review invariants: supported profiles, a hard two-round maximum, initial scope for round one, and focused scope with a prior-review reference for round two;
- pending-work schema separation between human actions, macro project gaps, and technical graph execution;
- mandatory user-facing progress/status fields—stage, progress, automatic work, human and macro pending items, active/ready/blocked graph snapshot, blockers, next action, and inspectable paths—with hostile field-removal mutations, automatic completion/next-task routing, and non-blocking assurance references across Codex and Claude entrypoints;
- executable assurance checkpoints: critical results can gate only explicitly affected graph actions while unrelated ready work continues;
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

Audio hash validation proves that the declared scripts and MP3 assets match the manifest bytes; it cannot independently recognize speech. A newly rendered track remains `candidate-awaiting-audition` until a human approves listening quality and semantic fidelity.

If Python 3 is unavailable, an adapter or human runner must implement these same checks and record durable evidence. Lack of a validator is explicit degradation, never a passing result.
