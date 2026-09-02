#!/usr/bin/env python3

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent_harness_kit.preflight import run_preflight


class PreflightTests(unittest.TestCase):
    def test_reports_missing_project_inputs_before_planning(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temporary:
            root = Path(temporary)
            (root / "package.json").write_text(json.dumps({"scripts": {"test": "pytest"}}), encoding="utf-8")
            result = run_preflight(
                root,
                required_paths=["src/missing.ts"],
                required_scripts=["test", "test:integration"],
                required_env=["MISSING_PREFLIGHT_SECRET"],
                required_commands=["definitely-not-a-real-command"],
                browser="required-unavailable",
                workers=0,
            )

        self.assertEqual(result["schema"], "harness.preflight/v1")
        self.assertEqual(result["status"], "blocked")
        self.assertIn("path:src/missing.ts", result["blockers"])
        self.assertIn("script:test:integration", result["blockers"])
        self.assertIn("env:MISSING_PREFLIGHT_SECRET", result["blockers"])
        self.assertIn("command:definitely-not-a-real-command", result["blockers"])
        self.assertIn("browser", result["blockers"])
        self.assertIn("workers", result["blockers"])
        self.assertNotIn("pytest", json.dumps(result))

    def test_passes_and_never_exposes_environment_values(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temporary:
            root = Path(temporary)
            (root / "src").mkdir()
            (root / "src" / "app.py").write_text("", encoding="utf-8")
            (root / "package.json").write_text(json.dumps({"scripts": {"test": "pytest"}}), encoding="utf-8")
            with patch.dict("os.environ", {"PREFLIGHT_TOKEN": "super-secret-value"}):
                result = run_preflight(
                    root,
                    required_paths=["src/app.py"],
                    required_scripts=["test"],
                    required_env=["PREFLIGHT_TOKEN"],
                    required_commands=["python"],
                    browser="not-required",
                    workers=2,
                    validator="not-required",
                )

        self.assertEqual(result["status"], "passed")
        self.assertNotIn("super-secret-value", json.dumps(result))

    def test_checks_env_consumer_names_native_probe_and_sandbox(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temporary:
            root = Path(temporary)
            (root / "consumer.py").write_text("token = os.environ['EXPECTED_TOKEN']\n", encoding="utf-8")
            completed = type("Completed", (), {"returncode": 0})()
            with patch("agent_harness_kit.preflight.subprocess.run", return_value=completed) as run:
                result = run_preflight(
                    root,
                    env_consumers={"EXPECTED_TOKEN": ["consumer.py"]},
                    command_probes=[["native-tool", "--version"]],
                    sandbox="available",
                    validator="not-required",
                )
        self.assertEqual(result["status"], "passed")
        run.assert_called_once()

    def test_blocks_mismatched_env_consumer_failed_probe_and_required_sandbox(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temporary:
            root = Path(temporary)
            (root / "consumer.py").write_text("token = os.environ['OTHER_TOKEN']\n", encoding="utf-8")
            completed = type("Completed", (), {"returncode": 3})()
            with patch("agent_harness_kit.preflight.subprocess.run", return_value=completed):
                result = run_preflight(
                    root,
                    env_consumers={"EXPECTED_TOKEN": ["consumer.py"]},
                    command_probes=[["native-tool", "--version"]],
                    sandbox="required-unavailable",
                    validator="not-required",
                )
        self.assertIn("env-consumer:EXPECTED_TOKEN:consumer.py", result["blockers"])
        self.assertIn("command-probe:native-tool", result["blockers"])
        self.assertIn("sandbox", result["blockers"])


if __name__ == "__main__":
    unittest.main()
