#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("agent_harness_validator", ROOT / "tools" / "validate.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(VALIDATOR)


class MediaManifestTests(unittest.TestCase):
    def test_candidate_audio_may_wait_for_a_new_github_attachment(self) -> None:
        self.assertEqual(
            VALIDATOR.audio_attachment_errors(
                {
                    "language": "en",
                    "status": "candidate-awaiting-audition",
                    "github_attachment": None,
                }
            ),
            [],
        )

    def test_approved_audio_requires_a_valid_github_attachment(self) -> None:
        errors = VALIDATOR.audio_attachment_errors(
            {"language": "pt-BR", "status": "approved", "github_attachment": None}
        )
        self.assertEqual(errors, ["media.manifest-attachment: pt-BR"])

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

    def test_migration_file_identity_normalizes_text_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            left = Path(temporary) / "lf.md"
            right = Path(temporary) / "crlf.md"
            left.write_bytes(b"first line\nsecond line\n")
            right.write_bytes(b"first line\r\nsecond line\r\n")
            self.assertEqual(VALIDATOR.file_identity(left), VALIDATOR.file_identity(right))


if __name__ == "__main__":
    unittest.main()
