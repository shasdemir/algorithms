import copy


def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G


def graph_from_edge_list(e_list):
    graph = {}
    for edge in e_list:
        make_link(graph, *edge)
    return graph


def clustering_coefficient(G, v):
    neighbors = G[v].keys()
    if len(neighbors) == 1:
        return 0
    links = 0
    for w in neighbors:
        for u in neighbors:
            if u in G[w]:links += 0.5
    return 2.0 * links / (len(neighbors) * (len(neighbors)-1))


def cc_G(G):
    print clustering_coefficient(G, "ORD")

    total = 0
    for v in G.keys():
        total += clustering_coefficient(G, v)

    print total / len(G)


def mark_component(G, node, marked):
    marked[node] = True
    total_marked = 1
    for neighbor in G[node]:
        if neighbor not in marked:
            total_marked += mark_component(G, neighbor, marked)
    return total_marked


def mark_component_nr(G, node, marked):
    marked[node] = True
    open_list = [node]

    current = open_list.pop(0)
    for neighbor in G[current]:
        if neighbor not in marked:
            marked[neighbor] = True
            open_list.append(neighbor)
    return len(marked)


def list_component_sizes(G):
    marked = {}
    for node in G:
        if node not in marked:
            print "Component containing " + str(node) + ": " + str(mark_component(G, node, marked))


def check_connection(G, v1, v2):
    marked = {}
    mark_component(G, v1, marked)

    return v2 in marked


def path(G, v1, v2):
    path_from_start = {}

    open_list = [v1]
    path_from_start[v1] = [v1]

    while open_list:
        current = open_list.pop(0)  # bfs

        for neighbor in G[current]:
            if neighbor not in path_from_start:
                path_from_start[neighbor] = path_from_start[current] + [neighbor]
                if neighbor == v2:
                    return path_from_start[v2]
                open_list.append(neighbor)
    return False


def centrality(G, v):
    path_lengths = [len(path(G, v, other))-1 for other in G if other != v]
    return sum(path_lengths) / (len(path_lengths)-1.)


def count_connected_components(G):
    n_components = 0
    marked = {}
    for node in G:
        if node not in marked:
            mark_component_nr(G, node, marked)
            n_components += 1
    return n_components


def remove_link(G, v1, v2):
    for points in (v1, v2), (v2, v1):
        G[points[0]][points[1]] -= 1
        if G[points[0]][points[1]] == 0:
            del G[points[0]][points[1]]


def remove_unconnected_nodes(G):
    nodes = G.keys()
    for node in nodes:
        if not G[node]:
            del G[node]


def is_bridge_edge(G, v1, v2):
    """ Given a connected graph G and edge = (v1, v2) in G, return if G is a bridge edge. """

    # strategy: remove edge from the graph, and count the number of connected components. If 2, edge was a bridge edge.
    # in either case, put edge back into the graph.
    remove_link(G, v1, v2)
    result = count_connected_components(G) == 2
    make_link(G, v1, v2)

    return result


def list_edges(G):
    """ Return the edges in graph G as a counter of tuples. """

    def grow_edge_counter(counter, edge):
        for rep in edge, edge[::-1]:
            if rep in counter:
                counter[rep] += 1
            else:
                counter[rep] = 1
        if edge[::-1] in counter:
            del counter[edge]

    edge_counter = {}
    for node in G:
        for end in G[node]:
            grow_edge_counter(edge_counter, (node, end))

    return edge_counter


def list_bridge_edges(G):
    """ Return a list of bridge edges in G. """

    all_edges = list_edges(G)

    return [edge for edge in all_edges if is_bridge_edge(G, *edge)]


def remove_node(G, node):
    """ Remove a node and all edges connected to it from the graph G. """

    for neighbor in G[node]:
        del G[neighbor][node]
    del G[node]

    return G


def reset_G():
    flights = [("ORD", "SEA"), ("ORD", "LAX"), ('ORD', 'DFW'), ('ORD', 'PIT'),
               ('SEA', 'LAX'), ('LAX', 'DFW'), ('ATL', 'PIT'), ('ATL', 'RDU'),
               ('RDU', 'PHL'), ('PIT', 'PHL'), ('PHL', 'PVD')]
    G = {}
    for (x, y) in flights:
        make_link(G, x, y)


def edges_to_nbors(G, node):
    """ Return the list of all edges connected to node. """

    edges = []
    for nbor in G[node]:
        edges += [(node, nbor)] * G[node][nbor]

    return edges


def fleury(G):
    """ Implement Fleury's Algorithm of finding Eulerian Tours of graph G as descibed in
    http://www.ctl.ua.edu/math103/euler/ifagraph.htm. Return list of nodes visited. """

    graph = copy.deepcopy(G)

    remaining_edges = set(list_edges(graph))
    path = [graph.keys()[0]]  # start from a random point

    while remaining_edges:
        graph_of_remaining_edges = graph_from_edge_list(remaining_edges)

        possible_edges_to_go = edges_to_nbors(graph_of_remaining_edges, path[-1])

        is_bridge_of_untravelled = {edge: is_bridge_edge(graph_of_remaining_edges, *edge)
                                    for edge in possible_edges_to_go}

        edge_taken = None
        if is_bridge_of_untravelled == {edge: True for edge in is_bridge_of_untravelled}:
            edge_taken = is_bridge_of_untravelled.keys()[0]
        else:
            edge_taken = [edge for edge in possible_edges_to_go if is_bridge_of_untravelled[edge] is False][0]
        if not edge_taken:
            raise Exception("Can't find Eulerian path.")

        remaining_edges -= set(edge_taken)

        path.append(edge_taken[1] if path[-1] == edge_taken[0] else edge_taken[0])

    return path