#!/usr/bin/env python3
"""Build deterministic Agent Harness Kit distribution profiles with stdlib only."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "distribution" / "profiles"
PROJECT_METADATA = ROOT / "distribution" / "project.json"
IGNORED = {"work", "outputs", "__pycache__", ".git", "PACKAGE-MANIFEST.json"}
FIXED_TIME = (2000, 1, 1, 0, 0, 0)


def source_files() -> list[str]:
    return sorted(
        p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
        if p.is_file() and not any(part in IGNORED for part in p.relative_to(ROOT).parts)
    )


def read_profile(name: str, seen: set[str] | None = None) -> tuple[list[str], list[str]]:
    seen = seen or set()
    if name in seen:
        raise ValueError(f"profile inheritance cycle at {name}")
    path = PROFILES / f"{name}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    project = json.loads(PROJECT_METADATA.read_text(encoding="utf-8"))
    if data.get("project") != project["slug"]:
        raise ValueError(f"profile {name} has wrong project slug")
    if data.get("project_learning_activation") != "not-activated":
        raise ValueError(f"profile {name} must not activate project learning")
    includes: list[str] = []
    excludes: list[str] = []
    parent = data.get("extends")
    if parent:
        includes, _ = read_profile(parent, seen | {name})
    includes.extend(data.get("include", []))
    excludes.extend(data.get("exclude", []))
    return includes, excludes


def matches(path: str, pattern: str) -> bool:
    return fnmatch.fnmatchcase(path, pattern) or (pattern.endswith("/**") and path.startswith(pattern[:-3] + "/"))


def select(name: str) -> list[str]:
    includes, excludes = read_profile(name)
    files = [p for p in source_files() if any(matches(p, rule) for rule in includes)]
    files = [p for p in files if not any(matches(p, rule) for rule in excludes)]
    return sorted(set(files))


def boundary_errors(name: str, files: list[str]) -> list[str]:
    errors: list[str] = []
    if "LICENSE" not in files:
        errors.append(f"{name} does not include LICENSE")
    required_audio = {
        "media/agent-harness-kit-overview-en.mp3",
        "media/agent-harness-kit-overview-pt-BR.mp3",
        "media/overview-script-en.txt",
        "media/overview-script-pt-BR.txt",
        "media/overview-audio-manifest.json",
    }
    missing_audio = required_audio - set(files)
    if missing_audio:
        errors.append(f"{name} is missing overview audio: {sorted(missing_audio)}")
    if any(path.startswith("harness-state/") for path in files):
        errors.append(f"{name} contains activated host runtime state")
    project_learning = (
        "harness/roles/learning-", "harness/templates/LEARNING-",
        "harness/playbooks/learning-", "examples/development-plus-project-learning/",
        ".agents/skills/project-learning/", ".claude/skills/project-learning/",
        ".claude/agents/learning-assessor.md",
    )
    native_core = {
        "AGENTS.md", "CLAUDE.md", "adapters/codex.md", "adapters/claude.md",
        ".agents/skills/first-run-discovery/SKILL.md",
        ".agents/skills/graph-execution/SKILL.md",
        ".agents/skills/governed-review/SKILL.md",
        ".claude/skills/first-run-discovery/SKILL.md",
        ".claude/skills/graph-execution/SKILL.md",
        ".claude/skills/governed-review/SKILL.md",
        ".claude/agents/discovery-interviewer.md",
        ".claude/agents/task-specialist.md",
        ".claude/agents/independent-reviewer.md",
    }
    missing_native = native_core - set(files)
    if missing_native:
        errors.append(f"{name} is missing dual-platform native integration: {sorted(missing_native)}")
    if name == "core" and any(path.startswith(project_learning) for path in files):
        errors.append("core contains project-learning operational files")
    if name in {"core", "core-learning"} and any(path.startswith("learning-pack/") for path in files):
        errors.append(f"{name} contains learning-pack files")
    if name in {"core-learning", "full"}:
        expected_project_learning = {
            path for path in source_files()
            if path.startswith(project_learning)
        }
        missing_learning = expected_project_learning - set(files)
        if missing_learning:
            errors.append(f"{name} is missing project-learning files: {sorted(missing_learning)}")
    if name == "full":
        missing = set(source_files()) - set(files)
        if missing:
            errors.append(f"full is missing canonical source files: {sorted(missing)}")
    return errors


def manifest(name: str, version: str, files: list[str]) -> bytes:
    project = json.loads(PROJECT_METADATA.read_text(encoding="utf-8"))
    data = {
        "name": project["name"],
        "slug": project["slug"],
        "project_learning_activation": "not-activated",
        "profile": name,
        "version": version,
        "files": [{"path": path, "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest()} for path in files],
    }
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()


def build_zip(target: Path, name: str, version: str, files: list[str]) -> None:
    with zipfile.ZipFile(target, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            info = zipfile.ZipInfo(path, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (ROOT / path).read_bytes())
        info = zipfile.ZipInfo("PACKAGE-MANIFEST.json", FIXED_TIME)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, manifest(name, version, files))


def build_directory(target: Path, name: str, version: str, files: list[str]) -> None:
    target.mkdir(parents=True, exist_ok=False)
    for path in files:
        destination = target / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, destination)
    (target / "PACKAGE-MANIFEST.json").write_bytes(manifest(name, version, files))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("core", "core-learning", "full"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--format", choices=("zip", "directory"), default="zip")
    parser.add_argument("--check", action="store_true", help="validate selection without writing output")
    args = parser.parse_args()
    files = select(args.profile)
    errors = boundary_errors(args.profile, files)
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors), file=sys.stderr)
        return 1
    print(f"PROFILE {args.profile}: {len(files)} source files; boundaries passed")
    if args.check:
        return 0
    output = args.output.resolve()
    try:
        output.relative_to(ROOT)
    except ValueError:
        pass
    else:
        print("ERROR: output must be outside the source repository", file=sys.stderr)
        return 1
    project = json.loads(PROJECT_METADATA.read_text(encoding="utf-8"))
    version = (ROOT / project["version_file"]).read_text(encoding="utf-8").strip()
    output.mkdir(parents=True, exist_ok=True)
    suffix = ".zip" if args.format == "zip" else ""
    target = output / f"{project['slug']}-{version}-{args.profile}{suffix}"
    if target.exists():
        print(f"ERROR: target already exists: {target}", file=sys.stderr)
        return 1
    (build_zip if args.format == "zip" else build_directory)(target, args.profile, version, files)
    print(f"WROTE {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
