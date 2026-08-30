# Playbook: Hackathon delivery

Use this playbook when approved project context declares `mode: hackathon` or `mode: hackathon+learning`.

1. Follow the normal first-response handshake. In the first cohesive question, collect only missing demo audience/outcome, deadline/timebox, must-have path, and hard constraints. Ask no more than one further discovery question unless a consequential safety/authority gap blocks execution.
2. Draft the compressed context using [hackathon mode](../../docs/HACKATHON-MODE.md). Separate must-have demo scope, optional demo enhancers, post-MVP gaps, acceptable shortcuts, and non-negotiable constraints. Obtain one explicit context/mode approval.
3. Create the normal `PENDING.md`. Human decisions and macro post-MVP gaps stay there; do not turn every idea into an active technical node.
4. Run `writing-plans` in compressed form. Use the simple-task exception when it genuinely applies; otherwise produce one concise plan of two-to-five-minute spec-driven units around the smallest end-to-end demo slice. Record shortcuts and deferred cases rather than leaving them for implementers to invent.
5. Create one normal `TASK-GRAPH.md` from those specs. Split isolated frontend/backend/data/infrastructure/content work by role and context, add early integration, and end with a demo-rehearsal node. Populate `read_set`, `write_set`, `impact_set`, and `context_provenance` when evidence exists.
6. Dispatch the critical path first. Parallelize only non-overlapping leases with a real integration point. Prefer reversible choices already inside the approved capability and risk envelope; consequential authority expansion still requires the human owner.
7. Verify continuously in the actual demo environment. Clearly label fixtures, mocks, seed data, manual setup, feature flags, and non-production shortcuts in handoff and status evidence.
8. Use light independent review by default. A second review is focused only on prior blockers, their correction, and related regressions. There is no third loop.
9. If time pressure threatens the demo, cut enhancers and secondary breadth, update graph/pending artifacts, and preserve the primary path plus minimum safety and verification. Never silently declare incomplete behavior complete.
10. Close with a passing demo rehearsal, a short runbook, visible limitations/post-MVP gaps, released leases, completed graph state, and the next recommended post-hackathon action.

`hackathon+learning` uses the same fast delivery graph. Learning capture remains observational and requires its approved destination; it cannot slow or control delivery.
