import heapq as hq


def dijkstra_old(G, v):
    dist_so_far = {v: 0}
    final_dist = {}

    while len(final_dist) < len(G):  # assuming connected graph
        w = shortest_dist_node(dist_so_far)

        # lock it down
        final_dist[w] = dist_so_far[w]
        del dist_so_far[w]

        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far:
                    dist_so_far[x] = final_dist[w] + G[w][x]
                elif final_dist[w] + G[w][x] < dist_so_far[x]:
                    dist_so_far[x] = final_dist[w] + G[w][x]

    return final_dist


def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += w
    return G


def dijkstra(G, v):
    dist_so_far = [(0, v)]
    dsf_values_map = {v: 0}
    final_dist = {}

    while len(final_dist) < len(G):  # assuming connected graph
        w_dist, w = hq.heappop(dist_so_far)
        del dsf_values_map[w[0]]

        # lock it down
        final_dist[w] = w_dist

        for x in G[w]:
            if x not in final_dist:
                if x not in dsf_values_map:
                    hq.heappush(dist_so_far, (final_dist[w] + G[w][x], x))
                    dsf_values_map[x] = final_dist[w] + G[w][x]

                elif final_dist[w] + G[w][x] < dsf_values_map[x]:
                    for k in dist_so_far:
                        if k[1] == x:
                            dist_so_far[k] = (final_dist[w] + G[w][x], x)
                    hq.heapify(dist_so_far)
                    dsf_values_map[x] = final_dist[w] + G[w][x]

    return final_dist