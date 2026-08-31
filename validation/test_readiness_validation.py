#!/usr/bin/env python3

from __future__ import annotations

import unittest

from tools.validate import validate_graph


def node(
    task_id: str,
    *,
    status: str = "ready",
    depends_on: list[str] | None = None,
    checkpoint: object = None,
    assurance_status: str = "accepted",
    assurance_requires: list[str] | None = None,
) -> dict:
    return {
        "id": task_id,
        "goal": task_id,
        "depends_on": depends_on or [],
        "status": status,
        "assignee": f"agent:{task_id.lower()}",
        "reviewer": f"agent:reviewer-{task_id.lower()}",
        "write_set": [f"src/{task_id.lower()}/**"],
        "checkpoint": checkpoint,
        "evidence_profile": "handoff-review",
        "assurance_status": assurance_status,
        "assurance_requires": assurance_requires or [],
        "task_brief": f"tasks/{task_id}.md",
    }


class ReadinessValidationTests(unittest.TestCase):
    def test_rejects_ready_and_active_nodes_with_unmet_graph_local_gates(self) -> None:
        cases = (
            ("dependency", {"depends_on": ["BASE"]}, "graph.dependency-gate"),
            ("assurance", {"assurance_requires": ["BASE"]}, "graph.assurance-gate"),
            ("checkpoint", {"checkpoint": "DEC-001"}, "graph.checkpoint-gate"),
        )
        for status in ("ready", "active"):
            for name, target_fields, expected_code in cases:
                with self.subTest(status=status, gate=name):
                    graph = {
                        "nodes": [
                            node("BASE", status="active", assurance_status="pending"),
                            node("TARGET", status=status, **target_fields),
                        ]
                    }

                    codes = {error.split(":", 1)[0] for error in validate_graph(graph, "graph.json")}

                    self.assertIn(expected_code, codes)


if __name__ == "__main__":
    unittest.main()
