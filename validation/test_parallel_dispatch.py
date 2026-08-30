#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("agent_harness_validator_parallel", ROOT / "tools" / "validate.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(VALIDATOR)


class ParallelDispatchContractTests(unittest.TestCase):
    def test_valid_batch_has_runtime_evidence(self) -> None:
        path = ROOT / "validation" / "parallel-dispatch-fixtures" / "valid.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(VALIDATOR.validate_parallel_dispatch_payload(payload, str(path)), [])

    def test_hostile_batches_are_rejected(self) -> None:
        root = ROOT / "validation" / "parallel-dispatch-fixtures" / "invalid"
        for path in sorted(root.glob("*.json")):
            with self.subTest(path=path.name):
                payload = json.loads(path.read_text(encoding="utf-8"))
                actual = VALIDATOR.validate_parallel_dispatch_payload(payload, str(path))
                codes = {item.split(":", 1)[0] for item in actual}
                self.assertTrue(set(payload["expected_errors"]).issubset(codes), actual)


if __name__ == "__main__":
    unittest.main()
