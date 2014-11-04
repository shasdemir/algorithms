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

    def calc_po(spanning_tree, root, po_counter):
        children = direct_children(spanning_tree, root)

        for child in children:
            calc_po(spanning_tree, child, po_counter)

        po_counter += 1
        po[root] = po_counter

    spanning_tree = create_uncolored_tree(graph, root)
    po = {}
    po_counter = 0

    return calc_po(spanning_tree, root, po_counter)