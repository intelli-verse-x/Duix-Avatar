"""Check configuration bytes without importing or executing JavaScript."""
from pathlib import Path
from hashlib import sha256
import unittest

CONFIG = 'electron.vite.config.mjs'
EXPECTED_SHA256 = 'f193f934ffd46bc7843d50a2687751352bb71577c1825a21d34790fca918b50b'
# Reviewed predecessor blob: 8341459c19becc8f033f02bf0212cbf124f23222


def check_config_bytes(raw):
    if sha256(raw.replace(b"\r\n", b"\n")).hexdigest() != EXPECTED_SHA256:
        raise ValueError("Configuration differs from its reviewed pre-tail declarations")


class ConfigIntegrity(unittest.TestCase):
    def test_actual_config_has_only_reviewed_declarations(self):
        root = Path(__file__).resolve().parents[2]
        check_config_bytes((root / CONFIG).read_bytes())

    def test_executable_tail_is_rejected_without_execution(self):
        root = Path(__file__).resolve().parents[2]
        raw = (root / CONFIG).read_bytes()
        with self.assertRaises(ValueError):
            check_config_bytes(raw + b"\n(() => { throw new Error('untrusted tail'); })();\n")

    def test_create_require_injection_is_rejected_without_execution(self):
        root = Path(__file__).resolve().parents[2]
        raw = (root / CONFIG).read_bytes()
        with self.assertRaises(ValueError):
            check_config_bytes(b"import { createRequire } from 'module';\n" + raw)


if __name__ == "__main__":
    unittest.main()
