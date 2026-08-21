# Security policy

## Supported versions

| Version | Supported |
| --- | --- |
| `0.1.x` | Yes |
| Earlier development snapshots | No |

Support means maintainers will assess reports against the current source and may publish a corrective release. It is not a response-time or remediation-time guarantee.

## Reporting a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/Eduardo-Salvador/Agent-Harness-Kit/security/advisories/new) when it is available for this repository.

Do not disclose vulnerability details in a public issue, discussion, pull request, commit, log, or example. If the private reporting form is unavailable, open a public issue containing no vulnerability details and ask the maintainers to provide or enable a private reporting channel.

Include only information needed to reproduce and assess the issue:

- affected version, profile, adapter, or contract;
- impact and realistic threat scenario;
- minimal reproduction steps or sanitized fixture;
- affected files and expected safe behavior;
- suggested mitigation, if known.

Never include live credentials, private repository content, personal data, or production secrets. Replace them with sanitized placeholders.

## Scope

Relevant reports include permission expansion, secret exposure, unsafe path handling, cross-project data leakage, unapproved publication, contract bypass, provenance failure, malicious package contents, and unsafe native adapter behavior.

The kit is an operating scaffold, not a hosted service or autonomous runtime. Vulnerabilities in third-party models, Codex, Claude Code, GitHub, MCP servers, or another external product should normally be reported to that product's maintainer unless the Kit's integration or documentation creates the unsafe behavior.

## Handling

Maintainers will validate the report, define the affected scope, coordinate a fix and review, and decide disclosure timing. Reporters should allow a reasonable private remediation period. Credit is optional and will be included only with the reporter's approval. Publication, release, and advisory actions remain separate maintainer decisions.
