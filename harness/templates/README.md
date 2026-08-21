# Operational templates

Copy these templates into the runtime state location selected by the project. Phase 2 examples use `examples/*/state/`; the permanent runtime location remains an open decision.

| Template | Authority that updates instances |
| --- | --- |
| [Project context](PROJECT-CONTEXT.md) | Discovery drafts; human approves |
| [Task graph](TASK-GRAPH.md) | Orchestrator only |
| [Pending work](PENDING.md) | Orchestrator maintains human actions and macro project completion; technical execution stays in the graph |
| [Status](STATUS.md) | Orchestrator derives an inspectable user update from project context, pending authority, and graph |
| [Task brief](TASK.md) | Orchestrator; implementer updates attempt status only |
| [Handoff](HANDOFF.md) | Assigned implementer; includes the plain-language user closeout |
| [Review result](REVIEW.md) | Independent reviewer; one initial review plus at most one focused re-review |
| [Decision](DECISION.md) | Proposer drafts; named authority decides |
| [Migration manifest](MIGRATION-MANIFEST.md) | Adoption lead inventories; humans approve semantics/cutover |
| [Coexistence](COEXISTENCE.md) | Existing-harness owner + project owner |
| [Adapter binding](ADAPTER-BINDING.md) | Adapter maintainer; existing authority remains referenced |
| [Capability manifest](CAPABILITY-MANIFEST.md) | Discovery inventories; human policy approves consequential access |
| [Rules map](RULES-MAP.md) | Human-approved durable rules, scoped through progressive disclosure |
| [Model routing](MODEL-ROUTING.md) | Humans approve tier policy; adapters maintain current model mappings; orchestrator records dispatch reasons |
| [Execution budget](EXECUTION-BUDGET.md) | Orchestrator initializes and reconciles lineage counters; implementer records usage but cannot raise limits or reset lineage |
| [Root AGENTS bridge](ROOT-AGENTS-BRIDGE.md) | Installer or adoption lead adds one managed block without replacing host instructions |
| [Root Claude bridge](ROOT-CLAUDE-BRIDGE.md) | Installer or adoption lead adds one managed import block without replacing host instructions |
| Learning profile (`LEARNING-PROFILE.md`, `core-learning`/`full`) | User/learning subsystem under consent policy |
| Learning queue (`LEARNING-QUEUE.md`, `core-learning`/`full`) | Learning subsystem; user controls priorities |

Keep YAML scalar values concrete, retain required headings, and replace the task graph's JSON block with valid JSON. Run the validator after copying.
