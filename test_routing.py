import unittest
import routing
import graph_generation

class Test(unittest.TestCase):
    
    def one_bit_straight(self):
        graph = {}

        graph_generation.add_edge(graph, (0,0), (10,0))
        graph_generation.add_edge(graph, (10,0), (10,10))
        graph_generation.add_edge(graph, (10,10), (20,10))
        graph_generation.add_edge(graph, (20,10), (20,20))
        graph_generation.add_edge(graph, (20,20), (30,20))
        graph_generation.add_edge(graph, (30,20), (30,30))
        
        test = routing.one_bit((0, 0), (30, 30), graph)
        self.assertEqual(test, (30,30))

    def one_bit_angle(self):
        graph = {}

        graph_generation.add_edge(graph, (0,0), (0,10))
        graph_generation.add_edge(graph, (0,10), (0,20))
        graph_generation.add_edge(graph, (0,20), (0,30))
        graph_generation.add_edge(graph, (0,30), (10,30))
        graph_generation.add_edge(graph, (10,30), (30,10))
        graph_generation.add_edge(graph, (30,10), (30,0))
        
        test = routing.one_bit((0,0), (30, 0))
        self.assertEqual(test, (30, 0))

    def one_bit_u(self):
        graph = {}

        graph_generation.add_edge(graph, (0,0), (0,10))
        graph_generation.add_edge(graph, (0,10), (0,20))
        graph_generation.add_edge(graph, (0,0), (0,30))
        graph_generation.add_edge(graph, (0,30), (10,30))
        graph_generation.add_edge(graph, (10,30), (30,10))
        graph_generation.add_edge(graph, (30,10), (30,0))
        
        test = routing.one_bit((0,0), (30, 0))
        self.assertEqual(test, (30, 0))

    

