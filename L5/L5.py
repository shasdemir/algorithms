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
    left = lambda i: 2 * i + 1
    right = lambda i: 2 * i + 2
    parent = lambda i: (i - 1) // 2
    is_root = lambda i: i == 0
    is_leaf = lambda L, i: right(i) > len(L) and left(i) > len(L)
    one_child = lambda L, i: right(i) == len(L)  # the node only has a left child

    def __init__(self, heap_list, heaped_names):
        self.heap_list = heap_list
        self.heaped_names = heaped_names
        self.name_mapping = dict(zip(heaped_names, heap_list))

        self.build_heap(self, 0)

    def __up_heapify__(self, i):
        if not (i == 0 or self.heap_list[parent(i)] <= self.heap_list[i]):
            self.heap_list[parent(i)], self.heap_list[i] = self.heap_list[i], self.heap_list[parent(i)]
            self.heaped_names[parent(i)], self.heaped_names[i] = self.heaped_names[i], self.heaped_names[parent(i)]

            self.__up_heapify__(parent(i))

    def get_value(self, name):
        return self.name_mapping[name]

    def get_minimum(self):
        return self.heaped_names[0], self.heap_list[0]

    #def add_value(self, new_name, new_value):

