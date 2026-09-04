#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent_harness_kit import cli


class CliTests(unittest.TestCase):
    def test_route_prints_machine_readable_preflight_decision(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(
                cli.main(
                    [
                        "route",
                        "Fix the button label typo",
                        "--mode",
                        "auto",
                        "--graph-bound",
                        "--workstreams",
                        "1",
                    ]
                ),
                0,
            )
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["route"], "graph-only")
        self.assertEqual(payload["harness_shape"], "compact")

    def test_route_can_select_eligible_graph_only_work(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(
                cli.main(
                    [
                        "route",
                        "Execute a tarefa já especificada",
                        "--graph-bound",
                        "--graph-only-eligible",
                    ]
                ),
                0,
            )
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["route"], "graph-only")

    def test_route_explicit_vibe_is_forwarded_to_the_engine(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(cli.main(["route", "Polish this interaction", "--mode", "vibe"]), 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["route"], "vibe")
        self.assertEqual(payload["durable_artifacts"], [])

    def test_route_explicit_full_forces_full_harness(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(cli.main(["route", "Polish this interaction", "--mode", "full"]), 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["route"], "full-harness")
        self.assertEqual(payload["reason"], "explicit-full")

    def test_route_accepts_adaptive_controls(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(
                cli.main(
                    [
                        "route",
                        "Coordinate frontend and backend with an API contract",
                        "--mode",
                        "graph-only",
                        "--assurance",
                        "none",
                        "--shape",
                        "compact",
                        "--agents",
                        "1",
                        "--workstreams",
                        "2",
                        "--model-capability",
                        "strong",
                    ]
                ),
                0,
            )
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["route"], "graph-only")
        self.assertEqual(payload["assurance"], "none")
        self.assertEqual(payload["harness_shape"], "compact")
        self.assertIn("minimal_artifacts", payload)
        self.assertIn("explicit-assurance-below-risk-recommendation", payload["warnings"])

    def test_route_full_condition_flags(self) -> None:
        for flag in ("--human-loop", "--audit-required"):
            with self.subTest(flag=flag):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(cli.main(["route", "Fix the typo", flag]), 0)
                self.assertEqual(json.loads(output.getvalue())["route"], "full-harness")

    def test_route_agents_must_be_positive(self) -> None:
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            with self.assertRaises(SystemExit) as raised:
                cli.main(["route", "Fix the typo", "--agents", "0"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("positive integer", error.getvalue())

    def test_route_rejects_non_positive_workstream_count(self) -> None:
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            with self.assertRaises(SystemExit) as raised:
                cli.main(["route", "Fix the typo", "--workstreams", "0"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("positive integer", error.getvalue())

    def test_install_defaults_to_current_directory_and_core(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            installer = type(
                "Installer",
                (),
                {
                    "InstallError": RuntimeError,
                    "install": staticmethod(lambda profile, path, dry_run: [f"{profile}|{Path(path).resolve()}|{dry_run}"]),
                },
            )
            output = io.StringIO()
            with patch.object(cli, "installer_module", return_value=installer), patch.object(Path, "cwd", return_value=Path(temporary)), contextlib.redirect_stdout(output):
                result = cli.main(["install", "--dry-run"])
            self.assertEqual(result, 0)
            self.assertIn(f"WOULD: core|{Path(temporary).resolve()}|True", output.getvalue())

    def test_prompt_uses_installer_contract(self) -> None:
        installer = type("Installer", (), {"ACTIVATION_PROMPT": "activate safely"})
        output = io.StringIO()
        with patch.object(cli, "installer_module", return_value=installer), contextlib.redirect_stdout(output):
            self.assertEqual(cli.main(["prompt"]), 0)
        self.assertEqual(output.getvalue().strip(), "activate safely")

    def test_doctor_reports_ready_installation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "agent-harness-kit").mkdir()
            for item in (root / "AGENTS.md", root / "CLAUDE.md", root / "agent-harness-kit" / "PACKAGE-MANIFEST.json"):
                item.write_text("ok\n", encoding="utf-8")
            (root / "agent-harness-kit" / "PACKAGE-MANIFEST.json").write_text(
                json.dumps({"schema": "agent-harness-kit.runtime-manifest/v1"}), encoding="utf-8",
            )
            output = io.StringIO()
            with patch.object(cli.runtime_validation, "validate_runtime_install", return_value=[]), contextlib.redirect_stdout(output):
                self.assertEqual(cli.doctor(root), 0)
            self.assertIn("is ready", output.getvalue())

    def test_doctor_rejects_runtime_integrity_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "agent-harness-kit").mkdir()
            for item in (root / "AGENTS.md", root / "CLAUDE.md", root / "agent-harness-kit" / "PACKAGE-MANIFEST.json"):
                item.write_text("ok\n", encoding="utf-8")
            (root / "agent-harness-kit" / "PACKAGE-MANIFEST.json").write_text(
                json.dumps({"schema": "agent-harness-kit.runtime-manifest/v1"}), encoding="utf-8",
            )
            output = io.StringIO()
            with patch.object(
                cli.runtime_validation, "validate_runtime_install", return_value=["runtime.file-hash: AGENTS.md"]
            ), contextlib.redirect_stdout(output):
                self.assertEqual(cli.doctor(root), 1)
            self.assertIn("runtime.file-hash", output.getvalue())

    def test_doctor_delegates_expanded_profile_to_bundled_validator(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            kit = root / "agent-harness-kit"
            kit.mkdir()
            (root / "AGENTS.md").write_text("agents\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("claude\n", encoding="utf-8")
            (kit / "PACKAGE-MANIFEST.json").write_text(
                json.dumps({"profile": "full", "files": []}), encoding="utf-8",
            )
            completed = type("Completed", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            output = io.StringIO()
            with patch.object(cli, "run_expanded_validator", return_value=completed) as validator, contextlib.redirect_stdout(output):
                self.assertEqual(cli.doctor(root), 0)
            self.assertEqual(validator.call_args.args[0], kit.resolve())
            self.assertIn("is ready", output.getvalue())

    def test_validate_reports_compact_manifest_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            kit = root / "agent-harness-kit"
            kit.mkdir()
            manifest = {
                "schema": "agent-harness-kit.runtime-manifest/v1",
                "profile": "core",
                "version": "9.9.9",
                "files": [{"path": "AGENTS.md"}],
            }
            (kit / "PACKAGE-MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
            output = io.StringIO()
            with patch.object(cli.runtime_validation, "validate_runtime_install", return_value=[]), contextlib.redirect_stdout(output):
                self.assertEqual(cli.main(["validate", str(root)]), 0)
            self.assertEqual(json.loads(output.getvalue())["profile"], "core")

    def test_validate_delegates_expanded_profile_to_bundled_validator(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            kit = root / "agent-harness-kit"
            kit.mkdir()
            (kit / "PACKAGE-MANIFEST.json").write_text(
                json.dumps({"profile": "full", "files": []}), encoding="utf-8",
            )
            completed = type("Completed", (), {"returncode": 0})()
            with patch.object(cli, "run_expanded_validator", return_value=completed) as validator:
                self.assertEqual(cli.main(["validate", str(root)]), 0)
            self.assertEqual(validator.call_args.args[0], kit.resolve())

    def test_validate_rejects_unknown_path_without_source_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            error = io.StringIO()
            with patch.object(cli, "source_root", side_effect=AssertionError("unexpected fallback")), contextlib.redirect_stderr(error):
                self.assertEqual(cli.main(["validate", str(root)]), 2)
            self.assertIn("no compact installation or source checkout", error.getvalue())

    def test_scaffold_list_reports_unreadable_template_pack_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            kit = root / "agent-harness-kit"
            kit.mkdir()
            (kit / "PACKAGE-MANIFEST.json").write_text(
                json.dumps({"schema": "agent-harness-kit.runtime-manifest/v1"}), encoding="utf-8",
            )
            error = io.StringIO()
            with contextlib.redirect_stderr(error):
                self.assertEqual(cli.main(["scaffold", "--list", "--path", str(root)]), 2)
            self.assertIn("template pack is missing", error.getvalue())

    def test_schedule_prints_machine_readable_ready_batch(self) -> None:
        graph = {
            "nodes": [
                {"id": "A", "status": "ready", "depends_on": [], "assurance_requires": [], "write_set": ["src/a/**"]},
                {"id": "B", "status": "ready", "depends_on": [], "assurance_requires": [], "write_set": ["src/b/**"]},
            ]
        }
        output = io.StringIO()
        with patch.object(cli.scheduler, "load_graph", return_value=graph), contextlib.redirect_stdout(output):
            self.assertEqual(cli.main(["schedule", "graph.md", "--capacity", "2"]), 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["selected"], ["A", "B"])
        self.assertEqual(payload["schema"], "harness.parallel-dispatch-plan/v1")

    def test_preflight_prints_machine_readable_result_and_exit_status(self) -> None:
        result = {"schema": "harness.preflight/v1", "status": "blocked", "blockers": ["script:test"]}
        output = io.StringIO()
        with patch.object(cli.preflight, "run_preflight", return_value=result) as run, contextlib.redirect_stdout(output):
            self.assertEqual(
                cli.main(["preflight", ".", "--path", "src/app.py", "--script", "test", "--workers", "2"]),
                1,
            )
        self.assertEqual(json.loads(output.getvalue()), result)
        self.assertEqual(run.call_args.kwargs["required_scripts"], ["test"])
        self.assertEqual(run.call_args.kwargs["workers"], 2)

    def test_transition_uses_compare_and_swap_inputs(self) -> None:
        result = {"revision": 8, "transition": {"task": "TASK-7", "to": "completed"}}
        output = io.StringIO()
        with patch.object(cli.state_runtime, "transition_task_graph", return_value=result) as transition, contextlib.redirect_stdout(output):
            self.assertEqual(
                cli.main([
                    "transition", "TASK-GRAPH.md", "TASK-7", "completed",
                    "--expected-revision", "7", "--actor", "orchestrator", "--context", "ctx-1",
                ]),
                0,
            )
        self.assertEqual(json.loads(output.getvalue()), result)
        self.assertEqual(transition.call_args.args[3], 7)

    def test_metrics_summary_is_machine_readable(self) -> None:
        result = {"runs": 3, "suggested_lane": "graph-only"}
        output = io.StringIO()
        with patch.object(cli.state_runtime, "summarize_metrics", return_value=result), contextlib.redirect_stdout(output):
            self.assertEqual(cli.main(["metrics", "metrics.jsonl", "--no-gate-threshold", "3"]), 0)
        self.assertEqual(json.loads(output.getvalue()), result)

    def test_metric_record_appends_declared_run_payload(self) -> None:
        payload = {"lane": "vibe", "assurance": "none", "harness_shape": "none"}
        result = {"schema": "harness.runtime-metric/v1", **payload}
        output = io.StringIO()
        with patch.object(Path, "read_text", return_value=json.dumps(payload)), patch.object(
            cli.state_runtime, "record_metric", return_value=result
        ) as record, contextlib.redirect_stdout(output):
            self.assertEqual(cli.main(["metric-record", "run.json", "metrics.jsonl"]), 0)
        self.assertEqual(json.loads(output.getvalue()), result)
        self.assertEqual(record.call_args.args[0].name, "metrics.jsonl")
        self.assertEqual(record.call_args.kwargs["lane"], "vibe")

    def test_codex_dispatch_prints_native_call_plan(self) -> None:
        request = {
            "task": {
                "id": "TASK-7",
                "revision": 1,
                "task_spec": "tasks/TASK-7.md",
                "agent_role": "role:generic-specialist",
            },
            "purpose": "implementation",
            "model_dispatch": {
                "id": "model-7@1",
                "status": "resolved",
                "selected_model": "gpt-5.6-terra",
                "reasoning_effort": "medium",
                "override_confirmed": True,
            },
            "capabilities": {
                "spawn_subagent": {
                    "available": True,
                    "operation": "spawn_agent",
                    "evidence": "host@1",
                }
            },
        }
        output = io.StringIO()
        with patch.object(Path, "read_text", return_value=json.dumps(request)), contextlib.redirect_stdout(output):
            self.assertEqual(cli.main(["codex-dispatch", "request.json"]), 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["schema"], "harness.codex-agent-dispatch-plan/v1")
        self.assertEqual(payload["native_call"]["operation"], "spawn_agent")

    def test_codex_dispatch_records_adapter_response(self) -> None:
        plan = {
            "schema": "harness.codex-agent-dispatch-plan/v1",
            "status": "ready-to-dispatch",
            "task": "TASK-7@1",
            "purpose": "implementation",
            "agent_identity": "agent:implementer:TASK-7:attempt-1",
            "role": {"requested": "role:generic-specialist", "executor": "role:generic-specialist", "role_file": "harness/roles/generic-specialist.md"},
            "context_packet": {"task_spec": "tasks/TASK-7.md"},
            "model": {"requested": "gpt-5.6-terra", "reasoning_effort": "medium", "dispatch_ref": "model-7@1"},
            "separation": {"implementer_identity": "unassigned", "implementer_context_ref": "unassigned", "fresh_context_required": False},
            "native_call": {"operation": "spawn_agent", "arguments": {}},
        }
        response = {
            "agent_id": "agent-7",
            "operation_id": "spawn-7",
            "accepted_model": "gpt-5.6-terra",
            "accepted_reasoning_effort": "medium",
        }
        output = io.StringIO()
        with patch.object(Path, "read_text", side_effect=[json.dumps(plan), json.dumps(response)]), contextlib.redirect_stdout(output):
            self.assertEqual(cli.main(["codex-dispatch", "plan.json", "--response", "response.json"]), 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["schema"], "harness.codex-agent-dispatch/v1")
        self.assertEqual(payload["execution_context_ref"], "codex:agent-7")


if __name__ == "__main__":
    unittest.main()
