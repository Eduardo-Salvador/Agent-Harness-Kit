# Scoped graph execution

The task graph is not only a dependency list. It is the execution index that tells an agent what to read, what it may change, and what related behavior it must verify.

## Node context fields

Each implementation node can declare:

- `read_set`: the smallest source paths that should be inspected before broader discovery;
- `write_set`: the exclusively leased paths the assignee may change;
- `impact_set`: related consumers and tests used to bound regression analysis;
- `context_provenance`: the inspection method and pinned source revision that produced those relationships.

Only `write_set` grants ownership. Read and impact paths may overlap between nodes because they are navigation and verification hints, not write authority.

## Execution behavior

An agent starts from the node's local graph neighborhood and `read_set` instead of rescanning the whole repository. It expands context only when evidence shows that the declared scope is incomplete, records that expansion against the execution budget, and updates the node provenance when the useful source boundary changes.

Technical transitions are graph transactions. Dispatch, start, material progress, dependency changes, block or unblock, remediation, completion, lease changes, context changes, and newly ready nodes increment the `TASK-GRAPH.md` revision before progress is reported. `PENDING.md` remains the authority for human actions and macro project gaps; it is never a substitute for a technical graph transition.

The validator rejects missing dependencies, cycles, concurrent write collisions, execution-context collisions, path traversal, self-review, and readiness that bypasses required assurance. User-facing status exposes active, ready, and blocked nodes together with the graph revision used.

## Repository graph enrichment

An approved and fresh repository graph tool, such as Graphify, may suggest `read_set`, `impact_set`, and `context_provenance`. Those relationships remain navigation hints until verified in source. The external tool does not become a second task authority, change lifecycle state, infer completion, or mutate dependencies automatically.

When no repository graph is available, the same contract works with scoped source inspection. This keeps the optimization portable while avoiding a claim that graph tooling alone guarantees lower token usage.

## Demo-first graphs

Hackathon mode applies the same contract to a smaller graph. It prioritizes the shortest vertical path to a testable demo, isolates workstreams that can progress safely in parallel, introduces an integration node early, and postpones secondary scope. Leases, checks, status, provenance, and review limits remain active.
