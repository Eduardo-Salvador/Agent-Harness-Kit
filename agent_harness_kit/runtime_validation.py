"""Validate a compact installed runtime without executing source QA fixtures."""

from __future__ import annotations

import hashlib
import json
import posixpath
import re
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

from .runtime_profiles import RUNTIME_FILE_BUDGETS, RUNTIME_FORBIDDEN_PREFIXES


RUNTIME_MANIFEST_SCHEMA = "agent-harness-kit.runtime-manifest/v1"
IGNORED_RUNTIME_PARTS = {"__pycache__"}
REQUIRED_RUNTIME_FILES = {
    "AGENTS.md",
    "CLAUDE.md",
    "LICENSE",
    "VERSION",
    "resources/templates.zip",
    "runtime.pyz",
    "tools/validate.py",
    ".agents/skills/request-router/SKILL.md",
    ".agents/skills/first-run-discovery/SKILL.md",
    ".claude/skills/request-router/SKILL.md",
    ".claude/skills/first-run-discovery/SKILL.md",
}
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


class RuntimeValidationError(ValueError):
    """Raised when runtime validation cannot safely inspect its input."""


def _safe_relative(raw: object) -> str:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise RuntimeValidationError(f"unsafe manifest path: {raw!r}")
    candidate = PurePosixPath(raw)
    if (
        candidate.is_absolute()
        or candidate.as_posix() != raw
        or not candidate.parts
        or ".." in candidate.parts
        or ":" in candidate.parts[0]
    ):
        raise RuntimeValidationError(f"unsafe manifest path: {raw!r}")
    return raw


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_runtime_manifest(kit_root: Path) -> dict:
    path = kit_root.expanduser().resolve() / "PACKAGE-MANIFEST.json"
    if path.is_symlink():
        raise RuntimeValidationError("runtime manifest must not be a symlink")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeValidationError(f"runtime manifest is unreadable: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("schema") != RUNTIME_MANIFEST_SCHEMA:
        raise RuntimeValidationError("runtime manifest schema is invalid")
    return payload


def _actual_files(kit_root: Path) -> set[str]:
    result: set[str] = set()
    for path in kit_root.rglob("*"):
        relative = path.relative_to(kit_root)
        if any(part in IGNORED_RUNTIME_PARTS for part in relative.parts):
            continue
        if path.is_file() and path.name != "PACKAGE-MANIFEST.json" and path.suffix != ".pyc":
            result.add(relative.as_posix())
    return result


def _template_pack_errors(kit_root: Path, manifest: dict) -> list[str]:
    errors: list[str] = []
    resources = manifest.get("resources", {})
    if not isinstance(resources, dict):
        return ["runtime.resources-manifest: expected an object"]
    expected = resources.get("templates", [])
    if not isinstance(expected, list):
        return ["runtime.templates-manifest: expected a list"]
    expected_map: dict[str, str] = {}
    for entry in expected:
        if not isinstance(entry, dict):
            errors.append("runtime.templates-manifest: invalid entry")
            continue
        try:
            name = _safe_relative(entry.get("path"))
        except RuntimeValidationError as exc:
            errors.append(f"runtime.templates-path: {exc}")
            continue
        if name in expected_map:
            errors.append(f"runtime.templates-duplicate: {name}")
        digest = str(entry.get("sha256", ""))
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(f"runtime.templates-hash-format: {name}")
        expected_map[name] = digest
    pack = kit_root / "resources" / "templates.zip"
    if not pack.is_file():
        return errors + ["runtime.templates-pack: missing resources/templates.zip"]
    if pack.is_symlink():
        return errors + ["runtime.templates-pack: resources/templates.zip must not be a symlink"]
    try:
        with zipfile.ZipFile(pack) as archive:
            actual = {name for name in archive.namelist() if not name.endswith("/")}
            for name in actual:
                try:
                    _safe_relative(name)
                except RuntimeValidationError as exc:
                    errors.append(f"runtime.templates-path: {exc}")
            for missing in sorted(set(expected_map) - actual):
                errors.append(f"runtime.templates-missing: {missing}")
            for extra in sorted(actual - set(expected_map)):
                errors.append(f"runtime.templates-unlisted: {extra}")
            for name in sorted(actual & set(expected_map)):
                digest = hashlib.sha256(archive.read(name)).hexdigest()
                if digest != expected_map[name]:
                    errors.append(f"runtime.templates-hash: {name}")
    except (OSError, zipfile.BadZipFile) as exc:
        errors.append(f"runtime.templates-pack: {exc}")
    return errors


def _runtime_archive_errors(kit_root: Path) -> list[str]:
    archive_path = kit_root / "runtime.pyz"
    required = {
        "__main__.py",
        "agent_harness_kit/__init__.py",
        "agent_harness_kit/cli.py",
        "agent_harness_kit/runtime_resources.py",
        "agent_harness_kit/runtime_validation.py",
    }
    try:
        with zipfile.ZipFile(archive_path) as archive:
            names = {name for name in archive.namelist() if not name.endswith("/")}
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"runtime.archive: {exc}"]
    return [f"runtime.archive-missing: {name}" for name in sorted(required - names)]


def _markdown_link_errors(kit_root: Path, expected_files: set[str]) -> list[str]:
    errors: list[str] = []
    for relative in sorted(path for path in expected_files if path.casefold().endswith(".md")):
        path = kit_root / relative
        if not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            errors.append(f"runtime.markdown-unreadable: {relative}: {exc}")
            continue
        for line_number, line in enumerate(lines, 1):
            for match in MARKDOWN_LINK.finditer(line):
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
                if resolved.startswith("../") or resolved not in expected_files:
                    errors.append(f"runtime.markdown-link: {relative}:{line_number} -> {raw}")
    return errors


def _bridge_errors(host_root: Path) -> list[str]:
    errors: list[str] = []
    expected = {
        "AGENTS.md": "agent-harness-kit/AGENTS.md",
        "CLAUDE.md": "@agent-harness-kit/CLAUDE.md",
    }
    for name, route in expected.items():
        path = host_root / name
        if not path.is_file():
            errors.append(f"runtime.bridge-missing: {name}")
            continue
        if path.is_symlink():
            errors.append(f"runtime.bridge-symlink: {name}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"runtime.bridge-unreadable: {name}: {exc}")
            continue
        if text.count("<!-- agent-harness-kit:begin -->") != 1 or text.count("<!-- agent-harness-kit:end -->") != 1:
            errors.append(f"runtime.bridge-markers: {name}")
        if route not in text:
            errors.append(f"runtime.bridge-route: {name}")
    return errors


def validate_runtime_install(kit_root: Path, host_root: Path | None = None) -> list[str]:
    """Return deterministic integrity and client-boundary errors for one installation."""
    kit = kit_root.expanduser().resolve()
    host = host_root.expanduser().resolve() if host_root is not None else kit.parent
    try:
        manifest = load_runtime_manifest(kit)
    except RuntimeValidationError as exc:
        return [f"runtime.manifest: {exc}"]

    errors: list[str] = []
    entries = manifest.get("files")
    if not isinstance(entries, list):
        return ["runtime.manifest-files: expected a list"]
    expected: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("runtime.manifest-files: invalid entry")
            continue
        try:
            relative = _safe_relative(entry.get("path"))
        except RuntimeValidationError as exc:
            errors.append(f"runtime.manifest-path: {exc}")
            continue
        if relative in expected:
            errors.append(f"runtime.manifest-duplicate: {relative}")
        digest = str(entry.get("sha256", ""))
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(f"runtime.manifest-hash-format: {relative}")
        expected[relative] = digest

    profile = manifest.get("profile")
    budgets = RUNTIME_FILE_BUDGETS
    if profile not in budgets:
        errors.append(f"runtime.profile: {profile!r}")
    elif manifest.get("file_budget") != budgets[profile]:
        errors.append(f"runtime.file-budget-declaration: {profile}")
    if not isinstance(manifest.get("version"), str) or not manifest["version"].strip():
        errors.append("runtime.version: missing")

    for missing in sorted(REQUIRED_RUNTIME_FILES - set(expected)):
        errors.append(f"runtime.required: {missing}")
    for relative in sorted(expected):
        if relative.startswith(RUNTIME_FORBIDDEN_PREFIXES):
            errors.append(f"runtime.forbidden-client-payload: {relative}")
        path = kit / relative
        if path.is_symlink():
            errors.append(f"runtime.file-symlink: {relative}")
        elif not path.is_file():
            errors.append(f"runtime.file-missing: {relative}")
        elif _sha256(path) != expected[relative]:
            errors.append(f"runtime.file-hash: {relative}")

    actual = _actual_files(kit)
    for relative in sorted(actual - set(expected)):
        errors.append(f"runtime.file-unlisted: {relative}")
    if profile in budgets and len(entries) + 1 > budgets[profile]:
        errors.append(f"runtime.file-budget: {profile} has {len(entries) + 1} files")
    if manifest.get("project_learning_activation") != "not-activated":
        errors.append("runtime.learning-activation: installation must not activate learning")
    errors.extend(_template_pack_errors(kit, manifest))
    errors.extend(_runtime_archive_errors(kit))
    errors.extend(_markdown_link_errors(kit, set(expected)))
    errors.extend(_bridge_errors(host))
    return errors
