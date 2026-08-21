#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("agent_harness_installer", ROOT / "tools" / "install.py")
INSTALLER = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(INSTALLER)


class InstallerTests(unittest.TestCase):
    def host(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        work = ROOT / "work"
        work.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=work)
        return temporary, Path(temporary.name)

    def install(self, host: Path, dry_run: bool = False) -> list[str]:
        with patch.object(INSTALLER, "package_files", return_value=["AGENTS.md"]):
            return INSTALLER.install("core", host, dry_run)

    def test_preserves_entrypoints_and_installs_profile(self) -> None:
        temporary, host = self.host()
        self.addCleanup(temporary.cleanup)
        (host / "AGENTS.md").write_text("project agents\n", encoding="utf-8")
        (host / "CLAUDE.md").write_text("project claude\n", encoding="utf-8")
        self.install(host)
        self.assertTrue((host / "agent-harness-kit" / "AGENTS.md").is_file())
        self.assertIn("project agents", (host / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertEqual((host / "AGENTS.md").read_text(encoding="utf-8").count(INSTALLER.BEGIN), 1)
        self.assertIn("project claude", (host / "CLAUDE.md").read_text(encoding="utf-8"))

    def test_creates_missing_entrypoints(self) -> None:
        temporary, host = self.host()
        self.addCleanup(temporary.cleanup)
        self.install(host)
        self.assertIn("agent-harness-kit/AGENTS.md", (host / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertIn("@agent-harness-kit/CLAUDE.md", (host / "CLAUDE.md").read_text(encoding="utf-8"))

    def test_dry_run_changes_nothing(self) -> None:
        temporary, host = self.host()
        self.addCleanup(temporary.cleanup)
        self.install(host, True)
        self.assertEqual(list(host.iterdir()), [])

    def test_rejects_malformed_marker_without_writes(self) -> None:
        temporary, host = self.host()
        self.addCleanup(temporary.cleanup)
        original = "project\n<!-- agent-harness-kit:begin -->\n"
        (host / "AGENTS.md").write_text(original, encoding="utf-8")
        with self.assertRaises(INSTALLER.InstallError):
            self.install(host)
        self.assertEqual((host / "AGENTS.md").read_text(encoding="utf-8"), original)
        self.assertFalse((host / "agent-harness-kit").exists())

    def test_rejects_existing_destination(self) -> None:
        temporary, host = self.host()
        self.addCleanup(temporary.cleanup)
        (host / "agent-harness-kit").mkdir()
        with self.assertRaises(INSTALLER.InstallError):
            self.install(host)

    def test_rejects_traversal_and_absolute_paths(self) -> None:
        unsafe = ("../escape.txt", "/absolute.txt", "C:/absolute.txt", "nested\\escape.txt")
        for value in unsafe:
            with self.subTest(value=value):
                with self.assertRaises(INSTALLER.InstallError):
                    INSTALLER.safe_relative(value)


if __name__ == "__main__":
    unittest.main()
