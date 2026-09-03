# Accompanied delivery and executable acceptance

Product builds default to **accompanied delivery**: the agent works autonomously inside an approved block, then stops for the client at meaningful product milestones. This is independent of lane, pace, and technical assurance. It is not a pause after every task, every fixed number of tasks, or every passing test. Small decided fixes and maintenance remain continuous. A user may explicitly choose continuous delivery; record that choice without waiving other required decisions or safety gates.

## Plan with the client, execute inside the block

1. Reuse approved intent. Resolve consequential missing actors, customer/niche, business rules, exclusions, and success examples before implementation. Do not repeat discovery or invent domain facts.
2. Before each substantial block, summarize what the spec means in the user's language: outcome, a successful example, a rejected example, and what will be shown next. An already approved block needs no new permission. A new product choice does.
3. Plan a checkpoint at the **first usable vertical slice**, then at each material user-facing capability or uncertain direction before investing in dependent expansion. Group technical tasks into a demonstrable outcome. Hackathon mode keeps the first demo checkpoint; compress scope, not client participation.
4. At the checkpoint, show the runnable result or available evidence, checks and limitations, the relevant acceptance examples, and the proposed next block. Ask whether this result matches the client's intent and genuinely wait before dependent work. Do not ask merely whether to run more tests.
5. Record one human-owned item in `PENDING.md`; the executable graph links affected descendants through `product_requires`. Unrelated, already-authorized, collision-free work may continue. If none exists, yield the turn; do not poll for approval or invent busywork.
6. Approval must refer to this result and revision. Silence, elapsed time, a general instruction to finish, initial plan approval, or an agent's technical review is not milestone approval. Do not repeat a current recorded approval. Explicitly delegated continuous delivery removes optional product checkpoints, not mandatory authority gates.

The technical node can be `completed` while its product review remains `pending`. Do not call the product client-accepted or delivered when a required milestone is pending. Client feedback becomes a bounded correction when it preserves scope; new product direction requires the exact new decision. After changes, increment the acceptance revision, invalidate the old approval, and attach fresh demonstration evidence. Use a remediation node for code changes; do not reopen terminal lifecycle states or reset execution budgets.

For existing approved projects, preserve recorded interaction choices. If none exists, announce this default at the next substantial product block; do not restart onboarding or add retroactive pauses to completed work.

## Executable product gate

### Progressive scope closure

Initial discovery establishes direction and the first bounded slice, not blanket authority to invent all future features. Detail only the next approved block. Before a later functionality enters execution, resolve its inputs, rules, exclusions, and **completion conditions** through focused [feature discovery](../harness/playbooks/feature-discovery.md). If approved evidence does not determine a stopping condition, ask the client and help close it with concrete examples and options; never make up the answer to fill the graph. No repeated interview is needed for ordinary technical tasks inside a defined feature.

New executable nodes declare `scope_status: approved` only with a current approved scope/acceptance reference. Keep future ideas in the macro roadmap. If an existing graph already has an unresolved placeholder, use pending/blocked plus `scope_status: needs-discovery`; `schedule` defers it and `transition` cannot mark it ready, active, or completed. After the client approves the bounded feature and completion conditions, update the spec/decision reference and scope status, then reconcile other gates. Approval of this scope is distinct from evaluating its later implemented milestone.

The completed milestone carries this optional declaration in the executable graph:

```json
{
  "id": "FIRST-SLICE",
  "status": "completed",
  "acceptance_revision": 1,
  "product_review": {
    "status": "pending",
    "reviewed_revision": 1,
    "approved_by": null,
    "decision_ref": null,
    "evidence": ["demo:first-slice@1"]
  }
}
```

This fragment supplements the usual node fields. Each affected downstream node declares both `"depends_on": ["FIRST-SLICE"]` and `"product_requires": ["FIRST-SLICE"]`; preserve other dependencies. Keep affected nodes pending/blocked until the gate clears. They cannot be truthfully ready or active. Requiring a normal dependency also keeps product order in the existing cycle check, rather than creating a second graph.

After an actual human decision, the orchestrator records `status: approved`, matching `reviewed_revision`, `approved_by: human:<identity>`, a nonempty `decision_ref` pointing to that decision, and nonempty demonstration `evidence`. `changes-requested` and `rejected` remain blocked. Missing, stale, agent-owned, or empty approval never unlocks the dependency. Record approval and readiness reconciliation as one meaningful graph revision/event, with the related pending item resolved in the same operational step.

`schedule` defers declared gated nodes with `product-review:<id>`. The validator rejects false-ready/active claims. `transition` rejects attempts to mark affected nodes ready, active, or completed before their gates pass, for JSON graphs and Markdown executable JSON blocks. Technical `assurance_status: accepted` cannot unlock a product gate.

## Specs that test intent, not the implementation's assumptions

Every behavioral unit has concrete **input → expected result** examples, at least one meaningful rejected/boundary case, and failure/recovery behavior. Derive the oracle from approved intent, not from whatever the implementation currently returns. Do not require a generic domain questionnaire for unrelated work.

Example: a search for bakeries in São Paulo must include an in-scope bakery and exclude a bakery in another city and an unrelated São Paulo business. Specify AND/OR grouping, missing-location handling, and empty results before translating them into tests. A green test that expects the same incorrect OR expression as the code proves consistency, not correct product behavior. Have the client evaluate representative results at the first slice.

## Evidence-backed technical completion

Every new spec includes **"This task is complete only when..."** with numbered conditions describing successfully implemented behavior, not a checklist of coding actions. Mirror these in `acceptance_criteria`, for example `[{"id": "AC-001", "condition": "The scheduled search cycle retains only in-scope matches and exposes upstream failures"}]`. Record `verification.acceptance` as `[{"criterion": "AC-001", "result": "passed", "observed": "One matching result retained; injected timeout surfaced", "evidence": "run:cycle"}]`. Require exactly one passing result with observed behavior and evidence per criterion, pinned to the current `spec_revision`. Unknown, duplicate, missing, failed, or empty evidence cannot close the task. A remaining defect against a required condition is a blocker. Legacy nodes without declarations remain compatible; all newly planned nodes must declare the conditions.

For new nodes, pin `acceptance_revision`, `test_strategy`, and `runtime_smoke_required` during planning. Use `tdd` when required by the execution policy; `focused`/`verification-only`/`not-applicable` are explicit proportional alternatives, not a way to hide a missed mandatory RED. Runtime evidence is stored inline under `verification` on the node; link original command logs rather than copying them into extra artifacts.

```json
{
  "acceptance_revision": 1,
  "test_strategy": "tdd",
  "runtime_smoke_required": true,
  "verification": {
    "spec_revision": 1,
    "tdd": {
      "red": {"command": "pytest -k search_cycle", "exit_code": 1, "failure_kind": "behavior", "evidence": "run:red", "sequence": 1},
      "implementation_sequence": 2,
      "green": {"command": "pytest -k search_cycle", "exit_code": 0, "evidence": "run:green", "sequence": 3}
    },
    "runtime_smoke": {
      "command": "run controlled search cycle",
      "exit_code": 0,
      "evidence": "run:smoke",
      "expected": "only matching results; upstream failure becomes visible",
      "observed": "matching result retained; injected failure reported"
    }
  }
}
```

These illustrative commands are replaced by actual project commands. The runtime checks required fields, revision, integer exit codes, identical RED/GREEN command, behavioral failure classification, and positive RED < implementation < GREEN sequence. A syntax/import/environment failure is not a meaningful RED. Do not fabricate retroactive RED when code was written first: disclose the process failure, correct the test/spec under the existing bounded policy, and obtain any required exception instead of claiming TDD compliance.

Require an affected-flow smoke for automation/background jobs, runtime entrypoints, configuration consumers, and external integration paths. Exercise a controlled cycle through the real entrypoint with safe fixtures or a permitted test environment, including failure visibility. Verify renamed configuration at its consumer. Compilation and unit tests alone do not prove a job ran. Never contact production services, send messages, incur cost, or mutate customer data without authority; report unavailable capability and block the required evidence rather than substituting a green build.

The smoke may be an integration test that already exercises that path: reference its result, do not rerun the same global suite. Climb focused → workspace → integration → checkpoint → delivery only as needed. `transition` rejects completion with missing/failed/stale declared evidence; validation also detects false completion and scheduling rejects dependencies with invalid required completion evidence.

These are structural checks on **recorded evidence**, not execution attestation or proof of authentic human identity. Agent hosts must provide truthful command/decision references and obey the pause. Legacy JSON nodes without declarations remain compatible and gain no automatic evidence guarantee; adopt the fields on the next planned work. Legacy table-only Markdown cannot express these gates: the runtime rejects ready/active/completed transitions until it is migrated to the executable JSON block. Blocking/recovery transitions remain available. The Kit does not intercept arbitrary file edits or independently control the host's conversation.

## Keep the ceremony proportional

One meaningful state change means one graph transition, not a revision per tool call or sentence. Store check details in the existing inline verification/transition; do not clone records into handoffs without a consumer. Update `PENDING.md` only when human/macro state changes, and the rules map only when a durable rule changes. Client checkpoints use the existing graph and pending authority, not a new packet hierarchy. Brief progress messages do not require a full status form; explicit status/pending requests still receive the complete, current view.
