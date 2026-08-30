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
- When parallel capacity is proven, consume the deterministic `agent-harness schedule` batch, reserve it against the expected graph revision, launch every selected child before waiting, persist `harness.parallel-dispatch/v1`, and refill the first freed slot. A planned batch without adapter context references is not execution.
- Report the model catalog and model/reasoning override support per dispatch surface. Return the selected model, confirmation, context reference, and response evidence in `harness.model-dispatch/v1`.
- After verification, prefer `spawn_subagent` for review when proven. Otherwise use a new visible/manual clean context and send only the pinned SPEC-led review packet; prompt or conversation memory is not acceptance authority.

## First-run approximation

Before first-run, an explicit edit may use the neutral `direct-trivial` fast path only when it is a localized presentation/static-content mechanic with no behavior, rule, state, contract, data, dependency, risk, or cross-workstream impact. Perform it directly with a minimal check and concise closeout; create no harness artifacts. Promote on uncertainty.

Before planning, the host or agent performs the side-effect-free initialization test in `harness/playbooks/first-run.md`. If no approved context exists at the neutral default path, it surfaces the discovery interviewer role. A runtime without startup hooks performs this check at the beginning of each operational session; approved versioned state makes the check idempotent.

For mature existing harnesses, use a namespaced adapter binding with source identity, provenance backlinks, and explicit precedence. Existing prompts/tool declarations do not prove runtime capability, and generated worktree state is not authoritative context.
