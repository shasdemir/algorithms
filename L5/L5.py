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


def shortest_dist_node(dist):
    return min(dist.items(), key=lambda tup: tup[1])[0]  # Theta(n)


def dijkstra(G, v):
    dist_so_far_heap = NamedHeap(heap_list=[(0, v)])
    final_dist = {}

    while len(final_dist) < len(G):  # assuming connected graph
        w_dist, w = dist_so_far_heap.pop_minimum()

        # lock it down
        final_dist[w] = w_dist

        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far_heap.value_map:
                    dist_so_far_heap.insert_value(new_name=x, new_value=final_dist[w] + G[w][x])
                elif final_dist[w] + G[w][x] < dist_so_far_heap.get_value(x):
                    dist_so_far_heap.decrease_value(name=x, new_value=final_dist[w] + G[w][x])

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


class NamedHeap(object):
    def __init__(self, heap_list):
        """ heap_list is a list of tuples (no, name)
            value_map maps item names to their values on the heap
            position_map maps item names to their positions on the heap_list. """

        self.heap_list = heap_list
        self.value_map = {item[1]: item[0] for item in heap_list}

        self.position_map = {}
        for k in xrange(len(heap_list)):
            self.position_map[self.heap_list[k][1]] = k

        self.left = lambda i: 2 * i + 1
        self.right = lambda i: 2 * i + 2
        self.parent = lambda i: (i - 1) // 2
        self.is_root = lambda i: i == 0
        self.is_leaf = lambda L, i: self.right(i) >= len(L) and self.left(i) >= len(L)
        self.one_child = lambda L, i: self.right(i) == len(L)  # the node only has a left child

        self.__build_heap__()

    def __normalized_index__(self, i):
        """ Return non-negative list indices. """

        return i + len(self.heap_list) if i < 0 else i

    def __swap__(self, p1, p2):
        """ Swap elements of heap_list at positions p1 and p2. """

        p1, p2 = (self.__normalized_index__(k) for k in (p1, p2))

        self.heap_list[p1], self.heap_list[p2] = self.heap_list[p2], self.heap_list[p1]

        self.position_map[self.heap_list[p1][1]], self.position_map[self.heap_list[p2][1]] = \
            self.position_map[self.heap_list[p2][1]], self.position_map[self.heap_list[p1][1]]

    def __up_heapify__(self, i):
        i = self.__normalized_index__(i)

        if not (i == 0 or self.heap_list[self.parent(i)] <= self.heap_list[i]):
            self.__swap__(self.parent(i), i)
            self.__up_heapify__(self.parent(i))

    def __down_heapify__(self, i):
        """ Call this if the heap rooted at i satisfies the heap property except perhaps i to its immediate
        children. """

        i = self.__normalized_index__(i)

        if self.is_leaf(self.heap_list, i):
            return

        if self.one_child(self.heap_list, i):
            if self.heap_list[i] > self.heap_list[self.left(i)]:
                self.__swap__(i, self.left(i))
            return

        # i has two children, check heap property
        if min(self.heap_list[self.left(i)], self.heap_list[self.right(i)]) >= self.heap_list[i]:
            return

        # if that fails, swap with the smaller child, and recurse on its children
        if self.heap_list[self.left(i)] < self.heap_list[self.right(i)]:
            self.__swap__(i, self.left(i))
            self.__down_heapify__(self.left(i))
        else:
            self.__swap__(i, self.right(i))
            self.__down_heapify__(self.right(i))

    def __build_heap__(self):
        for i in range(len(self.heap_list)-1, -1, -1):
            self.__down_heapify__(i)

    def __remove_min__(self):
        del self.value_map[self.heap_list[0][1]]
        del self.position_map[self.heap_list[0][1]]

        if len(self.heap_list) == 1:
            self.heap_list = []
        else:
            self.heap_list[0] = self.heap_list.pop()

            self.position_map[self.heap_list[0][1]] = 0

            self.__down_heapify__(0)

    def get_value(self, name):
        return self.value_map[name]

    def get_minimum(self):
        return self.heap_list[0]

    def shortest_dist_node(self):
        return self.get_minimum()

    def pop_minimum(self):
        minimum = self.get_minimum()
        self.__remove_min__()
        return minimum

    def insert_value(self, new_name, new_value):
        self.heap_list.append((new_value, new_name))
        self.value_map[new_name] = new_value
        self.position_map[new_name] = len(self.heap_list) - 1

        self.__up_heapify__(-1)

    def decrease_value(self, name, new_value):
        """ Decrease the value of already existing name. """

        index = self.position_map[name]
        self.heap_list[index] = (new_value, name)
        self.value_map[name] = new_value

        self.__up_heapify__(index)


def path(G, v1, v2):
    open_list = [v1]
    path_from_start = {v1: [v1]}

    if v1 == v2:
        return path_from_start[v1]

    while open_list:
        current = open_list.pop(0)  # bfs

        for neighbor in G[current]:
            if neighbor not in path_from_start:
                path_from_start[neighbor] = path_from_start[current] + [neighbor]
                if neighbor == v2:
                    return path_from_start[v2]
                open_list.append(neighbor)
    return False


def bfs_allpaths(G, v):
    open_list = [v]
    path_from_start = {v: [v]}

    while open_list:
        current = open_list.pop(0)  # bfs

        for neighbor in G[current]:
            if neighbor not in path_from_start:
                path_from_start[neighbor] = path_from_start[current] + [neighbor]
                open_list.append(neighbor)
    return path_from_start


def dijkstra_paths(G, v):
    dist_path_so_far = [(0, v, [v])]
    dsf_values_map = {v: 0}
    final_dist_path = {}

    while len(dist_path_so_far) > 0:  # assuming connected graph
        w_dist, w, w_path = hq.heappop(dist_path_so_far)

        if w in final_dist_path:
            continue

        del dsf_values_map[w]  # lock it down
        final_dist_path[w] = (w_dist, w_path)

        for x in G[w]:
            if x not in final_dist_path:
                route_dist = final_dist_path[w][0] + G[w][x]
                route_path = final_dist_path[w][1] + [x]

                if x not in dsf_values_map or route_dist < dsf_values_map[x]:
                    hq.heappush(dist_path_so_far, (route_dist, x, route_path))
                    dsf_values_map[x] = route_dist

    # erase distances from final_dist_path
    for hero in final_dist_path:
        final_dist_path[hero] = final_dist_path[hero][1]
    return final_dist_path