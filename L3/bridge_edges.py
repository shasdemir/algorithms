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


def create_uncolored_tree(G):
    spanning_tree = {}

    visited = set()
    open_list = [G.keys()[0]]

    while open_list:
        current = open_list.pop(0)

        if current not in spanning_tree:
            spanning_tree[current] = {}

        for neighbor in G[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                open_list.append(neighbor)

                make_link(G=spanning_tree, node1=current, node2=neighbor)

    return spanning_tree


def create_rooted_spanning_tree(G):
    spanning_tree = create_uncolored_tree(G)
    colored_tree = {}

    for node in G:
        for nbor in G[node]:
            if nbor in spanning_tree[node]:
                make_colored_link(G=colored_tree, node1=node, node2=nbor, color='green')
            else:
                make_colored_link(G=colored_tree, node1=node, node2=nbor, color='red')

    return colored_tree