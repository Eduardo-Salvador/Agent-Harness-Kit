#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import io
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


if __name__ == "__main__":
    unittest.main()
