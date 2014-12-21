def long_and_simple_path_try(G,u,v,l):
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


def long_and_simple_path(G,u,v,l):  # just try all permutations :p
    if not long_and_simple_decision(G,u,v,l):
        return False

    no_cycles = lambda path: len(path) == len(set(path))

    n = len(G)
    perms = all_perms(G.keys())
    for perm in perms:
        if not perm:
            continue
        # check path
        if (len(perm) == l and check_path(G,perm) and perm[0] == u
            and perm[-1] == v and no_cycles(perm)):
            return perm
    return False


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


# if cert a k-coloring of G?
#   colors in {0, ..., k-1}
def verify(G, cert, k):
    for node in G:
        for nbor in G[node]:
            if cert[nbor] == cert[node] or cert[nbor] >= k:
                return False
    return True


def invert(H):
    """ Invert graph. """

    # strategy: create a full graph, except where links are in H
    H_inv = {}

    for node1 in H:
        for node2 in H:
            if node2 != node1 and node2 not in H[node1]:
                make_link(H_inv, node1, node2)

    # add unconnected nodes
    for node in H:
        if node not in H_inv:
            H_inv[node] = {}

    return H_inv


# This function should use the k_clique_decision function
# to solve the independent set decision problem
def independent_set_decision(H, s):
    H_inv = invert(H)

    return k_clique_decision(H_inv, s)


def remove_node(G, node):
    """ Return a new graph with :node removed from G. """

    import copy

    G_minus = copy.deepcopy(G)
    for nbor in G[node]:
        break_link(G_minus, node, nbor)

    return G_minus


def k_clique(G, k):
    if not k_clique_decision(G, k):
        return False

    import copy
    result = copy.deepcopy(G)

    for node in G:
        G_minus = remove_node(result, node)

        if k_clique_decision(G_minus, k):
            result = G_minus

    # if there is more than a single node in result, remove unconnected nodes
    node_list = result.keys()
    if len(node_list) > 1:
        for node in node_list:
            if result[node] == {}:
                del result[node]
    return result.keys()