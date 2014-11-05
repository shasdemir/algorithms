from L3 import *


def make_colored_link(G, node1, node2, color):
    if node1 not in G:
        G[node1] = {node2: color}
    elif node2 not in G[node1]:
        G[node1][node2] = color

    if node2 not in G:
        G[node2] = {node1: color}
    elif node1 not in G[node2]:
        G[node2][node1] = color

    return G


def create_uncolored_tree(G, root):
    spanning_tree = {}

    open_list = [root]
    checked = {open_list[0]}

    while open_list:
        current = open_list.pop(0)

        if current not in spanning_tree:
            spanning_tree[current] = {}

        for neighbor in G[current]:
            if neighbor not in checked:
                checked.add(neighbor)
                open_list.append(neighbor)

                make_link(G=spanning_tree, node1=current, node2=neighbor)

    return spanning_tree


def create_rooted_spanning_tree(G, root):
    spanning_tree = create_uncolored_tree(G, root)

    colored_tree = {}
    for node in G:
        for nbor in G[node]:
            if nbor in spanning_tree[node]:
                make_colored_link(G=colored_tree, node1=node, node2=nbor, color='green')
            else:
                make_colored_link(G=colored_tree, node1=node, node2=nbor, color='red')

    return colored_tree


def post_order(graph, root):
    """ Return mapping between nodes in graph and their post-order. """

    def calc_po(spanning_tree, root, node, po_counter, po):
        children = direct_children(spanning_tree, root, node)

        for child in children:
            po_counter, po = calc_po(spanning_tree, root, child, po_counter, po)

        po_counter += 1
        po[node] = po_counter
        return po_counter, po

    spanning_tree = create_uncolored_tree(graph, root)
    po = {}
    po_counter = 0
    calc_po(spanning_tree, root, root, po_counter, po)

    return po


def direct_children(spanning_tree, root, node):
    """ Return the list of direct children of node node, in a tree with root root."""

    neighbors = spanning_tree[node].keys()

    if node == root:
        return neighbors

    path_to_node = path(spanning_tree, root, node)

    return [node for node in neighbors if node not in path_to_node]


def list_descendants(spanning_tree, root, node):
    """ List all descendants of node, including itself. """

    spanning_tree = create_uncolored_tree(spanning_tree, root)  # we only need green connections

    all_nodes = spanning_tree.keys()

    if node == root:
        return all_nodes

    path_to_node = path(spanning_tree, root, node)
    dist_to_node = len(path_to_node)

    return [other for other in all_nodes if path(spanning_tree, root, other)[:dist_to_node] == path_to_node]


def number_of_descendants(spanning_tree, root):
    """ Return the mapping between the nodes of spanning_tree and number of their descendants. """

    return {node: len(list_descendants(spanning_tree, root, node)) for node in spanning_tree}


def find_search_set(spanning_tree, root, node):
    """ Return the set of nodes to compare post_order values to calculate L (red)
    number for the node. """

    descendants = list_descendants(spanning_tree, root, node)

    # find points reachable from the descendants with a single red line
    reachable = set()
    for desc in descendants:
        for nbor in spanning_tree[desc]:
            if spanning_tree[desc][nbor] == 'red':
                reachable.add(nbor)

    return reachable.union(set(descendants))


def lowest_post_order(spanning_tree, root, po):
    lpo = {}

    for node in po:
        search_set = find_search_set(spanning_tree, root, node)
        lpo[node] = min([po[s_node] for s_node in search_set])

    return lpo


def highest_post_order(spanning_tree, root, po):
    hpo = {}

    for node in po:
        search_set = find_search_set(spanning_tree, root, node)
        hpo[node] = max([po[s_node] for s_node in search_set])

    return hpo


def check_edge_end(H, black, L, nd):
    """ Given highest po H,
    po black,
    lowest po L,
    number of descendants nd, check if this node is the end of a bridge edge. """

    return (H <= black) and (L > (black - nd))