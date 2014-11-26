def dijkstra(G, v):
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


def shortest_dist_node(dist):
    return min(dist.items(), key=lambda tup: tup[1])[0]  # Theta(n)


class NamedHeap(object):
    def __init__(self, heap_list, heaped_names):
        self.heap_list = heap_list
        self.heaped_names = heaped_names
        self.name_mapping = dict(zip(heaped_names, heap_list))

        self.down_heapify(self, 0)

    def get_value(self, name):
        return self.name_mapping[name]

    def get_minimum(self):
        return self.heaped_names[0], self.heap_list[0]


