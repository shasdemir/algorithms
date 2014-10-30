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
    distance_from_start = {}
    path_from_start = {}

    open_list = [v1]
    distance_from_start[v1] = 0
    path_from_start[v1] = [v1]

    while open_list:
        current = open_list[0]  # bfs
        open_list.pop(0)

        for neighbor in G[current]:
            if neighbor not in distance_from_start:
                distance_from_start[neighbor] = distance_from_start[current] + 1
                if neighbor == v2:
                    return distance_from_start[v2]
                open_list.append(neighbor)
    return False