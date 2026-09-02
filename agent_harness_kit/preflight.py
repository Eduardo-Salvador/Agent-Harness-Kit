"""Deterministic project preflight checks run before graph decomposition."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path, PurePosixPath


class PreflightError(ValueError):
    """Raised for an invalid preflight request."""


def _relative_path(raw: str) -> PurePosixPath:
    path = PurePosixPath(raw.replace("\\", "/"))
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise PreflightError(f"required path must be project-relative: {raw!r}")
    return path


def _package_scripts(root: Path) -> set[str]:
    package_json = root / "package.json"
    if not package_json.is_file():
        return set()
    try:
        payload = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PreflightError(f"cannot read package.json: {exc}") from exc
    scripts = payload.get("scripts", {}) if isinstance(payload, dict) else {}
    return set(scripts) if isinstance(scripts, dict) else set()


def run_preflight(
    project: Path,
    *,
    required_paths: list[str] | None = None,
    required_scripts: list[str] | None = None,
    required_env: list[str] | None = None,
    required_commands: list[str] | None = None,
    env_consumers: dict[str, list[str]] | None = None,
    command_probes: list[list[str]] | None = None,
    browser: str = "not-required",
    sandbox: str = "not-required",
    workers: int = 1,
    validator: str = "required",
) -> dict[str, object]:
    """Check declared prerequisites without executing project code or exposing secrets."""
    root = project.expanduser().resolve()
    if browser not in {"not-required", "available", "required-unavailable"}:
        raise PreflightError("browser must be not-required, available, or required-unavailable")
    if sandbox not in {"not-required", "available", "required-unavailable"}:
        raise PreflightError("sandbox must be not-required, available, or required-unavailable")
    if validator not in {"required", "not-required"}:
        raise PreflightError("validator must be required or not-required")
    if not isinstance(workers, int) or isinstance(workers, bool) or workers < 0:
        raise PreflightError("workers must be a non-negative integer")

    paths = required_paths or []
    scripts = required_scripts or []
    env_names = required_env or []
    commands = required_commands or []
    consumers = env_consumers or {}
    probes = command_probes or []
    blockers: list[str] = []
    checks: list[dict[str, object]] = []

    for raw in paths:
        relative = _relative_path(raw)
        passed = root.joinpath(*relative.parts).exists()
        checks.append({"kind": "path", "name": raw, "passed": passed})
        if not passed:
            blockers.append(f"path:{raw}")

    available_scripts = _package_scripts(root) if scripts else set()
    for name in scripts:
        passed = name in available_scripts
        checks.append({"kind": "script", "name": name, "passed": passed})
        if not passed:
            blockers.append(f"script:{name}")

    for name in env_names:
        passed = bool(os.environ.get(name))
        checks.append({"kind": "env", "name": name, "passed": passed})
        if not passed:
            blockers.append(f"env:{name}")

    for name, consumer_paths in consumers.items():
        if not isinstance(consumer_paths, list) or not consumer_paths:
            raise PreflightError(f"env consumer {name!r} needs at least one relative path")
        for raw in consumer_paths:
            relative = _relative_path(raw)
            path = root.joinpath(*relative.parts)
            try:
                passed = path.is_file() and name in path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                passed = False
            checks.append({"kind": "env-consumer", "name": name, "path": raw, "passed": passed})
            if not passed:
                blockers.append(f"env-consumer:{name}:{raw}")

    for name in commands:
        passed = shutil.which(name) is not None
        checks.append({"kind": "command", "name": name, "passed": passed})
        if not passed:
            blockers.append(f"command:{name}")

    for command in probes:
        if not isinstance(command, list) or not command or not all(isinstance(part, str) and part for part in command):
            raise PreflightError("each command probe must be a non-empty string array")
        try:
            completed = subprocess.run(
                command, cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, timeout=15, check=False, shell=False,
            )
            passed = completed.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            passed = False
        checks.append({"kind": "command-probe", "name": command[0], "passed": passed})
        if not passed:
            blockers.append(f"command-probe:{command[0]}")

    if validator == "required":
        passed = (root / "tools" / "validate.py").is_file() or (root / "agent-harness-kit" / "tools" / "validate.py").is_file()
        checks.append({"kind": "validator", "name": "agent-harness", "passed": passed})
        if not passed:
            blockers.append("validator")

    browser_passed = browser != "required-unavailable"
    checks.append({"kind": "browser", "name": browser, "passed": browser_passed})
    if not browser_passed:
        blockers.append("browser")

    sandbox_passed = sandbox != "required-unavailable"
    checks.append({"kind": "sandbox", "name": sandbox, "passed": sandbox_passed})
    if not sandbox_passed:
        blockers.append("sandbox")

    workers_passed = workers >= 1
    checks.append({"kind": "workers", "name": "parallel-capacity", "passed": workers_passed, "count": workers})
    if not workers_passed:
        blockers.append("workers")

    return {
        "schema": "harness.preflight/v1",
        "status": "passed" if not blockers else "blocked",
        "project": str(root),
        "checks": checks,
        "blockers": blockers,
        "safe_to_plan": not blockers,
    }
