"""
test_min_vertex_coloring.py

Test cases for the exact minimum vertex coloring implementation.
"""

import unittest
from min_vertex_coloring import find_minimum_vertex_coloring


def is_proper_coloring(graph, coloring):
    """
    Utility: check that 'coloring' is a proper vertex coloring of 'graph'.
    """
    for v, neighbors in graph.items():
        if v not in coloring:
            return False
        for u in neighbors:
            if u not in coloring:
                return False
            if coloring[v] == coloring[u]:
                return False
    return True


class TestMinimumVertexColoring(unittest.TestCase):

    def test_empty_graph(self):
        G = {}
        chi, coloring = find_minimum_vertex_coloring(G)
        self.assertEqual(chi, 0)
        self.assertEqual(coloring, {})

    def test_single_vertex(self):
        G = {0: set()}
        chi, coloring = find_minimum_vertex_coloring(G)
        self.assertEqual(chi, 1)
        self.assertTrue(is_proper_coloring(G, coloring))

    def test_edge(self):
        # Simple edge: 0 -- 1, needs 2 colors
        G = {
            0: {1},
            1: {0}
        }
        chi, coloring = find_minimum_vertex_coloring(G)
        self.assertEqual(chi, 2)
        self.assertTrue(is_proper_coloring(G, coloring))

    def test_path_4(self):
        # Path on 4 vertices is bipartite => 2 colors
        G = {
            0: {1},
            1: {0, 2},
            2: {1, 3},
            3: {2},
        }
        chi, coloring = find_minimum_vertex_coloring(G)
        self.assertEqual(chi, 2)
        self.assertTrue(is_proper_coloring(G, coloring))

    def test_cycle_even(self):
        # C4 (4-cycle) is bipartite => 2 colors
        G = {
            0: {1, 3},
            1: {0, 2},
            2: {1, 3},
            3: {0, 2},
        }
        chi, coloring = find_minimum_vertex_coloring(G)
        self.assertEqual(chi, 2)
        self.assertTrue(is_proper_coloring(G, coloring))

    def test_cycle_odd(self):
        # C5 (5-cycle) needs 3 colors
        G = {
            0: {1, 4},
            1: {0, 2},
            2: {1, 3},
            3: {2, 4},
            4: {0, 3},
        }
        chi, coloring = find_minimum_vertex_coloring(G)
        self.assertEqual(chi, 3)
        self.assertTrue(is_proper_coloring(G, coloring))

    def test_complete_graph_small(self):
        # Complete graph K4 (clique of size 4) needs 4 colors
        G = {
            0: {1, 2, 3},
            1: {0, 2, 3},
            2: {0, 1, 3},
            3: {0, 1, 2},
        }
        chi, coloring = find_minimum_vertex_coloring(G)
        self.assertEqual(chi, 4)
        self.assertTrue(is_proper_coloring(G, coloring))

    def test_disconnected_graph(self):
        # Disjoint union of K3 (needs 3) and an edge (needs 2)
        # Whole graph needs max(3,2) = 3 colors.
        G = {
            0: {1, 2},  # K3 part
            1: {0, 2},
            2: {0, 1},
            3: {4},     # edge part
            4: {3},
        }
        chi, coloring = find_minimum_vertex_coloring(G)
        self.assertEqual(chi, 3)
        self.assertTrue(is_proper_coloring(G, coloring))


if __name__ == "__main__":
    unittest.main()
