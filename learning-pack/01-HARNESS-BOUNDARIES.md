# Harness engineering and its boundaries

Harness engineering designs the environment around an agent: authority, context, tools, state, isolation, verification, and coordination. The goal is not a longer prompt. It is a system in which useful work can proceed while unsafe or unsupported claims fail visibly.

Two boundaries help:

- **User harness:** the workflow a developer experiences—discovery, approvals, task briefs, review, evidence, and optional project learning.
- **Tool harness:** the runtime machinery that exposes files, commands, sandboxes, events, secrets, and platform capabilities.

The user harness owns meaning and policy. The tool harness translates operations. Mixing them creates lock-in: a vendor feature can accidentally become the product's memory or authority model.

In this repository, [architecture](../docs/ARCHITECTURE.md) and [playbooks](../harness/playbooks/README.md) define the user harness; [adapters](../adapters/README.md) bound the tool harness. Read `AGENTS.md` to see how an operational agent crosses the boundary without making the root vendor-specific.
