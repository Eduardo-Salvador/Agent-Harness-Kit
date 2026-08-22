# Distribution profiles

Agent Harness Kit uses the package slug `agent-harness-kit`.

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

## Version strategy

`VERSION` is the single version value shared by all three bundles; profile names are suffixes, not independent versions. `0.1.0` is the initial public source version, `0.2.0` adds contained installation plus continuous-delivery governance, `0.3.0` adds executable status reporting, focused re-review boundaries, hostile governance mutations, and GitHub-compatible overview media, and `0.4.0` adds default frontend routing, explicit project-learning activation/destinations, workstream-isolated execution contexts, and per-area status. A future approved release changes `VERSION` once, validates all profiles, and may attach the three archives to one GitHub Release. Release automation remains an open decision.
