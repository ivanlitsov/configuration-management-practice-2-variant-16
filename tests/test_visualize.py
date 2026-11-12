import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from visualize import ascii_tree, d2_source


class VisualizationTests(unittest.TestCase):
    def test_d2_source(self):
        graph = {"A": ["B", "C"], "B": ["A"], "C": []}
        self.assertEqual(
            d2_source(graph),
            'n1: "A"\nn2: "B"\nn3: "C"\nn1 -> n2\nn1 -> n3\nn2 -> n1\n',
        )
        self.assertEqual(d2_source({"D": []}), 'n1: "D"\n')

    def test_ascii_tree(self):
        graph = {"A": ["B", "C"], "B": ["A", "C"], "C": []}
        self.assertEqual(
            ascii_tree(graph, "A"),
            "A\n|-- B\n|   |-- A (cycle)\n|   `-- C\n`-- C (shown)",
        )
