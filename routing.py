import pandas
import math

num_steps = 0
base = ""
recovery = ""

def import_graphs(filename):
    with open(filename, "r") as file:
        
        csvFile = pandas.read_csv(file)
        print(csvFile)


def path(start, end, graph):

    print("TODO")


def distance_calc(point1, point2):
    return (math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))) 

def calc_angle(center, point1, point2):
    line1 = (center[0] - point1[0], center[1]- point1[1])
    line2 = (point2[0] - center[0], point2[1] - center[1])

    dot = line1[0] * line2[0] + line1[1] * line2[1]
    line1_len = math.sqrt(line1[0] * line1[0] + line1[1] * line1[1])
    line2_len = math.sqrt(line2[0] * line2[0] + line2[1] * line2[1])

    return math.acos(min(max(dot/(line1_len * line2_len), -1), 1))

def greedy(start, end, graph):
    node = start

    while node != end:
        next_node = node
        distance = distance_calc(node, end) 
        for neighbor in graph[node]: 
            if distance_calc(neighbor, end)< distance:
                next_node = neighbor
                distance = distance_calc(neighbor, end) 
        if next_node == node:          
            unstuck(node, end, graph)
        else:
            node = next_node
            num_steps +=1

def compass(start, end, graph):
    node = start

    while node != end:
        next_node = node
        min_angle = math.pi/2
        for neighbor in graph[node]:
            if neighbor == end:
                num_steps += 1
                return None
            angle = calc_angle(node,end, neighbor)
            if min_angle > angle: 
                min_angle = angle
                next_node = neighbor

        if next_node == node:
            unstuck(node, end, graph)
        else:
            node = next_node
            num_steps += 1

def greedy_compass(start, end, graph):
    node = start

    while node != end:
        next_node1 = node
        next_node2 = node
        min_angle1 = math.pi/2
        min_angle2 = math.pi/2
        for neighbor in graph[node]:
            if neighbor == end:
                num_steps += 1
                return None 
            angle = calc_angle(node, end, neighbor)
            if angle < min_angle1 or angle < min_angle2:
                if min_angle1 < min_angle2:
                   min_angle2 = angle
                   next_node2 = neighbor
                else:
                   min_angle1 = angle
                   next_node1 = neighbor 
        if next_node1 == node and next_node2 == node:
            node = unstuck(node, end, graph)
        else:
            node = next_node1 if min_angle1 < min_angle2 else next_node2
            num_steps += 1


def unstuck(node, end, graph):
    next_node = ()

    if recovery == "face":
        next_node = face(node, end, graph)
    elif recovery == "one bit":
        next_node = one_bit(node, end, graph)

    print("TODO")
    return next_node    

def face(node, end, graph):
    print("TODO")
    return node

def one_bit(node, end, graph):
    last = None
    while node != end:
        if graph[node].index(end):
            num_steps += 1
            return None
        elif last == None:
            # forward to right neighbor if not left
            print("TODO")

        elif
    return node


import_graphs("graphs.csv")