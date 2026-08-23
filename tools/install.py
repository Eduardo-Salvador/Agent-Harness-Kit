#!/usr/bin/env python3
"""Install one contained Agent Harness Kit profile into a host project."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import uuid
from pathlib import Path
from pathlib import PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DESTINATION_NAME = "agent-harness-kit"
BEGIN = "<!-- agent-harness-kit:begin -->"
END = "<!-- agent-harness-kit:end -->"
ENTRYPOINTS = {
    "AGENTS.md": ROOT / "harness" / "templates" / "ROOT-AGENTS-BRIDGE.md",
    "CLAUDE.md": ROOT / "harness" / "templates" / "ROOT-CLAUDE-BRIDGE.md",
}


class InstallError(RuntimeError):
    pass


def safe_relative(raw: object) -> str:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise InstallError(f"unsafe package path: {raw!r}")
    candidate = PurePosixPath(raw)
    normalized = candidate.as_posix()
    if candidate.is_absolute() or normalized != raw or ".." in candidate.parts or ":" in candidate.parts[0]:
        raise InstallError(f"unsafe package path: {raw!r}")
    return normalized


def package_files(profile: str) -> list[str]:
    manifest_path = ROOT / "PACKAGE-MANIFEST.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("profile") != profile:
            raise InstallError(f"package profile is {manifest.get('profile')!r}, not {profile!r}")
        files = []
        for entry in manifest.get("files", []):
            path = safe_relative(entry.get("path") if isinstance(entry, dict) else None)
            source = (ROOT / path).resolve()
            try:
                source.relative_to(ROOT.resolve())
            except ValueError as exc:
                raise InstallError(f"package path escapes source: {path}") from exc
            if not source.is_file():
                raise InstallError(f"package manifest references missing file: {path!r}")
            actual = hashlib.sha256(source.read_bytes()).hexdigest()
            if actual != entry.get("sha256"):
                raise InstallError(f"package file hash mismatch: {path}")
            files.append(path)
        files.append("PACKAGE-MANIFEST.json")
        return sorted(files)
    sys.path.insert(0, str(ROOT / "tools"))
    from package import boundary_errors, select

    files = select(profile)
    errors = boundary_errors(profile, files)
    if errors:
        raise InstallError("; ".join(errors))
    return [safe_relative(path) for path in files]


def newline_for(data: bytes) -> str:
    return "\r\n" if b"\r\n" in data else "\n"


def render_entrypoint(path: Path, bridge_path: Path) -> bytes:
    bridge = bridge_path.read_text(encoding="utf-8").strip()
    if bridge.count(BEGIN) != 1 or bridge.count(END) != 1:
        raise InstallError(f"invalid bridge template: {bridge_path.name}")
    if not path.exists():
        return (bridge + "\n").encode("utf-8")
    if path.is_symlink() or not path.is_file():
        raise InstallError(f"entrypoint must be a regular file: {path.name}")
    original = path.read_bytes()
    text = original.decode("utf-8")
    bom = "\ufeff" if text.startswith("\ufeff") else ""
    body = text[len(bom):]
    begin_count = body.count(BEGIN)
    end_count = body.count(END)
    if begin_count != end_count or begin_count > 1:
        raise InstallError(f"malformed or duplicated managed block in {path.name}")
    newline = newline_for(original)
    normalized_bridge = bridge.replace("\n", newline)
    if begin_count == 1:
        start = body.index(BEGIN)
        finish = body.index(END, start) + len(END)
        remaining = (body[:start] + body[finish:]).lstrip("\r\n")
    else:
        remaining = body
    separator = newline if remaining else ""
    updated = bom + normalized_bridge + newline + separator + remaining
    return updated.encode("utf-8")


def install(profile: str, host: Path, dry_run: bool) -> list[str]:
    requested_host = host.expanduser()
    if requested_host.is_symlink():
        raise InstallError("host path must not be a symlink")
    host_root = requested_host.resolve()
    if not host_root.is_dir():
        raise InstallError(f"host directory does not exist: {host_root}")
    destination = host_root / DESTINATION_NAME
    if destination.exists() or destination.is_symlink():
        raise InstallError(f"destination already exists: {destination}")
    files = package_files(profile)
    generated_manifest: bytes | None = None
    if "PACKAGE-MANIFEST.json" not in files:
        sys.path.insert(0, str(ROOT / "tools"))
        from package import manifest

        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        generated_manifest = manifest(profile, version, files)
    rendered = {name: render_entrypoint(host_root / name, bridge) for name, bridge in ENTRYPOINTS.items()}
    installed_count = len(files) + (1 if generated_manifest is not None else 0)
    actions = [f"install {installed_count} files into {destination}"]
    actions.extend(f"create or update managed bridge in {host_root / name}" for name in ENTRYPOINTS)
    if dry_run:
        return actions

    staging = host_root / f".ahk-{uuid.uuid4().hex[:8]}"
    staging.mkdir()
    staged_distribution = staging / "kit"
    originals = {name: (host_root / name).read_bytes() if (host_root / name).is_file() else None for name in ENTRYPOINTS}
    try:
        staged_distribution.mkdir()
        for relative in files:
            relative = safe_relative(relative)
            source = (ROOT / relative).resolve()
            target = (staged_distribution / relative).resolve()
            try:
                source.relative_to(ROOT.resolve())
                target.relative_to(staged_distribution.resolve())
            except ValueError as exc:
                raise InstallError(f"package path escapes installation boundary: {relative}") from exc
            if source.is_symlink() or not source.is_file():
                raise InstallError(f"source must be a regular file: {relative}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        if generated_manifest is not None:
            (staged_distribution / "PACKAGE-MANIFEST.json").write_bytes(generated_manifest)
        os.replace(staged_distribution, destination)
        for name, content in rendered.items():
            target = host_root / name
            temporary = staging / f"{name}.new"
            temporary.write_bytes(content)
            os.replace(temporary, target)
    except Exception:
        if destination.exists():
            shutil.rmtree(destination)
        for name, content in originals.items():
            target = host_root / name
            if content is None:
                if target.exists():
                    target.unlink()
            else:
                target.write_bytes(content)
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return actions


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Agent Harness Kit into a host project")
    parser.add_argument("--profile", choices=("core", "core-learning", "full"), required=True)
    parser.add_argument("--host", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        actions = install(args.profile, args.host, args.dry_run)
    except (InstallError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    prefix = "WOULD " if args.dry_run else "DONE "
    for action in actions:
        print(prefix + action)
    return 0


if __name__ == "__main__":
    sys.exit(main())
