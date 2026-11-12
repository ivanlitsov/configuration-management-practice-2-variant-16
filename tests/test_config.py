import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from config import read_config


VALID = (
    'package = "python3"\n'
    'repository = "https://example.org/alpine/"\n'
    'test_mode = false\n'
    'ascii_tree = true\n'
)


class ConfigTests(unittest.TestCase):
    def read(self, contents):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.toml"
            path.write_text(contents, encoding="utf-8")
            return read_config(path)

    def test_valid_config(self):
        self.assertEqual(self.read(VALID)["package"], "python3")

    def test_bad_values(self):
        cases = (
            ("package", '"python3"', '"invalid name"'),
            ("repository", '"https://example.org/alpine/"', '"index"'),
            ("test_mode", "false", '"false"'),
            ("ascii_tree", "true", "1"),
        )
        for key, old, new in cases:
            with self.subTest(key=key):
                config = VALID.replace(f"{key} = {old}", f"{key} = {new}")
                with self.assertRaisesRegex(ValueError, key):
                    self.read(config)

    def test_missing_field(self):
        with self.assertRaisesRegex(ValueError, "ascii_tree"):
            self.read(VALID.replace("ascii_tree = true\n", ""))
