"""Friendly CLI for installing Agent Harness Kit into a project."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

from . import __version__
from . import codex_dispatch
from . import request_router
from . import scheduler


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


def positive_integer(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


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
    schedule = commands.add_parser("schedule", help="compute the next safe parallel task batch")
    schedule.add_argument("graph", type=Path, help="TASK-GRAPH.md or graph JSON path")
    schedule.add_argument("--capacity", type=int, required=True, help="host-proven maximum concurrent implementation contexts")
    dispatch = commands.add_parser("codex-dispatch", help="prepare or record one native Codex agent dispatch")
    dispatch.add_argument("request", type=Path, help="JSON dispatch request or previously prepared plan")
    dispatch.add_argument("--response", type=Path, help="JSON adapter response to record")
    route = commands.add_parser("route", help="classify a request before workflow selection")
    route.add_argument("request", help="request text to classify")
    route.add_argument("--mode", choices=("auto", "vibe", "full"), default="auto", help="explicit routing mode")
    route.add_argument("--graph-bound", action="store_true", help="classify as graph-bound work")
    route.add_argument(
        "--graph-only-eligible",
        action="store_true",
        help="allow eligible graph-bound work to use the graph-only lane",
    )
    route.add_argument("--workstreams", type=positive_integer, default=1, help="positive workstream count")
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
    if args.command == "route":
        if not args.request.strip():
            print("ERROR: request must not be empty", file=sys.stderr)
            return 2
        decision = request_router.classify_request(
            args.request,
            graph_bound=args.graph_bound,
            graph_only_eligible=args.graph_only_eligible,
            explicit_mode=args.mode,
            workstream_count=args.workstreams,
        )
        print(json.dumps(decision, indent=2, ensure_ascii=False))
        return 0
    if args.command == "schedule":
        try:
            graph = scheduler.load_graph(args.graph.expanduser().resolve())
            plan = scheduler.schedule_ready(graph, capacity=args.capacity)
        except (OSError, json.JSONDecodeError, scheduler.ScheduleError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return 0
    if args.command == "codex-dispatch":
        try:
            request = json.loads(args.request.expanduser().resolve().read_text(encoding="utf-8"))
            if not isinstance(request, dict):
                raise codex_dispatch.DispatchError("dispatch input must be a JSON object")
            if args.response:
                response = json.loads(args.response.expanduser().resolve().read_text(encoding="utf-8"))
                if not isinstance(response, dict):
                    raise codex_dispatch.DispatchError("adapter response must be a JSON object")
                result = codex_dispatch.record_dispatch(request, response)
            else:
                result = codex_dispatch.build_dispatch(request)
        except (OSError, json.JSONDecodeError, codex_dispatch.DispatchError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    if args.command == "doctor":
        return doctor(args.path)
    installer = installer_module()
    if args.command == "prompt":
        print(installer.ACTIVATION_PROMPT)
        return 0
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
