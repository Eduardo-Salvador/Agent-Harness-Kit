#!/usr/bin/env python3

from __future__ import annotations

import os
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


ROOT = Path(__file__).resolve().parents[1]
TEMP_BASE_ENV = "AGENT_HARNESS_SMOKE_TEMP_BASE"


@contextmanager
def working_directory(path: Path) -> Iterator[None]:
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


class InstalledHostSmokeTests(unittest.TestCase):
    def run_command(self, *command: object, cwd: Path) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [str(part) for part in command],
            cwd=cwd,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=(
                f"command failed in {cwd}: {' '.join(str(part) for part in command)}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            ),
        )
        return result

    def test_core_directory_package_installs_and_resolves_from_external_host(self) -> None:
        configured_base = os.environ.get(TEMP_BASE_ENV)
        if configured_base:
            temp_base = Path(configured_base).expanduser().resolve()
            temp_base.mkdir(parents=True, exist_ok=True)
        else:
            temp_base = None

        with tempfile.TemporaryDirectory(prefix="agent-harness-installed-smoke-", dir=temp_base) as temporary:
            external_root = Path(temporary).resolve()
            with self.assertRaises(ValueError):
                external_root.relative_to(ROOT.resolve())

            package_output = external_root / "package-output"
            host = external_root / "host-project"
            host.mkdir()

            self.run_command(
                sys.executable,
                ROOT / "tools" / "package.py",
                "--profile",
                "core",
                "--output",
                package_output,
                "--format",
                "directory",
                cwd=host,
            )

            version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
            package = package_output / f"agent-harness-kit-{version}-core"
            self.assertTrue((package / "PACKAGE-MANIFEST.json").is_file())

            self.run_command(
                sys.executable,
                package / "tools" / "install.py",
                "--profile",
                "core",
                "--host",
                host,
                cwd=host,
            )

            installed = host / "agent-harness-kit"
            compact_manifest = json.loads((installed / "PACKAGE-MANIFEST.json").read_text(encoding="utf-8"))
            self.assertLessEqual(len(compact_manifest["files"]) + 1, 80)
            self.assertFalse((installed / "validation").exists())
            self.assertFalse((installed / "media").exists())
            self.assertFalse((installed / "harness" / "templates").exists())

            self.run_command(
                sys.executable,
                installed / "runtime.pyz",
                "scaffold",
                "PROJECT-CONTEXT",
                "--path",
                host,
                "--output",
                "harness-state/PROJECT-CONTEXT.md",
                cwd=host,
            )

            context_relative = Path("harness-state/PROJECT-CONTEXT.md")
            task_relative = Path("harness-state/tasks/TASK-SMOKE.md")
            context = host / context_relative
            task = host / task_relative
            task.parent.mkdir(parents=True)
            context.write_text(
                "---\n"
                "schema: harness.project-context/v1\n"
                "id: project-context\n"
                "revision: 1\n"
                "status: approved\n"
                "approved_by: human:smoke-test\n"
                f"active_task: {task_relative.as_posix()}\n"
                "---\n\n"
                "# Installed host smoke context\n",
                encoding="utf-8",
            )
            task.write_text(
                "---\n"
                "schema: harness.task/v1\n"
                "id: TASK-SMOKE\n"
                "revision: 1\n"
                "status: ready\n"
                "test_strategy: verification-only\n"
                "---\n\n"
                "# TASK-SMOKE\n",
                encoding="utf-8",
            )

            with working_directory(host):
                host_cwd = Path.cwd()
                installed = host_cwd / "agent-harness-kit"
                agents_bridge = Path("AGENTS.md").read_text(encoding="utf-8")
                claude_bridge = Path("CLAUDE.md").read_text(encoding="utf-8")
                self.assertIn("agent-harness-kit/AGENTS.md", agents_bridge)
                self.assertTrue(Path("agent-harness-kit/AGENTS.md").is_file())
                self.assertIn("@agent-harness-kit/CLAUDE.md", claude_bridge)
                self.assertTrue(Path("agent-harness-kit/CLAUDE.md").is_file())

                for bridge in (agents_bridge, claude_bridge):
                    self.assertIn(context_relative.as_posix(), bridge)
                    self.assertIn('greeting-only', bridge)
                    self.assertIn('autonomous', bridge)

                context_before = context.read_text(encoding='utf-8')
                version_result = self.run_command(
                    sys.executable, installed / 'runtime.pyz', '--version', cwd=installed,
                )
                self.assertIn(version, version_result.stdout)
                for preset, interaction in (('accompanied', 'accompanied'), ('autonomous', 'continuous'), ('hackathon', 'accompanied')):
                    mode_result = self.run_command(
                        sys.executable, installed / 'runtime.pyz', 'delivery-mode', preset, cwd=installed,
                    )
                    policy = json.loads(mode_result.stdout)
                    self.assertEqual(policy['preset'], preset)
                    self.assertEqual(policy['interaction'], interaction)
                    self.assertFalse(policy['applies_changes'])
                self.assertEqual(context.read_text(encoding='utf-8'), context_before)
                context_text = context_relative.read_text(encoding="utf-8")
                self.assertIn("schema: harness.project-context/v1", context_text)
                self.assertIn("status: approved", context_text)

                embedded_skill = installed / ".agents/skills/request-router/SKILL.md"
                self.assertTrue(embedded_skill.is_file())
                self.assertIn("name: request-router", embedded_skill.read_text(encoding="utf-8"))

                first_run_skill = installed / ".agents/skills/first-run-discovery/SKILL.md"
                first_run_text = first_run_skill.read_text(encoding="utf-8").lower()
                self.assertIn("architecture and folder organization", first_run_text)
                self.assertIn("coding conventions are optional", first_run_text)
                self.assertTrue((installed / "resources/templates.zip").is_file())

                active_task = next(
                    line.removeprefix("active_task: ").strip()
                    for line in context_text.splitlines()
                    if line.startswith("active_task: ")
                )
                self.assertEqual(active_task, task_relative.as_posix())
                self.assertTrue(Path(active_task).is_file())

                validation = self.run_command(
                    sys.executable,
                    installed / "tools" / "validate.py",
                    cwd=host_cwd,
                )
                self.assertIn("RUNTIME VALIDATION PASSED", validation.stdout)
                cli_validation = self.run_command(
                    sys.executable,
                    installed / "runtime.pyz",
                    "validate",
                    str(host_cwd),
                    cwd=host_cwd,
                )
                self.assertEqual(json.loads(cli_validation.stdout)["status"], "passed")


if __name__ == "__main__":
    unittest.main()
