import random
import math

graph_adjacency_map = {}

#add_vertex(graph_adjacency_map, 1, [0, 2])
def add_vertex(graph, vertex, neighbor):
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
        random_points.append((x, y))
    return random_points


#distance_threshold = 10.0
def process_points_within_distance(points, distance_threshold):
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
                add_vertex(graph_adjacency_map, i, j)


def main():
    num_points = 10
    for i in range(num_points):
        graph_adjacency_map[i] = []

    points = generate_random_points(num_points, (0,50), (0,50))
    process_points_within_distance(points, 15)

    print(points)
    print(graph_adjacency_map)


main()