#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("agent_harness_validator", ROOT / "tools" / "validate.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(VALIDATOR)


class MediaManifestTests(unittest.TestCase):
    def test_text_hash_normalizes_checkout_line_endings(self) -> None:
        lf = b"first line\nsecond line\n"
        crlf = b"first line\r\nsecond line\r\n"
        self.assertEqual(
            VALIDATOR.content_sha256(lf, normalize_text=True),
            VALIDATOR.content_sha256(crlf, normalize_text=True),
        )

    def test_binary_hash_remains_byte_exact(self) -> None:
        lf = b"first line\nsecond line\n"
        crlf = b"first line\r\nsecond line\r\n"
        self.assertNotEqual(VALIDATOR.content_sha256(lf), VALIDATOR.content_sha256(crlf))


if __name__ == "__main__":
    unittest.main()
