# Contributing

Thank you for improving Agent Harness Kit. Contributions are reviewed against the product boundaries, neutral contracts, portability goals, and safety defaults documented in this repository.

## Before starting

1. Read the [product definition](../docs/PRODUCT.md), [architecture](../docs/ARCHITECTURE.md), and [open decisions](../OPEN-DECISIONS.md).
2. Search existing issues before opening a new one.
3. Open an issue before a material contract, architecture, security, distribution, or compatibility change. Describe the problem, intended outcome, affected profiles, and migration impact.
4. Do not treat an unchecked open decision as permission to implement a choice.

Small documentation corrections and narrowly scoped fixes may proceed directly to a pull request.

## Change requirements

- Keep changes within one coherent acceptance and rollback unit.
- Preserve platform-neutral core state and the documented Codex and Claude Code entrypoints.
- Do not add credentials, live service configuration, personal paths, generated packages, caches, or private project evidence.
- Do not expand permissions, enable integrations, activate learning, or publish external data by default.
- Update contracts, examples, fixtures, validation, and distribution profiles when their behavior changes.
- Add migration notes for breaking contract or packaging changes.
- Use English for repository content except the canonical Portuguese README.

## Branches and commits

Use a readable branch name in the form `<type>/<area>/<slug>`, such as `docs/governance/support-policy` or `fix/validator/review-budget`.

Use Conventional Commits with an area when useful, for example:

```text
feat(contracts): add checkpoint recovery state
fix(validator): reject stale task revisions
docs(governance): define support channels
```

Do not add automated-agent attribution, `Co-authored-by`, or similar authorship trailers. The human committer remains responsible for the contribution and its history.

## Validation

Run the repository validator:

```text
python tools/validate.py
```

When distribution boundaries change, check all profiles:

```text
python tools/package.py --profile core --output work/core --format directory --check
python tools/package.py --profile core-learning --output work/core-learning --format directory --check
python tools/package.py --profile full --output work/full --format directory --check
```

Record any unavailable check or explicit degradation. Do not describe an unexecuted check as passing.

## Pull requests

A pull request should include:

- the problem and outcome;
- the exact scope and excluded work;
- affected contracts, profiles, and compatibility boundaries;
- verification performed and any known degradation;
- migration or rollback notes when applicable;
- linked issues or decisions.

At least one independent review is required. A blocking finding may receive one focused remediation and re-review. Optional improvements become follow-ups and do not block acceptance. Maintainers make the final acceptance and release decision and may decline changes that conflict with project scope or maintenance capacity.

## Conduct

Be respectful, specific, and evidence-based. Harassment, discrimination, threats, doxxing, and disclosure of another person's private information are not accepted. Maintainers may edit, hide, lock, or remove disruptive content and restrict participation when necessary to protect the project and its community.

Security vulnerabilities must follow the [security policy](SECURITY.md), not a public issue or pull request.
