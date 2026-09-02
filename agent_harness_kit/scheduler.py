"""Deterministic ready-batch selection for agent-driven parallel dispatch."""

from __future__ import annotations

import json
import re
from itertools import combinations
from pathlib import Path, PurePosixPath

from .readiness import readiness_blocker


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
    """Select a maximum-cardinality safe ready batch in stable graph order.

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
    deferred: list[dict[str, str]] = []
    candidates: list[tuple[str, list[str]]] = []

    for node in nodes:
        if node.get("status") != "ready":
            continue
        node_id = node["id"]
        blocker = readiness_blocker(node, by_id)
        if blocker:
            deferred.append({"id": node_id, "reason": blocker})
            continue
        owned_paths = _owned_paths(node)
        collision = _collision(owned_paths, active_owners)
        if collision:
            deferred.append({"id": node_id, "reason": f"write-collision:{collision}"})
            continue
        candidates.append((node_id, owned_paths))

    maximum_safe: list[tuple[str, list[str]]] = []
    for size in range(len(candidates), -1, -1):
        for indexes in combinations(range(len(candidates)), size):
            batch = [candidates[index] for index in indexes]
            if all(
                not any(paths_collide(left, right) for left in left_paths for right in right_paths)
                for offset, (_, left_paths) in enumerate(batch)
                for _, right_paths in batch[offset + 1 :]
            ):
                maximum_safe = batch
                break
        if maximum_safe or size == 0:
            break

    selected_owners = maximum_safe[:available_slots]

    selected = [node_id for node_id, _ in selected_owners]
    selected_ids = set(selected)
    already_deferred = {item["id"] for item in deferred}
    for node_id, owned_paths in candidates:
        if node_id in selected_ids or node_id in already_deferred:
            continue
        collision = _collision(owned_paths, selected_owners)
        deferred.append({
            "id": node_id,
            "reason": f"write-collision:{collision}" if collision else "capacity",
        })

    ready_count = len(candidates)
    collision_free_count = len(maximum_safe)

    return {
        "schema": "harness.parallel-dispatch-plan/v1",
        "capacity": capacity,
        "active_count": len(active),
        "available_slots": available_slots,
        "graph_revision": graph.get("revision"),
        "ready_count": ready_count,
        "ready_without_collision_count": collision_free_count,
        "selected": selected,
        "deferred": deferred,
        "announcement": f"{collision_free_count} collision-free ready nodes, capacity {available_slots}: dispatching {len(selected)} now",
    }
