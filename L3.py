def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G


flights = [("ORD", "SEA"), ("ORD", "LAX"), ('ORD', 'DFW'), ('ORD', 'PIT'),
           ('SEA', 'LAX'), ('LAX', 'DFW'), ('ATL', 'PIT'), ('ATL', 'RDU'),
           ('RDU', 'PHL'), ('PIT', 'PHL'), ('PHL', 'PVD')]


def clustering_coefficient(G, v):
    neighbors = G[v].keys()
    if len(neighbors) == 1:
        return 0
    links = 0
    for w in neighbors:
        for u in neighbors:
            if u in G[w]:links += 0.5
    return 2.0 * links / (len(neighbors) * (len(neighbors)-1))


def cc_G():
    G = {}
    for (x, y) in flights:
        make_link(G, x, y)

    print clustering_coefficient(G,"ORD")

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


def remove_edge(G, edge):
    for endp in edge:
        G[edge[endp]] -= 1
        if G[edge[endp]] == 0:
            del G[edge[endp]]


def is_bridge_edge(G, edge):
    """ Given a connected graph G and edge = (v1, v2) in G, return if G is a bridge edge. """

    # strategy: remove edge from the graph, and count the number of connected components. If 2, edge was a bridge edge.
    # in either case, put edge back into the graph.
