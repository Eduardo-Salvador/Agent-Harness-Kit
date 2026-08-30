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
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(cli.doctor(root), 0)
            self.assertIn("is ready", output.getvalue())

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
