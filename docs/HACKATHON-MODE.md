# Hackathon mode

`hackathon` is a runtime delivery mode for a time-boxed MVP or live demo. It shortens discovery and prioritizes a demonstrable vertical slice without removing project context, task-graph coordination, file leases, verification, status reporting, or independent review.

Hackathon is one of the three [delivery presets](DELIVERY-MODES.md), alongside default accompanied delivery and explicit autonomous end-to-end delivery. It keeps the first-demo client evaluation before dependent expansion; it does not pause after every technical task. Selecting hackathon changes pace and scope, not evidence requirements or worker capacity.

## Activation

Plain-language requests such as “hackathon mode,” “build an MVP fast,” “demo first,” or a stated hackathon deadline trigger a proposal to use `mode: hackathon`. If the user also explicitly requests guided study, use `hackathon+learning` and complete the normal learning-destination gate before capturing notes.

The user approves the context and mode once. Low-risk reversible choices inside the approved envelope do not become repeated approval checkpoints.

## Compressed discovery

Ask at most two discovery questions before presenting the draft context and demo graph, unless a security, legal, destructive-action, credential, payment, external-publication, or materially ambiguous product decision genuinely blocks safe execution.

The compact interview establishes:

1. the demo audience, deadline/timebox, and single outcome that must visibly work;
2. must-have user path and supplied assets/data;
3. hard technical, brand, security, privacy, permission, or platform constraints;
4. available runtime and the smallest credible verification;
5. explicit exclusions and acceptable demo shortcuts.

Unknown details that do not block the demo are recorded as assumptions, not turned into more questions.

## Demo-first graph

The initial `TASK-GRAPH.md` uses the normal contracts and separates workstreams/agents, but prioritizes:

- one thin end-to-end demo slice before secondary breadth;
- parallel frontend, backend, data, infrastructure, and content nodes only when their write sets and execution contexts are isolated;
- an early integration node and a final demo-rehearsal node;
- `read_set`, `write_set`, `impact_set`, and `context_provenance` on active work;
- must-have nodes on the critical path, demo-enhancers off the critical path, and post-MVP ideas in `PENDING.md` as macro gaps rather than active tasks.

## Fast-path policy

- Prefer existing project capabilities and reversible implementation choices.
- Use fixtures, seed data, feature flags, mocks, or manual demo setup only when visibly labeled and acceptable for the approved demo; never fake acceptance evidence or conceal a non-production limitation.
- Default to a light independent review. Run the second focused review only for unresolved blockers or related regressions; never a third loop.
- Complete and report passing nodes immediately. Do not wait for ceremonial approval between authorized tasks.
- Status remains complete but compact and grouped by workstream.
- Cut scope before cutting the primary user path, security boundaries, ownership isolation, or the checks required to prove the demo works.

## Definition of done

Hackathon delivery is complete when the approved primary path runs in the declared environment, the demo script/rehearsal passes, known shortcuts and post-MVP gaps are visible, and the repository can be resumed from its artifacts. “Looks promising” is not completion.
