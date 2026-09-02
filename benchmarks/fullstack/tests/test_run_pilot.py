import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "run_pilot.py"
SPEC = importlib.util.spec_from_file_location("run_pilot", SCRIPT_PATH)
run_pilot = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(run_pilot)


class PilotIsolationTests(unittest.TestCase):
    def test_rejects_all_contaminated_ancestors_without_calling(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repository = root / "repository"
            nested = repository / "scratch" / "pilot"
            nested.mkdir(parents=True)
            (repository / "AGENTS.md").write_text("instructions", encoding="utf-8")
            (repository / ".agents").mkdir()
            (repository / "scratch" / "harness-state").mkdir()
            report_path = root / "artifacts" / "isolation-report.json"
            calls = []

            with self.assertRaises(run_pilot.IsolationError):
                run_pilot.run_pilot(
                    workdir=nested,
                    report_path=report_path,
                    call_fn=lambda: calls.append("called"),
                )

            self.assertEqual(calls, [])
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "rejected")
            self.assertEqual(
                report["contamination"][:2],
                [
                    {"ancestor_depth": 1, "markers": ["harness-state"]},
                    {
                        "ancestor_depth": 2,
                        "markers": [".agents", "AGENTS.md"],
                    },
                ],
            )

    def test_each_harness_marker_rejects_an_adversarial_ancestor(self):
        for marker in run_pilot.HARNESS_MARKERS:
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                repository = root / "secret-token-must-not-leak"
                workdir = repository / "deep" / "deeper"
                workdir.mkdir(parents=True)
                marker_path = repository / marker
                if "." in marker and not marker.startswith("."):
                    marker_path.write_text("instructions", encoding="utf-8")
                else:
                    marker_path.mkdir()
                report_path = root / "report" / "isolation-report.json"
                call_count = 0

                def counted_call():
                    nonlocal call_count
                    call_count += 1

                with self.assertRaises(run_pilot.IsolationError):
                    run_pilot.run_pilot(workdir, counted_call, report_path)

                self.assertEqual(call_count, 0)
                report_text = report_path.read_text(encoding="utf-8")
                self.assertNotIn("secret-token-must-not-leak", report_text)
                self.assertNotIn(str(repository), report_text)

    def test_safe_workdir_emits_report_before_injected_call(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workdir = Path(temp_dir) / "clean" / "pilot"
            workdir.mkdir(parents=True)
            report_path = Path(temp_dir) / "artifacts" / "isolation-report.json"
            observations = []

            def injected_call():
                observations.append(json.loads(report_path.read_text(encoding="utf-8")))
                return "result"

            with mock.patch.object(
                run_pilot,
                "scan_ancestors",
                return_value=(workdir.resolve(), []),
            ):
                result = run_pilot.run_pilot(workdir, injected_call, report_path)

            self.assertEqual(result, "result")
            self.assertEqual(len(observations), 1)
            self.assertEqual(observations[0]["status"], "ready")
            self.assertEqual(observations[0]["contamination"], [])
            self.assertNotIn("environment", observations[0])
            self.assertNotIn("call", observations[0])

    def test_missing_or_non_directory_workdir_rejects_before_call(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            report_path = root / "isolation-report.json"
            calls = []

            with self.assertRaises(run_pilot.IsolationError):
                run_pilot.run_pilot(
                    root / "missing",
                    lambda: calls.append("called"),
                    report_path,
                )

            self.assertEqual(calls, [])
            self.assertEqual(
                json.loads(report_path.read_text(encoding="utf-8"))["status"],
                "rejected",
            )


if __name__ == "__main__":
    unittest.main()
