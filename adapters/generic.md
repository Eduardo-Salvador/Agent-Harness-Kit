# Generic adapter contract

## Capability manifest

An implementation must report, without side effects:

| Capability | Neutral operation | Safe degradation |
| --- | --- | --- |
| Artifact I/O | Read/write scoped files with expected revision | Block if atomic/auditable revision cannot be preserved |
| Isolation | Create/identify/release task boundary | Serialize in an exclusive directory/branch |
| Execution | Run an allowed check with timeout/cancel | Declared manual evidence; never fabricate a run |
| Delegation | Start bounded implementer contexts and fresh SPEC-led review contexts | Manually open a clean reviewer context; never review inside the implementer context |
| Visible thread lifecycle | Create/resume/message/close a user-visible chat or task | Internal subagent, manually opened fresh context, or serialized artifact handoff |
| Parallel contexts | Run independently leased contexts concurrently | Serialize dependency-ready tasks without changing graph semantics |
| Model override | Enumerate current models/efforts and apply explicit values when creating or delegating a task | Fresh manual selection or block; never silently use the host default |
| Approval | Present choice and record disposition | Stop and request human disposition |
| Events | Announce artifact transition | Periodically reconcile canonical files |
| Secrets/network | Inject scoped capability under policy | `approval-required` or `unavailable` |
| Integration | Apply accepted change with provenance | Human-mediated integration with recorded evidence |

## Result envelope

Every operation returns capability name, status, adapter/version identity, start/end time when relevant, concise result, and durable evidence reference. Errors are data, not hidden retries.

## Rules

- Normalize paths before enforcing scope.
- Default to no network, no secrets, no destructive action, and repository-scoped writes until policy grants more.
- Never expose credentials in artifacts.
- Report degradation before dispatch; block when the fallback violates core invariants.
- Report `spawn_subagent`, `create_thread`, `resume_thread`, `message_thread`, `close_thread`, and `parallel_contexts` separately; one does not imply another. Parallel evidence includes numeric child capacity, quota sharing, and a first-completion/attention wait operation.
- When numeric capacity greater than one is proven, launch every collision-free selected child before waiting, report the active worker count, and refill the first freed slot. Warn after 60–90 seconds without observable progress; on the second consecutive occurrence interrupt and reassign/serialize within budget.
- Report the model catalog and model/reasoning override support per dispatch surface. Return the selected model, confirmation, context reference, and response evidence in `harness.model-dispatch/v1`.
- For `assurance: light|full`, use a separate reviewer and send the pinned SPEC-led packet; `none` uses executor verification. Create a handoff only for an actual receiving context.

## First-run approximation

Read-only audits, explanations, and diagnosis do not trigger first-run. Before first-run, an explicit localized static edit may use `direct-trivial`; perform it with a minimal check and no Harness artifacts.

Before planning, the host or agent performs the side-effect-free initialization test in `harness/playbooks/first-run.md`. If no approved context exists at the neutral default path, it surfaces the discovery interviewer role. A runtime without startup hooks performs this check at the beginning of each operational session; approved versioned state makes the check idempotent.

For mature existing harnesses, use a namespaced adapter binding with source identity, provenance backlinks, and explicit precedence. Existing prompts/tool declarations do not prove runtime capability, and generated worktree state is not authoritative context.
