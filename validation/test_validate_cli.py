#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import importlib.util
import io
import unittest
from pathlib import Path
from unittest.mock import patch


VALIDATE_PATH = Path(__file__).resolve().parents[1] / "tools" / "validate.py"
SPEC = importlib.util.spec_from_file_location("validate_cli_under_test", VALIDATE_PATH)
assert SPEC and SPEC.loader
validate_cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_cli)


class ValidateCliTests(unittest.TestCase):
    def test_task_scope_requires_task_path(self) -> None:
        error = io.StringIO()
        with contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as raised:
            validate_cli.main(["--scope", "task"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("--scope task requires --task PATH", error.getvalue())

    def test_changed_scope_reports_git_unavailable_clearly(self) -> None:
        failure = type("Result", (), {"returncode": 128, "stdout": "", "stderr": "not a git repository"})()
        output = io.StringIO()
        with patch.object(validate_cli.subprocess, "run", return_value=failure), contextlib.redirect_stdout(output):
            result = validate_cli.main(["--scope", "changed"])
        self.assertEqual(result, 2)
        self.assertIn("VALIDATION SCOPE ERROR", output.getvalue())
        self.assertIn("Git", output.getvalue())

    def test_foundational_changed_path_escalates_to_repository(self) -> None:
        for path in ("tools/validate.py", "distribution/profiles/core.json", "AGENTS.md"):
            with self.subTest(path=path), patch.object(validate_cli, "git_changed_paths", return_value={path}):
                selection = validate_cli.resolve_scope("changed", None)
            self.assertEqual(selection.effective_scope, "repository")
            self.assertTrue(selection.escalated)
            self.assertIsNone(selection.paths)

    def test_task_scope_selects_task_and_owned_paths(self) -> None:
        expected = {"src/widget.py", "tasks/TASK-7.md", "tests/widget/test_widget.py"}
        with patch.object(validate_cli, "task_scope_paths", return_value=expected):
            selection = validate_cli.resolve_scope("task", Path("tasks/TASK-7.md"))
        self.assertEqual(
            selection.paths,
            expected,
        )

    def test_error_summary_is_deterministic_and_uses_code_prefix(self) -> None:
        errors = [
            "graph.cycle: second",
            "markdown.fence: first",
            "graph.missing-dependency: first",
            "identity.metadata: bad",
        ]
        self.assertEqual(
            validate_cli.summarize_error_categories(errors),
            "graph=2, identity=1, markdown=1",
        )

    def test_repository_default_prints_category_summary_before_details(self) -> None:
        output = io.StringIO()
        errors = ["markdown.fence: docs/a.md", "graph.cycle: validation/graph.json"]
        with patch.object(validate_cli, "validate_repository", return_value=errors), contextlib.redirect_stdout(output):
            result = validate_cli.main([])
        self.assertEqual(result, 1)
        lines = output.getvalue().splitlines()
        self.assertEqual(lines[0], "VALIDATION FAILED (2 error(s))")
        self.assertEqual(lines[1], "ERROR CATEGORIES: graph=1, markdown=1")
        self.assertEqual(lines[2:], [f"- {error}" for error in errors])

    def test_scoped_errors_exclude_unselected_paths(self) -> None:
        errors = ["markdown.fence: docs/a.md", "markdown.fence: docs/b.md"]
        self.assertEqual(validate_cli.scoped_errors(errors, {"docs/b.md"}), [errors[1]])

    def test_selected_required_count_uses_package_manifest_selection(self) -> None:
        manifest = {"profile": "core", "files": [{"path": "README.md"}, {"path": "tools/validate.py"}]}
        self.assertEqual(
            validate_cli.selected_required_count(manifest, {"README.md", "notes/not-required.md"}),
            1,
        )
        self.assertEqual(validate_cli.selected_required_count(manifest, None), 2)


if __name__ == "__main__":
    unittest.main()
