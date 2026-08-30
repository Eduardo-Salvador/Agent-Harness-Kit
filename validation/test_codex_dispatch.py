#!/usr/bin/env python3

from __future__ import annotations

import unittest

from agent_harness_kit.codex_dispatch import DispatchError, build_dispatch, record_dispatch


def request(*, purpose: str = "implementation", subagents: bool = True) -> dict:
    return {
        "task": {
            "id": "TASK-042",
            "revision": 3,
            "task_spec": "harness-state/tasks/TASK-042.md",
            "agent_role": "role:backend-specialist",
            "approved_authorities": ["harness-state/PROJECT-CONTEXT.md@4"],
            "scoped_rules": ["harness-state/RULES.md#backend"],
            "read_set": ["src/api/router.py"],
            "impact_set": ["tests/api/test_router.py"],
            "implementation_plan": "harness-state/plans/PLAN-9.md",
            "conversation": "must never be copied",
        },
        "purpose": purpose,
        "attempt": 1,
        "review_round": 1,
        "model_dispatch": {
            "id": "model-dispatch-TASK-042@1",
            "status": "resolved",
            "selected_model": "gpt-5.6-terra",
            "reasoning_effort": "medium",
            "override_confirmed": True,
        },
        "capabilities": {
            "spawn_subagent": {
                "available": subagents,
                "operation": "spawn_agent" if subagents else "unavailable",
                "evidence": "codex-host@2026-08-30T18:00:00Z",
            }
        },
        "implementer_identity": "agent:implementer:TASK-042:attempt-1",
        "implementer_context_ref": "codex:agent-impl-42",
    }


class CodexDispatchTests(unittest.TestCase):
    def test_builds_native_implementation_call_with_minimal_context(self) -> None:
        plan = build_dispatch(request())
        self.assertEqual(plan["status"], "ready-to-dispatch")
        self.assertEqual(plan["role"]["executor"], "role:generic-specialist")
        self.assertEqual(plan["role"]["requested"], "role:backend-specialist")
        self.assertEqual(plan["native_call"]["operation"], "spawn_agent")
        args = plan["native_call"]["arguments"]
        self.assertEqual(args["fork_turns"], "none")
        self.assertEqual(args["model"], "gpt-5.6-terra")
        self.assertEqual(args["reasoning_effort"], "medium")
        packet = plan["context_packet"]
        self.assertEqual(packet["task_spec"], "harness-state/tasks/TASK-042.md")
        self.assertNotIn("conversation", packet)
        self.assertNotIn("implementation_plan", packet)
        self.assertNotIn("must never be copied", args["message"])

    def test_records_adapter_owned_identity_context_and_response(self) -> None:
        plan = build_dispatch(request())
        record = record_dispatch(
            plan,
            {
                "agent_id": "codex-agent-99",
                "operation_id": "spawn-op-99",
                "accepted_model": "gpt-5.6-terra",
                "accepted_reasoning_effort": "medium",
                "status": "running",
                "secret": "must-not-be-persisted",
            },
        )
        self.assertEqual(record["schema"], "harness.codex-agent-dispatch/v1")
        self.assertEqual(record["status"], "dispatched")
        self.assertEqual(record["agent_identity"], "agent:implementer:TASK-042:attempt-1")
        self.assertEqual(record["execution_context_ref"], "codex:codex-agent-99")
        self.assertEqual(record["adapter_response"]["operation_id"], "spawn-op-99")
        self.assertNotIn("secret", record["adapter_response"])
        self.assertEqual(record["model"]["accepted"], "gpt-5.6-terra")

    def test_review_dispatch_is_fresh_and_distinct(self) -> None:
        plan = build_dispatch(request(purpose="review"))
        self.assertEqual(plan["role"]["executor"], "role:reviewer-integrator")
        self.assertEqual(plan["agent_identity"], "agent:reviewer:TASK-042:round-1")
        self.assertNotEqual(plan["agent_identity"], plan["separation"]["implementer_identity"])
        self.assertNotIn("codex:agent-impl-42", plan["native_call"]["arguments"]["message"])
        with self.assertRaisesRegex(DispatchError, "implementer context"):
            record_dispatch(
                plan,
                {
                    "agent_id": "agent-impl-42",
                    "operation_id": "spawn-op-bad",
                    "accepted_model": "gpt-5.6-terra",
                    "accepted_reasoning_effort": "medium",
                },
            )
        with self.assertRaisesRegex(DispatchError, "implementer context"):
            record_dispatch(
                plan,
                {
                    "agent_id": "new-reviewer-id",
                    "context_ref": "codex:agent-impl-42",
                    "operation_id": "spawn-op-mixed",
                    "accepted_model": "gpt-5.6-terra",
                    "accepted_reasoning_effort": "medium",
                },
            )

    def test_explicit_fallback_never_fakes_review_independence(self) -> None:
        implementation = build_dispatch(request(subagents=False))
        self.assertEqual(implementation["status"], "sequential-fallback")
        self.assertIsNone(implementation["native_call"])

        review = build_dispatch(request(purpose="review", subagents=False))
        self.assertEqual(review["status"], "manual-fresh-context-required")
        self.assertIsNone(review["native_call"])
        self.assertEqual(review["fallback"], "open-new-review-context")

    def test_rejects_unresolved_model_dispatch(self) -> None:
        payload = request()
        payload["model_dispatch"]["override_confirmed"] = False
        with self.assertRaisesRegex(DispatchError, "model dispatch"):
            build_dispatch(payload)


if __name__ == "__main__":
    unittest.main()
