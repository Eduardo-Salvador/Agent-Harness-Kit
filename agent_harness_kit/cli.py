"""Friendly CLI for installing Agent Harness Kit into a project."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

from . import __version__


def source_root() -> Path:
    bundled = Path(__file__).resolve().parent / "assets"
    if (bundled / "tools" / "install.py").is_file():
        return bundled
    checkout = Path(__file__).resolve().parents[1]
    if (checkout / "tools" / "install.py").is_file():
        return checkout
    raise RuntimeError("Agent Harness Kit assets are missing from this installation")


def installer_module() -> ModuleType:
    root = source_root()
    path = root / "tools" / "install.py"
    spec = importlib.util.spec_from_file_location("agent_harness_kit_embedded_installer", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load installer from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-harness",
        description="Install and inspect Agent Harness Kit.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command")

    install = commands.add_parser("install", help="install the Kit into a project")
    install.add_argument("path", nargs="?", type=Path, default=Path.cwd(), help="project directory (default: current directory)")
    install.add_argument(
        "--profile",
        choices=("core", "core-learning", "full"),
        default="core",
        help="content profile (default: core)",
    )
    install.add_argument("--dry-run", action="store_true", help="preview without changing files")

    commands.add_parser("prompt", help="print the fallback activation prompt")
    doctor = commands.add_parser("doctor", help="check whether a project has the expected entrypoints")
    doctor.add_argument("path", nargs="?", type=Path, default=Path.cwd(), help="project directory (default: current directory)")
    return parser


def doctor(path: Path) -> int:
    root = path.expanduser().resolve()
    expected = ("AGENTS.md", "CLAUDE.md", "agent-harness-kit/PACKAGE-MANIFEST.json")
    missing = [item for item in expected if not (root / item).is_file()]
    if missing:
        print("Agent Harness Kit is not ready in this project.")
        for item in missing:
            print(f"MISSING {item}")
        return 1
    print(f"Agent Harness Kit is ready in {root}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    installer = installer_module()
    if args.command == "prompt":
        print(installer.ACTIVATION_PROMPT)
        return 0
    if args.command == "doctor":
        return doctor(args.path)
    try:
        actions = installer.install(args.profile, args.path, args.dry_run)
    except installer.InstallError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    prefix = "WOULD" if args.dry_run else "DONE"
    for action in actions:
        print(f"{prefix}: {action}")
    if not args.dry_run:
        print("\nOpen a new agent context at the project root.")
        print("If the Kit is not detected automatically, run: agent-harness prompt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
