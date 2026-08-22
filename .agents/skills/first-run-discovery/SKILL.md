---
name: first-run-discovery
description: Use when project context is missing, unapproved, stale, or when an existing harness must be adopted before implementation planning.
---

# First-run discovery

1. Read `../../../harness/playbooks/first-run.md` and the discovery-interviewer role it references.
2. Test `../../../harness-state/PROJECT-CONTEXT.md` only if it exists in the host. Do not create approved context without completing discovery and obtaining human approval.
3. On an uninitialized project's first response, say briefly that Agent Harness Kit is active and that it organizes project context, pending work, and verifiable execution; state that discovery comes before implementation planning, and ask the highest-leverage unanswered question in the same message. Localize the opening to the user's language.
4. If the project directory is empty or effectively empty, do not propose product scope, features, design, architecture, stack, implementation steps, or a graph. Ask first what the user wants to create, for whom, which problem/value it addresses, and what first success looks like.
5. For mature hosts, use `../../../harness/playbooks/mature-harness-adoption.md`; never overwrite existing root or platform-native authorities.
6. Inventory actual rules and capabilities without assuming installation, authentication, secrets, network, or authorization.
7. Produce neutral artifacts. Do not plan implementation until context is approved and the initial graph exists.
