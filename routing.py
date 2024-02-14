#import pandas
import math

num_steps = 0
base = ""
recovery = "one bit"

def import_graphs(filename):
    with open(filename, "r") as file:
        
#        csvFile = pandas.read_csv(file)
#        print(csvFile)
        print("TODO")


def path(start, end, graph):

    print("TODO")


def distance_calc(point1, point2):
    print(point1, point2)
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

def greedy(start, end, graph):
    global num_steps
    print("start", start, end)
    node = start

    while node != end:
        next_node = node
        distance = distance_calc(node, end) 
        for neighbor in graph[node]: 
            if distance_calc(neighbor, end)< distance:
                next_node = neighbor
                distance = distance_calc(neighbor, end) 
        if next_node == node:          
            node = unstuck(node, end, graph)
        else:
            node = next_node
            num_steps = num_steps + 1 

def compass(start, end, graph):
    global num_steps
    node = start

    while node != end:
        next_node = node
        min_angle = math.pi/2
        for neighbor in graph[node]:
            if neighbor == end:
                num_steps = num_steps + 1
                return None
            angle = calc_angle(node,end, neighbor)
            if min_angle > angle: 
                min_angle = angle
                next_node = neighbor

        if next_node == node:
            node = unstuck(node, end, graph)
        else:
            node = next_node
            num_steps = num_steps + 1

def greedy_compass(start, end, graph):
    global num_steps
    node = start

    while node != end:
        right_node = node
        left_node = node
        right_angle = math.pi/2
        left_angle = -1 * math.pi/2
        for neighbor in graph[node]:
            if neighbor == end:
                num_steps = num_steps + 1
                return None 
            angle = calc_angle(node, end, neighbor)
            if angle < right_angle:
                right_node = neighbor
                right_angle = angle
            elif angle > left_angle:
                left_node = neighbor
                left_angle = angle
        if right_node == node and left_node == node:
            node = unstuck(node, end, graph)
        else:
            node = right_node if distance_calc(right_node, end) < distance_calc(left_node, end) else left_node 
            num_steps = num_steps + 1


def unstuck(node, end, graph):
    global recovery
    next_node = ()

    if recovery == "face":
        next_node = face(node, end, graph)
    elif recovery == "one bit":
        next_node = one_bit(node, end, graph)

    return next_node    

def is_unstuck(node, stop, end):
    return distance_calc(node, end) < distance_calc(stop, end) 

def face(node, end, graph):
    print("TODO")
    return node

def one_bit(node, end, graph):
    global num_steps
    print(node, end, graph)
    stop = node
    last = None
    next = None
    while node != end and not is_unstuck(node, stop, end):
    #if True:
        num_steps = num_steps + 1
        if end in graph[node]:
            return end

        left_sorted = []
        right_sorted = []

        line1 = (node[0] - end[0], node[1]- end[1])
        line1_len = math.sqrt(line1[0] * line1[0] + line1[1] * line1[1])

        for neighbor in graph[node]:
            # calc angle 
            line2 = (neighbor[0] - node[0], neighbor[1] - node[1])
            line2_len = math.sqrt(line2[0] * line2[0] + line2[1] * line2[1])

            dot = line1[0] * line2[0] + line1[1] * line2[1]
            angle = dot/(line1_len * line2_len)
            sign = -1 if angle < 0 else 1

            angle = sign * math.acos(min(max(angle, -1), 1))
            #print(angle, node, end, neighbor, line1, line1_len, line2, line2_len, dot)
            if angle > 0:
                left_sorted.append((angle,neighbor))
            else:
                right_sorted.append((angle, neighbor))

        left_sorted.sort(reverse=False)
        right_sorted.sort(reverse=True)

        left = []
        right = []

        for neighbor in left_sorted:
            left.append(neighbor[1])

        for neighbor in right_sorted:
            right.append(neighbor[1])


        print(node,last,end,  "left:", left, "right: ", right)
        if last == None:
            if len(right) > 0:
                next = right[0]
            else:
                next = left[0]
        elif left and last == left[0]:
            print(9)
            if right:
                next = right[0]
            else:
                next = last
        elif last in left and left.index(last) > 0:
            next = last
        else:
            print(17)
            if last in right and len(right) > right.index(last) + 1:
                #print(right.index(last), right)
                next = right[right.index(last) + 1]
            elif len(left) > 0:
                next = left[0]
            else:
                next = right[0]
                
        last = node
        node = next

    return node

