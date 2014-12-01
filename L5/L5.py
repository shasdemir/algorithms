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
        """ Swap elements of both heap_list and heaped_names at positions p1 and p2. """

        p1, p2 = (self.__normalized_index__(k) for k in (p1, p2))

        self.heap_list[p1], self.heap_list[p2] = self.heap_list[p2], self.heap_list[p1]
        self.heaped_names[p1], self.heaped_names[p2] = self.heaped_names[p2], self.heaped_names[p1]

    def __up_heapify__(self, i):
        i = self.__normalized_index__(i)

        if not (i == 0 or self.heap_list[self.parent(i)] <= self.heap_list[i]):
            self.__swap__(self.parent(i), i)
            self.__up_heapify__(self.parent(i))

    def __down_heapify__(self, i):
        """ Call this if the heap rooted at i satisfies the heap property except perhaps i to its immediate
        children. """

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
        del self.name_mapping[self.heaped_names[0]]
        self.heap_list[0] = self.heap_list.pop()
        self.heaped_names[0] = self.heaped_names.pop()

        self.__down_heapify__(0)

    def get_value(self, name):
        return self.name_mapping[name]

    def get_minimum(self):
        return self.heaped_names[0], self.heap_list[0]

    def pop_minimum(self):
        minimum = self.get_minimum()
        self.__remove_min__()
        return minimum

    def insert_value(self, new_name, new_value):
        self.heaped_names.append(new_name)
        self.heap_list.append(new_value)
        self.name_mapping[new_name] = new_value

        self.__up_heapify__(len(self.heap_list)-1)
