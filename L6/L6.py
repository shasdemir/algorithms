def long_and_simple_path(G,u,v,l):
    """
    G: Graph
    u: starting node
    v: ending node
    l: minimum length of path
    """

    if not long_and_simple_decision(G,u,v,l):
        return False
    # Otherwise, build and return the path

    if l <= 2 and u in G[v]:
        return [u, v]

    reachable_neighbors = [nbor for nbor in G[v] if long_and_simple_decision(G, u, nbor, l-1)]

    if not reachable_neighbors:
        return False

    paths_to_neighbors = [(r_nbor, long_and_simple_path(G, u, r_nbor, l-1)) for r_nbor in reachable_neighbors]

    noncyclic_paths = [(nbor, path) for nbor, path in paths_to_neighbors if v not in path]

    one_noncyclic_path = noncyclic_paths[0][1]

    return one_noncyclic_path + [v]


def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G


def all_perms(seq):
    if len(seq) == 0: return [[]]
    if len(seq) == 1: return [seq, []]
    most = all_perms(seq[1:])
    first = seq[0]
    rest = []
    for perm in most:
        for i in range(len(perm)+1):
            rest.append(perm[0:i] + [first] + perm[i:])
    return most + rest


def check_path(G,path):
    for i in range(len(path)-1):
        if path[i+1] not in G[path[i]]: return False
    return True


def long_and_simple_decision(G,u,v,l):
    if l == 0:
        return long_and_simple_decision(G, u, v, 1)
    n = len(G)
    perms = all_perms(G.keys())
    for perm in perms:
        if not perm:
            continue
        # check path
        if (len(perm) >= l and check_path(G,perm) and perm[0] == u
            and perm[-1] == v):
            return True
    return False


flights = [(1,2),(1,3),(2,3),(2,6),(2,4),(2,5),(3,6),(4,5)]
G = {}
for (x, y) in flights: make_link(G, x, y)