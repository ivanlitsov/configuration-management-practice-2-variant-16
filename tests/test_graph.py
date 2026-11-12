import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from apk_index import parse_index
from graph import build_graph
from repository import apk_graph, load_test_repository


DATA = Path(__file__).parent / "data"


class GraphTests(unittest.TestCase):
    def test_shared_dependency(self):
        repository = load_test_repository(DATA / "diamond.txt")
        graph, cycles, order = build_graph(repository, "A")
        self.assertEqual(list(graph), ["A", "B", "D", "C"])
        self.assertEqual(graph["C"], ["D"])
        self.assertEqual(cycles, [])
        self.assertEqual(order, ["D", "B", "C", "A"])

    def test_cycle(self):
        repository = load_test_repository(DATA / "cycle.txt")
        graph, cycles, order = build_graph(repository, "A")
        self.assertEqual(graph["C"], ["A", "D"])
        self.assertEqual(cycles, [["A", "B", "C", "A"]])
        self.assertEqual(order, [])

    def test_single_and_unknown_package(self):
        repository = load_test_repository(DATA / "diamond.txt")
        self.assertEqual(build_graph(repository, "D"), ({"D": []}, [], ["D"]))
        with self.assertRaisesRegex(ValueError, "X"):
            build_graph(repository, "X")

    def test_provider_mapping(self):
        index = (
            "P:a\nD:so:libb.so.1 b=2-r0 missing !c b>=9-r0\n\n"
            "P:b\nV:2-r0\np:so:libb.so.1=1\n"
        )
        graph, _, _ = build_graph(apk_graph(parse_index(index)), "a")
        self.assertEqual(graph["a"], ["b", "missing", "b>=9-r0"])
        self.assertEqual(graph["b"], [])
