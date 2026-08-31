"""Graph-local readiness evaluation shared by scheduling and validation."""

from __future__ import annotations

from collections.abc import Mapping


def readiness_blocker(node: dict, nodes_by_id: Mapping[str, dict]) -> str | None:
    """Return the first unmet graph-local readiness gate for *node*, if any."""
    for dependency in node.get("depends_on", []):
        dependency_id = str(dependency)
        if dependency_id not in nodes_by_id or nodes_by_id[dependency_id].get("status") != "completed":
            return f"dependency:{dependency_id}"
    for required in node.get("assurance_requires", []):
        required_id = str(required)
        if required_id not in nodes_by_id or nodes_by_id[required_id].get("assurance_status") != "accepted":
            return f"assurance:{required_id}"
    if node.get("checkpoint") is not None and node.get("checkpoint") != "":
        return "checkpoint"
    return None
