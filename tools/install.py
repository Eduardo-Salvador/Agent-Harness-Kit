#!/usr/bin/env python3
"""Install one contained Agent Harness Kit profile into a host project."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import shutil
import sys
import uuid
import zipfile
from pathlib import Path
from pathlib import PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_harness_kit.runtime_profiles import (
    RUNTIME_FILE_BUDGETS,
    RuntimeProfileError,
    load_runtime_profile,
    runtime_payload_paths,
)

DESTINATION_NAME = "agent-harness-kit"
BEGIN = "<!-- agent-harness-kit:begin -->"
END = "<!-- agent-harness-kit:end -->"
ENTRYPOINTS = {
    "AGENTS.md": ROOT / "harness" / "templates" / "ROOT-AGENTS-BRIDGE.md",
    "CLAUDE.md": ROOT / "harness" / "templates" / "ROOT-CLAUDE-BRIDGE.md",
}
ACTIVATION_PROMPT = (
    "Agent Harness Kit is installed in this project. Before scanning, proposing, planning, "
    "reporting status, or changing files, read the applicable root AGENTS.md or CLAUDE.md, "
    "then follow the referenced instructions under agent-harness-kit/. Check "
    "harness-state/PROJECT-CONTEXT.md first: approved context resumes without a first-run "
    "welcome; only missing or unapproved context starts first-run discovery."
)


class InstallError(RuntimeError):
    pass


RUNTIME_MANIFEST_SCHEMA = "agent-harness-kit.runtime-manifest/v1"
FIXED_TIME = (2000, 1, 1, 0, 0, 0)


def safe_relative(raw: object) -> str:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise InstallError(f"unsafe package path: {raw!r}")
    candidate = PurePosixPath(raw)
    normalized = candidate.as_posix()
    if (
        candidate.is_absolute()
        or normalized != raw
        or not candidate.parts
        or ".." in candidate.parts
        or ":" in candidate.parts[0]
    ):
        raise InstallError(f"unsafe package path: {raw!r}")
    return normalized


def package_files(profile: str) -> list[str]:
    manifest_path = ROOT / "PACKAGE-MANIFEST.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("profile") != profile:
            raise InstallError(f"package profile is {manifest.get('profile')!r}, not {profile!r}")
        source_overrides = package_module_overlays()
        files = []
        for entry in manifest.get("files", []):
            path = safe_relative(entry.get("path") if isinstance(entry, dict) else None)
            source = source_overrides.get(path, ROOT / path).resolve()
            try:
                source.relative_to(ROOT.parent.resolve() if path in source_overrides else ROOT.resolve())
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


def package_module_overlays() -> dict[str, Path]:
    """Expose wheel runtime modules inside the contained installed profile."""
    if ROOT.name != "assets":
        return {}
    package_root = ROOT.parent
    if not (package_root / "__init__.py").is_file():
        return {}
    return {
        f"agent_harness_kit/{source.name}": source
        for source in sorted(package_root.glob("*.py"))
        if source.is_file() and not source.is_symlink()
    }


def runtime_files(profile: str) -> list[str]:
    """Return the exact compact payload, including generated runtime resources."""
    if profile not in {"core", "core-learning"}:
        return package_files(profile)
    try:
        return runtime_payload_paths(ROOT, profile)
    except (RuntimeProfileError, OSError, json.JSONDecodeError) as exc:
        raise InstallError(str(exc)) from exc


def _zip_entry(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data)


def runtime_archive_sources() -> dict[str, Path]:
    """Return every Python source incorporated into the portable runtime."""
    package_root = ROOT.parent if ROOT.name == "assets" else ROOT / "agent_harness_kit"
    if not (package_root / "cli.py").is_file():
        raise InstallError(f"runtime package modules are missing from {package_root}")
    return {
        f"agent_harness_kit/{source.name}": source
        for source in sorted(package_root.glob("*.py"))
        if source.is_file() and not source.is_symlink()
    }


def verify_compact_source_closure(profile: str, resolved: dict[str, object]) -> None:
    """Verify a generated package before any compact artifacts are derived from it."""
    if not (ROOT / "PACKAGE-MANIFEST.json").is_file():
        return
    declared = set(package_files(profile))
    declared.discard("PACKAGE-MANIFEST.json")
    required = set(resolved["files"]) | set(resolved["templates"])
    required.update(runtime_archive_sources())
    required.update({
        "VERSION",
        "tools/install.py",
        "distribution/runtime/core.json",
        f"distribution/runtime/{profile}.json",
        "harness/templates/ROOT-AGENTS-BRIDGE.md",
        "harness/templates/ROOT-CLAUDE-BRIDGE.md",
    })
    missing = sorted(required - declared)
    if missing:
        raise InstallError(f"package manifest does not declare compact runtime sources: {missing}")


def runtime_archive() -> bytes:
    """Build a deterministic portable zipapp containing the CLI runtime modules."""
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        _zip_entry(
            archive,
            "__main__.py",
            b"from agent_harness_kit.cli import main\nraise SystemExit(main())\n",
        )
        for relative, source in sorted(runtime_archive_sources().items()):
            _zip_entry(archive, relative, source.read_bytes())
    return stream.getvalue()


def template_archive(profile: str) -> tuple[bytes, list[dict[str, str]]]:
    """Pack canonical templates without exposing dozens of client files."""
    resolved = load_runtime_profile(ROOT, profile)
    stream = io.BytesIO()
    entries: list[dict[str, str]] = []
    members: set[str] = set()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in resolved["templates"]:
            data = (ROOT / relative).read_bytes()
            member = Path(relative).name
            if member in members:
                raise InstallError(f"duplicate template archive member: {member}")
            members.add(member)
            _zip_entry(archive, member, data)
            entries.append({"path": member, "sha256": hashlib.sha256(data).hexdigest()})
    return stream.getvalue(), entries


def generated_runtime_files(profile: str) -> tuple[dict[str, bytes], list[dict[str, str]]]:
    templates, template_entries = template_archive(profile)
    return {
        "resources/templates.zip": templates,
        "runtime.pyz": runtime_archive(),
    }, template_entries


def runtime_manifest(
    profile: str,
    version: str,
    static_files: list[str],
    generated: dict[str, bytes],
    template_entries: list[dict[str, str]],
) -> bytes:
    entries = []
    for relative in sorted(set(static_files) | set(generated)):
        data = generated.get(relative)
        digest = hashlib.sha256(data if data is not None else (ROOT / relative).read_bytes()).hexdigest()
        entries.append({"path": relative, "sha256": digest})
    payload = {
        "schema": RUNTIME_MANIFEST_SCHEMA,
        "name": "Agent Harness Kit",
        "slug": "agent-harness-kit",
        "profile": profile,
        "version": version,
        "project_learning_activation": "not-activated",
        "file_budget": RUNTIME_FILE_BUDGETS[profile],
        "files": entries,
        "resources": {"templates": template_entries},
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


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
    source_root = ROOT.resolve()
    if host_root == source_root or host_root in source_root.parents or source_root in host_root.parents:
        raise InstallError("Kit source and host project must be separate, non-nested directories")
    destination = host_root / DESTINATION_NAME
    if destination.exists() or destination.is_symlink():
        raise InstallError(f"destination already exists: {destination}")
    compact_runtime = profile in {"core", "core-learning"}
    generated: dict[str, bytes] = {}
    template_entries: list[dict[str, str]] = []
    if compact_runtime:
        try:
            resolved = load_runtime_profile(ROOT, profile)
            verify_compact_source_closure(profile, resolved)
            static_files = list(resolved["files"])
            generated, template_entries = generated_runtime_files(profile)
        except (RuntimeProfileError, OSError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
            raise InstallError(f"compact runtime {profile} is invalid: {exc}") from exc
        source_overrides: dict[str, Path] = {}
        files = sorted(set(static_files) | set(generated))
        installed_count = len(files) + 1
        if installed_count > RUNTIME_FILE_BUDGETS[profile]:
            raise InstallError(
                f"compact runtime {profile} has {installed_count} files; "
                f"budget is {RUNTIME_FILE_BUDGETS[profile]}"
            )
    else:
        files = package_files(profile)
        source_overrides = package_module_overlays()
        files = sorted(set(files) | set(source_overrides))
    generated_manifest: bytes | None = None
    if compact_runtime:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        generated_manifest = runtime_manifest(profile, version, static_files, generated, template_entries)
    elif "PACKAGE-MANIFEST.json" not in files:
        sys.path.insert(0, str(ROOT / "tools"))
        from package import manifest

        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        generated_manifest = manifest(profile, version, files, source_overrides)
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
            target = (staged_distribution / relative).resolve()
            generated_data = generated.get(relative)
            source = source_overrides.get(relative, ROOT / relative).resolve() if generated_data is None else None
            try:
                target.relative_to(staged_distribution.resolve())
                if source is not None:
                    if relative in source_overrides:
                        source.relative_to(ROOT.parent.resolve())
                    else:
                        source.relative_to(ROOT.resolve())
            except ValueError as exc:
                raise InstallError(f"package path escapes installation boundary: {relative}") from exc
            if source is not None and (source.is_symlink() or not source.is_file()):
                raise InstallError(f"source must be a regular file: {relative}")
            target.parent.mkdir(parents=True, exist_ok=True)
            if generated_data is None:
                assert source is not None
                shutil.copyfile(source, target)
            else:
                target.write_bytes(generated_data)
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install Agent Harness Kit into a host project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
epilog="""profiles:
  core           Compact delivery, graph, status, review, and validation runtime.
  core-learning  Compact core plus optional, consented project-learning support.
  full           Expanded source, QA, media, learning, and harness-engineering study pack.

examples:
  python tools/install.py --profile core --host ../my-project --dry-run
  python tools/install.py --profile core-learning --host ../my-project

The Kit source/fork and host project must be different directories. After installation,
open a new agent context at the host-project root so AGENTS.md or CLAUDE.md is reloaded.
Beginner guides: README.pt-BR.md and README.md#beginner-installation.""",
    )
    parser.add_argument(
        "--profile",
        choices=("core", "core-learning", "full"),
        required=True,
        help="installation profile; see descriptions below",
    )
    parser.add_argument("--host", type=Path, required=True, help="existing project directory that will receive the Kit")
    parser.add_argument("--dry-run", action="store_true", help="show planned actions without writing files")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        actions = install(args.profile, args.host, args.dry_run)
    except (InstallError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    prefix = "WOULD " if args.dry_run else "DONE "
    for action in actions:
        print(prefix + action)
    if not args.dry_run:
        print("NEXT Open a new agent context at the host-project root.")
        print("NEXT If the host does not load root instructions automatically, paste this prompt:")
        print(ACTIVATION_PROMPT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
