# Runtime state, events, and metrics

Version 0.7 adds standard-library runtime primitives without introducing a daemon.

## Graph transitions

Use `agent-harness transition <TASK-GRAPH.md|json> <task> <status> --expected-revision <n> --actor <id> --context <id>`. A sibling interprocess lock serializes real agent processes, and the compare-and-swap revision check rejects stale writers. A valid lifecycle transition updates status, releases ownership on completion/block, increments the revision, and adds exactly one transition entry through a flushed temporary file and atomic replacement.

`harness-state/events.jsonl` is the append-only technical history. Runtime integrations call `append_runtime_event` with the graph transaction/revisions; event IDs are idempotent and every record carries payload and chain hashes. `TASK-GRAPH.md` remains the current-state authority—events are recovery/audit history, not another scheduler.

## Run metrics

Every graph/full run records one `harness.runtime-metric/v1` row in `harness-state/metrics.jsonl`: lane, assurance, shape, artifacts created, ceremony/implementation duration, approvals, effective gate hits, target/actual duration, review outcome, graph revisions, remediation, repeated global checks, and host-reported tokens when available. Never estimate unavailable tokens.

Append a JSON payload with `agent-harness metric-record <run.json> harness-state/metrics.jsonl`. Summarize it with `agent-harness metrics harness-state/metrics.jsonl`. After the configured consecutive no-gate threshold, the summary suggests the next lighter lane instead of silently changing policy.

## Inactivity

`evaluate_inactivity` emits `warn-checkpoint` after a configured 60–90 seconds without a patch, check, or concrete discovery, and `interrupt-reassign` on the second consecutive occurrence. A declared long-running tool wait is exempt while the tool is observably active.
