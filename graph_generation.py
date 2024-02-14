import random
import math
import csv
import heapq
import routing

#add_vertex(graph_adjacency_map, 1, [0, 2])
def add_edge(graph, vertex, neighbor):
    """
    Add a new vertex to the graph adjacency map.

    Parameters:
    - graph (dict): The existing graph adjacency map.
    - vertex: The new vertex to be added.
    - neighbor : The new  neighbor for the vertex.
    """
    if vertex != neighbor: # don't allow duplicate points
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
               # print( point1, point2)
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
            r = distance_calc(node, (cx, cy))
            for point in graph[node]:
                   if neighbor != point and distance_calc(point, (cx,cy))< r:
                       remove_edge(graph, node, neighbor)         
                       removed = True
                       #print(node, neighbor, point, cx, cy, r)
                       break
            if removed:
                break

def distance_calc(point1, point2):
    return (math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))) 

def calc_angle(center, point1, point2):
    line1 = (center[0] - point1[0], center[1]- point1[1])
    line2 = (point2[0] - center[0], point2[1] - center[1])

    dot = line1[0] * line2[0] + line1[1] * line2[1]
    line1_len = math.sqrt(line1[0] * line1[0] + line1[1] * line1[1])
    line2_len = math.sqrt(line2[0] * line2[0] + line2[1] * line2[1])

    angle = min(max(dot/(line1_len * line2_len), -1), 1)
    sign = -1 if angle < 0 else 1

    return sign * math.acos(angle )

def greedy_stuck(start, end, graph):
    node = start

    while node != end:
        next_node = node
        distance = distance_calc(node, end) 
        for neighbor in graph[node]: 
            if distance_calc(neighbor, end)< distance:
                next_node = neighbor
                distance = distance_calc(neighbor, end) 
        if next_node == node:          
            #print(node, end, graph[node])
            return node
        node = next_node

    return None

def compass_stuck(start, end, graph):
    node = start

    while node != end:
        next_node = node
        min_angle = math.pi/2
        for neighbor in graph[node]:
            if neighbor == end:
                return None
            #print(node, neighbor, end, graph[node]) 
            angle = abs(calc_angle(node,end, neighbor))
            if min_angle > angle: 
                min_angle = angle
                next_node = neighbor

        if next_node == node:
            #print(node, end, graph[node])
            return node
        node = next_node

    return None 

def greedy_compass_stuck(start, end, graph):
    node = start

    while node != end: 
        right_node = node
        left_node = node
        right_angle = math.pi/2
        left_angle = -1 * math.pi/2
        for neighbor in graph[node]:
            if neighbor == end:
               return None 
            angle = calc_angle(node, end, neighbor)
            if angle < right_angle:
                right_node = neighbor
                right_angle = angle
            elif angle > left_angle:
                left_node = neighbor
                left_angle = angle
        if right_node == node and left_node == node:
            print(node, end, graph[node])
            return node
        
        node = right_node if distance_calc(right_node, end) < distance_calc(left_node, end) else left_node 

    return None

def main():
    generate_graphs = 100
    graphs = 0

    not_stuck = 0

    with open("graphs.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["num_nodes","graph", "start", "end", "path_length", "stuck"])
        
        num_points = 100
        min_points = .5 # % of points that must remain for valid graph
        while graphs < generate_graphs: 
            graph = {}
            
            graph #= {key: [] for key in range(num_points)}

            points = generate_random_points(num_points, (0,100), (0,100))
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

                stuck = True 
                #stuck = greedy_stuck(start_node, end_node, graph)
                #stuck = compass_stuck(start_node, end_node, graph)
                #stuck = greedy_compass_stuck(start_node, end_node, graph)

                distance = dijkstra(valid_graph,start_node, end_node) 


                if distance > 1 and stuck:
                #print(valid_graph, list(valid_graph.keys())[start], list(valid_graph.keys())[end],distance )
                    graphs += 1
                    #num_points += 1
                    #routing.one_bit(start_node, end_node, graph)
                    print(num_keys)
                    writer.writerow([num_keys, valid_graph,start_node, end_node, distance, stuck]) 
                elif not stuck:
                    not_stuck +=1
    
    print(not_stuck)


main()
