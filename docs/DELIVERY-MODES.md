# Delivery modes

Offer three user-facing presets. They configure participation and pace, not model choice, agent count, execution lane, assurance, or verification quality.

| Preset | User experience | Existing runtime mode | Interaction | Optional client checkpoints |
| --- | --- | --- | --- | --- |
| `accompanied` (default) | Define features together, implement a block, demonstrate, then evaluate together. | `delivery` | `accompanied` | First usable slice and material capabilities. |
| `autonomous` | Agree on scope and completion conditions up front; implement, test, correct, and finish that envelope end to end. | `delivery` | `continuous` | None unless separately requested. |
| `hackathon` | Reach one working demo inside the timebox; compress discovery and cut secondary scope. | `hackathon` | `accompanied` | First demo before dependent expansion. |

## Select and remember

During first run, visibly welcome the user and ask the unanswered delivery-mode preference in one cohesive kickoff question, combining missing project intent when needed. Offer standard accompanied delivery, autonomous end-to-end delivery, and hackathon mode. Present accompanied as the default, include the resolved choice in consolidated context approval, and honor an explicit alternative without asking again. A simple greeting such as "oi" is enough to start this handshake in an uninitialized project; no activation prompt or implementation request is needed on hosts that load root instructions. Correct questions without the welcome are incomplete. If the user delegates the choice or has no preference, use accompanied. Do not repeat the first-run welcome for an initialized project.

Recognize natural language such as “build this with me,” “execute the agreed scope end to end,” and “prioritize my hackathon demo.” Autonomous means less client involvement, **not one agent**: parallel workers remain capability- and ownership-bound. Do not infer an agent-count restriction from delivery preference.

Record `delivery_preset`, existing `mode`, and `interaction` in `PROJECT-CONTEXT.md`, together with the user's decision reference, approved scope, completion conditions, cost/authority limits, and any checkpoint override. Retain existing approved learning consent and the `+learning` suffix when applicable; selecting a preset never activates learning or creates notes. New context starts without learning unless its separate consent/destination gate is completed.

```yaml
delivery_preset: autonomous
mode: delivery
interaction: continuous
```

These fields describe the project policy. They do not replace task-specific gates or the approval of product scope. An agent selecting a mode must persist the policy through normal context revision and report the result. A command's output alone is not a saved or approved selection.

The installer prepares the root instruction files; it does not send a message by itself. Start a fresh agent context at the project root after installation. Hosts that disable or ignore project instructions cannot be guaranteed to follow the handshake; use `agent-harness doctor` to inspect entrypoints and `agent-harness prompt` as the explicit fallback.

## Inspect from the CLI

```bash
agent-harness delivery-mode
agent-harness delivery-mode autonomous
agent-harness delivery-mode hackathon
```

The command returns `harness.delivery-mode/v1` JSON describing the preset, runtime mode, interaction, checkpoints, scope policy, required verification, host-capability parallelism, unchanged learning activation, and `applies_changes: false`. It is a read-only inspector: it does not read/change the current project policy, install files, start agents, clear gates, or authorize work. No argument previews the default, not the active project's saved mode. Unknown presets fail instead of silently selecting a default.

## Execute each mode

- **Accompanied:** follow [accompanied delivery](ACCOMPANIED-DELIVERY.md). Detail the next approved block; ask when a feature rule or stopping condition is unresolved; demonstrate and actually wait at the planned milestones before dependent expansion.
- **Autonomous:** close the overall approved envelope and acceptance boundary at the start. Decompose it progressively without requiring evaluation between every feature. Continue implementation, verification, and bounded correction automatically inside that envelope. Do not create optional `product_requires` gates merely because a new feature is reached. A missing consequential business rule still needs a decision; end-to-end execution is not permission to invent scope. Report progress and a verified final result rather than going silent.
- **Hackathon:** follow [hackathon delivery](../harness/playbooks/hackathon-delivery.md): at most two cohesive discovery questions unless consequential authority/safety is missing, one primary demo path, visible shortcuts, proportional checks, and the first-demo evaluation. Do not turn every technical unit into a client review.

All modes require explicit completion conditions, truthful criterion-level evidence, the selected test strategy, required affected-flow checks, bounded recovery, and applicable independent assurance. All stop at unavailable required capabilities, unresolved consequential scope, exhausted budgets, or authority limits. Small decided fixes retain their lightweight route in every preset.

## Switching and existing projects

An explicit “continue autonomously” or “I want to evaluate the next features” changes future participation after the current bounded operation. Record the decision and context revision; preserve work, leases, evidence, budgets, and consent. Do not restart discovery, recreate the graph, or silently cancel active work.

Changing a preset never makes an existing `product_requires`, assurance, or scope gate pass. A previously declared optional client checkpoint may be removed only through an explicit scoped human waiver recorded by the orchestrator; never fabricate `product_review: approved`. Mandatory safety, cost, publication, and authority gates cannot be waived by a generic mode switch.

Preserve legacy approved choices. Existing `mode: delivery` plus continuous interaction corresponds to autonomous; delivery with accompanied interaction corresponds to accompanied. Existing hackathon or `+learning` modes retain their approved pace, interaction overrides, and consent. If interaction is missing, announce the default at the next substantial product block without restarting onboarding. If saved fields conflict, report that exact conflict and do not guess a broader authority.
