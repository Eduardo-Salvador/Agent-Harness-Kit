#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("agent_harness_validator", ROOT / "tools" / "validate.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(VALIDATOR)


class ModelDispatchTests(unittest.TestCase):
    def test_valid_resolved_override_is_accepted(self) -> None:
        path = ROOT / "validation" / "model-dispatch-fixtures" / "valid.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(VALIDATOR.validate_model_dispatch_payload(payload, str(path)), [])

    def test_hostile_dispatch_claims_are_rejected(self) -> None:
        fixture_root = ROOT / "validation" / "model-dispatch-fixtures" / "invalid"
        for path in sorted(fixture_root.glob("*.json")):
            with self.subTest(path=path.name):
                payload = json.loads(path.read_text(encoding="utf-8"))
                actual = VALIDATOR.validate_model_dispatch_payload(payload, str(path))
                actual_codes = {item.split(":", 1)[0] for item in actual}
                self.assertTrue(set(payload["expected_errors"]).issubset(actual_codes), actual)


if __name__ == "__main__":
    unittest.main()
