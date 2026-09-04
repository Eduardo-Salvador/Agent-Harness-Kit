#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import posixpath
import re
import tempfile
import unittest
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
from unittest.mock import patch

from agent_harness_kit import runtime_profiles, runtime_resources, runtime_validation


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("agent_harness_runtime_installer", ROOT / "tools" / "install.py")
INSTALLER = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(INSTALLER)
PACKAGE_SPEC = importlib.util.spec_from_file_location("agent_harness_runtime_packager", ROOT / "tools" / "package.py")
PACKAGER = importlib.util.module_from_spec(PACKAGE_SPEC)
assert PACKAGE_SPEC and PACKAGE_SPEC.loader
PACKAGE_SPEC.loader.exec_module(PACKAGER)


class RuntimeDistributionTests(unittest.TestCase):
    def test_dot_is_rejected_by_runtime_path_validators(self) -> None:
        with self.assertRaises(runtime_profiles.RuntimeProfileError):
            runtime_profiles.safe_relative(".")
        with self.assertRaises(runtime_validation.RuntimeValidationError):
            runtime_validation._safe_relative(".")

    def test_core_runtime_manifest_is_explicit_small_and_excludes_release_qa(self) -> None:
        files = INSTALLER.runtime_files("core")
        self.assertLessEqual(len(files) + 1, 80)  # payload plus package manifest
        forbidden = (
            ".github/",
            "benchmarks/",
            "distribution/",
            "examples/",
            "media/",
            "validation/",
        )
        self.assertFalse([path for path in files if path.startswith(forbidden)])
        self.assertIn("AGENTS.md", files)
        self.assertIn("CLAUDE.md", files)
        self.assertIn("tools/validate.py", files)
        self.assertFalse([path for path in files if path.startswith("harness/templates/")])

    def test_core_runtime_markdown_links_close_inside_static_payload(self) -> None:
        static_files = set(runtime_profiles.load_runtime_profile(ROOT, "core")["files"])
        link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
        broken: list[str] = []
        for relative in sorted(path for path in static_files if path.casefold().endswith(".md")):
            text = (ROOT / relative).read_text(encoding="utf-8")
            for line_number, line in enumerate(text.splitlines(), 1):
                for match in link_pattern.finditer(line):
                    raw = match.group(1).strip()
                    if raw.startswith("<") and ">" in raw:
                        raw = raw[1 : raw.index(">")]
                    else:
                        raw = raw.split(maxsplit=1)[0]
                    parsed = urlsplit(raw)
                    if parsed.scheme or parsed.netloc or not parsed.path:
                        continue
                    target = unquote(parsed.path)
                    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(relative), target))
                    if resolved.startswith("../") or resolved not in static_files:
                        broken.append(f"{relative}:{line_number} -> {raw}")
        self.assertEqual(broken, [])

    def test_packed_templates_have_no_location_dependent_relative_links(self) -> None:
        archive_bytes, _ = INSTALLER.template_archive("core")
        relative_links: list[str] = []
        with tempfile.TemporaryFile() as stream:
            stream.write(archive_bytes)
            stream.seek(0)
            with zipfile.ZipFile(stream) as archive:
                for member in archive.namelist():
                    text = archive.read(member).decode("utf-8")
                    for line_number, line in enumerate(text.splitlines(), 1):
                        for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", line):
                            raw = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
                            parsed = urlsplit(raw)
                            if not parsed.scheme and not parsed.netloc and parsed.path:
                                relative_links.append(f"{member}:{line_number} -> {raw}")
        self.assertEqual(relative_links, [])

    def test_real_core_install_is_hash_valid_self_contained_and_under_budget(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            host = Path(temporary)
            INSTALLER.install("core", host, False)
            kit = host / "agent-harness-kit"
            manifest = json.loads((kit / "PACKAGE-MANIFEST.json").read_text(encoding="utf-8"))

            self.assertEqual(manifest["schema"], "agent-harness-kit.runtime-manifest/v1")
            self.assertEqual(manifest["profile"], "core")
            self.assertLessEqual(len(manifest["files"]) + 1, 80)
            self.assertTrue((kit / "resources" / "templates.zip").is_file())
            self.assertFalse((kit / "validation").exists())
            self.assertFalse((kit / "media").exists())
            self.assertFalse((kit / "harness" / "templates").exists())
            self.assertEqual(runtime_validation.validate_runtime_install(kit, host), [])

            names = runtime_resources.template_names(kit)
            self.assertIn("PROJECT-CONTEXT", names)
            self.assertIn("TASK-GRAPH", names)

    def test_runtime_validator_rejects_tampering_and_unlisted_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            host = Path(temporary)
            INSTALLER.install("core", host, False)
            kit = host / "agent-harness-kit"

            (kit / "AGENTS.md").write_text("tampered\n", encoding="utf-8")
            errors = runtime_validation.validate_runtime_install(kit, host)
            self.assertTrue(any("hash" in error and "AGENTS.md" in error for error in errors))

            (kit / "unexpected.txt").write_text("unexpected\n", encoding="utf-8")
            errors = runtime_validation.validate_runtime_install(kit, host)
            self.assertTrue(any("unlisted" in error and "unexpected.txt" in error for error in errors))

    def test_packaged_compact_install_rejects_tampered_archive_sources_before_writing(self) -> None:
        tampered_sources = (
            "harness/templates/PROJECT-CONTEXT.md",
            "agent_harness_kit/runtime_resources.py",
        )
        for relative in tampered_sources:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                source = root / "source-package"
                host = root / "host"
                host.mkdir()
                files = PACKAGER.select("core")
                version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
                PACKAGER.build_directory(source, "core", version, files)
                target = source / relative
                target.write_bytes(target.read_bytes() + b"\nTAMPERED\n")
                entrypoints = {
                    "AGENTS.md": source / "harness/templates/ROOT-AGENTS-BRIDGE.md",
                    "CLAUDE.md": source / "harness/templates/ROOT-CLAUDE-BRIDGE.md",
                }
                with patch.object(INSTALLER, "ROOT", source), patch.object(
                    INSTALLER, "ENTRYPOINTS", entrypoints
                ):
                    with self.assertRaisesRegex(INSTALLER.InstallError, "hash mismatch"):
                        INSTALLER.install("core", host, False)
                self.assertFalse((host / "agent-harness-kit").exists())
                self.assertFalse((host / "AGENTS.md").exists())
                self.assertFalse((host / "CLAUDE.md").exists())

    def test_scaffold_materializes_one_template_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            host = Path(temporary)
            INSTALLER.install("core", host, False)
            kit = host / "agent-harness-kit"
            output = host / "harness-state" / "PROJECT-CONTEXT.md"

            created = runtime_resources.scaffold_template(kit, "project-context", output, host_root=host)
            self.assertEqual(created, output.resolve())
            self.assertIn("schema: harness.project-context/v1", output.read_text(encoding="utf-8"))
            with self.assertRaises(FileExistsError):
                runtime_resources.scaffold_template(kit, "PROJECT-CONTEXT", output, host_root=host)
            with self.assertRaises(runtime_resources.RuntimeResourceError):
                runtime_resources.template_bytes(kit, "../PROJECT-CONTEXT")
            with self.assertRaises(runtime_resources.RuntimeResourceError):
                runtime_resources.scaffold_template(
                    kit, "PROJECT-CONTEXT", host.parent / "escape.md", host_root=host,
                )

    def test_wheel_asset_packager_overlays_python_runtime_modules(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package_root = Path(temporary) / "agent_harness_kit"
            assets = package_root / "assets"
            assets.mkdir(parents=True)
            (package_root / "__init__.py").write_text("", encoding="utf-8")
            (package_root / "cli.py").write_text("VALUE = 1\n", encoding="utf-8")
            with patch.object(PACKAGER, "ROOT", assets):
                self.assertEqual(
                    sorted(PACKAGER.package_module_overlays()),
                    ["agent_harness_kit/__init__.py", "agent_harness_kit/cli.py"],
                )
                self.assertIn("agent_harness_kit/cli.py", PACKAGER.source_files())


if __name__ == "__main__":
    unittest.main()
