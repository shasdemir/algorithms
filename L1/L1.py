def russian(a, b):
    x = a; y = b
    z = 0
    while x > 0:
        if x % 2 == 1: z = z + y
        y = y << 1
        x = x >> 1
    return z


def countdown(x):
    y = 0
    while x > 0:
        x = x - 5
        y = y + 1
    print y
    return y


def time(n):
    """ Return the number of steps necessary to calculate `print countdown(n)`"""

    steps = 3 + 2 * (n / 5 + (n % 5 != 0))
    return steps


def rec_russian(a, b):
    if a == 0: return 0
    if a % 2 == 0: return rec_russian(a/2, b) * 2
    return rec_russian((a-1)/2, b) * 2


def create_tour(nodes):
    """Write a function, `create_tour` that takes as input a list of nodes and outputs a list of tuples representing
    edges between nodes that have an Eulerian tour. """

    # I'll just make a circle
    circle = []

    for node_no in range(len(nodes)-1):
        circle.append((nodes[node_no], nodes[node_no+1]))
    circle.append((nodes[-1], nodes[0]))

    return circle


def count(n):
    """ How many ops for clique(n) """

    return ((n**2) / 2.) + (n/2.) + 2


def find_eulerian_tour_wrong(graph):
    def find_accessible_neighbors(edge_list, node):
        nbors = set()
        for link in edge_list:
            if link[0] == node:
                nbors.add(link[1])
            elif link[1] == node:
                nbors.add(link[0])
        return nbors

    # only visit a node if you can get out, unless it is the last move
    def decide_the_next_move(edge_list, position):
        """ return the link taken """

        if len(edge_list) == 1:
            return edge_list[-1]
        else:
            for link in edge_list:
                if position in link:
                    other = link[0] if position == link[1] else link[1]
                    if len(find_accessible_neighbors(edge_list, other)) > 1:
                        return link

    new_point = graph[0][0]
    path = [new_point]
    while graph:
        edge_taken = decide_the_next_move(edge_list=graph, position=new_point)

        new_point = edge_taken[1] if edge_taken[0] == new_point else edge_taken[0]
        path.append(new_point)

        for k in range(len(graph)):
            if graph[k] == edge_taken:
                graph.pop(k)
            break

    return path


def is_eulerian_tour(edge_list, path):
    """ Check if path is an eulerian tour through the edge_list. """

    # checks:
    # 1. each successive point is accessible
    # 3. all links are used, no extra link made up
    # 4. we end up where we began

    if path[0] != path[-1]:  # 4:
        return False

    current_edge_list = []
    for edge in edge_list:
        current_edge_list.append(edge)

    for k in range(len(path)-1):
        if (path[k], path[k+1]) not in current_edge_list and (path[k+1], path[k]) not in current_edge_list:
            return False
        else:

            for i in range(len(edge_list)):
                if current_edge_list[i] == (path[k], path[k+1]) or current_edge_list[i] == (path[k+1], path[k]):
                    current_edge_list.pop(i)
                    break

    return not current_edge_list


def find_eulerian_tour(edge_list):
    """ Try random paths until an Eulerian path is found. """

    import random

    found = False
    while not found:
        current_node = edge_list[0][0]
        path = [current_node]

        remaining_edges = []
        for edge in edge_list:
            remaining_edges.append(edge)

        while remaining_edges:
            possible_edges = [edge for edge in remaining_edges if current_node in edge]

            if possible_edges:
                edge_taken = random.choice(possible_edges)
            else:
                break

            path.append(edge_taken[0] if edge_taken[1] == current_node else edge_taken[1])

            current_node = path[-1]

            for k in range(len(remaining_edges)):
                if remaining_edges[k] == edge_taken:
                    remaining_edges.pop(k)
                    break

        if is_eulerian_tour(edge_list, path):
            return path

