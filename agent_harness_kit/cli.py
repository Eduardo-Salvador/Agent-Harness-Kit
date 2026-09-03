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
from . import delivery_modes
from . import preflight
from . import request_router
from . import scheduler
from . import state_runtime


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


def env_consumer(value: str) -> tuple[str, str]:
    name, separator, path = value.partition("=")
    if not separator or not name.strip() or not path.strip():
        raise argparse.ArgumentTypeError("must use ENV_NAME=project/relative/path")
    return name.strip(), path.strip()


def command_probe(value: str) -> list[str]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError("must be a JSON string array") from exc
    if not isinstance(parsed, list) or not parsed or not all(isinstance(part, str) and part for part in parsed):
        raise argparse.ArgumentTypeError("must be a non-empty JSON string array")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-harness",
        description="Install and inspect Agent Harness Kit.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command")

    delivery = commands.add_parser("delivery-mode", help="inspect a delivery preset without changing project state")
    delivery.add_argument("preset", nargs="?", choices=delivery_modes.PRESETS, default="accompanied")

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
    preflight_command = commands.add_parser("preflight", help="verify declared prerequisites before planning")
    preflight_command.add_argument("path", nargs="?", type=Path, default=Path.cwd(), help="project directory")
    preflight_command.add_argument("--path", dest="required_paths", action="append", default=[], help="required project-relative path")
    preflight_command.add_argument("--script", dest="required_scripts", action="append", default=[], help="required package.json script")
    preflight_command.add_argument("--env", dest="required_env", action="append", default=[], help="required environment variable name")
    preflight_command.add_argument("--command", dest="required_commands", action="append", default=[], help="required executable")
    preflight_command.add_argument("--env-consumer", type=env_consumer, action="append", default=[], help="ENV_NAME=project-relative consumer path")
    preflight_command.add_argument("--probe-command", type=command_probe, action="append", default=[], help='safe native probe as JSON, e.g. ["python","--version"]')
    preflight_command.add_argument("--browser", choices=("not-required", "available", "required-unavailable"), default="not-required")
    preflight_command.add_argument("--sandbox", choices=("not-required", "available", "required-unavailable"), default="not-required")
    preflight_command.add_argument("--workers", type=int, default=1, help="proven worker capacity; zero blocks planning")
    preflight_command.add_argument("--no-validator", action="store_true", help="do not require a Harness validator in the target")
    transition = commands.add_parser("transition", help="atomically advance one task in TASK-GRAPH")
    transition.add_argument("graph", type=Path)
    transition.add_argument("task")
    transition.add_argument("status", choices=("pending", "ready", "active", "completed", "blocked"))
    transition.add_argument("--expected-revision", type=int, required=True)
    transition.add_argument("--actor", required=True)
    transition.add_argument("--context", required=True)
    transition.add_argument("--reason")
    metrics = commands.add_parser("metrics", help="summarize the append-only runtime metrics ledger")
    metrics.add_argument("ledger", type=Path)
    metrics.add_argument("--no-gate-threshold", type=positive_integer, default=3)
    metric_record = commands.add_parser("metric-record", help="append one declared run metric JSON payload")
    metric_record.add_argument("input", type=Path, help="JSON object with record_metric fields")
    metric_record.add_argument("ledger", type=Path, help="destination metrics.jsonl")
    dispatch = commands.add_parser("codex-dispatch", help="prepare or record one native Codex agent dispatch")
    dispatch.add_argument("request", type=Path, help="JSON dispatch request or previously prepared plan")
    dispatch.add_argument("--response", type=Path, help="JSON adapter response to record")
    route = commands.add_parser("route", help="classify a request before workflow selection")
    route.add_argument("request", help="request text to classify")
    route.add_argument(
        "--mode",
        choices=("auto", "direct-trivial", "vibe", "graph-only", "full"),
        default="auto",
        help="explicit routing mode",
    )
    route.add_argument("--assurance", choices=("auto", "none", "light", "full"), default="auto")
    route.add_argument("--shape", choices=("auto", "compact", "complete"), default="auto")
    route.add_argument("--agents", type=positive_integer, default=1, help="positive count of real execution agents")
    route.add_argument("--human-loop", action="store_true", help="require explicit human-in-loop execution")
    route.add_argument("--audit-required", action="store_true", help="require auditable full execution")
    route.add_argument("--model-capability", choices=("strong", "normal", "weak"), default="normal")
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
    if args.command == "delivery-mode":
        print(json.dumps(delivery_modes.resolve_delivery_mode(args.preset), indent=2))
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
            assurance=args.assurance,
            harness_shape=args.shape,
            agent_count=args.agents,
            human_in_loop=args.human_loop,
            audit_required=args.audit_required,
            model_capability=args.model_capability,
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
    if args.command == "preflight":
        try:
            consumers: dict[str, list[str]] = {}
            for name, path in args.env_consumer:
                consumers.setdefault(name, []).append(path)
            result = preflight.run_preflight(
                args.path,
                required_paths=args.required_paths,
                required_scripts=args.required_scripts,
                required_env=args.required_env,
                required_commands=args.required_commands,
                env_consumers=consumers,
                command_probes=args.probe_command,
                browser=args.browser,
                sandbox=args.sandbox,
                workers=args.workers,
                validator="not-required" if args.no_validator else "required",
            )
        except (OSError, preflight.PreflightError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["status"] == "passed" else 1
    if args.command == "transition":
        try:
            result = state_runtime.transition_task_graph(
                args.graph.expanduser().resolve(), args.task, args.status,
                args.expected_revision, args.actor, args.context, reason=args.reason,
            )
        except (OSError, KeyError, ValueError, state_runtime.StateRuntimeError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    if args.command == "metrics":
        try:
            result = state_runtime.summarize_metrics(
                args.ledger.expanduser().resolve(), no_gate_threshold=args.no_gate_threshold,
            )
        except (OSError, ValueError, state_runtime.StateRuntimeError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    if args.command == "metric-record":
        try:
            payload = json.loads(args.input.expanduser().resolve().read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("metric input must be a JSON object")
            result = state_runtime.record_metric(args.ledger.expanduser().resolve(), **payload)
        except (OSError, TypeError, ValueError, json.JSONDecodeError, state_runtime.StateRuntimeError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2, ensure_ascii=False))
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
