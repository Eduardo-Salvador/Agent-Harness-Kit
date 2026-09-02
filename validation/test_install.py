#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
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
        temporary = tempfile.TemporaryDirectory()
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
        self.assertTrue((host / "AGENTS.md").read_text(encoding="utf-8").startswith(INSTALLER.BEGIN))
        self.assertEqual((host / "AGENTS.md").read_text(encoding="utf-8").count(INSTALLER.BEGIN), 1)
        self.assertIn("project claude", (host / "CLAUDE.md").read_text(encoding="utf-8"))
        self.assertTrue((host / "CLAUDE.md").read_text(encoding="utf-8").startswith(INSTALLER.BEGIN))
        self.assertIn("first-run discovery interview automatically", (host / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertIn("first-run discovery interview automatically", (host / "CLAUDE.md").read_text(encoding="utf-8"))

    def test_approved_context_branch_precedes_and_forbids_first_run_welcome(self) -> None:
        for entrypoint in ("AGENTS.md", "CLAUDE.md"):
            with self.subTest(entrypoint=entrypoint):
                bridge = INSTALLER.ENTRYPOINTS[entrypoint].read_text(encoding="utf-8")
                approved = "status: approved"
                uninitialized = "first-run discovery interview automatically"
                self.assertIn("do not emit the first-run welcome", bridge)
                self.assertLess(bridge.index(approved), bridge.index(uninitialized))

    def test_creates_missing_entrypoints(self) -> None:
        temporary, host = self.host()
        self.addCleanup(temporary.cleanup)
        self.install(host)
        self.assertIn("agent-harness-kit/AGENTS.md", (host / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertIn("@agent-harness-kit/CLAUDE.md", (host / "CLAUDE.md").read_text(encoding="utf-8"))

    def test_source_install_generates_profile_manifest(self) -> None:
        temporary, host = self.host()
        self.addCleanup(temporary.cleanup)
        self.install(host)
        manifest_path = host / "agent-harness-kit" / "PACKAGE-MANIFEST.json"
        self.assertTrue(manifest_path.is_file())
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(data["profile"], "core")
        self.assertEqual(data["project_learning_activation"], "not-activated")
        self.assertEqual([entry["path"] for entry in data["files"]], ["AGENTS.md"])

    def test_existing_managed_block_is_repositioned_to_top(self) -> None:
        temporary, host = self.host()
        self.addCleanup(temporary.cleanup)
        path = host / "AGENTS.md"
        bridge = INSTALLER.ENTRYPOINTS["AGENTS.md"].read_text(encoding="utf-8").strip()
        path.write_text("project rules\n\n" + bridge + "\n", encoding="utf-8")
        rendered = INSTALLER.render_entrypoint(path, INSTALLER.ENTRYPOINTS["AGENTS.md"]).decode("utf-8")
        self.assertTrue(rendered.startswith(INSTALLER.BEGIN))
        self.assertIn("project rules", rendered)
        self.assertEqual(rendered.count(INSTALLER.BEGIN), 1)

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

    def test_rejects_source_as_host(self) -> None:
        with self.assertRaisesRegex(INSTALLER.InstallError, "separate, non-nested directories"):
            INSTALLER.install("core", ROOT, True)

    def test_rejects_traversal_and_absolute_paths(self) -> None:
        unsafe = ("../escape.txt", "/absolute.txt", "C:/absolute.txt", "nested\\escape.txt")
        for value in unsafe:
            with self.subTest(value=value):
                with self.assertRaises(INSTALLER.InstallError):
                    INSTALLER.safe_relative(value)

    def test_help_explains_profiles_host_and_post_install_context(self) -> None:
        help_text = INSTALLER.build_parser().format_help()
        for expected in ("core-learning", "harness-engineering study pack", "different directories", "new agent context"):
            self.assertIn(expected, help_text)

    def test_activation_prompt_routes_through_root_and_embedded_kit(self) -> None:
        prompt = INSTALLER.ACTIVATION_PROMPT
        for expected in ("root AGENTS.md or CLAUDE.md", "agent-harness-kit/", "PROJECT-CONTEXT.md", "approved context resumes without a first-run welcome", "only missing or unapproved context starts first-run discovery"):
            self.assertIn(expected, prompt)

    def test_wheel_assets_overlay_runtime_modules_into_installed_profile(self) -> None:
        temporary, root = self.host()
        self.addCleanup(temporary.cleanup)
        package_root = root / "agent_harness_kit"
        assets = package_root / "assets"
        assets.mkdir(parents=True)
        (package_root / "__init__.py").write_text("", encoding="utf-8")
        (package_root / "scheduler.py").write_text("VALUE = 1\n", encoding="utf-8")
        with patch.object(INSTALLER, "ROOT", assets):
            overlays = INSTALLER.package_module_overlays()
        self.assertEqual(
            sorted(overlays),
            ["agent_harness_kit/__init__.py", "agent_harness_kit/scheduler.py"],
        )


if __name__ == "__main__":
    unittest.main()
