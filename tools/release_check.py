#!/usr/bin/env python3
"""Run the complete, stdlib-only quality gate required before a release build."""

from __future__ import annotations

import argparse
import contextlib
import json
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QA_MANIFEST = Path("validation/qa-manifest.json")
QA_SCHEMA = "harness.qa-manifest/v1"
TEST_PATTERN = "test_*.py"
PROFILES = ("core", "core-learning", "full")
IGNORED_QA_PARTS = {"__pycache__", ".pytest_cache"}
UNITTEST_COUNT = re.compile(r"\bRan\s+(\d+)\s+tests?\b")

Runner = Callable[[Sequence[str], Path], subprocess.CompletedProcess[str]]


class ReleaseCheckError(RuntimeError):
    """A release precondition is unsafe or cannot be evaluated."""


def ensure_outside_repository(path: Path, root: Path) -> Path:
    """Resolve *path* and reject it when it is inside the source repository."""

    resolved = path.resolve()
    repository = root.resolve()
    try:
        resolved.relative_to(repository)
    except ValueError:
        return resolved
    raise ReleaseCheckError(f"temporary output must be outside the source repository: {resolved}")


@contextlib.contextmanager
def temporary_output_root(root: Path):
    """Create one unique OS-temporary directory and remove only that verified path."""

    base = Path(tempfile.gettempdir()).resolve()
    ensure_outside_repository(base, root)
    temporary: Path | None = None
    for _ in range(20):
        candidate = base / f"agent-harness-release-{secrets.token_hex(8)}"
        try:
            candidate.mkdir()
        except FileExistsError:
            continue
        temporary = ensure_outside_repository(candidate, root)
        break
    if temporary is None:
        raise ReleaseCheckError(f"could not allocate a unique temporary directory under {base}")
    try:
        yield temporary
    finally:
        resolved = ensure_outside_repository(temporary, root)
        if resolved.parent != base or not resolved.name.startswith("agent-harness-release-"):
            raise ReleaseCheckError(f"refusing to remove unverified temporary directory: {resolved}")
        if resolved.exists():
            shutil.rmtree(resolved)


def safe_qa_path(root: Path, value: Any) -> str:
    """Validate one canonical, repository-relative QA manifest path."""

    if not isinstance(value, str) or not value:
        raise ReleaseCheckError("QA manifest paths must be non-empty strings")
    if "\\" in value:
        raise ReleaseCheckError(f"QA manifest path must use forward slashes: {value!r}")
    relative = PurePosixPath(value)
    if (
        relative.is_absolute()
        or relative.as_posix() != value
        or any(part in {"", ".", ".."} for part in relative.parts)
        or len(relative.parts) < 2
        or relative.parts[0] != "validation"
    ):
        raise ReleaseCheckError(f"unsafe QA manifest path: {value!r}")
    candidate = root.joinpath(*relative.parts).resolve()
    validation_root = (root / "validation").resolve()
    try:
        candidate.relative_to(validation_root)
    except ValueError as error:
        raise ReleaseCheckError(f"QA manifest path escapes validation/: {value!r}") from error
    return value


def discover_qa_tree(root: Path) -> tuple[list[str], list[str]]:
    """Return every release test and every fixture/auxiliary file under validation/."""

    repository = root.resolve()
    validation_root = repository / "validation"
    if not validation_root.is_dir():
        raise ReleaseCheckError(f"validation directory is missing: {validation_root}")

    tests: list[str] = []
    support_files: list[str] = []
    manifest_path = (repository / QA_MANIFEST).resolve()
    for path in validation_root.rglob("*"):
        if not path.is_file():
            continue
        relative_to_validation = path.relative_to(validation_root)
        if any(part in IGNORED_QA_PARTS for part in relative_to_validation.parts):
            continue
        if path.resolve() == manifest_path:
            continue
        relative = path.relative_to(repository).as_posix()
        if path.parent == validation_root and path.match(TEST_PATTERN):
            tests.append(relative)
        else:
            support_files.append(relative)
    return sorted(tests), sorted(support_files)


def load_qa_manifest(root: Path) -> dict[str, Any]:
    path = root.resolve() / QA_MANIFEST
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ReleaseCheckError(f"cannot read QA manifest {path}: {error}") from error
    if not isinstance(data, dict):
        raise ReleaseCheckError("QA manifest root must be a JSON object")
    return data


def _manifest_entries(
    data: dict[str, Any], field: str, root: Path, errors: list[str]
) -> list[str]:
    values = data.get(field)
    if not isinstance(values, list):
        errors.append(f"QA manifest field {field!r} must be a list")
        return []
    entries: list[str] = []
    for index, value in enumerate(values):
        try:
            entries.append(safe_qa_path(root, value))
        except ReleaseCheckError as error:
            errors.append(f"{field}[{index}]: {error}")
    duplicates = sorted({entry for entry in entries if entries.count(entry) > 1})
    if duplicates:
        errors.append(f"duplicate {field}: {', '.join(duplicates)}")
    if entries != sorted(entries):
        errors.append(f"QA manifest field {field!r} must be sorted")
    return entries


def qa_manifest_errors(root: Path) -> list[str]:
    """Compare the explicit QA inventory with the current validation tree."""

    try:
        data = load_qa_manifest(root)
        discovered_tests, discovered_support = discover_qa_tree(root)
    except ReleaseCheckError as error:
        return [str(error)]

    errors: list[str] = []
    expected_fields = {"schema", "minimum_test_cases", "tests", "support_files"}
    missing_fields = sorted(expected_fields - set(data))
    unknown_fields = sorted(set(data) - expected_fields)
    if missing_fields:
        errors.append(f"QA manifest missing fields: {', '.join(missing_fields)}")
    if unknown_fields:
        errors.append(f"QA manifest has unknown fields: {', '.join(unknown_fields)}")
    if data.get("schema") != QA_SCHEMA:
        errors.append(f"QA manifest schema must be {QA_SCHEMA!r}")
    minimum = data.get("minimum_test_cases")
    if isinstance(minimum, bool) or not isinstance(minimum, int) or minimum < 1:
        errors.append("QA manifest minimum_test_cases must be a positive integer")

    declared_tests = _manifest_entries(data, "tests", root, errors)
    declared_support = _manifest_entries(data, "support_files", root, errors)
    overlap = sorted(set(declared_tests) & set(declared_support))
    if overlap:
        errors.append(f"QA manifest entries appear in both lists: {', '.join(overlap)}")

    missing_tests = sorted(set(discovered_tests) - set(declared_tests))
    stale_tests = sorted(set(declared_tests) - set(discovered_tests))
    missing_support = sorted(set(discovered_support) - set(declared_support))
    stale_support = sorted(set(declared_support) - set(discovered_support))
    if missing_tests:
        errors.append(f"unmanifested tests: {', '.join(missing_tests)}")
    if stale_tests:
        errors.append(f"manifested tests missing from tree: {', '.join(stale_tests)}")
    if missing_support:
        errors.append(f"unmanifested fixture/auxiliary files: {', '.join(missing_support)}")
    if stale_support:
        errors.append(f"manifested fixture/auxiliary files missing from tree: {', '.join(stale_support)}")
    return errors


def default_runner(command: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def run_step(
    label: str,
    command: Sequence[str],
    root: Path,
    runner: Runner,
) -> subprocess.CompletedProcess[str]:
    print(f"\n== {label} ==", flush=True)
    print(f"+ {subprocess.list2cmdline(list(command))}", flush=True)
    result = runner(command, root)
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(
            result.stderr,
            end="" if result.stderr.endswith("\n") else "\n",
            file=sys.stderr,
        )
    return result


def failure_status(returncode: int) -> int:
    return returncode if returncode > 0 else 1


def unittest_count(result: subprocess.CompletedProcess[str]) -> int | None:
    matches = UNITTEST_COUNT.findall((result.stdout or "") + "\n" + (result.stderr or ""))
    return int(matches[-1]) if matches else None


def run_release_checks(root: Path = ROOT, runner: Runner = default_runner) -> int:
    """Run release gates in build-blocking order and return a process status."""

    repository = root.resolve()
    required = (
        repository / "tools" / "validate.py",
        repository / "tools" / "package.py",
        repository / QA_MANIFEST,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        print(f"RELEASE CHECK FAILED: missing required files: {', '.join(missing)}", file=sys.stderr)
        return 1

    validator = run_step(
        "Source validator",
        (sys.executable, str(repository / "tools" / "validate.py")),
        repository,
        runner,
    )
    if validator.returncode != 0:
        print("RELEASE CHECK FAILED: source validator", file=sys.stderr)
        return failure_status(validator.returncode)

    manifest_errors = qa_manifest_errors(repository)
    if manifest_errors:
        print("RELEASE CHECK FAILED: QA manifest", file=sys.stderr)
        for error in manifest_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    manifest = load_qa_manifest(repository)

    unit_tests = run_step(
        "Complete unittest suite",
        (
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "validation",
            "-p",
            TEST_PATTERN,
        ),
        repository,
        runner,
    )
    if unit_tests.returncode != 0:
        print("RELEASE CHECK FAILED: unittest suite", file=sys.stderr)
        return failure_status(unit_tests.returncode)
    observed_count = unittest_count(unit_tests)
    minimum_count = int(manifest["minimum_test_cases"])
    if observed_count is None:
        print("RELEASE CHECK FAILED: unittest did not report a test count", file=sys.stderr)
        return 1
    if observed_count < minimum_count:
        print(
            f"RELEASE CHECK FAILED: unittest ran {observed_count}; minimum is {minimum_count}",
            file=sys.stderr,
        )
        return 1

    with temporary_output_root(repository) as temporary_root:
        for profile in PROFILES:
            output = ensure_outside_repository(temporary_root / profile, repository)
            profile_check = run_step(
                f"Distribution profile: {profile}",
                (
                    sys.executable,
                    str(repository / "tools" / "package.py"),
                    "--profile",
                    profile,
                    "--output",
                    str(output),
                    "--format",
                    "directory",
                    "--check",
                ),
                repository,
                runner,
            )
            if profile_check.returncode != 0:
                print(f"RELEASE CHECK FAILED: profile {profile}", file=sys.stderr)
                return failure_status(profile_check.returncode)

    print(f"\nRELEASE CHECK PASSED: {observed_count} tests; {len(PROFILES)} profiles")
    return 0


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        description="Run every quality gate required before building or publishing a release."
    )


def main(argv: Sequence[str] | None = None) -> int:
    build_parser().parse_args(argv)
    try:
        return run_release_checks()
    except (OSError, ReleaseCheckError) as error:
        print(f"RELEASE CHECK FAILED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
