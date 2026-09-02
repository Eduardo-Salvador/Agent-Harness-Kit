"""Run a benchmark pilot only from a Harness-free working directory.

The isolation report intentionally excludes paths, environment variables, command
arguments, call results, and exception details so that it is safe to retain.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Callable, TypeVar


HARNESS_MARKERS = (
    ".agents",
    ".claude",
    "AGENTS.md",
    "CLAUDE.md",
    "harness-state",
)

T = TypeVar("T")


class IsolationError(RuntimeError):
    """Raised after reporting a work directory that failed isolation preflight."""


def scan_ancestors(workdir: str | os.PathLike[str]) -> tuple[Path, list[dict[str, object]]]:
    """Return the resolved directory and every Harness marker found above it."""

    resolved = Path(workdir).expanduser().resolve()
    contamination: list[dict[str, object]] = []
    for depth, ancestor in enumerate((resolved, *resolved.parents)):
        markers = sorted(
            marker for marker in HARNESS_MARKERS if (ancestor / marker).exists()
        )
        if markers:
            contamination.append(
                {"ancestor_depth": depth, "markers": markers}
            )
    return resolved, contamination


def _write_report(report_path: Path, report: dict[str, object]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(report, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=report_path.parent,
        prefix=f".{report_path.name}.",
        suffix=".tmp",
        delete=False,
    ) as temporary:
        temporary.write(serialized)
        temporary_path = Path(temporary.name)
    os.replace(temporary_path, report_path)


def run_pilot(
    workdir: str | os.PathLike[str],
    call_fn: Callable[[], T],
    report_path: str | os.PathLike[str] = "isolation-report.json",
) -> T:
    """Preflight ``workdir``, emit a report, then invoke ``call_fn`` if safe."""

    resolved, contamination = scan_ancestors(workdir)
    rejection_reasons: list[str] = []
    if not resolved.is_dir():
        rejection_reasons.append("workdir_not_directory")
    if contamination:
        rejection_reasons.append("harness_marker_in_ancestor")

    report = {
        "schema": "agent-harness.pilot-isolation/v1",
        "status": "rejected" if rejection_reasons else "ready",
        "scanned_ancestor_count": 1 + len(resolved.parents),
        "contamination": contamination,
        "rejection_reasons": rejection_reasons,
    }
    _write_report(Path(report_path).expanduser().resolve(), report)

    if rejection_reasons:
        raise IsolationError("pilot isolation preflight rejected the work directory")
    return call_fn()


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", required=True, type=Path)
    parser.add_argument(
        "--report-path",
        type=Path,
        default=Path("isolation-report.json"),
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="command to run after '--' when isolation succeeds",
    )
    args = parser.parse_args(argv)
    if args.command[:1] == ["--"]:
        args.command = args.command[1:]
    if not args.command:
        parser.error("a command is required after '--'")
    return args


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    def invoke() -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(args.command, cwd=args.workdir, check=False)

    try:
        completed = run_pilot(args.workdir, invoke, args.report_path)
    except IsolationError as error:
        print(str(error), file=sys.stderr)
        return 2
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
