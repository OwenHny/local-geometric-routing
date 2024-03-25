import random
import math
import csv
import heapq
import copy

base_options = ["greedy", "compass", "greedy_compass"]
base = base_options[0]

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
            if neighbor not in graph[vertex]:#graph.get(vertex, []):
                graph[vertex].append(neighbor)    
        else:
            graph[vertex] = [neighbor]        

        if neighbor in graph:
            if vertex not in graph[neighbor]:#graph.get(neighbor, []):
                graph[neighbor].append(vertex)
        else:
            graph[neighbor] = [vertex]


def remove_edge(graph, point1, point2):
    if point2 in graph[point1]:
        graph[point1].remove(point2)
    if point1 in graph[point2]:
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

    return distances[end]

def remove_points(num_points, keys, points):
    correction = 0
    for key in range(num_points):
        if key not in keys:
            del points[key - correction]
            correction += 1
    
def planar(graph):
    planar = copy.deepcopy(graph) 
    for node in graph: # loop for each node in graph
        for neighbor in graph[node]: # loop through all neighbors of a node
            cx = (neighbor[0] - node[0])/2 + node[0]
            cy = (neighbor[1] - node[1])/2 + node[1]
            r = distance_calc(node, (cx, cy))
            for point in graph[node]: # check if any other neighbors of the node are in the collision range, if so remove the edge
                   if neighbor != point and distance_calc(point, (cx,cy)) < r:
                       remove_edge(planar, node, neighbor)         
                       break
    return planar

def count_neighbors(graph):
    count = 0
    for node in graph:
        count += len(graph[node])

    return count

def distance_calc(point1, point2):
    return (math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))) 

def calc_angle(center, point1, point2):
    return math.atan2(point2[1] - center[1], point2[0] - center[0]) - math.atan2(point1[1] - center[1], point1[0] - center[0])


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

def compass_stuck(start, end, graph, num_nodes):
    node = start
    steps = 0

    while node != end:
        next_node = node
        min_angle = math.pi/2
        for neighbor in graph[node]:
            if neighbor == end:
                return None
            angle = abs(calc_angle(node,end, neighbor))
            if angle > math.pi:
                angle = (math.pi*2  - angle) 
            if min_angle >= angle: 
                min_angle = angle
                next_node = neighbor

        if next_node == node or steps > num_nodes *2:
            return node
        node = next_node
        steps += 1

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
            angle = abs(calc_angle(node, end, neighbor))

            if angle > math.pi:
                angle = (math.pi*2  - angle) * - 1             
#            print(angle, neighbor)
            if angle <= right_angle and angle >= 0:
                right_node = neighbor
                right_angle = angle
            elif angle >= left_angle and angle < 0:
                left_node = neighbor
                left_angle = angle

        if right_node == node and left_node == node:            
#            print(node, end, graph)
            return node
        elif right_node == node:
            next = left_node
        elif left_node == node:
            next = right_node
        else:
            next = right_node if distance_calc(right_node, end) < distance_calc(left_node, end) else left_node 

        if distance_calc(next, end) < distance_calc(node, end):
            node = next
        else:
#            print(node, end, graph)
            return node
    return None

def main():
    #for base in base_options:
    #    print(base)
        base = ""
        generate_graphs = 20000
        graphs = 0

        failed_graph = 0
        not_stuck = 0 
        #frame_size = 20
        frame_size = 75 

        #num_points = 10
        num_points = 125
        min_points = .5 # % of points that must remain for valid graph

        with open(base + "_graphs.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["num_nodes","graph", "planar", "start", "end", "path_length", "stuck", "average_neighbors"])
            
            while graphs < generate_graphs: 
                graph = {}
                
                points = generate_random_points(num_points, (0,frame_size), (0,frame_size))
                process_points_within_distance(graph,points, 10)

                valid_graph = remove_unconnected_nodes(graph)

                num_keys = len(valid_graph.keys())
                if num_keys >= num_points * min_points: # filter on large enough graph
                    remove_points(num_points, valid_graph.keys(), points)

                    planar_graph = planar(valid_graph)
                    
                    start = random.randrange(num_keys)
                    start_node = list(valid_graph.keys())[start] 
                    end_node = start_node
                    end = start
                    distance = 0
                    while end == start and distance < 2: 
                        end = random.randrange(num_keys)
                        end_node = list(valid_graph.keys())[end]
                        distance = dijkstra(valid_graph,start_node, end_node) 


                    stuck = start_node
                    if base == base_options[0]:
                        stuck = greedy_stuck(start_node, end_node, graph)
                    if base == base_options[1]:
                        stuck = compass_stuck(start_node, end_node, graph, num_keys)
                    if base == base_options[2]:
                        stuck = greedy_compass_stuck(start_node, end_node, graph)

                    if stuck:
                        average_neighbors = count_neighbors(valid_graph) / num_keys
                        graphs += 1
                        #num_points += 1
                        #frame_size = math.floor(graphs*.37 + 20) 
                        #print(graphs, failed_graph, not_stuck, num_points, num_keys, frame_size, distance)
                        writer.writerow([num_keys, valid_graph, planar_graph,start_node, end_node, distance, stuck, average_neighbors]) 
                        if graphs % 100 == 0:
                            print(graphs)
                    else:
                        not_stuck +=1
                else:
                    failed_graph += 1   
    


if __name__ == '__main__':
    main()
