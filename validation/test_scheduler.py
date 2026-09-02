#!/usr/bin/env python3

from __future__ import annotations

import unittest

from agent_harness_kit.scheduler import ScheduleError, schedule_ready


def node(
    task_id: str,
    *,
    status: str = "ready",
    depends_on: list[str] | None = None,
    write_set: list[str] | None = None,
    checkpoint: object = None,
    assurance_status: str = "accepted",
    assurance_requires: list[str] | None = None,
) -> dict:
    return {
        "id": task_id,
        "status": status,
        "depends_on": depends_on or [],
        "write_set": write_set or [f"src/{task_id.lower()}/**"],
        "checkpoint": checkpoint,
        "assurance_status": assurance_status,
        "assurance_requires": assurance_requires or [],
    }


class SchedulerTests(unittest.TestCase):
    def test_selects_every_safe_ready_node_up_to_free_capacity(self) -> None:
        graph = {
            "nodes": [
                node("ACTIVE", status="active"),
                node("FRONTEND"),
                node("BACKEND"),
                node("DATA"),
            ]
        }
        plan = schedule_ready(graph, capacity=3)
        self.assertEqual(plan["selected"], ["FRONTEND", "BACKEND"])
        self.assertEqual(plan["active_count"], 1)
        self.assertEqual(plan["available_slots"], 2)
        self.assertEqual(plan["deferred"], [{"id": "DATA", "reason": "capacity"}])

    def test_rejects_false_ready_dependencies_and_assurance(self) -> None:
        graph = {
            "nodes": [
                node("BASE", status="active", assurance_status="pending"),
                node("DEPENDENT", depends_on=["BASE"]),
                node("RISK", assurance_requires=["BASE"]),
            ]
        }
        plan = schedule_ready(graph, capacity=4)
        self.assertEqual(plan["selected"], [])
        self.assertEqual(
            plan["deferred"],
            [
                {"id": "DEPENDENT", "reason": "dependency:BASE"},
                {"id": "RISK", "reason": "assurance:BASE"},
            ],
        )

    def test_defers_a_ready_node_with_an_unresolved_checkpoint(self) -> None:
        graph = {"nodes": [node("GATED", checkpoint="DEC-001")]}

        plan = schedule_ready(graph, capacity=1)

        self.assertEqual(plan["selected"], [])
        self.assertEqual(plan["deferred"], [{"id": "GATED", "reason": "checkpoint"}])

    def test_never_selects_a_write_collision(self) -> None:
        graph = {
            "nodes": [
                node("FIRST", write_set=["src/shared/**"]),
                node("SECOND", write_set=["src/shared/file.ts"]),
            ]
        }
        plan = schedule_ready(graph, capacity=2)
        self.assertEqual(plan["selected"], ["FIRST"])
        self.assertEqual(plan["deferred"], [{"id": "SECOND", "reason": "write-collision:FIRST"}])

    def test_maximizes_parallel_batch_instead_of_taking_greedy_first_node(self) -> None:
        graph = {
            "revision": 9,
            "nodes": [
                node("BROAD", write_set=["src/**"]),
                node("FRONTEND", write_set=["src/frontend/**"]),
                node("BACKEND", write_set=["src/backend/**"]),
            ],
        }

        plan = schedule_ready(graph, capacity=2)

        self.assertEqual(plan["selected"], ["FRONTEND", "BACKEND"])
        self.assertEqual(plan["graph_revision"], 9)
        self.assertEqual(plan["ready_without_collision_count"], 2)
        self.assertEqual(plan["announcement"], "2 collision-free ready nodes, capacity 2: dispatching 2 now")
        self.assertEqual(plan["deferred"], [{"id": "BROAD", "reason": "write-collision:FRONTEND"}])

    def test_reports_all_collision_free_ready_nodes_even_when_capacity_is_lower(self) -> None:
        graph = {"nodes": [node("A"), node("B"), node("C")]}
        plan = schedule_ready(graph, capacity=2)
        self.assertEqual(plan["ready_without_collision_count"], 3)
        self.assertEqual(plan["selected"], ["A", "B"])
        self.assertEqual(plan["announcement"], "3 collision-free ready nodes, capacity 2: dispatching 2 now")

    def test_requires_a_positive_host_capacity(self) -> None:
        with self.assertRaisesRegex(ScheduleError, "capacity"):
            schedule_ready({"nodes": []}, capacity=0)

    def test_selects_fan_in_only_after_every_branch_completes(self) -> None:
        graph = {
            "nodes": [
                node("FRONTEND", status="completed"),
                node("BACKEND", status="active"),
                node("INTEGRATE", depends_on=["FRONTEND", "BACKEND"]),
            ]
        }
        blocked = schedule_ready(graph, capacity=2)
        self.assertEqual(blocked["selected"], [])
        self.assertEqual(blocked["deferred"], [{"id": "INTEGRATE", "reason": "dependency:BACKEND"}])

        graph["nodes"][1]["status"] = "completed"
        ready = schedule_ready(graph, capacity=2)
        self.assertEqual(ready["selected"], ["INTEGRATE"])


if __name__ == "__main__":
    unittest.main()
