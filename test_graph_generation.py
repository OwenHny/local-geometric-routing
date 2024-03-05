import unittest
import graph_generation
import graph_print

class Test(unittest.TestCase):

    def test_add_vertex(self):
        graph_adjacency_map = []

        graph_generation.add_edge(graph_adjacency_map, 0, 1)
        graph_generation.add_edge(graph_adjacency_map, 0, 2)
        graph_generation.add_edge(graph_adjacency_map, 1, 3)
        graph_generation.add_edge(graph_adjacency_map, 2, 3)

        self.assertEqual(graph_adjacency_map,  {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]})
        print(graph_adjacency_map)

    def test_distance(self):
        self.assertTrue(False)

    def test_connected(self):
        self.assertTrue(False)

    def test_dijkstra(self):
        self.assertTrue(False)

    def test_planar(self):
        graph = {(23, 4): [(22, 1), (14, 1), (25, 8), (14, 6)], (20, 14): [(24, 12), (18, 15), (23, 19), (13, 20), (14, 6)], (26, 27): [(27, 21)], (14, 1): [(15, 1), (15, 3), (12, 3), (23, 4)], (23, 19): [(24, 12), (20, 14), (27, 21)], (5, 16): [(7, 14), (3, 25), (8, 18)], (3, 25): [(5, 16), (8, 18), (8, 26)], (12, 25): [(13, 25), (13, 23), (8, 26)], (10, 9): [(7, 14), (18, 15), (13, 14), (8, 7), (14, 6), (7, 9)], (8, 18): [(7, 14), (5, 16), (3, 25), (13, 20), (13, 14), (8, 26)], (13, 14): [(7, 14), (10, 9), (18, 15), (13, 20), (8, 18)], (13, 23): [(13, 25), (13, 20), (12, 25)], (22, 1): [(15, 1), (15, 3), (25, 8), (23, 4)], (13, 20): [(18, 15), (20, 14), (8, 18), (13, 14), (13, 23)], (12, 3): [(15, 3), (8, 7), (14, 1), (14, 6)], (14, 6): [(10, 9), (20, 14), (15, 3), (12, 3), (23, 4)], (27, 21): [(23, 19), (26, 27)], (8, 26): [(3, 25), (8, 18), (12, 25)], (15, 1): [(22, 1), (15, 3), (14, 1)], (7, 9): [(7, 14), (10, 9), (8, 7)], (13, 25): [(12, 25), (13, 23)], (18, 15): [(10, 9), (20, 14), (13, 20), (13, 14)], (8, 7): [(10, 9), (12, 3), (7, 9)], (25, 8): [(24, 12), (22, 1), (23, 4)], (24, 12): [(23, 19), (20, 14), (25, 8)], (15, 3): [(15, 1), (22, 1), (14, 1), (12, 3), (14, 6)], (7, 14): [(10, 9), (5, 16), (8, 18), (13, 14), (7, 9)]}
        graph_generation.planar(graph)
        graph_print(graph)



if __name__ == '__main__':
    unittest.main()
