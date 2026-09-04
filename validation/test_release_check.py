#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import secrets
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_CHECK_PATH = ROOT / "tools" / "release_check.py"


def load_release_check():
    if not RELEASE_CHECK_PATH.is_file():
        raise AssertionError("tools/release_check.py must exist before release builds are allowed")
    spec = importlib.util.spec_from_file_location("release_check_under_test", RELEASE_CHECK_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseCheckTests(unittest.TestCase):
    def test_release_check_script_exists_as_release_gate(self) -> None:
        self.assertTrue(
            RELEASE_CHECK_PATH.is_file(),
            "tools/release_check.py must exist before release builds are allowed",
        )

    def fixture_repository(self, minimum_test_cases: int = 136) -> Path:
        temporary_base = (ROOT / ".tmp" / "release-check-tests").resolve()
        temporary_base.mkdir(parents=True, exist_ok=True)
        root = temporary_base / f"case-{secrets.token_hex(8)}"
        root.mkdir()
        self.addCleanup(self.remove_fixture_repository, root, temporary_base)
        (root / "tools").mkdir(parents=True)
        (root / "validation" / "fixtures").mkdir(parents=True)
        (root / "tools" / "validate.py").write_text("", encoding="utf-8")
        (root / "tools" / "package.py").write_text("", encoding="utf-8")
        (root / "validation" / "test_sample.py").write_text("", encoding="utf-8")
        (root / "validation" / "fixtures" / "sample.json").write_text("{}\n", encoding="utf-8")
        manifest = {
            "schema": "harness.qa-manifest/v1",
            "minimum_test_cases": minimum_test_cases,
            "tests": ["validation/test_sample.py"],
            "support_files": ["validation/fixtures/sample.json"],
        }
        (root / "validation" / "qa-manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )
        return root

    @staticmethod
    def remove_fixture_repository(root: Path, temporary_base: Path) -> None:
        resolved = root.resolve()
        if resolved.parent != temporary_base or not resolved.name.startswith("case-"):
            raise AssertionError(f"refusing to remove unverified test fixture: {resolved}")
        if resolved.exists():
            shutil.rmtree(resolved)

    def test_manifest_exactly_matches_tests_and_fixture_auxiliary_tree(self) -> None:
        release_check = load_release_check()
        self.assertEqual(release_check.qa_manifest_errors(ROOT), [])
        manifest = release_check.load_qa_manifest(ROOT)
        tests, support_files = release_check.discover_qa_tree(ROOT)
        self.assertEqual(manifest["tests"], tests)
        self.assertEqual(manifest["support_files"], support_files)
        self.assertGreaterEqual(manifest["minimum_test_cases"], 136)
        self.assertIn("validation/test_release_check.py", manifest["tests"])

    def test_manifest_detects_unlisted_and_removed_qa_files(self) -> None:
        release_check = load_release_check()
        root = self.fixture_repository()
        (root / "validation" / "test_added.py").write_text("", encoding="utf-8")
        (root / "validation" / "fixtures" / "sample.json").unlink()
        errors = release_check.qa_manifest_errors(root)
        self.assertTrue(
            any("unmanifested tests: validation/test_added.py" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("manifested fixture/auxiliary files missing from tree" in error for error in errors),
            errors,
        )

    def test_manifest_rejects_traversal(self) -> None:
        release_check = load_release_check()
        root = self.fixture_repository()
        path = root / "validation" / "qa-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["tests"].append("validation/../outside.py")
        path.write_text(json.dumps(manifest), encoding="utf-8")
        errors = release_check.qa_manifest_errors(root)
        self.assertTrue(any("unsafe QA manifest path" in error for error in errors), errors)

    def test_gate_runs_validator_tests_and_all_profiles_in_order(self) -> None:
        release_check = load_release_check()
        root = self.fixture_repository()
        calls: list[tuple[list[str], Path]] = []

        def runner(command, cwd):
            command = list(command)
            calls.append((command, cwd))
            stderr = "Ran 136 tests in 0.001s\n\nOK\n" if "unittest" in command else ""
            return subprocess.CompletedProcess(command, 0, stdout="", stderr=stderr)

        self.assertEqual(release_check.run_release_checks(root, runner), 0)
        self.assertEqual(len(calls), 5)
        self.assertEqual(Path(calls[0][0][1]), root / "tools" / "validate.py")
        self.assertEqual(calls[1][0][1:4], ["-m", "unittest", "discover"])
        self.assertEqual(
            [command[command.index("--profile") + 1] for command, _ in calls[2:]],
            ["core", "core-learning", "full"],
        )
        for command, cwd in calls[2:]:
            self.assertEqual(cwd, root.resolve())
            self.assertIn("--check", command)
            output = Path(command[command.index("--output") + 1]).resolve()
            with self.assertRaises(ValueError):
                output.relative_to(root.resolve())

    def test_gate_stops_on_the_first_nonzero_status(self) -> None:
        release_check = load_release_check()
        root = self.fixture_repository()
        calls = []

        def runner(command, cwd):
            calls.append((list(command), cwd))
            return subprocess.CompletedProcess(command, 9, stdout="", stderr="validator failed\n")

        self.assertEqual(release_check.run_release_checks(root, runner), 9)
        self.assertEqual(len(calls), 1)

    def test_gate_rejects_a_silently_reduced_test_count(self) -> None:
        release_check = load_release_check()
        root = self.fixture_repository()
        calls = []

        def runner(command, cwd):
            command = list(command)
            calls.append((command, cwd))
            stderr = "Ran 135 tests in 0.001s\n\nOK\n" if "unittest" in command else ""
            return subprocess.CompletedProcess(command, 0, stdout="", stderr=stderr)

        self.assertNotEqual(release_check.run_release_checks(root, runner), 0)
        self.assertEqual(len(calls), 2)

    def test_workflow_runs_release_gate_before_build(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "python-publish.yml").read_text(encoding="utf-8")
        self.assertIn("python tools/release_check.py", workflow)
        self.assertLess(workflow.index("python tools/release_check.py"), workflow.index("python -m build"))
        self.assertIn("Smoke-test built wheel and compact install", workflow)
        self.assertLess(
            workflow.index("python -m build"),
            workflow.index("Smoke-test built wheel and compact install"),
        )
        self.assertLess(
            workflow.index("Smoke-test built wheel and compact install"),
            workflow.index("Upload distributions"),
        )

    def test_contributor_guide_names_the_release_gate(self) -> None:
        guide = (ROOT / ".github" / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("python tools/release_check.py", guide)


if __name__ == "__main__":
    unittest.main()
