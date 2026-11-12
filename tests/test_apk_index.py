import io
import sys
import tarfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from apk_index import direct_requirements, fetch_index, parse_index


INDEX = (
    "P:demo\nV:1-r0\nD:libx=2-r0 so:liby.so.1\n\n"
    "P:libx\nV:2-r0\n\n"
    "P:liby\nV:1-r0\np:so:liby.so.1=1\n"
)


class ApkIndexTests(unittest.TestCase):
    def test_direct_requirements(self):
        packages = parse_index(INDEX)
        self.assertEqual(
            direct_requirements(packages, "demo"),
            ["libx=2-r0", "so:liby.so.1"],
        )
        self.assertEqual(direct_requirements(packages, "libx"), [])
        with self.assertRaisesRegex(ValueError, "missing"):
            direct_requirements(packages, "missing")

    def test_download_archive(self):
        buffer = io.BytesIO()
        data = INDEX.encode("utf-8")
        with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
            entry = tarfile.TarInfo("APKINDEX")
            entry.size = len(data)
            archive.addfile(entry, io.BytesIO(data))
        buffer.seek(0)
        with patch("apk_index.urlopen", return_value=buffer) as fetch:
            packages = fetch_index("https://example.org/main/x86_64/")
        fetch.assert_called_once_with(
            "https://example.org/main/x86_64/APKINDEX.tar.gz", timeout=20
        )
        self.assertIn("demo", packages)
