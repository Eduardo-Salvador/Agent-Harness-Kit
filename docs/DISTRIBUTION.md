# Distribution profiles

Agent Harness Kit uses the repository slug `Agent-Harness-Kit`, the contained installation directory `agent-harness-kit/`, and the PyPI distribution name `agent-harness-kit-cli`. The shorter PyPI name is owned by an unrelated project.

One canonical source tree produces three downloadable profiles. Long-lived branches are not editions: they would duplicate fixes, contracts, and safety rules and eventually drift. Profiles are generated views of one shared project version.

Every profile includes the root [MIT License](../LICENSE) with the same copyright notice.
Every profile also includes both versioned overview audios, their bilingual narration scripts, and `media/overview-audio-manifest.json`. The manifest binds script/audio hashes and audition status so README and audio drift cannot remain invisible after copying.

Every profile includes the provider-neutral capability-routing policy and template. Adapter mappings resolve model names at runtime; changing providers or model catalogs does not fork the core contracts.

Every profile includes both native platform entrypoints and the smallest operational extensions: root `AGENTS.md` plus `.agents/skills/` for Codex, and root `CLAUDE.md` plus `.claude/skills/` and bounded `.claude/agents/` for Claude Code. Profile selection is about learning content, not platform. No runtime guess or manual switch is required; each tool reads its own entrypoint and converges on the same neutral core/state. Project-learning skills and agents appear only in `core-learning` and `full`.

| Profile | Includes | Excludes |
| --- | --- | --- |
| `core` | Development Core, development-only example, contracts, validation, adapters | Project-learning operational files and Learning Pack |
| `core-learning` | `core` plus project-learning roles/templates/playbook/example | Learning Pack |
| `full` | `core-learning` plus the removable Learning Pack | Nothing selected by the full manifest |

Every generated package records `project_learning_activation: not-activated`. Profile selection controls file availability only; it never activates consent, observation, retention, or publication. Mature hosts should install into a namespace and follow the [adoption playbook](../harness/playbooks/mature-harness-adoption.md), not overwrite colliding root entrypoints, `.agents/`, `.claude/`, or `.mcp.json`.

The recommended contained host layout places the complete generated profile under `agent-harness-kit/` and adds only managed bridge blocks to host root entrypoints. The distribution remains replaceable while host-owned `harness-state/` remains outside it. See [embedded installation](EMBEDDED-INSTALLATION.md).

The end-user CLI is packaged through `pyproject.toml` with no runtime dependencies. Its PyPI distribution name is `agent-harness-kit-cli` because `agent-harness-kit` belongs to an unrelated project. The persistent flow is `uv tool install agent-harness-kit-cli`, then `agent-harness install`; the GitHub `uvx --from git+...` route and legacy source installer remain supported.

The explicit manifests are in [distribution/profiles](../distribution/profiles/core.json). `extends` expresses inheritance; source files remain single-copy. The packager expands sorted inclusion globs, applies exclusions, validates profile boundaries, and writes a generated inventory.

## Build

Use Python 3 standard library only. The output directory must be outside the source repository and must not already contain the target.

```text
python tools/package.py --profile core --output <outside-directory>
python tools/package.py --profile core-learning --output <outside-directory> --format directory
python tools/package.py --profile full --output <outside-directory>
```

Install a profile into a host project with a preflight-only pass followed by the explicit write:

```text
python tools/install.py --profile core --host <host-project> --dry-run
python tools/install.py --profile core --host <host-project>
```

The source checkout selects the requested profile. A generated package installs only its own manifest-declared profile and verifies every packaged file hash before writing.

ZIP entries are sorted, use a fixed timestamp and permissions, and contain source bytes plus `PACKAGE-MANIFEST.json`. Repeating a build from identical source/version produces identical archive bytes.

Generated names follow `agent-harness-kit-<version>-<profile>.zip` (or the same name as a directory).

Build the installable Python package separately with `uv build`. Before each release, test the resulting wheel in a clean environment and install a profile into an empty host. Publishing to PyPI is an external release action and is not performed by the build itself. Version `0.5.3` was published as `agent-harness-kit-cli`, then downloaded from PyPI and smoke-tested through a clean contained `core` installation and its bundled validator.

## Version strategy

Release `0.6.1` adds graph-local readiness validation before dispatch. It evaluates already-loaded graph data to catch false-ready dependency, assurance, and checkpoint state, with no AI call or repository scan. This does not affect `direct-trivial` or `vibe`, and does not validate live capabilities or task SPEC contents.

`VERSION` is the single version value shared by all three bundles; profile names are suffixes, not independent versions. `0.1.0` is the initial public source version, `0.2.0` adds contained installation plus continuous-delivery governance, `0.3.0` adds executable status reporting, focused re-review boundaries, hostile governance mutations, and GitHub-compatible overview media, `0.4.0` adds default frontend routing, explicit project-learning destinations, isolated workstream contexts, and per-area status, `0.5.0` adds the installable CLI, enriched graph context, hackathon delivery, and direct vector README assets, `0.5.1` exposes the standard/hackathon choice in the mandatory first-run welcome, `0.5.2` simplifies the public banner and adds concise stack/compatibility badges, `0.5.3` refreshes the bilingual overview audio and reorganizes the README around installation, pace, and the operating loop, and `0.6.0` adds automatic feature discovery, executable short-task specifications, TDD, native Codex/model dispatch, collision-safe parallel scheduling, and SPEC-led independent review. A future approved release changes `VERSION` once and validates all profiles.
