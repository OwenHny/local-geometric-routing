import random
import math
import csv
import heapq

#add_vertex(graph_adjacency_map, 1, [0, 2])
def add_edge(graph, vertex, neighbor):
    """
    Add a new vertex to the graph adjacency map.

    Parameters:
    - graph (dict): The existing graph adjacency map.
    - vertex: The new vertex to be added.
    - neighbor : The new  neighbor for the vertex.
    """
    if vertex in graph:
        if neighbor not in graph.get(vertex, []):
            graph[vertex].append(neighbor)    
    else:
        graph[vertex] = [neighbor]        

    if neighbor in graph:
        if vertex not in graph.get(neighbor, []):
            graph[neighbor].append(vertex)
    else:
        graph[neighbor] = [vertex]


def remove_edge(graph, point1, point2):
    graph[point1].remove(point2)
    graph[point2].remove(point1)

# Example usage:
#num_points = 10
#x_range = (0, 100)
#y_range = (0, 100)
def generate_random_points(num_points, x_range, y_range):
    """
    Generate random points within the specified x and y ranges.

    Parameters:
    - num_points: Number of points to generate
    - x_range: Tuple (min_x, max_x) specifying the x-axis range
    - y_range: Tuple (min_y, max_y) specifying the y-axis range

    Returns:
    - List of tuples representing random points (x, y)
    """
    random_points = []
    for _ in range(num_points):
        x = random.uniform(x_range[0], x_range[1])
        y = random.uniform(y_range[0], y_range[1])
        random_points.append((round(x), round(y)))
    return random_points


#distance_threshold = 10.0
def process_points_within_distance(graph, points, distance_threshold):
    """
    Loop through the list of points and call a function for pairs that are within a given distance.

    Parameters:
    - points: List of tuples representing points
    - distance_threshold: The maximum distance allowed between points
    - process_function: The function to call for points within the given distance

    Returns:
    - None
    """
    num_points = len(points)
    for i in range(num_points - 1):
        for j in range(i + 1, num_points):
            point1 = points[i]
            point2 = points[j]
            distance = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
            if distance <= distance_threshold:
                #print( point1, point2)
                add_edge(graph, point1, point2)

def remove_unconnected_nodes(graph):
    """
    Remove nodes that are not connected to any other nodes in the graph.

    Parameters:
    - graph: Dictionary representing the graph

    Returns:
    - Updated graph with unconnected nodes removed
    """
    updated_graph = dict()
    visited = set()
    start = None
    for key in graph:
        if len(graph[key]) > 0:
            start = key
            break
    if start:
        traverse(graph, start, visited)

    for node in visited:
        updated_graph[node] = graph[node]

    return updated_graph

def traverse(graph, node, visited):
    visited.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            traverse(graph, neighbor, visited)

def dijkstra(graph, start, end):
    visited = set()
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node not in visited:
            visited.add(current_node)
        
            for neighbor in graph[current_node]:
                distance = current_distance + 1

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

    #print(distances)
    return distances[end]

def remove_points(num_points, keys, points):
    correction = 0
    for key in range(num_points):
        if key not in keys:
            del points[key - correction]
            correction += 1
    
def planar(graph):
    #print(graph)
    removed = False
    for node in graph:
        for neighbor in graph[node]:
            cx = (neighbor[0] - node[0])/2 + node[0]
            cy = (neighbor[1] - node[1])/2 + node[1]
            r = math.sqrt(pow(node[0] - cx, 2) + pow(node[1] - cy, 2)) 
            for point in graph[node]:
                   if neighbor != point and math.sqrt(pow(point[0] - cx,2) + pow(point[1] - cy, 2)) < r:
                       remove_edge(graph, node, neighbor)         
                       removed = True
                       #print(node, neighbor, point, cx, cy, r)
                       break
            if removed:
                break


def main():
    generate_graphs = 10
    graphs = 0
    with open("graphs.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["num_nodes","graph", "start", "end", "points", "path_length"])
        
        num_points = 10
        min_points = .8 # % of points that must remain for valid graph
        while graphs < generate_graphs: 
            graph = {}
            
            graph #= {key: [] for key in range(num_points)}

            points = generate_random_points(num_points, (0,40), (0,40))
            process_points_within_distance(graph,points, 10)

            valid_graph = remove_unconnected_nodes(graph)

            num_keys = len(valid_graph.keys())
            if num_keys >= num_points * min_points: # filter on large enough graph
                remove_points(num_points, valid_graph.keys(), points)
                #valid_graph = reindexgraph(valid_graph)

                planar(valid_graph)                
                
                start = random.randrange(num_keys)
                end = start
                while end == start: 
                    end = random.randrange(num_keys)

                start_node = list(valid_graph.keys())[start] 
                end_node = list(valid_graph.keys())[end]

                distance = dijkstra(valid_graph,start_node, end_node) 

                if distance > 1:
                #print(valid_graph, list(valid_graph.keys())[start], list(valid_graph.keys())[end],distance )
                    graphs += 1
                    num_points += 4
                    writer.writerow([num_keys, valid_graph,start_node, end_node, distance]) 

main()