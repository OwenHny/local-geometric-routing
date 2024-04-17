import pandas
import math
import ast
import graph_print
import random

BUMPED_ZERO = 0.000001
ROUTING_FAILURE = 3000

base_options = ["greedy", "compass", "greedy_compass", "aware_compass", "forward_compass"]
#recovery_options = ["face", "quick_face","left", "left_nonplanar", "void", "quick_void", "long_face", "random"]
recovery_options = ["face", "quick_face","left", "left_nonplanar", "void", "quick_void", "long_face"]
#recovery_options = ["face", "quick_face"]

quick_exit = False

num_steps = 0
base = base_options[0] 
recovery = recovery_options[1] 

# loop recovery options
loop_recovery = False
step_limit = 0 
limit_modifier = 2

def import_graphs(filename):
    global num_steps, recovery, base, step_limit, quick_exit
    num_graphs = 0

    if loop_recovery:
        quick_exit = False

    with open(filename, "r") as file:

        result = {}
        for option in recovery_options:
            result[option] = [[0,0],[0,0]]

        csvFile = pandas.read_csv(file)
        for case in csvFile.iterrows():
            num_graphs += 1
            if case[0] % 2500 == 0:
                print(case[0])
            start = ast.literal_eval(case[1].start)
            end = ast.literal_eval(case[1].end)
            graph = ast.literal_eval(case[1].graph)
            planar = ast.literal_eval(case[1].planar)
            
            if base == base_options[1]:
                step_limit = limit_modifier * case[1].num_nodes

            for option in recovery_options:
                recovery = option 
                path(start, end, graph, planar)
                stretch = num_steps / case[1].path_length
                #if option == recovery_options[0]:
                #    print(stretch)
                if stretch < 2:
                    result[option][0][0] = result[option][0][0] + stretch 
                    result[option][0][1] += 1
                else:
                    result[option][1][0] = result[option][1][0] + stretch 
                    result[option][1][1] += 1
                num_steps = 0
            #print(result) 
            #print(case[0])

        for option in recovery_options:
            #result[option] = result[option] / num_graphs
            result[option][0][0] = result[option][0][0] / result[option][0][1]
            result[option][1][0] = result[option][1][0] / result[option][1][1]
            
        print(result)
#        print(result["face"]/result["quick_face"], result["face"]/result["quick_void"])


def path(start, end, graph, planar):
    if base == "greedy":
        greedy(start, end, graph, planar)
    elif base == "compass":
        compass(start, end, graph, planar)
    elif base == "greedy_compass":
        greedy_compass(start, end, graph, planar)
    elif base == "aware_compass":
        aware_compass(start, end, graph, planar)
    elif base == "forward_compass":
        forward_compass(start, end, graph, planar)
    else:
        print("no base")
        return None


def distance_calc(point1, point2):
    return (math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))) 

def calc_angle(center, point1, point2):
    return math.atan2(point2[1] - center[1], point2[0] - center[0]) - math.atan2(point1[1] - center[1], point1[0] - center[0])

def calc_intersect_angle(point1, point2, point3, point4):
    A = point4[1] - point3[1]
    B = point3[0] - point4[0]
    C = point3[1]*(point4[0] - point3[0]) - point3[0]*(point4[1] - point3[1])
    line = [A,B,C]

    A = point2[1] - point1[1]
    B = point1[0] - point2[0]
    C = point1[1]*(point2[0] - point1[0]) - point1[0]*(point2[1] - point1[1])

    if line[0]*B - A * line[1] != 0:
        x = (line[1] * C - B * line[2])/(line[0]*B - A * line[1])
        y = (A * line[2] - line[0] * C)/(line[0]*B - A * line[1])

        if (x <= point1[0] and x >= point2[0] or x >= point1[0] and x <= point2[0]) and (y <= point1[1] and y >=  point2[1] or y >= point1[1] and y <= point2[1]):
            if (x <= point3[0] and x >= point4[0] or x >= point3[0] and x <= point4[0]) and (y <= point3[1] and y >= point4[1] or y >= point3[1] and y <= point4[1]):
                return calc_angle((x,y), point2, point4)
    return 0
    
def crossing_points(point1, point2, point3, point4):
    
    A = point4[1] - point3[1]
    B = point3[0] - point4[0]
    C = point3[1]*(point4[0] - point3[0]) - point3[0]*(point4[1] - point3[1])
    line = [A,B,C]

    A = point2[1] - point1[1]
    B = point1[0] - point2[0]
    C = point1[1]*(point2[0] - point1[0]) - point1[0]*(point2[1] - point1[1])

    if line[0]*B - A * line[1] != 0:
        x = (line[1] * C - B * line[2])/(line[0]*B - A * line[1])
        y = (A * line[2] - line[0] * C)/(line[0]*B - A * line[1])

        if (x < point1[0] and x > point2[0] or x > point1[0] and x < point2[0]) and (y < point1[1] and y >  point2[1] or y > point1[1] and y < point2[1]):
            if ((x < point3[0] and x > point4[0] or x > point3[0] and x < point4[0]) and (y < point3[1] and y > point4[1] or y > point3[1] and y < point4[1])):
                return distance_calc((x,y), point4)
                
    return 0

def crossing_point(point1, point2, Line, end):
    A = point2[1] - point1[1]
    B = point1[0] - point2[0]
    C = point1[1]*(point2[0] - point1[0]) - point1[0]*(point2[1] - point1[1])

    if Line[0]*B - A * Line[1] != 0:
        x = (Line[1] * C - B * Line[2])/(Line[0]*B - A * Line[1])
        y = (A * Line[2] - Line[0] * C)/(Line[0]*B - A * Line[1])

        if (x <= point1[0] and x >= point2[0] or x >= point1[0] and x <= point2[0]) and (y <= point1[1] and y >= point2[1] or y >= point1[1] and y <= point2[1]):
            return distance_calc((x,y), end)
    return 0


def greedy(start, end, graph, planar):
    global num_steps, loop_recovery
    loop_recovery = False
    node = start

    while node != end:
        #print(node, graph[node])
        next_node = node
        distance = distance_calc(node, end) 
        for neighbor in graph[node]: 
            if distance_calc(neighbor, end) < distance:
                next_node = neighbor
                distance = distance_calc(neighbor, end) 
        if next_node == node:          
            node = unstuck(node, end, planar, graph)
        else:
            node = next_node
            num_steps = num_steps + 1 

def compass(start, end, graph, planar):
    global num_steps, step_limit, loop_recovery
    loop_recovery = True
    node = start

    while node != end:
        next_node = node
        min_angle = math.pi/2
        for neighbor in graph[node]:
            if neighbor == end:
                num_steps = num_steps + 1
                return None
            angle = abs(calc_angle(node,end, neighbor))
            if angle > math.pi:
                angle = math.pi * 2 - angle
            if min_angle >= angle: 
                min_angle = angle
                next_node = neighbor

        if next_node == node or num_steps > step_limit:
            node = unstuck(node, end, planar, graph)
        else:
            node = next_node
            num_steps = num_steps + 1

def aware_compass(start, end, graph, planar):
    global num_steps, limit_modifier, loop_recovery
    loop_recovery = True
    node = start
    previous_nodes = {}

    while node != end:
        if node in previous_nodes: # check if this node has seen this message previously
            if previous_nodes[node] > limit_modifier:
                node = unstuck(node, end, planar, graph)
            else:
                previous_nodes[node] += 1
        else:
            previous_nodes[node] = 1
        next_node = node
        min_angle = math.pi/2
        for neighbor in graph[node]:
            if neighbor == end:
                num_steps = num_steps + 1
                return None
            angle = abs(calc_angle(node,end, neighbor))
            if angle > math.pi:
                angle = math.pi * 2 - angle
            if min_angle >= angle: 
                min_angle = angle
                next_node = neighbor

        if next_node == node:
            node = unstuck(node, end, planar, graph)
        else:
            node = next_node
            num_steps = num_steps + 1

def forward_compass(start, end, graph, planar):
    global num_steps, step_limit, loop_recovery
    loop_recovery = False
    node = start

    while node != end:
        next_node = node
        min_angle = math.pi/2
        for neighbor in graph[node]:
            if neighbor == end:
                num_steps = num_steps + 1
                return None
            angle = abs(calc_angle(node,end, neighbor))
            if angle > math.pi:
                angle = math.pi * 2 - angle
            if min_angle >= angle: 
                min_angle = angle
                next_node = neighbor

        if next_node == node or distance_calc(node, end) <= distance_calc(next_node, end):
            node = unstuck(node, end, planar, graph)
        else:
            node = next_node
            num_steps = num_steps + 1



def greedy_compass(start, end, graph, planar):
    global num_steps, loop_recovery
    loop_recovery = False
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
            if angle <= right_angle and angle >=0:
                right_node = neighbor
                right_angle = angle
            elif angle >= left_angle and angle < 0:
                left_node = neighbor
                left_angle = angle
        if right_node == node and left_node == node:            
            next = unstuck(node, end, planar, graph)
        elif right_node == node:
            next = left_node
        elif left_node == node:
            next = right_node
        else:
            next = right_node if distance_calc(right_node, end) < distance_calc(left_node, end) else left_node 

        if distance_calc(next, end) < distance_calc(node, end):
            node = next
            num_steps = num_steps + 1
        else:
            node = unstuck(node, end, planar, graph)
            

def unstuck(node, end, planar, graph):
    global recovery, recovery_options
    next_node = ()

    if recovery == recovery_options[0]: 
        next_node = face(node, end, planar)
    elif recovery == recovery_options[1]:  
        next_node = quick_face(node, end, planar)
    elif recovery == recovery_options[2] and not loop_recovery:
        next_node = left(node, end, planar)
    elif recovery == recovery_options[3] and not loop_recovery:
        next_node = left_nonplanar(node, end, graph)
    elif recovery == recovery_options[4] and not loop_recovery: 
        next_node = void(node, end, graph) 
    elif recovery == recovery_options[5] and not loop_recovery:
        next_node = quick_void(node, end, graph)
    elif recovery == recovery_options[6] and not loop_recovery:
        next_node = long_face(node, end, planar)
    #elif recovery == recovery_options[7] and not loop_recovery:
    #    next_node = random_recovery(node, end, graph)
    else:
        #print("No Unstuck specified")
        next_node = end 

    return next_node    

def is_unstuck(node, stop, end):
    global loop_recovery
    if loop_recovery:
        return False        
    else:
        return distance_calc(node, end) < distance_calc(stop, end) 

# Stop, last, 
def left(node, end, graph):
    global num_steps, quick_exit
    stop = node
    last = end

    while node != end and not is_unstuck(node, stop, end): 
        next = node
        if num_steps > ROUTING_FAILURE:
            raise Exception("stop") 

        if end in graph[node]:
            return end
        
        angle = math.pi * 3
        for neighbor in graph[node]:
            if quick_exit and is_unstuck(neighbor, stop, end):
                return neighbor
            test_angle  = calc_angle(node, last, neighbor)
            if test_angle == -0.0:
                test_angle = 0
            if test_angle == 0 or neighbor == last:
                test_angle = math.pi * 2
            if test_angle < 0:
                test_angle = math.pi * 2 + test_angle 

            if test_angle < angle:
                next = neighbor
                angle = test_angle

        num_steps += 1
        last = node
        node = next
    return node

def bump_point(point):
    return [point[0] + point[1]/1000 , point[1] + point[0]/1000]

def face(node, end, graph):
    global num_steps, quick_exit
    A = end[1] - node[1]
    B = node[0] - end[0]
    C = node[1]*(end[0] - node[0]) - node[0]*(end[1] - node[1])

    path = []
    path.append(end)

    stop = node
    last = end
    direction = 1 
    #best_crossing = None
    best_crossing = distance_calc(node, end) #+ 1# + BUMPED_ZERO
    full_loop = node
    #best_crossing = distance_calc(bump_point(node), bump_point(end))

    while node != end and not is_unstuck(node, stop, end):
        path.append(node)
        #print(node, last, graph[node])
        next = node
        if num_steps > ROUTING_FAILURE:
            print(stop, end, graph)
            print("face failure")
            #graph_print.plot_graph((node, end, stop), graph)
            graph_print.plot_graph(path, graph)
            raise Exception("stop")
        angle = math.pi * 3 
        if end in graph[node]:
            return end

        for neighbor in graph[node]:
            if quick_exit and is_unstuck(neighbor, stop, end):
                return neighbor
            test_angle = calc_angle(node, last, neighbor) * direction
            #test_angle = calc_angle(bump_point(node), bump_point(last), bump_point(neighbor)) * direction
            
            if test_angle == -0.0:
                test_angle = 0 
            if test_angle == 0 or neighbor == last:
                test_angle = math.pi * 2
            elif test_angle < 0 :
                test_angle = math.pi * 2 - (test_angle * -1)

            #print(node, neighbor, test_angle)
            if test_angle < angle: 
                angle = test_angle 
                next = neighbor
            #elif test_angle + .05 > math.pi *2 and node == stop:
            #    angle = math.pi * 2 - test_angle
            #    next = neighbor 
            #    direction = direction * -1

        crossing = crossing_point(bump_point(node), bump_point(next), (A,B,C), bump_point(end))
        side = (A * node[0] + B * node[1] + C ) # ensures that the direction is not switched on entry and exit to a point on the line 
        #crossing = crossing_point(node, next, (A,B,C), end)
        #print(num_steps, last, node, next, best_crossing, crossing)
        #if crossing == best_crossing and last != end and last != next and node != stop and side != 0:
        #    print("direction")
        if full_loop == node and last != end:
            full_loop = None

        if full_loop == None and (crossing == best_crossing and last != end and last != next) or best_crossing == distance_calc(stop, end) + 10 and next == stop: 
            #best_crossing = distance_calc(stop, end)
            if best_crossing == distance_calc(stop, end) + 10:
                next = end
            best_crossing = distance_calc(stop, end) #+ 1 
            direction = direction * -1
            full_loop = node
            #print("direction")
        elif crossing != 0 and  crossing < best_crossing + BUMPED_ZERO and last != end: 
            best_crossing = crossing
        elif next == stop and last != end and best_crossing == distance_calc(stop, end) and full_loop == None:#and last != stop:
            #print("here")
            #direction = direction * -1
            best_crossing = distance_calc(stop, end) + 10
        #elif node == stop and last != end:
            #print("here")
            #direction = direction * -1
            #next = node
            #node = end
        #elif last == end and direction * (A* bump_point(next)[0] + B * bump_point(next)[1] + C) <= 0:
            #direction = direction * -1

        num_steps += 1
        last = node
        node = next
        next = None

    return node
    
def left_nonplanar(node, end, graph):
    # left routing, doing planar calcs during forwarding descision
    global num_steps, quick_exit
    stop = node
    last = end

    while node != end and not is_unstuck(node, stop, end): 
        next = node
        if num_steps > ROUTING_FAILURE:
            print("Left non Planar failure")
            raise Exception("stop")
        if end in graph[node]:
            return end
        
        angle = math.pi * 3
        for neighbor in graph[node]:
            if quick_exit and is_unstuck(neighbor, stop, end):
                return neighbor
            test_angle  = calc_angle(node, last, neighbor)
            if test_angle == -0.0:
                test_angle = 0
            if test_angle == 0 or neighbor == last:
                test_angle = math.pi * 2
            if test_angle < 0:
                test_angle = math.pi * 2 + test_angle 

            if test_angle < angle:
                planar = True
                cx = (neighbor[0] - node[0])/2 + node[0]
                cy = (neighbor[1] - node[1])/2 + node[1]
                r = distance_calc(node, (cx, cy))
                for point in graph[node]: # check if any other neighbors of the node are in the collision range, if so remove the edge
                    if neighbor != point and distance_calc(point, (cx,cy)) < r:
                        planar = False
                        break
                if planar:
                    next = neighbor
                    angle = test_angle

        num_steps += 1
        last = node
        node = next
    return node

# face routing, change direction as soon as a crossing point is found
# stop node, end point, last node, best crossing, and routing direction all passed with message
def quick_face(node, end, graph):
    global num_steps, quick_exit
    A = end[1] - node[1]
    B = node[0] - end[0]
    C = node[1]*(end[0] - node[0]) - node[0]*(end[1] - node[1])

    stop = node
    last = end
    direction = 1 
    best_crossing = distance_calc(node, end)

    while node != end and not is_unstuck(node, stop, end):
        next = node
        if num_steps > ROUTING_FAILURE:
            print("Quick face failure")
            return end
 
        angle = math.pi * 3 
        if end in graph[node]:
            return end

        for neighbor in graph[node]:
            if quick_exit and is_unstuck(neighbor, stop, end):
                return neighbor
            test_angle = calc_angle(node, last, neighbor) * direction
            if test_angle == -0.0:
                test_angle = 0 
            if test_angle == 0 or neighbor == last:
                test_angle = math.pi * 2
            elif test_angle < 0 :
                test_angle = math.pi * 2 - (test_angle * -1)

            if test_angle < angle: 
                angle = test_angle 
                next = neighbor

        # check if the next node is on the other side of the line from the current node 
        side = (A * node[0] + B * node[1] + C ) # ensures that the direction is not switched on entry and exit to a point on the line 
        crossing = crossing_point(node, next, (A,B,C), end)
        if crossing and crossing <= best_crossing and last != end and side != 0 and last != next: 
            best_crossing = crossing
            last = node
            node = next
            next = None
            direction = direction * -1
        else: 
            last = node
            node = next
            next = None

        num_steps += 1
    return node

def long_face(node, end, graph):
    global num_steps, quick_exit
    A = end[1] - node[1]
    B = node[0] - end[0]
    C = node[1]*(end[0] - node[0]) - node[0]*(end[1] - node[1])

    last = end
    direction = 1 
    best_crossing = distance_calc(node, end)

    while node != end: 
        next = node
        if num_steps > ROUTING_FAILURE:
            raise Exception("stop")
        angle = math.pi * 3 
        if end in graph[node]:
            return end

        for neighbor in graph[node]:
            test_angle = calc_angle(node, last, neighbor) * direction
            if test_angle == -0.0:
                test_angle = 0 
            if test_angle == 0 or neighbor == last:
                test_angle = math.pi * 2
            elif test_angle < 0 :
                test_angle = math.pi * 2 - (test_angle * -1)

            if test_angle < angle: 
                angle = test_angle 
                next = neighbor

        crossing = crossing_point(bump_point(node), bump_point(next), (A,B,C), bump_point(end))
        if crossing == best_crossing and last != end and last != next:
            direction = direction * -1
        elif crossing != 0 and crossing < best_crossing and last != end: 
            best_crossing = crossing

        num_steps += 1
        last = node
        node = next
        next = None

    return node


def random_recovery(node, end, graph):
    global num_steps 
    
    counter = 0
    while counter < len(graph)/2:
        if end in graph[node]:
            num_steps += 1
            return end
        next = random.randint(0, len(graph[node]) - 1)
        node = graph[node][next]
        counter += 1
        num_steps +=1
    
    return node
  

def cross_product(p1,p2,p3):
    return (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])

# traverse void of non planar graph
def void(node, end, graph):
    global num_steps, quick_exit
    stop = node
    last = end
    next = None
    last_intersection = None
    direction = 1
    best_crossing = distance_calc(node, end)

    path = [] # for testing, and visualization
    path.append(end)
    
    A = end[1] - node[1]
    B = node[0] - end[0]
    C = node[1]*(end[0] - node[0]) - node[0]*(end[1] - node[1])

    while node != end and not is_unstuck(node, stop, end):
        if num_steps > ROUTING_FAILURE:
            print("void failure")
            #print(path, graph)
            #graph_print.plot_graph(path, graph)
            #raise Exception("stop")
            return end
        #print(num_steps, node, last)
        path.append(node)
 
        if end in graph[node]:
            return end

        if next == None:
            angle = math.pi * 3
            set_next = None
            face_intersection = None
            
            # check if previous edge is intersected by any two hop neighor edge
            # else normal face routing:    
            for neighbor in graph[node]:
                if quick_exit and is_unstuck(neighbor, stop, end): # quick exit
                    return neighbor

                for two_hop in graph[neighbor]:
                    if two_hop != node  and two_hop != last and neighbor != last and  last != end:
                        crossing = crossing_points(bump_point(neighbor), bump_point(two_hop), bump_point(node), bump_point(last)) 

                        if (crossing > BUMPED_ZERO and crossing < distance_calc(bump_point(node), bump_point(last)) - BUMPED_ZERO and 
                            (face_intersection == None or (crossing < face_intersection - BUMPED_ZERO) or 
                             (crossing <= face_intersection + BUMPED_ZERO and distance_calc(next, two_hop) < distance_calc(next, set_next)))  and
                            (last_intersection == None or crossing > last_intersection + BUMPED_ZERO )):

                            test_angle = calc_intersect_angle(node, last, neighbor, two_hop) * direction

                            vec1 = (last[0] - node[0], last[1] -node[1] )
                            vec2 = (two_hop[0] - neighbor[0], two_hop[1] - neighbor[1] )

                            cos_angle = (vec1[0] * vec2[0] + vec1[1] * vec2[1]) / math.sqrt((vec1[0]**2 + vec1[1]**2) * (vec2[0]**2 + vec2[1]**2))
                           
                            #if ((test_angle > 0  and test_angle < math.pi) or test_angle < math.pi * -1) and cos_angle < 0.97 and (test_angle > math.pi/4 or cos_angle < .8): 
                            if ((test_angle > 0  and test_angle < math.pi) or test_angle < math.pi * -1) and (test_angle > math.pi/4 or cos_angle < .5): 
                                #print("intersect", neighbor, two_hop, cos_angle, test_angle)

                                #print(test_angle > math.pi/4, cos_angle < .8)
                                if face_intersection and crossing > face_intersection - BUMPED_ZERO: # check that bumped equvilant crossing is going more left than current option
                                    vec3 = (set_next[0] - next[0], set_next[1] - next[1] )
                                    cos_angle2 = (vec1[0] * vec3[0] + vec1[1] * vec3[1]) / math.sqrt((vec1[0]**2 + vec1[1]**2) * (vec3[0]**2 + vec3[1]**2))
                                    if cos_angle2 < cos_angle + .1: 
                                        face_intersection = crossing
                                        next =  neighbor
                                        set_next = two_hop 
                                else:
                                    face_intersection = crossing
                                    next =  neighbor
                                    set_next = two_hop 

                if face_intersection == None:
                    test_angle = calc_angle(node, last, neighbor) * direction
                    if test_angle == -0.0:
                        test_angle = 0 
                    if test_angle == 0 or neighbor == last or test_angle > 0 - BUMPED_ZERO and test_angle < BUMPED_ZERO:
                        test_angle = math.pi * 2
                    elif test_angle < 0 :
                        test_angle = math.pi * 2 + test_angle 

                    if test_angle < angle: 
                        angle = test_angle 
                        next = neighbor
                    if test_angle == angle and distance_calc(node, neighbor) < distance_calc(node, next):
                        next = neighbor

            side = (A * node[0] + B * node[1] + C ) # ensures that the direction is not switched on entry and exit to a point on the line 
            if face_intersection != None:
                crossing = crossing_point(bump_point(node), bump_point(set_next), (A,B,C), bump_point(end))
                
                last_intersection= crossing_points(bump_point(node), bump_point(last), bump_point(set_next), bump_point(next))
                last = node
                node = next
                next = set_next 
                
            else:
                crossing = crossing_point(bump_point(node), bump_point(next), (A,B,C), bump_point(end))

                last = node
                node = next
                next = None
                last_intersection = None
            
            # check if the next node is on the other side of the line from the current node 
            if crossing == best_crossing and last != end and side != 0 and last != next:
                direction = direction * -1
            elif crossing and crossing < best_crossing and last != end and side != 0:  
                best_crossing = crossing
        else:
            last = node
            node = next
            next = None
        num_steps += 1
    return node

def quick_void(node, end, graph):
    global num_steps, quick_exit
    stop = node
    last = end
    next = None
    last_intersection = None
    direction = 1
    best_crossing = distance_calc(node, end)
    
    A = end[1] - node[1]
    B = node[0] - end[0]
    C = node[1]*(end[0] - node[0]) - node[0]*(end[1] - node[1])

    while node != end and not is_unstuck(node, stop, end):
        if num_steps > ROUTING_FAILURE:
            print("quick void failure")
            #print((stop,node, end), graph)
            return end
 
        if end in graph[node]:
            return end

        if next == None:
            angle = math.pi * 3
            set_next = None
            face_intersection = None
            
            # check if previous edge is intersected by any two hop neighor edge
            # else normal face routing:    
            for neighbor in graph[node]:
                if quick_exit and is_unstuck(neighbor, stop, end): # quick exit
                    return neighbor

                for two_hop in graph[neighbor]:
                    if two_hop != node  and two_hop != last and neighbor != last and  last != end:
                        crossing = crossing_points(bump_point(neighbor), bump_point(two_hop), bump_point(node), bump_point(last)) 

                        if (crossing > BUMPED_ZERO and crossing < distance_calc(bump_point(node), bump_point(last)) - BUMPED_ZERO and 
                            (face_intersection == None or (crossing < face_intersection - BUMPED_ZERO) or 
                             (crossing <= face_intersection + BUMPED_ZERO and distance_calc(next, two_hop) < distance_calc(next, set_next)))  and
                            (last_intersection == None or crossing > last_intersection + BUMPED_ZERO )):

                            test_angle = calc_intersect_angle(node, last, neighbor, two_hop) * direction

                            vec1 = (last[0] - node[0], last[1] -node[1] )
                            vec2 = (two_hop[0] - neighbor[0], two_hop[1] - neighbor[1] )

                            cos_angle = (vec1[0] * vec2[0] + vec1[1] * vec2[1]) / math.sqrt((vec1[0]**2 + vec1[1]**2) * (vec2[0]**2 + vec2[1]**2))
                           
                            #if ((test_angle > 0  and test_angle < math.pi) or test_angle < math.pi * -1) and cos_angle < 0.97: 
                            if ((test_angle > 0  and test_angle < math.pi) or test_angle < math.pi * -1) and (test_angle > math.pi/4 or cos_angle < .5): 

                                if face_intersection and crossing > face_intersection - BUMPED_ZERO: # check that bumped equvilant crossing is going more left than current option
                                    vec3 = (set_next[0] - next[0], set_next[1] - next[1] )
                                    cos_angle2 = (vec1[0] * vec3[0] + vec1[1] * vec3[1]) / math.sqrt((vec1[0]**2 + vec1[1]**2) * (vec3[0]**2 + vec3[1]**2))
                                    if cos_angle2 < cos_angle + .1: 
                                        face_intersection = crossing
                                        next =  neighbor
                                        set_next = two_hop 
                                else:
                                    face_intersection = crossing
                                    next =  neighbor
                                    set_next = two_hop 

                if face_intersection == None:
                    test_angle = calc_angle(node, last, neighbor) * direction
                    if test_angle == -0.0:
                        test_angle = 0 
                    if test_angle == 0 or neighbor == last or test_angle > 0 - BUMPED_ZERO and test_angle < BUMPED_ZERO:
                        test_angle = math.pi * 2
                    elif test_angle < 0 :
                        test_angle = math.pi * 2 + test_angle 

                    if test_angle < angle: 
                        angle = test_angle 
                        next = neighbor
                    if test_angle == angle and distance_calc(node, neighbor) < distance_calc(node, next):
                        next = neighbor

            side = (A * node[0] + B * node[1] + C ) # ensures that the direction is not switched on entry and exit to a point on the line 
            if face_intersection != None:
                crossing = crossing_point(bump_point(node), bump_point(set_next), (A,B,C), bump_point(end))
                
                last_intersection= crossing_points(bump_point(node), bump_point(last), bump_point(set_next), bump_point(next))
                if set_next in graph[node]:
                    last = next
                    node = set_next
                    next = None
                else:
                    last = node
                    node = next
                    next = set_next 
                
            else:
                crossing = crossing_point(bump_point(node), bump_point(next), (A,B,C), bump_point(end))

                last = node
                node = next
                next = None
                last_intersection = None
            
            # check if the next node is on the other side of the line from the current node 
            if crossing == best_crossing and last != end and side != 0 and last != next:
                direction = direction * -1
            elif crossing and crossing < best_crossing and last != end and side != 0:  
                best_crossing = crossing
        else:
            last = node
            node = next
            next = None
        num_steps += 1
    return node

if __name__ == '__main__': 
    
    #base = base_options[3]
    #loop_recovery = True
    #import_graphs("dense_graphs.csv")
    #import_graphs("sparse_graphs.csv")
    #loop_recovery = False
    quick_exit = True
    #base = base_options[0]
    #import_graphs("dense_graphs.csv")
    #import_graphs("basic/greedy_graphs.csv")
    #import_graphs("sparse_graphs.csv")
    #base = base_options[2]
    #import_graphs("dense_graphs.csv")
    #import_graphs("sparse_graphs.csv")
    #import_graphs("100s v2/greedy_compass_graphs.csv")
    #import_graphs("basic/greedy_compass_graphs.csv")
    #import_graphs("basic/greedy_compass_graphs.csv")
    #import_graphs("100s v2/greedy_compass_graphs.csv")

    #base = base_options[2]
    #import_graphs("100s v2/greedy_compass_graphs.csv")
    #loop_recovery = True
    #base = base_options[3]
    #import_graphs("100s v2/compass_graphs.csv")

    #loop_recovery = True
    #base = base_options[3]
    #import_graphs("basic/greedy_graphs.csv")
    #import_graphs("dense_graphs.csv")
    #import_graphs("sparse_graphs.csv")
 
    #base = base_options[1]
    #limit_modifier = .5
    #import_graphs("dense_graphs.csv")
    #import_graphs("sparse_graphs.csv")
    
    #limit_modifier = .25
    #import_graphs("dense_graphs.csv")
    #import_graphs("sparse_graphs.csv")
    
    #limit_modifier = .1
    #import_graphs("dense_graphs.csv")
    #import_graphs("sparse_graphs.csv")

    #limit_modifier = .05
    #import_graphs("dense_graphs.csv")
    #import_graphs("sparse_graphs.csv")
    #base = base_options[3]
    #limit_modifier = 2
    #import_graphs("basic/compass_graphs.csv")
    #limit_modifier = 1
    #import_graphs("basic/compass_graphs.csv")
    #base = base_options[4]
    #import_graphs("basic/compass_graphs.csv")
    

    base = base_options[0]
    import_graphs("basic/" +base + "_graphs.csv")
    #import_graphs("100s/" + base + "_graphs.csv")
    #import_graphs("100s v2/" +base + "_graphs.csv")
    #import_graphs("high density/" +base + "_graphs.csv")
    #import_graphs("lower density/" +base + "_graphs.csv")


    base = base_options[2]
    #import_graphs("basic/" +base + "_graphs.csv")
    #import_graphs("100s/" + base + "_graphs.csv")
    #import_graphs("100s v2/" +base + "_graphs.csv")
    #import_graphs("high density/" +base + "_graphs.csv")
    #import_graphs("lower density/" +base + "_graphs.csv")
    
    #base = base_options[4]
    #import_graphs("dense_graphs.csv")
    #import_graphs("sparse_graphs.csv")
    
