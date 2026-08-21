---
name: first-run-discovery
description: Use when project context is missing, unapproved, stale, or when an existing harness must be adopted before implementation planning.
---

# First-run discovery

1. Read `../../../harness/playbooks/first-run.md` and the discovery-interviewer role it references.
2. Test `../../../harness-state/PROJECT-CONTEXT.md` only if it exists in the host. Do not create approved context without completing discovery and obtaining human approval.
3. For mature hosts, use `../../../harness/playbooks/mature-harness-adoption.md`; never overwrite existing root or platform-native authorities.
4. Inventory actual rules and capabilities without assuming installation, authentication, secrets, network, or authorization.
5. Produce neutral artifacts. Do not plan implementation until context is approved and the initial graph exists.
