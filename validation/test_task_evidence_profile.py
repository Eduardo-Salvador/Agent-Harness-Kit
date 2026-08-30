"""Hostile checks for proportional graph-only task closeout."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from validate import validate_graph, validate_task_evidence_profile


class TaskEvidenceProfileTests(unittest.TestCase):
    def graph_only(self) -> dict[str, str]:
        return {
            "evidence_profile": "graph-only",
            "planning_mode": "inline-simple",
            "test_strategy": "verification-only",
            "reviewer": "not-required",
            "review_profile": "none",
            "max_review_rounds": "0",
            "assurance_gate": "none",
        }

    def test_accepts_bounded_graph_only_task(self) -> None:
        self.assertEqual(validate_task_evidence_profile(self.graph_only(), "task.md"), [])

    def test_rejects_graph_only_tdd_bypass(self) -> None:
        task = self.graph_only()
        task["test_strategy"] = "tdd"
        self.assertTrue(any(item.startswith("task.graph-only-scope:") for item in validate_task_evidence_profile(task, "task.md")))

    def test_rejects_graph_only_review_or_assurance_bypass(self) -> None:
        task = self.graph_only()
        task.update({"reviewer": "agent:reviewer", "review_profile": "light", "max_review_rounds": "1", "assurance_gate": "affected-actions"})
        errors = validate_task_evidence_profile(task, "task.md")
        self.assertTrue(any(item.startswith("task.graph-only-review:") for item in errors))
        self.assertTrue(any(item.startswith("task.graph-only-assurance:") for item in errors))

    def test_rejects_handoff_review_without_reviewer(self) -> None:
        task = self.graph_only()
        task.update({"evidence_profile": "handoff-review", "review_profile": "light", "max_review_rounds": "1"})
        errors = validate_task_evidence_profile(task, "task.md")
        self.assertTrue(any(item.startswith("task.handoff-review-reviewer:") for item in errors))

    def test_rejects_graph_only_node_with_review_or_assurance(self) -> None:
        graph = {
            "nodes": [{
                "id": "TASK-A", "goal": "A", "depends_on": [], "status": "ready",
                "assignee": "agent:a", "reviewer": "agent:r", "write_set": ["src/a/**"],
                "checkpoint": None, "evidence_profile": "graph-only", "assurance_status": "pending",
                "assurance_requires": ["TASK-A"], "task_brief": "TASK-A.md",
            }]
        }
        errors = validate_graph(graph, "graph.json")
        self.assertTrue(any(item.startswith("graph.graph-only-reviewer:") for item in errors))
        self.assertTrue(any(item.startswith("graph.graph-only-assurance:") for item in errors))


if __name__ == "__main__":
    unittest.main()
