"""Load explicit client-runtime profiles without repository-wide globs."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
from typing import Any


RUNTIME_PROFILE_SCHEMA = "agent-harness-kit.runtime-profile/v1"
GENERATED_RUNTIME_PATHS = ("resources/templates.zip", "runtime.pyz")
RUNTIME_FILE_BUDGETS = {"core": 80, "core-learning": 96}
RUNTIME_FORBIDDEN_PREFIXES = (
    ".github/", "benchmarks/", "distribution/", "examples/", "media/", "validation/",
)


class RuntimeProfileError(ValueError):
    """Raised when a runtime profile is unsafe or internally inconsistent."""


def safe_relative(raw: object) -> str:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise RuntimeProfileError(f"unsafe runtime path: {raw!r}")
    candidate = PurePosixPath(raw)
    normalized = candidate.as_posix()
    if (
        candidate.is_absolute()
        or normalized != raw
        or not candidate.parts
        or ".." in candidate.parts
        or ":" in candidate.parts[0]
    ):
        raise RuntimeProfileError(f"unsafe runtime path: {raw!r}")
    return normalized


def _profile_path(root: Path, name: str) -> Path:
    return root / "distribution" / "runtime" / f"{name}.json"


def load_runtime_profile(root: Path, name: str, seen: set[str] | None = None) -> dict[str, Any]:
    """Return one resolved runtime profile with exact files and template members."""
    seen = seen or set()
    if name in seen:
        raise RuntimeProfileError(f"runtime profile inheritance cycle at {name}")
    path = _profile_path(root, name)
    if not path.is_file():
        raise RuntimeProfileError(f"runtime profile does not exist: {name}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != RUNTIME_PROFILE_SCHEMA or data.get("profile") != name:
        raise RuntimeProfileError(f"invalid runtime profile metadata: {name}")
    if data.get("project_learning_activation") != "not-activated":
        raise RuntimeProfileError(f"runtime profile {name} must not activate learning")

    declared_files = data.get("files", [])
    declared_templates = data.get("templates", [])
    if not isinstance(declared_files, list) or not isinstance(declared_templates, list):
        raise RuntimeProfileError(f"runtime profile {name} files and templates must be lists")

    files: list[str] = []
    templates: list[str] = []
    parent = data.get("extends")
    if parent:
        if not isinstance(parent, str):
            raise RuntimeProfileError(f"runtime profile {name} extends must be a string or null")
        resolved_parent = load_runtime_profile(root, str(parent), seen | {name})
        files.extend(resolved_parent["files"])
        templates.extend(resolved_parent["templates"])
    files.extend(safe_relative(item) for item in declared_files)
    templates.extend(safe_relative(item) for item in declared_templates)

    resolved_files = sorted(set(files))
    resolved_templates = sorted(set(templates))
    forbidden = [item for item in resolved_files if item.startswith(RUNTIME_FORBIDDEN_PREFIXES)]
    if forbidden:
        raise RuntimeProfileError(f"runtime profile {name} contains source-only files: {forbidden}")
    if any(item.startswith("harness/templates/") for item in resolved_files):
        raise RuntimeProfileError(f"runtime profile {name} must pack templates instead of exposing them")
    repository = root.resolve()
    missing: list[str] = []
    for item in resolved_files + resolved_templates:
        candidate = root / item
        if candidate.is_symlink() or not candidate.is_file():
            missing.append(item)
            continue
        try:
            candidate.resolve().relative_to(repository)
        except ValueError:
            missing.append(item)
    if missing:
        raise RuntimeProfileError(f"runtime profile {name} references missing or unsafe files: {missing}")
    return {
        "schema": RUNTIME_PROFILE_SCHEMA,
        "profile": name,
        "project_learning_activation": "not-activated",
        "files": resolved_files,
        "templates": resolved_templates,
        "generated": list(GENERATED_RUNTIME_PATHS),
    }


def runtime_payload_paths(root: Path, name: str) -> list[str]:
    profile = load_runtime_profile(root, name)
    return sorted(set(profile["files"]) | set(profile["generated"]))
