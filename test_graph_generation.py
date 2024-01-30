import unittest
import graph_generation

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

