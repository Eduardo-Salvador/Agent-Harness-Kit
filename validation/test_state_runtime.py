import json
import multiprocessing
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from agent_harness_kit.state_runtime import (
    CorruptLedgerError,
    DuplicateEventError,
    IllegalTransitionError,
    RevisionConflictError,
    append_runtime_event,
    evaluate_inactivity,
    record_metric,
    summarize_metrics,
    transition_task_graph,
    verify_event_chain,
)


def _transition_worker(path: str, queue) -> None:
    try:
        transition_task_graph(path, "T", "active", 1, "worker", "ctx")
        queue.put("success")
    except RevisionConflictError:
        queue.put("conflict")


def _event_worker(path: str, index: int, queue) -> None:
    try:
        append_runtime_event(
            path, event_id=f"event-{index}", transaction_id=f"tx-{index}",
            expected_revision=index, resulting_revision=index + 1, task=f"T-{index}",
            actor="worker", context=f"ctx-{index}", payload={"index": index},
            timestamp=f"2026-09-02T12:00:0{index}Z",
        )
        queue.put("success")
    except Exception as exc:  # pragma: no cover - returned for parent assertion
        queue.put(type(exc).__name__)


class GraphTransitionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_json_transition_is_cas_validated_and_releases_ownership(self):
        path = self.root / "TASK-GRAPH.json"
        path.write_text(json.dumps({
            "schema": "harness.task-graph/v1",
            "revision": 4,
            "tasks": {"TASK-1": {
                "status": "active", "lease": "lease-1",
                "execution_context": "ctx-1", "thread_ref": "thread-1",
            }},
            "transitions": [],
        }), encoding="utf-8")

        result = transition_task_graph(
            path, "TASK-1", "completed", expected_revision=4,
            actor="role:orchestrator", context="ctx-orch",
            timestamp="2026-09-02T12:00:00Z",
        )

        self.assertEqual(result["revision"], 5)
        task = result["tasks"]["TASK-1"]
        self.assertEqual(task["status"], "completed")
        self.assertIsNone(task["lease"])
        self.assertIsNone(task["execution_context"])
        self.assertIsNone(task["thread_ref"])
        self.assertEqual(len(result["transitions"]), 1)
        self.assertEqual(result["transitions"][0]["revision"], 5)

        with self.assertRaises(RevisionConflictError):
            transition_task_graph(path, "TASK-1", "blocked", 4, "actor", "ctx")

    def test_illegal_transition_does_not_mutate_file(self):
        path = self.root / "TASK-GRAPH.json"
        original = {"revision": 1, "tasks": [{"id": "T", "status": "pending"}]}
        path.write_text(json.dumps(original), encoding="utf-8")
        with self.assertRaises(IllegalTransitionError):
            transition_task_graph(path, "T", "completed", 1, "actor", "ctx")
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), original)

    def test_markdown_transition_updates_frontmatter_table_and_one_log_entry(self):
        path = self.root / "TASK-GRAPH.md"
        path.write_text(
            "---\nschema: harness.task-graph/v1\nrevision: 7\nupdated_at: old\n"
            "updated_by: old\n---\n\n# Task graph\n\n"
            "| ID | Status | Agent/context |\n| --- | --- | --- |\n"
            "| TASK-7 | active | builder / ctx-7 |\n\n"
            "## Transition log\n- r7: started\n",
            encoding="utf-8",
        )
        transition_task_graph(
            path, "TASK-7", "blocked", 7, "role:orchestrator", "ctx-o",
            reason="dependency missing", timestamp="2026-09-02T12:00:00Z",
        )
        text = path.read_text(encoding="utf-8")
        self.assertIn("revision: 8", text)
        self.assertIn("| TASK-7 | blocked | unassigned / released |", text)
        self.assertEqual(text.count("- r8:"), 1)

    def test_markdown_transition_updates_executable_json_graph_block(self):
        path = self.root / "TASK-GRAPH.md"
        path.write_text(
            "---\nschema: harness.task-graph/v1\nrevision: 2\nupdated_at: old\nupdated_by: old\n---\n\n"
            "# Task graph\n\n```json\n"
            + json.dumps({"nodes": [{"id": "TASK-2", "status": "active", "assigned_to": "agent:x", "thread_ref": "ctx-x"}]}, indent=2)
            + "\n```\n\n## Transition log\n\n- r2: started\n",
            encoding="utf-8",
        )

        result = transition_task_graph(
            path, "TASK-2", "completed", 2, "role:orchestrator", "ctx-o",
            timestamp="2026-09-02T12:00:00Z",
        )

        text = path.read_text(encoding="utf-8")
        payload = json.loads(text.split("```json\n", 1)[1].split("\n```", 1)[0])
        self.assertEqual(result["revision"], 3)
        self.assertEqual(payload["nodes"][0]["status"], "completed")
        self.assertIsNone(payload["nodes"][0]["assigned_to"])
        self.assertIsNone(payload["nodes"][0]["thread_ref"])
        self.assertEqual(text.count("- r3:"), 1)

    def test_cross_process_cas_allows_only_one_writer(self):
        path = self.root / "TASK-GRAPH.json"
        path.write_text(json.dumps({"revision": 1, "tasks": {"T": {"status": "ready"}}, "transitions": []}), encoding="utf-8")
        context = multiprocessing.get_context("spawn")
        queue = context.Queue()
        workers = [context.Process(target=_transition_worker, args=(str(path), queue)) for _ in range(2)]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(15)
            self.assertEqual(worker.exitcode, 0)
        outcomes = sorted(queue.get(timeout=2) for _ in workers)
        self.assertEqual(outcomes, ["conflict", "success"])
        graph = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(graph["revision"], 2)
        self.assertEqual(len(graph["transitions"]), 1)


class EventLedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "events.jsonl"

    def test_event_append_is_idempotent_and_hash_chain_verifies(self):
        kwargs = dict(
            event_id="event-1", transaction_id="tx-1", expected_revision=2,
            resulting_revision=3, task="TASK-1", actor="orchestrator",
            context="ctx", payload={"status": "active"},
            timestamp="2026-09-02T12:00:00Z",
        )
        first = append_runtime_event(self.path, **kwargs)
        duplicate = append_runtime_event(self.path, **kwargs)
        self.assertEqual(first, duplicate)
        self.assertEqual(len(self.path.read_text(encoding="utf-8").splitlines()), 1)
        report = verify_event_chain(self.path)
        self.assertTrue(report["valid"])
        self.assertEqual(report["event_count"], 1)

    def test_retry_without_fixed_timestamp_is_idempotent(self):
        kwargs = dict(
            event_id="retry-event", transaction_id="retry-tx", expected_revision=0,
            resulting_revision=1, task="T", actor="A", context="C", payload={"ok": True},
        )
        first = append_runtime_event(self.path, **kwargs)
        second = append_runtime_event(self.path, **kwargs)
        self.assertEqual(first["event_hash"], second["event_hash"])
        self.assertEqual(verify_event_chain(self.path)["event_count"], 1)

        changed = dict(kwargs)
        changed["payload"] = {"ok": False}
        with self.assertRaises(DuplicateEventError):
            append_runtime_event(self.path, **changed)

    def test_torn_or_corrupt_ledger_is_rejected(self):
        append_runtime_event(
            self.path, event_id="e", transaction_id="t", expected_revision=0,
            resulting_revision=1, task="T", actor="A", context="C", payload={},
        )
        with self.path.open("ab") as stream:
            stream.write(b'{"schema":')
        with self.assertRaises(CorruptLedgerError):
            verify_event_chain(self.path)

    def test_cross_process_appends_preserve_hash_chain(self):
        context = multiprocessing.get_context("spawn")
        queue = context.Queue()
        workers = [context.Process(target=_event_worker, args=(str(self.path), index, queue)) for index in range(4)]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(15)
            self.assertEqual(worker.exitcode, 0)
        self.assertEqual([queue.get(timeout=2) for _ in workers].count("success"), 4)
        self.assertEqual(verify_event_chain(self.path)["event_count"], 4)


class MetricTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "metrics.jsonl"

    def test_metric_aggregation_and_no_gate_lane_suggestion(self):
        for index in range(3):
            record_metric(
                self.path, lane="full-harness", assurance="light",
                harness_shape="compact", artifacts_created=2,
                ceremony_ms=100, implementation_ms=900,
                human_approvals=0, gate_hits=[], target_minutes=1,
                actual_minutes=2 if index == 0 else 1,
                task=f"TASK-{index}", graph_revisions=2,
                first_pass_accepted=index != 2,
                remediation=index == 2,
                global_regressions=["suite-a"] if index < 2 else [],
                review_verdict="bogus" if index == 2 else "accept",
            )
        summary = summarize_metrics(self.path, no_gate_threshold=3)
        self.assertEqual(summary["runs"], 3)
        self.assertEqual(summary["first_pass_acceptance"]["accepted"], 2)
        self.assertAlmostEqual(summary["governance_product_ratio"], 1 / 9)
        self.assertAlmostEqual(summary["governance_share"], 0.1)
        self.assertEqual(summary["repeated_global_regressions"], {"suite-a": 2})
        self.assertAlmostEqual(summary["remediation_ratio"], 1 / 3)
        self.assertEqual(summary["graph_revisions_per_task"]["average"], 2)
        self.assertEqual(summary["invalid_review_verdict_count"], 1)
        self.assertEqual(summary["target_overrun"]["count"], 1)
        self.assertEqual(summary["suggested_lane"], "graph-only")


class InactivityTests(unittest.TestCase):
    def test_inactivity_stages_and_long_wait_exemption(self):
        now = datetime(2026, 9, 2, 12, 2, tzinfo=timezone.utc)
        last = datetime(2026, 9, 2, 12, 0, tzinfo=timezone.utc)
        warning = evaluate_inactivity(last, now=now, consecutive_occurrences=0)
        self.assertEqual(warning["action"], "warn-checkpoint")
        second = evaluate_inactivity(last, now=now, consecutive_occurrences=1)
        self.assertEqual(second["action"], "interrupt-reassign")
        exempt = evaluate_inactivity(
            last, now=now, consecutive_occurrences=9,
            declared_long_running_tool_wait=True,
        )
        self.assertEqual(exempt["action"], "exempt")


if __name__ == "__main__":
    unittest.main()
