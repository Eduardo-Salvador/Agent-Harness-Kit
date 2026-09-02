#!/usr/bin/env python3

from __future__ import annotations

import unittest

from agent_harness_kit.request_router import LANES, classify_request


class RequestRouterTests(unittest.TestCase):
    def test_explicit_full_always_wins(self) -> None:
        decision = classify_request(
            "Use the full harness even though this is only a static label change. Vibe it."
        )
        self.assertEqual(decision["route"], "full-harness")
        self.assertFalse(decision["needs_ai"])

    def test_risk_signal_raises_assurance_without_inflating_explicit_route(self) -> None:
        decision = classify_request("Use vibe mode to change the authentication flow")
        self.assertEqual(decision["route"], "vibe")
        self.assertEqual(decision["assurance"], "full")
        self.assertEqual(decision["harness_shape"], "none")
        self.assertIn("authentication", decision["matched_triggers"])

    def test_registration_cannot_bypass_hard_gate_with_vibe(self) -> None:
        for request in ("Vibe: add user registration", "Modo vibe: adicione cadastro de usuário"):
            with self.subTest(request=request):
                decision = classify_request(request)
                self.assertEqual(decision["route"], "vibe")
                self.assertEqual(decision["assurance"], "full")
                self.assertIn("authentication", decision["matched_triggers"])

    def test_email_invitation_cannot_bypass_external_side_effect_gate(self) -> None:
        for request in ("Vibe: invite users by email", "Modo vibe: convide usuários por e-mail"):
            with self.subTest(request=request):
                decision = classify_request(request)
                self.assertEqual(decision["route"], "vibe")
                self.assertEqual(decision["assurance"], "full")
                self.assertIn("external-side-effect", decision["matched_triggers"])

    def test_obvious_static_request_is_direct_trivial(self) -> None:
        decision = classify_request("Correct the typo in the static submit button label")
        self.assertEqual(decision["schema"], "harness.request-route/v1")
        self.assertEqual(decision["route"], "direct-trivial")
        self.assertEqual(decision["hard_triggers"], [])
        self.assertEqual(decision["durable_artifacts"], [])
        self.assertEqual(decision["verification"], "smallest-useful-check")

    def test_explicit_vibe_has_focused_verification_and_no_artifacts(self) -> None:
        decision = classify_request("Vibe: add a small local validation behavior")
        self.assertEqual(decision["route"], "vibe")
        self.assertEqual(decision["verification"], "focused-check")
        self.assertEqual(decision["durable_artifacts"], [])

    def test_eligible_graph_bound_work_is_graph_only(self) -> None:
        decision = classify_request(
            "Implement the already specified task",
            graph_bound=True,
            graph_only_eligible=True,
        )
        self.assertEqual(decision["route"], "graph-only")
        self.assertEqual(decision["verification"], "declared-graph-check")
        self.assertEqual(decision["assurance"], "light")
        self.assertEqual(decision["harness_shape"], "compact")

    def test_ambiguity_requests_ai_without_changing_the_lane_contract(self) -> None:
        decision = classify_request("Make this better")
        self.assertEqual(decision["route"], "full-harness")
        self.assertEqual(decision["assurance"], "full")
        self.assertTrue(decision["needs_ai"])
        self.assertEqual(decision["classification"], "fallback")
        self.assertEqual(decision["lanes"], LANES)
        self.assertIn("ambiguity-unresolved", decision["promotion_triggers"])

    def test_portuguese_hard_trigger_overrides_portuguese_vibe(self) -> None:
        decision = classify_request("Faz no modo vibe e adiciona login com Google")
        self.assertEqual(decision["route"], "vibe")
        self.assertEqual(decision["assurance"], "full")
        self.assertIn("authentication", decision["matched_triggers"])

    def test_portuguese_static_request_is_direct_trivial(self) -> None:
        decision = classify_request("Corrija o texto estático do botão")
        self.assertEqual(decision["route"], "direct-trivial")

    def test_ambiguous_copy_is_not_mistaken_for_static_copywriting(self) -> None:
        decision = classify_request("Copy user data into another account")
        self.assertEqual(decision["route"], "full-harness")
        self.assertTrue(decision["needs_ai"])

    def test_structured_inputs_do_not_depend_on_injected_prompt_words(self) -> None:
        decision = classify_request(
            "Ajuste esta interação local",
            explicit_mode="vibe",
            workstream_count=2,
        )
        self.assertEqual(decision["route"], "vibe")
        self.assertEqual(decision["user_override"], "vibe")
        self.assertEqual(decision["harness_shape"], "none")
        self.assertIn("multiple-workstreams", decision["matched_triggers"])

    def test_multiple_workstreams_without_real_agents_use_compact_graph(self) -> None:
        decision = classify_request("Coordinate frontend and backend", workstream_count=2, agent_count=1)
        self.assertEqual(decision["route"], "graph-only")
        self.assertEqual(decision["harness_shape"], "compact")
        self.assertNotEqual(decision["assurance"], "none")

    def test_two_real_agents_require_full_harness(self) -> None:
        decision = classify_request("Coordinate two tasks", agent_count=2)
        self.assertEqual(decision["route"], "full-harness")
        self.assertIn("multi-agent-execution", decision["reasons"])

    def test_other_full_conditions_are_orthogonal_structured_inputs(self) -> None:
        cases = (
            ({"human_in_loop": True}, "human-in-loop"),
            ({"audit_required": True}, "audit-required"),
            ({"model_capability": "weak"}, "weak-model"),
        )
        for kwargs, reason in cases:
            with self.subTest(reason=reason):
                decision = classify_request("Fix the button label typo", **kwargs)
                self.assertEqual(decision["route"], "full-harness")
                self.assertIn(reason, decision["reasons"])

    def test_weak_model_uses_compact_full_harness_by_default(self) -> None:
        decision = classify_request("Implement the decided bounded change", model_capability="weak")
        self.assertEqual(decision["route"], "full-harness")
        self.assertEqual(decision["harness_shape"], "compact")

    def test_all_structured_route_overrides_are_supported(self) -> None:
        expected = {
            "direct-trivial": ("none", "none"),
            "vibe": ("none", "none"),
            "graph-only": ("light", "compact"),
            "full": ("full", "complete"),
        }
        for mode, (assurance, shape) in expected.items():
            with self.subTest(mode=mode):
                decision = classify_request("A decided change", explicit_mode=mode)
                self.assertEqual(decision["route"], "full-harness" if mode == "full" else mode)
                self.assertEqual(decision["assurance"], assurance)
                self.assertEqual(decision["harness_shape"], shape)

    def test_assurance_and_shape_overrides_are_reported(self) -> None:
        decision = classify_request(
            "A decided change",
            explicit_mode="vibe",
            assurance="light",
            harness_shape="compact",
        )
        self.assertEqual(decision["route"], "vibe")
        self.assertEqual(decision["assurance"], "light")
        self.assertEqual(decision["harness_shape"], "compact")
        self.assertEqual(decision["minimal_artifacts"], ["task-graph-transition"])

    def test_non_mandatory_risk_does_not_override_explicit_assurance(self) -> None:
        decision = classify_request(
            "Change the API contract",
            explicit_mode="graph-only",
            assurance="none",
        )
        self.assertEqual(decision["route"], "graph-only")
        self.assertEqual(decision["assurance"], "none")
        self.assertIn("explicit-assurance-below-risk-recommendation", decision["warnings"])

    def test_mandatory_security_policy_can_raise_explicit_assurance(self) -> None:
        decision = classify_request(
            "Change authentication and access control",
            explicit_mode="graph-only",
            assurance="none",
        )
        self.assertEqual(decision["assurance"], "full")
        self.assertIn("assurance-raised-by-mandatory-policy", decision["reasons"])

    def test_scope_growth_exposes_full_harness_promotion_triggers(self) -> None:
        decision = classify_request("Vibe: adjust a small local calculation")
        self.assertIn("multi-agent-execution", decision["promotion_triggers"])
        self.assertIn("ambiguity-unresolved", decision["promotion_triggers"])
        self.assertNotIn("dependency", decision["promotion_triggers"])


if __name__ == "__main__":
    unittest.main()
