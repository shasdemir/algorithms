from L3 import *


def make_colored_link(G, node1, node2, color=1):
    if node1 not in G:
        G[node1] = {node2: color}
    elif node2 not in G[node1]:
        G[node1][node2] = color

    if node2 not in G:
        G[node2] = {node1: color}
    elif node1 not in G[node2]:
        G[node2][node1] = color

    return G


# def create_rooted_spanning_tree(G):
#     colored = {}

