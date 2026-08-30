"""Deterministic ready-batch selection for agent-driven parallel dispatch."""

from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath


class ScheduleError(ValueError):
    """Raised when a graph cannot produce a safe dispatch plan."""


def normalize_owned_path(raw: str) -> str:
    value = raw.replace("\\", "/").strip()
    if value.endswith("/**"):
        value = value[:-3]
    if not value or value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        raise ScheduleError(f"invalid owned path: {raw!r}")
    parts = PurePosixPath(value).parts
    if ".." in parts:
        raise ScheduleError(f"invalid owned path: {raw!r}")
    wildcard_at = next((index for index, part in enumerate(parts) if "*" in part or "?" in part), None)
    if wildcard_at is not None:
        parts = parts[:wildcard_at]
    normalized = "/".join(part for part in parts if part not in {"", "."}).casefold().rstrip("/")
    if not normalized:
        raise ScheduleError(f"invalid owned path: {raw!r}")
    return normalized


def paths_collide(left: str, right: str) -> bool:
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def load_graph(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        match = re.search(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
        if not match:
            raise ScheduleError(f"no JSON graph block in {path}")
        data = json.loads(match.group(1))
    if not isinstance(data, dict):
        raise ScheduleError("graph root must be an object")
    return data


def _owned_paths(node: dict) -> list[str]:
    paths = node.get("write_set")
    if not isinstance(paths, list) or not paths:
        raise ScheduleError(f"{node.get('id', '<unknown>')} has no write_set")
    return [normalize_owned_path(str(path)) for path in paths]


def _collision(paths: list[str], owners: list[tuple[str, list[str]]]) -> str | None:
    for owner_id, owner_paths in owners:
        if any(paths_collide(left, right) for left in paths for right in owner_paths):
            return owner_id
    return None


def schedule_ready(graph: dict, *, capacity: int) -> dict:
    """Select the largest safe ready batch in stable graph order.

    The caller supplies host-proven parallel capacity. This function plans dispatch;
    the orchestrator still reserves leases and invokes the host's subagent API.
    """
    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
        raise ScheduleError("capacity must be a positive integer")
    nodes = graph.get("nodes")
    if not isinstance(nodes, list):
        raise ScheduleError("graph has no nodes array")
    by_id: dict[str, dict] = {}
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get("id"), str) or not node["id"]:
            raise ScheduleError("every node needs a unique string id")
        if node["id"] in by_id:
            raise ScheduleError(f"duplicate node id: {node['id']}")
        by_id[node["id"]] = node

    active = [node for node in nodes if node.get("status") == "active"]
    active_owners = [(node["id"], _owned_paths(node)) for node in active]
    available_slots = max(capacity - len(active), 0)
    selected: list[str] = []
    deferred: list[dict[str, str]] = []
    selected_owners: list[tuple[str, list[str]]] = []

    for node in nodes:
        if node.get("status") != "ready":
            continue
        node_id = node["id"]
        dependency_blocker = next(
            (
                str(dependency)
                for dependency in node.get("depends_on", [])
                if dependency not in by_id or by_id[dependency].get("status") != "completed"
            ),
            None,
        )
        if dependency_blocker:
            deferred.append({"id": node_id, "reason": f"dependency:{dependency_blocker}"})
            continue
        assurance_blocker = next(
            (
                str(required)
                for required in node.get("assurance_requires", [])
                if required not in by_id or by_id[required].get("assurance_status") != "accepted"
            ),
            None,
        )
        if assurance_blocker:
            deferred.append({"id": node_id, "reason": f"assurance:{assurance_blocker}"})
            continue
        owned_paths = _owned_paths(node)
        collision = _collision(owned_paths, active_owners + selected_owners)
        if collision:
            deferred.append({"id": node_id, "reason": f"write-collision:{collision}"})
            continue
        if len(selected) >= available_slots:
            deferred.append({"id": node_id, "reason": "capacity"})
            continue
        selected.append(node_id)
        selected_owners.append((node_id, owned_paths))

    return {
        "schema": "harness.parallel-dispatch-plan/v1",
        "capacity": capacity,
        "active_count": len(active),
        "available_slots": available_slots,
        "selected": selected,
        "deferred": deferred,
    }
