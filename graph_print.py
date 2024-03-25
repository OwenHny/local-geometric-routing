import matplotlib.pyplot as plt

def plot_graph(colour, graph):
    plt.figure(figsize=(20, 20))
    for point, neighbors in graph.items():
        x, y = point
        if point in colour:
            plt.plot(x, y, 'ro')  # Plot the point
        else:
            plt.plot(x, y, 'bo')  # Plot the point
        
        # Plot edges to neighbors
        for neighbor in neighbors:
            nx, ny = neighbor
            plt.plot([x, nx], [y, ny], 'b-')
    
    plt.title('Graph')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.savefig("plot.png")

# Example usage:
#graph = {(4, 3): [(10, 3), (0, 3)], (23, 16): [(21, 22), (23, 13)], (21, 22): [(23, 16), (13, 19), (23, 24)], (23, 13): [(25, 11), (18, 7), (23, 16)], (10, 3): [(11, 1), (11, 3), (4, 3)], (5, 22): [(8, 16), (7, 25), (1, 18), (13, 19), (1, 24)], (1, 18): [(8, 16), (1, 16), (5, 22), (1, 24)], (18, 7): [(25, 11), (20, 1), (15, 7), (23, 13)], (1, 24): [(5, 22), (1, 18)], (20, 1): [(11, 1), (18, 7), (11, 3)], (7, 25): [(5, 22), (13, 19), (10, 16)], (23, 24): [(21, 22)], (11, 1): [(10, 3), (20, 1), (11, 3)], (15, 7): [(18, 7), (11, 3)], (13, 19): [(7, 25), (21, 22), (5, 22), (10, 16)], (11, 3): [(10, 3), (11, 1), (20, 1), (15, 7)], (0, 3): [(4, 3)], (8, 16): [(1, 16), (5, 22), (1, 18), (10, 16)], (10, 16): [(8, 16), (7, 25), (13, 19)], (1, 16): [(8, 16), (1, 18)], (25, 11): [(18, 7), (23, 13)]}
