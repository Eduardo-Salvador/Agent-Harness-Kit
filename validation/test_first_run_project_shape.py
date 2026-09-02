#!/usr/bin/env python3

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FirstRunProjectShapeTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8").lower()

    def test_first_run_closes_architecture_structure_and_optional_conventions(self) -> None:
        playbook = self.read("harness/playbooks/first-run.md")
        for expected in (
            "architecture and organization closure",
            "architecture decision",
            "folder organization",
            "coding conventions are optional",
            "recommend for me",
            "do not ask again",
        ):
            self.assertIn(expected, playbook)

    def test_native_first_run_skills_route_the_same_project_shape_decisions(self) -> None:
        for relative in (
            ".agents/skills/first-run-discovery/SKILL.md",
            ".claude/skills/first-run-discovery/SKILL.md",
        ):
            with self.subTest(relative=relative):
                skill = self.read(relative)
                self.assertIn("architecture and folder organization", skill)
                self.assertIn("coding conventions", skill)
                self.assertIn("optional", skill)
                self.assertIn("recommend", skill)

    def test_project_context_has_explicit_project_shape_fields(self) -> None:
        for relative in (
            "harness/templates/PROJECT-CONTEXT.md",
            "docs/contracts/PROJECT-CONTEXT.md",
        ):
            with self.subTest(relative=relative):
                context = self.read(relative)
                self.assertIn("## architecture and project organization", context)
                self.assertIn("- architecture:", context)
                self.assertIn("- folder organization:", context)
                self.assertIn("- coding conventions:", context)
                self.assertIn("- evidence:", context)

    def test_public_readmes_explain_adaptive_project_shape_discovery(self) -> None:
        expectations = {
            "README.md": ("architecture", "folder organization", "optional coding conventions"),
            "README.pt-BR.md": ("arquitetura", "organização de pastas", "convenções de código opcionais"),
            "docs/PYPI-README.md": ("architecture", "folder organization", "optional coding conventions"),
        }
        for relative, expected_tokens in expectations.items():
            with self.subTest(relative=relative):
                readme = self.read(relative)
                for expected in expected_tokens:
                    self.assertIn(expected, readme)


if __name__ == "__main__":
    unittest.main()
