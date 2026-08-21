# Playbook: Discovery to graph

1. Apply the [first-run initialization test](first-run.md). Discovery interviewer inventories evidence, identifies `greenfield`, `existing`, or `uncertain` state, and creates a known/inferred/conflicting/unknown map.
2. Interview adaptively under [the discovery protocol](../../docs/DISCOVERY-INTERVIEW.md).
3. Draft project context and one decision per consequential choice.
4. Select `delivery` or `delivery+learning`, obtain explicit human dispositions, and pin the approved context revision. The separate Harness Engineering Learning Pack is not a runtime selection.
5. Create or reconcile the pending authority with human decisions/actions and the macro project completion overview. It must not contain task order, dependencies, leases, or dispatch state.
6. Task decomposer proposes outcome-sized nodes, dependencies, write sets, criteria, checks, capabilities, and checkpoints in the task graph.
7. Validate the graph. Resolve cycles, missing dependencies, and parallel write collisions.
8. Human approves consequential scope/topology. Orchestrator activates the graph and creates briefs for ready nodes.

Exit only when at least one node is safely ready or the graph records a specific blocker.
