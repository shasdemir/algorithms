# graphs are represented as dict of dicts
# a connection appears 2 times for both ends


def make_link(graph, node_1, node_2):
    if node_1 not in graph:
        graph[node_1] = {}
    graph[node_1][node_2] = 1

    if node_2 not in graph:
        graph[node_2] = {}
    graph[node_2][node_1] = 1

    return graph


def new_ring(n):
    ring = {}

    for k in range(n):
        ring = make_link(ring, k, (k+1) % n)

    return ring


def count_nodes(graph):
    return len(graph.keys())


def count_links(graph):
    return sum([len(graph[node]) for node in graph]) / 2