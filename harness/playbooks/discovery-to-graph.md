# Playbook: Discovery to graph

1. Apply the [first-run initialization test](first-run.md). Discovery interviewer inventories evidence, identifies `greenfield`, `existing`, or `uncertain` state, and creates a known/inferred/conflicting/unknown map.
2. Interview adaptively under [the discovery protocol](../../docs/DISCOVERY-INTERVIEW.md).
3. Draft project context and one decision per consequential choice. Also draft `harness-state/MODEL-ROUTING.md` from the current host catalog and adapter override evidence; keep it advisory until the human explicitly enables or declines automatic routing.
4. Select `delivery`, `delivery+learning`, `hackathon`, or `hackathon+learning`, obtain explicit human dispositions—including automatic model routing—and pin the approved context/routing revisions. Hackathon modes use the compressed demo-first playbook; the separate Harness Engineering Learning Pack is not a runtime selection.
5. Create or reconcile the pending authority with human decisions/actions and the macro project completion overview. It must not contain task order, dependencies, leases, or dispatch state.
6. Run [writing plans](writing-plans.md). Use compact inline specs where sufficient; otherwise create 15–30-minute executable units, justify exceptions, and create task artifacts only for actual separate executors.
7. Task decomposer maps specified units to nodes, dependencies, write sets, criteria, checks, capabilities, and checkpoints in the task graph.
8. Validate the plan/spec/graph mapping. Resolve missing specs, oversized units, cycles, missing dependencies, and parallel write collisions.
9. Human approves only consequential scope/topology. Orchestrator activates the graph and dispatches ready nodes without a ceremonial plan approval.

Exit only when at least one node is safely ready or the graph records a specific blocker.
