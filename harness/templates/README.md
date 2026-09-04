# Operational templates

Copy these templates into the host project's `harness-state/` runtime directory. Paths under `examples/*/state/` are illustrative fixtures, not the canonical runtime location.

| Template | Authority that updates instances |
| --- | --- |
| [Request route](REQUEST-ROUTE.md) ([contract](../../docs/contracts/REQUEST-ROUTE.md)) | Optional adapter/test exchange shape; fast routes do not persist it |
| [Project context](PROJECT-CONTEXT.md) | Discovery drafts; human approves |
| [Feature brief](FEATURE-BRIEF.md) | Feature discovery drafts; human approves before graph mutation |
| [Implementation plan](IMPLEMENTATION-PLAN.md) | Task decomposer writes one for non-trivial work; orchestrator validates and marks ready |
| [Task graph](TASK-GRAPH.md) | Orchestrator only |
| [Pending work](PENDING.md) | Orchestrator maintains human actions and macro project completion; technical execution stays in the graph |
| [Status](STATUS.md) | Orchestrator derives an inspectable user update from project context, pending authority, and graph |
| [Task brief](TASK.md) | Orchestrator writes the executable spec, including test strategy and RED/GREEN cycle; implementer updates attempt status only |
| [Handoff](HANDOFF.md) | Assigned implementer; includes test-first evidence and the plain-language user closeout |
| [Review result](REVIEW.md) ([contract](../../docs/contracts/REVIEW.md)) | Fresh-context independent reviewer; SPEC-led initial review plus at most one focused re-review |
| [Decision](DECISION.md) | Proposer drafts; named authority decides |
| [Migration manifest](MIGRATION-MANIFEST.md) | Adoption lead inventories; humans approve semantics/cutover |
| [Coexistence](COEXISTENCE.md) | Existing-harness owner + project owner |
| [Adapter binding](ADAPTER-BINDING.md) | Adapter maintainer; existing authority remains referenced |
| [Capability manifest](CAPABILITY-MANIFEST.md) | Discovery inventories; human policy approves consequential access |
| [Rules map](RULES-MAP.md) ([contract](../../docs/contracts/RULES-MAP.md)) | Human-approved durable rules, scoped through progressive disclosure |
| [Model routing](MODEL-ROUTING.md) | Humans approve tier policy; adapters maintain current model mappings; orchestrator records dispatch reasons |
| [Model dispatch](MODEL-DISPATCH.md) | Orchestrator resolves a tier through the active adapter and records the model override plus returned runtime evidence |
| [Parallel dispatch](PARALLEL-DISPATCH.md) ([contract](../../docs/contracts/PARALLEL-DISPATCH.md)) | Orchestrator records collision-safe batch selection, actual launches, first-event refill, and fan-in |
| [Codex agent dispatch](CODEX-AGENT-DISPATCH.md) | Codex orchestrator records role, minimal packet, native call, returned context/model evidence, and separation |
| [Execution budget](EXECUTION-BUDGET.md) | Orchestrator initializes and reconciles lineage counters; implementer records usage but cannot raise limits or reset lineage |
| [Root AGENTS bridge](ROOT-AGENTS-BRIDGE.md) | Installer or adoption lead adds one managed block without replacing host instructions |
| [Root Claude bridge](ROOT-CLAUDE-BRIDGE.md) | Installer or adoption lead adds one managed import block without replacing host instructions |
| Learning profile (`LEARNING-PROFILE.md`, `core-learning`/`full`) | User/learning subsystem under consent policy |
| Learning queue (`LEARNING-QUEUE.md`, `core-learning`/`full`) | Learning subsystem; user controls priorities |

Keep YAML scalar values concrete, retain required headings, and replace the task graph's JSON block with valid JSON. Run the validator after copying.
